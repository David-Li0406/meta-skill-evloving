/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { isRef, type ref } from "./containers/ref.js";
import { SortedMap } from "./containers/sortedmap.js";
import { SortedSet } from "./containers/sortedset.js";
import { type variant, variant_symbol } from "./containers/variant.js";

/**
 * Error thrown when type operations encounter incompatible types.
 *
 * @remarks
 * Used by type union, intersection, and equality operations when types
 * cannot be combined or compared as requested.
 */
class TypeMismatchError extends Error {
  constructor(message: string, options?: ErrorOptions) {
    super(message, options);
    this.name = "TypeMismatchError";
  }
}

/** Represents the Never type (bottom type) in East's type system. */
export type NeverType = { type: "Never" };
/** Singleton instance of the Never type. */
export const NeverType: NeverType = { type: "Never" };

/** Represents the Null type (unit type) in East's type system. */
export type NullType = { type: "Null" };
/** Singleton instance of the Null type. */
export const NullType: NullType = { type: "Null" };

/** Represents the Boolean type in East's type system. */
export type BooleanType = { type: "Boolean" };
/** Singleton instance of the Boolean type. */
export const BooleanType: BooleanType = { type: "Boolean" };

/** Represents the Integer type (arbitrary-precision integers) in East's type system. */
export type IntegerType = { type: "Integer" };
/** Singleton instance of the Integer type. */
export const IntegerType: IntegerType = { type: "Integer" };

/** Represents the Float type (64-bit floating point) in East's type system. */
export type FloatType = { type: "Float" };
/** Singleton instance of the Float type. */
export const FloatType: FloatType = { type: "Float" };

/** Represents the String type in East's type system. */
export type StringType = { type: "String" };
/** Singleton instance of the String type. */
export const StringType: StringType = { type: "String" };

/** Represents the DateTime type in East's type system. */
export type DateTimeType = { type: "DateTime" };
/** Singleton instance of the DateTime type. */
export const DateTimeType: DateTimeType = { type: "DateTime" };

/** Represents the Blob type (immutable binary data) in East's type system. */
export type BlobType = { type: "Blob" };
/** Singleton instance of the Blob type. */
export const BlobType: BlobType = { type: "Blob" };

/**
 * Represents a reference type in East's type system.
 * 
 * Conceptually, a reference is a box or cell that can hold a value of a specified type.
 * The reference can be mutated by updating the contents of the reference.
 * Multiple references can point to the same underlying value.
 *
 * @typeParam T - The type of value held by the reference
 */
export type RefType<T = any> = { type: "Ref", value: T };
/**
 * Constructs a reference (or cell) type with the specified element type.
 *
 * Conceptually, a reference is a box or cell that can hold a value of a specified type.
 * The reference can be mutated by updating the contents of the reference.
 * Multiple references can point to the same underlying value.
 *
 * @typeParam T - The type of value held by the reference
 * @param type - The element type
 * @returns A reference type
 * @throws When the element type contains functions
 */
export function RefType<const T>(type: T): RefType<T> {
  return { type: "Ref", value: type };
};

/**
 * Represents an Array type in East's type system.
 *
 * @typeParam T - The type of elements in the array
 */
export type ArrayType<T = any> = { type: "Array", value: T };
/**
 * Constructs an Array type with the specified element type.
 *
 * @typeParam T - The type of elements in the array
 * @param type - The element type
 * @returns An Array type
 * @throws When the element type contains functions
 */
export function ArrayType<const T>(type: T): ArrayType<T> {
  return { type: "Array", value: type };
};

/**
 * Represents a Set type in East's type system.
 *
 * @typeParam T - The type of keys in the set
 *
 * @remarks
 * Sets are mutable and sorted. Keys must be immutable types with a total ordering.
 */
export type SetType<T = any> = { type: "Set", key: T };
/**
 * Constructs a Set type with the specified key type.
 *
 * @typeParam T - The type of keys in the set
 * @param type - The key type
 * @returns A Set type
 * @throws When the key type is not immutable
 */
export function SetType<const T>(type: T): SetType<T> {
  if (typeof type !== "string" && !isImmutableType(type as EastType)) {
    throw new Error(`Set key type must be an immutable type, got ${printType(type as EastType)}`);
  }
  return { type: "Set", key: type };
};

/**
 * Represents a Dict type in East's type system.
 *
 * @typeParam K - The type of keys in the dictionary
 * @typeParam T - The type of values in the dictionary
 *
 * @remarks
 * Dicts are mutable and sorted by key. Keys must be immutable types with a total ordering.
 */
export type DictType<K = any, T = any> = { type: "Dict", key: K, value: T };
/**
 * Constructs a Dict type with the specified key and value types.
 *
 * @typeParam K - The type of keys in the dictionary
 * @typeParam T - The type of values in the dictionary
 * @param key - The key type
 * @param value - The value type
 * @returns A Dict type
 * @throws When the key type is not immutable or value type contains functions
 */
export function DictType<const K, const T>(key: K, value: T): DictType<K, T> {
  if (typeof key !== "string" && !isImmutableType(key as EastType)) {
    throw new Error(`Dict key type must be an immutable type, got ${printType(key as EastType)}`);
  }
  return { type: "Dict", key, value };
};

/**
 * Represents a Struct type (product type) in East's type system.
 *
 * @typeParam Fields - Object type mapping field names to their types
 *
 * @remarks
 * Structs are immutable and field order is significant for structural typing.
 */
export type StructType<Fields extends { [K in string]: any } = { [K in string]: any }> = { type: "Struct", fields: Fields };
/**
 * Constructs a Struct type with the specified field types.
 *
 * @typeParam Fields - Object type mapping field names to their types
 * @param field_types - Object mapping field names to {@link EastType} instances
 * @returns A Struct type
 */
export function StructType<const Fields extends { [K in string]: any }>(field_types: Fields): StructType<Fields> {
  return { type: "Struct", fields: field_types };
};

/**
 * Represents a Variant type (sum type) in East's type system.
 *
 * @typeParam Cases - Object type mapping case names to their value types
 *
 * @remarks
 * Variants are immutable and cases are automatically sorted alphabetically by name.
 */
export type VariantType<Cases extends { [K in string]: any } = { [K in string]: any }> = { type: "Variant", cases: Cases };
/**
 * Constructs a Variant type with the specified cases.
 *
 * @typeParam Cases - Object type mapping case names to their value types
 * @param case_types - Object mapping case names to {@link EastType} instances
 * @returns A Variant type with cases sorted alphabetically
 */
export function VariantType<const Cases extends { [K in string]: any }>(case_types: Cases): VariantType<Cases> {
  // Cases are sorted alphabetically by their name
  const cases_sorted = Object.fromEntries(Object.entries(case_types).sort((x, y) => x[0] < y[0] ? -1 : x[0] === y[0] ? 0 : 1)) as Cases;
  return { type: "Variant", cases: cases_sorted };
};

/**
 * Validates that a recursive type has SCC (Strongly Connected Component) size 1.
 *
 * @param type - The type to validate
 * @param allowedMarker - The recursive marker that is allowed (the one being defined)
 * @throws When nested RecursiveTypes with cross-references are detected
 *
 * @remarks
 * This ensures that recursive types don't have mutual recursion or nested
 * RecursiveTypes that reference outer scopes. Only simple recursion (SCC size 1)
 * is supported for predictable behavior and implementation simplicity.
 */
function validateNotMutuallyRecursive(type: EastType | string, allowedMarker: RecursiveType<undefined>): void {
  const visited = new Set<EastType>();

  function check(t: EastType | string, allowed: boolean): void {
    // Skip string placeholders (used for generic builtins)
    if (typeof t === "string") return;

    if (typeof t !== "object" || t === null) {
      let allowedMarkerString: string | null = null;
      try {
        allowedMarkerString = printType(allowedMarker);
      } catch {}

      throw new Error(`Invalid type encountered during recursion validation: ${t}${allowedMarkerString === null ? "" : ` (allowed marker: ${allowedMarkerString})`}`);
    }

    // Skip allowedMarker
    if (t === allowedMarker) {
      if (!allowed) {
        throw new Error("RecursiveType cannot pass into set keys, dictionary keys, or function input/output types");
      }
      return;
    }

    // Avoid infinite loops
    if (visited.has(t)) return;
    visited.add(t);

    if (t.type === "Recursive") {
      if (t.node === undefined) {
        throw new Error(
          "RecursiveType must have SCC size 1: nested RecursiveTypes with cross-references are not supported. " +
          "Each RecursiveType can only reference itself, not other recursive scopes."
        );
      } else {
        // Recurse into the recursive type's body, with t as the new root
        validateNotMutuallyRecursive(t.node, t);
      }
    } else if (t.type === "Struct") {
      for (const [_, field_type] of Object.entries(t.fields)) {
        check(field_type, allowed);
      }
    } else if (t.type === "Variant") {
      for (const [_, case_type] of Object.entries(t.cases)) {
        check(case_type, allowed);
      }
    } else if (t.type === "Ref") {
      check(t.value, allowed);
    } else if (t.type === "Array") {
      check(t.value, allowed);
    } else if (t.type === "Set") {
      check(t.key, false);
    } else if (t.type === "Dict") {
      check(t.key, false);
      check(t.value, allowed);
    } else if (t.type === "Function") {
      t.inputs.forEach(input => check(input, allowed));
      check(t.output, allowed);
    } else if (t.type === "AsyncFunction") {
      t.inputs.forEach(input => check(input, allowed));
      check(t.output, allowed);
    }
    // Primitive types don't need recursion
  }

  check(type, true);
}

