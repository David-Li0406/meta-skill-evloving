/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Stress test scenarios - large data, deep DAGs, wide DAGs
 *
 * Uses random East types from @elaraai/east/internal for thorough testing.
 */

import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import type { EastType } from '@elaraai/east';
import { East, StringType, ArrayType, IntegerType } from '@elaraai/east';
import { randomType as eastRandomType, randomValueFor } from '@elaraai/east/internal';
import e3 from '@elaraai/e3';
import type { TaskDef, DatasetDef, PackageDef } from '@elaraai/e3';
import {
  createTestDir,
  removeTestDir,
  runE3Command,
  random,
  type ScenarioResult,
} from '../helpers.js';

/**
 * Test large array handling with random element types.
 * Creates arrays with 1000-5000 elements to stress serialization.
 */
export async function testLargeArrays(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    // Generate a random element type (depth 1 to keep elements simple)
    const elementType = eastRandomType(1, { includeRecursive: false, includeFunctions: false });
    const arrayType = ArrayType(elementType);

    // Create a large array with random values
    const arraySize = random.int(5000, 10000);
    const valueGenerator = randomValueFor(elementType);
    const largeArray = Array.from({ length: arraySize }, () => valueGenerator());

    const input = e3.input('data', arrayType, largeArray);

    // Task that stringifies the array (works with any type)
    const task = e3.task(
      'stringify_array',
      [input],
      East.function(
        [arrayType],
        StringType,
        ($, arr) => East.str`array of ${arr.length()} elements`
      )
    );

    const pkg = e3.package(`large_array_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    if (startResult.exitCode !== 0) {
      throw new Error(`start failed: ${startResult.stderr}`);
    }

    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.stringify_array.output'], testDir);
    const output = getResult.stdout.trim();

    // Verify output contains expected array size
    const expectedPattern = `array of ${arraySize} elements`;
    if (!output.includes(expectedPattern)) {
      throw new Error(`Output mismatch: expected "${expectedPattern}" but got "${output}"`);
    }

    removeTestDir(testDir);

    return {
      success: true,
      state: {
        arraySize,
        elementType: elementType,
        actualOutput: output,
      },
      duration: Date.now() - startTime,
    };
  } catch (error) {
    return {
      success: false,
      error: error as Error,
      state: { testDir },
      duration: Date.now() - startTime,
    };
  }
}

/**
 * Test large string handling.
 * Creates strings with 10000-50000 characters.
 */
export async function testLargeStrings(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const stringSize = random.int(50000, 100000);
    const largeString = random.string(stringSize);

    const input = e3.input('text', StringType, largeString);

    // Task that returns info about the string
    const task = e3.task(
      'string_info',
      [input],
      East.function(
        [StringType],
        StringType,
        ($, s) => East.str`string of length ${s.length()}`
      )
    );

    const pkg = e3.package(`large_string_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    if (startResult.exitCode !== 0) {
      throw new Error(`start failed: ${startResult.stderr}`);
    }

    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.string_info.output'], testDir);
    const output = getResult.stdout.trim();

    // Verify output contains expected string length
    const expectedPattern = `string of length ${stringSize}`;
    if (!output.includes(expectedPattern)) {
      throw new Error(`Output mismatch: expected "${expectedPattern}" but got "${output}"`);
    }

    removeTestDir(testDir);

    return {
      success: true,
      state: {
        stringSize,
        actualOutput: output,
      },
      duration: Date.now() - startTime,
    };
  } catch (error) {
    return {
      success: false,
      error: error as Error,
      state: { testDir },
      duration: Date.now() - startTime,
    };
  }
}

/**
 * Test deeply nested data structures with random types.
 * Creates 2D arrays (array of arrays) with random element types.
 */
