/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { test } from "node:test";
import * as assert from "node:assert/strict";
import { parseDateTimeFormatted } from "./parse.js";
import { tokenizeDateTimeFormat } from "./tokenize.js";
import { variant } from "../containers/variant.js";

test("parse - basic ISO 8601 date", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025-01-15", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2025);
    assert.equal(result.value.getUTCMonth(), 0); // January
    assert.equal(result.value.getUTCDate(), 15);
  }
});

test("parse - ISO 8601 datetime", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD HH:mm:ss");
  const result = parseDateTimeFormatted("2025-01-15 14:30:45", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2025);
    assert.equal(result.value.getUTCMonth(), 0);
    assert.equal(result.value.getUTCDate(), 15);
    assert.equal(result.value.getUTCHours(), 14);
    assert.equal(result.value.getUTCMinutes(), 30);
    assert.equal(result.value.getUTCSeconds(), 45);
  }
});

test("parse - with milliseconds", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD HH:mm:ss.SSS");
  const result = parseDateTimeFormatted("2025-01-15 14:30:45.123", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCMilliseconds(), 123);
  }
});

test("parse - 12-hour format with PM", () => {
  const tokens = tokenizeDateTimeFormat("h:mm A");
  const result = parseDateTimeFormatted("2:30 PM", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCHours(), 14); // 2 PM = 14:00
    assert.equal(result.value.getUTCMinutes(), 30);
  }
});

test("parse - 12-hour format with AM", () => {
  const tokens = tokenizeDateTimeFormat("h:mm A");
  const result = parseDateTimeFormatted("9:30 AM", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCHours(), 9);
    assert.equal(result.value.getUTCMinutes(), 30);
  }
});

test("parse - 12 AM (midnight)", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD h A");
  const result = parseDateTimeFormatted("2025-01-15 12 AM", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCHours(), 0); // 12 AM = 00:00
  }
});

test("parse - 12 PM (noon)", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD h A");
  const result = parseDateTimeFormatted("2025-01-15 12 PM", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCHours(), 12); // 12 PM = 12:00
  }
});

test("parse - month names (full)", () => {
  const tokens = tokenizeDateTimeFormat("MMMM D, YYYY");
  const result = parseDateTimeFormatted("January 15, 2025", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2025);
    assert.equal(result.value.getUTCMonth(), 0); // January
    assert.equal(result.value.getUTCDate(), 15);
  }
});

test("parse - month names (short)", () => {
  const tokens = tokenizeDateTimeFormat("MMM D, YYYY");
  const result = parseDateTimeFormatted("Jan 15, 2025", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCMonth(), 0); // January
  }
});

test("parse - month names case insensitive", () => {
  const tokens = tokenizeDateTimeFormat("MMMM D, YYYY");
  const result = parseDateTimeFormatted("january 15, 2025", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCMonth(), 0); // January
  }
});

test("parse - weekday names (ignored but consumed)", () => {
  const tokens = tokenizeDateTimeFormat("dddd, MMMM D, YYYY");
  const result = parseDateTimeFormatted("Wednesday, January 15, 2025", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2025);
    assert.equal(result.value.getUTCMonth(), 0);
    assert.equal(result.value.getUTCDate(), 15);
  }
});

test("parse - unpadded single-digit month", () => {
  const tokens = tokenizeDateTimeFormat("M/D/YY");
  const result = parseDateTimeFormatted("1/5/25", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2025);
    assert.equal(result.value.getUTCMonth(), 0); // January
    assert.equal(result.value.getUTCDate(), 5);
  }
});

test("parse - unpadded double-digit month", () => {
  const tokens = tokenizeDateTimeFormat("M/D/YY");
  const result = parseDateTimeFormatted("12/25/25", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCMonth(), 11); // December
    assert.equal(result.value.getUTCDate(), 25);
  }
});

test("parse - 2-digit year", () => {
  const tokens = tokenizeDateTimeFormat("YY-MM-DD");
  const result = parseDateTimeFormatted("25-01-15", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2025); // 25 -> 2025
  }
});

test("parse - error: missing year", () => {
  const tokens = [
    variant("month2", null),
    variant("literal", "-"),
    variant("day2", null)
  ];
  const result = parseDateTimeFormatted("01-15", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("year"));
  }
});

test("parse - error: missing month", () => {
  const tokens = [
    variant("year4", null),
    variant("literal", "-"),
    variant("day2", null)
  ];
  const result = parseDateTimeFormatted("2025-15", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("month"));
  }
});

test("parse - missing day defaults to 1st", () => {
  const tokens = [
    variant("year4", null),
    variant("literal", "-"),
    variant("month2", null)
  ];
  const result = parseDateTimeFormatted("2025-01", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2025);
    assert.equal(result.value.getUTCMonth(), 0); // January
    assert.equal(result.value.getUTCDate(), 1); // Defaults to 1st
  }
});

test("parse - error: month out of range", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025-13-15", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("out of range"));
    assert.equal(result.position, 5);
  }
});

test("parse - error: day out of range", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025-01-32", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("out of range"));
  }
});

test("parse - error: invalid date (Feb 31)", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025-02-31", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("Invalid date"));
  }
});

test("parse - valid leap year date", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2024-02-29", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2024);
    assert.equal(result.value.getUTCMonth(), 1); // February
    assert.equal(result.value.getUTCDate(), 29);
  }
});

test("parse - error: invalid leap year date", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025-02-29", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("Invalid date"));
  }
});

