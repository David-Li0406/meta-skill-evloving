/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Datetime formatting runtime implementation.
 *
 * This module provides the runtime formatting logic for converting Date objects
 * to strings according to parsed format token arrays. This is called by the
 * DateTimePrintFormat builtin.
 */

import type { DateTimeFormatToken } from "./types.js";

/**
 * Month names in English.
 */
const MONTH_NAMES_FULL = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
] as const;

/**
 * Abbreviated month names in English.
 */
const MONTH_NAMES_SHORT = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
] as const;

/**
 * Full weekday names in English, starting with Sunday.
 */
const WEEKDAY_NAMES_FULL = [
  "Sunday", "Monday", "Tuesday", "Wednesday",
  "Thursday", "Friday", "Saturday"
] as const;

/**
 * Abbreviated weekday names in English, starting with Sunday.
 */
const WEEKDAY_NAMES_SHORT = [
  "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
] as const;

/**
 * Minimal weekday names (2 characters), starting with Sunday.
 */
const WEEKDAY_NAMES_MIN = [
  "Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"
] as const;

/**
 * Formats a Date according to an array of format tokens.
 *
 * @param date - The Date object to format
 * @param tokens - Array of format tokens specifying the output format
 * @returns The formatted date string
 *
 * @remarks
 * This function implements the runtime formatting logic for East's datetime
 * formatting. It is called by the DateTimePrintFormat builtin.
 *
 * All dates are treated as UTC (naive datetimes with no timezone information).
 * The Date object's UTC time components are used for formatting.
 *
 * @example
 * ```ts
 * const date = new Date("2025-01-15T14:30:45.123Z"); // Jan 15, 2025 14:30:45.123 UTC
 * const tokens = parseDateTimeFormat("YYYY-MM-DD HH:mm:ss.SSS");
 * formatDateTime(date, tokens); // "2025-01-15 14:30:45.123"
 * ```
 */
export function formatDateTime(date: Date, tokens: DateTimeFormatToken[]): string {
  const parts: string[] = [];

  for (const token of tokens) {
    let part: string;

    switch (token.type) {
      // Year
      case "year4":
        part = date.getUTCFullYear().toString();
        break;

      case "year2":
        part = (date.getUTCFullYear() % 100).toString().padStart(2, "0");
        break;

      // Month
      case "month1":
        part = (date.getUTCMonth() + 1).toString();
        break;

      case "month2":
        part = (date.getUTCMonth() + 1).toString().padStart(2, "0");
        break;

      case "monthNameShort":
        part = MONTH_NAMES_SHORT[date.getUTCMonth()]!;
        break;

      case "monthNameFull":
        part = MONTH_NAMES_FULL[date.getUTCMonth()]!;
        break;

      // Day of month
      case "day1":
        part = date.getUTCDate().toString();
        break;

      case "day2":
        part = date.getUTCDate().toString().padStart(2, "0");
        break;

      // Day of week
      case "weekdayNameMin":
        part = WEEKDAY_NAMES_MIN[date.getUTCDay()]!;
        break;

      case "weekdayNameShort":
        part = WEEKDAY_NAMES_SHORT[date.getUTCDay()]!;
        break;

      case "weekdayNameFull":
        part = WEEKDAY_NAMES_FULL[date.getUTCDay()]!;
        break;

      // Hour (24-hour)
      case "hour24_1":
        part = date.getUTCHours().toString();
        break;

      case "hour24_2":
        part = date.getUTCHours().toString().padStart(2, "0");
        break;

      // Hour (12-hour)
      case "hour12_1": {
        const hour12 = date.getUTCHours() % 12 || 12;
        part = hour12.toString();
        break;
      }

      case "hour12_2": {
        const hour12 = date.getUTCHours() % 12 || 12;
        part = hour12.toString().padStart(2, "0");
        break;
      }

      // Minute
      case "minute1":
        part = date.getUTCMinutes().toString();
        break;

      case "minute2":
        part = date.getUTCMinutes().toString().padStart(2, "0");
        break;

      // Second
      case "second1":
        part = date.getUTCSeconds().toString();
        break;

      case "second2":
        part = date.getUTCSeconds().toString().padStart(2, "0");
        break;

      // Millisecond
      case "millisecond3":
        part = date.getUTCMilliseconds().toString().padStart(3, "0");
        break;

      // AM/PM
      case "ampmUpper":
        part = date.getUTCHours() < 12 ? "AM" : "PM";
        break;

      case "ampmLower":
        part = date.getUTCHours() < 12 ? "am" : "pm";
        break;

      // Literal
      case "literal":
        part = token.value;
        break;

      default:
        // TypeScript exhaustiveness check
        const _exhaustive: never = token;
        throw new Error(`Unknown datetime format token type: ${(_exhaustive as DateTimeFormatToken).type}`);
    }

    parts.push(part);
  }

  return parts.join("");
}
