/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { Hono } from 'hono';
import type { StorageBackend } from '@elaraai/e3-core';
import {
  listWorkspaces,
  createWorkspace,
  getWorkspace,
  getWorkspaceStatus,
  deleteWorkspace,
  deployWorkspace,
  exportWorkspace,
} from '../handlers/workspaces.js';
import { decodeBody } from '../beast2.js';
import { CreateWorkspaceType, DeployRequestType } from '../types.js';

export function createWorkspaceRoutes(
  storage: StorageBackend,
  getRepoPath: (repo: string) => string
) {
  const app = new Hono();

  // GET /api/repos/:repo/workspaces - List all workspaces
  app.get('/', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    return listWorkspaces(storage, repoPath);
  });

  // POST /api/repos/:repo/workspaces - Create a new workspace
  app.post('/', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const body = await decodeBody(c, CreateWorkspaceType);
    return createWorkspace(storage, repoPath, body.name);
  });

  // GET /api/repos/:repo/workspaces/:ws - Get workspace state
  app.get('/:ws', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    return getWorkspace(storage, repoPath, ws);
  });

  // GET /api/repos/:repo/workspaces/:ws/status - Get comprehensive workspace status
  app.get('/:ws/status', (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    return getWorkspaceStatus(storage, repoPath, ws);
  });

  // DELETE /api/repos/:repo/workspaces/:ws - Remove a workspace
  app.delete('/:ws', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    return deleteWorkspace(storage, repoPath, ws);
  });

  // POST /api/repos/:repo/workspaces/:ws/deploy - Deploy a package to a workspace
  app.post('/:ws/deploy', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    const body = await decodeBody(c, DeployRequestType);
    return deployWorkspace(storage, repoPath, ws, body.packageRef);
  });

  // GET /api/repos/:repo/workspaces/:ws/export - Export workspace as a package zip
  app.get('/:ws/export', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;
    return exportWorkspace(storage, repoPath, ws);
  });

  return app;
}
