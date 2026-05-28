/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { LogChunk, LogStore } from '../interfaces.js';
import { isNotFoundError } from '../../errors.js';

/**
 * Local filesystem implementation of LogStore.
 *
 * Logs are stored as text files in the execution directory:
 *   executions/<taskHash>/<inputsHash>/stdout.txt
 *   executions/<taskHash>/<inputsHash>/stderr.txt
 *
 * The `repo` parameter is the path to the e3 repository directory.
 */
export class LocalLogStore implements LogStore {
  private logPath(repo: string, taskHash: string, inputsHash: string, stream: 'stdout' | 'stderr'): string {
    return path.join(
      repo,
      'executions',
      taskHash,
      inputsHash,
      `${stream}.txt`
    );
  }

  async append(
    repo: string,
    taskHash: string,
    inputsHash: string,
    stream: 'stdout' | 'stderr',
    data: string
  ): Promise<void> {
    const logFile = this.logPath(repo, taskHash, inputsHash, stream);
    const dir = path.dirname(logFile);

    await fs.mkdir(dir, { recursive: true });
    await fs.appendFile(logFile, data);
  }

  async read(
    repo: string,
    taskHash: string,
    inputsHash: string,
    stream: 'stdout' | 'stderr',
    options?: { offset?: number; limit?: number }
  ): Promise<LogChunk> {
    const logFile = this.logPath(repo, taskHash, inputsHash, stream);

    const offset = options?.offset ?? 0;
    const limit = options?.limit ?? 65536; // 64KB default

    try {
      const stat = await fs.stat(logFile);
      const totalSize = stat.size;

      // Open file and read chunk
      const fd = await fs.open(logFile, 'r');
      try {
        const buffer = Buffer.alloc(Math.min(limit, Math.max(0, totalSize - offset)));
        const { bytesRead } = await fd.read(buffer, 0, buffer.length, offset);

        return {
          data: buffer.slice(0, bytesRead).toString('utf-8'),
          offset,
          size: bytesRead,
          totalSize,
          complete: offset + bytesRead >= totalSize,
        };
      } finally {
        await fd.close();
      }
    } catch (err) {
      if (isNotFoundError(err)) {
        // Log file doesn't exist yet
        return {
          data: '',
          offset: 0,
          size: 0,
          totalSize: 0,
          complete: true,
        };
      }
      throw err;
    }
  }
}
