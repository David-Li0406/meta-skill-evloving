# e3 Fuzz Testing: The Virtual Idiot

A comprehensive fuzz testing system for e3 that exercises the entire stack (East types, e3-core, e3-cli) to find edge cases and bugs before demos.

## Goals

1. **Find bugs before demos** - Automated stress testing catches issues human testers miss
2. **Exercise the full stack** - From East value generation through package creation, workspace execution, and result validation
3. **Reproducible failures** - When something breaks, log the exact state that caused it
4. **Long-running capability** - Run overnight or continuously to maximize coverage

## Architecture

```
test/
├── index.ts              # Main entry point and CLI
├── helpers.ts            # Test utilities
├── reporter.ts           # Logs failures with full state
├── runner.ts             # Orchestrates fuzz test runs
├── generators/
│   ├── index.ts          # Re-exports all generators
│   ├── types.ts          # Random East type generation (uses east/internal.js)
│   ├── values.ts         # Random value generation (uses east/internal.js)
│   └── packages.ts       # Random e3 package generation
└── scenarios/
    ├── package-lifecycle.ts    # Create, export, import, deploy
    ├── task-execution.ts       # Execute tasks, validate outputs
    └── input-mutation.ts       # Set values, re-execute, check cache

/tmp/e3-fuzz-failures/    # Persisted failure states (in /tmp)
└── YYYY-MM-DD-HHMMSS-<hash>/
    ├── state.json        # Full state that caused failure
    ├── error.txt         # Error message and stack trace
    └── repo/             # Repository snapshot (if applicable)
```

## Components

### 1. Type and Value Generators

Extend East's `randomType()` and `randomValueFor()` to cover e3-specific needs:

```typescript
// generators/types.ts
import { randomType, randomValueFor } from '@elaraai/east/internal.js';

// Prefer types commonly used in real packages
export function randomE3Type(depth = 0): EastType {
  const weights = {
    primitive: 0.4,      // Integer, Float, String, Boolean
    collection: 0.3,     // Array, Dict, Set
    struct: 0.2,         // Struct (common in e3 packages)
    variant: 0.1,        // Variant, Option
  };
  // ... weighted selection
}

// Generate values that stress-test serialization
export function randomStressValue<T extends EastType>(type: T): ValueTypeOf<T> {
  // Include edge cases:
  // - Empty strings, very long strings
  // - Integer boundaries (MAX_SAFE_INTEGER, etc.)
  // - Float special values (NaN, Infinity, -0.0)
  // - Empty collections, deeply nested structures
  // - Unicode edge cases, null bytes in strings
}
```

### 2. Package Generators

Generate random but valid e3 packages:

```typescript
// generators/packages.ts
export interface PackageSpec {
  name: string;
  version: string;
  inputs: Array<{ name: string; type: EastType; defaultValue: any }>;
  tasks: Array<TaskSpec>;
}

export interface TaskSpec {
  name: string;
  inputs: string[];           // References to input names or task.output names
  outputType: EastType;
  kind: 'east' | 'custom';    // East function or custom bash command
  behavior: TaskBehavior;     // What the task does
}

type TaskBehavior =
  | { type: 'identity' }                    // Returns first input unchanged
  | { type: 'transform'; fn: string }       // Simple transform (add, multiply, etc.)
  | { type: 'aggregate'; fn: string }       // Combine multiple inputs
  | { type: 'fail'; probability: number }   // Randomly fail
  | { type: 'slow'; delayMs: number };      // Simulate slow execution

export function randomPackage(config: PackageConfig = {}): PackageSpec {
  const numInputs = config.minInputs ?? 1 + Math.floor(Math.random() * 4);
  const numTasks = config.minTasks ?? 1 + Math.floor(Math.random() * 5);

  // Generate random DAG of tasks
  // Ensure no cycles, valid input references
  // Mix of East tasks and custom tasks
}
```

### 3. Task DAG Generator

Generate valid task dependency graphs:

```typescript
// generators/tasks.ts
export type DAGShape =
  | 'linear'     // A → B → C → D
  | 'diamond'    // A → B, A → C, B → D, C → D
  | 'wide'       // A → B, A → C, A → D (parallel)
  | 'deep'       // Long chain
  | 'random';    // Random valid DAG

export function randomTaskDAG(
  inputs: string[],
  shape: DAGShape = 'random',
  config: DAGConfig = {}
): TaskSpec[] {
  // Generate tasks with valid dependency ordering
  // Ensure all inputs are connected
  // Randomly include failing tasks (with low probability)
}
```

### 4. Operation Sequence Generator

Generate sequences of e3 operations:

