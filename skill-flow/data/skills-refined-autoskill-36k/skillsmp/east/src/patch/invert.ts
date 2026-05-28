/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * invertFor - Invert a patch.
 *
 * @module
 */

import { toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import type { EastType } from "../types.js";
import { isVariant, variant, type variant as VariantValue } from "../containers/variant.js";
import { equalFor, compareFor } from "../comparison.js";
import { SortedMap } from "../containers/sortedmap.js";
import { type InvertContext } from "./types.js";

export function invertFor(type: EastTypeValue, ctx?: InvertContext): (patch: any) => any;
export function invertFor<T extends EastType>(type: T): (patch: any) => any;
export function invertFor(type: EastTypeValue | EastType, ctx: InvertContext = { invert: [], types: [], equal: [] }): (patch: any) => any {
  // Convert to EastTypeValue and use a properly typed variable
  const t: EastTypeValue = isVariant(type) ? type : toEastTypeValue(type as EastType);

  if (t.type === "Never") {
    return (_patch: any) => {
      throw new Error("Cannot invert patches for type Never");
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
    return (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else {
        throw new Error(`Invalid patch type for primitive inversion: ${patch.type}`);
      }
    };
  } else if (t.type === "Array") {
    let elementInvert: (patch: any) => any;

    const ret = (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else if (patch.type === "patch") {
        const operations: any[] = patch.value;
        const inverted: any[] = [];

        for (let i = operations.length - 1; i >= 0; i--) {
          const op = operations[i]!;
          if (op.operation.type === "delete") {
            // Delete becomes insert at same position
            inverted.push({
              key: op.key,
              offset: 0n,
              operation: variant("insert", op.operation.value),
            });
          } else if (op.operation.type === "insert") {
            // Insert becomes delete at same position
            inverted.push({
              key: op.key,
              offset: 0n,
              operation: variant("delete", op.operation.value),
            });
          } else if (op.operation.type === "update") {
            inverted.push({
              key: op.key,
              offset: 0n,
              operation: variant("update", elementInvert(op.operation.value)),
            });
          }
        }

        return variant("patch", inverted);
      } else {
        throw new Error(`Invalid patch type for array inversion: ${patch.type}`);
      }
    };

    // Build array equality using equalFor with current context
    const arrayEqual = equalFor(t, ctx.equal);

    ctx.invert.push(ret);
    ctx.types.push(t);
    ctx.equal.push(arrayEqual);
    elementInvert = invertFor(t.value, ctx);
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Set") {
    const keyCompare = compareFor(t.value);

    return (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else if (patch.type === "patch") {
        const operations: SortedMap<any, any> = patch.value;
        const inverted = new SortedMap<any, any>(undefined, keyCompare);

        for (const [key, op] of operations) {
          if (op.type === "delete") {
            inverted.set(key, variant("insert", null));
          } else if (op.type === "insert") {
            inverted.set(key, variant("delete", null));
          }
        }

        return variant("patch", inverted);
      } else {
        throw new Error(`Invalid patch type for set inversion: ${patch.type}`);
      }
    };
  } else if (t.type === "Dict") {
    let valueInvert: (patch: any) => any;
    const keyCompare = compareFor(t.value.key);

    const ret = (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else if (patch.type === "patch") {
        const operations: SortedMap<any, any> = patch.value;
        const inverted = new SortedMap<any, any>(undefined, keyCompare);

        for (const [key, op] of operations) {
          if (op.type === "delete") {
            inverted.set(key, variant("insert", op.value));
          } else if (op.type === "insert") {
            inverted.set(key, variant("delete", op.value));
          } else if (op.type === "update") {
            inverted.set(key, variant("update", valueInvert(op.value)));
          }
        }

        return variant("patch", inverted);
      } else {
        throw new Error(`Invalid patch type for dict inversion: ${patch.type}`);
      }
    };

    // Build dict equality using equalFor with current context
    const dictEqual = equalFor(t, ctx.equal);

    ctx.invert.push(ret);
    ctx.types.push(t);
    ctx.equal.push(dictEqual);
    valueInvert = invertFor(t.value.value, ctx);
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Struct") {
    const fieldInverts: Record<string, (patch: any) => any> = {};

    const ret = (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else if (patch.type === "patch") {
        const result: Record<string, any> = {};
        let allUnchanged = true;

        for (const { name } of t.value) {
          const inverted = fieldInverts[name]!(patch.value[name]);
          result[name] = inverted;
          if (inverted.type !== "unchanged") {
            allUnchanged = false;
          }
        }

        if (allUnchanged) {
          return variant("unchanged", null);
        }

        return variant("patch", result);
      } else {
        throw new Error(`Invalid patch type for struct inversion: ${patch.type}`);
      }
    };

    // Build struct equality using equalFor with current context
    const structEqual = equalFor(t, ctx.equal);

    ctx.invert.push(ret);
    ctx.types.push(t);
    ctx.equal.push(structEqual);
    for (const { name, type: fieldType } of t.value) {
      fieldInverts[name] = invertFor(fieldType, ctx);
    }
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Variant") {
    const caseInverts: Record<string, (patch: any) => any> = {};

    const ret = (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else if (patch.type === "patch") {
        const caseName = patch.value.type;
        const inverted = caseInverts[caseName]!(patch.value.value);

        if (inverted.type === "unchanged") {
          return variant("unchanged", null);
        }

        return variant("patch", variant(caseName, inverted));
      } else {
        throw new Error(`Invalid patch type for variant inversion: ${patch.type}`);
      }
    };

    // Build variant equality using equalFor with current context
    const variantEqual = equalFor(t, ctx.equal);

    ctx.invert.push(ret);
    ctx.types.push(t);
    ctx.equal.push(variantEqual);
    for (const { name, type: caseType } of t.value) {
      caseInverts[name] = invertFor(caseType, ctx);
    }
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Ref") {
    let innerInvert: (patch: any) => any;

    const ret = (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else if (patch.type === "patch") {
        const inverted = innerInvert(patch.value);
        if (inverted.type === "unchanged") {
          return variant("unchanged", null);
        }
        return variant("patch", inverted);
      } else {
        throw new Error(`Invalid patch type for ref inversion: ${patch.type}`);
      }
    };

    // Build ref equality using equalFor with current context
    const refEqual = equalFor(t, ctx.equal);

    ctx.invert.push(ret);
    ctx.types.push(t);
    ctx.equal.push(refEqual);
    innerInvert = invertFor(t.value, ctx);
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();

    return ret;
  } else if (t.type === "Recursive") {
    // Recursive types use replace-only semantics - only unchanged and replace patches
    return (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else {
        throw new Error(`Invalid patch type for recursive type inversion: ${patch.type}`);
      }
    };
  } else if (t.type === "Function" || t.type === "AsyncFunction") {
    return (patch: VariantValue) => {
      if (patch.type === "unchanged") {
        return patch;
      } else if (patch.type === "replace") {
        return variant("replace", { before: patch.value.after, after: patch.value.before });
      } else {
        throw new Error(`Invalid patch type for function inversion: ${patch.type}`);
      }
    };
  } else {
    throw new Error(`Unhandled type in invertFor: ${(t as EastTypeValue).type}`);
  }
}
