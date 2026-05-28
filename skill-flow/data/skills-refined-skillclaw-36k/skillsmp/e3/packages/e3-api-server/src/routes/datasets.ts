/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { Hono } from 'hono';
import { urlPathToTreePath } from '@elaraai/e3-types';
import type { StorageBackend } from '@elaraai/e3-core';
import {
  listDatasets,
  listDatasetsRecursive,
  getDataset,
  setDataset,
} from '../handlers/datasets.js';

export function createDatasetRoutes(
  storage: StorageBackend,
  getRepoPath: (repo: string) => string
) {
  const app = new Hono();

  // GET /api/repos/:repo/workspaces/:ws/datasets - List root fields (or recursive list if ?recursive=true)
  app.get('/', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;

    // Check if this is a recursive list request
    const recursive = c.req.query('recursive');
    if (recursive === 'true') {
      return listDatasetsRecursive(storage, repoPath, ws, []);
    }

    return listDatasets(storage, repoPath, ws, []);
  });

  // GET /api/repos/:repo/workspaces/:ws/datasets/* - Get dataset value (or list if ?list=true, or recursive if ?recursive=true)
  app.get('/*', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;

    // Extract the wildcard path
    const fullPath = c.req.path;
    // Path format: /api/repos/:repo/workspaces/:ws/datasets/*
    // Find the position after /datasets/
    const datasetsPrefix = `/api/repos/${repo}/workspaces/${ws}/datasets/`;
    const pathStr = fullPath.startsWith(datasetsPrefix) ? fullPath.slice(datasetsPrefix.length) : '';
    const treePath = urlPathToTreePath(pathStr);

    // Check if this is a recursive list request
    const recursive = c.req.query('recursive');
    if (recursive === 'true') {
      return listDatasetsRecursive(storage, repoPath, ws, treePath);
    }

    // Check if this is a list request
    const listParam = c.req.query('list');
    if (listParam === 'true') {
      return listDatasets(storage, repoPath, ws, treePath);
    }

    return getDataset(storage, repoPath, ws, treePath);
  });

  // PUT /api/repos/:repo/workspaces/:ws/datasets/* - Set dataset value
  app.put('/*', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const ws = c.req.param('ws')!;

    // Extract the wildcard path
    const fullPath = c.req.path;
    const datasetsPrefix = `/api/repos/${repo}/workspaces/${ws}/datasets/`;
    const pathStr = fullPath.startsWith(datasetsPrefix) ? fullPath.slice(datasetsPrefix.length) : '';
    const treePath = urlPathToTreePath(pathStr);

    // Body is raw BEAST2
    const buffer = await c.req.arrayBuffer();
    const body = new Uint8Array(buffer);

    return setDataset(storage, repoPath, ws, treePath, body);
  });

  return app;
}
