// Experimenting with type-safe generic platform functions
// Using MAPPED TYPES approach - single variadic function

import type {
  EastType,
  NullType,
  IntegerType,
  StringType,
  FloatType,
  ArrayType,
  FunctionType,
} from "../src/types.js";

import {
  NullType as NullTypeValue,
  IntegerType as IntegerTypeValue,
  StringType as StringTypeValue,
  FloatType as FloatTypeValue,
  FunctionType as FunctionTypeConstructor,
  ArrayType as ArrayTypeConstructor,
} from "../src/types.js";

import type { Expr } from "../src/expr/expr.js";
import type { ExprType, SubtypeExprOrValue } from "../src/expr/types.js";
import type { EastTypeValue } from "../src/type_of_type.js";

// =============================================================================
// PLATFORM FUNCTION TYPE (returned by .implement)
// =============================================================================

type PlatformFunction = {
  name: string;
  inputs: EastTypeValue[];
  output: EastTypeValue;
  type: 'sync' | 'async';
  fn: (...args: unknown[]) => unknown;
  type_parameters?: string[];
  inputsFn?: (...typeParams: EastTypeValue[]) => EastTypeValue[];
  outputsFn?: (...typeParams: EastTypeValue[]) => EastTypeValue;
};

// =============================================================================
// MAPPED TYPE APPROACH: Indexed placeholders
//
// Instead of fixed T_, U_, V_ types, we create placeholders branded by index.
// This allows a single genericPlatform function that works with any arity.
// =============================================================================

// Placeholder type branded by its index position
declare const PlaceholderBrand: unique symbol;
type Placeholder<K extends PropertyKey> = EastType & {
  readonly [PlaceholderBrand]: K
};

// Create placeholder values for runtime - these are strings like "T1", "T2"
function createPlaceholder<K extends PropertyKey>(index: K): Placeholder<K> {
  return `T${Number(index) + 1}` as unknown as Placeholder<K>;
}

// Map type params array to placeholder types
type Placeholders<TParams extends readonly string[]> = {
  [K in keyof TParams]: TParams[K] extends string ? Placeholder<K> : never
};

// Create runtime placeholder values from type params
function createPlaceholders<TParams extends readonly string[]>(
  typeParams: TParams
): Placeholders<TParams> {
  return typeParams.map((_, i) => createPlaceholder(i)) as Placeholders<TParams>;
}

// =============================================================================
// Substitution: Replace Placeholder<K> with ActualTypes[K]
// =============================================================================

// Substitute all placeholders with actual types from the tuple
type SubstituteAll<Type, ActualTypes extends readonly EastType[]> =
  [Type] extends [Placeholder<infer K>]
    ? K extends keyof ActualTypes
      ? ActualTypes[K]
      : Type
    : [Type] extends [FunctionType<infer I extends EastType[], infer O extends EastType>]
      ? FunctionType<SubstituteAllArray<I, ActualTypes>, SubstituteAll<O, ActualTypes>>
      : [Type] extends [ArrayType<infer E extends EastType>]
        ? ArrayType<SubstituteAll<E, ActualTypes>>
        : Type;

type SubstituteAllArray<Types extends readonly EastType[], ActualTypes extends readonly EastType[]> = {
  [K in keyof Types]: Types[K] extends EastType ? SubstituteAll<Types[K], ActualTypes> : never
};

// Map to SubtypeExprOrValue
type ToExprArgs<Types extends readonly EastType[]> = {
  [K in keyof Types]: Types[K] extends EastType ? SubtypeExprOrValue<Types[K]> : never
};

// =============================================================================
// The single genericPlatform function
// =============================================================================

type GenericPlatformCallable<
  TParams extends readonly string[],
  Inputs extends readonly EastType[],
  Output extends EastType
> = <ActualTypes extends { [K in keyof TParams]: EastType }>(
  ...args: [...ActualTypes, ...ToExprArgs<SubstituteAllArray<Inputs, ActualTypes>>]
) => ExprType<SubstituteAll<Output, ActualTypes>>;

/** Definition for a generic platform function with `.implement` method.
 *
 * The `implement` method receives a factory function where:
 * - Type parameters are `EastTypeValue` (the runtime representation of types)
 * - Value arguments are `unknown` (cast to specific types as needed based on the type parameters)
 */
type GenericPlatformDefinition<
  TParams extends readonly string[],
  Inputs extends readonly EastType[],
  Output extends EastType
> = GenericPlatformCallable<TParams, Inputs, Output> & {
  implement: (
    factory: (...typeParams: { [K in keyof TParams]: EastTypeValue }) =>
      (...args: unknown[]) => unknown
  ) => PlatformFunction;
};

function genericPlatform<
  const TParams extends readonly string[],
  const Inputs extends readonly EastType[],
  Output extends EastType
