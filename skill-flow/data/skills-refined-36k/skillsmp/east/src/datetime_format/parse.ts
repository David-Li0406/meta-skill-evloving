/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Datetime parsing runtime implementation.
 *
 * This module provides the runtime parsing logic for converting strings
 * to Date objects according to parsed format token arrays. This is called by the
 * DateTimeParseFormat builtin.
 */

import type { DateTimeFormatToken } from "./types.js";

/**
 * Result of parsing a datetime string.
 */
export type DateTimeParseResult =
  | { success: true; value: Date }
  | { success: false; error: string; position: number };

/**
 * Month names in English for parsing.
 */
const MONTH_NAMES_FULL = [
  "january", "february", "march", "april", "may", "june",
  "july", "august", "september", "october", "november", "december"
] as const;

const MONTH_NAMES_SHORT = [
  "jan", "feb", "mar", "apr", "may", "jun",
  "jul", "aug", "sep", "oct", "nov", "dec"
] as const;

/**
 * Weekday names in English for parsing (currently ignored during parsing).
 */
const WEEKDAY_NAMES_FULL = [
  "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"
] as const;

const WEEKDAY_NAMES_SHORT = [
  "sun", "mon", "tue", "wed", "thu", "fri", "sat"
] as const;

const WEEKDAY_NAMES_MIN = [
  "su", "mo", "tu", "we", "th", "fr", "sa"
] as const;

/**
 * Parses a datetime string according to format tokens.
 *
 * @param input - The string to parse
 * @param tokens - Array of format tokens specifying the expected format
 * @returns Parse result containing either the Date or an error with position
 *
 * @remarks
 * All dates are treated as UTC (naive datetimes with no timezone information).
 * The parsed components are used to construct a Date using Date.UTC().
 *
 * Weekday tokens (dd, ddd, dddd) are currently ignored during parsing - they
 * are consumed from the input but not validated against the actual weekday.
 *
 * @example
 * ```ts
 * const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
 * const result = parseDateTimeFormatted("2025-01-15", tokens);
 * if (result.success) {
 *   console.log(result.value); // Date object for 2025-01-15T00:00:00.000Z
 * } else {
 *   console.log(`Parse error at position ${result.position}: ${result.error}`);
 * }
 * ```
 */
