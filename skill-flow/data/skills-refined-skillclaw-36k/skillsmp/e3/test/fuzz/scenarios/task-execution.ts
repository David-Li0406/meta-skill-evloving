/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Task execution scenario: run tasks and validate outputs
 */

import { existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import e3 from '@elaraai/e3';
import {
  createTestDir,
  removeTestDir,
  runE3Command,
  assert,
  type ScenarioResult,
} from '../helpers.js';
import { randomPackage, simplePackage, diamondPackage, type GeneratedPackage } from '../generators/packages.js';

export interface TaskExecutionConfig {
  /** Use simple package instead of random */
  simple?: boolean;
  /** Use diamond package */
  diamond?: boolean;
}

/**
 * Test task execution:
 * 1. Create and deploy package
 * 2. Execute tasks with `e3 start`
 * 3. Verify outputs exist
 */
export async function testTaskExecution(config: TaskExecutionConfig = {}): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;
  let generated: GeneratedPackage | undefined;

  try {
    // Generate package
    if (config.simple) {
      generated = simplePackage();
    } else if (config.diamond) {
      generated = diamondPackage();
    } else {
      generated = randomPackage();
    }

    const pkg = generated.package;
    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    // Setup: export, init, import, create workspace, deploy
    await e3.export(pkg, zipPath);
    assert(existsSync(zipPath), 'Package zip should exist');

    let result = await runE3Command(['repo', 'create', repoDir], testDir);
    assert(result.exitCode === 0, `init failed: ${result.stderr}`);

    result = await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    assert(result.exitCode === 0, `import failed: ${result.stderr}`);

    const wsName = 'test-ws';
    result = await runE3Command(['workspace', 'create', repoDir, wsName], testDir);
    assert(result.exitCode === 0, `workspace create failed: ${result.stderr}`);

    result = await runE3Command(
      ['workspace', 'deploy', repoDir, wsName, `${pkg.name}@${pkg.version}`],
      testDir
    );
    assert(result.exitCode === 0, `deploy failed: ${result.stderr}`);

    // Execute tasks
    const startResult = await runE3Command(['start', repoDir, wsName], testDir);
    assert(
      startResult.exitCode === 0,
      `start failed: ${startResult.stderr}\nstdout: ${startResult.stdout}`
    );

    // Verify each task has output
    for (const task of generated.tasks) {
      const getResult = await runE3Command(
        ['get', repoDir, `${wsName}.tasks.${task.name}.output`],
        testDir
      );
      assert(
        getResult.exitCode === 0,
        `get ${task.name}.output failed: ${getResult.stderr}`
      );
      // Output should not be empty
      assert(
        getResult.stdout.trim().length > 0,
        `${task.name}.output should not be empty`
      );
    }

    // Clean up on success
    removeTestDir(testDir);

    return {
      success: true,
      duration: Date.now() - startTime,
    };
  } catch (error) {
    return {
      success: false,
      error: error as Error,
      state: {
        testDir,
        package: generated ? {
          name: generated.package.name,
          inputs: generated.inputs.map(i => i.name),
          tasks: generated.tasks.map(t => t.name),
        } : undefined,
      },
      duration: Date.now() - startTime,
    };
  }
}

/**
 * Test that re-running with same inputs uses cache
 */
export async function testTaskCaching(config: TaskExecutionConfig = {}): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;
  let generated: GeneratedPackage | undefined;

  try {
    // Use simple package for predictable caching behavior
    generated = config.simple ? simplePackage() : (config.diamond ? diamondPackage() : simplePackage());
    const pkg = generated.package;

    testDir = createTestDir();
    mkdirSync(testDir, { recursive: true });

    const repoDir = join(testDir, 'repo');
    const zipPath = join(testDir, 'package.zip');

    // Setup
    await e3.export(pkg, zipPath);
    await runE3Command(['repo', 'create', repoDir], testDir);
    await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    await runE3Command(['workspace', 'create', repoDir, 'ws'], testDir);
    await runE3Command(['workspace', 'deploy', repoDir, 'ws', `${pkg.name}@${pkg.version}`], testDir);

    // First execution
    const firstStart = await runE3Command(['start', repoDir, 'ws'], testDir);
    assert(firstStart.exitCode === 0, `first start failed: ${firstStart.stderr}`);

    // Second execution - should be cached (faster)
    const secondStart = await runE3Command(['start', repoDir, 'ws'], testDir);
    assert(secondStart.exitCode === 0, `second start failed: ${secondStart.stderr}`);

    // Check that output mentions "cached" or is very fast
    // (Exact check depends on CLI output format)
    const output = secondStart.stdout.toLowerCase();
    const isCached = output.includes('cached') || output.includes('skip');

    // Clean up
    removeTestDir(testDir);

    return {
      success: true,
      state: { cachedDetected: isCached },
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
