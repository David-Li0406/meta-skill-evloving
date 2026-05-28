/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Failure reporter - logs failures to /tmp for reproduction
 */

import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { copyDir, formatDateForFilename } from './helpers.js';
import { createHash } from 'node:crypto';

const FAILURE_DIR = '/tmp/e3-fuzz-failures';

export interface FailureReport {
  timestamp: Date;
  scenario: string;
  seed: number;
  iteration: number;
  state: Record<string, unknown>;
  error: Error;
}

/**
 * Report a failure by saving state to /tmp
 */
export async function reportFailure(report: FailureReport): Promise<string> {
  // Create hash from state for unique directory name
  const stateStr = JSON.stringify(report.state);
  const hash = createHash('sha256').update(stateStr).digest('hex').slice(0, 8);
  const timestamp = formatDateForFilename(report.timestamp);
  const dirName = `${timestamp}-${hash}`;
  const failureDir = join(FAILURE_DIR, dirName);

  mkdirSync(failureDir, { recursive: true });

  // Save state as JSON
  writeFileSync(
    join(failureDir, 'state.json'),
    JSON.stringify(report.state, null, 2)
  );

  // Save error details
  writeFileSync(
    join(failureDir, 'error.txt'),
    `Scenario: ${report.scenario}
Seed: ${report.seed}
Iteration: ${report.iteration}
Timestamp: ${report.timestamp.toISOString()}

Error: ${report.error.message}

Stack Trace:
${report.error.stack ?? 'No stack trace available'}
`
  );

  // Copy repository snapshot if it exists
  const testDir = report.state.testDir as string | undefined;
  if (testDir && existsSync(testDir)) {
    try {
      copyDir(testDir, join(failureDir, 'repo'));
    } catch {
      // Ignore copy errors
    }
  }

  return failureDir;
}

/**
 * Print a summary of a failure to console
 */
export function printFailureSummary(report: FailureReport, failureDir: string): void {
  console.error(`\n❌ FAILURE in ${report.scenario}`);
  console.error(`   Error: ${report.error.message}`);
  console.error(`   Seed: ${report.seed}`);
  console.error(`   Iteration: ${report.iteration}`);
  console.error(`   Details saved to: ${failureDir}`);
}

/**
 * Print reproduction instructions
 */
export function printReproductionInstructions(seed: number, scenario?: string): void {
  console.error('\nTo reproduce:');
  if (scenario) {
    console.error(`  npm run fuzz -- --seed ${seed} --scenario ${scenario} -n 1`);
  } else {
    console.error(`  npm run fuzz -- --seed ${seed} -n 1`);
  }
}
