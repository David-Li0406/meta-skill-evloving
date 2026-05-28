/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * composeFor - Combine two sequential patches.
 *
 * @module
 */

import { toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import type { EastType } from "../types.js";
import { isVariant, variant, type variant as VariantValue } from "../containers/variant.js";
import { equalFor, compareFor } from "../comparison.js";
import { printFor } from "../serialization/east.js";
import { SortedMap } from "../containers/sortedmap.js";
import { type ComposeContext, ConflictError } from "./types.js";
import { applyFor } from "./apply.js";
import { invertFor } from "./invert.js";

export function composeFor(type: EastTypeValue, ctx?: ComposeContext): (first: any, second: any) => any;
export function composeFor<T extends EastType>(type: T): (first: any, second: any) => any;
export function composeFor(type: EastTypeValue | EastType, ctx: ComposeContext = { compose: [], apply: [], invert: [], types: [], equal: [], print: [] }): (first: any, second: any) => any {
  // Convert to EastTypeValue and use a properly typed variable
  const t: EastTypeValue = isVariant(type) ? type : toEastTypeValue(type as EastType);

  if (t.type === "Never") {
    return (_first: any, _second: any) => {
      throw new Error("Cannot compose patches for type Never");
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
    return (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else if (first.type === "replace" && second.type === "replace") {
        return variant("replace", { before: first.value.before, after: second.value.after });
      } else {
        throw new Error("Invalid patch composition for primitive");
      }
    };
  } else if (t.type === "Array") {
    let applyRet: (base: any, patch: any) => any;
    let invertRet: (patch: any) => any;

    const composeRet = (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else if (first.type === "replace" && second.type === "replace") {
        return variant("replace", { before: first.value.before, after: second.value.after });
      } else if (first.type === "replace" && second.type === "patch") {
        const afterSecond = applyRet(first.value.after, second);
        return variant("replace", { before: first.value.before, after: afterSecond });
      } else if (first.type === "patch" && second.type === "replace") {
        const invertedFirst = invertRet(first);
        const originalBefore = applyRet(second.value.before, invertedFirst);
        return variant("replace", { before: originalBefore, after: second.value.after });
      } else {
        // patch + patch: concatenate operations
        const p1Ops = first.value as any[];
        const p2Ops = second.value as any[];
        const result = [...p1Ops, ...p2Ops];
        if (result.length === 0) {
          return variant("unchanged", null);
        }
        return variant("patch", result);
      }
    };

    const arrayEqual = equalFor(t, ctx.equal);
    const arrayPrint = printFor(t, ctx.print);

    // Push compose context first
    ctx.compose.push(composeRet);
    ctx.types.push(t);
    ctx.equal.push(arrayEqual);
    ctx.print.push(arrayPrint);

    // Build apply/invert handlers using applyFor/invertFor
    applyRet = applyFor(t, { apply: ctx.apply, types: ctx.types, equal: ctx.equal, print: ctx.print });
    invertRet = invertFor(t, { invert: ctx.invert, types: ctx.types, equal: ctx.equal });

    // Push them so .Recursive lookups work during element compose recursion
    ctx.apply.push(applyRet);
    ctx.invert.push(invertRet);

    // Recurse into element type for compose
    composeFor(t.value, ctx);

    ctx.compose.pop();
    ctx.apply.pop();
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return composeRet;
  } else if (t.type === "Set") {
    const keyPrint = printFor(t.value);
    const keyCompare = compareFor(t.value);

    // Pass full context so recursive type references can be resolved
    const apply = applyFor(t, { apply: ctx.apply, types: ctx.types, equal: ctx.equal, print: ctx.print });
    const invert = invertFor(t, { invert: ctx.invert, types: ctx.types, equal: ctx.equal });

    return (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else if (first.type === "replace" && second.type === "replace") {
        return variant("replace", { before: first.value.before, after: second.value.after });
      } else if (first.type === "patch" && second.type === "patch") {
        const result = new SortedMap<any, any>(undefined, keyCompare);

        for (const [key, op] of first.value as SortedMap<any, any>) {
          result.set(key, op);
        }

        for (const [key, op] of second.value as SortedMap<any, any>) {
          if (result.has(key)) {
            const firstOp = result.get(key)!;
            if (firstOp.type === "insert" && op.type === "delete") {
              result.delete(key);
            } else if (firstOp.type === "delete" && op.type === "insert") {
              result.delete(key);
            } else {
              throw new ConflictError(
                `Cannot compose patches - conflicting operations on key ${keyPrint(key)}`
              );
            }
          } else {
            result.set(key, op);
          }
        }

        if (result.size === 0) {
          return variant("unchanged", null);
        }

        return variant("patch", result);
      } else {
        if (first.type === "replace") {
          const afterSecond = apply(first.value.after, second);
          return variant("replace", { before: first.value.before, after: afterSecond });
        } else {
          // Compute original before by inverting first and applying to second.before
          const invertedFirst = invert(first);
          const originalBefore = apply(second.value.before, invertedFirst);
          return variant("replace", { before: originalBefore, after: second.value.after });
        }
      }
    };
  } else if (t.type === "Dict") {
    let valueCompose: (first: any, second: any) => any;
    let valueApply: (base: any, patch: any) => any;
    let applyRet: (base: any, patch: any) => any;
    let invertRet: (patch: any) => any;
    const keyPrint = printFor(t.value.key);
    const keyCompare = compareFor(t.value.key);

    const composeRet = (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else if (first.type === "replace" && second.type === "replace") {
        return variant("replace", { before: first.value.before, after: second.value.after });
      } else if (first.type === "patch" && second.type === "patch") {
        const result = new SortedMap<any, any>(undefined, keyCompare);

        for (const [key, op] of first.value as SortedMap<any, any>) {
          result.set(key, op);
        }

        for (const [key, op] of second.value as SortedMap<any, any>) {
          if (result.has(key)) {
            const firstOp = result.get(key)!;

            if (firstOp.type === "insert" && op.type === "delete") {
              result.delete(key);
            } else if (firstOp.type === "insert" && op.type === "update") {
              const newValue = valueApply(firstOp.value, op.value);
              result.set(key, variant("insert", newValue));
            } else if (firstOp.type === "delete" && op.type === "insert") {
              result.set(key, variant("update", variant("replace", { before: firstOp.value, after: op.value })));
            } else if (firstOp.type === "update" && op.type === "delete") {
              throw new ConflictError(
                `Cannot compose patches - update then delete on key ${keyPrint(key)}`
              );
            } else if (firstOp.type === "update" && op.type === "update") {
              const composed = valueCompose(firstOp.value, op.value);
              result.set(key, variant("update", composed));
            } else {
              throw new ConflictError(
                `Cannot compose patches - conflicting operations on key ${keyPrint(key)}`
              );
            }
          } else {
            result.set(key, op);
          }
        }

        if (result.size === 0) {
          return variant("unchanged", null);
        }

        return variant("patch", result);
      } else {
        if (first.type === "replace") {
          const afterSecond = applyRet(first.value.after, second);
          return variant("replace", { before: first.value.before, after: afterSecond });
        } else {
          // Compute original before by inverting first and applying to second.before
          const invertedFirst = invertRet(first);
          const originalBefore = applyRet(second.value.before, invertedFirst);
          return variant("replace", { before: originalBefore, after: second.value.after });
        }
      }
    };

    // Build print handler for this dict type
    const dictPrint = printFor(t, ctx.print);

    // Build dict equality using equalFor with current context
    const dictEqual = equalFor(t, ctx.equal);

    // Push compose context first
    ctx.compose.push(composeRet);
    ctx.types.push(t);
    ctx.equal.push(dictEqual);
    ctx.print.push(dictPrint);

    // Build Dict apply/invert handlers (these recurse internally with their own push/pop)
    applyRet = applyFor(t, { apply: ctx.apply, types: ctx.types, equal: ctx.equal, print: ctx.print });
    invertRet = invertFor(t, { invert: ctx.invert, types: ctx.types, equal: ctx.equal });

    // Push them so .Recursive lookups work during value compose recursion
    ctx.apply.push(applyRet);
    ctx.invert.push(invertRet);

    // Recurse into value type for compose
    valueCompose = composeFor(t.value.value, ctx);
    // Build value apply with proper context (Dict handler is now in ctx.apply)
    valueApply = applyFor(t.value.value as EastTypeValue, { apply: ctx.apply, types: ctx.types, equal: ctx.equal, print: ctx.print });

    ctx.compose.pop();
    ctx.apply.pop();
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return composeRet;
  } else if (t.type === "Struct") {
    const fieldComposes: Record<string, (first: any, second: any) => any> = {};
    let applyRet: (base: any, patch: any) => any;
    let invertRet: (patch: any) => any;

    const composeRet = (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else if (first.type === "replace" && second.type === "replace") {
        return variant("replace", { before: first.value.before, after: second.value.after });
      } else if (first.type === "patch" && second.type === "patch") {
        const result: Record<string, any> = {};
        let allUnchanged = true;

        for (const { name } of t.value) {
          const composed = fieldComposes[name]!(first.value[name], second.value[name]);
          result[name] = composed;
          if (composed.type !== "unchanged") {
            allUnchanged = false;
          }
        }

        if (allUnchanged) {
          return variant("unchanged", null);
        }

        return variant("patch", result);
      } else {
        if (first.type === "replace") {
          const afterSecond = applyRet(first.value.after, second);
          return variant("replace", { before: first.value.before, after: afterSecond });
        } else {
          // Compute original before by inverting first and applying to second.before
          const invertedFirst = invertRet(first);
          const originalBefore = applyRet(second.value.before, invertedFirst);
          return variant("replace", { before: originalBefore, after: second.value.after });
        }
      }
    };

    const structEqual = equalFor(t, ctx.equal);
    const structPrint = printFor(t, ctx.print);

    // Push compose context first
    ctx.compose.push(composeRet);
    ctx.types.push(t);
    ctx.equal.push(structEqual);
    ctx.print.push(structPrint);

    // Build apply/invert handlers using applyFor/invertFor
    applyRet = applyFor(t, { apply: ctx.apply, types: ctx.types, equal: ctx.equal, print: ctx.print });
    invertRet = invertFor(t, { invert: ctx.invert, types: ctx.types, equal: ctx.equal });

    // Push them so .Recursive lookups work during field compose recursion
    ctx.apply.push(applyRet);
    ctx.invert.push(invertRet);

    // Recurse into field types for compose
    for (const { name, type: fieldType } of t.value) {
      fieldComposes[name] = composeFor(fieldType, ctx);
    }

    ctx.compose.pop();
    ctx.apply.pop();
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return composeRet;
  } else if (t.type === "Variant") {
    const caseComposes: Record<string, (first: any, second: any) => any> = {};
    let applyRet: (base: any, patch: any) => any;
    let invertRet: (patch: any) => any;

    const composeRet = (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else if (first.type === "replace" && second.type === "replace") {
        return variant("replace", { before: first.value.before, after: second.value.after });
      } else if (first.type === "patch" && second.type === "patch") {
        if (first.value.type !== second.value.type) {
          throw new ConflictError(
            `Cannot compose variant patches for different cases: ${first.value.type} and ${second.value.type}`
          );
        }
        const caseName = first.value.type;
        const composed = caseComposes[caseName]!(first.value.value, second.value.value);

        if (composed.type === "unchanged") {
          return variant("unchanged", null);
        }

        return variant("patch", variant(caseName, composed));
      } else {
        if (first.type === "replace") {
          const afterSecond = applyRet(first.value.after, second);
          return variant("replace", { before: first.value.before, after: afterSecond });
        } else {
          // first is "patch", second is "replace"
          // Compute original before by inverting first and applying to second.before
          const invertedFirst = invertRet(first);
          const originalBefore = applyRet(second.value.before, invertedFirst);
          return variant("replace", { before: originalBefore, after: second.value.after });
        }
      }
    };

    const variantEqual = equalFor(t, ctx.equal);
    const variantPrint = printFor(t, ctx.print);

    // Push compose context first
    ctx.compose.push(composeRet);
    ctx.types.push(t);
    ctx.equal.push(variantEqual);
    ctx.print.push(variantPrint);

    // Build apply/invert handlers using applyFor/invertFor
    applyRet = applyFor(t, { apply: ctx.apply, types: ctx.types, equal: ctx.equal, print: ctx.print });
    invertRet = invertFor(t, { invert: ctx.invert, types: ctx.types, equal: ctx.equal });

    // Push them so .Recursive lookups work during case compose recursion
    ctx.apply.push(applyRet);
    ctx.invert.push(invertRet);

    // Recurse into case types for compose
    for (const { name, type: caseType } of t.value) {
      caseComposes[name] = composeFor(caseType, ctx);
    }

    ctx.compose.pop();
    ctx.apply.pop();
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return composeRet;
  } else if (t.type === "Ref") {
    let innerCompose: (first: any, second: any) => any;
    let applyRet: (base: any, patch: any) => any;
    let invertRet: (patch: any) => any;

    const composeRet = (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else if (first.type === "replace" && second.type === "replace") {
        return variant("replace", { before: first.value.before, after: second.value.after });
      } else if (first.type === "patch" && second.type === "patch") {
        const composed = innerCompose(first.value, second.value);
        if (composed.type === "unchanged") {
          return variant("unchanged", null);
        }
        return variant("patch", composed);
      } else {
        if (first.type === "replace") {
          const afterSecond = applyRet(first.value.after, second);
          return variant("replace", { before: first.value.before, after: afterSecond });
        } else {
          // Compute original before by inverting first and applying to second.before
          const invertedFirst = invertRet(first);
          const originalBefore = applyRet(second.value.before, invertedFirst);
          return variant("replace", { before: originalBefore, after: second.value.after });
        }
      }
    };

    // Build print handler for this ref type
    const refPrint = printFor(t, ctx.print);

    // Build ref equality using equalFor with current context
    const refEqual = equalFor(t, ctx.equal);

    // Push compose context first
    ctx.compose.push(composeRet);
    ctx.types.push(t);
    ctx.equal.push(refEqual);
    ctx.print.push(refPrint);

    // Build Ref apply/invert handlers (these recurse internally with their own push/pop)
    applyRet = applyFor(t, { apply: ctx.apply, types: ctx.types, equal: ctx.equal, print: ctx.print });
    invertRet = invertFor(t, { invert: ctx.invert, types: ctx.types, equal: ctx.equal });

    // Push them so .Recursive lookups work during inner compose recursion
    ctx.apply.push(applyRet);
    ctx.invert.push(invertRet);

    // Recurse into inner type for compose
    innerCompose = composeFor(t.value, ctx);

    ctx.compose.pop();
    ctx.apply.pop();
    ctx.invert.pop();
    ctx.types.pop();
    ctx.equal.pop();
    ctx.print.pop();

    return composeRet;
  } else if (t.type === "Recursive") {
    // Recursive types use replace-only semantics - only unchanged and replace patches
    return (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else if (first.type === "replace" && second.type === "replace") {
        return variant("replace", { before: first.value.before, after: second.value.after });
      } else {
        throw new Error(`Invalid patch types for recursive type composition: ${first.type}, ${second.type}`);
      }
    };
  } else if (t.type === "Function" || t.type === "AsyncFunction") {
    return (first: VariantValue, second: VariantValue) => {
      if (first.type === "unchanged") {
        return second;
      } else if (second.type === "unchanged") {
        return first;
      } else {
        return variant("replace", { before: first.value.before, after: second.value.after });
      }
    };
  } else {
    throw new Error(`Unhandled type in composeFor: ${(t as EastTypeValue).type}`);
  }
}
