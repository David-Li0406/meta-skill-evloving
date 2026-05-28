/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Tests for dataflow.ts - DAG execution
 */

import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { join } from 'node:path';
import { mkdirSync, writeFileSync } from 'node:fs';
import { variant, StringType, ArrayType, encodeBeast2For, StructType, East, IRType } from '@elaraai/east';
import {
  TaskObjectType,
  PackageObjectType,
  DataRefType,
  type TreePath,
  type Structure,
  type DataRef,
} from '@elaraai/e3-types';
import {
  dataflowExecute,
  dataflowGetGraph,
  dataflowGetReadyTasks,
  dataflowGetDependentsToSkip,
  type DataflowGraph,
} from './dataflow.js';
import { objectWrite } from './objects.js';
import { workspaceDeploy } from './workspaces.js';
import { workspaceGetDataset, workspaceSetDataset } from './trees.js';
import { WorkspaceLockError, DataflowAbortedError } from './errors.js';
import { createTestRepo, removeTestRepo } from './test-helpers.js';
import { LocalStorage } from './storage/local/index.js';
import type { StorageBackend } from './storage/interfaces.js';

describe('dataflow', () => {
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

  // Helper to create a package with tasks
  async function createPackageWithTasks(
    repoPath: string,
    tasks: Array<{
      name: string;
      command: string[];  // Command parts with placeholders
      inputs: TreePath[];
      output: TreePath;
    }>,
    structure: Structure,
    initialData?: Record<string, { value: unknown; ref: DataRef }>
  ): Promise<string> {
    const taskEncoder = encodeBeast2For(TaskObjectType);
    const tasksMap = new Map<string, string>();

    for (const t of tasks) {
      // Create command IR for this task
      const commandIrHash = await createCommandIr(repoPath, t.command);

      const taskObj = {
        commandIr: commandIrHash,
        inputs: t.inputs,
        output: t.output,
      };
      const taskHash = await objectWrite(repoPath, taskEncoder(taskObj));
      tasksMap.set(t.name, taskHash);
    }

    // Build initial data tree
    // For simplicity, we'll create a flat structure with DataRefs
    const structFields = (structure as { type: 'struct'; value: Map<string, Structure> }).value;
    const dataRefFields: Record<string, typeof DataRefType> = {};
    for (const key of structFields.keys()) {
      dataRefFields[key] = DataRefType;
    }
    const dataTreeType = StructType(dataRefFields);
    const dataTreeEncoder = encodeBeast2For(dataTreeType);

    // Create data refs for initial data
    const dataRefs: Record<string, DataRef> = {};
    for (const key of (structure as { type: 'struct'; value: Map<string, Structure> }).value.keys()) {
      if (initialData && key in initialData) {
        dataRefs[key] = initialData[key].ref;
      } else {
        // Unassigned by default
        dataRefs[key] = { type: 'unassigned', value: null } as DataRef;
      }
    }

    const dataHash = await objectWrite(repoPath, dataTreeEncoder(dataRefs));

    // Create package object
    const pkgEncoder = encodeBeast2For(PackageObjectType);
    const pkgObj = {
      data: {
        structure,
        value: dataHash,
      },
      tasks: tasksMap,
    };
    const pkgHash = await objectWrite(repoPath, pkgEncoder(pkgObj));

    // Write package ref - the ref file is at packages/<name>/<version> (version is the file, not a directory)
    const pkgDir = join(repoPath, 'packages', 'test');
    mkdirSync(pkgDir, { recursive: true });
    writeFileSync(join(pkgDir, '1.0.0'), pkgHash + '\n');

    return pkgHash;
  }

  describe('dataflowGetGraph', () => {
    it('returns empty graph for package with no tasks', async () => {
      // Create a minimal package with no tasks
      const structure: Structure = {
        type: 'struct',
        value: new Map([['input', { type: 'value', value: StringType }]]),
      } as unknown as Structure;

      await createPackageWithTasks(testRepo, [], structure);
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');

      const graph = await dataflowGetGraph(storage, testRepo, 'test-ws');
      assert.strictEqual(graph.tasks.length, 0);
    });

    it('returns task dependencies', async () => {
      // Create a package with two tasks: A -> B
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['middle', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const middlePath: TreePath = [variant('field', 'middle')];
      const outputPath: TreePath = [variant('field', 'output')];

      await createPackageWithTasks(
        testRepo,
        [
          { name: 'task-a', command: ['cp', '{input}', '{output}'], inputs: [inputPath], output: middlePath },
          { name: 'task-b', command: ['cp', '{input}', '{output}'], inputs: [middlePath], output: outputPath },
        ],
        structure
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');

      const graph = await dataflowGetGraph(storage, testRepo, 'test-ws');
      assert.strictEqual(graph.tasks.length, 2);

      const taskA = graph.tasks.find((t) => t.name === 'task-a');
      const taskB = graph.tasks.find((t) => t.name === 'task-b');

      assert.ok(taskA);
      assert.ok(taskB);
      assert.deepStrictEqual(taskA.dependsOn, []); // A depends on external input
      assert.deepStrictEqual(taskB.dependsOn, ['task-a']); // B depends on A
    });
  });

  describe('dataflowGetReadyTasks', () => {
    it('returns all tasks when none have dependencies', () => {
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: [] },
          { name: 'c', hash: 'h3', inputs: [], output: 'out-c', dependsOn: [] },
        ],
      };

      const ready = dataflowGetReadyTasks(graph, new Set());
      assert.deepStrictEqual(ready.sort(), ['a', 'b', 'c']);
    });

    it('returns only tasks with satisfied dependencies', () => {
      // Diamond: A -> B, A -> C, B -> D, C -> D
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: ['a'] },
          { name: 'c', hash: 'h3', inputs: [], output: 'out-c', dependsOn: ['a'] },
          { name: 'd', hash: 'h4', inputs: [], output: 'out-d', dependsOn: ['b', 'c'] },
        ],
      };

      // Initially only A is ready
      let ready = dataflowGetReadyTasks(graph, new Set());
      assert.deepStrictEqual(ready, ['a']);

      // After A completes, B and C are ready
      ready = dataflowGetReadyTasks(graph, new Set(['a']));
      assert.deepStrictEqual(ready.sort(), ['b', 'c']);

      // After A and B complete, C is ready (D still waiting for C)
      ready = dataflowGetReadyTasks(graph, new Set(['a', 'b']));
      assert.deepStrictEqual(ready, ['c']);

      // After A, B, C complete, D is ready
      ready = dataflowGetReadyTasks(graph, new Set(['a', 'b', 'c']));
      assert.deepStrictEqual(ready, ['d']);

      // After all complete, nothing is ready
      ready = dataflowGetReadyTasks(graph, new Set(['a', 'b', 'c', 'd']));
      assert.deepStrictEqual(ready, []);
    });

    it('excludes already completed tasks', () => {
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: [] },
        ],
      };

      const ready = dataflowGetReadyTasks(graph, new Set(['a']));
      assert.deepStrictEqual(ready, ['b']);
    });
  });

  describe('dataflowGetDependentsToSkip', () => {
    it('returns empty array when no tasks depend on failed task', () => {
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: [] },
        ],
      };

      const toSkip = dataflowGetDependentsToSkip(graph, 'a', new Set(), new Set());
      assert.deepStrictEqual(toSkip, []);
    });

    it('returns direct dependents', () => {
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: ['a'] },
          { name: 'c', hash: 'h3', inputs: [], output: 'out-c', dependsOn: ['a'] },
        ],
      };

      const toSkip = dataflowGetDependentsToSkip(graph, 'a', new Set(), new Set());
      assert.deepStrictEqual(toSkip.sort(), ['b', 'c']);
    });

    it('returns transitive dependents', () => {
      // a -> b -> c -> d
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: ['a'] },
          { name: 'c', hash: 'h3', inputs: [], output: 'out-c', dependsOn: ['b'] },
          { name: 'd', hash: 'h4', inputs: [], output: 'out-d', dependsOn: ['c'] },
        ],
      };

      const toSkip = dataflowGetDependentsToSkip(graph, 'a', new Set(), new Set());
      assert.deepStrictEqual(toSkip.sort(), ['b', 'c', 'd']);
    });

    it('handles diamond dependencies', () => {
      // a -> b -> d
      // a -> c -> d
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: ['a'] },
          { name: 'c', hash: 'h3', inputs: [], output: 'out-c', dependsOn: ['a'] },
          { name: 'd', hash: 'h4', inputs: [], output: 'out-d', dependsOn: ['b', 'c'] },
        ],
      };

      const toSkip = dataflowGetDependentsToSkip(graph, 'a', new Set(), new Set());
      assert.deepStrictEqual(toSkip.sort(), ['b', 'c', 'd']);
    });

    it('excludes already completed tasks', () => {
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: ['a'] },
          { name: 'c', hash: 'h3', inputs: [], output: 'out-c', dependsOn: ['a'] },
        ],
      };

      // b is already completed
      const toSkip = dataflowGetDependentsToSkip(graph, 'a', new Set(['b']), new Set());
      assert.deepStrictEqual(toSkip, ['c']);
    });

    it('excludes already skipped tasks', () => {
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: ['a'] },
          { name: 'c', hash: 'h3', inputs: [], output: 'out-c', dependsOn: ['b'] },
        ],
      };

      // b is already skipped
      const toSkip = dataflowGetDependentsToSkip(graph, 'a', new Set(), new Set(['b']));
      // c depends on b which is already skipped, so only c should be returned (not b again)
      // But since b is skipped, we skip it, and c is a transitive dependent through b
      assert.deepStrictEqual(toSkip, ['c']);
    });

    it('does not skip tasks that have alternative paths', () => {
      // a (fails) -> b -> d
      // c (success) -> d
      // d depends on both b and c. If a fails, b is skipped, but d might still be reachable via c
      // However, our function finds ALL transitive dependents - the caller decides what to do
      const graph: DataflowGraph = {
        tasks: [
          { name: 'a', hash: 'h1', inputs: [], output: 'out-a', dependsOn: [] },
          { name: 'b', hash: 'h2', inputs: [], output: 'out-b', dependsOn: ['a'] },
          { name: 'c', hash: 'h3', inputs: [], output: 'out-c', dependsOn: [] },
          { name: 'd', hash: 'h4', inputs: [], output: 'out-d', dependsOn: ['b', 'c'] },
        ],
      };

      // d is a transitive dependent of a through b
      const toSkip = dataflowGetDependentsToSkip(graph, 'a', new Set(), new Set());
      assert.deepStrictEqual(toSkip.sort(), ['b', 'd']);
    });
  });

  describe('dataflowExecute', () => {
    it('executes single task', async () => {
      // Create package with one task
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const outputPath: TreePath = [variant('field', 'output')];

      // Create input value
      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('hello world'));

      await createPackageWithTasks(
        testRepo,
        [{ name: 'copy-task', command: ['cp', '{input}', '{output}'], inputs: [inputPath], output: outputPath }],
        structure,
        {
          input: {
            value: 'hello world',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');

      // Set the input value in workspace
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'hello world', StringType);

      const result = await dataflowExecute(storage, testRepo, 'test-ws');

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.executed, 1);
      assert.strictEqual(result.failed, 0);
      assert.strictEqual(result.tasks.length, 1);
      assert.strictEqual(result.tasks[0].state, 'success');

      // Verify output was written
      const outputValue = await workspaceGetDataset(storage, testRepo, 'test-ws', outputPath);
      assert.strictEqual(outputValue, 'hello world');
    });

    it('executes task chain in order', async () => {
      // Create package with A -> B chain
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['middle', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const middlePath: TreePath = [variant('field', 'middle')];
      const outputPath: TreePath = [variant('field', 'output')];

      // Create input value
      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('chain test'));

      await createPackageWithTasks(
        testRepo,
        [
          { name: 'task-a', command: ['cp', '{input}', '{output}'], inputs: [inputPath], output: middlePath },
          { name: 'task-b', command: ['cp', '{input}', '{output}'], inputs: [middlePath], output: outputPath },
        ],
        structure,
        {
          input: {
            value: 'chain test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');

      // Set the input value in workspace
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'chain test', StringType);

      const completedOrder: string[] = [];
      const result = await dataflowExecute(storage, testRepo, 'test-ws', {
        onTaskComplete: (r) => completedOrder.push(r.name),
      });

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.executed, 2);
      assert.strictEqual(completedOrder[0], 'task-a'); // A must complete before B
      assert.strictEqual(completedOrder[1], 'task-b');

      // Verify final output
      const outputValue = await workspaceGetDataset(storage, testRepo, 'test-ws', outputPath);
      assert.strictEqual(outputValue, 'chain test');
    });

    it('handles task failure with fail-fast', async () => {
      // Create package with A (fails) -> B (should be skipped)
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['middle', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const middlePath: TreePath = [variant('field', 'middle')];
      const outputPath: TreePath = [variant('field', 'output')];

      // Create input value
      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('fail test'));

      await createPackageWithTasks(
        testRepo,
        [
          { name: 'task-a', command: ['bash', '-c', 'exit 1'], inputs: [inputPath], output: middlePath },
          { name: 'task-b', command: ['cp', '{input}', '{output}'], inputs: [middlePath], output: outputPath },
        ],
        structure,
        {
          input: {
            value: 'fail test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');

      // Set the input value
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'fail test', StringType);

      const result = await dataflowExecute(storage, testRepo, 'test-ws');

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.failed, 1);
      assert.strictEqual(result.skipped, 1);

      const taskA = result.tasks.find((t) => t.name === 'task-a');
      const taskB = result.tasks.find((t) => t.name === 'task-b');

      assert.ok(taskA);
      assert.ok(taskB);
      assert.strictEqual(taskA.state, 'failed');
      assert.strictEqual(taskB.state, 'skipped');
    });

    it('caches successful task results', async () => {
      // Create package
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const outputPath: TreePath = [variant('field', 'output')];

      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('cache test'));

      await createPackageWithTasks(
        testRepo,
        [{ name: 'copy-task', command: ['cp', '{input}', '{output}'], inputs: [inputPath], output: outputPath }],
        structure,
        {
          input: {
            value: 'cache test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'cache test', StringType);

      // First execution
      const result1 = await dataflowExecute(storage, testRepo, 'test-ws');
      assert.strictEqual(result1.executed, 1);
      assert.strictEqual(result1.cached, 0);

      // Second execution should be cached (output already assigned)
      const result2 = await dataflowExecute(storage, testRepo, 'test-ws');
      assert.strictEqual(result2.executed, 0);
      assert.strictEqual(result2.cached, 1);
    });

    it('respects concurrency limit', async () => {
      // Create package with 4 parallel tasks
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['out1', { type: 'value', value: StringType }],
          ['out2', { type: 'value', value: StringType }],
          ['out3', { type: 'value', value: StringType }],
          ['out4', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];

      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('parallel test'));

      // Use a slow command
      const slowCopyCmd = ['bash', '-c', 'sleep 0.1; cp "$1" "$2"', '--', '{input}', '{output}'];

      await createPackageWithTasks(
        testRepo,
        [
          { name: 'task-1', command: slowCopyCmd, inputs: [inputPath], output: [variant('field', 'out1')] },
          { name: 'task-2', command: slowCopyCmd, inputs: [inputPath], output: [variant('field', 'out2')] },
          { name: 'task-3', command: slowCopyCmd, inputs: [inputPath], output: [variant('field', 'out3')] },
          { name: 'task-4', command: slowCopyCmd, inputs: [inputPath], output: [variant('field', 'out4')] },
        ],
        structure,
        {
          input: {
            value: 'parallel test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'parallel test', StringType);

      // Track concurrent execution count
      let currentConcurrent = 0;
      let maxConcurrent = 0;

      const result = await dataflowExecute(storage, testRepo, 'test-ws', {
        concurrency: 2,
        onTaskStart: () => {
          currentConcurrent++;
          maxConcurrent = Math.max(maxConcurrent, currentConcurrent);
        },
        onTaskComplete: () => {
          currentConcurrent--;
        },
      });

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.executed, 4);
      assert.ok(maxConcurrent <= 2, `Max concurrent was ${maxConcurrent}, expected <= 2`);
    });

    it('rejects concurrent dataflow execution on same workspace', async () => {
      // Create a simple package with a slow task
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const outputPath: TreePath = [variant('field', 'output')];

      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('test'));

      // Use sleep to make the task take some time
      const slowCopyCmd = ['bash', '-c', 'sleep 0.3; cp "$1" "$2"', '--', '{input}', '{output}'];
      await createPackageWithTasks(
        testRepo,
        [{ name: 'slow-task', command: slowCopyCmd, inputs: [inputPath], output: outputPath }],
        structure,
        {
          input: {
            value: 'test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'test', StringType);

      // Start first execution (don't await)
      const firstExecution = dataflowExecute(storage, testRepo, 'test-ws');

      // Give it a moment to acquire the lock
      await new Promise(resolve => setTimeout(resolve, 150));

      // Try to start second execution - should fail with WorkspaceLockError
      await assert.rejects(
        dataflowExecute(storage, testRepo, 'test-ws'),
        (err: Error) => {
          assert.ok(err instanceof WorkspaceLockError, `Expected WorkspaceLockError, got ${err.constructor.name}`);
          assert.strictEqual((err as WorkspaceLockError).workspace, 'test-ws');
          return true;
        }
      );

      // Wait for first execution to complete
      const result = await firstExecution;
      assert.strictEqual(result.success, true);
    });

    it('allows sequential dataflow executions', async () => {
      // Create a simple package
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const outputPath: TreePath = [variant('field', 'output')];

      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('test'));

      await createPackageWithTasks(
        testRepo,
        [{ name: 'task', command: ['cp', '{input}', '{output}'], inputs: [inputPath], output: outputPath }],
        structure,
        {
          input: {
            value: 'test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'test', StringType);

      // First execution
      const result1 = await dataflowExecute(storage, testRepo, 'test-ws');
      assert.strictEqual(result1.success, true);

      // Second execution (should succeed because first released the lock)
      const result2 = await dataflowExecute(storage, testRepo, 'test-ws');
      assert.strictEqual(result2.success, true);
    });

    it('allows external lock management', async () => {
      // Create a simple package
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const outputPath: TreePath = [variant('field', 'output')];

      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('test'));

      await createPackageWithTasks(
        testRepo,
        [{ name: 'task', command: ['cp', '{input}', '{output}'], inputs: [inputPath], output: outputPath }],
        structure,
        {
          input: {
            value: 'test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'test', StringType);

      // Acquire lock externally
      const lock = await storage.locks.acquire(testRepo, 'test-ws', variant('dataflow', null));
      assert.ok(lock);

      try {
        // Execute with external lock
        const result = await dataflowExecute(storage, testRepo, 'test-ws', { lock });
        assert.strictEqual(result.success, true);

        // Lock should still be held (we can't acquire another)
        const attemptedLock = await storage.locks.acquire(testRepo, 'test-ws', variant('dataflow', null));
        assert.strictEqual(attemptedLock, null);
      } finally {
        await lock.release();
      }

      // Now lock should be released - can acquire again
      const lock2 = await storage.locks.acquire(testRepo, 'test-ws', variant('dataflow', null));
      assert.ok(lock2);
      await lock2.release();
    });

    it('aborts execution when signal is triggered', async () => {
      // Create a package with a slow task
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const outputPath: TreePath = [variant('field', 'output')];

      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('test'));

      // Task that sleeps for 2 seconds
      const slowCmd = ['bash', '-c', 'sleep 2; cp "$1" "$2"', '--', '{input}', '{output}'];
      await createPackageWithTasks(
        testRepo,
        [{ name: 'slow-task', command: slowCmd, inputs: [inputPath], output: outputPath }],
        structure,
        {
          input: {
            value: 'test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'test', StringType);

      const controller = new AbortController();

      // Start execution
      const executionPromise = dataflowExecute(storage, testRepo, 'test-ws', {
        signal: controller.signal,
      });

      // Abort after a short delay
      await new Promise(resolve => setTimeout(resolve, 200));
      controller.abort();

      // Should throw DataflowAbortedError
      await assert.rejects(
        executionPromise,
        (err: Error) => {
          assert.ok(err instanceof DataflowAbortedError, `Expected DataflowAbortedError, got ${err.constructor.name}`);
          return true;
        }
      );
    });

    it('includes partial results in DataflowAbortedError', async () => {
      // Create a package with two tasks: one fast, one slow
      const structure: Structure = {
        type: 'struct',
        value: new Map([
          ['input', { type: 'value', value: StringType }],
          ['fast_output', { type: 'value', value: StringType }],
          ['slow_output', { type: 'value', value: StringType }],
        ]),
      } as unknown as Structure;

      const inputPath: TreePath = [variant('field', 'input')];
      const fastOutputPath: TreePath = [variant('field', 'fast_output')];
      const slowOutputPath: TreePath = [variant('field', 'slow_output')];

      const inputEncoder = encodeBeast2For(StringType);
      const inputHash = await objectWrite(testRepo, inputEncoder('test'));

      // Fast task completes quickly, slow task takes long
      await createPackageWithTasks(
        testRepo,
        [
          { name: 'fast-task', command: ['cp', '{input}', '{output}'], inputs: [inputPath], output: fastOutputPath },
          { name: 'slow-task', command: ['bash', '-c', 'sleep 2; cp "$1" "$2"', '--', '{input}', '{output}'], inputs: [inputPath], output: slowOutputPath },
        ],
        structure,
        {
          input: {
            value: 'test',
            ref: { type: 'value', value: inputHash } as DataRef,
          },
        }
      );
      await workspaceDeploy(storage, testRepo, 'test-ws', 'test', '1.0.0');
      await workspaceSetDataset(storage, testRepo, 'test-ws', inputPath, 'test', StringType);

      const controller = new AbortController();

      // Start execution with concurrency 2 so both tasks start
      const executionPromise = dataflowExecute(storage, testRepo, 'test-ws', {
        signal: controller.signal,
        concurrency: 2,
      });

      // Wait for fast task to complete, then abort
      await new Promise(resolve => setTimeout(resolve, 300));
      controller.abort();

      // Should throw with partial results
      try {
        await executionPromise;
        assert.fail('Expected DataflowAbortedError');
      } catch (err) {
        assert.ok(err instanceof DataflowAbortedError);
        const abortErr = err as DataflowAbortedError;
        assert.ok(abortErr.partialResults);
        // Fast task should have completed
        const fastResult = abortErr.partialResults!.find(r => r.name === 'fast-task');
        assert.ok(fastResult, 'Fast task should be in partial results');
        assert.strictEqual(fastResult!.state, 'success');
      }
    });
  });
});
