/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { ast_to_ir } from "../ast_to_ir.js";
import { EastIR } from "../eastir.js";
import type { FunctionIR } from "../ir.js";
import { get_location } from "../location.js";
import { FunctionType, type EastType } from "../types.js";
import { valueOrExprToAstTyped } from "./ast.js";
import { AstSymbol, Expr, FactorySymbol, type ToExpr } from "./expr.js";
import type { ExprType, SubtypeExprOrValue } from "./types.js";

/**
 * Return type for function calls - uses ExprType for all types including RecursiveType
 */
type FunctionReturnType<O> = ExprType<O>;

/**
* Expression representing the Function type.
* Used for function calls, composition, etc.
*/
export class FunctionExpr<I extends any[], O extends any> extends Expr<FunctionType<I, O>> {
  constructor(private input_types: I, private output_type: O, ast: AST, createExpr: ToExpr) {
    super(ast.type as FunctionType<I, O>, ast, createExpr);
  }
  
  /** Note that {@link CallableFunctionExpr} provides a more ergonomic way to call functions.
   *
   * @internal */
  call(...args: { [K in keyof I]: SubtypeExprOrValue<I[K]> }): FunctionReturnType<O> {
    if (args.length !== this.input_types.length) {
      throw new Error(`Expected ${this.input_types.length} arguments, got ${args.length}`);
    }

    const inputs = this.input_types.map((input_type: EastType, i) => valueOrExprToAstTyped(args[i], input_type));
    
    return this[FactorySymbol]({
      ast_type: "Call",
      type: this.output_type as EastType,
      location: get_location(),
      function: this[AstSymbol],
      arguments: inputs,
    }) as FunctionReturnType<O>;
  }
  
  /** Convert the function to East's "intermediate representation" (IR). This can then be serialized or compiled.
  * 
  * Note that the function must be a "free" function, with no captures.
  */
  toIR(): EastIR<I, O> {
    const ir = ast_to_ir(this[AstSymbol]) as FunctionIR;
    return new EastIR(ir);
  }
}

/** 
 * Expression representing the Function type.
 * Used for function calls, composition, etc.
 * 
 * Supports direct calling of functions using `f(x, y)` syntax instead using a method, like `f.call(x, y)`.
 */
export type CallableFunctionExpr<I extends any[], O> = FunctionExpr<I, O> & ((...args: { [K in keyof I]: SubtypeExprOrValue<I[K]> }) => FunctionReturnType<O>);

/**
 * Factory producing a callable FunctionExpr so users can invoke it directly.
 * Prototype chain preserved for instanceof checks.
 * 
 * @internal
 */
export function createFunctionExpr<I extends any[], O extends any>(
  input_types: I,
  output_type: O,
  ast: AST,
  createExpr: ToExpr
): CallableFunctionExpr<I, O> {
  const inst = new FunctionExpr<I, O>(input_types, output_type, ast, createExpr);
  const callable = function (...args: { [K in keyof I]: SubtypeExprOrValue<I[K]> }): FunctionReturnType<O> {
    return inst.call(...(args as any));
  } as unknown as CallableFunctionExpr<I, O>;
  Object.setPrototypeOf(callable, inst);
  return callable;
}