export type RecursiveTypeMarker = { type: "Recursive" };

/**
 * Represents a recursive data type in East's type system.
 *
 * @typeParam T - the type of each node in the recursive structure
 *
 * @remarks
 * Recursive data types can be used to represent tree-like structures or circular data structures.
 * Only simple recursion (SCC size 1) is supported - nested RecursiveTypes with cross-references
 * will throw an error during construction.
 */
export type RecursiveType<Node = any> = { type: "Recursive", node: Node };
/**
 * Constructs a recursive type with the specified node structure.
 *
 * @typeParam F - Function type that defines the recursive structure
 * @param f - Function that receives a self-reference marker and returns the node type
 * @returns A RecursiveType representing the recursive structure
 * @throws When the type contains functions or has SCC size > 1 (mutual recursion)
 *
 * @remarks
 * The function `f` receives a `RecursiveTypeMarker` representing the recursive
 * reference point. This marker should be used wherever the type recursively refers to itself.
 *
 * Only simple recursion is supported - the type can reference itself multiple times, but
 * nested RecursiveTypes with cross-references (mutual recursion) are not allowed.
 *
 * @example
 * ```ts
 * // Linked list
 * const ListType = RecursiveType(self =>
 *   VariantType({
 *     nil: NullType,
 *     cons: StructType({ head: IntegerType, tail: self })
 *   })
 * );
 *
 * // Binary tree
 * const TreeType = RecursiveType(self =>
 *   StructType({
 *     value: IntegerType,
 *     left: OptionType(self),
 *     right: OptionType(self)
 *   })
 * );
 * ```
 */
export function RecursiveType<F extends (self: RecursiveTypeMarker) => EastType>(f: F): RecursiveType<ReturnType<F>> {
  const ret = { type: "Recursive", node: undefined } as any;
  const type = f(ret);
  (ret as any).node = type;

  // Validate SCC size 1 (no nested RecursiveTypes with cross-references)
  validateNotMutuallyRecursive(type, ret);

  return ret as RecursiveType<ReturnType<F>>;
};

/**
 * Represents a Function type in East's type system.
 *
 * @typeParam I - Tuple type of input parameter types
 * @typeParam O - The output/return type
 *
 * @remarks
 * Functions are first-class values that can be serialized as IR but not as data.
 * The `platforms` field tracks which platform functions are invoked by this function
 * (transitively through any called functions), enabling effect tracking and async analysis.
 * 
 * @see {@link AsyncFunctionType} for asynchronous functions.
 */
export type FunctionType<I extends any[] = any[], O extends any = any> = { type: "Function", inputs: I, output: O };
/**
 * Constructs a Function type with the specified input and output types.
 *
 * @param inputs - Array of {@link EastType} instances for each parameter
 * @param output - The {@link EastType} of the return value
 * @returns A Function type
 * 
 * @see {@link AsyncFunctionType} for asynchronous functions.
 */
export function FunctionType<const I extends any[], const O extends any>(inputs: I, output: O): FunctionType<I, O> {
  return { type: "Function", inputs, output };
};

/**
 * Represents an asynchronous Function type in East's type system.
 *
 * @typeParam I - Tuple type of input parameter types
 * @typeParam O - The output/return type
 *
 * @remarks
 * Functions are first-class values that can be serialized as IR but not as data.
 * The `platforms` field tracks which platform functions are invoked by this function
 * (transitively through any called functions), enabling effect tracking and async analysis.
 * 
 * @see {@link FunctionType} for synchronous functions.
 */
export type AsyncFunctionType<I extends any[] = any[], O extends any = any> = { type: "AsyncFunction", inputs: I, output: O };
/**
 * Constructs an AsyncFunction type with the specified input and output types.
 *
 * @param inputs - Array of {@link EastType} instances for each parameter
 * @param output - The {@link EastType} of the return value
 * @returns An AsyncFunction type
 * 
 * @see {@link AsyncFunctionType} for asynchronous functions.
 */
export function AsyncFunctionType<const I extends any[], const O extends any>(inputs: I, output: O): AsyncFunctionType<I, O> {
  return { type: "AsyncFunction", inputs, output };
};


/**
 * Union of all East types.
 *
 * @remarks
 * This includes all primitive types, compound types, and function types.
 */
export type EastType =
  | NeverType
  | NullType
  | BooleanType
  | IntegerType
  | FloatType
  | DateTimeType
  | StringType
  | BlobType
  | RefType
  | ArrayType
  | SetType
  | DictType
  | StructType
  | VariantType
  | RecursiveType
  | FunctionType
  | AsyncFunctionType;

/**
 * Union of all East data types (excludes {@link FunctionType} and {@link AsyncFunctionType}).
 *
 * @remarks
 * Data types have a total ordering, can be fully serialized and transmitted between runtimes.
 * Functions can be serialized as IR but not as pure data.
 */
export type DataType =
  | NeverType
  | NullType
  | BooleanType
  | IntegerType
  | FloatType
  | DateTimeType
  | StringType
  | BlobType
  | RefType
  | ArrayType
  | SetType
  | DictType
  | StructType
  | VariantType
  | RecursiveType;

/**
 * Union of all immutable East types.
 *
 * @remarks
 * Immutable types can be used as dictionary keys and set elements.
 * Excludes {@link RefType}, {@link ArrayType}, {@link SetType}, {@link DictType}, {@link FunctionType} and {@link AsyncFunctionType}.
 */
export type ImmutableType =
  | NeverType
  | NullType
  | BooleanType
  | IntegerType
  | FloatType
  | StringType
  | DateTimeType
  | BlobType
  | StructType
  | VariantType
  | RecursiveType;

/**
 * Checks if a type is a pure data type (excludes functions).
 *
 * @param type - The {@link EastType} to check
 * @param recursive_type - Internal parameter for tracking the current recursive type being checked
 * @returns `true` if the type is a pure data type, `false` if it contains functions
 *
 * @remarks
 * Data types have a total ordering, can be fully serialized and transmitted between runtimes.
 */
export function isDataType(type: EastType, recursive_type?: EastType): type is DataType {
  // Avoid infinite loops
  if (type === recursive_type) {
    return true;
  }

  if (type.type === "Ref") {
    return isDataType(type.value, recursive_type);
  } else if (type.type === "Array") {
    return isDataType(type.value, recursive_type);
  } else if (type.type === "Set") {
    // Set constructors check their key type is an (immutable) data type
    return true;
  } else if (type.type === "Dict") {
    // Dict constructors check their key type is an (immutable) data type
    return isDataType(type.value, recursive_type);
  } else if (type.type === "Struct") {
    for (const field_type of Object.values(type.fields)) {
      if (!isDataType(field_type, recursive_type)) {
        return false;
      }
    }
    return true;
  } else if (type.type === "Variant") {
    for (const variant of Object.values(type.cases)) {
      if (!isDataType(variant, recursive_type)) {
        return false;
      }
    }
    return true;
  } else if (type.type === "Recursive") {
    return type.node === recursive_type ? true : isDataType(type.node, type);
  } else if (type.type === "Function") {
    return false;
  } else if (type.type === "AsyncFunction") {
    return false;
  } else {
    // Primitive types are data types
    return true
  }
}

/**
 * Checks if a type is immutable (can be used as dict keys or set elements).
 *
 * @param type - The {@link EastType} to check
 * @param recursive_type - Internal parameter for tracking the current recursive type being checked
 * @returns `true` if the type is immutable, `false` if it contains mutable collections or functions
 *
 * @remarks
 * Immutable types exclude {@link ArrayType}, {@link SetType}, {@link DictType}, {@link FunctionType} and {@link AsyncFunctionType}.
 */