>(
  name: string,
  typeParams: TParams,
  inputsFn: (...placeholders: Placeholders<TParams>) => Inputs,
  outputFn: (...placeholders: Placeholders<TParams>) => Output
): GenericPlatformDefinition<TParams, Inputs, Output> {
  const placeholders = createPlaceholders(typeParams);

  // The callable (for use in East code)
  const fn = ((..._args: unknown[]) => {
    // Would create AST node here
    return {} as any;
  }) as unknown as GenericPlatformDefinition<TParams, Inputs, Output>;

  // Add .implement method
  (fn as any).implement = (
    factory: (...typeParams: any[]) => (...args: any[]) => any
  ): PlatformFunction => {
    const templateInputs = inputsFn(...placeholders);
    const templateOutput = outputFn(...placeholders);

    // Helper to substitute placeholder with actual type
    const substitute = (t: EastType, actualTypes: EastTypeValue[]): EastTypeValue => {
      // Placeholders are strings like "T1", "T2" at runtime
      if (typeof t === 'string' && (t as string).match(/^T\d+$/)) {
        const idx = parseInt((t as string).slice(1)) - 1;
        return actualTypes[idx] ?? t as unknown as EastTypeValue;
      }
      return t as unknown as EastTypeValue;
    };

    return {
      name,
      type_parameters: [...typeParams],
      inputs: [],
      output: { type: "Null", value: null } as EastTypeValue,
      type: 'sync',
      fn: factory,
      inputsFn: (...actualTypes: EastTypeValue[]) => {
        return templateInputs.map(t => substitute(t, actualTypes));
      },
      outputsFn: (...actualTypes: EastTypeValue[]) => {
        return substitute(templateOutput, actualTypes);
      },
    };
  };

  return fn;
}

// =============================================================================
// TEST
// =============================================================================

// Define log: (T) => [T] -> Null
const log = genericPlatform(
  "log",
  ["T"],
  (t) => [t],
  (_t) => NullTypeValue
);

// Define map: (T, U) => [T, (T) -> U] -> U
const map = genericPlatform(
  "map",
  ["T", "U"],
  (t, u) => [t, FunctionTypeConstructor([t], u)],
  (_t, u) => u
);

// Define wrap: (T) => [T] -> Array<T>
const wrap = genericPlatform(
  "wrap",
  ["T"],
  (t) => [t],
  (t) => ArrayTypeConstructor(t)
);

// =============================================================================
// TEST TYPE SAFETY
// =============================================================================

declare const stringExpr: Expr<StringType>;
declare const intExpr: Expr<IntegerType>;
declare const floatExpr: Expr<FloatType>;
declare const strToIntFn: Expr<FunctionType<[StringType], IntegerType>>;
declare const intToStrFn: Expr<FunctionType<[IntegerType], StringType>>;
declare const intToIntFn: Expr<FunctionType<[IntegerType], IntegerType>>;

// ----- LOG TESTS -----

// Good: log(StringType, stringExpr)
const log_good = log(StringTypeValue, stringExpr);

// Bad: log(StringType, intExpr) - should error
// @ts-expect-error - intExpr is not compatible with StringType
const log_bad = log(StringTypeValue, intExpr);

// ----- MAP TESTS -----

// Good: map(String, Int, stringExpr, String->Int fn)
const map_good = map(StringTypeValue, IntegerTypeValue, stringExpr, strToIntFn);

// Bad: wrong first arg
// @ts-expect-error - first arg should be string, not int
const map_bad1 = map(StringTypeValue, IntegerTypeValue, intExpr, strToIntFn);

// Bad: wrong function type
// @ts-expect-error - function should be String->Int, not Int->String
const map_bad2 = map(StringTypeValue, IntegerTypeValue, stringExpr, intToStrFn);

// Bad: function input doesn't match T
// @ts-expect-error - function input should be String (T), not Int
const map_bad3 = map(StringTypeValue, IntegerTypeValue, stringExpr, intToIntFn);

// ----- WRAP TESTS -----

// Good: wrap(Int, intExpr) -> Array<Int>
const wrap_good = wrap(IntegerTypeValue, intExpr);

// Bad: wrap(Int, stringExpr) - should error
// @ts-expect-error - stringExpr not compatible with IntegerType
const wrap_bad = wrap(IntegerTypeValue, stringExpr);

// ----- CHECK RETURN TYPES -----

// log should return ExprType<NullType>
const log_return: ExprType<NullType> = log(StringTypeValue, stringExpr);

// map(String, Int, ...) should return ExprType<IntegerType> (U)
const map_return: ExprType<IntegerType> = map(StringTypeValue, IntegerTypeValue, stringExpr, strToIntFn);

// wrap(Int, ...) should return ExprType<ArrayType<IntegerType>>
const wrap_return: ExprType<ArrayType<IntegerType>> = wrap(IntegerTypeValue, intExpr);

// =============================================================================
// TEST .implement
// =============================================================================

// Implementation for log - receives type param, returns function that handles value
const logImpl = log.implement(
  (T: EastTypeValue) => (value: unknown) => {
    console.log(`[${T.type}] ${value}`);
    return null;
  }
);

// Implementation for wrap - wraps value in array
const wrapImpl = wrap.implement(
  (_T: EastTypeValue) => (value: unknown) => {
    return [value];
  }
);

// Implementation for map - applies function to value
const mapImpl = map.implement(
  (_T: EastTypeValue, _U: EastTypeValue) => (value: unknown, fn: unknown) => {
    return (fn as (v: unknown) => unknown)(value);
  }
);

// These would be passed to East.compile():
const _platform = [logImpl, wrapImpl, mapImpl];

console.log("Mapped type approach - check for ts-expect-error warnings above");
