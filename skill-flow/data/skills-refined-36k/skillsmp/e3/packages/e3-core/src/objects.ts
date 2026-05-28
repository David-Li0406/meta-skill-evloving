/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import * as crypto from 'crypto';
import { Readable } from 'stream';
import { pipeline } from 'stream/promises';
import { createWriteStream } from 'fs';
import { ObjectNotFoundError, isNotFoundError } from './errors.js';

/**
 * Calculate SHA256 hash of data
 */
export function computeHash(data: Uint8Array): string {
  return crypto.createHash('sha256').update(data).digest('hex');
}

/**
 * Calculate SHA256 hash of a stream
 * @internal
 */
async function computeHashFromStream(
  stream: ReadableStream<Uint8Array>
): Promise<{ hash: string; data: Uint8Array[] }> {
  const hash = crypto.createHash('sha256');
  const chunks: Uint8Array[] = [];

  const reader = stream.getReader();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    hash.update(value);
    chunks.push(value);
  }

  return {
    hash: hash.digest('hex'),
    data: chunks,
  };
}

/**
 * Atomically write an object to the repository
 *
 * @param repoPath - Path to e3 repository
 * @param data - Data to store
 * @returns SHA256 hash of the data
 */
export async function objectWrite(
  repoPath: string,
  data: Uint8Array
): Promise<string> {
  const extension = '.beast2';
  const hash = computeHash(data);

  // Split hash: first 2 chars as directory
  const dirName = hash.slice(0, 2);
  const fileName = hash.slice(2) + extension;

  const dirPath = path.join(repoPath, 'objects', dirName);
  const filePath = path.join(dirPath, fileName);

  // Check if already exists
  try {
    await fs.access(filePath);
    return hash; // Already exists
  } catch {
    // Doesn't exist, continue
  }

  // Create directory if needed
  await fs.mkdir(dirPath, { recursive: true });

  // Write atomically: stage in same directory (same filesystem) + rename
  // Staging files use .partial extension; gc can clean up any orphaned ones
  // Use random suffix to avoid collisions with concurrent writes
  const randomSuffix = Math.random().toString(36).slice(2, 10);
  const stagingPath = path.join(dirPath, `${fileName}.${Date.now()}.${randomSuffix}.partial`);
  await fs.writeFile(stagingPath, data);

  try {
    await fs.rename(stagingPath, filePath);
  } catch (err) {
    // If rename fails because target exists (concurrent write won), that's fine
    // Clean up our staging file
    try {
      await fs.unlink(stagingPath);
    } catch {
      // Ignore cleanup errors
    }
    // Verify the file exists (another writer should have created it)
    try {
      await fs.access(filePath);
    } catch {
      // File doesn't exist and rename failed - re-throw original error
      throw err;
    }
  }

  return hash;
}

/**
 * Atomically write a stream to the repository
 *
 * @param repoPath - Path to e3 repository
 * @param stream - Stream to store
 * @returns SHA256 hash of the data
 */
export async function objectWriteStream(
  repoPath: string,
  stream: ReadableStream<Uint8Array>
): Promise<string> {
  const extension = '.beast2';
  // First pass: compute hash while collecting data
  const { hash, data } = await computeHashFromStream(stream);

  // Split hash: first 2 chars as directory
  const dirName = hash.slice(0, 2);
  const fileName = hash.slice(2) + extension;

  const dirPath = path.join(repoPath, 'objects', dirName);
  const filePath = path.join(dirPath, fileName);

  // Check if already exists
  try {
    await fs.access(filePath);
    return hash; // Already exists
  } catch {
    // Doesn't exist, continue
  }

  // Create directory if needed
  await fs.mkdir(dirPath, { recursive: true });

  // Write atomically: stage in same directory (same filesystem) + rename
  // Staging files use .partial extension; gc can clean up any orphaned ones
  // Use random suffix to avoid collisions with concurrent writes
  const randomSuffix = Math.random().toString(36).slice(2, 10);
  const stagingPath = path.join(dirPath, `${fileName}.${Date.now()}.${randomSuffix}.partial`);

  // Reconstruct stream from collected chunks
  const nodeStream = Readable.from(data);
  const writeStream = createWriteStream(stagingPath);

  await pipeline(nodeStream, writeStream);

  try {
    await fs.rename(stagingPath, filePath);
  } catch (err) {
    // If rename fails because target exists (concurrent write won), that's fine
    // Clean up our staging file
    try {
      await fs.unlink(stagingPath);
    } catch {
      // Ignore cleanup errors
    }
    // Verify the file exists (another writer should have created it)
    try {
      await fs.access(filePath);
    } catch {
      // File doesn't exist and rename failed - re-throw original error
      throw err;
    }
  }

  return hash;
}

