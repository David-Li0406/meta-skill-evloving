/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import type { AST } from "../ast.js";
import { get_location } from "../location.js";
import { ArrayType, DateTimeType, FloatType, IntegerType, StringType } from "../types.js";
import type { FloatExpr } from "./float.js";
import type { IntegerExpr } from "./integer.js";
import type { StringExpr } from "./string.js";
import { AstSymbol, Expr, FactorySymbol, TypeSymbol, type ToExpr } from "./expr.js";
import { valueOrExprToAst } from "./ast.js";
import { tokenizeDateTimeFormat } from "../datetime_format/tokenize.js";
import { DateTimeFormatTokenType } from "../datetime_format/types.js";
import { validateDateTimeFormatTokens } from "../datetime_format/validate.js";
import type { SubtypeExprOrValue } from "./types.js";
import type { BooleanExpr } from "./boolean.js";
import { equal, notEqual, less, lessEqual, greater, greaterEqual } from "./block.js";

/**
 * Expression representing date and time values and operations.
 *
 * DateTimeExpr provides methods for extracting components (year, month, day, hour, etc.),
 * adding/subtracting durations, calculating differences, formatting, and parsing.
 * DateTime values are immutable and represent UTC timestamps with millisecond precision.
 *
 * @example
 * ```ts
 * // Creating and manipulating dates
 * const addTime = East.function([DateTimeType], DateTimeType, ($, date) => {
 *   const tomorrow = date.addDays(1n);
 *   const nextWeek = date.addWeeks(1n);
 *   $.return(nextWeek);
 * });
 *
 * // Extracting components
 * const getComponents = East.function([DateTimeType], StructType({year: IntegerType, month: IntegerType}), ($, date) => {
 *   $.return({year: date.getYear(), month: date.getMonth()});
 * });
 *
 * // Formatting dates
 * const formatDate = East.function([DateTimeType], StringType, ($, date) => {
 *   $.return(date.printFormatted("YYYY-MM-DD HH:mm:ss"));
 * });
 * ```
 */
export class DateTimeExpr extends Expr<DateTimeType> {
  constructor(ast: AST, createExpr: ToExpr) {
    super(DateTimeType, ast, createExpr);
  }

