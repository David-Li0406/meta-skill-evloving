/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 watch command - Live development with auto-deploy on save
 *
 * Usage:
 *   e3 watch . dev ./src/my-package.ts
 *   e3 watch . dev ./src/my-package.ts --start
 *   e3 watch . dev ./src/my-package.ts --start --abort-on-change
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import * as os from 'node:os';
import * as esbuild from 'esbuild';
import e3 from '@elaraai/e3';
import type { PackageDef } from '@elaraai/e3';
import {
  packageImport,
  workspaceCreate,
  workspaceGetState,
  workspaceDeploy,
  dataflowExecute,
  DataflowAbortedError,
  LocalStorage,
  type TaskExecutionResult,
} from '@elaraai/e3-core';
import { resolveRepo, formatError } from '../utils.js';

interface WatchOptions {
  start?: boolean;
  concurrency?: string;
  abortOnChange?: boolean;
}

/**
 * Result of loading a package file, includes watched dependencies
 */
interface LoadResult {
  pkg: PackageDef<Record<string, unknown>>;
  watchedFiles: string[];
}

/**
 * Load and execute a TypeScript file using esbuild for bundling.
 * esbuild automatically finds and uses the nearest tsconfig.json.
 * Returns both the package and list of files to watch.
 */
async function loadPackageFile(filePath: string): Promise<LoadResult> {
  const absolutePath = path.resolve(filePath);

  // Bundle with esbuild - handles multi-file TS, ESM packages, and tsconfig automatically
  const result = esbuild.buildSync({
    entryPoints: [absolutePath],
    bundle: true,
    platform: 'node',
    format: 'esm',  // ESM output for ESM-only packages like @elaraai/e3
    write: false,
    metafile: true,
    external: ['@elaraai/*'],
    logLevel: 'silent',
  });

  const jsCode = result.outputFiles?.[0]?.text;
  if (!jsCode) {
    throw new Error(`esbuild produced no output for ${filePath}`);
  }

  // Extract list of bundled source files for watching
  // esbuild metafile paths are relative to cwd
  const watchedFiles = result.metafile
    ? Object.keys(result.metafile.inputs)
        .map(f => path.resolve(f))  // Resolve relative to cwd
        .filter(f => !f.includes('node_modules'))
    : [absolutePath];

  // Write bundle to temp file in project directory and import it dynamically
  // Must be in project dir so node_modules resolution works for external packages
  // This avoids cross-realm instanceof issues that occur with vm.createContext
  const tempDir = path.join(path.dirname(absolutePath), 'node_modules', '.cache', 'e3');
  fs.mkdirSync(tempDir, { recursive: true });
  const tempFile = path.join(tempDir, `bundle-${Date.now()}.mjs`);
  let defaultExport: unknown;
  try {
    fs.writeFileSync(tempFile, jsCode);
    // Use dynamic import for ESM
    // Add cache-busting query param to avoid Node's ESM cache
    const moduleExports = await import(`${tempFile}?t=${Date.now()}`) as Record<string, unknown>;
    defaultExport = moduleExports.default ?? moduleExports;
  } catch (err) {
    if (err instanceof Error && err.stack) {
      console.error('Stack trace:', err.stack);
    }
    throw new Error(`Failed to execute ${path.basename(filePath)}: ${err instanceof Error ? err.message : String(err)}`);
  } finally {
    try {
      fs.unlinkSync(tempFile);
    } catch {
      // Ignore cleanup errors
    }
  }

  // Validate it's a PackageDef
  if (!defaultExport || (defaultExport as { kind?: string }).kind !== 'package') {
    throw new Error(
      `Default export must be a PackageDef (created with e3.package()).\n\n` +
      `Expected:\n` +
      `  const pkg = e3.package('name', '1.0.0', ...tasks);\n` +
      `  export default pkg;\n\n` +
      `Got: ${typeof defaultExport}${(defaultExport as { kind?: string }).kind ? ` with kind="${(defaultExport as { kind?: string }).kind}"` : ''}`
    );
  }

  return {
    pkg: defaultExport as PackageDef<Record<string, unknown>>,
    watchedFiles,
  };
}

/**
 * Format timestamp for log output
 */
function timestamp(): string {
  return new Date().toLocaleTimeString('en-US', { hour12: false });
}

