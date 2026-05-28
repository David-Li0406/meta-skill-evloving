/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { test } from "node:test";
import * as assert from "node:assert/strict";
import { formatDateTime } from "./print.js";
import { tokenizeDateTimeFormat } from "./tokenize.js";
import { variant } from "../containers/variant.js";

test("formatDateTime - year tokens", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 30, 45, 123)); // Jan 15, 2025 14:30:45.123

  assert.equal(
    formatDateTime(date, [variant("year4", null)]),
    "2025"
  );

  assert.equal(
    formatDateTime(date, [variant("year2", null)]),
    "25"
  );
});

test("formatDateTime - year2 padding", () => {
  const date = new Date(Date.UTC(2001, 0, 1)); // Year ending in 01

  assert.equal(
    formatDateTime(date, [variant("year2", null)]),
    "01"
  );
});

test("formatDateTime - month tokens", () => {
  const date = new Date(Date.UTC(2025, 0, 15)); // January

  assert.equal(
    formatDateTime(date, [variant("month1", null)]),
    "1"
  );

  assert.equal(
    formatDateTime(date, [variant("month2", null)]),
    "01"
  );

  assert.equal(
    formatDateTime(date, [variant("monthNameShort", null)]),
    "Jan"
  );

  assert.equal(
    formatDateTime(date, [variant("monthNameFull", null)]),
    "January"
  );
});

test("formatDateTime - month names for all months", () => {
  const shortNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const fullNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

  for (let month = 0; month < 12; month++) {
    const date = new Date(Date.UTC(2025, month, 15));

    assert.equal(
      formatDateTime(date, [variant("monthNameShort", null)]),
      shortNames[month]
    );

    assert.equal(
      formatDateTime(date, [variant("monthNameFull", null)]),
      fullNames[month]
    );
  }
});

test("formatDateTime - day tokens", () => {
  const date = new Date(Date.UTC(2025, 0, 5)); // 5th day

  assert.equal(
    formatDateTime(date, [variant("day1", null)]),
    "5"
  );

  assert.equal(
    formatDateTime(date, [variant("day2", null)]),
    "05"
  );
});

test("formatDateTime - weekday tokens", () => {
  const date = new Date(Date.UTC(2025, 0, 15)); // Wednesday

  assert.equal(
    formatDateTime(date, [variant("weekdayNameMin", null)]),
    "We"
  );

  assert.equal(
    formatDateTime(date, [variant("weekdayNameShort", null)]),
    "Wed"
  );

  assert.equal(
    formatDateTime(date, [variant("weekdayNameFull", null)]),
    "Wednesday"
  );
});

test("formatDateTime - weekday names for all days", () => {
  const minNames = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
  const shortNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const fullNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  // January 5, 2025 is a Sunday, so we can iterate from there
  for (let dayOffset = 0; dayOffset < 7; dayOffset++) {
    const date = new Date(Date.UTC(2025, 0, 5 + dayOffset));

    assert.equal(
      formatDateTime(date, [variant("weekdayNameMin", null)]),
      minNames[dayOffset],
      `Day ${dayOffset} min name`
    );

    assert.equal(
      formatDateTime(date, [variant("weekdayNameShort", null)]),
      shortNames[dayOffset],
      `Day ${dayOffset} short name`
    );

    assert.equal(
      formatDateTime(date, [variant("weekdayNameFull", null)]),
      fullNames[dayOffset],
      `Day ${dayOffset} full name`
    );
  }
});

test("formatDateTime - 24-hour format", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 9, 30)); // 9:30 AM

  assert.equal(
    formatDateTime(date, [variant("hour24_1", null)]),
    "9"
  );

  assert.equal(
    formatDateTime(date, [variant("hour24_2", null)]),
    "09"
  );

  const date2 = new Date(Date.UTC(2025, 0, 15, 14, 30)); // 2:30 PM

  assert.equal(
    formatDateTime(date2, [variant("hour24_1", null)]),
    "14"
  );

  assert.equal(
    formatDateTime(date2, [variant("hour24_2", null)]),
    "14"
  );
});

test("formatDateTime - 12-hour format", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 9, 30)); // 9:30 AM

  assert.equal(
    formatDateTime(date, [variant("hour12_1", null)]),
    "9"
  );

  assert.equal(
    formatDateTime(date, [variant("hour12_2", null)]),
    "09"
  );

  const date2 = new Date(Date.UTC(2025, 0, 15, 14, 30)); // 2:30 PM

  assert.equal(
    formatDateTime(date2, [variant("hour12_1", null)]),
    "2"
  );

  assert.equal(
    formatDateTime(date2, [variant("hour12_2", null)]),
    "02"
  );
});