  /**
   * Extracts the year component from the DateTime.
   *
   * @returns An IntegerExpr representing the year (e.g., 2025n)
   *
   * @example
   * ```ts
   * const extractYear = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.getYear());
   * });
   * const compiled = East.compile(extractYear.toIR(), []);
   * compiled(new Date("2025-01-15T10:30:00.000Z"));  // 2025n
   * compiled(new Date("1999-12-31T23:59:59.999Z"));  // 1999n
   * ```
   */
  getYear(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeGetYear",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Extracts the month component from the DateTime.
   *
   * @returns An IntegerExpr representing the month (1-12, where 1 = January, 12 = December)
   *
   * @example
   * ```ts
   * const extractMonth = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.getMonth());
   * });
   * const compiled = East.compile(extractMonth.toIR(), []);
   * compiled(new Date("2025-01-15T10:30:00.000Z"));  // 1n
   * compiled(new Date("2025-12-31T23:59:59.999Z"));  // 12n
   * ```
   */
  getMonth(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeGetMonth",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Extracts the day of the month from the DateTime.
   *
   * @returns An IntegerExpr representing the day (1-31)
   *
   * @example
   * ```ts
   * const extractDay = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.getDayOfMonth());
   * });
   * const compiled = East.compile(extractDay.toIR(), []);
   * compiled(new Date("2025-01-15T10:30:00.000Z"));  // 15n
   * compiled(new Date("2025-02-28T12:00:00.000Z"));  // 28n
   * ```
   */
  getDayOfMonth(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeGetDayOfMonth",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Extracts the hour component from the DateTime.
   *
   * @returns An IntegerExpr representing the hour (0-23 in 24-hour format)
   *
   * @example
   * ```ts
   * const extractHour = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.getHour());
   * });
   * const compiled = East.compile(extractHour.toIR(), []);
   * compiled(new Date("2025-01-15T14:30:00.000Z"));  // 14n
   * compiled(new Date("2025-01-15T00:00:00.000Z"));  // 0n
   * ```
   */
  getHour(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeGetHour",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Extracts the minute component from the DateTime.
   *
   * @returns An IntegerExpr representing the minute (0-59)
   *
   * @example
   * ```ts
   * const extractMinute = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.getMinute());
   * });
   * const compiled = East.compile(extractMinute.toIR(), []);
   * compiled(new Date("2025-01-15T14:30:45.000Z"));  // 30n
   * compiled(new Date("2025-01-15T14:00:00.000Z"));  // 0n
   * ```
   */
  getMinute(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeGetMinute",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Extracts the second component from the DateTime.
   *
   * @returns An IntegerExpr representing the second (0-59)
   *
   * @example
   * ```ts
   * const extractSecond = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.getSecond());
   * });
   * const compiled = East.compile(extractSecond.toIR(), []);
   * compiled(new Date("2025-01-15T14:30:45.000Z"));  // 45n
   * compiled(new Date("2025-01-15T14:30:00.000Z"));  // 0n
   * ```
   */
  getSecond(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeGetSecond",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Extracts the day of the week from the DateTime.
   *
   * @returns An IntegerExpr representing the day (0-6, where 0 = Sunday, 6 = Saturday)
   *
   * @example
   * ```ts
   * const extractDayOfWeek = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.getDayOfWeek());
   * });
   * const compiled = East.compile(extractDayOfWeek.toIR(), []);
   * compiled(new Date("2025-01-15T00:00:00.000Z"));  // 3n (Wednesday)
   * compiled(new Date("2025-01-12T00:00:00.000Z"));  // 0n (Sunday)
   * ```
   */
  getDayOfWeek(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeGetDayOfWeek",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Extracts the millisecond component from the DateTime.
   *
   * @returns An IntegerExpr representing the millisecond (0-999)
   *
   * @example
   * ```ts
   * const extractMillisecond = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.getMillisecond());
   * });
   * const compiled = East.compile(extractMillisecond.toIR(), []);
   * compiled(new Date("2025-01-15T14:30:45.123Z"));  // 123n
   * compiled(new Date("2025-01-15T14:30:45.000Z"));  // 0n
   * ```
   */
  getMillisecond(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeGetMillisecond",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Adds milliseconds to the DateTime, returning a new DateTime.
   *
   * @param milliseconds - The number of milliseconds to add (integer or float)
   * @returns A DateTimeExpr representing the new DateTime
   *
   * @remarks Floats are rounded to the nearest millisecond. Accepts negative values.
   *
   * @example
   * ```ts
   * const addMs = East.function([DateTimeType, IntegerType], DateTimeType, ($, date, ms) => {
   *   $.return(date.addMilliseconds(ms));
   * });
   * const compiled = East.compile(addMs.toIR(), []);
   * const date = new Date("2025-01-15T14:30:45.000Z");
   * compiled(date, 500n);   // Date("2025-01-15T14:30:45.500Z")
   * compiled(date, 1000n);  // Date("2025-01-15T14:30:46.000Z")
   * ```
   */
  addMilliseconds(milliseconds: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    // Convert to bigint milliseconds
    let ms: Expr<IntegerType>;
    if (typeof milliseconds === 'bigint') {
      ms = Expr.from(milliseconds, IntegerType);
    } else if (typeof milliseconds === 'number') {
      // Round float to nearest millisecond and convert to bigint
      ms = Expr.from(BigInt(Math.round(milliseconds)), IntegerType);
    } else if (milliseconds[TypeSymbol] === IntegerType) {
      ms = milliseconds as Expr<IntegerType>;
    } else if (milliseconds[TypeSymbol] === FloatType) {
      // Convert float expression to integer expression by rounding
      ms = this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "FloatToInteger",
        type_parameters: [],
        arguments: [milliseconds[AstSymbol]],
      }) as Expr<IntegerType>;
    } else {
      throw new Error("Expected integer or float");
    }

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: DateTimeType,
      location: get_location(),
      builtin: "DateTimeAddMilliseconds",
      type_parameters: [],
      arguments: [this[AstSymbol], ms[AstSymbol]],
    }) as DateTimeExpr;
  }

  /**
   * Subtracts milliseconds from the DateTime, returning a new DateTime.
   *
   * @param milliseconds - The number of milliseconds to subtract (integer or float)
   * @returns A DateTimeExpr representing the new DateTime
   *
   * @remarks Floats are rounded to the nearest millisecond.
   *
   * @example
   * ```ts
   * const subMs = East.function([DateTimeType, IntegerType], DateTimeType, ($, date, ms) => {
   *   $.return(date.subtractMilliseconds(ms));
   * });
   * const compiled = East.compile(subMs.toIR(), []);
   * const date = new Date("2025-01-15T14:30:45.500Z");
   * compiled(date, 500n);   // Date("2025-01-15T14:30:45.000Z")
   * compiled(date, 1000n);  // Date("2025-01-15T14:30:44.500Z")
   * ```
   */
  subtractMilliseconds(milliseconds: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    // Negate the input and use addMilliseconds
    if (typeof milliseconds === 'bigint') {
      return this.addMilliseconds(-milliseconds);
    } else if (typeof milliseconds === 'number') {
      return this.addMilliseconds(-milliseconds);
    } else if (milliseconds[TypeSymbol] === IntegerType) {
      // Negate integer expression
      const negated = this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerNegate",
        type_parameters: [],
        arguments: [milliseconds[AstSymbol]],
      }) as Expr<IntegerType>;
      return this.addMilliseconds(negated);
    } else if (milliseconds[TypeSymbol] === FloatType) {
      // Negate float expression
      const negated = this[FactorySymbol]({
        ast_type: "Builtin",
        type: FloatType,
        location: get_location(),
        builtin: "FloatNegate",
        type_parameters: [],
        arguments: [milliseconds[AstSymbol]],
      }) as Expr<FloatType>;
      return this.addMilliseconds(negated);
    } else {
      throw new Error("Expected integer or float");
    }
  }

  /**
   * Adds seconds to the DateTime, returning a new DateTime.
   *
   * @param seconds - The number of seconds to add (integer or float)
   * @returns A DateTimeExpr representing the new DateTime
   *
   * @example
   * ```ts
   * const addSec = East.function([DateTimeType, IntegerType], DateTimeType, ($, date, secs) => {
   *   $.return(date.addSeconds(secs));
   * });
   * const compiled = East.compile(addSec.toIR(), []);
   * compiled(new Date("2025-01-15T14:30:00.000Z"), 30n);   // Date("2025-01-15T14:30:30.000Z")
   * ```
   */
  addSeconds(seconds: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._addDuration(seconds, 1000n, 1000);
  }

  /**
   * Adds minutes to the DateTime, returning a new DateTime.
   *
   * @param minutes - The number of minutes to add (integer or float)
   * @returns A DateTimeExpr representing the new DateTime
   *
   * @example
   * ```ts
   * const addMin = East.function([DateTimeType, IntegerType], DateTimeType, ($, date, mins) => {
   *   $.return(date.addMinutes(mins));
   * });
   * const compiled = East.compile(addMin.toIR(), []);
   * compiled(new Date("2025-01-15T14:00:00.000Z"), 30n);   // Date("2025-01-15T14:30:00.000Z")
   * ```
   */
  addMinutes(minutes: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._addDuration(minutes, 60000n, 60000);
  }

  /**
   * Adds hours to the DateTime, returning a new DateTime.
   *
   * @param hours - The number of hours to add (integer or float)
   * @returns A DateTimeExpr representing the new DateTime
   *
   * @example
   * ```ts
   * const addHr = East.function([DateTimeType, IntegerType], DateTimeType, ($, date, hrs) => {
   *   $.return(date.addHours(hrs));
   * });
   * const compiled = East.compile(addHr.toIR(), []);
   * compiled(new Date("2025-01-15T14:00:00.000Z"), 2n);    // Date("2025-01-15T16:00:00.000Z")
   * ```
   */
  addHours(hours: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._addDuration(hours, 3600000n, 3600000);
  }

  /**
   * Adds days to the DateTime, returning a new DateTime.
   *
   * @param days - The number of days to add (integer or float)
   * @returns A DateTimeExpr representing the new DateTime
   *
   * @example
   * ```ts
   * const addDay = East.function([DateTimeType, IntegerType], DateTimeType, ($, date, days) => {
   *   $.return(date.addDays(days));
   * });
   * const compiled = East.compile(addDay.toIR(), []);
   * compiled(new Date("2025-01-15T00:00:00.000Z"), 1n);    // Date("2025-01-16T00:00:00.000Z")
   * compiled(new Date("2025-01-31T00:00:00.000Z"), 1n);    // Date("2025-02-01T00:00:00.000Z")
   * ```
   */
  addDays(days: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._addDuration(days, 86400000n, 86400000);
  }

  /**
   * Adds weeks to the DateTime, returning a new DateTime.
   *
   * @param weeks - The number of weeks to add (integer or float)
   * @returns A DateTimeExpr representing the new DateTime
   *
   * @example
   * ```ts
   * const addWk = East.function([DateTimeType, IntegerType], DateTimeType, ($, date, weeks) => {
   *   $.return(date.addWeeks(weeks));
   * });
   * const compiled = East.compile(addWk.toIR(), []);
   * compiled(new Date("2025-01-15T00:00:00.000Z"), 1n);    // Date("2025-01-22T00:00:00.000Z")
   * compiled(new Date("2025-01-15T00:00:00.000Z"), 2n);    // Date("2025-01-29T00:00:00.000Z")
   * ```
   */
  addWeeks(weeks: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._addDuration(weeks, 604800000n, 604800000); // 7 * 24 * 60 * 60 * 1000 = 604800000ms
  }

  /**
   * Subtracts seconds from the DateTime, returning a new DateTime.
   *
   * @param seconds - The number of seconds to subtract
   * @returns A DateTimeExpr representing the new DateTime
   */
  subtractSeconds(seconds: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._subtractDuration(seconds, 1000n, 1000);
  }

  /**
   * Subtracts minutes from the DateTime, returning a new DateTime.
   *
   * @param minutes - The number of minutes to subtract
   * @returns A DateTimeExpr representing the new DateTime
   */
  subtractMinutes(minutes: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._subtractDuration(minutes, 60000n, 60000);
  }

  /**
   * Subtracts hours from the DateTime, returning a new DateTime.
   *
   * @param hours - The number of hours to subtract
   * @returns A DateTimeExpr representing the new DateTime
   */
  subtractHours(hours: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._subtractDuration(hours, 3600000n, 3600000);
  }

  /**
   * Subtracts days from the DateTime, returning a new DateTime.
   *
   * @param days - The number of days to subtract
   * @returns A DateTimeExpr representing the new DateTime
   */
  subtractDays(days: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._subtractDuration(days, 86400000n, 86400000);
  }

  /**
   * Subtracts weeks from the DateTime, returning a new DateTime.
   *
   * @param weeks - The number of weeks to subtract
   * @returns A DateTimeExpr representing the new DateTime
   */
  subtractWeeks(weeks: bigint | number | Expr<IntegerType> | Expr<FloatType>): DateTimeExpr {
    return this._subtractDuration(weeks, 604800000n, 604800000); // 7 * 24 * 60 * 60 * 1000 = 604800000ms
  }

  /**
   * Helper method to add duration with conversion factor
   */
  private _addDuration(
    value: bigint | number | Expr<IntegerType> | Expr<FloatType>,
    bigintFactor: bigint,
    numberFactor: number
  ): DateTimeExpr {
    let ms: Expr<IntegerType>;
    
    if (typeof value === 'bigint') {
      ms = Expr.from(value * bigintFactor, IntegerType);
    } else if (typeof value === 'number') {
      // Round to nearest millisecond after conversion
      ms = Expr.from(BigInt(Math.round(value * numberFactor)), IntegerType);
    } else if (value[TypeSymbol] === IntegerType) {
      // Multiply integer expression by factor
      const factorExpr = Expr.from(bigintFactor, IntegerType);
      ms = this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerMultiply",
        type_parameters: [],
        arguments: [value[AstSymbol], factorExpr[AstSymbol]],
      }) as Expr<IntegerType>;
    } else if (value[TypeSymbol] === FloatType) {
      // Convert float to integer, then multiply by factor
      const intValue = this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "FloatToInteger",
        type_parameters: [],
        arguments: [value[AstSymbol]],
      }) as Expr<IntegerType>;
      
