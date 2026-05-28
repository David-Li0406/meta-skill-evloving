/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { SetType, BooleanType, FunctionType, IntegerType, type EastType, NullType, NeverType, DictType, printType, FloatType, isTypeEqual, ArrayType, VariantType, StringType } from "../types.js";
import { valueOrExprToAst, valueOrExprToAstTyped } from "./ast.js";
import type { BooleanExpr } from "./boolean.js";
import { equal, notEqual } from "./block.js";
import type { IntegerExpr } from "./integer.js";
import { AstSymbol, Expr, TypeSymbol, type ToExpr } from "./expr.js";
import type { ExprType, SubtypeExprOrValue, TypeOf } from "./types.js";
import type { NullExpr } from "./null.js";
import type { DictExpr } from "./dict.js";
import type { BlockBuilder } from "./block.js";
import type { FloatExpr } from "./float.js";
import type { ArrayExpr } from "./array.js";
import { none, some } from "../containers/variant.js";

/**
 * Expression representing set (sorted unique collection) values and operations.
 *
 * SetExpr provides methods for working with sorted sets including membership testing, insertion,
 * deletion, iteration, mapping, filtering, set operations (union, intersection, difference), and
 * aggregation operations. Sets maintain their elements sorted by key using East's total ordering
 * and guarantee uniqueness.
 *
 * @example
 * ```ts
 * // Creating and manipulating sets
 * const buildSet = East.function([ArrayType(StringType)], SetType(StringType), ($, items) => {
 *   const uniqueItems = Expr.from(new Set(), SetType(StringType));
 *   $(items.forEach(($, item) => {
 *     $(uniqueItems.tryInsert(item));
 *   }));
 *   $.return(uniqueItems);
 * });
 * const compiled = East.compile(buildSet.toIR(), []);
 * compiled(["apple", "banana", "apple", "cherry"]);  // Set(["apple", "banana", "cherry"])
 * ```
 *
 * @example
 * ```ts
 * // Set operations
 * const unionSets = East.function([SetType(IntegerType), SetType(IntegerType)], SetType(IntegerType), ($, set1, set2) => {
 *   $.return(set1.union(set2));
 * });
 * const compiled = East.compile(unionSets.toIR(), []);
 * compiled(new Set([1n, 2n, 3n]), new Set([3n, 4n, 5n]));  // Set([1n, 2n, 3n, 4n, 5n])
 * ```
 */
export class SetExpr<K extends any> extends Expr<SetType<K>> {
  constructor(private key_type: K, ast: AST, createExpr: ToExpr) {
    super(ast.type as SetType<K>, ast, createExpr);
  }