export function isImmutableType(type: EastType, recursive_type?: EastType): type is ImmutableType {
  // Avoid infinite loops
  if (type === recursive_type) {
    return true;
  }

  if (type.type === "Ref") {
    // Refs are mutable
    return false;
  } else if (type.type === "Array") {
    // Arrays are mutable
    return false;
  } else if (type.type === "Set") {
    // Set are mutable
    return false;
  } else if (type.type === "Dict") {
    // Dict are mutable
    return false;
  } else if (type.type === "Struct") {
    for (const field_type of Object.values(type.fields)) {
      if (!isImmutableType(field_type, recursive_type)) {
        return false;
      }
    }
    return true;
  } else if (type.type === "Variant") {
    for (const variant of Object.values(type.cases)) {
      if (!isImmutableType(variant, recursive_type)) {
        return false;
      }
    }
    return true;
  } else if (type.type === "Recursive") {
    return type.node === recursive_type ? true : isImmutableType(type.node, type);
  } else if (type.type === "Function") {
    // Functions are not data types, and "immutable data" is a subset of "data"
    return false;
  } else if (type.type === "AsyncFunction") {
    // Functions are not data types, and "immutable data" is a subset of "data"
    return false;
  } else {
    // Primitive types are immutable
    return true;
  }
}

/**
 * Maps an East type to its corresponding TypeScript value type.
 *
 * @typeParam T - The {@link EastType} to convert
 * @typeParam Node - Internal parameter for tracking the current recursive type node
 * @typeParam Depth - Internal parameter for preventing infinite recursion in TypeScript
 *
 * @remarks
 * This type-level function converts East types to their runtime TypeScript equivalents:
 * - {@link IntegerType} → `bigint`
 * - {@link RefType} → {@link ref} objects
 * - {@link ArrayType} → JavaScript `Array`
 * - {@link SetType} → JavaScript `Set`
 * - {@link DictType} → JavaScript `Map`
 * - {@link VariantType} → {@link variant} objects
 * - {@link RecursiveType} → recursive JavaScript values (no wrapper)
 * - {@link FunctionType} → JavaScript functions
 */
export type ValueTypeOf<T> =
  T extends NeverType ? never :
  T extends NullType ? null :
  T extends BooleanType ? boolean :
  T extends IntegerType ? bigint :
  T extends FloatType ? number :
  T extends StringType ? string :
  T extends DateTimeType ? Date :
  T extends BlobType ? Uint8Array :
  T extends RefType<infer U> ? ref<ValueTypeOf<U>> :
  T extends ArrayType<infer U> ? ValueTypeOf<U>[] :
  T extends SetType<infer U> ? Set<ValueTypeOf<U>> :
  T extends DictType<infer U, infer V> ? Map<ValueTypeOf<U>, ValueTypeOf<V>> :
  T extends StructType<infer U> ? keyof U extends never ? { [K in never]: never } : { [K in keyof U]: U[K] extends undefined ? never : ValueTypeOf<Exclude<U[K], undefined>> } :
  T extends VariantType<infer U> ? Exclude<{ [K in keyof U]: U[K] extends undefined ? never : { type: K, value: ValueTypeOf<Exclude<U[K], undefined>>, [variant_symbol]: null } }[keyof U], undefined> :
  T extends RecursiveType<infer U> ? ValueTypeOf<U> :
  T extends RecursiveTypeMarker ? any : // make TypeScript faster - don't expand further
  T extends FunctionType<infer I, infer O> ? (...inputs: { [K in keyof I]: ValueTypeOf<I[K]> }) => ValueTypeOf<O> :
  T extends AsyncFunctionType<infer I, infer O> ? (...inputs: { [K in keyof I]: ValueTypeOf<I[K]> }) => Promise<ValueTypeOf<O>> :
  any;

// export type ValueTypeOf<_T> = any;

/**
 * Maps a TypeScript value type to its corresponding East type (type-level).
 *
 * @typeParam V - The TypeScript value type to convert
 *
 * @remarks
 * This is the inverse of {@link ValueTypeOf} at the type level.
 * Infers the East type from a TypeScript value type.
 */
export type EastTypeOf<V> =
  V extends never ? NeverType :
  V extends null ? NullType :
  V extends boolean ? BooleanType :
  V extends bigint ? IntegerType :
  V extends number ? FloatType :
  V extends string ? StringType :
  V extends Date ? DateTimeType :
  V extends Uint8Array ? BlobType :
  V extends ref<infer U> ? RefType<EastTypeOf<U>> :
  V extends Array<infer U> ? ArrayType<EastTypeOf<U>> :
  V extends Set<infer K> ? SetType<EastTypeOf<K>> :
  V extends Map<infer K, infer U> ? DictType<EastTypeOf<K>, EastTypeOf<U>> :
  V extends variant<infer Name, infer U> ? Name extends string ? VariantType<{ [K in Name]: EastTypeOf<U> }> : never :
  StructType<{ [K in keyof V]: EastTypeOf<V[K]> }>;

/**
 * Infers the East type from a runtime JavaScript value.
 *
 * @typeParam V - The TypeScript type of the value
 * @param value - The JavaScript value to analyze
 * @returns The corresponding {@link EastType}
 * @throws When the value is a JavaScript function or cannot be typed
 *
 * @remarks
 * This is the runtime version of the {@link EastTypeOf} type.
 * For arrays, it infers the element type from the first element.
 */
export function EastTypeOf<V>(value: V): EastTypeOf<V> {
  if (value === null) {
    return NullType as EastTypeOf<V>;
  } else if (typeof value === "boolean") {
    return BooleanType as EastTypeOf<V>;
  } else if (typeof value === "bigint") {
    return IntegerType as EastTypeOf<V>;
  } else if (typeof value === "number") {
    return FloatType as EastTypeOf<V>;
  } else if (typeof value === "string") {
    return StringType as EastTypeOf<V>;
  } if (value instanceof Date) {
    return DateTimeType as EastTypeOf<V>;
  } else if (value instanceof Uint8Array) {
    return BlobType as EastTypeOf<V>;
  } else if (Array.isArray(value)) {
    if (value.length === 0) {
      throw new Error(`Cannot infer East type of empty array`);
    }
    return ArrayType(EastTypeOf(value[0])) as EastTypeOf<V>;
  } else if (value instanceof Set || value instanceof SortedSet) {
    if (value.size === 0) {
      throw new Error(`Cannot infer East type of empty set`);
    }
    const first = value.values().next().value!;
    return SetType(EastTypeOf(first)) as EastTypeOf<V>;
  } else if (value instanceof Map || value instanceof SortedMap) {
    if (value.size === 0) {
      throw new Error(`Cannot infer East type of empty map`);
    }
    const first = value.entries().next().value!;
    return DictType(EastTypeOf(first[0]), EastTypeOf(first[1])) as EastTypeOf<V>;
  } else if (typeof value === "function") {
    throw new Error(`Javascript functions cannot be converted to East functions`);
  } else if (typeof value === "object") {
    return StructType(Object.fromEntries(Object.entries(value).map(([k, v]) => [k, EastTypeOf(v)]))) as EastTypeOf<V>;
  } else {
    throw new Error(`Cannot determine East type for value ${value}`);
  }
}

/**
 * Checks if two East types are structurally equal.
 *
 * @param t1 - First {@link EastType} to compare
 * @param t2 - Second {@link EastType} to compare
 * @param r1 - Internal parameter for tracking the first recursive type being compared
 * @param r2 - Internal parameter for tracking the second recursive type being compared
 * @returns `true` if the types are equal, `false` otherwise
 *
 * @remarks
 * Performs structural equality checking, recursively comparing compound types.
 * For {@link StructType} and {@link VariantType}, field/case order matters.
 * For {@link RecursiveType}, uses cycle tracking to handle recursive references.
 */
// Cache for memoizing isTypeEqual results (top-level calls only)
const typeEqualCache = new WeakMap<EastType, WeakMap<EastType, boolean>>();

export function isTypeEqual(t1: EastType, t2: EastType, r1: EastType = t1, r2: EastType = t2): boolean {
  // Fast path: reference equality
  if (t1 === t2) return true;

  // Memoization for top-level calls only (r1/r2 are just for internal cycle detection)
  const isTopLevel = r1 === t1 && r2 === t2;
  if (isTopLevel) {
    const innerCache = typeEqualCache.get(t1);
    if (innerCache) {
      const cached = innerCache.get(t2);
      if (cached !== undefined) return cached;
    }
    const result = isTypeEqualImpl(t1, t2, r1, r2);
    // Store result in cache
    let cache = typeEqualCache.get(t1);
    if (!cache) {
      cache = new WeakMap();
      typeEqualCache.set(t1, cache);
    }
    cache.set(t2, result);
    return result;
  }

  return isTypeEqualImpl(t1, t2, r1, r2);
}

