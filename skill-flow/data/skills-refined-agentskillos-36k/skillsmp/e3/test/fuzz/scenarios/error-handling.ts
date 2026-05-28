/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Error handling scenarios - verify failures are caught and reported properly
 */

import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { East, IntegerType, FloatType, StringType, ArrayType } from '@elaraai/east';
import e3 from '@elaraai/e3';
import {
  createTestDir,
  removeTestDir,
  runE3Command,
  assert,
  random,
  type ScenarioResult,
} from '../helpers.js';

/**
 * Test that division by zero is handled properly
 */
export async function testDivisionByZero(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('x', IntegerType, 10n);

    // Task that divides by zero
    const task = e3.task(
      'divide',
      [input],
      East.function(
        [IntegerType],
        IntegerType,
        ($, x) => x.divide(0n)
      )
    );

    const pkg = e3.package(`div_zero_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    // This should fail gracefully
    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);

    // Either exit code is non-zero OR output mentions error/fail
    const output = (startResult.stdout + startResult.stderr).toLowerCase();
    const indicatesFailure = startResult.exitCode !== 0 ||
      output.includes('error') ||
      output.includes('fail') ||
      output.includes('exception');

    assert(indicatesFailure, `Division by zero should fail, got exitCode=${startResult.exitCode}`);

    removeTestDir(testDir);

    return {
      success: true,
      state: { exitCode: startResult.exitCode, indicatesFailure },
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
 * Test that array index out of bounds is handled properly
 */
export async function testArrayOutOfBounds(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('arr', ArrayType(IntegerType), [1n, 2n, 3n]);

    // Task that accesses out of bounds index
    const task = e3.task(
      'oob',
      [input],
      East.function(
        [ArrayType(IntegerType)],
        IntegerType,
        ($, arr) => arr.get(100n)  // Index 100 doesn't exist
      )
    );

    const pkg = e3.package(`oob_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);

    const output = (startResult.stdout + startResult.stderr).toLowerCase();
    const indicatesFailure = startResult.exitCode !== 0 ||
      output.includes('error') ||
      output.includes('fail') ||
      output.includes('bound') ||
      output.includes('index');

    assert(indicatesFailure, `Array OOB should fail, got exitCode=${startResult.exitCode}`);

    removeTestDir(testDir);

    return {
      success: true,
      state: { exitCode: startResult.exitCode, indicatesFailure },
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
 * Test that custom task with failing bash command is handled
 */
export async function testCustomTaskFailure(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('x', IntegerType, 1n);

    // Custom task that always fails
    const task = e3.customTask(
      'fail',
      [input],
      IntegerType,
      (_$, _inputs, _output) => East.str`exit 1`
    );

    const pkg = e3.package(`fail_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);

    const output = (startResult.stdout + startResult.stderr).toLowerCase();
    const indicatesFailure = startResult.exitCode !== 0 ||
      output.includes('error') ||
      output.includes('fail');

    assert(indicatesFailure, `Custom task exit 1 should fail, got exitCode=${startResult.exitCode}`);

    removeTestDir(testDir);

    return {
      success: true,
      state: { exitCode: startResult.exitCode, indicatesFailure },
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
 * Test NaN handling in float operations
 */
export async function testNaNHandling(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    // Input NaN
    const input = e3.input('x', FloatType, NaN);

    // Task that uses NaN
    const task = e3.task(
      'use_nan',
      [input],
      East.function(
        [FloatType],
        StringType,
        ($, x) => East.str`value is ${x}`
      )
    );

    const pkg = e3.package(`nan_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    // This should succeed - NaN is a valid float value
    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    assert(startResult.exitCode === 0, `NaN handling should succeed: ${startResult.stderr}`);

    // Output should contain NaN representation
    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.use_nan.output'], testDir);
    assert(getResult.exitCode === 0, `get should succeed: ${getResult.stderr}`);

    removeTestDir(testDir);

    return {
      success: true,
      state: { output: getResult.stdout.trim() },
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
 * Test Infinity handling
 */
export async function testInfinityHandling(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('x', FloatType, Infinity);

    const task = e3.task(
      'use_inf',
      [input],
      East.function(
        [FloatType],
        StringType,
        ($, x) => East.str`value is ${x}`
      )
    );

    const pkg = e3.package(`inf_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    assert(startResult.exitCode === 0, `Infinity handling should succeed: ${startResult.stderr}`);

    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.use_inf.output'], testDir);
    assert(getResult.exitCode === 0, `get should succeed: ${getResult.stderr}`);

    removeTestDir(testDir);

    return {
      success: true,
      state: { output: getResult.stdout.trim() },
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
 * Test empty string handling
 */
export async function testEmptyStringHandling(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('s', StringType, '');

    const task = e3.task(
      'use_empty',
      [input],
      East.function(
        [StringType],
        StringType,
        ($, s) => East.str`length is ${s.length()}`
      )
    );

    const pkg = e3.package(`empty_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    assert(startResult.exitCode === 0, `Empty string should succeed: ${startResult.stderr}`);

    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.use_empty.output'], testDir);
    assert(getResult.exitCode === 0, `get should succeed: ${getResult.stderr}`);
    assert(getResult.stdout.includes('0'), `Empty string length should be 0: ${getResult.stdout}`);

    removeTestDir(testDir);

    return {
      success: true,
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
 * Test empty array handling
 */
export async function testEmptyArrayHandling(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('arr', ArrayType(IntegerType), []);

    const task = e3.task(
      'use_empty_arr',
      [input],
      East.function(
        [ArrayType(IntegerType)],
        StringType,
        ($, arr) => East.str`length is ${arr.size()}`
      )
    );

    const pkg = e3.package(`empty_arr_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    const startResult = await runE3Command(['start', repoDir, 'ws'], testDir);
    assert(startResult.exitCode === 0, `Empty array should succeed: ${startResult.stderr}`);

    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.use_empty_arr.output'], testDir);
    assert(getResult.exitCode === 0, `get should succeed: ${getResult.stderr}`);
    assert(getResult.stdout.includes('0'), `Empty array length should be 0: ${getResult.stdout}`);

    removeTestDir(testDir);

    return {
      success: true,
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
