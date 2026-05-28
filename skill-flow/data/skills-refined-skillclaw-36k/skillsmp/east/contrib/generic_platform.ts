import {
  type EastType,
  type RefType,
  type SetType,
  type DictType,
  type VariantType,
  type ValueTypeOf,
  type RecursiveType,
  type RecursiveTypeMarker,
  ArrayType,
  FunctionType,
  StringType,
  NullType,
  FloatType,
  StructType,
  IntegerType,
} from "../src/types.js";

import type { ExprType, SubtypeExprOrValue } from "../src/expr/types.js";
import type { EastTypeValue } from "../src/type_of_type.js";
import { Expr, get_location, printFor } from "../src/index.js";

// =============================================================================
// PLATFORM FUNCTION TYPE (returned by .implement)
// =============================================================================

type PlatformFunction = {
  name: string;
  inputs: EastTypeValue[];
  output: EastTypeValue;
  type: 'sync' | 'async';
  fn: (...args: unknown[]) => unknown;
  type_parameters: string[];
  inputsFn?: (typeParams: Map<string, EastTypeValue>) => EastTypeValue[];
  outputsFn?: (typeParams: Map<string, EastTypeValue>) => EastTypeValue;
};

// =============================================================================
// GENERIC PLATFORM DEFINITION TYPE (returned by genericPlatform)
// =============================================================================

// Helper to find index of a string in a tuple
type IndexOf<T extends readonly string[], S extends string, Acc extends unknown[] = []> =
  T extends readonly [infer First, ...infer Rest extends readonly string[]]
    ? First extends S
      ? Acc['length']
      : IndexOf<Rest, S, [...Acc, unknown]>
    : never;

// Helper type to zip parameter names with type arguments into a record
// E.g., ZipToRecord<["A", "B"], [IntegerType, StringType]> = { A: IntegerType, B: StringType }
type ZipToRecord<Names extends readonly string[], Types extends readonly unknown[]> = {
  [K in Names[number]]: Types[IndexOf<Names, K>]
};

type ApplyTypeArgs<TypeArgs extends Record<string, EastType>, T> =
  T extends keyof TypeArgs ? TypeArgs[T] :
  T extends RefType<infer U> ? RefType<ApplyTypeArgs<TypeArgs, U>> :
  T extends ArrayType<infer U> ? ArrayType<ApplyTypeArgs<TypeArgs, U>> :
  T extends SetType<infer U> ? SetType<ApplyTypeArgs<TypeArgs, U>> :
  T extends DictType<infer K, infer V> ? DictType<ApplyTypeArgs<TypeArgs, K>, ApplyTypeArgs<TypeArgs, V>> :
  T extends StructType<infer Fields> ? StructType<{ [K in keyof Fields]: ApplyTypeArgs<TypeArgs, Fields[K]> }> :
  // RecursiveType must be checked BEFORE VariantType to preserve the wrapper
  T extends RecursiveType<infer U> ? RecursiveType<ApplyTypeArgs<TypeArgs, U>> :
  T extends VariantType<infer Options> ? VariantType<{ [K in keyof Options]: ApplyTypeArgs<TypeArgs, Options[K]> }> :
  T extends RecursiveTypeMarker ? T : // Self-reference - leave alone
  T extends FunctionType<infer Ins, infer Out> ? FunctionType<
    { [K in keyof Ins]: ApplyTypeArgs<TypeArgs, Ins[K]> },
    ApplyTypeArgs<TypeArgs, Out>
  > :
  T;

function applyTypeArgs<TypeArgs extends Record<string, EastType>, T extends EastType | string>(typeArgs: TypeArgs, t: T): ApplyTypeArgs<TypeArgs, T> {
  if (typeof t === 'string') {
    const ret = typeArgs[t];
    if (ret === undefined) {
      throw new Error(`Unexpected type argument ${t}`);
    }
    return ret as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Ref") {
    return { type: "Ref", value: applyTypeArgs(typeArgs, t.value) } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Array") {
    return { type: "Array", value: applyTypeArgs(typeArgs, t.value) } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Set") {
    return { type: "Set", key: applyTypeArgs(typeArgs, t.key) } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Dict") {
    return { type: "Dict", key: applyTypeArgs(typeArgs, t.key), value: applyTypeArgs(typeArgs, t.value) } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Struct") {
    const newFields: any = {};
    for (const k in t.fields) {
      newFields[k] = applyTypeArgs(typeArgs, t.fields[k]);
    }
    return { type: "Struct", fields: newFields } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Variant") {
    const newCases: any = {};
    for (const k in t.cases) {
      newCases[k] = applyTypeArgs(typeArgs, t.cases[k]);
    }
    return { type: "Variant", cases: newCases } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Function") {
    const newInputs = t.inputs.map(inputType => applyTypeArgs(typeArgs, inputType));
    const newOutput = applyTypeArgs(typeArgs, t.output);
    return { type: "Function", inputs: newInputs, output: newOutput } as ApplyTypeArgs<TypeArgs, T>;
  } else if (t.type === "Recursive") {
    // RecursiveType - recurse into the inner node, preserving the wrapper
    if (t.node === undefined) {
      // This is a RecursiveTypeMarker (self-reference) - leave it alone
      return t as ApplyTypeArgs<TypeArgs, T>;
    }
    return { type: "Recursive", node: applyTypeArgs(typeArgs, t.node) } as ApplyTypeArgs<TypeArgs, T>;
  } else {
    return t as ApplyTypeArgs<TypeArgs, T>;
  }
}

