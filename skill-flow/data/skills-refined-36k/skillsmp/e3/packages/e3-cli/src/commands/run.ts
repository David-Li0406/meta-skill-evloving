/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 run command - Ad-hoc task execution
 *
 * Usage:
 *   e3 run . acme-forecast/train ./sales.beast2 -o ./model.beast2
 *   e3 run . my-pkg@1.0.0/process ./input1.beast2 ./input2.beast2 -o ./output.beast2
 *   e3 run . my-pkg/task ./data.beast2 -o ./out.beast2 --force
 */

import { readFile, writeFile } from 'fs/promises';
import {
  packageRead,
  objectWrite,
  objectRead,
  taskExecute,
  LocalStorage,
} from '@elaraai/e3-core';
import { decodeBeast2 } from '@elaraai/east';
import { resolveRepo, parsePackageSpec, formatError, exitError } from '../utils.js';

/**
 * Parse task specifier: pkg/task or pkg@version/task
 */
function parseTaskSpec(spec: string): { name: string; version: string; task: string } {
  const slashIndex = spec.indexOf('/');
  if (slashIndex === -1) {
    throw new Error(
      `Invalid task specifier: ${spec}. Expected format: pkg/task or pkg@version/task`
    );
  }

  const pkgPart = spec.slice(0, slashIndex);
  const task = spec.slice(slashIndex + 1);

  if (!task) {
    throw new Error(
      `Invalid task specifier: ${spec}. Task name cannot be empty.`
    );
  }

  const { name, version } = parsePackageSpec(pkgPart);
  return { name, version, task };
}

/**
 * Run a task ad-hoc with file inputs and output.
 */
export async function runCommand(
  repoArg: string,
  taskSpec: string,
  inputs: string[],
  options: { output?: string; force?: boolean }
): Promise<void> {
  try {
    const repoPath = resolveRepo(repoArg);
    const storage = new LocalStorage();

    // Parse task specifier
    const { name, version, task } = parseTaskSpec(taskSpec);

    // Validate output is provided
    if (!options.output) {
      exitError('Output file is required. Use -o <path> to specify output.');
    }

    // Get package and find task hash
    const pkg = await packageRead(storage, repoPath, name, version);
    const taskHash = pkg.tasks.get(task);

    if (!taskHash) {
      const available = Array.from(pkg.tasks.keys()).join(', ');
      exitError(
        `Task '${task}' not found in ${name}@${version}. Available: ${available || '(none)'}`
      );
    }

    console.log(`Running ${name}@${version}/${task}`);

    // Read input files and store as objects
    const inputHashes: string[] = [];
    for (const inputPath of inputs) {
      const data = await readFile(inputPath);

      // Verify it's valid beast2 (will throw if not)
      try {
        decodeBeast2(data);
      } catch {
        exitError(`Invalid beast2 file: ${inputPath}`);
      }

      const hash = await objectWrite(repoPath, data);
      inputHashes.push(hash);
      console.log(`  Input: ${inputPath} -> ${hash.slice(0, 8)}...`);
    }

    // Execute the task
    const startTime = Date.now();
    const result = await taskExecute(storage, repoPath, taskHash, inputHashes, {
      force: options.force,
    });

    const elapsed = Date.now() - startTime;

    if (result.cached) {
      console.log(`Cached (${elapsed}ms)`);
    } else {
      console.log(`Done (${elapsed}ms)`);
    }

    // Handle result
    if (result.state === 'success' && result.outputHash) {
      // Read output object and write to file
      const outputData = await objectRead(repoPath, result.outputHash);
      await writeFile(options.output, outputData);
      console.log(`Output: ${options.output}`);
    } else if (result.state === 'failed') {
      console.error(`Task failed with exit code: ${result.exitCode}`);
      process.exit(1);
    } else if (result.state === 'error') {
      exitError(result.error ?? 'Unknown error');
    }
  } catch (err) {
    exitError(formatError(err));
  }
}
