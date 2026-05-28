/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { FloatType, IntegerType, isTypeEqual, printType } from "../types.js";
import { AstSymbol, Expr, FactorySymbol, type ToExpr } from "./expr.js";
import { valueOrExprToAstTyped } from "./ast.js";
import type { IntegerExpr } from "./integer.js";
import type { BooleanExpr } from "./boolean.js";
import { equal, notEqual, less, lessEqual, greater, greaterEqual } from "./block.js";

/**
 * Expression representing floating-point values and operations (IEEE 754 double-precision).
 *
 * FloatExpr provides arithmetic, trigonometric, and conversion operations for 64-bit floats.
 * Automatically converts integer operands to float when needed. Supports special values: Infinity, -Infinity, NaN.
 *
 * @example
 * ```ts
 * // Basic arithmetic
 * const calculate = East.function([FloatType, FloatType], FloatType, ($, x, y) => {
 *   const sum = x.add(y);
 *   const ratio = x.divide(y);
 *   $.return(sum.multiply(ratio));
 * });
 *
 * // Trigonometry
 * const angle = East.function([FloatType], FloatType, ($, degrees) => {
 *   const radians = degrees.multiply(Math.PI / 180);
 *   $.return(radians.sin());
 * });
 *
 * // Mixed with integers
 * const mixed = East.function([IntegerType], FloatType, ($, x) => {
 *   $.return(x.add(2.5));  // Integer auto-converts to float
 * });
 * ```
 */
export class FloatExpr extends Expr<FloatType> {
  constructor(ast: AST, createExpr: ToExpr) {
    super(FloatType, ast, createExpr);
  }

