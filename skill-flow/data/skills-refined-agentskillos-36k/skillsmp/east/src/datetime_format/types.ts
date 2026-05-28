/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Datetime formatting support for East.
 *
 * This module defines the structured representation of datetime format strings.
 * Format strings are parsed once in the TypeScript SDK and serialized as structured
 * tokens, ensuring consistent formatting behavior across all East backends.
 */

import { NullType, StringType, VariantType } from "../types.js";
import { variant } from "../containers/variant.js";

/**
 * Structured representation of a datetime format string.
 *
 * Format strings are parsed into an array of tokens at AST construction time.
 * Each token represents either a datetime component (year, month, day, etc.)
 * or a literal string to be included verbatim in the output.
 *
 * This structured representation serves as East's "narrow waist" for datetime
 * formatting - the TypeScript SDK parses format strings once, and all backends
 * implement formatting from the same token structure, guaranteeing identical
 * behavior across JavaScript, Julia, and other future backends.
 *
 * @remarks
 * Formats do not support timezones or locales.
 *
 * @example
 * ```ts
 * // Format string "YYYY-MM-DD" parses to:
 * [
 *   variant("year4", null),
 *   variant("literal", "-"),
 *   variant("month2", null),
 *   variant("literal", "-"),
 *   variant("day2", null)
 * ]
 * ```
 */
export const DateTimeFormatTokenType = VariantType({
  /**
   * Literal text to include verbatim in formatted output.
   * Any characters in the format string that are not recognized as format
   * codes are treated as literals.
   */
  literal: StringType,

  // Year
  /** Four-digit year (e.g., "2025") - Format: YYYY */
  year4: NullType,
  /** Two-digit year (e.g., "25") - Format: YY */
  year2: NullType,

  // Month
  /** Month as 1-12 without zero-padding (e.g., "1", "12") - Format: M */
  month1: NullType,
  /** Month as 01-12 with zero-padding (e.g., "01", "12") - Format: MM */
  month2: NullType,
  /** Short month name (e.g., "Jan", "Feb") - Format: MMM */
  monthNameShort: NullType,
  /** Full month name (e.g., "January", "February") - Format: MMMM */
  monthNameFull: NullType,

  // Day of month
  /** Day of month as 1-31 without zero-padding (e.g., "1", "31") - Format: D */
  day1: NullType,
  /** Day of month as 01-31 with zero-padding (e.g., "01", "31") - Format: DD */
  day2: NullType,

  // Day of week
  /** Minimal weekday name (e.g., "Su", "Mo") - Format: dd */
  weekdayNameMin: NullType,
  /** Short weekday name (e.g., "Sun", "Mon") - Format: ddd */
  weekdayNameShort: NullType,
  /** Full weekday name (e.g., "Sunday", "Monday") - Format: dddd */
  weekdayNameFull: NullType,

  // Hour (24-hour)
  /** Hour 0-23 without zero-padding (e.g., "0", "23") - Format: H */
  hour24_1: NullType,
  /** Hour 00-23 with zero-padding (e.g., "00", "23") - Format: HH */
  hour24_2: NullType,

  // Hour (12-hour)
  /** Hour 1-12 without zero-padding (e.g., "1", "12") - Format: h */
  hour12_1: NullType,
  /** Hour 01-12 with zero-padding (e.g., "01", "12") - Format: hh */
  hour12_2: NullType,

  // Minute
  /** Minute 0-59 without zero-padding (e.g., "0", "59") - Format: m */
  minute1: NullType,
  /** Minute 00-59 with zero-padding (e.g., "00", "59") - Format: mm */
  minute2: NullType,

  // Second
  /** Second 0-59 without zero-padding (e.g., "0", "59") - Format: s */
  second1: NullType,
  /** Second 00-59 with zero-padding (e.g., "00", "59") - Format: ss */
  second2: NullType,

  // Millisecond
  /** Millisecond 000-999 with zero-padding (e.g., "000", "999") - Format: SSS */
  millisecond3: NullType,

  // AM/PM
  /** Uppercase AM/PM (e.g., "AM", "PM") - Format: A */
  ampmUpper: NullType,
  /** Lowercase am/pm (e.g., "am", "pm") - Format: a */
  ampmLower: NullType,
});

/**
 * TypeScript type for datetime format tokens.
 *
 * This is a union of all possible datetime format token variants.
 */
export type DateTimeFormatToken =
  | variant<"literal", string>
  | variant<"year4", null>
  | variant<"year2", null>
  | variant<"month1", null>
  | variant<"month2", null>
  | variant<"monthNameShort", null>
  | variant<"monthNameFull", null>
  | variant<"day1", null>
  | variant<"day2", null>
  | variant<"weekdayNameMin", null>
  | variant<"weekdayNameShort", null>
  | variant<"weekdayNameFull", null>
  | variant<"hour24_1", null>
  | variant<"hour24_2", null>
  | variant<"hour12_1", null>
  | variant<"hour12_2", null>
  | variant<"minute1", null>
  | variant<"minute2", null>
  | variant<"second1", null>
  | variant<"second2", null>
  | variant<"millisecond3", null>
  | variant<"ampmUpper", null>
  | variant<"ampmLower", null>;
