/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Package lifecycle scenario: create, export, import, deploy
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

export interface PackageLifecycleConfig {
  /** Use simple package instead of random */
  simple?: boolean;
  /** Use diamond package */
  diamond?: boolean;
}

/**
 * Test the full package lifecycle:
 * 1. Create package using SDK
 * 2. Export to zip
 * 3. Init repository
 * 4. Import package
 * 5. Create workspace
 * 6. Deploy package
 * 7. Verify status
 */
export async function testPackageLifecycle(config: PackageLifecycleConfig = {}): Promise<ScenarioResult> {
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

    // Step 1-2: Export package to zip
    await e3.export(pkg, zipPath);
    assert(existsSync(zipPath), 'Package zip should exist after export');

    // Step 3: Init repository
    const initResult = await runE3Command(['repo', 'create', repoDir], testDir);
    assert(initResult.exitCode === 0, `init failed: ${initResult.stderr}`);
    assert(existsSync(join(repoDir, 'objects')), 'objects directory should exist');

    // Step 4: Import package
    const importResult = await runE3Command(['package', 'import', repoDir, zipPath], testDir);
    assert(importResult.exitCode === 0, `import failed: ${importResult.stderr}`);

    // Verify package is listed
    const listPkgResult = await runE3Command(['package', 'list', repoDir], testDir);
    assert(listPkgResult.exitCode === 0, `package list failed: ${listPkgResult.stderr}`);
    assert(
      listPkgResult.stdout.includes(pkg.name),
      `Package ${pkg.name} should be listed, got: ${listPkgResult.stdout}`
    );

    // Step 5: Create workspace
    const wsName = 'test-ws';
    const wsCreateResult = await runE3Command(['workspace', 'create', repoDir, wsName], testDir);
    assert(wsCreateResult.exitCode === 0, `workspace create failed: ${wsCreateResult.stderr}`);

    // Step 6: Deploy package
    const deployResult = await runE3Command(
      ['workspace', 'deploy', repoDir, wsName, `${pkg.name}@${pkg.version}`],
      testDir
    );
    assert(deployResult.exitCode === 0, `deploy failed: ${deployResult.stderr}`);

    // Step 7: Verify status
    const statusResult = await runE3Command(['repo', 'status', repoDir], testDir);
    assert(statusResult.exitCode === 0, `status failed: ${statusResult.stderr}`);

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