```typescript
// generators/operations.ts
export type E3Operation =
  | { type: 'init'; path: string }
  | { type: 'package-import'; zipPath: string }
  | { type: 'workspace-create'; name: string }
  | { type: 'workspace-deploy'; workspace: string; package: string }
  | { type: 'set'; path: string; value: any }
  | { type: 'get'; path: string }
  | { type: 'start'; workspace: string }
  | { type: 'list'; workspace?: string }
  | { type: 'status' }
  | { type: 'gc' };

export function randomOperationSequence(
  state: RepositoryState,
  length: number = 10
): E3Operation[] {
  // Generate valid operation sequences based on current state
  // E.g., can't deploy without importing, can't start without deploying
}
```

### 5. Test Scenarios

#### Package Lifecycle

```typescript
// scenarios/package-lifecycle.ts
export async function testPackageLifecycle(config: ScenarioConfig): Promise<TestResult> {
  const pkg = randomPackage();
  const testDir = createTestDir();

  try {
    // 1. Create package using SDK
    const sdkPackage = buildPackageFromSpec(pkg);

    // 2. Export to zip
    const zipPath = join(testDir, 'package.zip');
    await e3.export(sdkPackage, zipPath);

    // 3. Init repository
    const repoDir = join(testDir, 'repo');
    await runE3Command(['init', repoDir]);

    // 4. Import package
    await runE3Command(['package', 'import', repoDir, zipPath]);

    // 5. Verify package list
    const listResult = await runE3Command(['package', 'list', repoDir]);
    assert(listResult.stdout.includes(pkg.name));

    // 6. Create and deploy workspace
    await runE3Command(['workspace', 'create', repoDir, 'test-ws']);
    await runE3Command(['workspace', 'deploy', repoDir, 'test-ws', `${pkg.name}@${pkg.version}`]);

    return { success: true };
  } catch (error) {
    return { success: false, error, state: { pkg, testDir } };
  }
}
```

#### Task Execution

```typescript
// scenarios/task-execution.ts
export async function testTaskExecution(config: ScenarioConfig): Promise<TestResult> {
  const pkg = randomPackage({
    taskBehaviors: ['identity', 'transform', 'aggregate']  // No failing tasks
  });

  // Setup repository and workspace...

  // Execute and validate
  const startResult = await runE3Command(['start', repoDir, 'test-ws']);

  // For deterministic tasks, validate outputs match expected
  for (const task of pkg.tasks) {
    if (isDeterministic(task)) {
      const expected = computeExpectedOutput(task, pkg.inputs);
      const actual = await runE3Command(['get', repoDir, `test-ws.tasks.${task.name}.output`]);
      assertEqual(expected, parseOutput(actual.stdout));
    }
  }

  return { success: true };
}
```

#### Input Mutation

```typescript
// scenarios/input-mutation.ts
export async function testInputMutation(config: ScenarioConfig): Promise<TestResult> {
  // Setup with deterministic package...

  // Execute once
  await runE3Command(['start', repoDir, 'test-ws']);
  const output1 = await getOutput('test-ws.tasks.main.output');

  // Change input
  const newValue = randomValueFor(inputType)();
  await setInput('test-ws.inputs.x', newValue);

  // Re-execute
  await runE3Command(['start', repoDir, 'test-ws']);
  const output2 = await getOutput('test-ws.tasks.main.output');

  // Validate output changed appropriately
  const expected = computeExpectedOutput(newValue);
  assertEqual(expected, output2);

  // Verify cache behavior: same input again should be cached
  await runE3Command(['start', repoDir, 'test-ws']);  // Should be fast
}
```

#### Concurrent Operations (Future)

```typescript
// scenarios/concurrent-ops.ts
export async function testConcurrentOperations(config: ScenarioConfig): Promise<TestResult> {
  // Test race conditions:
  // - Multiple `e3 set` commands simultaneously
  // - `e3 start` while another is running
  // - `e3 gc` during execution
}
```

#### Edge Cases

```typescript
// scenarios/edge-cases.ts
export const edgeCaseTests = [
  // Empty/minimal packages
  { name: 'empty-package', fn: () => randomPackage({ numInputs: 0, numTasks: 0 }) },
  { name: 'single-task', fn: () => randomPackage({ numInputs: 1, numTasks: 1 }) },

  // Deep nesting
  { name: 'deeply-nested-type', fn: () => randomPackage({ typeDepth: 10 }) },
  { name: 'long-task-chain', fn: () => randomPackage({ dagShape: 'deep', chainLength: 20 }) },

  // Large data
  { name: 'large-array', fn: () => randomPackage({ arraySize: 10000 }) },
  { name: 'many-inputs', fn: () => randomPackage({ numInputs: 50 }) },
  { name: 'many-tasks', fn: () => randomPackage({ numTasks: 50 }) },

  // Special values
  { name: 'unicode-names', fn: () => randomPackage({ useUnicodeNames: true }) },
  { name: 'special-floats', fn: () => randomPackage({ includeNaN: true, includeInfinity: true }) },

  // Workspace operations
  { name: 'redeploy', fn: testRedeployPackage },
  { name: 'multiple-workspaces', fn: testMultipleWorkspaces },
];
```

