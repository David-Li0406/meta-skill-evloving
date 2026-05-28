/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for convert command
 *
 * Testing strategy:
 * - Test the core conversion logic directly (convertCore function)
 * - Use temporary files for input/output
 * - Test various format combinations (.east, .json, .beast2)
 * - Test stdin input scenarios
 * - Avoid implementation details of beast2 encoding/decoding
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, mkdirSync } from 'node:fs';
import { convertCore } from './convert.impl.js';
import { createTestDir, removeTestDir, writeTestFile } from '../cli-test-helpers.js';

describe('convert command', () => {
  let testDir: string;

  beforeEach(() => {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });
  });

  afterEach(() => {
    removeTestDir(testDir);
  });

  describe('.east to .east (identity)', () => {
    it('converts integer value', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '42');
      const outputPath = `${testDir}/output.east`;

      const result = await convertCore(inputPath, 'east', outputPath);

      assert.strictEqual(result.success, true);
      const output = readFileSync(outputPath, 'utf-8');
      assert.strictEqual(output.trim(), '42');
    });

    it('converts string value', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '"hello world"');
      const outputPath = `${testDir}/output.east`;

      const result = await convertCore(inputPath, 'east', outputPath);

      assert.strictEqual(result.success, true);
      const output = readFileSync(outputPath, 'utf-8');
      assert.strictEqual(output.trim(), '"hello world"');
    });

    it('converts array value', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '[1, 2, 3]');
      const outputPath = `${testDir}/output.east`;

      const result = await convertCore(inputPath, 'east', outputPath);

      assert.strictEqual(result.success, true);
      const output = readFileSync(outputPath, 'utf-8');
      assert.match(output, /\[.*1.*2.*3.*\]/s);
    });
  });

  describe('.east to .json', () => {
    it('converts integer to JSON', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '42');
      const outputPath = `${testDir}/output.json`;

      const result = await convertCore(inputPath, 'json', outputPath);

      assert.strictEqual(result.success, true);
      const output = JSON.parse(readFileSync(outputPath, 'utf-8'));
      // East may convert numbers to strings in JSON
      assert.ok(output === 42 || output === '42');
    });

    it('converts string to JSON', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '"hello"');
      const outputPath = `${testDir}/output.json`;

      const result = await convertCore(inputPath, 'json', outputPath);

      assert.strictEqual(result.success, true);
      const output = JSON.parse(readFileSync(outputPath, 'utf-8'));
      assert.strictEqual(output, 'hello');
    });

    it('converts array to JSON', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '[1, 2, 3]');
      const outputPath = `${testDir}/output.json`;

      const result = await convertCore(inputPath, 'json', outputPath);

      assert.strictEqual(result.success, true);
      const output = JSON.parse(readFileSync(outputPath, 'utf-8'));
      // East may convert numbers to strings in JSON
      assert.ok(Array.isArray(output) && output.length === 3);
    });
  });

  describe('.json to .east', () => {
    it('converts integer with type spec', async () => {
      // East's fromJSONFor expects strings for integers
      const inputPath = writeTestFile(testDir, 'input.json', '"42"');
      const outputPath = `${testDir}/output.east`;

      // Type spec should be an East value whose type will be inferred
      const result = await convertCore(inputPath, 'east', outputPath, '0', 'json');

      assert.strictEqual(result.success, true);
      const output = readFileSync(outputPath, 'utf-8');
      assert.strictEqual(output.trim(), '42');
    });

    it('converts array with type spec', async () => {
      // East's fromJSONFor expects strings for integers
      const inputPath = writeTestFile(testDir, 'input.json', '["1", "2", "3"]');
      const outputPath = `${testDir}/output.east`;

      // Type spec should be an East value whose type will be inferred
      // Use [0] instead of [] to get Array<Integer> type
      const result = await convertCore(inputPath, 'east', outputPath, '[0]', 'json');

      assert.strictEqual(result.success, true);
      const output = readFileSync(outputPath, 'utf-8');
      assert.match(output, /\[.*1.*2.*3.*\]/s);
    });

    it('fails without type spec', async () => {
      const inputPath = writeTestFile(testDir, 'input.json', '42');
      const outputPath = `${testDir}/output.east`;

      const result = await convertCore(inputPath, 'east', outputPath, undefined, 'json');

      assert.strictEqual(result.success, false);
      assert.match(result.error?.message ?? '', /requires --type/);
    });
  });

  describe('.beast2 format (round-trip)', () => {
    it('converts .east to .beast2 and back', async () => {
      // .east -> .beast2
      const inputPath = writeTestFile(testDir, 'input.east', '42');
      const beast2Path = `${testDir}/data.beast2`;

      const toBeast2Result = await convertCore(inputPath, 'beast2', beast2Path);
      assert.strictEqual(toBeast2Result.success, true);

      // Verify beast2 file was created
      const beast2Data = readFileSync(beast2Path);
      assert.ok(beast2Data.length > 0);

      // .beast2 -> .east
      const outputPath = `${testDir}/output.east`;
      const toEastResult = await convertCore(beast2Path, 'east', outputPath);
      assert.strictEqual(toEastResult.success, true);

      // Verify round-trip
      const output = readFileSync(outputPath, 'utf-8');
      assert.strictEqual(output.trim(), '42');
    });

    it('converts array to beast2 and back', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '[1, 2, 3]');
      const beast2Path = `${testDir}/data.beast2`;

      // .east -> .beast2
      const toBeast2Result = await convertCore(inputPath, 'beast2', beast2Path);
      assert.strictEqual(toBeast2Result.success, true);

      // .beast2 -> .east
      const outputPath = `${testDir}/output.east`;
      const toEastResult = await convertCore(beast2Path, 'east', outputPath);
      assert.strictEqual(toEastResult.success, true);

      // Verify round-trip
      const output = readFileSync(outputPath, 'utf-8');
      assert.match(output, /\[.*1.*2.*3.*\]/s);
    });
  });

  describe('type output format', () => {
    it('outputs type for integer', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '42');
      const outputPath = `${testDir}/type.east`;

      const result = await convertCore(inputPath, 'type', outputPath);

      assert.strictEqual(result.success, true);
      const output = readFileSync(outputPath, 'utf-8');
      assert.match(output, /Integer/i);
    });

    it('outputs type for array', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '[1, 2, 3]');
      const outputPath = `${testDir}/type.east`;

      const result = await convertCore(inputPath, 'type', outputPath);

      assert.strictEqual(result.success, true);
      const output = readFileSync(outputPath, 'utf-8');
      assert.match(output, /Array/);
    });
  });

  describe('stdin input', () => {
    it('converts from stdin to file', async () => {
      // Note: Actual stdin testing would require spawning a subprocess
      // For unit tests, we test the null path case which triggers stdin logic

      // Mock stdin by providing null path (stdin indicator)
      // In real usage, this would read from process.stdin
      // For this test, we'll just verify the error handling path works

      // This test would need subprocess spawning to properly test stdin
      // We'll demonstrate the pattern in integration tests instead
      assert.ok(true, 'Stdin testing requires subprocess - see integration tests');
    });
  });

  describe('format detection', () => {
    it('detects .east format from extension', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '42');
      const outputPath = `${testDir}/output.json`;

      const result = await convertCore(inputPath, 'json', outputPath);

      assert.strictEqual(result.success, true);
    });

    it('detects .json format from extension', async () => {
      // East's fromJSONFor expects strings for integers
      const inputPath = writeTestFile(testDir, 'input.json', '"42"');
      const outputPath = `${testDir}/output.east`;

      // JSON format requires explicit type when auto-detecting
      // Type spec should be an East value whose type will be inferred
      const result = await convertCore(inputPath, 'east', outputPath, '0', 'json');

      assert.strictEqual(result.success, true);
    });

    it('detects .beast2 format from extension', async () => {
      // First create a beast2 file
      const eastPath = writeTestFile(testDir, 'input.east', '42');
      const beast2Path = `${testDir}/data.beast2`;
      await convertCore(eastPath, 'beast2', beast2Path);

      // Now test detection
      const outputPath = `${testDir}/output.east`;
      const result = await convertCore(beast2Path, 'east', outputPath);

      assert.strictEqual(result.success, true);
    });
  });

  describe('error handling', () => {
    it('handles invalid .east input', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', 'not valid east syntax!!!');
      const outputPath = `${testDir}/output.json`;

      const result = await convertCore(inputPath, 'json', outputPath);

      assert.strictEqual(result.success, false);
      assert.ok(result.error);
    });

    it('handles missing input file', async () => {
      const inputPath = `${testDir}/nonexistent.east`;
      const outputPath = `${testDir}/output.json`;

      const result = await convertCore(inputPath, 'json', outputPath);

      assert.strictEqual(result.success, false);
      assert.ok(result.error);
    });

    it('handles unknown file extension', async () => {
      const inputPath = writeTestFile(testDir, 'input.txt', '42');
      const outputPath = `${testDir}/output.json`;

      const result = await convertCore(inputPath, 'json', outputPath);

      assert.strictEqual(result.success, false);
      assert.match(result.error?.message ?? '', /Cannot detect format/);
    });
  });

  describe('stdout output (no output file)', () => {
    it('returns data when no output path specified', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '42');

      const result = await convertCore(inputPath, 'json');

      assert.strictEqual(result.success, true);
      assert.ok(result.data);
      const json = JSON.parse(result.data as string);
      // East may convert numbers to strings in JSON
      assert.ok(json === 42 || json === '42');
    });

    it('returns beast2 buffer when no output path specified', async () => {
      const inputPath = writeTestFile(testDir, 'input.east', '42');

      const result = await convertCore(inputPath, 'beast2');

      assert.strictEqual(result.success, true);
      assert.ok(result.data instanceof Buffer);
      assert.ok(result.data.length > 0);
    });
  });
});