      const factorExpr = Expr.from(bigintFactor, IntegerType);
      ms = this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerMultiply",
        type_parameters: [],
        arguments: [intValue[AstSymbol], factorExpr[AstSymbol]],
      }) as Expr<IntegerType>;
    } else {
      throw new Error("Expected integer or float");
    }

    return this.addMilliseconds(ms);
  }

  /**
   * Helper method to subtract duration with conversion factor
   */
  private _subtractDuration(
    value: bigint | number | Expr<IntegerType> | Expr<FloatType>,
    bigintFactor: bigint,
    numberFactor: number
  ): DateTimeExpr {
    let negatedValue: bigint | number | Expr<IntegerType> | Expr<FloatType>;
    
    if (typeof value === 'bigint') {
      negatedValue = -value;
    } else if (typeof value === 'number') {
      negatedValue = -value;
    } else if (value[TypeSymbol] === IntegerType) {
      // Negate integer expression
      negatedValue = this[FactorySymbol]({
        ast_type: "Builtin",
        type: IntegerType,
        location: get_location(),
        builtin: "IntegerNegate",
        type_parameters: [],
        arguments: [value[AstSymbol]],
      }) as Expr<IntegerType>;
    } else if (value[TypeSymbol] === FloatType) {
      // Negate float expression
      negatedValue = this[FactorySymbol]({
        ast_type: "Builtin",
        type: FloatType,
        location: get_location(),
        builtin: "FloatNegate",
        type_parameters: [],
        arguments: [value[AstSymbol]],
      }) as Expr<FloatType>;
    } else {
      throw new Error("Expected integer or float");
    }

    return this._addDuration(negatedValue, bigintFactor, numberFactor);
  }

  /**
   * Calculates the duration in milliseconds between this DateTime and another.
   *
   * @param other - The DateTime to compare with
   * @returns An IntegerExpr representing the duration (positive if other is after this, negative if before)
   *
   * @example
   * ```ts
   * const getDuration = East.function([DateTimeType, DateTimeType], IntegerType, ($, date1, date2) => {
   *   $.return(date1.durationMilliseconds(date2));
   * });
   * const compiled = East.compile(getDuration.toIR(), []);
   * const d1 = new Date("2025-01-15T14:30:00.000Z");
   * const d2 = new Date("2025-01-15T14:30:01.500Z");
   * compiled(d1, d2);   // 1500n (1.5 seconds later)
   * compiled(d2, d1);   // -1500n (1.5 seconds earlier)
   * ```
   */
  durationMilliseconds(other: SubtypeExprOrValue<DateTimeType>): IntegerExpr {
    const otherAst = valueOrExprToAst(other);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeDurationMilliseconds",
      type_parameters: [],
      arguments: [otherAst, this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Calculates the duration in seconds between this DateTime and another.
   *
   * @param other - The DateTime to compare with
   * @returns A FloatExpr representing the duration in seconds
   *
   * @example
   * ```ts
   * const getDurationSec = East.function([DateTimeType, DateTimeType], FloatType, ($, date1, date2) => {
   *   $.return(date1.durationSeconds(date2));
   * });
   * const compiled = East.compile(getDurationSec.toIR(), []);
   * const d1 = new Date("2025-01-15T14:30:00.000Z");
   * const d2 = new Date("2025-01-15T14:30:30.000Z");
   * compiled(d1, d2);   // 30.0 (30 seconds later)
   * ```
   */
  durationSeconds(other: SubtypeExprOrValue<DateTimeType>): FloatExpr {
    const milliseconds = this.durationMilliseconds(other);
    
    // Convert to float
    const millisecondsFloat = this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "IntegerToFloat",
      type_parameters: [],
      arguments: [milliseconds[AstSymbol]],
    }) as FloatExpr;

    // Divide by 1000 to get seconds
    const divisor = Expr.from(1000.0, FloatType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatDivide",
      type_parameters: [],
      arguments: [millisecondsFloat[AstSymbol], divisor[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Calculates the duration in minutes between this DateTime and another.
   *
   * @param other - The DateTime to compare with
   * @returns A FloatExpr representing the duration in minutes
   *
   * @example
   * ```ts
   * const getDurationMin = East.function([DateTimeType, DateTimeType], FloatType, ($, date1, date2) => {
   *   $.return(date1.durationMinutes(date2));
   * });
   * const compiled = East.compile(getDurationMin.toIR(), []);
   * const d1 = new Date("2025-01-15T14:00:00.000Z");
   * const d2 = new Date("2025-01-15T14:30:00.000Z");
   * compiled(d1, d2);   // 30.0 (30 minutes later)
   * ```
   */
  durationMinutes(other: SubtypeExprOrValue<DateTimeType>): FloatExpr {
    const milliseconds = this.durationMilliseconds(other);
    
    // Convert to float
    const millisecondsFloat = this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "IntegerToFloat",
      type_parameters: [],
      arguments: [milliseconds[AstSymbol]],
    }) as FloatExpr;

    // Divide by 60000 to get minutes
    const divisor = Expr.from(60000.0, FloatType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatDivide",
      type_parameters: [],
      arguments: [millisecondsFloat[AstSymbol], divisor[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Calculates the duration in hours between this DateTime and another.
   *
   * @param other - The DateTime to compare with
   * @returns A FloatExpr representing the duration in hours
   *
   * @example
   * ```ts
   * const getDurationHr = East.function([DateTimeType, DateTimeType], FloatType, ($, date1, date2) => {
   *   $.return(date1.durationHours(date2));
   * });
   * const compiled = East.compile(getDurationHr.toIR(), []);
   * const d1 = new Date("2025-01-15T10:00:00.000Z");
   * const d2 = new Date("2025-01-15T14:30:00.000Z");
   * compiled(d1, d2);   // 4.5 (4.5 hours later)
   * ```
   */
  durationHours(other: SubtypeExprOrValue<DateTimeType>): FloatExpr {
    const milliseconds = this.durationMilliseconds(other);
    
    // Convert to float
    const millisecondsFloat = this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "IntegerToFloat",
      type_parameters: [],
      arguments: [milliseconds[AstSymbol]],
    }) as FloatExpr;

    // Divide by 3600000 to get hours
    const divisor = Expr.from(3600000.0, FloatType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatDivide",
      type_parameters: [],
      arguments: [millisecondsFloat[AstSymbol], divisor[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Calculates the duration in days between this DateTime and another.
   *
   * @param other - The DateTime to compare with
   * @returns A FloatExpr representing the duration in days
   *
   * @example
   * ```ts
   * const getDurationDay = East.function([DateTimeType, DateTimeType], FloatType, ($, date1, date2) => {
   *   $.return(date1.durationDays(date2));
   * });
   * const compiled = East.compile(getDurationDay.toIR(), []);
   * const d1 = new Date("2025-01-15T00:00:00.000Z");
   * const d2 = new Date("2025-01-17T12:00:00.000Z");
   * compiled(d1, d2);   // 2.5 (2.5 days later)
   * ```
   */
  durationDays(other: SubtypeExprOrValue<DateTimeType>): FloatExpr {
    const milliseconds = this.durationMilliseconds(other);
    
    // Convert to float
    const millisecondsFloat = this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "IntegerToFloat",
      type_parameters: [],
      arguments: [milliseconds[AstSymbol]],
    }) as FloatExpr;

    // Divide by 86400000 to get days
    const divisor = Expr.from(86400000.0, FloatType);
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatDivide",
      type_parameters: [],
      arguments: [millisecondsFloat[AstSymbol], divisor[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Calculates the duration in weeks between this DateTime and another.
   *
   * @param other - The DateTime to compare with
   * @returns A FloatExpr representing the duration in weeks
   *
   * @example
   * ```ts
   * const getDurationWk = East.function([DateTimeType, DateTimeType], FloatType, ($, date1, date2) => {
   *   $.return(date1.durationWeeks(date2));
   * });
   * const compiled = East.compile(getDurationWk.toIR(), []);
   * const d1 = new Date("2025-01-01T00:00:00.000Z");
   * const d2 = new Date("2025-01-15T00:00:00.000Z");
   * compiled(d1, d2);   // 2.0 (2 weeks later)
   * ```
   */
  durationWeeks(other: SubtypeExprOrValue<DateTimeType>): FloatExpr {
    const milliseconds = this.durationMilliseconds(other);
    
    // Convert to float
    const millisecondsFloat = this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "IntegerToFloat",
      type_parameters: [],
      arguments: [milliseconds[AstSymbol]],
    }) as FloatExpr;

    // Divide by 604800000 to get weeks
    const divisor = Expr.from(604800000.0, FloatType); // 7 * 24 * 60 * 60 * 1000 = 604800000ms
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: FloatType,
      location: get_location(),
      builtin: "FloatDivide",
      type_parameters: [],
      arguments: [millisecondsFloat[AstSymbol], divisor[AstSymbol]],
    }) as FloatExpr;
  }

  /**
   * Converts the DateTime to milliseconds since the Unix epoch (like Date.valueOf()).
   *
   * @returns An IntegerExpr representing milliseconds since January 1, 1970 00:00:00 UTC
   *
   * @example
   * ```ts
   * const toEpoch = East.function([DateTimeType], IntegerType, ($, date) => {
   *   $.return(date.toEpochMilliseconds());
   * });
   * const compiled = East.compile(toEpoch.toIR(), []);
   * compiled(new Date("1970-01-01T00:00:00.000Z"));  // 0n
   * compiled(new Date("2025-01-15T14:30:45.123Z"));  // 1736950245123n
   * ```
   */
  toEpochMilliseconds(): IntegerExpr {
    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: IntegerType,
      location: get_location(),
      builtin: "DateTimeToEpochMilliseconds",
      type_parameters: [],
      arguments: [this[AstSymbol]],
    }) as IntegerExpr;
  }

  /**
   * Format DateTime as a string using Day.js-style format tokens.
   *
   * @param formatString - Format string using Day.js syntax (e.g., "YYYY-MM-DD HH:mm:ss")
   * @returns A StringExpr containing the formatted datetime
   *
   * @remarks
   * The format string is parsed at compile time into structured tokens.
   * Use backslash to escape characters: `\Y` produces literal "Y".
   *
   * Supported tokens:
   * - Year: YYYY (4-digit), YY (2-digit)
   * - Month: M (1-12), MM (01-12), MMM (Jan), MMMM (January)
   * - Day: D (1-31), DD (01-31)
   * - Weekday: dd (Su), ddd (Sun), dddd (Sunday)
   * - Hour 24h: H (0-23), HH (00-23)
   * - Hour 12h: h (1-12), hh (01-12)
   * - Minute: m (0-59), mm (00-59)
   * - Second: s (0-59), ss (00-59)
   * - Millisecond: SSS (000-999)
   * - AM/PM: A (AM/PM), a (am/pm)
   *
   * @example
   * ```ts
   * const date = fromComponents(2025n, 1n, 15n, 14n, 30n, 45n);
   * date.printFormatted("YYYY-MM-DD HH:mm:ss");
   * // Returns: "2025-01-15 14:30:45"
   * ```
   *
   * @example
   * ```ts
   * const date = fromComponents(2025n, 1n, 15n, 14n, 30n);
   * date.printFormatted("MMMM D, YYYY \\a\\t h:mm A");
   * // Returns: "January 15, 2025 at 2:30 PM"
   * ```
   */
  printFormatted(formatString: string): StringExpr {
    // Parse format string at compile time to tokens
    const tokens = tokenizeDateTimeFormat(formatString);

    // Create a literal array of format tokens
    const tokensArray = Expr.from(tokens, ArrayType(DateTimeFormatTokenType));

    return this[FactorySymbol]({
      ast_type: "Builtin",
      type: StringType,
      location: get_location(),
      builtin: "DateTimePrintFormat",
      type_parameters: [],
      arguments: [this[AstSymbol], tokensArray[AstSymbol]],
    }) as StringExpr;
  }

  /**
   * Checks if this DateTime equals another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are equal
   *
   * @example
   * ```ts
   * const isEqual = East.function([DateTimeType, DateTimeType], BooleanType, ($, a, b) => {
   *   $.return(a.equals(b));
   * });
   * const compiled = East.compile(isEqual.toIR(), []);
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // true
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-16T00:00:00.000Z"));  // false
   * ```
   */
  equals(other: DateTimeExpr | Date): BooleanExpr {
    return equal(this, other);
  }

  /**
   * Checks if this DateTime does not equal another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if the values are not equal
   *
   * @example
   * ```ts
   * const isNotEqual = East.function([DateTimeType, DateTimeType], BooleanType, ($, a, b) => {
   *   $.return(a.notEquals(b));
   * });
   * const compiled = East.compile(isNotEqual.toIR(), []);
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-16T00:00:00.000Z"));  // true
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // false
   * ```
   */
  notEquals(other: DateTimeExpr | Date): BooleanExpr {
    return notEqual(this, other);
  }

  /**
   * Checks if this DateTime is after another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this DateTime is after the other
   *
   * @example
   * ```ts
   * const isAfter = East.function([DateTimeType, DateTimeType], BooleanType, ($, a, b) => {
   *   $.return(a.greaterThan(b));
   * });
   * const compiled = East.compile(isAfter.toIR(), []);
   * compiled(new Date("2025-01-16T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // true
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-16T00:00:00.000Z"));  // false
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // false
   * ```
   */
  greaterThan(other: DateTimeExpr | Date): BooleanExpr {
    return greater(this, other);
  }

  /**
   * Checks if this DateTime is before another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this DateTime is before the other
   *
   * @example
   * ```ts
   * const isBefore = East.function([DateTimeType, DateTimeType], BooleanType, ($, a, b) => {
   *   $.return(a.lessThan(b));
   * });
   * const compiled = East.compile(isBefore.toIR(), []);
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-16T00:00:00.000Z"));  // true
   * compiled(new Date("2025-01-16T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // false
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // false
   * ```
   */
  lessThan(other: DateTimeExpr | Date): BooleanExpr {
    return less(this, other);
  }

  /**
   * Checks if this DateTime is after or equal to another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this DateTime is after or equal to the other
   *
   * @example
   * ```ts
   * const isAfterOrEqual = East.function([DateTimeType, DateTimeType], BooleanType, ($, a, b) => {
   *   $.return(a.greaterThanOrEqual(b));
   * });
   * const compiled = East.compile(isAfterOrEqual.toIR(), []);
   * compiled(new Date("2025-01-16T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // true
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // true
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-16T00:00:00.000Z"));  // false
   * ```
   */
  greaterThanOrEqual(other: DateTimeExpr | Date): BooleanExpr {
    return greaterEqual(this, other);
  }

  /**
   * Checks if this DateTime is before or equal to another value.
   *
   * @param other - The value to compare against
   * @returns A BooleanExpr that is true if this DateTime is before or equal to the other
   *
   * @example
   * ```ts
   * const isBeforeOrEqual = East.function([DateTimeType, DateTimeType], BooleanType, ($, a, b) => {
   *   $.return(a.lessThanOrEqual(b));
   * });
   * const compiled = East.compile(isBeforeOrEqual.toIR(), []);
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-16T00:00:00.000Z"));  // true
   * compiled(new Date("2025-01-15T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // true
   * compiled(new Date("2025-01-16T00:00:00.000Z"), new Date("2025-01-15T00:00:00.000Z"));  // false
   * ```
   */
  lessThanOrEqual(other: DateTimeExpr | Date): BooleanExpr {
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
}

export function fromEpochMilliseconds(milliseconds: IntegerExpr | bigint): DateTimeExpr {
  const millis = typeof milliseconds === 'bigint' ? Expr.from(milliseconds, IntegerType) : milliseconds;
  if (millis[TypeSymbol] !== IntegerType) {
    throw new Error("Expected integer or bigint");
  }

  return Expr.fromAst({
    ast_type: "Builtin",
    type: DateTimeType,
    location: get_location(),
    builtin: "DateTimeFromEpochMilliseconds",
    type_parameters: [],
    arguments: [millis[AstSymbol]],
  }) as DateTimeExpr;
};

export function fromComponents(
  year: IntegerExpr | bigint,
  month: IntegerExpr | bigint = 1n,
  day: IntegerExpr | bigint = 1n,
  hour: IntegerExpr | bigint = 0n,
  minute: IntegerExpr | bigint = 0n,
  second: IntegerExpr | bigint = 0n,
  millisecond: IntegerExpr | bigint = 0n,
): DateTimeExpr {
  const y = typeof year === 'bigint' ? Expr.from(year, IntegerType) : year;
  const mo = typeof month === 'bigint' ? Expr.from(month, IntegerType) : month;
  const d = typeof day === 'bigint' ? Expr.from(day, IntegerType) : day;
  const h = typeof hour === 'bigint' ? Expr.from(hour, IntegerType) : hour;
  const mi = typeof minute === 'bigint' ? Expr.from(minute, IntegerType) : minute;
  const s = typeof second === 'bigint' ? Expr.from(second, IntegerType) : second;
  const ms = typeof millisecond === 'bigint' ? Expr.from(millisecond, IntegerType) : millisecond;

  if (y[TypeSymbol] !== IntegerType || mo[TypeSymbol] !== IntegerType || d[TypeSymbol] !== IntegerType ||
      h[TypeSymbol] !== IntegerType || mi[TypeSymbol] !== IntegerType || s[TypeSymbol] !== IntegerType ||
      ms[TypeSymbol] !== IntegerType) {
    throw new Error("Expected integer or bigint for all components");
  }

  return Expr.fromAst({
    ast_type: "Builtin",
    type: DateTimeType,
    location: get_location(),
    builtin: "DateTimeFromComponents",
    type_parameters: [],
    arguments: [y[AstSymbol], mo[AstSymbol], d[AstSymbol], h[AstSymbol], mi[AstSymbol], s[AstSymbol], ms[AstSymbol]],
  }) as DateTimeExpr;
};

/**
 * Parse a string into a DateTime using Day.js-style format tokens.
 *
 * @param input - The string to parse (literal string or StringExpr)
 * @param formatString - Format string using Day.js syntax (e.g., "YYYY-MM-DD HH:mm:ss")
 * @returns A DateTimeExpr containing the parsed datetime
 * @throws {EastError} At runtime if the string doesn't match the format or contains invalid values
 *
 * @remarks
 * The format string is parsed at compile time into structured tokens.
 * Use backslash to escape characters: `\Y` produces literal "Y".
 * All parsing is done in UTC (naive datetime).
 *
 * Supported tokens:
 * - Year: YYYY (4-digit), YY (2-digit, 00-99 → 2000-2099)
 * - Month: M (1-12), MM (01-12), MMM (Jan), MMMM (January) - case insensitive
 * - Day: D (1-31), DD (01-31)
 * - Weekday: dd (Su), ddd (Sun), dddd (Sunday) - consumed but not validated
 * - Hour 24h: H (0-23), HH (00-23)
 * - Hour 12h: h (1-12), hh (01-12) - requires A/a token
 * - Minute: m (0-59), mm (00-59)
 * - Second: s (0-59), ss (00-59)
 * - Millisecond: SSS (000-999)
 * - AM/PM: A (AM/PM), a (am/pm) - case insensitive
 *
 * @example
 * ```ts
 * // Parse ISO 8601 datetime
 * const date = parseFormatted("2025-01-15 14:30:45", "YYYY-MM-DD HH:mm:ss");
 * ```
 *
 * @example
 * ```ts
 * // Parse with month names and 12-hour time
 * const date = parseFormatted("January 15, 2025 at 2:30 PM", "MMMM D, YYYY \\a\\t h:mm A");
 * ```
 *
 * @example
 * ```ts
 * // Parse runtime string expression
 * const userInput = Expr.from(getUserInput(), StringType);
 * const date = parseFormatted(userInput, "MM/DD/YYYY");
 * ```
 */
export function parseFormatted(input: string | StringExpr, formatString: string): DateTimeExpr {
  // Convert input to StringExpr if it's a literal string
  const inputExpr = typeof input === 'string' ? Expr.from(input, StringType) : input;
  if (inputExpr[TypeSymbol] !== StringType) {
    throw new Error("Expected string or StringExpr");
  }

  // Parse format string at compile time to tokens
  const tokens = tokenizeDateTimeFormat(formatString);

  // Validate format tokens at compile time for early error detection
  const validation = validateDateTimeFormatTokens(tokens);
  if (!validation.valid) {
    throw new Error(`Invalid datetime format string "${formatString}": ${validation.error}`);
  }

  // Create a literal array of format tokens
  const tokensArray = Expr.from(tokens, ArrayType(DateTimeFormatTokenType));

  return Expr.fromAst({
    ast_type: "Builtin",
    type: DateTimeType,
    location: get_location(),
    builtin: "DateTimeParseFormat",
    type_parameters: [],
    arguments: [inputExpr[AstSymbol], tokensArray[AstSymbol]],
  }) as DateTimeExpr;
};