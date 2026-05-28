/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { ObjectStore } from '../interfaces.js';
import {
  objectWrite,
  objectWriteStream,
  objectRead,
  objectExists,
} from '../../objects.js';
import { isNotFoundError } from '../../errors.js';

/**
 * Local filesystem implementation of ObjectStore.
 *
 * Wraps the existing objects.ts functions.
 * The `repo` parameter is the path to the e3 repository directory.
 */
export class LocalObjectStore implements ObjectStore {
  async write(repo: string, data: Uint8Array): Promise<string> {
    return objectWrite(repo, data);
  }

  async writeStream(repo: string, stream: AsyncIterable<Uint8Array>): Promise<string> {
    // Convert AsyncIterable to ReadableStream for objectWriteStream
    const readableStream = new ReadableStream<Uint8Array>({
      async start(controller) {
        for await (const chunk of stream) {
          controller.enqueue(chunk);
        }
        controller.close();
      },
    });
    return objectWriteStream(repo, readableStream);
  }

  async read(repo: string, hash: string): Promise<Uint8Array> {
    return objectRead(repo, hash);
  }

  async exists(repo: string, hash: string): Promise<boolean> {
    return objectExists(repo, hash);
  }

  async list(repo: string): Promise<string[]> {
    const objectsDir = path.join(repo, 'objects');
    const hashes: string[] = [];

    try {
      const prefixDirs = await fs.readdir(objectsDir);

      for (const prefix of prefixDirs) {
        if (!/^[a-f0-9]{2}$/.test(prefix)) continue;

        const prefixPath = path.join(objectsDir, prefix);
        const stat = await fs.stat(prefixPath);
        if (!stat.isDirectory()) continue;

        const files = await fs.readdir(prefixPath);
        for (const file of files) {
          if (file.endsWith('.beast2') && !file.includes('.partial')) {
            // Reconstruct full hash: prefix + filename without extension
            const hash = prefix + file.slice(0, -7);
            hashes.push(hash);
          }
        }
      }
    } catch (err) {
      // Only suppress ENOENT - directory may not exist yet
      if (!isNotFoundError(err)) {
        throw err;
      }
    }

    return hashes;
  }
}