  /**
   * Negates a floating-point number (-x).
   *
   * @returns A FloatExpr representing the negated value
   *
   * @example
   * ```ts
   * const negateFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.negate());
   * });
   * const compiled = East.compile(negateFloat.toIR(), []);
   * compiled(3.14);    // -3.14
   * compiled(-2.5);    // 2.5
   * compiled(0.0);     // -0.0 (negative zero)
   * ```
   */
  negate(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatNegate",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Adds two floating-point numbers or converts integer to float and adds (x + y).
   *
   * @param y - The float, number, IntegerExpr, or bigint to add
   * @returns A FloatExpr representing the sum
   *
   * @remarks Automatically converts integer operands to float before addition.
   *
   * @example
   * ```ts
   * const addFloats = East.function([FloatType, FloatType], FloatType, ($, x, y) => {
   *   $.return(x.add(y));
   * });
   * const compiled = East.compile(addFloats.toIR(), []);
   * compiled(3.14, 2.86);  // 6.0
   * compiled(1.5, -0.5);   // 1.0
   *
   * // Mixed with integers
   * const addMixed = East.function([FloatType, IntegerType], FloatType, ($, x, y) => {
   *   $.return(x.add(y));  // Integer auto-converts to float
   * });
   * compiled = East.compile(addMixed.toIR(), []);
   * compiled(3.14, 2n);    // 5.14
   * ```
   */
  add(y: FloatExpr | number | IntegerExpr | bigint): FloatExpr {
    let rightAst: AST;
    if (typeof y === "bigint") {
      // Convert integer to float first
      rightAst = valueOrExprToAstTyped(Number(y), FloatType);
    } else if (typeof y === "number") {
      rightAst = valueOrExprToAstTyped(y, FloatType);
    } else if (y instanceof Expr) {
      if (isTypeEqual(Expr.type(y as Expr<IntegerType>), IntegerType)) {
        // Convert integer to float first
        rightAst = (y as IntegerExpr).toFloat()[AstSymbol];
      } else if (isTypeEqual(Expr.type(y as Expr<FloatType>), FloatType)) {
        rightAst = y[AstSymbol];
      } else {
        throw new Error(`Cannot add Float and ${printType(Expr.type(y as any))}`);
      }
    } else {
      throw new Error(`Cannot add Float and ${typeof y}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatAdd",
      type_parameters: [],
      arguments: [this[AstSymbol], rightAst],
    }) as FloatExpr;
  }

  /**
   * Subtracts two floating-point numbers or converts integer to float and subtracts (x - y).
   *
   * @param y - The float, number, IntegerExpr, or bigint to subtract
   * @returns A FloatExpr representing the difference
   *
   * @remarks Automatically converts integer operands to float before subtraction.
   *
   * @example
   * ```ts
   * const subtractFloats = East.function([FloatType, FloatType], FloatType, ($, x, y) => {
   *   $.return(x.subtract(y));
   * });
   * const compiled = East.compile(subtractFloats.toIR(), []);
   * compiled(5.5, 2.3);    // 3.2
   * compiled(1.0, 1.0);    // 0.0
   * compiled(-2.5, 3.5);   // -6.0
   * ```
   */
  subtract(y: FloatExpr | number | IntegerExpr | bigint): FloatExpr {
    let rightAst: AST;
    if (typeof y === "bigint") {
      // Convert integer to float first
      rightAst = valueOrExprToAstTyped(Number(y), FloatType);
    } else if (typeof y === "number") {
      rightAst = valueOrExprToAstTyped(y, FloatType);
    } else if (y instanceof Expr) {
      if (isTypeEqual(Expr.type(y as Expr<IntegerType>), IntegerType)) {
        // Convert integer to float first
        rightAst = (y as IntegerExpr).toFloat()[AstSymbol];
      } else if (isTypeEqual(Expr.type(y as Expr<FloatType>), FloatType)) {
        rightAst = y[AstSymbol];
      } else {
        throw new Error(`Cannot add Float and ${printType(Expr.type(y as any))}`);
      }
    } else {
      throw new Error(`Cannot add Float and ${typeof y}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatSubtract",
      type_parameters: [],
      arguments: [this[AstSymbol], rightAst],
    }) as FloatExpr;
  }

  /**
   * Multiplies two floating-point numbers or converts integer to float and multiplies (x * y).
   *
   * @param y - The float, number, IntegerExpr, or bigint to multiply
   * @returns A FloatExpr representing the product
   *
   * @remarks Automatically converts integer operands to float before multiplication.
   *
   * @example
   * ```ts
   * const multiplyFloats = East.function([FloatType, FloatType], FloatType, ($, x, y) => {
   *   $.return(x.multiply(y));
   * });
   * const compiled = East.compile(multiplyFloats.toIR(), []);
   * compiled(3.0, 2.5);    // 7.5
   * compiled(2.0, -1.5);   // -3.0
   * compiled(0.5, 0.5);    // 0.25
   * ```
   */
  multiply(y: FloatExpr | number | IntegerExpr | bigint): FloatExpr {
    let rightAst: AST;
    if (typeof y === "bigint") {
      // Convert integer to float first
      rightAst = valueOrExprToAstTyped(Number(y), FloatType);
    } else if (typeof y === "number") {
      rightAst = valueOrExprToAstTyped(y, FloatType);
    } else if (y instanceof Expr) {
      if (isTypeEqual(Expr.type(y as Expr<IntegerType>), IntegerType)) {
        // Convert integer to float first
        rightAst = (y as IntegerExpr).toFloat()[AstSymbol];
      } else if (isTypeEqual(Expr.type(y as Expr<FloatType>), FloatType)) {
        rightAst = y[AstSymbol];
      } else {
        throw new Error(`Cannot add Float and ${printType(Expr.type(y as any))}`);
      }
    } else {
      throw new Error(`Cannot add Float and ${typeof y}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatMultiply",
      type_parameters: [],
      arguments: [this[AstSymbol], rightAst],
    }) as FloatExpr;
  }

  /**
   * Divides two floating-point numbers or converts integer to float and divides (x / y).
   *
   * @param y - The float, number, IntegerExpr, or bigint divisor
   * @returns A FloatExpr representing the quotient
   *
   * @remarks Division by zero returns Infinity, -Infinity, or NaN according to IEEE 754.
   *          Automatically converts integer operands to float before division.
   *
   * @example
   * ```ts
   * const divideFloats = East.function([FloatType, FloatType], FloatType, ($, x, y) => {
   *   $.return(x.divide(y));
   * });
   * const compiled = East.compile(divideFloats.toIR(), []);
   * compiled(10.0, 2.0);   // 5.0
   * compiled(1.0, 3.0);    // 0.3333333333333333
   * compiled(5.0, 0.0);    // Infinity
   * compiled(-5.0, 0.0);   // -Infinity
   * compiled(0.0, 0.0);    // NaN
   * ```
   */
  divide(y: FloatExpr | number | IntegerExpr | bigint): FloatExpr {
    let rightAst: AST;
    if (typeof y === "bigint") {
      // Convert integer to float first
      rightAst = valueOrExprToAstTyped(Number(y), FloatType);
    } else if (typeof y === "number") {
      rightAst = valueOrExprToAstTyped(y, FloatType);
    } else if (y instanceof Expr) {
      if (isTypeEqual(Expr.type(y as Expr<IntegerType>), IntegerType)) {
        // Convert integer to float first
        rightAst = (y as IntegerExpr).toFloat()[AstSymbol];
      } else if (isTypeEqual(Expr.type(y as Expr<FloatType>), FloatType)) {
        rightAst = y[AstSymbol];
      } else {
        throw new Error(`Cannot add Float and ${printType(Expr.type(y as any))}`);
      }
    } else {
      throw new Error(`Cannot add Float and ${typeof y}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatDivide",
      type_parameters: [],
      arguments: [this[AstSymbol], rightAst],
    }) as FloatExpr;
  }

  /**
   * Computes floating-point remainder of division (x % y).
   *
   * @param y - The float, number, IntegerExpr, or bigint divisor
   * @returns A FloatExpr representing the remainder
   *
   * @remarks Uses IEEE 754 remainder semantics. Automatically converts integer operands to float.
   *
   * @example
   * ```ts
   * const remainderFloats = East.function([FloatType, FloatType], FloatType, ($, x, y) => {
   *   $.return(x.remainder(y));
   * });
   * const compiled = East.compile(remainderFloats.toIR(), []);
   * compiled(7.5, 2.0);    // 1.5
   * compiled(10.0, 3.0);   // 1.0
   * compiled(-7.5, 2.0);   // -1.5
   * ```
   */
  remainder(y: FloatExpr | number | IntegerExpr | bigint): FloatExpr {
    let rightAst: AST;
    if (typeof y === "bigint") {
      // Convert integer to float first
      rightAst = valueOrExprToAstTyped(Number(y), FloatType);
    } else if (typeof y === "number") {
      rightAst = valueOrExprToAstTyped(y, FloatType);
    } else if (y instanceof Expr) {
      if (isTypeEqual(Expr.type(y as Expr<IntegerType>), IntegerType)) {
        // Convert integer to float first
        rightAst = (y as IntegerExpr).toFloat()[AstSymbol];
      } else if (isTypeEqual(Expr.type(y as Expr<FloatType>), FloatType)) {
        rightAst = y[AstSymbol];
      } else {
        throw new Error(`Cannot add Float and ${printType(Expr.type(y as any))}`);
      }
    } else {
      throw new Error(`Cannot add Float and ${typeof y}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatRemainder",
      type_parameters: [],
      arguments: [this[AstSymbol], rightAst],
    }) as FloatExpr;
  }

  /**
   * Raises a floating-point number to a power (x ** y).
   *
   * @param y - The float, number, IntegerExpr, or bigint exponent
   * @returns A FloatExpr representing x raised to the power of y
   *
   * @remarks Automatically converts integer operands to float before exponentiation.
   *
   * @example
   * ```ts
   * const powFloats = East.function([FloatType, FloatType], FloatType, ($, x, y) => {
   *   $.return(x.pow(y));
   * });
   * const compiled = East.compile(powFloats.toIR(), []);
   * compiled(2.0, 3.0);    // 8.0
   * compiled(9.0, 0.5);    // 3.0 (square root)
   * compiled(2.0, -1.0);   // 0.5
   * compiled(-1.0, 0.5);   // NaN (square root of negative)
   * ```
   */
  pow(y: FloatExpr | number | IntegerExpr | bigint): FloatExpr {
    let rightAst: AST;
    if (typeof y === "bigint") {
      // Convert integer to float first
      rightAst = valueOrExprToAstTyped(Number(y), FloatType);
    } else if (typeof y === "number") {
      rightAst = valueOrExprToAstTyped(y, FloatType);
    } else if (y instanceof Expr) {
      if (isTypeEqual(Expr.type(y as Expr<IntegerType>), IntegerType)) {
        // Convert integer to float first
        rightAst = (y as IntegerExpr).toFloat()[AstSymbol];
      } else if (isTypeEqual(Expr.type(y as Expr<FloatType>), FloatType)) {
        rightAst = y[AstSymbol];
      } else {
        throw new Error(`Cannot add Float and ${printType(Expr.type(y as any))}`);
      }
    } else {
      throw new Error(`Cannot add Float and ${typeof y}`);
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatPow",
      type_parameters: [],
      arguments: [this[AstSymbol], rightAst],
    }) as FloatExpr;
  }

  /**
   * Computes the absolute value of a floating-point number (|x|).
   *
   * @returns A FloatExpr representing the absolute value
   *
   * @example
   * ```ts
   * const absFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.abs());
   * });
   * const compiled = East.compile(absFloat.toIR(), []);
   * compiled(3.14);     // 3.14
   * compiled(-2.5);     // 2.5
   * compiled(0.0);      // 0.0
   * compiled(-0.0);     // 0.0
   * ```
   */
  abs(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatAbs",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Computes the sign of a floating-point number.
   *
   * @returns A FloatExpr representing -1.0 for negative, 0.0 for zero, 1.0 for positive, or NaN for NaN
   *
   * @example
   * ```ts
   * const signFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.sign());
   * });
   * const compiled = East.compile(signFloat.toIR(), []);
   * compiled(3.14);     // 1.0
   * compiled(-2.5);     // -1.0
   * compiled(0.0);      // 0.0
   * compiled(-0.0);     // -0.0
   * ```
   */
  sign(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatSign",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Computes the square root of a floating-point number (√x).
   *
   * @returns A FloatExpr representing the square root
   *
   * @remarks Returns NaN for negative numbers.
   *
   * @example
   * ```ts
   * const sqrtFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.sqrt());
   * });
   * const compiled = East.compile(sqrtFloat.toIR(), []);
   * compiled(9.0);      // 3.0
   * compiled(2.0);      // 1.4142135623730951
   * compiled(0.0);      // 0.0
   * compiled(-1.0);     // NaN
   * ```
   */
  sqrt(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatSqrt",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Computes the exponential function (e^x).
   *
   * @returns A FloatExpr representing e raised to the power of x
   *
   * @example
   * ```ts
   * const expFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.exp());
   * });
   * const compiled = East.compile(expFloat.toIR(), []);
   * compiled(0.0);      // 1.0
   * compiled(1.0);      // 2.718281828459045
   * compiled(2.0);      // 7.38905609893065
   * compiled(-1.0);     // 0.36787944117144233
   * ```
   */
  exp(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatExp",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Computes the natural logarithm (ln(x)).
   *
   * @returns A FloatExpr representing the natural logarithm of x
   *
   * @remarks Returns NaN for negative numbers, -Infinity for 0.
   *
   * @example
   * ```ts
   * const logFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.log());
   * });
   * const compiled = East.compile(logFloat.toIR(), []);
   * compiled(Math.E);   // 1.0
   * compiled(1.0);      // 0.0
   * compiled(10.0);     // 2.302585092994046
   * compiled(0.0);      // -Infinity
   * compiled(-1.0);     // NaN
   * ```
   */
  log(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatLog",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Computes the sine of a floating-point number (sin(x)).
   *
   * @returns A FloatExpr representing the sine of x (x in radians)
   *
   * @example
   * ```ts
   * const sinFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.sin());
   * });
   * const compiled = East.compile(sinFloat.toIR(), []);
   * compiled(0.0);              // 0.0
   * compiled(Math.PI / 2);      // 1.0
   * compiled(Math.PI);          // ~0.0 (very close to zero)
   * compiled(Math.PI / 6);      // 0.5
   * ```
   */
  sin(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatSin",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Computes the cosine of a floating-point number (cos(x)).
   *
   * @returns A FloatExpr representing the cosine of x (x in radians)
   *
   * @example
   * ```ts
   * const cosFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.cos());
   * });
   * const compiled = East.compile(cosFloat.toIR(), []);
   * compiled(0.0);              // 1.0
   * compiled(Math.PI / 2);      // ~0.0 (very close to zero)
   * compiled(Math.PI);          // -1.0
   * compiled(Math.PI / 3);      // 0.5
   * ```
   */
  cos(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatCos",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Computes the tangent of a floating-point number (tan(x)).
   *
   * @returns A FloatExpr representing the tangent of x (x in radians)
   *
   * @example
   * ```ts
   * const tanFloat = East.function([FloatType], FloatType, ($, x) => {
   *   $.return(x.tan());
   * });
   * const compiled = East.compile(tanFloat.toIR(), []);
   * compiled(0.0);              // 0.0
   * compiled(Math.PI / 4);      // 1.0
   * compiled(Math.PI / 6);      // 0.5773502691896257
   * compiled(-Math.PI / 4);     // -1.0
   * ```
   */
  tan(): FloatExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatTan",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Converts a floating-point number to an integer.
   *
   * @returns An IntegerExpr representing the converted value
   *
   * @throws East runtime error if the float is NaN, infinite, larger than 2^63-1, smaller than -2^63, or not an integer value
   *
   * @example
   * ```ts
   * const floatToInt = East.function([FloatType], IntegerType, ($, x) => {
   *   $.return(x.toInteger());
   * });
   * const compiled = East.compile(floatToInt.toIR(), []);
   * compiled(42.0);     // 42n
   * compiled(-10.0);    // -10n
   * compiled(0.0);      // 0n
   * // compiled(3.14) would throw error (not an integer value)
   * // compiled(NaN) would throw error
   * // compiled(Infinity) would throw error
   * ```
   */
  toInteger(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "FloatToInteger",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // Comparison methods
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Checks if this float equals another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are equal
   *
   * @example
   * ```ts
   * const checkEqual = East.function([FloatType, FloatType], BooleanType, ($, x, y) => {
   *   $.return(x.equals(y));
   * });
   * const compiled = East.compile(checkEqual.toIR(), []);
   * compiled(3.14, 3.14);  // true
   * compiled(3.14, 2.0);   // false
   * ```
   */
  equals(other: FloatExpr | number): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this float does not equal another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are not equal
   *
   * @example
   * ```ts
   * const checkNotEqual = East.function([FloatType, FloatType], BooleanType, ($, x, y) => {
   *   $.return(x.notEquals(y));
   * });
   * const compiled = East.compile(checkNotEqual.toIR(), []);
   * compiled(3.14, 2.0);   // true
   * compiled(3.14, 3.14);  // false
   * ```
   */
  notEquals(other: FloatExpr | number): BooleanExpr {
    return notEqual(this, other);
  }

  /**
   * Checks if this float is greater than another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this value is greater
   *
   * @example
   * ```ts
   * const checkGreater = East.function([FloatType, FloatType], BooleanType, ($, x, y) => {
   *   $.return(x.greaterThan(y));
   * });
   * const compiled = East.compile(checkGreater.toIR(), []);
   * compiled(3.14, 2.0);   // true
   * compiled(2.0, 3.14);   // false
   * compiled(3.14, 3.14);  // false
   * ```
   */
  greaterThan(other: FloatExpr | number): BooleanExpr {
    return greater(this, other);
  }

  /**
   * Checks if this float is less than another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this value is less
   *
   * @example
   * ```ts
   * const checkLess = East.function([FloatType, FloatType], BooleanType, ($, x, y) => {
   *   $.return(x.lessThan(y));
   * });
   * const compiled = East.compile(checkLess.toIR(), []);
   * compiled(2.0, 3.14);   // true
   * compiled(3.14, 2.0);   // false
   * compiled(3.14, 3.14);  // false
   * ```
   */
  lessThan(other: FloatExpr | number): BooleanExpr {
    return less(this, other);
  }

  /**
   * Checks if this float is greater than or equal to another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this value is greater than or equal
   *
   * @example
   * ```ts
   * const checkGte = East.function([FloatType, FloatType], BooleanType, ($, x, y) => {
   *   $.return(x.greaterThanOrEqual(y));
   * });
   * const compiled = East.compile(checkGte.toIR(), []);
   * compiled(3.14, 2.0);   // true
   * compiled(3.14, 3.14);  // true
   * compiled(2.0, 3.14);   // false
   * ```
   */
  greaterThanOrEqual(other: FloatExpr | number): BooleanExpr {
    return greaterEqual(this, other);
  }

  /**
   * Checks if this float is less than or equal to another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this value is less than or equal
   *
   * @example
   * ```ts
   * const checkLte = East.function([FloatType, FloatType], BooleanType, ($, x, y) => {
   *   $.return(x.lessThanOrEqual(y));
   * });
   * const compiled = East.compile(checkLte.toIR(), []);
   * compiled(2.0, 3.14);   // true
   * compiled(3.14, 3.14);  // true
   * compiled(3.14, 2.0);   // false
   * ```
   */
  lessThanOrEqual(other: FloatExpr | number): BooleanExpr {
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