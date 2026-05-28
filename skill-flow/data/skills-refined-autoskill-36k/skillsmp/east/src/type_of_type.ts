
/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { ArrayType, BlobType, BooleanType, DateTimeType, FloatType, IntegerType, NullType, printType, RecursiveType, StringType, StructType, VariantType, type EastType } from "./types.js"
import { isVariant, variant } from "./containers/variant.js";
import { equalFor } from "./comparison.js";

/** The type of primitive literal values in IR.
 * Used to represent the values in ValueIR nodes.
 */
export const LiteralValueType = VariantType({
  Null: NullType,
  Boolean: BooleanType,
  Integer: IntegerType,
  Float: FloatType,
  String: StringType,
  DateTime: DateTimeType,
  Blob: BlobType
});
export type LiteralValueType = VariantType<{
  Null: NullType,
  Boolean: BooleanType,
  Integer: IntegerType,
  Float: FloatType,
  String: StringType,
  DateTime: DateTimeType,
  Blob: BlobType
}>;

/** The TypeScript type of literal values in IR. */
export type LiteralValue =
  | variant<"Null", null>
  | variant<"Boolean", boolean>
  | variant<"Integer", bigint>
  | variant<"Float", number>
  | variant<"String", string>
  | variant<"DateTime", Date>
  | variant<"Blob", Uint8Array>;

/** The type of East values, represented as an `EastType`.
 * This format is used for serialization of types, IR, etc.
 *
 * It also opens the door to type reflection and meta-programming within East.
*/
export const EastTypeType = RecursiveType(type => VariantType({
  "Never": NullType,
  "Null": NullType,
  "Boolean": NullType,
  "Integer": NullType,
  "Float": NullType,
  "String": NullType,
  "DateTime": NullType,
  "Blob": NullType,
  "Ref": type,
  "Array": type,
  "Set": type,
  "Dict": StructType({ key: type, value: type }),
  "Struct": ArrayType(StructType({ name: StringType, type: type })),
  "Variant": ArrayType(StructType({ name: StringType, type: type })),
  "Recursive": IntegerType,
  "Function": StructType({
    inputs: ArrayType(type),
    output: type,
  }),
  "AsyncFunction": StructType({
    inputs: ArrayType(type),
    output: type,
  })
}));
export type EastTypeType = typeof EastTypeType;

export type RefTypeValue = variant<"Ref", any>;
export type ArrayTypeValue = variant<"Array", any>;
export type SetTypeValue = variant<"Set", any>;
export type DictTypeValue = variant<"Dict", { key: any, value: any }>;
export type VariantTypeValue = variant<"Variant", { name: string, type: any }[]>;
export type StructTypeValue = variant<"Struct", { name: string, type: any }[]>;
export type FunctionTypeValue = variant<"Function", {
  inputs: any[],
  output: any,
}>;
export type AsyncFunctionTypeValue = variant<"AsyncFunction", {
  inputs: any[],
  output: any,
}>;

/** A serializable representation of East types. Note that `any` is used to terminate recursing of TypeScript types. */
export type EastTypeValue = 
  | variant<"Never", null>
  | variant<"Null", null>
  | variant<"Boolean", null>
  | variant<"Integer", null>
  | variant<"Float", null>
  | variant<"String", null>
  | variant<"DateTime", null>
  | variant<"Blob", null>
  | RefTypeValue
  | ArrayTypeValue
  | SetTypeValue
  | DictTypeValue
  | StructTypeValue
  | VariantTypeValue
  | variant<"Recursive", bigint>
  | FunctionTypeValue
  | AsyncFunctionTypeValue;


// Cache for memoizing toEastTypeValue results (top-level non-recursive calls only)
const toEastTypeValueCache = new WeakMap<EastType, EastTypeValue>();

export function toEastTypeValue(type: EastType, stack?: EastType[], is_recursive?: boolean): EastTypeValue
export function toEastTypeValue(type: EastType | string): EastTypeValue | string
export function toEastTypeValue(type: EastType | string, stack: EastType[] = [], is_recursive: boolean = false): EastTypeValue | string {
  if (typeof type === "string") {
    // Used for generics (type parameters)
    return type;
  }

  if (isVariant(type)) {
    return type as EastTypeValue;  // Already converted, return as-is
  }

  // Memoization for top-level calls (empty stack, not in recursive context)
  const isTopLevel = stack.length === 0 && !is_recursive;
  if (isTopLevel) {
    const cached = toEastTypeValueCache.get(type);
    if (cached !== undefined) return cached;
    const result = toEastTypeValueImpl(type, stack, is_recursive);
    toEastTypeValueCache.set(type, result);
    return result;
  }

  return toEastTypeValueImpl(type, stack, is_recursive);
}

