/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Test fixture creation utilities.
 *
 * Creates test packages using the @elaraai/e3 SDK to ensure
 * fixtures stay in sync with the SDK.
 */

import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

import e3 from '@elaraai/e3';
import { IntegerType, StringType, East } from '@elaraai/east';

/**
 * Create a simple compute package for testing.
 *
 * Creates a package with:
 * - Input: "value" (Integer, default 10)
 * - Task: "compute" - multiplies input by 2
 *
 * @param tempDir - Directory to write the zip file
 * @param name - Package name
 * @param version - Package version
 * @returns Path to the created zip file
 */
export async function createPackageZip(
  tempDir: string,
  name: string,
  version: string
): Promise<string> {
  mkdirSync(tempDir, { recursive: true });

  const input = e3.input('value', IntegerType, 10n);
  const task = e3.task(
    'compute',
    [input],
    East.function([IntegerType], IntegerType, ($, x) => x.multiply(2n))
  );
  const pkg = e3.package(name, version, task);

  const zipPath = join(tempDir, `${name}-${version}.zip`);
  await e3.export(pkg, zipPath);

  return zipPath;
}

/**
 * Create a package with multiple inputs for testing.
 *
 * Creates a package with:
 * - Input: "a" (Integer, default 1)
 * - Input: "b" (Integer, default 2)
 * - Task: "add" - returns a + b
 *
 * @param tempDir - Directory to write the zip file
 * @param name - Package name
 * @param version - Package version
 * @returns Path to the created zip file
 */
export async function createMultiInputPackageZip(
  tempDir: string,
  name: string,
  version: string
): Promise<string> {
  mkdirSync(tempDir, { recursive: true });

  const inputA = e3.input('a', IntegerType, 1n);
  const inputB = e3.input('b', IntegerType, 2n);
  const task = e3.task(
    'add',
    [inputA, inputB],
    East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.add(b))
  );
  const pkg = e3.package(name, version, task);

  const zipPath = join(tempDir, `${name}-${version}.zip`);
  await e3.export(pkg, zipPath);

  return zipPath;
}

/**
 * Create a package with string input for testing.
 *
 * Creates a package with:
 * - Input: "config" (String, default "default")
 * - Task: "echo" - returns input unchanged
 *
 * @param tempDir - Directory to write the zip file
 * @param name - Package name
 * @param version - Package version
 * @returns Path to the created zip file
 */
export async function createStringPackageZip(
  tempDir: string,
  name: string,
  version: string
): Promise<string> {
  mkdirSync(tempDir, { recursive: true });

  const input = e3.input('config', StringType, 'default');
  const task = e3.task(
    'echo',
    [input],
    East.function([StringType], StringType, ($, x) => x)
  );
  const pkg = e3.package(name, version, task);

  const zipPath = join(tempDir, `${name}-${version}.zip`);
  await e3.export(pkg, zipPath);

  return zipPath;
}

/**
 * Create a package with diamond dependencies for testing dataflow.
 *
 * Creates a package with:
 * - Input: "a" (Integer, default 10)
 * - Input: "b" (Integer, default 5)
 * - Task: "left" - returns a + b
 * - Task: "right" - returns a * b
 * - Task: "merge" - returns left + right
 *
 * @param tempDir - Directory to write the zip file
 * @param name - Package name
 * @param version - Package version
 * @returns Path to the created zip file
 */
export async function createDiamondPackageZip(
  tempDir: string,
  name: string,
  version: string
): Promise<string> {
  mkdirSync(tempDir, { recursive: true });

  const inputA = e3.input('a', IntegerType, 10n);
  const inputB = e3.input('b', IntegerType, 5n);

  const leftTask = e3.task(
    'left',
    [inputA, inputB],
    East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.add(b))
  );

  const rightTask = e3.task(
    'right',
    [inputA, inputB],
    East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.multiply(b))
  );

  const mergeTask = e3.task(
    'merge',
    [leftTask.output, rightTask.output],
    East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.add(b))
  );

  const pkg = e3.package(name, version, mergeTask);

  const zipPath = join(tempDir, `${name}-${version}.zip`);
  await e3.export(pkg, zipPath);

  return zipPath;
}
