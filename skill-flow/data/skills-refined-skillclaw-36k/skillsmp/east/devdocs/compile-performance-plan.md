# East Compiler Performance Optimization Plan

Reference: [compile-performance-design.md](./compile-performance-design.md)

## Phase 1: Type Reference Equality Fast Path

Low risk, high impact. Add `===` checks before structural comparison.

- [ ] **1.1** Add reference equality to `isTypeEqual` in `src/types.ts`
  ```typescript
  if (t1 === t2) return true;
  ```

- [ ] **1.2** Add reference equality to `isTypeValueEqual` in `src/type_of_type.ts`
  - Note: This is generated via `equalFor(EastTypeValueType)` - may need to modify `equalFor` or create a custom implementation

- [ ] **1.3** Add reference equality to `isSubtypeValue` in `src/type_of_type.ts`
  ```typescript
  if (t1 === t2) return true;  // reflexivity
  ```

- [ ] **1.4** Add reference equality to `expandTypeValue` in `src/type_of_type.ts`
  ```typescript
  if (type.type !== "Recursive") return type;  // early exit for non-recursive
  ```

- [ ] **1.5** Benchmark: Run profiler, compare before/after times

## Phase 2: Memoized Type Comparisons

Medium risk. Cache results of expensive comparisons.

- [ ] **2.1** Add WeakMap cache to `isTypeEqual` in `src/types.ts`
  - Use nested WeakMap: `WeakMap<EastType, WeakMap<EastType, boolean>>`
  - EastType objects are suitable WeakMap keys

- [ ] **2.2** Add ID-based cache for `isTypeValueEqual`
  - EastTypeValue are plain objects (variants), need ID assignment
  - Option A: Assign incrementing IDs via WeakMap
  - Option B: Use Map with string key (slower but simpler)

- [ ] **2.3** Add cache to `isSubtypeValue`
  - Similar approach to isTypeValueEqual
  - Note: Result depends on stack arguments, may need to cache only base cases

- [ ] **2.4** Benchmark: Run profiler, compare before/after times

## Phase 3: Reduce Comparison Calls (analyze.ts)

Medium risk. Reduce unnecessary type checks during analysis.

- [ ] **3.1** Audit `analyzeIR` for redundant type comparisons
  - Count actual call sites for `isTypeValueEqual`, `isSubtypeValue`
  - Identify which can be eliminated or short-circuited

- [ ] **3.2** Cache variable type lookups
  - Variable types are looked up repeatedly during analysis
  - Store resolved types in analysis context

- [ ] **3.3** Benchmark

## Phase 4: Reduce Comparison Calls (compile.ts)

Medium risk. Reduce type operations during compilation.

- [ ] **4.1** Audit `compile_internal` for type operations
  - 30 uses of type functions identified
  - Many may be redundant after analysis phase

- [ ] **4.2** Trust analysis results
  - If analysis validates types, compilation shouldn't re-check
  - Remove defensive type checks where analysis guarantees correctness

- [ ] **4.3** Benchmark

## Phase 5: Type Interning (Optional)

Higher risk, more invasive. Ensure unique type objects.

- [ ] **5.1** Design interning strategy
  - Which type representations to intern (EastType vs EastTypeValue)
  - Where to call intern (type construction sites)

- [ ] **5.2** Implement `internType` function
  - Fast hash/key generation
  - Thread-safe if needed (likely not for browser)

- [ ] **5.3** Update type construction sites
  - `toEastTypeValue`
  - `StructType`, `VariantType`, `ArrayType`, etc.
  - Ensure all paths return interned types

- [ ] **5.4** Benchmark

## Benchmarking Protocol

For each phase:

1. Run `npx tsx test-compile-profile-v8.mjs` in `east-ui-vite`
2. Record times for each step:
   - `toIR()`
   - `analyzeIR()`
   - `compile_internal()`
3. Analyze CPU profile for comparison function hits
4. Compare against baseline

### Baseline (Current)

| Step | Time |
|------|------|
| toIR() | 1.5-2.0s |
| analyzeIR() | 1.6-1.7s |
| compile_internal() | 3.4-4.0s |
| **Total** | **~7s** |

### Target

| Step | Time |
|------|------|
| toIR() | <0.5s |
| analyzeIR() | <0.3s |
| compile_internal() | <0.5s |
| **Total** | **<1.5s** |

## Files to Modify

- `src/types.ts` - `isTypeEqual`
- `src/type_of_type.ts` - `isTypeValueEqual`, `isSubtypeValue`, `expandTypeValue`, `toEastTypeValue`
- `src/comparison.ts` - `equalFor` (if modifying generated comparers)
- `src/analyze.ts` - Remove redundant checks
- `src/compile.ts` - Remove redundant checks
