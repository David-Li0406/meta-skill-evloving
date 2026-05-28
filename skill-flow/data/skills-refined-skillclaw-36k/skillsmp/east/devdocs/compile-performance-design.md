# East Compiler Performance Optimization Design

## Problem Statement

Compilation of East IR to JavaScript closures is slow. Profiling shows:

| Step | Time (layout showcase) |
|------|------------------------|
| `toIR()` | ~1.5-2s |
| `analyzeIR()` | ~1.6-1.7s |
| `compile_internal()` | ~3.4-4s |
| **Total** | **~7s** |

For larger showcases, total compilation can exceed 20-30 seconds.

## Profiling Results

Top functions by CPU time (hit count):

| Function | Hits | Location |
|----------|------|----------|
| `ret` (generated comparers) | 2776 | comparison.js |
| `(garbage collector)` | 2287 | native |
| `isTypeEqual` | 1142 | types.js |
| `toEastTypeValue` | 327 | type_of_type.js |
| `expandTypeValue` | 205 | type_of_type.js |
| `isSubtypeValue` | 61 | type_of_type.js |

By file:
- `comparison.js`: 2830 hits
- `types.js`: 1199 hits
- `type_of_type.js`: 676 hits

## Root Causes

### 1. Repeated Type Comparisons Without Caching

The `isTypeEqual`, `isSubtypeValue`, and generated comparers are called thousands of times on the same type pairs. Each call recursively walks the entire type tree.

For a UI component type like:
```typescript
StructType({
  children: ArrayType(VariantType({
    Box: StructType({ ... 20 fields ... }),
    Stack: StructType({ ... 15 fields ... }),
    Text: StructType({ ... 10 fields ... }),
    // ... more variants
  }))
})
```

A single equality check may traverse 100+ type nodes. With 1000+ comparisons during compilation, this becomes O(100,000+) operations.

### 2. Type Identity Not Leveraged

Currently, types are compared by structural equality (deep comparison). However, many types in a program are **the same object reference** - they come from shared type definitions.

```typescript
// These are the same object reference:
const TextType = StructType({ value: StringType, color: StringType });
const t1 = TextType;
const t2 = TextType;

// Current: isTypeEqual does deep structural comparison
// Optimal: t1 === t2 should short-circuit immediately
```

### 3. GC Pressure from Temporary Allocations

2287 GC hits indicate significant memory pressure from:
- `variant()` calls creating wrapper objects
- `Object.create(ctx)` for scope inheritance
- Array/object allocations in type traversal

## Proposed Optimizations

### Optimization 1: Type Reference Equality Fast Path

Add reference equality check before structural comparison:

```typescript
// In types.js - isTypeEqual
export function isTypeEqual(t1: EastType, t2: EastType): boolean {
  // Fast path: same reference
  if (t1 === t2) return true;

  // Existing structural comparison...
}

// In type_of_type.js - isTypeValueEqual
export function isTypeValueEqual(t1: EastTypeValue, t2: EastTypeValue): boolean {
  // Fast path: same reference
  if (t1 === t2) return true;

  // Existing structural comparison...
}

// In type_of_type.js - isSubtypeValue
export function isSubtypeValue(t1: EastTypeValue, t2: EastTypeValue, ...): boolean {
  // Fast path: same reference means subtype (reflexivity)
  if (t1 === t2) return true;

  // Existing structural comparison...
}
```

**Expected impact**: High. Many comparisons in practice are between identical type references. This is a single pointer comparison vs recursive tree walk.

### Optimization 2: Memoized Type Comparisons

Cache comparison results using a WeakMap-based cache:

```typescript
// Cache for isTypeEqual results
const typeEqualCache = new WeakMap<EastType, WeakMap<EastType, boolean>>();

export function isTypeEqual(t1: EastType, t2: EastType): boolean {
  // Fast path: same reference
  if (t1 === t2) return true;

  // Check cache
  let innerCache = typeEqualCache.get(t1);
  if (innerCache) {
    const cached = innerCache.get(t2);
    if (cached !== undefined) return cached;
  }

  // Compute result
  const result = isTypeEqualUncached(t1, t2);

  // Store in cache (both directions for symmetry)
  if (!innerCache) {
    innerCache = new WeakMap();
    typeEqualCache.set(t1, innerCache);
  }
  innerCache.set(t2, result);

  return result;
}
```

**For EastTypeValue comparisons** (which are plain objects, not suitable for WeakMap keys), use a Map with a composite key or consider interning.

```typescript
// Option A: String key (slower but works)
const typeValueEqualCache = new Map<string, boolean>();

function getCacheKey(t1: EastTypeValue, t2: EastTypeValue): string {
  // Use object identity via a WeakMap-assigned ID
  return `${getTypeId(t1)}:${getTypeId(t2)}`;
}

// Option B: Type interning (better long-term)
// Ensure each unique type structure has exactly one canonical object
// Then use WeakMap with the canonical objects
```

**Expected impact**: Medium-High. After first comparison of a type pair, subsequent comparisons are O(1) lookup.

### Optimization 3: Type Interning (Advanced)

Ensure each unique type has exactly one object instance:

```typescript
const typeInternPool = new Map<string, EastTypeValue>();

export function internType(type: EastTypeValue): EastTypeValue {
  const key = printTypeValue(type); // or a faster serialization
  const existing = typeInternPool.get(key);
  if (existing) return existing;

  typeInternPool.set(key, type);
  return type;
}

// In toEastTypeValue, analyzeIR, etc:
// Always return interned types
return internType(variant("Struct", fields));
```

**Benefits**:
- All type comparisons become reference equality
- WeakMap caching works naturally
- Reduced memory (shared type objects)

**Drawbacks**:
- Serialization overhead on type creation
- Need to ensure all type creation paths go through interning

**Expected impact**: High if implemented comprehensively.

### Optimization 4: Lazy/Incremental Compilation (Future)

Instead of compiling entire IR tree upfront, compile on-demand:

```typescript
// Return a lazy wrapper that compiles on first call
function compileLazy(ir: AnalyzedIR, ctx, platform, asyncPlatformFns) {
  let compiled: ((ctx: Record<string, any>) => any) | null = null;

  return (ctx: Record<string, any>) => {
    if (!compiled) {
      compiled = compile_internal(ir, ctx, platform, asyncPlatformFns);
    }
    return compiled(ctx);
  };
}
```

This is more complex and may not help if all code paths are exercised, but could help for large programs where only some branches are used.

## Implementation Priority

1. **Type Reference Equality** - Lowest risk, highest impact, trivial to implement
2. **Memoized Type Comparisons** - Medium risk, high impact
3. **Type Interning** - Higher risk, requires more changes, but best long-term solution

## Measuring Success

Before and after each optimization, measure:
- Total compilation time for layout showcase
- Hit counts for comparison functions (via profiling)
- GC time/pressure

Target: Reduce compilation time from ~7s to <1s for layout showcase.