function toEastTypeValueImpl(type: EastType, stack: EastType[], is_recursive: boolean): EastTypeValue {
  if (is_recursive) {
    const idx = stack.indexOf(type);
    if (idx !== -1) {
      return variant("Recursive", BigInt(stack.length - idx));
    }
  }

  if (type.type === "Never") {
    return variant("Never", null);
  } else if (type.type === "Null") {
    return variant("Null", null);
  } else if (type.type === "Boolean") {
    return variant("Boolean", null);
  } else if (type.type === "Integer") {
    return variant("Integer", null);
  } else if (type.type === "Float") {
    return variant("Float", null);
  } else if (type.type === "String") {
    return variant("String", null);
  } else if (type.type === "Blob") {
    return variant("Blob", null);
  } else if (type.type === "DateTime") {
    return variant("DateTime", null);
  } else if (type.type === "Ref") {
    stack.push(type);
    const ret = variant("Ref", toEastTypeValue(type.value, stack, false));
    stack.pop();
    return ret;
  } else if (type.type === "Array") {
    stack.push(type);
    const ret = variant("Array", toEastTypeValue(type.value, stack, false));
    stack.pop();
    return ret;
  } else if (type.type === "Set") {
    stack.push(type);
    const ret = variant("Set", toEastTypeValue(type.key, stack, false));
    stack.pop();
    return ret;
  } else if (type.type === "Dict") {
    stack.push(type);
    const ret = variant("Dict", {
      key: toEastTypeValue(type.key, stack, false),
      value: toEastTypeValue(type.value, stack, false),
    });
    stack.pop();
    return ret;
  } else if (type.type === "Struct") {
    stack.push(type);
    const ret = variant("Struct", Object.entries(type.fields).map(([name, fieldType]) => ({ name, type: toEastTypeValue(fieldType as EastType, stack, false) })));
    stack.pop();
    return ret;
  } else if (type.type === "Variant") {
    stack.push(type);
    const ret = variant("Variant", Object.entries(type.cases).map(([name, caseType]) => ({ name, type: toEastTypeValue(caseType as EastType, stack, false) })));
    stack.pop();
    return ret;
  } else if (type.type === "Recursive") {
    return toEastTypeValue(type.node, stack, true);
  } else if (type.type === "Function") {
    stack.push(type);
    const ret = variant("Function", {
      inputs: type.inputs.map(p => toEastTypeValue(p, stack, false)),
      output: toEastTypeValue(type.output, stack, false),
    });
    stack.pop();
    return ret;
  } else if (type.type === "AsyncFunction") {
    stack.push(type);
    const ret = variant("AsyncFunction", {
      inputs: type.inputs.map(p => toEastTypeValue(p, stack, false)),
      output: toEastTypeValue(type.output, stack, false),
    });
    stack.pop();
    return ret;
  } else {
    throw new Error(`Unknown type: ${printType(type satisfies never)}`);
  }
}

export const EastTypeValueType: EastTypeValue = toEastTypeValue(EastTypeType);

/**
 * Compares two EastTypeValue instances for type equality.
 *
 * @param t1 - First type value to compare
 * @param t2 - Second type value to compare
 * @returns `true` if the types are equal, `false` otherwise
 *
 * @remarks
 * This is the {@link EastTypeValue} version of {@link isTypeEqual}.
*/
const isTypeValueEqualUncached = equalFor(EastTypeValueType);
const isTypeValueEqualCache = new WeakMap<EastTypeValue, WeakMap<EastTypeValue, boolean>>();

export function isTypeValueEqual(t1: EastTypeValue, t2: EastTypeValue): boolean {
  // Fast path: reference equality
  if (t1 === t2) return true;

  // Check cache
  const innerCache = isTypeValueEqualCache.get(t1);
  if (innerCache) {
    const cached = innerCache.get(t2);
    if (cached !== undefined) return cached;
  }

  const result = isTypeValueEqualUncached(t1, t2);

  // Store in cache
  let cache = isTypeValueEqualCache.get(t1);
  if (!cache) {
    cache = new WeakMap();
    isTypeValueEqualCache.set(t1, cache);
  }
  cache.set(t2, result);
  return result;
}

