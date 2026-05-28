#!/usr/bin/env node
/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Virtual Idiot - Fuzz testing CLI for e3
 *
 * Usage:
 *   npm run fuzz                      # Run 100 iterations
 *   npm run fuzz -- -n 1000           # Run 1000 iterations
 *   npm run fuzz -- --scenario task-execution
 *   npm run fuzz -- --seed 12345      # Reproduce with specific seed
 *   npm run fuzz -- --stop-on-failure
 *   npm run fuzz -- -v                # Verbose output
 */

import { parseArgs } from 'node:util';
import { runFuzzTests, listScenarios } from './runner.js';
import { formatDuration } from './helpers.js';

async function main() {
  const { values } = parseArgs({
    options: {
      iterations: { type: 'string', short: 'n', default: '100' },
      scenario: { type: 'string', short: 's' },
      seed: { type: 'string' },
      'stop-on-failure': { type: 'boolean', default: false },
      verbose: { type: 'boolean', short: 'v', default: false },
      list: { type: 'boolean', short: 'l', default: false },
      help: { type: 'boolean', short: 'h', default: false },
    },
  });

  if (values.help) {
    console.log(`
Virtual Idiot - Fuzz testing for e3

Usage:
  npm run fuzz [options]

Options:
  -n, --iterations <n>   Number of iterations (default: 100)
  -s, --scenario <name>  Run specific scenario
  --seed <n>             Random seed for reproduction
  --stop-on-failure      Stop on first failure
  -v, --verbose          Verbose output
  -l, --list             List available scenarios
  -h, --help             Show this help

Examples:
  npm run fuzz                           # Run 100 iterations of all scenarios
  npm run fuzz -- -n 1000                # Run 1000 iterations
  npm run fuzz -- -s task-execution      # Run only task-execution scenarios
  npm run fuzz -- --seed 12345 -n 1      # Reproduce specific run
  npm run fuzz -- --stop-on-failure -v   # Stop on first failure, verbose
`);
    process.exit(0);
  }

  if (values.list) {
    console.log('Available scenarios:');
    for (const name of listScenarios()) {
      console.log(`  ${name}`);
    }
    process.exit(0);
  }

  const config = {
    iterations: parseInt(values.iterations!, 10),
    scenario: values.scenario,
    seed: values.seed ? parseInt(values.seed, 10) : undefined,
    stopOnFailure: values['stop-on-failure']!,
    verbose: values.verbose!,
  };

  console.log('🤖 Virtual Idiot starting...\n');

  const results = await runFuzzTests(config);

  console.log('\n📊 Results:');
  console.log(`   Passed: ${results.passed}`);
  console.log(`   Failed: ${results.failed}`);
  console.log(`   Duration: ${formatDuration(results.duration)}`);

  if (results.failures.length > 0) {
    console.log('\n❌ Failures:');
    for (const failure of results.failures) {
      console.log(`   - [${failure.iteration}] ${failure.scenario}`);
      console.log(`     ${failure.dir}`);
    }
    process.exit(1);
  } else {
    console.log('\n✅ All tests passed!');
  }
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