function isTypeEqualImpl(t1: EastType, t2: EastType, r1: EastType, r2: EastType): boolean {
  if (t1.type === "Recursive") {
    if (t2.type === "Recursive") {
      if (t1.node === r1) {
        return t2.node === r2;
      } else if (t2.node === r2) {
        return false;
      } else {
        return isTypeEqual(t1.node, t2.node, t1.node, t2.node);
      }
    } else {
      // The RecursiveType wrapper is transparent
      return isTypeEqual(t1.node, t2, t1.node, r2);
    }
  } else if (t2.type === "Recursive") {
    // The RecursiveType wrapper is transparent
    return isTypeEqual(t1, t2.node, r1, t2.node);
  } else if (t1.type === "Never") {
    return t2.type === "Never";
  } else if (t1.type === "Null") {
    return t2.type === "Null";
  } else if (t1.type === "Boolean") {
    return t2.type === "Boolean";
  } else if (t1.type === "Integer") {
    return t2.type === "Integer";
  } else if (t1.type === "Float") {
    return t2.type === "Float";
  } else if (t1.type === "String") {
    return t2.type === "String";
  } else if (t1.type === "DateTime") {
    return t2.type === "DateTime";
  } else if (t1.type === "Blob") {
    return t2.type === "Blob";
  } else if (t1.type === "Ref") {
    if (t2.type === "Ref") {
      return isTypeEqual(t1.value, t2.value, r1, r2);
    } else {
      return false;
    }
  } else if (t1.type === "Array") {
    if (t2.type === "Array") {
      return isTypeEqual(t1.value, t2.value, r1, r2);
    } else {
      return false;
    }
  } else if (t1.type === "Set") {
    if (t2.type === "Set") {
      return isTypeEqual(t1.key, t2.key, r1, r2);
    } else {
      return false;
    }
  } else if (t1.type === "Dict") {
    if (t2.type === "Dict") {
      return isTypeEqual(t1.key, t2.key, r1, r2) && isTypeEqual(t1.value, t2.value, r1, r2);
    } else {
      return false;
    }
  } else if (t1.type === "Struct") {
    if (t2.type === "Struct") {
      const e1 = Object.entries(t1.fields as Record<string, EastType>);
      const e2 = Object.entries(t2.fields as Record<string, EastType>);
      if (e1.length !== e2.length) return false;
      let i = 0;
      for (const [k1, f1] of e1) {
        const [k2, f2] = e2[i]!;
        if (k1 !== k2) return false;
        if (!isTypeEqual(f1, f2, r1, r2)) return false;
        i += 1;
      }
      return true
    } else {
      return false;
    }
  } else if (t1.type === "Variant") {
    if (t2.type === "Variant") {
      const e1 = Object.entries(t1.cases as Record<string, EastType>);
      const e2 = Object.entries(t2.cases as Record<string, EastType>);
      if (e1.length !== e2.length) return false;
      let i = 0;
      for (const [k1, f1] of e1) {
        const [k2, f2] = e2[i]!;
        if (k1 !== k2) return false;
        if (!isTypeEqual(f1, f2, r1, r2)) return false;
        i += 1;
      }
      return true
    } else {
      return false;
    }
  } else if (t1.type === "Function") {
    if (t2.type !== "Function") {
      return false;
    }

    // Check input types match
    if (t1.inputs.length !== t2.inputs.length) {
      return false;
    }
    for (let i = 0; i < t1.inputs.length; i++) {
      if (!isTypeEqual(t1.inputs[i], t2.inputs[i], r1, r2)) {
        return false;
      }
    }

    // Check output type matches
    if (!isTypeEqual(t1.output, t2.output, r1, r2)) {
      return false;
    }

    return true;
  } else if (t1.type === "AsyncFunction") {
    if (t2.type !== "AsyncFunction") {
      return false;
    }

    // Check input types match
    if (t1.inputs.length !== t2.inputs.length) {
      return false;
    }
    for (let i = 0; i < t1.inputs.length; i++) {
      if (!isTypeEqual(t1.inputs[i], t2.inputs[i], r1, r2)) {
        return false;
      }
    }

    // Check output type matches
    if (!isTypeEqual(t1.output, t2.output, r1, r2)) {
      return false;
    }

    return true;
  } else {
    throw new Error(`Unknown type encountered during type equality check: ${(t1 satisfies never as any).type}`);
  }
}

/**
 * Checks if a JavaScript value conforms to an East type.
 *
 * @param value - The JavaScript value to check
 * @param type - The {@link EastType} to validate against
 * @param node_type - Internal parameter for tracking the current recursive type node
 * @param nodes_visited - Internal parameter for tracking visited nodes to detect cycles
 * @returns `true` if the value matches the type, `false` otherwise
 *
 * @remarks
 * Performs runtime type checking, recursively validating compound types.
 * Accepts both native JavaScript `Set`/`Map` and {@link SortedSet}/{@link SortedMap}.
 * For {@link RecursiveType}, uses cycle detection to handle recursive values.
 */
export function isValueOf(value: any, type: EastType, node_type?: EastType, nodes_visited?: Set<any>): boolean {
  if (type.type === "Never") {
    return false;
  } else if (type.type === "Null") {
    return value === null;
  } else if (type.type === "Boolean") {
    return typeof value === "boolean";
  } else if (type.type === "Integer") {
    return typeof value === "bigint";
  } else if (type.type === "Float") {
    return typeof value === "number";
  } else if (type.type === "String") {
    return typeof value === "string";
  } else if (type.type === "DateTime") {
    return value instanceof Date;
  } else if (type.type === "Blob") {
    return value instanceof Uint8Array;
  } else if (type.type === "Ref") {
    if (!isRef(value)) {
      return false;
    }
    return isValueOf(value.value, type.value, node_type, nodes_visited);
  } else if (type.type === "Array") {
    if (!Array.isArray(value)) {
      return false;
    }
    for (const x of value) {
      if (!isValueOf(x, type.value, node_type, nodes_visited)) {
        return false;
      }
    }
    return true;
  } else if (type.type === "Set") {
    if (!(value instanceof Set || value instanceof SortedSet)) {
      return false;
    }
    for (const x of value) {
      if (!isValueOf(x, type.key, node_type, nodes_visited)) {
        return false;
      }
    }
    return true;
  } else if (type.type === "Dict") {
    if (!(value instanceof Map || value instanceof SortedMap)) {
      return false;
    }
    for (const [k, v] of value) {
      if (!isValueOf(k, type.key, node_type, nodes_visited) || !isValueOf(v, type.value, node_type, nodes_visited)) {
        return false;
      }
    }
    return true;
  } else if (type.type === "Struct") {
    if (typeof value !== "object" || value === null || Object.getPrototypeOf(value) !== Object.getPrototypeOf({})) return false;
    const vs = Object.entries(value as Record<string, any>);
    const ts = Object.entries(type.fields as Record<string, EastType>);
    if (vs.length !== ts.length) return false;
    let i = 0;
    for (const [k1, ft] of ts) {
      const [k2, fv] = vs[i]!;
      if (k1 !== k2) return false;
      if (!isValueOf(fv, ft, node_type, nodes_visited)) return false;
      i += 1;
    }
    return true;
  } else if (type.type === "Variant") {
    if (typeof value !== "object" || value === null || value[variant_symbol] !== null) return false;
    const t = type.cases[(value as variant).type];
    if (t === undefined) { return false };
    return isValueOf((value as variant).value, t, node_type, nodes_visited);
  } else if (type.type === "Recursive") {
    if (node_type === type.node) {
      if (nodes_visited!.has(value)) {
        return true; // already seen this object
      }
      nodes_visited!.add(value);
      return isValueOf(value, type.node, type.node, nodes_visited);
    } else {
      // new recursive type, reset stack
      return isValueOf(value, type.node, type.node, new Set([value]));
    }
  } else if (type.type === "Function") {
    throw new Error('Javascript functions cannot be converted to East functions');
  } else if (type.type === "AsyncFunction") {
    throw new Error('Javascript functions cannot be converted to East async functions');
  } else {
    throw new Error(`Unknown type encountered during value type check: ${(type satisfies never as any).type}`);
  }
}

/**
 * Converts an East type to its string representation.
 *
 * @param type - The {@link EastType} to print
 * @param stack - Internal parameter for tracking recursive types
 * @returns A human-readable string representation of the type
 *
 * @remarks
 * Uses East's value syntax with leading dots (e.g., `.Integer`, `.Array .String`).
 */
