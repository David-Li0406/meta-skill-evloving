/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Concurrent operations scenarios - stress test race conditions
 *
 * These tests intentionally try to break things by simulating
 * realistic "idiot user" behavior - concurrent writes while
 * tasks are running, multiple simultaneous starts, etc.
 */

import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { East, IntegerType, variant } from '@elaraai/east';
import e3 from '@elaraai/e3';
import {
  dataflowExecute,
  workspaceSetDataset,
  WorkspaceLockError,
  LocalStorage,
} from '@elaraai/e3-core';
import {
  createTestDir,
  removeTestDir,
  runE3Command,
  random,
  type ScenarioResult,
} from '../helpers.js';

/**
 * Test concurrent writes while a task is running.
 *
 * This simulates a user frantically updating inputs while
 * execution is in progress. Expected to expose race conditions.
 */
export async function testConcurrentWritesDuringExecution(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    // Create a package with a slow-ish task
    const input = e3.input('x', IntegerType, 1n);

    // Task that does some work (identity, but gives us something to run)
    const task = e3.task(
      'compute',
      [input],
      East.function(
        [IntegerType],
        IntegerType,
        ($, x) => x.multiply(2n)
      )
    );

    const pkg = e3.package(`concurrent_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    // Setup
    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    // Start execution in background (don't await)
    const startPromise = runE3Command(['start', repoDir, 'ws'], testDir);

    // Blast concurrent writes while start is running
    const writePromises: Promise<any>[] = [];
    for (let i = 0; i < 10; i++) {
      const valuePath = join(testDir, `value_${i}.east`);
      writeFileSync(valuePath, `${i * 10}`);

      // Fire off set commands without waiting
      writePromises.push(
        runE3Command(['set', repoDir, 'ws.inputs.x', valuePath], testDir)
      );
    }

    // Wait for everything to complete
    const [startResult, ...writeResults] = await Promise.all([startPromise, ...writePromises]);

    // Check what happened
    const startSucceeded = startResult.exitCode === 0;
    const LOCK_ERROR_MSG = 'Workspace is locked by another process with PID:';
    const isLockError = (r: { stdout: string; stderr: string }) =>
      r.stdout.includes(LOCK_ERROR_MSG);
    const writeSuccesses = writeResults.filter(r => r.exitCode === 0).length;
    const writeFailures = writeResults.filter(r => r.exitCode !== 0).length;
    const lockErrors = writeResults.filter(r => r.exitCode !== 0 && isLockError(r)).length;

    // Get final output
    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.compute.output'], testDir);

    removeTestDir(testDir);

    // Verify expected behavior:
    // - Start should succeed (or fail with lock if a set got there first)
    // - Some operations should fail with lock errors (proves locking is working)
    const startLockError = isLockError(startResult);
    if (!startSucceeded && !startLockError) {
      throw new Error(`Start command failed with non-lock error: stdout=${startResult.stdout}, stderr=${startResult.stderr}`);
    }

    // Any failures must be lock errors
    const nonLockErrors = writeResults.filter(r => r.exitCode !== 0 && !isLockError(r));
    if (nonLockErrors.length > 0) {
      throw new Error(`Writes failed with unexpected errors: ${nonLockErrors.map(r => `stdout=${r.stdout}, stderr=${r.stderr}`).join('; ')}`);
    }

    // We expect at least some lock errors to prove locking is working
    const totalLockErrors = lockErrors + (startLockError ? 1 : 0);
    if (totalLockErrors === 0) {
      throw new Error(`Expected some operations to fail with lock errors, but all succeeded. Locking may not be working.`);
    }

    return {
      success: true,
      state: {
        startSucceeded,
        writeSuccesses,
        writeFailures,
        lockErrors,
        finalOutput: getResult.stdout.trim(),
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
 * Test multiple simultaneous start commands.
 *
 * What happens if user spams the start button?
 */
export async function testMultipleSimultaneousStarts(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('x', IntegerType, 42n);
    const task = e3.task(
      'double',
      [input],
      East.function(
        [IntegerType],
        IntegerType,
        ($, x) => x.multiply(2n)
      )
    );

    const pkg = e3.package(`multi_start_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    // Fire off 5 start commands simultaneously
    const startPromises = Array.from({ length: 5 }, () =>
      runE3Command(['start', repoDir, 'ws'], testDir!)
    );

    const results = await Promise.all(startPromises);

    const LOCK_ERROR_MSG = 'Workspace is locked by another process with PID:';
    const isLockError = (r: { stdout: string; stderr: string }) =>
      r.stdout.includes(LOCK_ERROR_MSG);
    const successes = results.filter(r => r.exitCode === 0).length;
    const failures = results.filter(r => r.exitCode !== 0).length;
    const lockErrors = results.filter(r => r.exitCode !== 0 && isLockError(r)).length;

    // Verify final state is consistent
    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.double.output'], testDir);

    removeTestDir(testDir);

    // Verify expected locking behavior:
    // - Exactly 1 start should succeed (got the lock)
    // - All others should fail with lock errors
    if (successes !== 1) {
      throw new Error(`Expected exactly 1 successful start, got ${successes}`);
    }

    if (failures !== 4) {
      throw new Error(`Expected 4 failed starts, got ${failures}`);
    }

    if (lockErrors !== 4) {
      const nonLockErrors = results.filter(r => r.exitCode !== 0 && !isLockError(r));
      throw new Error(`Expected 4 lock errors, got ${lockErrors}. Non-lock errors: ${nonLockErrors.map(r => `stdout=${r.stdout}, stderr=${r.stderr}`).join('; ')}`);
    }

    // Verify output is correct
    const finalOutput = getResult.stdout.trim();
    if (finalOutput !== '84') {
      throw new Error(`Expected output '84', got '${finalOutput}'`);
    }

    return {
      success: true,
      state: {
        successes,
        failures,
        lockErrors,
        finalOutput,
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
 * Test rapid fire set-then-start cycles with external locks.
 *
 * Simulates multiple users doing "set then start" as an atomic operation
 * by acquiring a lock, doing both operations, then releasing.
 * Uses e3-core API directly since locks are object handles.
 */
export async function testRapidSetStartCycles(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('x', IntegerType, 1n);
    const task = e3.task(
      'double',
      [input],
      East.function(
        [IntegerType],
        IntegerType,
        ($, x) => x.multiply(2n)
      )
    );

    const pkg = e3.package(`rapid_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    // Simulate multiple users doing atomic "set then start" concurrently
    // Each batch acquires a lock, does set+start, then releases
    interface BatchResult {
      value: number;
      success: boolean;
      lockError: boolean;
      error?: string;
    }

    const batches = Array.from({ length: 10 }, (_, i) => {
      const value = BigInt(i + 1);

      return (async (): Promise<BatchResult> => {
        try {
          const storage = new LocalStorage();
          // Try to acquire lock (non-blocking)
          const lock = await storage.locks.acquire(repoDir, 'ws', variant('dataflow', null));
          if (!lock) {
            return { value: Number(value), success: false, lockError: true };
          }
          try {
            // Set the input value using the lock
            await workspaceSetDataset(storage, repoDir, 'ws', [variant('field', 'inputs'), variant('field', 'x')], value, IntegerType, { lock });
            // Execute dataflow using the lock
            await dataflowExecute(storage, repoDir, 'ws', { lock });
            return { value: Number(value), success: true, lockError: false };
          } finally {
            await lock.release();
          }
        } catch (err) {
          if (err instanceof WorkspaceLockError) {
            return { value: Number(value), success: false, lockError: true };
          }
          return { value: Number(value), success: false, lockError: false, error: String(err) };
        }
      })();
    });

    const results = await Promise.all(batches);

    // Count outcomes
    const fullSuccesses = results.filter(r => r.success).length;
    const lockErrors = results.filter(r => r.lockError).length;
    const otherErrors = results.filter(r => !r.success && !r.lockError);

    // Final state check
    const getResult = await runE3Command(['get', repoDir, 'ws.tasks.double.output'], testDir);

    removeTestDir(testDir);

    // Verify at least one batch completed fully
    if (fullSuccesses < 1) {
      const summary = results.map(r =>
        `batch${r.value}: ${r.success ? 'ok' : r.lockError ? 'locked' : r.error}`
      ).join('; ');
      throw new Error(`Expected at least 1 fully successful batch, got ${fullSuccesses}. Results: ${summary}`);
    }

    // All failures must be lock errors
    if (otherErrors.length > 0) {
      throw new Error(`Unexpected errors: ${otherErrors.map(r => `batch${r.value}: ${r.error}`).join('; ')}`);
    }

    // We expect at least some lock errors to prove locking is working
    if (lockErrors === 0) {
      throw new Error(`Expected some batches to fail with lock errors, but all ${fullSuccesses} succeeded. Locking may not be working.`);
    }

    // Verify we got a valid output (should be even number since we double)
    const finalOutput = getResult.stdout.trim();
    const outputNum = parseInt(finalOutput, 10);
    if (isNaN(outputNum) || outputNum % 2 !== 0) {
      throw new Error(`Expected even number output, got '${finalOutput}'`);
    }

    return {
      success: true,
      state: {
        fullSuccesses,
        lockErrors,
        finalOutput,
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
 * Test interleaved operations on multiple workspaces.
 *
 * User has multiple workspaces open and is clicking around.
 */
export async function testInterleavedMultiWorkspace(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const input = e3.input('x', IntegerType, 1n);
    const task = e3.task(
      'double',
      [input],
      East.function(
        [IntegerType],
        IntegerType,
        ($, x) => x.multiply(2n)
      )
    );

    const pkg = e3.package(`multi_ws_${random.string(6)}`, '1.0.0', task);

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);

    // Create 3 workspaces
    await runE3Command(['workspace', 'create', repoDir, 'ws1'], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws2'], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws3'], testDir);

    await runE3Command(['workspace', 'deploy', repoDir, 'ws1', `${pkg.name}@${pkg.version}`], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws2', `${pkg.name}@${pkg.version}`], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws3', `${pkg.name}@${pkg.version}`], testDir);

    // Interleaved operations across workspaces
    const ops: Promise<any>[] = [];
    for (let i = 0; i < 5; i++) {
      // Random workspace operations
      ops.push(runE3Command(['start', repoDir, 'ws1'], testDir));
      ops.push(runE3Command(['start', repoDir, 'ws2'], testDir));
      ops.push(runE3Command(['start', repoDir, 'ws3'], testDir));
    }

    const results = await Promise.all(ops);
    const LOCK_ERROR_MSG = 'Workspace is locked by another process with PID:';
    const isLockError = (r: { stdout: string; stderr: string }) =>
      r.stdout.includes(LOCK_ERROR_MSG);
    const successes = results.filter(r => r.exitCode === 0).length;
    const lockErrors = results.filter(r => r.exitCode !== 0 && isLockError(r)).length;

    // Verify each workspace has valid output
    const get1 = await runE3Command(['get', repoDir, 'ws1.tasks.double.output'], testDir);
    const get2 = await runE3Command(['get', repoDir, 'ws2.tasks.double.output'], testDir);
    const get3 = await runE3Command(['get', repoDir, 'ws3.tasks.double.output'], testDir);

    removeTestDir(testDir);

    // Verify behavior:
    // - Some starts should fail with lock errors (same workspace locked)
    // - Different workspaces should not block each other
    // - All failures must be lock errors
    const failures = results.filter(r => r.exitCode !== 0).length;
    if (failures > 0 && lockErrors !== failures) {
      const nonLockErrors = results.filter(r => r.exitCode !== 0 && !isLockError(r));
      throw new Error(`Failures should be lock errors. Got ${lockErrors} lock errors out of ${failures} failures. Non-lock errors: ${nonLockErrors.map(r => `stdout=${r.stdout}, stderr=${r.stderr}`).join('; ')}`);
    }

    // We expect at least some lock errors to prove locking is working
    // (5 iterations * 3 workspaces = 15 starts, but each workspace can only run 1 at a time)
    if (lockErrors === 0) {
      throw new Error(`Expected some starts to fail with lock errors, but all ${successes} starts succeeded. Locking may not be working.`);
    }

    // Verify all workspaces produced correct output
    const ws1Output = get1.stdout.trim();
    const ws2Output = get2.stdout.trim();
    const ws3Output = get3.stdout.trim();

    if (ws1Output !== '2' || ws2Output !== '2' || ws3Output !== '2') {
      throw new Error(`Expected all outputs to be '2', got ws1='${ws1Output}', ws2='${ws2Output}', ws3='${ws3Output}'`);
    }

    return {
      success: true,
      state: {
        successes,
        lockErrors,
        totalOps: results.length,
        ws1Output,
        ws2Output,
        ws3Output,
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
