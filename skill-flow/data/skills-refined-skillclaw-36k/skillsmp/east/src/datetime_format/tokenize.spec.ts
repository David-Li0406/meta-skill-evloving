/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import * as assert from "node:assert/strict";
import { tokenizeDateTimeFormat, formatTokensToString } from "./tokenize.js";
import { variant } from "../containers/variant.js";

describe("parseDateTimeFormat", () => {
  test("empty string", () => {
    const result = tokenizeDateTimeFormat("");
    assert.deepEqual(result, []);
  });

  test("year tokens", () => {
    assert.deepEqual(tokenizeDateTimeFormat("YYYY"), [variant("year4", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("YY"), [variant("year2", null)]);
  });

  test("month tokens", () => {
    assert.deepEqual(tokenizeDateTimeFormat("M"), [variant("month1", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("MM"), [variant("month2", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("MMM"), [variant("monthNameShort", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("MMMM"), [variant("monthNameFull", null)]);
  });

  test("day tokens", () => {
    assert.deepEqual(tokenizeDateTimeFormat("D"), [variant("day1", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("DD"), [variant("day2", null)]);
  });

  test("weekday tokens", () => {
    assert.deepEqual(tokenizeDateTimeFormat("dd"), [variant("weekdayNameMin", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("ddd"), [variant("weekdayNameShort", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("dddd"), [variant("weekdayNameFull", null)]);
  });

  test("hour tokens - 24h", () => {
    assert.deepEqual(tokenizeDateTimeFormat("H"), [variant("hour24_1", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("HH"), [variant("hour24_2", null)]);
  });

  test("hour tokens - 12h", () => {
    assert.deepEqual(tokenizeDateTimeFormat("h"), [variant("hour12_1", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("hh"), [variant("hour12_2", null)]);
  });

  test("minute tokens", () => {
    assert.deepEqual(tokenizeDateTimeFormat("m"), [variant("minute1", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("mm"), [variant("minute2", null)]);
  });

  test("second tokens", () => {
    assert.deepEqual(tokenizeDateTimeFormat("s"), [variant("second1", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("ss"), [variant("second2", null)]);
  });

  test("millisecond token", () => {
    assert.deepEqual(tokenizeDateTimeFormat("SSS"), [variant("millisecond3", null)]);
  });

  test("AM/PM tokens", () => {
    assert.deepEqual(tokenizeDateTimeFormat("A"), [variant("ampmUpper", null)]);
    assert.deepEqual(tokenizeDateTimeFormat("a"), [variant("ampmLower", null)]);
  });

  test("ISO 8601 date format", () => {
    const result = tokenizeDateTimeFormat("YYYY-MM-DD");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("literal", "-"),
      variant("month2", null),
      variant("literal", "-"),
      variant("day2", null),
    ]);
  });

  test("ISO 8601 datetime format", () => {
    const result = tokenizeDateTimeFormat("YYYY-MM-DD HH:mm:ss");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("literal", "-"),
      variant("month2", null),
      variant("literal", "-"),
      variant("day2", null),
      variant("literal", " "),
      variant("hour24_2", null),
      variant("literal", ":"),
      variant("minute2", null),
      variant("literal", ":"),
      variant("second2", null),
    ]);
  });

  test("datetime with milliseconds", () => {
    const result = tokenizeDateTimeFormat("YYYY-MM-DD HH:mm:ss.SSS");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("literal", "-"),
      variant("month2", null),
      variant("literal", "-"),
      variant("day2", null),
      variant("literal", " "),
      variant("hour24_2", null),
      variant("literal", ":"),
      variant("minute2", null),
      variant("literal", ":"),
      variant("second2", null),
      variant("literal", "."),
      variant("millisecond3", null),
    ]);
  });

  test("12-hour format with AM/PM", () => {
    const result = tokenizeDateTimeFormat("h:mm A");
    assert.deepEqual(result, [
      variant("hour12_1", null),
      variant("literal", ":"),
      variant("minute2", null),
      variant("literal", " "),
      variant("ampmUpper", null),
    ]);
  });

  test("long date format with month name", () => {
    const result = tokenizeDateTimeFormat("MMMM D, YYYY");
    assert.deepEqual(result, [
      variant("monthNameFull", null),
      variant("literal", " "),
      variant("day1", null),
      variant("literal", ", "),
      variant("year4", null),
    ]);
  });

  test("weekday format", () => {
    const result = tokenizeDateTimeFormat("dddd, MMMM D, YYYY");
    assert.deepEqual(result, [
      variant("weekdayNameFull", null),
      variant("literal", ", "),
      variant("monthNameFull", null),
      variant("literal", " "),
      variant("day1", null),
      variant("literal", ", "),
      variant("year4", null),
    ]);
  });

  test("pure literal string - must escape", () => {
    // Unescaped format codes are parsed as tokens
    const result = tokenizeDateTimeFormat("\\H\\e\\l\\l\\o\\ \\W\\o\\r\\l\\d");
    assert.deepEqual(result, [variant("literal", "Hello World")]);
  });

  test("literal grouping - escape letters that are format codes", () => {
    // 'a' and 's' are format codes, so they must be escaped
    const result = tokenizeDateTimeFormat("Tod\\ay i\\s YYYY");
    assert.deepEqual(result, [
      variant("literal", "Today is "),
      variant("year4", null),
    ]);
  });

  test("escape single character", () => {
    const result = tokenizeDateTimeFormat("\\Y\\Y\\Y\\Y");
    assert.deepEqual(result, [variant("literal", "YYYY")]);
  });

  test("escape within tokens", () => {
    const result = tokenizeDateTimeFormat("YYYY\\-MM\\-DD");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("literal", "-"),
      variant("month2", null),
      variant("literal", "-"),
      variant("day2", null),
    ]);
  });

  test("escape backslash", () => {
    const result = tokenizeDateTimeFormat("YYYY\\\\MM");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("literal", "\\"),
      variant("month2", null),
    ]);
  });

  test("multiple escaped backslashes", () => {
    const result = tokenizeDateTimeFormat("\\\\\\\\");
    assert.deepEqual(result, [variant("literal", "\\\\")]);
  });

  test("escape non-token characters", () => {
    const result = tokenizeDateTimeFormat("\\a\\b\\c");
    assert.deepEqual(result, [variant("literal", "abc")]);
  });

  test("terminating backslash", () => {
    const result = tokenizeDateTimeFormat("YYYY\\");
    assert.deepEqual(result, [variant("year4", null), variant("literal", "\\")]);
  });

  test("unicode - CJK characters", () => {
    const result = tokenizeDateTimeFormat("YYYY年MM月DD日");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("literal", "年"),
      variant("month2", null),
      variant("literal", "月"),
      variant("day2", null),
      variant("literal", "日"),
    ]);
  });

  test("unicode - emoji", () => {
    const result = tokenizeDateTimeFormat("📅 YYYY-MM-DD");
    assert.deepEqual(result, [
      variant("literal", "📅 "),
      variant("year4", null),
      variant("literal", "-"),
      variant("month2", null),
      variant("literal", "-"),
      variant("day2", null),
    ]);
  });

  test("unicode - emoji in escape", () => {
    const result = tokenizeDateTimeFormat("\\📅");
    assert.deepEqual(result, [variant("literal", "📅")]);
  });

  test("mixed padding - unpadded time", () => {
    const result = tokenizeDateTimeFormat("H:m:s");
    assert.deepEqual(result, [
      variant("hour24_1", null),
      variant("literal", ":"),
      variant("minute1", null),
      variant("literal", ":"),
      variant("second1", null),
    ]);
  });

  test("ambiguous MM vs M - longer pattern wins", () => {
    const result = tokenizeDateTimeFormat("MM");
    assert.deepEqual(result, [variant("month2", null)]);
  });

  test("ambiguous MMMM vs MMM - longer pattern wins", () => {
    const result = tokenizeDateTimeFormat("MMMM");
    assert.deepEqual(result, [variant("monthNameFull", null)]);
  });

  test("adjacent tokens without separators", () => {
    const result = tokenizeDateTimeFormat("YYYYMMDD");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("month2", null),
      variant("day2", null),
    ]);
  });

  test("adjacent different token types", () => {
    const result = tokenizeDateTimeFormat("YYYYMMDDHHmmss");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("month2", null),
      variant("day2", null),
      variant("hour24_2", null),
      variant("minute2", null),
      variant("second2", null),
    ]);
  });

  test("partial token followed by literal", () => {
    const result = tokenizeDateTimeFormat("Mx");
    assert.deepEqual(result, [variant("month1", null), variant("literal", "x")]);
  });

  test("token at end", () => {
    // 'D' is a format code, must escape
    const result = tokenizeDateTimeFormat("\\D\\ate: YYYY");
    assert.deepEqual(result, [variant("literal", "Date: "), variant("year4", null)]);
  });

  test("complex real-world format 1", () => {
    // Must escape 'a' in "at" since it's a format code
    const result = tokenizeDateTimeFormat("dddd, MMMM D, YYYY [\\at] h:mm A");
    assert.deepEqual(result, [
      variant("weekdayNameFull", null),
      variant("literal", ", "),
      variant("monthNameFull", null),
      variant("literal", " "),
      variant("day1", null),
      variant("literal", ", "),
      variant("year4", null),
      variant("literal", " [at] "),
      variant("hour12_1", null),
      variant("literal", ":"),
      variant("minute2", null),
      variant("literal", " "),
      variant("ampmUpper", null),
    ]);
  });

  test("complex real-world format 2", () => {
    const result = tokenizeDateTimeFormat("MM/DD/YYYY hh:mm:ss A");
    assert.deepEqual(result, [
      variant("month2", null),
      variant("literal", "/"),
      variant("day2", null),
      variant("literal", "/"),
      variant("year4", null),
      variant("literal", " "),
      variant("hour12_2", null),
      variant("literal", ":"),
      variant("minute2", null),
      variant("literal", ":"),
      variant("second2", null),
      variant("literal", " "),
      variant("ampmUpper", null),
    ]);
  });

  test("format with newlines", () => {
    const result = tokenizeDateTimeFormat("YYYY-MM-DD\nHH:mm:ss");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("literal", "-"),
      variant("month2", null),
      variant("literal", "-"),
      variant("day2", null),
      variant("literal", "\n"),
      variant("hour24_2", null),
      variant("literal", ":"),
      variant("minute2", null),
      variant("literal", ":"),
      variant("second2", null),
    ]);
  });

  test("format with tabs", () => {
    const result = tokenizeDateTimeFormat("YYYY\tMM\tDD");
    assert.deepEqual(result, [
      variant("year4", null),
      variant("literal", "\t"),
      variant("month2", null),
      variant("literal", "\t"),
      variant("day2", null),
    ]);
  });

  test("escape n as literal n (not newline)", () => {
    const result = tokenizeDateTimeFormat("\\n");
    assert.deepEqual(result, [variant("literal", "n")]);
  });

  test("escape t as literal t (not tab)", () => {
    const result = tokenizeDateTimeFormat("\\t");
    assert.deepEqual(result, [variant("literal", "t")]);
  });
});

describe("formatTokensToString", () => {
  test("empty token array", () => {
    assert.equal(formatTokensToString([]), "");
  });

  test("single format token", () => {
    assert.equal(formatTokensToString([variant("year4", null)]), "YYYY");
    assert.equal(formatTokensToString([variant("month2", null)]), "MM");
  });

  test("ISO 8601 format", () => {
    const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
    assert.equal(formatTokensToString(tokens), "YYYY-MM-DD");
  });

  test("minimal escaping - only escapes when necessary", () => {
    // "Hello" - 'H' and 'h' patterns need escaping ('HH', 'H')
    const tokens1 = [variant("literal", "Hello")];
    assert.equal(formatTokensToString(tokens1), "\\Hello");

    // "World" - 'd' at end could form pattern, but single 'd' alone isn't a pattern
    const tokens2 = [variant("literal", "World")];
    assert.equal(formatTokensToString(tokens2), "World");

    // "Date" - 'D' at position 0 could start 'DD' or 'D' pattern, 'a' is pattern
    const tokens3 = [variant("literal", "Date")];
    assert.equal(formatTokensToString(tokens3), "\\D\\ate");
  });

  test("minimal escaping - format tokens separate literals", () => {
    // When tokens are properly separated, literals stringify cleanly
    const tokens = [
      variant("literal", "Tod"),
      variant("ampmLower", null),
      variant("literal", "y i"),
      variant("second1", null),
      variant("literal", " "),
      variant("year4", null),
    ];
    // "Tod" safe (no D or other patterns at start), "a" token, "y i" safe, "s" token, " " safe, "YYYY" token
    assert.equal(formatTokensToString(tokens), "Today is YYYY");
  });

  test("escapes backslashes", () => {
    const tokens = [variant("literal", "\\")];
    assert.equal(formatTokensToString(tokens), "\\\\");
  });

  test("escapes multiple backslashes", () => {
    const tokens = [variant("literal", "\\\\")];
    assert.equal(formatTokensToString(tokens), "\\\\\\\\");
  });

  test("unicode - CJK characters need no escaping", () => {
    const tokens = [
      variant("year4", null),
      variant("literal", "年"),
      variant("month2", null),
      variant("literal", "月"),
    ];
    assert.equal(formatTokensToString(tokens), "YYYY年MM月");
  });

  test("unicode - emoji need no escaping", () => {
    const tokens = [variant("literal", "📅 ")];
    assert.equal(formatTokensToString(tokens), "📅 ");
  });

  test("round-trip property - ISO format", () => {
    const original = "YYYY-MM-DD HH:mm:ss";
    const tokens = tokenizeDateTimeFormat(original);
    const canonical = formatTokensToString(tokens);
    const tokens2 = tokenizeDateTimeFormat(canonical);
    assert.deepEqual(tokens, tokens2);
  });

  test("round-trip property - escaped format", () => {
    const original = "\\Y\\Y\\Y\\Y-\\M\\M";
    const tokens = tokenizeDateTimeFormat(original);
    const canonical = formatTokensToString(tokens);
    const tokens2 = tokenizeDateTimeFormat(canonical);
    assert.deepEqual(tokens, tokens2);
  });

  test("round-trip property - mixed", () => {
    const original = "Tod\\ay i\\s YYYY";
    const tokens = tokenizeDateTimeFormat(original);
    const canonical = formatTokensToString(tokens);
    const tokens2 = tokenizeDateTimeFormat(canonical);
    assert.deepEqual(tokens, tokens2);
  });

  test("round-trip property - complex format", () => {
    const original = "dddd, MMMM D, YYYY [\\at] h:mm A";
    const tokens = tokenizeDateTimeFormat(original);
    const canonical = formatTokensToString(tokens);
    const tokens2 = tokenizeDateTimeFormat(canonical);
    assert.deepEqual(tokens, tokens2);
  });

  test("YYYY as literal requires multiple escapes", () => {
    // "YYYY" - Each Y can start "YY" or "YYYY" pattern, need multiple escapes
    const tokens = [variant("literal", "YYYY")];
    // Y at 0: starts "YYYY", escape. Y at 1: starts "YY", escape. Y at 2: starts "YY", escape. Y at 3: safe.
    assert.equal(formatTokensToString(tokens), "\\Y\\Y\\YY");
  });

  test("pattern at end of literal with format codes in middle", () => {
    const tokens = [variant("literal", "Year: YYYY")];
    // "Year: YYYY" -> Y-e-a-r-:-space-Y-Y-Y-Y
    // Position 0: "Y" starts "YY"? No, "Ye" doesn't match. But "YYYY" at position 6!
    // Actually: Y at 0 doesn't start pattern (would need YY), e-a-r safe, then "a" matches!
    assert.equal(formatTokensToString(tokens), "Ye\\ar: \\Y\\Y\\YY");
  });

  test("adjacent literals and tokens", () => {
    const tokens = [
      variant("literal", "Date is "),
      variant("year4", null),
      variant("literal", ", time is "),
      variant("hour24_2", null),
    ];
    // "Date is " -> D-a-t-e-space-i-s-space
    // D at 0 starts "D" or "DD", escape. a at 1 starts "a", escape. Others safe.
    // ", time is " -> comma safe, space safe, t safe, i safe, m starts "m" or "mm", escape. Others safe.
    assert.equal(formatTokensToString(tokens), "\\D\\ate i\\s YYYY, ti\\me i\\s HH");
  });

  test("all token types round-trip with separators", () => {
    // Note: Format tokens need separators to avoid ambiguity
    // "MMMMM" could be MMMM+M or MM+MMM, etc.
    const allTokens = [
      variant("year4", null),
      variant("literal", " "),
      variant("year2", null),
      variant("literal", " "),
      variant("month1", null),
      variant("literal", " "),
      variant("month2", null),
      variant("literal", " "),
      variant("monthNameShort", null),
      variant("literal", " "),
      variant("monthNameFull", null),
      variant("literal", " "),
      variant("day1", null),
      variant("literal", " "),
      variant("day2", null),
      variant("literal", " "),
      variant("weekdayNameMin", null),
      variant("literal", " "),
      variant("weekdayNameShort", null),
      variant("literal", " "),
      variant("weekdayNameFull", null),
      variant("literal", " "),
      variant("hour24_1", null),
      variant("literal", " "),
      variant("hour24_2", null),
      variant("literal", " "),
      variant("hour12_1", null),
      variant("literal", " "),
      variant("hour12_2", null),
      variant("literal", " "),
      variant("minute1", null),
      variant("literal", " "),
      variant("minute2", null),
      variant("literal", " "),
      variant("second1", null),
      variant("literal", " "),
      variant("second2", null),
      variant("literal", " "),
      variant("millisecond3", null),
      variant("literal", " "),
      variant("ampmUpper", null),
      variant("literal", " "),
      variant("ampmLower", null),
    ];
    const str = formatTokensToString(allTokens);
    const parsed = tokenizeDateTimeFormat(str);
    assert.deepEqual(parsed, allTokens);
  });

  test("debugging use case - show interpretation", () => {
    // User writes something with accidental format codes
    const userInput = "Today is YYYY-MM-DD at HH:MM";
    const tokens = tokenizeDateTimeFormat(userInput);
    const canonical = formatTokensToString(tokens);

    // The parser breaks "Today" at 'a' and "is" at 's', producing tokens that
    // stringify back to the same string (format tokens act as separators)
    assert.equal(canonical, "Today is YYYY-MM-DD at HH:MM");

    // And it round-trips correctly
    const tokens_again = tokenizeDateTimeFormat(canonical);
    assert.deepEqual(tokens, tokens_again);

    // User remembers to escape format codes
    const userInput2 = "Tod\\ay i\\s YYYY-MM-DD \\at HH:MM";
    const tokens2 = tokenizeDateTimeFormat(userInput2);
    const canonical2 = formatTokensToString(tokens2);

    // The parser breaks "Today" at 'a' and "is" at 's', producing tokens that
    // stringify back to the same string (format tokens act as separators)
    assert.equal(canonical2, "Tod\\ay i\\s YYYY-MM-DD \\at HH:MM");

    // And it round-trips correctly
    const tokens_again2 = tokenizeDateTimeFormat(canonical2);
    assert.deepEqual(tokens2, tokens_again2);
  });
});