export function printType(type: EastType, stack: EastType[] = []): string {
  // Note this is essentially a bootstrap function.
  
  // It should print the same output as printing an `EastType` as an `EastTypeType`, but
  // printing values hasn't been defined by this stage and printType is crucial for
  // internal debugging and `Expr` error messages.

  // We do skip mutable aliasing of struct field or variant case lists for clarity.
  // Types are intended to be immutable in any case.
  if (type.type === "Never") {
    return ".Never";
  } else if (type.type === "Null") {
    return ".Null";
  } else if (type.type === "Boolean") {
    return ".Boolean";
  } else if (type.type === "Integer") {
    return ".Integer";
  } else if (type.type === "Float") {
    return ".Float";
  } else if (type.type === "String") {
    return ".String";
  } else if (type.type === "DateTime") {
    return ".DateTime";
  } else if (type.type === "Blob") {
    return ".Blob";
  } else if (type.type === "Ref") {
    stack.push(type);
    const ret = `.Ref ${printType(type.value, stack)}`;
    stack.pop();
    return ret;
  } else if (type.type === "Array") {
    stack.push(type);
    const ret = `.Array ${printType(type.value, stack)}`;
    stack.pop();
    return ret;
  } else if (type.type === "Set") {
    stack.push(type);
    const ret = `.Set ${printType(type.key, stack)}`;
    stack.pop();
    return ret;
  } else if (type.type === "Dict") {
    stack.push(type);
    const ret = `.Dict (key=${printType(type.key, stack)}, value=${printType(type.value, stack)})`;
    stack.pop();
    return ret;
  } else if (type.type === "Struct") {
    stack.push(type);
    const ret = `.Struct [${Object.entries(type.fields).map(([k, t]) => `(name=${JSON.stringify(k)}, type=${printType(t, stack)})`).join(", ")}]`;
    stack.pop();
    return ret;
  } else if (type.type === "Variant") {
    stack.push(type);
    const ret = `.Variant [${Object.entries(type.cases).map(([k, t]) => `(name=${JSON.stringify(k)}, type=${printType(t, stack)})`).join(", ")}]`;
    stack.pop();
    return ret;
  } else if (type.type === "Recursive") {
    // TODO update for our new recursive type representation
    const idx = stack.indexOf(type.node);
    if (idx !== -1) {
      // Recursive reference
      return `.Recursive ${stack.length - idx}`;
    }

    return printType(type.node, stack);
  } else if (type.type === "Function") {
    // Note: functions can't be inside recursive types
    stack.push(type);
    const ret = `.Function (inputs=[${type.inputs.map(t => printType(t, stack)).join(", ")}], output=${printType(type.output, stack)})`;
    stack.pop();
    return ret;
  } else if (type.type === "AsyncFunction") {
    // Note: functions can't be inside recursive types
    stack.push(type);
    const ret = `.AsyncFunction (inputs=[${type.inputs.map(t => printType(t, stack)).join(", ")}], output=${printType(type.output, stack)})`;
    stack.pop();
    return ret;
  } else {
    throw new Error(`Unknown type encountered during type printing: ${(type satisfies never as any).type}`);
  }
}

/**
 * Expands a {@link RecursiveType} one level deeper, replacing {@link RecursiveTypeMarker} with the node type.
 *
 * @typeParam T - The type to expand
 * @typeParam NodeType - The recursive type to substitute for markers
 *
 * @remarks
 * Used to unfold recursive types for head covariance while maintaining tail invariance.
 * Internal helper for {@link SubType}.
 */
type ExpandOnce<T, NodeType> =
  T extends RefType<infer U> ? RefType<ExpandOnce<U, NodeType>> :
  T extends ArrayType<infer U> ? ArrayType<ExpandOnce<U, NodeType>> :
  T extends SetType<infer U> ? SetType<ExpandOnce<U, NodeType>> :
  T extends DictType<infer K, infer V> ? DictType<ExpandOnce<K, NodeType>, ExpandOnce<V, NodeType>> :
  T extends StructType<infer Fields> ? StructType<{ [K in keyof Fields]: ExpandOnce<Fields[K], NodeType> }> :
  T extends VariantType<infer Cases> ? VariantType<{ [K in keyof Cases]: ExpandOnce<Cases[K], NodeType> }> :
  T extends RecursiveTypeMarker ? NodeType :
  T;

/**
 * Computes the subtype relationship for East types (type-level).
 *
 * @typeParam T - The {@link EastType} to compute subtypes for
 *
 * @remarks
 * Subtyping rules:
 * - {@link ArrayType}, {@link SetType}, {@link DictType} are invariant (mutable)
 * - {@link StructType} is covariant in all fields
 * - {@link VariantType} is covariant (subtypes can have fewer cases)
 * - {@link FunctionType} and {@link AsyncFunctionType} are contravariant in inputs, covariant in output (and synchronous functions are subtypes of async functions)
 * - {@link RecursiveType} allows head covariance with tail invariance (one level deep)
 * - {@link NeverType} is a subtype of all types
 */
export type SubType<T> =
  T extends RecursiveType<infer U> ? RecursiveType<U> | ExpandOnce<SubType<U>, T> :
  T extends StructType<infer Fields> ? StructType<{ [K in keyof Fields]: SubType<Fields[K]> }> :
  T extends VariantType<infer Cases> ? VariantType<{ [K in keyof Cases]?: SubType<Cases[K]> }> :
  T extends FunctionType<infer I, infer O> ? FunctionType<I, SubType<O>> :
  T extends AsyncFunctionType<infer I, infer O> ? AsyncFunctionType<I, SubType<O>> | FunctionType<I, SubType<O>> :
  T;

/**
 * Checks if one East type is a subtype of another.
 *
 * @param t1 - The potential subtype
 * @param t2 - The potential supertype
 * @returns `true` if t1 is a subtype of t2, `false` otherwise
 *
 * @remarks
 * Implements East's subtyping rules:
 * - {@link NeverType} is a subtype of all types
 * - Mutable collections ({@link ArrayType}, {@link SetType}, {@link DictType}) are invariant
 * - {@link VariantType} supports width subtyping (more cases → fewer cases)
 * - {@link FunctionType} uses contravariant inputs and covariant outputs
 */
// Cache for memoizing isSubtype results
const isSubtypeCache = new WeakMap<EastType, WeakMap<EastType, boolean>>();

export function isSubtype(t1: EastType, t2: EastType): boolean {
  // Fast path: reference equality (reflexivity)
  if (t1 === t2) return true;

  // Check cache
  const innerCache = isSubtypeCache.get(t1);
  if (innerCache) {
    const cached = innerCache.get(t2);
    if (cached !== undefined) return cached;
  }

  const result = isSubtypeImpl(t1, t2);

  // Store in cache
  let cache = isSubtypeCache.get(t1);
  if (!cache) {
    cache = new WeakMap();
    isSubtypeCache.set(t1, cache);
  }
  cache.set(t2, result);
  return result;
}

function isSubtypeImpl(t1: EastType, t2: EastType): boolean {
  // Equi-recursive type subtyping: unfold recursive types when only one side is recursive
  if (t1.type === "Recursive") {
    if (t2.type === "Recursive") {
      // Recursive types are invariant - we want any compatible heap-allocated objects to have exactly the same layout
      return isTypeEqual(t1.node, t2.node);
    } else {
      // The recursive type wrapper is "transparent", but invariant
      return isTypeEqual(t1.node, t2);
    }
  } else if (t2.type === "Recursive") {
    // The recursive type wrapper is "transparent"
    // If the head is "on the stack" we can do head covariance by unfolding once
    return isSubtype(t1, t2.node);
  } else if (t1.type === "Never") {
    // t2 must be a supertype of Never
    return true;
  } else if (t1.type === "Null") {
    return t2.type === "Null";
  } else if (t1.type === "Boolean") {
    return t2.type === "Boolean";
  } else if (t1.type === "Integer") {
    return t2.type === "Integer";
  } else if (t1.type === "Float") {
    return t2.type === "Float";
  } else if (t1.type === "String") {
    return t2.type === "String";
  } else if (t1.type === "DateTime") {
    return t2.type === "DateTime";
  } else if (t1.type === "Blob") {
    return t2.type === "Blob";
  } else if (t1.type === "Ref") {
    if (t2.type === "Ref") {
      return isTypeEqual(t1.value, t2.value);
    } else {
      return false;
    }
  } else if (t1.type === "Array") {
    if (t2.type === "Array") {
      return isTypeEqual(t1.value, t2.value);
    } else {
      return false;
    }
  } else if (t1.type === "Set") {
    if (t2.type === "Set") {
      return isTypeEqual(t1.key, t2.key);
    } else {
      return false;
    }
  } else if (t1.type === "Dict") {
    if (t2.type === "Dict") {
      return isTypeEqual(t1.key, t2.key) && isTypeEqual(t1.value, t2.value);
    } else {
      return false;
    }
  } else if (t1.type === "Struct") {
    if (t2.type === "Struct") {
      const e1 = Object.entries(t1.fields);
      const e2 = Object.entries(t2.fields);
      if (e1.length !== e2.length) return false;
      let i = 0;
      for (const [k1, f1] of e1) {
        const [k2, f2] = e2[i]!;
        if (k1 !== k2) return false;
        if (!isSubtype(f1, f2)) return false;
        i += 1;
      }
      return true;
    } else {
      return false;
    }
  } else if (t1.type === "Variant") {
    if (t2.type === "Variant") {
      // Unlike structs, we don't care about the order (they are sorted by name already) and we only need a subset of cases in t2
      for (const [k, v1] of Object.entries(t1.cases)) {
        const v2 = t2.cases[k] ?? NeverType;
        if (!isSubtype(v1, v2)) return false;
      }
      return true;
    } else {
      return false;
    }
  } else if (t1.type === "Function") {
    if (t2.type === "Function" || t2.type === "AsyncFunction") {
      return t1.inputs.length === t2.inputs.length && t1.inputs.every((t, i) => isSubtype(t2.inputs[i], t)) && isSubtype(t1.output, t2.output); // contravariant inputs and covariant output
    } else {
      return false;
    }
  } else if (t1.type === "AsyncFunction") {
    if (t2.type === "AsyncFunction") {
      return t1.inputs.length === t2.inputs.length && t1.inputs.every((t, i) => isSubtype(t2.inputs[i], t)) && isSubtype(t1.output, t2.output); // contravariant inputs and covariant output
    } else {
      return false;
    }
  } else {
    throw new Error(`Unknown type encountered during subtype check: ${(t1 satisfies never as any).type}`);
  }
}