/**
 * Checks if one EastTypeValue is a subtype of another.
 *
 * @param t1 - The potential subtype
 * @param t2 - The potential supertype
 * @param visited - Internal parameter for tracking recursive type pairs (cycle detection)
 * @returns `true` if t1 is a subtype of t2, `false` otherwise
 *
 * @remarks
 * This is the {@link EastTypeValue} version of {@link isSubtype}.
 * Implements East's subtyping rules:
 * - {@link NeverType} is a subtype of all types
 * - Mutable collections (Array, Set, Dict) are invariant
 * - {@link VariantType} supports width subtyping (more cases → fewer cases)
 * - {@link RecursiveType} is invariant for heap-to-heap, but allows head covariance for stack-to-heap
 * - {@link FunctionType} and {@link AsyncFunctionType} use contravariant inputs and covariant outputs (and FunctionType is a subtype of AsyncFunctionType if their signatures match)
 */
// Cache for memoizing isSubtypeValue results (top-level calls only)
const isSubtypeValueCache = new WeakMap<EastTypeValue, WeakMap<EastTypeValue, boolean>>();

export function isSubtypeValue(
  t1: EastTypeValue | string,
  t2: EastTypeValue | string,
  stack1: EastTypeValue[] = [],
  stack2: EastTypeValue[] = [],
): boolean {
  // Handle string type parameters (used for generics)
  if (typeof t1 === "string" || typeof t2 === "string") {
    return t1 === t2;
  }

  // Fast path: reference equality (reflexivity - every type is subtype of itself)
  if (t1 === t2) return true;

  // Memoization for top-level calls (empty stacks)
  const isTopLevel = stack1.length === 0 && stack2.length === 0;
  if (isTopLevel) {
    const innerCache = isSubtypeValueCache.get(t1);
    if (innerCache) {
      const cached = innerCache.get(t2);
      if (cached !== undefined) return cached;
    }
    const result = isSubtypeValueImpl(t1, t2, stack1, stack2);
    // Store in cache
    let cache = isSubtypeValueCache.get(t1);
    if (!cache) {
      cache = new WeakMap();
      isSubtypeValueCache.set(t1, cache);
    }
    cache.set(t2, result);
    return result;
  }

  return isSubtypeValueImpl(t1, t2, stack1, stack2);
}

