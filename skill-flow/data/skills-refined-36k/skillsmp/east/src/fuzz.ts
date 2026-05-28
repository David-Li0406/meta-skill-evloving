/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 *
 * @remarks
 */

import {
  type EastType,
  type ValueTypeOf,
  NullType,
  BooleanType,
  IntegerType,
  FloatType,
  StringType,
  DateTimeType,
  BlobType,
  ArrayType,
  SetType,
  DictType,
  StructType,
  VariantType,
  OptionType,
  RecursiveType,
  FunctionType,
  RefType,
} from "./types.js";
import { isVariant, variant } from "./containers/variant.js";
import { printType } from "./types.js";
import { printFor } from "./serialization/east.js";
import { toEastTypeValue, type EastTypeValue } from "./type_of_type.js";
import { ref } from "./containers/ref.js";

/**
 * Generates a random primitive East type.
 */
function randomPrimitiveType(): EastType {
  const r = Math.random() * 7;
  if (r < 1) return NullType;
  if (r < 2) return BooleanType;
  if (r < 3) return IntegerType;
  if (r < 4) return FloatType;
  if (r < 5) return StringType;
  if (r < 6) return DateTimeType;
  return BlobType;
}

/**
 * Generates a random East type for fuzz testing.
 *
 * @param depth - Current nesting depth (used internally to limit recursion)
 * @param options - Configuration options
 * @returns A randomly generated {@link EastType}
 *
 * @remarks
 * Types are kept reasonably simple to avoid generating huge nested structures:
 * - Maximum nesting depth of 3 levels
 * - Higher chance of primitives at deeper levels
 * - Sets and Dicts use {@link StringType} keys (immutability constraint)
 * - Structs have 0-4 random fields
 * - Variants have 1-3 random cases, with 30% chance of {@link OptionType}
 * - Recursive types include linked lists, trees, and option-wrapped patterns
 * - Function types have 0-3 arguments with random input/output types
 */
export function randomType(
  depth: number = 0,
  options: { includeRecursive?: boolean; includeFunctions?: boolean } = {}
): EastType {
  const { includeRecursive = true, includeFunctions = true } = options;

  // Limit nesting to avoid stack overflow and keep tests fast
  const maxDepth = 3;

  // Higher chance of primitives at deeper levels
  const primitiveWeight = depth >= maxDepth ? 0.9 : 0.5;

  if (Math.random() < primitiveWeight) {
    return randomPrimitiveType();
  }

  // Complex type - weights adjusted based on options
  let totalWeight = 5; // Array, Set, Dict, Struct, Variant
  if (includeRecursive && depth === 0) totalWeight += 1; // Recursive only at top level
  if (includeFunctions) totalWeight += 1;

  const r = Math.random() * totalWeight;

  if (r < 1) {
    // Array
    return ArrayType(randomType(depth + 1, { includeRecursive: false, includeFunctions: false }));
  } else if (r < 2) {
    // Set (keys must be immutable)
    return SetType(StringType);
  } else if (r < 3) {
    // Dict (keys must be immutable)
    return DictType(StringType, randomType(depth + 1, { includeRecursive: false, includeFunctions: false }));
  } else if (r < 4) {
    // Struct with 0-4 fields
    const fieldCount = Math.floor(Math.random() * 5);
    const fields: Record<string, EastType> = {};
    for (let i = 0; i < fieldCount; i++) {
      fields[`field${i}`] = randomType(depth + 1, { includeRecursive: false, includeFunctions: false });
    }
    return StructType(fields);
  } else if (r < 5) {
    // Variant
    if (Math.random() < 0.3) {
      // Option type (common variant pattern)
      return OptionType(randomType(depth + 1, { includeRecursive: false, includeFunctions: false }));
    } else {
      // Custom variant with 1-3 cases
      const caseCount = 1 + Math.floor(Math.random() * 3);
      const cases: Record<string, EastType> = {};
      for (let i = 0; i < caseCount; i++) {
        cases[`case${i}`] = randomType(depth + 1, { includeRecursive: false, includeFunctions: false });
      }
      return VariantType(cases);
    }
  } else if (r < 6 && includeRecursive && depth === 0) {
    // Recursive type - only at top level to avoid nested recursion complexity
    return randomRecursiveType();
  } else {
    // Function type
    return randomFunctionType();
  }
}

