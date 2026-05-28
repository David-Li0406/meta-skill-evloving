/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { DictType, BooleanType, FunctionType, IntegerType, type EastType, NullType, OptionType, SetType, NeverType, VariantType, printType, FloatType, isTypeEqual, ArrayType } from "../types.js";
import { valueOrExprToAst, valueOrExprToAstTyped } from "./ast.js";
import type { BooleanExpr } from "./boolean.js";
import { equal, notEqual } from "./block.js";
import type { IntegerExpr } from "./integer.js";
import { AstSymbol, Expr, FactorySymbol, TypeSymbol, type ToExpr } from "./expr.js";
import type { SubtypeExprOrValue, ExprType, TypeOf } from "./types.js";
import type { NullExpr } from "./null.js";
import type { BlockBuilder } from "./block.js";
import type { SetExpr } from "./set.js";
import type { FloatExpr } from "./float.js";
import type { ArrayExpr } from "./array.js";
import { none, some } from "../containers/variant.js";

/**
 * Expression representing dictionary (key-value map) values and operations.
 *
 * DictExpr provides methods for working with sorted dictionaries (maps) including lookup,
 * insertion, deletion, iteration, mapping, filtering, grouping, and aggregation operations.
 * Dictionaries maintain their entries sorted by key using East's total ordering.
 *
 * @example
 * ```ts
 * // Creating and manipulating dictionaries
 * const updateCounts = East.function([DictType(StringType, IntegerType), StringType], DictType(StringType, IntegerType), ($, counts, word) => {
 *   // Increment count for a word, initializing to 0 if missing
 *   $.return(counts.merge(word, 1n, ($, existing, increment) => existing.add(increment), () => 0n));
 * });
 * const compiled = East.compile(updateCounts.toIR(), []);
 * const counts = new Map([["hello", 5n], ["world", 3n]]);
 * compiled(counts, "hello");  // Map([["hello", 6n], ["world", 3n]])
 * compiled(counts, "new");    // Map([["hello", 6n], ["new", 1n], ["world", 3n]])
 * ```
 *
 * @example
 * ```ts
 * // Filtering and mapping
 * const filterHighScores = East.function([DictType(StringType, IntegerType)], DictType(StringType, IntegerType), ($, scores) => {
 *   $.return(scores.filter(($, score, name) => score.greaterOrEqual(100n)));
 * });
 * const compiled = East.compile(filterHighScores.toIR(), []);
 * const scores = new Map([["alice", 150n], ["bob", 75n], ["charlie", 200n]]);
 * compiled(scores);  // Map([["alice", 150n], ["charlie", 200n]])
 * ```
 */
export class DictExpr<K extends any, T extends any> extends Expr<DictType<K, T>> {
  constructor(private key_type: K, private value_type: T, ast: AST, createExpr: ToExpr) {
    super(ast.type as DictType<K, T>, ast, createExpr);
  }

  /**
   * Returns the number of key-value pairs in the dictionary.
   *
   * @returns An IntegerExpr representing the count of entries
   *
   * @example
   * ```ts
   * const getSize = East.function([DictType(StringType, IntegerType)], IntegerType, ($, dict) => {
   *   $.return(dict.size());
   * });
   * const compiled = East.compile(getSize.toIR(), []);
   * compiled(new Map([["a", 1n], ["b", 2n], ["c", 3n]]));  // 3n
   * compiled(new Map());  // 0n
   * ```
   */
  size(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DictSize",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Checks if a key exists in the dictionary.
   *
   * @param key - The key to search for
   * @returns A BooleanExpr that is true if the key exists, false otherwise
   *
   * @example
   * ```ts
   * const hasKey = East.function([DictType(StringType, IntegerType), StringType], BooleanType, ($, dict, key) => {
   *   $.return(dict.has(key));
   * });
   * const compiled = East.compile(hasKey.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict, "a");     // true
   * compiled(dict, "c");     // false
   * ```
   */
  has(key: SubtypeExprOrValue<K>): BooleanExpr {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "DictHas",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as BooleanExpr;
  }

  /**
   * Gets the value associated with a key in the dictionary.
   *
   * @param key - The key to look up
   * @param onMissing - Optional function to call if key is not found; if omitted, an error is thrown on missing key
   * @returns An expression of the value type
   *
   * @throws East runtime error if key is not found and onMissing is not provided
   *
   * @see {@link tryGet} for a safe lookup that returns an Option type
   * @see {@link getOrInsert} to insert a default value if the key is missing
   *
   * @example
   * ```ts
   * const getValue = East.function([DictType(StringType, IntegerType), StringType], IntegerType, ($, dict, key) => {
   *   $.return(dict.get(key));
   * });
   * const compiled = East.compile(getValue.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict, "a");  // 1n
   * // compiled(dict, "c") would throw error
   * ```
   *
   * @example
   * ```ts
   * // With missing handler
   * const getWithDefault = East.function([DictType(StringType, IntegerType), StringType], IntegerType, ($, dict, key) => {
   *   $.return(dict.get(key, () => -1n));
   * });
   * const compiled = East.compile(getWithDefault.toIR(), []);
   * compiled(dict, "a");  // 1n
   * compiled(dict, "c");  // -1n
   * ```
   */
  get(key: SubtypeExprOrValue<K>, onMissing?: SubtypeExprOrValue<FunctionType<[K], T>>): ExprType<T> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);