function isSubtypeValueImpl(
  t1: EastTypeValue,
  t2: EastTypeValue,
  stack1: EastTypeValue[],
  stack2: EastTypeValue[],
): boolean {
  // Equi-recursive type subtyping: unfold recursive types when only one side is recursive
  if (t1.type === "Recursive") {
    if (t2.type === "Recursive") {
      // Recursive types are invariant - heap allocations must match exactly
      const r1 = stack1[stack1.length - Number(t1.value)];
      if (r1 === undefined) {
        throw new Error(`Invalid Recursive type reference: ${t1.value} at depth ${stack1.length}`);
      }
      const r2 = stack2[stack2.length - Number(t2.value)];
      if (r2 === undefined) {
        throw new Error(`Invalid Recursive type reference: ${t2.value} at depth ${stack2.length}`);
      }
      return isTypeValueEqual(r1, r2);
    } else {
      // Recursive cannot fit in non-recursive (infinite cannot fit in finite)
      return false;
    }
  } else if (t2.type === "Recursive") {
    // If the head is "on the stack" we can do head covariance by unfolding once
    const r2 = stack2[stack2.length - Number(t2.value)];
    if (r2 === undefined) {
      throw new Error(`Invalid Recursive type reference: ${t2.value} at depth ${stack2.length}`);
    }
    return isSubtypeValue(t1, r2, stack1, stack2.slice(0, stack2.length - Number(t2.value)));
  }

  // Never is subtype of everything
  if (t1.type === "Never") {
    return true;
  }

  // Primitive types - must match exactly
  if (t1.type === "Null") return t2.type === "Null";
  if (t1.type === "Boolean") return t2.type === "Boolean";
  if (t1.type === "Integer") return t2.type === "Integer";
  if (t1.type === "Float") return t2.type === "Float";
  if (t1.type === "String") return t2.type === "String";
  if (t1.type === "DateTime") return t2.type === "DateTime";
  if (t1.type === "Blob") return t2.type === "Blob";

  // Ref type - invariant (mutable)
  if (t1.type === "Ref" && t2.type === "Ref") {
    return isTypeValueEqual(t1.value, t2.value);
  }

  // Array type - invariant (mutable)
  if (t1.type === "Array" && t2.type === "Array") {
    return isTypeValueEqual(t1.value, t2.value);
  }

  // Set type - invariant (mutable)
  if (t1.type === "Set" && t2.type === "Set") {
    return isTypeValueEqual(t1.value, t2.value);
  }

  // Dict type - invariant (mutable)
  if (t1.type === "Dict" && t2.type === "Dict") {
    return isTypeValueEqual(t1.value.key, t2.value.key) &&
           isTypeValueEqual(t1.value.value, t2.value.value);
  }

  // Struct type - covariant in fields
  if (t1.type === "Struct" && t2.type === "Struct") {
    const fields1 = t1.value;
    const fields2 = t2.value;
    if (fields1.length !== fields2.length) return false;
    stack1.push(t1);
    stack2.push(t2);
    try {
      for (let i = 0; i < fields1.length; i++) {
        if (fields1[i]!.name !== fields2[i]!.name) return false;
        if (!isSubtypeValue(fields1[i]!.type, fields2[i]!.type, stack1, stack2)) return false;
      }
      return true;
    } finally {
      stack1.pop();
      stack2.pop();
    }
  }

  // Variant type - width subtyping (t1 can have more cases than t2)
  if (t1.type === "Variant" && t2.type === "Variant") {
    const cases1 = t1.value;
    const cases2 = t2.value;
    // For each case in t1, there must be a corresponding case in t2
    // and the payload type must be a subtype
    stack1.push(t1);
    stack2.push(t2);
    try {
      for (const case1 of cases1) {
        const case2 = cases2.find(c => c.name === case1.name);
        if (!case2) {
          // t2 doesn't have this case, so it can't accept all values of t1
          // (unless t2's corresponding case would be Never, but we don't model that explicitly)
          return false;
        }
        if (!isSubtypeValue(case1.type, case2.type, stack1, stack2)) return false;
      }
      return true;
    } finally {
      stack1.pop();
      stack2.pop();
    }
  }

  // Function type - contravariant inputs, covariant output
  if (t1.type === "Function" && (t2.type === "Function" || t2.type === "AsyncFunction")) {
    const inputs1 = t1.value.inputs;
    const inputs2 = t2.value.inputs;
    if (inputs1.length !== inputs2.length) return false;
    stack1.push(t1);
    stack2.push(t2);
    try {
      // Contravariant inputs: t2's inputs must be subtypes of t1's inputs
      for (let i = 0; i < inputs1.length; i++) {
        if (!isSubtypeValue(inputs2[i], inputs1[i], stack2, stack1)) return false;
      }
      // Covariant output
      return isSubtypeValue(t1.value.output, t2.value.output, stack1, stack2);
    } finally {
      stack1.pop();
      stack2.pop();
    }
  }

  if (t1.type === "AsyncFunction" && t2.type === "AsyncFunction") {
    const inputs1 = t1.value.inputs;
    const inputs2 = t2.value.inputs;
    if (inputs1.length !== inputs2.length) return false;
    stack1.push(t1);
    stack2.push(t2);
    try {
      // Contravariant inputs: t2's inputs must be subtypes of t1's inputs
      for (let i = 0; i < inputs1.length; i++) {
        if (!isSubtypeValue(inputs2[i], inputs1[i], stack2, stack1)) return false;
      }
      // Covariant output
      return isSubtypeValue(t1.value.output, t2.value.output, stack1, stack2);
    } finally {
      stack1.pop();
      stack2.pop();
    }
  }

  // Different type constructors - not subtypes
  return false;
}

// Cache for memoizing expandTypeValue results (top-level calls only)
const expandTypeValueCache = new WeakMap<EastTypeValue, EastTypeValue>();

