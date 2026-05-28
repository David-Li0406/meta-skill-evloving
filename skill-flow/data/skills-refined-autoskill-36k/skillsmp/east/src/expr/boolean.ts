/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { BooleanType, NeverType, TypeUnion } from "../types.js";
import { AstSymbol, Expr, FactorySymbol, type ToExpr } from "./expr.js";
import type { ExprType, TypeOf } from "./types.js";
import { valueOrExprToAstTyped } from "./ast.js";
import type { BlockBuilder } from "./block.js";
import { equal, notEqual } from "./block.js";

/**
 * Expression representing boolean values and logical operations.
 *
 * BooleanExpr provides logical operations (AND, OR, NOT, XOR) and conditional expressions.
 * Supports both short-circuit evaluation (and, or) and non-short-circuit bitwise operations
 * (bitAnd, bitOr, bitXor) for performance-critical code.
 *
 * @example
 * ```ts
 * // Basic boolean operations
 * const logic = East.function([BooleanType, BooleanType], BooleanType, ($, a, b) => {
 *   const notA = a.not();
 *   const orResult = a.or(() => b);  // Short-circuits
 *   const andResult = a.and(() => b);  // Short-circuits
 *   $.return(notA.bitXor(orResult.bitAnd(andResult)));
 * });
 *
 * // Conditional expression
 * const conditional = East.function([BooleanType, IntegerType, IntegerType], IntegerType, ($, condition, x, y) => {
 *   $.return(condition.ifElse(() => x, () => y));
 * });
 * const compiled = East.compile(conditional.toIR(), []);
 * compiled(true, 10n, 20n);   // 10n
 * compiled(false, 10n, 20n);  // 20n
 * ```
 */
export class BooleanExpr extends Expr<BooleanType> {
  constructor(ast: AST, createExpr: ToExpr) {
    super(BooleanType, ast, createExpr);
  }