/**
 * Computes the union of two East types (type-level).
 *
 * @typeParam T1 - First {@link EastType}
 * @typeParam T2 - Second {@link EastType}
 *
 * @remarks
 * Type union rules:
 * - {@link NeverType} is the identity: `Union<Never, T> = T`
 * - {@link StructType} unions require same fields, unions field types
 * - {@link VariantType} unions combine all cases from both types
 * - {@link FunctionType} unions intersect inputs (contravariant), union outputs (covariant)
 * - {@link AsyncFunctionType} unions intersect inputs (contravariant), union outputs (covariant), and synchronous functions are subtypes of async functions
 * - Mutable collections must have identical element/key/value types
 */
export type TypeUnion<T1, T2> =
  T1 extends NeverType ? T2 :
  T2 extends NeverType ? T1 :
  // arrays, sets and dicts are invariant
  T1 extends StructType<infer Fields1> ? T2 extends StructType<infer Fields2> ? StructType<{ [K in keyof Fields1 & keyof Fields2]: TypeUnion<Fields1[K], Fields2[K]> }> : never :
  T1 extends VariantType<infer Cases1> ? T2 extends VariantType<infer Cases2> ? VariantType<{ [K in Exclude<keyof Cases1, keyof Cases2>]: Cases1[K] } & { [K in Exclude<keyof Cases2, keyof Cases1>]: Cases2[K] } & { [K in keyof Cases1 & keyof Cases2]: TypeUnion<Cases1[K], Cases2[K]> }> : never :
  T1 extends FunctionType<infer I1, infer O1> ? T2 extends FunctionType<infer I2, infer O2> ? FunctionType<{ [K in keyof I1 & keyof I2]: TypeIntersect<I1[K], I2[K]> }, TypeUnion<O1, O2>> : T2 extends AsyncFunctionType<infer I2, infer O2> ? AsyncFunctionType<{ [K in keyof I1 & keyof I2]: TypeIntersect<I1[K], I2[K]> }, TypeUnion<O1, O2>> : never :
  T1 extends AsyncFunctionType<infer I1, infer O1> ? T2 extends FunctionType<infer I2, infer O2> ? AsyncFunctionType<{ [K in keyof I1 & keyof I2]: TypeIntersect<I1[K], I2[K]> }, TypeUnion<O1, O2>> : T2 extends AsyncFunctionType<infer I2, infer O2> ? AsyncFunctionType<{ [K in keyof I1 & keyof I2]: TypeIntersect<I1[K], I2[K]> }, TypeUnion<O1, O2>> : never :
  T1 extends T2 ? T1 :
  never;

/**
 * Computes the intersection of two East types (type-level).
 *
 * @typeParam T1 - First {@link EastType}
 * @typeParam T2 - Second {@link EastType}
 *
 * @remarks
 * Type intersection rules:
 * - {@link NeverType} is absorbing: `Intersect<Never, T> = Never`
 * - {@link StructType} intersections require same fields, intersect field types
 * - {@link VariantType} intersections keep only common cases
 * - {@link FunctionType} intersections union inputs (contravariant), intersect outputs (covariant), and synchronous functions are subtypes of async functions
 * - {@link AsyncFunctionType} intersections union inputs (contravariant), intersect outputs (covariant)
 * - Mutable collections must have identical element/key/value types
 */
export type TypeIntersect<T1, T2> =
  T1 extends NeverType ? NeverType :
  T2 extends NeverType ? NeverType :
  // arrays, sets and dicts are invariant
  T1 extends StructType<infer Fields1> ? T2 extends StructType<infer Fields2> ? StructType<{ [K in keyof Fields1 & keyof Fields2]: TypeIntersect<Fields1[K], Fields2[K]> }> : never :
  T1 extends VariantType<infer Cases1> ? T2 extends VariantType<infer Cases2> ? VariantType<{ [K in keyof Cases1 & keyof Cases2]: TypeIntersect<Cases1[K], Cases2[K]> }> : never :
  T1 extends FunctionType<infer I1, infer O1> ? T2 extends FunctionType<infer I2, infer O2> ? FunctionType<{ [K in keyof I1 & keyof I2]: TypeUnion<I1[K], I2[K]> }, TypeIntersect<O1, O2>> : T2 extends AsyncFunctionType<infer I2, infer O2> ? FunctionType<{ [K in keyof I1 & keyof I2]: TypeUnion<I1[K], I2[K]> }, TypeIntersect<O1, O2>> : never :
  T1 extends AsyncFunctionType<infer I1, infer O1> ? T2 extends FunctionType<infer I2, infer O2> ? FunctionType<{ [K in keyof I1 & keyof I2]: TypeUnion<I1[K], I2[K]> }, TypeIntersect<O1, O2>> : T2 extends AsyncFunctionType<infer I2, infer O2> ? AsyncFunctionType<{ [K in keyof I1 & keyof I2]: TypeUnion<I1[K], I2[K]> }, TypeIntersect<O1, O2>> : never :
  T1 extends T2 ? T1 :
  never;

/**
 * Computes the union of two East types at runtime.
 *
 * @typeParam T1 - First {@link EastType}
 * @typeParam T2 - Second {@link EastType}
 * @param t1 - First type
 * @param t2 - Second type
 * @returns The union type
 * @throws {TypeMismatchError} When the types cannot be unified
 *
 * @remarks
 * This is the runtime version of the {@link TypeUnion} type.
 * Error messages include the full type path for debugging.
 */
