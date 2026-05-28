/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Authentication commands for e3 CLI.
 */

import { Command } from 'commander';
import {
  fetchDiscovery,
  startDeviceAuth,
  pollForTokens,
  setCredential,
  removeCredential,
  listCredentials,
  getCredential,
  getValidToken,
  isExpired,
  decodeJwtPayload,
  normalizeServerUrl,
  type CredentialEntry,
} from '../credentials.js';

/**
 * Try to open a URL in the default browser.
 */
async function openBrowser(url: string): Promise<boolean> {
  const { exec } = await import('node:child_process');
  const { platform } = await import('node:os');

  return new Promise((resolve) => {
    let command: string;
    switch (platform()) {
      case 'darwin':
        command = `open "${url}"`;
        break;
      case 'win32':
        command = `start "" "${url}"`;
        break;
      default:
        command = `xdg-open "${url}"`;
    }

    exec(command, (error) => {
      resolve(!error);
    });
  });
}

/**
 * Create the auth command group.
 */
export function createAuthCommand(): Command {
  const auth = new Command('auth')
    .description('Authentication commands');

  // e3 auth status - List all saved credentials
  auth
    .command('status')
    .description('List saved credentials')
    .action(() => {
      const creds = listCredentials();
      if (creds.length === 0) {
        console.log('No saved credentials.');
        console.log('Run: e3 login <server>');
        return;
      }

      console.log('Saved credentials:\n');
      for (const { server, expiresAt } of creds) {
        const expired = isExpired(expiresAt);
        const status = expired ? '(expired)' : '(valid)';
        console.log(`  ${server} ${status}`);
        console.log(`    Token expires: ${expiresAt}`);
      }
    });

  // e3 auth token <server> - Print access token for use with curl
  auth
    .command('token')
    .description('Print access token for a server (for curl/debugging)')
    .argument('<server>', 'Server URL')
    .action(async (server: string) => {
      const serverUrl = normalizeServerUrl(server);
      try {
        // getValidToken handles refresh automatically if token is expired
        const token = await getValidToken(serverUrl);
        // Print just the token, suitable for: curl -H "Authorization: Bearer $(e3 auth token <server>)"
        console.log(token);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'unknown error';
        console.error(message);
        process.exit(1);
      }
    });

  // e3 auth whoami [server] - Show current identity
  auth
    .command('whoami')
    .description('Show current identity')
    .argument('[server]', 'Server URL')
    .action((server?: string) => {
      const creds = listCredentials();
      if (creds.length === 0) {
        console.log('Not logged in to any servers.');
        return;
      }

      const servers = server ? [server] : creds.map((c) => c.server);
      for (const serverUrl of servers) {
        const credential = getCredential(serverUrl);
        if (!credential) {
          console.log(`${serverUrl}: Not logged in`);
          continue;
        }

        try {
          const payload = decodeJwtPayload(credential.accessToken);
          const expired = isExpired(credential.expiresAt);
          const status = expired ? '(token expired)' : '';
          console.log(`${serverUrl}: ${status}`);
          console.log(`  Subject: ${payload.sub ?? 'unknown'}`);
          if (payload.email) {
            console.log(`  Email: ${payload.email}`);
          }
          console.log(`  Issuer: ${payload.iss ?? 'unknown'}`);
        } catch {
          console.log(`${serverUrl}: Invalid token`);
        }
      }
    });

  return auth;
}

/**
 * Create the login command.
 */
export function createLoginCommand(): Command {
  return new Command('login')
    .description('Log in to a server using OAuth2 Device Flow')
    .argument('<server>', 'Server URL (e.g., http://localhost:3000)')
    .option('--no-browser', 'Do not open browser (for CI/headless environments)')
    .action(async (server: string, options: { browser: boolean }) => {
      const serverUrl = normalizeServerUrl(server);

      console.log(`Logging in to ${serverUrl}...`);

      // Fetch OIDC discovery document
      let discovery;
      try {
        discovery = await fetchDiscovery(serverUrl);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'unknown error';
        console.error(`Failed to connect to server: ${message}`);
        console.error('Make sure the server is running with --oidc enabled.');
        process.exit(1);
      }

      // Start device authorization
      let deviceAuth;
      try {
        deviceAuth = await startDeviceAuth(discovery);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'unknown error';
        console.error(`Failed to start login: ${message}`);
        process.exit(1);
      }

      // Display user code and URL (unless in quiet CI mode)
      if (options.browser) {
        console.log('\nTo complete login:');
        console.log(`  1. Open: ${deviceAuth.verification_uri}`);
        console.log(`  2. Enter code: ${deviceAuth.user_code}`);
        console.log(`\nOr visit this URL directly:`);
        console.log(`  ${deviceAuth.verification_uri_complete}`);

        // Try to open browser
        const opened = await openBrowser(deviceAuth.verification_uri_complete);
        if (opened) {
          console.log('\nBrowser opened. Waiting for approval...');
        } else {
          console.log('\nWaiting for approval...');
        }
      } else {
        console.log('Waiting for server approval (--no-browser mode)...');
      }

      // Poll for tokens
      try {
        const tokens = await pollForTokens(
          discovery,
          deviceAuth.device_code,
          deviceAuth.interval,
          deviceAuth.expires_in
        );

        // Save credentials
        const entry: CredentialEntry = {
          accessToken: tokens.access_token,
          refreshToken: tokens.refresh_token,
          expiresAt: new Date(Date.now() + tokens.expires_in * 1000).toISOString(),
        };
        setCredential(serverUrl, entry);

        // Show identity
        const payload = decodeJwtPayload(tokens.access_token);
        console.log(`\nSuccessfully logged in as: ${payload.sub ?? 'unknown'}`);
        console.log(`Token expires: ${entry.expiresAt}`);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'unknown error';
        console.error(`\nLogin failed: ${message}`);
        process.exit(1);
      }
    });
}

/**
 * Create the logout command.
 */
export function createLogoutCommand(): Command {
  return new Command('logout')
    .description('Log out from a server')
    .argument('<server>', 'Server URL')
    .action((server: string) => {
      const serverUrl = normalizeServerUrl(server);
      const removed = removeCredential(serverUrl);
      if (removed) {
        console.log(`Logged out from ${serverUrl}`);
      } else {
        console.log(`Not logged in to ${serverUrl}`);
      }
    });
}
