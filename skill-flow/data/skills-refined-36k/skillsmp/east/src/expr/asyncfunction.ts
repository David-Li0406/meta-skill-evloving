/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { ast_to_ir } from "../ast_to_ir.js";
import { AsyncEastIR } from "../eastir.js";
import type { AsyncFunctionIR } from "../ir.js";
import { get_location } from "../location.js";
import { AsyncFunctionType, type EastType } from "../types.js";
import { valueOrExprToAstTyped } from "./ast.js";
import { AstSymbol, Expr, FactorySymbol, type ToExpr } from "./expr.js";
import type { ExprType, SubtypeExprOrValue } from "./types.js";

/**
* Expression representing the AsyncFunction type.
* Used for async function calls, composition, etc.
*/
export class AsyncFunctionExpr<I extends any[], O extends any> extends Expr<AsyncFunctionType<I, O>> {
  constructor(private input_types: I, private output_type: O, ast: AST, createExpr: ToExpr) {
    super(ast.type as AsyncFunctionType<I, O>, ast, createExpr);
  }
  
  /** Call the async function with the given arguments (awaiting the result eagerly).
   * 
   * Note that {@link CallableAsyncFunctionExpr} provides a more ergonomic way to call async functions.
   * 
   * @internal */
  call(...args: { [K in keyof I]: SubtypeExprOrValue<I[K]> }): ExprType<O> {
    if (args.length !== this.input_types.length) {
      throw new Error(`Expected ${this.input_types.length} arguments, got ${args.length}`);
    }

    const inputs = this.input_types.map((input_type: EastType, i) => valueOrExprToAstTyped(args[i], input_type));
    
    return this[FactorySymbol]({
      ast_type: "CallAsync",
      type: this.output_type as EastType,
      location: get_location(),
      function: this[AstSymbol],
      arguments: inputs,
    }) as ExprType<O>;
  }
  
  /** Convert the function to East's "intermediate representation" (IR). This can then be serialized or compiled.
  * 
  * Note that the function must be a "free" function, with no captures.
  */
  toIR(): AsyncEastIR<I, O> {
    const ir = ast_to_ir(this[AstSymbol]) as AsyncFunctionIR;
    return new AsyncEastIR(ir);
  }
}

/** 
 * Expression representing the AsyncFunction type.
 * Used for async function calls, composition, etc.
 * 
 * Supports direct calling of functions using `f(x, y)` syntax instead using a method, like `f.call(x, y)`.
 * Awaiting the result is handled automatically.
 */
export type CallableAsyncFunctionExpr<I extends any[], O> = AsyncFunctionExpr<I, O> & ((...args: { [K in keyof I]: SubtypeExprOrValue<I[K]> }) => ExprType<O>);

/**
 * Factory producing a callable AsyncFunctionExpr so users can invoke it directly.
 * Prototype chain preserved for instanceof checks.
 * 
 * @internal
 */
export function createAsyncFunctionExpr<I extends any[], O extends any>(
  input_types: I,
  output_type: O,
  ast: AST,
  createExpr: ToExpr
): CallableAsyncFunctionExpr<I, O> {
  const inst = new AsyncFunctionExpr<I, O>(input_types, output_type, ast, createExpr);
  const callable = function (...args: { [K in keyof I]: SubtypeExprOrValue<I[K]> }): ExprType<O> {
    return inst.call(...(args as any));
  } as unknown as CallableAsyncFunctionExpr<I, O>;
  Object.setPrototypeOf(callable, inst);
  return callable;
}