export function TypeUnion<T1 extends EastType, T2 extends EastType>(t1: T1, t2: T2): TypeUnion<T1, T2> {
  // TODO this is broken for recursive types (need to do cycle tracking in tandem with TypeEqual/TypeIntersect)
  try {
    if (t1.type === "Never") {
      return t2 as TypeUnion<T1, T2>;
    } else if (t2.type === "Never") {
      return t1 as TypeUnion<T1, T2>;
    } else if (t1.type === "Recursive") {
      if (t2.type === "Recursive") {
        // Both recursive - require exact match (heap invariance)
        return TypeEqual(t1, t2) as TypeUnion<T1, T2>;
        // return RecursiveType(() => TypeEqual(t1.node, t2.node, t1.node, t2.node)) as TypeUnion<T1, T2>;
      } else {
        // Rec(A) ∪ NonRec: If NonRec <: A, union is Rec(A) (NonRec can be widened to heap type)
        if (isSubtype(t2, t1.node)) {
          return t1 as TypeUnion<T1, T2>;
        }
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t2.type === "Recursive") {
      // NonRec ∪ Rec(B): If NonRec <: B, union is Rec(B) (symmetric case)
      if (isSubtype(t1, t2.node)) {
        return t2 as TypeUnion<T1, T2>;
      }
      throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
    } else if (t1.type === "Ref") {
      if (t2.type === "Ref") {
        return RefType(TypeEqual(t1.value, t2.value)) as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Array") {
      if (t2.type === "Array") {
        return ArrayType(TypeEqual(t1.value, t2.value)) as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Set") {
      if (t2.type === "Set") {
        return SetType(TypeEqual(t1.key, t2.key)) as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Dict") {
      if (t2.type === "Dict") {
        return DictType(TypeEqual(t1.key, t2.key), TypeEqual(t1.value, t2.value)) as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Struct") {
      if (t2.type === "Struct") {
        const e1 = Object.entries(t1.fields as Record<string, EastType>);
        const e2 = Object.entries(t2.fields as Record<string, EastType>);
        if (e1.length !== e2.length) throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: structs contain different number of fields`);
        let i = 0;
        const e: Record<string, EastType> = {};
        for (const [k1, f1] of e1) {
          const [k2, f2] = e2[i]!;
          if (k1 !== k2) throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: struct field ${i} has mismatched names ${printIdentifier(k1)} and ${printIdentifier(k2)}`);
          e[k1] = TypeUnion(f1, f2);
          i += 1;
        }
        return StructType(e) as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Variant") {
      if (t2.type === "Variant") {
        const cases: Record<string, EastType> = {};
        for (const [k1, f1] of Object.entries(t1.cases as Record<string, EastType>)) {
          const f2 = t2.cases[k1];
          if (f2 === undefined) {
            cases[k1] = f1;
          } else {
            cases[k1] = TypeUnion(f1, f2);
          }
        }
        for (const [k2, f2] of Object.entries(t2.cases as Record<string, EastType>)) {
          const f1 = t1.cases[k2];
          if (f1 === undefined) {
            cases[k2] = f2;
          }
        }
        return VariantType(cases) as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Function") {
      if (t2.type === "Function") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: functions take different number of arguments`)
        }
        return FunctionType(t1.inputs.map((t, i) => TypeIntersect(t, t2.inputs[i])), TypeUnion(t1.output, t2.output)) as TypeUnion<T1, T2>;
      } else if (t2.type === "AsyncFunction") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: functions take different number of arguments`)
        }
        return AsyncFunctionType(t1.inputs.map((t, i) => TypeIntersect(t, t2.inputs[i])), TypeUnion(t1.output, t2.output)) as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "AsyncFunction") {
      if (t2.type === "Function") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: functions take different number of arguments`)
        }
        return AsyncFunctionType(t1.inputs.map((t, i) => TypeIntersect(t, t2.inputs[i])), TypeUnion(t1.output, t2.output)) as TypeUnion<T1, T2>;
      } else if (t2.type === "AsyncFunction") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: functions take different number of arguments`)
        }
        return AsyncFunctionType(t1.inputs.map((t, i) => TypeIntersect(t, t2.inputs[i])), TypeUnion(t1.output, t2.output)) as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else {
      if (t1.type === t2.type) {
        return t1 as TypeUnion<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    }
  } catch (cause: unknown) {
    if (cause instanceof TypeMismatchError) {
      throw cause; // Don't wrap our own errors - they already have the full path
    }
    throw new TypeMismatchError(`Cannot union ${printType(t1)} with ${printType(t2)}`, { cause });
  }
}

/**
 * Computes the intersection of two East types at runtime.
 *
 * @typeParam T1 - First {@link EastType}
 * @typeParam T2 - Second {@link EastType}
 * @param t1 - First type
 * @param t2 - Second type
 * @returns The intersection type
 * @throws {TypeMismatchError} When the types cannot be intersected
 *
 * @remarks
 * This is the runtime version of the {@link TypeIntersect} type.
 * For {@link VariantType}, returns {@link NeverType} if no common cases exist.
 */
export function TypeIntersect<T1 extends EastType, T2 extends EastType>(t1: T1, t2: T2): TypeIntersect<T1, T2> {
  // TODO this is broken for recursive types (need to do cycle tracking in tandem with TypeEqual/TypeUnion)
  try {
    if (t1.type === "Never") {
      return NeverType as TypeIntersect<T1, T2>;
    } else if (t2.type === "Never") {
      return NeverType as TypeIntersect<T1, T2>;
    } else if (t1.type === "Recursive") {
      if (t2.type === "Recursive") {
        // Both recursive - require exact match (heap invariance)
        return RecursiveType(() => TypeEqual(t1.node, t2.node, t1.node, t2.node)) as TypeIntersect<T1, T2>;
      } else {
        // Rec(A) ∩ NonRec: If NonRec <: A, intersection is NonRec (the more specific type)
        if (isSubtype(t2, t1.node)) {
          return t2 as TypeIntersect<T1, T2>;
        }
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t2.type === "Recursive") {
      // NonRec ∩ Rec(B): If NonRec <: B, intersection is NonRec (symmetric case)
      if (isSubtype(t1, t2.node)) {
        return t1 as TypeIntersect<T1, T2>;
      }
      throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
    } else if (t1.type === "Ref") {
      if (t2.type === "Ref") {
        return RefType(TypeEqual(t1.value, t2.value)) as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Array") {
      if (t2.type === "Array") {
        return ArrayType(TypeEqual(t1.value, t2.value)) as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Set") {
      if (t2.type === "Set") {
        return SetType(TypeEqual(t1.key, t2.key)) as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Dict") {
      if (t2.type === "Dict") {
        return DictType(TypeEqual(t1.key, t2.key), TypeEqual(t1.value, t2.value)) as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Struct") {
      if (t2.type === "Struct") {
        const e1 = Object.entries(t1.fields as Record<string, EastType>);
        const e2 = Object.entries(t2.fields as Record<string, EastType>);
        if (e1.length !== e2.length) throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: structs contain different number of fields`);
        let i = 0;
        const e: Record<string, EastType> = {};
        for (const [k1, f1] of e1) {
          const [k2, f2] = e2[i]!;
          if (k1 !== k2) throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: struct field ${i} has mismatched names ${printIdentifier(k1)} and ${printIdentifier(k2)}`);
          e[k1] = TypeIntersect(f1, f2);
          i += 1;
        }
        return StructType(e) as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Variant") {
      if (t2.type === "Variant") {
        const cases: Record<string, EastType> = {};
        let empty = true;
        for (const [k1, f1] of Object.entries(t1.cases as Record<string, EastType>)) {
          const f2 = t2.cases[k1];
          if (f2 !== undefined) {
            cases[k1] = TypeIntersect(f1, f2);
            empty = false;
          }
        }
        if (empty) {
          throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: variants have no overlapping cases`)
        }
        return VariantType(cases) as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Function") {
      if (t2.type === "Function") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: functions take different number of arguments`)
        }
        return FunctionType(t1.inputs.map((t, i) => TypeUnion(t, t2.inputs[i])), TypeIntersect(t1.output, t2.output)) as TypeIntersect<T1, T2>;
      } else if (t2.type === "AsyncFunction") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: functions take different number of arguments`)
        }
        return FunctionType(t1.inputs.map((t, i) => TypeUnion(t, t2.inputs[i])), TypeIntersect(t1.output, t2.output)) as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "AsyncFunction") {
      if (t2.type === "Function") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: functions take different number of arguments`)
        }
        return FunctionType(t1.inputs.map((t, i) => TypeUnion(t, t2.inputs[i])), TypeIntersect(t1.output, t2.output)) as TypeIntersect<T1, T2>;
      } else if (t2.type === "AsyncFunction") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: functions take different number of arguments`)
        }
        return AsyncFunctionType(t1.inputs.map((t, i) => TypeUnion(t, t2.inputs[i])), TypeIntersect(t1.output, t2.output)) as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else {
      if (t1.type === t2.type) {
        return t1 as TypeIntersect<T1, T2>;
      } else {
        throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    }
  } catch (cause: unknown) {
    if (cause instanceof TypeMismatchError) {
      throw cause; // Don't wrap our own errors - they already have the full path
    }
    throw new TypeMismatchError(`Cannot intersect ${printType(t1)} with ${printType(t2)}`, { cause });
  }
}

/**
 * Asserts that two East types are equal, returning the first type.
 *
 * @typeParam T1 - First {@link EastType}
 * @typeParam T2 - Second {@link EastType}
 * @param t1 - First type
 * @param t2 - Second type
 * @param r1 - Internal parameter for tracking the first recursive type being compared
 * @param r2 - Internal parameter for tracking the second recursive type being compared
 * @returns The first type if types are equal
 * @throws {TypeMismatchError} When the types are not equal
 *
 * @remarks
 * This function recursively validates type equality and throws detailed errors
 * on mismatch. Used to enforce type constraints in compound type constructors.
 * Unlike {@link isTypeEqual}, this throws rather than returning a boolean.
 */
export function TypeEqual<T1 extends EastType, T2 extends EastType>(t1: T1, t2: T2, r1: any = t1, r2: any = t2): T1 {
  // TODO this is broken for recursive types (need to do cycle tracking in tandem with TypeUnion/TypeIntersect)
  try {
    if (t1.type === "Ref") {
      if (t2.type === "Ref") {
        return RefType(TypeEqual(t1.value, t2.value, r1, r2)) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Array") {
      if (t2.type === "Array") {
        return ArrayType(TypeEqual(t1.value, t2.value, r1, r2)) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Set") {
      if (t2.type === "Set") {
        return SetType(TypeEqual(t1.key, t2.key, r1, r2)) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Dict") {
      if (t2.type === "Dict") {
        return DictType(TypeEqual(t1.key, t2.key, r1, r2), TypeEqual(t1.value, t2.value, r1, r2)) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Struct") {
      if (t2.type === "Struct") {
        const e1 = Object.entries(t1.fields as Record<string, EastType>);
        const e2 = Object.entries(t2.fields as Record<string, EastType>);
        if (e1.length !== e2.length) throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: structs contain different number of fields`);
        let i = 0;
        const e: Record<string, EastType> = {};
        for (const [k1, f1] of e1) {
          const [k2, f2] = e2[i]!;
          if (k1 !== k2) throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: struct field ${i} has mismatched names ${printIdentifier(k1)} and ${printIdentifier(k2)}`);
          e[k1] = TypeEqual(f1, f2, r1, r2);
          i += 1;
        }
        return StructType(e) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Variant") {
      // We can reuse the logic for structs here, taking advantage of the ordering guarantees
      if (t2.type === "Variant") {
        const e1 = Object.entries(t1.cases as Record<string, EastType>);
        const e2 = Object.entries(t2.cases as Record<string, EastType>);
        if (e1.length !== e2.length) throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: variants contain different number of cases`);
        let i = 0;
        const e: Record<string, EastType> = {};
        for (const [k1, f1] of e1) {
          const [k2, f2] = e2[i]!;
          if (k1 !== k2) {
            if (k1 < k2) {
              throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: variant case ${k1} is not present in both variants`);
            } else {
              throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: variant case ${k2} is not present in both variants`);
            }
          }
          e[k1] = TypeEqual(f1, f2, r1, r2);
          i += 1;
        }
        return VariantType(e) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Recursive") {
      if (t2.type === "Recursive") {
        if (t1.node === r1) {
          if (t2.node === r2) {
            return t1 as T1; // both are references to the same recursive type
          } else {
            throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: recursive types do not match`);
          }
        } else if (t2.node === r2) {
          throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: recursive types do not match`);
        }
        // this is the root of a new recursive type - assert the node types are equal
        return RecursiveType(() => TypeEqual(t1.node, t2.node, t1.node, t2.node)) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Function") {
      if (t2.type === "Function") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: functions take different number of arguments`)
        }
        return FunctionType(t1.inputs.map((t, i) => TypeEqual(t, t2.inputs[i], r1, r2)), TypeEqual(t1.output, t2.output, r1, r2)) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "AsyncFunction") {
      if (t2.type === "AsyncFunction") {
        if (t1.inputs.length !== t2.inputs.length) {
          throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: functions take different number of arguments`)
        }
        return AsyncFunctionType(t1.inputs.map((t, i) => TypeEqual(t, t2.inputs[i], r1, r2)), TypeEqual(t1.output, t2.output, r1, r2)) as T1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    } else {
      if (t1.type === t2.type) {
        return t1;
      } else {
        throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}: incompatible types`)
      }
    }
  } catch (cause: unknown) {
    if (cause instanceof TypeMismatchError) {
      throw cause; // Don't wrap our own errors - they already have the full path
    }
    throw new TypeMismatchError(`${printType(t1)} is not equal to ${printType(t2)}`, { cause });
  }
}

/**
 * Create a type wide enough to hold values from two East types at runtime.
 *
 * @param t1 - First type
 * @param t2 - Second type
 * @returns The union type
 * @throws {TypeMismatchError} When the types cannot be unified
 *
 * @remarks
 * This is a more forgiving version of the {@link TypeUnion} type, designed for inferring types from values.
 * Functions and recursive types are not supported.
 * Error messages include the full type path for debugging.
 */
export function TypeWiden(t1: EastType, t2: EastType): EastType {
  try {
    if (t1.type === "Never") {
      return t2;
    } else if (t2.type === "Never") {
      return t1;
    } else if (t1.type === "Recursive") {
      throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: recursive types not supported`)
    } else if (t2.type === "Recursive") {
      throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: recursive types not supported`)
    } else if (t1.type === "Ref") {
      if (t2.type === "Ref") {
        return RefType(TypeWiden(t1.value, t2.value));
      } else {
        throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Array") {
      if (t2.type === "Array") {
        return ArrayType(TypeWiden(t1.value, t2.value));
      } else {
        throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Set") {
      if (t2.type === "Set") {
        return SetType(TypeWiden(t1.key, t2.key));
      } else {
        throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Dict") {
      if (t2.type === "Dict") {
        return DictType(TypeWiden(t1.key, t2.key), TypeWiden(t1.value, t2.value));
      } else {
        throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Struct") {
      if (t2.type === "Struct") {
        const e1 = Object.entries(t1.fields as Record<string, EastType>);
        const e2 = Object.entries(t2.fields as Record<string, EastType>);
        if (e1.length !== e2.length) throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: structs contain different number of fields`);
        let i = 0;
        const e: Record<string, EastType> = {};
        for (const [k1, f1] of e1) {
          const [k2, f2] = e2[i]!;
          if (k1 !== k2) throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: struct field ${i} has mismatched names ${printIdentifier(k1)} and ${printIdentifier(k2)}`);
          e[k1] = TypeWiden(f1, f2);
          i += 1;
        }
        return StructType(e);
      } else {
        throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Variant") {
      if (t2.type === "Variant") {
        const cases: Record<string, EastType> = {};
        for (const [k1, f1] of Object.entries(t1.cases as Record<string, EastType>)) {
          const f2 = t2.cases[k1];
          if (f2 === undefined) {
            cases[k1] = f1;
          } else {
            cases[k1] = TypeWiden(f1, f2);
          }
        }
        for (const [k2, f2] of Object.entries(t2.cases as Record<string, EastType>)) {
          const f1 = t1.cases[k2];
          if (f1 === undefined) {
            cases[k2] = f2;
          }
        }
        return VariantType(cases);
      } else {
        throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    } else if (t1.type === "Function") {
      throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: functions not supported`)
    } else if (t1.type === "AsyncFunction") {
      throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: functions not supported`)
    } else {
      if (t1.type === t2.type) {
        return t1;
      } else {
        throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}: incompatible types`)
      }
    }
  } catch (cause: unknown) {
    if (cause instanceof TypeMismatchError) {
      throw cause; // Don't wrap our own errors - they already have the full path
    }
    throw new TypeMismatchError(`Cannot widen ${printType(t1)} with ${printType(t2)}`, { cause });
  }
}