test("formatDateTime - 12-hour format edge cases", () => {
  // Midnight (12:00 AM)
  const midnight = new Date(Date.UTC(2025, 0, 15, 0, 0));
  assert.equal(
    formatDateTime(midnight, [variant("hour12_1", null)]),
    "12"
  );

  // Noon (12:00 PM)
  const noon = new Date(Date.UTC(2025, 0, 15, 12, 0));
  assert.equal(
    formatDateTime(noon, [variant("hour12_1", null)]),
    "12"
  );

  // 1 AM
  const oneAm = new Date(Date.UTC(2025, 0, 15, 1, 0));
  assert.equal(
    formatDateTime(oneAm, [variant("hour12_1", null)]),
    "1"
  );

  // 1 PM
  const onePm = new Date(Date.UTC(2025, 0, 15, 13, 0));
  assert.equal(
    formatDateTime(onePm, [variant("hour12_1", null)]),
    "1"
  );
});

test("formatDateTime - minute tokens", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 5)); // 5 minutes

  assert.equal(
    formatDateTime(date, [variant("minute1", null)]),
    "5"
  );

  assert.equal(
    formatDateTime(date, [variant("minute2", null)]),
    "05"
  );
});

test("formatDateTime - second tokens", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 30, 7)); // 7 seconds

  assert.equal(
    formatDateTime(date, [variant("second1", null)]),
    "7"
  );

  assert.equal(
    formatDateTime(date, [variant("second2", null)]),
    "07"
  );
});

test("formatDateTime - millisecond token", () => {
  const date1 = new Date(Date.UTC(2025, 0, 15, 14, 30, 45, 123));

  assert.equal(
    formatDateTime(date1, [variant("millisecond3", null)]),
    "123"
  );

  const date2 = new Date(Date.UTC(2025, 0, 15, 14, 30, 45, 7));

  assert.equal(
    formatDateTime(date2, [variant("millisecond3", null)]),
    "007"
  );
});

test("formatDateTime - AM/PM tokens", () => {
  const am = new Date(Date.UTC(2025, 0, 15, 9, 30));

  assert.equal(
    formatDateTime(am, [variant("ampmUpper", null)]),
    "AM"
  );

  assert.equal(
    formatDateTime(am, [variant("ampmLower", null)]),
    "am"
  );

  const pm = new Date(Date.UTC(2025, 0, 15, 14, 30));

  assert.equal(
    formatDateTime(pm, [variant("ampmUpper", null)]),
    "PM"
  );

  assert.equal(
    formatDateTime(pm, [variant("ampmLower", null)]),
    "pm"
  );

  // Midnight is AM
  const midnight = new Date(Date.UTC(2025, 0, 15, 0, 0));
  assert.equal(
    formatDateTime(midnight, [variant("ampmUpper", null)]),
    "AM"
  );

  // Noon is PM
  const noon = new Date(Date.UTC(2025, 0, 15, 12, 0));
  assert.equal(
    formatDateTime(noon, [variant("ampmUpper", null)]),
    "PM"
  );
});

test("formatDateTime - literal token", () => {
  const date = new Date(Date.UTC(2025, 0, 15));

  assert.equal(
    formatDateTime(date, [variant("literal", "Hello")]),
    "Hello"
  );

  assert.equal(
    formatDateTime(date, [variant("literal", "Year: ")]),
    "Year: "
  );
});

test("formatDateTime - ISO 8601 date format", () => {
  const date = new Date(Date.UTC(2025, 0, 15));
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");

  assert.equal(
    formatDateTime(date, tokens),
    "2025-01-15"
  );
});

test("formatDateTime - ISO 8601 datetime format", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 30, 45));
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD HH:mm:ss");

  assert.equal(
    formatDateTime(date, tokens),
    "2025-01-15 14:30:45"
  );
});

test("formatDateTime - ISO 8601 with milliseconds", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 30, 45, 123));
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD HH:mm:ss.SSS");

  assert.equal(
    formatDateTime(date, tokens),
    "2025-01-15 14:30:45.123"
  );
});

test("formatDateTime - 12-hour format with AM/PM", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 30));
  const tokens = tokenizeDateTimeFormat("h:mm A");

  assert.equal(
    formatDateTime(date, tokens),
    "2:30 PM"
  );
});

test("formatDateTime - long date format", () => {
  const date = new Date(Date.UTC(2025, 0, 15));
  const tokens = tokenizeDateTimeFormat("MMMM D, YYYY");

  assert.equal(
    formatDateTime(date, tokens),
    "January 15, 2025"
  );
});

test("formatDateTime - weekday with date", () => {
  const date = new Date(Date.UTC(2025, 0, 15)); // Wednesday
  const tokens = tokenizeDateTimeFormat("dddd, MMMM D, YYYY");

  assert.equal(
    formatDateTime(date, tokens),
    "Wednesday, January 15, 2025"
  );
});

test("formatDateTime - compact format", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 30));
  const tokens = tokenizeDateTimeFormat("M/D/YY h:mm A");

  assert.equal(
    formatDateTime(date, tokens),
    "1/15/25 2:30 PM"
  );
});