/**
 * Generates a random recursive type pattern.
 *
 * @returns A randomly generated {@link RecursiveType}
 *
 * @remarks
 * Generates common recursive patterns:
 * - Linked list: `rec t. <nil: Null, cons: (head: T, tail: t)>`
 * - Tree: `rec t. (value: T, children: Array<t>)`
 * - Option chain: `rec t. (value: T, next: Option<t>)`
 * - Binary tree: `rec t. <leaf: T, node: (left: t, right: t)>`
 * - Nested variant: `rec t. <a: T, b: (inner: t)>`
 */
export function randomRecursiveType(): EastType {
  const innerType = randomPrimitiveType();
  const pattern = Math.floor(Math.random() * 5);

  switch (pattern) {
    case 0:
      // Linked list: rec t. <nil: Null, cons: (head: T, tail: t)>
      return RecursiveType((self) =>
        VariantType({
          nil: NullType,
          cons: StructType({ head: innerType, tail: self }),
        })
      );

    case 1:
      // Tree with children array: rec t. (value: T, children: Array<t>)
      return RecursiveType((self) =>
        StructType({
          value: innerType,
          children: ArrayType(self),
        })
      );

    case 2:
      // Option chain: rec t. (value: T, next: Option<t>)
      return RecursiveType((self) =>
        StructType({
          value: innerType,
          next: OptionType(self),
        })
      );

    case 3:
      // Binary tree: rec t. <leaf: T, node: (left: t, right: t)>
      return RecursiveType((self) =>
        VariantType({
          leaf: innerType,
          node: StructType({ left: self, right: self }),
        })
      );

    case 4:
    default:
      // Nested variant with ref: rec t. <done: T, more: Ref<t>>
      return RecursiveType((self) =>
        VariantType({
          done: innerType,
          more: RefType(self),
        })
      );
  }
}

/**
 * Generates a random function type.
 *
 * @returns A randomly generated {@link FunctionType}
 *
 * @remarks
 * Functions have 0-3 arguments with random primitive or simple types.
 * Output types are also kept simple to avoid excessive nesting.
 */
export function randomFunctionType(): EastType {
  const argCount = Math.floor(Math.random() * 4);
  const args: EastType[] = [];

  for (let i = 0; i < argCount; i++) {
    // Use simple types for arguments to keep things manageable
    const argType = Math.random() < 0.7
      ? randomPrimitiveType()
      : ArrayType(randomPrimitiveType());
    args.push(argType);
  }

  // Output type - also keep simple
  const outputType = Math.random() < 0.7
    ? randomPrimitiveType()
    : StructType({
        result: randomPrimitiveType(),
        status: BooleanType,
      });

  return FunctionType(args, outputType);
}

/**
 * Check if a type contains any `.Recursive n` back-references.
 * A type without recursive refs is "terminal" - it won't cause infinite recursion.
 * @internal
 */
function containsRecursive(type: EastTypeValue): boolean {
  switch (type.type) {
    case "Recursive":
      return true;
    case "Ref":
    case "Array":
      return containsRecursive(type.value);
    case "Set":
      return containsRecursive(type.value);
    case "Dict":
      return containsRecursive(type.value.key) || containsRecursive(type.value.value);
    case "Struct":
      return type.value.some(f => containsRecursive(f.type));
    case "Variant":
      return type.value.some(c => containsRecursive(c.type));
    default:
      // Primitives, functions don't contain recursive refs
      return false;
  }
}

/**
 * Context for generating values of recursive types.
 * Uses explicit depth passing (not shared mutable state) for correct recursion tracking.
 * @internal
 */
interface RecursiveValueContext {
  /** Stack of value generators for recursive back-references. Each takes depth and returns a value. */
  generators: Array<(depth: number) => any>;
  /** Maximum recursion depth before forcing termination */
  maxDepth: number;
}

/**
 * Internal helper that generates random values with explicit depth passing.
 * Returns a function that takes depth and produces a value.
 *
 * This design passes depth explicitly through all generators, avoiding the bug
 * where shared mutable depth state was incorrectly restored after generating
 * sibling fields in structs.
 * @internal
 */