  /**
   * Returns the number of elements in the set.
   *
   * @returns An IntegerExpr representing the count of elements
   *
   * @example
   * ```ts
   * const getSize = East.function([SetType(StringType)], IntegerType, ($, set) => {
   *   $.return(set.size());
   * });
   * const compiled = East.compile(getSize.toIR(), []);
   * compiled(new Set(["a", "b", "c"]));  // 3n
   * compiled(new Set());  // 0n
   * ```
   */
  size(): IntegerExpr {
    return Expr.fromAst({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "SetSize",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Checks if an element exists in the set.
   *
   * @param key - The element to search for
   * @returns A BooleanExpr that is true if the element exists, false otherwise
   *
   * @example
   * ```ts
   * const hasElement = East.function([SetType(StringType), StringType], BooleanType, ($, set, element) => {
   *   $.return(set.has(element));
   * });
   * const compiled = East.compile(hasElement.toIR(), []);
   * const set = new Set(["a", "b", "c"]);
   * compiled(set, "b");  // true
   * compiled(set, "d");  // false
   * ```
   */
  has(key: SubtypeExprOrValue<K>): BooleanExpr {
    const valueAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "SetHas",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], valueAst],
    }) as BooleanExpr;
  }

  /**
   * Inserts a new element into the set.
   *
   * @param key - The element to insert
   * @returns A NullExpr
   *
   * @throws East runtime error if the element already exists in the set
   *
   * @see {@link tryInsert} for a version that doesn't error on duplicates
   *
   * @example
   * ```ts
   * const insertElement = East.function([SetType(StringType), StringType], NullType, ($, set, element) => {
   *   $(set.insert(element));
   *   $.return(null);
   * });
   * const compiled = East.compile(insertElement.toIR(), []);
   * const set = new Set(["a", "b"]);
   * compiled(set, "c");  // set now has Set(["a", "b", "c"])
   * // compiled(set, "a") would throw error (duplicate element)
   * ```
   */
  insert(key: SubtypeExprOrValue<K>): NullExpr {
    const location = get_location();
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);

    return Expr.fromAst({
      ast_type: "Builtin",
      type: NullType,
      location,
      builtin: "SetInsert",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as NullExpr;
  }

  /**
   * Tries to insert an element into the set, returning whether it was inserted.
   *
   * @param key - The element to insert
   * @returns A BooleanExpr that is true if the element was inserted, false if it already existed
   *
   * @see {@link insert} for a version that errors on duplicates
   *
   * @example
   * ```ts
   * const tryInsertElement = East.function([SetType(StringType), StringType], BooleanType, ($, set, element) => {
   *   $.return(set.tryInsert(element));
   * });
   * const compiled = East.compile(tryInsertElement.toIR(), []);
   * const set = new Set(["a", "b"]);
   * compiled(set, "c");  // true (set now has Set(["a", "b", "c"]))
   * compiled(set, "a");  // false (element already exists, set unchanged)
   * ```
   */
  tryInsert(key: SubtypeExprOrValue<K>): BooleanExpr {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    
    return Expr.fromAst({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "SetTryInsert",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as BooleanExpr;
  }

  /**
   * Deletes an element from the set.
   *
   * @param key - The element to delete
   * @returns A NullExpr
   *
   * @throws East runtime error if the element does not exist
   *
   * @see {@link tryDelete} for a version that doesn't error on missing elements
   * @see {@link clear} to remove all elements
   *
   * @example
   * ```ts
   * const deleteElement = East.function([SetType(StringType), StringType], NullType, ($, set, element) => {
   *   $(set.delete(element));
   *   $.return(null);
   * });
   * const compiled = East.compile(deleteElement.toIR(), []);
   * const set = new Set(["a", "b", "c"]);
   * compiled(set, "b");  // set now has Set(["a", "c"])
   * // compiled(set, "d") would throw error (element not found)
   * ```
   */
  delete(key: SubtypeExprOrValue<K>): NullExpr {
    const location = get_location();
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);

    return Expr.fromAst({
      ast_type: "Builtin",
      type: NullType,
      location,
      builtin: "SetDelete",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as NullExpr;
  }

  /**
   * Tries to delete an element from the set, returning whether it was deleted.
   *
   * @param key - The element to delete
   * @returns A BooleanExpr that is true if the element was deleted, false if it didn't exist
   *
   * @see {@link delete} for a version that errors on missing elements
   *
   * @example
   * ```ts
   * const tryDeleteElement = East.function([SetType(StringType), StringType], BooleanType, ($, set, element) => {
   *   $.return(set.tryDelete(element));
   * });
   * const compiled = East.compile(tryDeleteElement.toIR(), []);
   * const set = new Set(["a", "b", "c"]);
   * compiled(set, "b");  // true (set now has Set(["a", "c"]))
   * compiled(set, "d");  // false (element not found, set unchanged)
   * ```
   */
  tryDelete(key: SubtypeExprOrValue<K>): BooleanExpr {
    const keyAst = valueOrExprToAstTyped(key, this.key_type as EastType);
    
    return Expr.fromAst({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "SetTryDelete",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], keyAst],
    }) as BooleanExpr;
  }

  /**
   * Removes all elements from the set.
   *
   * @returns A NullExpr
   *
   * @see {@link delete} or {@link tryDelete} to remove individual elements
   *
   * @example
   * ```ts
   * const clearSet = East.function([SetType(StringType)], NullType, ($, set) => {
   *   $(set.clear());
   *   $.return(null);
   * });
   * const compiled = East.compile(clearSet.toIR(), []);
   * const set = new Set(["a", "b", "c"]);
   * compiled(set);  // set is now Set([])
   * ```
   */
  clear(): NullExpr {
    return Expr.fromAst({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "SetClear",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol]],
    }) as NullExpr;
  }

  /**
   * Unions another set into this one in place.
   *
   * @param other - The set whose elements to add to this set
   * @returns A NullExpr
   *
   * @see {@link union} for a version that returns a new set
   *
   * @example
   * ```ts
   * const unionInPlace = East.function([SetType(IntegerType), SetType(IntegerType)], NullType, ($, set1, set2) => {
   *   $(set1.unionInPlace(set2));
   *   $.return(null);
   * });
   * const compiled = East.compile(unionInPlace.toIR(), []);
   * const set1 = new Set([1n, 2n, 3n]);
   * const set2 = new Set([3n, 4n, 5n]);
   * compiled(set1, set2);  // set1 now has Set([1n, 2n, 3n, 4n, 5n])
   * ```
   */
  unionInPlace(other: SubtypeExprOrValue<SetType<K>>): NullExpr {
    const otherAst = valueOrExprToAstTyped(other, this[TypeSymbol]);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "SetUnionInPlace",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], otherAst],
    }) as NullExpr;
  }

  /**
   * Returns the union of two sets (all elements from both sets).
   *
   * @param other - The set to union with this set
   * @returns A new SetExpr containing all elements from both sets
   *
   * @see {@link unionInPlace} to modify this set in place
   *
   * @example
   * ```ts
   * const unionSets = East.function([SetType(IntegerType), SetType(IntegerType)], SetType(IntegerType), ($, set1, set2) => {
   *   $.return(set1.union(set2));
   * });
   * const compiled = East.compile(unionSets.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]), new Set([3n, 4n, 5n]));  // Set([1n, 2n, 3n, 4n, 5n])
   * ```
   */
  union(other: SubtypeExprOrValue<SetType<K>>): SetExpr<K> {
    const otherAst = valueOrExprToAstTyped(other, this[TypeSymbol]);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "SetUnion",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], otherAst],
    }) as SetExpr<K>;
  }

  /**
   * Returns the intersection of two sets (elements common to both).
   *
   * @param other - The set to intersect with this set
   * @returns A new SetExpr containing only elements present in both sets
   *
   * @example
   * ```ts
   * const intersectSets = East.function([SetType(IntegerType), SetType(IntegerType)], SetType(IntegerType), ($, set1, set2) => {
   *   $.return(set1.intersection(set2));
   * });
   * const compiled = East.compile(intersectSets.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]), new Set([2n, 3n, 4n]));  // Set([2n, 3n])
   * ```
   */
  intersection(other: SubtypeExprOrValue<SetType<K>>): SetExpr<K> {
    const otherAst = valueOrExprToAstTyped(other, this[TypeSymbol]);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "SetIntersect",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], otherAst],
    }) as SetExpr<K>;
  }

  /**
   * Returns the difference between two sets (elements in this set but not in the other).
   *
   * @param other - The set to subtract from this set
   * @returns A new SetExpr containing elements in this set but not in the other
   *
   * @example
   * ```ts
   * const diffSets = East.function([SetType(IntegerType), SetType(IntegerType)], SetType(IntegerType), ($, set1, set2) => {
   *   $.return(set1.difference(set2));
   * });
   * const compiled = East.compile(diffSets.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]), new Set([2n, 3n, 4n]));  // Set([1n])
   * ```
   */
  difference(other: SubtypeExprOrValue<SetType<K>>): SetExpr<K> {
    const otherAst = valueOrExprToAstTyped(other, this[TypeSymbol]);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "SetDiff",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], otherAst],
    }) as SetExpr<K>;
  }

  /**
   * Returns the symmetric difference between two sets (elements in either set but not in both).
   *
   * @param other - The set to compute symmetric difference with
   * @returns A new SetExpr containing elements in either set but not in both
   *
   * @example
   * ```ts
   * const symDiffSets = East.function([SetType(IntegerType), SetType(IntegerType)], SetType(IntegerType), ($, set1, set2) => {
   *   $.return(set1.symmetricDifference(set2));
   * });
   * const compiled = East.compile(symDiffSets.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]), new Set([2n, 3n, 4n]));  // Set([1n, 4n])
   * ```
   */
  symmetricDifference(other: SubtypeExprOrValue<SetType<K>>): SetExpr<K> {
    const otherAst = valueOrExprToAstTyped(other, this[TypeSymbol]);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "SetSymDiff",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], otherAst],
    }) as SetExpr<K>;
  }

  /**
   * Checks if this set is a subset of another set (all elements in this set are in the other).
   *
   * @param other - The set to check against
   * @returns A BooleanExpr that is true if this set is a subset of the other
   *
   * @example
   * ```ts
   * const checkSubset = East.function([SetType(IntegerType), SetType(IntegerType)], BooleanType, ($, set1, set2) => {
   *   $.return(set1.isSubsetOf(set2));
   * });
   * const compiled = East.compile(checkSubset.toIR(), []);
   * compiled(new Set([1n, 2n]), new Set([1n, 2n, 3n]));  // true
   * compiled(new Set([1n, 4n]), new Set([1n, 2n, 3n]));  // false
   * ```
   */
  isSubsetOf(other: SubtypeExprOrValue<SetType<K>>): BooleanExpr {
    const otherAst = valueOrExprToAstTyped(other, this[TypeSymbol]);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "SetIsSubset",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], otherAst],
    }) as BooleanExpr;
  }

  /**
   * Checks if this set is a superset of another set (all elements in the other set are in this set).
   *
   * @param other - The set to check against
   * @returns A BooleanExpr that is true if this set is a superset of the other
   *
   * @example
   * ```ts
   * const checkSuperset = East.function([SetType(IntegerType), SetType(IntegerType)], BooleanType, ($, set1, set2) => {
   *   $.return(set1.isSupersetOf(set2));
   * });
   * const compiled = East.compile(checkSuperset.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]), new Set([1n, 2n]));  // true
   * compiled(new Set([1n, 2n]), new Set([1n, 2n, 3n]));  // false
   * ```
   */
  isSupersetOf(other: SubtypeExprOrValue<SetType<K>>): BooleanExpr {
    const otherAst = valueOrExprToAstTyped(other, this[TypeSymbol]);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "SetIsSubset",
      type_parameters: [this.key_type as EastType],
      arguments: [otherAst, this[AstSymbol]], // Note: arguments swapped for superset
    }) as BooleanExpr;
  }

  /**
   * Checks if this set is disjoint from another set (no common elements).
   *
   * @param other - The set to check against
   * @returns A BooleanExpr that is true if the sets have no elements in common
   *
   * @example
   * ```ts
   * const checkDisjoint = East.function([SetType(IntegerType), SetType(IntegerType)], BooleanType, ($, set1, set2) => {
   *   $.return(set1.isDisjointFrom(set2));
   * });
   * const compiled = East.compile(checkDisjoint.toIR(), []);
   * compiled(new Set([1n, 2n]), new Set([3n, 4n]));  // true
   * compiled(new Set([1n, 2n]), new Set([2n, 3n]));  // false
   * ```
   */
  isDisjointFrom(other: SubtypeExprOrValue<SetType<K>>): BooleanExpr {
    const otherAst = valueOrExprToAstTyped(other, this[TypeSymbol]);
    return Expr.fromAst({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "SetIsDisjoint",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], otherAst],
    }) as BooleanExpr;
  }

  /**
   * Creates a shallow copy of the set.
   *
   * @returns A new SetExpr containing the same elements
   *
   * @example
   * ```ts
   * const copySet = East.function([SetType(StringType)], SetType(StringType), ($, set) => {
   *   $.return(set.copy());
   * });
   * const compiled = East.compile(copySet.toIR(), []);
   * const set = new Set(["a", "b", "c"]);
   * const copy = compiled(set);  // Set(["a", "b", "c"])
   * // Modifying copy doesn't affect set
   * ```
   */
  copy(): SetExpr<K> {
    // Note that keys are immutable so shallow and deep copy are the same
    return Expr.fromAst({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "SetCopy",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol]],
    }) as SetExpr<K>;
  }
  
  /**
   * Filters the set using a predicate function.
   *
   * @param pred - Function that returns true to keep an element, false to discard it
   * @returns A new SetExpr containing only elements for which the predicate returned true
   *
   * @example
   * ```ts
   * const filterEven = East.function([SetType(IntegerType)], SetType(IntegerType), ($, set) => {
   *   $.return(set.filter(($, x) => x.modulo(2n).equal(0n)));
   * });
   * const compiled = East.compile(filterEven.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n, 5n, 6n]));  // Set([2n, 4n, 6n])
   * ```
   */
  filter(pred: SubtypeExprOrValue<FunctionType<[K], BooleanType>>): SetExpr<K> {
    const predExpr = Expr.from(pred as any, FunctionType([this.key_type as EastType], BooleanType));
    return Expr.fromAst({
      ast_type: "Builtin",
      type: this[TypeSymbol],
      location: get_location(),
      builtin: "SetFilter",
      type_parameters: [this.key_type as EastType],
      arguments: [this[AstSymbol], Expr.ast(predExpr as any)],
    }) as SetExpr<K>;
  }

  /** Combined filter and map operation using Option types.
   *
   * Applies a function to each key in the set. If the function returns `some(value)`,
   * the key is included in the result dictionary with the transformed value. If it returns `none`,
   * the key is excluded.
   *
   * @param fn - Function that takes a key and returns an option containing the transformed value
   * @returns A dictionary mapping keys to transformed values for keys where the function returned `some`
   *
   * @example
   * ```ts
   * const s = new Set([1n, 2n, 3n, 4n, 5n])
   * // Only include even numbers, mapping them to their string representation
   * const result = s.filterMap(($, x) =>
   *   x.remainder(2n).equal(0n).if(
   *     () => East.some(East.print(x)),
   *     () => East.none
   *   )
   * )
   * // Result: { 2: "2", 4: "4" }
   * ```
   */
  filterMap<V2>(fn: Expr<FunctionType<[K], VariantType<{ none: NullType, some: V2 }>>>): DictExpr<K, V2>;
  filterMap<F extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(fn: F): DictExpr<K, any>;
  filterMap(fn: any): DictExpr<K, any> {
    let fnExpr: Expr<FunctionType>;
    if (typeof fn === "function") {
      fnExpr = Expr.function([this.key_type], undefined, fn) as Expr<FunctionType>;
    } else {
      fnExpr = fn;
    }
    const fnType = fnExpr[TypeSymbol] as FunctionType;
    const returnType = fnType.output as EastType;

    // Extract V2 from the option type
    if (returnType.type !== "Variant" || !("some" in returnType.cases)) {
      throw new Error(`filterMap function must return an option type (variant with 'none' and 'some'), got ${printType(returnType)}`);
    }
    const valueType = returnType.cases.some;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: DictType(this.key_type, valueType),
      location: get_location(),
      builtin: "SetFilterMap",
      type_parameters: [this.key_type as EastType, valueType],
      arguments: [this[AstSymbol], Expr.ast(fnExpr as any)],
    }) as DictExpr<K, any>;
  }

  /**
   * Find the first key where the mapping function returns `some(value)`, and return that value wrapped in an Option.
   *
   * The supplied function must return an Option type. This method stops iterating as soon as the first `some` value is found,
   * making it efficient for early termination searches.
   *
   * Returns `none` if no key produces a `some` value, or `some(value)` with the first mapped result.
   *
   * @param fn - Function that maps each key to an Option type
   * @returns Option containing the first successfully mapped value, or `none` if none found
   *
   * @example
   * ```ts
   * const s = new Set([1n, 2n, 3n, 4n, 5n])
   * // Find the first even number and return its square
   * const result = s.firstMap(($, x) =>
   *   x.remainder(2n).equal(0n).ifElse(
   *     () => East.some(x.multiply(x)),
   *     () => East.none
   *   )
   * )
   * // Result: some(4n)
   * ```
   *
   * @see {@link filterMap} to collect all mapped values that return `some` (scans entire set).
   */
  firstMap<T2>(fn: Expr<FunctionType<[K], VariantType<{ none: NullType, some: T2 }>>>): Expr<VariantType<{ none: NullType, some: T2 }>>;
  firstMap<F extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(fn: F): ExprType<TypeOf<ReturnType<F>>>;
  firstMap(fn: any): Expr {
    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.key_type], undefined));

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
      builtin: "SetFirstMap",
      type_parameters: [this.key_type as EastType, someType as EastType],
      arguments: [this[AstSymbol], fnAst],
    });
  }

  /**
   * Iterates over each element in the set, applying a function to each.
   *
   * @param fn - Function to apply to each element
   * @returns A NullExpr
   *
   * @example
   * ```ts
   * const printElements = East.function([SetType(StringType)], NullType, ($, set) => {
   *   $(set.forEach(($, element) => {
   *     // In a real platform, you could use a platform function to log
   *   }));
   *   $.return(null);
   * });
   * const compiled = East.compile(printElements.toIR(), []);
   * compiled(new Set(["a", "b", "c"]));  // Iterates over all elements
   * ```
   */
  forEach(fn: SubtypeExprOrValue<FunctionType<[K], undefined>>): NullExpr {
    const fnExpr = Expr.function([this.key_type], undefined, fn as any);
    const fnType = fnExpr[TypeSymbol] as FunctionType;
    const returnType = fnType.output as EastType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: NullType,
      location: get_location(),
      builtin: "SetForEach",
      type_parameters: [this.key_type as EastType, returnType],
      arguments: [this[AstSymbol], Expr.ast(fnExpr as any)],
    }) as NullExpr;
  }

  /**
   * Creates a dictionary by mapping each element through a function.
   *
   * The dictionary keys are the original set elements, and the values are the results of the mapping function.
   *
   * @param fn - Function that maps each element to a value
   * @returns A DictExpr with set elements as keys and mapped values as values
   *
   * @example
   * ```ts
   * const mapToLengths = East.function([SetType(StringType)], DictType(StringType, IntegerType), ($, set) => {
   *   $.return(set.map(($, str) => str.size()));
   * });
   * const compiled = East.compile(mapToLengths.toIR(), []);
   * compiled(new Set(["a", "hello", "world"]));  // Map([["a", 1n], ["hello", 5n], ["world", 5n]])
   * ```
   */
  map<T2>(fn: Expr<FunctionType<[K], T2>>): DictExpr<K, T2>;
  map<F extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(fn: F): DictExpr<K, TypeOf<ReturnType<F>>>;
  map(fn: Expr<FunctionType> | (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)): DictExpr<K, any> {
    let fnExpr: Expr<FunctionType>;
    if (typeof fn === "function") {
      fnExpr = Expr.function([this.key_type], undefined, fn) as Expr<FunctionType>;
    } else {
      fnExpr = fn;
    }
    const fnType = fnExpr[TypeSymbol] as FunctionType;
    const returnType = fnType.output as EastType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: DictType(this.key_type, returnType),
      location: get_location(),
      builtin: "SetMap",
      type_parameters: [this.key_type as EastType, returnType],
      arguments: [this[AstSymbol], Expr.ast(fnExpr as any)],
    }) as DictExpr<K, any>;
  }

  /**
   * Reduce set to single value using projection and accumulator functions.
   *
   * The first element of the set is used as initial value and reduction starts from the second element.
   * If the set is empty, an error is thrown.
   *
   * @param mapFn - Function that projects each key to a value
   * @param combineFn - Function that combines two projected values
   * @returns The final reduced value
   *
   * @example
   * ```ts
   * const s = new Set([1n, 2n, 3n, 4n, 5n])
   * // Sum of squares
   * const result = s.mapReduce(
   *   ($, x) => x.multiply(x),
   *   ($, a, b) => a.add(b)
   * )
   * // Result: 55n (1 + 4 + 9 + 16 + 25)
   * ```
   *
   * @see {@link reduce} for a version with an initial value
   */
  mapReduce<T2>(mapFn: Expr<FunctionType<[K], T2>>, combineFn: SubtypeExprOrValue<FunctionType<[previous: NoInfer<T2>, value: NoInfer<T2>], NoInfer<T2>>>): ExprType<T2>;
  mapReduce<F extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(mapFn: F, combineFn: SubtypeExprOrValue<FunctionType<[previous: NoInfer<TypeOf<ReturnType<F>>>, value: NoInfer<TypeOf<ReturnType<F>>>], NoInfer<TypeOf<ReturnType<F>>>>>): ExprType<TypeOf<ReturnType<F>>>;
  mapReduce<_T2>(mapFn: any, combineFn: any): Expr {
    const mapAst = valueOrExprToAstTyped(mapFn, FunctionType([this.key_type], undefined));
    const mapType = mapAst.type.output as EastType;
    const combineAst = valueOrExprToAstTyped(combineFn, FunctionType([mapType, mapType], mapType));

    return Expr.fromAst({
      ast_type: "Builtin",
      type: mapType as EastType,
      location: get_location(),
      builtin: "SetMapReduce",
      type_parameters: [this.key_type as EastType, mapType],
      arguments: [this[AstSymbol], mapAst, combineAst],
    });
  }

  /**
   * Reduces the set to a single value using an accumulator function.
   *
   * @param fn - Function accepting (accumulator, element) and returning the new accumulator value
   * @param init - Initial value for the accumulator
   * @returns The final accumulated value
   *
   * @see {@link mapReduce} for a version that projects elements before combining
   *
   * @example
   * ```ts
   * const sumSet = East.function([SetType(IntegerType)], IntegerType, ($, set) => {
   *   $.return(set.reduce(($, acc, element) => acc.add(element), 0n));
   * });
   * const compiled = East.compile(sumSet.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n]));  // 10n
   * ```
   */
  reduce<T2>(fn: SubtypeExprOrValue<FunctionType<[TypeOf<NoInfer<T2>>, K], TypeOf<NoInfer<T2>>>>, init: T2): ExprType<TypeOf<NoInfer<T2>>> {
    const initAst = valueOrExprToAst(init);
    const returnType = initAst.type;

    const fnExpr = Expr.from(fn as any, FunctionType([returnType, this.key_type], returnType));

    return Expr.fromAst({
      ast_type: "Builtin",
      type: returnType,
      location: get_location(),
      builtin: "SetReduce",
      type_parameters: [this.key_type as EastType, returnType],
      arguments: [this[AstSymbol], Expr.ast(fnExpr as any), initAst],
    }) as ExprType<TypeOf<NoInfer<T2>>>;
  }

  /**
   * Creates an array from the set by mapping each element through a function.
   *
   * If no function is provided, the set elements are copied as-is.
   *
   * @param fn - Optional function to map each element to an array value
   * @returns An ArrayExpr containing the mapped values
   *
   * @example
   * ```ts
   * const setToArray = East.function([SetType(IntegerType)], ArrayType(IntegerType), ($, set) => {
   *   $.return(set.toArray());
   * });
   * const compiled = East.compile(setToArray.toIR(), []);
   * compiled(new Set([3n, 1n, 2n]));  // [1n, 2n, 3n] (sorted order)
   * ```
   *
   * @example
   * ```ts
   * // With mapping function
   * const doubleToArray = East.function([SetType(IntegerType)], ArrayType(IntegerType), ($, set) => {
   *   $.return(set.toArray(($, x) => x.multiply(2n)));
   * });
   * const compiled = East.compile(doubleToArray.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]));  // [2n, 4n, 6n]
   * ```
   */
  toArray<T2>(fn: Expr<FunctionType<[K], T2>>): ArrayExpr<T2>;
  toArray<F extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(fn: F): ArrayExpr<TypeOf<ReturnType<F>>>;
  toArray(): K extends IntegerType | FloatType | BooleanType | NullType | StringType ? ArrayExpr<K> : never;
  toArray(fn?: any): ArrayExpr<any> {
    let fnExpr: Expr<FunctionType>;
    if (fn === undefined) {
      // Identity function
      fnExpr = Expr.function([this.key_type as EastType], this.key_type as EastType, ($, key) => key) as Expr<FunctionType>;
    } else if (typeof fn === "function") {
      fnExpr = Expr.function([this.key_type], undefined, fn) as Expr<FunctionType>;
    } else {
      fnExpr = fn;
    }
    const fnType = fnExpr[TypeSymbol] as FunctionType;
    const returnType = fnType.output as EastType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: ArrayType(returnType),
      location: get_location(),
      builtin: "SetToArray",
      type_parameters: [this.key_type as EastType, returnType],
      arguments: [this[AstSymbol], Expr.ast(fnExpr as any)],
    }) as ArrayExpr<any>;
  }

  /**
   * Creates a new set by mapping each element through a function.
   *
   * Duplicates produced by the mapping function are ignored, and only unique values are kept.
   *
   * @param fn - Function to map each element to a new set element
   * @returns A SetExpr containing the unique mapped values
   *
   * @example
   * ```ts
   * const extractFirstChar = East.function([SetType(StringType)], SetType(StringType), ($, set) => {
   *   $.return(set.toSet(($, str) => str.substring(0n, 1n)));
   * });
   * const compiled = East.compile(extractFirstChar.toIR(), []);
   * compiled(new Set(["apple", "apricot", "banana", "blueberry"]));  // Set(["a", "b"])
   * ```
   */
  toSet<K2>(fn: Expr<FunctionType<[K], K2>>): SetExpr<K2>
  toSet<F extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(fn: F): SetExpr<TypeOf<ReturnType<F>>>
  toSet(keyFn?: any): SetExpr<any> {
    let keyFnAst
    if (keyFn !== undefined) {
      let fnExpr: Expr<FunctionType>;
      if (typeof keyFn === "function") {
        fnExpr = Expr.function([this.key_type], undefined, keyFn) as Expr<FunctionType>;
      } else {
        fnExpr = keyFn;
      }
      keyFnAst = Expr.ast(fnExpr as any);
    } else {
      // Identity function
      const identityFunction = Expr.function([this.key_type as EastType], this.key_type as EastType, ($, key) => key);
      keyFnAst = Expr.ast(identityFunction as any);
    }

    const keyType = (keyFnAst.type as FunctionType).output as EastType;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: SetType(keyType),
      location: get_location(),
      builtin: "SetToSet",
      type_parameters: [this.key_type as EastType, keyType as EastType],
      arguments: [this[AstSymbol], keyFnAst],
    }) as SetExpr<any>;
  }

  /**
   * Converts the set to a dictionary using custom key and value functions.
   *
   * @param keyFn - Optional function that maps each element to a dictionary key (defaults to identity)
   * @param valueFn - Optional function that maps each element to a dictionary value (defaults to identity)
   * @param onConflict - Optional function to handle duplicate keys, receives (existing_value, new_value, key) and returns the value to keep
   * @returns A DictExpr containing the converted elements
   *
   * @throws East runtime error if duplicate keys are produced and no conflict handler is provided
   *
   * @see {@link toArray} to convert to an array, {@link toSet} to transform element types
   *
   * @example
   * ```ts
   * // Convert set to dict with custom keys and values
   * const convertToDict = East.function([SetType(StringType)], DictType(IntegerType, StringType), ($, words) => {
   *   $.return(words.toDict(
   *     ($, word) => word.size(),      // Key: word length
   *     ($, word) => word.upper(),     // Value: uppercase word
   *     ($, existing, newVal, key) => existing  // Keep first value on conflict
   *   ));
   * });
   * const compiled = East.compile(convertToDict.toIR(), []);
   * compiled(new Set(["hi", "bye", "up"]));  // { 2n: "HI", 3n: "BYE" }
   * ```
   *
   * @example
   * ```ts
   * // Simple conversion with identity functions
   * const identityDict = East.function([SetType(StringType)], DictType(StringType, StringType), ($, items) => {
   *   $.return(items.toDict());  // Same key and value
   * });
   * const compiled = East.compile(identityDict.toIR(), []);
   * compiled(new Set(["a", "b"]));  // { "a": "a", "b": "b" }
   * ```
   */
  toDict<K2, T2>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: Expr<FunctionType<[K], T2>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<T2>, NoInfer<T2>, NoInfer<K2>], NoInfer<T2>>>): DictExpr<K2, T2>
  toDict<K2, ValueFn extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: ValueFn, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, NoInfer<K2>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<K2, TypeOf<ReturnType<ValueFn>>>;
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any), T2>(keyFn: KeyFn, valueFn: Expr<FunctionType<[K], T2>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<T2>, NoInfer<T2>, TypeOf<ReturnType<NoInfer<KeyFn>>>], NoInfer<T2>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, T2>
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: ValueFn, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, NoInfer<TypeOf<ReturnType<NoInfer<KeyFn>>>>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<ValueFn>>>;
  toDict<K2>(keyFn: Expr<FunctionType<[K], K2>>): DictExpr<K2, K>
  toDict<KeyFn extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, K>;
  toDict(): DictExpr<K, K>
  toDict(keyFn?: any, valueFn?: any, onConflictFn?: any): DictExpr<any, any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn ?? ((_$: any, x: any, i: any) => i), FunctionType([this.key_type], undefined));
    const keyType = keyFnAst.type.output as EastType;

    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.key_type], undefined));
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
      builtin: "SetToDict",
      type_parameters: [this.key_type as EastType, keyType, valueType],
      arguments: [this[AstSymbol], keyFnAst, valueFnAst, onConflictAst],
    }) as DictExpr<any, any>;
  }

  /**
   * Maps each element to an array and concatenates all resulting arrays into a single array.
   *
   * @param fn - Function that maps each element to an array
   * @returns An ArrayExpr containing all elements from all arrays, concatenated in order
   *
   * @remarks The function must return an Array type. Use this for one-to-many transformations.
   *
   * @see {@link toArray} to create an array with the same number of elements, {@link flattenToSet} to flatten to a set, {@link flattenToDict} to flatten to a dictionary
   *
   * @example
   * ```ts
   * // Expand each number to a range of numbers
   * const expandRanges = East.function([SetType(IntegerType)], ArrayType(IntegerType), ($, numbers) => {
   *   $.return(numbers.flattenToArray(($, n) => {
   *     const result = Expr.from([], ArrayType(IntegerType));
   *     $(Expr.for(0n, n, ($, i) => {
   *       $(result.push(i));
   *     }));
   *     return result;
   *   }));
   * });
   * const compiled = East.compile(expandRanges.toIR(), []);
   * compiled(new Set([2n, 3n]));  // [0n, 1n, 0n, 1n, 2n]
   * ```
   */
  flattenToArray<T2>(fn: Expr<FunctionType<[K], ArrayType<T2>>>): ArrayExpr<T2>;
  flattenToArray<F extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any)>(fn: F): TypeOf<ReturnType<F>> extends ArrayType<infer U> ? ArrayExpr<U> : never;
  flattenToArray(fn: any): ArrayExpr<any> {
    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.key_type], undefined));

    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Array") {
      throw new Error(`Expected Function to return an Array type, got ${printType(returnType)}`);
    }
    const elementType = returnType.value;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: ArrayType(elementType as EastType),
      location: get_location(),
      builtin: "SetFlattenToArray",
      type_parameters: [this.key_type as EastType, elementType as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as ArrayExpr<any>;
  }

  /**
   * Maps each element to a set and unions all resulting sets into a single set.
   *
   * @param fn - Function that maps each element to a set
   * @returns A SetExpr containing all unique elements from all sets
   *
   * @remarks The function must return a Set type. Duplicates are automatically removed.
   *
   * @see {@link flattenToArray} to flatten to an array, {@link flattenToDict} to flatten to a dictionary, {@link toSet} to map without flattening
   *
   * @example
   * ```ts
   * // Generate multiples for each number
   * const generateMultiples = East.function([SetType(IntegerType)], SetType(IntegerType), ($, numbers) => {
   *   $.return(numbers.flattenToSet(($, n) => {
   *     const multiples = Expr.from(new Set(), SetType(IntegerType));
   *     $(multiples.insert(n.multiply(2n)));
   *     $(multiples.insert(n.multiply(3n)));
   *     return multiples;
   *   }));
   * });
   * const compiled = East.compile(generateMultiples.toIR(), []);
   * compiled(new Set([2n, 3n]));  // Set([4n, 6n, 9n])  (6n appears once)
   * ```
   */
  flattenToSet<K2>(fn: Expr<FunctionType<[K], SetType<K2>>>): SetExpr<K2>;
  flattenToSet<F extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any)>(fn: F): TypeOf<ReturnType<F>> extends SetType<infer U> ? SetExpr<U> : never;
  flattenToSet(fn: any): SetExpr<any> {
    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.key_type], undefined));
    
    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Set") {
      throw new Error(`Expected Function to return a Set type, got ${printType(returnType)}`);
    }
    const elementType = returnType.key;

    return Expr.fromAst({
      ast_type: "Builtin",
      type: SetType(elementType as EastType),
      location: get_location(),
      builtin: "SetFlattenToSet",
      type_parameters: [this.key_type as EastType, elementType as EastType],
      arguments: [this[AstSymbol], fnAst],
    }) as SetExpr<any>;
  }

  /**
   * Maps each element to a dictionary and merges all resulting dictionaries into a single dictionary.
   *
   * @param fn - Function that maps each element to a dictionary
   * @param onConflict - Optional function to handle duplicate keys, receives (existing_value, new_value, key) and returns the value to keep
   * @returns A DictExpr containing all entries from all dictionaries
   *
   * @throws East runtime error if duplicate keys are produced and no conflict handler is provided
   *
   * @remarks The function must return a Dict type. Use this for one-to-many transformations with key-value pairs.
   *
   * @see {@link flattenToArray} to flatten to an array, {@link flattenToSet} to flatten to a set, {@link toDict} to convert without flattening
   *
   * @example
   * ```ts
   * // Generate word statistics for each prefix
   * const wordStats = East.function([SetType(StringType)], DictType(StringType, IntegerType), ($, prefixes) => {
   *   $.return(prefixes.flattenToDict(($, prefix) => {
   *     const stats = Expr.from(new Map(), DictType(StringType, IntegerType));
   *     $(stats.set(Expr.str`${prefix}_count`, prefix.size()));
   *     $(stats.set(Expr.str`${prefix}_double`, prefix.size().multiply(2n)));
   *     return stats;
   *   }));
   * });
   * const compiled = East.compile(wordStats.toIR(), []);
   * compiled(new Set(["hi", "bye"]));  // { "hi_count": 2n, "hi_double": 4n, "bye_count": 3n, "bye_double": 6n }
   * ```
   */
  flattenToDict<K2, V2>(fn: Expr<FunctionType<[K], DictType<K2, V2>>>, onConflict?: SubtypeExprOrValue<FunctionType<[NoInfer<V2>, NoInfer<V2>, NoInfer<K2>], NoInfer<V2>>>): DictExpr<K2, V2>;
  flattenToDict<F extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any)>(fn: F, onConflict?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never, TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never, TypeOf<ReturnType<NoInfer<F>>> extends DictType<infer K2, any> ? K2 : never], TypeOf<ReturnType<NoInfer<F>>> extends DictType<any, infer V2> ? V2 : never>>): TypeOf<ReturnType<F>> extends DictType<infer K2, infer V2> ? DictExpr<K2, V2> : never;
  flattenToDict(fn: any, onConflictFn?: any): DictExpr<any, any> {
    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.key_type], undefined));
    
    const returnType = fnAst.type.output as EastType;
    if (returnType.type !== "Dict") {
      throw new Error(`Expected Function to return a Dict type, got ${printType(returnType)}`);
    }
    const keyType = returnType.key as EastType;
    const valueType = returnType.value as EastType;

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
      builtin: "SetFlattenToDict",
      type_parameters: [this.key_type as EastType, keyType as EastType, valueType as EastType],
      arguments: [this[AstSymbol], fnAst, onConflictAst],
    }) as DictExpr<any, any>;
  }

  /**
   * Groups elements by a key and performs a fold/reduce operation on each group.
   *
   * @param keyFn - Function that maps each element to a group key
   * @param initFn - Function that creates the initial accumulator value for each group
   * @param reduceFn - Function that combines the accumulator with each element in the group
   * @returns A DictExpr mapping group keys to reduced values
   *
   * @see {@link groupToArrays} to collect elements into arrays, {@link groupToSets} to collect into sets
   *
   * @example
   * ```ts
   * // Group by even/odd and sum each group
   * const groupSum = East.function([SetType(IntegerType)], DictType(StringType, IntegerType), ($, numbers) => {
   *   $.return(numbers.groupReduce(
   *     ($, x) => x.remainder(2n).equal(0n).ifElse(() => "even", () => "odd"),
   *     ($, groupKey) => 0n,
   *     ($, acc, x) => acc.add(x)
   *   ));
   * });
   * const compiled = East.compile(groupSum.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n, 5n, 6n]));  // { "even": 12n, "odd": 9n }
   * ```
   */
  groupReduce<K2, T2>(keyFn: Expr<FunctionType<[K], K2>>, initFn: Expr<FunctionType<[K2], T2>>, reduceFn: SubtypeExprOrValue<FunctionType<[T2, K], T2>>): DictExpr<K2, T2>
  groupReduce<K2, InitFn extends ($: BlockBuilder<NeverType>, k2: ExprType<NoInfer<K2>>) => any>(keyFn: Expr<FunctionType<[K], K2>>, initFn: InitFn, reduceFn: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<InitFn>>>, K], TypeOf<ReturnType<NoInfer<InitFn>>>>>): DictExpr<K2, TypeOf<ReturnType<InitFn>>>
  groupReduce<KeyFn extends ($: BlockBuilder<NeverType>, key: ExprType<K>) => any, T2>(keyFn: KeyFn, initFn: Expr<FunctionType<[TypeOf<ReturnType<NoInfer<KeyFn>>>], T2>>, reduceFn: SubtypeExprOrValue<FunctionType<[T2, K], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, T2>
  groupReduce<KeyFn extends ($: BlockBuilder<NeverType>, key: ExprType<K>) => any, InitFn extends ($: BlockBuilder<NeverType>, k2: ExprType<TypeOf<ReturnType<NoInfer<KeyFn>>>>) => any>(keyFn: KeyFn, initFn: InitFn, reduceFn: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<InitFn>>>, K], TypeOf<ReturnType<NoInfer<InitFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<InitFn>>>
  groupReduce(keyFn: any, initFn: any, reduceFn: any): DictExpr<any, any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.key_type], undefined));
    const keyType = keyFnAst.type.output as EastType;

    const initFnAst = valueOrExprToAstTyped(initFn, FunctionType([keyType], undefined));
    const initType = initFnAst.type.output as EastType;

    const reduceFnAst = valueOrExprToAstTyped(reduceFn, FunctionType([initType, this.key_type], initType));

    return Expr.fromAst({
      ast_type: "Builtin",
      type: DictType(keyType as EastType, initType as EastType),
      location: get_location(),
      builtin: "SetGroupFold",
      type_parameters: [this.key_type as EastType, keyType as EastType, initType as EastType],
      arguments: [this[AstSymbol], keyFnAst, initFnAst, reduceFnAst],
    }) as DictExpr<any, any>;
  }

  /**
   * Groups elements by a key and collects each group into an array.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values (defaults to identity)
   * @returns A DictExpr mapping each group key to an array of elements
   *
   * @see {@link groupToSets} to collect into sets, {@link groupReduce} for custom aggregation
   *
   * @example
   * ```ts
   * const groupByParity = East.function([SetType(IntegerType)], DictType(IntegerType, ArrayType(IntegerType)), ($, numbers) => {
   *   $.return(numbers.groupToArrays(($, x) => x.remainder(2n)));
   * });
   * const compiled = East.compile(groupByParity.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n]));  // { 0n: [2n, 4n], 1n: [1n, 3n] }
   * ```
   */
  groupToArrays<K2, T2>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: Expr<FunctionType<[K], T2>>): DictExpr<K2, ArrayType<T2>>
  groupToArrays<K2, ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: ValueFn): DictExpr<K2, ArrayType<TypeOf<ReturnType<ValueFn>>>>
  groupToArrays<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), T2>(keyFn: KeyFn, valueFn: Expr<FunctionType<[K], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<T2>>
  groupToArrays<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<TypeOf<ReturnType<ValueFn>>>>
  groupToArrays<K2>(keyFn: Expr<FunctionType<[K], K2>>): DictExpr<K2, ArrayType<K>>
  groupToArrays<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, ArrayType<K>>
  groupToArrays(keyFn: any, valueFn?: any): DictExpr<any, ArrayType<any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.key_type], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);
    const valueFnExpr = Expr.fromAst(valueFnAst);
    const valueType = valueFnAst.type.output as EastType;
    return this.groupReduce(
      ((_$: any, key: any) => keyFnExpr(key)) as any,
      ((_$: any, _groupKey: any) => Expr.from([], ArrayType(valueType))) as any,
      (($: any, acc: any, key: any) => {
        const val = valueFnExpr(key);
        $(acc.pushLast(val));
        return acc;
      }) as any
    );
  }

  /**
   * Groups elements by a key and collects each group into a set.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values (defaults to identity)
   * @returns A DictExpr mapping each group key to a set of unique elements
   *
   * @see {@link groupToArrays} to collect into arrays, {@link groupReduce} for custom aggregation
   *
   * @example
   * ```ts
   * const groupByParity = East.function([SetType(IntegerType)], DictType(IntegerType, SetType(IntegerType)), ($, numbers) => {
   *   $.return(numbers.groupToSets(($, x) => x.remainder(2n)));
   * });
   * const compiled = East.compile(groupByParity.toIR(), []);
   * compiled(new Set([1n, 2n, 1n, 2n]));  // { 0n: Set([2n]), 1n: Set([1n]) }
   * ```
   */
  groupToSets<K2, T2>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: Expr<FunctionType<[K], T2>>): DictExpr<K2, SetType<T2>>
  groupToSets<K2, ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: ValueFn): DictExpr<K2, SetType<TypeOf<ReturnType<ValueFn>>>>
  groupToSets<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), T2>(keyFn: KeyFn, valueFn: Expr<FunctionType<[K], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, SetType<T2>>
  groupToSets<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, SetType<TypeOf<ReturnType<ValueFn>>>>
  groupToSets<K2>(keyFn: Expr<FunctionType<[K], K2>>): DictExpr<K2, SetType<K>>
  groupToSets<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, SetType<K>>
  groupToSets(keyFn: any, valueFn?: any): DictExpr<any, SetType<any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.key_type], undefined));
    const keyFnExpr = Expr.fromAst(keyFnAst);
    const valueFnExpr = Expr.fromAst(valueFnAst);
    const valueType = valueFnAst.type.output as EastType;
    return this.groupReduce(
      ((_$: any, key: any) => keyFnExpr(key)) as any,
      ((_$: any, _groupKey: any) => Expr.from(new Set<any>(), SetType(valueType))) as any,
      (($: any, acc: any, key: any) => {
        const val = valueFnExpr(key);
        $(acc.tryInsert(val));
        return acc;
      }) as any
    );
  }

  /**
   * Groups elements into nested dictionaries (dictionary-of-dictionaries).
   *
   * @param keyFn - Function that computes the outer grouping key
   * @param keyFn2 - Function that computes the inner dictionary key
   * @param valueFn - Optional projection function for inner dictionary values (defaults to identity)
   * @param combineFn - Optional function to resolve conflicts when the same inner key appears multiple times
   * @returns A DictExpr mapping group keys to dictionaries
   *
   * @throws East runtime error if duplicate inner keys are produced and no conflict handler is provided
   *
   * @see {@link groupToArrays} to collect into arrays, {@link groupToSets} to collect into sets
   *
   * @example
   * ```ts
   * // Group numbers by parity, then by sign
   * const nestedGroup = East.function([SetType(IntegerType)], DictType(StringType, DictType(StringType, IntegerType)), ($, numbers) => {
   *   $.return(numbers.groupToDicts(
   *     ($, n) => n.remainder(2n).equal(0n).ifElse(() => "even", () => "odd"),
   *     ($, n) => n.greaterThan(0n).ifElse(() => "positive", () => "negative"),
   *     ($, n) => n,
   *     ($, existing, newVal, key) => existing  // Keep first on conflict
   *   ));
   * });
   * const compiled = East.compile(nestedGroup.toIR(), []);
   * compiled(new Set([1n, -2n, 3n, -4n]));  // { "even": { "negative": -2n, "positive": ... }, "odd": { ... } }
   * ```
   */
  groupToDicts<K1, K2, T2>(keyFn: Expr<FunctionType<[K], K1>>, keyFn2: Expr<FunctionType<[K], K2>>, valueFn: Expr<FunctionType<[K], T2>>, combineFn?: SubtypeExprOrValue<FunctionType<[T2, T2, K1], T2>>): DictExpr<K1, DictType<K2, T2>>
  groupToDicts<K1, K2, ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[K], K1>>, keyFn2: Expr<FunctionType<[K], K2>>, valueFn: ValueFn, combineFn?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, K1], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<K1, DictType<K2, TypeOf<ReturnType<ValueFn>>>>
  groupToDicts<K1, KeyFn2 extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), T2>(keyFn: Expr<FunctionType<[K], K1>>, keyFn2: KeyFn2, valueFn: Expr<FunctionType<[K], T2>>, combineFn?: SubtypeExprOrValue<FunctionType<[T2, T2, K1], T2>>): DictExpr<K1, DictType<TypeOf<ReturnType<KeyFn2>>, T2>>
  groupToDicts<K1, KeyFn2 extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[K], K1>>, keyFn2: KeyFn2, valueFn: ValueFn, combineFn?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, K1], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<K1, DictType<TypeOf<ReturnType<KeyFn2>>, TypeOf<ReturnType<ValueFn>>>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), K2, T2>(keyFn: KeyFn, keyFn2: Expr<FunctionType<[K], K2>>, valueFn: Expr<FunctionType<[K], T2>>, combineFn?: SubtypeExprOrValue<FunctionType<[T2, T2, TypeOf<ReturnType<NoInfer<KeyFn>>>], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<K2, T2>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), K2, ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, keyFn2: Expr<FunctionType<[K], K2>>, valueFn: ValueFn, combineFn?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<KeyFn>>>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<K2, TypeOf<ReturnType<ValueFn>>>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), KeyFn2 extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), T2>(keyFn: KeyFn, keyFn2: KeyFn2, valueFn: Expr<FunctionType<[K], T2>>, combineFn?: SubtypeExprOrValue<FunctionType<[T2, T2, TypeOf<ReturnType<NoInfer<KeyFn>>>], T2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<TypeOf<ReturnType<KeyFn2>>, T2>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), KeyFn2 extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, keyFn2: KeyFn2, valueFn: ValueFn, combineFn?: SubtypeExprOrValue<FunctionType<[TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<ValueFn>>>, TypeOf<ReturnType<NoInfer<KeyFn>>>], TypeOf<ReturnType<NoInfer<ValueFn>>>>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<TypeOf<ReturnType<KeyFn2>>, TypeOf<ReturnType<ValueFn>>>>

  groupToDicts<K1, K2>(keyFn: Expr<FunctionType<[K], K1>>, keyFn2: Expr<FunctionType<[K], K2>>): DictExpr<K1, DictType<K2, K>>
  groupToDicts<K1, KeyFn2 extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[K], K1>>, keyFn2: KeyFn2): DictExpr<K1, DictType<TypeOf<ReturnType<KeyFn2>>, K>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), K2>(keyFn: KeyFn, keyFn2: Expr<FunctionType<[K], K2>>): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<K2, K>>
  groupToDicts<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), KeyFn2 extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, keyFn2: KeyFn2): DictExpr<TypeOf<ReturnType<KeyFn>>, DictType<TypeOf<ReturnType<KeyFn2>>, K>>

  groupToDicts(keyFn: any, keyFn2: any, valueFn?: any, combineFn?: any): DictExpr<any, DictType<any, any>> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.key_type], undefined));
    const keyFn2Ast = valueOrExprToAstTyped(keyFn2, FunctionType([this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.key_type], undefined));
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
        ((_$: any, key: any) => keyFnExpr(key)) as any,
        ((_$: any, _key: any) => Expr.from(new Map(), DictType(key2Type, valueType))) as any,
        (($: any, dict: any, key: any) => {
          const innerKey = keyFn2Expr(key);
          const val = valueFnExpr(key);
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
        ((_$: any, key: any) => keyFnExpr(key)) as any,
        ((_$: any, _key: any) => Expr.from(new Map(), DictType(key2Type, valueType))) as any,
        (($: any, dict: any, key: any) => {
          const innerKey = keyFn2Expr(key);
          const val = valueFnExpr(key);
          $(dict.insert(innerKey, val));
          return dict;
        }) as any
      );
    }
  }

  /**
   * Counts the number of elements in each group.
   *
   * @param keyFn - Optional function that computes the grouping key (defaults to identity)
   * @returns A DictExpr mapping each group key to the count of elements
   *
   * @see {@link groupToArrays} to collect elements instead of counting them
   *
   * @example
   * ```ts
   * // Group by parity and count
   * const countByParity = East.function([SetType(IntegerType)], DictType(IntegerType, IntegerType), ($, numbers) => {
   *   $.return(numbers.groupSize(($, x) => x.remainder(2n)));
   * });
   * const compiled = East.compile(countByParity.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n, 5n, 6n]));  // { 0n: 3n, 1n: 3n }
   * ```
   */
  groupSize<K2>(keyFn: Expr<FunctionType<[K], K2>>): DictExpr<K2, IntegerType>
  groupSize<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn): DictExpr<TypeOf<ReturnType<KeyFn>>, IntegerType>
  groupSize(): DictExpr<K, IntegerType>
  groupSize(keyFn?: any): DictExpr<any, IntegerType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn ?? ((_$: any, x: any) => x), FunctionType([this.key_type], undefined));
    return this.toDict(
      ((_$: any, key: any) => Expr.fromAst(keyFnAst)(key)) as any,
      ((_$: any) => 1n) as any,
      ((_$: any, a: any, b: any) => a.add(b)) as any
    );
  }

  /**
   * Checks if every element in each group satisfies a predicate.
   *
   * @param keyFn - Function that computes the grouping key
   * @param predFn - Predicate function to test each element
   * @returns A DictExpr mapping each group key to true if all elements satisfy the predicate
   *
   * @see {@link groupSome} to check if at least one element satisfies the predicate
   *
   * @example
   * ```ts
   * // Check if all numbers in each parity group are positive
   * const allPositive = East.function([SetType(IntegerType)], DictType(IntegerType, BooleanType), ($, numbers) => {
   *   $.return(numbers.groupEvery(
   *     ($, x) => x.remainder(2n),
   *     ($, x) => x.greaterThan(0n)
   *   ));
   * });
   * const compiled = East.compile(allPositive.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n]));  // { 0n: true, 1n: true }
   * ```
   */
  groupEvery<K2>(keyFn: Expr<FunctionType<[K], K2>>, predFn: SubtypeExprOrValue<FunctionType<[K], BooleanType>>): DictExpr<K2, BooleanType>
  groupEvery<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, predFn: SubtypeExprOrValue<FunctionType<[K], BooleanType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, BooleanType>
  groupEvery(keyFn: any, predFn: any): DictExpr<any, BooleanType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.key_type], undefined));
    const predFnAst = valueOrExprToAstTyped(predFn, FunctionType([this.key_type], BooleanType));
    return this.groupReduce(
      ((_$: any, key: any) => Expr.fromAst(keyFnAst)(key)) as any,
      (() => true) as any,
      ((_$: any, acc: BooleanExpr, key: any) => {
        const pred = Expr.fromAst(predFnAst)(key) as BooleanExpr;
        return acc.and(() => pred);
      }) as any
    );
  }

  /**
   * Checks if at least one element in each group satisfies a predicate.
   *
   * @param keyFn - Function that computes the grouping key
   * @param predFn - Predicate function to test each element
   * @returns A DictExpr mapping each group key to true if any element satisfies the predicate
   *
   * @see {@link groupEvery} to check if all elements satisfy the predicate
   *
   * @example
   * ```ts
   * // Check if any number in each parity group is greater than 3
   * const anyLarge = East.function([SetType(IntegerType)], DictType(IntegerType, BooleanType), ($, numbers) => {
   *   $.return(numbers.groupSome(
   *     ($, x) => x.remainder(2n),
   *     ($, x) => x.greaterThan(3n)
   *   ));
   * });
   * const compiled = East.compile(anyLarge.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n]));  // { 0n: true, 1n: false }
   * ```
   */
  groupSome<K2>(keyFn: Expr<FunctionType<[K], K2>>, predFn: SubtypeExprOrValue<FunctionType<[K], BooleanType>>): DictExpr<K2, BooleanType>
  groupSome<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, predFn: SubtypeExprOrValue<FunctionType<[K], BooleanType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, BooleanType>
  groupSome(keyFn: any, predFn: any): DictExpr<any, BooleanType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.key_type], undefined));
    const predFnAst = valueOrExprToAstTyped(predFn, FunctionType([this.key_type], BooleanType));
    return this.groupReduce(
      ((_$: any, key: any) => Expr.fromAst(keyFnAst)(key)) as any,
      (() => false) as any,
      ((_$: any, acc: BooleanExpr, key: any) => {
        const pred = Expr.fromAst(predFnAst)(key) as BooleanExpr;
        return acc.or(() => pred);
      }) as any
    );
  }

  /**
   * Computes the sum of elements in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values to sum (defaults to identity)
   * @returns A DictExpr mapping each group key to the sum
   *
   * @see {@link groupMean} to calculate the mean instead of sum
   *
   * @example
   * ```ts
   * // Sum numbers in each parity group
   * const sumByParity = East.function([SetType(IntegerType)], DictType(IntegerType, IntegerType), ($, numbers) => {
   *   $.return(numbers.groupSum(($, x) => x.remainder(2n)));
   * });
   * const compiled = East.compile(sumByParity.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n]));  // { 0n: 6n, 1n: 4n }
   * ```
   */
  groupSum<K2>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: Expr<FunctionType<[K], IntegerType>>): DictExpr<K2, IntegerType>
  groupSum<K2>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: Expr<FunctionType<[K], FloatType>>): DictExpr<K2, FloatType>
  groupSum<K2, ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: ValueFn): DictExpr<K2, TypeOf<ReturnType<ValueFn>>>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[K], IntegerType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, IntegerType>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[K], FloatType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, TypeOf<ReturnType<ValueFn>>>
  groupSum<K2>(keyFn: Expr<FunctionType<[K], K2>>): K extends IntegerType | FloatType ? DictExpr<K2, K> : never
  groupSum<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn): K extends IntegerType | FloatType ? DictExpr<TypeOf<ReturnType<KeyFn>>, K> : never
  groupSum(keyFn: any, valueFn?: any): DictExpr<any, any> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.key_type], undefined));
    const valueType = valueFnAst.type.output as EastType;
    const isInteger = isTypeEqual(valueType, IntegerType);
    const isFloat = isTypeEqual(valueType, FloatType);
    if (!isInteger && !isFloat) {
      throw new Error(`Can only perform groupSum on Integer or Float values, got ${printType(valueType)}`);
    }
    return this.toDict(
      ((_$: any, key: any) => Expr.fromAst(keyFnAst)(key)) as any,
      ((_$: any, key: any) => Expr.fromAst(valueFnAst)(key)) as any,
      ((_$: any, a: any, b: any) => a.add(b)) as any
    );
  }

  /**
   * Computes the arithmetic mean (average) of elements in each group.
   *
   * @param keyFn - Function that computes the grouping key
   * @param valueFn - Optional projection function for values (defaults to identity)
   * @returns A DictExpr mapping each group key to the mean value (always float)
   *
   * @see {@link groupSum} to calculate the sum instead of mean
   *
   * @example
   * ```ts
   * // Calculate mean of numbers in each parity group
   * const meanByParity = East.function([SetType(IntegerType)], DictType(IntegerType, FloatType), ($, numbers) => {
   *   $.return(numbers.groupMean(($, x) => x.remainder(2n)));
   * });
   * const compiled = East.compile(meanByParity.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n]));  // { 0n: 3.0, 1n: 2.0 }
   * ```
   */
  groupMean<K2>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: Expr<FunctionType<[K], IntegerType | FloatType>>): DictExpr<K2, FloatType>
  groupMean<K2, ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: Expr<FunctionType<[K], K2>>, valueFn: ValueFn): DictExpr<K2, FloatType>
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: Expr<FunctionType<[K], IntegerType | FloatType>>): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any), ValueFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn, valueFn: ValueFn): DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType>
  groupMean<K2>(keyFn: Expr<FunctionType<[K], K2>>): K extends IntegerType | FloatType ? DictExpr<K2, FloatType> : never
  groupMean<KeyFn extends (($: BlockBuilder<NeverType>, key: ExprType<K>) => any)>(keyFn: KeyFn): K extends IntegerType | FloatType ? DictExpr<TypeOf<ReturnType<KeyFn>>, FloatType> : never
  groupMean(keyFn: any, valueFn?: any): DictExpr<any, FloatType> {
    const keyFnAst = valueOrExprToAstTyped(keyFn, FunctionType([this.key_type], undefined));
    const valueFnAst = valueOrExprToAstTyped(valueFn ?? ((_$: any, x: any) => x), FunctionType([this.key_type], undefined));
    const valueType = valueFnAst.type.output as EastType;
    const isInteger = isTypeEqual(valueType, IntegerType);
    const isFloat = isTypeEqual(valueType, FloatType);
    if (!isInteger && !isFloat) {
      throw new Error(`Can only perform groupMean on Integer or Float values, got ${printType(valueType)}`);
    }
    return this.toDict(
      ((_$: any, key: any) => Expr.fromAst(keyFnAst)(key)) as any,
      ((_$: any, key: any) => {
        const val = Expr.fromAst(valueFnAst)(key);
        return { sum: isInteger ? (val as IntegerExpr).toFloat() : val, count: 1n };
      }) as any,
      ((_$: any, a: any, b: any) => ({ sum: a.sum.add(b.sum), count: a.count.add(b.count) })) as any
    ).map(((_$: any, v: any) => v.sum.divide(v.count.toFloat())) as any) as any;
  }

  // Common reducers are provided, based on reduce

  /**
   * Returns true if all elements satisfy a condition (or are true for boolean sets).
   *
   * @param fn - Optional predicate function to test each element (required for non-boolean sets)
   * @returns A BooleanExpr that is true if all elements pass the test, false otherwise
   *
   * @remarks
   * - Empty sets always return true
   * - Short-circuits on the first false element for efficiency
   * - For boolean sets, the function parameter can be omitted
   *
   * @see {@link some} to check if at least one element satisfies the condition
   *
   * @example
   * ```ts
   * // Check if all numbers are positive
   * const allPositive = East.function([SetType(IntegerType)], BooleanType, ($, numbers) => {
   *   $.return(numbers.every(($, n) => n.greaterThan(0n)));
   * });
   * const compiled = East.compile(allPositive.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]));    // true
   * compiled(new Set([1n, -2n, 3n]));   // false
   * compiled(new Set([]));              // true (empty set)
   * ```
   *
   * @example
   * ```ts
   * // For boolean sets, no function needed
   * const allTrue = East.function([SetType(BooleanType)], BooleanType, ($, flags) => {
   *   $.return(flags.every());
   * });
   * const compiled = East.compile(allTrue.toIR(), []);
   * compiled(new Set([true, true]));   // true
   * compiled(new Set([true, false]));  // false
   * ```
   */
  every(fn?: SubtypeExprOrValue<FunctionType<[K], BooleanType>>): BooleanExpr {
    if (fn === undefined) {
      if (!isTypeEqual(this.key_type as EastType, BooleanType)) {
        throw new Error(`Can only perform every on set of booleans, got ${printType(this.key_type as EastType)}`);
      }
      // Short-circuit on first false value - use explicit function AST to avoid type inference issues
      const optionType = VariantType({ none: NullType, some: NullType });
      const paramVariable: AST = {
        ast_type: "Variable",
        type: this.key_type as EastType,
        location: get_location(),
        mutable: false,
      };
      // Check if boolean is NOT true, then return some(null) to stop, otherwise return none to continue
      const notCondition: AST = {
        ast_type: "Builtin",
        type: BooleanType,
        location: get_location(),
        builtin: "BooleanNot",
        type_parameters: [],
        arguments: [paramVariable]
      };
      const checkFnAst: AST = {
        ast_type: "Function",
        type: FunctionType([this.key_type as EastType], optionType) as any,
        location: get_location(),
        parameters: [paramVariable as any],
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
        builtin: "SetFirstMap",
        type_parameters: [this.key_type as EastType, NullType],
        arguments: [this[AstSymbol], checkFnAst],
      });
      return Expr.match(result, { some: () => false, none: () => true }) as BooleanExpr;
    }

    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.key_type], BooleanType));

    // Short-circuit on first false value
    const result = this.firstMap(($, k) => {
      const result = Expr.fromAst(fnAst)(k as any) as BooleanExpr;
      return result.not().ifElse(() => some(null), () => none);
    });
    return Expr.match(result, { some: () => false, none: () => true });
  }

  /**
   * Returns true if at least one element satisfies a condition (or is true for boolean sets).
   *
   * @param fn - Optional predicate function to test each element (required for non-boolean sets)
   * @returns A BooleanExpr that is true if any element passes the test, false otherwise
   *
   * @remarks
   * - Empty sets always return false
   * - Short-circuits on the first true element for efficiency
   * - For boolean sets, the function parameter can be omitted
   *
   * @see {@link every} to check if all elements satisfy the condition
   *
   * @example
   * ```ts
   * // Check if any number is negative
   * const hasNegative = East.function([SetType(IntegerType)], BooleanType, ($, numbers) => {
   *   $.return(numbers.some(($, n) => n.lessThan(0n)));
   * });
   * const compiled = East.compile(hasNegative.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]));    // false
   * compiled(new Set([1n, -2n, 3n]));   // true
   * compiled(new Set([]));              // false (empty set)
   * ```
   *
   * @example
   * ```ts
   * // For boolean sets, no function needed
   * const anyTrue = East.function([SetType(BooleanType)], BooleanType, ($, flags) => {
   *   $.return(flags.some());
   * });
   * const compiled = East.compile(anyTrue.toIR(), []);
   * compiled(new Set([false, false]));  // false
   * compiled(new Set([false, true]));   // true
   * ```
   */
  some(fn?: SubtypeExprOrValue<FunctionType<[K], BooleanType>>): BooleanExpr {
    if (fn === undefined) {
      if (!isTypeEqual(this.key_type as EastType, BooleanType)) {
        throw new Error(`Can only perform some on set of booleans, got ${printType(this.key_type as EastType)}`);
      }
      // Short-circuit on first true value - use explicit function AST to avoid type inference issues
      const optionType = VariantType({ none: NullType, some: NullType });
      const paramVariable: AST = {
        ast_type: "Variable",
        type: this.key_type as EastType,
        location: get_location(),
        mutable: false,
      };
      // Check if boolean is true, then return some(null) to stop, otherwise return none to continue
      const checkFnAst: AST = {
        ast_type: "Function",
        type: FunctionType([this.key_type as EastType], optionType) as any,
        location: get_location(),
        parameters: [paramVariable as any],
        body: {
          ast_type: "IfElse",
          type: optionType as any,
          location: get_location(),
          ifs: [{
            predicate: paramVariable,
            body: { ast_type: "Variant", type: optionType as any, location: get_location(), case: "some", value: { ast_type: "Value", type: NullType, location: get_location(), value: null } }
          }],
          else_body: { ast_type: "Variant", type: optionType as any, location: get_location(), case: "none", value: { ast_type: "Value", type: NullType, location: get_location(), value: null } }
        }
      };
      const result: any = Expr.fromAst({
        ast_type: "Builtin",
        type: optionType as any,
        location: get_location(),
        builtin: "SetFirstMap",
        type_parameters: [this.key_type as EastType, NullType],
        arguments: [this[AstSymbol], checkFnAst],
      });
      return Expr.match(result, { some: () => true, none: () => false }) as BooleanExpr;
    }

    const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.key_type], BooleanType));

    // Short-circuit on first true value
    const result = this.firstMap(($, k) => {
      const result = Expr.fromAst(fnAst)(k as any) as BooleanExpr;
      return result.ifElse(() => some(null), () => none);
    });
    return Expr.match(result, { some: () => true, none: () => false });
  }
  
  /**
   * Computes the sum of all elements in the set.
   *
   * @param fn - Optional function to map each element to a number (required for non-numeric sets)
   * @returns An IntegerExpr or FloatExpr containing the sum
   *
   * @remarks
   * - For integer sets, returns an IntegerExpr
   * - For float sets, returns a FloatExpr
   * - Empty sets return 0n (integer) or 0.0 (float)
   * - For non-numeric sets, a mapping function must be provided
   *
   * @see {@link mean} to calculate the average value
   *
   * @example
   * ```ts
   * // Sum numeric elements
   * const sumNumbers = East.function([SetType(IntegerType)], IntegerType, ($, numbers) => {
   *   $.return(numbers.sum());
   * });
   * const compiled = East.compile(sumNumbers.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n]));  // 10n
   * ```
   *
   * @example
   * ```ts
   * // Sum with mapping function
   * const sumLengths = East.function([SetType(StringType)], IntegerType, ($, words) => {
   *   $.return(words.sum(($, word) => word.size()));
   * });
   * const compiled = East.compile(sumLengths.toIR(), []);
   * compiled(new Set(["hi", "bye"]));  // 5n (2 + 3)
   * ```
   */
  sum(fn: Expr<FunctionType<[K], IntegerType>>): IntegerExpr
  sum(fn: Expr<FunctionType<[K], FloatType>>): FloatExpr
  sum<F extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any)>(fn: F): TypeOf<ReturnType<F>> extends IntegerType ? IntegerExpr : TypeOf<ReturnType<F>> extends FloatType ? FloatExpr : never
  sum(): K extends IntegerType | FloatType ? ExprType<K> : never
  sum(fn?: any): Expr<IntegerType | FloatType> {
    if (fn === undefined) {
      if (!(isTypeEqual(this.key_type as EastType, IntegerType) || isTypeEqual(this.key_type as EastType, FloatType))) {
        throw new Error(`Can only perform sum on set of numbers (Integer or Float), got ${printType(this.key_type as EastType)}`);
      }
      const zero = isTypeEqual(this.key_type as EastType, IntegerType) ? 0n : 0.0;
      return this.reduce(($, previous, value) => previous.add(value as any) as any, zero) as any;
    } else {
      const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.key_type], undefined));
      const returnType = fnAst.type.output as EastType;
      if (!(isTypeEqual(returnType, IntegerType) || isTypeEqual(returnType, FloatType))) {
        throw new Error(`Can only perform sum on array of numbers (Integer or Float), got ${printType(returnType)}`);
      }
      const zero = isTypeEqual(returnType, IntegerType) ? 0n : 0.0;
      return this.reduce(($, previous, key) => previous.add(Expr.fromAst(fnAst)(key as any) as any) as any, zero) as any;
    }
  }

  /**
   * Computes the arithmetic mean (average) of all elements in the set.
   *
   * @param fn - Optional function to map each element to a number (required for non-numeric sets)
   * @returns A FloatExpr containing the mean value
   *
   * @remarks
   * - Always returns a float, even for integer sets
   * - Empty sets return NaN
   * - Integer values are automatically converted to floats
   * - For non-numeric sets, a mapping function must be provided
   *
   * @see {@link sum} to calculate the total sum
   *
   * @example
   * ```ts
   * // Calculate mean of numbers
   * const average = East.function([SetType(IntegerType)], FloatType, ($, numbers) => {
   *   $.return(numbers.mean());
   * });
   * const compiled = East.compile(average.toIR(), []);
   * compiled(new Set([1n, 2n, 3n, 4n]));  // 2.5
   * compiled(new Set([]));                // NaN
   * ```
   *
   * @example
   * ```ts
   * // Mean with mapping function
   * const avgLength = East.function([SetType(StringType)], FloatType, ($, words) => {
   *   $.return(words.mean(($, word) => word.size()));
   * });
   * const compiled = East.compile(avgLength.toIR(), []);
   * compiled(new Set(["hi", "hello"]));  // 3.5 ((2 + 5) / 2)
   * ```
   */
  mean(fn: Expr<FunctionType<[K], IntegerType>>): FloatExpr
  mean(fn: Expr<FunctionType<[K], FloatType>>): FloatExpr
  mean<F extends (($: BlockBuilder<NeverType>, k: ExprType<K>) => any)>(fn: F): TypeOf<ReturnType<F>> extends IntegerType | FloatType ? FloatExpr : never
  mean(): K extends IntegerType | FloatType ? FloatExpr : never
  mean(fn?: any): Expr<FloatType> {
    if (fn === undefined) {
      if (isTypeEqual(this.key_type as EastType, IntegerType)) {
        return this.reduce(($, previous, value) => previous.add((value as IntegerExpr).toFloat()), 0.0).divide(this.size().toFloat());
      } else if (isTypeEqual(this.key_type as EastType, FloatType)) {
        return this.reduce(($, previous, value) => previous.add(value as FloatExpr), 0.0).divide(this.size().toFloat());
      } else {
        throw new Error(`Can only perform mean on set of numbers (Integer or Float), got ${printType(this.key_type as EastType)}`);
      }
    } else {
      const fnAst = valueOrExprToAstTyped(fn, FunctionType([this.key_type], undefined));
      const returnType = fnAst.type.output as EastType;
      if (isTypeEqual(returnType, IntegerType)) {
        return this.reduce(($, previous: any, key) => previous.add((Expr.fromAst(fnAst)(key as any) as IntegerExpr).toFloat()) as FloatExpr, 0.0).divide(this.size().toFloat());
      } else if (isTypeEqual(returnType, FloatType)) {
        return this.reduce(($, previous, key) => previous.add(Expr.fromAst(fnAst)(key as any) as FloatExpr), 0.0).divide(this.size().toFloat());
      } else {
        throw new Error(`Can only perform mean on set of numbers (Integer or Float), got ${printType(returnType)}`);
      }
    }
  }

  /**
   * Checks if this set equals another set (same elements).
   *
   * @param other - The set to compare against
   * @returns A BooleanExpr that is true if the sets are equal
   *
   * @example
   * ```ts
   * const isEqual = East.function([SetType(IntegerType), SetType(IntegerType)], BooleanType, ($, a, b) => {
   *   $.return(a.equals(b));
   * });
   * const compiled = East.compile(isEqual.toIR(), []);
   * compiled(new Set([1n, 2n, 3n]), new Set([1n, 2n, 3n]));  // true
   * compiled(new Set([1n, 2n]), new Set([1n, 2n, 3n]));      // false
   * ```
   */
  equals(other: SetExpr<K> | Set<SubtypeExprOrValue<K>>): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this set does not equal another set.
   *
   * @param other - The set to compare against
   * @returns A BooleanExpr that is true if the sets are not equal
   *
   * @example
   * ```ts
   * const isNotEqual = East.function([SetType(IntegerType), SetType(IntegerType)], BooleanType, ($, a, b) => {
   *   $.return(a.notEquals(b));
   * });
   * const compiled = East.compile(isNotEqual.toIR(), []);
   * compiled(new Set([1n, 2n]), new Set([1n, 2n, 3n]));      // true
   * compiled(new Set([1n, 2n, 3n]), new Set([1n, 2n, 3n]));  // false
   * ```
   */
  notEquals(other: SetExpr<K> | Set<SubtypeExprOrValue<K>>): BooleanExpr {
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