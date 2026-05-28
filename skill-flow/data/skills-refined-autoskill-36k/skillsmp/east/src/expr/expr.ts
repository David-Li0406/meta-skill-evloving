/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import type { Location } from "../location.js";
import type { ExprType, TypeOf, SubtypeExprOrValue } from "./types.js";
import { type BooleanType, type StringType, type EastType, type NeverType, type StructType, ArrayType, FunctionType, IntegerType, VariantType, AsyncFunctionType } from "../types.js";
import type { BlockBuilder } from "./block.js";
import type { CallableFunctionExpr } from "./function.js";
import type { NeverExpr } from "./never.js";
import type { CallableAsyncFunctionExpr } from "./asyncfunction.js";

/**
 * Simple factory function type for creating expressions from AST
 */
export type ToExpr = <T extends AST>(ast: T, node_type?: any) => Expr<T["type"]>

export const TypeSymbol = Symbol("type");
export type TypeSymbol = typeof TypeSymbol;

export const AstSymbol = Symbol("ast");
export type AstSymbol = typeof AstSymbol;

export const FactorySymbol = Symbol("factory");
export type FactorySymbol = typeof FactorySymbol;

/**
 * Abstract base class for all East expressions
 * Contains core functionality that doesn't create new expressions
 */
export abstract class Expr<T = any> {
  /** @internal */
  // @ts-expect-error - we use defineProperty to set this in the constructor
  [TypeSymbol]: T;
  /** @internal */
  // @ts-expect-error - we use defineProperty to set this in the constructor
  [AstSymbol]: AST;
  /** @internal */
  // @ts-expect-error - we use defineProperty to set this in the constructor
  [FactorySymbol]: ToExpr;

  /** @internal */
  constructor(
    type: T,
    ast: AST,
    factory: ToExpr
  ) {
    // Make the properies not enumerable (so they don't appear in spreads - for StructExpr)
    Object.defineProperty(this, TypeSymbol, { enumerable: false, value: type });
    Object.defineProperty(this, AstSymbol, { enumerable: false, value: ast });
    Object.defineProperty(this, FactorySymbol, { enumerable: false, value: factory });
  }

  /** @internal */
  static type<T>(expr: Expr<T>): T {
    return expr[TypeSymbol];
  }

  /** @internal */
  static ast<T>(expr: Expr<T>): AST & { type: T } {
    return expr[AstSymbol] as AST & { type: T };
  }

  

  /** Create an expression from a JavaScript value (optionally providing the type). */
  static from<T>(value: SubtypeExprOrValue<NoInfer<T>>, type: T): ExprType<T>
  static from<T>(value: T): ExprType<TypeOf<T>>
  static from(value: any): Expr {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void value;
  }

