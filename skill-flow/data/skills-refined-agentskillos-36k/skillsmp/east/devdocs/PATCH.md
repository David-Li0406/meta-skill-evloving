# Patch System Design

This document describes the design for a patch/diff system in East, enabling efficient representation of changes between values.

## Overview

The patch system provides four core operations for any East type:

1. **`diffFor(type)`** - Compute the difference between two values → returns a patch
2. **`applyFor(type)`** - Apply a patch to a value → returns the patched value
3. **`composeFor(type)`** - Combine two sequential patches → returns a single patch
4. **`invertFor(type)`** - Invert a patch → returns the reverse patch

These operations satisfy important algebraic properties:
- `apply(before, diff(before, after)) = after`
- `apply(after, invert(diff(before, after))) = before`
- `compose(diff(a, b), diff(b, c)) = diff(a, c)`
- `compose(patch, invert(patch)) = unchanged`

## Patch Representation

Every patch is a **variant type** with three possible cases:

```typescript
PatchType<T> = VariantType<{
  unchanged: NullType,              // No changes
  replace: StructType<{             // Complete replacement
    before: T,
    after: T
  }>,
  patch: <type-specific>            // Structural patch (for compound types)
}>
```

The `patch` case is only available for compound types (Dict, Set, Array, Struct, Variant). Primitive types only support `unchanged` or `replace`.

## Type-Specific Patch Structures

### Primitive Types

**NullType, BooleanType, IntegerType, FloatType, StringType, DateTimeType, BlobType**

Primitives only support `unchanged` or `replace`:

```typescript
PatchType<PrimitiveType> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: T, after: T }>
}>
```

### DictType

Dict patches track insertions, deletions, and updates by key:

```typescript
PatchType<DictType<K, V>> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: DictType<K, V>, after: DictType<K, V> }>,
  patch: DictType<K, VariantType<{
    delete: V,           // Key removed, stores deleted value for verification
    insert: V,           // Key added, stores new value
    update: PatchType<V> // Value changed, stores nested patch
  }>>
}>
```

**Semantics:**
- `delete`: Removes a key. Stores the deleted value to detect conflicts.
- `insert`: Adds a new key. Fails if key already exists.
- `update`: Recursively patches the value at an existing key.

### SetType

Set patches are simpler since there are no values to update:

```typescript
PatchType<SetType<K>> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: SetType<K>, after: SetType<K> }>,
  patch: DictType<K, VariantType<{
    delete: NullType,    // Key removed
    insert: NullType     // Key added
  }>>
}>
```

### ArrayType

Array patches are the most complex, tracking position changes:

```typescript
PatchType<ArrayType<T>> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: ArrayType<T>, after: ArrayType<T> }>,
  patch: ArrayType<StructType<{
    key: IntegerType,      // Position in the new array
    offset: IntegerType,   // Offset to find position in old array (old_key = key + offset)
    operation: VariantType<{
      delete: T,           // Element removed at this position
      insert: T,           // Element inserted at this position
      update: PatchType<T> // Element updated at this position
    }>
  }>>
}>
```

**Offset Semantics:**
- `key` is the position in the **new** (after) array
- `offset` tracks cumulative position shifts from prior operations
- `old_key = key + offset` maps to position in the intermediate array during apply
- Deletions increment offset, insertions decrement it
- Patches are naturally generated in `(key, offset)` order; no post-sort needed

**Worked Example:**

```
before: ["a", "b", "c", "d"]
after:  ["x", "b", "d", "y"]

LCS: ["b", "d"]
  beforeIndices: [1, 3]
  afterIndices:  [1, 2]

Generated operations (in order):
  1. { key: 0, offset: 0, op: .delete "a" }  // delete before[0]
  2. { key: 0, offset: 1, op: .insert "x" }  // insert at position 0
  3. { key: 2, offset: 0, op: .delete "c" }  // delete before[2] (now at pos 2)
  4. { key: 3, offset: 1, op: .insert "y" }  // insert at position 3

Apply trace:
  Start:    ["a", "b", "c", "d"]
  After 1:  ["b", "c", "d"]          // deleted "a" at 0+0=0
  After 2:  ["x", "b", "c", "d"]     // inserted "x" at 0
  After 3:  ["x", "b", "d"]          // deleted "c" at 2+0=2
  After 4:  ["x", "b", "d", "y"]     // inserted "y" at 3
```

