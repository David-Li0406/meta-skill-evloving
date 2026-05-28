# Function Captures Serialization Design

This document describes the design for extending BEAST2 serialization to support functions with captures (closures).

## Table of Contents

1. [Background](#background)
2. [Current Implementation](#current-implementation)
3. [Problem Statement](#problem-statement)
4. [Proposed Design](#proposed-design)
5. [Implementation Plan](#implementation-plan)
6. [Wire Format](#wire-format)
7. [Edge Cases](#edge-cases)

---

## Background

East functions can capture variables from their enclosing scope, creating closures. For example:

```typescript
const makeAdder = East.function([IntegerType], FunctionType([IntegerType], IntegerType), ($, x) => {
  return $.function([IntegerType], IntegerType, ($, y) => {
    return x.add(y);  // captures 'x' from outer scope
  });
});
```

The inner function captures `x`. When compiled, this creates a JavaScript closure where `x` is stored in the closure's environment.

### Key Concepts

- **East function**: Always IR (the `FunctionIR` node is the value) unless compiled to JavaScript
- **Compiled function**: A JavaScript function produced by `compile()`, with IR attached via `EAST_IR_SYMBOL`
- **Captures**: Variables referenced from an enclosing scope, stored in `FunctionIR.captures` as `VariableIR[]` (names + types, not values)
- **Capture values**: Runtime values extracted from the execution context when the function is instantiated

---

## Current Implementation

### IR Structure (`src/ir.ts:84-98`)

```typescript
export type FunctionIR = variant<"Function", {
  type: EastTypeValue,
  location: LocationValue,
  captures: VariableIR[],      // Variable references (name + type)
  parameters: VariableIR[],
  body: any,
}>;

export type VariableIR = variant<"Variable", {
  type: EastTypeValue,
  name: string,
  location: LocationValue,
  mutable: boolean,
  captured: boolean,
}>;
```

### Compilation (`src/compile.ts:275-302`)

When a function is compiled, capture values are extracted from the execution context:

```typescript
const capture_names = ir.value.captures.map(v => v.value.name);
const parameter_names = ir.value.parameters.map(v => v.value.name);
const originalIR = ir;

return (ctx: Record<string, any>) => {
  const ctx2: Record<string, any> = {};
  for (const name of capture_names) {
    ctx2[name] = ctx[name];  // Extract capture VALUES from context
  }

  const fn = (...args: any) => {
    const ctx3 = { ...ctx2 };
    parameter_names.forEach((name, i) => ctx3[name] = args[i]);
    return compiled_body(ctx3);
  };

  // Only IR is attached, not capture values
  Object.defineProperty(fn, EAST_IR_SYMBOL, {
    value: originalIR,
    writable: false,
    enumerable: false,
    configurable: false
  });

  return fn;
}
```

### Current Serialization (`src/serialization/beast2.ts:207-229`)

Functions with captures are explicitly rejected:

```typescript
} else if (type.type === "Function") {
  return (value: any, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
    const ir = value[EAST_IR_SYMBOL] as FunctionIR | undefined;

    if (!ir) {
      throw new Error(
        `Cannot serialize function: no IR attached. ` +
        `Functions must be compiled from East IR to be serializable.`
      );
    }

    if (ir.value.captures.length > 0) {
      throw new Error(
        `Cannot serialize closure with ${ir.value.captures.length} captured variable(s): ` +
        `${ir.value.captures.map((v: any) => v.value.name).join(", ")}. ` +
        `Only free functions (no captures) can be serialized.`
      );
    }

    irEncoder(ir, writer, ctx);
  };
}
```

### Current Deserialization (`src/serialization/beast2.ts:449-477`)

Decoded functions are compiled with an empty context:

```typescript
} else if (type.type === "Function") {
  return (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
    const [ir, newOffset] = irDecoder(buffer, offset, ctx);

    if (ir.type !== "Function") {
      throw new Error(`Expected Function IR, got ${ir.type} at offset ${offset}`);
    }

    let fn: any;
    try {
      const analyzedIR = analyzeIR(ir, platform, {});
      const compiled = compile_internal(analyzedIR, {}, platformFns, asyncPlatformFns, platform, true, new Set());
      fn = compiled({});  // Empty context - captures would be undefined!
    } catch (e: unknown) {
      throw new Error(`Failed to compile decoded function: ${(e as Error).message}`);
    }

    return [fn, newOffset];
  };
}
```

---

## Problem Statement

The current implementation cannot serialize closures because:

1. **Missing capture values**: Only `EAST_IR_SYMBOL` (the IR) is stored on compiled functions. The capture *values* exist only in the JavaScript closure, not accessible for serialization.

2. **Empty context on decode**: `compiled({})` passes an empty context, so captured variables would be `undefined`.

However, closures are useful and commonly needed. The restriction should be lifted.

---

## Proposed Design

### Overview

1. Store capture values alongside IR on compiled functions using a new `EAST_CAPTURES_SYMBOL`
2. Serialize capture values after the IR using their types from `VariableIR.type`
3. Deserialize capture values and pass them as context when compiling

### Key Insight

BEAST2 already tracks value references via `Beast2EncodeContext.refs` for aliasing/circular reference support. When serializing a struct containing both a captured variable and a closure that captures it, BEAST2's reference mechanism will automatically handle identity preservation:

```typescript
// If serializing: { arr: someArray, f: closureThatCapturesArr }
// 1. Serialize arr -> stored at offset X in refs
// 2. Serialize f -> serialize f's capture values -> arr emits back-reference to X
// 3. On decode, arr and f's captured arr resolve to same instance
```

---

## Implementation Plan

### Phase 1: Add `EAST_CAPTURES_SYMBOL` to compile.ts

**File**: `src/compile.ts`

**Change 1**: Add new symbol (after line 35)

```typescript
/**
 * Symbol used to attach source IR to compiled functions.
 * This enables serialization of free functions (functions with no captures).
 */
export const EAST_IR_SYMBOL = Symbol.for("east.ir");

/**
 * Symbol used to attach capture values to compiled functions.
 * This enables serialization of closures (functions with captures).
 */
export const EAST_CAPTURES_SYMBOL = Symbol.for("east.captures");
```

**Change 2**: Store capture context on compiled functions (modify lines 293-300)

```typescript
const fn = (...args: any) => {
  const ctx3 = { ...ctx2 };
  parameter_names.forEach((name, i) => ctx3[name] = args[i]);
  return compiled_body(ctx3);
};

// Attach IR to function for serialization support
Object.defineProperty(fn, EAST_IR_SYMBOL, {
  value: originalIR,
  writable: false,
  enumerable: false,
  configurable: false
});

// Attach capture values for serialization support
Object.defineProperty(fn, EAST_CAPTURES_SYMBOL, {
  value: ctx2,  // The capture context with actual values
  writable: false,
  enumerable: false,
  configurable: false
});

return fn;
```

**Change 3**: Apply same change to AsyncFunction compilation (lines 333-340)

### Phase 2: Update BEAST2 Encoder

**File**: `src/serialization/beast2.ts`

**Change 1**: Import new symbol (line 19)

```typescript
import { EAST_IR_SYMBOL, EAST_CAPTURES_SYMBOL, compile_internal } from "../compile.js";
```

**Change 2**: Replace Function encoder (lines 207-229)

```typescript
} else if (type.type === "Function") {
  return (value: any, writer: BufferWriter, ctx: Beast2EncodeContext = { refs: new Map() }) => {
    const ir = value[EAST_IR_SYMBOL] as FunctionIR | undefined;

    if (!ir) {
      throw new Error(
        `Cannot serialize function: no IR attached. ` +
        `Functions must be compiled from East IR to be serializable.`
      );
    }

    // Serialize the IR
    irEncoder(ir, writer, ctx);

    // Serialize capture values
    const captures = value[EAST_CAPTURES_SYMBOL] as Record<string, any> | undefined;
    const captureCount = ir.value.captures.length;

    // Write number of captures (for validation on decode)
    writer.writeVarint(captureCount);

    // Serialize each capture value using its type from the IR
    for (const captureVar of ir.value.captures) {
      const name = captureVar.value.name;
      const captureType = captureVar.value.type;
      const captureValue = captures?.[name];

      // Get encoder for this capture's type and encode the value
      const captureEncoder = encodeBeast2ValueToBufferFor(captureType, typeCtx);
      captureEncoder(captureValue, writer, ctx);
    }
  };
}
```

**Change 3**: Apply same change to AsyncFunction encoder (lines 230-252)

### Phase 3: Update BEAST2 Decoder

**File**: `src/serialization/beast2.ts`

**Change 1**: Replace Function decoder (lines 449-477)

```typescript
} else if (type.type === "Function") {
  const platform = options?.platform ?? [];
  const platformFns = Object.fromEntries(platform.map(fn => [fn.name, fn.fn]));
  const asyncPlatformFns = new Set(platform.filter(fn => fn.type === 'async').map(fn => fn.name));

  return (buffer: Uint8Array, offset: number, ctx: Beast2DecodeContext = { refs: new Map() }): [any, number] => {
    // Decode the IR
    const [ir, newOffset] = irDecoder(buffer, offset, ctx);
    let currentOffset = newOffset;

    if (ir.type !== "Function") {
      throw new Error(`Expected Function IR, got ${ir.type} at offset ${offset}`);
    }

    // Decode capture count (for validation)
    const [captureCount, offsetAfterCount] = readVarint(buffer, currentOffset);
    currentOffset = offsetAfterCount;

    if (captureCount !== ir.value.captures.length) {
      throw new Error(
        `Capture count mismatch: IR has ${ir.value.captures.length} captures, ` +
        `but serialized data has ${captureCount}`
      );
    }

    // Decode capture values
    const captureContext: Record<string, any> = {};
    for (const captureVar of ir.value.captures) {
      const name = captureVar.value.name;
      const captureType = captureVar.value.type;

      // Get decoder for this capture's type and decode the value
      const captureDecoder = decodeBeast2ValueFor(captureType, typeCtx, options);
      const [captureValue, nextOffset] = captureDecoder(buffer, currentOffset, ctx);
      currentOffset = nextOffset;

      captureContext[name] = captureValue;
    }

    // Compile with capture context
    let fn: any;
    try {
      const analyzedIR = analyzeIR(ir, platform, {});
      const compiled = compile_internal(analyzedIR, {}, platformFns, asyncPlatformFns, platform, true, new Set());
      fn = compiled(captureContext);  // Pass capture values!
    } catch (e: unknown) {
      throw new Error(`Failed to compile decoded function: ${(e as Error).message}`);
    }

    return [fn, currentOffset];
  };
}
```

**Change 2**: Apply same change to AsyncFunction decoder (lines 478-506)

### Phase 4: Export New Symbol

**File**: `src/serialization/beast2.ts`

**Change**: Update exports (around line 657)

```typescript
export { EAST_IR_SYMBOL, EAST_CAPTURES_SYMBOL } from "../compile.js";
```

**File**: `src/serialization/index.ts`

**Change**: Update exports (line 8)

```typescript
export { encodeBeast2For, decodeBeast2For, decodeBeast2, compileFunctionIR, compileAsyncFunctionIR, EAST_IR_SYMBOL, EAST_CAPTURES_SYMBOL } from "./beast2.js";
```

### Phase 5: Update Streaming API (if needed)

**File**: `src/serialization/beast2-stream.ts`

The streaming API currently throws for Function types (lines 662-665). This should be updated to match the changes above, or at minimum update the error message to reflect that the limitation is in the streaming API, not BEAST2 generally.

---

## Wire Format

### Current Format (Free Functions)

```
[IR encoded as IRType variant]
```

### New Format (Functions with Captures)

```
[IR encoded as IRType variant]
[varint: capture count]
[capture value 0 encoded using VariableIR[0].type]
[capture value 1 encoded using VariableIR[1].type]
...
[capture value N-1 encoded using VariableIR[N-1].type]
```

For free functions (no captures), the capture count is 0 and no values follow.

### Backward Compatibility

This is a **breaking change** to the wire format. Existing serialized functions (with 0 captures) will not have the capture count varint. Options:

1. **Version bump**: Require BEAST v3 for functions with captures
2. **Magic byte**: Add a marker byte to distinguish old vs new format
3. **Accept breakage**: Since functions with captures couldn't be serialized before, there's no existing data to migrate

Recommendation: Option 3 - there's no existing serialized closure data since it was forbidden.

---

## Edge Cases

### Mutable Captures

If a capture is a mutable type (Array, Set, Dict), the serialized value is a snapshot. After deserialization:
- The function has its own copy of the mutable value
- If the same value appears elsewhere in the serialized structure, BEAST2's reference mechanism ensures they share identity

### Nested Closures

A closure capturing another closure works naturally:
- Outer closure is a value (compiled function with its own captures)
- Serializing it serializes its IR + capture values
- If a capture value is itself a closure, that gets serialized recursively

### Captures of Function Type

If a closure captures a function:
1. The capture's type is `FunctionType`
2. The capture's value is a compiled function
3. Serialization encodes that function (its IR + its captures)
4. BEAST2 references handle identity if the same function appears multiple times

---

## Testing

### Unit Tests to Add (`test/function.spec.ts`)

1. **Basic closure serialization**
   ```typescript
   test("closure with integer capture", $ => {
     const x = $.let(42n);
     const f = $.let($.function([], IntegerType, ($) => x));
     const blob = $.let(East.Blob.encodeBeast(f, 'v2'));
     const decoded = $.let(blob.decodeBeast(FunctionType([], IntegerType), 'v2'));
     $(assert.equal(decoded(), 42n));
   });
   ```

2. **Closure with mutable capture**
   ```typescript
   test("closure with array capture", $ => {
     const arr = $.let(East.array([1n, 2n, 3n]));
     const f = $.let($.function([], IntegerType, ($) => arr.length()));
     const blob = $.let(East.Blob.encodeBeast(f, 'v2'));
     const decoded = $.let(blob.decodeBeast(FunctionType([], IntegerType), 'v2'));
     $(assert.equal(decoded(), 3n));
   });
   ```

3. **Shared identity between struct field and closure capture**
   ```typescript
   test("closure capture shares identity with struct field", $ => {
     const arr = $.let(East.array([1n, 2n]));
     const f = $.let($.function([IntegerType], NullType, ($, val) => {
       $(arr.push(val));
     }));
     const data = $.let(East.struct({ arr, f }));
     const DataType = StructType({ arr: ArrayType(IntegerType), f: FunctionType([IntegerType], NullType) });
     const blob = $.let(East.Blob.encodeBeast(data, 'v2'));
     const decoded = $.let(blob.decodeBeast(DataType, 'v2'));
     $(decoded.f(3n));  // Push via decoded function
     $(assert.equal(decoded.arr.length(), 3n));  // Array updated
   });
   ```

4. **Nested closures**
   ```typescript
   test("nested closures serialize correctly", $ => {
     const makeAdder = $.let($.function([IntegerType], FunctionType([IntegerType], IntegerType), ($, x) => {
       return $.function([IntegerType], IntegerType, ($, y) => x.add(y));
     }));
     const add5 = $.let(makeAdder(5n));
     const blob = $.let(East.Blob.encodeBeast(add5, 'v2'));
     const decoded = $.let(blob.decodeBeast(FunctionType([IntegerType], IntegerType), 'v2'));
     $(assert.equal(decoded(3n), 8n));
   });
   ```

---

## Summary of Changes

| File | Change |
|------|--------|
| `src/compile.ts:35` | Add `EAST_CAPTURES_SYMBOL` |
| `src/compile.ts:293-300` | Attach capture context to Function |
| `src/compile.ts:333-340` | Attach capture context to AsyncFunction |
| `src/serialization/beast2.ts:19` | Import `EAST_CAPTURES_SYMBOL` |
| `src/serialization/beast2.ts:207-229` | Encode captures after IR |
| `src/serialization/beast2.ts:230-252` | Encode captures for AsyncFunction |
| `src/serialization/beast2.ts:449-477` | Decode captures and pass to compiler |
| `src/serialization/beast2.ts:478-506` | Decode captures for AsyncFunction |
| `src/serialization/beast2.ts:657` | Export `EAST_CAPTURES_SYMBOL` |
| `src/serialization/index.ts:8` | Export `EAST_CAPTURES_SYMBOL` |
| `src/serialization/beast2-stream.ts` | Update or document limitation |
| `test/function.spec.ts` | Add closure serialization tests |
