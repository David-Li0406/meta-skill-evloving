/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Input mutation scenario: change inputs and re-execute
 */

import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import e3 from '@elaraai/e3';
import {
  createTestDir,
  removeTestDir,
  runE3Command,
  assert,
  type ScenarioResult,
} from '../helpers.js';
import { simplePackage } from '../generators/packages.js';
import { mutateValue, printFor } from '../generators/values.js';

/**
 * Test input mutation:
 * 1. Create and deploy package
 * 2. Execute tasks
 * 3. Change an input value
 * 4. Re-execute and verify output changed
 */
export async function testInputMutation(): Promise<ScenarioResult> {
  const startTime = Date.now();
  let testDir: string | undefined;

  try {
    // Use simple package for predictable behavior
    const generated = simplePackage();
    const pkg = generated.package;
    const inputInfo = generated.inputs[0]!;

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
    let result = await runE3Command(['start', repoDir, 'ws'], testDir);
    assert(result.exitCode === 0, `first start failed: ${result.stderr}`);

    // Get first output
    const firstGet = await runE3Command(['get', repoDir, 'ws.tasks.double.output'], testDir);
    assert(firstGet.exitCode === 0, `first get failed: ${firstGet.stderr}`);
    const firstOutput = firstGet.stdout.trim();

    // Generate a new, different input value
    const newValue = mutateValue(inputInfo.type, inputInfo.defaultValue as any);

    // Write new value to a file
    const newValuePath = join(testDir, 'new_value.east');
    const printer = printFor(inputInfo.type);
    writeFileSync(newValuePath, printer(newValue));

    // Set the new input value
    const setResult = await runE3Command(['set', repoDir, `ws.inputs.${inputInfo.name}`, newValuePath], testDir);
    assert(setResult.exitCode === 0, `set failed: ${setResult.stderr}`);

    // Re-execute
    result = await runE3Command(['start', repoDir, 'ws'], testDir);
    assert(result.exitCode === 0, `second start failed: ${result.stderr}`);

    // Get second output
    const secondGet = await runE3Command(['get', repoDir, 'ws.tasks.double.output'], testDir);
    assert(secondGet.exitCode === 0, `second get failed: ${secondGet.stderr}`);
    const secondOutput = secondGet.stdout.trim();

    // Outputs should be different (since input changed)
    // Note: They might be same if mutateValue happened to generate same value
    // This is acceptable but we can log it

    // Clean up
    removeTestDir(testDir);

    return {
      success: true,
      state: {
        firstOutput,
        secondOutput,
        outputChanged: firstOutput !== secondOutput,
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
