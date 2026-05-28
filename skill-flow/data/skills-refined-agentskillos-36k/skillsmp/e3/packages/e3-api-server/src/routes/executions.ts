/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { Hono } from 'hono';
import type { StorageBackend } from '@elaraai/e3-core';
import {
  startDataflow,
  getDataflowStatus,
  getDataflowGraph,
  getTaskLogs,
  getDataflowExecution,
} from '../handlers/dataflow.js';
import { decodeBody } from '../beast2.js';
import { DataflowRequestType } from '../types.js';

export function createExecutionRoutes(
  storage: StorageBackend,
  getRepoPath: (repo: string) => string
) {
  const app = new Hono();

  // POST /api/repos/:repo/workspaces/:ws/dataflow - Start dataflow execution (non-blocking)
  app.post('/', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;

    const body = await decodeBody(c, DataflowRequestType);
    const concurrency = body.concurrency.type === 'some' ? Number(body.concurrency.value) : 4;
    const filter = body.filter.type === 'some' ? body.filter.value : undefined;

    return startDataflow(storage, repoPath, ws, {
      concurrency,
      force: body.force,
      filter,
    });
  });

  // GET /api/repos/:repo/workspaces/:ws/dataflow - Get workspace status (for polling)
  app.get('/', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    return getDataflowStatus(storage, repoPath, ws);
  });

  // GET /api/repos/:repo/workspaces/:ws/dataflow/graph - Get dependency graph
  app.get('/graph', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    return getDataflowGraph(storage, repoPath, ws);
  });

  // GET /api/repos/:repo/workspaces/:ws/dataflow/logs/:task - Get task logs
  app.get('/logs/:task', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    const taskName = c.req.param('task')!;

    // Get query params
    const stream = (c.req.query('stream') as 'stdout' | 'stderr') || 'stdout';
    const offset = parseInt(c.req.query('offset') || '0', 10);
    const limit = parseInt(c.req.query('limit') || '65536', 10);

    return getTaskLogs(storage, repoPath, ws, taskName, stream, offset, limit);
  });

  // GET /api/repos/:repo/workspaces/:ws/dataflow/execution - Get execution state (for polling)
  app.get('/execution', (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;

    // Get query params for pagination
    const offset = c.req.query('offset') ? parseInt(c.req.query('offset')!, 10) : undefined;
    const limit = c.req.query('limit') ? parseInt(c.req.query('limit')!, 10) : undefined;

    return getDataflowExecution(repoPath, ws, { offset, limit });
  });

  return app;
}