/**
 * Formats an identifier for display in type strings.
 *
 * @param x - The identifier to format
 * @returns The identifier, escaped with backticks if it contains special characters
 *
 * @remarks
 * Used by {@link printType} to format field and case names.
 * Identifiers matching `/^[a-zA-Z_][a-zA-Z0-9_]*$/` are returned as-is,
 * others are wrapped in backticks with escaping.
 */
export function printIdentifier(x: string) {
  if (/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(x)) {
    return x;
  } else {
    return `\`${x.replace('\\', '\\\\').replace('`', '\\`')}\``;
  }
}

/**
 * Represents the None case of the {@link OptionType} pattern.
 *
 * @remarks
 * Equivalent to `VariantType({ none: NullType })`.
 * Use with {@link SomeType} and {@link OptionType} for optional values.
 */
export type NoneType = VariantType<{ none: NullType }>;
/** Singleton instance of {@link NoneType}. */
export const NoneType: NoneType = VariantType({ none: NullType });

/**
 * Represents the Some case of the {@link OptionType} pattern.
 *
 * @typeParam T - The type of the wrapped value
 */
export type SomeType<T> = VariantType<{ some: T }>;
/**
 * Constructs a Some type wrapping a value type.
 *
 * @typeParam T - The type of the wrapped value
 * @param type - The {@link EastType} to wrap
 * @returns A SomeType variant
 */
export function SomeType<T>(type: T): SomeType<T> {
  return VariantType({ some: type });
}

/**
 * Represents an optional value that may be present or absent.
 *
 * @typeParam T - The type of the value when present
 *
 * @remarks
 * This is East's type-level representation of the {@link option} runtime pattern.
 * Equivalent to `VariantType({ none: NullType, some: T })`.
 */
export type OptionType<T> = VariantType<{ none: NullType, some: T }>;
/**
 * Constructs an Option type for optional values.
 *
 * @typeParam T - The type of the value when present
 * @param type - The {@link EastType} of the wrapped value
 * @returns An OptionType variant with none and some cases
 *
 * @example
 * ```ts
 * const maybeInt = OptionType(IntegerType);
 * // Type: VariantType<{ none: NullType, some: IntegerType }>
 * ```
 */
export function OptionType<T>(type: T): OptionType<T> {
  return VariantType({ none: NullType, some: type });
}
