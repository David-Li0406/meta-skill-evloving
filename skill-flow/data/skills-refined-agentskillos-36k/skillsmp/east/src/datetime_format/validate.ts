/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Validation for datetime format tokens to ensure they form a valid
 * contiguous prefix of components (can't skip from year to hour without month/day).
 */

import type { DateTimeFormatToken } from "./types.js";

/**
 * Result of validating datetime format tokens.
 */
export type DateTimeFormatValidationResult =
  | { valid: true }
  | { valid: false; error: string };

/**
 * Validates that datetime format tokens form a valid contiguous prefix.
 *
 * The component hierarchy is: Year → Month → Day → Hour → Minute → Second → Millisecond
 *
 * Valid prefixes:
 * - (empty) - for time-only formats like "HH:mm"
 * - Year - e.g., "YYYY"
 * - Year, Month - e.g., "YYYY-MM"
 * - Year, Month, Day - e.g., "YYYY-MM-DD"
 * - Year, Month, Day, Hour - e.g., "YYYY-MM-DD HH"
 * - Year, Month, Day, Hour, Minute - e.g., "YYYY-MM-DD HH:mm"
 * - etc.
 *
 * Invalid combinations:
 * - Year, Hour (skipped Month and Day) - e.g., "YYYY HH:mm"
 * - Month without Year - e.g., "MM-DD"
 * - Day without Year and Month - e.g., "DD"
 *
 * @param tokens - Array of format tokens to validate
 * @returns Validation result indicating success or error
 *
 * @example
 * ```ts
 * const tokens = tokenizeDateTimeFormat("YYYY HH:mm");
 * const result = validateDateTimeFormatTokens(tokens);
 * if (!result.valid) {
 *   console.error(result.error); // "Invalid format: cannot have hour without month and day..."
 * }
 * ```
 */
export function validateDateTimeFormatTokens(tokens: DateTimeFormatToken[]): DateTimeFormatValidationResult {
  // Check which component categories are present
  let hasYear = false;
  let hasMonth = false;
  let hasDay = false;
  let hasHour = false;
  let hasMinute = false;
  let hasSecond = false;
  let hasMillisecond = false;

  for (const token of tokens) {
    switch (token.type) {
      case "year4":
      case "year2":
        hasYear = true;
        break;

      case "month2":
      case "month1":
      case "monthNameFull":
      case "monthNameShort":
        hasMonth = true;
        break;

      case "day2":
      case "day1":
        hasDay = true;
        break;

      case "hour24_2":
      case "hour24_1":
      case "hour12_2":
      case "hour12_1":
        hasHour = true;
        break;

      case "minute2":
      case "minute1":
        hasMinute = true;
        break;

      case "second2":
      case "second1":
        hasSecond = true;
        break;

      case "millisecond3":
        hasMillisecond = true;
        break;

      // Weekday, AM/PM, and literals don't affect the hierarchy
      case "weekdayNameFull":
      case "weekdayNameShort":
      case "weekdayNameMin":
      case "ampmUpper":
      case "ampmLower":
      case "literal":
        break;

      default: {
        // TypeScript exhaustiveness check
        const _exhaustive: never = token;
        return {
          valid: false,
          error: `Unknown token type: ${(_exhaustive as DateTimeFormatToken).type}`
        };
      }
    }
  }

  // Validate the "contiguous prefix" invariant
  // The hierarchy is: Year → Month → Day → Hour → Minute → Second → Millisecond

  // If we have month, we must have year
  if (hasMonth && !hasYear) {
    return {
      valid: false,
      error: "Invalid format: cannot have month without year. Use YYYY or YY before month tokens."
    };
  }

  // If we have day, we must have year and month
  if (hasDay && !hasYear) {
    return {
      valid: false,
      error: "Invalid format: cannot have day without year. Use YYYY or YY before day tokens."
    };
  }
  if (hasDay && !hasMonth) {
    return {
      valid: false,
      error: "Invalid format: cannot have day without month. Use MM or M before day tokens."
    };
  }

  // If we have hour, we must have year, month, and day (or none of them for time-only)
  if (hasHour && hasYear && !hasMonth) {
    return {
      valid: false,
      error: "Invalid format: cannot skip from year to hour. Include month (MM or M) and day (DD or D) tokens, or remove year for time-only format."
    };
  }
  if (hasHour && hasYear && hasMonth && !hasDay) {
    return {
      valid: false,
      error: "Invalid format: cannot skip from year/month to hour. Include day (DD or D) token, or remove year/month for time-only format."
    };
  }

  // If we have minute, we must have hour (and if we have date components, all of them)
  if (hasMinute && !hasHour) {
    return {
      valid: false,
      error: "Invalid format: cannot have minute without hour. Use HH or H before minute tokens."
    };
  }
  if (hasMinute && hasYear && !hasMonth) {
    return {
      valid: false,
      error: "Invalid format: cannot skip from year to minute. Include month and day tokens, or remove year for time-only format."
    };
  }
  if (hasMinute && hasYear && hasMonth && !hasDay) {
    return {
      valid: false,
      error: "Invalid format: cannot skip from year/month to minute. Include day token, or remove year/month for time-only format."
    };
  }

  // If we have second, we must have hour and minute
  if (hasSecond && !hasHour) {
    return {
      valid: false,
      error: "Invalid format: cannot have second without hour. Use HH or H before second tokens."
    };
  }
  if (hasSecond && !hasMinute) {
    return {
      valid: false,
      error: "Invalid format: cannot have second without minute. Use mm or m before second tokens."
    };
  }
  if (hasSecond && hasYear && !hasMonth) {
    return {
      valid: false,
      error: "Invalid format: cannot skip from year to second. Include month and day tokens, or remove year for time-only format."
    };
  }
  if (hasSecond && hasYear && hasMonth && !hasDay) {
    return {
      valid: false,
      error: "Invalid format: cannot skip from year/month to second. Include day token, or remove year/month for time-only format."
    };
  }

  // If we have millisecond, we must have hour, minute, and second
  if (hasMillisecond && !hasHour) {
    return {
      valid: false,
      error: "Invalid format: cannot have millisecond without hour. Use HH or H before millisecond tokens."
    };
  }
  if (hasMillisecond && !hasMinute) {
    return {
      valid: false,
      error: "Invalid format: cannot have millisecond without minute. Use mm or m before millisecond tokens."
    };
  }
  if (hasMillisecond && !hasSecond) {
    return {
      valid: false,
      error: "Invalid format: cannot have millisecond without second. Use ss or s before millisecond tokens."
    };
  }
  if (hasMillisecond && hasYear && !hasMonth) {
    return {
      valid: false,
      error: "Invalid format: cannot skip from year to millisecond. Include month and day tokens, or remove year for time-only format."
    };
  }
  if (hasMillisecond && hasYear && hasMonth && !hasDay) {
    return {
      valid: false,
      error: "Invalid format: cannot skip from year/month to millisecond. Include day token, or remove year/month for time-only format."
    };
  }

  return { valid: true };
}
