# Generic Platform Functions Design

This document describes the design for adding generic (polymorphic) platform functions to East, enabling platform authors to define type-parameterized functions similar to how builtins work.

## Motivation

Currently, platform functions have fixed concrete types:

```typescript
const log = East.platform("log", [StringType], NullType);
```

This forces users to either:
1. Define separate platform functions for each type (`logString`, `logInteger`, etc.)
2. Wrap `East.platform` in a TypeScript generic function to simulate polymorphism:

```typescript
export const alns_optimize = <S extends EastType>(solutionType: S) =>
    East.platform(
        "alns_optimize",
        [
            solutionType,
            FunctionType([solutionType], FloatType),
            ArrayType(FunctionType([solutionType], solutionType)),
            ArrayType(FunctionType([solutionType], solutionType)),
            ALNSConfigType,
        ],
        ALNSResultType(solutionType)
    );
```

The second approach works but:
- Creates a new platform function definition for each type instantiation
- Doesn't carry type parameters through to the IR
- Implementation cannot access type information at runtime

Builtins already support type parameters via `BuiltinIR.type_parameters`. This design extends the same capability to platform functions.

## API Design

### `East.genericPlatform`

Generic platform functions use **string placeholders** directly in the input and output type definitions. Type parameters like `"T"`, `"U"` appear as strings in the types array, and are substituted with actual types at call sites:

```typescript
function genericPlatform<
  const TParams extends readonly string[],
  const Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
>(
  name: string,
  typeParams: TParams,
  inputs: Inputs,
  output: Output
): GenericPlatformDefinition<TParams, Inputs, Output>
```

**Simple example (1 type parameter):**

```typescript
const log = genericPlatform(
  "log",
  ["T"],        // Type parameter names
  ["T"],        // Inputs: one argument of type T (string placeholder)
  NullType      // Output: Null (concrete type)
);

// User calls with type args as array, then value args:
log([StringType], myStringExpr)
log([IntegerType], myIntegerExpr)
```

**Multiple type parameters (2 type parameters):**

```typescript
const map = genericPlatform(
  "map",
  ["T", "U"],
  ["T", FunctionType(["T"], "U")],  // String placeholders in nested types
  "U"                                // Output is type parameter U
);

// Call:
map([StringType, IntegerType], myString, myMapperFn)
```

**Complex computed output type:**

```typescript
const alns_optimize = genericPlatform(
  "alns_optimize",
  ["S"],
  [
    "S",                                           // initial_solution: S
    FunctionType(["S"], FloatType),                // objective: S -> Float
    ArrayType(FunctionType(["S"], "S")),           // destroy_operators: Array<S -> S>
    ArrayType(FunctionType(["S"], "S")),           // repair_operators: Array<S -> S>
    ALNSConfigType,
  ],
  StructType({ solution: "S" })                    // Output: { solution: S }
);

// Call:
alns_optimize([MySolutionType], initial, objective, destroyOps, repairOps, config)
```

### Type Safety

TypeScript provides **full call-site type safety** using the `ApplyTypeArgs` mapped type. When you call `log([StringType], myIntegerExpr)`, TypeScript produces an error because `Expr<IntegerType>` is not assignable to a parameter expecting `Expr<StringType>`.

This is achieved through:

1. **String placeholders** - Type parameters are string literals like `"T"`, `"U"` that appear directly in input/output definitions
2. **`ApplyTypeArgs` type** - Recursively substitutes string placeholders with actual types from a type argument record
3. **`const` type parameter** modifier to infer narrow tuple types (no `as const` needed)

#### `ApplyTypeArgs` Type

The core substitution type recursively walks through type structures, replacing string keys with their corresponding types from `TypeArgs`:

```typescript
type ApplyTypeArgs<TypeArgs extends Record<string, EastType>, T> =
  T extends keyof TypeArgs ? TypeArgs[T] :
  T extends RefType<infer U> ? RefType<ApplyTypeArgs<TypeArgs, U>> :
  T extends ArrayType<infer U> ? ArrayType<ApplyTypeArgs<TypeArgs, U>> :
  T extends SetType<infer U> ? SetType<ApplyTypeArgs<TypeArgs, U>> :
  T extends DictType<infer K, infer V> ? DictType<ApplyTypeArgs<TypeArgs, K>, ApplyTypeArgs<TypeArgs, V>> :
  T extends StructType<infer Fields> ? StructType<{ [K in keyof Fields]: ApplyTypeArgs<TypeArgs, Fields[K]> }> :
  T extends RecursiveType<infer U> ? RecursiveType<ApplyTypeArgs<TypeArgs, U>> :
  T extends VariantType<infer Options> ? VariantType<{ [K in keyof Options]: ApplyTypeArgs<TypeArgs, Options[K]> }> :
  T extends RecursiveTypeMarker ? T :  // Self-reference - leave alone
  T extends FunctionType<infer Ins, infer Out> ? FunctionType<
    { [K in keyof Ins]: ApplyTypeArgs<TypeArgs, Ins[K]> },
    ApplyTypeArgs<TypeArgs, Out>
  > :
  T;
```

#### Runtime `applyTypeArgs` Function

The runtime counterpart applies type substitution to actual type values:

```typescript
function applyTypeArgs<TypeArgs extends Record<string, EastType>, T extends EastType | string>(
  typeArgs: TypeArgs,
  t: T
): ApplyTypeArgs<TypeArgs, T> {
  if (typeof t === 'string') {
    const ret = typeArgs[t];
    if (ret === undefined) {
      throw new Error(`Unexpected type argument ${t}`);
    }
    return ret as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Array") {
    return { type: "Array", value: applyTypeArgs(typeArgs, t.value) } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Struct") {
    const newFields: any = {};
    for (const k in t.fields) {
      newFields[k] = applyTypeArgs(typeArgs, t.fields[k]);
    }
    return { type: "Struct", fields: newFields } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Recursive") {
    if (t.node === undefined) {
      // RecursiveTypeMarker (self-reference) - leave alone
      return t as ApplyTypeArgs<TypeArgs, T>;
    }
    return { type: "Recursive", node: applyTypeArgs(typeArgs, t.node) } as ApplyTypeArgs<TypeArgs, T>;
  }
  // ... handle other type constructors
  return t as ApplyTypeArgs<TypeArgs, T>;
}
```

#### Callable Type Definition

```typescript
type GenericPlatformCallable<
  TParams extends readonly string[],
  Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
> = <TypeArgs extends { [K in keyof TParams]: EastType }>(
  type_args: TypeArgs,
  ...args: { [K in keyof Inputs]: SubtypeExprOrValue<ApplyTypeArgs<
    { [P in TParams[number]]: TypeArgs[P & keyof TypeArgs] },
    Inputs[K]
  >> }
) => ExprType<ApplyTypeArgs<{ [P in TParams[number]]: TypeArgs[P & keyof TypeArgs] }, Output>>;
```

#### Example: Type Safety in Action

```typescript
// Define log: forall T. T -> Null
const log = genericPlatform(
  "log",
  ["T"],
  ["T"],      // Input is type parameter T
  NullType
);

declare const stringExpr: Expr<StringType>;
declare const intExpr: Expr<IntegerType>;

// Good: types match
log([StringType], stringExpr);  // OK

// Bad: type mismatch - TypeScript ERROR
log([StringType], intExpr);
// Error: Argument of type 'Expr<IntegerType>' is not assignable to
//        parameter of type 'SubtypeExprOrValue<StringType>'
```

#### Multiple Type Parameters

```typescript
// Define map: forall T U. (T, T -> U) -> U
const map = genericPlatform(
  "map",
  ["T", "U"],
  ["T", FunctionType(["T"], "U")],  // Inputs: [T, Function<[T], U>]
  "U"
);

declare const strToIntFn: Expr<FunctionType<[StringType], IntegerType>>;
declare const intToStrFn: Expr<FunctionType<[IntegerType], StringType>>;

// Good: all types match
map([StringType, IntegerType], stringExpr, strToIntFn);  // OK

// Bad: wrong first arg type
map([StringType, IntegerType], intExpr, strToIntFn);  // ERROR

// Bad: wrong function type (output doesn't match U)
map([StringType, IntegerType], stringExpr, intToStrFn);  // ERROR
```