/** Expand recursive types one level deeper, if necessary */
export function expandTypeValue(type: EastTypeValue, root: EastTypeValue = type, depth = 0n): EastTypeValue {
  // Fast path: primitive types cannot contain recursive references
  if (type.type === "Never" || type.type === "Null" || type.type === "Boolean" ||
      type.type === "Integer" || type.type === "Float" || type.type === "String" ||
      type.type === "DateTime" || type.type === "Blob") {
    return type;
  }

  // Memoization for top-level calls
  const isTopLevel = root === type && depth === 0n;
  if (isTopLevel) {
    const cached = expandTypeValueCache.get(type);
    if (cached !== undefined) return cached;
    const result = expandTypeValueImpl(type, root, depth);
    expandTypeValueCache.set(type, result);
    return result;
  }

  return expandTypeValueImpl(type, root, depth);
}

function expandTypeValueImpl(type: EastTypeValue, root: EastTypeValue, depth: bigint): EastTypeValue {
  if (type.type === "Ref") {
    return variant("Ref", expandTypeValue(type.value, root, depth + 1n));
  } else if (type.type === "Array") {
    return variant("Array", expandTypeValue(type.value, root, depth + 1n));
  } else if (type.type === "Dict") {
    return variant("Dict", {
      key: type.value.key,
      value: expandTypeValue(type.value.value, root, depth + 1n),
    });
  } else if (type.type === "Struct") {
    return variant("Struct", type.value.map(f => ({
      name: f.name,
      type: expandTypeValue(f.type, root, depth + 1n),
    })));
  } else if (type.type === "Variant") {
    return variant("Variant", type.value.map(c => ({
      name: c.name,
      type: expandTypeValue(c.type, root, depth + 1n),
    })));
  } else if (type.type === "Function") {
    return variant("Function", {
      inputs: type.value.inputs.map(i => expandTypeValue(i, root, depth + 1n)),
      output: expandTypeValue(type.value.output, root, depth + 1n),
    });
  } else if (type.type === "AsyncFunction") {
    return variant("AsyncFunction", {
      inputs: type.value.inputs.map(i => expandTypeValue(i, root, depth + 1n)),
      output: expandTypeValue(type.value.output, root, depth + 1n),
    });
  } else if (type.type === "Recursive" && depth === type.value) {
    // Unfold once
    return root;
  } else {
    return type;
  }
}

/**
 * Checks if an EastTypeValue represents a data type (serializable, no functions).
 *
 * This is the {@link EastTypeValue} version of {@link isDataType}.
 * Data types have a total ordering, can be fully serialized and transmitted between runtimes.
 *
 * @param type - The type value to check
 * @param depth - Internal parameter for tracking recursion depth
 * @returns `true` if the type is a data type (no functions), `false` otherwise
 */
export function isDataTypeValue(
  type: EastTypeValue,
  depth: number = 0,
): boolean {
  // Handle recursive type references - back-reference means we've already
  // checked this type in the current path, so it's safe (would have returned
  // false already if it contained functions)
  if (type.type === "Recursive") {
    return true;
  }

  // Function types are not data types
  if (type.type === "Function" || type.type === "AsyncFunction") {
    return false;
  }

  // Primitive types are data types
  if (type.type === "Never" || type.type === "Null" || type.type === "Boolean" ||
      type.type === "Integer" || type.type === "Float" || type.type === "String" ||
      type.type === "DateTime" || type.type === "Blob") {
    return true;
  }

  // Container types - recursively check contents
  if (type.type === "Ref") {
    return isDataTypeValue(type.value, depth + 1);
  }

  if (type.type === "Array") {
    return isDataTypeValue(type.value, depth + 1);
  }

  if (type.type === "Set") {
    // Set keys are checked at construction time to be immutable data types
    return true;
  }

  if (type.type === "Dict") {
    // Dict keys are checked at construction time
    return isDataTypeValue(type.value.value, depth + 1);
  }

  if (type.type === "Struct") {
    for (const field of type.value) {
      if (!isDataTypeValue(field.type, depth + 1)) {
        return false;
      }
    }
    return true;
  }

  if (type.type === "Variant") {
    for (const case_ of type.value) {
      if (!isDataTypeValue(case_.type, depth + 1)) {
        return false;
      }
    }
    return true;
  }

  // Unknown type - assume it's a data type (shouldn't happen)
  return true;
}