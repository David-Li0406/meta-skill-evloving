/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as path from 'node:path';
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { serve, type ServerType } from '@hono/node-server';
import { LocalStorage, repoInit, RepositoryNotFoundError } from '@elaraai/e3-core';
import type { StorageBackend } from '@elaraai/e3-core';
import { createAuthMiddleware, type AuthConfig } from './middleware/auth.js';
import { createOidcProvider, type OidcProvider, type OidcConfig } from './auth/index.js';
import { listRepos } from './handlers/repos.js';
import { startRepoDelete, getRepoDeleteStatus } from './handlers/repository.js';
import { sendError, sendSuccessWithStatus } from './beast2.js';
import { StringType, NullType, variant } from '@elaraai/east';
import { createPackageRoutes } from './routes/packages.js';
import { createWorkspaceRoutes } from './routes/workspaces.js';
import { createDatasetRoutes } from './routes/datasets.js';
import { createTaskRoutes } from './routes/tasks.js';
import { createExecutionRoutes } from './routes/executions.js';
import { createRepositoryRoutes } from './routes/repository.js';

export type { AuthConfig } from './middleware/auth.js';
export type { OidcConfig } from './auth/index.js';

/**
 * Server configuration options.
 *
 * Must specify exactly one of:
 * - reposDir: Multi-repo mode - serves multiple repositories from subdirectories
 * - singleRepoPath: Single-repo mode - serves a single repository at /repos/default
 */
export interface ServerConfig {
  /** Directory containing repositories (multi-repo mode) */
  reposDir?: string;
  /** Path to a single repository (single-repo mode, access via /repos/default) */
  singleRepoPath?: string;
  /** HTTP port (default: 3000) */
  port?: number;
  /** Bind address (default: "localhost") */
  host?: string;
  /** Enable CORS for cross-origin requests (default: false) */
  cors?: boolean;
  /** Optional JWT authentication config (for external JWKS validation) */
  auth?: AuthConfig;
  /** Optional OIDC provider config (enables built-in auth server) */
  oidc?: OidcConfig;
}

/**
 * Server instance handle.
 */
export interface Server {
  /** Start the server */
  start(): Promise<void>;
  /** Stop the server */
  stop(): Promise<void>;
  /** The underlying HTTP server */
  readonly httpServer: ServerType;
  /** The port the server is listening on */
  readonly port: number;
}

/**
 * Create an e3 API server.
 *
 * The server operates in multi-repo mode, serving multiple repositories
 * from subdirectories of the configured reposDir.
 *
 * URL structure:
 * - GET /api/repos - List available repositories
 * - /api/repos/:repo/... - Repository-specific endpoints
 *
 * @param config - Server configuration
 * @returns Server instance
 */
