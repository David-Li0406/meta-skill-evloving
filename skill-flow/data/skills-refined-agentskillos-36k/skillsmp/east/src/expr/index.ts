/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

// Re-export all types
export * from './types.js';

// Re-export abstract base and concrete classes
import { Expr } from './expr.js';
export { Expr } from './expr.js';

export { NeverExpr } from './never.js';
export { NullExpr } from './null.js';
export { BooleanExpr } from './boolean.js';
export { IntegerExpr } from './integer.js';
export { FloatExpr } from './float.js';
export { DateTimeExpr } from './datetime.js';
export { StringExpr } from './string.js';
export { BlobExpr } from './blob.js';
export { RefExpr } from './ref.js';
export { ArrayExpr } from './array.js';
export { SetExpr } from './set.js';
export { DictExpr } from './dict.js';
export { StructExpr } from './struct.js';
export { VariantExpr } from './variant.js';
export { RecursiveExpr } from './recursive.js';
export { type CallableFunctionExpr, FunctionExpr } from './function.js';
export { type CallableAsyncFunctionExpr, AsyncFunctionExpr } from './asyncfunction.js';

// Import factory implementation
import { from, equal, notEqual, less, lessEqual, print, is, greaterEqual, greater, func, str, platform, asyncFunction, asyncPlatform, genericPlatform, asyncGenericPlatform, compile, compileAsync, equals, eq, notEquals, ne, lessThan, lt, lessThanOrEqual, lte, le, greaterThan, gt, greaterThanOrEqual, gte, ge, diff, applyPatch, composePatch, invertPatch } from './block.js';
export { BlockBuilder, type AsyncPlatformDefinition, type PlatformDefinition, type GenericPlatformDefinition, type AsyncGenericPlatformDefinition, equals, eq, notEquals, ne, lessThan, lt, lessThanOrEqual, lte, le, greaterThan, gt, greaterThanOrEqual, gte, ge, diff, applyPatch, composePatch, invertPatch } from './block.js';

// Import standard libraries
import IntegerLib from './libs/integer.js';
import FloatLib from './libs/float.js';
import DateTimeLib from './libs/datetime.js';
import StringLib from './libs/string.js';
import BlobLib from './libs/blob.js';
import ArrayLib from './libs/array.js';
import SetLib from './libs/set.js';
import DictLib from './libs/dict.js';

// Set up the factory in concrete classes so they can create expressions
// This allows methods like str.length() to work without passing factory manually
export type { ToExpr as ExprFactory } from './expr.js';

// /** Compile an East function to executable JavaScript.
//  *
//  * This is a convenience wrapper around `fn.toIR().compile(platform)`.
//  *
//  * @param fn - The East function to compile
//  * @param platform - Object mapping platform function names to their JavaScript implementations
//  * @returns Compiled JavaScript function that can be called with the specified input types
//  *
//  * @example
//  * ```ts
//  * const add = East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => a.add(b));
//  * const compiled = East.compile(add, {});
//  * const result = compiled(5n, 3n); // 8n
//  * ```
//  */
// function compile<I extends any[], O extends any>(
//   fn: FunctionExpr<I, O>,
//   platform: Record<string, (...args: any[]) => any>
// ): any {
//   return fn.toIR().compile(platform);
// }

/**
 * Standard entry point for constructing East expressions.
 *
 * @example
 * ```ts
 * // Create expressions from values
 * East.value(3.14).add(2)
 *
 * // String interpolation
 * East.str`Hello, ${name}!`
 *
 * // Comparisons
 * East.equal(x, y)
 * East.less(x, y)
 *
 * // Create functions
 * East.function([IntegerType], IntegerType, ($, x) => $.return(x.add(1n)))
 *
 * // Standard library
 * East.Integer.printCommaSeperated(1234567890n)
 * East.Array.range(0n, 10n)
 * ```
 */