#### Return Type Inference

Return types are also correctly substituted:

```typescript
// wrap: forall T. T -> Array<T>
const wrap = genericPlatform(
  "wrap",
  ["T"],
  ["T"],
  ArrayType("T")  // String placeholder in output type constructor
);

// Return type is correctly inferred as ExprType<ArrayType<IntegerType>>
const wrapped = wrap([IntegerType], intExpr);
const _typeCheck: ExprType<ArrayType<IntegerType>> = wrapped;  // OK
```

### Calling Convention

When calling a generic platform function, type arguments are passed as an array first, followed by value arguments:

```
genericPlatformFn([Type1, Type2, ..., TypeN], arg1, arg2, ..., argM)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^
                  N type parameters (array)     M value arguments
```

### `.implement` Method

The implementation receives type parameters as a factory function. The factory can optionally have typed value arguments using `ValueTypeOf<ApplyTypeArgs<...>>`:

```typescript
type GenericPlatformDefinition<
  TParams extends readonly string[],
  Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
> = GenericPlatformCallable<TParams, Inputs, Output> & {
  implement: <TypeArgs extends { [K in keyof TParams]: EastType }>(
    factory: (...type_args: TypeArgs) =>
      (...args: { [K in keyof Inputs]: ValueTypeOf<ApplyTypeArgs<
        { [P in TParams[number]]: TypeArgs[P & keyof TypeArgs] },
        Inputs[K]
      >> }) => ValueTypeOf<ApplyTypeArgs<{ [P in TParams[number]]: TypeArgs[P & keyof TypeArgs] }, Output>>
  ) => PlatformFunction;
};
```

**Usage:**

```typescript
const log = genericPlatform(
  "log",
  ["T"],
  ["T"],
  NullType
);

// Implementation receives type params, returns the actual evaluator
const log_platform: PlatformFunction = log.implement((T) => (value) => {
  const print = printFor(T);
  const str = print(value);
  console.log(str);
  return null;
});

// Multiple type params:
const alns_platform: PlatformFunction = alns_optimize.implement((S) => (
  initial_solution,
  objective,
  destroy_operators,
  repair_operators,
  config
) => {
  // ALNS implementation with access to S type...
  return { solution: initial_solution };
});
```

This mirrors the `builtin_evaluators` pattern in `compile.ts`:

```typescript
// From compile.ts
Print: (_location, _platformDef, T: EastTypeValue) => {
  return printFor(T);
},
```

## IR Changes

### PlatformIR

Add `type_parameters` field to `PlatformIR` in `src/ir.ts`:

```typescript
// After:
export type PlatformIR = variant<"Platform", {
  type: EastTypeValue,
  location: LocationValue,
  name: string,
  type_parameters: EastTypeValue[],  // NEW - mirrors BuiltinIR
  arguments: any[], // IR[]
  async: boolean,
}>;
```

For reference, `BuiltinIR` already has this field:
```typescript
export type BuiltinIR = variant<"Builtin", {
  type: EastTypeValue,
  location: LocationValue,
  builtin: BuiltinName,
  type_parameters: EastTypeValue[],  // <-- We mirror this
  arguments: any[], // IR[]
}>;
```

### PlatformAST

Add `type_parameters` field to `PlatformAST` in `src/ast.ts`:

```typescript
// After:
export type PlatformAST = {
  ast_type: "Platform",
  type: EastType,
  location: Location,
  name: string,
  type_parameters: EastType[],  // NEW
  arguments: AST[],
  async: boolean,
};
```

## Platform Function Definition Changes

### PlatformFunction Type

Update `PlatformFunction` in `src/platform.ts`:

```typescript
export type PlatformFunction = {
  name: string,
  inputs: EastTypeValue[],
  output: EastTypeValue,
  type: 'sync' | 'async',
  fn: (...args: any) => any;
  // NEW fields for generic platform functions:
  type_parameters?: string[];  // ["T", "U"] or undefined for non-generic
  inputsFn?: (...typeParams: EastTypeValue[]) => EastTypeValue[];
  outputFn?: (...typeParams: EastTypeValue[]) => EastTypeValue;
}
```

For non-generic platform functions:
- `type_parameters` is undefined or `[]`
- `inputs`/`output` are concrete `EastTypeValue`
- `fn` is the evaluator directly

For generic platform functions:
- `type_parameters` contains the parameter names (for error messages and debugging)
- `inputsFn`/`outputFn` compute concrete types from resolved type params
- `fn` is a factory that receives type params and returns the evaluator

## Expression Layer Changes

### `src/expr/block.ts`

#### `genericPlatform` Function

```typescript
function genericPlatform<
  const TParams extends readonly string[],
  const Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
>(
  name: string,
  typeParams: TParams,
  inputs: Inputs,
  output: Output
): GenericPlatformDefinition<TParams, Inputs, Output> {
  const fn = ((
    type_args: EastType[],
    ...args: unknown[]
  ) => {
    // Map type parameters to provided types
    const typeArgMap: Record<string, EastType> = {};
    typeParams.forEach((param, idx) => {
      typeArgMap[param] = type_args[idx]!;
    });

    // Apply type substitution to get concrete input/output types
    const input_types = inputs.map(t => applyTypeArgs(typeArgMap, t));
    const output_type = applyTypeArgs(typeArgMap, output);

    // Convert value arguments to AST
    const arg_asts: AST[] = [];
    for (let i = 0; i < args.length; i++) {
      const expected_type = input_types[i]!;
      const expr = Expr.from(args[i], expected_type);
      arg_asts.push(Expr.ast(expr));
    }

    // Create AST node
    return fromAst({
      ast_type: "Platform",
      type: output_type,
      location: get_location(2),
      name,
      type_parameters: type_args,
      arguments: arg_asts,
      async: false,
    });
  }) as unknown as GenericPlatformDefinition<TParams, Inputs, Output>;

  // Add .implement method
  (fn as any).implement = (
    factory: (...typeParams: any[]) => (...args: any[]) => any
  ): PlatformFunction => {
    return {
      name,
      type_parameters: [...typeParams],
      inputs: [],  // Computed at call time via inputsFn
      output: toEastTypeValue(NullType),  // Placeholder
      type: 'sync' as const,
      fn: factory,
      inputsFn: (...tps: EastTypeValue[]) => {
        const typeArgMap: Record<string, EastTypeValue> = {};
        typeParams.forEach((param, idx) => {
          typeArgMap[param] = tps[idx]!;
        });
        return inputs.map(t =>
          typeof t === 'string' ? typeArgMap[t]! : toEastTypeValue(applyTypeArgs(typeArgMap as any, t))
        );
      },
      outputsFn: (...tps: EastTypeValue[]) => {
        const typeArgMap: Record<string, EastTypeValue> = {};
        typeParams.forEach((param, idx) => {
          typeArgMap[param] = tps[idx]!;
        });
        return typeof output === 'string'
          ? typeArgMap[output]!
          : toEastTypeValue(applyTypeArgs(typeArgMap as any, output));
      },
    };
  };

  return fn;
}
```

#### `asyncGenericPlatform`

Async variant follows the same pattern but sets `async: true` in the AST:

```typescript
function asyncGenericPlatform<
  const TParams extends readonly string[],
  const Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
>(
  name: string,
  typeParams: TParams,
  inputs: Inputs,
  output: Output
): AsyncGenericPlatformDefinition<TParams, Inputs, Output>
```

## AST to IR Conversion

Update `src/ast_to_ir.ts` Platform handling:

```typescript
} else if (ast.ast_type === "Platform") {
  if (ctx.async === false && ast.async === true) {
    throw new Error(`Async platform call not allowed outside async function at ${printLocation(ast.location)}`);
  }

  // Convert type parameters from EastType to EastTypeValue
  const typeParamsIR = (ast.type_parameters ?? []).map(tp => toEastTypeValue(tp));

  return variant("Platform", {
    type: toEastTypeValue(ast.type),
    location: toLocationValue(ast.location),
    name: ast.name,
    type_parameters: typeParamsIR,  // NEW
    arguments: ast.arguments.map(ast => ast_to_ir(ast, ctx)),
    async: ast.async,
  });
}
```

## Analysis Phase

### PlatformDefinition Type

Update `PlatformDefinition` in `src/analyze.ts`:

```typescript
export type PlatformDefinition = {
  name: string,
  inputs: EastTypeValue[],
  output: EastTypeValue,
  type: 'sync' | 'async',
  // NEW fields for generic platform functions:
  type_parameters?: string[];
  inputsFn?: (...typeParams: EastTypeValue[]) => EastTypeValue[];
  outputFn?: (...typeParams: EastTypeValue[]) => EastTypeValue;
};
```

### Platform Handling

Update `src/analyze.ts` Platform handling:

```typescript
else if (node.type === "Platform") {
  const platformFn = platformMap.get(node.value.name);
  if (!platformFn) {
    throw new Error(`Platform function '${node.value.name}' not found ...`);
  }

  // Handle generic platform functions
  const typeParams = node.value.type_parameters ?? [];
  const expectedTypeParamCount = platformFn.type_parameters?.length ?? 0;

  if (typeParams.length !== expectedTypeParamCount) {
    throw new Error(
      `Platform function '${node.value.name}' expects ${expectedTypeParamCount} ` +
      `type parameters, got ${typeParams.length}`
    );
  }

  // Compute concrete input/output types by substituting type parameters
  let inputTypes: EastTypeValue[];
  let outputType: EastTypeValue;

  if (expectedTypeParamCount > 0 && platformFn.inputsFn && platformFn.outputFn) {
    // Generic platform function - use callbacks to compute types
    inputTypes = platformFn.inputsFn(...typeParams);
    outputType = platformFn.outputFn(...typeParams);
  } else {
    // Non-generic - use stored concrete types
    inputTypes = platformFn.inputs;
    outputType = platformFn.output;
  }

  // Validate argument count and types using computed inputTypes/outputType
  // ...
}
```

## Compilation Phase

Update `src/compile.ts` Platform handling:

```typescript
} else if (ir.type === "Platform") {
  // ... compile arguments ...

  // Look up platform function definition to check if generic
  const platformFn = platformDef.find(p => p.name === ir.value.name);
  if (!platformFn) {
    throw new Error(`Platform function '${ir.value.name}' not found`);
  }

  // Get evaluator - for generic functions, call factory with type params
  let evaluator: (...args: any[]) => any;
  const typeParams = ir.value.type_parameters ?? [];

  if (typeParams.length > 0 && platformFn.type_parameters?.length) {
    // Generic platform function - fn is a factory that takes type params
    evaluator = platformFn.fn(...typeParams);
  } else {
    // Non-generic - fn is the evaluator directly
    evaluator = platform[ir.value.name];
  }

  // ... apply evaluator to arguments ...
}
```

## Backwards Compatibility

### Non-Generic Platform Functions

The existing `East.platform` function remains unchanged. Non-generic platform functions have:
- `type_parameters: []` (empty array)
- `inputs`/`output` as concrete `EastTypeValue[]`/`EastTypeValue`
- `fn` as the direct evaluator (not a factory)

### IR Compatibility

The `type_parameters` field is added to `PlatformIR`. For backwards compatibility:
- When reading IR without `type_parameters`, default to `[]`
- The field is always written (even if empty) for new IR

## File Changes Summary

