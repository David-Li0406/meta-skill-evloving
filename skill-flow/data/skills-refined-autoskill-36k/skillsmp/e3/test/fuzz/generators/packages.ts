/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Random e3 package generation for fuzz testing.
 */

import type { EastType, ValueTypeOf } from '@elaraai/east';
import { East, IntegerType, StringType } from '@elaraai/east';
import { randomType as eastRandomType } from '@elaraai/east/internal';
import e3 from '@elaraai/e3';
import type { PackageDef, TaskDef, DatasetDef } from '@elaraai/e3';
import { random } from '../helpers.js';
import { randomValue } from './values.js';

export interface PackageConfig {
  /** Minimum number of inputs (default: 1) */
  minInputs?: number;
  /** Maximum number of inputs (default: 4) */
  maxInputs?: number;
  /** Minimum number of tasks (default: 1) */
  minTasks?: number;
  /** Maximum number of tasks (default: 5) */
  maxTasks?: number;
  /** DAG shape preference */
  dagShape?: 'linear' | 'diamond' | 'wide' | 'random';
}

export interface GeneratedPackage {
  /** The e3 package definition */
  package: PackageDef<any>;
  /** Input specifications for validation */
  inputs: Array<{
    name: string;
    type: EastType;
    defaultValue: unknown;
  }>;
  /** Task specifications for validation */
  tasks: Array<{
    name: string;
    inputRefs: string[];  // Names of inputs or task outputs this depends on
    outputType: EastType;
  }>;
}

/**
 * Generate a random e3 package with inputs and tasks.
 */
export function randomPackage(config: PackageConfig = {}): GeneratedPackage {
  const minInputs = config.minInputs ?? 1;
  const maxInputs = config.maxInputs ?? 4;
  const minTasks = config.minTasks ?? 1;
  const maxTasks = config.maxTasks ?? 5;

  const numInputs = random.int(minInputs, maxInputs);
  const numTasks = random.int(minTasks, maxTasks);

  // Generate inputs with random East types
  const inputs: Array<{ name: string; type: EastType; defaultValue: unknown; dataset: DatasetDef }> = [];
  for (let i = 0; i < numInputs; i++) {
    const name = `input_${i}`;
    // Use East's full random type generator - depth 2 to keep it manageable
    const type = eastRandomType(2, { includeRecursive: false, includeFunctions: false });
    const defaultValue = randomValue(type);
    const dataset = e3.input(name, type, defaultValue as ValueTypeOf<typeof type>);
    inputs.push({ name, type, defaultValue, dataset });
  }

  // Generate tasks in a DAG structure
  const tasks: Array<{
    name: string;
    inputRefs: string[];
    outputType: EastType;
    taskDef: TaskDef;
  }> = [];

  // Available outputs that can be used as inputs to subsequent tasks
  const availableOutputs: Array<{ name: string; dataset: DatasetDef; type: EastType }> = [
    ...inputs.map(i => ({ name: `inputs.${i.name}`, dataset: i.dataset, type: i.type }))
  ];

  for (let i = 0; i < numTasks; i++) {
    const taskName = `task_${i}`;

    // Pick 1-2 inputs from available outputs
    const numTaskInputs = random.int(1, Math.min(2, availableOutputs.length));
    const selectedInputs: typeof availableOutputs = [];
    const availableCopy = [...availableOutputs];

    for (let j = 0; j < numTaskInputs; j++) {
      const idx = random.int(0, availableCopy.length - 1);
      selectedInputs.push(availableCopy[idx]!);
      availableCopy.splice(idx, 1);
    }

    // Randomly choose task behavior:
    // - identity: return first input unchanged
    // - stringify: convert inputs to string (works with any type via East.str)
    const taskKind = random.pick(['identity', 'stringify', 'stringify']);

    let taskDef: TaskDef;
    let outputType: EastType;

    if (taskKind === 'stringify') {
      // Use East.str`${x}` to stringify any input - great for testing serialization
      taskDef = createStringifyTask(taskName, selectedInputs.map(s => s.dataset));
      outputType = StringType;
    } else {
      // Identity - return first input
      const firstInputType = selectedInputs[0]!.type;
      taskDef = createIdentityTask(taskName, selectedInputs.map(s => s.dataset), firstInputType);
      outputType = firstInputType;
    }

    tasks.push({
      name: taskName,
      inputRefs: selectedInputs.map(s => s.name),
      outputType,
      taskDef,
    });

    // Add this task's output to available outputs
    availableOutputs.push({
      name: `tasks.${taskName}.output`,
      dataset: taskDef.output,
      type: outputType,
    });
  }

  // Build the package including all tasks (not just the last one)
  // This ensures orphaned branches in the DAG are still included
  const pkgName = `fuzz_pkg_${random.string(6)}`;
  const pkg = e3.package(pkgName, '1.0.0', ...tasks.map(t => t.taskDef));

  return {
    package: pkg,
    inputs: inputs.map(i => ({ name: i.name, type: i.type, defaultValue: i.defaultValue })),
    tasks: tasks.map(t => ({ name: t.name, inputRefs: t.inputRefs, outputType: t.outputType })),
  };
}