type GenericPlatformCallable<
  TParams extends readonly string[],
  Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
> = <TypeArgs extends readonly EastType[] & { [K in keyof TParams]: EastType }>(
  type_args: TypeArgs,
  ...args: { [K in keyof Inputs]: SubtypeExprOrValue<ApplyTypeArgs<
    ZipToRecord<TParams, TypeArgs>,
    Inputs[K]
  >> }
) => ExprType<ApplyTypeArgs<ZipToRecord<TParams, TypeArgs>, Output>>;


/** Definition for a generic platform function with `.implement` method.
*
* The `implement` method receives a factory function where:
* - Type parameters are `EastTypeValue` (the runtime representation of types)
* - Value arguments are `unknown` (cast to specific types as needed based on the type parameters)
*/
type GenericPlatformDefinition<
  TParams extends readonly string[],
  Inputs extends readonly (EastType | string)[],
  Output extends EastType | string
> = GenericPlatformCallable<TParams, Inputs, Output> & {
  implement: (
    factory: (...type_args: { [K in keyof TParams]: EastTypeValue }) =>
      (...args: unknown[]) => unknown
  ) => PlatformFunction;
};

// =============================================================================
// GENERIC PLATFORM DEFINITION FUNCTION
// =============================================================================

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
  // The callable (for use in East code)
  const fn = ((
    type_args: EastType[],
    ...args: unknown[]
  ) => {
    // Map type parameters to provided types
    const typeArgMap: Record<string, EastType> = {};
    typeParams.forEach((param, idx) => {
      typeArgMap[param] = type_args[idx]!;
    });

    const input_types: any[] = inputs.map((t: any) => (applyTypeArgs as any)(typeArgMap, t));
    const output_type: any = applyTypeArgs(typeArgMap, output);

    // Process value arguments (args) as needed
    const arg_asts: any[] = [];
    for (let i = 0; i < args.length; i++) {
      const expected_type = input_types[i];
      const expr = Expr.from(args[i], expected_type);
      arg_asts.push(Expr.ast(expr));
    }

    // Create AST node here
    return {
      ast_type: "Platform",
      type: output_type,
      location: get_location(),
      name,
      arguments: arg_asts,
      async: false,
    } as any;
  }) as unknown as GenericPlatformDefinition<TParams, Inputs, Output>;
  
  // Add .implement method
  (fn as any).implement = (
    factory: (...typeParams: any[]) => (...args: any[]) => any
  ): PlatformFunction => {
    throw new Error("TODO")
  };
  
  return fn;
}

// =============================================================================
// Example: log
// =============================================================================

const log = genericPlatform(
  "log",
  ["T1"],
  ["T1"],
  NullType
);

const log_platform: PlatformFunction = log.implement((T1) => (value) => {
  const print = printFor(T1);
  const str = print(value);
  console.log(str);
  return null;
});

const log_expr = log(
  // type arguments (as array)
  [ArrayType(StringType)],
  // value arguments (one at a time)
  ["Hello, East!"]
);


// =============================================================================
// Example alns
// =============================================================================

const ALNSConfigType = StructType({
  max_iterations: IntegerType,
  // config fields...
});

function ALNSResultType<S>(s: S) {
  return StructType({
    solution: s,
  });
}

const alns_optimize = genericPlatform(
  "alns_optimize",
  ["S"],
  [
    "S",                                 // initial_solution: S
    FunctionType(["S"], FloatType),      // objective: S -> Float
    ArrayType(FunctionType(["S"], "S")), // destroy_operators: Array<S -> S>
    ArrayType(FunctionType(["S"], "S")), // repair_operators: Array<S -> S>
    ALNSConfigType,
  ],
  StructType({
    solution: ["S"],
  })
);

const s = ArrayType(IntegerType);
const optimize_expr = alns_optimize(
  // type arguments (as array)
  [s],
  // value arguments (one at a time)
  [1n, 2n, 3n],
  ($, sol) => sol.sum().toFloat(),
  [
    ($, sol) => {
      $(sol.update(0n, sol.get(0n).add(1n)));
      $.return(sol);
    },
    // ...
  ],
  [
    ($, sol) => {
      $(sol.update(0n, sol.get(0n).subtract(1n)));
      $.return(sol);
    },
    // ...
  ],
  {
    max_iterations: 1000n,
    // config fields...
  }
);

const alns_platform: PlatformFunction = alns_optimize.implement((S) => (
  initial_solution,
  objective,
  destroy_operators,
  repair_operators,
  config
) => {
  // ALNS implementation...
  return {
    solution: initial_solution,
  };
});

// =============================================================================
// Example: pair (multi-type-parameter test)
// =============================================================================

const pair = genericPlatform(
  "pair",
  ["A", "B"],
  ["A", "B"],
  StructType({ first: "A", second: "B" })
);

// This should infer: StructType<{ first: IntegerType, second: StringType }>
// NOT: StructType<{ first: IntegerType | StringType, second: IntegerType | StringType }>
const pair_expr = pair(
  [IntegerType, StringType],
  42n,
  "hello"
);

// Type check: access the fields - if inference is correct, these should have distinct types
const _first = pair_expr.first;   // Should be IntegerExpr
const _second = pair_expr.second; // Should be StringExpr