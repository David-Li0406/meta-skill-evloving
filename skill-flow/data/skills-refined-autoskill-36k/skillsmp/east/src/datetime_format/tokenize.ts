/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Parser/tokenizer for datetime format strings.
 *
 * Converts Day.js-style format strings into structured token arrays.
 * The parser handles escape sequences and groups consecutive literal
 * characters into single tokens for efficiency.
 *
 * @remarks
 * Escaping: Use backslash (`\`) to escape any character. `\x` produces
 * literal `x` for any character. A terminating backslash is treated as
 * a literal backslash.
 *
 * Unicode: The parser correctly handles Unicode codepoints including
 * surrogate pairs (but not grapheme clusters).
 */

import { variant } from "../containers/variant.js";
import type { DateTimeFormatToken } from "./types.js";

/**
 * Parses a datetime format string into structured tokens.
 *
 * @param format - The format string to parse (e.g., "YYYY-MM-DD HH:mm:ss")
 * @returns Array of format tokens
 *
 * @example
 * ```ts
 * parseDateTimeFormat("YYYY-MM-DD")
 * // Returns:
 * // [
 * //   variant("year4", null),
 * //   variant("literal", "-"),
 * //   variant("month2", null),
 * //   variant("literal", "-"),
 * //   variant("day2", null)
 * // ]
 * ```
 *
 * @example
 * ```ts
 * // Escaping
 * parseDateTimeFormat("\\YYYY-MM-DD")  // literal "YYYY-MM-DD"
 * parseDateTimeFormat("YYYY\\-MM")      // year4, literal "-", month2
 * ```
 *
 * @example
 * ```ts
 * // Unicode support
 * parseDateTimeFormat("YYYY年MM月DD日")
 * // Returns: year4, literal("年"), month2, literal("月"), day2, literal("日")
 * ```
 */
export function tokenizeDateTimeFormat(format: string): DateTimeFormatToken[] {
  const tokens: DateTimeFormatToken[] = [];

  // Convert to array of codepoints to handle surrogate pairs correctly
  const codePoints = Array.from(format);
  let i = 0;
  let literal = "";

  /**
   * Flushes accumulated literal characters as a single token.
   */
  const flushLiteral = () => {
    if (literal) {
      tokens.push(variant("literal", literal));
      literal = "";
    }
  };

  /**
   * Attempts to match a format token pattern at current position.
   *
   * @param pattern - The pattern to match (e.g., "YYYY", "MM")
   * @param tokenType - The token type to emit if matched
   * @returns true if pattern matched and consumed, false otherwise
   */
  const tryMatch = (
    pattern: string,
    tokenType: Exclude<DateTimeFormatToken["type"], "literal">
  ): boolean => {
    // Check if we have enough characters left
    if (i + pattern.length > codePoints.length) {
      return false;
    }

    // Check if the pattern matches
    const slice = codePoints.slice(i, i + pattern.length).join("");
    if (slice === pattern) {
      flushLiteral();
      tokens.push(variant(tokenType, null));
      i += pattern.length;
      return true;
    }

    return false;
  };

  while (i < codePoints.length) {
    const char = codePoints[i]!;

    // Handle escaping: \x produces literal x
    if (char === "\\") {
      if (i + 1 < codePoints.length) {
        // Escape next character
        literal += codePoints[i + 1];
        i += 2;
        continue;
      } else {
        // Terminating backslash - treat as literal
        literal += "\\";
        i++;
        continue;
      }
    }

    // Try to match format tokens (longest patterns first)
    // Year
    if (tryMatch("YYYY", "year4") || tryMatch("YY", "year2")) {
      continue;
    }

    // Month (MMMM before MMM before MM before M)
    if (
      tryMatch("MMMM", "monthNameFull") ||
      tryMatch("MMM", "monthNameShort") ||
      tryMatch("MM", "month2") ||
      tryMatch("M", "month1")
    ) {
      continue;
    }

    // Day of month
    if (tryMatch("DD", "day2") || tryMatch("D", "day1")) {
      continue;
    }

    // Day of week (dddd before ddd before dd)
    if (
      tryMatch("dddd", "weekdayNameFull") ||
      tryMatch("ddd", "weekdayNameShort") ||
      tryMatch("dd", "weekdayNameMin")
    ) {
      continue;
    }

    // Hour 24h
    if (tryMatch("HH", "hour24_2") || tryMatch("H", "hour24_1")) {
      continue;
    }

    // Hour 12h
    if (tryMatch("hh", "hour12_2") || tryMatch("h", "hour12_1")) {
      continue;
    }

    // Minute
    if (tryMatch("mm", "minute2") || tryMatch("m", "minute1")) {
      continue;
    }

    // Second
    if (tryMatch("ss", "second2") || tryMatch("s", "second1")) {
      continue;
    }

    // Millisecond
    if (tryMatch("SSS", "millisecond3")) {
      continue;
    }

    // AM/PM
    if (tryMatch("A", "ampmUpper") || tryMatch("a", "ampmLower")) {
      continue;
    }

    // Not a format token - accumulate as literal
    literal += char;
    i++;
  }

  // Flush any remaining literal
  flushLiteral();

  return tokens;
}

/**
 * Converts a token array back to a canonical format string.
 *
 * This produces a format string with minimal escaping - only escaping
 * characters when they would otherwise be parsed as format tokens.
 *
 * @param tokens - Array of format tokens to stringify
 * @param colorize - Whether to colorize format tokens with ANSI cyan (default: false)
 * @returns A canonical format string that parses to the same tokens
 *
 * @remarks
 * This is useful for debugging and error messages. When users write
 * format strings with accidental format codes, showing the canonical
 * version helps them understand what was parsed.
 *
 * When `colorize` is true, format tokens (e.g., "YYYY", "MM", "DD") are
 * wrapped in ANSI escape codes to display in cyan, making them visually
 * distinct from literal characters in terminal output.
 *
 * @example
 * ```ts
 * // Show user what their format string was interpreted as
 * const tokens = parseDateTimeFormat("Today is YYYY");
 * console.warn(`Parsed as: "${formatTokensToString(tokens)}"`);
 * // Output: Parsed as: "Tod\ay i\s YYYY"
 * ```
 *
 * @example
 * ```ts
 * // Colorized output for terminal
 * const tokens = parseDateTimeFormat("YYYY-MM-DD");
 * console.log(formatTokensToString(tokens, true));
 * // Output: format tokens in cyan, literals in default color
 * ```
 */
export function formatTokensToString(tokens: DateTimeFormatToken[], colorize: boolean = false): string {
  // Map token types to their format patterns
  const TOKEN_PATTERNS: Record<Exclude<DateTimeFormatToken["type"], "literal">, string> = {
    year4: "YYYY",
    year2: "YY",
    month1: "M",
    month2: "MM",
    monthNameShort: "MMM",
    monthNameFull: "MMMM",
    day1: "D",
    day2: "DD",
    weekdayNameMin: "dd",
    weekdayNameShort: "ddd",
    weekdayNameFull: "dddd",
    hour24_1: "H",
    hour24_2: "HH",
    hour12_1: "h",
    hour12_2: "hh",
    minute1: "m",
    minute2: "mm",
    second1: "s",
    second2: "ss",
    millisecond3: "SSS",
    ampmUpper: "A",
    ampmLower: "a",
  };

  // All format patterns in descending length order for greedy matching
  const FORMAT_PATTERNS = [
    "YYYY", "MMMM", "dddd", "SSS", "HH", "MM", "DD", "hh", "mm", "ss",
    "YY", "MMM", "ddd", "dd", "H", "M", "D", "h", "m", "s", "A", "a",
  ];

  // ANSI escape codes for colorization
  const CYAN = "\x1b[36m";
  const RESET = "\x1b[0m";

  return tokens.map(token => {
    if (token.type === "literal") {
      const chars = Array.from(token.value);
      let result = "";
      let i = 0;

      while (i < chars.length) {
        const remaining = chars.slice(i).join("");

        // Check if remaining string starts with a format pattern
        let matchedPattern = null;
        for (const pattern of FORMAT_PATTERNS) {
          if (remaining.startsWith(pattern)) {
            matchedPattern = pattern;
            break;
          }
        }

        if (matchedPattern) {
          // Escape first character to prevent token recognition
          result += "\\" + chars[i];
          i++;
        } else if (chars[i] === "\\") {
          // Always escape backslashes
          result += "\\\\";
          i++;
        } else {
          // Safe to emit as-is
          result += chars[i];
          i++;
        }
      }

      return result;
    } else {
      // Emit the format pattern for this token type
      const pattern = TOKEN_PATTERNS[token.type];
      return colorize ? `${CYAN}${pattern}${RESET}` : pattern;
    }
  }).join("");
}
