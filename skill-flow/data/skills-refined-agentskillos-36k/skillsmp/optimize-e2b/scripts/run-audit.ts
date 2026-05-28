#!/usr/bin/env bun
/**
 * E2B Audit Runner - Standalone bun script
 *
 * Runs accessibility and SEO audits in E2B cloud sandboxes.
 *
 * Usage:
 *   bun run-audit.ts --url https://example.com
 *   bun run-audit.ts  # Uses localhost:4321 (uploads codebase, starts dev server)
 *
 * Requires:
 *   - E2B_API_KEY environment variable
 *   - bun installed globally
 */

import { Sandbox } from 'e2b';
import { parseArgs } from 'node:util';
import { mkdir, writeFile, readdir } from 'node:fs/promises';
import { join, relative } from 'node:path';

// Custom E2B template with Node 22 + Chrome + audit tools pre-installed
const TEMPLATE_ID = 'o9qbmv9te4ms59ge7b0o';
const PROJECT_DIR = '/home/user/project';
const RESULTS_DIR = '/home/user/project/audit-results';

// Chrome configuration for headless operation in sandboxed environments
const CHROME_ENV = 'CHROME_PATH=/usr/bin/chromium PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium';
const CHROME_FLAGS = [
  '--headless=new',
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--disable-gpu',
  '--disable-dev-shm-usage',
  '--disable-software-rasterizer',
  '--disable-extensions',
  '--no-first-run',
  '--disable-background-networking',
  '--disable-default-apps',
].join(' ');

interface Options {
  url?: string;
  output: string;
  tools: string[];
  verbose: boolean;
  devCommand: string;
  devPort: number;
  timeout: number;
}

function parseOptions(): Options {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      url: { type: 'string', short: 'u' },
      output: { type: 'string', short: 'o', default: 'docs/audits/raw' },
      tools: { type: 'string', short: 't', default: 'lighthouse,axe,pa11y' },
      verbose: { type: 'boolean', short: 'v', default: false },
      'dev-command': { type: 'string', default: 'npm run dev' },
      'dev-port': { type: 'string', default: '4321' },
      timeout: { type: 'string', default: '600' },
    },
    allowPositionals: true,
  });

  return {
    url: values.url,
    output: values.output as string,
    tools: (values.tools as string).split(',').map(t => t.trim()),
    verbose: values.verbose as boolean,
    devCommand: values['dev-command'] as string,
    devPort: parseInt(values['dev-port'] as string, 10),
    timeout: parseInt(values.timeout as string, 10),
  };
}

function log(verbose: boolean, message: string): void {
  if (verbose) {
    console.log(`[e2b-audit] ${message}`);
  }
}

async function runCommand(
  sandbox: Sandbox,
  command: string,
  options: { cwd?: string; timeout?: number; stream?: boolean } = {}
): Promise<{ exitCode: number; stdout: string; stderr: string }> {
  const { cwd = PROJECT_DIR, timeout = 120000, stream = false } = options;

  const result = await sandbox.commands.run(command, {
    cwd,
    timeoutMs: timeout,
    onStdout: stream ? (data) => process.stdout.write(data) : undefined,
    onStderr: stream ? (data) => process.stderr.write(data) : undefined,
  });

  return {
    exitCode: result.exitCode,
    stdout: result.stdout,
    stderr: result.stderr,
  };
}

async function uploadCodebase(sandbox: Sandbox, localDir: string): Promise<{ uploaded: number; skipped: number }> {
  const ignorePatterns = [
    'node_modules', '.git', 'dist', 'build', '.next', '.nuxt', '.output',
    '.cache', '.turbo', '.vercel', '.netlify', 'coverage', '.nyc_output',
    '*.log', '.DS_Store', 'thumbs.db', '.env', '.env.*', '!.env.example',
  ];

  const shouldIgnore = (path: string): boolean => {
    const name = path.split('/').pop() || '';
    return ignorePatterns.some(pattern => {
      if (pattern.startsWith('!')) return false;
      if (pattern.includes('*')) {
        const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
        return regex.test(name);
      }
      return name === pattern || path.includes(`/${pattern}/`);
    });
  };

  let uploaded = 0;
  let skipped = 0;

  async function uploadDir(dir: string, remotePath: string): Promise<void> {
    const entries = await readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const localPath = join(dir, entry.name);
      const relPath = relative(localDir, localPath);

      if (shouldIgnore(relPath)) {
        skipped++;
        continue;
      }

      const remoteFilePath = `${remotePath}/${entry.name}`;

      if (entry.isDirectory()) {
        await sandbox.files.makeDir(remoteFilePath);
        await uploadDir(localPath, remoteFilePath);
      } else if (entry.isFile()) {
        const content = await Bun.file(localPath).text();
        await sandbox.files.write(remoteFilePath, content);
        uploaded++;
      }
    }
  }

  await sandbox.files.makeDir(PROJECT_DIR);
  await uploadDir(localDir, PROJECT_DIR);

  return { uploaded, skipped };
}

async function startDevServer(
  sandbox: Sandbox,
  command: string,
  port: number,
  verbose: boolean
): Promise<void> {
  log(verbose, `Starting dev server: ${command}`);

  // Start server in background
  await runCommand(sandbox, `${command} > /tmp/dev-server.log 2>&1 &`, { timeout: 5000 });

  // Wait for server to be ready (poll for up to 60 seconds)
  const maxAttempts = 30;
  for (let i = 0; i < maxAttempts; i++) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    const check = await runCommand(sandbox, `curl -s -o /dev/null -w "%{http_code}" http://localhost:${port} || echo "000"`, { timeout: 5000 });
    const statusCode = check.stdout.trim();
    if (statusCode === '200' || statusCode === '304') {
      log(verbose, `Dev server ready on port ${port}`);
      return;
    }
    log(verbose, `Waiting for dev server... (attempt ${i + 1}/${maxAttempts}, status: ${statusCode})`);
  }

  // Log server output for debugging
  const serverLog = await runCommand(sandbox, 'cat /tmp/dev-server.log', { timeout: 5000 });
  console.error('Dev server log:', serverLog.stdout);
  throw new Error(`Dev server failed to start on port ${port}`);
}

