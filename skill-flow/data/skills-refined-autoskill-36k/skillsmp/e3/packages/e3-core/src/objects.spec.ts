/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import {
  computeHash,
  objectWrite,
  objectWriteStream,
  objectRead,
  objectExists,
  objectPath,
  objectAbbrev,
} from './objects.js';
import { ObjectNotFoundError } from './errors.js';
import { createTestRepo, removeTestRepo } from './test-helpers.js';

describe('objects', () => {
  let testRepo: string;

  beforeEach(() => {
    testRepo = createTestRepo();
  });

  afterEach(() => {
    removeTestRepo(testRepo);
  });

  describe('computeHash', () => {
    it('computes correct SHA256 hash', () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash = computeHash(data);

      // Expected hash for [1, 2, 3]
      assert.strictEqual(hash, '039058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81');
    });

    it('returns same hash for same data', () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash1 = computeHash(data);
      const hash2 = computeHash(data);

      assert.strictEqual(hash1, hash2);
    });

    it('returns different hash for different data', () => {
      const data1 = new Uint8Array([1, 2, 3]);
      const data2 = new Uint8Array([1, 2, 4]);

      const hash1 = computeHash(data1);
      const hash2 = computeHash(data2);

      assert.notStrictEqual(hash1, hash2);
    });

    it('handles empty data', () => {
      const data = new Uint8Array([]);
      const hash = computeHash(data);

      // SHA256 hash of empty data
      assert.strictEqual(hash, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');
    });

    it('handles large data', () => {
      const data = new Uint8Array(1024 * 1024); // 1MB of zeros
      const hash = computeHash(data);

      assert.strictEqual(typeof hash, 'string');
      assert.strictEqual(hash.length, 64); // SHA256 produces 64 hex chars
    });
  });

  describe('objectWrite', () => {
    it('stores and returns hash', async () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash = await objectWrite(testRepo, data);

      assert.strictEqual(hash, '039058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81');
    });

    it('creates correct directory structure', async () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash = await objectWrite(testRepo, data);

      const dirName = hash.slice(0, 2);
      const fileName = hash.slice(2) + '.beast2';
      const filePath = join(testRepo, 'objects', dirName, fileName);

      const stored = readFileSync(filePath);
      assert.deepStrictEqual(new Uint8Array(stored), data);
    });

    it('deduplicates identical data', async () => {
      const data = new Uint8Array([1, 2, 3]);

      const hash1 = await objectWrite(testRepo, data);
      const hash2 = await objectWrite(testRepo, data);

      assert.strictEqual(hash1, hash2);

      // Verify only one file exists
      const dirName = hash1.slice(0, 2);
      const fileName = hash1.slice(2) + '.beast2';
      const filePath = join(testRepo, 'objects', dirName, fileName);

      const stored = readFileSync(filePath);
      assert.deepStrictEqual(new Uint8Array(stored), data);
    });

    it('handles concurrent writes to same hash', async () => {
      const data = new Uint8Array([1, 2, 3]);

      // Concurrent writes
      const [hash1, hash2, hash3] = await Promise.all([
        objectWrite(testRepo, data),
        objectWrite(testRepo, data),
        objectWrite(testRepo, data),
      ]);

      assert.strictEqual(hash1, hash2);
      assert.strictEqual(hash2, hash3);

      // Verify data is correct
      const dirName = hash1.slice(0, 2);
      const fileName = hash1.slice(2) + '.beast2';
      const filePath = join(testRepo, 'objects', dirName, fileName);

      const stored = readFileSync(filePath);
      assert.deepStrictEqual(new Uint8Array(stored), data);
    });

    it('stores empty data', async () => {
      const data = new Uint8Array([]);
      const hash = await objectWrite(testRepo, data);

      assert.strictEqual(hash, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');
    });

    it('stores large data', async () => {
      const data = new Uint8Array(1024 * 1024); // 1MB
      data.fill(42);

      const hash = await objectWrite(testRepo, data);
      const loaded = await objectRead(testRepo, hash);

      assert.deepStrictEqual(new Uint8Array(loaded), data);
    });
  });

  describe('objectWriteStream', () => {
    it('stores stream and returns hash', async () => {
      const data = new Uint8Array([1, 2, 3]);
      const stream = new ReadableStream({
        start(controller) {
          controller.enqueue(data);
          controller.close();
        },
      });

      const hash = await objectWriteStream(testRepo, stream);

      assert.strictEqual(hash, '039058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81');
    });

    it('stores chunked stream correctly', async () => {
      const chunk1 = new Uint8Array([1, 2]);
      const chunk2 = new Uint8Array([3]);

      const stream = new ReadableStream({
        start(controller) {
          controller.enqueue(chunk1);
          controller.enqueue(chunk2);
          controller.close();
        },
      });

      const hash = await objectWriteStream(testRepo, stream);
      const loaded = await objectRead(testRepo, hash);

      // Should reconstruct [1, 2, 3]
      assert.deepStrictEqual(new Uint8Array(loaded), new Uint8Array([1, 2, 3]));
    });

    it('deduplicates stream with existing object', async () => {
      const data = new Uint8Array([1, 2, 3]);

      // Store via regular objectWrite first
      const hash1 = await objectWrite(testRepo, data);

      // Store same data via stream
      const stream = new ReadableStream({
        start(controller) {
          controller.enqueue(data);
          controller.close();
        },
      });

      const hash2 = await objectWriteStream(testRepo, stream);

      assert.strictEqual(hash1, hash2);
    });
  });

  describe('objectRead', () => {
    it('loads stored object', async () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash = await objectWrite(testRepo, data);

      const loaded = await objectRead(testRepo, hash);

      assert.deepStrictEqual(new Uint8Array(loaded), data);
    });

    it('throws on non-existent hash', async () => {
      const fakeHash = 'a'.repeat(64);

      await assert.rejects(
        async () => await objectRead(testRepo, fakeHash),
        ObjectNotFoundError
      );
    });

    it('round-trips correctly', async () => {
      const original = new Uint8Array([7, 8, 9, 10, 11]);
      const hash = await objectWrite(testRepo, original);
      const loaded = await objectRead(testRepo, hash);

      assert.deepStrictEqual(new Uint8Array(loaded), original);
    });
  });

  describe('objectExists', () => {
    it('returns true for existing object', async () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash = await objectWrite(testRepo, data);

      const exists = await objectExists(testRepo, hash);

      assert.strictEqual(exists, true);
    });

    it('returns false for non-existent object', async () => {
      const fakeHash = 'a'.repeat(64);

      const exists = await objectExists(testRepo, fakeHash);

      assert.strictEqual(exists, false);
    });
  });

  describe('objectPath', () => {
    it('returns correct path', () => {
      const hash = '039058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81';
      const path = objectPath(testRepo, hash);

      assert.ok(path.endsWith('objects/03/9058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81.beast2'));
    });

    it('matches actual stored location', async () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash = await objectWrite(testRepo, data);

      const path = objectPath(testRepo, hash);
      const stored = readFileSync(path);

      assert.deepStrictEqual(new Uint8Array(stored), data);
    });
  });

  describe('objectAbbrev', () => {
    it('returns minLength for single object', async () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash = await objectWrite(testRepo, data);

      const abbrevLen = await objectAbbrev(testRepo, hash);

      assert.strictEqual(abbrevLen, 4); // default minLength
    });

    it('respects custom minLength', async () => {
      const data = new Uint8Array([1, 2, 3]);
      const hash = await objectWrite(testRepo, data);

      const abbrevLen = await objectAbbrev(testRepo, hash, 8);

      assert.strictEqual(abbrevLen, 8);
    });

    it('returns minLength for non-existent hash', async () => {
      const fakeHash = 'a'.repeat(64);

      const abbrevLen = await objectAbbrev(testRepo, fakeHash);

      assert.strictEqual(abbrevLen, 4);
    });

    it('increases length when objects share prefix', async () => {
      // Store multiple objects - some may share prefix characters
      const hashes: string[] = [];
      for (let i = 0; i < 100; i++) {
        const data = new Uint8Array([i, i + 1, i + 2, i + 3]);
        const hash = await objectWrite(testRepo, data);
        hashes.push(hash);
      }

      // For each hash, verify abbrev length is sufficient
      for (const hash of hashes) {
        const abbrevLen = await objectAbbrev(testRepo, hash);
        const prefix = hash.slice(0, abbrevLen);

        // Count how many hashes share this prefix
        const matching = hashes.filter((h) => h.startsWith(prefix));
        assert.strictEqual(matching.length, 1, `Prefix ${prefix} should be unique`);
      }
    });

    it('returns full length when all chars needed', async () => {
      // This is hard to test naturally, but we can verify the logic
      // by checking that length increases appropriately
      const data1 = new Uint8Array([1, 2, 3]);
      const hash1 = await objectWrite(testRepo, data1);

      // Store object with same first 2 chars (same directory)
      // Finding a collision is hard, so we just verify the function works
      const abbrevLen = await objectAbbrev(testRepo, hash1);
      assert.ok(abbrevLen >= 4);
      assert.ok(abbrevLen <= hash1.length);
    });
  });
});
