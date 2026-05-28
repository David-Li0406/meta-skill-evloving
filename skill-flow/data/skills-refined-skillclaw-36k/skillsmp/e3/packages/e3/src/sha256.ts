/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * SHA256 hashing utilities for e3.
 */

import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';

/**
 * Computes the SHA256 hash of a file.
 *
 * Reads the file in streaming mode to handle large files efficiently
 * without loading the entire contents into memory.
 *
 * @param path - Absolute or relative path to the file
 * @returns The SHA256 hash as a 64-character lowercase hex string
 *
 * @throws {Error} When the file does not exist or cannot be read
 *
 * @remarks
 * - Uses Node.js crypto module for hashing
 * - Streams file contents to avoid memory pressure on large files
 * - Returns lowercase hex encoding (64 characters for SHA256)
 *
 * @example
 * ```ts
 * import { sha256File } from '@elaraai/e3';
 *
 * const hash = await sha256File('./myfile.txt');
 * // hash: "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
 * ```
 */
export async function sha256File(path: string): Promise<string> {
  // Check file exists first for a clearer error message
  try {
    const stats = await stat(path);
    if (!stats.isFile()) {
      throw new Error(`Not a file: ${path}`);
    }
  } catch (err) {
    if (err instanceof Error && 'code' in err && err.code === 'ENOENT') {
      throw new Error(`File not found: ${path}`);
    }
    throw err;
  }

  return new Promise((resolve, reject) => {
    const hash = createHash('sha256');
    const stream = createReadStream(path);

    stream.on('data', (chunk) => {
      hash.update(chunk);
    });

    stream.on('end', () => {
      resolve(hash.digest('hex'));
    });

    stream.on('error', (err) => {
      reject(err);
    });
  });
}

/**
 * Computes the SHA256 hash of a byte array.
 *
 * @param data - The bytes to hash
 * @returns The SHA256 hash as a 64-character lowercase hex string
 *
 * @example
 * ```ts
 * import { sha256Bytes } from '@elaraai/e3';
 *
 * const data = new TextEncoder().encode('hello world');
 * const hash = sha256Bytes(data);
 * // hash: "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
 * ```
 */
export function sha256Bytes(data: Uint8Array): string {
  return createHash('sha256').update(data).digest('hex');
}

/**
 * Converts a SHA256 hex string to an object store path.
 *
 * The path uses the first 2 characters as a directory prefix for sharding,
 * followed by the remaining 62 characters as the filename.
 *
 * @param hash - A 64-character lowercase hex SHA256 hash
 * @returns Path of the form "objects/ab/cdef1234..."
 *
 * @throws {Error} When the hash is not a valid 64-character hex string
 *
 * @example
 * ```ts
 * import { hashToPath } from '@elaraai/e3';
 *
 * const path = hashToPath('b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9');
 * // path: "objects/b9/4d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
 * ```
 */
export function hashToPath(hash: string): string {
  if (!/^[0-9a-f]{64}$/.test(hash)) {
    throw new Error(`Invalid SHA256 hash: expected 64 lowercase hex characters, got "${hash}"`);
  }
  return `objects/${hash.slice(0, 2)}/${hash.slice(2)}`;
}
