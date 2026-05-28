#!/usr/bin/env node
/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { Command } from 'commander';
import { createServer } from './server.js';

const program = new Command();

program
  .name('e3-api-server')
  .description('HTTP server for e3 repositories')
  .version('0.0.1-beta.0')
  .option('--repos <dir>', 'Directory containing e3 repositories (multi-repo mode)')
  .option('--repo <path>', 'Path to a single repository (single-repo mode, access via /repos/default)')
  .option('-p, --port <port>', 'HTTP port', '3000')
  .option('-H, --host <host>', 'Bind address', 'localhost')
  .option('--cors', 'Enable CORS')
  .option('--oidc', 'Enable built-in OIDC authentication provider')
  .option('--token-expiry <duration>', 'Access token expiry (e.g., "5s", "15m", "1h")', '1h')
  .option('--refresh-token-expiry <duration>', 'Refresh token expiry (e.g., "1h", "7d", "90d")', '90d')
  .option('--auth-key <path>', 'JWT public key path (external auth)')
  .option('--auth-issuer <iss>', 'Expected JWT issuer (external auth)')
  .option('--auth-audience <aud>', 'Expected JWT audience (external auth)')
  .action(async (options: {
    repos?: string;
    repo?: string;
    port: string;
    host: string;
    cors?: boolean;
    oidc?: boolean;
    tokenExpiry: string;
    refreshTokenExpiry: string;
    authKey?: string;
    authIssuer?: string;
    authAudience?: string;
  }) => {
    // Validate mutually exclusive options
    if (options.repos && options.repo) {
      console.error('Error: Cannot specify both --repos and --repo');
      process.exit(1);
    }
    if (!options.repos && !options.repo) {
      console.error('Error: Must specify either --repos or --repo');
      process.exit(1);
    }

    const port = parseInt(options.port, 10);
    const host = options.host;

    // Build auth config if all auth options provided (external provider)
    const auth = options.authKey && options.authIssuer && options.authAudience
      ? {
          publicKeyPath: options.authKey,
          issuer: options.authIssuer,
          audience: options.authAudience,
        }
      : undefined;

    // Build OIDC config if enabled (built-in provider)
    const oidc = options.oidc
      ? {
          baseUrl: `http://${host}:${port}`,
          tokenExpiry: options.tokenExpiry,
          refreshTokenExpiry: options.refreshTokenExpiry,
        }
      : undefined;

    const server = await createServer({
      reposDir: options.repos,
      singleRepoPath: options.repo,
      port,
      host,
      cors: options.cors,
      auth,
      oidc,
    });

    await server.start();
    console.log(`e3-api-server listening on http://${host}:${server.port}`);
    if (options.repos) {
      console.log(`Serving repositories from: ${options.repos}`);
    } else {
      console.log(`Serving single repository from: ${options.repo}`);
      console.log(`Access via: http://${host}:${server.port}/repos/default`);
    }
    if (oidc) {
      console.log(`OIDC provider enabled (token expiry: ${options.tokenExpiry})`);
      if (process.env.E3_AUTH_AUTO_APPROVE === '1') {
        console.log('  Auto-approve mode enabled (E3_AUTH_AUTO_APPROVE=1)');
      }
    }

    // Handle shutdown signals
    const shutdown = async () => {
      console.log('\nShutting down...');
      await server.stop();
      process.exit(0);
    };

    process.on('SIGINT', () => void shutdown());
    process.on('SIGTERM', () => void shutdown());
  });

program.parse();
