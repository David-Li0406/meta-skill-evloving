/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { Hono } from 'hono';
import type { StorageBackend } from '@elaraai/e3-core';
import { getStatus, startGc, getGcStatus } from '../handlers/repository.js';
import { decodeBody } from '../beast2.js';
import { GcRequestType } from '../types.js';

export function createRepositoryRoutes(
  storage: StorageBackend,
  getRepoPath: (repo: string) => string
) {
  const app = new Hono();

  // GET /api/repos/:repo/status - Get repository status
  app.get('/status', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    return getStatus(storage, repoPath);
  });

  // POST /api/repos/:repo/gc - Start garbage collection (async)
  app.post('/gc', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const options = await decodeBody(c, GcRequestType);
    const minAge = options.minAge?.type === 'some' ? Number(options.minAge.value) : undefined;
    return startGc(storage, repoPath, { dryRun: options.dryRun, minAge });
  });

  // GET /api/repos/:repo/gc/:executionId - Get GC status
  app.get('/gc/:executionId', (c) => {
    const executionId = c.req.param('executionId')!;
    return getGcStatus(executionId);
  });

  return app;
}
