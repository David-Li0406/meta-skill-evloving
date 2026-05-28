/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Garbage collection for e3 repositories.
 *
 * Uses mark-and-sweep algorithm:
 * 1. Mark: Find all root refs (packages, executions, workspaces) and trace reachable objects
 * 2. Sweep: Delete unreachable objects and orphaned staging files
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { decodeBeast2For } from '@elaraai/east';
import { WorkspaceStateType } from '@elaraai/e3-types';
import type { StorageBackend } from './storage/interfaces.js';
import { LocalStorage } from './storage/local/index.js';

/**
 * Options for garbage collection
 */
export interface GcOptions {
  /**
   * Minimum age in milliseconds for files to be considered for deletion.
   * Files younger than this are skipped to avoid race conditions with concurrent writes.
   * Default: 60000 (1 minute)
   */
  minAge?: number;

  /**
   * If true, only report what would be deleted without actually deleting.
   * Default: false
   */
  dryRun?: boolean;
}

/**
 * Result of garbage collection
 */
export interface GcResult {
  /**
   * Number of objects deleted
   */
  deletedObjects: number;

  /**
   * Number of orphaned staging files deleted
   */
  deletedPartials: number;

  /**
   * Number of objects retained
   */
  retainedObjects: number;

  /**
   * Number of files skipped due to being too young
   */
  skippedYoung: number;

  /**
   * Total bytes freed
   */
  bytesFreed: number;
}

/**
 * Run garbage collection on an e3 repository.
 *
 * Note: GC currently requires LocalStorage as it needs direct filesystem access
 * to enumerate and delete unreachable objects. Cloud backends will need their
 * own GC implementation (e.g., using S3 lifecycle policies).
 *
 * @param storage - Storage backend (must be LocalStorage)
 * @param repo - Repository identifier (for local storage, the path to e3 repository directory)
 * @param options - GC options
 * @returns GC result with statistics
 * @throws Error if storage is not a LocalStorage
 */
export async function repoGc(
  storage: StorageBackend,
  repo: string,
  options: GcOptions = {}
): Promise<GcResult> {
  // GC requires direct filesystem access - verify we have LocalStorage
  if (!(storage instanceof LocalStorage)) {
    throw new Error('GC is only supported with LocalStorage storage');
  }

  const minAge = options.minAge ?? 60000; // Default 1 minute
  const dryRun = options.dryRun ?? false;
  const now = Date.now();

  // Step 1: Collect all root hashes
  const roots = await collectRoots(repo);

  // Step 2: Mark all reachable objects starting from roots
  const reachable = new Set<string>();
  for (const root of roots) {
    await markReachable(storage, repo, root, reachable);
  }

  // Step 3: Sweep - enumerate all objects and delete unreachable ones
  const result = await sweep(repo, reachable, minAge, now, dryRun);

  return result;
}

/**
 * Collect all root hashes from refs in packages, executions, and workspaces.
 */
async function collectRoots(repoPath: string): Promise<Set<string>> {
  const roots = new Set<string>();

  // Collect from packages/<name>/<version> files
  const packagesDir = path.join(repoPath, 'packages');
  await collectRefsFromDir(packagesDir, roots, 2); // depth 2: packages/<name>/<version>

  // Collect from executions/<taskHash>/<inputsHash>/output files
  const executionsDir = path.join(repoPath, 'executions');
  await collectRefsFromDir(executionsDir, roots, 3); // depth 3: executions/<taskHash>/<inputsHash>/output

  // Collect from workspaces/<name>/state.beast2 files
  const workspacesDir = path.join(repoPath, 'workspaces');
  await collectWorkspaceRoots(workspacesDir, roots);

  return roots;
}

/**
 * Collect root hashes from workspace state files.
 */
async function collectWorkspaceRoots(
  workspacesDir: string,
  roots: Set<string>
): Promise<void> {
  try {
    const entries = await fs.readdir(workspacesDir);

    for (const entry of entries) {
      if (!entry.endsWith('.beast2')) continue;

      const stateFile = path.join(workspacesDir, entry);
      try {
        const data = await fs.readFile(stateFile);
        // Skip empty files (undeployed workspaces)
        if (data.length === 0) continue;

        const decoder = decodeBeast2For(WorkspaceStateType);
        const state = decoder(data);

        // Add both the package hash and root hash as roots
        roots.add(state.packageHash);
        roots.add(state.rootHash);
      } catch {
        // State file can't be parsed - skip
      }
    }
  } catch {
    // Workspaces directory doesn't exist
  }
}