/**
 * Watch a TypeScript file and auto-deploy on changes
 */
export async function watchCommand(
  repoArg: string,
  workspace: string,
  sourceFile: string,
  options: WatchOptions
): Promise<void> {
  const repoPath = resolveRepo(repoArg);
  const absoluteSourcePath = path.resolve(sourceFile);
  const concurrency = options.concurrency ? parseInt(options.concurrency, 10) : 4;

  // Validate source file exists
  if (!fs.existsSync(absoluteSourcePath)) {
    console.error(`Error: Source file not found: ${absoluteSourcePath}`);
    process.exit(1);
  }

  console.log(`Watching: ${sourceFile}`);
  console.log(`Repository: ${repoPath}`);
  console.log(`Target workspace: ${workspace}`);
  if (options.start) {
    console.log(`Auto-start: enabled (concurrency: ${concurrency})`);
    if (options.abortOnChange) {
      console.log(`Abort on change: enabled`);
    }
  }
  console.log('');

  // State for managing concurrent execution
  let isExecuting = false;
  let pendingReload = false;
  let currentAbortController: AbortController | null = null;

  /**
   * Load, export, import, and deploy the package
   */
  async function deployPackage(): Promise<{ name: string; version: string; watchedFiles: string[] } | null> {
    // Load package from TypeScript file
    let pkg: PackageDef<Record<string, unknown>>;
    let watchedFiles: string[];
    try {
      const result = await loadPackageFile(absoluteSourcePath);
      pkg = result.pkg;
      watchedFiles = result.watchedFiles;
      console.log(`[${timestamp()}] Loaded: ${pkg.name}@${pkg.version} (${watchedFiles.length} files)`);
    } catch (err) {
      console.log(`[${timestamp()}] Error loading package:`);
      console.log(`  ${err instanceof Error ? err.message : String(err)}`);
      return null;
    }

    // Export to temp zip
    const tempZip = path.join(os.tmpdir(), `e3-watch-${Date.now()}.zip`);
    try {
      await e3.export(pkg, tempZip);
    } catch (err) {
      console.log(`[${timestamp()}] Error exporting package:`);
      console.log(`  ${err instanceof Error ? err.message : String(err)}`);
      return null;
    }

    // Import into repository
    const deployStorage = new LocalStorage();
    try {
      await packageImport(deployStorage, repoPath, tempZip);
    } catch (err) {
      console.log(`[${timestamp()}] Error importing package:`);
      console.log(`  ${err instanceof Error ? err.message : String(err)}`);
      return null;
    } finally {
      // Clean up temp file
      try {
        fs.unlinkSync(tempZip);
      } catch {
        // Ignore cleanup errors
      }
    }

    // Ensure workspace exists
    try {
      await workspaceGetState(deployStorage, repoPath, workspace);
    } catch {
      // Workspace doesn't exist, create it
      try {
        await workspaceCreate(deployStorage, repoPath, workspace);
        console.log(`[${timestamp()}] Created workspace: ${workspace}`);
      } catch (err) {
        console.log(`[${timestamp()}] Error creating workspace:`);
        console.log(`  ${err instanceof Error ? err.message : String(err)}`);
        return null;
      }
    }

    // Deploy to workspace
    try {
      await workspaceDeploy(deployStorage, repoPath, workspace, pkg.name, pkg.version);
      console.log(`[${timestamp()}] Deployed to workspace: ${workspace}`);
    } catch (err) {
      console.log(`[${timestamp()}] Error deploying:`);
      console.log(`  ${err instanceof Error ? err.message : String(err)}`);
      return null;
    }

    return { name: pkg.name, version: pkg.version, watchedFiles };
  }

  const storage = new LocalStorage();

  /**
   * Execute the dataflow in the workspace
   */
  async function runDataflow(signal: AbortSignal): Promise<void> {
    console.log(`[${timestamp()}] Starting dataflow...`);

    try {
      const result = await dataflowExecute(storage, repoPath, workspace, {
        concurrency,
        signal,
        onTaskStart: (name) => {
          console.log(`  [START] ${name}`);
        },
        onTaskComplete: (taskResult: TaskExecutionResult) => {
          const status = taskResult.state === 'success' ? 'DONE' :
                        taskResult.state === 'failed' ? 'FAIL' :
                        taskResult.state === 'skipped' ? 'SKIP' : 'ERR';
          const cached = taskResult.cached ? ' (cached)' : '';
          const duration = taskResult.duration > 0 ? ` [${taskResult.duration}ms]` : '';
          console.log(`  [${status}] ${taskResult.name}${cached}${duration}`);
        },
      });

      if (result.success) {
        console.log(`[${timestamp()}] Dataflow complete (${result.executed} executed, ${result.cached} cached)`);
      } else {
        console.log(`[${timestamp()}] Dataflow failed (${result.failed} failed)`);
      }
    } catch (err) {
      if (err instanceof DataflowAbortedError) {
        console.log(`[${timestamp()}] Dataflow aborted`);
      } else {
        console.log(`[${timestamp()}] Dataflow error:`);
        console.log(`  ${err instanceof Error ? err.message : String(err)}`);
      }
    }
  }

  /**
   * Handle a file change event
   */
  async function handleChange(): Promise<void> {
    if (isExecuting) {
      if (options.abortOnChange && currentAbortController) {
        console.log(`[${timestamp()}] File changed, aborting current execution...`);
        currentAbortController.abort();
      } else {
        console.log(`[${timestamp()}] File changed (queued, execution in progress)`);
        pendingReload = true;
      }
      return;
    }

    isExecuting = true;
    pendingReload = false;

    console.log(`[${timestamp()}] File changed, reloading...`);

    const deployed = await deployPackage();

    if (deployed) {
      setupWatchers(deployed.watchedFiles);
      if (options.start) {
        currentAbortController = new AbortController();
        await runDataflow(currentAbortController.signal);
        currentAbortController = null;
      }
    }
    // Note: Don't reset watchers on failure - keep watching existing files
    // so we can recover when the error is fixed

    isExecuting = false;

    // Process queued reload if any
    if (pendingReload) {
      console.log(`[${timestamp()}] Processing queued reload...`);
      await handleChange();
    } else {
      console.log(`[${timestamp()}] Waiting for changes...`);
    }
  }

  // Track file watchers for all source files
  const watchers = new Map<string, fs.FSWatcher>();
  let debounceTimer: NodeJS.Timeout | null = null;

  function setupWatchers(files: string[]) {
    // Close watchers for files no longer in the list
    for (const [filePath, watcher] of watchers) {
      if (!files.includes(filePath)) {
        watcher.close();
        watchers.delete(filePath);
      }
    }

    // Add watchers for new files
    for (const filePath of files) {
      if (!watchers.has(filePath) && fs.existsSync(filePath)) {
        const watcher = fs.watch(filePath, () => {
          if (debounceTimer) {
            clearTimeout(debounceTimer);
          }
          debounceTimer = setTimeout(() => {
            handleChange().catch(err => {
              console.log(`[${timestamp()}] Unexpected error:`);
              console.log(`  ${formatError(err)}`);
            });
          }, 100);
        });
        watchers.set(filePath, watcher);
      }
    }
  }

  // Initial load
  console.log(`[${timestamp()}] Initial load...`);
  isExecuting = true;

  const deployed = await deployPackage();

  if (deployed) {
    setupWatchers(deployed.watchedFiles);
    if (options.start) {
      currentAbortController = new AbortController();
      await runDataflow(currentAbortController.signal);
      currentAbortController = null;
    }
  } else {
    // Even if deploy failed, watch the source file so we can recover
    setupWatchers([absoluteSourcePath]);
  }

  isExecuting = false;
  console.log(`[${timestamp()}] Ready. Waiting for changes...`);
  console.log('');

  // Handle signals for graceful shutdown
  const cleanup = () => {
    console.log('');
    console.log('Stopping watch...');
    for (const watcher of watchers.values()) {
      watcher.close();
    }
    if (currentAbortController) {
      currentAbortController.abort();
    }
    process.exit(0);
  };

  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);

  // Debug: show what files are being watched
  console.log(`Watching ${watchers.size} files:`);
  for (const file of watchers.keys()) {
    console.log(`  - ${file}`);
  }

  // Keep process alive - the fs.watch handlers should do this,
  // but use setInterval as backup
  setInterval(() => {}, 1000 * 60 * 60);  // 1 hour intervals
}
