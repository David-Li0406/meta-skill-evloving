/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * CLI utilities for path parsing and resolution
 */

import { resolve } from 'path';
import { repoGet } from '@elaraai/e3-core';
import { parseDatasetPath, parsePackageRef } from '@elaraai/e3-types';
import { getValidToken } from './credentials.js';

// Re-export for convenience
export { parseDatasetPath, parsePackageRef };

/**
 * Repository location - either local filesystem or remote URL.
 */
export type RepoLocation =
  | { type: 'local'; path: string }
  | { type: 'remote'; baseUrl: string; repo: string; token: string };

/**
 * Parse a repository location argument.
 *
 * Supports:
 * - Local paths: `.`, `./repo`, `/path/to/repo`
 * - Remote URLs: `http://...`, `https://...`
 *
 * For remote URLs, the URL should be the user-facing "shareable" URL,
 * e.g., `https://platform.example.com/repos/my_repo`.
 * The CLI will internally add `/api` when making API calls.
 *
 * For remote locations, this function will load and validate the auth token.
 * If not logged in or token is expired and cannot be refreshed, throws an error.
 *
 * @returns For local: { type: 'local', path: '/absolute/path/to/repo' }
 *          For remote: { type: 'remote', baseUrl: 'https://example.com', repo: 'my_repo', token: '...' }
 */
export async function parseRepoLocation(arg: string): Promise<RepoLocation> {
  if (arg.startsWith('https://') || arg.startsWith('http://')) {
    const url = new URL(arg);

    // Extract repo name from path: /repos/{repo}[/...]
    const match = url.pathname.match(/^\/repos\/([^/]+)/);
    if (!match) {
      throw new Error(`Invalid remote URL: expected /repos/{repo} in path, got ${url.pathname}`);
    }

    // Load and validate token
    const token = await getValidToken(url.origin);

    return {
      type: 'remote',
      baseUrl: url.origin,
      repo: match[1],
      token,
    };
  }
  return { type: 'local', path: resolveRepo(arg) };
}

/**
 * Repository location without required token (for sync parsing).
 */
export type RepoLocationNoToken =
  | { type: 'local'; path: string }
  | { type: 'remote'; baseUrl: string; repo: string };

/**
 * Parse a repository location (synchronous, no auth).
 *
 * Use this only for operations that don't need authentication (e.g., local repos).
 * For remote repos, use parseRepoLocation() instead.
 */
export function parseRepoLocationSync(arg: string): RepoLocationNoToken {
  if (arg.startsWith('https://') || arg.startsWith('http://')) {
    const url = new URL(arg);
    const match = url.pathname.match(/^\/repos\/([^/]+)/);
    if (!match) {
      throw new Error(`Invalid remote URL: expected /repos/{repo} in path, got ${url.pathname}`);
    }
    return {
      type: 'remote',
      baseUrl: url.origin,
      repo: match[1],
    };
  }
  return { type: 'local', path: resolveRepo(arg) };
}

/**
 * Resolve repository path from CLI argument.
 * Supports `.` for current directory and relative/absolute paths.
 */
export function resolveRepo(repoArg: string): string {
  const absolutePath = resolve(repoArg);
  return repoGet(absolutePath);
}

/**
 * Parse package specification: name[@version]
 * Returns { name, version } where version defaults to 'latest' if not specified.
 */
export function parsePackageSpec(spec: string): { name: string; version: string } {
  const { name, version } = parsePackageRef(spec);
  return { name, version: version ?? 'latest' };
}

/**
 * Format error for CLI output.
 */
export function formatError(err: unknown): string {
  if (err instanceof Error) {
    return err.message;
  }
  return String(err);
}

/**
 * Exit with error message.
 */
export function exitError(message: string): never {
  console.error(`Error: ${message}`);
  process.exit(1);
}
