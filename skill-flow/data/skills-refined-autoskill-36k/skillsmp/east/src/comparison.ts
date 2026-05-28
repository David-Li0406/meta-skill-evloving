/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { toEastTypeValue, type EastTypeValue } from "./type_of_type.js";
import type { EastType, ValueTypeOf } from "./types.js";
import { isVariant, variant } from "./containers/variant.js";
import type { ref } from "./containers/ref.js";

/** Stack of comparers for recursive types */
type TypeContext = (((x: any, y: any, ctx?: ValueContext) => boolean))[];

/** Tracks (x,y) pairs previously/currently being compared */
type ValueContext = Map<any, Set<any>>;

export function isFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => boolean
export function isFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => boolean
export function isFor(type: EastTypeValue | EastType, typeCtx: TypeContext = []): (x: any, y: any, ctx?: ValueContext) => boolean {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type as EastType);
  }

  if (type.type === "Never") {
    return (_x: unknown, _y: unknown, _ctx?: ValueContext) => { throw new Error(`Attempted to compare values of type .Never`) };
  } else if (type.type === "Null") {
    return (_x: null, _y: null, _ctx?: ValueContext) => true;
  } else if (type.type === "Boolean") {
    return (x: boolean, y: boolean, _ctx?: ValueContext) => x === y;
  } else if (type.type === "Integer") {
    return (x: bigint, y: bigint, _ctx?: ValueContext) => x === y;
  } else if (type.type === "Float") {
    return (x: number, y: number, _ctx?: ValueContext) => Number.isNaN(x) ? Number.isNaN(y) : x === y; // Note Object.is can fail for different NaN representations
  } else if (type.type === "String") {
    return (x: string, y: string, _ctx?: ValueContext) => x === y;
  } else if (type.type === "DateTime") {
    return (x: Date, y: Date, _ctx?: ValueContext) => x.valueOf() === y.valueOf();
  } else if (type.type === "Blob") {
    // in our type system blobs are immutable (i.e. not reference types), so we must compare by value here
    return (x: Uint8Array, y: Uint8Array, _ctx?: ValueContext) => {
      if (x.length !== y.length) return false;
      for (let i = 0; i < x.length; i++) {
        if (x[i] !== y[i]) return false;
      }
      return true;
    }
  } else if (type.type === "Ref") {
    // mutable types are compared by identity
    return (x: any[], y: any, _ctx?: ValueContext) => Object.is(x, y);
  } else if (type.type === "Array") {
    // mutable types are compared by identity
    return (x: any[], y: any, _ctx?: ValueContext) => Object.is(x, y);
  } else if (type.type === "Set") {
    // mutable types are compared by identity
    return (x: Set<any>, y: any, _ctx?: ValueContext) => Object.is(x, y);
  } else if (type.type === "Dict") {
    // mutable types are compared by identity
    return (x: Map<any, any>, y: any, _ctx?: ValueContext) => Object.is(x, y);
  } else if (type.type === "Struct") {
    // const field_comparers = type.value.map(({ name, type }) => [name, isFor(type, typeCtx)] as const);
    const field_comparers: [string, (x: any, y: any, ctx?: ValueContext) => boolean][] = [];
    const ret = (x: Record<string, any>, y: Record<string, any>, ctx?: ValueContext) => {
      // Fast path: reference equality
      if (x === y) return true;

      for (const [k, comparer] of field_comparers) {
        if (!comparer(x[k], y[k], ctx)) {
          return false;
        }
      }
      return true;
    }
    typeCtx.push(ret);
    for (const field of type.value) {
      field_comparers.push([field.name, isFor(field.type, typeCtx)] as const);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Variant") {
    const case_comparers: Record<string, (x: any, y: any, ctx?: ValueContext) => boolean> = {};
    const ret = (x: variant, y: variant, ctx?: ValueContext) => {
      // Fast path: reference equality
      if (x === y) return true;

      if (x.type !== y.type) return false;
      return case_comparers[x.type]!(x.value, y.value, ctx);
    };
    typeCtx.push(ret);
    for (const { name, type: caseType } of type.value) {
      case_comparers[name] = isFor(caseType, typeCtx);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Recursive") {
    const ret = typeCtx[typeCtx.length - Number(type.value)];
    if (ret === undefined) {
      throw new Error(`Internal error: Recursive type context not found`);
    }
    return ret;
  } else if (type.type === "Function") {
    throw new Error(`Attempted to compare values of type .Function`);
  } else if (type.type === "AsyncFunction") {
    throw new Error(`Attempted to compare values of type .AsyncFunction`);
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  }
}

export function equalFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => boolean
export function equalFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => boolean
export function equalFor(type: EastTypeValue | EastType, typeCtx: TypeContext = []): (x: any, y: any, ctx?: ValueContext) => boolean {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type);
  }

  if (type.type === "Never") {
    return (_x: unknown, _y: unknown, _ctx?: ValueContext) => { throw new Error(`Attempted to compare values of type .Never`) };
  } else if (type.type === "Null") {
    return (_x: null, _y: null, _ctx?: ValueContext) => true;
  } else if (type.type === "Boolean") {
    return (x: boolean, y: boolean, _ctx?: ValueContext) => x === y;
  } else if (type.type === "Integer") {
    return (x: bigint, y: bigint, _ctx?: ValueContext) => x === y;
  } else if (type.type === "Float") {
    return (x: number, y: number, _ctx?: ValueContext) => Number.isNaN(x) ? Number.isNaN(y) : Object.is(x, y);
  } else if (type.type === "String") {
    return (x: string, y: string, _ctx?: ValueContext) => x === y;
  } else if (type.type === "DateTime") {
    return (x: Date, y: Date, _ctx?: ValueContext) => x.valueOf() === y.valueOf();
  } else if (type.type === "Blob") {
    return (x: Uint8Array, y: Uint8Array, _ctx?: ValueContext) => {
      if (x.length !== y.length) return false;
      for (let i = 0; i < x.length; i++) {
        if (x[i] !== y[i]) return false;
      }
      return true;
    }
  } else if (type.type === "Ref") {
    let value_comparer: (x: any, y: any, ctx?: ValueContext) => boolean;
    const ret = (x: ref<any>, y: ref<any>, ctx?: ValueContext) => {
      // Fast path
      if (Object.is(x, y)) return true;

      // Create context if needed (top-level call)
      if (!ctx) {
        ctx = new Map();
      }

      // Check if we've visited this pair
      const xSet = ctx.get(x);
      if (xSet?.has(y)) {
        return true; // Cycle - we're re-encountering this pair
      }

      // Mark as visited
      let visitedSet = ctx.get(x);
      if (!visitedSet) {
        visitedSet = new Set();
        ctx.set(x, visitedSet);
      }
      visitedSet.add(y);

      // Now do the actual comparison
      return value_comparer(x.value, y.value, ctx);
    };
    typeCtx.push(ret);
    value_comparer = equalFor(type.value as EastTypeValue, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Array") {
    let value_comparer: (x: any, y: any, ctx?: ValueContext) => boolean;
    const ret = (x: any[], y: any[], ctx?: ValueContext) => {
      // Fast path
      if (Object.is(x, y)) return true;

      // Create context if needed (top-level call)
      if (!ctx) {
        ctx = new Map();
      }

      // Check if we've visited this pair
      const xSet = ctx.get(x);
      if (xSet?.has(y)) {
        return true; // Cycle - we're re-encountering this pair
      }

      // Mark as visited
      let visitedSet = ctx.get(x);
      if (!visitedSet) {
        visitedSet = new Set();
        ctx.set(x, visitedSet);
      }
      visitedSet.add(y);

      // Now do the actual comparison
      if (x.length !== y.length) return false;
      for (let i = 0; i < x.length; i++) {
        if (!value_comparer(x[i], y[i], ctx)) {
          return false;
        }
      }
      return true;
    };
    typeCtx.push(ret);
    value_comparer = equalFor(type.value as EastTypeValue, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Set") {
    return (x: Set<any>, y: Set<any>, _ctx?: ValueContext) => {
      if (x.size !== y.size) return false;
      for (const xk of x) {
        if (!y.has(xk)) return false;
      }
      return true;
    }
  } else if (type.type === "Dict") {
    let value_comparer: (x: any, y: any, ctx?: ValueContext) => boolean;
    const ret = (x: Map<any, any>, y: any, ctx?: ValueContext) => {
      // Fast path
      if (Object.is(x, y)) return true;

      // Create context if needed (top-level call)
      if (!ctx) {
        ctx = new Map();
      }

      // Check if we've visited this pair
      const xSet = ctx.get(x);
      if (xSet?.has(y)) {
        return true; // Cycle - we're re-encountering this pair
      }

      // Mark as visited
      let visitedSet = ctx.get(x);
      if (!visitedSet) {
        visitedSet = new Set();
        ctx.set(x, visitedSet);
      }
      visitedSet.add(y);

      // Now do the actual comparison
      if (x.size !== y.size) return false;
      for (const [xk, xv] of x) {
        if (!y.has(xk)) return false;
        const yv = y.get(xk);
        if (!value_comparer(xv, yv, ctx)) return false;
      }
      return true;
    }
    typeCtx.push(ret);
    value_comparer = equalFor(type.value.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Struct") {
    const field_comparers: [string, (x: any, y: any, ctx?: ValueContext) => boolean][] = [];
    const ret = (x: Record<string, any>, y: Record<string, any>, ctx?: ValueContext) => {
      // Fast path: reference equality
      if (x === y) return true;

      // Check for cycles (needed for recursive types that can create circular references)
      if (!ctx) {
        ctx = new Map();
      }

      // Check if we've visited this pair
      const xSet = ctx.get(x);
      if (xSet?.has(y)) {
        return true; // Cycle - we're re-encountering this pair
      }

      // Mark as visited
      let visitedSet = ctx.get(x);
      if (!visitedSet) {
        visitedSet = new Set();
        ctx.set(x, visitedSet);
      }
      visitedSet.add(y);

      // Compare fields
      for (const [k, comparer] of field_comparers) {
        if (!comparer(x[k], y[k], ctx)) {
          return false;
        }
      }
      return true;
    }
    typeCtx.push(ret);
    for (const field of type.value) {
      field_comparers.push([field.name, equalFor(field.type, typeCtx)] as const);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Variant") {
    const case_comparers: Record<string, (x: any, y: any, ctx?: ValueContext) => boolean> = {};
    const ret = (x: variant, y: variant, ctx?: ValueContext) => {
      // Fast path: reference equality
      if (x === y) return true;

      if (x.type !== y.type) return false;

      // Check for cycles (needed for recursive types)
      if (!ctx) {
        ctx = new Map();
      }

      const xSet = ctx.get(x);
      if (xSet?.has(y)) {
        return true; // Cycle
      }

      let visitedSet = ctx.get(x);
      if (!visitedSet) {
        visitedSet = new Set();
        ctx.set(x, visitedSet);
      }
      visitedSet.add(y);

      return case_comparers[x.type]!(x.value, y.value, ctx);
    };
    typeCtx.push(ret);
    for (const { name, type: caseType } of type.value) {
      case_comparers[name] = equalFor(caseType, typeCtx);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Recursive") {
    const ret = typeCtx[typeCtx.length - Number(type.value)];
    if (ret === undefined) {
      throw new Error(`Internal error: Recursive type context not found`);
    }
    return ret;
  } else if (type.type === "Function") {
    return (_x: any, _y: any, _ctx?: ValueContext) => {
      return true; // Functions are always considered equal
    }
  } else if (type.type === "AsyncFunction") {
    return (_x: any, _y: any, _ctx?: ValueContext) => {
      return true; // Functions are always considered equal
    }
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  }
}

export function notEqualFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => boolean
export function notEqualFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => boolean
export function notEqualFor(type: EastTypeValue | EastType, typeCtx: TypeContext = []): (x: any, y: any, ctx?: ValueContext) => boolean {
  const equal = equalFor(type as any, typeCtx);
  return (x: any, y: any, ctx?: ValueContext) => !equal(x, y, ctx);

  // // Convert EastType to EastTypeValue if necessary
  // if (!isVariant(type)) {
  //   type = toEastTypeValue(type);
  // }

  // if (type.type === "Never") {
  //   return (_x: unknown, _y: unknown) => { throw new Error(`Attempted to compare values of type .Never`)};
  // } else if (type.type === "Null") {
  //   return (_x: null, _y: null) => false;
  // } else if (type.type === "Boolean") {
  //   return (x: boolean, y: boolean) => x !== y;
  // } else if (type.type === "Integer") {
  //   return (x: bigint, y: bigint) => x !== y;
  // } else if (type.type === "Float") {
  //   return (x: number, y: number) => Number.isNaN(x) ? !Number.isNaN(y) : !Object.is(x, y);
  // } else if (type.type === "String") {
  //   return (x: string, y: string) => x !== y;
  // } else if (type.type === "DateTime") {
  //   return (x: Date, y: Date) => x.valueOf() !== y.valueOf();
  // } else if (type.type === "Blob") {
  //   return (x: Uint8Array, y: Uint8Array) => {
  //     if (x.length !== y.length) return true;
  //     for (let i = 0; i < x.length; i++) {
  //       if (x[i] !== y[i]) return true;
  //     }
  //     return false;
  //   }
  // } else if (type.type === "Array") {
  //   const eq = equalFor(type as EastTypeValue, typeCtx);
  //   return (x: any[], y: any[], ctx?: ValueContext) => !eq(x, y, ctx);
  // } else if (type.type === "Set") {
  //   return (x: Set<any>, y: Set<any>) => {
  //     if (x.size !== y.size) return true;
  //     for (const xk of x) {
  //       if (!y.has(xk)) return true;
  //     }
  //     return false;
  //   }
  // } else if (type.type === "Dict") {
  //   const eq = equalFor(type as EastTypeValue, typeCtx);
  //   return (x: Map<any, any>, y: Map<any, any>, ctx?: ValueContext) => !eq(x, y, ctx);
  // } else if (type.type === "Struct") {
  //   const field_comparers: [string, (x: any, y: any, ctx?: ValueContext) => boolean][] = [];
  //   const ret = (x: Record<string, any>, y: Record<string, any>, ctx?: ValueContext) => {
  //     for (const [k, comparer] of field_comparers) {
  //       if (comparer(x[k], y[k], ctx)) return true;
  //     }
  //     return false;
  //   }
  //   typeCtx.push(ret);
  //   for (const field of type.value) {
  //     field_comparers.push([field.name, notEqualFor(field.type, typeCtx)] as const);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Variant") {
  //   const case_comparers: Record<string, (x: any, y: any, ctx?: ValueContext) => boolean> = {};
  //   const ret = (x: variant, y: variant, ctx?: ValueContext) => {
  //     if (x.type !== y.type) return true;
  //     return case_comparers[x.type]!(x.value, y.value, ctx);
  //   };
  //   typeCtx.push(ret);
  //   for (const { name, type: caseType } of type.value) {
  //     case_comparers[name] = notEqualFor(caseType, typeCtx);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Recursive") {
  //   const ret = typeCtx[typeCtx.length - Number(type.value)];
  //   if (ret === undefined) {
  //     throw new Error(`Internal error: Recursive type context not found`);
  //   }
  //   return ret;
  // } else if (type.type === "Function") {
  //   throw new Error(`Attempted to compare values of type .Function`);
  // } else {
  //   throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  // }
}

export function lessFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => boolean
export function lessFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => boolean
export function lessFor(type: EastTypeValue | EastType, typeCtx: TypeContext = []): (x: any, y: any, ctx?: ValueContext) => boolean {
  const cmp = compareFor(type as any, typeCtx);
  return (x: any, y: any, ctx?: ValueContext) => cmp(x, y, ctx) === -1;

  // // Convert EastType to EastTypeValue if necessary
  // if (!isVariant(type)) {
  //   type = toEastTypeValue(type);
  // }

  // if (type.type === "Never") {
  //   return (_x: unknown, _y: unknown) => { throw new Error(`Attempted to compare values of type .Never`)};
  // } else if (type.type === "Null") {
  //   return (_x: null, _y: null) => false;
  // } else if (type.type === "Boolean") {
  //   return (x: boolean, y: boolean) => x < y;
  // } else if (type.type === "Integer") {
  //   return (x: bigint, y: bigint) => x < y;
  // } else if (type.type === "Float") {
  //   return (x: number, y: number) => {
  //     if (Number.isNaN(y)) return !Number.isNaN(x);
  //     if (Object.is(x, -0) && Object.is(y, 0)) return true;
  //     if (Object.is(x, 0) && Object.is(y, -0)) return false;
  //     return x < y;
  //   };
  // } else if (type.type === "String") {
  //   return (x: string, y: string) => x < y;
  // } else if (type.type === "DateTime") {
  //   return (x: Date, y: Date) => x.valueOf() < y.valueOf();
  // } else if (type.type === "Blob") {
  //   return (x: Uint8Array, y: Uint8Array) => {
  //     const length = x.length < y.length ? x.length : y.length;
  //     for (let i = 0; i < length; i++) {
  //       if (x[i]! < y[i]!) return true;
  //       if (x[i]! > y[i]!) return false;
  //     }
  //     return x.length < y.length;
  //   }
  // } else if (type.type === "Array") {
  //   const cmp = compareFor(type as EastTypeValue, typeCtx);
  //   return (x: any[], y: any[], ctx?: ValueContext) => cmp(x, y, ctx) === -1;
  // } else if (type.type === "Set") {
  //   const key_comparer = compareFor(type.value, []);
  //   return (x: Set<any>, y: Set<any>) => {
  //     // co-iterate the two sets (assume they are sorted)
  //     const yiterator = y.keys();
  //     for (const xk of x) {
  //       const yresult = yiterator.next();
  //       if (yresult.done) return false; // if y runs out first, x is greater than y
  //       const yk = yresult.value;
  //       const c = key_comparer(xk, yk);
  //       if (c !== 0) return c === -1;
  //     }
  //     // x ran out first, check if y has more elements
  //     return !yiterator.next().done;
  //   }
  // } else if (type.type === "Dict") {
  //   const cmp = compareFor(type as EastTypeValue, typeCtx);
  //   return (x: Map<any, any>, y: Map<any, any>, ctx?: ValueContext) => cmp(x, y, ctx) === -1;
  // } else if (type.type === "Struct") {
  //   const field_comparers: [string, (x: any, y: any, ctx?: ValueContext) => boolean][] = [];
  //   const ret = (x: Record<string, any>, y: Record<string, any>, ctx?: ValueContext) => {
  //     for (const [k, comparer] of field_comparers) {
  //       if (comparer(x[k], y[k], ctx)) return true;
  //       if (comparer(y[k], x[k], ctx)) return false;
  //     }
  //     return false;
  //   };
  //   typeCtx.push(ret);
  //   for (const field of type.value) {
  //     field_comparers.push([field.name, lessFor(field.type, typeCtx)] as const);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Variant") {
  //   const case_comparers: Record<string, (x: any, y: any, ctx?: ValueContext) => boolean> = {};
  //   const ret = (x: variant, y: variant, ctx?: ValueContext) => {
  //     if (x.type < y.type) return true;
  //     if (x.type > y.type) return false;
  //     return case_comparers[x.type]!(x.value, y.value, ctx);
  //   };
  //   typeCtx.push(ret);
  //   for (const { name, type: caseType } of type.value) {
  //     case_comparers[name] = lessFor(caseType, typeCtx);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Recursive") {
  //   const ret = typeCtx[typeCtx.length - Number(type.value)];
  //   if (ret === undefined) {
  //     throw new Error(`Internal error: Recursive type context not found`);
  //   }
  //   return ret;
  // } else if (type.type === "Function") {
  //   throw new Error(`Attempted to compare values of type .Function`);
  // } else {
  //   throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  // }
}

export function lessEqualFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => boolean
export function lessEqualFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => boolean
export function lessEqualFor(type: EastTypeValue | EastType, typeCtx: TypeContext = []): (x: any, y: any, ctx?: ValueContext) => boolean {
  const cmp = compareFor(type as any, typeCtx);
  return (x: any, y: any, ctx?: ValueContext) => cmp(x, y, ctx) !== 1;

  // // Convert EastType to EastTypeValue if necessary
  // if (!isVariant(type)) {
  //   type = toEastTypeValue(type);
  // }

  // if (type.type === "Never") {
  //   return (_x: unknown, _y: unknown) => { throw new Error(`Attempted to compare values of type .Never`)};
  // } else if (type.type === "Null") {
  //   return (_x: null, _y: null) => true;
  // } else if (type.type === "Boolean") {
  //   return (x: boolean, y: boolean) => x <= y;
  // } else if (type.type === "Integer") {
  //   return (x: bigint, y: bigint) => x <= y;
  // } else if (type.type === "Float") {
  //   return (x: number, y: number) => Number.isNaN(y) ? true : x <= y;
  // } else if (type.type === "String") {
  //   return (x: string, y: string) => x <= y;
  // } else if (type.type === "DateTime") {
  //   return (x: Date, y: Date) => x.valueOf() <= y.valueOf();
  // } else if (type.type === "Blob") {
  //   return (x: Uint8Array, y: Uint8Array) => {
  //     const length = x.length < y.length ? x.length : y.length;
  //     for (let i = 0; i < length; i++) {
  //       if (x[i]! < y[i]!) return true;
  //       if (x[i]! > y[i]!) return false;
  //     }
  //     return x.length <= y.length;
  //   }
  // } else if (type.type === "Array") {
  //   const cmp = compareFor(type as EastTypeValue, typeCtx);
  //   return (x: any[], y: any[], ctx?: ValueContext) => cmp(x, y, ctx) <= 0;
  // } else if (type.type === "Set") {
  //   const key_comparer = compareFor(type.value, []);
  //   return (x: Set<any>, y: Set<any>) => {
  //     // co-iterate the two sets (assume they are sorted)
  //     const yiterator = y.keys();
  //     for (const xk of x) {
  //       const yresult = yiterator.next();
  //       if (yresult.done) return false; // if y runs out first, x is greater than y
  //       const yk = yresult.value;
  //       const c = key_comparer(xk, yk);
  //       if (c !== 0) return c === -1;
  //     }
  //     // x ran out first, x <= y if y has same size or more elements
  //     return true;
  //   }
  // } else if (type.type === "Dict") {
  //   const cmp = compareFor(type as EastTypeValue, typeCtx);
  //   return (x: Map<any, any>, y: Map<any, any>, ctx?: ValueContext) => cmp(x, y, ctx) <= 0;
  // } else if (type.type === "Struct") {
  //   const field_comparers: [string, (x: any, y: any, ctx?: ValueContext) => boolean][] = [];
  //   const ret = (x: Record<string, any>, y: Record<string, any>, ctx?: ValueContext) => {
  //     for (const [k, comparer] of field_comparers) {
  //       if (comparer(x[k], y[k], ctx)) return true;
  //       if (comparer(y[k], x[k], ctx)) return false;
  //     }
  //     return true;
  //   };
  //   typeCtx.push(ret);
  //   for (const field of type.value) {
  //     field_comparers.push([field.name, lessFor(field.type, typeCtx)] as const);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Variant") {
  //   const case_comparers: Record<string, (x: any, y: any, ctx?: ValueContext) => boolean> = {};
  //   const ret = (x: variant, y: variant, ctx?: ValueContext) => {
  //     if (x.type < y.type) return true;
  //     if (x.type > y.type) return false;
  //     return case_comparers[x.type]!(x.value, y.value, ctx);
  //   };
  //   typeCtx.push(ret);
  //   for (const { name, type: caseType } of type.value) {
  //     case_comparers[name] = lessEqualFor(caseType, typeCtx);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Recursive") {
  //   const ret = typeCtx[typeCtx.length - Number(type.value)];
  //   if (ret === undefined) {
  //     throw new Error(`Internal error: Recursive type context not found`);
  //   }
  //   return ret;
  // } else if (type.type === "Function") {
  //   throw new Error(`Attempted to compare values of type .Function`);
  // } else {
  //   throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  // }
}

export function greaterEqualFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => boolean
export function greaterEqualFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => boolean
export function greaterEqualFor(type: EastTypeValue | EastType, typeCtx: TypeContext = []): (x: any, y: any, ctx?: ValueContext) => boolean {
  const cmp = compareFor(type as any, typeCtx);
  return (x: any, y: any, ctx?: ValueContext) => cmp(x, y, ctx) !== -1;

  // // Convert EastType to EastTypeValue if necessary
  // if (!isVariant(type)) {
  //   type = toEastTypeValue(type);
  // }

  // if (type.type === "Never") {
  //   return (_x: unknown, _y: unknown) => { throw new Error(`Attempted to compare values of type .Never`)};
  // } else if (type.type === "Null") {
  //   return (_x: null, _y: null) => true;
  // } else if (type.type === "Boolean") {
  //   return (x: boolean, y: boolean) => x >= y;
  // } else if (type.type === "Integer") {
  //   return (x: bigint, y: bigint) => x >= y;
  // } else if (type.type === "Float") {
  //   return (x: number, y: number) => Number.isNaN(x) ? true : x >= y;
  // } else if (type.type === "String") {
  //   return (x: string, y: string) => x >= y;
  // } else if (type.type === "DateTime") {
  //   return (x: Date, y: Date) => x.valueOf() >= y.valueOf();
  // } else if (type.type === "Blob") {
  //   return (x: Uint8Array, y: Uint8Array) => {
  //     const length = x.length < y.length ? x.length : y.length;
  //     for (let i = 0; i < length; i++) {
  //       if (x[i]! < y[i]!) return false;
  //       if (x[i]! > y[i]!) return true;
  //     }
  //     return x.length >= y.length;
  //   }
  // } else if (type.type === "Array") {
  //   const cmp = compareFor(type as EastTypeValue, typeCtx);
  //   return (x: any[], y: any[], ctx?: ValueContext) => cmp(x, y, ctx) >= 0;
  // } else if (type.type === "Set") {
  //   const key_comparer = compareFor(type.value, []);
  //   return (x: Set<any>, y: Set<any>) => {
  //     // co-iterate the two sets (assume they are sorted)
  //     const yiterator = y.keys();
  //     for (const xk of x) {
  //       const yresult = yiterator.next();
  //       if (yresult.done) return true; // if y is a prefix of x, x is greater than y
  //       const yk = yresult.value;
  //       const c = key_comparer(xk, yk);
  //       if (c !== 0) return c === 1;
  //     }
  //     // we know x.size >= y.size here
  //     return true;
  //   }
  // } else if (type.type === "Dict") {
  //   const cmp = compareFor(type as EastTypeValue, typeCtx);
  //   return (x: Map<any, any>, y: Map<any, any>, ctx?: ValueContext) => cmp(x, y, ctx) >= 0;
  // } else if (type.type === "Struct") {
  //   const field_comparers: [string, (x: any, y: any, ctx?: ValueContext) => boolean][] = [];
  //   const ret = (x: Record<string, any>, y: Record<string, any>, ctx?: ValueContext) => {
  //     for (const [k, comparer] of field_comparers) {
  //       if (comparer(x[k], y[k], ctx)) return true;
  //       if (comparer(y[k], x[k], ctx)) return false;
  //     }
  //     return true;
  //   };
  //   typeCtx.push(ret);
  //   for (const field of type.value) {
  //     field_comparers.push([field.name, greaterFor(field.type, typeCtx)] as const);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Variant") {
  //   const case_comparers: Record<string, (x: any, y: any, ctx?: ValueContext) => boolean> = {};
  //   const ret = (x: variant, y: variant, ctx?: ValueContext) => {
  //     if (x.type < y.type) return false;
  //     if (x.type > y.type) return true;
  //     return case_comparers[x.type]!(x.value, y.value, ctx);
  //   };
  //   typeCtx.push(ret);
  //   for (const { name, type: caseType } of type.value) {
  //     case_comparers[name] = greaterEqualFor(caseType, typeCtx);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Recursive") {
  //   const ret = typeCtx[typeCtx.length - Number(type.value)];
  //   if (ret === undefined) {
  //     throw new Error(`Internal error: Recursive type context not found`);
  //   }
  //   return ret;
  // } else if (type.type === "Function") {
  //   throw new Error(`Attempted to compare values of type .Function`);
  // } else {
  //   throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  // }
}

export function greaterFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => boolean
export function greaterFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => boolean
export function greaterFor(type: EastTypeValue | EastType, typeCtx: TypeContext = []): (x: any, y: any, ctx?: ValueContext) => boolean {
  const cmp = compareFor(type as any, typeCtx);
  return (x: any, y: any, ctx?: ValueContext) => cmp(x, y, ctx) === 1;

  // // Convert EastType to EastTypeValue if necessary
  // if (!isVariant(type)) {
  //   type = toEastTypeValue(type);
  // }

  // if (type.type === "Never") {
  //   return (_x: unknown, _y: unknown) => { throw new Error(`Attempted to compare values of type .Never`)};
  // } else if (type.type === "Null") {
  //   return (_x: null, _y: null) => false;
  // } else if (type.type === "Boolean") {
  //   return (x: boolean, y: boolean) => x > y;
  // } else if (type.type === "Integer") {
  //   return (x: bigint, y: bigint) => x > y;
  // } else if (type.type === "Float") {
  //   return (x: number, y: number) => Number.isNaN(x) ? !Number.isNaN(y) : x > y;
  // } else if (type.type === "String") {
  //   return (x: string, y: string) => x > y;
  // } else if (type.type === "DateTime") {
  //   return (x: Date, y: Date) => x.valueOf() > y.valueOf();
  // } else if (type.type === "Blob") {
  //   return (x: Uint8Array, y: Uint8Array) => {
  //     const length = x.length < y.length ? x.length : y.length;
  //     for (let i = 0; i < length; i++) {
  //       if (x[i]! < y[i]!) return false;
  //       if (x[i]! > y[i]!) return true;
  //     }
  //     return x.length > y.length;
  //   }
  // } else if (type.type === "Array") {
  //   const cmp = compareFor(type as EastTypeValue, typeCtx);
  //   return (x: any[], y: any[], ctx?: ValueContext) => cmp(x, y, ctx) === 1;
  // } else if (type.type === "Set") {
  //   const key_comparer = compareFor(type.value, []);
  //   return (x: Set<any>, y: Set<any>) => {
  //     // co-iterate the two sets (assume they are sorted)
  //     const yiterator = y.keys();
  //     for (const xk of x) {
  //       const yresult = yiterator.next();
  //       if (yresult.done) return true; // if y is a prefix of x, x is greater than y
  //       const yk = yresult.value;
  //       const c = key_comparer(xk, yk);
  //       if (c !== 0) return c === 1;
  //     }
  //     // we know x.size >= y.size here
  //     return x.size > y.size;
  //   }
  // } else if (type.type === "Dict") {
  //   const cmp = compareFor(type as EastTypeValue, typeCtx);
  //   return (x: Map<any, any>, y: Map<any, any>, ctx?: ValueContext) => cmp(x, y, ctx) === 1;
  // } else if (type.type === "Struct") {
  //   const field_comparers: [string, (x: any, y: any, ctx?: ValueContext) => boolean][] = [];
  //   const ret = (x: Record<string, any>, y: Record<string, any>, ctx?: ValueContext) => {
  //     for (const [k, comparer] of field_comparers) {
  //       if (comparer(x[k], y[k], ctx)) return true;
  //       if (comparer(y[k], x[k], ctx)) return false;
  //     }
  //     return false;
  //   };
  //   typeCtx.push(ret);
  //   for (const field of type.value) {
  //     field_comparers.push([field.name, greaterFor(field.type, typeCtx)] as const);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Variant") {
  //   const case_comparers: Record<string, (x: any, y: any, ctx?: ValueContext) => boolean> = {};
  //   const ret = (x: variant, y: variant, ctx?: ValueContext) => {
  //     if (x.type < y.type) return false;
  //     if (x.type > y.type) return true;
  //     return case_comparers[x.type]!(x.value, y.value, ctx);
  //   };
  //   typeCtx.push(ret);
  //   for (const { name, type: caseType } of type.value) {
  //     case_comparers[name] = greaterFor(caseType, typeCtx);
  //   }
  //   typeCtx.pop();
  //   return ret;
  // } else if (type.type === "Recursive") {
  //   const ret = typeCtx[typeCtx.length - Number(type.value)];
  //   if (ret === undefined) {
  //     throw new Error(`Internal error: Recursive type context not found`);
  //   }
  //   return ret;
  // } else if (type.type === "Function") {
  //   throw new Error(`Attempted to compare values of type .Function`);
  // } else {
  //   throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  // }
}

export function compareFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => 1 | 0 | -1
export function compareFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => 1 | 0 | -1
export function compareFor(type: EastTypeValue | EastType, typeCtx: TypeContext = []): (x: any, y: any, ctx?: ValueContext) => 1 | 0 | -1 {
  // Convert EastType to EastTypeValue if necessary
  if (!isVariant(type)) {
    type = toEastTypeValue(type as EastType);
  }

  if (type.type === "Never") {
    return (_x: unknown, _y: unknown, _ctx?: ValueContext) => { throw new Error(`Attempted to compare values of type .Never`) };
  } else if (type.type === "Null") {
    return (_x: null, _y: null, _ctx?: ValueContext) => 0;
  } else if (type.type === "Boolean") {
    return (x: boolean, y: boolean, _ctx?: ValueContext) => x ? (y ? 0 : 1) : (y ? -1 : 0);
  } else if (type.type === "Integer") {
    return (x: bigint, y: bigint, _ctx?: ValueContext) => x < y ? -1 : (x > y ? 1 : 0);
  } else if (type.type === "Float") {
    return (x: number, y: number, _ctx?: ValueContext) => {
      if (Number.isNaN(x)) return Number.isNaN(y) ? 0 : 1;
      if (Number.isNaN(y)) return -1;
      if (Object.is(x, -0) && Object.is(y, 0)) return -1;
      if (Object.is(x, 0) && Object.is(y, -0)) return 1;
      return x < y ? -1 : (x > y ? 1 : 0);
    };
  } else if (type.type === "String") {
    return (x: string, y: string, _ctx?: ValueContext) => x < y ? -1 : (x > y ? 1 : 0);
  } else if (type.type === "DateTime") {
    return (x: Date, y: Date, _ctx?: ValueContext) => x.valueOf() < y.valueOf() ? -1 : (x.valueOf() > y.valueOf() ? 1 : 0);
  } else if (type.type === "Blob") {
    return (x: Uint8Array, y: Uint8Array, _ctx?: ValueContext) => {
      const length = x.length < y.length ? x.length : y.length;
      for (let i = 0; i < length; i++) {
        if (x[i]! < y[i]!) return -1;
        if (x[i]! > y[i]!) return 1;
      }
      return x.length < y.length ? -1 : (x.length > y.length ? 1 : 0);
    }
  } else if (type.type === "Ref") {
    let value_comparer: (x: any, y: any, ctx?: ValueContext) => 1 | 0 | -1;
    const ret = (x: ref<any>, y: ref<any>, ctx?: ValueContext) => {
      // Fast path
      if (Object.is(x, y)) return 0;

      // Create context if needed (top-level call)
      if (!ctx) {
        ctx = new Map();
      }

      // Check if we've visited this pair
      const xSet = ctx.get(x);
      if (xSet?.has(y)) {
        return 0; // Cycle - we're re-encountering this pair
      }

      // Mark as visited
      let visitedSet = ctx.get(x);
      if (!visitedSet) {
        visitedSet = new Set();
        ctx.set(x, visitedSet);
      }
      visitedSet.add(y);

      // Now do the actual comparison
      return value_comparer(x.value, y.value, ctx);
    };
    typeCtx.push(ret as any);
    value_comparer = compareFor(type.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Array") {
    let value_comparer: (x: any, y: any, ctx?: ValueContext) => 1 | 0 | -1;
    const ret = (x: any[], y: any[], ctx?: ValueContext) => {
      // Fast path
      if (Object.is(x, y)) return 0;

      // Create context if needed (top-level call)
      if (!ctx) {
        ctx = new Map();
      }

      // Check if we've visited this pair
      const xSet = ctx.get(x);
      if (xSet?.has(y)) {
        return 0; // Cycle - we're re-encountering this pair
      }

      // Mark as visited
      let visitedSet = ctx.get(x);
      if (!visitedSet) {
        visitedSet = new Set();
        ctx.set(x, visitedSet);
      }
      visitedSet.add(y);

      // Now do the actual comparison
      const length = x.length < y.length ? x.length : y.length;
      for (let i = 0; i < length; i++) {
        const c = value_comparer(x[i], y[i], ctx);
        if (c !== 0) return c;
      }
      return x.length > y.length ? 1 : x.length < y.length ? -1 : 0;
    };
    typeCtx.push(ret as any);
    value_comparer = compareFor(type.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Set") {
    // Set keys cannot contain mutable containers, so no cycles possible
    const key_comparer = compareFor(type.value, typeCtx);
    return (x: Set<any>, y: Set<any>, _ctx?: ValueContext) => {
      // Fast path
      if (Object.is(x, y)) return 0;

      // co-iterate the two sets (assume they are sorted)
      const yiterator = y.keys();
      for (const xk of x) {
        const yresult = yiterator.next();
        if (yresult.done) return 1; // if y runs out first, x is greater than y
        const yk = yresult.value;
        const c = key_comparer(xk, yk); // keys are standalone, no ctx needed
        if (c !== 0) return c;
      }
      // x ran out first, compare sizes: if y has more elements, x < y
      return yiterator.next().done ? 0 : -1;
    };
  } else if (type.type === "Dict") {
    // Dict keys cannot contain mutable containers, but values can
    const key_comparer = compareFor(type.value.key, typeCtx);
    let value_comparer: (x: any, y: any, ctx?: ValueContext) => 1 | 0 | -1;
    const ret = (x: Map<any, any>, y: Map<any, any>, ctx?: ValueContext) => {
      // Fast path
      if (Object.is(x, y)) return 0;

      // Create context if needed (top-level call)
      if (!ctx) {
        ctx = new Map();
      }

      // Check if we've visited this pair
      const xSet = ctx.get(x);
      if (xSet?.has(y)) {
        return 0; // Cycle - we're re-encountering this pair
      }

      // Mark as visited
      let visitedSet = ctx.get(x);
      if (!visitedSet) {
        visitedSet = new Set();
        ctx.set(x, visitedSet);
      }
      visitedSet.add(y);

      // Now do the actual comparison
      // co-iterate the two maps (assume they are sorted by key)
      const yiterator = y.entries();
      for (const [xk, xv] of x) {
        const yresult = yiterator.next();
        if (yresult.done) return 1; // if y is a prefix of x, x is greater than y
        const [yk, yv] = yresult.value;
        const kc = key_comparer(xk, yk); // keys are standalone, no ctx needed
        if (kc !== 0) return kc;
        const vc = value_comparer(xv, yv, ctx); // values can have cycles
        if (vc !== 0) return vc;
      }
      // x ran out first, compare sizes: if y has more elements, x < y
      return yiterator.next().done ? 0 : -1;
    };
    typeCtx.push(ret as any);
    value_comparer = compareFor(type.value.value, typeCtx);
    typeCtx.pop();
    return ret;
  } else if (type.type === "Struct") {
    const field_comparers: [string, (x: any, y: any, ctx?: ValueContext) => 1 | 0 | -1][] = [];
    const ret = (x: Record<string, any>, y: Record<string, any>, ctx?: ValueContext) => {
      for (const [k, comparer] of field_comparers) {
        const c = comparer(x[k], y[k], ctx);
        if (c !== 0) return c;
      }
      return 0;
    };
    typeCtx.push(ret as any);
    for (const field of type.value) {
      field_comparers.push([field.name, compareFor(field.type, typeCtx)] as const);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Variant") {
    const case_comparers: Record<string, (x: any, y: any, ctx?: ValueContext) => 1 | 0 | -1> = {};
    const ret = (x: variant, y: variant, ctx?: ValueContext) => {
      if (x.type < y.type) return -1;
      if (x.type > y.type) return 1;

      return case_comparers[x.type]!(x.value, y.value, ctx);
    };
    typeCtx.push(ret as any);
    for (const { name, type: caseType } of type.value) {
      case_comparers[name] = compareFor(caseType, typeCtx);
    }
    typeCtx.pop();
    return ret;
  } else if (type.type === "Recursive") {
    const ret = typeCtx[typeCtx.length - Number(type.value)] as any;
    if (ret === undefined) {
      throw new Error(`Internal error: Recursive type context not found`);
    }
    return ret;
  } else if (type.type === "Function") {
    return (_x: any, _y: any, _ctx?: ValueContext | undefined) => {
      return 0; // Functions are always considered equal
    };
  } else if (type.type === "AsyncFunction") {
    return (_x: any, _y: any, _ctx?: ValueContext | undefined) => {
      return 0; // Functions are always considered equal
    };
  } else {
    throw new Error(`Unhandled type ${(type satisfies never as EastTypeValue).type}`);
  }
}