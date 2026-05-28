/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { ArrayType, StringType } from '@elaraai/east';
import { sendSuccess, sendError } from '../beast2.js';
import { errorToVariant } from '../errors.js';

/**
 * Check if a directory is a valid e3 repository.
 * A valid repository has objects, packages, executions, and workspaces subdirectories.
 */
async function isValidRepository(repoPath: string): Promise<boolean> {
  const requiredDirs = ['objects', 'packages', 'executions', 'workspaces'];

  for (const dir of requiredDirs) {
    try {
      const stat = await fs.stat(path.join(repoPath, dir));
      if (!stat.isDirectory()) {
        return false;
      }
    } catch {
      return false;
    }
  }

  return true;
}

/**
 * List available repositories in the repos directory.
 *
 * Scans the directory for subdirectories that are valid e3 repositories.
 */
export async function listRepos(reposDir: string): Promise<Response> {
  try {
    const entries = await fs.readdir(reposDir, { withFileTypes: true });
    const repos: string[] = [];

    for (const entry of entries) {
      if (entry.isDirectory()) {
        const repoPath = path.join(reposDir, entry.name);
        if (await isValidRepository(repoPath)) {
          repos.push(entry.name);
        }
      }
    }

    return sendSuccess(ArrayType(StringType), repos);
  } catch (err) {
    return sendError(ArrayType(StringType), errorToVariant(err));
  }
}