async function runAuditTool(
  sandbox: Sandbox,
  tool: string,
  url: string,
  verbose: boolean
): Promise<void> {
  log(verbose, `Running ${tool}...`);

  await runCommand(sandbox, `mkdir -p ${RESULTS_DIR}`);

  let command: string;

  switch (tool) {
    case 'lighthouse':
      command = `${CHROME_ENV} lighthouse ${url} --output json --output-path ${RESULTS_DIR}/lighthouse-results.json --only-categories=accessibility,best-practices,performance,seo --chrome-flags="${CHROME_FLAGS}"`;
      break;
    case 'axe':
      command = `cd ${RESULTS_DIR} && ${CHROME_ENV} axe ${url} --save axe-results.json --chrome-options="headless,no-sandbox,disable-gpu,disable-dev-shm-usage"`;
      break;
    case 'pa11y':
      // Pa11y returns exit code 2 when issues found - use || true to capture output
      command = `bash -c '${CHROME_ENV} pa11y ${url} --reporter json --runner htmlcs > ${RESULTS_DIR}/pa11y-results.json 2>&1 || true'`;
      break;
    default:
      throw new Error(`Unknown tool: ${tool}`);
  }

  const result = await runCommand(sandbox, command, {
    timeout: 300000, // 5 minutes per tool
    stream: verbose
  });

  if (result.exitCode !== 0 && tool !== 'pa11y') {
    console.warn(`Warning: ${tool} exited with code ${result.exitCode}`);
    if (verbose) {
      console.warn(`stderr: ${result.stderr}`);
    }
  }

  log(verbose, `${tool} complete`);
}

async function downloadResults(
  sandbox: Sandbox,
  localOutputDir: string,
  verbose: boolean
): Promise<string[]> {
  await mkdir(localOutputDir, { recursive: true });

  const files = ['lighthouse-results.json', 'axe-results.json', 'pa11y-results.json'];
  const downloaded: string[] = [];

  for (const file of files) {
    try {
      const remotePath = `${RESULTS_DIR}/${file}`;
      const content = await sandbox.files.read(remotePath);
      const localPath = join(localOutputDir, file);
      await writeFile(localPath, content);
      downloaded.push(file);
      log(verbose, `Downloaded: ${file}`);
    } catch (err) {
      log(verbose, `Not found: ${file}`);
    }
  }

  return downloaded;
}

async function main(): Promise<void> {
  const options = parseOptions();

  // Validate E2B API key
  if (!process.env.E2B_API_KEY) {
    console.error('Error: E2B_API_KEY environment variable is required');
    console.error('Get your API key from https://e2b.dev/dashboard');
    process.exit(1);
  }

  const isLocalUrl = !options.url || options.url.includes('localhost') || options.url.includes('127.0.0.1');
  const cwd = process.cwd();

  console.log('');
  console.log('========================================');
  console.log('E2B Audit Runner');
  console.log('========================================');
  console.log('');
  console.log(`URL: ${options.url || `http://localhost:${options.devPort} (local dev server)`}`);
  console.log(`Tools: ${options.tools.join(', ')}`);
  console.log(`Output: ${options.output}`);
  console.log('');

  log(options.verbose, 'Creating sandbox...');
  const sandbox = await Sandbox.create(TEMPLATE_ID, {
    timeoutMs: options.timeout * 1000,
  });

  console.log(`Sandbox created: ${sandbox.sandboxId}`);

  try {
    if (isLocalUrl) {
      // Upload codebase and start dev server
      log(options.verbose, 'Uploading codebase...');
      const { uploaded, skipped } = await uploadCodebase(sandbox, cwd);
      console.log(`Uploaded ${uploaded} files (${skipped} skipped)`);

      // Install dependencies
      log(options.verbose, 'Installing dependencies...');
      const installResult = await runCommand(sandbox, 'npm install', {
        timeout: 300000,
        stream: options.verbose,
      });

      if (installResult.exitCode !== 0) {
        throw new Error(`npm install failed: ${installResult.stderr}`);
      }

      // Start dev server
      await startDevServer(sandbox, options.devCommand, options.devPort, options.verbose);
    }

    // Run each audit tool
    const auditUrl = isLocalUrl ? `http://localhost:${options.devPort}` : options.url!;
    const startTime = Date.now();

    for (const tool of options.tools) {
      await runAuditTool(sandbox, tool, auditUrl, options.verbose);
    }

    const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    console.log(`\nAudits completed in ${duration}s`);

    // Download results
    log(options.verbose, 'Downloading results...');
    const localOutputDir = join(cwd, options.output);
    const downloaded = await downloadResults(sandbox, localOutputDir, options.verbose);

    console.log('');
    console.log('========================================');
    console.log('AUDIT COMPLETE');
    console.log('========================================');
    console.log('');
    console.log(`Results saved to: ${options.output}/`);
    for (const file of downloaded) {
      console.log(`  - ${file}`);
    }
    console.log('');

  } finally {
    log(options.verbose, 'Cleaning up sandbox...');
    await sandbox.kill();
  }
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