test("formatDateTime - with escaped literals", () => {
  const date = new Date(Date.UTC(2025, 0, 15));
  const tokens = tokenizeDateTimeFormat("\\Y\\e\\a\\r: YYYY");

  assert.equal(
    formatDateTime(date, tokens),
    "Year: 2025"
  );
});

test("formatDateTime - complex real-world format", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 30, 45));
  const tokens = tokenizeDateTimeFormat("ddd, MMM D, YYYY \\a\\t h:mm:ss A");

  assert.equal(
    formatDateTime(date, tokens),
    "Wed, Jan 15, 2025 at 2:30:45 PM"
  );
});

test("formatDateTime - edge case: year 2000", () => {
  const date = new Date(Date.UTC(2000, 0, 1));
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");

  assert.equal(
    formatDateTime(date, tokens),
    "2000-01-01"
  );
});

test("formatDateTime - edge case: leap year", () => {
  const date = new Date(Date.UTC(2024, 1, 29)); // Feb 29, 2024
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD");

  assert.equal(
    formatDateTime(date, tokens),
    "2024-02-29"
  );
});

test("formatDateTime - edge case: end of year", () => {
  const date = new Date(Date.UTC(2025, 11, 31, 23, 59, 59, 999));
  const tokens = tokenizeDateTimeFormat("YYYY-MM-DD HH:mm:ss.SSS");

  assert.equal(
    formatDateTime(date, tokens),
    "2025-12-31 23:59:59.999"
  );
});

test("formatDateTime - empty token array", () => {
  const date = new Date(Date.UTC(2025, 0, 15));

  assert.equal(
    formatDateTime(date, []),
    ""
  );
});

test("formatDateTime - only literals", () => {
  const date = new Date(Date.UTC(2025, 0, 15));
  const tokens = [
    variant("literal", "Hello "),
    variant("literal", "World"),
  ];

  assert.equal(
    formatDateTime(date, tokens),
    "Hello World"
  );
});

test("formatDateTime - all 24-hour hours", () => {
  for (let hour = 0; hour < 24; hour++) {
    const date = new Date(Date.UTC(2025, 0, 15, hour, 0));
    const tokens = [variant("hour24_2", null)];

    const expected = hour.toString().padStart(2, "0");
    assert.equal(
      formatDateTime(date, tokens),
      expected,
      `Hour ${hour}`
    );
  }
});

test("formatDateTime - all 12-hour hours with AM/PM", () => {
  const expected12Hour = [
    { hour12: "12", ampm: "AM" }, // 0:00 = 12 AM
    { hour12: "1", ampm: "AM" },  // 1:00 = 1 AM
    { hour12: "2", ampm: "AM" },
    { hour12: "3", ampm: "AM" },
    { hour12: "4", ampm: "AM" },
    { hour12: "5", ampm: "AM" },
    { hour12: "6", ampm: "AM" },
    { hour12: "7", ampm: "AM" },
    { hour12: "8", ampm: "AM" },
    { hour12: "9", ampm: "AM" },
    { hour12: "10", ampm: "AM" },
    { hour12: "11", ampm: "AM" },
    { hour12: "12", ampm: "PM" }, // 12:00 = 12 PM
    { hour12: "1", ampm: "PM" },  // 13:00 = 1 PM
    { hour12: "2", ampm: "PM" },
    { hour12: "3", ampm: "PM" },
    { hour12: "4", ampm: "PM" },
    { hour12: "5", ampm: "PM" },
    { hour12: "6", ampm: "PM" },
    { hour12: "7", ampm: "PM" },
    { hour12: "8", ampm: "PM" },
    { hour12: "9", ampm: "PM" },
    { hour12: "10", ampm: "PM" },
    { hour12: "11", ampm: "PM" },
  ];

  for (let hour = 0; hour < 24; hour++) {
    const date = new Date(Date.UTC(2025, 0, 15, hour, 0));
    const tokens = tokenizeDateTimeFormat("h A");

    const expected = `${expected12Hour[hour]!.hour12} ${expected12Hour[hour]!.ampm}`;
    assert.equal(
      formatDateTime(date, tokens),
      expected,
      `Hour ${hour} (${expected})`
    );
  }
});

test("formatDateTime - unicode in literals", () => {
  const date = new Date(Date.UTC(2025, 0, 15));
  const tokens = tokenizeDateTimeFormat("YYYY年MM月DD日");

  assert.equal(
    formatDateTime(date, tokens),
    "2025年01月15日"
  );
});

test("formatDateTime - newlines in format", () => {
  const date = new Date(Date.UTC(2025, 0, 15, 14, 30));
  const tokens = [
    variant("year4", null),
    variant("literal", "-"),
    variant("month2", null),
    variant("literal", "-"),
    variant("day2", null),
    variant("literal", "\n"),
    variant("hour24_2", null),
    variant("literal", ":"),
    variant("minute2", null),
  ];

  assert.equal(
    formatDateTime(date, tokens),
    "2025-01-15\n14:30"
  );
});
