/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { Hono } from 'hono';
import { BlobType } from '@elaraai/east';
import type { StorageBackend } from '@elaraai/e3-core';
import {
  listPackages,
  getPackage,
  importPackage,
  exportPackage,
  deletePackage,
} from '../handlers/packages.js';
import { decodeBody } from '../beast2.js';

export function createPackageRoutes(
  storage: StorageBackend,
  getRepoPath: (repo: string) => string
) {
  const app = new Hono();

  // GET /api/repos/:repo/packages - List all packages
  app.get('/', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    return listPackages(storage, repoPath);
  });

  // GET /api/repos/:repo/packages/:name/:version - Get package details
  app.get('/:name/:version', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const name = c.req.param('name')!;
    const version = c.req.param('version')!;
    return getPackage(storage, repoPath, name, version);
  });

  // POST /api/repos/:repo/packages - Import a package from zip
  app.post('/', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);

    // Read raw body as zip bytes
    const contentType = c.req.header('content-type');
    let archive: Uint8Array;

    if (contentType === 'application/beast2') {
      // BEAST2 encoded blob
      archive = await decodeBody(c, BlobType);
    } else {
      // Raw zip bytes
      const buffer = await c.req.arrayBuffer();
      archive = new Uint8Array(buffer);
    }

    return importPackage(storage, repoPath, archive);
  });

  // GET /api/repos/:repo/packages/:name/:version/export - Export package as zip
  app.get('/:name/:version/export', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const name = c.req.param('name')!;
    const version = c.req.param('version')!;
    return exportPackage(storage, repoPath, name, version);
  });

  // DELETE /api/repos/:repo/packages/:name/:version - Remove a package
  app.delete('/:name/:version', async (c) => {
    const repo = c.req.param('repo')!;
    const repoPath = getRepoPath(repo);
    const name = c.req.param('name')!;
    const version = c.req.param('version')!;
    return deletePackage(storage, repoPath, name, version);
  });

  return app;
}