function buildValueGenerator(
  type: EastTypeValue,
  ctx: RecursiveValueContext
): (depth: number) => any {
  if (type.type === "Never") {
    throw new Error("Cannot generate values for Never type");
  } else if (type.type === "Null") {
    return () => null;
  } else if (type.type === "Boolean") {
    return () => Math.random() < 0.5;
  } else if (type.type === "Integer") {
    return () => BigInt(Math.floor(Math.random() * 200) - 100);
  } else if (type.type === "Float") {
    return () => {
      const r = Math.random();
      if (r < 0.05) return NaN;
      if (r < 0.10) return Infinity;
      if (r < 0.15) return -Infinity;
      if (r < 0.20) return 0.0;
      if (r < 0.25) return -0.0;
      return Math.random() * 200 - 100;
    };
  } else if (type.type === "String") {
    return () => {
      const length = Math.floor(Math.random() * 20);
      if (length === 0) return "";
      return Math.random().toString(36).substring(2, 2 + length);
    };
  } else if (type.type === "DateTime") {
    return () => {
      const year2025 = new Date("2025-01-01T00:00:00.000Z").valueOf();
      const oneYear = 1000 * 60 * 60 * 24 * 365;
      return new Date(year2025 + Math.floor(Math.random() * oneYear));
    };
  } else if (type.type === "Blob") {
    return () => {
      const length = Math.floor(Math.random() * 100);
      const arr = new Uint8Array(length);
      for (let i = 0; i < length; i++) {
        arr[i] = Math.floor(Math.random() * 256);
      }
      return arr;
    };
  } else if (type.type === "Ref") {
    // Create function shell, push, recurse, pop - like apply.ts pattern
    let valueGen: (depth: number) => any;
    const ret = (depth: number) => ref(valueGen(depth));
    ctx.generators.push(ret);
    valueGen = buildValueGenerator(type.value, ctx);
    ctx.generators.pop();
    return ret;
  } else if (type.type === "Array") {
    let itemGen: (depth: number) => any;
    const ret = (depth: number) => {
      const maxLen = depth >= ctx.maxDepth ? 0 : Math.max(1, 5 - depth);
      const length = Math.floor(Math.random() * (maxLen + 1));
      return Array.from({ length }, () => itemGen(depth));
    };
    ctx.generators.push(ret);
    itemGen = buildValueGenerator(type.value, ctx);
    ctx.generators.pop();
    return ret;
  } else if (type.type === "Set") {
    let itemGen: (depth: number) => any;
    const ret = (depth: number) => {
      const maxLen = depth >= ctx.maxDepth ? 0 : 5;
      const length = Math.floor(Math.random() * (maxLen + 1));
      const set = new Set();
      for (let i = 0; i < length; i++) {
        set.add(itemGen(depth));
      }
      return set;
    };
    ctx.generators.push(ret);
    itemGen = buildValueGenerator(type.value, ctx);
    ctx.generators.pop();
    return ret;
  } else if (type.type === "Dict") {
    let keyGen: (depth: number) => any;
    let valueGen: (depth: number) => any;
    const ret = (depth: number) => {
      const maxLen = depth >= ctx.maxDepth ? 0 : 5;
      const length = Math.floor(Math.random() * (maxLen + 1));
      const dict = new Map();
      for (let i = 0; i < length; i++) {
        dict.set(keyGen(depth), valueGen(depth));
      }
      return dict;
    };
    ctx.generators.push(ret);
    keyGen = buildValueGenerator(type.value.key, ctx);
    valueGen = buildValueGenerator(type.value.value, ctx);
    ctx.generators.pop();
    return ret;
  } else if (type.type === "Struct") {
    let fieldGens: Array<{ name: string; gen: (depth: number) => any }>;
    const ret = (depth: number) => {
      const obj: Record<string, any> = {};
      for (const { name, gen } of fieldGens) {
        obj[name] = gen(depth);
      }
      return obj;
    };
    ctx.generators.push(ret);
    fieldGens = type.value.map(({ name, type: fieldType }) => ({
      name,
      gen: buildValueGenerator(fieldType, ctx),
    }));
    ctx.generators.pop();
    return ret;
  } else if (type.type === "Variant") {
    let caseInfos: Array<{ name: string; gen: (depth: number) => any; isTerminal: boolean }>;
    const ret = (depth: number) => {
      const terminalCases = caseInfos.filter((c) => c.isTerminal);
      const nonTerminalCases = caseInfos.filter((c) => !c.isTerminal);

      let chosen: (typeof caseInfos)[number];
      if (depth >= ctx.maxDepth && terminalCases.length > 0) {
        chosen = terminalCases[Math.floor(Math.random() * terminalCases.length)]!;
      } else if (terminalCases.length > 0 && nonTerminalCases.length > 0) {
        const terminalProb = Math.min(0.3 + depth * 0.2, 0.9);
        if (Math.random() < terminalProb) {
          chosen = terminalCases[Math.floor(Math.random() * terminalCases.length)]!;
        } else {
          chosen = nonTerminalCases[Math.floor(Math.random() * nonTerminalCases.length)]!;
        }
      } else {
        chosen = caseInfos[Math.floor(Math.random() * caseInfos.length)]!;
      }

      return variant(chosen.name, chosen.gen(depth));
    };
    ctx.generators.push(ret);
    caseInfos = type.value.map(({ name, type: caseType }) => ({
      name,
      gen: buildValueGenerator(caseType, ctx),
      isTerminal: !containsRecursive(caseType),
    }));
    ctx.generators.pop();
    return ret;
  } else if (type.type === "Recursive") {
    // Look up the generator from the context stack using de Bruijn index
    // IMPORTANT: Capture the generator reference at BUILD time, not runtime,
    // because the stack will be popped after building completes.
    const backRefIndex = Number(type.value);
    const index = ctx.generators.length - backRefIndex;
    if (index < 0 || index >= ctx.generators.length) {
      throw new Error(`Invalid recursive back-reference: ${backRefIndex}, stack size: ${ctx.generators.length}`);
    }
    const generator = ctx.generators[index];
    if (!generator) {
      throw new Error(`Recursive generator not found at index ${index}`);
    }
    // Return a generator that calls the captured recursive generator with depth+1
    return (depth: number) => generator(depth + 1);
  } else if (type.type === "Function") {
    let outputGen: (depth: number) => any;
    const ret = (depth: number) => {
      return (..._args: any[]) => outputGen(depth);
    };
    ctx.generators.push(ret);
    outputGen = buildValueGenerator(type.value.output, ctx);
    ctx.generators.pop();
    return ret;
  } else if (type.type === "AsyncFunction") {
    let outputGen: (depth: number) => any;
    const ret = (depth: number) => {
      return (..._args: any[]) => Promise.resolve(outputGen(depth));
    };
    ctx.generators.push(ret);
    outputGen = buildValueGenerator(type.value.output, ctx);
    ctx.generators.pop();
    return ret;
  } else {
    throw new Error(`Unhandled type: ${printType(type)}`);
  }
}

