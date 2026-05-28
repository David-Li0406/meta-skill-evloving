/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Helpers for creating East IR in integration tests
 */

import { East, IntegerType, ArrayType, printFor, IRType, encodeBeast2For } from '@elaraai/east';
import { writeFileSync } from 'fs';

/**
 * Create a simple function IR: () => 42
 * Returns the file path
 */
export function createSimpleFunctionIR(dir: string, filename: string = 'simple.beast2'): string {
  const fn = East.function([], IntegerType, (_$) => 42n);
  const ir = fn.toIR().ir;

  const encoder = encodeBeast2For(IRType);
  const path = `${dir}/${filename}`;
  writeFileSync(path, encoder(ir));

  return path;
}

/**
 * Create identity function IR: (x: Integer) => x
 * Returns the file path
 */
export function createIdentityFunctionIR(dir: string, filename: string = 'identity.beast2'): string {
  const fn = East.function([IntegerType], IntegerType, ($, x) => x);
  const ir = fn.toIR().ir;

  const encoder = encodeBeast2For(IRType);
  const path = `${dir}/${filename}`;
  writeFileSync(path, encoder(ir));

  return path;
}

/**
 * Create add function IR: (a: Integer, b: Integer) => a + b
 * Returns the file path
 */
export function createAddFunctionIR(dir: string, filename: string = 'add.beast2'): string {
  const fn = East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.add(b));
  const ir = fn.toIR().ir;

  const encoder = encodeBeast2For(IRType);
  const path = `${dir}/${filename}`;
  writeFileSync(path, encoder(ir));

  return path;
}

/**
 * Create an integer value file
 */
export function createIntegerValue(dir: string, value: bigint | number, filename: string = 'value.east'): string {
  const printer = printFor(IntegerType);
  const path = `${dir}/${filename}`;
  writeFileSync(path, printer(BigInt(value)));

  return path;
}

/**
 * Create an array of integers value file
 */
export function createIntegerArrayValue(dir: string, values: (bigint | number)[], filename: string = 'array.east'): string {
  const printer = printFor(ArrayType(IntegerType));
  const path = `${dir}/${filename}`;
  writeFileSync(path, printer(values.map(v => BigInt(v))));

  return path;
}
