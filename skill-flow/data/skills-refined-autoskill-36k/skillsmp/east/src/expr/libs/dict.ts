/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { DictType, IntegerType, type EastType, FunctionType } from "../../types.js";
import { AstSymbol, Expr } from "../expr.js";
import type { SubtypeExprOrValue, ExprType } from "../types.js";

/** Standard library functions for dictionaries */
export default {
  /**
   * Generates a dictionary of a given size programmatically with functions from index to key and value.
   *
   * @typeParam K - The type of the dictionary keys
   * @typeParam V - The type of the dictionary values
   * @param size - The number of entries to generate
   * @param keyType - The East type of the dictionary keys
   * @param valueType - The East type of the dictionary values
   * @param keyFn - A function that takes an index and returns the key at that index
   * @param valueFn - A function that takes an index and returns the value at that index
   * @param onConflict - Optional function `(oldValue, newValue, key) => resolvedValue` to handle duplicate keys
   * @returns A dictionary expression containing the programmatically generated entries
   *
   * @throws East runtime error if duplicate keys are produced and no onConflict is provided
   *
   * @remarks
   * If the generator produces duplicate keys, an error will be thrown by default.
   * To handle duplicates, provide an `onConflict` function that receives the old value,
   * new value, and the conflicting key, and returns the value to use.
   *
   * @example
   * ```ts
   * // Generate dict with string keys and integer values
   * const makeDict = East.function([], DictType(StringType, IntegerType), ($) => {
   *   $.return(East.Dict.generate(
   *     3n,
   *     StringType,
   *     IntegerType,
   *     ($, i) => Expr.str`key${i}`,
   *     ($, i) => i.multiply(10n)
   *   ));
   * });
   * const compiled = East.compile(makeDict.toIR(), []);
   * compiled();  // { "key0": 0n, "key1": 10n, "key2": 20n }
   * ```
   *
   * @example
   * ```ts
   * // Generate dict with conflict resolution (keep larger value)
   * const makeDictConflict = East.function([], DictType(IntegerType, IntegerType), ($) => {
   *   $.return(East.Dict.generate(
   *     5n,
   *     IntegerType,
   *     IntegerType,
   *     ($, i) => i.remainder(3n),  // Creates duplicates: 0,1,2,0,1
   *     ($, i) => i,
   *     ($, oldVal, newVal, key) => oldVal.greaterThan(newVal).ifElse(() => oldVal, () => newVal)
   *   ));
   * });
   * const compiled = East.compile(makeDictConflict.toIR(), []);
   * compiled();  // { 0n: 3n, 1n: 4n, 2n: 2n }
   * ```
   */
  generate<K extends EastType, V extends EastType>(size: Expr<IntegerType> | bigint, keyType: K, valueType: V, keyFn: SubtypeExprOrValue<FunctionType<[IntegerType], NoInfer<K>>>, valueFn: SubtypeExprOrValue<FunctionType<[IntegerType], NoInfer<V>>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<V>, NoInfer<V>, NoInfer<K>], NoInfer<V>>>): ExprType<DictType<K, V>> {
    const length_expr = Expr.from(size, IntegerType);
    const key_expr = Expr.from(keyFn, FunctionType([IntegerType], keyType));
    const value_expr = Expr.from(valueFn, FunctionType([IntegerType], valueType));
    const on_conflict_expr = onConflict ? Expr.from(onConflict, FunctionType([valueType, valueType, keyType], valueType)) : Expr.function([valueType, valueType, keyType], valueType as any, ($, _v1, _v2, key) => $.error(Expr.str`Duplicate key ${key} in dict`));

    return Expr.fromAst({
      ast_type: "Builtin",
      type: DictType(keyType, valueType),
      builtin: "DictGenerate",
      type_parameters: [keyType, valueType],
      arguments: [length_expr[AstSymbol], key_expr[AstSymbol], value_expr[AstSymbol], on_conflict_expr[AstSymbol]],
      location: length_expr[AstSymbol].location,
    });
  },
}