export async function createServer(config: ServerConfig): Promise<Server> {
  const { reposDir, singleRepoPath, port = 3000, host = 'localhost', cors: enableCors = false, auth, oidc } = config;

  // Validate config: exactly one of reposDir or singleRepoPath must be specified
  if (reposDir && singleRepoPath) {
    throw new Error('Cannot specify both reposDir and singleRepoPath');
  }
  if (!reposDir && !singleRepoPath) {
    throw new Error('Must specify either reposDir or singleRepoPath');
  }

  const isSingleRepoMode = !!singleRepoPath;

  // Single storage instance shared across all requests
  const storage: StorageBackend = new LocalStorage();

  // Helper to compute repo path from repo name
  // In single-repo mode, middleware validates 'default' before routes are called
  const getRepoPath = (repoName: string): string => {
    if (isSingleRepoMode) {
      // Middleware ensures repoName === 'default' before we get here
      return singleRepoPath!;
    }
    return path.join(reposDir!, repoName);
  };

  const app = new Hono();

  // Enable CORS if configured
  if (enableCors) {
    app.use('*', cors({ origin: '*' }));
  }

  // Create OIDC provider if configured (built-in auth server)
  let oidcProvider: OidcProvider | undefined;
  if (oidc) {
    oidcProvider = createOidcProvider(oidc);
    // Mount OIDC routes at root (/.well-known/*, /oauth2/*, /device)
    app.route('/', oidcProvider.routes);
  }

  // Apply auth middleware to all repo-specific routes if configured
  // If OIDC is enabled but auth is not separately configured, use OIDC keys for validation
  if (auth) {
    const authMiddleware = await createAuthMiddleware(auth);
    app.use('/api/repos/:repo/*', authMiddleware);
  } else if (oidcProvider) {
    // Use the OIDC provider's keys for JWT validation
    const authMiddleware = await createAuthMiddleware({
      jwksUrl: `${oidc!.baseUrl}/.well-known/jwks.json`,
      issuer: oidc!.baseUrl,
      audience: oidc!.baseUrl,
      // Provide keys directly to avoid HTTP fetch to self
      _internalKeys: oidcProvider.keys,
    });
    app.use('/api/repos/:repo/*', authMiddleware);
  }

  // Single-repo mode: validate repo name and handle disabled operations
  // Runs AFTER auth middleware (so unauthorized users get 401, not 404/405)
  if (isSingleRepoMode) {
    app.use('/api/repos/:repo/*', async (c, next) => {
      const method = c.req.method;

      // PUT (create repo) is always disabled in single-repo mode
      if (method === 'PUT') {
        return c.json({
          error: 'method_not_allowed',
          message: 'Repository creation is disabled in single-repo mode'
        }, 405);
      }

      // For DELETE (remove repo), check if it's the 'default' repo
      if (method === 'DELETE') {
        // DELETE on 'default' → 405 (deletion disabled)
        // DELETE on other repos → 404 (repo doesn't exist)
        const repo = c.req.param('repo');
        if (repo === 'default') {
          return c.json({
            error: 'method_not_allowed',
            message: 'Repository deletion is disabled in single-repo mode'
          }, 405);
        }
        return c.json({ error: 'not_found', message: `Repository '${repo}' not found` }, 404);
      }

      // For other methods (GET, POST, etc.), validate repo name
      const repo = c.req.param('repo');
      if (repo !== 'default') {
        return c.json({ error: 'not_found', message: `Repository '${repo}' not found` }, 404);
      }
      await next();
    });
  }

  // Validate repository exists before processing requests (multi-repo mode only)
  // In single-repo mode, this is handled by the middleware above
  // Skip validation for PUT/DELETE on /api/repos/:repo (repo create/remove)
  // Skip validation for /api/repos/:repo/delete/* (repo deletion status - repo may already be deleted)
  if (!isSingleRepoMode) {
    app.use('/api/repos/:repo/*', async (c, next) => {
      // Skip validation for repo create/remove operations at the repo level
      // These operate on repos that may not exist yet (PUT) or are being deleted (DELETE)
      const method = c.req.method;
      const path = c.req.path;
      // Check if this is the base repo path (no subpath after repo name)
      const repoPathMatch = path.match(/^\/api\/repos\/[^/]+$/);
      if (repoPathMatch && (method === 'PUT' || method === 'DELETE')) {
        await next();
        return;
      }

      // Skip validation for delete status endpoint (repo may already be deleted)
      const deleteStatusMatch = path.match(/^\/api\/repos\/[^/]+\/delete\/[^/]+$/);
      if (deleteStatusMatch) {
        await next();
        return;
      }

      const repo = c.req.param('repo')!;
      const repoPath = getRepoPath(repo);

      try {
        await storage.validateRepository(repoPath);
      } catch (err) {
        if (err instanceof RepositoryNotFoundError) {
          return sendError(NullType, variant('repository_not_found', { repo }));
        }
        throw err;
      }

      await next();
    });
  }

  // GET /api/repos - List available repositories
  app.get('/api/repos', async (c) => {
    if (isSingleRepoMode) {
      return c.json(['default']);
    }
    return listRepos(reposDir!);
  });

  // PUT /api/repos/:repo - Create a new repository (multi-repo mode only)
  // Note: Single-repo mode handler is registered earlier and takes precedence
  if (!isSingleRepoMode) {
    app.put('/api/repos/:repo', (c) => {
      const repo = c.req.param('repo');
      const repoPath = path.join(reposDir!, repo);
      const result = repoInit(repoPath);

      if (!result.success) {
        if (result.alreadyExists) {
          return sendError(StringType, variant('internal', { message: `Repository '${repo}' already exists` }));
        }
        return sendError(StringType, variant('internal', { message: result.error?.message ?? 'Unknown error' }));
      }

      return sendSuccessWithStatus(StringType, repo, 201);
    });

    // DELETE /api/repos/:repo - Remove a repository (async, multi-repo mode only)
    app.delete('/api/repos/:repo', (c) => {
      const repo = c.req.param('repo');
      const repoPath = path.join(reposDir!, repo);
      return startRepoDelete(repoPath);
    });

    // GET /api/repos/:repo/delete/:executionId - Get repo delete status
    app.get('/api/repos/:repo/delete/:executionId', (c) => {
      const executionId = c.req.param('executionId')!;
      return getRepoDeleteStatus(executionId);
    });
  }

  // Mount repository-specific routes
  // Each route file creates a sub-app that uses getRepoPath to resolve the repo

  // Repository status and GC: /api/repos/:repo/status, /api/repos/:repo/gc
  app.route('/api/repos/:repo', createRepositoryRoutes(storage, getRepoPath));

  // Package routes: /api/repos/:repo/packages/*
  app.route('/api/repos/:repo/packages', createPackageRoutes(storage, getRepoPath));

  // Workspace routes: /api/repos/:repo/workspaces/*
  app.route('/api/repos/:repo/workspaces', createWorkspaceRoutes(storage, getRepoPath));

  // Dataset routes: /api/repos/:repo/workspaces/:ws/datasets/*
  app.route('/api/repos/:repo/workspaces/:ws/datasets', createDatasetRoutes(storage, getRepoPath));

  // Task routes: /api/repos/:repo/workspaces/:ws/tasks/*
  app.route('/api/repos/:repo/workspaces/:ws/tasks', createTaskRoutes(storage, getRepoPath));

  // Execution/Dataflow routes: /api/repos/:repo/workspaces/:ws/dataflow/*
  app.route('/api/repos/:repo/workspaces/:ws/dataflow', createExecutionRoutes(storage, getRepoPath));

  let httpServer: ServerType | null = null;
  let actualPort = port;

  const server: Server = {
    async start() {
      return new Promise((resolve) => {
        httpServer = serve({
          fetch: app.fetch,
          port,
          hostname: host,
        }, (info) => {
          actualPort = info.port;
          resolve();
        });
      });
    },

    async stop() {
      return new Promise((resolve, reject) => {
        if (!httpServer) {
          resolve();
          return;
        }
        // Force close all connections immediately
        (httpServer as unknown as { closeAllConnections(): void }).closeAllConnections();
        httpServer.close((err) => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        });
      });
    },

    get httpServer() {
      if (!httpServer) {
        throw new Error('Server not started');
      }
      return httpServer;
    },

    get port() {
      return actualPort;
    },
  };

  return server;
}
