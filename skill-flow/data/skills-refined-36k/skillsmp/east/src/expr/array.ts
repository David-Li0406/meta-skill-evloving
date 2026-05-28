/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { ArrayType, BooleanType, FunctionType, IntegerType, NullType, StringType, type EastType, isSubtype, isTypeEqual, printType, NeverType, OptionType, isDataType, StructType, VariantType, SetType, FloatType, DictType, type ValueTypeOf, type SubType } from "../types.js";
import { valueOrExprToAst, valueOrExprToAstTyped } from "./ast.js";
import type { IntegerExpr } from "./integer.js";
import type { NullExpr } from "./null.js";
import { AstSymbol, Expr, FactorySymbol, TypeSymbol, type ToExpr } from "./expr.js";
import type { StringExpr } from "./string.js";
import type { SubtypeExprOrValue, ExprType, TypeOf } from "./types.js";
import type { BlockBuilder } from "./block.js";
import { equal, notEqual } from "./block.js";
import type { BooleanExpr } from "./boolean.js";
import type { SetExpr } from "./set.js";
import type { FloatExpr } from "./float.js";
import type { DictExpr } from "./dict.js";
import type { CallableFunctionExpr } from "./function.js";
import { none, some } from "../containers/variant.js";
import { CsvSerializeConfigType, csvSerializeOptionsToValue, type CsvSerializeOptions } from "../serialization/csv.js";
import type { BlobExpr } from "./blob.js";
import { BlobType } from "../types.js";

/**
 * Expression representing mutable array values and operations.
 *
 * ArrayExpr provides comprehensive methods for array manipulation including element access,
 * mutation (push/pop/sort/reverse), transformation (map/filter/reduce), searching, slicing,
 * grouping, and aggregation. Arrays are mutable, ordered collections with zero-based indexing.
 *
 * @example
 * ```ts
 * // Array manipulation
 * const processArray = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
 *   $(arr.pushLast(10n));  // Mutate: add element
 *   const doubled = arr.map(($, x, i) => x.multiply(2n));
 *   $.return(doubled);
 * });
 *
 * // Filtering and mapping
 * const filterMap = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
 *   const evens = arr.filter(($, x, i) => x.remainder(2n).equal(0n));
 *   $.return(evens.map(($, x, i) => x.add(1n)));
 * });
 *
 * // Aggregation
 * const sumArray = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
 *   $.return(arr.reduce(($, acc, x, i) => acc.add(x), 0n));
 * });
 * ```
 */
export class ArrayExpr<T extends any> extends Expr<ArrayType<T>> {
  constructor(private value_type: T, ast: AST, createExpr: ToExpr) {
    super(ast.type as ArrayType<T>, ast, createExpr);
  }

