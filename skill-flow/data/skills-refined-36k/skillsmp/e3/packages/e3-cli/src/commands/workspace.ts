/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 workspace commands - Workspace management
 */

import {
  workspaceCreate,
  workspaceDeploy,
  workspaceExport,
  workspaceList,
  workspaceRemove,
  workspaceGetState,
  workspaceStatus,
  WorkspaceLockError,
  LocalStorage,
  type WorkspaceStatusResult,
} from '@elaraai/e3-core';
import {
  workspaceCreate as workspaceCreateRemote,
  workspaceDeploy as workspaceDeployRemote,
  workspaceExport as workspaceExportRemote,
  workspaceList as workspaceListRemote,
  workspaceRemove as workspaceRemoveRemote,
  workspaceStatus as workspaceStatusRemote,
} from '@elaraai/e3-api-client';
import { writeFileSync } from 'node:fs';
import { parseRepoLocation, parsePackageSpec, formatError, exitError } from '../utils.js';

export const workspaceCommand = {
  /**
   * Create an empty workspace.
   */
  async create(repoArg: string, name: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);

      if (location.type === 'local') {
        const storage = new LocalStorage();
        await workspaceCreate(storage, location.path, name);
      } else {
        await workspaceCreateRemote(location.baseUrl, location.repo, name, { token: location.token });
      }

      console.log(`Created workspace: ${name}`);
      console.log('Deploy a package with: e3 workspace deploy <repo> <ws> <pkg>[@<ver>]');
    } catch (err) {
      exitError(formatError(err));
    }
  },

  /**
   * Deploy a package to a workspace.
   */
  async deploy(repoArg: string, ws: string, pkgSpec: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);
      const { name, version } = parsePackageSpec(pkgSpec);

      if (location.type === 'local') {
        const storage = new LocalStorage();
        await workspaceDeploy(storage, location.path, ws, name, version);
      } else {
        // Remote API accepts packageRef string (name@version)
        const packageRef = version === 'latest' ? name : `${name}@${version}`;
        await workspaceDeployRemote(location.baseUrl, location.repo, ws, packageRef, { token: location.token });
      }

      console.log(`Deployed ${name}@${version} to workspace: ${ws}`);
    } catch (err) {
      if (err instanceof WorkspaceLockError) {
        console.log('');
        console.log(`Workspace is locked by another process with PID: ${err.holder?.pid ?? 'unknown'}`);
        process.exit(1);
      }
      exitError(formatError(err));
    }
  },

  /**
   * Export workspace as a package.
   */
  async export(
    repoArg: string,
    ws: string,
    zipPath: string,
    options: { name?: string; version?: string }
  ): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);

      if (location.type === 'local') {
        const storage = new LocalStorage();
        const result = await workspaceExport(storage, location.path, ws, zipPath, options.name, options.version);

        console.log(`Exported workspace ${ws} as ${result.name}@${result.version}`);
        console.log(`  Output: ${zipPath}`);
        console.log(`  Package hash: ${result.packageHash.slice(0, 12)}...`);
        console.log(`  Objects: ${result.objectCount}`);
      } else {
        // Remote export - fetch zip bytes and write to local file
        // Note: Remote export doesn't support custom name/version options
        if (options.name || options.version) {
          console.warn('Warning: --name and --version options are not supported for remote export');
        }
        const zipBytes = await workspaceExportRemote(location.baseUrl, location.repo, ws, { token: location.token });
        writeFileSync(zipPath, zipBytes);

        console.log(`Exported workspace ${ws}`);
        console.log(`  Output: ${zipPath}`);
        console.log(`  Size: ${zipBytes.length} bytes`);
      }
    } catch (err) {
      exitError(formatError(err));
    }
  },

  /**
   * List workspaces.
   */
  async list(repoArg: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);

      if (location.type === 'local') {
        const storage = new LocalStorage();
        const workspaces = await workspaceList(storage, location.path);

        if (workspaces.length === 0) {
          console.log('No workspaces');
          return;
        }

        console.log('Workspaces:');
        for (const ws of workspaces) {
          const state = await workspaceGetState(storage, location.path, ws);
          if (state) {
            console.log(`  ${ws} (${state.packageName}@${state.packageVersion})`);
          } else {
            console.log(`  ${ws} (not deployed)`);
          }
        }
      } else {
        // Remote - workspaceListRemote returns WorkspaceInfo[] with package info
        const workspaces = await workspaceListRemote(location.baseUrl, location.repo, { token: location.token });

        if (workspaces.length === 0) {
          console.log('No workspaces');
          return;
        }

        console.log('Workspaces:');
        for (const info of workspaces) {
          if (info.deployed && info.packageName.type === 'some') {
            const pkgVersion = info.packageVersion.type === 'some' ? info.packageVersion.value : 'unknown';
            console.log(`  ${info.name} (${info.packageName.value}@${pkgVersion})`);
          } else {
            console.log(`  ${info.name} (not deployed)`);
          }
        }
      }
    } catch (err) {
      exitError(formatError(err));
    }
  },

  /**
   * Remove a workspace.
   */
  async remove(repoArg: string, ws: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);

      if (location.type === 'local') {
        const storage = new LocalStorage();
        await workspaceRemove(storage, location.path, ws);
        console.log(`Removed workspace: ${ws}`);
        console.log('Run `e3 repo gc` to reclaim disk space');
      } else {
        await workspaceRemoveRemote(location.baseUrl, location.repo, ws, { token: location.token });
        console.log(`Removed workspace: ${ws}`);
      }
    } catch (err) {
      if (err instanceof WorkspaceLockError) {
        console.log('');
        console.log(`Workspace is locked by another process with PID: ${err.holder?.pid ?? 'unknown'}`);
        process.exit(1);
      }
      exitError(formatError(err));
    }
  },

  /**
   * Show detailed workspace status.
   */
  async status(repoArg: string, ws: string): Promise<void> {
    try {
      const location = await parseRepoLocation(repoArg);

      let status: WorkspaceStatusResult;

      if (location.type === 'local') {
        const storage = new LocalStorage();
        status = await workspaceStatus(storage, location.path, ws);
      } else {
        const remoteStatus = await workspaceStatusRemote(location.baseUrl, location.repo, ws, { token: location.token });
        // Convert remote status to local format
        status = {
          workspace: remoteStatus.workspace,
          lock: remoteStatus.lock.type === 'some' ? {
            pid: Number(remoteStatus.lock.value.pid),
            acquiredAt: remoteStatus.lock.value.acquiredAt,
            operation: remoteStatus.lock.value.command.type === 'some' ? remoteStatus.lock.value.command.value : undefined,
          } : null,
          datasets: remoteStatus.datasets.map(d => ({
            path: d.path,
            status: d.status as WorkspaceStatusResult['datasets'][0]['status'],
            hash: d.hash.type === 'some' ? d.hash.value : null,
            isTaskOutput: d.isTaskOutput,
            producedBy: d.producedBy.type === 'some' ? d.producedBy.value : null,
          })),
          tasks: remoteStatus.tasks.map(t => ({
            name: t.name,
            hash: t.hash,
            status: convertTaskStatus(t.status),
            inputs: t.inputs,
            output: t.output,
            dependsOn: t.dependsOn,
          })),
          summary: {
            datasets: {
              total: Number(remoteStatus.summary.datasets.total),
              unset: Number(remoteStatus.summary.datasets.unset),
              stale: Number(remoteStatus.summary.datasets.stale),
              upToDate: Number(remoteStatus.summary.datasets.upToDate),
            },
            tasks: {
              total: Number(remoteStatus.summary.tasks.total),
              upToDate: Number(remoteStatus.summary.tasks.upToDate),
              ready: Number(remoteStatus.summary.tasks.ready),
              waiting: Number(remoteStatus.summary.tasks.waiting),
              inProgress: Number(remoteStatus.summary.tasks.inProgress),
              failed: Number(remoteStatus.summary.tasks.failed),
              error: Number(remoteStatus.summary.tasks.error),
              staleRunning: Number(remoteStatus.summary.tasks.staleRunning),
            },
          },
        };
      }

      console.log(`Workspace: ${status.workspace}`);
      console.log('');

      // Lock status
      if (status.lock) {
        console.log('Lock:');
        console.log(`  Held by PID ${status.lock.pid}`);
        console.log(`  Since: ${status.lock.acquiredAt}`);
        if (status.lock.operation) {
          console.log(`  Operation: ${status.lock.operation}`);
        }
        console.log('');
      }

      // Summary
      console.log('Summary:');
      console.log(`  Datasets: ${status.summary.datasets.upToDate} up-to-date, ${status.summary.datasets.stale} stale, ${status.summary.datasets.unset} unset`);

      // Build task summary line - only include non-zero counts
      const taskParts: string[] = [];
      if (status.summary.tasks.upToDate > 0) taskParts.push(`${status.summary.tasks.upToDate} up-to-date`);
      if (status.summary.tasks.ready > 0) taskParts.push(`${status.summary.tasks.ready} ready`);
      if (status.summary.tasks.waiting > 0) taskParts.push(`${status.summary.tasks.waiting} waiting`);
      if (status.summary.tasks.inProgress > 0) taskParts.push(`${status.summary.tasks.inProgress} in-progress`);
      if (status.summary.tasks.failed > 0) taskParts.push(`${status.summary.tasks.failed} failed`);
      if (status.summary.tasks.error > 0) taskParts.push(`${status.summary.tasks.error} error`);
      if (status.summary.tasks.staleRunning > 0) taskParts.push(`${status.summary.tasks.staleRunning} stale-running`);
      console.log(`  Tasks: ${taskParts.join(', ') || 'none'}`);
      console.log('');

      // Tasks section
      if (status.tasks.length > 0) {
        console.log('Tasks:');
        for (const task of status.tasks) {
          const statusStr = formatTaskStatus(task.status);
          console.log(`  ${task.name}: ${statusStr}`);
          if (task.dependsOn.length > 0) {
            console.log(`    depends on: ${task.dependsOn.join(', ')}`);
          }
        }
        console.log('');
      }

      // Datasets section (only show non-up-to-date ones for brevity)
      const nonUpToDate = status.datasets.filter(d => d.status.type !== 'up-to-date');
      if (nonUpToDate.length > 0) {
        console.log('Datasets needing attention:');
        for (const dataset of nonUpToDate) {
          const statusStr = dataset.status.type === 'unset' ? 'unset' : 'stale';
          const producer = dataset.producedBy ? ` (from ${dataset.producedBy})` : ' (input)';
          console.log(`  ${dataset.path}: ${statusStr}${producer}`);
        }
      } else if (status.datasets.length > 0) {
        console.log('All datasets up-to-date');
      }
    } catch (err) {
      exitError(formatError(err));
    }
  },
};