/**
 * Create an identity-like task that returns its first input.
 * This preserves types through the pipeline while still being a valid task.
 */
function createIdentityTask(
  name: string,
  inputDatasets: DatasetDef[],
  outputType: EastType
): TaskDef {
  // Create a function that returns the first input (identity)
  if (inputDatasets.length === 1) {
    return e3.task(
      name,
      inputDatasets,
      East.function(
        [inputDatasets[0]!.type],
        outputType,
        (_$, x) => x
      )
    );
  } else {
    // Multiple inputs - still return the first one
    return e3.task(
      name,
      inputDatasets,
      East.function(
        inputDatasets.map(d => d.type),
        outputType,
        (_$, x, ..._rest) => x
      ) as any
    );
  }
}

/**
 * Create a task that stringifies its inputs using East.str.
 * This works with ANY East type and tests serialization thoroughly.
 */
function createStringifyTask(
  name: string,
  inputDatasets: DatasetDef[]
): TaskDef {
  if (inputDatasets.length === 1) {
    return e3.task(
      name,
      inputDatasets,
      East.function(
        [inputDatasets[0]!.type],
        StringType,
        (_$, x) => East.str`value: ${x}`
      )
    );
  } else if (inputDatasets.length === 2) {
    return e3.task(
      name,
      inputDatasets,
      East.function(
        inputDatasets.map(d => d.type),
        StringType,
        (_$, a, b) => East.str`a=${a}, b=${b}`
      ) as any
    );
  } else {
    // 3+ inputs - just stringify the first two
    return e3.task(
      name,
      inputDatasets,
      East.function(
        inputDatasets.map(d => d.type),
        StringType,
        (_$, a, b, ..._rest) => East.str`a=${a}, b=${b}`
      ) as any
    );
  }
}

/**
 * Generate a simple package with a single input and task for basic testing.
 */
export function simplePackage(): GeneratedPackage {
  const inputType = IntegerType;
  const inputValue = random.int(1, 100);
  const input = e3.input('x', inputType, BigInt(inputValue));

  const task = e3.task(
    'double',
    [input],
    East.function(
      [IntegerType],
      IntegerType,
      ($, x) => x.multiply(2n)
    )
  );

  const pkg = e3.package(`simple_${random.string(6)}`, '1.0.0', task);

  return {
    package: pkg,
    inputs: [{ name: 'x', type: inputType, defaultValue: BigInt(inputValue) }],
    tasks: [{ name: 'double', inputRefs: ['inputs.x'], outputType: IntegerType }],
  };
}

/**
 * Generate a diamond-shaped package for testing parallel execution.
 *
 *       input_a    input_b
 *          \        /
 *        task_left  task_right
 *              \    /
 *            task_merge
 */
export function diamondPackage(): GeneratedPackage {
  const input_a = e3.input('a', IntegerType, BigInt(random.int(1, 100)));
  const input_b = e3.input('b', IntegerType, BigInt(random.int(1, 100)));

  const task_left = e3.task(
    'left',
    [input_a, input_b],
    East.function(
      [IntegerType, IntegerType],
      IntegerType,
      ($, a, b) => a.add(b)
    )
  );

  const task_right = e3.task(
    'right',
    [input_a, input_b],
    East.function(
      [IntegerType, IntegerType],
      IntegerType,
      ($, a, b) => a.multiply(b)
    )
  );

  const task_merge = e3.task(
    'merge',
    [task_left.output, task_right.output],
    East.function(
      [IntegerType, IntegerType],
      IntegerType,
      ($, left, right) => left.add(right)
    )
  );

  const pkg = e3.package(`diamond_${random.string(6)}`, '1.0.0', task_merge);

  return {
    package: pkg,
    inputs: [
      { name: 'a', type: IntegerType, defaultValue: (input_a as any).default },
      { name: 'b', type: IntegerType, defaultValue: (input_b as any).default },
    ],
    tasks: [
      { name: 'left', inputRefs: ['inputs.a', 'inputs.b'], outputType: IntegerType },
      { name: 'right', inputRefs: ['inputs.a', 'inputs.b'], outputType: IntegerType },
      { name: 'merge', inputRefs: ['tasks.left.output', 'tasks.right.output'], outputType: IntegerType },
    ],
  };
}