### 6. Failure Reporter

```typescript
// reporter.ts
export interface FailureReport {
  timestamp: Date;
  scenario: string;
  seed: number;           // Random seed for reproduction
  state: any;             // Full state that caused failure
  error: Error;
  stackTrace: string;
}

export async function reportFailure(report: FailureReport): Promise<string> {
  const hash = sha256(JSON.stringify(report.state)).slice(0, 8);
  const dirName = `${formatDate(report.timestamp)}-${hash}`;
  const failureDir = join('fuzz-failures', dirName);

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
Timestamp: ${report.timestamp.toISOString()}

Error: ${report.error.message}

Stack Trace:
${report.stackTrace}
`
  );

  // Optionally copy repository snapshot
  if (report.state.repoDir && existsSync(report.state.repoDir)) {
    await copyDir(report.state.repoDir, join(failureDir, 'repo'));
  }

  console.error(`\n❌ Failure logged to: ${failureDir}`);
  return failureDir;
}
```

### 7. CLI Runner

```typescript
// index.ts (CLI entry point)
import { parseArgs } from 'node:util';

const args = parseArgs({
  options: {
    iterations: { type: 'string', short: 'n', default: '100' },
    scenario: { type: 'string', short: 's' },           // Run specific scenario
    seed: { type: 'string' },                            // For reproduction
    timeout: { type: 'string', default: '60000' },       // Per-test timeout
    'stop-on-failure': { type: 'boolean', default: false },
    verbose: { type: 'boolean', short: 'v', default: false },
  },
});

async function main() {
  const config: RunnerConfig = {
    iterations: parseInt(args.values.iterations!),
    scenario: args.values.scenario,
    seed: args.values.seed ? parseInt(args.values.seed) : undefined,
    timeout: parseInt(args.values.timeout!),
    stopOnFailure: args.values['stop-on-failure'],
    verbose: args.values.verbose,
  };

  console.log('🤖 Virtual Idiot starting...');
  console.log(`   Iterations: ${config.iterations}`);
  console.log(`   Scenario: ${config.scenario ?? 'all'}`);
  if (config.seed) console.log(`   Seed: ${config.seed}`);

  const results = await runFuzzTests(config);

  console.log('\n📊 Results:');
  console.log(`   Passed: ${results.passed}`);
  console.log(`   Failed: ${results.failed}`);
  console.log(`   Duration: ${results.duration}ms`);

  if (results.failures.length > 0) {
    console.log('\n❌ Failures:');
    for (const failure of results.failures) {
      console.log(`   - ${failure.scenario}: ${failure.dir}`);
    }
    process.exit(1);
  }
}
```

## Usage

```bash
# Run 100 iterations of all scenarios
npm run fuzz

# Run specific scenario
npm run fuzz -- --scenario task-execution

# Run with specific seed (for reproduction)
npm run fuzz -- --seed 12345

# Run until first failure
npm run fuzz -- --stop-on-failure -n 1000

# Long-running stress test
npm run fuzz -- -n 10000 --timeout 120000

# Verbose output
npm run fuzz -- -v
```

Add to `package.json`:

```json
{
  "scripts": {
    "fuzz": "tsx src/fuzz/index.ts",
    "fuzz:quick": "npm run fuzz -- -n 10",
    "fuzz:stress": "npm run fuzz -- -n 1000 --stop-on-failure"
  }
}
```

## Reproduction

When a failure occurs:

```bash
# Check failure log
cat fuzz-failures/2025-01-15-143022-a3f8b2c1/error.txt

# Reproduce with same seed
npm run fuzz -- --seed 12345 --scenario task-execution -n 1

# Inspect saved repository state
ls fuzz-failures/2025-01-15-143022-a3f8b2c1/repo/
```

## Integration with CI

Add to `.github/workflows/test.yml`:

```yaml
- name: Run fuzz tests (quick)
  working-directory: e3
  run: npm run fuzz:quick

# Optional: nightly stress test
- name: Run fuzz tests (stress)
  if: github.event_name == 'schedule'
  working-directory: e3
  run: npm run fuzz -- -n 1000 --timeout 300000
```

## Future Enhancements

1. **Shrinking** - Automatically minimize failing cases to smallest reproduction
2. **Coverage tracking** - Track which code paths are exercised
3. **Property-based testing** - Define invariants that must always hold
4. **Distributed fuzzing** - Run across multiple machines
5. **Mutation testing** - Inject bugs to verify tests catch them
6. **East-py integration** - Fuzz test the Python runtime alongside e3

## Summary

The Virtual Idiot provides:

- **Generators** for random types, values, packages, and operation sequences
- **Scenarios** covering package lifecycle, task execution, input mutation, and edge cases
- **Persistent failure logging** with full state for reproduction
- **CLI** for running stress tests with configurable iterations and seeds
- **CI integration** for automated regression testing