/**
 * Internal helper to handle RecursiveType before conversion.
 * Sets up the context stack and builds the value generator.
 *
 * The key insight: we create the generator function first, register it in the
 * context stack, then build the inner generator. This allows the inner generator
 * to find the outer generator via de Bruijn index lookup when it hits a
 * `.Recursive n` back-reference.
 * @internal
 */
function randomValueForRecursive(
  innerNode: EastType,
  ctx: RecursiveValueContext
): () => any {
  // The inner generator - will be set after building
  let innerGen: ((depth: number) => any) | null = null;

  // Create the self-referential generator
  // This will be called when we hit a .Recursive n back-reference
  const selfGenerator = (depth: number): any => {
    if (!innerGen) {
      throw new Error("Internal error: recursive generator not initialized");
    }

    // Hard limit to prevent stack overflow
    if (depth > ctx.maxDepth + 5) {
      throw new Error("Fuzz value generation exceeded max recursion depth");
    }

    return innerGen(depth);
  };

  // Push BEFORE building the inner generator so .Recursive can find it
  ctx.generators.push(selfGenerator);

  // Convert inner node to EastTypeValue with recursive context
  // Pass empty stack - the type structure will build up the stack naturally
  // as it recurses. When self-references (RecursiveType pointing back) are hit,
  // they'll find the struct in the stack and return .Recursive indices.
  const innerTypeValue = toEastTypeValue(innerNode, [], true);

  // Build the inner generator
  innerGen = buildValueGenerator(innerTypeValue, ctx);

  // Pop after building (generator is now self-contained via closure)
  ctx.generators.pop();

  // Return a function that starts generation at depth 0
  return () => selfGenerator(0);
}