  /**
   * Returns the size (length) of the array.
   *
   * @returns An IntegerExpr representing the number of elements
   *
   * @example
   * ```ts
   * const getSize = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
   *   $.return(arr.size());
   * });
   * const compiled = East.compile(getSize.toIR(), []);
   * compiled([1n, 2n, 3n]);  // 3n
   * compiled([]);            // 0n
   * ```
   */
  size(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "ArraySize",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  
  /**
   * Returns the length of the array (an alias for size).
   *
   * @returns An IntegerExpr representing the number of elements
   *
   * @example
   * ```ts
   * const getLength = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
   *   $.return(arr.length());
   * });
   * const compiled = East.compile(getLength.toIR(), []);
   * compiled([1n, 2n, 3n]);  // 3n
   * compiled([]);            // 0n
   * ```
   */
  length(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "ArraySize",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Checks if an element exists at the specified index (i.e., if the index is in bounds).
   *
   * @param key - The zero-based index to check
   * @returns A BooleanExpr that is true if the index is valid (0 <= index < size)
   *
   * @example
   * ```ts
   * const hasElement = East.function([ArrayType(IntegerType), IntegerType], BooleanType, ($, arr, index) => {
   *   $.return(arr.has(index));
   * });
   * const compiled = East.compile(hasElement.toIR(), []);
   * compiled([10n, 20n, 30n], 1n);   // true
   * compiled([10n, 20n, 30n], 5n);   // false
   * compiled([10n, 20n, 30n], -1n);  // false
   * ```
   */
  has(key: Expr<IntegerType> | bigint, ): ExprType<BooleanType> {
    const keyAst = valueOrExprToAstTyped(key, IntegerType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "ArrayHas",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as ExprType<BooleanType>;
  }

  /**
   * Gets the element at the specified index.
   *
   * @param key - The zero-based index
   * @param defaultFn - Optional function to provide a default value for out-of-bounds indices
   * @returns An expression of the array's element type
   *
   * @throws East runtime error if index is out of bounds and no defaultFn is provided
   *
   * @example
   * ```ts
   * const getElement = East.function([ArrayType(IntegerType), IntegerType], IntegerType, ($, arr, index) => {
   *   $.return(arr.get(index));
   * });
   * const compiled = East.compile(getElement.toIR(), []);
   * compiled([10n, 20n, 30n], 1n);  // 20n
   * // compiled([10n, 20n, 30n], 5n) would throw error
   *
   * // With default value
   * const getOrDefault = East.function([ArrayType(IntegerType), IntegerType], IntegerType, ($, arr, index) => {
   *   $.return(arr.get(index, ($, i) => -1n));
   * });
   * compiled = East.compile(getOrDefault.toIR(), []);
   * compiled([10n, 20n, 30n], 5n);  // -1n (out of bounds)
   * ```
   */
  get(key: Expr<IntegerType> | bigint, defaultFn?: SubtypeExprOrValue<FunctionType<[IntegerType], T>>): ExprType<T> {
    const keyAst = valueOrExprToAstTyped(key, IntegerType);

    if (defaultFn !== undefined) {
      const defaultFnAst = valueOrExprToAstTyped(defaultFn, FunctionType([IntegerType], this.value_type as EastType));
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: this.value_type as EastType,
        location: get_location(),
        builtin: "ArrayGetOrDefault",
        type_parameters: [this.value_type as EastType],
        arguments: [this[AstSymbol], keyAst, defaultFnAst],
      }) as ExprType<T>;
    } else {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: this.value_type as EastType,
        location: get_location(),
        builtin: "ArrayGet",
        type_parameters: [this.value_type as EastType],
        arguments: [this[AstSymbol], keyAst],
      }) as ExprType<T>;
    }
  }

  
  /**
   * Gets the element at the specified index (alias for get).
   *
   * @param key - The zero-based index
   * @param defaultFn - Optional function to provide a default value for out-of-bounds indices
   * @returns An expression of the array's element type
   *
   * @throws East runtime error if index is out of bounds and no defaultFn is provided
   *
   * @example
   * ```ts
   * const getElement = East.function([ArrayType(IntegerType), IntegerType], IntegerType, ($, arr, index) => {
   *   $.return(arr.get(index));
   * });
   * const compiled = East.compile(getElement.toIR(), []);
   * compiled([10n, 20n, 30n], 1n);  // 20n
   * // compiled([10n, 20n, 30n], 5n) would throw error
   *
   * // With default value
   * const getOrDefault = East.function([ArrayType(IntegerType), IntegerType], IntegerType, ($, arr, index) => {
   *   $.return(arr.get(index, ($, i) => -1n));
   * });
   * compiled = East.compile(getOrDefault.toIR(), []);
   * compiled([10n, 20n, 30n], 5n);  // -1n (out of bounds)
   * ```
   */
  at(key: Expr<IntegerType> | bigint, defaultFn?: SubtypeExprOrValue<FunctionType<[IntegerType], T>>): ExprType<T> {
    const keyAst = valueOrExprToAstTyped(key, IntegerType);

    if (defaultFn !== undefined) {
      const defaultFnAst = valueOrExprToAstTyped(defaultFn, FunctionType([IntegerType], this.value_type as EastType));
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: this.value_type as EastType,
        location: get_location(),
        builtin: "ArrayGetOrDefault",
        type_parameters: [this.value_type as EastType],
        arguments: [this[AstSymbol], keyAst, defaultFnAst],
      }) as ExprType<T>;
    } else {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: this.value_type as EastType,
        location: get_location(),
        builtin: "ArrayGet",
        type_parameters: [this.value_type as EastType],
        arguments: [this[AstSymbol], keyAst],
      }) as ExprType<T>;
    }
  }


  /**
   * Safely gets the element at the specified index, returning an Option variant.
   *
   * @param key - The zero-based index
   * @returns An OptionType expression containing .some(value) if in bounds, or .none if out of bounds
   *
   * @example
   * ```ts
   * const tryGetElement = East.function([ArrayType(IntegerType), IntegerType], OptionType(IntegerType), ($, arr, index) => {
   *   $.return(arr.tryGet(index));
   * });
   * const compiled = East.compile(tryGetElement.toIR(), []);
   * compiled([10n, 20n, 30n], 1n);  // {_tag: "some", some: 20n}
   * compiled([10n, 20n, 30n], 5n);  // {_tag: "none", none: null}
   * ```
   */
  tryGet(key: Expr<IntegerType> | bigint): ExprType<OptionType<T>> {
    const keyAst = valueOrExprToAstTyped(key, IntegerType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: OptionType(this.value_type),
      location: get_location(),
      builtin: "ArrayTryGet",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as ExprType<OptionType<T>>;
  }

  /**
   * Updates (replaces) the element at the specified index (mutates the array).
   *
   * @param key - The zero-based index to update
   * @param value - The new value to set at that index
   * @returns NullExpr (operation performed for side effect)
   *
   * @throws East runtime error if index is out of bounds
   *
   * @example
   * ```ts
   * const updateElement = East.function([ArrayType(IntegerType), IntegerType, IntegerType], ArrayType(IntegerType), ($, arr, index, value) => {
   *   $(arr.update(index, value));  // Mutate the array
   *   $.return(arr);
   * });
   * const compiled = East.compile(updateElement.toIR(), []);
   * compiled([10n, 20n, 30n], 1n, 99n);  // [10n, 99n, 30n]
   * ```
   */
  update(key: Expr<IntegerType> | bigint, value: SubtypeExprOrValue<T>): NullExpr {
    const keyAst = valueOrExprToAstTyped(key, IntegerType);
    const valueAst = valueOrExprToAstTyped(value, this.value_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayUpdate",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], keyAst, valueAst],
    }) as NullExpr;
  }

  /** Modify an array element at index by merging it with a new value using a function accepting the new and current value. An error is thrown on missing key (index out of bounds).
   * 
   * This is useful for patterns where you want to update an element based on its current value, e.g. incrementing a number, appending to a string, updating fields in a struct, or pushing to an array.
   * 
   * @see {@link update} for simply replacing the value.
   */
  merge<T2>(key: Expr<IntegerType> | bigint, value: Expr<T2>, updateFn: SubtypeExprOrValue<FunctionType<[T, NoInfer<T2>, IntegerType], T>>): ExprType<NullType> {
    const location = get_location();
    const keyAst = valueOrExprToAstTyped(key, IntegerType);
    const value2Type = value[TypeSymbol];

    const updateFnExpr = Expr.from(updateFn as any, FunctionType([value2Type, this.value_type, IntegerType], this.value_type));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location,
      builtin: "ArrayMerge",
      type_parameters: [this.value_type as EastType, value2Type as EastType],
      arguments: [this[AstSymbol], keyAst, value[AstSymbol], updateFnExpr[AstSymbol]],
    }) as ExprType<NullType>;
  }

  /**
   * Adds an element to the end of the array (mutates the array).
   *
   * @param value - The value to append
   * @returns NullExpr (operation performed for side effect)
   *
   * @example
   * ```ts
   * const appendValue = East.function([ArrayType(IntegerType), IntegerType], ArrayType(IntegerType), ($, arr, value) => {
   *   $(arr.pushLast(value));  // Mutate the array
   *   $.return(arr);
   * });
   * const compiled = East.compile(appendValue.toIR(), []);
   * compiled([1n, 2n, 3n], 4n);  // [1n, 2n, 3n, 4n]
   * ```
   */
  pushLast(value: SubtypeExprOrValue<T>): NullExpr {
    const valueAst = valueOrExprToAstTyped(value, this.value_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayPushLast",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], valueAst],
    }) as NullExpr;
  }

  /**
   * Removes and returns the last element from the array (mutates the array).
   *
   * @returns An expression of the array's element type containing the removed value
   *
   * @throws East runtime error if the array is empty
   *
   * @example
   * ```ts
   * const removeLastValue = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
   *   $.return(arr.popLast());
   * });
   * const compiled = East.compile(removeLastValue.toIR(), []);
   * compiled([1n, 2n, 3n]);  // 3n (arr is now [1n, 2n])
   * ```
   */
  popLast(): ExprType<T> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this.value_type as EastType,
      location: get_location(),
      builtin: "ArrayPopLast",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as ExprType<T>;
  }

  /**
   * Adds an element to the beginning of the array (mutates the array).
   *
   * @param value - The value to prepend
   * @returns NullExpr (operation performed for side effect)
   *
   * @example
   * ```ts
   * const prependValue = East.function([ArrayType(IntegerType), IntegerType], ArrayType(IntegerType), ($, arr, value) => {
   *   $(arr.pushFirst(value));  // Mutate the array
   *   $.return(arr);
   * });
   * const compiled = East.compile(prependValue.toIR(), []);
   * compiled([1n, 2n, 3n], 0n);  // [0n, 1n, 2n, 3n]
   * ```
   */
  pushFirst(value: SubtypeExprOrValue<T>): NullExpr {
    const valueAst = valueOrExprToAstTyped(value, this.value_type as EastType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayPushFirst",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], valueAst],
    }) as NullExpr;
  }

  /**
   * Removes and returns the first element from the array (mutates the array).
   *
   * @returns An expression of the array's element type containing the removed value
   *
   * @throws East runtime error if the array is empty
   *
   * @example
   * ```ts
   * const removeFirstValue = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
   *   $.return(arr.popFirst());
   * });
   * const compiled = East.compile(removeFirstValue.toIR(), []);
   * compiled([1n, 2n, 3n]);  // 1n (arr is now [2n, 3n])
   * ```
   */
  popFirst(): ExprType<T> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this.value_type as EastType,
      location: get_location(),
      builtin: "ArrayPopFirst",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as ExprType<T>;
  }

  /**
   * Appends all elements from another array to this array (mutates the array).
   *
   * @param array - The array whose elements will be appended
   * @returns NullExpr (operation performed for side effect)
   *
   * @example
   * ```ts
   * const appendArray = East.function([ArrayType(IntegerType), ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr1, arr2) => {
   *   $(arr1.append(arr2));  // Mutate arr1
   *   $.return(arr1);
   * });
   * const compiled = East.compile(appendArray.toIR(), []);
   * compiled([1n, 2n], [3n, 4n]);  // [1n, 2n, 3n, 4n]
   * ```
   */
  append(array: SubtypeExprOrValue<ArrayType<T>>): ExprType<NullType> {
    const arrayExpr = Expr.from(array, this[TypeSymbol]) as ArrayExpr<T>;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayAppend",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], arrayExpr[AstSymbol]],
    });
  }

  /**
   * Prepends all elements from another array to this array (mutates the array).
   *
   * @param array - The array whose elements will be prepended
   * @returns NullExpr (operation performed for side effect)
   *
   * @example
   * ```ts
   * const prependArray = East.function([ArrayType(IntegerType), ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr1, arr2) => {
   *   $(arr1.prepend(arr2));  // Mutate arr1
   *   $.return(arr1);
   * });
   * const compiled = East.compile(prependArray.toIR(), []);
   * compiled([3n, 4n], [1n, 2n]);  // [1n, 2n, 3n, 4n]
   * ```
   */
  prepend(array: SubtypeExprOrValue<ArrayType<T>>): ExprType<NullType> {
    // Convert the input array to an expression of the right type
    const arrayExpr = Expr.from(array, this[TypeSymbol]) as ArrayExpr<T>;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayPrepend",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], arrayExpr[AstSymbol]],
    });
  }

  /**
   * Merges all elements from another array into this array using a merge function.
   *
   * @param array - The array to merge from
   * @param mergeFn - Function taking (currentValue, otherValue, index) and returning the merged value
   * @returns Null (mutates the array in place)
   *
   * @throws East runtime error if the other array has more elements than this array
   *
   * @example
   * ```ts
   * const mergeArrays = East.function([ArrayType(IntegerType), ArrayType(IntegerType)], NullType, ($, arr1, arr2) => {
   *   arr1.mergeAll(arr2, ($, current, other, index) => current.add(other));
   *   $.return(null);
   * });
   * const compiled = East.compile(mergeArrays.toIR(), []);
   * const arr1 = [10n, 20n, 30n];
   * const arr2 = [1n, 2n, 3n];
   * compiled(arr1, arr2);  // null (arr1 is now [11n, 22n, 33n])
   * ```
   *
   * @example
   * ```ts
   * // Combining strings
   * const mergeStrings = East.function([ArrayType(StringType), ArrayType(StringType)], ArrayType(StringType), ($, arr1, arr2) => {
   *   arr1.mergeAll(arr2, ($, current, other, index) => current.concat(" + ").concat(other));
   *   $.return(arr1);
   * });
   * const compiled = East.compile(mergeStrings.toIR(), []);
   * compiled(["a", "b"], ["x", "y"]);  // ["a + x", "b + y"]
   * ```
   */
  mergeAll<T2>(array: Expr<ArrayType<T2>>, mergeFn: SubtypeExprOrValue<FunctionType<[T, NoInfer<T2>, IntegerType],T>>): ExprType<NullType> {
    const array_type = array[TypeSymbol];
    if (!array_type || array_type.type !== "Array") {
      throw new Error(`Expected array type for mergeAll, got ${array_type ? printType(array_type) : "unknown"}`);
    }
    const value2Type = array_type.value;
    const mergeFnExpr = Expr.from(mergeFn as any, FunctionType([this.value_type as EastType, value2Type, IntegerType], this.value_type as EastType));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayMergeAll",
      type_parameters: [this.value_type as EastType, value2Type as EastType],
      arguments: [this[AstSymbol], array[AstSymbol], mergeFnExpr[AstSymbol]],
    });
  }

  /**
   * Clears all elements from the array, making it empty.
   *
   * @returns Null (mutates the array in place)
   *
   * @example
   * ```ts
   * const clearArray = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
   *   arr.clear();
   *   $.return(arr);
   * });
   * const compiled = East.compile(clearArray.toIR(), []);
   * compiled([1n, 2n, 3n]);  // []
   * ```
   */
  clear() {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayClear",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as NullExpr;
  }

  /**
   * Sorts the array in place, re-ordering it in memory.
   *
   * @param by - Optional projection function to determine sort order (defaults to sorting by the values themselves)
   * @returns Null (mutates the array in place)
   *
   * @remarks
   * The optional `by` function can project values to determine sort order (e.g., sort by a specific field).
   *
   * @example
   * ```ts
   * const sortNumbers = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
   *   arr.sortInPlace();
   *   $.return(arr);
   * });
   * const compiled = East.compile(sortNumbers.toIR(), []);
   * compiled([3n, 1n, 4n, 1n, 5n]);  // [1n, 1n, 3n, 4n, 5n]
   * ```
   *
   * @example
   * ```ts
   * // Sorting structs by a field
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const sortByAge = East.function([ArrayType(PersonType)], ArrayType(PersonType), ($, people) => {
   *   people.sortInPlace(($, p) => p.age);
   *   $.return(people);
   * });
   * const compiled = East.compile(sortByAge.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);
   * // [{ name: "Bob", age: 25n }, { name: "Alice", age: 30n }]
   * ```
   *
   * @see {@link sort} to produce a new sorted array instead of sorting in place.
   */
  sortInPlace(by?: SubtypeExprOrValue<FunctionType<[T], undefined>>): NullExpr {
    let byExpr;
    if (by === undefined) {
      byExpr = Expr.function([this.value_type as EastType], this.value_type as EastType, ($, x) => x);
    } else {
      byExpr = by instanceof Expr ? by : Expr.function([this.value_type], undefined, by);
    }
    const byType = byExpr[TypeSymbol];
    const projectedType = byType.output as EastType;
    if (!(isDataType(projectedType))) {
      throw new Error(`Can only sort by data types, got ${printType(projectedType)}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArraySortInPlace",
      type_parameters: [this.value_type as EastType, projectedType],
      arguments: [this[AstSymbol], byExpr[AstSymbol]],
    }) as NullExpr;
  }

  /**
   * Produces a new array with the values sorted.
   *
   * @param by - Optional projection function to determine sort order (defaults to sorting by the values themselves)
   * @returns A new ArrayExpr containing the sorted elements
   *
   * @remarks
   * The optional `by` function can project values to determine sort order (e.g., sort by a specific field).
   * This method does not mutate the original array.
   *
   * @example
   * ```ts
   * const sortNumbers = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
   *   $.return(arr.sort());
   * });
   * const compiled = East.compile(sortNumbers.toIR(), []);
   * compiled([3n, 1n, 4n, 1n, 5n]);  // [1n, 1n, 3n, 4n, 5n]
   * ```
   *
   * @example
   * ```ts
   * // Sorting structs by a field (descending)
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const sortByAgeDesc = East.function([ArrayType(PersonType)], ArrayType(PersonType), ($, people) => {
   *   $.return(people.sort(($, p) => p.age.negate()));
   * });
   * const compiled = East.compile(sortByAgeDesc.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);
   * // [{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]
   * ```
   *
   * @see {@link sortInPlace} to sort the array in place.
   */
  sort(by?: SubtypeExprOrValue<FunctionType<[T], undefined>>): ArrayExpr<T> {
    let byExpr;
    if (by === undefined) {
      byExpr = Expr.function([this.value_type as EastType], this.value_type as EastType, ($, x) => x);
    } else {
      byExpr = by instanceof Expr ? by : Expr.function([this.value_type], undefined, by);
    }
    const byType = byExpr[TypeSymbol];
    const projectedType = byType.output as EastType;
    if (!(isDataType(projectedType))) {
      throw new Error(`Can only sort by data types, got ${printType(projectedType)}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "ArraySort",
      type_parameters: [this.value_type as EastType, projectedType],
      arguments: [this[AstSymbol], byExpr[AstSymbol]],
    }) as ArrayExpr<T>;
  }

  /**
   * Reverses the array in place.
   *
   * @returns Null (mutates the array in place)
   *
   * @example
   * ```ts
   * const reverseArray = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
   *   arr.reverseInPlace();
   *   $.return(arr);
   * });
   * const compiled = East.compile(reverseArray.toIR(), []);
   * compiled([1n, 2n, 3n, 4n, 5n]);  // [5n, 4n, 3n, 2n, 1n]
   * ```
   *
   * @see {@link reverse} to produce a new reversed array instead of reversing in place.
   */
  reverseInPlace(): NullExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayReverseInPlace",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as NullExpr;
  }

  /**
   * Produces a new array with the values in reverse order.
   *
   * @returns A new ArrayExpr with elements in reverse order
   *
   * @remarks
   * This method does not mutate the original array.
   *
   * @example
   * ```ts
   * const reverseArray = East.function([ArrayType(StringType)], ArrayType(StringType), ($, arr) => {
   *   $.return(arr.reverse());
   * });
   * const compiled = East.compile(reverseArray.toIR(), []);
   * compiled(["a", "b", "c"]);  // ["c", "b", "a"]
   * ```
   *
   * @see {@link reverseInPlace} to reverse the array in place.
   */
  reverse(): ArrayExpr<T> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "ArrayReverse",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as ArrayExpr<T>;
  }

  /**
   * Checks if the array is sorted in ascending order.
   *
   * @param by - Optional projection function to determine sort order (defaults to sorting by the values themselves)
   * @returns A BooleanExpr indicating whether the array is sorted
   *
   * @example
   * ```ts
   * const checkSorted = East.function([ArrayType(IntegerType)], BooleanType, ($, arr) => {
   *   $.return(arr.isSorted());
   * });
   * const compiled = East.compile(checkSorted.toIR(), []);
   * compiled([1n, 2n, 3n, 4n]);  // true
   * compiled([1n, 3n, 2n, 4n]);  // false
   * ```
   *
   * @example
   * ```ts
   * // Checking if sorted by a specific field
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const checkSortedByAge = East.function([ArrayType(PersonType)], BooleanType, ($, people) => {
   *   $.return(people.isSorted(($, p) => p.age));
   * });
   * const compiled = East.compile(checkSortedByAge.toIR(), []);
   * compiled([{ name: "Bob", age: 25n }, { name: "Alice", age: 30n }]);  // true
   * ```
   */
  isSorted(by?: SubtypeExprOrValue<FunctionType<[T], undefined>>): BooleanExpr {
    let byExpr;
    if (by === undefined) {
      byExpr = Expr.function([this.value_type as EastType], this.value_type as EastType, ($, x) => x);
    } else {
      byExpr = by instanceof Expr ? by : Expr.function([this.value_type], undefined, by);
    }
    const byType = byExpr[TypeSymbol];
    const projectedType = byType.output as EastType;
    if (!(isDataType(projectedType))) {
      throw new Error(`Can only sort by data types, got ${printType(projectedType)}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "ArrayIsSorted",
      type_parameters: [this.value_type as EastType, projectedType],
      arguments: [this[AstSymbol], byExpr[AstSymbol]],
    }) as BooleanExpr;
  }

  /**
   * Returns the index of the first element in a sorted array that is >= the given value (binary search).
   *
   * @param value - The value to search for
   * @param by - Optional projection function used for sorting (must match the array's sort order)
   * @returns An IntegerExpr representing the index (may be out of bounds if all elements are less)
   *
   * @remarks
   * This method assumes the array is already sorted. If all elements are less than the given value,
   * the returned index will equal the array size (out-of-bounds).
   *
   * @example
   * ```ts
   * const findFirst = East.function([ArrayType(IntegerType), IntegerType], IntegerType, ($, arr, value) => {
   *   $.return(arr.findSortedFirst(value));
   * });
   * const compiled = East.compile(findFirst.toIR(), []);
   * compiled([1n, 3n, 5n, 7n, 9n], 5n);  // 2n (index of 5)
   * compiled([1n, 3n, 5n, 7n, 9n], 4n);  // 2n (index where 4 would be inserted)
   * compiled([1n, 3n, 5n, 7n, 9n], 10n); // 5n (out of bounds)
   * ```
   *
   * @example
   * ```ts
   * // Using with projection function
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const findByAge = East.function([ArrayType(PersonType), IntegerType], IntegerType, ($, people, age) => {
   *   $.return(people.findSortedFirst(age, ($, p) => p.age));
   * });
   * const compiled = East.compile(findByAge.toIR(), []);
   * // Assumes people array is sorted by age
   * compiled([{ name: "Bob", age: 25n }, { name: "Alice", age: 30n }], 28n); // 1n
   * ```
   */
  findSortedFirst<T2>(value: T2, by?: SubtypeExprOrValue<FunctionType<[T], TypeOf<NoInfer<T2>>>>): IntegerExpr {
    const valueAst = valueOrExprToAst(value);
    const projectedType = valueAst.type;
    if (!isDataType(projectedType)) {
      throw new Error(`Can only search for data types, got ${printType(projectedType)}`);
    }

    let byExpr;
    if (by === undefined) {
      // It would be cool to infer an "obvious" projection here, e.g. prefix of a struct
      byExpr = Expr.function([this.value_type] as any, projectedType as any, ($, x) => x);
    } else {
      byExpr = by instanceof Expr ? by : Expr.function([this.value_type], projectedType as any, by as any);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "ArrayFindSortedFirst",
      type_parameters: [this.value_type as EastType, projectedType],
      arguments: [this[AstSymbol], valueAst, byExpr[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Returns the index of the last element in a sorted array that is <= the given value (binary search).
   *
   * @param value - The value to search for
   * @param by - Optional projection function used for sorting (must match the array's sort order)
   * @returns An IntegerExpr representing the index (may be -1 if all elements are greater)
   *
   * @remarks
   * This method assumes the array is already sorted. If all elements are greater than the given value,
   * the returned index will be -1 (out-of-bounds).
   *
   * @example
   * ```ts
   * const findLast = East.function([ArrayType(IntegerType), IntegerType], IntegerType, ($, arr, value) => {
   *   $.return(arr.findSortedLast(value));
   * });
   * const compiled = East.compile(findLast.toIR(), []);
   * compiled([1n, 3n, 5n, 7n, 9n], 5n);  // 2n (index of 5)
   * compiled([1n, 3n, 5n, 7n, 9n], 6n);  // 2n (index of last element <= 6)
   * compiled([1n, 3n, 5n, 7n, 9n], 0n);  // -1n (all elements are greater)
   * ```
   */
  findSortedLast<T2>(value: T2, by?: SubtypeExprOrValue<FunctionType<[T], TypeOf<NoInfer<T2>>>>): IntegerExpr {
    const valueAst = valueOrExprToAst(value);
    const projectedType = valueAst.type;
    if (!isDataType(projectedType)) {
      throw new Error(`Can only search for data types, got ${printType(projectedType)}`);
    }

    let byExpr;
    if (by === undefined) {
      // It would be cool to infer an "obvious" projection here, e.g. prefix of a struct
      byExpr = Expr.function([this.value_type] as any, projectedType as any, ($, x) => x);
    } else {
      byExpr = by instanceof Expr ? by : Expr.function([this.value_type], projectedType as any, by as any);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "ArrayFindSortedLast",
      type_parameters: [this.value_type as EastType, projectedType],
      arguments: [this[AstSymbol], valueAst, byExpr[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Returns the start and end indices of elements in a sorted array that equal the given value (binary search).
   *
   * @param value - The value to search for
   * @param by - Optional projection function used for sorting (must match the array's sort order)
   * @returns A struct with `start` and `end` indices (exclusive end, may be out of bounds if not found)
   *
   * @remarks
   * This method assumes the array is already sorted. If no elements match, the range will have zero size.
   * The indices may be out-of-bounds if no elements are found.
   *
   * @example
   * ```ts
   * const findRange = East.function([ArrayType(IntegerType), IntegerType], StructType({ start: IntegerType, end: IntegerType }), ($, arr, value) => {
   *   $.return(arr.findSortedRange(value));
   * });
   * const compiled = East.compile(findRange.toIR(), []);
   * compiled([1n, 3n, 5n, 5n, 5n, 7n, 9n], 5n);  // { start: 2n, end: 5n }
   * compiled([1n, 3n, 5n, 7n, 9n], 4n);          // { start: 2n, end: 2n } (not found)
   * ```
   */
  findSortedRange<T2>(value: T2, by?: SubtypeExprOrValue<FunctionType<[T], TypeOf<NoInfer<T2>>>>): ExprType<StructType<{ start: IntegerType; end: IntegerType }>> {
    const valueAst = valueOrExprToAst(value);
    const projectedType = valueAst.type;
    if (!isDataType(projectedType)) {
      throw new Error(`Can only search for data types, got ${printType(projectedType)}`);
    }

    let byExpr;
    if (by === undefined) {
      // It would be cool to infer an "obvious" projection here, e.g. prefix of a struct
      byExpr = Expr.function([this.value_type] as any, projectedType as any, ($, x) => x);
    } else {
      byExpr = by instanceof Expr ? by : Expr.function([this.value_type], projectedType as any, by as any);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StructType({ start: IntegerType, end: IntegerType }),
      location: get_location(),
      builtin: "ArrayFindSortedRange",
      type_parameters: [this.value_type as EastType, projectedType],
      arguments: [this[AstSymbol], valueAst, byExpr[AstSymbol]],
    }) as ExprType<StructType<{ start: IntegerType; end: IntegerType }>>;
  }

  /**
   * Extracts a slice of the array from start to end index (exclusive).
   *
   * @param start - The starting index (inclusive)
   * @param end - The ending index (exclusive)
   * @returns A new ArrayExpr containing the sliced elements
   *
   * @remarks
   * This method does not mutate the original array.
   *
   * @example
   * ```ts
   * const sliceArray = East.function([ArrayType(IntegerType), IntegerType, IntegerType], ArrayType(IntegerType), ($, arr, start, end) => {
   *   $.return(arr.slice(start, end));
   * });
   * const compiled = East.compile(sliceArray.toIR(), []);
   * compiled([10n, 20n, 30n, 40n, 50n], 1n, 4n);  // [20n, 30n, 40n]
   * compiled([10n, 20n, 30n, 40n, 50n], 0n, 2n);  // [10n, 20n]
   * ```
   */
  slice(start: SubtypeExprOrValue<IntegerType>, end: SubtypeExprOrValue<IntegerType>): ArrayExpr<T> {
    const startExpr = Expr.from(start, IntegerType) as ExprType<IntegerType>;
    const endExpr = Expr.from(end, IntegerType) as ExprType<IntegerType>;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "ArraySlice",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], startExpr[AstSymbol], endExpr[AstSymbol]],
    }) as ArrayExpr<T>;
  }

  /**
   * Creates a new array containing values from this array followed by values of the other array.
   *
   * @param other - The array to concatenate
   * @returns A new ArrayExpr with combined elements
   *
   * @remarks
   * This method does not mutate the original arrays.
   *
   * @example
   * ```ts
   * const concatArrays = East.function([ArrayType(IntegerType), ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr1, arr2) => {
   *   $.return(arr1.concat(arr2));
   * });
   * const compiled = East.compile(concatArrays.toIR(), []);
   * compiled([1n, 2n, 3n], [4n, 5n]);  // [1n, 2n, 3n, 4n, 5n]
   * ```
   */
  concat(other: SubtypeExprOrValue<ArrayType<T>>): ArrayExpr<T> {
    const otherExpr = Expr.from(other, this[TypeSymbol]) as ArrayExpr<T>;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "ArrayConcat",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], otherExpr[AstSymbol]],
    }) as ArrayExpr<T>;
  }

  /**
   * Returns a new array containing values at the specified indices.
   *
   * @param keys - An array of indices to retrieve
   * @param onMissing - Optional function to provide default values for out-of-bounds indices
   * @returns A new ArrayExpr with elements at the specified indices
   *
   * @throws East runtime error if an index is out of bounds and no onMissing function is provided
   *
   * @example
   * ```ts
   * const getMultiple = East.function([ArrayType(StringType), ArrayType(IntegerType)], ArrayType(StringType), ($, arr, indices) => {
   *   $.return(arr.getKeys(indices));
   * });
   * const compiled = East.compile(getMultiple.toIR(), []);
   * compiled(["a", "b", "c", "d"], [0n, 2n, 3n]);  // ["a", "c", "d"]
   * ```
   *
   * @example
   * ```ts
   * // With default for missing keys
   * const getWithDefault = East.function([ArrayType(IntegerType), ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr, indices) => {
   *   $.return(arr.getKeys(indices, ($, key) => -1n));
   * });
   * const compiled = East.compile(getWithDefault.toIR(), []);
   * compiled([10n, 20n, 30n], [1n, 5n, 2n]);  // [20n, -1n, 30n]
   * ```
   */
  getKeys(keys: SubtypeExprOrValue<ArrayType<IntegerType>>, onMissing?: SubtypeExprOrValue<FunctionType<[IntegerType], T>>): ArrayExpr<T> {
    const keysExpr = Expr.from(keys, ArrayType(IntegerType)) as ArrayExpr<IntegerType>;

    let default_function_ast;
    if (onMissing === undefined) {
      const location = get_location();
      const default_function = Expr.function([IntegerType], this.value_type as EastType, ($, key) => $.error(Expr.str`Cannot get key ${key} from array`, location));
      default_function_ast = Expr.ast(default_function);
    } else {
      const default_function_expr = Expr.from(onMissing, FunctionType([IntegerType], this.value_type));

      default_function_ast = Expr.ast(default_function_expr);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "ArrayGetKeys",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol], keysExpr[AstSymbol], default_function_ast],
    }) as ArrayExpr<T>;
  }

  /**
   * Executes a function for each element in the array.
   *
   * @param fn - Function taking (element, index) to execute for each entry
   * @returns Null
   *
   * @example
   * ```ts
   * const log = East.platform(FunctionType([StringType], NullType));
   * const forEachExample = East.function([ArrayType(IntegerType)], NullType, ($, arr) => {
   *   arr.forEach(($, elem, index) => {
   *     log(Expr.str`Index ${index}: ${elem}`);
   *   });
   *   $.return(null);
   * });
   * const compiled = East.compile(forEachExample.toIR(), [log.implement(console.log)]);
   * compiled([10n, 20n, 30n]);
   * // Logs: "Index 0: 10", "Index 1: 20", "Index 2: 30"
   * ```
   */
  forEach(fn: SubtypeExprOrValue<FunctionType<[T, IntegerType], undefined>>): NullExpr {
    if (!(fn instanceof Expr)) {
      fn = Expr.function([this.value_type, IntegerType], undefined, fn);
    }
    const fnType = fn[TypeSymbol];
    const returnType = fnType.output as EastType;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "ArrayForEach",
      type_parameters: [this.value_type as EastType, returnType],
      arguments: [this[AstSymbol], fn[AstSymbol]],
    }) as NullExpr;
  }
  /**
   * Creates a shallow copy of the array.
   *
   * @returns A new ArrayExpr with the same elements
   *
   * @remarks
   * Only the top-level array is cloned. Deeply nested structures (e.g., arrays of arrays) share references.
   *
   * @example
   * ```ts
   * const copyArray = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
   *   const copy = arr.copy();
   *   copy.pushLast(99n);
   *   $.return(copy);
   * });
   * const compiled = East.compile(copyArray.toIR(), []);
   * const original = [1n, 2n, 3n];
   * compiled(original);  // [1n, 2n, 3n, 99n]
   * // original is unchanged: [1n, 2n, 3n]
   * ```
   */
  copy(): ArrayExpr<T> {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "ArrayCopy",
      type_parameters: [this.value_type as EastType],
      arguments: [this[AstSymbol]],
    }) as ArrayExpr<T>;
  }

  /**
   * Maps each element to a new value using a transform function.
   *
   * @param fn - Function taking (element, index) and returning the transformed value
   * @returns A new ArrayExpr with transformed elements
   *
   * @example
   * ```ts
   * const doubleNumbers = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
   *   $.return(arr.map(($, x, i) => x.multiply(2n)));
   * });
   * const compiled = East.compile(doubleNumbers.toIR(), []);
   * compiled([1n, 2n, 3n, 4n]);  // [2n, 4n, 6n, 8n]
   * ```
   *
   * @example
   * ```ts
   * // Mapping to a different type
   * const numbersToStrings = East.function([ArrayType(IntegerType)], ArrayType(StringType), ($, arr) => {
   *   $.return(arr.map(($, x, i) => Expr.str`Number: ${x}`));
   * });
   * const compiled = East.compile(numbersToStrings.toIR(), []);
   * compiled([10n, 20n]);  // ["Number: 10", "Number: 20"]
   * ```
   *
   * @example
   * ```ts
   * // Mapping structs to extract a field
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const getNames = East.function([ArrayType(PersonType)], ArrayType(StringType), ($, people) => {
   *   $.return(people.map(($, p, i) => p.name));
   * });
   * const compiled = East.compile(getNames.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);  // ["Alice", "Bob"]
   * ```
   */
  map<T2>(fn: Expr<FunctionType<[T, IntegerType], T2>>): ArrayExpr<T2>;
  map<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(fn: F): ArrayExpr<TypeOf<ReturnType<F>>>;
  map(fn: Expr<FunctionType> | (($: BlockBuilder<NeverType>, x: ExprType<T>, y: ExprType<IntegerType>) => any)): Expr<ArrayType> {
    // We need to infer the output type
    if (fn instanceof Expr) {
      // The function was provided as an expression
      if (!(fn[TypeSymbol] && fn[TypeSymbol].type === "Function")) {
        throw new Error("Expected a Function expression");
      }
      const output_type = (fn[TypeSymbol] as FunctionType<any[], any>).output as EastType;
      const n_inputs = (fn[TypeSymbol] as FunctionType<any[], any>).inputs.length;
      if (n_inputs === 2) {
        // Two input function (value, index)
        if (!isSubtype(this.value_type as EastType, (fn[TypeSymbol] as FunctionType<any[], any>).inputs[0] as EastType)) {
          throw new Error(`Expected Function input to be ${printType(this.value_type as EastType)}, got ${printType((fn[TypeSymbol] as FunctionType<any[], any>).inputs[0] as EastType)}`);
        }
        if (!isTypeEqual(IntegerType, (fn[TypeSymbol] as FunctionType<any[], any>).inputs[1] as EastType)) {
          throw new Error(`Expected Function second input to be ${printType(IntegerType)}, got ${printType((fn[TypeSymbol] as FunctionType<any[], any>).inputs[1] as EastType)}`);
        }

        return this[FactorySymbol]({
          ast_type: "Builtin",
          type: ArrayType(output_type),
          location: get_location(),
          builtin: "ArrayMap",
          type_parameters: [this.value_type as EastType, output_type],
          arguments: [this[AstSymbol], fn[AstSymbol]],
        });
      } else {
        throw new Error(`Expected Function to have 2 inputs, got ${n_inputs} inputs`);
      }
    } else {
      // The function was provided as a lambda
      // We need to convert it to a FunctionExpr first, but we also need to infer the output type (using undefined)
      const functionExpr = Expr.function([this.value_type, IntegerType], undefined, fn);
      return this.map(functionExpr);
    }
  }

  /**
   * Filters array elements using a predicate function.
   *
   * @param predicate - Function taking (element, index) and returning true to keep the element
   * @returns A new ArrayExpr containing only elements for which the predicate returned true
   *
   * @example
   * ```ts
   * const filterEven = East.function([ArrayType(IntegerType)], ArrayType(IntegerType), ($, arr) => {
   *   $.return(arr.filter(($, x, i) => x.modulo(2n).equal(0n)));
   * });
   * const compiled = East.compile(filterEven.toIR(), []);
   * compiled([1n, 2n, 3n, 4n, 5n, 6n]);  // [2n, 4n, 6n]
   * ```
   *
   * @example
   * ```ts
   * // Filter by index
   * const filterFirstThree = East.function([ArrayType(StringType)], ArrayType(StringType), ($, arr) => {
   *   $.return(arr.filter(($, elem, index) => index.lessThan(3n)));
   * });
   * const compiled = East.compile(filterFirstThree.toIR(), []);
   * compiled(["a", "b", "c", "d", "e"]);  // ["a", "b", "c"]
   * ```
   *
   * @example
   * ```ts
   * // Filter structs by field
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const filterAdults = East.function([ArrayType(PersonType)], ArrayType(PersonType), ($, people) => {
   *   $.return(people.filter(($, p, i) => p.age.greaterOrEqual(18n)));
   * });
   * const compiled = East.compile(filterAdults.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 15n }]);  // [{ name: "Alice", age: 30n }]
   * ```
   */
  filter(predicate: SubtypeExprOrValue<FunctionType<[T, IntegerType], BooleanType>>): ArrayExpr<T> {
    if (!(predicate instanceof Expr)) {
      predicate = Expr.function([this.value_type, IntegerType], BooleanType, predicate);
    }

    // Check if it's actually a FunctionExpr by looking at its type
    if (!predicate[TypeSymbol] || predicate[TypeSymbol].type !== "Function") {
      throw new Error("forEach expects a Function expression");
    }

    const functionType = predicate[TypeSymbol] as FunctionType<any[], any>;
    
    if (functionType.inputs.length === 2) {
      // Two input function (value, index)
      if (!isSubtype(this.value_type as EastType, functionType.inputs[0] as EastType)) {
        throw new Error(`Expected Function input to be ${printType(this.value_type as EastType)}, got ${printType(functionType.inputs[0] as EastType)}`);
      }
      if (!isTypeEqual(IntegerType, functionType.inputs[1] as EastType)) {
        throw new Error(`Expected Function second input to be ${printType(IntegerType)}, got ${printType(functionType.inputs[1] as EastType)}`);
      }

      return this[FactorySymbol]({
        ast_type: "Builtin",
        location: get_location(),
        type: this[TypeSymbol],
        builtin: "ArrayFilter",
        type_parameters: [this.value_type as EastType],
        arguments: [this[AstSymbol], predicate[AstSymbol]],
      }) as ArrayExpr<any>;
    } else {
      throw new Error(`Expected Function to have 2 inputs, got ${functionType.inputs.length} inputs`);
    }
  }

  /**
   * Filters and maps array elements in a single pass using an Option-returning function.
   *
   * @param fn - Function taking (element, index) and returning Option<T2> (.some(value) to include, .none to exclude)
   * @returns A new ArrayExpr containing only the mapped values from .some() results
   *
   * @remarks
   * This is more efficient than using `filter` followed by `map`, as it only iterates the array once.
   *
   * @example
   * ```ts
   * const parseSafe = East.function([ArrayType(StringType)], ArrayType(IntegerType), ($, arr) => {
   *   $.return(arr.filterMap(($, str, i) => {
   *     const num = str.toInteger();
   *     return $.if(num.isNone(), () => Expr.none, () => Expr.some(num.unwrap()));
   *   }));
   * });
   * const compiled = East.compile(parseSafe.toIR(), []);
   * compiled(["10", "not-a-number", "20", "30"]);  // [10n, 20n, 30n]
   * ```
   *
   * @example
   * ```ts
   * // Extract and transform field if condition met
   * const PersonType = StructType({ name: StringType, age: IntegerType, active: BooleanType });
   * const getActiveNames = East.function([ArrayType(PersonType)], ArrayType(StringType), ($, people) => {
   *   $.return(people.filterMap(($, p, i) =>
   *     $.if(p.active, () => Expr.some(p.name.toUpperCase()), () => Expr.none)
   *   ));
   * });
   * const compiled = East.compile(getActiveNames.toIR(), []);
   * compiled([
   *   { name: "Alice", age: 30n, active: true },
   *   { name: "Bob", age: 25n, active: false },
   *   { name: "Carol", age: 35n, active: true }
   * ]);  // ["ALICE", "CAROL"]
   * ```
   *
   * @see {@link filter} to only filter values, and {@link map} to only map values.
   */
  filterMap<T2>(fn: Expr<FunctionType<[T, IntegerType], OptionType<T2>>>): ArrayExpr<T2>;
  filterMap<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(fn: F): ArrayExpr<TypeOf<ReturnType<F>> extends VariantType<infer U> ? "some" extends keyof U ? U["some"] : NeverType : NeverType>;
  filterMap(fn: any): ArrayExpr<any> {
    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, IntegerType], undefined));

    const returnType = fnAst.type.output as EastType;

    if (returnType.type !== "Variant") {
      throw new Error(`Expected Function to return an Option type, got ${printType(returnType)}`);
    }
    if (!Object.keys(returnType.cases).every(k => k === "none" || k === "some")) {
      throw new Error(`Expected Function to return an Option type, got ${printType(returnType)}`);
    }
    const someType = returnType.cases["some"] ?? NeverType;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: ArrayType(someType as EastType),
      location: get_location(),
      builtin: "ArrayFilterMap",
      type_parameters: [this.value_type as EastType, someType as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as ArrayExpr<any>;
  }

  /**
   * Find the first element where the mapping function returns `some(value)`, and return that value wrapped in an Option.
   *
   * The supplied function must return an Option type. This method stops iterating as soon as the first `some` value is found,
   * making it efficient for early termination searches.
   *
   * Returns `none` if no element produces a `some` value, or `some(value)` with the first mapped result.
   *
   * @param fn - Function that maps each element to an Option type
   * @returns Option containing the first successfully mapped value, or `none` if none found
   *
   * @see {@link filterMap} to collect all mapped values that return `some` (scans entire array).
   */
  firstMap<T2>(fn: Expr<FunctionType<[T, IntegerType], OptionType<T2>>>): ExprType<OptionType<T2>>;
  firstMap<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(fn: F): ExprType<TypeOf<ReturnType<F>>>;
  firstMap(fn: any): Expr {
    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, IntegerType], undefined));

    const returnType = fnAst.type.output as EastType;

    if (returnType.type !== "Variant") {
      throw new Error(`Expected Function to return an Option type, got ${printType(returnType)}`);
    }
    if (!Object.keys(returnType.cases).every(k => k === "none" || k === "some")) {
      throw new Error(`Expected Function to return an Option type, got ${printType(returnType)}`);
    }
    const someType = returnType.cases["some"] ?? NeverType;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: returnType as EastType,
      location: get_location(),
      builtin: "ArrayFirstMap",
      type_parameters: [this.value_type as EastType, someType as EastType],
      arguments: [this[AstSymbol], fnAst],
    });
  }

  /**
   * Finds the index of the first element equal to the given value.
   *
   * @param value - The value to search for
   * @param by - Optional projection function to transform elements before comparison
   * @returns Option containing the index of the first matching element, or .none if not found
   *
   * @example
   * ```ts
   * const findValue = East.function([ArrayType(IntegerType), IntegerType], OptionType(IntegerType), ($, arr, val) => {
   *   $.return(arr.findFirst(val));
   * });
   * const compiled = East.compile(findValue.toIR(), []);
   * compiled([10n, 20n, 30n, 20n], 20n);  // .some(1n)
   * compiled([10n, 20n, 30n], 99n);       // .none
   * ```
   *
   * @example
   * ```ts
   * // Finding by a projected field
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const findByAge = East.function([ArrayType(PersonType), IntegerType], OptionType(IntegerType), ($, people, targetAge) => {
   *   $.return(people.findFirst(targetAge, ($, p, i) => p.age));
   * });
   * const compiled = East.compile(findByAge.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }], 25n);  // .some(1n)
   * ```
   *
   * @see {@link findAll} to find all matching elements (returns array of indices).
   * @see {@link findSortedFirst} for binary search on sorted arrays (returns index directly, may be out of bounds).
   * @see {@link firstMap} for predicate-based searches that can transform results.
   */
  findFirst<T2>(value: SubtypeExprOrValue<T2>, by: Expr<FunctionType<[T, IntegerType], T2>>): ExprType<OptionType<IntegerType>>
  findFirst<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(value: ValueTypeOf<TypeOf<ReturnType<NoInfer<F>>>>, by: F): ExprType<OptionType<IntegerType>>
  findFirst<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(value: Expr<SubType<TypeOf<ReturnType<NoInfer<F>>>>>, by: F): ExprType<OptionType<IntegerType>>
  findFirst(value: SubtypeExprOrValue<T>): ExprType<OptionType<IntegerType>>
  findFirst(value: any, by?: SubtypeExprOrValue<FunctionType<[T, IntegerType], any>>): ExprType<OptionType<IntegerType>> {
    if (by === undefined) {
      return this.firstMap(($, v, k) => Expr.equal(v as any, value).ifElse(() => some(k) as any, () => none as any)) as any;
    } else {
      const byExpr = (by instanceof Expr ? by : Expr.function([this.value_type, IntegerType], undefined, by)) as CallableFunctionExpr<[T, IntegerType], any>;

      if (byExpr[TypeSymbol].type !== "Function") {
        throw new Error("Expected a Function expression for 'by' parameter");
      }
      const byType = byExpr[TypeSymbol] as FunctionType<any[], any>;
      if (byType.inputs.length !== 2) {
        throw new Error(`Expected 'by' function to have 2 inputs, got ${byType.inputs.length}`);
      }
      if (!isSubtype(this.value_type as EastType, byType.inputs[0] as EastType)) {
        throw new Error(`Expected 'by' function input to be ${printType(this.value_type as EastType)}, got ${printType(byType.inputs[0] as EastType)}`);
      }

      return this.firstMap(($, v, k) => Expr.equal(byExpr(v as any, k), value).ifElse(() => some(k) as any, () => none as any)) as any;
    }
  }

  /**
   * Finds the indices of all elements equal to the given value.
   *
   * @param value - The value to search for
   * @param by - Optional projection function to transform elements before comparison
   * @returns An ArrayExpr<IntegerType> of indices for all matching elements (empty if none found)
   *
   * @example
   * ```ts
   * const findAllValues = East.function([ArrayType(IntegerType), IntegerType], ArrayType(IntegerType), ($, arr, val) => {
   *   $.return(arr.findAll(val));
   * });
   * const compiled = East.compile(findAllValues.toIR(), []);
   * compiled([10n, 20n, 30n, 20n, 10n], 20n);  // [1n, 3n]
   * compiled([10n, 20n, 30n], 99n);            // []
   * ```
   *
   * @example
   * ```ts
   * // Finding all by a projected field
   * const PersonType = StructType({ name: StringType, role: StringType });
   * const findByRole = East.function([ArrayType(PersonType), StringType], ArrayType(IntegerType), ($, people, targetRole) => {
   *   $.return(people.findAll(targetRole, ($, p, i) => p.role));
   * });
   * const compiled = East.compile(findByRole.toIR(), []);
   * compiled([
   *   { name: "Alice", role: "admin" },
   *   { name: "Bob", role: "user" },
   *   { name: "Carol", role: "admin" }
   * ], "admin");  // [0n, 2n]
   * ```
   *
   * @see {@link findSortedRange} for binary search on sorted arrays (returns start/end indices, may be out of bounds).
   * @see {@link findFirst} to find only the first match (returns Option).
   * @see {@link filterMap} for predicate-based searches that can transform results.
   */
  findAll<T2>(value: SubtypeExprOrValue<T2>, by: Expr<FunctionType<[T, IntegerType], T2>>): ArrayExpr<IntegerType>
  findAll<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(value: ValueTypeOf<TypeOf<ReturnType<NoInfer<F>>>>, by: F): ArrayExpr<IntegerType>
  findAll<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(value: Expr<SubType<TypeOf<ReturnType<NoInfer<F>>>>>, by: F): ArrayExpr<IntegerType>
  findAll(value: SubtypeExprOrValue<T>): ArrayExpr<IntegerType>
  findAll(value: any, by?: SubtypeExprOrValue<FunctionType<[T, IntegerType], any>>): ArrayExpr<IntegerType> {
    if (by === undefined) {
      return this.filterMap(($, v, k) => Expr.equal(v as any, value).ifElse(() => some(k) as any, () => none as any)) as any;
    } else {
      const byExpr = (by instanceof Expr ? by : Expr.function([this.value_type, IntegerType], undefined, by)) as CallableFunctionExpr<[T, IntegerType], any>;

      if (byExpr[TypeSymbol].type !== "Function") {
        throw new Error("Expected a Function expression for 'by' parameter");
      }
      const byType = byExpr[TypeSymbol] as FunctionType<any[], any>;
      if (byType.inputs.length !== 2) {
        throw new Error(`Expected 'by' function to have 2 inputs, got ${byType.inputs.length}`);
      }
      if (!isSubtype(this.value_type as EastType, byType.inputs[0] as EastType)) {
        throw new Error(`Expected 'by' function input to be ${printType(this.value_type as EastType)}, got ${printType(byType.inputs[0] as EastType)}`);
      }

      return this.filterMap(($, v, k) => Expr.equal(byExpr(v as any, k), value).ifElse(() => some(k) as any, () => none as any)) as any;
    }
  }

  /**
   * Reduces the array to a single value using an accumulator function and initial value.
   *
   * @param combineFn - Function taking (accumulator, element, index) and returning the new accumulator value
   * @param init - Initial value for the reduction (determines output type)
   * @returns The final accumulated value
   *
   * @remarks
   * The accumulator function is called for each element with the previous result (or initial value for first element),
   * the current value, and the current index. This operation is safe on empty arrays (returns the initial value).
   *
   * @example
   * ```ts
   * const sumArray = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
   *   $.return(arr.reduce(($, acc, val, index) => acc.add(val), 0n));
   * });
   * const compiled = East.compile(sumArray.toIR(), []);
   * compiled([1n, 2n, 3n, 4n]);  // 10n
   * compiled([]);                // 0n (initial value)
   * ```
   *
   * @example
   * ```ts
   * // Building a string from array
   * const joinArray = East.function([ArrayType(StringType)], StringType, ($, arr) => {
   *   $.return(arr.reduce(($, acc, val, index) =>
   *     $.if(index.equal(0n), () => val, () => acc.concat(", ").concat(val))
   *   , ""));
   * });
   * const compiled = East.compile(joinArray.toIR(), []);
   * compiled(["a", "b", "c"]);  // "a, b, c"
   * ```
   *
   * @see {@link mapReduce} for a version that projects each value before reducing (and errors on empty arrays).
   * @see {@link sum}, {@link mean}, {@link every}, and {@link some} for common reduction operations.
   */
  reduce<T2>(combineFn: SubtypeExprOrValue<FunctionType<[previous: TypeOf<NoInfer<T2>>, value: T, key: IntegerType], TypeOf<NoInfer<T2>>>>, init: T2): ExprType<TypeOf<T2>> {
    const initAst = valueOrExprToAst(init);
    const returnType = initAst.type;

    const combineAst = valueOrExprToAstTyped(combineFn, FunctionType([returnType, this.value_type, IntegerType], returnType));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: returnType as EastType,
      location: get_location(),
      builtin: "ArrayFold",
      type_parameters: [this.value_type as EastType, returnType as EastType],
      arguments: [this[AstSymbol], initAst, combineAst],
    }) as ExprType<TypeOf<T2>>;
  }

  /**
   * Reduce array to single value using projection and accumulator functions.
   *
   * The first element of the array is used as initial value and reduction starts from the second element.
   * If the array is empty, an error is thrown.
   *
   * @see {@link reduce} for a version with an initial value
   */
  mapReduce<T2>(mapFn: Expr<FunctionType<[value: T, key: IntegerType], T2>>, combineFn: SubtypeExprOrValue<FunctionType<[previous: NoInfer<T2>, value: NoInfer<T2>], NoInfer<T2>>>): ExprType<T2>
  mapReduce<F extends ($: BlockBuilder<NeverType>, value: ExprType<T>, key: IntegerExpr) => any>(mapFn: F, combineFn: SubtypeExprOrValue<FunctionType<[previous: NoInfer<TypeOf<ReturnType<F>>>, value: NoInfer<TypeOf<ReturnType<F>>>], NoInfer<TypeOf<ReturnType<F>>>>>): ExprType<TypeOf<ReturnType<F>>>
  mapReduce<T2>(mapFn:any, combineFn: any): Expr {
    const mapAst = valueOrExprToAstTyped(mapFn, FunctionType([this.value_type, IntegerType], undefined));
    const mapType = mapAst.type.output as EastType;
    const combineAst = valueOrExprToAstTyped(combineFn, FunctionType([mapType, mapType], mapType));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: mapType as EastType,
      location: get_location(),
      builtin: "ArrayMapReduce",
      type_parameters: [this.value_type as EastType, mapType],
      arguments: [this[AstSymbol], mapAst, combineAst],
    }) as ExprType<T2>;
  }

  // Common reducers are provided, based on reduce

  /**
   * Returns true if every element satisfies the predicate, false otherwise.
   *
   * @param fn - Optional predicate function (required for non-Boolean arrays)
   * @returns A BooleanExpr (true for empty arrays)
   *
   * @remarks
   * This method short-circuits on the first false element for efficiency.
   *
   * @example
   * ```ts
   * const allPositive = East.function([ArrayType(IntegerType)], BooleanType, ($, arr) => {
   *   $.return(arr.every(($, x, i) => x.greater(0n)));
   * });
   * const compiled = East.compile(allPositive.toIR(), []);
   * compiled([1n, 2n, 3n]);   // true
   * compiled([1n, -2n, 3n]);  // false
   * compiled([]);             // true (empty array)
   * ```
   *
   * @example
   * ```ts
   * // Checking structs
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const allAdults = East.function([ArrayType(PersonType)], BooleanType, ($, people) => {
   *   $.return(people.every(($, p, i) => p.age.greaterOrEqual(18n)));
   * });
   * const compiled = East.compile(allAdults.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);  // true
   * ```
   *
   * @see {@link some} to check if at least one element is true.
   */
  every(fn?: SubtypeExprOrValue<FunctionType<[T, IntegerType], BooleanType>>): BooleanExpr {
    if (fn === undefined) {
      if (!isTypeEqual(this.value_type as EastType, BooleanType)) {
        throw new Error(`Can only perform every on array of booleans, got ${printType(this.value_type as EastType)}`);
      }
      // Short-circuit on first false value
      const result = this.firstMap(($, v, _k) => (v as BooleanExpr).not().ifElse(() => some(null), () => none));
      return Expr.match(result, { some: () => false, none: () => true });
    }

    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, IntegerType], BooleanType));

    // Short-circuit on first false value
    const result = this.firstMap(($, v, k) => {
      const result = Expr.fromAst(fnAst)(v as any, k) as BooleanExpr;
      return result.not().ifElse(() => some(null), () => none);
    });
    return Expr.match(result, { some: () => false, none: () => true });
  }

  /**
   * Returns true if at least one element satisfies the predicate, false otherwise.
   *
   * @param fn - Optional predicate function (required for non-Boolean arrays)
   * @returns A BooleanExpr (false for empty arrays)
   *
   * @remarks
   * This method short-circuits on the first true element for efficiency.
   *
   * @example
   * ```ts
   * const hasNegative = East.function([ArrayType(IntegerType)], BooleanType, ($, arr) => {
   *   $.return(arr.some(($, x, i) => x.less(0n)));
   * });
   * const compiled = East.compile(hasNegative.toIR(), []);
   * compiled([1n, 2n, 3n]);    // false
   * compiled([1n, -2n, 3n]);   // true
   * compiled([]);              // false (empty array)
   * ```
   *
   * @example
   * ```ts
   * // Checking structs
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const hasMinor = East.function([ArrayType(PersonType)], BooleanType, ($, people) => {
   *   $.return(people.some(($, p, i) => p.age.less(18n)));
   * });
   * const compiled = East.compile(hasMinor.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 15n }]);  // true
   * ```
   *
   * @see {@link every} to check if all elements are true.
   */
  some(fn?: SubtypeExprOrValue<FunctionType<[T, IntegerType], BooleanType>>): BooleanExpr {
    if (fn === undefined) {
      if (!isTypeEqual(this.value_type as EastType, BooleanType)) {
        throw new Error(`Can only perform some on array of booleans, got ${printType(this.value_type as EastType)}`);
      }
      // Short-circuit on first true value
      const result = this.firstMap(($, v, _k) => (v as BooleanExpr).ifElse(() => some(null), () => none));
      return Expr.match(result, { some: () => true, none: () => false });
    }

    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, IntegerType], BooleanType));

    // Short-circuit on first true value
    const result = this.firstMap(($, v, k) => {
      const result = Expr.fromAst(fnAst)(v as any, k) as BooleanExpr;
      return result.ifElse(() => some(null), () => none);
    });
    return Expr.match(result, { some: () => true, none: () => false });
  }
  
  /**
   * Sums all elements in the array.
   *
   * @param fn - Optional mapping function to project elements to numbers (required for non-numeric arrays)
   * @returns IntegerExpr or FloatExpr depending on the element type (0 for empty arrays)
   *
   * @example
   * ```ts
   * const sumIntegers = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
   *   $.return(arr.sum());
   * });
   * const compiled = East.compile(sumIntegers.toIR(), []);
   * compiled([1n, 2n, 3n, 4n]);  // 10n
   * compiled([]);                // 0n
   * ```
   *
   * @example
   * ```ts
   * // Sum with projection function
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const totalAge = East.function([ArrayType(PersonType)], IntegerType, ($, people) => {
   *   $.return(people.sum(($, p, i) => p.age));
   * });
   * const compiled = East.compile(totalAge.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);  // 55n
   * ```
   */
  sum(fn: Expr<FunctionType<[T, IntegerType], IntegerType>>): IntegerExpr
  sum(fn: Expr<FunctionType<[T, IntegerType], FloatType>>): FloatExpr
  sum<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(fn: F): TypeOf<ReturnType<F>> extends IntegerType ? IntegerExpr : TypeOf<ReturnType<F>> extends FloatType ? FloatExpr : never
  sum(): T extends IntegerType | FloatType ? ExprType<T> : never
  sum(fn?: any): Expr<IntegerType | FloatType> {
    if (fn === undefined) {
      if (!(isTypeEqual(this.value_type as EastType, IntegerType) || isTypeEqual(this.value_type as EastType, FloatType))) {
        throw new Error(`Can only perform sum on array of numbers (Integer or Float), got ${printType(this.value_type as EastType)}`);
      }
      const zero = isTypeEqual(this.value_type as EastType, IntegerType) ? 0n : 0.0;
      return this.reduce(($, previous, value) => previous.add(value as any) as any, zero) as any;
    } else {
      const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, IntegerType], undefined));
      const returnType = fnAst.type.output as EastType;
      if (!(isTypeEqual(returnType, IntegerType) || isTypeEqual(returnType, FloatType))) {
        throw new Error(`Can only perform sum on array of numbers (Integer or Float), got ${printType(returnType)}`);
      }
      const zero = isTypeEqual(returnType, IntegerType) ? 0n : 0.0;
      return this.reduce(($, previous, value, key) => previous.add(Expr.fromAst(fnAst)(value as any, key) as any) as any, zero) as any;
    }
  }

  /**
   * Calculates the mean (average) of all elements in the array.
   *
   * @param fn - Optional mapping function to project elements to numbers (required for non-numeric arrays)
   * @returns A FloatExpr representing the mean (NaN for empty arrays)
   *
   * @remarks
   * The mean is defined as the sum of all elements divided by the number of elements.
   *
   * @example
   * ```ts
   * const avgNumbers = East.function([ArrayType(IntegerType)], FloatType, ($, arr) => {
   *   $.return(arr.mean());
   * });
   * const compiled = East.compile(avgNumbers.toIR(), []);
   * compiled([1n, 2n, 3n, 4n]);  // 2.5
   * compiled([]);                // NaN
   * ```
   *
   * @example
   * ```ts
   * // Mean with projection function
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const avgAge = East.function([ArrayType(PersonType)], FloatType, ($, people) => {
   *   $.return(people.mean(($, p, i) => p.age));
   * });
   * const compiled = East.compile(avgAge.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 20n }]);  // 25.0
   * ```
   */
  mean(fn: Expr<FunctionType<[T, IntegerType], IntegerType>>): FloatExpr
  mean(fn: Expr<FunctionType<[T, IntegerType], FloatType>>): FloatExpr
  mean<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(fn: F): TypeOf<ReturnType<F>> extends IntegerType | FloatType ? FloatExpr : never
  mean(): T extends IntegerType | FloatType ? FloatExpr : never
  mean(fn?: any): Expr<IntegerType | FloatType> {
    if (fn === undefined) {
      if (isTypeEqual(this.value_type as EastType, IntegerType)) {
        return this.reduce(($, previous, value) => previous.add((value as IntegerExpr).toFloat()), 0.0).divide(this.size().toFloat());
      } else if (isTypeEqual(this.value_type as EastType, FloatType)) {
        return this.reduce(($, previous, value) => previous.add(value as FloatExpr), 0.0).divide(this.size().toFloat());
      } else {
        throw new Error(`Can only perform sum on array of numbers (Integer or Float), got ${printType(this.value_type as EastType)}`);
      }
    } else {
      const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.value_type, IntegerType], undefined));
      const returnType = fnAst.type.output as EastType;
      if (isTypeEqual(returnType, IntegerType)) {
        return this.reduce(($, previous: any, value, key) => previous.add((Expr.fromAst(fnAst)(value as any, key) as IntegerExpr).toFloat()) as FloatExpr, 0.0).divide(this.size().toFloat());
      } else if (isTypeEqual(returnType, FloatType)) {
        return this.reduce(($, previous, value, key) => previous.add(Expr.fromAst(fnAst)(value as any, key) as FloatExpr), 0.0).divide(this.size().toFloat());
      } else {
        throw new Error(`Can only perform sum on array of numbers (Integer or Float), got ${printType(returnType)}`);
      }
    }
  }

  /**
   * Finds the index of the maximum element in the array.
   *
   * @param by - Optional projection function to transform elements for comparison
   * @returns Option containing the index of the maximum element, or .none if the array is empty
   *
   * @example
   * ```ts
   * const findMax = East.function([ArrayType(IntegerType)], OptionType(IntegerType), ($, arr) => {
   *   $.return(arr.findMaximum());
   * });
   * const compiled = East.compile(findMax.toIR(), []);
   * compiled([3n, 1n, 4n, 1n, 5n]);  // .some(4n) - index of 5
   * compiled([]);                     // .none
   * ```
   *
   * @example
   * ```ts
   * // Finding index by projection
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const findOldest = East.function([ArrayType(PersonType)], OptionType(IntegerType), ($, people) => {
   *   $.return(people.findMaximum(($, p, i) => p.age));
   * });
   * const compiled = East.compile(findOldest.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);  // .some(0n)
   * ```
   *
   * @see {@link findMinimum} to find the index of the minimum element.
   * @see {@link maximum} to get the maximum element itself (throws on empty array).
   */
  findMaximum(by: Expr<FunctionType<[T, IntegerType], any>>): ExprType<OptionType<IntegerType>>
  findMaximum<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(by: F): ExprType<OptionType<IntegerType>>
  findMaximum(): T extends (IntegerType | FloatType | StringType) ? ExprType<OptionType<IntegerType>> : never
  findMaximum(by?: any): ExprType<OptionType<IntegerType>> {
    if (by === undefined) {
      // No projection - compare elements directly
      if (!(isDataType(this.value_type as EastType))) {
        throw new Error(`Can only perform findMaximum on arrays of data types, got ${printType(this.value_type as EastType)}`);
      }
      // Check if array is empty first
      return Expr.equal(this.size(), 0n).ifElse(
        () => none as any,
        () => {
          const result = this.mapReduce(
            ($, x: any, k: any) => ({ index: k, value: x }),
            ($, a: any, b: any) => Expr.greaterEqual(a.value, b.value).ifElse(() => a, () => b) as any
          );
          return some((result as any).index) as any;
        }
      ) as any;
    } else {
      // With projection - need to track element, projected value, and index
      const byExpr = (by instanceof Expr ? by : Expr.function([this.value_type, IntegerType], undefined, by)) as CallableFunctionExpr<[T, IntegerType], any>;

      if (byExpr[TypeSymbol].type !== "Function") {
        throw new Error("Expected a Function expression for 'by' parameter");
      }
      const byType = byExpr[TypeSymbol] as FunctionType<any[], any>;
      const projectedType = byType.output as EastType;

      if (!isDataType(projectedType)) {
        throw new Error(`Can only compare data types, got ${printType(projectedType)}`);
      }

      // Check if array is empty first
      return Expr.equal(this.size(), 0n).ifElse(
        () => none as any,
        () => {
          // Map to { index, key }, reduce by comparing keys, extract index
          const result = this.mapReduce(
            ($, x: any, k: any) => ({ index: k, key: byExpr(x as any, k) }),
            ($, a: any, b: any) => Expr.greaterEqual(a.key, b.key).ifElse(() => a, () => b) as any
          );
          return some((result as any).index) as any;
        }
      ) as any;
    }
  }

  /**
   * Finds the index of the minimum element in the array.
   *
   * @param by - Optional projection function to transform elements for comparison
   * @returns Option containing the index of the minimum element, or .none if the array is empty
   *
   * @example
   * ```ts
   * const findMin = East.function([ArrayType(IntegerType)], OptionType(IntegerType), ($, arr) => {
   *   $.return(arr.findMinimum());
   * });
   * const compiled = East.compile(findMin.toIR(), []);
   * compiled([3n, 1n, 4n, 1n, 5n]);  // .some(1n) - index of first 1
   * compiled([]);                     // .none
   * ```
   *
   * @example
   * ```ts
   * // Finding index by projection
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const findYoungest = East.function([ArrayType(PersonType)], OptionType(IntegerType), ($, people) => {
   *   $.return(people.findMinimum(($, p, i) => p.age));
   * });
   * const compiled = East.compile(findYoungest.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);  // .some(1n)
   * ```
   *
   * @see {@link findMaximum} to find the index of the maximum element.
   * @see {@link minimum} to get the minimum element itself (throws on empty array).
   */
  findMinimum(by: Expr<FunctionType<[T, IntegerType], any>>): ExprType<OptionType<IntegerType>>
  findMinimum<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(by: F): ExprType<OptionType<IntegerType>>
  findMinimum(): T extends (IntegerType | FloatType | StringType) ? ExprType<OptionType<IntegerType>> : never
  findMinimum(by?: any): ExprType<OptionType<IntegerType>> {
    if (by === undefined) {
      // No projection - compare elements directly
      if (!(isDataType(this.value_type as EastType))) {
        throw new Error(`Can only perform findMinimum on arrays of data types, got ${printType(this.value_type as EastType)}`);
      }
      // Check if array is empty first
      return Expr.equal(this.size(), 0n).ifElse(
        () => none as any,
        () => {
          const result = this.mapReduce(
            ($, x: any, k: any) => ({ index: k, value: x }),
            ($, a: any, b: any) => Expr.lessEqual(a.value, b.value).ifElse(() => a, () => b) as any
          );
          return some((result as any).index) as any;
        }
      ) as any;
    } else {
      // With projection - need to track element, projected value, and index
      const byExpr = (by instanceof Expr ? by : Expr.function([this.value_type, IntegerType], undefined, by)) as CallableFunctionExpr<[T, IntegerType], any>;

      if (byExpr[TypeSymbol].type !== "Function") {
        throw new Error("Expected a Function expression for 'by' parameter");
      }
      const byType = byExpr[TypeSymbol] as FunctionType<any[], any>;
      const projectedType = byType.output as EastType;

      if (!isDataType(projectedType)) {
        throw new Error(`Can only compare data types, got ${printType(projectedType)}`);
      }

      // Check if array is empty first
      return Expr.equal(this.size(), 0n).ifElse(
        () => none as any,
        () => {
          // Map to { index, key }, reduce by comparing keys, extract index
          const result = this.mapReduce(
            ($, x: any, k: any) => ({ index: k, key: byExpr(x as any, k) }),
            ($, a: any, b: any) => Expr.lessEqual(a.key, b.key).ifElse(() => a, () => b) as any
          );
          return some((result as any).index) as any;
        }
      ) as any;
    }
  }

  /**
   * Returns the maximum element in the array.
   *
   * @param by - Optional projection function to transform elements for comparison
   * @returns The element with the maximum value (or maximum projected value)
   *
   * @throws East runtime error if the array is empty
   *
   * @example
   * ```ts
   * const getMax = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
   *   $.return(arr.maximum());
   * });
   * const compiled = East.compile(getMax.toIR(), []);
   * compiled([3n, 1n, 4n, 1n, 5n]);  // 5n
   * // compiled([]) would throw error
   * ```
   *
   * @example
   * ```ts
   * // Getting element by projection
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const getOldest = East.function([ArrayType(PersonType)], PersonType, ($, people) => {
   *   $.return(people.maximum(($, p, i) => p.age));
   * });
   * const compiled = East.compile(getOldest.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);
   * // { name: "Alice", age: 30n }
   * ```
   *
   * @see {@link minimum} to find the minimum element.
   * @see {@link findMaximum} to get the index instead (returns Option, safe for empty arrays).
   */
  maximum(by: Expr<FunctionType<[T, IntegerType], any>>): ExprType<T>
  maximum<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(by: F): ExprType<T>
  maximum(): T extends (IntegerType | FloatType | StringType) ? ExprType<T> : never
  maximum(by?: any): ExprType<T> {
    if (by === undefined) {
      // No projection - compare elements directly
      // Use mapReduce with lambda functions directly
      return this.mapReduce(
        ($, x: any) => x,
        Expr.function([this.value_type, this.value_type], this.value_type as EastType, ($, a: any, b: any) => Expr.max(a, b) as any)
      ) as any;
    } else {
      // With projection - need to track both element and projected value
      const byExpr = (by instanceof Expr ? by : Expr.function([this.value_type, IntegerType], undefined, by)) as CallableFunctionExpr<[T, IntegerType], any>;

      if (byExpr[TypeSymbol].type !== "Function") {
        throw new Error("Expected a Function expression for 'by' parameter");
      }
      const byType = byExpr[TypeSymbol] as FunctionType<any[], any>;
      const projectedType = byType.output as EastType;

      if (!isDataType(projectedType)) {
        throw new Error(`Can only compare data types, got ${printType(projectedType)}`);
      }

      // Map to { element, key }, reduce by comparing keys, extract element
      // Use greaterEqual to keep the first element when keys are equal
      const result = this.mapReduce(
        ($, x: any, k: any) => ({ element: x, key: byExpr(x as any, k) }),
        ($, a: any, b: any) => Expr.greaterEqual(a.key, b.key).ifElse(() => a, () => b) as any
      );
      return (result as any).element as any;
    }
  }

  /**
   * Returns the minimum element in the array.
   *
   * @param by - Optional projection function to transform elements for comparison
   * @returns The element with the minimum value (or minimum projected value)
   *
   * @throws East runtime error if the array is empty
   *
   * @example
   * ```ts
   * const getMin = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
   *   $.return(arr.minimum());
   * });
   * const compiled = East.compile(getMin.toIR(), []);
   * compiled([3n, 1n, 4n, 1n, 5n]);  // 1n
   * // compiled([]) would throw error
   * ```
   *
   * @example
   * ```ts
   * // Getting element by projection
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const getYoungest = East.function([ArrayType(PersonType)], PersonType, ($, people) => {
   *   $.return(people.minimum(($, p, i) => p.age));
   * });
   * const compiled = East.compile(getYoungest.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);
   * // { name: "Bob", age: 25n }
   * ```
   *
   * @see {@link maximum} to find the maximum element.
   * @see {@link findMinimum} to get the index instead (returns Option, safe for empty arrays).
   */
  minimum(by: Expr<FunctionType<[T, IntegerType], any>>): ExprType<T>
  minimum<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(by: F): ExprType<T>
  minimum(): T extends (IntegerType | FloatType | StringType) ? ExprType<T> : never
  minimum(by?: any): ExprType<T> {
    if (by === undefined) {
      // No projection - compare elements directly
      if (!(isDataType(this.value_type as EastType))) {
        throw new Error(`Can only perform minimum on arrays of data types, got ${printType(this.value_type as EastType)}`);
      }
      // Use mapReduce with lambda functions directly
      return this.mapReduce(
        ($, x: any) => x,
        Expr.function([this.value_type, this.value_type], this.value_type as EastType, ($, a: any, b: any) => Expr.min(a, b) as any)
      ) as any;
    } else {
      // With projection - need to track both element and projected value
      const byExpr = (by instanceof Expr ? by : Expr.function([this.value_type, IntegerType], undefined, by)) as CallableFunctionExpr<[T, IntegerType], any>;

      if (byExpr[TypeSymbol].type !== "Function") {
        throw new Error("Expected a Function expression for 'by' parameter");
      }
      const byType = byExpr[TypeSymbol] as FunctionType<any[], any>;
      const projectedType = byType.output as EastType;

      if (!isDataType(projectedType)) {
        throw new Error(`Can only compare data types, got ${printType(projectedType)}`);
      }

      // Map to { element, key }, reduce by comparing keys, extract element
      // Use lessEqual to keep the first element when keys are equal
      const result = this.mapReduce(
        ($, x: any, k: any) => ({ element: x, key: byExpr(x as any, k) }),
        ($, a: any, b: any) => Expr.lessEqual(a.key, b.key).ifElse(() => a, () => b) as any
      );
      return (result as any).element as any;
    }
  }

  /**
   * Joins string array elements with a delimiter.
   *
   * @param string - The delimiter string to insert between elements
   * @returns A StringExpr with all elements joined
   *
   * @remarks
   * This method only works on arrays of strings.
   *
   * @example
   * ```ts
   * const joinStrings = East.function([ArrayType(StringType), StringType], StringType, ($, arr, delimiter) => {
   *   $.return(arr.stringJoin(delimiter));
   * });
   * const compiled = East.compile(joinStrings.toIR(), []);
   * compiled(["a", "b", "c"], ", ");  // "a, b, c"
   * compiled(["hello", "world"], " "); // "hello world"
   * compiled([], ", ");                // ""
   * ```
   */
  stringJoin(string: T extends StringType ? Expr<StringType> | string : never): StringExpr {
    if (!isTypeEqual(this.value_type as EastType, StringType)) {
      throw new Error(`Can only perform stringJoin on array of strings - try using map to convert the values to strings first`);
    }

    const stringAst = valueOrExprToAstTyped(string, StringType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "ArrayStringJoin",
      type_parameters: [],
      arguments: [this[AstSymbol], stringAst],
    }) as StringExpr;
  }

  /**
   * Converts the array to a set, keeping only unique values.
   *
   * @param keyFn - Optional function to project elements to set keys (defaults to the elements themselves)
   * @returns A SetExpr containing unique values
   *
   * @remarks
   * Duplicates are automatically ignored. Later values with the same key overwrite earlier ones.
   *
   * @example
   * ```ts
   * const uniqueNumbers = East.function([ArrayType(IntegerType)], SetType(IntegerType), ($, arr) => {
   *   $.return(arr.toSet());
   * });
   * const compiled = East.compile(uniqueNumbers.toIR(), []);
   * compiled([1n, 2n, 3n, 2n, 1n]);  // Set{1n, 2n, 3n}
   * ```
   *
   * @example
   * ```ts
   * // Project to keys
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   * const uniqueAges = East.function([ArrayType(PersonType)], SetType(IntegerType), ($, people) => {
   *   $.return(people.toSet(($, p, i) => p.age));
   * });
   * const compiled = East.compile(uniqueAges.toIR(), []);
   * compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }, { name: "Carol", age: 30n }]);
   * // Set{25n, 30n}
   * ```
   */
  toSet<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): SetExpr<K2>
  toSet<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(keyFn: KeyFn): SetExpr<TypeOf<ReturnType<KeyFn>>>;
  toSet(): SetExpr<T>
  toSet(keyFn?: any): SetExpr<any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));

    const keyType = keyFnAst.type.output as EastType;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: SetType(keyType as EastType),
      location: get_location(),
      builtin: "ArrayToSet",
      type_parameters: [this.value_type as EastType, keyType as EastType],
      arguments: [this[AstSymbol], keyFnAst],
    }) as SetExpr<any>;
  }

  /**
   * Converts the array to a dictionary.
   *
   * @param keyFn - Optional function to project elements to dict keys (defaults to array indices)
   * @param valueFn - Optional function to project elements to dict values (defaults to the elements themselves)
   * @param onConflict - Optional function to handle duplicate keys (defaults to throwing an error)
   * @returns A DictExpr mapping keys to values
   *
   * @throws East runtime error if duplicate keys are produced and no onConflict function is provided
   *
   * @example
   * ```ts
   * const indexToValue = East.function([ArrayType(StringType)], DictType(IntegerType, StringType), ($, arr) => {
   *   $.return(arr.toDict());
   * });
   * const compiled = East.compile(indexToValue.toIR(), []);
   * compiled(["a", "b", "c"]);  // Dict{0n: "a", 1n: "b", 2n: "c"}
   * ```
   *
   * @example
   * ```ts
   * // Custom key and value projection
   * const PersonType = StructType({ id: IntegerType, name: StringType });
   * const idToName = East.function([ArrayType(PersonType)], DictType(IntegerType, StringType), ($, people) => {
   *   $.return(people.toDict(($, p, i) => p.id, ($, p, i) => p.name));
   * });
   * const compiled = East.compile(idToName.toIR(), []);
   * compiled([{ id: 1n, name: "Alice" }, { id: 2n, name: "Bob" }]);
   * // Dict{1n: "Alice", 2n: "Bob"}
   *
   * // With conflict handler
   * const mergeOnConflict = East.function([ArrayType(PersonType)], DictType(IntegerType, StringType), ($, people) => {
   *   $.return(people.toDict(
   *     ($, p, i) => p.id,
   *     ($, p, i) => p.name,
   *     ($, existing, newVal, key) => existing.concat(" & ").concat(newVal)
   *   ));
   * });
   * ```
   */
  toDict<K2, T2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: Expr<FunctionType<[T, IntegerType], T2>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<T2>, NoInfer<T2>, NoInfer<K2>], NoInfer<T2>>>): DictExpr<K2, T2>
  toDict<K2, ValueFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: ValueFn, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, NoInfer<K2>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<K2, TypeOf<ReturnType<ValueFn>>>;
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any), T2>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, IntegerType], T2>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<T2>, NoInfer<T2>, TypeOf<ReturnType<NoInfer<KeyFn>>>], NoInfer<T2>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, T2>
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any), ValueFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(keyFn: KeyFn, valueFn: ValueFn, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, NoInfer<TypeOf<ReturnType<NoInfer<KeyFn>>>>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<ValueFn>>>;
  toDict<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): DictExpr<K2, T>
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, T>;
  toDict(): DictExpr<IntegerType, T>
  toDict(keyFn?: any, valueFn?: any, onConflictFn?: any): DictExpr<any, any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn ?? ((_$: any, x: any, i: any) => i), FunctionType([this.value_type, IntegerType], undefined));
    const keyType = keyFnAst.type.output as EastType;

    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    const valueType = valueFnAst.type.output as EastType;

    let onConflictAst;
    if (onConflictFn === undefined) {
      const location = get_location();
      const onConflictFunction = Expr.function([valueType, valueType, keyType], valueType, ($, existing, value, key) => $.error(Expr.str`Cannot insert duplicate key ${key} into dict`, location));
      onConflictAst = Expr.ast(onConflictFunction);
    } else {
      onConflictAst = valueOrExprToAstTyped(onConflictFn as any, FunctionType([valueType, valueType, keyType], valueType));
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: DictType(keyType, valueType),
      location: get_location(),
      builtin: "ArrayToDict",
      type_parameters: [this.value_type as EastType, keyType, valueType],
      arguments: [this[AstSymbol], keyFnAst, valueFnAst, onConflictAst],
    }) as DictExpr<any, any>;
  }

  /**
   * Maps each element to an array and flattens the result into a single array.
   *
   * @param fn - Optional function to project elements to arrays (omit if already an array-of-arrays)
   * @returns A flattened ArrayExpr
   *
   * @remarks
   * This is more efficient than using `map` followed by `concat`, as it only iterates once.
   *
   * @example
   * ```ts
   * const flattenArrays = East.function([ArrayType(ArrayType(IntegerType))], ArrayType(IntegerType), ($, arr) => {
   *   $.return(arr.flatMap());
   * });
   * const compiled = East.compile(flattenArrays.toIR(), []);
   * compiled([[1n, 2n], [3n, 4n], [5n]]);  // [1n, 2n, 3n, 4n, 5n]
   * ```
   *
   * @example
   * ```ts
   * // Map and flatten in one step
   * const PersonType = StructType({ name: StringType, friends: ArrayType(StringType) });
   * const allFriends = East.function([ArrayType(PersonType)], ArrayType(StringType), ($, people) => {
   *   $.return(people.flatMap(($, p, i) => p.friends));
   * });
   * const compiled = East.compile(allFriends.toIR(), []);
   * compiled([
   *   { name: "Alice", friends: ["Bob", "Carol"] },
   *   { name: "Bob", friends: ["Alice"] }
   * ]);  // ["Bob", "Carol", "Alice"]
   * ```
   *
   * @see {@link map} to only map values, {@link concat} to only concatenate arrays
   * @see {@link flattenToSet} to flatten to a set instead, {@link flattenToDict} to flatten to a dictionary
   */
  flatMap<T2>(fn: Expr<FunctionType<[T, IntegerType], ArrayType<T2>>>): ArrayExpr<T2>;
  flatMap<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(fn: F): TypeOf<ReturnType<F>> extends ArrayType<infer U> ? ArrayExpr<U> : never;
  flatMap(): T extends ArrayType<infer U> ? ArrayExpr<U> : never;
  flatMap(fn?: any): ArrayExpr<any> {
    const fnAst = valueOrExprToAstTyped(fn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));

    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Array") {
      throw new Error(`Expected Function to return an Array type, got ${printType(returnType)}`);
    }
    const elementType = returnType.value;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: ArrayType(elementType as EastType),
      location: get_location(),
      builtin: "ArrayFlattenToArray",
      type_parameters: [this.value_type as EastType, elementType as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as ArrayExpr<any>;
  }

  /**
   * Maps each element to a set and flattens the result into a single set.
   *
   * @param fn - Optional function to project elements to sets (omit if already an array-of-sets)
   * @returns A flattened SetExpr (duplicates removed)
   *
   * @remarks
   * The resulting sets are unioned together. Duplicates are automatically ignored.
   *
   * @example
   * ```ts
   * const flattenSets = East.function([ArrayType(SetType(IntegerType))], SetType(IntegerType), ($, arr) => {
   *   $.return(arr.flattenToSet());
   * });
   * const compiled = East.compile(flattenSets.toIR(), []);
   * compiled([Set{1n, 2n}, Set{2n, 3n}, Set{3n, 4n}]);  // Set{1n, 2n, 3n, 4n}
   * ```
   *
   * @see {@link flatMap} to flatten to an array instead, {@link flattenToDict} to flatten to a dictionary
   * @see {@link toSet} to convert an array to a set without flattening
   */
  flattenToSet<K2>(fn: Expr<FunctionType<[T, IntegerType], SetType<K2>>>): SetExpr<K2>;
  flattenToSet<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(fn: F): TypeOf<ReturnType<F>> extends SetType<infer U> ? SetExpr<U> : never;
  flattenToSet(): T extends SetType<infer U> ? SetExpr<U> : never;
  flattenToSet(fn?: any): SetExpr<any> {
    const fnAst = valueOrExprToAstTyped(fn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    
    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Set") {
      throw new Error(`Expected Function to return a Set type, got ${printType(returnType)}`);
    }
    const elementType = returnType.key;

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: SetType(elementType as EastType),
      location: get_location(),
      builtin: "ArrayFlattenToSet",
      type_parameters: [this.value_type as EastType, elementType as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as SetExpr<any>;
  }

  /**
   * Maps each element to a dictionary and flattens the result into a single dictionary.
   *
   * @param fn - Optional function to project elements to dicts (omit if already an array-of-dicts)
   * @param onConflict - Optional function to handle duplicate keys (defaults to throwing an error)
   * @returns A flattened DictExpr
   *
   * @throws East runtime error if duplicate keys are encountered and no onConflict function is provided
   *
   * @remarks
   * The resulting dictionaries are merged together.
   *
   * @example
   * ```ts
   * const flattenDicts = East.function([ArrayType(DictType(StringType, IntegerType))], DictType(StringType, IntegerType), ($, arr) => {
   *   $.return(arr.flattenToDict());
   * });
   * const compiled = East.compile(flattenDicts.toIR(), []);
   * compiled([Dict{"a": 1n, "b": 2n}, Dict{"c": 3n}]);  // Dict{"a": 1n, "b": 2n, "c": 3n}
   * ```
   *
   * @see {@link flatMap} to flatten to an array instead, {@link flattenToSet} to flatten to a set
   * @see {@link toDict} to convert an array to a dictionary without flattening
   */
  flattenToDict<K2, V2>(fn: Expr<FunctionType<[T, IntegerType], DictType<K2, V2>>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<V2>, NoInfer<V2>, NoInfer<K2>], NoInfer<V2>>>): DictExpr<K2, V2>;
  flattenToDict<F extends (($: BlockBuilder<NeverType>, v: ExprType<T>, k: ExprType<IntegerType>) => any)>(fn: F, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never, TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never, TypeOf<ReturnType<NoInfer<F>>> extends DictType<infer K2, any> ? K2 : never], TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never>>): TypeOf<ReturnType<F>> extends DictType<infer K2, infer V2> ? DictExpr<K2, V2> : never;
  flattenToDict(): T extends DictType<infer K2, infer V2> ? DictExpr<K2, V2> : never;
  flattenToDict(fn?: any, onConflictFn?: any): DictExpr<any, any> {
    const fnAst = valueOrExprToAstTyped(fn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    
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

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: DictType(keyType as EastType, valueType as EastType),
      location: get_location(),
      builtin: "ArrayFlattenToDict",
      type_parameters: [this.value_type as EastType, keyType as EastType, valueType as EastType],
      arguments: [this[AstSymbol], fnAst, onConflictAst],
    }) as DictExpr<any, any>;
  }

  /**
   * Group array elements by a key function, initialize each group, and reduce within each group.
   *
   * This method partitions the array into groups based on a key function, initializes each group
   * with a starting value (which can depend on the group key), and then reduces all elements
   * within each group using an accumulator function.
   *
   * This is useful for computing aggregates per group where you need a custom initial value,
   * such as computing a weighted sum, building complex data structures, or maintaining counters
   * that start from a non-zero value.
   *
   * @param keyFn - Function that computes the grouping key for each element
   * @param initFn - Function that computes the initial value for each group (receives the group key)
   * @param reduceFn - Function that combines the accumulator with each element in the group
   * @returns Dictionary mapping each unique key to its reduced value
   *
   * @example
   * ```ts
   * // Group numbers by even/odd and sum them starting from 100
   * const numbers = East.value([1n, 2n, 3n, 4n]);
   * numbers.groupReduce(
   *   ($, x) => x.remainder(2n),        // key: 0 for even, 1 for odd
   *   ($, key) => 100n,                 // start each group at 100
   *   ($, acc, x) => acc.add(x)         // sum the values
   * )
   * // Result: { 0n: 106n, 1n: 104n }
   * //          even: 100 + 2 + 4 = 106
   * //          odd:  100 + 1 + 3 = 104
   * ```
   *
   * @example
   * ```ts
   * // Group users by department and count them, starting from department size
   * users.groupReduce(
   *   ($, u) => u.department,
   *   ($, dept) => deptSizes.get(dept),    // initial count from base data
   *   ($, count, user, idx) => count.add(1n)
   * )
   * ```
   *
   * @see {@link toDict} to create a dictionary without reduction, or for using a conflict handler instead of reduction.
   * @see {@link reduce} for reducing the entire array without grouping.
   */
  groupReduce<K2, T2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, initFn: Expr<FunctionType<[K2], T2>>, reduceFn: SubtypeExprOrValue<FunctionType<[T2, T, IntegerType], T2>>): DictExpr<K2, T2>
  groupReduce<K2, InitFn extends ($: BlockBuilder<NeverType>, k2: ExprType<NoInfer<K2>>) => any>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, initFn: InitFn, reduceFn: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<InitFn>>>, T, IntegerType], TypeOf<ReturnType<NoInfer<InitFn>>>>>): DictExpr<K2, TypeOf<ReturnType<InitFn>>>
  groupReduce<KeyFn extends ($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any, T2>(keyFn: KeyFn, initFn: Expr<FunctionType<[TypeOf<ReturnType<NoInfer<KeyFn>>>], T2>>, reduceFn: SubtypeExprOrValue<FunctionType<[T2, T, IntegerType], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, T2>
  groupReduce<KeyFn extends ($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any, InitFn extends ($: BlockBuilder<NeverType>, k2: ExprType<TypeOf<ReturnType<NoInfer<KeyFn>>>>) => any>(keyFn: KeyFn, initFn: InitFn, reduceFn: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<InitFn>>>, T, IntegerType], TypeOf<ReturnType<NoInfer<InitFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<InitFn>>>
  groupReduce(keyFn: any, initFn: any, reduceFn: any): Expr {
    // Note - initFn has to be before reduceFn, otherwise the TypeScript type inference doesn't work properly

    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const keyType = keyFnAst.type.output as EastType;
    
    const initFnAst = valueOrExprToAstTyped(initFn, FunctionType([keyType], undefined));
    const initType = initFnAst.type.output as EastType;

    const reduceFnAst = valueOrExprToAstTyped(reduceFn, FunctionType([initType, this.value_type, IntegerType], initType));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: DictType(keyType as EastType, initType as EastType),
      location: get_location(),
      builtin: "ArrayGroupFold",
      type_parameters: [this.value_type as EastType, keyType as EastType, initType as EastType],
      arguments: [this[AstSymbol], keyFnAst, initFnAst, reduceFnAst],
    });
  }

  /**
   * Count the number of elements in each group.
   *
   * Groups elements by a key function and returns a dictionary mapping each unique key
   * to the count of elements in that group.
   *
   * @param keyFn - Function that computes the grouping key for each element (defaults to identity)
   * @returns Dictionary mapping each unique key to the count of elements in that group
   *
   * @example
   * ```ts
   * // Count occurrences of each number
   * [1n, 2n, 1n, 3n, 2n, 1n].groupSize()
   * // Result: { 1n: 3n, 2n: 2n, 3n: 1n }
   *
   * // Group by even/odd and count
   * [1n, 2n, 3n, 4n, 5n, 6n].groupSize(($, x) => x.remainder(2n))
   * // Result: { 0n: 3n, 1n: 3n }
   * ```
   *
   * @see {@link groupToArrays} to collect elements instead of counting them.
   */
  groupSize<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): DictExpr<K2, IntegerType>
  groupSize<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, IntegerType>
  groupSize(): DictExpr<T, IntegerType>
  groupSize(keyFn?: any): DictExpr<any, IntegerType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    return this.toDict(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      ((_$: any) => 1n) as any,
      ((_$: any, a: any, b: any) => a.add(b)) as any
    );
  }

  /**
   * Check if every element in each group satisfies a predicate.
   *
   * @param keyFn - Function that computes the grouping key
   * @param predFn - Predicate function to test each element
   * @returns Dictionary mapping each key to true if all elements in that group satisfy the predicate
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n, 5n, 6n].groupEvery(
   *   ($, x) => x.remainder(2n),
   *   ($, x) => x.greater(0n)
   * )
   * // Result: { 0n: true, 1n: true }
   * ```
   */
  groupEvery<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, predFn: SubtypeExprOrValue<FunctionType<[T, IntegerType], BooleanType>>): DictExpr<K2, BooleanType>
  groupEvery<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, predFn: SubtypeExprOrValue<FunctionType<[T, IntegerType], BooleanType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, BooleanType>
  groupEvery(keyFn: any, predFn: any): DictExpr<any, BooleanType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const predFnAst = valueOrExprToAstTyped(predFn, FunctionType([this.value_type, IntegerType], BooleanType));
    return this.groupReduce(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      (() => true) as any,
      ((_$: any, acc: BooleanExpr, elem: any, idx: any) => {
        const pred = Expr.fromAst(predFnAst)(elem, idx) as BooleanExpr;
        return acc.and(() => pred);
      }) as any
    );
  }

  /**
   * Check if any element in each group satisfies a predicate.
   *
   * @param keyFn - Function that computes the grouping key
   * @param predFn - Predicate function to test each element
   * @returns Dictionary mapping each key to true if at least one element in that group satisfies the predicate
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n].groupSome(
   *   ($, x) => x.remainder(2n),
   *   ($, x) => x.greater(3n)
   * )
   * // Result: { 0n: true, 1n: false }
   * ```
   */
  groupSome<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, predFn: SubtypeExprOrValue<FunctionType<[T, IntegerType], BooleanType>>): DictExpr<K2, BooleanType>
  groupSome<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, predFn: SubtypeExprOrValue<FunctionType<[T, IntegerType], BooleanType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, BooleanType>
  groupSome(keyFn: any, predFn: any): DictExpr<any, BooleanType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const predFnAst = valueOrExprToAstTyped(predFn, FunctionType([this.value_type, IntegerType], BooleanType));
    return this.groupReduce(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      (() => false) as any,
      ((_$: any, acc: BooleanExpr, elem: any, idx: any) => {
        const pred = Expr.fromAst(predFnAst)(elem, idx) as BooleanExpr;
        return acc.or(() => pred);
      }) as any
    );
  }

  /**
   * Find all indices where a value matches, grouped by key.
   *
   * @param keyFn - Function that computes the grouping key
   * @param value - The value to search for
   * @param projFn - Optional projection function to extract the value to compare
   * @returns Dictionary mapping each key to an array of matching indices
   *
   * @example
   * ```ts
   * // Without projection - find all occurrences of value 2
   * [1n, 2n, 3n, 2n, 5n, 2n].groupFindAll(
   *   ($, x) => x.remainder(2n),
   *   2n
   * )
   * // Result: { 0n: [1n, 3n, 5n], 1n: [] }
   *
   * // With projection - find all orders in "CA" grouped by customer
   * orders.groupFindAll(
   *   ($, o) => o.customer,
   *   "CA",
   *   ($, o) => o.state
   * )
   * ```
   */
  groupFindAll<K2, T2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, value: SubtypeExprOrValue<T2>, projFn: Expr<FunctionType<[T, IntegerType], T2>>): DictExpr<K2, ArrayType<IntegerType>>
  groupFindAll<K2, ProjFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, value: ValueTypeOf<TypeOf<ReturnType<NoInfer<ProjFn>>>>, projFn: ProjFn): DictExpr<K2, ArrayType<IntegerType>>
  groupFindAll<K2, ProjFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, value: Expr<SubType<TypeOf<ReturnType<NoInfer<ProjFn>>>>>, projFn: ProjFn): DictExpr<K2, ArrayType<IntegerType>>
  groupFindAll<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), T2>(keyFn: KeyFn, value: SubtypeExprOrValue<T2>, projFn: Expr<FunctionType<[T, IntegerType], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<IntegerType>>
  groupFindAll<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ProjFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, value: ValueTypeOf<TypeOf<ReturnType<NoInfer<ProjFn>>>>, projFn: ProjFn): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<IntegerType>>
  groupFindAll<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ProjFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, value: Expr<SubType<TypeOf<ReturnType<NoInfer<ProjFn>>>>>, projFn: ProjFn): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<IntegerType>>
  groupFindAll<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, value: SubtypeExprOrValue<T>): DictExpr<K2, ArrayType<IntegerType>>
  groupFindAll<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, value: SubtypeExprOrValue<T>): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<IntegerType>>
  groupFindAll(keyFn: any, value: any, projFn?: any): DictExpr<any, ArrayType<IntegerType>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);

    if (projFn === undefined) {
      // Without projection: find where element == value
      return this.groupReduce(
        ((_$: any, elem: any, idx: any) => keyFnExpr(elem, idx)) as any,
        ((_$: any, _key: any) => Expr.from([], ArrayType(IntegerType))) as any,
        (($: any, acc: any, elem: any, idx: any) => {
          $.if(Expr.equal(elem, value), ($: any) => $(acc.pushLast(idx)));
          return acc;
        }) as any
      );
    } else {
      // With projection: find where projFn(element) == value
      const projFnExpr = (projFn instanceof Expr ? projFn : Expr.function([this.value_type, IntegerType], undefined, projFn)) as CallableFunctionExpr<[T, IntegerType], any>;
      if (projFnExpr[TypeSymbol].type !== "Function") {
        throw new Error("Expected a Function expression for 'projFn' parameter");
      }
      return this.groupReduce(
        ((_$: any, elem: any, idx: any) => keyFnExpr(elem, idx)) as any,
        ((_$: any, _key: any) => Expr.from([], ArrayType(IntegerType))) as any,
        (($: any, acc: any, elem: any, idx: any) => {
          $.if(Expr.equal(projFnExpr(elem as any, idx), value), ($: any) => $(acc.pushLast(idx)));
          return acc;
        }) as any
      );
    }
  }

  /**
   * Find the first index where a value matches, grouped by key.
   *
   * @param keyFn - Function that computes the grouping key
   * @param value - The value to search for
   * @param projFn - Optional projection function to extract the value to compare
   * @returns Dictionary mapping each key to an Option containing the first matching index
   *
   * @example
   * ```ts
   * // Without projection - find value 4
   * [1n, 2n, 3n, 4n, 5n, 6n].groupFindFirst(
   *   ($, x) => x.remainder(2n),
   *   4n
   * )
   * // Result: { 0n: some(3n), 1n: none }
   *
   * // With projection - find orders in "CA" grouped by customer
   * orders.groupFindFirst(
   *   ($, o) => o.customer,
   *   "CA",
   *   ($, o) => o.state
   * )
   * ```
   */
  groupFindFirst<K2, T2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, value: SubtypeExprOrValue<T2>, projFn: Expr<FunctionType<[T, IntegerType], T2>>): DictExpr<K2, OptionType<IntegerType>>
  groupFindFirst<K2, ProjFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, value: ValueTypeOf<TypeOf<ReturnType<NoInfer<ProjFn>>>>, projFn: ProjFn): DictExpr<K2, OptionType<IntegerType>>
  groupFindFirst<K2, ProjFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, value: Expr<SubType<TypeOf<ReturnType<NoInfer<ProjFn>>>>>, projFn: ProjFn): DictExpr<K2, OptionType<IntegerType>>
  groupFindFirst<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), T2>(keyFn: KeyFn, value: SubtypeExprOrValue<T2>, projFn: Expr<FunctionType<[T, IntegerType], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, OptionType<IntegerType>>
  groupFindFirst<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ProjFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, value: ValueTypeOf<TypeOf<ReturnType<NoInfer<ProjFn>>>>, projFn: ProjFn): DictExpr<TypeOf<ReturnType<KeyFn>>, OptionType<IntegerType>>
  groupFindFirst<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ProjFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, value: Expr<SubType<TypeOf<ReturnType<NoInfer<ProjFn>>>>>, projFn: ProjFn): DictExpr<TypeOf<ReturnType<KeyFn>>, OptionType<IntegerType>>
  groupFindFirst<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, value: SubtypeExprOrValue<T>): DictExpr<K2, OptionType<IntegerType>>
  groupFindFirst<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, value: SubtypeExprOrValue<T>): DictExpr<TypeOf<ReturnType<KeyFn>>, OptionType<IntegerType>>
  groupFindFirst(keyFn: any, value: any, projFn?: any): DictExpr<any, OptionType<IntegerType>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);

    if (projFn === undefined) {
      // Without projection: find where element == value
      return this.groupReduce(
        ((_$: any, elem: any, idx: any) => keyFnExpr(elem, idx)) as any,
        ((_$: any, _key: any) => Expr.from(none, OptionType(IntegerType))) as any,
        ((_$: any, acc: any, elem: any, idx: any) => {
          const isSome = (acc as any).hasTag("some") as BooleanExpr;
          return isSome.ifElse(
            () => acc,
            () => Expr.equal(elem, value).ifElse(
              () => some(idx),
              () => Expr.from(none, OptionType(IntegerType))
            )
          );
        }) as any
      );
    } else {
      // With projection: find where projFn(element) == value
      const projFnExpr = (projFn instanceof Expr ? projFn : Expr.function([this.value_type, IntegerType], undefined, projFn)) as CallableFunctionExpr<[T, IntegerType], any>;
      if (projFnExpr[TypeSymbol].type !== "Function") {
        throw new Error("Expected a Function expression for 'projFn' parameter");
      }
      return this.groupReduce(
        ((_$: any, elem: any, idx: any) => keyFnExpr(elem, idx)) as any,
        ((_$: any, _key: any) => Expr.from(none, OptionType(IntegerType))) as any,
        ((_$: any, acc: any, elem: any, idx: any) => {
          const isSome = (acc as any).hasTag("some") as BooleanExpr;
          return isSome.ifElse(
            () => acc,
            () => Expr.equal(projFnExpr(elem as any, idx), value).ifElse(
              () => some(idx),
              () => Expr.from(none, OptionType(IntegerType))
            )
          );
        }) as any
      );
    }
  }

  /**
   * Find the index of the minimum element in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param byFn - Optional projection function for comparison
   * @returns Dictionary mapping each key to the index of the minimum element in that group
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n, 5n, 6n].groupFindMinimum(($, x) => x.remainder(2n))
   * // Result: { 0n: 1n, 1n: 0n }
   * ```
   */
  groupFindMinimum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, byFn?: SubtypeExprOrValue<FunctionType<[T, IntegerType], any>>): DictExpr<K2, IntegerType>
  groupFindMinimum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, byFn?: SubtypeExprOrValue<FunctionType<[T, IntegerType], any>>): DictExpr<TypeOf<ReturnType<KeyFn>>, IntegerType>
  groupFindMinimum(keyFn: any, byFn?: any): DictExpr<any, IntegerType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const byFnAst = valueOrExprToAstTyped(byFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    return this.toDict(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      ((_$: any, elem: any, idx: any) => ({ by: Expr.fromAst(byFnAst)(elem, idx), index: idx })) as any,
      ((_$: any, a: any, b: any) => Expr.lessEqual(a.by, b.by).ifElse(() => a, () => b)) as any
    ).map(((_$: any, v: any) => v.index) as any) as any;
  }

  /**
   * Find the index of the maximum element in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param byFn - Optional projection function for comparison
   * @returns Dictionary mapping each key to the index of the maximum element in that group
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n, 5n, 6n].groupFindMaximum(($, x) => x.remainder(2n))
   * // Result: { 0n: 5n, 1n: 4n }
   * ```
   */
  groupFindMaximum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, byFn?: SubtypeExprOrValue<FunctionType<[T, IntegerType], any>>): DictExpr<K2, IntegerType>
  groupFindMaximum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, byFn?: SubtypeExprOrValue<FunctionType<[T, IntegerType], any>>): DictExpr<TypeOf<ReturnType<KeyFn>>, IntegerType>
  groupFindMaximum(keyFn: any, byFn?: any): DictExpr<any, IntegerType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const byFnAst = valueOrExprToAstTyped(byFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    return this.toDict(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      ((_$: any, elem: any, idx: any) => ({ by: Expr.fromAst(byFnAst)(elem, idx), index: idx })) as any,
      ((_$: any, a: any, b: any) => Expr.greaterEqual(a.by, b.by).ifElse(() => a, () => b)) as any
    ).map(((_$: any, v: any) => v.index) as any) as any;
  }

  /**
   * Sum elements in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values to sum
   * @returns Dictionary mapping each key to the sum of elements in that group
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n].groupSum(($, x) => x.remainder(2n))
   * // Result: { 0n: 6n, 1n: 4n }
   * ```
   */
  groupSum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: Expr<FunctionType<[T, IntegerType], IntegerType>>): DictExpr<K2, IntegerType>
  groupSum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: Expr<FunctionType<[T, IntegerType], FloatType>>): DictExpr<K2, FloatType>
  groupSum<K2, ValueFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: ValueFn): DictExpr<K2, TypeOf<ReturnType<ValueFn>>>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, IntegerType], IntegerType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, IntegerType>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, IntegerType], FloatType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ValueFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<ValueFn>>>
  groupSum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): T extends IntegerType | FloatType ? DictExpr<K2, T> : never
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn): T extends IntegerType | FloatType ? DictExpr<TypeOf<ReturnType<KeyFn>>, T> : never
  groupSum(keyFn: any, valueFn?: any): DictExpr<any, any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    const valueType = valueFnAst.type.output as EastType;
    const isInteger = isTypeEqual(valueType, IntegerType);
    const isFloat = isTypeEqual(valueType, FloatType);
    if (!isInteger && !isFloat) {
      throw new Error(`Can only perform groupSum on Integer or Float values, got ${printType(valueType)}`);
    }
    return this.toDict(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      ((_$: any, elem: any, idx: any) => Expr.fromAst(valueFnAst)(elem, idx)) as any,
      ((_$: any, a: any, b: any) => a.add(b)) as any
    );
  }

  /**
   * Compute the mean of elements in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values
   * @returns Dictionary mapping each key to the mean of elements in that group
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n].groupMean(($, x) => x.remainder(2n))
   * // Result: { 0n: 3.0, 1n: 2.0 }
   * ```
   */
  groupMean<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: Expr<FunctionType<[T, IntegerType], IntegerType | FloatType>>): DictExpr<K2, FloatType>
  groupMean<K2, ValueFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: ValueFn): DictExpr<K2, FloatType>
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, IntegerType], IntegerType | FloatType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ValueFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupMean<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): T extends IntegerType | FloatType ? DictExpr<K2, FloatType> : never
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn): T extends IntegerType | FloatType ? DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType> : never
  groupMean(keyFn: any, valueFn?: any): DictExpr<any, FloatType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    const valueType = valueFnAst.type.output as EastType;
    const isInteger = isTypeEqual(valueType, IntegerType);
    const isFloat = isTypeEqual(valueType, FloatType);
    if (!isInteger && !isFloat) {
      throw new Error(`Can only perform groupMean on Integer or Float values, got ${printType(valueType)}`);
    }
    return this.toDict(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      ((_$: any, elem: any, idx: any) => {
        const val = Expr.fromAst(valueFnAst)(elem, idx);
        return { sum: isInteger ? (val as IntegerExpr).toFloat() : val, count: 1n };
      }) as any,
      ((_$: any, a: any, b: any) => ({ sum: a.sum.add(b.sum), count: a.count.add(b.count) })) as any
    ).map(((_$: any, v: any) => v.sum.divide(v.count.toFloat())) as any) as any;
  }

  /**
   * Collect elements in each group into arrays.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values
   * @returns Dictionary mapping each key to an array of elements in that group
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n].groupToArrays(($, x) => x.remainder(2n))
   * // Result: { 0n: [2n, 4n], 1n: [1n, 3n] }
   * ```
   */
  groupToArrays<K2, T2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: Expr<FunctionType<[T, IntegerType], T2>>): DictExpr<K2, ArrayType<T2>>
  groupToArrays<K2, ValueFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: ValueFn): DictExpr<K2, ArrayType<TypeOf<ReturnType<ValueFn>>>>
  groupToArrays<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), T2>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, IntegerType], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<T2>>
  groupToArrays<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ValueFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<TypeOf<ReturnType<ValueFn>>>>
  groupToArrays<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): DictExpr<K2, ArrayType<T>>
  groupToArrays<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<T>>
  groupToArrays(keyFn: any, valueFn?: any): DictExpr<any, ArrayType<any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);
    const valueFnExpr = Expr.fromAst(valueFnAst);
    const valueType = valueFnAst.type.output as EastType;
    return this.groupReduce(
      ((_$: any, elem: any, idx: any) => keyFnExpr(elem, idx)) as any,
      ((_$: any, _key: any) => Expr.from([], ArrayType(valueType))) as any,
      (($: any, acc: any, elem: any, idx: any) => {
        const val = valueFnExpr(elem, idx);
        $(acc.pushLast(val));
        return acc;
      }) as any
    );
  }

  /**
   * Collect elements in each group into sets.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values
   * @returns Dictionary mapping each key to a set of elements in that group
   *
   * @example
   * ```ts
   * [1n, 2n, 1n, 2n].groupToSets(($, x) => x.remainder(2n))
   * // Result: { 0n: Set([2n]), 1n: Set([1n]) }
   * ```
   */
  groupToSets<K2, T2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: Expr<FunctionType<[T, IntegerType], T2>>): DictExpr<K2, SetType<T2>>
  groupToSets<K2, ValueFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: ValueFn): DictExpr<K2, SetType<TypeOf<ReturnType<ValueFn>>>>
  groupToSets<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), T2>(keyFn: KeyFn, valueFn: Expr<FunctionType<[T, IntegerType], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, SetType<T2>>
  groupToSets<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ValueFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, SetType<TypeOf<ReturnType<ValueFn>>>>
  groupToSets<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): DictExpr<K2, SetType<T>>
  groupToSets<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, SetType<T>>
  groupToSets(keyFn: any, valueFn?: any): DictExpr<any, SetType<any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);
    const valueFnExpr = Expr.fromAst(valueFnAst);
    const valueType = valueFnAst.type.output as EastType;
    return this.groupReduce(
      ((_$: any, elem: any, idx: any) => keyFnExpr(elem, idx)) as any,
      ((_$: any, _key: any) => Expr.from(new Set<any>(), SetType(valueType))) as any,
      (($: any, acc: any, elem: any, idx: any) => {
        const val = valueFnExpr(elem, idx);
        $(acc.tryInsert(val));
        return acc;
      }) as any
    );
  }

  /**
   * Find the minimum element in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param byFn - Optional projection function for comparison
   * @returns Dictionary mapping each key to the minimum element in that group
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n].groupMinimum(($, x) => x.remainder(2n))
   * // Result: { 0n: 2n, 1n: 1n }
   * ```
   */
  groupMinimum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, byFn: Expr<FunctionType<[T, IntegerType], any>>): DictExpr<K2, T>
  groupMinimum<K2, ByFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, byFn: ByFn): DictExpr<K2, T>
  groupMinimum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, byFn: Expr<FunctionType<[T, IntegerType], any>>): DictExpr<TypeOf<ReturnType<KeyFn>>, T>
  groupMinimum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ByFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, byFn: ByFn): DictExpr<TypeOf<ReturnType<KeyFn>>, T>
  groupMinimum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): DictExpr<K2, T>
  groupMinimum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, T>
  groupMinimum(keyFn: any, byFn?: any): DictExpr<any, T> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const byFnAst = valueOrExprToAstTyped(byFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    return this.toDict(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      ((_$: any, elem: any, idx: any) => ({ by: Expr.fromAst(byFnAst)(elem, idx), elem })) as any,
      ((_$: any, a: any, b: any) => Expr.lessEqual(a.by, b.by).ifElse(() => a, () => b)) as any
    ).map(((_$: any, v: any) => v.elem) as any) as any;
  }

  /**
   * Find the maximum element in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param byFn - Optional projection function for comparison
   * @returns Dictionary mapping each key to the maximum element in that group
   *
   * @example
   * ```ts
   * [1n, 2n, 3n, 4n].groupMaximum(($, x) => x.remainder(2n))
   * // Result: { 0n: 4n, 1n: 3n }
   * ```
   */
  groupMaximum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, byFn: Expr<FunctionType<[T, IntegerType], any>>): DictExpr<K2, T>
  groupMaximum<K2, ByFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>, byFn: ByFn): DictExpr<K2, T>
  groupMaximum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, byFn: Expr<FunctionType<[T, IntegerType], any>>): DictExpr<TypeOf<ReturnType<KeyFn>>, T>
  groupMaximum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any), ByFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, byFn: ByFn): DictExpr<TypeOf<ReturnType<KeyFn>>, T>
  groupMaximum<K2>(keyFn: Expr<FunctionType<[T, IntegerType], K2>>): DictExpr<K2, T>
  groupMaximum<KeyFn extends (($: BlockBuilder<NeverType>, x: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, T>
  groupMaximum(keyFn: any, byFn?: any): DictExpr<any, T> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const byFnAst = valueOrExprToAstTyped(byFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
    return this.toDict(
      ((_$: any, elem: any, idx: any) => Expr.fromAst(keyFnAst)(elem, idx)) as any,
      ((_$: any, elem: any, idx: any) => ({ by: Expr.fromAst(byFnAst)(elem, idx), elem })) as any,
      ((_$: any, a: any, b: any) => Expr.greaterEqual(a.by, b.by).ifElse(() => a, () => b)) as any
    ).map(((_$: any, v: any) => v.elem) as any) as any;
  }

  /**
   * Group elements into nested dictionaries.
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
   * users.groupToDicts(
   *   ($, u) => u.department,
   *   ($, u) => u.role
   * )
   * // Result: { "eng": { "dev": user1, "lead": user2 }, "sales": { "rep": user3 } }
   *
   * // With conflict handler - merges duplicate keys
   * orders.groupToDicts(
   *   ($, o) => o.customer,
   *   ($, o) => o.product,
   *   ($, o) => o.quantity,
   *   ($, a, b) => a.add(b)
   * )
   * // Sums quantities for same customer+product
   * ```
   */
  groupToDicts<K1, K2, T2>(keyFn: Expr<FunctionType<[T, IntegerType], K1>>, keyFn2: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: Expr<FunctionType<[T, IntegerType], T2>>, combineFn?: SubtypeExprOrValue<FunctionType<[T2, T2, K1], T2>>): DictExpr<K1, DictType<K2, T2>>
  groupToDicts<K1, K2, ValueFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K1>>, keyFn2: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: ValueFn, combineFn?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, K1], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<K1, DictType<K2, TypeOf<ReturnType<ValueFn>>>>
  groupToDicts<K1, KeyFn2 extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), T2>(keyFn: Expr<FunctionType<[T, IntegerType], K1>>, keyFn2: KeyFn2, valueFn: Expr<FunctionType<[T, IntegerType], T2>>, combineFn?: SubtypeExprOrValue<FunctionType<[T2, T2, K1], T2>>): DictExpr<K1, DictType<TypeOf<ReturnType<KeyFn2>>, T2>>
  groupToDicts<K1, KeyFn2 extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), ValueFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K1>>, keyFn2: KeyFn2, valueFn: ValueFn, combineFn?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, K1], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<K1, DictType<TypeOf<ReturnType<KeyFn2>>, TypeOf<ReturnType<ValueFn>>>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), K2, T2>(keyFn: KeyFn, keyFn2: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: Expr<FunctionType<[T, IntegerType], T2>>, combineFn?: SubtypeExprOrValue<FunctionType<[T2, T2, TypeOf<ReturnType<NoInfer<KeyFn>>>], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<K2, T2>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), K2, ValueFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, keyFn2: Expr<FunctionType<[T, IntegerType], K2>>, valueFn: ValueFn, combineFn?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<KeyFn>>>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<K2, TypeOf<ReturnType<ValueFn>>>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), KeyFn2 extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), T2>(keyFn: KeyFn, keyFn2: KeyFn2, valueFn: Expr<FunctionType<[T, IntegerType], T2>>, combineFn?: SubtypeExprOrValue<FunctionType<[T2, T2, TypeOf<ReturnType<NoInfer<KeyFn>>>], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<TypeOf<ReturnType<KeyFn2>>, T2>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), KeyFn2 extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), ValueFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, keyFn2: KeyFn2, valueFn: ValueFn, combineFn?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<KeyFn>>>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<TypeOf<ReturnType<KeyFn2>>, TypeOf<ReturnType<ValueFn>>>>
  
  groupToDicts<K1, K2>(keyFn: Expr<FunctionType<[T, IntegerType], K1>>, keyFn2: Expr<FunctionType<[T, IntegerType], K2>>): DictExpr<K1, DictType<K2, T>>
  groupToDicts<K1, KeyFn2 extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(keyFn: Expr<FunctionType<[T, IntegerType], K1>>, keyFn2: KeyFn2): DictExpr<K1, DictType<TypeOf<ReturnType<KeyFn2>>, T>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), K2>(keyFn: KeyFn, keyFn2: Expr<FunctionType<[T, IntegerType], K2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<K2, T>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any), KeyFn2 extends (($: BlockBuilder<NeverType>, v: ExprType<T>, i: IntegerExpr) => any)>(keyFn: KeyFn, keyFn2: KeyFn2): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<TypeOf<ReturnType<KeyFn2>>, T>>
  
  groupToDicts(keyFn: any, keyFn2: any, valueFn?: any, combineFn?: any): DictExpr<any, DictType<any, any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.value_type, IntegerType], undefined));
    const keyFn2Ast = valueOrExprToAstTyped(keyFn2, FunctionType([this.value_type, IntegerType], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.value_type, IntegerType], undefined));
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
        ((_$: any, elem: any, idx: any) => keyFnExpr(elem, idx)) as any,
        ((_$: any, _key: any) => Expr.from(new Map(), DictType(key2Type, valueType))) as any,
        (($: any, dict: any, elem: any, idx: any) => {
          const innerKey = keyFn2Expr(elem, idx);
          const val = valueFnExpr(elem, idx);
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
        ((_$: any, elem: any, idx: any) => keyFnExpr(elem, idx)) as any,
        ((_$: any, _key: any) => Expr.from(new Map(), DictType(key2Type, valueType))) as any,
        (($: any, dict: any, elem: any, idx: any) => {
          const innerKey = keyFn2Expr(elem, idx);
          const val = valueFnExpr(elem, idx);
          $(dict.insert(innerKey, val));
          return dict;
        }) as any
      );
    }
  }

  /**
   * Encodes this array of structs as CSV data.
   *
   * @param options - CSV serialization options
   * @returns A BlobExpr containing the encoded CSV data
   *
   * @remarks Only works on arrays of structs with primitive or optional primitive fields.
   *
   * @example
   * ```ts
   * const PersonType = StructType({ name: StringType, age: IntegerType });
   *
   * const toCsv = East.function([ArrayType(PersonType)], BlobType, ($, people) => {
   *   $.return(people.encodeCsv({ delimiter: ',' }));
   * });
   * const compiled = East.compile(toCsv.toIR(), []);
   * const blob = compiled([{ name: "Alice", age: 30n }, { name: "Bob", age: 25n }]);
   * new TextDecoder().decode(blob);  // "name,age\r\nAlice,30\r\nBob,25"
   * ```
   */
  encodeCsv(options?: CsvSerializeOptions): BlobExpr {
    // Convert options to East config value
    const configValue = csvSerializeOptionsToValue(options);
    const configAst = valueOrExprToAstTyped(configValue, CsvSerializeConfigType);

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BlobType,
      location: get_location(),
      builtin: "ArrayEncodeCsv",
      type_parameters: [this.value_type as EastType, CsvSerializeConfigType],
      arguments: [this[AstSymbol], configAst],
    }) as BlobExpr;
  }

  /**
   * Checks if this array equals another array (deep comparison).
   *
   * @param other - The array to compare against
   * @returns A BooleanExpr that is true if the arrays are deeply equal
   *
   * @example
   * ```ts
   * const isEqual = East.function([ArrayType(IntegerType), ArrayType(IntegerType)], BooleanType, ($, a, b) => {
   *   $.return(a.equals(b));
   * });
   * const compiled = East.compile(isEqual.toIR(), []);
   * compiled([1n, 2n, 3n], [1n, 2n, 3n]);  // true
   * compiled([1n, 2n], [1n, 2n, 3n]);      // false
   * ```
   */
  equals(other: ArrayExpr<T> | SubtypeExprOrValue<T>[]): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this array does not equal another array.
   *
   * @param other - The array to compare against
   * @returns A BooleanExpr that is true if the arrays are not equal
   *
   * @example
   * ```ts
   * const isNotEqual = East.function([ArrayType(IntegerType), ArrayType(IntegerType)], BooleanType, ($, a, b) => {
   *   $.return(a.notEquals(b));
   * });
   * const compiled = East.compile(isNotEqual.toIR(), []);
   * compiled([1n, 2n], [1n, 2n, 3n]);      // true
   * compiled([1n, 2n, 3n], [1n, 2n, 3n]);  // false
   * ```
   */
  notEquals(other: ArrayExpr<T> | SubtypeExprOrValue<T>[]): BooleanExpr {
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
