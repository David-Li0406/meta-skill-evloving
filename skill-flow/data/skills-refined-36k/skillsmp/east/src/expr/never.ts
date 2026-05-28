/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { NeverType } from "../types.js";
import { Expr, type ToExpr } from "./expr.js";

/**
 * Expression representing the Never type (bottom type).
 * Used for error expressions and unreachable code paths.
 */
export class NeverExpr extends Expr<NeverType> {
  constructor(ast: AST, createExpr: ToExpr) {
    super(NeverType, ast, createExpr);
  }
}