export async function testNestedStructures(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    // Generate a random element type (depth 1)
    const elementType = eastRandomType(1, { includeRecursive: false, includeFunctions: false });
    const rowType = ArrayType(elementType);
    const matrixType = ArrayType(rowType);

    // Create a 2D array with random values
    const rows = random.int(50, 100);
    const cols = random.int(50, 100);
    const valueGenerator = randomValueFor(elementType);

    const matrix: unknown[][] = [];
    for (let i = 0; i < rows; i++) {
      const row: unknown[] = [];
      for (let j = 0; j < cols; j++) {
        row.push(valueGenerator());
      }
      matrix.push(row);
    }

    const input = e3.input('matrix', matrixType, matrix);

    // Task that describes the matrix
    const task = e3.task(
      'matrix_info',
      [input],
      East.function(
        [matrixType],
        StringType,
        ($, m) => East.str`matrix with ${m.length()} rows`
      )
    );

    const pkg = e3.package(`nested_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    if (startResult.exitCode !== 0) {
      throw new Error(`start failed: ${startResult.stderr}`);
    }

    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.matrix_info.output'], testDir);
    const output = getResult.stdout.trim();

    // Verify output contains expected row count
    const expectedPattern = `matrix with ${rows} rows`;
    if (!output.includes(expectedPattern)) {
      throw new Error(`Output mismatch: expected "${expectedPattern}" but got "${output}"`);
    }

    removeTestDir(testDir);

    return {
      success: true,
      state: {
        rows,
        cols,
        totalElements: rows * cols,
        elementType: elementType,
        actualOutput: output,
      },
      duration: Date.now() - startTime,
    };
  } catch (error) {
    return {
      success: false,
      error: error as Error,
      state: { testDir },
      duration: Date.now() - startTime,
    };
  }
}

/**
 * Test deep DAG - long chain of tasks (10-20 deep).
 * Each task depends on the previous one, using random types.
 */
export async function testDeepDAG(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const depth = random.int(30, 50);

    // Use integers for deep DAG to focus on testing chain depth, not type complexity
    const initialValue = BigInt(random.int(1, 1000));

    const input = e3.input('x', IntegerType, initialValue);

    // First task stringifies the input
    const stringifyInit = e3.task(
      'stringify_init',
      [input],
      East.function(
        [IntegerType],
        StringType,
        ($, x) => East.str`${x}`
      )
    );

    // Create a chain of tasks, each passing through via stringify
    let prevOutput: DatasetDef = stringifyInit.output;
    const tasks: TaskDef[] = [stringifyInit];

    for (let i = 0; i < depth; i++) {
      const stepName = `step_${i}`;
      // Alternate between two string transformations
      if (i % 2 === 0) {
        // Prefix with step name
        const task = e3.task(
          stepName,
          [prevOutput],
          East.function(
            [StringType],
            StringType,
            ($, x) => East.str`${stepName}: ${x}`
          )
        );
        tasks.push(task);
        prevOutput = task.output;
      } else {
        // Suffix with step name
        const task = e3.task(
          stepName,
          [prevOutput],
          East.function(
            [StringType],
            StringType,
            ($, x) => East.str`${x} -> ${stepName}`
          )
        );
        tasks.push(task);
        prevOutput = task.output;
      }
    }

    // Pass last task - it will pull in all dependencies via the chain
    const pkg: PackageDef<any> = e3.package(`deep_dag_${random.string(6)}`, '1.0.0', tasks[tasks.length - 1]!);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    if (startResult.exitCode !== 0) {
      throw new Error(`start failed: ${startResult.stderr}`);
    }

    // Get the stringified initial value
    const initResult = await runE3Command(['get', repoDir, 'ws.tasks.stringify_init.output'], testDir);
    const initString = JSON.parse(initResult.stdout.trim()) as string;

    // Compute expected output by applying the transformations
    let expectedOutput = initString;
    for (let i = 0; i < depth; i++) {
      const stepName = `step_${i}`;
      if (i % 2 === 0) {
        expectedOutput = `${stepName}: ${expectedOutput}`;
      } else {
        expectedOutput = `${expectedOutput} -> ${stepName}`;
      }
    }

    // Check the final task output
    const lastTaskName = `step_${depth - 1}`;
    const getResult = await runE3Command(['get', repoDir, `ws.tasks.${lastTaskName}.output`], testDir);
    const output = getResult.stdout.trim();

    // Verify exact output match (output is JSON-encoded)
    const expectedJson = JSON.stringify(expectedOutput);
    if (output !== expectedJson) {
      throw new Error(`Output mismatch:\nExpected: ${expectedJson.slice(0, 200)}...\nActual: ${output.slice(0, 200)}...`);
    }

    removeTestDir(testDir);

    return {
      success: true,
      state: {
        depth,
        initialValue: initialValue.toString(),
        initialString: initString.slice(0, 50),
        actualOutput: output.slice(0, 100) + '...',
      },
      duration: Date.now() - startTime,
    };
  } catch (error) {
    return {
      success: false,
      error: error as Error,
      state: { testDir },
      duration: Date.now() - startTime,
    };
  }
}

/**
 * Test wide DAG - many parallel tasks (10-20 wide).
 * All tasks depend on the same input, then merge.
 */
export async function testWideDAG(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const width = random.int(30, 50);

    // Use integers for wide DAG to focus on testing parallelism, not type complexity
    const initialValue = BigInt(random.int(1, 1000));

    const input = e3.input('x', IntegerType, initialValue);

    // Create a stringify task to get the initial value as a string
    const stringifyInit = e3.task(
      'stringify_init',
      [input],
      East.function(
        [IntegerType],
        StringType,
        ($, x) => East.str`${x}`
      )
    );

    // Create many parallel tasks, each stringifying with a different prefix
    const parallelTasks: TaskDef[] = [];
    for (let i = 0; i < width; i++) {
      const prefix = `p${i}`;
      const task = e3.task(
        `parallel_${i}`,
        [input],
        East.function(
          [IntegerType],
          StringType,
          ($, x) => East.str`${prefix}: ${x}`
        )
      );
      parallelTasks.push(task);
    }

    // Create a merge task that concatenates all parallel outputs
    let mergeTask: TaskDef = e3.task(
      'merge_0_1',
      [parallelTasks[0]!.output, parallelTasks[1]!.output],
      East.function(
        [StringType, StringType],
        StringType,
        ($, a, b) => East.str`${a} | ${b}`
      )
    );

    const mergeTasks: TaskDef[] = [mergeTask];
    for (let i = 2; i < width; i++) {
      mergeTask = e3.task(
        `merge_${i}`,
        [mergeTask.output, parallelTasks[i]!.output],
        East.function(
          [StringType, StringType],
          StringType,
          ($, a, b) => East.str`${a} | ${b}`
        )
      );
      mergeTasks.push(mergeTask);
    }

    // Pass last merge task and stringify_init
    const pkg: PackageDef<any> = e3.package(`wide_dag_${random.string(6)}`, '1.0.0', mergeTask, stringifyInit);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    if (startResult.exitCode !== 0) {
      throw new Error(`start failed: ${startResult.stderr}`);
    }

    // Get the stringified initial value
    const initResult = await runE3Command(['get', repoDir, 'ws.tasks.stringify_init.output'], testDir);
    const initString = JSON.parse(initResult.stdout.trim()) as string;

    // Compute expected output: p0: X | p1: X | p2: X | ... | pN-1: X
    let expectedOutput = `p0: ${initString} | p1: ${initString}`;
    for (let i = 2; i < width; i++) {
      expectedOutput = `${expectedOutput} | p${i}: ${initString}`;
    }

    // Check the final merge task output
    const lastMergeName = `merge_${width - 1}`;
    const getResult = await runE3Command(['get', repoDir, `ws.tasks.${lastMergeName}.output`], testDir);
    const output = getResult.stdout.trim();

    // Verify exact output match (output is JSON-encoded)
    const expectedJson = JSON.stringify(expectedOutput);
    if (output !== expectedJson) {
      throw new Error(`Output mismatch:\nExpected: ${expectedJson.slice(0, 200)}...\nActual: ${output.slice(0, 200)}...`);
    }

    removeTestDir(testDir);

    return {
      success: true,
      state: {
        width,
        initialValue: initialValue.toString(),
        totalTasks: parallelTasks.length + mergeTasks.length + 1,
        initialString: initString.slice(0, 50),
        actualOutput: output.slice(0, 100) + '...',
      },
      duration: Date.now() - startTime,
    };
  } catch (error) {
    return {
      success: false,
      error: error as Error,
      state: { testDir },
      duration: Date.now() - startTime,
    };
  }
}

/**
 * Test diamond DAG at scale - multiple diamond patterns chained.
 * Tests both parallelism and dependency resolution with random types.
 */
export async function testDiamondChain(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const diamonds = random.int(8, 15);

    // Use integers for diamond chain to avoid exponential string growth
    // (each diamond doubles the output size since both branches stringify the input)
    const initialValue = BigInt(random.int(1, 1000));

    const input = e3.input('x', IntegerType, initialValue);

    // Create a stringify task to get the initial value as a string
    const stringifyInit = e3.task(
      'stringify_init',
      [input],
      East.function(
        [IntegerType],
        StringType,
        ($, x) => East.str`${x}`
      )
    );

    let prevOutput: DatasetDef = input;
    let prevType: EastType = IntegerType;
    const allTasks: TaskDef[] = [];

    // Create a chain of diamond patterns
    for (let d = 0; d < diamonds; d++) {
      const leftPrefix = `L${d}`;
      const rightPrefix = `R${d}`;

      // Left branch: stringify with "L" prefix
      const left = e3.task(
        `d${d}_left`,
        [prevOutput],
        East.function(
          [prevType],
          StringType,
          ($, x) => East.str`${leftPrefix}(${x})`
        )
      );

      // Right branch: stringify with "R" prefix
      const right = e3.task(
        `d${d}_right`,
        [prevOutput],
        East.function(
          [prevType],
          StringType,
          ($, x) => East.str`${rightPrefix}(${x})`
        )
      );

      // Merge: concatenate both branches
      const merge = e3.task(
        `d${d}_merge`,
        [left.output, right.output],
        East.function(
          [StringType, StringType],
          StringType,
          ($, a, b) => East.str`[${a}+${b}]`
        )
      );

      allTasks.push(left, right, merge);
      prevOutput = merge.output;
      prevType = StringType;
    }

    // Pass last merge task and stringify_init
    const pkg: PackageDef<any> = e3.package(`diamond_chain_${random.string(6)}`, '1.0.0', allTasks[allTasks.length - 1]!, stringifyInit);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    if (startResult.exitCode !== 0) {
      throw new Error(`start failed: ${startResult.stderr}`);
    }

    // Get the stringified initial value
    const initResult = await runE3Command(['get', repoDir, 'ws.tasks.stringify_init.output'], testDir);
    const initString = JSON.parse(initResult.stdout.trim()) as string;

    // Compute expected output by applying diamond transformations
    let expectedOutput = initString;
    for (let d = 0; d < diamonds; d++) {
      const leftPrefix = `L${d}`;
      const rightPrefix = `R${d}`;
      expectedOutput = `[${leftPrefix}(${expectedOutput})+${rightPrefix}(${expectedOutput})]`;
    }

    const lastMergeName = `d${diamonds - 1}_merge`;
    const getResult = await runE3Command(['get', repoDir, `ws.tasks.${lastMergeName}.output`], testDir);
    const output = getResult.stdout.trim();

    // Verify exact output match (output is JSON-encoded)
    const expectedJson = JSON.stringify(expectedOutput);
    if (output !== expectedJson) {
      throw new Error(`Output mismatch:\nExpected: ${expectedJson.slice(0, 200)}...\nActual: ${output.slice(0, 200)}...`);
    }

    removeTestDir(testDir);

    return {
      success: true,
      state: {
        diamonds,
        totalTasks: allTasks.length + 1,
        initialValue: initialValue.toString(),
        initialString: initString.slice(0, 50),
        actualOutput: output.slice(0, 100) + '...',
      },
      duration: Date.now() - startTime,
    };
  } catch (error) {
    return {
      success: false,
      error: error as Error,
      state: { testDir },
      duration: Date.now() - startTime,
    };
  }
}
