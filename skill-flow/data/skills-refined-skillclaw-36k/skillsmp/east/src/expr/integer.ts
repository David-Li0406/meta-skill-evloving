/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { FloatType, IntegerType, isTypeEqual } from "../types.js";
import { AstSymbol, Expr, FactorySymbol, type ToExpr } from "./expr.js";
import { valueOrExprToAst } from "./ast.js";
import type { FloatExpr } from "./float.js";
import type { BooleanExpr } from "./boolean.js";
import { equal, notEqual, less, lessEqual, greater, greaterEqual } from "./block.js";

/**
 * Expression representing integer values and operations.
 *
 * IntegerExpr provides arithmetic, comparison, and conversion operations for 64-bit signed integers.
 * Operations automatically promote to FloatExpr when mixed with float operands.
 *
 * @example
 * ```ts
 * // Basic arithmetic
 * const calculate = East.function([IntegerType, IntegerType], IntegerType, ($, a, b) => {
 *   const sum = a.add(b);
 *   const product = a.multiply(b);
 *   const power = a.pow(2n);
 *   $.return(sum.add(product).add(power));
 * });
 *
 * // Integer division and remainder
 * const divMod = East.function([IntegerType, IntegerType], StructType({quot: IntegerType, rem: IntegerType}), ($, x, y) => {
 *   $.return({quot: x.divide(y), rem: x.remainder(y)});
 * });
 *
 * // Type promotion with floats
 * const mixed = East.function([IntegerType], FloatType, ($, x) => {
 *   $.return(x.add(2.5));  // Returns FloatExpr
 * });
 * ```
 */
export class IntegerExpr extends Expr<IntegerType> {
  constructor(ast: AST, createExpr: ToExpr) {
    super(IntegerType, ast, createExpr);
  }