    if (onMissing === undefined) {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: this.value_type as EastType,
        location: get_location(),
        builtin: "DictGet",
        type_parameters: [this.key_type as EastType, this.value_type as EastType],
        arguments: [this[AstSymbol], keyAst],
      }) as ExprType<T>;
    } else {
      const onMissingExpr = Expr.from(onMissing as any, FunctionType([this.key_type as EastType], this.value_type as EastType));
      const onMissingAst = Expr.ast(onMissingExpr);

      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: this.value_type as EastType,
        location: get_location(),
        builtin: "DictGetOrDefault",
        type_parameters: [this.key_type as EastType, this.value_type as EastType],
        arguments: [this[AstSymbol], keyAst, onMissingAst],
      }) as ExprType<T>;
    }
  }

  /**
   * Safely gets a value from the dictionary, returning an Option type.
   *
   * @param key - The key to look up
   * @returns An Option containing the value if found (.some(value)), or .none if not found
   *
   * @see {@link get} for a version that throws an error on missing keys
   *
   * @example
   * ```ts
   * const tryGetValue = East.function([DictType(StringType, IntegerType), StringType], OptionType(IntegerType), ($, dict, key) => {
   *   $.return(dict.tryGet(key));
   * });
   * const compiled = East.compile(tryGetValue.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict, "a");  // { tag: "some", value: 1n }
   * compiled(dict, "c");  // { tag: "none", value: null }
   * ```
   *
   * @example
   * ```ts
   * // Using with match
   * const getOrDefault = East.function([DictType(StringType, IntegerType), StringType], IntegerType, ($, dict, key) => {
   *   $.return($.match(dict.tryGet(key), {
   *     some: ($, value) => value,
   *     none: () => 0n
   *   }));
   * });
   * const compiled = East.compile(getOrDefault.toIR(), []);
   * compiled(dict, "a");  // 1n
   * compiled(dict, "c");  // 0n
   * ```
   */
  tryGet(key: SubtypeExprOrValue<K>): ExprType<OptionType<T>> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: OptionType(this.value_type as EastType),
      location: get_location(),
      builtin: "DictTryGet",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as ExprType<OptionType<T>>;
  }

  /**
   * Inserts a new key-value pair into the dictionary.
   *
   * @param key - The key to insert
   * @param value - The value to associate with the key
   * @returns A NullExpr
   *
   * @throws East runtime error if the key already exists in the dictionary
   *
   * @see {@link update} for replacing an existing value
   * @see {@link insertOrUpdate} for inserting or updating without error
   * @see {@link getOrInsert} to insert a value lazily on lookup
   *
   * @example
   * ```ts
   * const insertEntry = East.function([DictType(StringType, IntegerType), StringType, IntegerType], NullType, ($, dict, key, value) => {
   *   $(dict.insert(key, value));
   *   $.return(null);
   * });
   * const compiled = East.compile(insertEntry.toIR(), []);
   * const dict = new Map([["a", 1n]]);
   * compiled(dict, "b", 2n);  // dict now has Map([["a", 1n], ["b", 2n]])
   * // compiled(dict, "a", 10n) would throw error (duplicate key)
   * ```
   */
  insert(key: SubtypeExprOrValue<K>, value: SubtypeExprOrValue<T>): ExprType<NullType> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    const valueAst = valueOrExprToAstTyped(value, this.value_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictInsert",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst, valueAst],
    }) as ExprType<NullType>;
  }

  /**
   * Inserts or updates a key-value pair in the dictionary.
   *
   * If the key already exists, the value is overwritten with the provided value. This operation is idempotent.
   *
   * @param key - The key to insert or update
   * @param value - The new value to associate with the key
   * @returns A NullExpr
   *
   * @see {@link insert} for inserting only (errors on duplicate)
   * @see {@link update} for updating only (errors on missing key)
   *
   * @example
   * ```ts
   * const upsert = East.function([DictType(StringType, IntegerType), StringType, IntegerType], NullType, ($, dict, key, value) => {
   *   $(dict.insertOrUpdate(key, value));
   *   $.return(null);
   * });
   * const compiled = East.compile(upsert.toIR(), []);
   * const dict = new Map([["a", 1n]]);
   * compiled(dict, "b", 2n);   // dict now has Map([["a", 1n], ["b", 2n]])
   * compiled(dict, "a", 10n);  // dict now has Map([["a", 10n], ["b", 2n]])
   * ```
   */
  insertOrUpdate(key: SubtypeExprOrValue<K>, value: SubtypeExprOrValue<T>): ExprType<NullType> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    const valueAst = valueOrExprToAstTyped(value, this.value_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictInsertOrUpdate",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst, valueAst],
    }) as ExprType<NullType>;
  }

  /**
   * Updates an existing value in the dictionary.
   *
   * @param key - The key to update
   * @param value - The new value to set
   * @returns A NullExpr
   *
   * @throws East runtime error if the key does not exist
   *
   * @see {@link insertOrUpdate} for inserting or updating without error
   * @see {@link getOrInsert} to get or insert a value
   * @see {@link merge} to update based on the existing value
   *
   * @example
   * ```ts
   * const updateValue = East.function([DictType(StringType, IntegerType), StringType, IntegerType], NullType, ($, dict, key, newValue) => {
   *   $(dict.update(key, newValue));
   *   $.return(null);
   * });
   * const compiled = East.compile(updateValue.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict, "a", 10n);  // dict now has Map([["a", 10n], ["b", 2n]])
   * // compiled(dict, "c", 3n) would throw error (key not found)
   * ```
   */
  update(key: SubtypeExprOrValue<K>, value: SubtypeExprOrValue<T>): ExprType<NullType> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    const valueAst = valueOrExprToAstTyped(value, this.value_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictUpdate",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst, valueAst],
    }) as ExprType<NullType>;
  }

  /**
   * Modifies a dictionary value at a key by merging it with a new value.
   *
   * This is useful for patterns where you want to update an entry based on its current value, e.g. incrementing a number,
   * appending to a string, updating fields in a struct, or pushing to an array.
   *
   * @param key - The key to update
   * @param value - The value to merge with the existing value
   * @param updateFn - Function accepting (existing, new, key) and returning the merged value
   * @param initialFn - Optional function to produce an initial value if key is missing; if omitted, an error is thrown on missing key
   * @returns A NullExpr
   *
   * @throws East runtime error if key is not found and initialFn is not provided
   *
   * @see {@link insertOrUpdate} and {@link update} for simply replacing the value
   *
   * @example
   * ```ts
   * // Increment counter, initializing to 0 if missing
   * const increment = East.function([DictType(StringType, IntegerType), StringType], NullType, ($, counts, word) => {
   *   $(counts.merge(word, 1n, ($, existing, inc) => existing.add(inc), () => 0n));
   *   $.return(null);
   * });
   * const compiled = East.compile(increment.toIR(), []);
   * const counts = new Map([["hello", 5n]]);
   * compiled(counts, "hello");  // counts now has Map([["hello", 6n]])
   * compiled(counts, "world");  // counts now has Map([["hello", 6n], ["world", 1n]])
   * ```
   *
   * @example
   * ```ts
   * // Append to string
   * const appendText = East.function([DictType(StringType, StringType), StringType, StringType], NullType, ($, dict, key, suffix) => {
   *   $(dict.merge(key, suffix, ($, existing, newVal) => existing.concat(newVal), () => ""));
   *   $.return(null);
   * });
   * const compiled = East.compile(appendText.toIR(), []);
   * const dict = new Map([["greeting", "Hello"]]);
   * compiled(dict, "greeting", " World");  // Map([["greeting", "Hello World"]])
   * compiled(dict, "new", "Hi");           // Map([["greeting", "Hello World"], ["new", "Hi"]])
   * ```
   */
  merge<T2>(key: SubtypeExprOrValue<K>, value: T2, updateFn: SubtypeExprOrValue<FunctionType<[T, TypeOf<NoInfer<T2>>, K], T>>, initialFn?: SubtypeExprOrValue<FunctionType<[K], T>>): ExprType<NullType> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    const valueAst = valueOrExprToAst(value);
    const value2Type = valueAst.type;

    const updateFnExpr = Expr.from(updateFn as any, FunctionType([this.value_type, value2Type, this.key_type], this.value_type));

    let initialExpr;
    if (initialFn === undefined) {
      // Default: create function that throws error
      initialExpr = Expr.function([this.key_type as EastType], this.value_type as EastType, ($, key) => $.error(Expr.str`Key ${key} not found in dictionary`, get_location()));
    } else {
      initialExpr = Expr.from(initialFn as any, FunctionType([this.key_type as EastType], this.value_type as EastType));
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictMerge",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, value2Type as EastType],
      arguments: [this[AstSymbol], keyAst, valueAst, Expr.ast(updateFnExpr as any), Expr.ast(initialExpr as any)],
    }) as ExprType<NullType>;
  }

  /**
   * Gets a value from the dictionary or inserts it if the key is not present.
   *
   * The default value is evaluated and inserted if the key is not present, otherwise the existing value is returned.
   *
   * @param key - The key to get or insert
   * @param defaultValue - Function that computes the default value if key is missing
   * @returns The existing value or the newly inserted value
   *
   * @see {@link get} for getting with a missing handler
   * @see {@link insert} for inserting with a conflict handler
   * @see {@link update} for updating existing values
   *
   * @example
   * ```ts
   * const getOrCreate = East.function([DictType(StringType, IntegerType), StringType], IntegerType, ($, dict, key) => {
   *   $.return(dict.getOrInsert(key, () => 0n));
   * });
   * const compiled = East.compile(getOrCreate.toIR(), []);
   * const dict = new Map([["a", 1n]]);
   * compiled(dict, "a");  // 1n (existing value)
   * compiled(dict, "b");  // 0n (new value inserted)
   * // dict now has Map([["a", 1n], ["b", 0n]])
   * ```
   */
  getOrInsert(key: SubtypeExprOrValue<K>, defaultValue: SubtypeExprOrValue<FunctionType<[K], T>>): ExprType<T> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    const defaultValueExpr = Expr.from(defaultValue as any, FunctionType([this.key_type as EastType], this.value_type as EastType));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this.value_type as EastType,
      location: get_location(),
      builtin: "DictGetOrInsert",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst, Expr.ast(defaultValueExpr as any)],
    }) as ExprType<T>;
  }

  /**
   * Deletes a key from the dictionary.
   *
   * @param key - The key to delete
   * @returns A NullExpr
   *
   * @throws East runtime error if the key does not exist
   *
   * @see {@link tryDelete} for a version that doesn't error on missing keys
   * @see {@link clear} to remove all keys
   * @see {@link pop} to delete and return the value
   *
   * @example
   * ```ts
   * const deleteKey = East.function([DictType(StringType, IntegerType), StringType], NullType, ($, dict, key) => {
   *   $(dict.delete(key));
   *   $.return(null);
   * });
   * const compiled = East.compile(deleteKey.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict, "a");  // dict now has Map([["b", 2n]])
   * // compiled(dict, "c") would throw error (key not found)
   * ```
   */
  delete(key: SubtypeExprOrValue<K>): ExprType<NullType> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictDelete",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as ExprType<NullType>;
  }

  /**
   * Tries to delete a key from the dictionary, returning whether it was deleted.
   *
   * @param key - The key to delete
   * @returns A BooleanExpr that is true if the key was deleted, false if not found
   *
   * @see {@link delete} for a version that errors on missing keys
   * @see {@link clear} to remove all keys
   *
   * @example
   * ```ts
   * const tryDeleteKey = East.function([DictType(StringType, IntegerType), StringType], BooleanType, ($, dict, key) => {
   *   $.return(dict.tryDelete(key));
   * });
   * const compiled = East.compile(tryDeleteKey.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict, "a");  // true (dict now has Map([["b", 2n]]))
   * compiled(dict, "c");  // false (key not found, dict unchanged)
   * ```
   */
  tryDelete(key: SubtypeExprOrValue<K>): ExprType<BooleanType> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "DictTryDelete",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as ExprType<BooleanType>;
  }

  /**
   * Removes a key from the dictionary and returns its value.
   *
   * @param key - The key to pop
   * @returns The value that was associated with the key
   *
   * @throws East runtime error if the key does not exist
   *
   * @see {@link delete} to remove a key without returning the value
   * @see {@link swap} to replace a value and return the old one
   *
   * @example
   * ```ts
   * const popKey = East.function([DictType(StringType, IntegerType), StringType], IntegerType, ($, dict, key) => {
   *   $.return(dict.pop(key));
   * });
   * const compiled = East.compile(popKey.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict, "a");  // 1n (dict now has Map([["b", 2n]]))
   * // compiled(dict, "c") would throw error (key not found)
   * ```
   */
  pop(key: SubtypeExprOrValue<K>): ExprType<T> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this.value_type as EastType,
      location: get_location(),
      builtin: "DictPop",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as ExprType<T>;
  }

  /**
   * Swaps a value in the dictionary, returning the previous value.
   *
   * @param key - The key to swap
   * @param value - The new value to insert
   * @returns The previous value that was associated with the key
   *
   * @throws East runtime error if the key does not exist
   *
   * @see {@link pop} to remove a key and return its value
   * @see {@link update} to update without returning the old value
   *
   * @example
   * ```ts
   * const swapValue = East.function([DictType(StringType, IntegerType), StringType, IntegerType], IntegerType, ($, dict, key, newValue) => {
   *   $.return(dict.swap(key, newValue));
   * });
   * const compiled = East.compile(swapValue.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict, "a", 10n);  // 1n (dict now has Map([["a", 10n], ["b", 2n]]))
   * // compiled(dict, "c", 3n) would throw error (key not found)
   * ```
   */
  swap(key: SubtypeExprOrValue<K>, value: SubtypeExprOrValue<T>): ExprType<T> {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    const valueAst = valueOrExprToAstTyped(value, this.value_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this.value_type as EastType,
      location: get_location(),
      builtin: "DictSwap",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst, valueAst],
    }) as ExprType<T>;
  }

  /**
   * Removes all keys from the dictionary.
   *
   * @returns A NullExpr
   *
   * @see {@link delete} or {@link tryDelete} to remove individual keys
   *
   * @example
   * ```ts
   * const clearDict = East.function([DictType(StringType, IntegerType)], NullType, ($, dict) => {
   *   $(dict.clear());
   *   $.return(null);
   * });
   * const compiled = East.compile(clearDict.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n], ["c", 3n]]);
   * compiled(dict);  // dict is now Map([])
   * ```
   */
  clear(): NullExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictClear",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as NullExpr;
  }

  /**
   * Unions another dictionary into this one in place.
   *
   * If a key exists in both dictionaries, a merger function can be provided to combine the values.
   * Without a merger function, an error is thrown on overlapping keys.
   *
   * @param dict2 - The dictionary to union with this one
   * @param mergeFn - Optional function to combine values when keys overlap; accepts (existing, new, key) and returns merged value
   * @returns A NullExpr
   *
   * @throws East runtime error if keys overlap and mergeFn is not provided
   *
   * @see {@link mergeAll} for a more general merge operation with different value types
   *
   * @example
   * ```ts
   * const unionDicts = East.function([DictType(StringType, IntegerType), DictType(StringType, IntegerType)], NullType, ($, dict1, dict2) => {
   *   $(dict1.unionInPlace(dict2, ($, existing, newVal) => existing.add(newVal)));
   *   $.return(null);
   * });
   * const compiled = East.compile(unionDicts.toIR(), []);
   * const dict1 = new Map([["a", 1n], ["b", 2n]]);
   * const dict2 = new Map([["b", 3n], ["c", 4n]]);
   * compiled(dict1, dict2);  // dict1 now has Map([["a", 1n], ["b", 5n], ["c", 4n]])
   * ```
   */
  unionInPlace(dict2: SubtypeExprOrValue<DictType<K, T>>, mergeFn?: SubtypeExprOrValue<FunctionType<[T, T, K], T>>): NullExpr {
    const dict2Expr = Expr.from(dict2 as any, this[TypeSymbol]);
    
    let mergerAst;
    if (mergeFn === undefined) {
      // Default: replace existing value with new value (ignore key and existing, return new)
      const mergerExpr = Expr.function([this.value_type as EastType, this.value_type as EastType, this.key_type as EastType], this.value_type as EastType, ($, _v1, _v2, k) => $.error(Expr.str`Key ${k} exists in both dictionaries`, get_location()));
      mergerAst = Expr.ast(mergerExpr);
    } else {
      const mergerExpr = Expr.from(mergeFn as any, FunctionType([this.value_type as EastType, this.value_type as EastType, this.key_type as EastType], this.value_type as EastType));
      mergerAst = Expr.ast(mergerExpr);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictUnionInPlace",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], Expr.ast(dict2Expr), mergerAst],
    }) as NullExpr;
  }

  /**
   * Merges all values from another dictionary into this one using a merge function.
   *
   * The type of the other dictionary can be different from this one, so long as the merge function can combine
   * the two value types into this dictionary's value type. This is useful for patterns like merging counts from
   * multiple dictionaries, pushing to nested arrays, or partially updating dictionaries-of-structs.
   *
   * @param dict2 - The dictionary whose values to merge into this one
   * @param mergeFn - Function accepting (existing, new, key) and returning the merged value
   * @param initialFn - Optional function to produce initial value for missing keys; if omitted, an error is thrown on missing key
   * @returns A NullExpr
   *
   * @throws East runtime error if a key is missing and initialFn is not provided
   *
   * @see {@link unionInPlace} for merging dictionaries of the same type
   * @see {@link merge} to merge a single key
   *
   * @example
   * ```ts
   * // Merge counts from two dictionaries
   * const mergeCounts = East.function(
   *   [DictType(StringType, IntegerType), DictType(StringType, IntegerType)],
   *   NullType,
   *   ($, counts1, counts2) => {
   *     $(counts1.mergeAll(counts2, ($, existing, newVal) => existing.add(newVal), () => 0n));
   *     $.return(null);
   *   }
   * );
   * const compiled = East.compile(mergeCounts.toIR(), []);
   * const counts1 = new Map([["apple", 5n], ["banana", 3n]]);
   * const counts2 = new Map([["banana", 2n], ["cherry", 7n]]);
   * compiled(counts1, counts2);  // counts1 now has Map([["apple", 5n], ["banana", 5n], ["cherry", 7n]])
   * ```
   */
  mergeAll<V2>(dict2: Expr<DictType<K, V2>>, mergeFn: SubtypeExprOrValue<FunctionType<[T, NoInfer<V2>, K], T>>, initialFn?: SubtypeExprOrValue<FunctionType<[K], T>>): NullExpr {
    const dict2Ast = Expr.ast(dict2);
    const value2Type = (dict2Ast.type as DictType<any, any>).value;

    const mergerExpr = Expr.from(mergeFn as any, FunctionType([this.value_type as EastType, value2Type as EastType, this.key_type as EastType], this.value_type as EastType));
    
    let initialExpr;
    if (initialFn === undefined) {
      // Default: create function that throws error
      initialExpr = Expr.function([this.key_type as EastType], this.value_type as EastType, ($, key) => $.error(Expr.str`Key ${key} not found in dictionary`, get_location()));
    } else {
      initialExpr = Expr.from(initialFn as any, FunctionType([this.key_type as EastType], this.value_type as EastType));
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictMergeAll",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, value2Type as EastType],
      arguments: [this[AstSymbol], dict2Ast, Expr.ast(mergerExpr as any), Expr.ast(initialExpr as any)],
    }) as NullExpr;
  }

  /**
   * Returns a set containing all keys in the dictionary.
   *
   * @returns A SetExpr containing all the dictionary's keys
   *
   * @see {@link getKeys} to get values for a subset of keys
   *
   * @example
   * ```ts
   * const getKeys = East.function([DictType(StringType, IntegerType)], SetType(StringType), ($, dict) => {
   *   $.return(dict.keys());
   * });
   * const compiled = East.compile(getKeys.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n], ["c", 3n]]);
   * compiled(dict);  // Set(["a", "b", "c"])
   * ```
   */
  keys(): ExprType<SetType<K>> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: SetType(this.key_type as EastType),
      location: get_location(),
      builtin: "DictKeys",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as ExprType<SetType<K>>;
  }

  /**
   * Collects the values associated with the given keys in a new dictionary.
   *
   * @param keys - Set of keys to look up
   * @param onMissing - Optional function to produce values for missing keys; if omitted, an error is thrown on missing key
   * @returns A new dictionary containing only the specified keys
   *
   * @throws East runtime error if a key is not found and onMissing is not provided
   *
   * @see {@link keys} to get all keys as a set
   *
   * @example
   * ```ts
   * const selectKeys = East.function([DictType(StringType, IntegerType), SetType(StringType)], DictType(StringType, IntegerType), ($, dict, keysToSelect) => {
   *   $.return(dict.getKeys(keysToSelect));
   * });
   * const compiled = East.compile(selectKeys.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n], ["c", 3n], ["d", 4n]]);
   * const keysToSelect = new Set(["a", "c"]);
   * compiled(dict, keysToSelect);  // Map([["a", 1n], ["c", 3n]])
   * ```
   *
   * @example
   * ```ts
   * // With missing handler
   * const selectWithDefault = East.function([DictType(StringType, IntegerType), SetType(StringType)], DictType(StringType, IntegerType), ($, dict, keys) => {
   *   $.return(dict.getKeys(keys, () => 0n));
   * });
   * const compiled = East.compile(selectWithDefault.toIR(), []);
   * const keysWithMissing = new Set(["a", "x"]);
   * compiled(dict, keysWithMissing);  // Map([["a", 1n], ["x", 0n]])
   * ```
   */
  getKeys(keys: SubtypeExprOrValue<SetType<K>>, onMissing?: SubtypeExprOrValue<FunctionType<[K], T>>): ExprType<DictType<K, T>> {
    const keysAst = valueOrExprToAstTyped(keys, SetType(this.key_type as EastType));

    let onMissingAst;
    if (onMissing === undefined) {
      // Default: throw error with key information if key doesn't exist
      const defaultFunction = Expr.function([this.key_type as EastType], this.value_type as EastType, ($, key) => $.error(Expr.str`Key ${key} not found in dictionary`, get_location()));
      onMissingAst = Expr.ast(defaultFunction);
    } else {
      const onMissingExpr = Expr.from(onMissing as any, FunctionType([this.key_type as EastType], this.value_type as EastType));
      onMissingAst = Expr.ast(onMissingExpr);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "DictGetKeys",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], keysAst, onMissingAst],
    }) as ExprType<DictType<K, T>>;
  }

  /**
   * Iterates over each key-value pair in the dictionary, applying a function to each.
   *
   * @param fn - Function to apply to each (value, key) pair
   * @returns A NullExpr
   *
   * @example
   * ```ts
   * const printEntries = East.function([DictType(StringType, IntegerType)], NullType, ($, dict) => {
   *   $(dict.forEach(($, value, key) => {
   *     // In a real platform, you could use a platform function to log
   *     // For this example, we just demonstrate the iteration structure
   *   }));
   *   $.return(null);
   * });
   * const compiled = East.compile(printEntries.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict);  // Iterates over all entries
   * ```
   */
  forEach(fn: SubtypeExprOrValue<FunctionType<[T, K], undefined>>): ExprType<NullType> {
    let fnAst;
    if (typeof fn === "function") {
      const fnExpr = Expr.function([this.value_type as EastType, this.key_type as EastType], undefined, fn as any);
      fnAst = Expr.ast(fnExpr);
    } else {
      const fnExpr = Expr.from(fn as any, FunctionType([this.value_type as EastType, this.key_type as EastType], undefined));
      fnAst = Expr.ast(fnExpr);
    }
    const returnType = fnAst.type.output as EastType;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "DictForEach",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, returnType],
      arguments: [this[AstSymbol], fnAst],
    }) as ExprType<NullType>;
  }

  /**
   * Creates a shallow copy of the dictionary.
   *
   * @returns A new DictExpr containing the same key-value pairs
   *
   * @example
   * ```ts
   * const copyDict = East.function([DictType(StringType, IntegerType)], DictType(StringType, IntegerType), ($, dict) => {
   *   $.return(dict.copy());
   * });
   * const compiled = East.compile(copyDict.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * const copy = compiled(dict);  // Map([["a", 1n], ["b", 2n]])
   * // Modifying copy doesn't affect dict
   * ```
   */
  copy(): ExprType<DictType<K, T>> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "DictCopy",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as ExprType<DictType<K, T>>;
  }

  /**
   * Creates a new dictionary by mapping each value through a function.
   *
   * The dictionary will have the same keys as the original, but the values will be transformed.
   *
   * @param fn - Function that maps each (value, key) pair to a new value
   * @returns A new DictExpr with the same keys but transformed values
   *
   * @see {@link toDict} to also transform keys
   * @see {@link filter} to select a subset of entries
   *
   * @example
   * ```ts
   * const doubleValues = East.function([DictType(StringType, IntegerType)], DictType(StringType, IntegerType), ($, dict) => {
   *   $.return(dict.map(($, value, key) => value.multiply(2n)));
   * });
   * const compiled = East.compile(doubleValues.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n], ["c", 3n]]);
   * compiled(dict);  // Map([["a", 2n], ["b", 4n], ["c", 6n]])
   * ```
   */
  map<T2>(fn: Expr<FunctionType<[T, K], T2>>): DictExpr<K, T2>;
  map<F extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(fn: F): DictExpr<K, TypeOf<ReturnType<F>>>;
  map(fn: Expr<FunctionType> | (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)): DictExpr<K, any> {
    let fnExpr: Expr<FunctionType>;
    if (typeof fn === "function") {
      fnExpr = Expr.function([this.value_type, this.key_type], undefined, fn) as Expr<FunctionType>;
    } else {
      fnExpr = fn;
    }
    const fnAst = Expr.ast(fnExpr);
    const returnType = fnAst.type.output as EastType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: DictType(this.key_type, returnType),
      location: get_location(),
      builtin: "DictMap",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, returnType],
      arguments: [this[AstSymbol], Expr.ast(fnExpr as any)],
    }) as DictExpr<K, any>;
  }

  /**
   * Filters the dictionary by applying a predicate function to each entry.
   *
   * @param fn - Predicate function that returns true to keep an entry, false to discard it
   * @returns A new DictExpr containing only entries for which the predicate returned true
   *
   * @see {@link filterMap} to filter and map in one operation
   * @see {@link map} to transform values without filtering
   *
   * @example
   * ```ts
   * const filterLargeValues = East.function([DictType(StringType, IntegerType)], DictType(StringType, IntegerType), ($, dict) => {
   *   $.return(dict.filter(($, value, key) => value.greaterOrEqual(10n)));
   * });
   * const compiled = East.compile(filterLargeValues.toIR(), []);
   * const dict = new Map([["a", 5n], ["b", 15n], ["c", 20n], ["d", 8n]]);
   * compiled(dict);  // Map([["b", 15n], ["c", 20n]])
   * ```
   */
  filter(fn: SubtypeExprOrValue<FunctionType<[T, K], BooleanType>>): DictExpr<K, T> {
    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type as EastType, this.key_type as EastType], BooleanType));

    return Expr.fromAst({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "DictFilter",
      type_parameters: [this.key_type as EastType, this.value_type as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as DictExpr<K, T>;
  }

  /**
   * Filters and maps the dictionary in a single operation.
   *
   * The supplied function must return an Option type, where `none` indicates the key should be filtered out,
   * and `some(value)` indicates the value should be included in the output, mapped to `value`.
   *
   * This is more efficient than using `filter` followed by `map`, as it only iterates once.
   *
   * @param fn - Function that returns an Option type for each (value, key) pair
   * @returns A new DictExpr containing only entries that returned some(value), with mapped values
   *
   * @see {@link filter} to only filter values
   * @see {@link map} to only map values
   *
   * @example
   * ```ts
   * const filterMapEven = East.function([DictType(StringType, IntegerType)], DictType(StringType, IntegerType), ($, dict) => {
   *   $.return(dict.filterMap(($, value, key) =>
   *     value.modulo(2n).equal(0n).ifElse(
   *       () => East.some(value.divide(2n)),
   *       () => East.none
   *     )
   *   ));
   * });
   * const compiled = East.compile(filterMapEven.toIR(), []);
   * const dict = new Map([["a", 2n], ["b", 3n], ["c", 4n], ["d", 5n]]);
   * compiled(dict);  // Map([["a", 1n], ["c", 2n]]) - only even values, halved
   * ```
   */
  filterMap<T2>(fn: Expr<FunctionType<[T, IntegerType], OptionType<T2>>>): DictExpr<K, T2>;
  filterMap<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(fn: F): DictExpr<K, TypeOf<ReturnType<F>> extends VariantType<infer U> ? "some" extends keyof U ? U["some"] : NeverType : NeverType>;
  filterMap(fn: any): DictExpr<K, any> {
    let fnExpr: Expr<FunctionType>;
    if (typeof fn === "function") {
      fnExpr = Expr.function([this.value_type as EastType, this.key_type as EastType], undefined, fn as any) as Expr<FunctionType>;
    } else {
      fnExpr = fn;
    }

    const fnAst = Expr.ast(fnExpr);
    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Variant") {
      throw new Error(`Expected Function to return an Option type, got ${printType(returnType)}`);
    }
    if (!Object.keys(returnType.cases).every(k => k === "none" || k === "some")) {
      throw new Error(`Expected Function to return an Option type, got ${printType(returnType)}`);
    }
    const someType = returnType.cases["some"] ?? NeverType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "DictFilterMap",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, someType as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as DictExpr<K, any>;
  }

  /**
   * Creates an array from the dictionary by mapping each entry through a function.
   *
   * If no function is provided, the dictionary values are copied as-is (and the keys are discarded).
   *
   * @param fn - Optional function to map each (value, key) pair to an array element
   * @returns An ArrayExpr containing the mapped values
   *
   * @see {@link toSet} to create a set instead
   * @see {@link toDict} to create a dictionary with transformed keys
   *
   * @example
   * ```ts
   * const dictToArray = East.function([DictType(StringType, IntegerType)], ArrayType(IntegerType), ($, dict) => {
   *   $.return(dict.toArray());  // Just values
   * });
   * const compiled = East.compile(dictToArray.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n], ["c", 3n]]);
   * compiled(dict);  // [1n, 2n, 3n]
   * ```
   *
   * @example
   * ```ts
   * // With mapping function
   * const pairsToArray = East.function([DictType(StringType, IntegerType)], ArrayType(StringType), ($, dict) => {
   *   $.return(dict.toArray(($, value, key) => Expr.str`${key}: ${value}`));
   * });
   * const compiled = East.compile(pairsToArray.toIR(), []);
   * compiled(dict);  // ["a: 1", "b: 2", "c: 3"]
   * ```
   */
  toArray<T2>(fn: Expr<FunctionType<[T, K], T2>>): ArrayExpr<T2>;
  toArray<F extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(fn: F): ArrayExpr<TypeOf<ReturnType<F>>>;
  toArray(): ArrayExpr<T>;
  toArray(fn?: any): ArrayExpr<any> {
    let fnExpr: Expr<FunctionType>;
    if (fn === undefined) {
      // Identity function
      fnExpr = Expr.function([this.value_type as EastType, this.key_type as EastType], this.value_type as EastType, ($, value) => value) as Expr<FunctionType>;
    } else if (typeof fn === "function") {
      fnExpr = Expr.function([this.value_type, this.key_type], undefined, fn) as Expr<FunctionType>;
    } else {
      fnExpr = fn;
    }
    const fnType = fnExpr[TypeSymbol] as FunctionType;
    const returnType = fnType.output as EastType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: ArrayType(returnType),
      location: get_location(),
      builtin: "DictToArray",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, returnType as EastType],
      arguments: [this[AstSymbol], Expr.ast(fnExpr as any)],
    }) as ArrayExpr<any>;
  }

  /**
   * Creates a set by mapping each dictionary entry through a function.
   *
   * Duplicates are ignored, and only unique values are kept.
   *
   * @param fn - Function to map each (value, key) pair to a set element
   * @returns A SetExpr containing the unique mapped values
   *
   * @see {@link keys} to get a set of the dictionary's keys
   * @see {@link toArray} to create an array instead
   *
   * @example
   * ```ts
   * const extractCategories = East.function([DictType(StringType, StructType({category: StringType, price: IntegerType}))], SetType(StringType), ($, products) => {
   *   $.return(products.toSet(($, product, name) => product.category));
   * });
   * const compiled = East.compile(extractCategories.toIR(), []);
   * const products = new Map([
   *   ["apple", {category: "fruit", price: 100n}],
   *   ["banana", {category: "fruit", price: 80n}],
   *   ["carrot", {category: "vegetable", price: 50n}]
   * ]);
   * compiled(products);  // Set(["fruit", "vegetable"])
   * ```
   */
  toSet<K2>(fn: Expr<FunctionType<[T, K], K2>>): SetExpr<K2>
  toSet<F extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(fn: F): SetExpr<TypeOf<ReturnType<F>>>
  toSet(keyFn?: any): SetExpr<any> {
    let keyFnAst
    if (keyFn !== undefined) {
      let fnExpr: Expr<FunctionType>;
      if (typeof keyFn === "function") {
        fnExpr = Expr.function([this.value_type, this.key_type], undefined, keyFn) as Expr<FunctionType>;
      } else {
        fnExpr = keyFn;
      }
      keyFnAst = Expr.ast(fnExpr as any);
    } else {
      // Identity function
      const identityFunction = Expr.function([this.value_type as EastType, this.key_type as EastType], this.value_type as EastType, ($, value) => value);
      keyFnAst = Expr.ast(identityFunction as any);
    }

    const keyType = (keyFnAst.type as FunctionType).output as EastType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: SetType(keyType),
      location: get_location(),
      builtin: "DictToSet",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, keyType as EastType],
      arguments: [this[AstSymbol], keyFnAst],
    }) as SetExpr<any>;
  }

  /**
   * Converts the dictionary to another dictionary with transformed keys and/or values.
   *
   * Functions can be provided to calculate the new key and value for each entry. If a duplicate key is produced,
   * an error is thrown by default. A conflict handler function may be provided to merge duplicate keys.
   *
   * This method differs from {@link map} in that the keys of the dictionary are also transformed.
   *
   * @param keyFn - Function to compute the new key for each entry
   * @param valueFn - Optional function to compute the new value for each entry; if omitted, values are kept as-is
   * @param onConflict - Optional function to handle duplicate keys; accepts (existing, new, key) and returns merged value
   * @returns A new DictExpr with transformed keys and values
   *
   * @throws East runtime error if duplicate keys are produced and onConflict is not provided
   *
   * @see {@link map} to transform only values while keeping keys
   * @see {@link groupReduce} for more complex grouping operations
   *
   * @example
   * ```ts
   * // Transform keys to uppercase, keep values
   * const uppercaseKeys = East.function([DictType(StringType, IntegerType)], DictType(StringType, IntegerType), ($, dict) => {
   *   $.return(dict.toDict(($, value, key) => key.toUpper()));
   * });
   * const compiled = East.compile(uppercaseKeys.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n]]);
   * compiled(dict);  // Map([["A", 1n], ["B", 2n]])
   * ```
   *
   * @example
   * ```ts
   * // Group by key length, sum values for duplicate lengths
   * const groupByLength = East.function([DictType(StringType, IntegerType)], DictType(IntegerType, IntegerType), ($, dict) => {
   *   $.return(dict.toDict(
   *     ($, value, key) => key.size(),
   *     ($, value, key) => value,
   *     ($, existing, newVal, len) => existing.add(newVal)
   *   ));
   * });
   * const compiled = East.compile(groupByLength.toIR(), []);
   * const dict2 = new Map([["a", 1n], ["ab", 2n], ["c", 3n], ["def", 4n]]);
   * compiled(dict2);  // Map([[1n, 4n], [2n, 2n], [3n, 4n]])
   * ```
   */
  toDict<K2, T2>(keyFn: Expr<FunctionType<[T, K], K2>>, valueFn: Expr<FunctionType<[T, K], T2>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<T2>, NoInfer<T2>, NoInfer<K2>], NoInfer<T2>>>): DictExpr<K2, T2>
  toDict<K2, ValueFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[T, K], K2>>, valueFn: ValueFn, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, NoInfer<K2>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<K2, TypeOf<ReturnType<ValueFn>>>;
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any), T2>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, K], T2>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<T2>, NoInfer<T2>, TypeOf<ReturnType<NoInfer<KeyFn>>>], NoInfer<T2>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, T2>
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: ValueFn, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, NoInfer<TypeOf<ReturnType<NoInfer<KeyFn>>>>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<ValueFn>>>;
  toDict<K2>(keyFn: Expr<FunctionType<[T, K], K2>>): DictExpr<K2, T>
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, T>;
  toDict(keyFn: any, valueFn?: any, onConflictFn?: any): DictExpr<any, any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn ?? ((_$: any, v: any, k: any) => k), FunctionType([this.value_type, this.key_type], undefined));
    const keyType = keyFnAst.type.output as EastType;

    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, v: any) => v), FunctionType([this.value_type, this.key_type], undefined));
    const valueType = valueFnAst.type.output as EastType;

    let onConflictAst;
    if (onConflictFn === undefined) {
      const location = get_location();
      const onConflictFunction = Expr.function([valueType, valueType, keyType], valueType, ($, existing, value, key) => $.error(Expr.str`Cannot insert duplicate key ${key} into dict`, location));
      onConflictAst = Expr.ast(onConflictFunction);
    } else {
      onConflictAst = valueOrExprToAstTyped(onConflictFn as any, FunctionType([valueType, valueType, keyType], valueType));
    }

    return Expr.fromAst({
      ast_type: "Builtin",
      type: DictType(keyType, valueType),
      location: get_location(),
      builtin: "DictToDict",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, keyType, valueType],
      arguments: [this[AstSymbol], keyFnAst, valueFnAst, onConflictAst],
    }) as DictExpr<any, any>;
  }

  /**
   * Maps each entry to an array and flattens the results into a single array.
   *
   * The supplied function must return an Array type. The resulting arrays are concatenated together.
   * If the dictionary values are already arrays, the mapping function can be omitted.
   *
   * @param fn - Function that maps each (value, key) pair to an array
   * @returns A single ArrayExpr containing all elements from all mapped arrays
   *
   * @see {@link toArray} to create an array with the same number of elements (no flattening)
   * @see {@link flattenToSet} to flatten to a set instead
   * @see {@link flattenToDict} to flatten to a dictionary
   *
   * @example
   * ```ts
   * const expandRanges = East.function([DictType(StringType, IntegerType)], ArrayType(IntegerType), ($, dict) => {
   *   $.return(dict.flattenToArray(($, count, name) => {
   *     const arr = Expr.from([], ArrayType(IntegerType));
   *     $.for(0n, ($) => count, ($, i) => {
   *       $(arr.pushLast(i));
   *     });
   *     return arr;
   *   }));
   * });
   * const compiled = East.compile(expandRanges.toIR(), []);
   * const dict = new Map([["a", 2n], ["b", 3n]]);
   * compiled(dict);  // [0n, 1n, 0n, 1n, 2n] - flattened ranges
   * ```
   */
  flattenToArray<T2>(fn: Expr<FunctionType<[T, K], ArrayType<T2>>>): ArrayExpr<T2>;
  flattenToArray<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(fn: F): TypeOf<ReturnType<F>> extends ArrayType<infer U> ? ArrayExpr<U> : never;
  flattenToArray(): T extends ArrayType<infer T2> ? ArrayExpr<T2> : never;
  flattenToArray(fn?: any): ArrayExpr<any> {
    const fnAst = valueOrExprToAstTyped(fn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, this.key_type], undefined));

    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Array") {
      throw new Error(`Expected Function to return an Array type, got ${printType(returnType)}`);
    }
    const elementType = returnType.value;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: ArrayType(elementType as EastType),
      location: get_location(),
      builtin: "DictFlattenToArray",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, elementType as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as ArrayExpr<any>;
  }

  /**
   * Maps each entry to a set and flattens the results by unioning them together.
   *
   * The supplied function must return a Set type. The resulting sets are unioned to produce a single flattened set.
   * Duplicates are ignored. If the dictionary values are already sets, the mapping function can be omitted.
   *
   * @param fn - Function that maps each (value, key) pair to a set
   * @returns A single SetExpr containing all unique elements from all mapped sets
   *
   * @see {@link flattenToArray} to flatten to an array instead
   * @see {@link flattenToDict} to flatten to a dictionary
   * @see {@link toSet} to convert to a set without flattening
   *
   * @example
   * ```ts
   * const getAllTags = East.function([DictType(StringType, ArrayType(StringType))], SetType(StringType), ($, articles) => {
   *   $.return(articles.flattenToSet(($, tags, title) => tags.toSet()));
   * });
   * const compiled = East.compile(getAllTags.toIR(), []);
   * const articles = new Map([
   *   ["Article 1", ["javascript", "programming"]],
   *   ["Article 2", ["python", "programming"]],
   *   ["Article 3", ["javascript", "web"]]
   * ]);
   * compiled(articles);  // Set(["javascript", "programming", "python", "web"])
   * ```
   */
  flattenToSet<K2>(fn: Expr<FunctionType<[T, K], SetType<K2>>>): SetExpr<K2>;
  flattenToSet<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(fn: F): TypeOf<ReturnType<F>> extends SetType<infer U> ? SetExpr<U> : never;
  flattenToSet(): T extends SetType<infer K2> ? SetExpr<K2> : never;
  flattenToSet(fn?: any): SetExpr<any> {
    const fnAst = valueOrExprToAstTyped(fn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, this.key_type], undefined));
    
    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Set") {
      throw new Error(`Expected Function to return a Set type, got ${printType(returnType)}`);
    }
    const elementType = returnType.key;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: SetType(elementType as EastType),
      location: get_location(),
      builtin: "DictFlattenToSet",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, elementType as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as SetExpr<any>;
  }

  /**
   * Maps each entry to a dictionary and flattens the results by merging them together.
   *
   * The supplied function must return a Dict type. The resulting dictionaries are merged together to produce a single
   * flattened dictionary. In case of duplicate keys, an error is thrown by default. A conflict handler function may be
   * provided to merge duplicate keys. If the dictionary values are already dictionaries, the mapping function can be omitted.
   *
   * @param fn - Function that maps each (value, key) pair to a dictionary
   * @param onConflict - Optional function to handle duplicate keys; accepts (existing, new, key) and returns merged value
   * @returns A single DictExpr containing all entries from all mapped dictionaries
   *
   * @throws East runtime error if duplicate keys are found and onConflict is not provided
   *
   * @see {@link flattenToArray} to flatten to an array instead
   * @see {@link flattenToSet} to flatten to a set
   * @see {@link toDict} to convert to a dictionary without flattening
   *
   * @example
   * ```ts
   * const mergeNestedDicts = East.function([DictType(StringType, DictType(StringType, IntegerType))], DictType(StringType, IntegerType), ($, nested) => {
   *   $.return(nested.flattenToDict(undefined, ($, existing, newVal) => existing.add(newVal)));
   * });
   * const compiled = East.compile(mergeNestedDicts.toIR(), []);
   * const nested = new Map([
   *   ["group1", new Map([["a", 1n], ["b", 2n]])],
   *   ["group2", new Map([["b", 3n], ["c", 4n]])]
   * ]);
   * compiled(nested);  // Map([["a", 1n], ["b", 5n], ["c", 4n]])
   * ```
   */
  flattenToDict<K2, V2>(fn: Expr<FunctionType<[K], DictType<K2, V2>>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<V2>, NoInfer<V2>, NoInfer<K2>], NoInfer<V2>>>): DictExpr<K2, V2>;
  flattenToDict<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(fn: F, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never, TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never, TypeOf<ReturnType<NoInfer<F>>> extends DictType<infer K2, any> ? K2 : never], TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never>>): TypeOf<ReturnType<F>> extends DictType<infer K2, infer V2> ? DictExpr<K2, V2> : never;
  flattenToDict(): T extends DictType<infer K2, infer V2> ? DictExpr<K2, V2> : never;
  flattenToDict(fn?: any, onConflictFn?: any): DictExpr<any, any> {
    const fnAst = valueOrExprToAstTyped(fn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, this.key_type], undefined));
    
    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Dict") {
      throw new Error(`Expected Function to return a Dict type, got ${printType(returnType)}`);
    }
    const keyType = returnType.key;
    const valueType = returnType.value;

    let onConflictAst;
    if (onConflictFn === undefined) {
      const location = get_location();
      const onConflictFunction = Expr.function([valueType, valueType, keyType], valueType, ($, existing, value, key) => $.error(Expr.str`Cannot insert duplicate key ${key} into dict`, location));
      onConflictAst = Expr.ast(onConflictFunction);
    } else {
      onConflictAst = valueOrExprToAstTyped(onConflictFn as any, FunctionType([valueType, valueType, keyType], valueType));
    }

    return Expr.fromAst({
      ast_type: "Builtin",
      type: DictType(keyType as EastType, valueType as EastType),
      location: get_location(),
      builtin: "DictFlattenToDict",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, keyType as EastType, valueType as EastType],
      arguments: [this[AstSymbol], fnAst, onConflictAst],
    }) as DictExpr<any, any>;
  }

  /** Group entries by key and perform a fold/reduce operation on each group.
   *
   * @param keyFn - Function that maps each value and key to a group key
   * @param initFn - Function that creates the initial accumulator value for each group
   * @param reduceFn - Function that combines the accumulator with each value and key in the group
   * @returns A dictionary mapping group keys to reduced values
   *
   * @example
   * ```ts
   * const d = new Dict({ a: 1n, b: 2n, c: 3n, d: 4n, e: 5n, f: 6n })
   * // Group by even/odd and sum each group
   * const result = d.groupReduce(
   *   ($, v, k) => v.remainder(2n).equal(0n).ifElse(() => "even", () => "odd"),
   *   ($, groupKey) => 0n,
   *   ($, acc, v, k) => acc.add(v)
   * )
   * // Result: { "even": 12n, "odd": 9n }
   * ```
   */
  groupReduce<K2, T2>(keyFn: Expr<FunctionType<[T, K], K2>>, initFn: Expr<FunctionType<[K2], T2>>, reduceFn: SubtypeExprOrValue<FunctionType<[T2, T, K], T2>>): DictExpr<K2, T2>
  groupReduce<K2, InitFn extends ($: BlockBuilder<NeverType>, k2: ExprType<NoInfer<K2>>) => any>(keyFn: Expr<FunctionType<[T, K], K2>>, initFn: InitFn, reduceFn: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<InitFn>>>, T, K], TypeOf<ReturnType<NoInfer<InitFn>>>>>): DictExpr<K2, TypeOf<ReturnType<InitFn>>>
  groupReduce<KeyFn extends ($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any, T2>(keyFn: KeyFn, initFn: Expr<FunctionType<[TypeOf<ReturnType<NoInfer<KeyFn>>>], T2>>, reduceFn: SubtypeExprOrValue<FunctionType<[T2, T, K], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, T2>
  groupReduce<KeyFn extends ($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any, InitFn extends ($: BlockBuilder<NeverType>, k2: ExprType<TypeOf<ReturnType<NoInfer<KeyFn>>>>) => any>(keyFn: KeyFn, initFn: InitFn, reduceFn: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<InitFn>>>, T, K], TypeOf<ReturnType<NoInfer<InitFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<InitFn>>>
  groupReduce(keyFn: any, initFn: any, reduceFn: any): DictExpr<any, any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, this.key_type], undefined));
    const keyType = keyFnAst.type.output as EastType;

    const initFnAst = valueOrExprToAstTyped(initFn, FunctionType([keyType], undefined));
    const initType = initFnAst.type.output as EastType;

    const reduceFnAst = valueOrExprToAstTyped(reduceFn, FunctionType([initType, this.value_type, this.key_type], initType));

    return Expr.fromAst({
      ast_type: "Builtin",
      type: DictType(keyType as EastType, initType as EastType),
      location: get_location(),
      builtin: "DictGroupFold",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, keyType as EastType, initType as EastType],
      arguments: [this[AstSymbol], keyFnAst, initFnAst, reduceFnAst],
    }) as DictExpr<any, any>;
  }

  /**
   * Collect entries in each group into arrays.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values
   * @returns Dictionary mapping each key to an array of elements in that group
   *
   * @example
   * ```ts
   * new Dict({ a: 1n, b: 2n, c: 3n, d: 4n }).groupToArrays(($, v, k) => v.remainder(2n))
   * // Result: { 0n: [2n, 4n], 1n: [1n, 3n] }
   * ```
   */
  groupToArrays(keyFn: any, valueFn?: any): DictExpr<any, ArrayType<any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, v: any) => v), FunctionType([this.value_type, this.key_type], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);
    const valueFnExpr = Expr.fromAst(valueFnAst);
    const valueType = valueFnAst.type.output as EastType;
    return this.groupReduce(
      ((_$: any, value: any, key: any) => keyFnExpr(value, key)) as any,
      ((_$: any, _groupKey: any) => Expr.from([], ArrayType(valueType))) as any,
      (($: any, acc: any, value: any, key: any) => {
        const val = valueFnExpr(value, key);
        $(acc.pushLast(val));
        return acc;
      }) as any
    );
  }

  /**
   * Collect entries in each group into sets, ignoring duplicates.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values
   * @returns Dictionary mapping each key to a set of elements in that group
   *
   * @example
   * ```ts
   * new Dict({ a: 1n, b: 2n, c: 1n, d: 2n }).groupToSets(($, v, k) => v.remainder(2n))
   * // Result: { 0n: Set([2n]), 1n: Set([1n]) }
   * ```
   */
  groupToSets(keyFn: any, valueFn?: any): DictExpr<any, SetType<any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, v: any) => v), FunctionType([this.value_type, this.key_type], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);
    const valueFnExpr = Expr.fromAst(valueFnAst);
    const valueType = valueFnAst.type.output as EastType;
    return this.groupReduce(
      ((_$: any, value: any, key: any) => keyFnExpr(value, key)) as any,
      ((_$: any, _groupKey: any) => Expr.from(new Set<any>(), SetType(valueType))) as any,
      (($: any, acc: any, value: any, key: any) => {
        const val = valueFnExpr(value, key);
        $(acc.tryInsert(val));
        return acc;
      }) as any
    );
  }

  /**
   * Group entries into nested dictionaries.
   *
   * @param keyFn - Function that computes the outer grouping key
   * @param keyFn2 - Function that computes the inner dictionary key
   * @param valueFn - Optional projection function for inner dictionary values
   * @param combineFn - Optional function to resolve conflicts when the same inner key appears multiple times
   * @returns Dictionary-of-dictionaries mapping group keys to dictionaries
   *
   * @example
   * ```ts
   * // Without conflict handler - errors on duplicate keys
   * orders.groupToDicts(
   *   ($, v, k) => v.department,
   *   ($, v, k) => v.role
   * )
   * // Result: { "eng": { "dev": user1, "lead": user2 }, "sales": { "rep": user3 } }
   *
   * // With conflict handler - merges duplicate keys
   * orders.groupToDicts(
   *   ($, v, k) => v.customer,
   *   ($, v, k) => v.product,
   *   ($, v, k) => v.quantity,
   *   ($, a, b) => a.add(b)
   * )
   * // Sums quantities for same customer+product
   * ```
   */
  groupToDicts(keyFn: any, keyFn2: any, valueFn?: any, combineFn?: any): DictExpr<any, DictType<any, any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, this.key_type], undefined));
    const keyFn2Ast = valueOrExprToAstTyped(keyFn2, FunctionType([this.value_type, this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, v: any) => v), FunctionType([this.value_type, this.key_type], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);
    const keyFn2Expr = Expr.fromAst(keyFn2Ast);
    const valueFnExpr = Expr.fromAst(valueFnAst);
    const key2Type = keyFn2Ast.type.output as EastType;
    const valueType = valueFnAst.type.output as EastType;

    if (combineFn !== undefined) {
      // With conflict resolution - use tryGet + match to check existence, then insert or combine
      const combineFnAst = valueOrExprToAstTyped(combineFn, FunctionType([valueType, valueType], valueType));
      const combineFnExpr = Expr.fromAst(combineFnAst);

      return this.groupReduce(
        ((_$: any, value: any, key: any) => keyFnExpr(value, key)) as any,
        ((_$: any, _groupKey: any) => Expr.from(new Map(), DictType(key2Type, valueType))) as any,
        (($: any, dict: any, value: any, key: any) => {
          const innerKey = keyFn2Expr(value, key);
          const val = valueFnExpr(value, key);
          $.match(dict.tryGet(innerKey), {
            some: ($: any, existing: any) => {
              const combined = combineFnExpr(existing, val);
              $(dict.update(innerKey, combined));
            },
            none: ($: any) => {
              $(dict.insert(innerKey, val));
            }
          });
          return dict;
        }) as any
      );
    } else {
      // Without conflict resolution - use insert (errors on duplicate)
      return this.groupReduce(
        ((_$: any, value: any, key: any) => keyFnExpr(value, key)) as any,
        ((_$: any, _groupKey: any) => Expr.from(new Map(), DictType(key2Type, valueType))) as any,
        (($: any, dict: any, value: any, key: any) => {
          const innerKey = keyFn2Expr(value, key);
          const val = valueFnExpr(value, key);
          $(dict.insert(innerKey, val));
          return dict;
        }) as any
      );
    }
  }

  /**
   * Count the number of entries in each group.
   *
   * Groups entries by a key function and returns a dictionary mapping each unique key
   * to the count of entries in that group.
   *
   * @param keyFn - Function that computes the grouping key for each entry (defaults to identity on values)
   * @returns Dictionary mapping each unique key to the count of entries in that group
   *
   * @example
   * ```ts
   * // Count occurrences of each value
   * new Dict({ a: 1n, b: 2n, c: 1n }).groupSize()
   * // Result: { 1n: 2n, 2n: 1n }
   *
   * // Group by even/odd and count
   * new Dict({ a: 1n, b: 2n, c: 3n, d: 4n, e: 5n, f: 6n }).groupSize(($, v, k) => v.remainder(2n))
   * // Result: { 0n: 3n, 1n: 3n }
   * ```
   *
   * @see {@link groupToArrays} to collect entries instead of counting them.
   */
  groupSize<K2>(keyFn: Expr<FunctionType<[T, K], K2>>): DictExpr<K2, IntegerType>
  groupSize<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, IntegerType>
  groupSize(): DictExpr<T, IntegerType>
  groupSize(keyFn?: any): DictExpr<any, IntegerType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn ?? ((_$: any, v: any) => v), FunctionType([this.value_type, this.key_type], undefined));
    return this.toDict(
      ((_$: any, value: any, key: any) => Expr.fromAst(keyFnAst)(value, key)) as any,
      ((_$: any) => 1n) as any,
      ((_$: any, a: any, b: any) => a.add(b)) as any
    );
  }

  /**
   * Check if every entry in each group satisfies a predicate.
   *
   * @param keyFn - Function that computes the grouping key
   * @param predFn - Predicate function to test each entry
   * @returns Dictionary mapping each key to true if all entries in that group satisfy the predicate
   *
   * @example
   * ```ts
   * new Dict({ a: 1n, b: 2n, c: 3n, d: 4n, e: 5n, f: 6n }).groupEvery(
   *   ($, v, k) => v.remainder(2n),
   *   ($, v, k) => v.greater(0n)
   * )
   * // Result: { 0n: true, 1n: true }
   * ```
   */
  groupEvery<K2>(keyFn: Expr<FunctionType<[T, K], K2>>, predFn: SubtypeExprOrValue<FunctionType<[T, K], BooleanType>>): DictExpr<K2, BooleanType>
  groupEvery<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn, predFn: SubtypeExprOrValue<FunctionType<[T, K], BooleanType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, BooleanType>
  groupEvery(keyFn: any, predFn: any): DictExpr<any, BooleanType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, this.key_type], undefined));
    const predFnAst = valueOrExprToAstTyped(predFn, FunctionType([this.value_type, this.key_type], BooleanType));
    return this.groupReduce(
      ((_$: any, value: any, key: any) => Expr.fromAst(keyFnAst)(value, key)) as any,
      (() => true) as any,
      ((_$: any, acc: BooleanExpr, value: any, key: any) => {
        const pred = Expr.fromAst(predFnAst)(value, key) as BooleanExpr;
        return acc.and(() => pred);
      }) as any
    );
  }

  /**
   * Check if any entry in each group satisfies a predicate.
   *
   * @param keyFn - Function that computes the grouping key
   * @param predFn - Predicate function to test each entry
   * @returns Dictionary mapping each key to true if at least one entry in that group satisfies the predicate
   *
   * @example
   * ```ts
   * new Dict({ a: 1n, b: 2n, c: 3n, d: 4n }).groupSome(
   *   ($, v, k) => v.remainder(2n),
   *   ($, v, k) => v.greater(3n)
   * )
   * // Result: { 0n: true, 1n: false }
   * ```
   */
  groupSome<K2>(keyFn: Expr<FunctionType<[T, K], K2>>, predFn: SubtypeExprOrValue<FunctionType<[T, K], BooleanType>>): DictExpr<K2, BooleanType>
  groupSome<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn, predFn: SubtypeExprOrValue<FunctionType<[T, K], BooleanType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, BooleanType>
  groupSome(keyFn: any, predFn: any): DictExpr<any, BooleanType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, this.key_type], undefined));
    const predFnAst = valueOrExprToAstTyped(predFn, FunctionType([this.value_type, this.key_type], BooleanType));
    return this.groupReduce(
      ((_$: any, value: any, key: any) => Expr.fromAst(keyFnAst)(value, key)) as any,
      (() => false) as any,
      ((_$: any, acc: BooleanExpr, value: any, key: any) => {
        const pred = Expr.fromAst(predFnAst)(value, key) as BooleanExpr;
        return acc.or(() => pred);
      }) as any
    );
  }

  /**
   * Sum values in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values to sum
   * @returns Dictionary mapping each key to the sum of values in that group
   *
   * @example
   * ```ts
   * new Dict({ a: 1n, b: 2n, c: 3n, d: 4n }).groupSum(($, v, k) => v.remainder(2n))
   * // Result: { 0n: 6n, 1n: 4n }
   * ```
   */
  groupSum<K2>(keyFn: Expr<FunctionType<[T, K], K2>>, valueFn: Expr<FunctionType<[T, K], IntegerType>>): DictExpr<K2, IntegerType>
  groupSum<K2>(keyFn: Expr<FunctionType<[T, K], K2>>, valueFn: Expr<FunctionType<[T, K], FloatType>>): DictExpr<K2, FloatType>
  groupSum<K2, ValueFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[T, K], K2>>, valueFn: ValueFn): DictExpr<K2, TypeOf<ReturnType<ValueFn>>>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, K], IntegerType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, IntegerType>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, K], FloatType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<ValueFn>>>
  groupSum<K2>(keyFn: Expr<FunctionType<[T, K], K2>>): T extends IntegerType | FloatType ? DictExpr<K2, T> : never
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn): T extends IntegerType | FloatType ? DictExpr<TypeOf<ReturnType<KeyFn>>, T> : never
  groupSum(keyFn: any, valueFn?: any): DictExpr<any, any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, v: any) => v), FunctionType([this.value_type, this.key_type], undefined));
    const valueType = valueFnAst.type.output as EastType;
    const isInteger = isTypeEqual(valueType, IntegerType);
    const isFloat = isTypeEqual(valueType, FloatType);
    if (!isInteger && !isFloat) {
      throw new Error(`Can only perform groupSum on Integer or Float values, got ${printType(valueType)}`);
    }
    return this.toDict(
      ((_$: any, value: any, key: any) => Expr.fromAst(keyFnAst)(value, key)) as any,
      ((_$: any, value: any, key: any) => Expr.fromAst(valueFnAst)(value, key)) as any,
      ((_$: any, a: any, b: any) => a.add(b)) as any
    );
  }

  /**
   * Compute the mean of values in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values
   * @returns Dictionary mapping each key to the mean of values in that group
   *
   * @example
   * ```ts
   * new Dict({ a: 1n, b: 2n, c: 3n, d: 4n }).groupMean(($, v, k) => v.remainder(2n))
   * // Result: { 0n: 3.0, 1n: 2.0 }
   * ```
   */
  groupMean<K2>(keyFn: Expr<FunctionType<[T, K], K2>>, valueFn: Expr<FunctionType<[T, K], IntegerType | FloatType>>): DictExpr<K2, FloatType>
  groupMean<K2, ValueFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[T, K], K2>>, valueFn: ValueFn): DictExpr<K2, FloatType>
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, K], IntegerType | FloatType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupMean<K2>(keyFn: Expr<FunctionType<[T, K], K2>>): T extends IntegerType | FloatType ? DictExpr<K2, FloatType> : never
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(keyFn: KeyFn): T extends IntegerType | FloatType ? DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType> : never
  groupMean(keyFn: any, valueFn?: any): DictExpr<any, FloatType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, v: any) => v), FunctionType([this.value_type, this.key_type], undefined));
    const valueType = valueFnAst.type.output as EastType;
    const isInteger = isTypeEqual(valueType, IntegerType);
    const isFloat = isTypeEqual(valueType, FloatType);
    if (!isInteger && !isFloat) {
      throw new Error(`Can only perform groupMean on Integer or Float values, got ${printType(valueType)}`);
    }
    return this.toDict(
      ((_$: any, value: any, key: any) => Expr.fromAst(keyFnAst)(value, key)) as any,
      ((_$: any, value: any, key: any) => {
        const val = Expr.fromAst(valueFnAst)(value, key);
        return { sum: isInteger ? (val as IntegerExpr).toFloat() : val, count: 1n };
      }) as any,
      ((_$: any, a: any, b: any) => ({ sum: a.sum.add(b.sum), count: a.count.add(b.count) })) as any
    ).map(((_$: any, v: any) => v.sum.divide(v.count.toFloat())) as any) as any;
  }

  /**
   * Reduces the dictionary to a single value using an accumulator function.
   *
   * @param fn - Function accepting (accumulator, value, key) and returning the new accumulator value
   * @param init - Initial value for the accumulator
   * @returns The final accumulated value
   *
   * @see {@link mapReduce} for a version that projects values before combining
   * @see {@link sum} and {@link mean} for common numeric reductions
   *
   * @example
   * ```ts
   * const sumValues = East.function([DictType(StringType, IntegerType)], IntegerType, ($, dict) => {
   *   $.return(dict.reduce(($, acc, value, key) => acc.add(value), 0n));
   * });
   * const compiled = East.compile(sumValues.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n], ["c", 3n]]);
   * compiled(dict);  // 6n
   * ```
   *
   * @example
   * ```ts
   * // Concatenate keys
   * const concatKeys = East.function([DictType(StringType, IntegerType)], StringType, ($, dict) => {
   *   $.return(dict.reduce(($, acc, value, key) => acc.concat(",").concat(key), ""));
   * });
   * const compiled = East.compile(concatKeys.toIR(), []);
   * compiled(dict);  // ",a,b,c"
   * ```
   */
  reduce<T2>(fn: SubtypeExprOrValue<FunctionType<[previous: TypeOf<NoInfer<T2>>, value: T, key: K], TypeOf<NoInfer<T2>>>>, init: T2): ExprType<TypeOf<T2>> {
    const initAst = valueOrExprToAst(init);
    const returnType = initAst.type;

    const fnAst = valueOrExprToAstTyped(fn, FunctionType([returnType, this.value_type, this.key_type], returnType));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: returnType as EastType,
      location: get_location(),
      builtin: "DictReduce",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, returnType as EastType],
      arguments: [this[AstSymbol], fnAst, initAst],
    }) as ExprType<TypeOf<T2>>;
  }

  /**
   * Reduce dictionary to single value using projection and accumulator functions.
   *
   * The first entry of the dictionary is used as initial value and reduction starts from the second entry.
   * If the dictionary is empty, an error is thrown.
   *
   * @param mapFn - Function that projects each value and key to a result
   * @param combineFn - Function that combines two projected values
   * @returns The final reduced value
   *
   * @example
   * ```ts
   * const d = new Dict({ a: 1n, b: 2n, c: 3n })
   * // Sum of squares
   * const result = d.mapReduce(
   *   ($, v) => v.multiply(v),
   *   ($, a, b) => a.add(b)
   * )
   * // Result: 14n (1 + 4 + 9)
   * ```
   *
   * @see {@link reduce} for a version with an initial value
   */
  mapReduce<T2>(mapFn: Expr<FunctionType<[value: T, key: K], T2>>, combineFn: SubtypeExprOrValue<FunctionType<[previous: NoInfer<T2>, value: NoInfer<T2>], NoInfer<T2>>>): ExprType<T2>
  mapReduce<F extends ($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any>(mapFn: F, combineFn: SubtypeExprOrValue<FunctionType<[previous: NoInfer<TypeOf<ReturnType<F>>>, value: NoInfer<TypeOf<ReturnType<F>>>], NoInfer<TypeOf<ReturnType<F>>>>>): ExprType<TypeOf<ReturnType<F>>>
  mapReduce<T2>(mapFn: any, combineFn: any): Expr {
    const mapAst = valueOrExprToAstTyped(mapFn, FunctionType([this.value_type, this.key_type], undefined));
    const mapType = mapAst.type.output as EastType;
    const combineAst = valueOrExprToAstTyped(combineFn, FunctionType([mapType, mapType], mapType));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: mapType as EastType,
      location: get_location(),
      builtin: "DictMapReduce",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, mapType],
      arguments: [this[AstSymbol], mapAst, combineAst],
    }) as ExprType<T2>;
  }

  /**
   * Find the first entry where the mapping function returns `some(value)`, and return that value wrapped in an Option.
   *
   * The supplied function must return an Option type. This method stops iterating as soon as the first `some` value is found,
   * making it efficient for early termination searches.
   *
   * Returns `none` if no entry produces a `some` value, or `some(value)` with the first mapped result.
   *
   * @param fn - Function that maps each value and key to an Option type
   * @returns Option containing the first successfully mapped value, or `none` if none found
   *
   * @example
   * ```ts
   * const d = new Dict({ a: 1n, b: 2n, c: 3n, d: 4n })
   * // Find the first even value and return its square
   * const result = d.firstMap(($, v, k) =>
   *   v.remainder(2n).equal(0n).ifElse(
   *     () => East.some(v.multiply(v)),
   *     () => East.none
   *   )
   * )
   * // Result: some(4n)
   * ```
   *
   * @see {@link filterMap} to collect all mapped values that return `some` (scans entire dictionary).
   */
  firstMap<T2>(fn: Expr<FunctionType<[T, K], VariantType<{ none: NullType, some: T2 }>>>): Expr<VariantType<{ none: NullType, some: T2 }>>;
  firstMap<F extends (($: BlockBuilder<NeverType>, value: ExprType<T>, key: ExprType<K>) => any)>(fn: F): ExprType<TypeOf<ReturnType<F>>>;
  firstMap(fn: any): Expr {
    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, this.key_type], undefined));

    const returnType = fnAst.type.output as EastType;

    if (returnType.type !== "Variant") {
      throw new Error(`Expected Function to return an Option type, got ${printType(returnType)}`);
    }
    if (!Object.keys(returnType.cases).every(k => k === "none" || k === "some")) {
      throw new Error(`Expected Function to return an Option type, got ${printType(returnType)}`);
    }
    const someType = returnType.cases["some"] ?? NeverType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: returnType as EastType,
      location: get_location(),
      builtin: "DictFirstMap",
      type_parameters: [this.key_type as EastType, this.value_type as EastType, someType as EastType],
      arguments: [this[AstSymbol], fnAst],
    });
  }

  // Common reducers are provided, based on reduce

    /**
     * Returns true if every value in the dictionary is true, or false otherwise.
     *
     * This method short-circuits on the first false value. Note that empty dictionaries always return true.
     * For dictionaries whose values are not Boolean, a mapping function must be provided.
     *
     * @param fn - Optional function to map each (value, key) pair to a boolean
     * @returns A BooleanExpr that is true if all values satisfy the condition
     *
     * @see {@link some} to check if at least one element is true
     * @see {@link groupEvery} to check every element within groups
     *
     * @example
     * ```ts
     * const allPositive = East.function([DictType(StringType, IntegerType)], BooleanType, ($, dict) => {
     *   $.return(dict.every(($, value, key) => value.greater(0n)));
     * });
     * const compiled = East.compile(allPositive.toIR(), []);
     * const dict1 = new Map([["a", 1n], ["b", 2n], ["c", 3n]]);
     * compiled(dict1);  // true
     * const dict2 = new Map([["a", 1n], ["b", -2n], ["c", 3n]]);
     * compiled(dict2);  // false (short-circuits at "b")
     * compiled(new Map());  // true (empty dictionary)
     * ```
     */
    every(fn?: SubtypeExprOrValue<FunctionType<[T, K], BooleanType>>): BooleanExpr {
      if (fn === undefined) {
        if (!isTypeEqual(this.value_type as EastType, BooleanType)) {
          throw new Error(`Can only perform every on dict of booleans, got ${printType(this.value_type as EastType)}`);
        }
        // Short-circuit on first false value - use explicit function AST to avoid type inference issues
        const optionType = VariantType({ none: NullType, some: NullType });
        const valueParam: AST = {
          ast_type: "Variable",
          type: this.value_type as EastType,
          location: get_location(),
          mutable: false,
        };
        const keyParam: AST = {
          ast_type: "Variable",
          type: this.key_type as EastType,
          location: get_location(),
          mutable: false,
        };
        // Check if boolean value is NOT true, then return some(null) to stop, otherwise return none to continue
        const notCondition: AST = {
          ast_type: "Builtin",
          type: BooleanType,
          location: get_location(),
          builtin: "BooleanNot",
          type_parameters: [],
          arguments: [valueParam]
        };
        const checkFnAst: AST = {
          ast_type: "Function",
          type: FunctionType([this.value_type as EastType, this.key_type as EastType], optionType) as any,
          location: get_location(),
          parameters: [valueParam as any, keyParam as any],
          body: {
            ast_type: "IfElse",
            type: optionType as any,
            location: get_location(),
            ifs: [{
              predicate: notCondition,
              body: { ast_type: "Variant", type: optionType as any, location: get_location(), case: "some", value: { ast_type: "Value", type: NullType, location: get_location(), value: null } }
            }],
            else_body: { ast_type: "Variant", type: optionType as any, location: get_location(), case: "none", value: { ast_type: "Value", type: NullType, location: get_location(), value: null } }
          }
        };
        const result: any = Expr.fromAst({
          ast_type: "Builtin",
          type: optionType as any,
          location: get_location(),
          builtin: "DictFirstMap",
          type_parameters: [this.key_type as EastType, this.value_type as EastType, NullType],
          arguments: [this[AstSymbol], checkFnAst],
        });
        return Expr.match(result, { some: () => false, none: () => true }) as BooleanExpr;
      }

      const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, this.key_type], BooleanType));

      // Short-circuit on first false value
      const result = this.firstMap(($, value, key) => {
        const result = Expr.fromAst(fnAst)(value as any, key as any) as BooleanExpr;
        return result.not().ifElse(() => some(null), () => none);
      });
      return Expr.match(result, { some: () => false, none: () => true });
    }
  
    /**
     * Returns true if at least one value in the dictionary is true, or false otherwise.
     *
     * This method short-circuits on the first true value. Note that empty dictionaries always return false.
     * For dictionaries whose values are not Boolean, a mapping function must be provided.
     *
     * @param fn - Optional function to map each (value, key) pair to a boolean
     * @returns A BooleanExpr that is true if any value satisfies the condition
     *
     * @see {@link every} to check if all elements are true
     * @see {@link groupSome} to check if some element exists within groups
     *
     * @example
     * ```ts
     * const hasNegative = East.function([DictType(StringType, IntegerType)], BooleanType, ($, dict) => {
     *   $.return(dict.some(($, value, key) => value.less(0n)));
     * });
     * const compiled = East.compile(hasNegative.toIR(), []);
     * const dict1 = new Map([["a", 1n], ["b", 2n], ["c", 3n]]);
     * compiled(dict1);  // false
     * const dict2 = new Map([["a", 1n], ["b", -2n], ["c", 3n]]);
     * compiled(dict2);  // true (short-circuits at "b")
     * compiled(new Map());  // false (empty dictionary)
     * ```
     */
    some(fn?: SubtypeExprOrValue<FunctionType<[T, K], BooleanType>>): BooleanExpr {
      if (fn === undefined) {
        if (!isTypeEqual(this.value_type as EastType, BooleanType)) {
          throw new Error(`Can only perform some on dict of booleans, got ${printType(this.value_type as EastType)}`);
        }
        // Short-circuit on first true value - use explicit function AST to avoid type inference issues
        const optionType = VariantType({ none: NullType, some: NullType });
        const valueParam: AST = {
          ast_type: "Variable",
          type: this.value_type as EastType,
          location: get_location(),
          mutable: false,
        };
        const keyParam: AST = {
          ast_type: "Variable",
          type: this.key_type as EastType,
          location: get_location(),
          mutable: false,
        };
        // Check if boolean value is true, then return some(null) to stop, otherwise return none to continue
        const checkFnAst: AST = {
          ast_type: "Function",
          type: FunctionType([this.value_type as EastType, this.key_type as EastType], optionType) as any,
          location: get_location(),
          parameters: [valueParam as any, keyParam as any],
          body: {
            ast_type: "IfElse",
            type: optionType as any,
            location: get_location(),
            ifs: [{
              predicate: valueParam,
              body: { ast_type: "Variant", type: optionType as any, location: get_location(), case: "some", value: { ast_type: "Value", type: NullType, location: get_location(), value: null } }
            }],
            else_body: { ast_type: "Variant", type: optionType as any, location: get_location(), case: "none", value: { ast_type: "Value", type: NullType, location: get_location(), value: null } }
          }
        };
        const result: any = Expr.fromAst({
          ast_type: "Builtin",
          type: optionType as any,
          location: get_location(),
          builtin: "DictFirstMap",
          type_parameters: [this.key_type as EastType, this.value_type as EastType, NullType],
          arguments: [this[AstSymbol], checkFnAst],
        });
        return Expr.match(result, { some: () => true, none: () => false }) as BooleanExpr;
      }

      const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, this.key_type], BooleanType));

      // Short-circuit on first true value
      const result = this.firstMap(($, value, key) => {
        const result = Expr.fromAst(fnAst)(value as any, key as any) as BooleanExpr;
        return result.ifElse(() => some(null), () => none);
      });
      return Expr.match(result, { some: () => true, none: () => false });
    }
    
    /**
     * Sums all values in the dictionary.
     *
     * For dictionaries whose values are not Integer or Float, a mapping function must be provided.
     *
     * @param fn - Optional function to map each (value, key) pair to a numeric value
     * @returns An IntegerExpr or FloatExpr containing the sum
     *
     * @see {@link mean} to calculate the average
     * @see {@link groupSum} to sum values within groups
     * @see {@link reduce} for custom aggregations
     *
     * @example
     * ```ts
     * const sumValues = East.function([DictType(StringType, IntegerType)], IntegerType, ($, dict) => {
     *   $.return(dict.sum());
     * });
     * const compiled = East.compile(sumValues.toIR(), []);
     * const dict = new Map([["a", 1n], ["b", 2n], ["c", 3n]]);
     * compiled(dict);  // 6n
     * ```
     *
     * @example
     * ```ts
     * // With mapping function
     * const sumLengths = East.function([DictType(StringType, StringType)], IntegerType, ($, dict) => {
     *   $.return(dict.sum(($, value, key) => value.size()));
     * });
     * const compiled = East.compile(sumLengths.toIR(), []);
     * const dict2 = new Map([["a", "hello"], ["b", "world"]]);
     * compiled(dict2);  // 10n (5 + 5)
     * ```
     */
    sum(fn: Expr<FunctionType<[T, K], IntegerType>>): IntegerExpr
    sum(fn: Expr<FunctionType<[T, K], FloatType>>): FloatExpr
    sum<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(fn: F): TypeOf<ReturnType<F>> extends IntegerType ? IntegerExpr : TypeOf<ReturnType<F>> extends FloatType ? FloatExpr : never
    sum(): T extends IntegerType | FloatType ? ExprType<T> : never
    sum(fn?: any): Expr<IntegerType | FloatType> {
      if (fn === undefined) {
        if (!(isTypeEqual(this.value_type as EastType, IntegerType) || isTypeEqual(this.value_type as EastType, FloatType))) {
          throw new Error(`Can only perform sum on dict of numbers (Integer or Float), got ${printType(this.value_type as EastType)}`);
        }
        const zero = isTypeEqual(this.value_type as EastType, IntegerType) ? 0n : 0.0;
        return this.reduce(($, previous, value) => previous.add(value as any) as any, zero) as any;
      } else {
        const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, this.key_type], undefined));
        const returnType = fnAst.type.output as EastType;
        if (!(isTypeEqual(returnType, IntegerType) || isTypeEqual(returnType, FloatType))) {
          throw new Error(`Can only perform sum on dict of numbers (Integer or Float), got ${printType(returnType)}`);
        }
        const zero = isTypeEqual(returnType, IntegerType) ? 0n : 0.0;
        return this.reduce(($, previous, value, key) => previous.add(Expr.fromAst(fnAst)(value as any, key as any) as any) as any, zero) as any;
      }
    }

  /**
   * Calculates the mean (average) of all values in the dictionary.
   *
   * Returns NaN for empty dictionaries.
   * For dictionaries whose values are not Integer or Float, a mapping function must be provided.
   *
   * @param fn - Optional function to map each (value, key) pair to a numeric value
   * @returns A FloatExpr containing the mean value
   *
   * @see {@link sum} to calculate the sum
   * @see {@link groupMean} to calculate mean values within groups
   *
   * @example
   * ```ts
   * const avgValue = East.function([DictType(StringType, IntegerType)], FloatType, ($, dict) => {
   *   $.return(dict.mean());
   * });
   * const compiled = East.compile(avgValue.toIR(), []);
   * const dict = new Map([["a", 1n], ["b", 2n], ["c", 3n], ["d", 4n]]);
   * compiled(dict);  // 2.5
   * ```
   *
   * @example
   * ```ts
   * // With mapping function
   * const avgLength = East.function([DictType(StringType, StringType)], FloatType, ($, dict) => {
   *   $.return(dict.mean(($, value, key) => value.size()));
   * });
   * const compiled = East.compile(avgLength.toIR(), []);
   * const dict2 = new Map([["a", "hi"], ["b", "hello"], ["c", "hey"]]);
   * compiled(dict2);  // 3.6666... (average of 2, 5, 3)
   * ```
   */
  mean(fn: Expr<FunctionType<[T, K], IntegerType>>): FloatExpr
  mean(fn: Expr<FunctionType<[T, K], FloatType>>): FloatExpr
  mean<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<K>) => any)>(fn: F): TypeOf<ReturnType<F>> extends IntegerType | FloatType ? FloatExpr : never
  mean(): T extends IntegerType | FloatType ? FloatExpr : never
  mean(fn?: any): Expr<FloatType> {
    if (fn === undefined) {
      if (isTypeEqual(this.value_type as EastType, IntegerType)) {
        return this.reduce(($, previous, value) => previous.add((value as IntegerExpr).toFloat()), 0.0).divide(this.size().toFloat());
      } else if (isTypeEqual(this.value_type as EastType, FloatType)) {
        return this.reduce(($, previous, value) => previous.add(value as FloatExpr), 0.0).divide(this.size().toFloat());
      } else {
        throw new Error(`Can only perform mean on dict of numbers (Integer or Float), got ${printType(this.value_type as EastType)}`);
      }
    } else {
      const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, this.key_type], undefined));
      const returnType = fnAst.type.output as EastType;
      if (isTypeEqual(returnType, IntegerType)) {
        return this.reduce(($, previous: any, value, key) => previous.add((Expr.fromAst(fnAst)(value as any, key as any) as IntegerExpr).toFloat()) as FloatExpr, 0.0).divide(this.size().toFloat());
      } else if (isTypeEqual(returnType, FloatType)) {
        return this.reduce(($, previous, value, key) => previous.add(Expr.fromAst(fnAst)(value as any, key as any) as FloatExpr), 0.0).divide(this.size().toFloat());
      } else {
        throw new Error(`Can only perform mean on dict of numbers (Integer or Float), got ${printType(returnType)}`);
      }
    }
  }

  /**
   * Checks if this dictionary equals another dictionary (same key-value pairs).
   *
   * @param other - The dictionary to compare against
   * @returns A BooleanExpr that is true if the dictionaries are equal
   *
   * @example
   * ```ts
   * const isEqual = East.function([DictType(StringType, IntegerType), DictType(StringType, IntegerType)], BooleanType, ($, a, b) => {
   *   $.return(a.equals(b));
   * });
   * const compiled = East.compile(isEqual.toIR(), []);
   * compiled(new Map([["a", 1n], ["b", 2n]]), new Map([["a", 1n], ["b", 2n]]));  // true
   * compiled(new Map([["a", 1n]]), new Map([["a", 1n], ["b", 2n]]));            // false
   * ```
   */
  equals(other: DictExpr<K, T> | Map<SubtypeExprOrValue<K>, SubtypeExprOrValue<T>>): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this dictionary does not equal another dictionary.
   *
   * @param other - The dictionary to compare against
   * @returns A BooleanExpr that is true if the dictionaries are not equal
   *
   * @example
   * ```ts
   * const isNotEqual = East.function([DictType(StringType, IntegerType), DictType(StringType, IntegerType)], BooleanType, ($, a, b) => {
   *   $.return(a.notEquals(b));
   * });
   * const compiled = East.compile(isNotEqual.toIR(), []);
   * compiled(new Map([["a", 1n]]), new Map([["a", 1n], ["b", 2n]]));            // true
   * compiled(new Map([["a", 1n], ["b", 2n]]), new Map([["a", 1n], ["b", 2n]]));  // false
   * ```
   */
  notEquals(other: DictExpr<K, T> | Map<SubtypeExprOrValue<K>, SubtypeExprOrValue<T>>): BooleanExpr {
    return notEqual(this, other);
  }

  // ============================================================================
  // Aliases for comparison operations
  // ============================================================================

  /** Alias for {@link equals} */
  eq = this.equals;
  /** Alias for {@link equals} */
  equal = this.equals;

  /** Alias for {@link notEquals} */
  ne = this.notEquals;
  /** Alias for {@link notEquals} */
  notEqual = this.notEquals;
}