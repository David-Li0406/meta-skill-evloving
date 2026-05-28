/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { mkdtempSync, rmSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

import { sha256File, sha256Bytes, hashToPath } from './sha256.js';

describe('sha256', () => {
  let testDir: string;

  beforeEach(() => {
    testDir = mkdtempSync(join(tmpdir(), 'e3-sha256-test-'));
  });

  afterEach(() => {
    rmSync(testDir, { recursive: true, force: true });
  });

  describe('sha256File', () => {
    it('computes correct hash for a file', async () => {
      const filePath = join(testDir, 'test.txt');
      writeFileSync(filePath, 'hello world');

      const hash = await sha256File(filePath);

      // Known SHA256 of "hello world"
      assert.strictEqual(
        hash,
        'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
      );
    });

    it('returns 64-character lowercase hex string', async () => {
      const filePath = join(testDir, 'test.txt');
      writeFileSync(filePath, 'any content');

      const hash = await sha256File(filePath);

      assert.strictEqual(hash.length, 64);
      assert.match(hash, /^[0-9a-f]{64}$/);
    });

    it('computes correct hash for empty file', async () => {
      const filePath = join(testDir, 'empty.txt');
      writeFileSync(filePath, '');

      const hash = await sha256File(filePath);

      // Known SHA256 of empty string
      assert.strictEqual(
        hash,
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
      );
    });

    it('computes correct hash for binary data', async () => {
      const filePath = join(testDir, 'binary.bin');
      const binaryData = Buffer.from([0x00, 0x01, 0x02, 0xff, 0xfe, 0xfd]);
      writeFileSync(filePath, binaryData);

      const hash = await sha256File(filePath);

      // Verify hash matches sha256Bytes for same data
      const expectedHash = sha256Bytes(binaryData);
      assert.strictEqual(hash, expectedHash);
    });

    it('throws for non-existent file', async () => {
      const filePath = join(testDir, 'does-not-exist.txt');

      await assert.rejects(
        () => sha256File(filePath),
        (err: Error) => {
          assert.match(err.message, /File not found/);
          return true;
        }
      );
    });

    it('throws for directory path', async () => {
      const dirPath = join(testDir, 'subdir');
      mkdirSync(dirPath);

      await assert.rejects(
        () => sha256File(dirPath),
        (err: Error) => {
          assert.match(err.message, /Not a file/);
          return true;
        }
      );
    });

    it('produces different hashes for different content', async () => {
      const file1 = join(testDir, 'file1.txt');
      const file2 = join(testDir, 'file2.txt');
      writeFileSync(file1, 'content one');
      writeFileSync(file2, 'content two');

      const hash1 = await sha256File(file1);
      const hash2 = await sha256File(file2);

      assert.notStrictEqual(hash1, hash2);
    });

    it('produces same hash for identical content in different files', async () => {
      const file1 = join(testDir, 'file1.txt');
      const file2 = join(testDir, 'file2.txt');
      writeFileSync(file1, 'identical content');
      writeFileSync(file2, 'identical content');

      const hash1 = await sha256File(file1);
      const hash2 = await sha256File(file2);

      assert.strictEqual(hash1, hash2);
    });
  });

  describe('sha256Bytes', () => {
    it('computes correct hash for byte array', () => {
      const data = new TextEncoder().encode('hello world');

      const hash = sha256Bytes(data);

      assert.strictEqual(
        hash,
        'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
      );
    });

    it('returns 64-character lowercase hex string', () => {
      const data = new TextEncoder().encode('any content');

      const hash = sha256Bytes(data);

      assert.strictEqual(hash.length, 64);
      assert.match(hash, /^[0-9a-f]{64}$/);
    });

    it('computes correct hash for empty array', () => {
      const data = new Uint8Array(0);

      const hash = sha256Bytes(data);

      assert.strictEqual(
        hash,
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
      );
    });

    it('matches sha256File for same content', async () => {
      const content = 'matching content test';
      const data = new TextEncoder().encode(content);
      const filePath = join(testDir, 'match.txt');
      writeFileSync(filePath, content);

      const bytesHash = sha256Bytes(data);
      const fileHash = await sha256File(filePath);

      assert.strictEqual(bytesHash, fileHash);
    });
  });

  describe('hashToPath', () => {
    it('converts hash to correct path format', () => {
      const hash = 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9';

      const path = hashToPath(hash);

      assert.strictEqual(
        path,
        'objects/b9/4d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
      );
    });

    it('uses first 2 chars as directory prefix', () => {
      const hash = 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890';

      const path = hashToPath(hash);

      assert.strictEqual(path, 'objects/ab/cdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890');
    });

    it('throws for invalid hash length', () => {
      assert.throws(
        () => hashToPath('abc123'),
        (err: Error) => {
          assert.match(err.message, /Invalid SHA256 hash/);
          assert.match(err.message, /64 lowercase hex characters/);
          return true;
        }
      );
    });

    it('throws for uppercase hex', () => {
      const hash = 'B94D27B9934D3E08A52E52D7DA7DABFAC484EFE37A5380EE9088F7ACE2EFCDE9';

      assert.throws(
        () => hashToPath(hash),
        (err: Error) => {
          assert.match(err.message, /Invalid SHA256 hash/);
          return true;
        }
      );
    });

    it('throws for non-hex characters', () => {
      const hash = 'g94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9';

      assert.throws(
        () => hashToPath(hash),
        (err: Error) => {
          assert.match(err.message, /Invalid SHA256 hash/);
          return true;
        }
      );
    });

    it('throws for empty string', () => {
      assert.throws(
        () => hashToPath(''),
        (err: Error) => {
          assert.match(err.message, /Invalid SHA256 hash/);
          return true;
        }
      );
    });

    it('works with hash from sha256Bytes', () => {
      const data = new TextEncoder().encode('hello world');
      const hash = sha256Bytes(data);

      const path = hashToPath(hash);

      assert.strictEqual(
        path,
        'objects/b9/4d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
      );
    });
  });
});