/**
 * Convert remote task status to local format.
 */
 
function convertTaskStatus(status: any): WorkspaceStatusResult['tasks'][0]['status'] {
  switch (status.type) {
    case 'up-to-date':
      return { type: 'up-to-date', cached: Boolean(status.cached) };
    case 'ready':
      return { type: 'ready' };
    case 'waiting':
      return { type: 'waiting', reason: String(status.reason ?? '') };
    case 'in-progress':
      return {
        type: 'in-progress',
        pid: status.pid?.type === 'some' ? Number(status.pid.value) : undefined,
        startedAt: status.startedAt?.type === 'some' ? status.startedAt.value : undefined,
      };
    case 'failed':
      return {
        type: 'failed',
        exitCode: Number(status.exitCode ?? 0),
        completedAt: status.completedAt?.type === 'some' ? status.completedAt.value : undefined,
      };
    case 'error':
      return {
        type: 'error',
        message: String(status.message ?? ''),
        completedAt: status.completedAt?.type === 'some' ? status.completedAt.value : undefined,
      };
    case 'stale-running':
      return {
        type: 'stale-running',
        pid: status.pid?.type === 'some' ? Number(status.pid.value) : undefined,
        startedAt: status.startedAt?.type === 'some' ? status.startedAt.value : undefined,
      };
    default:
      return { type: 'ready' };
  }
}

/**
 * Format task status for display.
 */
function formatTaskStatus(status: WorkspaceStatusResult['tasks'][0]['status']): string {
  switch (status.type) {
    case 'up-to-date':
      return status.cached ? 'up-to-date (cached)' : 'up-to-date';
    case 'ready':
      return 'ready to run';
    case 'waiting':
      return `waiting (${status.reason})`;
    case 'in-progress':
      return status.pid ? `in-progress (PID ${status.pid})` : 'in-progress';
    case 'failed':
      return `FAILED (exit code ${status.exitCode})`;
    case 'error':
      return `ERROR: ${status.message}`;
    case 'stale-running':
      return `stale-running (PID ${status.pid} no longer exists)`;
    default:
      return 'unknown';
  }
}
