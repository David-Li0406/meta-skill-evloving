/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { ArrayType, FloatType, FunctionType, IntegerType, type EastType } from "../../types.js";
import { AstSymbol, Expr, TypeSymbol } from "../expr.js";
import type { ExprType, SubtypeExprOrValue } from "../types.js";

/** Standard library functions for arrays */
export default {
  /**
   * Creates an array containing a linear range of integers.
   *
   * @param start - The starting value (inclusive)
   * @param end - The ending value (exclusive)
   * @param step - The step size between consecutive values (default: 1)
   * @returns An array expression containing the integer range
   *
   * @remarks
   * The end of the range is exclusive, such that `East.range(0n, n)` produces `[0, 1, 2, ..., n-1]`.
   * This corresponds with the indices of an array of size `n`.
   *
   * @example
   * ```ts
   * const makeRange = East.function([], ArrayType(IntegerType), ($) => {
   *   $.return(East.Array.range(0n, 5n));
   * });
   * const compiled = East.compile(makeRange.toIR(), []);
   * compiled();  // [0n, 1n, 2n, 3n, 4n]
   * ```
   *
   * @example
   * ```ts
   * // With step
   * const makeRangeStep = East.function([], ArrayType(IntegerType), ($) => {
   *   $.return(East.Array.range(1n, 10n, 2n));
   * });
   * const compiled = East.compile(makeRangeStep.toIR(), []);
   * compiled();  // [1n, 3n, 5n, 7n, 9n]
   * ```
   */
  range(start: Expr<IntegerType> | bigint, end: Expr<IntegerType> | bigint, step: Expr<IntegerType> | bigint = 1n): ExprType<ArrayType<IntegerType>> {
    const start_val = Expr.from(start, IntegerType);
    const end_val = Expr.from(end, IntegerType);
    const step_val = Expr.from(step, IntegerType);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: ArrayType(IntegerType),
      builtin: "ArrayRange",
      type_parameters: [],
      arguments: [start_val[AstSymbol], end_val[AstSymbol], step_val[AstSymbol]],
      location: start_val[AstSymbol].location,
    });
  },

  /**
   * Creates an array containing equally-spaced floating point values.
   *
   * @param start - The starting value (inclusive)
   * @param stop - The ending value (inclusive)
   * @param size - The number of values to generate
   * @returns An array expression containing the equally-spaced float values
   *
   * @remarks
   * The stop value is inclusive, such that `East.linspace(0.0, 1.0, 11n)` produces 11 values
   * from `0.0` to `1.0` with a step of `0.1`.
   *
   * @example
   * ```ts
   * const makeLinspace = East.function([], ArrayType(FloatType), ($) => {
   *   $.return(East.Array.linspace(0.0, 1.0, 11n));
   * });
   * const compiled = East.compile(makeLinspace.toIR(), []);
   * compiled();  // [0.0, 0.1, 0.2, ..., 0.9, 1.0]
   * ```
   *
   * @example
   * ```ts
   * // Different spacing
   * const makeLinspace2 = East.function([], ArrayType(FloatType), ($) => {
   *   $.return(East.Array.linspace(0.0, 10.0, 5n));
   * });
   * const compiled = East.compile(makeLinspace2.toIR(), []);
   * compiled();  // [0.0, 2.5, 5.0, 7.5, 10.0]
   * ```
   */
  linspace(start: Expr<FloatType> | number, stop: Expr<FloatType> | number, size: Expr<IntegerType> | bigint): ExprType<ArrayType<FloatType>> {
    const start_val = Expr.from(start, FloatType);
    const stop_val = Expr.from(stop, FloatType);
    const count_val = Expr.from(size, IntegerType);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: ArrayType(FloatType),
      builtin: "ArrayLinspace",
      type_parameters: [],
      arguments: [start_val[AstSymbol], stop_val[AstSymbol], count_val[AstSymbol]],
      location: start_val[AstSymbol].location,
    });
  },

  /**
   * Generates an array of a given size programmatically with a function from index to value.
   *
   * @typeParam T - The type of elements in the generated array
   * @param size - The size of the array to generate
   * @param valueType - The East type of the array elements
   * @param valueFn - A function that takes an index and returns the value at that index
   * @returns An array expression containing the programmatically generated values
   *
   * @example
   * ```ts
   * // Generate array [0, 1, 4, 9, 16] (squares)
   * const makeSquares = East.function([], ArrayType(IntegerType), ($) => {
   *   $.return(East.Array.generate(5n, IntegerType, ($, i) => i.multiply(i)));
   * });
   * const compiled = East.compile(makeSquares.toIR(), []);
   * compiled();  // [0n, 1n, 4n, 9n, 16n]
   * ```
   *
   * @example
   * ```ts
   * // Generate array of strings ["Item 0", "Item 1", "Item 2"]
   * const makeItems = East.function([], ArrayType(StringType), ($) => {
   *   $.return(East.Array.generate(3n, StringType, ($, i) => Expr.str`Item ${i}`));
   * });
   * const compiled = East.compile(makeItems.toIR(), []);
   * compiled();  // ["Item 0", "Item 1", "Item 2"]
   * ```
   */
  generate<T>(size: Expr<IntegerType> | bigint, valueType: T, valueFn: SubtypeExprOrValue<FunctionType<[IntegerType], NoInfer<T>>>): ExprType<ArrayType<T>> {
    const length_expr = Expr.from(size, IntegerType);
    const generator_expr = Expr.from(valueFn as any, FunctionType([IntegerType], valueType));
    const value_type_deduced = generator_expr[TypeSymbol].output;
    return Expr.fromAst({
      ast_type: "Builtin",
      type: ArrayType(value_type_deduced),
      builtin: "ArrayGenerate",
      type_parameters: [value_type_deduced as EastType],
      arguments: [length_expr[AstSymbol], generator_expr[AstSymbol]],
      location: length_expr[AstSymbol].location,
    });
  },
}