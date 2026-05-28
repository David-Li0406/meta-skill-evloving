/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * diffFor - Compute difference between two East values.
 *
 * @module
 */

import { toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import type { EastType, ValueTypeOf } from "../types.js";
import { isVariant, variant, type variant as VariantValue } from "../containers/variant.js";
import { equalFor, isFor, compareFor } from "../comparison.js";
import { SortedMap } from "../containers/sortedmap.js";
import { SortedSet } from "../containers/sortedset.js";
import type { ref } from "../containers/ref.js";
import { type DiffContext, computeLCS } from "./types.js";

export function diffFor(type: EastTypeValue, ctx?: DiffContext): (before: any, after: any) => any;
export function diffFor<T extends EastType>(type: T): (before: ValueTypeOf<T>, after: ValueTypeOf<T>) => any;
export function diffFor(type: EastTypeValue | EastType, ctx: DiffContext = { diff: [], types: [], equal: [] }): (before: any, after: any) => any {
  // Convert to EastTypeValue and use a properly typed variable
  const t: EastTypeValue = isVariant(type) ? type : toEastTypeValue(type as EastType);

  if (t.type === "Never") {
    return (_before: any, _after: any) => {
      throw new Error("Cannot diff values of type Never");
    };
  } else if (
    t.type === "Null" ||
    t.type === "Boolean" ||
    t.type === "Integer" ||
    t.type === "Float" ||
    t.type === "String" ||
    t.type === "DateTime" ||
    t.type === "Blob"
  ) {
    const equal = equalFor(t);
    return (before: any, after: any) => {
      if (equal(before, after)) {
        return variant("unchanged", null);
      }
      return variant("replace", { before, after });
    };
  } else if (t.type === "Array") {
    let elementEqual: (a: any, b: any) => boolean;
    let is: (a: any, b: any) => boolean;

    const ret = (before: any[], after: any[]) => {
      if (is(before, after)) {
        return variant("unchanged", null);
      }

      const { beforeIndices, afterIndices } = computeLCS(before, after, elementEqual);

      const operations: any[] = [];
      let beforePtr = 0;
      let afterPtr = 0;
      let lcsPtr = 0;
      let deleteCount = 0;
      let insertCount = 0;  // Track inserts that shift subsequent delete positions

      while (beforePtr < before.length || afterPtr < after.length) {
        const nextBeforeLCS = lcsPtr < beforeIndices.length ? beforeIndices[lcsPtr]! : before.length;
        const nextAfterLCS = lcsPtr < afterIndices.length ? afterIndices[lcsPtr]! : after.length;

        while (beforePtr < nextBeforeLCS) {
          // For deletes: key is the position in the mutating array
          // We need to account for:
          // - Previous deletes (which shrink the array)
          // - Previous inserts (which grow the array and shift positions)
          const actualPosition = beforePtr - deleteCount + insertCount;
          operations.push({
            key: BigInt(actualPosition),
            offset: 0n,
            operation: variant("delete", before[beforePtr]!),
          });
          deleteCount++;
          beforePtr++;
        }

        while (afterPtr < nextAfterLCS) {
          // For inserts: key is the position in the target array
          operations.push({
            key: BigInt(afterPtr),
            offset: 0n,
            operation: variant("insert", after[afterPtr]!),
          });
          insertCount++;
          afterPtr++;
        }

        if (lcsPtr < beforeIndices.length) {
          beforePtr++;
          afterPtr++;
          lcsPtr++;
        }
      }

      if (operations.length === 0) {
        return variant("unchanged", null);
      }

      return variant("patch", operations);
    };

    // Build array equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    const arrayEqual = equalFor(t, ctx.equal);

    ctx.diff.push(ret);
    ctx.types.push(t);
    ctx.equal.push(arrayEqual);
    is = isFor(t, ctx.equal);
    elementEqual = equalFor(t.value as EastTypeValue, ctx.equal);
    ctx.diff.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Set") {
    // Set keys cannot contain recursive types, so no context needed
    const is = isFor(t);
    const keyCompare = compareFor(t.value);

    return (before: SortedSet<any>, after: SortedSet<any>) => {
      if (is(before, after)) {
        return variant("unchanged", null);
      }

      const operations = new SortedMap<any, any>(undefined, keyCompare);

      for (const key of before) {
        if (!after.has(key)) {
          operations.set(key, variant("delete", null));
        }
      }

      for (const key of after) {
        if (!before.has(key)) {
          operations.set(key, variant("insert", null));
        }
      }

      if (operations.size === 0) {
        return variant("unchanged", null);
      }

      let deleteCount = 0;
      let insertCount = 0;
      for (const op of operations.values()) {
        if (op.type === "delete") deleteCount++;
        if (op.type === "insert") insertCount++;
      }
      if (deleteCount === before.size && insertCount === after.size && before.size > 0) {
        return variant("replace", { before, after });
      }

      return variant("patch", operations);
    };
  } else if (t.type === "Dict") {
    let valueDiff: (a: any, b: any) => any;
    let valueEqual: (a: any, b: any) => boolean;
    let is: (a: any, b: any) => boolean;
    // Dict keys cannot contain recursive types, so no context needed for keyCompare
    const keyCompare = compareFor(t.value.key);

    const ret = (before: SortedMap<any, any>, after: SortedMap<any, any>) => {
      if (is(before, after)) {
        return variant("unchanged", null);
      }

      const operations = new SortedMap<any, any>(undefined, keyCompare);

      for (const [key, beforeValue] of before) {
        if (!after.has(key)) {
          operations.set(key, variant("delete", beforeValue));
        } else {
          const afterValue = after.get(key)!;
          if (!valueEqual(beforeValue, afterValue)) {
            const patch = valueDiff(beforeValue, afterValue);
            operations.set(key, variant("update", patch));
          }
        }
      }

      for (const [key, afterValue] of after) {
        if (!before.has(key)) {
          operations.set(key, variant("insert", afterValue));
        }
      }

      if (operations.size === 0) {
        return variant("unchanged", null);
      }

      let insertCount = 0;
      let deleteCount = 0;
      for (const op of operations.values()) {
        if (op.type === "insert") insertCount++;
        if (op.type === "delete") deleteCount++;
      }
      if (insertCount === after.size && deleteCount === before.size && before.size > 0) {
        return variant("replace", { before, after });
      }

      return variant("patch", operations);
    };

    // Build dict equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    const dictEqual = equalFor(t, ctx.equal);

    ctx.diff.push(ret);
    ctx.types.push(t);
    ctx.equal.push(dictEqual);
    is = isFor(t, ctx.equal);
    valueDiff = diffFor(t.value.value, ctx);
    valueEqual = equalFor(t.value.value as EastTypeValue, ctx.equal);
    ctx.diff.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Struct") {
    const fieldDiffs: Record<string, (a: any, b: any) => any> = {};
    const fieldEquals: Record<string, (a: any, b: any) => boolean> = {};

    const ret = (before: Record<string, any>, after: Record<string, any>) => {
      if (before === after) {
        return variant("unchanged", null);
      }

      const patchFields: Record<string, any> = {};
      let allUnchanged = true;

      for (const { name } of t.value) {
        const beforeValue = before[name];
        const afterValue = after[name];

        if (fieldEquals[name]!(beforeValue, afterValue)) {
          patchFields[name] = variant("unchanged", null);
        } else {
          patchFields[name] = fieldDiffs[name]!(beforeValue, afterValue);
          allUnchanged = false;
        }
      }

      if (allUnchanged) {
        return variant("unchanged", null);
      }

      return variant("patch", patchFields);
    };

    // Build struct equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    const structEqual = equalFor(t, ctx.equal);

    ctx.diff.push(ret);
    ctx.types.push(t);
    ctx.equal.push(structEqual);
    for (const { name, type: fieldType } of t.value) {
      fieldDiffs[name] = diffFor(fieldType, ctx);
      fieldEquals[name] = equalFor(fieldType as EastTypeValue, ctx.equal);
    }
    ctx.diff.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Variant") {
    const caseDiffs: Record<string, (a: any, b: any) => any> = {};
    const caseEquals: Record<string, (a: any, b: any) => boolean> = {};

    const ret = (before: VariantValue, after: VariantValue) => {
      if (before === after) {
        return variant("unchanged", null);
      }

      if (before.type !== after.type) {
        return variant("replace", { before, after });
      }

      const caseName = before.type;
      if (caseEquals[caseName]!(before.value, after.value)) {
        return variant("unchanged", null);
      }

      const casePatch = caseDiffs[caseName]!(before.value, after.value);

      if (casePatch.type === "unchanged") {
        return variant("unchanged", null);
      }

      return variant("patch", variant(caseName, casePatch));
    };

    // Build variant equality using equalFor with current context
    const variantEqual = equalFor(t, ctx.equal);

    ctx.diff.push(ret);
    ctx.types.push(t);
    ctx.equal.push(variantEqual);
    for (const { name, type: caseType } of t.value) {
      caseDiffs[name] = diffFor(caseType, ctx);
      caseEquals[name] = equalFor(caseType as EastTypeValue, ctx.equal);
    }
    ctx.diff.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Ref") {
    let innerDiff: (a: any, b: any) => any;
    let innerEqual: (a: any, b: any) => boolean;
    let is: (a: any, b: any) => boolean;

    const ret = (before: ref<any>, after: ref<any>) => {
      if (is(before, after)) {
        return variant("unchanged", null);
      }

      if (innerEqual(before.value, after.value)) {
        return variant("unchanged", null);
      }

      const innerPatch = innerDiff(before.value, after.value);

      if (innerPatch.type === "unchanged") {
        return variant("unchanged", null);
      }

      return variant("patch", innerPatch);
    };

    // Build ref equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    const refEqual = equalFor(t, ctx.equal);

    ctx.diff.push(ret);
    ctx.types.push(t);
    ctx.equal.push(refEqual);
    is = isFor(t, ctx.equal);
    innerDiff = diffFor(t.value, ctx);
    innerEqual = equalFor(t.value as EastTypeValue, ctx.equal);
    ctx.diff.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Recursive") {
    // Recursive types use replace-only semantics - no structural patching.
    // Look up the type and equality function from context, but always replace.
    const resolvedType = ctx.types[ctx.types.length - Number(t.value)];
    if (resolvedType === undefined) {
      throw new Error(`Internal error: Recursive type context not found in diffFor`);
    }
    const equal = ctx.equal[ctx.equal.length - Number(t.value)];
    if (equal === undefined) {
      throw new Error(`Internal error: Recursive equal context not found in diffFor`);
    }
    return (before: any, after: any) => {
      if (equal(before, after)) {
        return variant("unchanged", null);
      }
      return variant("replace", { before, after });
    };
  } else if (t.type === "Function" || t.type === "AsyncFunction") {
    return (_before: any, _after: any) => variant("unchanged", null);
  } else {
    throw new Error(`Unhandled type in diffFor: ${(t as EastTypeValue).type}`);
  }
}