test("parse - error: literal mismatch", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025/01/15", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("Expected literal"));
    assert.equal(result.position, 4);
  }
});

test("parse - error: trailing characters", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025-01-15 extra", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("trailing characters"));
  }
});

test("parse - error: unexpected end of input", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD HH:mm:ss");
  const result = parseDateTimeFormatted("2025-01-15", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("Unexpected end of input") || result.error.includes("Expected literal"));
  }
});

test("parse - error: expected 4-digit year", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("25-01-15", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("4-digit year"));
    assert.equal(result.position, 0);
  }
});

test("parse - error: expected 2-digit month", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025-1-15", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("2-digit month"));
  }
});

test("parse - complex format with weekday", () => {
  const tokens = tokenizeDateTimeFormat("ddd, MMM D, YYYY \\a\\t h:mm A");
  const result = parseDateTimeFormatted("Wed, Jan 15, 2025 at 2:30 PM", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCFullYear(), 2025);
    assert.equal(result.value.getUTCMonth(), 0);
    assert.equal(result.value.getUTCDate(), 15);
    assert.equal(result.value.getUTCHours(), 14);
    assert.equal(result.value.getUTCMinutes(), 30);
  }
});

test("parse - round-trip: format then parse", () => {
  const formatStr = "YYYY-MM-DD HH:mm:ss.SSS";
  const tokens = tokenizeDateTimeFormat(formatStr);

  const originalDate = new Date(Date.UTC(2025, 0, 15, 14, 30, 45, 123));
  const formatted = "2025-01-15 14:30:45.123";
  const result = parseDateTimeFormatted(formatted, tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getTime(), originalDate.getTime());
  }
});

test("parse - all months", () => {
  const shortNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const tokens = tokenizeDateTimeFormat("MMM YYYY");

  for (let i = 0; i < 12; i++) {
    const result = parseDateTimeFormatted(`${shortNames[i]} 2025`, tokens);
    assert.ok(result.success, `Failed to parse ${shortNames[i]}`);
    if (result.success) {
      assert.equal(result.value.getUTCMonth(), i);
    }
  }
});

test("parse - all weekdays", () => {
  // Use dates that actually match each weekday (January 2025)
  const weekdaysWithDates = [
    { name: "Sunday", date: "2025-01-05" },     // Jan 5, 2025 is Sunday
    { name: "Monday", date: "2025-01-06" },     // Jan 6, 2025 is Monday
    { name: "Tuesday", date: "2025-01-07" },    // Jan 7, 2025 is Tuesday
    { name: "Wednesday", date: "2025-01-15" },  // Jan 15, 2025 is Wednesday
    { name: "Thursday", date: "2025-01-09" },   // Jan 9, 2025 is Thursday
    { name: "Friday", date: "2025-01-10" },     // Jan 10, 2025 is Friday
    { name: "Saturday", date: "2025-01-11" }    // Jan 11, 2025 is Saturday
  ];
  const tokens = tokenizeDateTimeFormat("dddd, YYYY-MM-DD");

  for (const { name, date } of weekdaysWithDates) {
    const result = parseDateTimeFormatted(`${name}, ${date}`, tokens);
    assert.ok(result.success, `Failed to parse ${name}`);
  }
});

test("parse - lowercase am/pm", () => {
  const tokens = tokenizeDateTimeFormat("h:mm a");

  const resultAm = parseDateTimeFormatted("9:30 am", tokens);
  assert.ok(resultAm.success);
  if (resultAm.success) {
    assert.equal(resultAm.value.getUTCHours(), 9);
  }

  const resultPm = parseDateTimeFormatted("2:30 pm", tokens);
  assert.ok(resultPm.success);
  if (resultPm.success) {
    assert.equal(resultPm.value.getUTCHours(), 14);
  }
});

test("parse - defaults for missing time components", () => {
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");
  const result = parseDateTimeFormatted("2025-01-15", tokens);

  assert.ok(result.success);
  if (result.success) {
    // Time components should default to 0
    assert.equal(result.value.getUTCHours(), 0);
    assert.equal(result.value.getUTCMinutes(), 0);
    assert.equal(result.value.getUTCSeconds(), 0);
    assert.equal(result.value.getUTCMilliseconds(), 0);
  }
});

test("parse - unpadded time components", () => {
  const tokens = tokenizeDateTimeFormat("H:m:s");
  const result = parseDateTimeFormatted("9:5:7", tokens);

  assert.ok(result.success);
  if (result.success) {
    assert.equal(result.value.getUTCHours(), 9);
    assert.equal(result.value.getUTCMinutes(), 5);
    assert.equal(result.value.getUTCSeconds(), 7);
  }
});

test("parse - error: hour 24-hour out of range", () => {
  const tokens = tokenizeDateTimeFormat("HH:mm");
  const result = parseDateTimeFormatted("24:00", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("out of range"));
  }
});

test("parse - error: hour 12-hour out of range", () => {
  const tokens = tokenizeDateTimeFormat("hh:mm A");
  const result = parseDateTimeFormatted("13:00 PM", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("out of range"));
  }
});

test("parse - error: minute out of range", () => {
  const tokens = tokenizeDateTimeFormat("HH:mm");
  const result = parseDateTimeFormatted("14:60", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("out of range"));
  }
});

test("parse - error: second out of range", () => {
  const tokens = tokenizeDateTimeFormat("HH:mm:ss");
  const result = parseDateTimeFormatted("14:30:60", tokens);

  assert.ok(!result.success);
  if (!result.success) {
    assert.ok(result.error.includes("out of range"));
  }
});