export const East = {
  // Expr factories

  /** 
   * Compiles an East function into JavaScript function. 
   * 
   * @param f the function expression to compile
   * @param platform the platform functions available during compilation
   * @returns the compiled function
   * 
   * @example
   * ```ts
   * const add = East.function(
   *  [IntegerType, IntegerType],
   *  IntegerType,
   *  ($, a, b) => $.return(a.add(b))
   * );
   * const compiledAdd = East.compile(add, []);
   * console.log(compiledAdd(2n, 3n));
   * 
   **/
  compile: compile,

  /** 
   * Compiles an asyncronous East function into an asynchronous JavaScript function. 
   * 
   * @param f the async function expression to compile
   * @param platform the platform functions available during compilation
   * @returns the compiled async function
   * 
   * @example
   * ```ts
   * const add = East.asyncFunction(
   *  [IntegerType, IntegerType],
   *  IntegerType,
   *  ($, a, b) => $.return(a.add(b))
   * );
   * const compiledAdd = East.compileAsync(add, []);
   * console.log(await compiledAdd(2n, 3n));
   * 
   **/
  compileAsync: compileAsync,

  /**
   * Creates an East expression from a JavaScript value.
   * Type is inferred from the value, or can be explicitly specified.
   *
   * @param value - The JavaScript value to convert to an East expression
   * @param type - Optional explicit type specification
   * @returns An East expression wrapping the value
   *
   * @example
   * ```ts
   * East.value(42n)                    // IntegerExpr
   * East.value(3.14)                   // FloatExpr
   * East.value("hello")                // StringExpr
   * East.value([1n, 2n, 3n])           // ArrayExpr<IntegerType>
   * East.value(new Map([[1n, "a"]]))   // DictExpr<IntegerType, StringType>
   * ```
   */
  value: from,

  /**
   * Creates a string expression with interpolation support.
   * Allows embedding East expressions inside template literals.
   *
   * @returns A StringExpr with the interpolated values
   *
   * @example
   * ```ts
   * East.str`Hello, ${name}!`
   * East.str`Total: ${count} items`
   * East.str`Result: ${x.add(y)}`
   * ```
   */
  str,

  /**
   * Creates an East function with typed inputs and output.
   * Functions can be nested, serialized to IR, and compiled to JavaScript.
   *
   * @param inputs - Array of East types for function parameters
   * @param output - East type for function return value
   * @param body - Function body using block builder and parameters
   * @returns A FunctionExpr that can be compiled or serialized
   *
   * @example
   * ```ts
   * const add = East.function(
   *   [IntegerType, IntegerType],
   *   IntegerType,
   *   ($, a, b) => $.return(a.add(b))
   * );
   *
   * const fibonacci = East.function([IntegerType], IntegerType, ($, n) => {
   *   $.if(East.lessEqual(n, 1n), $ => $.return(n));
   *   $.return(fibonacci(n.subtract(1n)).add(fibonacci(n.subtract(2n))));
   * });
   * ```
   */
  function: func,

  /**
   * Creates an async East function with typed inputs and output.
   * Functions can be nested, serialized to IR, and compiled to JavaScript.
   *
   * @param inputs - Array of East types for function parameters
   * @param output - East type for function return value
   * @param body - Function body using block builder and parameters
   * @returns An AsyncFunctionExpr that can be compiled or serialized
   *
   * @example
   * ```ts
   * // An async function that pauses the program for a given number of milliseconds
   * const sleep = East.asyncPlatform("sleep", [IntegerType], NullType);
   *
   * // Wrap it in an async East function to wait whole number of seconds
   * const sleepSeconds = East.asyncFunction(
   *   [IntegerType],
   *   NullType,
   *   ($, seconds) => $(sleep(seconds.multiply(1000n)))
   * );
   * ```
   */
  asyncFunction,

  /**
   * Defines a platform function that can be called from East code.
   * Platform functions allow East code to interact with the external environment.
   *
   * @param name - The name of the platform function
   * @param inputs - Array of East types for the function parameters
   * @param output - East type for the function return value
   * @returns A callable platform function helper
   * 
   * @see {@link asyncPlatform} for defining async platform functions.
   *
   * @example
   * ```ts
   * const log = East.platform("log", [StringType], NullType);
   * const readFile = East.platform("readFile", [StringType], StringType);
   *
   * const myFunction = East.function([StringType], NullType, ($, msg) => {
   *   $(log(East.str`Message: ${msg}`));
   *   $.return(null);
   * });
   *
   * const platform = [
   *   log.implement(console.log),
   *   readFile.implement(fs.readFileSync),
   * ];
   * ```
   */
  platform,

  /**
   * Defines an asynchronous platform function that can be called from East code.
   * Platform functions allow East code to interact with the external environment.
   * East will handle awaiting the result automatically, but the platform function can only
   * be called from async East functions.
   *
   * @param name - The name of the platform function
   * @param inputs - Array of East types for the function parameters
   * @param output - East type for the function return value
   * @returns A callable platform function helper
   * 
   * @see {@link platform} for synchronous platform functions.
   *
   * @example
   * ```ts
   * const log = East.platform("log", [StringType], NullType);
   * const readFile = East.asyncPlatform("readFile", [StringType], StringType);
   *
   * const myFunction = East.asyncFunction([StringType], NullType, ($, msg) => {
   *   $(log(East.str`Message: ${msg}`));
   *   $.return(null);
   * });
   *
   * const asyncPlatform = [
   *   log.implement(console.log),
   *   readFile.implement(fs.promises.readFile),
   * ];
   * ```
   */
  asyncPlatform,

  /**
   * Defines a generic (polymorphic) platform function with type parameters.
   * Type parameters are passed at call time and flow through to the implementation.
   *
   * @param name - The name of the platform function
   * @param typeParams - Array of type parameter names (e.g., `["T", "U"]`)
   * @param inputsFn - Callback that receives placeholder types and returns input types
   * @param outputFn - Callback that receives placeholder types and returns output type
   * @returns A callable generic platform function helper
   *
   * @see {@link platform} for non-generic platform functions.
   * @see {@link asyncGenericPlatform} for async generic platform functions.
   *
   * @example
   * ```ts
   * // Define a generic log function
   * const log = East.genericPlatform(
   *   "log",
   *   ["T"],
   *   (T) => [T],
   *   (_T) => NullType
   * );
   *
   * // Use it - type is passed first, then value
   * const myFunction = East.function([StringType], NullType, ($, s) => {
   *   $(log(StringType, s));
   * });
   *
   * // Implementation receives type params as a factory
   * const platform = [
   *   log.implement((T) => (value) => {
   *     console.log(printFor(T)(value));
   *     return null;
   *   }),
   * ];
   * ```
   */
  genericPlatform,

  /**
   * Defines an asynchronous generic (polymorphic) platform function with type parameters.
   * The async variant of `genericPlatform`.
   *
   * @param name - The name of the platform function
   * @param typeParams - Array of type parameter names (e.g., `["T", "U"]`)
   * @param inputsFn - Callback that receives placeholder types and returns input types
   * @param outputFn - Callback that receives placeholder types and returns output type
   * @returns A callable async generic platform function helper
   *
   * @see {@link genericPlatform} for sync generic platform functions.
   * @see {@link asyncPlatform} for non-generic async platform functions.
   *
   * @example
   * ```ts
   * // Define an async generic fetch function
   * const fetchAs = East.asyncGenericPlatform(
   *   "fetchAs",
   *   ["T"],
   *   (_T) => [StringType],  // URL input
   *   (T) => T               // Returns parsed value of type T
   * );
   *
   * // Implementation receives type params and returns async function
   * const platform = [
   *   fetchAs.implement((T) => async (url) => {
   *     const response = await fetch(url);
   *     return parseFor(T)(await response.text());
   *   }),
   * ];
   * ```
   */
  asyncGenericPlatform,

  /**
   * Converts any East expression to its string representation.
   * Uses the East serialization format (not JSON).
   *
   * @param expr - The expression to convert to a string
   * @returns A StringExpr containing the string representation
   *
   * @example
   * ```ts
   * East.print(42n)                    // "42"
   * East.print(3.14)                   // "3.14"
   * East.print([1n, 2n, 3n])           // "[1, 2, 3]"
   * East.print({a: 1n, b: true})       // "(a=1, b=true)"
   * ```
   */
  print,

  /**
   * Deep equality comparison between two expressions.
   * Compares values recursively, including nested structures.
   *
   * @param a - First expression to compare
   * @param b - Second expression to compare
   * @returns BooleanExpr that is true if values are deeply equal
   *
   * @example
   * ```ts
   * East.equal(42n, 42n)                     // true
   * East.equal([1n, 2n], [1n, 2n])           // true
   * East.equal({a: 1n}, {a: 1n})             // true
   * East.equal(x, y)                         // compare two expressions
   * ```
   */
  equal,

  /**
   * Deep inequality comparison between two expressions.
   * Returns true if values are not deeply equal.
   *
   * @param a - First expression to compare
   * @param b - Second expression to compare
   * @returns BooleanExpr that is true if values are not equal
   *
   * @example
   * ```ts
   * East.notEqual(42n, 43n)                  // true
   * East.notEqual([1n, 2n], [1n, 3n])        // true
   * ```
   */
  notEqual,

  /**
   * Less-than comparison using East's total ordering.
   * All East types have a defined total ordering, even complex structures.
   *
   * @param a - First expression to compare
   * @param b - Second expression to compare
   * @returns BooleanExpr that is true if a < b
   *
   * @example
   * ```ts
   * East.less(1n, 2n)                        // true
   * East.less(3.14, 2.0)                     // false
   * East.less("apple", "banana")             // true
   * ```
   */
  less,

  /**
   * Less-than-or-equal comparison using East's total ordering.
   *
   * @param a - First expression to compare
   * @param b - Second expression to compare
   * @returns BooleanExpr that is true if a <= b
   *
   * @example
   * ```ts
   * East.lessEqual(1n, 1n)                   // true
   * East.lessEqual(2n, 1n)                   // false
   * ```
   */
  lessEqual,

  /**
   * Greater-than comparison using East's total ordering.
   *
   * @param a - First expression to compare
   * @param b - Second expression to compare
   * @returns BooleanExpr that is true if a > b
   *
   * @example
   * ```ts
   * East.greater(2n, 1n)                     // true
   * East.greater("banana", "apple")          // true
   * ```
   */
  greater,

  /**
   * Greater-than-or-equal comparison using East's total ordering.
   *
   * @param a - First expression to compare
   * @param b - Second expression to compare
   * @returns BooleanExpr that is true if a >= b
   *
   * @example
   * ```ts
   * East.greaterEqual(2n, 2n)                // true
   * East.greaterEqual(1n, 2n)                // false
   * ```
   */
  greaterEqual,

  // ============================================================================
  // Comparison function aliases
  // ============================================================================

  /** Alias for {@link equal} */
  equals,
  /** Alias for {@link equal} */
  eq,

  /** Alias for {@link notEqual} */
  notEquals,
  /** Alias for {@link notEqual} */
  ne,

  /** Alias for {@link less} */
  lessThan,
  /** Alias for {@link less} */
  lt,

  /** Alias for {@link lessEqual} */
  lessThanOrEqual,
  /** Alias for {@link lessEqual} */
  lte,
  /** Alias for {@link lessEqual} */
  le,

  /** Alias for {@link greater} */
  greaterThan,
  /** Alias for {@link greater} */
  gt,

  /** Alias for {@link greaterEqual} */
  greaterThanOrEqual,
  /** Alias for {@link greaterEqual} */
  gte,
  /** Alias for {@link greaterEqual} */
  ge,

  /**
   * Reference equality comparison for mutable types (Array, Set, Dict).
   * Checks if two expressions reference the same object in memory.
   *
   * @param a - First expression to compare
   * @param b - Second expression to compare
   * @returns BooleanExpr that is true if they reference the same object
   *
   * @example
   * ```ts
   * const arr = $.let(East.value([1n, 2n]));
   * East.is(arr, arr)                        // true (same reference)
   * East.is([1n, 2n], [1n, 2n])              // false (different objects)
   * ```
   */
  is,

  // ============================================================================
  // Patch Operations
  // ============================================================================

  /**
   * Compute the difference between two values of the same type.
   * Returns a patch that, when applied to `before`, produces `after`.
   *
   * @param before - The original value
   * @param after - The modified value
   * @returns A patch describing the changes
   *
   * @example
   * ```ts
   * const before = East.value([1n, 2n, 3n]);
   * const after = East.value([1n, 4n, 3n]);
   * const patch = East.diff(before, after);
   * ```
   */
  diff,

  /**
   * Apply a patch to a value, producing the modified value.
   *
   * @param value - The value to patch
   * @param patch - The patch to apply
   * @returns The patched value
   * @throws East runtime error if the patch conflicts with the value
   *
   * @example
   * ```ts
   * const result = East.applyPatch(original, patch);
   * ```
   */
  applyPatch,

  /**
   * Compose two patches into a single patch.
   * The result is a patch that has the same effect as applying `first` then `second`.
   *
   * @param first - The first patch to apply
   * @param second - The second patch to apply
   * @param type - The East type of the values being patched
   * @returns A composed patch
   * @throws East runtime error if the patches are incompatible
   *
   * @example
   * ```ts
   * const composed = East.composePatch(patch1, patch2, ArrayType(IntegerType));
   * ```
   */
  composePatch,

  /**
   * Invert a patch, producing a patch that undoes the original.
   * Applying the inverted patch to the "after" value produces the "before" value.
   *
   * @param patch - The patch to invert
   * @param type - The East type of the values being patched
   * @returns An inverted patch
   *
   * @example
   * ```ts
   * const inverted = East.invertPatch(patch, ArrayType(IntegerType));
   * const original = East.applyPatch(modified, inverted);
   * ```
   */
  invertPatch,

  // Root stdlib

  /**
   * Returns the minimum of two values using East's total ordering.
   *
   * @param a - First value
   * @param b - Second value
   * @returns The smaller of the two values
   *
   * @example
   * ```ts
   * East.min(5n, 3n)                         // 3n
   * East.min(3.14, 2.71)                     // 2.71
   * ```
   */
  min: Expr.min,

  /**
   * Returns the maximum of two values using East's total ordering.
   *
   * @param a - First value
   * @param b - Second value
   * @returns The larger of the two values
   *
   * @example
   * ```ts
   * East.max(5n, 3n)                         // 5n
   * East.max(3.14, 2.71)                     // 3.14
   * ```
   */
  max: Expr.max,

  /**
   * Clamps a value between minimum and maximum bounds.
   *
   * @param value - The value to clamp
   * @param min - The minimum bound
   * @param max - The maximum bound
   * @returns The clamped value
   *
   * @example
   * ```ts
   * East.clamp(5n, 0n, 10n)                  // 5n
   * East.clamp(-5n, 0n, 10n)                 // 0n
   * East.clamp(15n, 0n, 10n)                 // 10n
   * ```
   */
  clamp: Expr.clamp,

  // Type stdlibs

  /**
   * Standard library functions for Integer operations.
   * Provides formatting, rounding, and utility functions for integers.
   *
   * @example
   * ```ts
   * East.Integer.printCommaSeperated(1234567n)   // "1,234,567"
   * East.Integer.printCompact(1500000n)          // "1.5M"
   * East.Integer.printOrdinal(42n)               // "42nd"
   * East.Integer.roundNearest(47n, 10n)          // 50n
   * ```
   */
  Integer: IntegerLib,

  /**
   * Standard library functions for Float operations.
   * Provides rounding, formatting, and comparison functions for floating-point numbers.
   *
   * @example
   * ```ts
   * East.Float.roundToDecimals(3.14159, 2n)      // 3.14
   * East.Float.printCurrency(1234.56)            // "$1234.56"
   * East.Float.printPercentage(0.452, 1n)        // "45.2%"
   * East.Float.approxEqual(0.1, 0.10001, 0.001)  // true
   * ```
   */
  Float: FloatLib,

  /**
   * Standard library functions for DateTime operations.
   * Provides construction, parsing, and rounding functions for date/time values.
   *
   * @example
   * ```ts
   * East.DateTime.fromEpochMilliseconds(1640000000000n)
   * East.DateTime.fromComponents(2025n, 1n, 15n, 10n, 30n)
   * East.DateTime.roundDownDay(date, 1n)
   * East.DateTime.parseFormatted("%Y-%m-%d", "2025-01-15")
   * ```
   */
  DateTime: DateTimeLib,

  /**
   * Standard library functions for String operations.
   * Provides error formatting utilities.
   *
   * @example
   * ```ts
   * East.String.printError(errorMsg, stackTrace)
   * ```
   */
  String: StringLib,

  /**
   * Standard library functions for Blob operations.
   * Provides binary encoding utilities.
   *
   * @example
   * ```ts
   * East.Blob.encodeBeast(myValue, 'v2')         // Encode to BEAST format
   * ```
   */
  Blob: BlobLib,

  /**
   * Standard library functions for Array operations.
   * Provides generation utilities for creating arrays.
   *
   * @example
   * ```ts
   * East.Array.range(0n, 10n, 2n)                // [0n, 2n, 4n, 6n, 8n]
   * East.Array.linspace(0.0, 1.0, 11n)           // [0.0, 0.1, ..., 1.0]
   * East.Array.generate(5n, IntegerType, ($, i) => i.multiply(i))
   * ```
   */
  Array: ArrayLib,

  /**
   * Standard library functions for Set operations.
   * Provides generation utilities for creating sets.
   *
   * @example
   * ```ts
   * East.Set.generate(5n, IntegerType, ($, i) => i.multiply(2n))
   * ```
   */
  Set: SetLib,

  /**
   * Standard library functions for Dict operations.
   * Provides generation utilities for creating dictionaries.
   *
   * @example
   * ```ts
   * East.Dict.generate(
   *   5n,
   *   IntegerType,
   *   IntegerType,
   *   ($, i) => i,
   *   ($, i) => i.multiply(10n)
   * )
   * ```
   */
  Dict: DictLib,
};
