/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Fuzz test runner - orchestrates test execution
 */

import { setRandomSeed, getRandomSeed, formatDuration } from './helpers.js';
import { reportFailure, printFailureSummary, printReproductionInstructions } from './reporter.js';
import { testPackageLifecycle } from './scenarios/package-lifecycle.js';
import { testTaskExecution, testTaskCaching } from './scenarios/task-execution.js';
import { testInputMutation } from './scenarios/input-mutation.js';
import {
  testDivisionByZero,
  testArrayOutOfBounds,
  testCustomTaskFailure,
  testNaNHandling,
  testInfinityHandling,
  testEmptyStringHandling,
  testEmptyArrayHandling,
} from './scenarios/error-handling.js';
import {
  testConcurrentWritesDuringExecution,
  testMultipleSimultaneousStarts,
  testRapidSetStartCycles,
  testInterleavedMultiWorkspace,
} from './scenarios/concurrent-ops.js';
import {
  testLargeArrays,
  testLargeStrings,
  testNestedStructures,
  testDeepDAG,
  testWideDAG,
  testDiamondChain,
} from './scenarios/stress.js';

export interface RunnerConfig {
  /** Number of iterations to run */
  iterations: number;
  /** Specific scenario to run (or undefined for all) */
  scenario?: string;
  /** Random seed for reproducibility */
  seed?: number;
  /** Stop on first failure */
  stopOnFailure: boolean;
  /** Verbose output */
  verbose: boolean;
}

export interface RunnerResults {
  passed: number;
  failed: number;
  duration: number;
  failures: Array<{
    scenario: string;
    iteration: number;
    dir: string;
  }>;
}

interface Scenario {
  name: string;
  fn: () => Promise<{ success: boolean; error?: Error; state?: Record<string, unknown>; duration: number }>;
}

const scenarios: Scenario[] = [
  // Package lifecycle
  { name: 'package-lifecycle', fn: testPackageLifecycle },
  { name: 'package-lifecycle-simple', fn: () => testPackageLifecycle({ simple: true }) },
  { name: 'package-lifecycle-diamond', fn: () => testPackageLifecycle({ diamond: true }) },

  // Task execution
  { name: 'task-execution', fn: testTaskExecution },
  { name: 'task-execution-simple', fn: () => testTaskExecution({ simple: true }) },
  { name: 'task-execution-diamond', fn: () => testTaskExecution({ diamond: true }) },
  { name: 'task-caching', fn: testTaskCaching },

  // Input mutation
  { name: 'input-mutation', fn: testInputMutation },

  // Error handling - failures that should be caught
  { name: 'error-division-by-zero', fn: testDivisionByZero },
  { name: 'error-array-oob', fn: testArrayOutOfBounds },
  { name: 'error-custom-task-fail', fn: testCustomTaskFailure },

  // Edge cases - should succeed
  { name: 'edge-nan', fn: testNaNHandling },
  { name: 'edge-infinity', fn: testInfinityHandling },
  { name: 'edge-empty-string', fn: testEmptyStringHandling },
  { name: 'edge-empty-array', fn: testEmptyArrayHandling },

  // Concurrent operations - stress test race conditions
  { name: 'concurrent-writes-during-exec', fn: testConcurrentWritesDuringExecution },
  { name: 'concurrent-multiple-starts', fn: testMultipleSimultaneousStarts },
  { name: 'concurrent-rapid-set-start', fn: testRapidSetStartCycles },
  { name: 'concurrent-multi-workspace', fn: testInterleavedMultiWorkspace },

  // Stress tests - large data and complex DAGs
  { name: 'stress-large-arrays', fn: testLargeArrays },
  { name: 'stress-large-strings', fn: testLargeStrings },
  { name: 'stress-nested-structures', fn: testNestedStructures },
  { name: 'stress-deep-dag', fn: testDeepDAG },
  { name: 'stress-wide-dag', fn: testWideDAG },
  { name: 'stress-diamond-chain', fn: testDiamondChain },
];

/**
 * Run fuzz tests
 */
export async function runFuzzTests(config: RunnerConfig): Promise<RunnerResults> {
  const startTime = Date.now();

  // Set up random seed
  if (config.seed !== undefined) {
    setRandomSeed(config.seed);
  }
  const seed = getRandomSeed();

  const results: RunnerResults = {
    passed: 0,
    failed: 0,
    duration: 0,
    failures: [],
  };

  // Filter scenarios if specified
  const activeScenarios = config.scenario
    ? scenarios.filter(s => s.name === config.scenario || s.name.startsWith(config.scenario + '-'))
    : scenarios;

  if (activeScenarios.length === 0) {
    console.error(`No scenarios matching: ${config.scenario}`);
    console.error(`Available scenarios: ${scenarios.map(s => s.name).join(', ')}`);
    return results;
  }

  console.log(`Running ${config.iterations} iterations across ${activeScenarios.length} scenarios`);
  console.log(`Seed: ${seed}\n`);

  for (let i = 0; i < config.iterations; i++) {
    for (const scenario of activeScenarios) {
      if (config.verbose) {
        process.stdout.write(`[${i + 1}/${config.iterations}] ${scenario.name}... `);
      }

      try {
        const result = await scenario.fn();

        if (result.success) {
          results.passed++;
          if (config.verbose) {
            console.log(`✓ (${formatDuration(result.duration)})`);
          }
        } else {
          results.failed++;

          const failureDir = await reportFailure({
            timestamp: new Date(),
            scenario: scenario.name,
            seed,
            iteration: i,
            state: result.state ?? {},
            error: result.error ?? new Error('Unknown error'),
          });

          results.failures.push({
            scenario: scenario.name,
            iteration: i,
            dir: failureDir,
          });

          printFailureSummary({
            timestamp: new Date(),
            scenario: scenario.name,
            seed,
            iteration: i,
            state: result.state ?? {},
            error: result.error ?? new Error('Unknown error'),
          }, failureDir);

          if (config.stopOnFailure) {
            printReproductionInstructions(seed, scenario.name);
            results.duration = Date.now() - startTime;
            return results;
          }
        }
      } catch (error) {
        results.failed++;

        const failureDir = await reportFailure({
          timestamp: new Date(),
          scenario: scenario.name,
          seed,
          iteration: i,
          state: {},
          error: error as Error,
        });

        results.failures.push({
          scenario: scenario.name,
          iteration: i,
          dir: failureDir,
        });

        if (config.verbose) {
          console.log(`✗ ${(error as Error).message}`);
        }

        printFailureSummary({
          timestamp: new Date(),
          scenario: scenario.name,
          seed,
          iteration: i,
          state: {},
          error: error as Error,
        }, failureDir);

        if (config.stopOnFailure) {
          printReproductionInstructions(seed, scenario.name);
          results.duration = Date.now() - startTime;
          return results;
        }
      }
    }

    // Progress indicator for non-verbose mode
    if (!config.verbose) {
      const completed = (i + 1) * activeScenarios.length;
      const total = config.iterations * activeScenarios.length;
      const pct = Math.round((completed / total) * 100);
      const elapsed = formatDuration(Date.now() - startTime);
      process.stdout.write(`\r[${pct}%] ${i + 1}/${config.iterations} iterations, ${results.passed} passed, ${results.failed} failed (${elapsed})`);
    }
  }

  if (!config.verbose) {
    console.log(); // Newline after progress
  }

  results.duration = Date.now() - startTime;
  return results;
}

/**
 * List available scenarios
 */
export function listScenarios(): string[] {
  return scenarios.map(s => s.name);
}
