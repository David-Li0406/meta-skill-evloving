/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * applyFor - Apply a patch to an East value.
 *
 * @module
 */

import { toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import type { EastType, ValueTypeOf } from "../types.js";
import { isVariant, variant, type variant as VariantValue } from "../containers/variant.js";
import { equalFor, compareFor } from "../comparison.js";
import { printFor } from "../serialization/east.js";
import { SortedMap } from "../containers/sortedmap.js";
import { SortedSet } from "../containers/sortedset.js";
import type { ref } from "../containers/ref.js";
import { type ApplyContext, ConflictError } from "./types.js";

export function applyFor(type: EastTypeValue, ctx?: ApplyContext): (base: any, patch: any) => any;
export function applyFor<T extends EastType>(type: T): (base: ValueTypeOf<T>, patch: any) => ValueTypeOf<T>;
export function applyFor(type: EastTypeValue | EastType, ctx: ApplyContext = { apply: [], types: [], equal: [], print: [] }): (base: any, patch: any) => any {
  // Convert to EastTypeValue and use a properly typed variable
  const t: EastTypeValue = isVariant(type) ? type : toEastTypeValue(type as EastType);

  if (t.type === "Never") {
    return (_base: any, _patch: any) => {
      throw new Error("Cannot apply patch to values of type Never");
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
    const print = printFor(t);
    return (base: any, patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        if (!equal(base, patch.value.before)) {
          throw new ConflictError(
            `Cannot apply replace - expected ${print(patch.value.before)}, found ${print(base)}`
          );
        }
        return patch.value.after;
      } else {
        throw new Error(`Invalid patch type for primitive: ${patch.type}`);
      }
    };
  } else if (t.type === "Array") {
    let elementApply: (base: any, patch: any) => any;
    let elementEqual: (a: any, b: any) => boolean;
    let elementPrint: (v: any) => string;
    let arrayEqual: (a: any, b: any) => boolean;

    const ret = (base: any[], patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        if (!arrayEqual(base, patch.value.before)) {
          throw new ConflictError("Cannot apply replace - base array does not match expected");
        }
        return [...patch.value.after];
      } else if (patch.type === "patch") {
        const result = [...base];
        const operations: any[] = patch.value;

        for (const op of operations) {
          const key = Number(op.key);
          const offset = Number(op.offset);
          const oldKey = key + offset;

          if (op.operation.type === "delete") {
            if (oldKey < 0 || oldKey >= result.length) {
              throw new ConflictError(
                `Cannot delete at index ${oldKey} - array length is ${result.length}`
              );
            }
            if (!elementEqual(result[oldKey]!, op.operation.value)) {
              throw new ConflictError(
                `Cannot delete at index ${oldKey} - expected ${elementPrint(op.operation.value)}, found ${elementPrint(result[oldKey])}`
              );
            }
            result.splice(oldKey, 1);
          } else if (op.operation.type === "insert") {
            if (key < 0 || key > result.length) {
              throw new ConflictError(
                `Cannot insert at index ${key} - array length is ${result.length}`
              );
            }
            result.splice(key, 0, op.operation.value);
          } else if (op.operation.type === "update") {
            if (oldKey < 0 || oldKey >= result.length) {
              throw new ConflictError(
                `Cannot update at index ${oldKey} - array length is ${result.length}`
              );
            }
            result[oldKey] = elementApply(result[oldKey]!, op.operation.value);
          }
        }

        return result;
      } else {
        throw new Error(`Invalid patch type for array: ${patch.type}`);
      }
    };

    // Build print handler for this array type (used in error messages)
    const arrayPrint = printFor(t, ctx.print);

    // Build array equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    arrayEqual = equalFor(t, ctx.equal);

    ctx.apply.push(ret);
    ctx.types.push(t);
    ctx.equal.push(arrayEqual);
    ctx.print.push(arrayPrint);
    elementApply = applyFor(t.value, ctx);
    elementEqual = equalFor(t.value as EastTypeValue, ctx.equal);
    elementPrint = printFor(t.value as EastTypeValue, ctx.print);
    ctx.apply.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return ret;
  } else if (t.type === "Set") {
    const keyPrint = printFor(t.value);
    const setEqual = equalFor(t, ctx.equal);
    const keyCompare = compareFor(t.value);

    return (base: SortedSet<any>, patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        if (!setEqual(base, patch.value.before)) {
          throw new ConflictError("Cannot apply replace - base set does not match expected");
        }
        return new SortedSet(patch.value.after, keyCompare);
      } else if (patch.type === "patch") {
        const result = new SortedSet(base, keyCompare);
        const operations: SortedMap<any, any> = patch.value;

        for (const [key, op] of operations) {
          if (op.type === "delete") {
            if (!result.has(key)) {
              throw new ConflictError(
                `Cannot delete key ${keyPrint(key)} - key does not exist`
              );
            }
            result.delete(key);
          } else if (op.type === "insert") {
            if (result.has(key)) {
              throw new ConflictError(
                `Cannot insert key ${keyPrint(key)} - key already exists`
              );
            }
            result.add(key);
          }
        }

        return result;
      } else {
        throw new Error(`Invalid patch type for set: ${patch.type}`);
      }
    };
  } else if (t.type === "Dict") {
    let valueApply: (base: any, patch: any) => any;
    let valueEqual: (a: any, b: any) => boolean;
    let dictEqual: (a: any, b: any) => boolean;
    let keyPrint: (v: any) => string;
    let valuePrint: (v: any) => string;
    const keyCompare = compareFor(t.value.key);

    const ret = (base: SortedMap<any, any>, patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        if (!dictEqual(base, patch.value.before)) {
          throw new ConflictError("Cannot apply replace - base dict does not match expected");
        }
        return new SortedMap(patch.value.after, keyCompare);
      } else if (patch.type === "patch") {
        const result = new SortedMap(base, keyCompare);
        const operations: SortedMap<any, any> = patch.value;

        for (const [key, op] of operations) {
          if (op.type === "delete") {
            if (!result.has(key)) {
              throw new ConflictError(
                `Cannot delete key ${keyPrint(key)} - key does not exist`
              );
            }
            if (!valueEqual(result.get(key), op.value)) {
              throw new ConflictError(
                `Cannot delete key ${keyPrint(key)} - expected value ${valuePrint(op.value)}, found ${valuePrint(result.get(key))}`
              );
            }
            result.delete(key);
          } else if (op.type === "insert") {
            if (result.has(key)) {
              throw new ConflictError(
                `Cannot insert key ${keyPrint(key)} - key already exists with value ${valuePrint(result.get(key))}`
              );
            }
            result.set(key, op.value);
          } else if (op.type === "update") {
            if (!result.has(key)) {
              throw new ConflictError(
                `Cannot update key ${keyPrint(key)} - key does not exist`
              );
            }
            result.set(key, valueApply(result.get(key), op.value));
          }
        }

        return result;
      } else {
        throw new Error(`Invalid patch type for dict: ${patch.type}`);
      }
    };

    // Build print handler for this dict type (used in error messages)
    const dictPrint = printFor(t, ctx.print);

    // Build dict equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    dictEqual = equalFor(t, ctx.equal);

    ctx.apply.push(ret);
    ctx.types.push(t);
    ctx.equal.push(dictEqual);
    ctx.print.push(dictPrint);
    valueApply = applyFor(t.value.value, ctx);
    valueEqual = equalFor(t.value.value as EastTypeValue, ctx.equal);
    // Keys can't be recursive, so no context needed
    keyPrint = printFor(t.value.key as EastTypeValue);
    // Values may contain recursive references, use print context
    valuePrint = printFor(t.value.value as EastTypeValue, ctx.print);
    ctx.apply.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return ret;
  } else if (t.type === "Struct") {
    const fieldApplies: Record<string, (base: any, patch: any) => any> = {};
    let equal: (a: any, b: any) => boolean;

    const ret = (base: Record<string, any>, patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        if (!equal(base, patch.value.before)) {
          throw new ConflictError("Cannot apply replace - base struct does not match expected");
        }
        return { ...patch.value.after };
      } else if (patch.type === "patch") {
        const result: Record<string, any> = {};

        for (const { name } of t.value) {
          const fieldPatch = patch.value[name];
          result[name] = fieldApplies[name]!(base[name], fieldPatch);
        }

        return result;
      } else {
        throw new Error(`Invalid patch type for struct: ${patch.type}`);
      }
    };

    // Build print handler for this struct type
    const structPrint = printFor(t, ctx.print);

    // Build struct equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    equal = equalFor(t, ctx.equal);

    ctx.apply.push(ret);
    ctx.types.push(t);
    ctx.equal.push(equal);
    ctx.print.push(structPrint);
    for (const { name, type: fieldType } of t.value) {
      fieldApplies[name] = applyFor(fieldType, ctx);
    }
    ctx.apply.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return ret;
  } else if (t.type === "Variant") {
    const caseApplies: Record<string, (base: any, patch: any) => any> = {};
    let equal: (a: any, b: any) => boolean;

    const ret = (base: VariantValue, patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        if (!equal(base, patch.value.before)) {
          throw new ConflictError("Cannot apply replace - base variant does not match expected");
        }
        return patch.value.after;
      } else if (patch.type === "patch") {
        const caseName = patch.value.type;
        if (base.type !== caseName) {
          throw new ConflictError(
            `Cannot apply patch for case ${caseName} to variant with case ${base.type}`
          );
        }
        const casePatch = patch.value.value;
        const newValue = caseApplies[caseName]!(base.value, casePatch);
        return variant(caseName, newValue);
      } else {
        throw new Error(`Invalid patch type for variant: ${patch.type}`);
      }
    };

    // Build print handler for this variant type
    const variantPrint = printFor(t, ctx.print);

    // Build variant equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    equal = equalFor(t, ctx.equal);

    ctx.apply.push(ret);
    ctx.types.push(t);
    ctx.equal.push(equal);
    ctx.print.push(variantPrint);
    for (const { name, type: caseType } of t.value) {
      caseApplies[name] = applyFor(caseType, ctx);
    }
    ctx.apply.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return ret;
  } else if (t.type === "Ref") {
    let innerApply: (base: any, patch: any) => any;
    let equal: (a: any, b: any) => boolean;

    const ret = (base: ref<any>, patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        if (!equal(base, patch.value.before)) {
          throw new ConflictError("Cannot apply replace - base ref does not match expected");
        }
        return { value: patch.value.after.value };
      } else if (patch.type === "patch") {
        const newValue = innerApply(base.value, patch.value);
        return { value: newValue };
      } else {
        throw new Error(`Invalid patch type for ref: ${patch.type}`);
      }
    };

    // Build print handler for this ref type
    const refPrint = printFor(t, ctx.print);

    // Build ref equality using equalFor with current context
    // This must be pushed BEFORE recursing so children can reference it via .Recursive
    equal = equalFor(t, ctx.equal);

    ctx.apply.push(ret);
    ctx.types.push(t);
    ctx.equal.push(equal);
    ctx.print.push(refPrint);
    innerApply = applyFor(t.value, ctx);
    ctx.apply.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return ret;
  } else if (t.type === "Recursive") {
    // Recursive types use replace-only semantics - only unchanged and replace patches
    return (base: any, patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        return patch.value.after;
      } else {
        throw new Error(`Invalid patch type for recursive type: ${patch.type}`);
      }
    };
  } else if (t.type === "Function" || t.type === "AsyncFunction") {
    return (base: any, patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return base;
      } else if (patch.type === "replace") {
        return patch.value.after;
      } else {
        throw new Error(`Invalid patch type for function: ${patch.type}`);
      }
    };
  } else {
    throw new Error(`Unhandled type in applyFor: ${(t as EastTypeValue).type}`);
  }
}
