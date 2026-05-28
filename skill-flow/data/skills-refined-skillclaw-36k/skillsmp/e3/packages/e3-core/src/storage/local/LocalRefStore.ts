/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { decodeBeast2For, encodeBeast2For } from '@elaraai/east';
import { ExecutionStatusType } from '@elaraai/e3-types';
import type { ExecutionStatus } from '@elaraai/e3-types';
import type { RefStore } from '../interfaces.js';
import { isNotFoundError, ExecutionCorruptError } from '../../errors.js';

/**
 * Local filesystem implementation of RefStore.
 *
 * The `repo` parameter is the path to the e3 repository directory.
 */
export class LocalRefStore implements RefStore {
  // -------------------------------------------------------------------------
  // Package References
  // -------------------------------------------------------------------------

  async packageList(repo: string): Promise<{ name: string; version: string }[]> {
    const packagesDir = path.join(repo, 'packages');
    const packages: { name: string; version: string }[] = [];

    try {
      const names = await fs.readdir(packagesDir);
      for (const name of names) {
        const nameDir = path.join(packagesDir, name);
        const stat = await fs.stat(nameDir);
        if (stat.isDirectory()) {
          const versions = await fs.readdir(nameDir);
          for (const version of versions) {
            packages.push({ name, version });
          }
        }
      }
    } catch (err) {
      // Only suppress ENOENT - directory may not exist yet
      if (!isNotFoundError(err)) {
        throw err;
      }
    }

    return packages;
  }

  async packageResolve(repo: string, name: string, version: string): Promise<string | null> {
    const refPath = path.join(repo, 'packages', name, version);
    try {
      const content = await fs.readFile(refPath, 'utf-8');
      return content.trim();
    } catch (err) {
      if (isNotFoundError(err)) {
        return null;
      }
      throw err;
    }
  }

  async packageWrite(repo: string, name: string, version: string, hash: string): Promise<void> {
    const refDir = path.join(repo, 'packages', name);
    await fs.mkdir(refDir, { recursive: true });
    const refPath = path.join(refDir, version);
    await fs.writeFile(refPath, hash + '\n');
  }

  async packageRemove(repo: string, name: string, version: string): Promise<void> {
    const refPath = path.join(repo, 'packages', name, version);
    try {
      await fs.unlink(refPath);
    } catch (err) {
      if (isNotFoundError(err)) {
        return; // Already removed, idempotent
      }
      throw err;
    }

    // Try to remove the package name directory if empty
    const packageDir = path.join(repo, 'packages', name);
    try {
      await fs.rmdir(packageDir);
    } catch {
      // Directory not empty, that's fine
    }
  }

  // -------------------------------------------------------------------------
  // Workspace State
  // -------------------------------------------------------------------------

  async workspaceList(repo: string): Promise<string[]> {
    const workspacesDir = path.join(repo, 'workspaces');
    const names: string[] = [];

    try {
      const entries = await fs.readdir(workspacesDir);
      for (const entry of entries) {
        if (entry.endsWith('.beast2')) {
          names.push(entry.slice(0, -7)); // Remove .beast2 extension
        }
      }
    } catch (err) {
      // Only suppress ENOENT - directory may not exist yet
      if (!isNotFoundError(err)) {
        throw err;
      }
    }

    return names;
  }

  async workspaceRead(repo: string, name: string): Promise<Uint8Array | null> {
    const stateFile = path.join(repo, 'workspaces', `${name}.beast2`);

    try {
      return await fs.readFile(stateFile);
    } catch (err) {
      if (isNotFoundError(err)) {
        return null;
      }
      throw err;
    }
  }

  async workspaceWrite(repo: string, name: string, state: Uint8Array): Promise<void> {
    const wsDir = path.join(repo, 'workspaces');
    const stateFile = path.join(wsDir, `${name}.beast2`);

    await fs.mkdir(wsDir, { recursive: true });

    // Write atomically: write to temp file, then rename
    const randomSuffix = Math.random().toString(36).slice(2, 10);
    const tempPath = path.join(wsDir, `.${name}.${Date.now()}.${randomSuffix}.tmp`);
    await fs.writeFile(tempPath, state);
    await fs.rename(tempPath, stateFile);
  }