/**
 * Creates a function that generates random values of a given type.
 *
 * @typeParam T - The {@link EastType} to generate values for
 * @param type - The type to generate values for
 * @returns A function that returns a new random value each time it's called
 * @throws When the type is {@link NeverType} or {@link FunctionType}
 *
 * @remarks
 * Generates diverse test values for each type:
 * - Floats include special values (NaN, ±Infinity, ±0.0)
 * - Integers range from -100 to 100 (as bigint)
 * - Strings use random alphanumeric sequences (0-20 chars)
 * - DateTimes are within one year of 2025-01-01
 * - Collections have 0-4 elements (kept small for performance)
 * - Variants randomly select one of their cases
 * - Recursive types generate finite values with depth limiting
 */
export function randomValueFor(type: EastTypeValue): () => any;
export function randomValueFor<T extends EastType>(type: T): () => ValueTypeOf<T>;
export function randomValueFor(type: EastTypeValue | EastType): () => any {
  const ctx: RecursiveValueContext = {
    generators: [],
    maxDepth: 5, // Limit recursion depth to avoid huge values
  };

  // Check if this is an EastType (not yet converted)
  if (!isVariant(type)) {
    // Handle RecursiveType specially before conversion
    if (type.type === "Recursive") {
      return randomValueForRecursive(type.node, ctx);
    }
    // Convert other EastTypes to EastTypeValue
    const typeValue = toEastTypeValue(type);
    const gen = buildValueGenerator(typeValue, ctx);
    return () => gen(0);
  }

  const gen = buildValueGenerator(type, ctx);
  return () => gen(0);
}

/**
 * Runs a fuzz test over a generic function parameterized by a type.
 *
 * @param fn - Factory function that takes a type and returns a test function for values of that type
 * @param n_types - Number of random types to test
 * @param n_samples - Number of random values to test per type
 * @returns `true` if all tests passed, `false` if any failed
 *
 * @remarks
 * For each randomly generated type:
 * 1. Creates a test function using the provided factory
 * 2. Generates random values of that type
 * 3. Runs the test function on each value
 * 4. Reports any failures to stderr with type, value, and error details
 *
 * Attempts to generate unique types (up to 100 attempts per type) to maximize
 * test coverage. Prints summary statistics showing success/failure counts.
 *
 * @example
 * ```ts
 * import { printFor, parseFor } from "./serialization/east.js";
 *
 * // Test that serialization and parsing work
 * await fuzzerTest(
 *   (type) => async (value) => {
 *     const parse = parseFor(type);
 *     const result = parse(serialized);
 *     if (!result.success) {
 *       throw new Error(`Parse failed: ${result.error}`);
 *     }
 *   },
 *   100,  // test 100 random types
 *   10    // with 10 random values each
 * );
 * ```
 */
export async function fuzzerTest(
  fn: (type: EastType) => (value: any) => Promise<void>,
  n_types: number = 100,
  n_samples: number = 10,
  options: { includeRecursive?: boolean; includeFunctions?: boolean } = {}
): Promise<boolean> {
  // Default: include recursive types but NOT functions (can't generate values for functions)
  const { includeRecursive = true, includeFunctions = false } = options;

  let n_type_success = 0;
  let n_type_fail = 0;
  const type_cache = new Set<string>();

  for (let i = 0; i < n_types; i++) {
    let n_success = 0;
    let n_fail = 0;

    // Generate a unique random type
    let type: EastType;
    let attempts = 0;
    while (true) {
      type = randomType(0, { includeRecursive, includeFunctions });
      const typeStr = printType(type);
      if (!type_cache.has(typeStr)) {
        type_cache.add(typeStr);
        break;
      }
      attempts++;
      if (attempts > 100) {
        // Give up and allow duplicates
        break;
      }
    }

    const type_fn = fn(type);
    const randomValue = randomValueFor(type);
    const print = printFor(type);

    for (let j = 0; j < n_samples; j++) {
      const value = randomValue();
      try {
        await type_fn(value);
        n_success++;
      } catch (e) {
        n_fail++;
        console.error(`    Test failed for type ${printType(type)}`);
        console.error(`    Value: ${print(value)}`);
        console.error(`    Error: ${(e as any)?.stack ?? e}`);
      }
    }

    if (n_fail > 0) {
      n_type_fail++;
      console.error(`  FAILED: ${n_success}/${n_samples} samples passed for type ${printType(type)}`);
    } else {
      n_type_success++;
    }
  }

  if (n_type_fail > 0) {
    console.error(`FAILED: ${n_type_success}/${n_types} types passed`);
    return false;
  } else {
    return true;
  }
}