See [Array Diff Algorithm](#array-diff-algorithm) section for the recommended LCS-based implementation.

### StructType

Struct patches contain a patch for each field:

```typescript
PatchType<StructType<{ f1: T1, f2: T2, ... }>> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: T, after: T }>,
  patch: StructType<{
    f1: PatchType<T1>,
    f2: PatchType<T2>,
    ...
  }>
}>
```

**Semantics:**
- A struct patch is `.unchanged` only if all field patches are `.unchanged`
- The `.patch` case includes **all fields**, even those that are `.unchanged`
- This simplifies type construction (patch type mirrors struct type) at cost of some redundancy
- Alternative: sparse representation using `Dict<String, PatchType<...>>` (more complex, saves space)

### VariantType

Variant patches handle same-case updates vs case changes:

```typescript
PatchType<VariantType<{ c1: T1, c2: T2, ... }>> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: T, after: T }>,
  patch: VariantType<{
    c1: PatchType<T1>,
    c2: PatchType<T2>,
    ...
  }>
}>
```

**Semantics:**
- If both values have the same case: recursively patch the case data
- If values have different cases: use `replace`

### RecursiveType

**Decision: Replace-only semantics**

RecursiveType uses only `unchanged` or `replace`, no structural patching:

```typescript
PatchType<RecursiveType<T>> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: T, after: T }>
}>
```

**Rationale:**
1. Recursive structures can be arbitrarily deep (trees, DAGs, circular references)
2. Structural patching requires lazy type construction to avoid infinite recursion
3. `replace` is simple, correct, and often the appropriate choice for tree updates
4. Structural patching can be added later as an optimization if needed

**Future Enhancement:**
If granular tree diffs become important, structural patching could be added. This would require careful handling of the recursive type definition to avoid infinite types at the TypeScript level. For now, replace-only is simpler and sufficient.

### FunctionType / AsyncFunctionType

Functions use replace-only semantics (cannot be structurally patched):

```typescript
PatchType<FunctionType<I, O>> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: T, after: T }>
}>
```

### RefType

Ref (mutable reference cell) patches the inner value structurally:

```typescript
PatchType<RefType<T>> = VariantType<{
  unchanged: NullType,
  replace: StructType<{ before: RefType<T>, after: RefType<T> }>,
  patch: PatchType<T>  // Patch to inner value
}>
```

**Semantics:**
- If refs are identical (same object): `.unchanged`
- If inner values are equal: `.unchanged`
- If inner values differ: `.patch` with nested patch for inner value
- Note: `apply` creates a new ref, it does not mutate the original

### NeverType

Never has no values, so diff/apply/compose/invert all throw at runtime:

```typescript
PatchType<NeverType> = NeverType  // No patch can exist
```

Attempting to diff/apply values of type Never throws `EastError`.

## API Design

### Architecture Overview

The patch system follows the same pattern as comparisons (`equal`, `less`, etc.):

1. **Builtins** defined in `src/builtins.ts` - Type signatures for IR validation
2. **Value-level `*For` functions** in `src/patch.ts` - Runtime implementations
3. **Expression builders** in `src/expr/block.ts` - Create AST nodes for use in East functions
4. **Compiler integration** in `src/compile.ts` - `builtin_evaluators` map builtins to `*For` functions

### Builtins (src/builtins.ts)

Add to `BuiltinName` type and `Builtins` record:

```typescript
// Add to BuiltinName union:
| "Diff" | "ApplyPatch" | "ComposePatch" | "InvertPatch"

// Add to Builtins record:
Diff: {
  type_parameters: ["T"],
  inputs: ["T", "T"] as const,
  output: PatchType("T"),  // Returns computed patch type
},
ApplyPatch: {
  type_parameters: ["T"],
  inputs: ["T", PatchType("T")] as const,
  output: "T",
},
ComposePatch: {
  type_parameters: ["T"],
  inputs: [PatchType("T"), PatchType("T")] as const,
  output: PatchType("T"),
},
InvertPatch: {
  type_parameters: ["T"],
  inputs: [PatchType("T")] as const,
  output: PatchType("T"),
},
```

**Note**: `PatchType` needs to work with the type parameter system. The `applyTypeParameters` function in `builtins.ts` must handle `PatchType` similar to how it handles `ArrayType`, `DictType`, etc.

### Value-Level API (src/patch.ts)

These implement the actual runtime behavior, following the pattern of `comparison.ts`:

```typescript
/**
 * Create a diff function for a given type.
 */
export function diffFor<T extends EastType>(type: T):
  (before: ValueTypeOf<T>, after: ValueTypeOf<T>) => ValueTypeOf<PatchType<T>>

/**
 * Create an apply function for a given type.
 * @throws EastError if patch conflicts with base value
 */
export function applyFor<T extends EastType>(type: T):
  (base: ValueTypeOf<T>, patch: ValueTypeOf<PatchType<T>>) => ValueTypeOf<T>

/**
 * Create a compose function for a given type.
 * @throws EastError if patches are incompatible
 */
export function composeFor<T extends EastType>(type: T):
  (first: ValueTypeOf<PatchType<T>>, second: ValueTypeOf<PatchType<T>>) => ValueTypeOf<PatchType<T>>

/**
 * Create an invert function for a given type.
 */
export function invertFor<T extends EastType>(type: T):
  (patch: ValueTypeOf<PatchType<T>>) => ValueTypeOf<PatchType<T>>
```

### Compiler Integration (src/compile.ts)

Add to `builtin_evaluators`:

```typescript
Diff: (_location: LocationValue, _platformDef: PlatformFunction[], T: EastTypeValue) => diffFor(T),
ApplyPatch: (_location: LocationValue, _platformDef: PlatformFunction[], T: EastTypeValue) => applyFor(T),
ComposePatch: (_location: LocationValue, _platformDef: PlatformFunction[], T: EastTypeValue) => composeFor(T),
InvertPatch: (_location: LocationValue, _platformDef: PlatformFunction[], T: EastTypeValue) => invertFor(T),
```

### Expression Builders (src/expr/block.ts)

Add functions that create AST nodes, following the pattern of `equal()`, `less()`, etc.:

```typescript
/**
 * Compute the difference between two values.
 */
export function diff<T>(before: Expr<T>, after: SubtypeExprOrValue<NoInfer<T>>): VariantExpr<PatchCases<T>> {
  const afterAst = valueOrExprToAstTyped(after, Expr.type(before) as any);
  const valueType = Expr.type(before) as EastType;
  return fromAst({
    ast_type: "Builtin",
    type: PatchType(valueType),
    location: get_location(2),
    builtin: "Diff",
    type_parameters: [valueType],
    arguments: [Expr.ast(before), afterAst],
  }) as VariantExpr<PatchCases<T>>;
}

/**
 * Apply a patch to a base value.
 */
export function applyPatch<T>(base: Expr<T>, patch: Expr<PatchType<T>>): Expr<T> {
  const valueType = Expr.type(base) as EastType;
  return fromAst({
    ast_type: "Builtin",
    type: valueType,
    location: get_location(2),
    builtin: "ApplyPatch",
    type_parameters: [valueType],
    arguments: [Expr.ast(base), Expr.ast(patch)],
  }) as Expr<T>;
}

// etc. for composePatch, invertPatch
```

### East Namespace Bindings

Add to `East` object in `src/expr/index.ts`:

```typescript
export const East = {
  // ... existing
  diff,
  applyPatch,    // Note: NOT "patch" to avoid confusion with the noun
  composePatch,
  invertPatch,
};
```

### Instance Methods (Optional)

For consistency with other operations like `equals()`, consider adding instance methods on `Expr`:

```typescript
// On Expr<T>
expr.diff(other: SubtypeExprOrValue<T>): VariantExpr<PatchCases<T>>

// On VariantExpr<PatchCases<T>> (patch expressions)
patchExpr.apply(base: Expr<T>): Expr<T>
patchExpr.compose(other: VariantExpr<PatchCases<T>>): VariantExpr<PatchCases<T>>
patchExpr.invert(): VariantExpr<PatchCases<T>>
```

**Decision:** Start with static `East.*` functions only. Add instance methods later if usage patterns warrant it.

### Type Constructor (src/types.ts or src/patch.ts)

```typescript
/**
 * Construct the patch type for a given East type.
 * This is a type-level constructor, similar to ArrayType, DictType, etc.
 */
export function PatchType<T extends EastType>(type: T): PatchType<T>
```

This must integrate with the type system in `types.ts` and be recognized by `applyTypeParameters` in `builtins.ts`.

### Usage in East Functions

```typescript
import { East, IntegerType, StringType, StructType, PatchType } from "@elaraai/east";

const PersonType = StructType({
    name: StringType,
    age: IntegerType,
});

// Create a diff between two values
const createDiff = East.function(
    [PersonType, PersonType],
    PatchType(PersonType),
    ($, before, after) => {
        $.return(East.diff(before, after));
    }
);

// Apply a patch to a value
const patchPerson = East.function(
    [PersonType, PatchType(PersonType)],
    PersonType,
    ($, base, patch) => {
        $.return(East.applyPatch(base, patch));
    }
);

// Practical example: Track changes and allow undo
const editWithUndo = East.function(
    [PersonType, PersonType],
    StructType({ result: PersonType, undo: PatchType(PersonType) }),
    ($, original, edited) => {
        const patch = $.let(East.diff(original, edited));
        const undoPatch = $.let(East.invertPatch(patch));
        $.return({ result: edited, undo: undoPatch });
    }
);
```

## File Structure

```
src/
  builtins.ts                 # Add Diff, ApplyPatch, ComposePatch, InvertPatch builtins
  compile.ts                  # Add builtin_evaluators for patch operations
  patch.ts                    # PatchType constructor, *For functions (value-level)
  patch.spec.ts               # Unit tests for *For functions (direct JS calls, not East expressions)
  types.ts                    # May need updates for PatchType integration

src/expr/
  block.ts                    # Add diff, applyPatch, composePatch, invertPatch functions
  index.ts                    # Export and add to East object

test/
  patch.spec.ts               # Compliance tests using describeEast (East expressions, runs on all backends)
```

**Test file distinction:**
- `src/patch.spec.ts` - Tests `diffFor`, `applyFor`, etc. directly as JavaScript functions. Fast, good for debugging the core implementation.
- `test/patch.spec.ts` - Tests `East.diff`, `East.applyPatch`, etc. as East expressions using `describeEast`. Validates the full pipeline (IR → compile → execute) and runs on all East backends for compliance.

### Integration Points

1. **`src/builtins.ts`**
   - Add `"Diff" | "ApplyPatch" | "ComposePatch" | "InvertPatch"` to `BuiltinName`
   - Add type signatures to `Builtins` record
   - Update `applyTypeParameters` to handle `PatchType`

2. **`src/patch.ts`** - Core implementation (new file)
   - `PatchType<T>` type constructor
   - `diffFor`, `applyFor`, `composeFor`, `invertFor` functions
   - Follow pattern of `comparison.ts`

3. **`src/compile.ts`**
   - Import `*For` functions from `patch.ts`
   - Add to `builtin_evaluators` record

4. **`src/expr/block.ts`**
   - Add `diff`, `applyPatch`, `composePatch`, `invertPatch` functions
   - Follow pattern of `equal`, `less`, etc.
   - Add to `Object.assign(Expr, {...})`

5. **`src/expr/index.ts`**
   - Export `PatchType` from `../patch.js`
   - Export expression builders from `./block.js`
   - Add to `East` object

## IR Representation

Patch operations use the existing `BuiltinIR` node type. **No changes to `src/ir.ts` are required** - we reuse the existing builtin infrastructure:

```typescript
// Example IR for East.diff(before, after)
{
  type: "Builtin",
  value: {
    type: PatchType(PersonType),  // Result type
    location: { ... },
    builtin: "Diff",
    type_parameters: [PersonType],  // The type being diffed
    arguments: [beforeIR, afterIR],
  }
}
```

### Compilation

The `builtin_evaluators` in `compile.ts` maps builtin names to runtime functions:

```typescript
builtin_evaluators: Record<BuiltinName, ...> = {
  // ... existing
  Diff: (_location, _platformDef, T) => diffFor(T),
  ApplyPatch: (_location, _platformDef, T) => applyFor(T),
  ComposePatch: (_location, _platformDef, T) => composeFor(T),
  InvertPatch: (_location, _platformDef, T) => invertFor(T),
}
```

The compiler hoists and caches `*For` functions per type (same pattern as `equalFor`).

## Implementation Notes

### Equality Comparison

The patch system uses `equalFor` from the comparison module for:
- Detecting unchanged values in `diffFor`
- Verifying base values in `applyFor`
- Checking patch compatibility in `composeFor`

### Heuristics

The diff algorithm includes heuristics to choose between `replace` and `patch`:
- If Dict keys don't intersect at all → use `replace`
- If Array is completely replaced → use `replace`
- These can be tuned based on patch size vs structural complexity

### Immutability

All operations are immutable:
- `applyFor` returns a new value, doesn't mutate input
- `composeFor` returns a new patch, doesn't mutate inputs
- `invertFor` returns a new patch, doesn't mutate input

### Normalisation Rules

Empty structural patches **must** collapse to `.unchanged`:

```typescript
// These are NOT valid patches - must be normalised:
{ type: 'patch', value: {} }           // empty DictType patch → .unchanged
{ type: 'patch', value: {} }           // empty SetType patch → .unchanged
{ type: 'patch', value: [] }           // empty ArrayType patch → .unchanged

// StructType: if ALL fields are .unchanged, collapse to .unchanged
{ type: 'patch', value: { a: { type: 'unchanged' }, b: { type: 'unchanged' } } }
// → { type: 'unchanged', value: null }

// VariantType: if inner patch is .unchanged, collapse to .unchanged
{ type: 'patch', value: { type: 'some', value: { type: 'unchanged' } } }
// → { type: 'unchanged', value: null }
```

This normalisation:
- Ensures `diff(x, x)` always returns `.unchanged` (not an empty `.patch`)
- Simplifies equality checks on patches
- Must be applied in `diffFor`, `composeFor`, and `invertFor`

### Error Messages

`ConflictError` must include actionable context for debugging:

```typescript
// Format: "Cannot <operation> <location> - expected <expected>, found <actual>"

// Examples:
ConflictError: Cannot delete key "foo" - expected value (x=1), found (x=2)
ConflictError: Cannot apply update at index 3 - expected 42, found 99
ConflictError: Cannot insert key "bar" - key already exists with value "hello"
ConflictError: Cannot apply patch to array - expected length 5, found length 3
ConflictError: Cannot compose patches - first patch deletes key "x", second patch updates it
```

Use `printFor` from `./serialization/east.js` to format values in error messages.

### Performance Considerations

**No lazy evaluation or caching.** The `*For` functions create closures that dispatch on type, but:
- Do NOT cache/memoize results
- Do NOT use lazy thunks for recursive types
- Each call to `diffFor(type)` creates a fresh function
- This keeps the implementation simple and predictable

## Test Specification (`test/patch.spec.ts`)

Tests use `describeEast` from `./platforms.spec.js` and must achieve high coverage with edge cases.

### Test Structure

```
test/patch.spec.ts
├── Primitive Types
│   ├── Null
│   ├── Boolean
│   ├── Integer
│   ├── Float
│   ├── String
│   ├── DateTime
│   └── Blob
├── Collection Types
│   ├── Array
│   ├── Set
│   └── Dict
├── Compound Types
│   ├── Struct
│   └── Variant
├── Reference Types
│   └── Ref
├── Nested Types
├── Algebraic Properties
├── Conflict Detection
├── Replace-Only Types (Recursive, Function, Never)
└── Performance/Stress Tests
```

### Primitive Type Tests

| Type | Test Case | Before | After | Expected Patch |
|------|-----------|--------|-------|----------------|
| Null | identical | `null` | `null` | `.unchanged` |
| Boolean | identical | `true` | `true` | `.unchanged` |
| Boolean | changed | `true` | `false` | `.replace (before=true, after=false)` |
| Integer | identical | `42n` | `42n` | `.unchanged` |
| Integer | changed | `0n` | `100n` | `.replace` |
| Integer | min value | `-9223372036854775808n` | `0n` | `.replace` |
| Integer | max value | `0n` | `9223372036854775807n` | `.replace` |
| Float | identical | `3.14` | `3.14` | `.unchanged` |
| Float | changed | `1.0` | `2.0` | `.replace` |
| Float | NaN to NaN | `NaN` | `NaN` | `.unchanged` |
| Float | NaN to number | `NaN` | `1.0` | `.replace` |
| Float | number to NaN | `1.0` | `NaN` | `.replace` |
| Float | Infinity | `Infinity` | `-Infinity` | `.replace` |
| Float | negative zero | `-0.0` | `0.0` | `.replace` |
| Float | zero to neg zero | `0.0` | `-0.0` | `.replace` |
| String | identical | `"hello"` | `"hello"` | `.unchanged` |
| String | changed | `"a"` | `"b"` | `.replace` |
| String | empty to non-empty | `""` | `"x"` | `.replace` |
| String | non-empty to empty | `"x"` | `""` | `.replace` |
| String | unicode | `"café"` | `"naïve"` | `.replace` |
| DateTime | identical | same date | same date | `.unchanged` |
| DateTime | changed | date1 | date2 | `.replace` |
| DateTime | epoch | epoch | now | `.replace` |
| Blob | identical | `0x00ff` | `0x00ff` | `.unchanged` |
| Blob | changed | `0x00` | `0xff` | `.replace` |
| Blob | empty to non-empty | `0x` | `0x00` | `.replace` |
| Blob | length change | `0x00` | `0x0000` | `.replace` |

### Array Tests

| Test Case | Before | After | Expected |
|-----------|--------|-------|----------|
| **Basic Operations** |
| identical empty | `[]` | `[]` | `.unchanged` |
| identical non-empty | `[1,2,3]` | `[1,2,3]` | `.unchanged` |
| empty to non-empty | `[]` | `[1]` | `.patch [{key:0, offset:0, op:.insert 1}]` |
| non-empty to empty | `[1]` | `[]` | `.patch [{key:0, offset:0, op:.delete 1}]` |
| **Single Element Changes** |
| update first | `[1,2,3]` | `[9,2,3]` | `.patch [{key:0, ..., op:.update}]` |
| update middle | `[1,2,3]` | `[1,9,3]` | `.patch [{key:1, ..., op:.update}]` |
| update last | `[1,2,3]` | `[1,2,9]` | `.patch [{key:2, ..., op:.update}]` |
| **Insertions** |
| insert at start | `[2,3]` | `[1,2,3]` | `.patch [{key:0, op:.insert 1}]` |
| insert at middle | `[1,3]` | `[1,2,3]` | `.patch [{key:1, op:.insert 2}]` |
| insert at end (push) | `[1,2]` | `[1,2,3]` | `.patch [{key:2, op:.insert 3}]` |
| insert multiple | `[1,4]` | `[1,2,3,4]` | inserts at 1,2 |
| **Deletions** |
| delete first | `[1,2,3]` | `[2,3]` | `.patch [{key:0, op:.delete 1}]` |
| delete middle | `[1,2,3]` | `[1,3]` | `.patch [{key:1, op:.delete 2}]` |
| delete last (pop) | `[1,2,3]` | `[1,2]` | `.patch [{key:2, op:.delete 3}]` |
| delete multiple | `[1,2,3,4]` | `[1,4]` | deletes at 1,2 |
| **Mixed Operations** |
| insert and delete | `[1,2,3]` | `[1,4,3]` | update at 1 OR delete+insert |
| reorder (swap) | `[1,2]` | `[2,1]` | delete+insert operations |
| reverse | `[1,2,3]` | `[3,2,1]` | multiple operations |
| shift left | `[1,2,3,4]` | `[2,3,4,5]` | mixed ops |
| **Offset Tracking** |
| verify offset after delete | `[a,b,c]` | `[a,c]` | offset increments correctly |
| verify offset after insert | `[a,c]` | `[a,b,c]` | offset decrements correctly |
| multiple ops with offsets | `[a,b,c,d]` | `[x,b,d,y]` | offsets track cumulative shifts |
| **Edge Cases** |
| large array unchanged | 1000 elements | same | `.unchanged` |
| complete replacement | `[1,2,3]` | `[a,b,c,d]` | `.replace` (heuristic) |
| nested array update | `[[1,2],[3,4]]` | `[[1,9],[3,4]]` | nested `.patch` |

### Set Tests

| Test Case | Before | After | Expected |
|-----------|--------|-------|----------|
| **Basic Operations** |
| identical empty | `{}` | `{}` | `.unchanged` |
| identical non-empty | `{1,2,3}` | `{1,2,3}` | `.unchanged` |
| empty to non-empty | `{}` | `{1}` | `.patch {1: .insert}` |
| non-empty to empty | `{1}` | `{}` | `.patch {1: .delete}` |
| **Single Element Changes** |
| insert one | `{1,2}` | `{1,2,3}` | `.patch {3: .insert}` |
| delete one | `{1,2,3}` | `{1,2}` | `.patch {3: .delete}` |
| **Multiple Changes** |
| insert multiple | `{1}` | `{1,2,3}` | `.patch {2:.insert, 3:.insert}` |
| delete multiple | `{1,2,3}` | `{1}` | `.patch {2:.delete, 3:.delete}` |
| mixed insert/delete | `{1,2,3}` | `{2,3,4}` | `.patch {1:.delete, 4:.insert}` |
| **Edge Cases** |
| disjoint sets | `{1,2}` | `{3,4}` | `.replace` (heuristic) |
| string keys | `{"a","b"}` | `{"b","c"}` | `.patch {"a":.delete, "c":.insert}` |
| struct keys | set of structs | modified | correct key comparison |

### Dict Tests

| Test Case | Before | After | Expected |
|-----------|--------|-------|----------|
| **Basic Operations** |
| identical empty | `{:}` | `{:}` | `.unchanged` |
| identical non-empty | `{a:1,b:2}` | `{a:1,b:2}` | `.unchanged` |
| empty to non-empty | `{:}` | `{a:1}` | `.patch {a: .insert 1}` |
| non-empty to empty | `{a:1}` | `{:}` | `.patch {a: .delete 1}` |
| **Value Updates** |
| update single value | `{a:1}` | `{a:2}` | `.patch {a: .update <patch>}` |
| update nested value | `{a:{x:1}}` | `{a:{x:2}}` | nested `.update` |
| **Key Changes** |
| insert key | `{a:1}` | `{a:1,b:2}` | `.patch {b: .insert 2}` |
| delete key | `{a:1,b:2}` | `{a:1}` | `.patch {b: .delete 2}` |
| **Mixed Operations** |
| insert + delete | `{a:1}` | `{b:2}` | `.patch {a:.delete, b:.insert}` |
| insert + update | `{a:1}` | `{a:2,b:3}` | `.patch {a:.update, b:.insert}` |
| delete + update | `{a:1,b:2}` | `{a:9}` | `.patch {a:.update, b:.delete}` |
| **Edge Cases** |
| integer keys | `{1n:a, 2n:b}` | modified | correct key handling |
| struct keys | complex keys | modified | correct comparison |
| nested dict update | `{a:{x:{y:1}}}` | `{a:{x:{y:2}}}` | deeply nested patch |
| complete key replacement | `{a:1,b:2,c:3}` | `{x:1,y:2,z:3}` | `.replace` (heuristic) |

### Struct Tests

| Test Case | Before | After | Expected |
|-----------|--------|-------|----------|
| **Basic Operations** |
| identical | `(a=1,b=2)` | `(a=1,b=2)` | `.unchanged` |
| single field change | `(a=1,b=2)` | `(a=1,b=9)` | `.patch (a=.unchanged, b=.replace)` |
| multiple field change | `(a=1,b=2)` | `(a=9,b=9)` | `.patch (a=.replace, b=.replace)` |
| all fields unchanged | `(a=1,b=2,c=3)` | `(a=1,b=2,c=3)` | `.unchanged` |
| **Nested Structs** |
| nested field change | `(a=(x=1))` | `(a=(x=2))` | `.patch (a=.patch (x=.replace))` |
| deeply nested | 3+ levels | modified | correct nesting |
| **Complex Fields** |
| array field | `(arr=[1,2])` | `(arr=[1,2,3])` | `.patch (arr=<array patch>)` |
| dict field | `(d={a:1})` | `(d={a:2})` | `.patch (d=<dict patch>)` |
| variant field | `(v=.some 1)` | `(v=.none)` | `.patch (v=.replace)` |

### Variant Tests

| Test Case | Before | After | Expected |
|-----------|--------|-------|----------|
| **Same Case** |
| identical null case | `.none` | `.none` | `.unchanged` |
| identical with data | `.some 42` | `.some 42` | `.unchanged` |
| same case, data changed | `.some 1` | `.some 2` | `.patch .some <patch>` |
| **Case Change** |
| none to some | `.none` | `.some 42` | `.replace` |
| some to none | `.some 42` | `.none` | `.replace` |
| different cases | `.ok 1` | `.error "x"` | `.replace` |
| **Nested Data** |
| nested struct | `.some (a=1)` | `.some (a=2)` | `.patch .some <struct patch>` |
| nested array | `.some [1,2]` | `.some [1,2,3]` | `.patch .some <array patch>` |
| **Multi-Case Variant** |
| 3+ cases, same | `.pending` | `.pending` | `.unchanged` |
| 3+ cases, change data | `.ok 1` | `.ok 2` | `.patch .ok <patch>` |
| 3+ cases, case change | `.ok 1` | `.pending` | `.replace` |

### Nested/Compound Type Tests

| Test Case | Description |
|-----------|-------------|
| `Array<Struct>` | Array of structs, update one struct field |
| `Array<Struct>` | Array of structs, insert/delete struct |
| `Dict<String, Array>` | Dict values are arrays, update array element |
| `Dict<String, Struct>` | Dict values are structs, update struct field |
| `Struct { arr: Array, dict: Dict }` | Multiple collection fields |
| `Array<Array<Integer>>` | 2D array, update inner element |
| `Dict<String, Dict<String, Integer>>` | Nested dicts |
| `Variant { a: Struct, b: Array }` | Variant with complex cases |
| `Array<Variant>` | Array of variants, mixed changes |
| Deeply nested (4+ levels) | Verify patch propagates correctly |

### Algebraic Property Tests

| Property | Test |
|----------|------|
| **Round-trip** | `apply(before, diff(before, after)) = after` for all types |
| **Invert round-trip** | `apply(after, invert(diff(before, after))) = before` |
| **Self-diff** | `diff(x, x) = .unchanged` for all types |
| **Identity compose** | `compose(patch, invert(patch)) = .unchanged` |
| **Inverse identity** | `compose(invert(patch), patch) = .unchanged` |
| **Transitivity** | `apply(a, compose(diff(a,b), diff(b,c))) = c` |
| **Transitivity** | `compose(diff(a,b), diff(b,c)) ≈ diff(a,c)` (semantically equal) |
| **Double invert** | `invert(invert(patch)) = patch` |
| **Unchanged apply** | `apply(x, .unchanged) = x` |
| **Unchanged compose** | `compose(.unchanged, patch) = patch` |
| **Unchanged compose** | `compose(patch, .unchanged) = patch` |

### Normalisation Tests

| Type | Test Case | Expected |
|------|-----------|----------|
| DictType | empty operations dict | `.unchanged` (not `.patch {:}`) |
| SetType | empty operations dict | `.unchanged` (not `.patch {:}`) |
| ArrayType | empty operations array | `.unchanged` (not `.patch []`) |
| StructType | all fields `.unchanged` | `.unchanged` (not `.patch (...)`) |
| VariantType | inner patch is `.unchanged` | `.unchanged` (not `.patch .case ...`) |
| Nested | struct with nested unchanged | correctly collapses |
| Compose | result has no ops | normalises to `.unchanged` |
| Invert | `.unchanged` input | returns `.unchanged` |

### Conflict Detection Tests (`ConflictError`)

| Operation | Test Case | Expected Error |
|-----------|-----------|----------------|
| **apply** | wrong base value | `ConflictError` |
| **apply** | delete non-existent key | `ConflictError` |
| **apply** | insert existing key | `ConflictError` |
| **apply** | update with mismatched before | `ConflictError` |
| **apply** | array index out of bounds | `ConflictError` |
| **apply** | dict key not found | `ConflictError` |
| **compose** | delete then delete same key | `ConflictError` |
| **compose** | insert then insert same key | `ConflictError` |
| **compose** | incompatible array offsets | `ConflictError` |

### RefType Tests

| Test Case | Before | After | Expected |
|-----------|--------|-------|----------|
| identical ref (same object) | `&x` | `&x` (same) | `.unchanged` |
| equal inner value | `&1` | `&1` (different ref) | `.unchanged` |
| different inner value | `&1` | `&2` | `.patch <inner patch>` |
| nested ref | `&(a=1)` | `&(a=2)` | `.patch .patch (a=.replace)` |
| apply creates new ref | verify `apply` returns new ref object | |

### Replace-Only Type Tests

| Type | Test Case | Expected |
|------|-----------|----------|
| RecursiveType | identical | `.unchanged` |
| RecursiveType | different | `.replace` |
| RecursiveType | nested change | `.replace` (no structural patch) |
| FunctionType | any | `.unchanged` (functions always equal) |
| AsyncFunctionType | any | `.unchanged` (functions always equal) |
| NeverType | any | throws `EastError` (no values exist) |

### Performance/Stress Tests

| Test Case | Description |
|-----------|-------------|
| Large array (10000 elements) | Single element change → small patch |
| Large array (10000 elements) | Append 100 elements → efficient patch |
| Large dict (1000 keys) | Single value update → small patch |
| Deeply nested (10 levels) | Single leaf change → correct path |
| Wide struct (50 fields) | Single field change → only that field in patch |

## Array Diff Algorithm

The legacy implementation uses a naive algorithm that compares elements at matching indices and always falls back to `replace` when any changes exist. This is inadequate for most real-world use cases.

### Recommended: LCS-Based Diff

Use the **Longest Common Subsequence (LCS)** algorithm to find optimal element alignment:

```typescript
/**
 * Compute LCS using dynamic programming.
 * Returns indices of matching elements in both arrays.
 */
function computeLCS<T>(
  before: T[],
  after: T[],
  equal: (a: T, b: T) => boolean
): { beforeIndices: number[], afterIndices: number[] } {
  const m = before.length;
  const n = after.length;

  // Build LCS table
  const dp: number[][] = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (equal(before[i - 1]!, after[j - 1]!)) {
        dp[i]![j] = dp[i - 1]![j - 1]! + 1;
      } else {
        dp[i]![j] = Math.max(dp[i - 1]![j]!, dp[i]![j - 1]!);
      }
    }
  }

  // Backtrack to find LCS indices
  const beforeIndices: number[] = [];
  const afterIndices: number[] = [];
  let i = m, j = n;

  while (i > 0 && j > 0) {
    if (equal(before[i - 1]!, after[j - 1]!)) {
      beforeIndices.unshift(i - 1);
      afterIndices.unshift(j - 1);
      i--; j--;
    } else if (dp[i - 1]![j]! > dp[i]![j - 1]!) {
      i--;
    } else {
      j--;
    }
  }

  return { beforeIndices, afterIndices };
}
```

### Generating Patch Operations

From the LCS alignment, generate operations:

1. Elements in `before` not in LCS → **delete** at original position
2. Elements in `after` not in LCS → **insert** at new position

**Note on LCS equality:** For primitive element types, LCS uses value equality, so matched elements are identical (no updates needed). For compound element types (structs, arrays, etc.), consider using **shallow equality** (e.g., match structs by an "id" field) to allow structural updates within matched elements. The implementation below uses full `equalFor`, meaning LCS elements are always equal and updates only occur if using a custom matcher.

```typescript
function generateArrayPatch<T>(
  before: T[],
  after: T[],
  equal: (a: T, b: T) => boolean,
  diff: (a: T, b: T) => Patch<T>
): ArrayPatch<T> {
  const { beforeIndices, afterIndices } = computeLCS(before, after, equal);
  const operations: ArrayPatchEntry<T>[] = [];

  let beforePtr = 0;
  let afterPtr = 0;
  let lcsPtr = 0;
  let offset = 0n;

  while (beforePtr < before.length || afterPtr < after.length) {
    const nextBeforeLCS = lcsPtr < beforeIndices.length ? beforeIndices[lcsPtr] : before.length;
    const nextAfterLCS = lcsPtr < afterIndices.length ? afterIndices[lcsPtr] : after.length;

    // Delete elements in `before` not in LCS
    while (beforePtr < nextBeforeLCS!) {
      operations.push({
        key: BigInt(afterPtr),
        offset,
        operation: variant('delete', before[beforePtr]!)
      });
      offset += 1n;
      beforePtr++;
    }

    // Insert elements in `after` not in LCS
    while (afterPtr < nextAfterLCS!) {
      operations.push({
        key: BigInt(afterPtr),
        offset,
        operation: variant('insert', after[afterPtr]!)
      });
      offset -= 1n;
      afterPtr++;
    }

    // Handle LCS element (may need update if structurally different)
    if (lcsPtr < beforeIndices.length) {
      const beforeElem = before[beforePtr]!;
      const afterElem = after[afterPtr]!;
      const patch = diff(beforeElem, afterElem);

      if (patch.type !== 'unchanged') {
        operations.push({
          key: BigInt(afterPtr),
          offset,
          operation: variant('update', patch)
        });
      }

      beforePtr++;
      afterPtr++;
      lcsPtr++;
    }
  }

  return operations;
}
```

### Complexity

- **Time**: O(m × n) for LCS computation where m, n are array lengths
- **Space**: O(m × n) for DP table, can be reduced to O(min(m, n)) with Hirschberg's algorithm

### Alternative: Myers Algorithm

For cases where edit distance D is expected to be small (D << m + n), Myers algorithm achieves O((m + n) × D) time. This is more efficient for incremental changes but more complex to implement.

Consider Myers when:
- Arrays are large (thousands of elements)
- Changes are typically small (few insertions/deletions)
- Performance is critical

### Heuristics

Apply these heuristics to choose between `patch` and `replace`:

```typescript
// If more than 50% of elements changed, use replace
if (operations.length > (before.length + after.length) / 2) {
  return variant('replace', { before, after });
}

// If no common elements, use replace
if (beforeIndices.length === 0) {
  return variant('replace', { before, after });
}

return variant('patch', operations);
```

**Tuning notes:**
- The 50% threshold is a heuristic balancing patch size vs. semantic granularity
- Lower thresholds favor `replace` (simpler patches, less conflict potential)
- Higher thresholds favor `patch` (more granular, better for compose/invert)
- Consider making this configurable or using byte-size comparison instead of operation count
- Similar heuristics apply to DictType (key overlap) and SetType (element overlap)

## Migration from Legacy

**Legacy implementation location:**
- `ELARACore/javascript/libs/core/src/east/patch.ts` - Implementation
- `ELARACore/javascript/libs/core/src/east/patch.spec.ts` - Tests

The legacy implementation uses:
- `mapValues`, `mapEntries` utilities → use native `Object.entries`/`Object.fromEntries`
- `variant` from `../utils/variant` → use `variant` from `./containers/variant.js`
- `Nullable(T)` type → use `OptionType(T)` pattern

**Already available in East** (no porting needed):
- `equalFor`, `compareFor` from `./comparison.js` - value equality and ordering
- `printFor` from `./serialization/east.js` - string serialization for error messages

Key differences:
1. East doesn't have `NullableType` - uses `OptionType` pattern instead
2. East has `RecursiveType` - needs handling (structural patching, not replace-only)
3. East has `FunctionType` / `AsyncFunctionType` - needs handling (replace-only)
4. Legacy array diff always returns `replace` - implement proper LCS-based algorithm

## Required Fixes and Refactoring

The current `src/patch.ts` implementation has TypeScript type issues when handling `RecursiveType`. This section documents the required fixes based on patterns from `comparison.ts` and `json.ts`.

### Problem Statement

The patch functions (`diffFor`, `applyFor`, `composeFor`, `invertFor`) need to call helper functions like `equalFor`, `compareFor`, and `isFor` from `comparison.ts`. These helpers have overloaded signatures:

```typescript
// comparison.ts overloads
export function equalFor(type: EastTypeValue, typeCtx?: TypeContext): (x: any, y: any, ctx?: ValueContext) => boolean;
export function equalFor<T extends EastType>(type: T): (x: ValueTypeOf<T>, y: ValueTypeOf<T>) => boolean;
```

The first overload accepts `typeCtx` for recursive type handling, but requires `EastTypeValue` exactly. The second overload accepts any `EastType` but doesn't accept `typeCtx`.

When the patch functions call `equalFor(type, typeCtx)` after converting to `EastTypeValue`, TypeScript cannot resolve the overload because the type is still inferred as `EastTypeValue | EastType`.

### The json.ts Pattern

The `json.ts` file handles this correctly by:

1. **Working purely with `EastTypeValue`** - After `toEastTypeValue()` conversion, all type handling uses the variant representation
2. **Using a `TypeContext` stack** - Functions like `toJSONFor` define their own context type and push/pop to handle recursive types:

```typescript
type JSONEncodeTypeContext = ((value: any, ctx?: JSONEncodeValueContext) => unknown)[];

export function toJSONFor(type: EastType | EastTypeValue, typeCtx: JSONEncodeTypeContext = []): (...) => unknown {
    if (!isVariant(type)) {
        type = toEastTypeValue(type);
    }

    // For container types:
    } else if (type.type === "Struct") {
        const fieldToJson: { ... } = {};
        const ret = (value: any, ctx: ...) => { ... };

        typeCtx.push(ret);  // Push BEFORE recursing into fields
        for (const { name, type: t } of type.value) {
            fieldToJson[name] = toJSONFor(t, typeCtx);  // Pass typeCtx
        }
        typeCtx.pop();  // Pop AFTER
        return ret;
    } else if (type.type === "Recursive") {
        // Look up the function from the stack using the back-reference index
        const ret = typeCtx[typeCtx.length - Number(type.value)];
        if (ret === undefined) {
            throw new Error(`Internal error: Recursive type context not found`);
        }
        return ret;
    }
}
```

Key points:
- **Push before recursing, pop after** - The function for the current container type is pushed onto the context stack before processing its inner types
- **Back-reference resolution** - When encountering `variant("Recursive", N)`, look up `typeCtx[typeCtx.length - N]`
- **Each container type follows the same pattern** - Ref, Array, Dict, Struct, Variant all push/pop

### The comparison.ts Pattern

The `comparison.ts` file follows the same pattern for `equalFor`, `compareFor`, `isFor`:

```typescript
type TypeContext = ((x: any, y: any, ctx?: ValueContext) => boolean)[];

export function equalFor(type: EastTypeValue, typeCtx: TypeContext = []): (...) => boolean {
    if (!isVariant(type)) {
        type = toEastTypeValue(type);
    }

    // For container types like Struct:
    } else if (type.type === "Struct") {
        const fieldEqualities: { [key: string]: (x: any, y: any, ctx?: ValueContext) => boolean } = {};

        const ret = (x: Record<string, any>, y: Record<string, any>, ctx: ValueContext = new Map()) => {
            // ... implementation
        };

        typeCtx.push(ret);
        for (const { name, type: fieldType } of type.value) {
            fieldEqualities[name] = equalFor(fieldType, typeCtx);
        }
        typeCtx.pop();

        return ret;
    } else if (type.type === "Recursive") {
        const ret = typeCtx[typeCtx.length - Number(type.value)];
        if (ret === undefined) {
            throw new Error("Internal error: Recursive type context not found");
        }
        return ret;
    }
}
```

### Required Changes to patch.ts

1. **Define proper TypeContext types for each function**:

```typescript
// Each patch function needs its own context type
type DiffTypeContext = ((before: any, after: any) => any)[];
type ApplyTypeContext = ((base: any, patch: any) => any)[];
type ComposeTypeContext = ((first: any, second: any) => any)[];
type InvertTypeContext = ((patch: any) => any)[];
```

2. **Follow the push/pop pattern for all container types**:

For `diffFor`:
```typescript
} else if (type.type === "Struct") {
    const fieldDiffs: Record<string, (a: any, b: any) => any> = {};
    const fieldEquals: Record<string, (a: any, b: any) => boolean> = {};

    const ret = (before: Record<string, any>, after: Record<string, any>) => {
        // ... implementation using fieldDiffs and fieldEquals
    };

    typeCtx.push(ret);  // Push BEFORE recursing
    for (const { name, type: fieldType } of type.value) {
        fieldDiffs[name] = diffFor(fieldType, typeCtx);
        fieldEquals[name] = equalFor(fieldType, typeCtx);  // Pass typeCtx!
    }
    typeCtx.pop();  // Pop AFTER

    return ret;
}
```

3. **Call comparison helpers with typeCtx**:

The key fix is passing `typeCtx` to calls like `equalFor`, `compareFor`, `isFor`. But there's a type system issue: these functions expect `EastTypeValue` when called with `typeCtx`, but the inner types from `type.value` are already `EastTypeValue`.

Looking at how `comparison.ts` handles this internally:
- After `toEastTypeValue()`, the type is guaranteed to be `EastTypeValue`
- Inner types accessed via `type.value`, `type.value.key`, `type.value.value` etc are also `EastTypeValue`
- The overload `equalFor(type: EastTypeValue, typeCtx?: TypeContext)` should match

**The issue**: TypeScript's control flow analysis doesn't narrow `type` after reassignment in `type = toEastTypeValue(type as EastType)`. The variable retains its original union type.

**Solution**: Use a separate variable for the narrowed type:

```typescript
export function diffFor(type: EastTypeValue | EastType, typeCtx: DiffTypeContext = []): (...) => any {
    // Convert EastType to EastTypeValue if necessary
    const t: EastTypeValue = isVariant(type) ? type : toEastTypeValue(type as EastType);

    // Now `t` is properly typed as EastTypeValue
    if (t.type === "Struct") {
        for (const { name, type: fieldType } of t.value) {
            // fieldType is EastTypeValue, typeCtx is provided
            fieldDiffs[name] = diffFor(fieldType, typeCtx);
            fieldEquals[name] = equalFor(fieldType, typeCtx);  // Now resolves to correct overload
        }
    }
}
```

4. **Handle RecursiveType with structural patching**:

The current design specifies replace-only semantics for RecursiveType, but the implementation attempts structural patching. The issue is that `PatchType` for `RecursiveType` creates an infinite type.

**Option A: Replace-only (simpler)**
```typescript
} else if (type.type === "Recursive") {
    // RecursiveType uses replace-only semantics
    const equal = equalFor(type, typeCtx);
    return (before: any, after: any) => {
        if (equal(before, after)) {
            return variant("unchanged", null);
        }
        return variant("replace", { before, after });
    };
}
```

**Option B: Structural patching with lazy type construction**

For structural patching of recursive types, `PatchType` must create a lazy/recursive patch type:

```typescript
// PatchType for RecursiveType creates a recursive patch type
} else if (t.type === "Recursive") {
    // The patch type is itself recursive - patches for tree nodes can contain patches for children
    const patchRecursive = { type: "Recursive" as const, node: undefined as unknown as EastType };

    const result = VariantType({
        unchanged: NullType,
        replace: StructType({ before: type, after: type }),
        patch: patchRecursive  // Will be filled in
    });

    context.set(type, result);  // Register before recursing

    const nodePatchType = PatchType(t.node, context);
    patchRecursive.node = nodePatchType;

    return result;
}
```

Then in `diffFor`:
```typescript
} else if (type.type === "Recursive") {
    // For Recursive, look up the function from the context stack
    const ret = typeCtx[typeCtx.length - Number(type.value)];
    if (ret === undefined) {
        throw new Error("Internal error: Recursive type context not found");
    }
    return ret;
}
```

But this requires the outer container (e.g., Struct containing the Recursive field) to have pushed its `ret` function before encountering the Recursive reference.

### Summary of Changes

1. **Type narrowing**: Use `const t: EastTypeValue = isVariant(type) ? type : toEastTypeValue(type)` instead of reassigning `type`

2. **All container types** (Ref, Array, Set, Dict, Struct, Variant) must:
   - Define their result function `ret`
   - Push `ret` to `typeCtx` before processing inner types
   - Process inner types, passing `typeCtx` to recursive calls and helper calls
   - Pop from `typeCtx` after

3. **Recursive type handling**: When `type.type === "Recursive"`, look up `typeCtx[typeCtx.length - Number(type.value)]`

4. **Helper function calls**: Pass `typeCtx` to `equalFor`, `compareFor`, `isFor` when inside container types

5. **PatchType for RecursiveType**: Use a context Map to track already-computed patch types and create proper recursive structures

### Test Verification

After refactoring, the following tests should pass:
- All primitive type tests
- All collection type tests (Array, Set, Dict)
- All compound type tests (Struct, Variant)
- RecursiveType tests with nested structures
- Circular reference handling in recursive types