/**
 * Read an object from the repository
 *
 * @param repoPath - Path to e3 repository
 * @param hash - SHA256 hash of the object
 * @returns Object data
 * @throws {ObjectNotFoundError} If object not found
 */
export async function objectRead(
  repoPath: string,
  hash: string
): Promise<Uint8Array> {
  const extension = '.beast2';
  const dirName = hash.slice(0, 2);
  const fileName = hash.slice(2) + extension;

  const filePath = path.join(repoPath, 'objects', dirName, fileName);

  try {
    return await fs.readFile(filePath);
  } catch (err) {
    if (isNotFoundError(err)) {
      throw new ObjectNotFoundError(hash);
    }
    throw err;
  }
}

/**
 * Check if an object exists in the repository
 *
 * @param repoPath - Path to e3 repository
 * @param hash - SHA256 hash of the object
 * @returns true if object exists
 */
export async function objectExists(
  repoPath: string,
  hash: string
): Promise<boolean> {
  const filePath = objectPath(repoPath, hash);

  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Get the filesystem path for an object
 *
 * @param repoPath - Path to e3 repository
 * @param hash - SHA256 hash of the object
 * @returns Filesystem path: objects/<hash[0..2]>/<hash[2..]>.beast2
 */
export function objectPath(repoPath: string, hash: string): string {
  const dirName = hash.slice(0, 2);
  const fileName = hash.slice(2) + '.beast2';
  return path.join(repoPath, 'objects', dirName, fileName);
}

/**
 * Get the minimum unambiguous prefix length for an object hash.
 *
 * Scans the object store to find the shortest prefix of the given hash
 * that uniquely identifies it among all stored objects.
 *
 * @param repoPath - Path to e3 repository
 * @param hash - Full SHA256 hash of the object
 * @param minLength - Minimum prefix length to return (default: 4)
 * @returns Minimum unambiguous prefix length
 */
export async function objectAbbrev(
  repoPath: string,
  hash: string,
  minLength: number = 4
): Promise<number> {
  const objectsDir = path.join(repoPath, 'objects');
  const targetPrefix = hash.slice(0, 2);

  // Collect all hashes that share the same 2-char prefix directory
  const hashes: string[] = [];

  try {
    const dirPath = path.join(objectsDir, targetPrefix);
    const entries = await fs.readdir(dirPath);

    for (const entry of entries) {
      if (entry.endsWith('.beast2') && !entry.includes('.partial')) {
        // Reconstruct full hash: dir prefix + filename without extension
        const fullHash = targetPrefix + entry.slice(0, -7); // remove '.beast2'
        hashes.push(fullHash);
      }
    }
  } catch {
    // Directory doesn't exist - hash is unique at minimum length
    return minLength;
  }

  // Find minimum length that disambiguates from all other hashes
  let length = minLength;

  while (length < hash.length) {
    const prefix = hash.slice(0, length);
    const conflicts = hashes.filter(
      (h) => h !== hash && h.startsWith(prefix)
    );

    if (conflicts.length === 0) {
      return length;
    }

    length++;
  }

  return hash.length;
}