  async workspaceRemove(repo: string, name: string): Promise<void> {
    const stateFile = path.join(repo, 'workspaces', `${name}.beast2`);
    try {
      await fs.unlink(stateFile);
    } catch (err) {
      if (isNotFoundError(err)) {
        return; // Already removed, idempotent
      }
      throw err;
    }
  }

  // -------------------------------------------------------------------------
  // Execution Cache
  // -------------------------------------------------------------------------

  private executionDir(repo: string, taskHash: string, inputsHash: string): string {
    return path.join(repo, 'executions', taskHash, inputsHash);
  }

  async executionGet(repo: string, taskHash: string, inputsHash: string): Promise<ExecutionStatus | null> {
    const execDir = this.executionDir(repo, taskHash, inputsHash);
    const statusPath = path.join(execDir, 'status.beast2');

    let data: Buffer;
    try {
      data = await fs.readFile(statusPath);
    } catch (err) {
      if (isNotFoundError(err)) {
        return null;
      }
      throw err;
    }

    try {
      const decoder = decodeBeast2For(ExecutionStatusType);
      return decoder(data);
    } catch (err) {
      throw new ExecutionCorruptError(
        taskHash,
        inputsHash,
        err instanceof Error ? err : new Error(String(err))
      );
    }
  }

  async executionWrite(repo: string, taskHash: string, inputsHash: string, status: ExecutionStatus): Promise<void> {
    const execDir = this.executionDir(repo, taskHash, inputsHash);
    await fs.mkdir(execDir, { recursive: true });

    const encoder = encodeBeast2For(ExecutionStatusType);
    await fs.writeFile(path.join(execDir, 'status.beast2'), encoder(status));
  }

  async executionGetOutput(repo: string, taskHash: string, inputsHash: string): Promise<string | null> {
    const execDir = this.executionDir(repo, taskHash, inputsHash);
    const outputPath = path.join(execDir, 'output');

    try {
      const content = await fs.readFile(outputPath, 'utf-8');
      return content.trim();
    } catch (err) {
      if (isNotFoundError(err)) {
        return null;
      }
      throw err;
    }
  }

  async executionWriteOutput(repo: string, taskHash: string, inputsHash: string, outputHash: string): Promise<void> {
    const execDir = this.executionDir(repo, taskHash, inputsHash);
    await fs.mkdir(execDir, { recursive: true });
    await fs.writeFile(path.join(execDir, 'output'), outputHash + '\n');
  }

  async executionList(repo: string): Promise<{ taskHash: string; inputsHash: string }[]> {
    const executionsDir = path.join(repo, 'executions');
    const result: { taskHash: string; inputsHash: string }[] = [];

    try {
      const taskDirs = await fs.readdir(executionsDir);

      for (const taskHash of taskDirs) {
        if (!/^[a-f0-9]{64}$/.test(taskHash)) continue;

        const taskDir = path.join(executionsDir, taskHash);
        const stat = await fs.stat(taskDir);
        if (!stat.isDirectory()) continue;

        const inputsDirs = await fs.readdir(taskDir);
        for (const inputsHash of inputsDirs) {
          if (/^[a-f0-9]{64}$/.test(inputsHash)) {
            result.push({ taskHash, inputsHash });
          }
        }
      }
    } catch (err) {
      // Only suppress ENOENT - directory may not exist yet
      if (!isNotFoundError(err)) {
        throw err;
      }
    }

    return result;
  }

  async executionListForTask(repo: string, taskHash: string): Promise<string[]> {
    const taskDir = path.join(repo, 'executions', taskHash);

    try {
      const entries = await fs.readdir(taskDir);
      return entries.filter((e) => /^[a-f0-9]{64}$/.test(e));
    } catch (err) {
      // Only suppress ENOENT - task may not have any executions yet
      if (!isNotFoundError(err)) {
        throw err;
      }
      return [];
    }
  }
}
