/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { Hono } from 'hono';
import type { StorageBackend } from '@elaraai/e3-core';
import { listTasks, getTask, listExecutions } from '../handlers/tasks.js';

export function createTaskRoutes(
  storage: StorageBackend,
  getRepoPath: (repo: string) => string
) {
  const app = new Hono();

  // GET /api/repos/:repo/workspaces/:ws/tasks - List tasks
  app.get('/', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    return listTasks(storage, repoPath, ws);
  });

  // GET /api/repos/:repo/workspaces/:ws/tasks/:task - Get task details
  app.get('/:task', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    const taskName = c.req.param('task')!;
    return getTask(storage, repoPath, ws, taskName);
  });

  // GET /api/repos/:repo/workspaces/:ws/tasks/:task/executions - List execution history
  app.get('/:task/executions', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    const taskName = c.req.param('task')!;
    return listExecutions(storage, repoPath, ws, taskName);
  });

  return app;
}
