/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { DateTimeType, IntegerType } from "../../types.js";
import { fromComponents, fromEpochMilliseconds, parseFormatted } from "../datetime.js";
import { Expr } from "../expr.js";

/** Standard library functions for datetimes */
export default {
  /**
   * Creates a DateTime from milliseconds since Unix epoch.
   *
   * @param milliseconds - The number of milliseconds since Unix epoch
   * @returns A DateTime expression representing the specified instant
   *
   * @remarks
   * Similar to JavaScript's `new Date(ms)`, this function converts a timestamp
   * (milliseconds since January 1, 1970 00:00:00 UTC) into an East DateTime.
   *
   * @example
   * ```ts
   * const fromEpoch = East.function([IntegerType], DateTimeType, ($, ms) => {
   *   $.return(East.DateTime.fromEpochMilliseconds(ms));
   * });
   * const compiled = East.compile(fromEpoch.toIR(), []);
   * compiled(0n);              // 1970-01-01T00:00:00.000Z
   * compiled(1609459200000n);  // 2021-01-01T00:00:00.000Z
   * ```
   */
  fromEpochMilliseconds,

  /**
   * Creates a DateTime from individual date and time components.
   *
   * @param year - The year component
   * @param month - The month component (1-12, default: 1)
   * @param day - The day component (1-31, default: 1)
   * @param hour - The hour component (0-23, default: 0)
   * @param minute - The minute component (0-59, default: 0)
   * @param second - The second component (0-59, default: 0)
   * @param millisecond - The millisecond component (0-999, default: 0)
   * @returns A DateTime expression representing the specified instant
   *
   * @remarks
   * Components are: year, month (1-12), day (1-31), hour (0-23), minute (0-59),
   * second (0-59), and millisecond (0-999).
   *
   * @example
   * ```ts
   * const makeDate = East.function([IntegerType], DateTimeType, ($, year) => {
   *   $.return(East.DateTime.fromComponents(year, 1n, 15n));
   * });
   * const compiled = East.compile(makeDate.toIR(), []);
   * compiled(2025n);  // 2025-01-15T00:00:00.000Z
   * ```
   *
   * @example
   * ```ts
   * const makeDateTime = East.function([], DateTimeType, ($) => {
   *   $.return(East.DateTime.fromComponents(2025n, 1n, 15n, 14n, 30n, 0n, 500n));
   * });
   * const compiled = East.compile(makeDateTime.toIR(), []);
   * compiled();  // 2025-01-15T14:30:00.500Z
   * ```
   */
  fromComponents,

  /**
   * Parses a formatted string into a DateTime using Day.js-style format tokens.
   *
   * @param input - The string to parse
   * @param format - The format string using Day.js-style tokens (e.g., `"YYYY-MM-DD HH:mm:ss"`)
   * @returns A DateTime expression representing the parsed instant
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
   * const parseDate = East.function([StringType], DateTimeType, ($, dateStr) => {
   *   $.return(East.DateTime.parseFormatted(dateStr, "YYYY-MM-DD"));
   * });
   * const compiled = East.compile(parseDate.toIR(), []);
   * compiled("2025-01-15");  // 2025-01-15T00:00:00.000Z
   * ```
   *
   * @example
   * ```ts
   * const parseDateTime = East.function([StringType], DateTimeType, ($, str) => {
   *   $.return(East.DateTime.parseFormatted(str, "MM/DD/YYYY HH:mm"));
   * });
   * const compiled = East.compile(parseDateTime.toIR(), []);
   * compiled("01/15/2025 14:30");  // 2025-01-15T14:30:00.000Z
   * ```
   */
  parseFormatted,

  /**
   * Rounds a DateTime down to the nearest multiple of milliseconds.
   *
   * @param date - The DateTime to round
   * @param step - The millisecond step size to round to
   * @returns A DateTime expression rounded down to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundMs = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundDownMillisecond(dt, step));
   * });
   * const compiled = East.compile(roundMs.toIR(), []);
   * // Round down to nearest 100ms
   * compiled(East.DateTime.fromEpochMilliseconds(1234n), 100n);  // Rounded to 1200ms
   * ```
   */
  roundDownMillisecond: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const remainder = $.let(epochMs.remainder(step));
    const roundedMs = $.let(epochMs.subtract(remainder));
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime down to the nearest multiple of seconds.
   *
   * @param date - The DateTime to round
   * @param step - The second step size to round to
   * @returns A DateTime expression rounded down to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundSec = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundDownSecond(dt, step));
   * });
   * const compiled = East.compile(roundSec.toIR(), []);
   * // Round down to nearest 30 seconds
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 0n, 0n, 45n), 30n);  // Rounds to 30s
   * ```
   */
  roundDownSecond: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const stepMs = $.let(step.multiply(1000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const roundedMs = $.let(epochMs.subtract(remainder));
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime down to the nearest multiple of minutes.
   *
   * @param date - The DateTime to round
   * @param step - The minute step size to round to
   * @returns A DateTime expression rounded down to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundMin = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundDownMinute(dt, step));
   * });
   * const compiled = East.compile(roundMin.toIR(), []);
   * // Round down to nearest 15 minutes
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 0n, 22n), 15n);  // Rounds to 15 min
   * ```
   */
  roundDownMinute: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const stepMs = $.let(step.multiply(60000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const roundedMs = $.let(epochMs.subtract(remainder));
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime down to the nearest multiple of hours.
   *
   * @param date - The DateTime to round
   * @param step - The hour step size to round to
   * @returns A DateTime expression rounded down to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundHour = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundDownHour(dt, step));
   * });
   * const compiled = East.compile(roundHour.toIR(), []);
   * // Round down to nearest 6 hours
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 8n), 6n);  // Rounds to 6:00
   * ```
   */
  roundDownHour: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const stepMs = $.let(step.multiply(3600000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const roundedMs = $.let(epochMs.subtract(remainder));
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime up to the nearest multiple of milliseconds.
   *
   * @param date - The DateTime to round
   * @param step - The millisecond step size to round to
   * @returns A DateTime expression rounded up to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundUpMs = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundUpMillisecond(dt, step));
   * });
   * const compiled = East.compile(roundUpMs.toIR(), []);
   * // Round up to nearest 100ms
   * compiled(East.DateTime.fromEpochMilliseconds(1234n), 100n);  // Rounds to 1300ms
   * ```
   */
  roundUpMillisecond: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());

    const remainder = $.let(epochMs.remainder(step));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => epochMs.add(step.subtract(remainder))
      )
    );

    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime to the nearest multiple of milliseconds.
   *
   * @param date - The DateTime to round
   * @param step - The millisecond step size to round to
   * @returns A DateTime expression rounded to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundNearMs = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundNearestMillisecond(dt, step));
   * });
   * const compiled = East.compile(roundNearMs.toIR(), []);
   * // Round to nearest 100ms
   * compiled(East.DateTime.fromEpochMilliseconds(1234n), 100n);  // Rounds to 1200ms
   * compiled(East.DateTime.fromEpochMilliseconds(1289n), 100n);  // Rounds to 1300ms
   * ```
   */
  roundNearestMillisecond: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const remainder = $.let(epochMs.remainder(step));
    const halfStep = $.let(step.divide(2n));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => Expr.greaterEqual(remainder, halfStep).ifElse(
          () => epochMs.add(step.subtract(remainder)),
          () => epochMs.subtract(remainder)
        )
      )
    );
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime up to the nearest multiple of seconds.
   *
   * @param date - The DateTime to round
   * @param step - The second step size to round to
   * @returns A DateTime expression rounded up to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundUpSec = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundUpSecond(dt, step));
   * });
   * const compiled = East.compile(roundUpSec.toIR(), []);
   * // Round up to nearest 30 seconds
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 0n, 0n, 15n), 30n);  // Rounds to 30s
   * ```
   */
  roundUpSecond: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const stepMs = $.let(step.multiply(1000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => epochMs.add(stepMs.subtract(remainder))
      )
    );
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime to the nearest multiple of seconds.
   *
   * @param date - The DateTime to round
   * @param step - The second step size to round to
   * @returns A DateTime expression rounded to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundNearSec = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundNearestSecond(dt, step));
   * });
   * const compiled = East.compile(roundNearSec.toIR(), []);
   * // Round to nearest 30 seconds
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 0n, 0n, 22n), 30n);  // Rounds to 30s
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 0n, 0n, 38n), 30n);  // Rounds to 30s
   * ```
   */
  roundNearestSecond: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const stepMs = $.let(step.multiply(1000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const halfStep = $.let(stepMs.divide(2n));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => Expr.greaterEqual(remainder, halfStep).ifElse(
          () => epochMs.add(stepMs.subtract(remainder)),
          () => epochMs.subtract(remainder)
        )
      )
    );
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime up to the nearest multiple of minutes.
   *
   * @param date - The DateTime to round
   * @param step - The minute step size to round to
   * @returns A DateTime expression rounded up to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundUpMin = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundUpMinute(dt, step));
   * });
   * const compiled = East.compile(roundUpMin.toIR(), []);
   * // Round up to nearest 15 minutes
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 0n, 22n), 15n);  // Rounds to 30 min
   * ```
   */
  roundUpMinute: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());

    const stepMs = $.let(step.multiply(60000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => epochMs.add(stepMs.subtract(remainder))
      )
    );

    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime to the nearest multiple of minutes.
   *
   * @param date - The DateTime to round
   * @param step - The minute step size to round to
   * @returns A DateTime expression rounded to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundNearMin = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundNearestMinute(dt, step));
   * });
   * const compiled = East.compile(roundNearMin.toIR(), []);
   * // Round to nearest 15 minutes
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 0n, 22n), 15n);  // Rounds to 15 min
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 0n, 38n), 15n);  // Rounds to 45 min
   * ```
   */
  roundNearestMinute: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const stepMs = $.let(step.multiply(60000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const halfStep = $.let(stepMs.divide(2n));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => Expr.greaterEqual(remainder, halfStep).ifElse(
          () => epochMs.add(stepMs.subtract(remainder)),
          () => epochMs.subtract(remainder)
        )
      )
    );
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime up to the nearest multiple of hours.
   *
   * @param date - The DateTime to round
   * @param step - The hour step size to round to
   * @returns A DateTime expression rounded up to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundUpHr = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundUpHour(dt, step));
   * });
   * const compiled = East.compile(roundUpHr.toIR(), []);
   * // Round up to nearest 6 hours
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 8n), 6n);  // Rounds to 12:00
   * ```
   */
  roundUpHour: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const stepMs = $.let(step.multiply(3600000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => epochMs.add(stepMs.subtract(remainder))
      )
    );
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime to the nearest multiple of hours.
   *
   * @param date - The DateTime to round
   * @param step - The hour step size to round to
   * @returns A DateTime expression rounded to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundNearHr = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundNearestHour(dt, step));
   * });
   * const compiled = East.compile(roundNearHr.toIR(), []);
   * // Round to nearest 6 hours
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 8n), 6n);  // Rounds to 6:00
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 10n), 6n);  // Rounds to 12:00
   * ```
   */
  roundNearestHour: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    const stepMs = $.let(step.multiply(3600000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const halfStep = $.let(stepMs.divide(2n));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => Expr.greaterEqual(remainder, halfStep).ifElse(
          () => epochMs.add(stepMs.subtract(remainder)),
          () => epochMs.subtract(remainder)
        )
      )
    );
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime down to the nearest multiple of days.
   *
   * @param date - The DateTime to round
   * @param step - The day step size to round to
   * @returns A DateTime expression rounded down to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundDownD = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundDownDay(dt, step));
   * });
   * const compiled = East.compile(roundDownD.toIR(), []);
   * // Round down to nearest day
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 12n, 30n), 1n);  // Rounds to start of day
   * ```
   */
  roundDownDay: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());

    // Convert step from days to milliseconds (step * 24 * 60 * 60 * 1000)
    const stepMs = $.let(step.multiply(86400000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const roundedMs = $.let(epochMs.subtract(remainder));
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime up to the nearest multiple of days.
   *
   * @param date - The DateTime to round
   * @param step - The day step size to round to
   * @returns A DateTime expression rounded up to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundUpD = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundUpDay(dt, step));
   * });
   * const compiled = East.compile(roundUpD.toIR(), []);
   * // Round up to nearest day
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 12n, 30n), 1n);  // Rounds to next day start
   * ```
   */
  roundUpDay: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());

    const stepMs = $.let(step.multiply(86400000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => epochMs.add(stepMs.subtract(remainder))
      )
    );
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime to the nearest multiple of days.
   *
   * @param date - The DateTime to round
   * @param step - The day step size to round to
   * @returns A DateTime expression rounded to the nearest multiple of the step
   *
   * @example
   * ```ts
   * const roundNearD = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundNearestDay(dt, step));
   * });
   * const compiled = East.compile(roundNearD.toIR(), []);
   * // Round to nearest day
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 8n), 1n);  // Rounds to start of day
   * compiled(East.DateTime.fromComponents(2025n, 1n, 1n, 16n), 1n);  // Rounds to next day start
   * ```
   */
  roundNearestDay: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());

    const stepMs = $.let(step.multiply(86400000n));
    const remainder = $.let(epochMs.remainder(stepMs));
    const halfStep = $.let(stepMs.divide(2n));
    const roundedMs = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => epochMs,
        () => Expr.greaterEqual(remainder, halfStep).ifElse(
          () => epochMs.add(stepMs.subtract(remainder)),
          () => epochMs.subtract(remainder)
        )
      )
    );
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime down to the nearest Monday (ISO week start).
   *
   * @param date - The DateTime to round
   * @param step - The week step size to round to
   * @returns A DateTime expression rounded down to the nearest multiple of weeks (starting on Monday)
   *
   * @example
   * ```ts
   * const roundDownWk = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundDownWeek(dt, step));
   * });
   * const compiled = East.compile(roundDownWk.toIR(), []);
   * // Round down to nearest Monday
   * compiled(East.DateTime.fromComponents(2025n, 1n, 3n), 1n);  // Rounds to previous Monday
   * ```
   */
  roundDownWeek: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    // Reference Monday: 1969-12-29T00:00:00.000Z (Monday before Unix epoch)
    const refMondayMs = $.let(-259200000n); // 3 days before epoch in milliseconds
    
    // Calculate offset from reference Monday and apply step-based rounding
    const offsetFromRefMonday = $.let(epochMs.subtract(refMondayMs));
    const stepMs = $.let(step.multiply(604800000n)); // 7 days in milliseconds
    const remainder = $.let(offsetFromRefMonday.remainder(stepMs));
    const roundedOffsetFromRef = $.let(offsetFromRefMonday.subtract(remainder));
    
    // Calculate result relative to reference Monday
    const roundedMs = $.let(refMondayMs.add(roundedOffsetFromRef));
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime up to the nearest Monday (ISO week start).
   *
   * @param date - The DateTime to round
   * @param step - The week step size to round to
   * @returns A DateTime expression rounded up to the nearest multiple of weeks (starting on Monday)
   *
   * @example
   * ```ts
   * const roundUpWk = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundUpWeek(dt, step));
   * });
   * const compiled = East.compile(roundUpWk.toIR(), []);
   * // Round up to nearest Monday
   * compiled(East.DateTime.fromComponents(2025n, 1n, 3n), 1n);  // Rounds to next Monday
   * ```
   */
  roundUpWeek: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    // Reference Monday: 1969-12-29T00:00:00.000Z (Monday before Unix epoch)
    const refMondayMs = $.let(-259200000n);
    
    // Calculate offset from reference Monday and apply step-based rounding
    const offsetFromRefMonday = $.let(epochMs.subtract(refMondayMs));
    const stepMs = $.let(step.multiply(604800000n));
    const remainder = $.let(offsetFromRefMonday.remainder(stepMs));
    const roundedOffsetFromRef = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => offsetFromRefMonday,
        () => offsetFromRefMonday.add(stepMs.subtract(remainder))
      )
    );
    
    // Calculate result relative to reference Monday
    const roundedMs = $.let(refMondayMs.add(roundedOffsetFromRef));

    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime to the nearest Monday (ISO week start).
   *
   * @param date - The DateTime to round
   * @param step - The week step size to round to
   * @returns A DateTime expression rounded to the nearest multiple of weeks (starting on Monday)
   *
   * @example
   * ```ts
   * const roundNearWk = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundNearestWeek(dt, step));
   * });
   * const compiled = East.compile(roundNearWk.toIR(), []);
   * // Round to nearest Monday
   * compiled(East.DateTime.fromComponents(2025n, 1n, 3n), 1n);  // Rounds to closest Monday
   * ```
   */
  roundNearestWeek: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const epochMs = $.let(date.toEpochMilliseconds());
    
    // Reference Monday: 1969-12-29T00:00:00.000Z (Monday before Unix epoch)
    const refMondayMs = $.let(-259200000n);
    
    // Calculate offset from reference Monday and apply step-based rounding
    const offsetFromRefMonday = $.let(epochMs.subtract(refMondayMs));
    const stepMs = $.let(step.multiply(604800000n));
    const remainder = $.let(offsetFromRefMonday.remainder(stepMs));
    const halfStep = $.let(stepMs.divide(2n));
    const roundedOffsetFromRef = $.let(
      Expr.equal(remainder, 0n).ifElse(
        () => offsetFromRefMonday,
        () => Expr.greaterEqual(remainder, halfStep).ifElse(
          () => offsetFromRefMonday.add(stepMs.subtract(remainder)),
          () => offsetFromRefMonday.subtract(remainder)
        )
      )
    );
    
    // Calculate result relative to reference Monday
    const roundedMs = $.let(refMondayMs.add(roundedOffsetFromRef));
    
    return fromEpochMilliseconds(roundedMs);
  }),

  /**
   * Rounds a DateTime down to the nearest month boundary.
   *
   * @param date - The DateTime to round
   * @param step - The month step size to round to
   * @returns A DateTime expression rounded down to the first day of the nearest multiple of months
   *
   * @example
   * ```ts
   * const roundDownMo = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundDownMonth(dt, step));
   * });
   * const compiled = East.compile(roundDownMo.toIR(), []);
   * // Round down to nearest month (first day of the month at midnight)
   * compiled(East.DateTime.fromComponents(2025n, 1n, 15n), 1n);  // Rounds to Jan 1, 2025
   * // Round down to nearest quarter (Jan 1, Apr 1, Jul 1, Oct 1)
   * compiled(East.DateTime.fromComponents(2025n, 5n, 15n), 3n);  // Rounds to Apr 1, 2025
   * ```
   */
  roundDownMonth: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const year = $.let(date.getYear());

    const month = $.let(date.getMonth());
    
    // Calculate step-aligned month: floor((month - 1) / step) * step + 1
    const monthIndex = $.let(month.subtract(1n)); // Convert to 0-based
    const steppedMonthIndex = $.let(monthIndex.subtract(monthIndex.remainder(step)));
    const roundedMonth = $.let(steppedMonthIndex.add(1n)); // Convert back to 1-based
    
    // Construct DateTime from components (1st day of month, midnight)
    return fromComponents(
      year,
      roundedMonth,
    );
  }),

  /**
   * Rounds a DateTime down to the nearest year boundary.
   *
   * @param date - The DateTime to round
   * @param step - The year step size to round to
   * @returns A DateTime expression rounded down to January 1st of the nearest multiple of years
   *
   * @example
   * ```ts
   * const roundDownYr = East.function([DateTimeType, IntegerType], DateTimeType, ($, dt, step) => {
   *   $.return(East.DateTime.roundDownYear(dt, step));
   * });
   * const compiled = East.compile(roundDownYr.toIR(), []);
   * // Round down to nearest year (January 1st at midnight)
   * compiled(East.DateTime.fromComponents(2025n, 6n, 15n), 1n);  // Rounds to Jan 1, 2025
   * // Round down to nearest decade
   * compiled(East.DateTime.fromComponents(2025n, 6n, 15n), 10n);  // Rounds to Jan 1, 2020
   * ```
   */
  roundDownYear: Expr.function([DateTimeType, IntegerType], DateTimeType, ($, date, step) => {
    const year = $.let(date.getYear());
    
    // Calculate step-aligned year: floor(year / step) * step
    const steppedYear = $.let(year.subtract(year.remainder(step)));
    
    // Construct DateTime from components (January 1st, midnight)
    return fromComponents(
      steppedYear,
    );
  }),
}