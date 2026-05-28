/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for executions.ts - task execution operations
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { join } from 'node:path';
import { mkdirSync, writeFileSync } from 'node:fs';
import { variant, StringType, ArrayType, encodeBeast2For, East, IRType } from '@elaraai/east';
import { TaskObjectType } from '@elaraai/e3-types';
import {
  inputsHash,
  executionGet,
  executionGetOutput,
  executionList,
  executionListForTask,
  executionReadLog,
  taskExecute,
} from './executions.js';
import { objectWrite } from './objects.js';
import { createTestRepo, removeTestRepo } from './test-helpers.js';
import { LocalStorage } from './storage/local/index.js';
import type { StorageBackend } from './storage/interfaces.js';

describe('executions', () => {
  let testRepo: string;
  let storage: StorageBackend;

  beforeEach(() => {
    testRepo = createTestRepo();
    storage = new LocalStorage();
  });

  afterEach(() => {
    removeTestRepo(testRepo);
  });

  /**
   * Helper to create a command IR object.
   *
   * Creates an East FunctionIR: (inputs: Array<String>, output: String) -> Array<String>
   * that returns the provided command parts as a literal array.
   */
  async function createCommandIr(repoPath: string, parts: string[]): Promise<string> {
    // Build an East function that returns the command array
    // The function signature is: (inputs: Array<String>, output: String) -> Array<String>
    const commandFn = East.function(
      [ArrayType(StringType), StringType],
      ArrayType(StringType),
      ($, inputs, output) => {
        // Build the result array, substituting inputs[i] and output as needed
        const result: (string | ReturnType<typeof inputs.get>)[] = [];
        for (const part of parts) {
          if (part === '{input}' || part === '{input0}') {
            result.push(inputs.get(0n));
          } else if (part.match(/^\{input(\d+)\}$/)) {
            const idx = BigInt(part.match(/^\{input(\d+)\}$/)![1]);
            result.push(inputs.get(idx));
          } else if (part === '{output}') {
            result.push(output);
          } else {
            result.push(part);
          }
        }
        return result;
      }
    );

    const ir = commandFn.toIR().ir;
    const encoder = encodeBeast2For(IRType);
    return objectWrite(repoPath, encoder(ir));
  }

  describe('inputsHash', () => {
    it('computes consistent hash for same inputs', () => {
      const hash1 = inputsHash(['abc', 'def']);
      const hash2 = inputsHash(['abc', 'def']);
      assert.strictEqual(hash1, hash2);
    });

    it('computes different hash for different inputs', () => {
      const hash1 = inputsHash(['abc', 'def']);
      const hash2 = inputsHash(['abc', 'xyz']);
      assert.notStrictEqual(hash1, hash2);
    });

    it('order matters', () => {
      const hash1 = inputsHash(['abc', 'def']);
      const hash2 = inputsHash(['def', 'abc']);
      assert.notStrictEqual(hash1, hash2);
    });

    it('handles empty array', () => {
      const hash = inputsHash([]);
      assert.strictEqual(hash.length, 64); // SHA256 hex
    });

    it('handles single input', () => {
      const hash = inputsHash(['abc']);
      assert.strictEqual(hash.length, 64);
    });
  });

  describe('executionGet', () => {
    it('returns null for non-existent execution', async () => {
      const taskHash = 'a'.repeat(64);
      const inHash = 'b'.repeat(64);
      const status = await executionGet(storage, testRepo, taskHash, inHash);
      assert.strictEqual(status, null);
    });
  });

  describe('executionGetOutput', () => {
    it('returns null for non-existent execution', async () => {
      const taskHash = 'a'.repeat(64);
      const inHash = 'b'.repeat(64);
      const output = await executionGetOutput(storage, testRepo, taskHash, inHash);
      assert.strictEqual(output, null);
    });

    it('returns hash from output ref file', async () => {
      const taskHash = 'a'.repeat(64);
      const inHash = 'b'.repeat(64);
      const outputHash = 'c'.repeat(64);

      // Create execution directory with output ref
      const execDir = join(testRepo, 'executions', taskHash, inHash);
      mkdirSync(execDir, { recursive: true });
      writeFileSync(join(execDir, 'output'), outputHash + '\n');

      const output = await executionGetOutput(storage, testRepo, taskHash, inHash);
      assert.strictEqual(output, outputHash);
    });
  });

  describe('executionList', () => {
    it('returns empty array for no executions', async () => {
      const list = await executionList(storage, testRepo);
      assert.deepStrictEqual(list, []);
    });

    it('lists all executions', async () => {
      const taskHash1 = 'a'.repeat(64);
      const taskHash2 = 'b'.repeat(64);
      const inHash1 = 'c'.repeat(64);
      const inHash2 = 'd'.repeat(64);

      // Create execution directories
      mkdirSync(join(testRepo, 'executions', taskHash1, inHash1), { recursive: true });
      mkdirSync(join(testRepo, 'executions', taskHash1, inHash2), { recursive: true });
      mkdirSync(join(testRepo, 'executions', taskHash2, inHash1), { recursive: true });

      const list = await executionList(storage, testRepo);
      assert.strictEqual(list.length, 3);
    });
  });

  describe('executionListForTask', () => {
    it('returns empty array for non-existent task', async () => {
      const taskHash = 'a'.repeat(64);
      const list = await executionListForTask(storage, testRepo, taskHash);
      assert.deepStrictEqual(list, []);
    });

    it('lists inputs for a task', async () => {
      const taskHash = 'a'.repeat(64);
      const inHash1 = 'b'.repeat(64);
      const inHash2 = 'c'.repeat(64);

      mkdirSync(join(testRepo, 'executions', taskHash, inHash1), { recursive: true });
      mkdirSync(join(testRepo, 'executions', taskHash, inHash2), { recursive: true });

      const list = await executionListForTask(storage, testRepo, taskHash);
      assert.strictEqual(list.length, 2);
      assert.ok(list.includes(inHash1));
      assert.ok(list.includes(inHash2));
    });
  });

  describe('executionReadLog', () => {
    it('returns empty chunk for non-existent log', async () => {
      const taskHash = 'a'.repeat(64);
      const inHash = 'b'.repeat(64);
      const chunk = await executionReadLog(storage, testRepo, taskHash, inHash, 'stdout');
      assert.strictEqual(chunk.data, '');
      assert.strictEqual(chunk.size, 0);
      assert.strictEqual(chunk.complete, true);
    });

    it('reads log content', async () => {
      const taskHash = 'a'.repeat(64);
      const inHash = 'b'.repeat(64);
      const logContent = 'Hello, world!\nLine 2\n';

      const execDir = join(testRepo, 'executions', taskHash, inHash);
      mkdirSync(execDir, { recursive: true });
      writeFileSync(join(execDir, 'stdout.txt'), logContent);

      const chunk = await executionReadLog(storage, testRepo, taskHash, inHash, 'stdout');
      assert.strictEqual(chunk.data, logContent);
      assert.strictEqual(chunk.size, logContent.length);
      assert.strictEqual(chunk.totalSize, logContent.length);
      assert.strictEqual(chunk.complete, true);
    });

    it('supports pagination', async () => {
      const taskHash = 'a'.repeat(64);
      const inHash = 'b'.repeat(64);
      const logContent = 'ABCDEFGHIJ';

      const execDir = join(testRepo, 'executions', taskHash, inHash);
      mkdirSync(execDir, { recursive: true });
      writeFileSync(join(execDir, 'stderr.txt'), logContent);

      // Read first 5 bytes
      const chunk1 = await executionReadLog(storage, testRepo, taskHash, inHash, 'stderr', {
        offset: 0,
        limit: 5,
      });
      assert.strictEqual(chunk1.data, 'ABCDE');
      assert.strictEqual(chunk1.offset, 0);
      assert.strictEqual(chunk1.size, 5);
      assert.strictEqual(chunk1.complete, false);

      // Read next 5 bytes
      const chunk2 = await executionReadLog(storage, testRepo, taskHash, inHash, 'stderr', {
        offset: 5,
        limit: 5,
      });
      assert.strictEqual(chunk2.data, 'FGHIJ');
      assert.strictEqual(chunk2.offset, 5);
      assert.strictEqual(chunk2.size, 5);
      assert.strictEqual(chunk2.complete, true);
    });
  });

  describe('taskExecute', () => {
    it('returns error for missing command IR', async () => {
      // Create a task object with non-existent command IR hash
      const task = {
        commandIr: 'a'.repeat(64), // Non-existent hash
        inputs: [],
        output: [],
      };
      const encoder = encodeBeast2For(TaskObjectType);
      const taskHash = await objectWrite(testRepo, encoder(task));

      const result = await taskExecute(storage, testRepo, taskHash, []);

      assert.strictEqual(result.state, 'error');
      assert.ok(result.error?.includes('Failed to evaluate command IR'));
    });

    it('executes simple cp command successfully', async () => {
      // Create command IR: cp {input} {output}
      const commandIrHash = await createCommandIr(testRepo, [
        'cp',
        '{input}',
        '{output}',
      ]);

      // Create a task object
      const task = {
        commandIr: commandIrHash,
        inputs: [[variant('field', 'test')]],
        output: [variant('field', 'output')],
      };
      const encoder = encodeBeast2For(TaskObjectType);
      const taskHash = await objectWrite(testRepo, encoder(task));

      // Create input data
      const inputEncoder = encodeBeast2For(StringType);
      const inputData = inputEncoder('hello world');
      const inputHash = await objectWrite(testRepo, inputData);

      // Execute
      const result = await taskExecute(storage, testRepo, taskHash, [inputHash]);

      assert.strictEqual(result.state, 'success');
      assert.strictEqual(result.cached, false);
      assert.ok(result.outputHash);
      assert.strictEqual(result.exitCode, 0);
      assert.ok(result.duration >= 0);
    });

    it('caches successful executions', async () => {
      // Create command IR
      const commandIrHash = await createCommandIr(testRepo, [
        'cp',
        '{input}',
        '{output}',
      ]);

      // Create task
      const task = {
        commandIr: commandIrHash,
        inputs: [[variant('field', 'test')]],
        output: [variant('field', 'output')],
      };
      const encoder = encodeBeast2For(TaskObjectType);
      const taskHash = await objectWrite(testRepo, encoder(task));

      // Create input
      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('test data'));

      // First execution
      const result1 = await taskExecute(storage, testRepo, taskHash, [inputHash]);
      assert.strictEqual(result1.cached, false);
      assert.strictEqual(result1.state, 'success');

      // Second execution should be cached
      const result2 = await taskExecute(storage, testRepo, taskHash, [inputHash]);
      assert.strictEqual(result2.cached, true);
      assert.strictEqual(result2.state, 'success');
      assert.strictEqual(result2.outputHash, result1.outputHash);
      assert.strictEqual(result2.duration, 0);
    });

    it('force bypasses cache', async () => {
      // Create command IR
      const commandIrHash = await createCommandIr(testRepo, [
        'cp',
        '{input}',
        '{output}',
      ]);

      // Create task
      const task = {
        commandIr: commandIrHash,
        inputs: [[variant('field', 'test')]],
        output: [variant('field', 'output')],
      };
      const encoder = encodeBeast2For(TaskObjectType);
      const taskHash = await objectWrite(testRepo, encoder(task));

      // Create input
      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('test data'));

      // First execution
      const result1 = await taskExecute(storage, testRepo, taskHash, [inputHash]);
      assert.strictEqual(result1.cached, false);

      // Force re-execution
      const result2 = await taskExecute(storage, testRepo, taskHash, [inputHash], { force: true });
      assert.strictEqual(result2.cached, false);
      assert.strictEqual(result2.state, 'success');
    });

    it('captures stdout and stderr', async () => {
      // Create command IR that echoes to both streams
      const commandIrHash = await createCommandIr(testRepo, [
        'bash',
        '-c',
        'echo stdout; echo stderr >&2; cp "$1" "$2"',
        '--',
        '{input}',
        '{output}',
      ]);

      // Create task
      const task = {
        commandIr: commandIrHash,
        inputs: [[variant('field', 'test')]],
        output: [variant('field', 'output')],
      };
      const encoder = encodeBeast2For(TaskObjectType);
      const taskHash = await objectWrite(testRepo, encoder(task));

      // Create input
      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('data'));

      // Capture callbacks
      const stdoutChunks: string[] = [];
      const stderrChunks: string[] = [];

      const result = await taskExecute(storage, testRepo, taskHash, [inputHash], {
        onStdout: (data) => stdoutChunks.push(data),
        onStderr: (data) => stderrChunks.push(data),
      });

      assert.strictEqual(result.state, 'success');

      // Check callbacks received data
      assert.ok(stdoutChunks.join('').includes('stdout'));
      assert.ok(stderrChunks.join('').includes('stderr'));

      // Check logs were written
      const inHash = result.inputsHash;
      const stdoutLog = await executionReadLog(storage, testRepo, taskHash, inHash, 'stdout');
      const stderrLog = await executionReadLog(storage, testRepo, taskHash, inHash, 'stderr');

      assert.ok(stdoutLog.data.includes('stdout'));
      assert.ok(stderrLog.data.includes('stderr'));
    });

    it('handles failed commands', async () => {
      // Create command IR that fails
      const commandIrHash = await createCommandIr(testRepo, [
        'bash',
        '-c',
        'exit 42',
      ]);

      // Create task
      const task = {
        commandIr: commandIrHash,
        inputs: [],
        output: [variant('field', 'output')],
      };
      const encoder = encodeBeast2For(TaskObjectType);
      const taskHash = await objectWrite(testRepo, encoder(task));

      const result = await taskExecute(storage, testRepo, taskHash, []);

      assert.strictEqual(result.state, 'failed');
      assert.strictEqual(result.exitCode, 42);
      assert.strictEqual(result.outputHash, null);

      // Check status was written
      const status = await executionGet(storage, testRepo, taskHash, result.inputsHash);
      assert.ok(status);
      assert.strictEqual(status.type, 'failed');
    });
  });
});
