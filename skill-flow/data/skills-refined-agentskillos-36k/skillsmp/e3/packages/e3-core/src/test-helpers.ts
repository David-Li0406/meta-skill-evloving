/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Test helpers for e3-core
 * Provides utilities for setting up and tearing down test repositories
 */

import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import yauzl from 'yauzl';
import { repoInit } from './repository.js';

/**
 * Creates a temporary directory for testing
 * @returns Path to temporary directory
 */
export function createTempDir(): string {
  return mkdtempSync(join(tmpdir(), 'e3-test-'));
}

/**
 * Removes a temporary directory and all its contents
 * @param dir Path to directory to remove
 */
export function removeTempDir(dir: string): void {
  rmSync(dir, { recursive: true, force: true });
}

/**
 * Creates a temporary e3 repository for testing
 * @returns Path to the repository directory
 */
export function createTestRepo(): string {
  const dir = createTempDir();
  const result = repoInit(dir);
  if (!result.success) {
    throw new Error(`Failed to create test repository: ${result.error?.message}`);
  }
  return result.repoPath;
}

/**
 * Remove a test repository
 * @param repoPath Path to repository directory
 */
export function removeTestRepo(repoPath: string): void {
  removeTempDir(repoPath);
}

/**
 * Read all entries from a zip file
 * @param zipPath Path to zip file
 * @returns Map of entry path to content buffer
 */
export async function readZipEntries(zipPath: string): Promise<Map<string, Buffer>> {
  return new Promise((resolve, reject) => {
    yauzl.open(zipPath, { lazyEntries: true }, (err, zipfile) => {
      if (err) return reject(err);
      if (!zipfile) return reject(new Error('No zipfile'));

      const entries = new Map<string, Buffer>();
      zipfile.readEntry();

      zipfile.on('entry', (entry) => {
        if (/\/$/.test(entry.fileName)) {
          // Directory entry, skip
          zipfile.readEntry();
        } else {
          zipfile.openReadStream(entry, (err, readStream) => {
            if (err) return reject(err);
            if (!readStream) return reject(new Error('No read stream'));

            const chunks: Buffer[] = [];
            readStream.on('data', (chunk) => chunks.push(chunk));
            readStream.on('end', () => {
              entries.set(entry.fileName, Buffer.concat(chunks));
              zipfile.readEntry();
            });
          });
        }
      });

      zipfile.on('end', () => resolve(entries));
      zipfile.on('error', reject);
    });
  });
}

/**
 * Compare two zip files for content equality.
 * Returns true if both zips have the same entries with the same content.
 * Does not compare timestamps or other metadata.
 *
 * @param zipPath1 Path to first zip file
 * @param zipPath2 Path to second zip file
 * @returns Object with equal flag and optional diff info
 */
export async function zipEqual(
  zipPath1: string,
  zipPath2: string
): Promise<{ equal: boolean; diff?: string }> {
  const entries1 = await readZipEntries(zipPath1);
  const entries2 = await readZipEntries(zipPath2);

  // Check for missing entries
  const keys1 = Array.from(entries1.keys()).sort();
  const keys2 = Array.from(entries2.keys()).sort();

  if (keys1.length !== keys2.length) {
    return {
      equal: false,
      diff: `Entry count differs: ${keys1.length} vs ${keys2.length}`,
    };
  }

  for (let i = 0; i < keys1.length; i++) {
    if (keys1[i] !== keys2[i]) {
      return {
        equal: false,
        diff: `Entry paths differ at index ${i}: ${keys1[i]} vs ${keys2[i]}`,
      };
    }
  }

  // Check content equality
  for (const [path, data1] of entries1) {
    const data2 = entries2.get(path)!;
    if (!data1.equals(data2)) {
      return {
        equal: false,
        diff: `Content differs at ${path}: ${data1.length} bytes vs ${data2.length} bytes`,
      };
    }
  }

  return { equal: true };
}
