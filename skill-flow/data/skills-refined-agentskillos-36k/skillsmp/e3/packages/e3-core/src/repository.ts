/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'fs';
import * as path from 'path';

/**
 * Result of initializing an e3 repository
 */
export interface InitRepositoryResult {
  success: boolean;
  repoPath: string;
  error?: Error;
  alreadyExists?: boolean;
}

/**
 * Initialize a new e3 repository
 *
 * Creates the repository directory structure:
 * - objects/
 * - packages/
 * - executions/
 * - workspaces/
 *
 * The repository IS the specified directory - subdirectories are created directly within it.
 *
 * Pure business logic - no UI dependencies
 */
export function repoInit(repoPath: string): InitRepositoryResult {
  const targetPath = path.resolve(repoPath);

  // Check if directory already is a valid repository
  if (isValidRepository(targetPath)) {
    return {
      success: false,
      repoPath: targetPath,
      alreadyExists: true,
      error: new Error(`e3 repository already exists at ${targetPath}`),
    };
  }

  try {
    // Create the repository directory if it doesn't exist
    fs.mkdirSync(targetPath, { recursive: true });

    // Create objects directory (content-addressed storage)
    fs.mkdirSync(path.join(targetPath, 'objects'), { recursive: true });

    // Create packages directory (package refs: packages/<name>/<version> -> hash)
    fs.mkdirSync(path.join(targetPath, 'packages'), { recursive: true });

    // Create executions directory (execution cache: executions/<hash>/output -> hash)
    fs.mkdirSync(path.join(targetPath, 'executions'), { recursive: true });

    // Create workspaces directory (workspace state)
    fs.mkdirSync(path.join(targetPath, 'workspaces'), { recursive: true });

    return {
      success: true,
      repoPath: targetPath,
    };
  } catch (error) {
    return {
      success: false,
      repoPath: targetPath,
      error: error instanceof Error ? error : new Error(String(error)),
    };
  }
}

/**
 * Validate that a directory is a valid e3 repository
 * @internal
 */
function isValidRepository(repoPath: string): boolean {
  const requiredDirs = ['objects', 'packages', 'executions', 'workspaces'];

  return requiredDirs.every((dir) => fs.existsSync(path.join(repoPath, dir)));
}

/**
 * Find the e3 repository directory
 *
 * Checks:
 * 1. E3_REPO environment variable
 * 2. The provided startPath (if given)
 *
 * Returns null if no valid repository is found.
 */
export function repoFind(startPath?: string): string | null {
  // 1. Check E3_REPO environment variable
  if (process.env.E3_REPO) {
    const repoPath = path.resolve(process.env.E3_REPO);
    if (fs.existsSync(repoPath) && isValidRepository(repoPath)) {
      return repoPath;
    }
  }

  // 2. Check the provided path
  if (startPath !== undefined) {
    const repoPath = path.resolve(startPath);
    if (fs.existsSync(repoPath) && isValidRepository(repoPath)) {
      return repoPath;
    }
  }

  return null;
}

/**
 * Get the e3 repository, throw error if not found
 */
export function repoGet(repoPath?: string): string {
  const repo = repoFind(repoPath);

  if (!repo) {
    throw new Error('e3 repository not found. Run `e3 repo create` to create one.');
  }

  return repo;
}
