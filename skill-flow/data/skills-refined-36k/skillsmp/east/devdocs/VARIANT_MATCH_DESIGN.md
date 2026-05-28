# Variant Match Expression Design

This document proposes adding a fluent `.match()` method to `VariantExpr` that returns a value, with support for partial matching and default handlers.

## Motivation

Currently, East provides two ways to pattern match on variants:

1. **`Expr.match(variant, handlers)`** - Expression-based, exhaustive matching
2. **`$.match(variant, handlers)`** - Statement-based, non-exhaustive, returns `NullExpr`

Neither provides a convenient fluent API directly on variant expressions. Users must use the verbose static function form:

```ts
// Current verbose approach
Expr.match(myVariant, {
  some: ($, val) => val,
  none: ($, _) => defaultValue
})
```

The requested syntax allows method chaining directly on variants:

```ts
// Proposed fluent approach
myVariant.match({
  some: ($, val) => val
}, ($) => defaultValue)
```

## Current Implementation Analysis

### VariantExpr (`/src/expr/variant.ts`)

The `VariantExpr` class already has helper methods built on `Expr.match()`:

| Method | Purpose | Returns |
|--------|---------|---------|
| `getTag()` | Get the case tag as a string | `StringExpr` |
| `hasTag(name)` | Check if variant has specific tag | `BooleanExpr` |
| `unwrap(name, onOther?)` | Extract value from specific case | Value type or union with fallback |

All three use `Expr.match()` internally, providing a pattern for the new method.

### Expr.match (`/src/expr/block.ts:739`)

```ts
function matchExpr<Cases, Handlers>(
  variant: Expr<VariantType<Cases>>,
  handlers: { [K in keyof Cases]: ($: BlockBuilder<NeverType>, data: ExprType<Cases[K]>) => any }
): ExprType<TypeOf<{ [K in keyof Cases]: ReturnType<Handlers[K]> }[keyof Cases]>>
```

Key characteristics:
- **Exhaustive**: All cases must have handlers
- **Returns value**: Union type of all handler return types
- **BlockBuilder scoped**: Handlers receive `$` for block building (but cannot use `$.return`)

### $.match (`/src/expr/block.ts:1416`)

```ts
$.match = <Cases>(
  variant: Expr<VariantType<Cases>>,
  cases: { [K in keyof Cases]?: ($, data) => any }
): NullExpr
```

Key characteristics:
- **Non-exhaustive**: Cases are optional (uses `?:`)
- **Statement only**: Returns `NullExpr`, cannot be used for expression values
- **Allows `$.return`**: Handlers receive full block builder with return capability

## Proposed Design

### Option A: Partial Match with Default (Recommended)

Add a `.match()` method to `VariantExpr` that allows partial case coverage with a required default:

```ts
class VariantExpr<Cases> {
  /**
   * Pattern match on this variant, handling specific cases with a default fallback.
   *
   * @param handlers - Object mapping case names to handler functions
   * @param defaultHandler - Required handler for any unmatched cases
   * @returns Expression of the union type of all handler return types
   */
  match<
    Handlers extends { [K in keyof Cases]?: ($: BlockBuilder<NeverType>, data: ExprType<Cases[K]>) => any },
    Default extends ($: BlockBuilder<NeverType>) => any
  >(
    handlers: Handlers,
    defaultHandler: Default
  ): ExprType<TypeUnion<
    TypeOf<{ [K in keyof Handlers]: ReturnType<NonNullable<Handlers[K]>> }[keyof Handlers]>,
    TypeOf<ReturnType<Default>>
  >>
}
```

**Usage:**

```ts
// Handle specific cases with default
const result = myOption.match({
  some: ($, val) => val.add(1n)
}, ($) => 0n);

// Single case extraction (like unwrap but with chaining)
const value = myResult.match({
  ok: ($, data) => data
}, ($) => $.error("Expected ok"));
```

**Benefits:**
- Fluent method chaining on variant expressions
- Flexible partial matching (handle only cases you care about)
- Type-safe default ensures all cases covered at runtime
- Consistent with `unwrap(name, onOther)` pattern

### Option B: Exhaustive Match Only

Add `.match()` that requires all cases (like current `Expr.match`):

```ts
match<Handlers extends { [K in keyof Cases]: ... }>(
  handlers: Handlers
): ExprType<...>
```

**Drawbacks:**
- No improvement over `Expr.match()` except syntax
- Cannot use default handlers for multiple cases

### Option C: Both Overloads

Provide both exhaustive and partial+default via overloads:

```ts
// Exhaustive (all cases required)
match<Handlers extends { [K in keyof Cases]: ... }>(
  handlers: Handlers
): ExprType<...>

// Partial with default
match<Handlers extends { [K in keyof Cases]?: ... }, Default>(
  handlers: Handlers,
  defaultHandler: Default
): ExprType<...>
```

**Drawbacks:**
- TypeScript overload resolution complexity
- Ambiguous which overload to use when all cases provided

## Recommended Approach: Option A

The partial match with required default provides:

1. **Maximum flexibility** - Handle any subset of cases
2. **Type safety** - Default ensures runtime coverage
3. **Ergonomic API** - Natural for common patterns like Option/Result
4. **Consistency** - Similar to `unwrap(name, onOther)` pattern

### Implementation Strategy

The implementation will build on the existing `Expr.match()` infrastructure:

```ts
// In /src/expr/variant.ts

match<
  Handlers extends { [K in keyof Cases]?: ($: BlockBuilder<NeverType>, data: ExprType<Cases[K]>) => any },
  Default extends ($: BlockBuilder<NeverType>) => any
>(
  handlers: Handlers,
  defaultHandler: Default
): ExprType<TypeUnion<...>> {
  // Build complete handler set by filling unhandled cases with default
  const completeHandlers = Object.fromEntries(
    Object.keys(this.cases).map(caseName => [
      caseName,
      handlers[caseName] ?? (($: BlockBuilder<NeverType>, _data: any) => defaultHandler($))
    ])
  ) as Record<keyof Cases, ($: BlockBuilder<NeverType>, data: any) => any>;

  return Expr.match(this, completeHandlers);
}
```

### Type Inference Considerations

The return type must be the union of:
1. Return types of all explicitly provided handlers
2. Return type of the default handler

TypeScript mapped types handle this:

```ts
type HandledCases<Handlers> = {
  [K in keyof Handlers]: ReturnType<NonNullable<Handlers[K]>>
}[keyof Handlers]

type Result = TypeUnion<HandledCases<Handlers>, ReturnType<Default>>
```

## Comparison with Existing Methods

| Method | Coverage | Returns | Use Case |
|--------|----------|---------|----------|
| `Expr.match()` | Exhaustive | Union of all | Full pattern match |
| `$.match()` | Partial | `NullExpr` | Statement control flow |
| `hasTag(name)` | Single | `BooleanExpr` | Tag checking |
| `unwrap(name, onOther?)` | Single+default | Value type | Single case extraction |
| **`match(handlers, default)`** | **Partial+default** | **Union type** | **Flexible value extraction** |

## Test Cases

```ts
// Basic partial match with default
const OptionType = VariantType({ some: IntegerType, none: NullType });

const getOrZero = East.function([OptionType], IntegerType, ($, opt) => {
  $.return(opt.match({
    some: ($, val) => val
  }, ($) => 0n));
});

// Multiple cases handled
const ResultType = VariantType({ ok: IntegerType, error: StringType, pending: NullType });

const handleResult = East.function([ResultType], IntegerType, ($, result) => {
  $.return(result.match({
    ok: ($, val) => val,
    error: ($, msg) => -1n
  }, ($) => 0n));  // pending -> 0
});

// All cases explicitly (exhaustive via default never called)
const explicitAll = East.function([OptionType], IntegerType, ($, opt) => {
  $.return(opt.match({
    some: ($, val) => val,
    none: ($, _) => 0n
  }, ($) => $.error("unreachable")));
});
```

## Migration Path

This is a purely additive change:
- Existing `Expr.match()` remains unchanged for exhaustive matching
- Existing `$.match()` remains unchanged for statement-based control flow
- New `.match()` method provides additional ergonomic option

No breaking changes to existing code.

## Open Questions

1. **Naming**: Should it be `.match()` or something else like `.when()`, `.cases()`, `.handle()`?
   - **Recommendation**: `.match()` aligns with functional programming conventions and the existing `$.match()` and `Expr.match()` naming.

2. **Default handler signature**: Should the default receive the full variant or just the tag?
   - **Recommendation**: Just `$` (like `unwrap`'s `onOther`). If users need the value, they can use the explicit handler for that case.

3. **Should we also add an exhaustive overload?**: Allow `.match(handlers)` without default when all cases covered?
   - **Recommendation**: No. Keep `Expr.match()` for exhaustive matching. The method's purpose is partial+default.

## Conclusion

Adding `VariantExpr.match(handlers, default)` provides a natural, fluent API for pattern matching that complements the existing static and statement-based approaches. The partial+default design maximizes flexibility while maintaining type safety.