  /**
   * Performs logical NOT operation (!x).
   *
   * @returns A BooleanExpr that is true if this is false, and false if this is true
   *
   * @example
   * ```ts
   * const negate = East.function([BooleanType], BooleanType, ($, x) => {
   *   $.return(x.not());
   * });
   * const compiled = East.compile(negate.toIR(), []);
   * compiled(true);   // false
   * compiled(false);  // true
   * ```
   */
  not(): BooleanExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "BooleanNot",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as BooleanExpr;
  }

  /**
   * Performs logical OR operation with short-circuit evaluation.
   *
   * @param y - Function that returns the second boolean operand (only evaluated if this is false)
   * @returns A BooleanExpr that is true if either operand is true
   *
   * @remarks
   * If this boolean is true, returns true without evaluating the second operand.
   * For non-short-circuit evaluation, use {@link bitOr}.
   *
   * @see {@link bitOr} for non-short-circuiting version (faster in tight loops)
   *
   * @example
   * ```ts
   * const shortCircuitOr = East.function([BooleanType, BooleanType], BooleanType, ($, a, b) => {
   *   $.return(a.or(() => b));  // b only evaluated if a is false
   * });
   * const compiled = East.compile(shortCircuitOr.toIR(), []);
   * compiled(true, false);   // true (doesn't evaluate second operand)
   * compiled(false, true);   // true
   * compiled(false, false);  // false
   * ```
   */
  or(y: ($: BlockBuilder<NeverType>) => Expr<BooleanType> | boolean): BooleanExpr {
    return this.ifElse(() => true, y) as any;
  }

  /**
   * Performs logical AND operation with short-circuit evaluation.
   *
   * @param y - Function that returns the second boolean operand (only evaluated if this is true)
   * @returns A BooleanExpr that is true if both operands are true
   *
   * @remarks
   * If this boolean is false, returns false without evaluating the second operand.
   * For non-short-circuit evaluation, use {@link bitAnd}.
   *
   * @see {@link bitAnd} for non-short-circuiting version (faster in tight loops)
   *
   * @example
   * ```ts
   * const shortCircuitAnd = East.function([BooleanType, BooleanType], BooleanType, ($, a, b) => {
   *   $.return(a.and(() => b));  // b only evaluated if a is true
   * });
   * const compiled = East.compile(shortCircuitAnd.toIR(), []);
   * compiled(false, true);   // false (doesn't evaluate second operand)
   * compiled(true, true);    // true
   * compiled(true, false);   // false
   * ```
   */
  and(y: ($: BlockBuilder<NeverType>) => Expr<BooleanType> | boolean): BooleanExpr {
    return this.ifElse(y, () => false) as any;
  }

  /**
   * Performs bitwise OR operation (non-short-circuit).
   *
   * @param y - The second boolean operand (always evaluated)
   * @returns A BooleanExpr that is true if either operand is true
   *
   * @remarks
   * Always evaluates both operands. Compiles to a non-branching instruction which can be
   * faster in tight loops. For short-circuit evaluation, use {@link or}.
   *
   * @see {@link or} for short-circuiting version
   *
   * @example
   * ```ts
   * const bitwiseOr = East.function([BooleanType, BooleanType], BooleanType, ($, a, b) => {
   *   $.return(a.bitOr(b));  // Both operands always evaluated
   * });
   * const compiled = East.compile(bitwiseOr.toIR(), []);
   * compiled(true, false);   // true
   * compiled(false, true);   // true
   * compiled(false, false);  // false
   * ```
   */
  bitOr(y: Expr<BooleanType> | boolean): BooleanExpr {
    const yAst = valueOrExprToAstTyped(y, BooleanType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "BooleanOr",
      type_parameters: [],
      arguments: [this[AstSymbol], yAst],
    }) as BooleanExpr;
  }

  /**
   * Performs bitwise AND operation (non-short-circuit).
   *
   * @param y - The second boolean operand (always evaluated)
   * @returns A BooleanExpr that is true if both operands are true
   *
   * @remarks
   * Always evaluates both operands. Compiles to a non-branching instruction which can be
   * faster in tight loops. For short-circuit evaluation, use {@link and}.
   *
   * @see {@link and} for short-circuiting version
   *
   * @example
   * ```ts
   * const bitwiseAnd = East.function([BooleanType, BooleanType], BooleanType, ($, a, b) => {
   *   $.return(a.bitAnd(b));  // Both operands always evaluated
   * });
   * const compiled = East.compile(bitwiseAnd.toIR(), []);
   * compiled(true, true);    // true
   * compiled(true, false);   // false
   * compiled(false, false);  // false
   * ```
   */
  bitAnd(y: Expr<BooleanType> | boolean): BooleanExpr {
    const yAst = valueOrExprToAstTyped(y, BooleanType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "BooleanAnd",
      type_parameters: [],
      arguments: [this[AstSymbol], yAst],
    }) as BooleanExpr;
  }

  /**
   * Performs bitwise XOR (exclusive OR) operation.
   *
   * @param y - The second boolean operand
   * @returns A BooleanExpr that is true if exactly one operand is true
   *
   * @remarks
   * Always evaluates both operands (XOR cannot short-circuit by definition).
   * Compiles to a non-branching instruction.
   *
   * @example
   * ```ts
   * const exclusiveOr = East.function([BooleanType, BooleanType], BooleanType, ($, a, b) => {
   *   $.return(a.bitXor(b));
   * });
   * const compiled = East.compile(exclusiveOr.toIR(), []);
   * compiled(true, false);   // true
   * compiled(false, true);   // true
   * compiled(true, true);    // false
   * compiled(false, false);  // false
   * ```
   */
  bitXor(y: Expr<BooleanType> | boolean): BooleanExpr {
    const yAst = valueOrExprToAstTyped(y, BooleanType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: BooleanType,
      location: get_location(),
      builtin: "BooleanXor",
      type_parameters: [],
      arguments: [this[AstSymbol], yAst],
    }) as BooleanExpr;
  }

  /**
   * Evaluates to one of two expressions based on this boolean value (ternary operator).
   *
   * @typeParam F1 - Type of the function returning the true branch value
   * @typeParam F2 - Type of the function returning the false branch value
   * @param true_value - Function returning the expression to use if this is true
   * @param false_value - Function returning the expression to use if this is false
   * @returns An expression of the union type of both branches
   *
   * @remarks
   * Note that you cannot use `$.return` inside the `true_value` or `false_value` functions.
   * This is for expressions, not statements.
   *
   * @example
   * ```ts
   * // Simple conditional
   * const max = East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => {
   *   $.return(a.greaterThan(b).ifElse(() => a, () => b));
   * });
   * const compiled = East.compile(max.toIR(), []);
   * compiled(10n, 20n);  // 20n
   * compiled(30n, 15n);  // 30n
   *
   * // Conditional with different types (union type result)
   * const conditional = East.function([BooleanType], VariantType({num: IntegerType, str: StringType}), ($, flag) => {
   *   $.return(flag.ifElse(
   *     () => Expr.variant("num", 42n),
   *     () => Expr.variant("str", "hello")
   *   ));
   * });
   * ```
   */
  ifElse<F1 extends ($: BlockBuilder<NeverType>) => any, F2 extends ($: BlockBuilder<NeverType>) => any>(true_value: F1, false_value: F2): ExprType<TypeUnion<TypeOf<ReturnType<F1>>, TypeOf<ReturnType<F2>>>> {
    const true_expr = Expr.block(true_value);
    const false_expr = Expr.block(false_value);
    const type = TypeUnion(Expr.type(true_expr) as any, Expr.type(false_expr) as any);

    return this[FactorySymbol]({
      ast_type: "IfElse",
      type,
      location: get_location(),
      ifs: [{
        predicate: this[AstSymbol],
        body: true_expr[AstSymbol],
      }],
      else_body: false_expr[AstSymbol],
    }) as ExprType<TypeUnion<TypeOf<ReturnType<F1>>, TypeOf<ReturnType<F2>>>>;
  }

  /**
   * Checks if this boolean equals another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are equal
   *
   * @example
   * ```ts
   * const isEqual = East.function([BooleanType, BooleanType], BooleanType, ($, a, b) => {
   *   $.return(a.equals(b));
   * });
   * const compiled = East.compile(isEqual.toIR(), []);
   * compiled(true, true);     // true
   * compiled(false, false);   // true
   * compiled(true, false);    // false
   * ```
   */
  equals(other: BooleanExpr | boolean): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this boolean does not equal another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are not equal
   *
   * @example
   * ```ts
   * const isNotEqual = East.function([BooleanType, BooleanType], BooleanType, ($, a, b) => {
   *   $.return(a.notEquals(b));
   * });
   * const compiled = East.compile(isNotEqual.toIR(), []);
   * compiled(true, false);    // true
   * compiled(false, true);    // true
   * compiled(true, true);     // false
   * ```
   */
  notEquals(other: BooleanExpr | boolean): BooleanExpr {
    return notEqual(this, other);
  }

  // ============================================================================
  // Aliases for comparison operations
  // ============================================================================

  /** Alias for {@link equals} */
  eq = this.equals;
  /** Alias for {@link equals} */
  equal = this.equals;

  /** Alias for {@link notEquals} */
  ne = this.notEquals;
  /** Alias for {@link notEquals} */
  notEqual = this.notEquals;
}