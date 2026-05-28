/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describe, it } from 'node:test';
import assert from 'node:assert';

import { East, StringType, IntegerType, FloatType, StructType, variant } from '@elaraai/east';
import { task } from './task.js';
import { input } from './input.js';

describe('task', () => {
  describe('type inference', () => {
    it('accepts single input dataset', () => {
      const name_input = input('name', StringType, 'World');

      const greet = task(
        'greet',
        [name_input],
        East.function(
          [StringType],
          StringType,
          ($, name) => $.return(East.str`Hello, ${name}!`)
        )
      );

      assert.strictEqual(greet.kind, 'task');
      assert.strictEqual(greet.name, 'greet');
      assert.strictEqual(greet.output.kind, 'dataset');
    });

    it('accepts multiple input datasets with different types', () => {
      const name_input = input('name', StringType, 'World');
      const count_input = input('count', IntegerType, 1n);

      const repeat_greet = task(
        'repeat_greet',
        [name_input, count_input],
        East.function(
          [StringType, IntegerType],
          StringType,
          ($, name, _count) => $.return(East.str`Hello, ${name}!`)
        )
      );

      assert.strictEqual(repeat_greet.kind, 'task');
      assert.strictEqual(repeat_greet.name, 'repeat_greet');
    });

    it('accepts three input datasets', () => {
      const a_input = input('a', StringType, 'a');
      const b_input = input('b', IntegerType, 1n);
      const c_input = input('c', FloatType, 1.0);

      const combine = task(
        'combine',
        [a_input, b_input, c_input],
        East.function(
          [StringType, IntegerType, FloatType],
          StringType,
          ($, a, _b, _c) => $.return(a)
        )
      );

      assert.strictEqual(combine.kind, 'task');
      assert.strictEqual(combine.inputs.length, 4); // 3 inputs + function_ir
    });

    it('accepts four input datasets (tuple type preservation)', () => {
      const a_input = input('a', StringType, 'a');
      const b_input = input('b', IntegerType, 1n);
      const c_input = input('c', FloatType, 1.0);
      const d_input = input('d', StringType, 'd');

      const combine_four = task(
        'combine_four',
        [a_input, b_input, c_input, d_input],
        East.function(
          [StringType, IntegerType, FloatType, StringType],
          StringType,
          ($, a, _b, _c, _d) => $.return(a)
        )
      );

      assert.strictEqual(combine_four.kind, 'task');
      assert.strictEqual(combine_four.inputs.length, 5); // 4 inputs + function_ir
    });

    it('accepts struct type inputs', () => {
      const PersonType = StructType({
        name: StringType,
        age: IntegerType,
      });

      const person_input = input('person', PersonType, { name: 'Alice', age: 30n });

      const describe_person = task(
        'describe_person',
        [person_input],
        East.function(
          [PersonType],
          StringType,
          ($, person) => $.return(East.str`${person.name} is ${person.age} years old`)
        )
      );

      assert.strictEqual(describe_person.kind, 'task');
    });
  });

  describe('task chaining', () => {
    it('allows using task output as input to another task', () => {
      const name_input = input('name', StringType, 'World');

      const greet = task(
        'greet',
        [name_input],
        East.function(
          [StringType],
          StringType,
          ($, name) => $.return(East.str`Hello, ${name}!`)
        )
      );

      const shout = task(
        'shout',
        [greet.output],
        East.function(
          [StringType],
          StringType,
          ($, greeting) => $.return(East.str`${greeting}!!!`)
        )
      );

      assert.strictEqual(shout.kind, 'task');
      assert.strictEqual(shout.name, 'shout');
      // shout depends on greet's output
      assert.ok(shout.deps.has(greet.output));
    });

    it('allows mixing inputs and task outputs', () => {
      const name_input = input('name', StringType, 'World');
      const suffix_input = input('suffix', StringType, '!');

      const greet = task(
        'greet',
        [name_input],
        East.function(
          [StringType],
          StringType,
          ($, name) => $.return(East.str`Hello, ${name}`)
        )
      );

      const add_suffix = task(
        'add_suffix',
        [greet.output, suffix_input],
        East.function(
          [StringType, StringType],
          StringType,
          ($, greeting, suffix) => $.return(East.str`${greeting}${suffix}`)
        )
      );

      assert.strictEqual(add_suffix.kind, 'task');
      assert.strictEqual(add_suffix.inputs.length, 3); // function_ir + 2 inputs
    });
  });

  describe('task structure', () => {
    it('creates correct output path', () => {
      const name_input = input('name', StringType, 'World');

      const greet = task(
        'my_task',
        [name_input],
        East.function(
          [StringType],
          StringType,
          ($, name) => $.return(name)
        )
      );

      assert.deepStrictEqual(greet.output.path, [
        variant('field', 'tasks'),
        variant('field', 'my_task'),
        variant('field', 'output'),
      ]);
    });

    it('includes function_ir as first input', () => {
      const name_input = input('name', StringType, 'World');

      const greet = task(
        'greet',
        [name_input],
        East.function(
          [StringType],
          StringType,
          ($, name) => $.return(name)
        )
      );

      // First input should be the function_ir dataset
      assert.strictEqual(greet.inputs[0].name, 'function_ir');
    });

    it('preserves custom runner config', () => {
      const name_input = input('name', StringType, 'World');

      const greet = task(
        'greet',
        [name_input],
        East.function(
          [StringType],
          StringType,
          ($, name) => $.return(name)
        ),
        {
          runner: ['uv', 'run', 'east-py', 'run', '-p', 'east-py-std']
        }
      );

      assert.strictEqual(greet.kind, 'task');
      // The runner is encoded in the command, we just verify the task was created
    });
  });
});
