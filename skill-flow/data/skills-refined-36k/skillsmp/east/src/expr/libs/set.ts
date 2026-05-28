/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { FunctionType, type EastType, IntegerType, NullType, SetType } from "../../types.js";
import { AstSymbol, Expr } from "../expr.js";
import type { SubtypeExprOrValue, ExprType } from "../types.js";

/** Standard library functions for sets */
export default {
  /**
   * Generates a set of a given size programmatically with a function from index to key.
   *
   * @typeParam K - The type of the set keys
   * @param size - The number of elements to generate
   * @param keyType - The East type of the set keys
   * @param keyFn - A function that takes an index and returns the key at that index
   * @param onConflict - Optional function `(key) => null` to handle duplicate keys by ignoring them
   * @returns A set expression containing the programmatically generated keys
   *
   * @throws East runtime error if duplicate keys are produced and no onConflict is provided
   *
   * @remarks
   * If the generator produces duplicate keys, an error will be thrown by default.
   * To handle duplicates, provide an `onConflict` function that receives the duplicate key
   * and returns `null` to ignore it.
   *
   * @example
   * ```ts
   * // Generate set with string keys
   * const makeSet = East.function([], SetType(StringType), ($) => {
   *   $.return(East.Set.generate(
   *     3n,
   *     StringType,
   *     ($, i) => Expr.str`key${i}`
   *   ));
   * });
   * const compiled = East.compile(makeSet.toIR(), []);
   * compiled();  // Set(["key0", "key1", "key2"])
   * ```
   *
   * @example
   * ```ts
   * // Generate set with conflict resolution (ignore duplicates)
   * const makeSetConflict = East.function([], SetType(IntegerType), ($) => {
   *   $.return(East.Set.generate(
   *     5n,
   *     IntegerType,
   *     ($, i) => i.remainder(3n),  // Creates duplicates: 0,1,2,0,1
   *     ($, key) => null  // Ignore duplicates
   *   ));
   * });
   * const compiled = East.compile(makeSetConflict.toIR(), []);
   * compiled();  // Set([0n, 1n, 2n])
   * ```
   */
  generate<K extends EastType>(size: Expr<IntegerType> | bigint, keyType: K, keyFn: SubtypeExprOrValue<FunctionType<[IntegerType], NoInfer<K>>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<K>], NoInfer<K>>>): ExprType<SetType<K>> {
    const length_expr = Expr.from(size, IntegerType);
    const generator_expr = Expr.from(keyFn as any, FunctionType([IntegerType], keyType));
    const on_conflict_expr = onConflict ? Expr.from(onConflict as any, FunctionType([keyType], NullType)) : Expr.function([keyType], NullType, ($, key) => $.error(Expr.str`Duplicate key ${key} in set`));

    return Expr.fromAst({
      ast_type: "Builtin",
      type: SetType(keyType),
      builtin: "SetGenerate",
      type_parameters: [keyType],
      arguments: [length_expr[AstSymbol], generator_expr[AstSymbol], on_conflict_expr[AstSymbol]],
      location: length_expr[AstSymbol].location,
    });
  },
}