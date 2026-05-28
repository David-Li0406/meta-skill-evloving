/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * PatchType constructor for computing patch types from East types.
 *
 * @module
 */

import {
  type EastType,
  NullType,
  StructType,
  VariantType,
  ArrayType,
  DictType,
  IntegerType,
} from "../types.js";

/**
 * Construct the patch type for a given East type.
 * Works directly with EastType objects (not EastTypeValue variants).
 * Uses a context map to handle recursive types.
 */
export function PatchType<T extends EastType>(type: T, ctx?: Map<EastType, EastType>): EastType {
  // Initialize context for tracking recursive types
  const context = ctx ?? new Map<EastType, EastType>();

  // Check if we've already computed the patch type for this type (handles recursion)
  const cached = context.get(type);
  if (cached !== undefined) {
    return cached;
  }

  const t = type as EastType;

  if (
    t.type === "Never" ||
    t.type === "Null" ||
    t.type === "Boolean" ||
    t.type === "Integer" ||
    t.type === "Float" ||
    t.type === "String" ||
    t.type === "DateTime" ||
    t.type === "Blob"
  ) {
    return VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
    });
  } else if (t.type === "Array") {
    const elementType = t.value;
    const elementPatchType = PatchType(elementType, context);
    const operationType = VariantType({
      delete: elementType,
      insert: elementType,
      update: elementPatchType,
    });
    const entryType = StructType({
      key: IntegerType,
      offset: IntegerType,
      operation: operationType,
    });
    return VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
      patch: ArrayType(entryType),
    });
  } else if (t.type === "Set") {
    const keyType = t.key;
    const operationType = VariantType({
      delete: NullType,
      insert: NullType,
    });
    return VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
      patch: DictType(keyType, operationType),
    });
  } else if (t.type === "Dict") {
    const keyType = t.key;
    const valueType = t.value;
    const valuePatchType = PatchType(valueType, context);
    const operationType = VariantType({
      delete: valueType,
      insert: valueType,
      update: valuePatchType,
    });
    return VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
      patch: DictType(keyType, operationType),
    });
  } else if (t.type === "Struct") {
    const fieldTypes = t.fields;
    const patchFields: Record<string, EastType> = {};
    for (const [name, fieldType] of Object.entries(fieldTypes)) {
      patchFields[name] = PatchType(fieldType, context);
    }
    return VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
      patch: StructType(patchFields),
    });
  } else if (t.type === "Variant") {
    const caseTypes = t.cases;
    const patchCases: Record<string, EastType> = {};
    for (const [name, caseType] of Object.entries(caseTypes)) {
      patchCases[name] = PatchType(caseType, context);
    }
    return VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
      patch: VariantType(patchCases),
    });
  } else if (t.type === "Ref") {
    const innerType = t.value;
    const innerPatchType = PatchType(innerType, context);
    return VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
      patch: innerPatchType,
    });
  } else if (t.type === "Recursive") {
    // Check if we've already seen this type (handles circular back-references)
    const cached = context.get(type);
    if (cached !== undefined) {
      return cached;
    }

    // For back-references within the recursive structure, use replace-only semantics
    // Register this BEFORE recursing so circular refs are caught
    const replaceOnlyType = VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
    });
    context.set(type, replaceOnlyType);

    // Recurse into the node - the outer structure gets structural patching
    return PatchType(t.node, context);
  } else if (t.type === "Function" || t.type === "AsyncFunction") {
    return VariantType({
      unchanged: NullType,
      replace: StructType({ before: type, after: type }),
    });
  } else {
    throw new Error(`Unhandled type in PatchType: ${(t as EastType).type}`);
  }
}