  /**
   * Negates an integer value (-x).
   *
   * @returns The negated integer
   *
   * @example
   * ```ts
   * const negate = East.function([IntegerType], IntegerType, ($, x) => {
   *   $.return(x.negate());
   * });
   * const compiled = East.compile(negate.toIR(), []);
   * compiled(5n);   // -5n
   * compiled(-3n);  // 3n
   * ```
   */
  negate(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "IntegerNegate",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Adds two integers or promotes to float if adding a float.
   *
   * @param y - The integer or float to add
   * @returns IntegerExpr if both operands are integers, FloatExpr if either is a float
   *
   * @example
   * ```ts
   * const addIntegers = East.function([IntegerType, IntegerType], IntegerType, ($, x, y) => {
   *   $.return(x.add(y));
   * });
   * const compiled = East.compile(addIntegers.toIR(), []);
   * compiled(3n, 4n);  // 7n
   *
   * // Adding with float promotes to float
   * const addFloat = East.function([IntegerType], FloatType, ($, x) => {
   *   $.return(x.add(2.5));
   * });
   * ```
   */
  add(y: Expr<IntegerType> | bigint): IntegerExpr
  add(y: Expr<FloatType> | number): FloatExpr
  add(y: any): Expr {
    const rightAst = valueOrExprToAst(y);
    if (isTypeEqual(rightAst.type, FloatType)) {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: FloatType,
        location: get_location(),
        builtin: "FloatAdd",
        type_parameters: [],
        arguments: [this.toFloat()[AstSymbol], rightAst],
      }) as FloatExpr;
    } else {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerAdd",
        type_parameters: [],
        arguments: [this[AstSymbol], rightAst],
      }) as IntegerExpr;
    }
  }

  /**
   * Subtracts two integers or promotes to float if subtracting a float.
   *
   * @param y - The integer or float to subtract
   * @returns IntegerExpr if both operands are integers, FloatExpr if either is a float
   *
   * @example
   * ```ts
   * const subtractIntegers = East.function([IntegerType, IntegerType], IntegerType, ($, x, y) => {
   *   $.return(x.subtract(y));
   * });
   * const compiled = East.compile(subtractIntegers.toIR(), []);
   * compiled(10n, 3n);  // 7n
   * compiled(5n, 8n);   // -3n
   * ```
   */
  subtract(y: Expr<IntegerType> | bigint): IntegerExpr
  subtract(y: Expr<FloatType> | number): FloatExpr
  subtract(y: any): Expr {
    const rightAst = valueOrExprToAst(y);
    if (isTypeEqual(rightAst.type, FloatType)) {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: FloatType,
        location: get_location(),
        builtin: "FloatSubtract",
        type_parameters: [],
        arguments: [this.toFloat()[AstSymbol], rightAst],
      }) as FloatExpr;
    } else {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerSubtract",
        type_parameters: [],
        arguments: [this[AstSymbol], rightAst],
      }) as IntegerExpr;
    }
  }

  /**
   * Multiplies two integers or promotes to float if multiplying by a float.
   *
   * @param y - The integer or float to multiply by
   * @returns IntegerExpr if both operands are integers, FloatExpr if either is a float
   *
   * @example
   * ```ts
   * const multiplyIntegers = East.function([IntegerType, IntegerType], IntegerType, ($, x, y) => {
   *   $.return(x.multiply(y));
   * });
   * const compiled = East.compile(multiplyIntegers.toIR(), []);
   * compiled(6n, 7n);   // 42n
   * compiled(-3n, 4n);  // -12n
   * ```
   */
  multiply(y: Expr<IntegerType> | bigint): IntegerExpr
  multiply(y: Expr<FloatType> | number): FloatExpr
  multiply(y: any): Expr {
    const rightAst = valueOrExprToAst(y);
    if (isTypeEqual(rightAst.type, FloatType)) {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: FloatType,
        location: get_location(),
        builtin: "FloatMultiply",
        type_parameters: [],
        arguments: [this.toFloat()[AstSymbol], rightAst],
      }) as FloatExpr;
    } else {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerMultiply",
        type_parameters: [],
        arguments: [this[AstSymbol], rightAst],
      }) as IntegerExpr;
    }
  }

  /**
   * Divides two integers (floor division) or promotes to float if dividing by a float.
   *
   * @param y - The integer or float divisor
   * @returns IntegerExpr (floor division) if both are integers, FloatExpr if either is a float
   *
   * @remarks Integer division by zero returns 0 (does not throw error).
   *          When dividing by a float, uses normal floating point division.
   *
   * @example
   * ```ts
   * const divideIntegers = East.function([IntegerType, IntegerType], IntegerType, ($, x, y) => {
   *   $.return(x.divide(y));
   * });
   * const compiled = East.compile(divideIntegers.toIR(), []);
   * compiled(10n, 3n);  // 3n (floor division)
   * compiled(10n, 2n);  // 5n
   * compiled(10n, 0n);  // 0n (division by zero returns 0)
   * compiled(-10n, 3n); // -4n (floor towards negative infinity)
   * ```
   */
  divide(y: Expr<IntegerType> | bigint): IntegerExpr
  divide(y: Expr<FloatType> | number): FloatExpr
  divide(y: any): Expr {
    const rightAst = valueOrExprToAst(y);
    if (isTypeEqual(rightAst.type, FloatType)) {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: FloatType,
        location: get_location(),
        builtin: "FloatDivide",
        type_parameters: [],
        arguments: [this.toFloat()[AstSymbol], rightAst],
      }) as FloatExpr;
    } else {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerDivide",
        type_parameters: [],
        arguments: [this[AstSymbol], rightAst],
      }) as IntegerExpr;
    }
  }

  /**
   * Computes the remainder of integer division or promotes to float.
   *
   * @param y - The integer or float divisor
   * @returns IntegerExpr if both are integers, FloatExpr if either is a float
   *
   * @remarks Integer remainder by zero returns 0 (does not throw error).
   *          Result has the same sign as the divisor (floor division semantics).
   *
   * @example
   * ```ts
   * const getRemainder = East.function([IntegerType, IntegerType], IntegerType, ($, x, y) => {
   *   $.return(x.remainder(y));
   * });
   * const compiled = East.compile(getRemainder.toIR(), []);
   * compiled(10n, 3n);   // 1n (10 = 3*3 + 1)
   * compiled(10n, 4n);   // 2n
   * compiled(-10n, 3n);  // 2n (floor division: -10 = 3*(-4) + 2)
   * compiled(10n, 0n);   // 0n (remainder by zero returns 0)
   * ```
   */
  remainder(y: Expr<IntegerType> | bigint): IntegerExpr
  remainder(y: Expr<FloatType> | number): FloatExpr
  remainder(y: any): Expr {
    const rightAst = valueOrExprToAst(y);
    if (isTypeEqual(rightAst.type, FloatType)) {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: FloatType,
        location: get_location(),
        builtin: "FloatRemainder",
        type_parameters: [],
        arguments: [this.toFloat()[AstSymbol], rightAst],
      }) as FloatExpr;
    } else {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerRemainder",
        type_parameters: [],
        arguments: [this[AstSymbol], rightAst],
      }) as IntegerExpr;
    }
  }

  /**
   * Raises an integer to a power or promotes to float.
   *
   * @param y - The integer or float exponent
   * @returns IntegerExpr if both are integers, FloatExpr if either is a float
   *
   * @remarks Integer exponentiation with negative exponent returns 0.
   *          When using a float exponent, uses floating point exponentiation.
   *
   * @example
   * ```ts
   * const power = East.function([IntegerType, IntegerType], IntegerType, ($, base, exp) => {
   *   $.return(base.pow(exp));
   * });
   * const compiled = East.compile(power.toIR(), []);
   * compiled(2n, 3n);    // 8n (2^3)
   * compiled(5n, 2n);    // 25n
   * compiled(10n, 0n);   // 1n (anything^0 = 1)
   * compiled(2n, -1n);   // 0n (negative exponent returns 0 for integers)
   * ```
   */
  pow(y: Expr<IntegerType> | bigint): IntegerExpr
  pow(y: Expr<FloatType> | number): FloatExpr
  pow(y: any): Expr {
    const rightAst = valueOrExprToAst(y);
    if (isTypeEqual(rightAst.type, FloatType)) {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: FloatType,
        location: get_location(),
        builtin: "FloatPow",
        type_parameters: [],
        arguments: [this.toFloat()[AstSymbol], rightAst],
      }) as FloatExpr;
    } else {
      return this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerPow",
        type_parameters: [],
        arguments: [this[AstSymbol], rightAst],
      }) as IntegerExpr;
    }
  }

  /**
   * Returns the absolute value of an integer.
   *
   * @returns The absolute value (always non-negative)
   *
   * @example
   * ```ts
   * const absoluteValue = East.function([IntegerType], IntegerType, ($, x) => {
   *   $.return(x.abs());
   * });
   * const compiled = East.compile(absoluteValue.toIR(), []);
   * compiled(5n);    // 5n
   * compiled(-5n);   // 5n
   * compiled(0n);    // 0n
   * ```
   */
  abs(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "IntegerAbs",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Returns the sign of an integer (-1 for negative, 0 for zero, 1 for positive).
   *
   * @returns -1n, 0n, or 1n depending on the sign of the integer
   *
   * @example
   * ```ts
   * const getSign = East.function([IntegerType], IntegerType, ($, x) => {
   *   $.return(x.sign());
   * });
   * const compiled = East.compile(getSign.toIR(), []);
   * compiled(42n);   // 1n
   * compiled(-17n);  // -1n
   * compiled(0n);    // 0n
   * ```
   */
  sign(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "IntegerSign",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Computes the integer logarithm with a specified base (floor of log).
   *
   * @param base - The base for the logarithm
   * @returns The floor of log_base(x)
   *
   * @remarks Returns 0 if x <= 0 or base <= 1.
   *
   * @example
   * ```ts
   * const logarithm = East.function([IntegerType, IntegerType], IntegerType, ($, x, base) => {
   *   $.return(x.log(base));
   * });
   * const compiled = East.compile(logarithm.toIR(), []);
   * compiled(1000n, 10n);  // 3n (10^3 = 1000)
   * compiled(8n, 2n);      // 3n (2^3 = 8)
   * compiled(100n, 10n);   // 2n (10^2 = 100)
   * compiled(7n, 2n);      // 2n (floor of log_2(7) ≈ 2.8)
   * ```
   */
  log(base: Expr<IntegerType> | bigint): IntegerExpr {
    const baseAst = valueOrExprToAst(base);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "IntegerLog",
      type_parameters: [],
      arguments: [this[AstSymbol], baseAst],
    }) as IntegerExpr;
  }

  /**
   * Converts an integer to a floating-point number.
   *
   * @returns The integer as a FloatExpr
   *
   * @remarks May lose precision for very large integers (beyond 2^53).
   *
   * @example
   * ```ts
   * const convertToFloat = East.function([IntegerType], FloatType, ($, x) => {
   *   $.return(x.toFloat());
   * });
   * const compiled = East.compile(convertToFloat.toIR(), []);
   * compiled(42n);    // 42.0
   * compiled(-17n);   // -17.0
   * compiled(0n);     // 0.0
   * ```
   */
  toFloat(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "IntegerToFloat",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Checks if this integer equals another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are equal
   *
   * @example
   * ```ts
   * const isEqual = East.function([IntegerType, IntegerType], BooleanType, ($, a, b) => {
   *   $.return(a.equals(b));
   * });
   * const compiled = East.compile(isEqual.toIR(), []);
   * compiled(5n, 5n);   // true
   * compiled(5n, 3n);   // false
   * ```
   */
  equals(other: IntegerExpr | bigint): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this integer does not equal another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are not equal
   *
   * @example
   * ```ts
   * const isNotEqual = East.function([IntegerType, IntegerType], BooleanType, ($, a, b) => {
   *   $.return(a.notEquals(b));
   * });
   * const compiled = East.compile(isNotEqual.toIR(), []);
   * compiled(5n, 3n);   // true
   * compiled(5n, 5n);   // false
   * ```
   */
  notEquals(other: IntegerExpr | bigint): BooleanExpr {
    return notEqual(this, other);
  }

  /**
   * Checks if this integer is greater than another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this value is greater
   *
   * @example
   * ```ts
   * const isGreater = East.function([IntegerType, IntegerType], BooleanType, ($, a, b) => {
   *   $.return(a.greaterThan(b));
   * });
   * const compiled = East.compile(isGreater.toIR(), []);
   * compiled(5n, 3n);   // true
   * compiled(3n, 5n);   // false
   * compiled(5n, 5n);   // false
   * ```
   */
  greaterThan(other: IntegerExpr | bigint): BooleanExpr {
    return greater(this, other);
  }

  /**
   * Checks if this integer is less than another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this value is less
   *
   * @example
   * ```ts
   * const isLess = East.function([IntegerType, IntegerType], BooleanType, ($, a, b) => {
   *   $.return(a.lessThan(b));
   * });
   * const compiled = East.compile(isLess.toIR(), []);
   * compiled(3n, 5n);   // true
   * compiled(5n, 3n);   // false
   * compiled(5n, 5n);   // false
   * ```
   */
  lessThan(other: IntegerExpr | bigint): BooleanExpr {
    return less(this, other);
  }

  /**
   * Checks if this integer is greater than or equal to another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this value is greater than or equal
   *
   * @example
   * ```ts
   * const isGreaterOrEqual = East.function([IntegerType, IntegerType], BooleanType, ($, a, b) => {
   *   $.return(a.greaterThanOrEqual(b));
   * });
   * const compiled = East.compile(isGreaterOrEqual.toIR(), []);
   * compiled(5n, 3n);   // true
   * compiled(5n, 5n);   // true
   * compiled(3n, 5n);   // false
   * ```
   */
  greaterThanOrEqual(other: IntegerExpr | bigint): BooleanExpr {
    return greaterEqual(this, other);
  }

  /**
   * Checks if this integer is less than or equal to another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this value is less than or equal
   *
   * @example
   * ```ts
   * const isLessOrEqual = East.function([IntegerType, IntegerType], BooleanType, ($, a, b) => {
   *   $.return(a.lessThanOrEqual(b));
   * });
   * const compiled = East.compile(isLessOrEqual.toIR(), []);
   * compiled(3n, 5n);   // true
   * compiled(5n, 5n);   // true
   * compiled(5n, 3n);   // false
   * ```
   */
  lessThanOrEqual(other: IntegerExpr | bigint): BooleanExpr {
    return lessEqual(this, other);
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

  /** Alias for {@link greaterThan} */
  gt = this.greaterThan;
  /** Alias for {@link greaterThan} */
  greater = this.greaterThan;

  /** Alias for {@link lessThan} */
  lt = this.lessThan;
  /** Alias for {@link lessThan} */
  less = this.lessThan;

  /** Alias for {@link greaterThanOrEqual} */
  gte = this.greaterThanOrEqual;
  /** Alias for {@link greaterThanOrEqual} */
  ge = this.greaterThanOrEqual;
  /** Alias for {@link greaterThanOrEqual} */
  greaterEqual = this.greaterThanOrEqual;

  /** Alias for {@link lessThanOrEqual} */
  lte = this.lessThanOrEqual;
  /** Alias for {@link lessThanOrEqual} */
  le = this.lessThanOrEqual;
  /** Alias for {@link lessThanOrEqual} */
  lessEqual = this.lessThanOrEqual;

  // ============================================================================
  // Aliases for arithmetic operations
  // ============================================================================

  /** Alias for {@link add} */
  plus = this.add;

  /** Alias for {@link subtract} */
  sub = this.subtract;
  /** Alias for {@link subtract} */
  minus = this.subtract;

  /** Alias for {@link multiply} */
  mul = this.multiply;
  /** Alias for {@link multiply} */
  times = this.multiply;

  /** Alias for {@link divide} */
  div = this.divide;

  /** Alias for {@link remainder} */
  mod = this.remainder;
  /** Alias for {@link remainder} */
  rem = this.remainder;
  /** Alias for {@link remainder} */
  modulo = this.remainder;
}