export function parseDateTimeFormatted(input: string, tokens: DateTimeFormatToken[]): DateTimeParseResult {
  let position = 0;

  // Datetime components - will validate redundancy and check for gaps
  let year: number | null = null;
  let month: number | null = null;
  let day: number | null = null;
  let hour: number | null = null;
  let minute: number | null = null;
  let second: number | null = null;
  let millisecond: number | null = null;
  let isPM: boolean | null = null;
  let hour12: number | null = null; // Track 12-hour format separately
  let parsedWeekday: number | null = null; // Track parsed weekday for validation

  for (const token of tokens) {
    if (position > input.length) {
      return {
        success: false,
        error: `Unexpected end of input`,
        position
      };
    }

    switch (token.type) {
      case "year4": {
        const match = input.slice(position, position + 4);
        if (match.length < 4 || !/^\d{4}$/.test(match)) {
          return {
            success: false,
            error: `Expected 4-digit year`,
            position
          };
        }
        const parsedYear = parseInt(match, 10);
        if (year !== null && year !== parsedYear) {
          return {
            success: false,
            error: `Year specified multiple times with different values: ${year} and ${parsedYear}`,
            position
          };
        }
        year = parsedYear;
        position += 4;
        break;
      }

      case "year2": {
        const match = input.slice(position, position + 2);
        if (match.length < 2 || !/^\d{2}$/.test(match)) {
          return {
            success: false,
            error: `Expected 2-digit year`,
            position
          };
        }
        const yy = parseInt(match, 10);
        // 2-digit year: 00-99 -> 2000-2099 (simple heuristic)
        const parsedYear = 2000 + yy;
        if (year !== null && year !== parsedYear) {
          return {
            success: false,
            error: `Year specified multiple times with different values: ${year} and ${parsedYear}`,
            position
          };
        }
        year = parsedYear;
        position += 2;
        break;
      }

      case "month2": {
        const match = input.slice(position, position + 2);
        if (match.length < 2 || !/^\d{2}$/.test(match)) {
          return {
            success: false,
            error: `Expected 2-digit month (01-12)`,
            position
          };
        }
        const parsedMonth = parseInt(match, 10);
        if (parsedMonth < 1 || parsedMonth > 12) {
          return {
            success: false,
            error: `Month out of range (got ${parsedMonth}, expected 01-12)`,
            position
          };
        }
        if (month !== null && month !== parsedMonth) {
          return {
            success: false,
            error: `Month specified multiple times with different values: ${month} and ${parsedMonth}`,
            position
          };
        }
        month = parsedMonth;
        position += 2;
        break;
      }

      case "month1": {
        // Try 2 digits first, then 1
        let match = input.slice(position, position + 2);
        let parsedMonth: number;
        if (/^\d{2}$/.test(match)) {
          parsedMonth = parseInt(match, 10);
          position += 2;
        } else {
          match = input.slice(position, position + 1);
          if (!/^\d$/.test(match)) {
            return {
              success: false,
              error: `Expected 1 or 2-digit month`,
              position
            };
          }
          parsedMonth = parseInt(match, 10);
          position += 1;
        }
        if (parsedMonth < 1 || parsedMonth > 12) {
          return {
            success: false,
            error: `Month out of range (got ${parsedMonth}, expected 1-12)`,
            position: position - match.length
          };
        }
        if (month !== null && month !== parsedMonth) {
          return {
            success: false,
            error: `Month specified multiple times with different values: ${month} and ${parsedMonth}`,
            position: position - match.length
          };
        }
        month = parsedMonth;
        break;
      }

      case "monthNameFull": {
        let matched = false;
        let parsedMonth: number | null = null;
        for (let i = 0; i < MONTH_NAMES_FULL.length; i++) {
          const name = MONTH_NAMES_FULL[i]!;
          const slice = input.slice(position, position + name.length).toLowerCase();
          if (slice === name) {
            parsedMonth = i + 1;
            position += name.length;
            matched = true;
            break;
          }
        }
        if (!matched) {
          return {
            success: false,
            error: `Expected full month name (e.g., "January")`,
            position
          };
        }
        if (month !== null && month !== parsedMonth) {
          return {
            success: false,
            error: `Month specified multiple times with different values: ${month} and ${parsedMonth}`,
            position
          };
        }
        month = parsedMonth;
        break;
      }

      case "monthNameShort": {
        let matched = false;
        let parsedMonth: number | null = null;
        for (let i = 0; i < MONTH_NAMES_SHORT.length; i++) {
          const name = MONTH_NAMES_SHORT[i]!;
          const slice = input.slice(position, position + name.length).toLowerCase();
          if (slice === name) {
            parsedMonth = i + 1;
            position += name.length;
            matched = true;
            break;
          }
        }
        if (!matched) {
          return {
            success: false,
            error: `Expected short month name (e.g., "Jan")`,
            position
          };
        }
        if (month !== null && month !== parsedMonth) {
          return {
            success: false,
            error: `Month specified multiple times with different values: ${month} and ${parsedMonth}`,
            position
          };
        }
        month = parsedMonth;
        break;
      }

      case "day2": {
        const match = input.slice(position, position + 2);
        if (match.length < 2 || !/^\d{2}$/.test(match)) {
          return {
            success: false,
            error: `Expected 2-digit day (01-31)`,
            position
          };
        }
        const parsedDay = parseInt(match, 10);
        if (parsedDay < 1 || parsedDay > 31) {
          return {
            success: false,
            error: `Day out of range (got ${parsedDay}, expected 01-31)`,
            position
          };
        }
        if (day !== null && day !== parsedDay) {
          return {
            success: false,
            error: `Day specified multiple times with different values: ${day} and ${parsedDay}`,
            position
          };
        }
        day = parsedDay;
        position += 2;
        break;
      }

      case "day1": {
        // Try 2 digits first, then 1
        let match = input.slice(position, position + 2);
        let parsedDay: number;
        if (/^\d{2}$/.test(match)) {
          parsedDay = parseInt(match, 10);
          position += 2;
        } else {
          match = input.slice(position, position + 1);
          if (!/^\d$/.test(match)) {
            return {
              success: false,
              error: `Expected 1 or 2-digit day`,
              position
            };
          }
          parsedDay = parseInt(match, 10);
          position += 1;
        }
        if (parsedDay < 1 || parsedDay > 31) {
          return {
            success: false,
            error: `Day out of range (got ${parsedDay}, expected 1-31)`,
            position: position - match.length
          };
        }
        if (day !== null && day !== parsedDay) {
          return {
            success: false,
            error: `Day specified multiple times with different values: ${day} and ${parsedDay}`,
            position: position - match.length
          };
        }
        day = parsedDay;
        break;
      }

      // Weekday parsing - store for validation after Date construction
      case "weekdayNameFull": {
        let matched = false;
        for (let i = 0; i < WEEKDAY_NAMES_FULL.length; i++) {
          const name = WEEKDAY_NAMES_FULL[i]!;
          const slice = input.slice(position, position + name.length).toLowerCase();
          if (slice === name) {
            // Map to JavaScript getDay() values: 0=Sunday, 1=Monday, ..., 6=Saturday
            const weekdayValue = i;
            if (parsedWeekday !== null && parsedWeekday !== weekdayValue) {
              return {
                success: false,
                error: `Weekday specified multiple times with different values`,
                position
              };
            }
            parsedWeekday = weekdayValue;
            position += name.length;
            matched = true;
            break;
          }
        }
        if (!matched) {
          return {
            success: false,
            error: `Expected full weekday name (e.g., "Monday")`,
            position
          };
        }
        break;
      }

      case "weekdayNameShort": {
        let matched = false;
        for (let i = 0; i < WEEKDAY_NAMES_SHORT.length; i++) {
          const name = WEEKDAY_NAMES_SHORT[i]!;
          const slice = input.slice(position, position + name.length).toLowerCase();
          if (slice === name) {
            // Map to JavaScript getDay() values: 0=Sunday, 1=Monday, ..., 6=Saturday
            const weekdayValue = i;
            if (parsedWeekday !== null && parsedWeekday !== weekdayValue) {
              return {
                success: false,
                error: `Weekday specified multiple times with different values`,
                position
              };
            }
            parsedWeekday = weekdayValue;
            position += name.length;
            matched = true;
            break;
          }
        }
        if (!matched) {
          return {
            success: false,
            error: `Expected short weekday name (e.g., "Mon")`,
            position
          };
        }
        break;
      }

      case "weekdayNameMin": {
        let matched = false;
        for (let i = 0; i < WEEKDAY_NAMES_MIN.length; i++) {
          const name = WEEKDAY_NAMES_MIN[i]!;
          const slice = input.slice(position, position + name.length).toLowerCase();
          if (slice === name) {
            // Map to JavaScript getDay() values: 0=Sunday, 1=Monday, ..., 6=Saturday
            const weekdayValue = i;
            if (parsedWeekday !== null && parsedWeekday !== weekdayValue) {
              return {
                success: false,
                error: `Weekday specified multiple times with different values`,
                position
              };
            }
            parsedWeekday = weekdayValue;
            position += name.length;
            matched = true;
            break;
          }
        }
        if (!matched) {
          return {
            success: false,
            error: `Expected minimal weekday name (e.g., "Mo")`,
            position
          };
        }
        break;
      }

      case "hour24_2": {
        const match = input.slice(position, position + 2);
        if (match.length < 2 || !/^\d{2}$/.test(match)) {
          return {
            success: false,
            error: `Expected 2-digit hour (00-23)`,
            position
          };
        }
        const parsedHour = parseInt(match, 10);
        if (parsedHour > 23) {
          return {
            success: false,
            error: `Hour out of range (got ${parsedHour}, expected 00-23)`,
            position
          };
        }
        if (hour !== null && hour !== parsedHour) {
          return {
            success: false,
            error: `Hour (24-hour) specified multiple times with different values: ${hour} and ${parsedHour}`,
            position
          };
        }
        hour = parsedHour;
        position += 2;
        break;
      }

      case "hour24_1": {
        // Try 2 digits first, then 1
        let match = input.slice(position, position + 2);
        let parsedHour: number;
        if (/^\d{2}$/.test(match)) {
          parsedHour = parseInt(match, 10);
          position += 2;
        } else {
          match = input.slice(position, position + 1);
          if (!/^\d$/.test(match)) {
            return {
              success: false,
              error: `Expected 1 or 2-digit hour`,
              position
            };
          }
          parsedHour = parseInt(match, 10);
          position += 1;
        }
        if (parsedHour > 23) {
          return {
            success: false,
            error: `Hour out of range (got ${parsedHour}, expected 0-23)`,
            position: position - match.length
          };
        }
        if (hour !== null && hour !== parsedHour) {
          return {
            success: false,
            error: `Hour (24-hour) specified multiple times with different values: ${hour} and ${parsedHour}`,
            position: position - match.length
          };
        }
        hour = parsedHour;
        break;
      }

      case "hour12_2": {
        const match = input.slice(position, position + 2);
        if (match.length < 2 || !/^\d{2}$/.test(match)) {
          return {
            success: false,
            error: `Expected 2-digit hour (01-12)`,
            position
          };
        }
        const parsedHour12 = parseInt(match, 10);
        if (parsedHour12 < 1 || parsedHour12 > 12) {
          return {
            success: false,
            error: `Hour out of range (got ${parsedHour12}, expected 01-12)`,
            position
          };
        }
        if (hour12 !== null && hour12 !== parsedHour12) {
          return {
            success: false,
            error: `Hour (12-hour) specified multiple times with different values: ${hour12} and ${parsedHour12}`,
            position
          };
        }
        hour12 = parsedHour12;
        position += 2;
        break;
      }

      case "hour12_1": {
        // Try 2 digits first, then 1
        let match = input.slice(position, position + 2);
        let parsedHour12: number;
        if (/^\d{2}$/.test(match)) {
          parsedHour12 = parseInt(match, 10);
          position += 2;
        } else {
          match = input.slice(position, position + 1);
          if (!/^\d$/.test(match)) {
            return {
              success: false,
              error: `Expected 1 or 2-digit hour`,
              position
            };
          }
          parsedHour12 = parseInt(match, 10);
          position += 1;
        }
        if (parsedHour12 < 1 || parsedHour12 > 12) {
          return {
            success: false,
            error: `Hour out of range (got ${parsedHour12}, expected 1-12)`,
            position: position - match.length
          };
        }
        if (hour12 !== null && hour12 !== parsedHour12) {
          return {
            success: false,
            error: `Hour (12-hour) specified multiple times with different values: ${hour12} and ${parsedHour12}`,
            position: position - match.length
          };
        }
        hour12 = parsedHour12;
        break;
      }

      case "minute2": {
        const match = input.slice(position, position + 2);
        if (match.length < 2 || !/^\d{2}$/.test(match)) {
          return {
            success: false,
            error: `Expected 2-digit minute (00-59)`,
            position
          };
        }
        const parsedMinute = parseInt(match, 10);
        if (parsedMinute > 59) {
          return {
            success: false,
            error: `Minute out of range (got ${parsedMinute}, expected 00-59)`,
            position
          };
        }
        if (minute !== null && minute !== parsedMinute) {
          return {
            success: false,
            error: `Minute specified multiple times with different values: ${minute} and ${parsedMinute}`,
            position
          };
        }
        minute = parsedMinute;
        position += 2;
        break;
      }

      case "minute1": {
        // Try 2 digits first, then 1
        let match = input.slice(position, position + 2);
        let parsedMinute: number;
        if (/^\d{2}$/.test(match)) {
          parsedMinute = parseInt(match, 10);
          position += 2;
        } else {
          match = input.slice(position, position + 1);
          if (!/^\d$/.test(match)) {
            return {
              success: false,
              error: `Expected 1 or 2-digit minute`,
              position
            };
          }
          parsedMinute = parseInt(match, 10);
          position += 1;
        }
        if (parsedMinute > 59) {
          return {
            success: false,
            error: `Minute out of range (got ${parsedMinute}, expected 0-59)`,
            position: position - match.length
          };
        }
        if (minute !== null && minute !== parsedMinute) {
          return {
            success: false,
            error: `Minute specified multiple times with different values: ${minute} and ${parsedMinute}`,
            position: position - match.length
          };
        }
        minute = parsedMinute;
        break;
      }

      case "second2": {
        const match = input.slice(position, position + 2);
        if (match.length < 2 || !/^\d{2}$/.test(match)) {
          return {
            success: false,
            error: `Expected 2-digit second (00-59)`,
            position
          };
        }
        const parsedSecond = parseInt(match, 10);
        if (parsedSecond > 59) {
          return {
            success: false,
            error: `Second out of range (got ${parsedSecond}, expected 00-59)`,
            position
          };
        }
        if (second !== null && second !== parsedSecond) {
          return {
            success: false,
            error: `Second specified multiple times with different values: ${second} and ${parsedSecond}`,
            position
          };
        }
        second = parsedSecond;
        position += 2;
        break;
      }

      case "second1": {
        // Try 2 digits first, then 1
        let match = input.slice(position, position + 2);
        let parsedSecond: number;
        if (/^\d{2}$/.test(match)) {
          parsedSecond = parseInt(match, 10);
          position += 2;
        } else {
          match = input.slice(position, position + 1);
          if (!/^\d$/.test(match)) {
            return {
              success: false,
              error: `Expected 1 or 2-digit second`,
              position
            };
          }
          parsedSecond = parseInt(match, 10);
          position += 1;
        }
        if (parsedSecond > 59) {
          return {
            success: false,
            error: `Second out of range (got ${parsedSecond}, expected 0-59)`,
            position: position - match.length
          };
        }
        if (second !== null && second !== parsedSecond) {
          return {
            success: false,
            error: `Second specified multiple times with different values: ${second} and ${parsedSecond}`,
            position: position - match.length
          };
        }
        second = parsedSecond;
        break;
      }

      case "millisecond3": {
        const match = input.slice(position, position + 3);
        if (match.length < 3 || !/^\d{3}$/.test(match)) {
          return {
            success: false,
            error: `Expected 3-digit millisecond (000-999)`,
            position
          };
        }
        const parsedMillisecond = parseInt(match, 10);
        if (millisecond !== null && millisecond !== parsedMillisecond) {
          return {
            success: false,
            error: `Millisecond specified multiple times with different values: ${millisecond} and ${parsedMillisecond}`,
            position
          };
        }
        millisecond = parsedMillisecond;
        position += 3;
        break;
      }

      case "ampmUpper": {
        const match = input.slice(position, position + 2).toUpperCase();
        if (match === "AM") {
          isPM = false;
          position += 2;
        } else if (match === "PM") {
          isPM = true;
          position += 2;
        } else {
          return {
            success: false,
            error: `Expected "AM" or "PM"`,
            position
          };
        }
        break;
      }

      case "ampmLower": {
        const match = input.slice(position, position + 2).toLowerCase();
        if (match === "am") {
          isPM = false;
          position += 2;
        } else if (match === "pm") {
          isPM = true;
          position += 2;
        } else {
          return {
            success: false,
            error: `Expected "am" or "pm"`,
            position
          };
        }
        break;
      }

      case "literal": {
        const expected = token.value;
        const actual = input.slice(position, position + expected.length);
        if (actual !== expected) {
          return {
            success: false,
            error: `Expected literal "${expected}", got "${actual}"`,
            position
          };
        }
        position += expected.length;
        break;
      }

      default: {
        // TypeScript exhaustiveness check
        const _exhaustive: never = token;
        return {
          success: false,
          error: `Unknown token type: ${(_exhaustive as DateTimeFormatToken).type}`,
          position
        };
      }
    }
  }

  // Check for unconsumed input
  if (position < input.length) {
    return {
      success: false,
      error: `Unexpected trailing characters: "${input.slice(position)}"`,
      position
    };
  }

  // Prefix validation: Fill in defaults while checking for gaps in the component hierarchy
  // The hierarchy is: Year → Month → Day → Hour → Minute → Second → Millisecond
  // We check for gaps and fill in defaults from most significant to least significant

  // Check if we have ANY date components to determine if this is a time-only format
  const hasAnyDateComponent = year !== null || month !== null || day !== null;

  let foundGap = false;

  // Date components
  if (year === null) {
    if (hasAnyDateComponent) {
      foundGap = true;
    }
    year = 1970; // Default epoch year for time-only formats
  }

  if (month === null) {
    if (hasAnyDateComponent) {
      foundGap = true;
    }
    month = 1;
  } else if (foundGap) {
    // Can't have month if we already found a gap (e.g., no year)
    return {
      success: false,
      error: `Invalid format: cannot have month without year`,
      position: 0
    };
  }

  if (day === null) {
    if (hasAnyDateComponent) {
      foundGap = true;
    }
    day = 1;
  } else if (foundGap) {
    // Can't have day if we already found a gap
    return {
      success: false,
      error: `Invalid format: cannot have day without year and month`,
      position: 0
    };
  }

  // Hour validation and conversion: handle hour24 vs hour12+AM/PM redundancy
  if (hour !== null && hour12 !== null) {
    // Both hour24 and hour12 specified - validate they match
    let expectedHour24: number;
    if (isPM === null) {
      // hour12 without AM/PM is ambiguous - can't validate
      return {
        success: false,
        error: `12-hour format specified without AM/PM indicator`,
        position: 0
      };
    }

    // Convert hour12 + isPM to hour24
    if (isPM) {
      expectedHour24 = hour12 === 12 ? 12 : hour12 + 12; // 12 PM -> 12, 1 PM -> 13
    } else {
      expectedHour24 = hour12 === 12 ? 0 : hour12; // 12 AM -> 0, 1 AM -> 1
    }

    if (hour !== expectedHour24) {
      return {
        success: false,
        error: `Hour mismatch: 24-hour format specifies ${hour}, but 12-hour format with ${isPM ? 'PM' : 'AM'} implies ${expectedHour24}`,
        position: 0
      };
    }
  } else if (hour === null && hour12 !== null) {
    // Only hour12 specified - convert to hour24
    if (isPM === null) {
      return {
        success: false,
        error: `12-hour format specified without AM/PM indicator`,
        position: 0
      };
    }

    if (isPM) {
      hour = hour12 === 12 ? 12 : hour12 + 12; // 12 PM -> 12, 1 PM -> 13
    } else {
      hour = hour12 === 12 ? 0 : hour12; // 12 AM -> 0, 1 AM -> 1
    }
  }

  // Continue with time components
  if (hour === null) {
    foundGap = true;
    hour = 0;
  } else if (foundGap) {
    return {
      success: false,
      error: `Invalid format: cannot have hour without year, month, and day (or use time-only format)`,
      position: 0
    };
  }

  if (minute === null) {
    foundGap = true;
    minute = 0;
  } else if (foundGap) {
    return {
      success: false,
      error: `Invalid format: cannot have minute without hour`,
      position: 0
    };
  }

  if (second === null) {
    foundGap = true;
    second = 0;
  } else if (foundGap) {
    return {
      success: false,
      error: `Invalid format: cannot have second without minute`,
      position: 0
    };
  }

  if (millisecond === null) {
    millisecond = 0;
  } else if (foundGap) {
    return {
      success: false,
      error: `Invalid format: cannot have millisecond without second`,
      position: 0
    };
  }

  // Construct Date using UTC
  const date = new Date(Date.UTC(year, month - 1, day, hour, minute, second, millisecond));

  // Validate the date is actually valid (e.g., not Feb 31)
  if (
    date.getUTCFullYear() !== year ||
    date.getUTCMonth() !== month - 1 ||
    date.getUTCDate() !== day
  ) {
    return {
      success: false,
      error: `Invalid date: ${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`,
      position: 0
    };
  }

  // Validate weekday if it was parsed
  if (parsedWeekday !== null) {
    const actualWeekday = date.getUTCDay();
    if (actualWeekday !== parsedWeekday) {
      const weekdayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
      return {
        success: false,
        error: `Weekday mismatch: parsed "${weekdayNames[parsedWeekday]}" but date is actually "${weekdayNames[actualWeekday]}"`,
        position: 0
      };
    }
  }

  return {
    success: true,
    value: date
  };
}