/**
 * Recursively collect hashes from ref files in a directory.
 *
 * @param dir - Directory to scan
 * @param roots - Set to add found hashes to
 * @param maxDepth - Maximum depth to traverse
 */
async function collectRefsFromDir(
  dir: string,
  roots: Set<string>,
  maxDepth: number,
  currentDepth: number = 0
): Promise<void> {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const entryPath = path.join(dir, entry.name);

      if (entry.isDirectory() && currentDepth < maxDepth) {
        await collectRefsFromDir(entryPath, roots, maxDepth, currentDepth + 1);
      } else if (entry.isFile()) {
        // Read the ref file - it contains a hash
        try {
          const content = await fs.readFile(entryPath, 'utf-8');
          const hash = content.trim();
          // Validate it looks like a SHA256 hash
          if (/^[a-f0-9]{64}$/.test(hash)) {
            roots.add(hash);
          }
        } catch {
          // Skip files we can't read
        }
      }
    }
  } catch {
    // Directory doesn't exist or can't be read - that's fine
  }
}

/**
 * Mark all objects reachable from a root hash.
 *
 * Traverses the object graph by scanning for hash patterns in the data.
 */
async function markReachable(
  storage: StorageBackend,
  repo: string,
  hash: string,
  reachable: Set<string>
): Promise<void> {
  // Already visited?
  if (reachable.has(hash)) {
    return;
  }

  // Try to load the object
  try {
    const data = await storage.objects.read(repo, hash);
    reachable.add(hash);

    // Scan for hash patterns in the data
    const dataStr = Buffer.from(data).toString('latin1');
    const hashPattern = /[a-f0-9]{64}/g;
    const matches = dataStr.matchAll(hashPattern);

    for (const match of matches) {
      const potentialHash = match[0];
      if (!reachable.has(potentialHash)) {
        // Recursively mark if it exists
        await markReachable(storage, repo, potentialHash, reachable);
      }
    }
  } catch {
    // Object doesn't exist - not an error, just means this hash
    // wasn't actually a reference to an object
  }
}

/**
 * Sweep unreachable objects and orphaned staging files.
 */
async function sweep(
  repoPath: string,
  reachable: Set<string>,
  minAge: number,
  now: number,
  dryRun: boolean
): Promise<GcResult> {
  const objectsDir = path.join(repoPath, 'objects');
  const result: GcResult = {
    deletedObjects: 0,
    deletedPartials: 0,
    retainedObjects: 0,
    skippedYoung: 0,
    bytesFreed: 0,
  };

  try {
    // Iterate through objects/xx/ directories
    const subdirs = await fs.readdir(objectsDir);

    for (const subdir of subdirs) {
      // Skip if not a 2-char hex directory
      if (!/^[a-f0-9]{2}$/.test(subdir)) {
        continue;
      }

      const subdirPath = path.join(objectsDir, subdir);
      const stat = await fs.stat(subdirPath);
      if (!stat.isDirectory()) {
        continue;
      }

      const files = await fs.readdir(subdirPath);

      for (const file of files) {
        const filePath = path.join(subdirPath, file);

        try {
          const fileStat = await fs.stat(filePath);

          // Check age - skip young files to avoid race with concurrent writes
          // Note: age can be negative if file was written after 'now' was captured
          const age = now - fileStat.mtimeMs;
          if (minAge > 0 && age < minAge) {
            result.skippedYoung++;
            continue;
          }

          // Handle .partial staging files
          if (file.endsWith('.partial')) {
            if (!dryRun) {
              await fs.unlink(filePath);
            }
            result.deletedPartials++;
            result.bytesFreed += fileStat.size;
            continue;
          }

          // Handle .beast2 object files
          if (file.endsWith('.beast2')) {
            // Reconstruct the hash: subdir (2 chars) + filename without extension
            const hash = subdir + file.slice(0, -7); // -7 removes '.beast2'

            if (reachable.has(hash)) {
              result.retainedObjects++;
            } else {
              if (!dryRun) {
                await fs.unlink(filePath);
              }
              result.deletedObjects++;
              result.bytesFreed += fileStat.size;
            }
          }
        } catch {
          // Skip files we can't stat or delete
        }
      }

      // Try to remove empty subdirectory
      if (!dryRun) {
        try {
          await fs.rmdir(subdirPath);
        } catch {
          // Directory not empty, that's fine
        }
      }
    }
  } catch {
    // Objects directory doesn't exist or can't be read
  }

  return result;
}