  /** @internal Create an expression from an AST node. */
  static fromAst<T extends AST>(ast: T): ExprType<T["type"]> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void ast;
  }

  /** Create a block expression. */
  static block<F extends ($: BlockBuilder<NeverType>) => any>(body: F): ReturnType<F> extends void ? NeverExpr : ExprType<TypeOf<ReturnType<F>>> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void body;
  }

  /** Create an error expression. */
  static error(message: SubtypeExprOrValue<StringType>, location?: Location[]): ExprType<NeverType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void message; void location;
  }

  /** Create a match expression. */
  static match<Cases extends Record<string, any>, Handlers extends { [K in keyof Cases]: ($: BlockBuilder<NeverType>, data: ExprType<Cases[K]>) => any }>(variant: Expr<VariantType<Cases>>, handlers: Handlers): ExprType<TypeOf<{ [K in keyof Cases] : ReturnType<Handlers[K]> }[keyof Cases]>> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void variant; void handlers;
  }

  /** Create a try-catch expression. */
  static tryCatch<T>(try_body: Expr<T>, catch_body: ($: BlockBuilder<NeverType>, message: ExprType<StringType>, stack: ExprType<ArrayType<StructType<{ filename: StringType, line: IntegerType, column: IntegerType }>>>) => SubtypeExprOrValue<T>): ExprType<T> {
    // TODO do better job of merging types?
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void try_body; void catch_body;
  }

  /** Create a function expression. */
  /** @internal */
  static function<const I extends any[], F extends ($: BlockBuilder<NeverType>, ...inputs: { [K in keyof I]: ExprType<I[K]> }) => any>(input_types: I, output_type: undefined, body: F): CallableFunctionExpr<I, TypeOf<ReturnType<F> extends void ? NeverType : ReturnType<F>>>
  static function<const I extends any[], O>(input_types: I, output_type: O, body: ($: BlockBuilder<O>, ...inputs: { [K in keyof I]: ExprType<I[K]> }) => SubtypeExprOrValue<O> | void): CallableFunctionExpr<I, O>
  static function(_input_types: any[], _output_type: any, _body: any): Expr<FunctionType<any[], any>> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
  }

  /** Create a function expression. */
  /** @internal */
  static asyncFunction<const I extends any[], F extends ($: BlockBuilder<NeverType>, ...inputs: { [K in keyof I]: ExprType<I[K]> }) => any>(input_types: I, output_type: undefined, body: F): CallableAsyncFunctionExpr<I, TypeOf<ReturnType<F> extends void ? NeverType : ReturnType<F>>>
  static asyncFunction<const I extends any[], O>(input_types: I, output_type: O, body: ($: BlockBuilder<O>, ...inputs: { [K in keyof I]: ExprType<I[K]> }) => SubtypeExprOrValue<O> | void): CallableAsyncFunctionExpr<I, O>
  static asyncFunction(_input_types: any[], _output_type: any, _body: any): Expr<AsyncFunctionType<any[], any>> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
  }

  //
  // Standard library functions
  //

  /** Print an expression as a string. */
  static print(expr: any): ExprType<StringType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void expr;
  }

  /** Perform string interpolation. */
  static str(strings: TemplateStringsArray, ...expressions: Expr[]): ExprType<StringType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void strings; void expressions;
  }

  /** Test equality between two expressions. */
  static equal<T>(a: Expr<T>, b: SubtypeExprOrValue<T>): ExprType<BooleanType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void a; void b;
  }

  /** Test inequality between two expressions. */
  static notEqual<T>(a: Expr<T>, b: SubtypeExprOrValue<T>): ExprType<BooleanType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void a; void b;
  }

  /** Test if first expression is less than second. */
  static less<T>(a: Expr<T>, b: SubtypeExprOrValue<T>): ExprType<BooleanType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void a; void b;
  }

  /** Test if first expression is less than or equal to second. */
  static lessEqual<T>(a: Expr<T>, b: SubtypeExprOrValue<T>): ExprType<BooleanType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void a; void b;
  }

  /** Test if first expression is greater than second. */
  static greater<T>(a: Expr<T>, b: SubtypeExprOrValue<T>): ExprType<BooleanType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void a; void b;
  }

  /** Test if first expression is greater than or equal to second. */
  static greaterEqual<T>(a: Expr<T>, b: SubtypeExprOrValue<T>): ExprType<BooleanType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void a; void b;
  }

  /** Test reference equality between two expressions. */
  static is<T>(a: Expr<T>, b: SubtypeExprOrValue<T>): ExprType<BooleanType> {
    // Note that this static method is overridden later
    throw new Error("Method used before initialization");
    void a; void b;
  }

  /** Return the minimum of two values. */
  static min<T>(a: Expr<T>, b: SubtypeExprOrValue<NoInfer<T>>): ExprType<T> {
    const type = Expr.type(a) as T;
    const b_expr = Expr.from(b as any, type);
    const fn = this.function([type, type], type as EastType, ($, a, b) => {
      $.return(Expr.less(a as Expr<T>, b as any).ifElse(_ => a, _ => b));
    })

    return fn(a as any, b_expr as any) as ExprType<T>;
  }

  /** Return the maximum of two values. */
  static max<T>(a: Expr<T>, b: SubtypeExprOrValue<NoInfer<T>>): ExprType<T> {
    const type = Expr.type(a) as T;
    const b_expr = Expr.from(b as any, type);
    const fn = this.function([type, type], type as EastType, ($, a, b) => {
      $.return(Expr.less(a as Expr<T>, b as any).ifElse(_ => b, _ => a));
    })

    return fn(a as any, b_expr as any) as ExprType<T>;
  }

  /** Clamp a value between a min and max value. */
  static clamp<T>(x: Expr<T>, min: SubtypeExprOrValue<NoInfer<T>>, max: SubtypeExprOrValue<NoInfer<T>>): ExprType<T> {
    const type = Expr.type(x) as T;
    const min_expr = Expr.from(min as any, type);
    const max_expr = Expr.from(max as any, type);
    const fn = this.function([type, type, type], type as EastType, ($, x, min, max) => {
      $.return(Expr.less(x as Expr<T>, min as any).ifElse(_ => min, _ => Expr.less(x as any, max as any).ifElse(_ => x, _ => max)));
    });

    return fn(x as any, min_expr as any, max_expr as any) as ExprType<T>;
  }
}