| File | Changes |
|------|---------|
| `src/ir.ts` | Add `type_parameters: EastTypeValue[]` to `PlatformIR` |
| `src/ast.ts` | Add `type_parameters: EastType[]` to `PlatformAST` |
| `src/platform.ts` | Update `PlatformFunction` with `type_parameters`, `inputsFn`, `outputFn` |
| `src/analyze.ts` | Update `PlatformDefinition`; validate generic platform calls |
| `src/ast_to_ir.ts` | Convert `type_parameters` from EastType to EastTypeValue |
| `src/compile.ts` | Call factory with type params for generic platform functions |
| `src/expr/block.ts` | Add `ApplyTypeArgs`, `applyTypeArgs`, `genericPlatform`, `asyncGenericPlatform` |
| `src/expr/index.ts` | Export `genericPlatform`, `asyncGenericPlatform`; add to `East` object |

## Test Plan

### Unit Tests (`src/platform.spec.ts`)

```typescript
describe("genericPlatform", () => {
  test("can define a generic log function with 1 type parameter", () => {
    const log = East.genericPlatform(
      "log",
      ["T"],
      ["T"],
      NullType
    );

    let logged: { type: EastTypeValue, value: unknown } | undefined;
    const platform = [
      log.implement((T: EastTypeValue) => (value: unknown) => {
        logged = { type: T, value };
        return null;
      }),
    ];

    const f = East.function([IntegerType], NullType, ($, input) => {
      $(log([IntegerType], input));
      $.return(null);
    });

    const f_compiled = East.compile(f, platform);
    f_compiled(42n);

    assert.strictEqual(logged.value, 42n);
    assert.strictEqual(logged.type.type, "Integer");
  });

  test("can define a generic function with computed output type", () => {
    const wrap = East.genericPlatform(
      "wrap",
      ["T"],
      ["T"],
      ArrayType("T")
    );

    const platform = [
      wrap.implement((_T: EastTypeValue) => (value: unknown) => [value]),
    ];

    const f = East.function([IntegerType], ArrayType(IntegerType), ($, input) => {
      $.return(wrap([IntegerType], input));
    });

    const f_compiled = East.compile(f, platform);
    const result = f_compiled(42n);

    assert.deepStrictEqual(result, [42n]);
  });

  test("can define a generic function with 2 type parameters", () => {
    const pair = East.genericPlatform(
      "pair",
      ["A", "B"],
      ["A", "B"],
      StructType({ first: "A", second: "B" })
    );

    const platform = [
      pair.implement((_A, _B) => (a, b) => ({ first: a, second: b })),
    ];

    const f = East.function(
      [IntegerType, StringType],
      StructType({ first: IntegerType, second: StringType }),
      ($, a, b) => {
        $.return(pair([IntegerType, StringType], a, b));
      }
    );

    const f_compiled = East.compile(f, platform);
    const result = f_compiled(42n, "hello");

    assert.deepStrictEqual(result, { first: 42n, second: "hello" });
  });
});
```

## Resolved Design Decisions

1. **String placeholders vs branded placeholder types**
   - **Decision**: Use string literals like `"T"`, `"U"` directly in input/output definitions
   - **Rationale**: Simpler API, more readable, and `ApplyTypeArgs` handles substitution cleanly

2. **Type args passing convention**
   - **Decision**: Type args passed as a single array: `log([StringType], value)`
   - **Rationale**: Clearer separation between type args and value args; matches IR representation

3. **Typed `.implement` method**
   - **Decision**: Use `ValueTypeOf<ApplyTypeArgs<...>>` for typed value parameters
   - **Rationale**: Provides better type safety in implementations when the type args are known

4. **`const` type parameter modifier**
   - **Decision**: Use `const` modifier (TypeScript 5.0+) to eliminate `as const` requirement
   - **Rationale**: Better ergonomics - `["T"]` infers as `readonly ["T"]` not `string[]`

## Open Questions

1. **Should non-generic platform functions also use the callback pattern?**
   - Current decision: Keep both APIs (`platform` for simple, `genericPlatform` for generic)

2. **Should we support type constraints?**
   - Current decision: No, keep it simple

3. **Should type parameters be named or positional?**
   - Current decision: Named (like `["T", "U"]`) for clarity and error messages
