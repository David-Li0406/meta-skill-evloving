/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { NullType } from "../types.js";
import { Expr, type ToExpr } from "./expr.js";

/**
* Expression representing the Null type (unit/void type).
* Used for null values and statement expressions.
*/
export class NullExpr extends Expr<NullType> {
  constructor(ast: AST, createExpr: ToExpr) {
    super(NullType, ast, createExpr);
  }
}