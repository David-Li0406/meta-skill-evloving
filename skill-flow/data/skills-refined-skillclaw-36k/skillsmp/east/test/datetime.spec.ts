/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, DateTimeType } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("DateTime", (test) => {
    test("Component extraction", $ => {
        // Create DateTimeExpr directly using const variables
        const date1 = $.const(new Date("2024-03-15T10:30:45.123Z"), DateTimeType);
        const date2 = $.const(new Date("2020-12-31T23:59:59.999Z"), DateTimeType);
        const date3 = $.const(new Date("1970-01-01T00:00:00.000Z"), DateTimeType);
        const date4 = $.const(new Date("2000-02-29T12:00:00.000Z"), DateTimeType);

        // Test getYear() with known dates
        $(assert.equal(date1.getYear(), 2024n))
        $(assert.equal(date2.getYear(), 2020n))
        $(assert.equal(date3.getYear(), 1970n))
        $(assert.equal(date4.getYear(), 2000n)) // Leap year

        // Test getMonth() (1-12)
        $(assert.equal(date1.getMonth(), 3n)) // March
        $(assert.equal(date2.getMonth(), 12n)) // December
        $(assert.equal(date3.getMonth(), 1n)) // January
        $(assert.equal(date4.getMonth(), 2n)) // February

        // Test getDayOfMonth() (1-31)
        $(assert.equal(date1.getDayOfMonth(), 15n))
        $(assert.equal(date2.getDayOfMonth(), 31n))
        $(assert.equal(date3.getDayOfMonth(), 1n))
        $(assert.equal(date4.getDayOfMonth(), 29n)) // Leap day

        // Test getHour() (0-23)
        $(assert.equal(date1.getHour(), 10n))
        $(assert.equal(date2.getHour(), 23n))
        $(assert.equal(date3.getHour(), 0n))
        $(assert.equal(date4.getHour(), 12n))

        // Test getMinute() (0-59)
        $(assert.equal(date1.getMinute(), 30n))
        $(assert.equal(date2.getMinute(), 59n))
        $(assert.equal(date3.getMinute(), 0n))
        $(assert.equal(date4.getMinute(), 0n))

        // Test getSecond() (0-59)
        $(assert.equal(date1.getSecond(), 45n))
        $(assert.equal(date2.getSecond(), 59n))
        $(assert.equal(date3.getSecond(), 0n))
        $(assert.equal(date4.getSecond(), 0n))

        // Test getDayOfWeek() (1-7, Monday=1, Sunday=7) - ISO 8601
        $(assert.equal(date1.getDayOfWeek(), 5n)) // March 15, 2024 is Friday (unchanged)
        $(assert.equal(date2.getDayOfWeek(), 4n)) // December 31, 2020 is Thursday (unchanged)
        $(assert.equal(date3.getDayOfWeek(), 4n)) // January 1, 1970 is Thursday (unchanged)
        $(assert.equal(date4.getDayOfWeek(), 2n)) // February 29, 2000 is Tuesday (unchanged)

        // Test specific Sunday to verify ISO conversion: March 17, 2024 is Sunday
        const sundayDate = $.const(new Date("2024-03-17T12:00:00.000Z"), DateTimeType);
        $(assert.equal(sundayDate.getDayOfWeek(), 7n)) // Sunday should be 7 in ISO 8601

        // Test getMillisecond() (0-999)
        $(assert.equal(date1.getMillisecond(), 123n))
        $(assert.equal(date2.getMillisecond(), 999n))
        $(assert.equal(date3.getMillisecond(), 0n))
        $(assert.equal(date4.getMillisecond(), 0n))
    });

    test("Duration arithmetic", $ => {
        // Test basic millisecond addition with integers
        const baseDate = $.const(new Date("2024-01-01T12:00:00.000Z"), DateTimeType);

        // Add exact milliseconds with bigint
        const plus500ms = baseDate.addMilliseconds(500n);
        $(assert.equal(plus500ms.getSecond(), 0n)) // Still same second

        // Add 1 second (1000ms) with bigint
        const plus1sec = baseDate.addMilliseconds(1000n);
        $(assert.equal(plus1sec.getSecond(), 1n))
        $(assert.equal(plus1sec.getMinute(), 0n)) // Still same minute

        // Add 1 minute (60000ms) with bigint
        const plus1min = baseDate.addMilliseconds(60000n);
        $(assert.equal(plus1min.getMinute(), 1n))
        $(assert.equal(plus1min.getHour(), 12n)) // Still same hour

        // Add 1 hour (3600000ms) with bigint
        const plus1hour = baseDate.addMilliseconds(3600000n);
        $(assert.equal(plus1hour.getHour(), 13n))
        $(assert.equal(plus1hour.getDayOfMonth(), 1n)) // Still same day

        // Test with float inputs (should round to nearest millisecond)
        const plus999point4ms = baseDate.addMilliseconds(999.4); // Should round to 999ms -> same second
        const plus999point6ms = baseDate.addMilliseconds(999.6); // Should round to 1000ms -> next second

        // Test rounding behavior by checking if it crosses the 1-second boundary
        $(assert.equal(plus999point4ms.getSecond(), 0n)) // 999ms -> still same second
        $(assert.equal(plus999point6ms.getSecond(), 1n)) // 1000ms -> next second

        // Test other fractional values for consistency
        const plus1500point3ms = baseDate.addMilliseconds(1500.3); // Should round to 1500ms = 1.5 seconds
        $(assert.equal(plus1500point3ms.getSecond(), 1n)) // Should be 1 second (1500ms total)

        const plus1500point7ms = baseDate.addMilliseconds(1500.7); // Should round to 1501ms
        $(assert.equal(plus1500point7ms.getSecond(), 1n)) // Should still be 1 second (1501ms total)

        // Test negative values (subtraction)
        const minus1sec = baseDate.addMilliseconds(-1000n);
        $(assert.equal(minus1sec.getSecond(), 59n)) // Should wrap to previous minute
        $(assert.equal(minus1sec.getMinute(), 59n))
        $(assert.equal(minus1sec.getHour(), 11n))
    });

    test("Duration methods", $ => {
        const baseDate = $.const(new Date("2024-01-01T12:30:45.000Z"), DateTimeType);

        // Test addSeconds with different input types
        const plus30sec_bigint = baseDate.addSeconds(30n);
        $(assert.equal(plus30sec_bigint.getSecond(), 15n)) // 45 + 30 = 75 -> 15 (wrap to next minute)
        $(assert.equal(plus30sec_bigint.getMinute(), 31n)) // 30 + 1 = 31

        const plus1point5sec = baseDate.addSeconds(1.5); // 1.5 seconds = 1500ms
        $(assert.equal(plus1point5sec.getSecond(), 46n)) // 45 + 1 = 46 (fractional part becomes milliseconds)

        // Test addMinutes
        const plus90min = baseDate.addMinutes(90n); // 90 minutes = 1.5 hours
        $(assert.equal(plus90min.getHour(), 14n)) // 12 + 1 = 13, plus 30 more minutes = 14
        $(assert.equal(plus90min.getMinute(), 0n)) // 30 + 90 = 120 -> 0 (wrap 2 hours)

        const plus2point5min = baseDate.addMinutes(2.5); // 2.5 minutes = 2min 30sec
        $(assert.equal(plus2point5min.getMinute(), 33n)) // 30 + 2 = 32, plus 30 seconds -> 33
        $(assert.equal(plus2point5min.getSecond(), 15n)) // 45 + 30 = 75 -> 15

        // Test addHours
        const plus36hours = baseDate.addHours(36n); // 36 hours = 1.5 days
        $(assert.equal(plus36hours.getDayOfMonth(), 3n)) // Jan 1 + 1.5 days = Jan 3 (approximately)
        $(assert.equal(plus36hours.getHour(), 0n)) // 12 + 36 = 48 -> 0 (wrap 2 days)

        const plus0point5hour = baseDate.addHours(0.5); // 0.5 hour = 30 minutes
        $(assert.equal(plus0point5hour.getHour(), 13n)) // Still 12 PM hour
        $(assert.equal(plus0point5hour.getMinute(), 0n)) // 30 + 30 = 60 -> 0 (wrap to next hour)

        // Test addDays
        const plus7days = baseDate.addDays(7n);
        $(assert.equal(plus7days.getDayOfMonth(), 8n)) // Jan 1 + 7 = Jan 8
        $(assert.equal(plus7days.getHour(), 12n)) // Same time

        const plus1point5days = baseDate.addDays(1.5); // 1.5 days = 36 hours
        $(assert.equal(plus1point5days.getDayOfMonth(), 3n)) // Jan 1 + 1.5 = Jan 3 (approximately)

        // Test addWeeks
        const plus2weeks = baseDate.addWeeks(2n);
        $(assert.equal(plus2weeks.getDayOfMonth(), 15n)) // Jan 1 + 14 days = Jan 15
        $(assert.equal(plus2weeks.getHour(), 12n)) // Same time

        const plus0point5week = baseDate.addWeeks(0.5); // 0.5 week = 3.5 days
        $(assert.equal(plus0point5week.getDayOfMonth(), 5n)) // Jan 1 + 3.5 days = Jan 5 (approximately)

        // Test subtractSeconds
        const minus30sec = baseDate.subtractSeconds(30n);
        $(assert.equal(minus30sec.getSecond(), 15n)) // 45 - 30 = 15

        const minus50sec = baseDate.subtractSeconds(50n);
        $(assert.equal(minus50sec.getSecond(), 55n)) // 45 - 50 = -5 -> 55 (wrap to previous minute)
        $(assert.equal(minus50sec.getMinute(), 29n)) // 30 - 1 = 29

        // Test subtractMinutes
        const minus40min = baseDate.subtractMinutes(40n);
        $(assert.equal(minus40min.getMinute(), 50n)) // 30 - 40 = -10 -> 50 (wrap to previous hour)
        $(assert.equal(minus40min.getHour(), 11n)) // 12 - 1 = 11

        // Test subtractHours
        const minus15hours = baseDate.subtractHours(15n);
        $(assert.equal(minus15hours.getHour(), 21n)) // 12 - 15 = -3 -> 21 (wrap to previous day)
        $(assert.equal(minus15hours.getDayOfMonth(), 31n)) // Wrap to Dec 31

        // Test subtractDays
        const minus2days = baseDate.subtractDays(2n);
        $(assert.equal(minus2days.getDayOfMonth(), 30n)) // Jan 1 - 2 = Dec 30
        $(assert.equal(minus2days.getMonth(), 12n)) // December

        // Test subtractWeeks
        const minus1week = baseDate.subtractWeeks(1n);
        $(assert.equal(minus1week.getDayOfMonth(), 25n)) // Jan 1 - 7 days = Dec 25
        $(assert.equal(minus1week.getMonth(), 12n)) // December
        $(assert.equal(minus1week.getHour(), 12n)) // Same time

        const minus2point5weeks = baseDate.subtractWeeks(2.5); // 2.5 weeks = 17.5 days
        $(assert.equal(minus2point5weeks.getMonth(), 12n)) // December
        $(assert.equal(minus2point5weeks.getDayOfMonth(), 15n)) // Jan 1 - 17.5 days ≈ Dec 15
    });

    test("Duration calculations", $ => {
        const baseDate = $.const(new Date("2024-01-01T12:00:00.000Z"), DateTimeType);
        const laterDate = $.const(new Date("2024-01-01T12:01:30.500Z"), DateTimeType); // 90.5 seconds later
        const earlierDate = $.const(new Date("2024-01-01T11:30:00.000Z"), DateTimeType); // 30 minutes earlier
        const sameDayLater = $.const(new Date("2024-01-02T15:30:00.000Z"), DateTimeType); // 1 day 3.5 hours later

        // Test durationMilliseconds with positive duration (future date)
        const millisToLater = baseDate.durationMilliseconds(laterDate);
        $(assert.equal(millisToLater, 90500n)) // 1 minute 30.5 seconds = 90500ms

        // Test durationMilliseconds with negative duration (past date)
        const millisToEarlier = baseDate.durationMilliseconds(earlierDate);
        $(assert.equal(millisToEarlier, -1800000n)) // -30 minutes = -1800000ms

        // Test durationMilliseconds with same date
        const millisToSame = baseDate.durationMilliseconds(baseDate);
        $(assert.equal(millisToSame, 0n))

        // Test durationSeconds with fractional result
        const secondsToLater = baseDate.durationSeconds(laterDate);
        $(assert.equal(secondsToLater, 90.5)) // 90.5 seconds exactly

        const secondsToEarlier = baseDate.durationSeconds(earlierDate);
        $(assert.equal(secondsToEarlier, -1800.0)) // -30 minutes = -1800 seconds

        // Test durationMinutes with fractional result
        const minutesToLater = baseDate.durationMinutes(laterDate);
        $(assert.equal(minutesToLater, 1.5083333333333333)) // 90.5 seconds ≈ 1.508 minutes

        const minutesToEarlier = baseDate.durationMinutes(earlierDate);
        $(assert.equal(minutesToEarlier, -30.0)) // -30 minutes exactly

        // Test durationHours with fractional result
        const hoursToEarlier = baseDate.durationHours(earlierDate);
        $(assert.equal(hoursToEarlier, -0.5)) // -30 minutes = -0.5 hours

        const hoursToSameDayLater = baseDate.durationHours(sameDayLater);
        $(assert.equal(hoursToSameDayLater, 27.5)) // 1 day 3.5 hours = 27.5 hours

        // Test durationDays with fractional result
        const daysToSameDayLater = baseDate.durationDays(sameDayLater);
        $(assert.equal(daysToSameDayLater, 1.1458333333333333)) // 27.5 hours ≈ 1.146 days

        const daysToEarlier = baseDate.durationDays(earlierDate);
        $(assert.equal(daysToEarlier, -0.020833333333333332)) // -0.5 hours ≈ -0.021 days

        // Test durationWeeks with fractional result
        const oneWeekLater = $.const(new Date("2024-01-08T12:00:00.000Z"), DateTimeType); // Exactly 1 week later
        const weeksToOneWeekLater = baseDate.durationWeeks(oneWeekLater);
        $(assert.equal(weeksToOneWeekLater, 1.0)) // Exactly 1 week

        const twoWeeksEarlier = $.const(new Date("2023-12-18T12:00:00.000Z"), DateTimeType); // 2 weeks earlier
        const weeksToTwoWeeksEarlier = baseDate.durationWeeks(twoWeeksEarlier);
        $(assert.equal(weeksToTwoWeeksEarlier, -2.0)) // Exactly -2 weeks

        const onePointFiveWeeksLater = $.const(new Date("2024-01-12T00:00:00.000Z"), DateTimeType); // 1.5 weeks later (10.5 days)
        const weeksToOnePointFiveWeeksLater = baseDate.durationWeeks(onePointFiveWeeksLater);
        $(assert.equal(weeksToOnePointFiveWeeksLater, 1.5)) // Exactly 1.5 weeks

        // Test edge case: duration to same date should be 0 for all units
        $(assert.equal(baseDate.durationSeconds(baseDate), 0.0))
        $(assert.equal(baseDate.durationMinutes(baseDate), 0.0))
        $(assert.equal(baseDate.durationHours(baseDate), 0.0))
        $(assert.equal(baseDate.durationDays(baseDate), 0.0))
        $(assert.equal(baseDate.durationWeeks(baseDate), 0.0))
    });

    test("Epoch conversion and component construction", $ => {
        const testDate = $.const(new Date("2024-03-15T10:30:45.123Z"), DateTimeType);
        const testEpoch = 1710498645123n; // 2024-03-15T10:30:45.123Z

        $(assert.equal(testDate.toEpochMilliseconds(), testEpoch));
        $(assert.equal(East.DateTime.fromEpochMilliseconds(testEpoch), testDate));

        const constructedDate = $.let(East.DateTime.fromComponents(2024n, 3n, 15n, 10n, 30n, 45n, 123n));
        $(assert.equal(constructedDate.getYear(), 2024n))
        $(assert.equal(constructedDate.getMonth(), 3n))
        $(assert.equal(constructedDate.getDayOfMonth(), 15n))
        $(assert.equal(constructedDate.getHour(), 10n))
        $(assert.equal(constructedDate.getMinute(), 30n))
        $(assert.equal(constructedDate.getSecond(), 45n))
        $(assert.equal(constructedDate.getMillisecond(), 123n))
        $(assert.equal(constructedDate, testDate));
    });

    test("DateTime rounding", $ => {
        // Test roundDownMillisecond
        const testDate = $.const(new Date("2024-03-15T10:30:45.123Z"), DateTimeType);
        const roundDownMillisecond = $.let(East.DateTime.roundDownMillisecond);

        // Round down to nearest 100ms
        const rounded100ms = $.let(roundDownMillisecond(testDate, 100n));
        $(assert.equal(rounded100ms.getYear(), 2024n))
        $(assert.equal(rounded100ms.getMonth(), 3n))
        $(assert.equal(rounded100ms.getDayOfMonth(), 15n))
        $(assert.equal(rounded100ms.getHour(), 10n))
        $(assert.equal(rounded100ms.getMinute(), 30n))
        $(assert.equal(rounded100ms.getSecond(), 45n))
        $(assert.equal(rounded100ms.getMillisecond(), 100n)) // 123ms -> 100ms

        // Round down to nearest 500ms
        const rounded500ms = $.let(roundDownMillisecond(testDate, 500n));
        $(assert.equal(rounded500ms.getMillisecond(), 0n)) // 123ms -> 0ms

        // Round down to nearest 1ms (should be same as original)
        const rounded1ms = $.let(roundDownMillisecond(testDate, 1n));
        $(assert.equal(rounded1ms.getMillisecond(), 123n)) // No change

        // Test roundDownSecond
        const roundDownSecond = $.let(East.DateTime.roundDownSecond);

        // Round down to nearest 10 seconds
        const rounded10sec = $.let(roundDownSecond(testDate, 10n));
        $(assert.equal(rounded10sec.getSecond(), 40n)) // 45s -> 40s
        $(assert.equal(rounded10sec.getMillisecond(), 0n)) // Should clear ms

        // Round down to nearest 30 seconds
        const rounded30sec = $.let(roundDownSecond(testDate, 30n));
        $(assert.equal(rounded30sec.getSecond(), 30n)) // 45s -> 30s

        // Test roundDownMinute
        const roundDownMinute = $.let(East.DateTime.roundDownMinute);

        // Round down to nearest 15 minutes
        const rounded15min = $.let(roundDownMinute(testDate, 15n));
        $(assert.equal(rounded15min.getMinute(), 30n)) // 30min -> 30min (already multiple)
        $(assert.equal(rounded15min.getSecond(), 0n)) // Should clear seconds
        $(assert.equal(rounded15min.getMillisecond(), 0n)) // Should clear ms

        // Round down to nearest 20 minutes
        const rounded20min = $.let(roundDownMinute(testDate, 20n));
        $(assert.equal(rounded20min.getMinute(), 20n)) // 30min -> 20min

        // Test roundDownHour
        const roundDownHour = $.let(East.DateTime.roundDownHour);

        // Round down to nearest 6 hours
        const rounded6hour = $.let(roundDownHour(testDate, 6n));
        $(assert.equal(rounded6hour.getHour(), 6n)) // 10am -> 6am
        $(assert.equal(rounded6hour.getMinute(), 0n)) // Should clear minutes
        $(assert.equal(rounded6hour.getSecond(), 0n)) // Should clear seconds
        $(assert.equal(rounded6hour.getMillisecond(), 0n)) // Should clear ms

        // Test roundUp East.functiontions
        const roundUpMillisecond = $.let(East.DateTime.roundUpMillisecond);
        const roundUpSecond = $.let(East.DateTime.roundUpSecond);
        const roundUpMinute = $.let(East.DateTime.roundUpMinute);
        const roundUpHour = $.let(East.DateTime.roundUpHour);

        // roundUpMillisecond: 123ms -> 200ms (round up to nearest 100ms)
        const upMs = $.let(roundUpMillisecond(testDate, 100n));
        $(assert.equal(upMs.getMillisecond(), 200n))

        // roundUpSecond: 45s -> 50s (round up to nearest 10s)
        const upSec = $.let(roundUpSecond(testDate, 10n));
        $(assert.equal(upSec.getSecond(), 50n))
        $(assert.equal(upSec.getMillisecond(), 0n)) // Should clear ms

        // roundUpMinute: 30min -> 45min (round up to nearest 15min)
        const upMin = $.let(roundUpMinute(testDate, 15n));
        $(assert.equal(upMin.getMinute(), 45n))

        // roundUpHour: 10am -> 12pm (round up to nearest 6 hours)
        const upHour = $.let(roundUpHour(testDate, 6n));
        $(assert.equal(upHour.getHour(), 12n))

        // Test roundNearest East.functiontions
        const roundNearestMillisecond = $.let(East.DateTime.roundNearestMillisecond);
        const roundNearestSecond = $.let(East.DateTime.roundNearestSecond);
        const roundNearestMinute = $.let(East.DateTime.roundNearestMinute);
        const roundNearestHour = $.let(East.DateTime.roundNearestHour);

        // roundNearestMillisecond: 123ms -> 100ms (closer to 100 than 200)
        const nearMs = $.let(roundNearestMillisecond(testDate, 100n));
        $(assert.equal(nearMs.getMillisecond(), 100n))

        // roundNearestSecond: 45s -> 50s (closer to 50 than 40)
        const nearSec = $.let(roundNearestSecond(testDate, 10n));
        $(assert.equal(nearSec.getSecond(), 50n))

        // roundNearestMinute: 30min -> 30min (exactly on 15min boundary)
        const nearMin = $.let(roundNearestMinute(testDate, 15n));
        $(assert.equal(nearMin.getMinute(), 30n))

        // roundNearestHour: 10am -> 12pm (closer to 12 than 6)
        const nearHour = $.let(roundNearestHour(testDate, 6n));
        $(assert.equal(nearHour.getHour(), 12n))

        // Test day rounding East.functiontions with a specific date for predictable results
        // Using 2024-03-17T14:30:45.123Z (March 17, 2024, 2:30 PM) - Sunday
        const dayTestDate = $.const(new Date("2024-03-17T14:30:45.123Z"), DateTimeType);

        const roundDownDay = $.let(East.DateTime.roundDownDay);
        const roundUpDay = $.let(East.DateTime.roundUpDay);
        const roundNearestDay = $.let(East.DateTime.roundNearestDay);

        // Test roundDownDay: Should round to start of day boundaries
        // Round down to nearest 1 day -> start of March 17
        const downDay1 = $.let(roundDownDay(dayTestDate, 1n));
        $(assert.equal(downDay1.getYear(), 2024n))
        $(assert.equal(downDay1.getMonth(), 3n))
        $(assert.equal(downDay1.getDayOfMonth(), 17n))
        $(assert.equal(downDay1.getHour(), 0n)) // Should clear to midnight
        $(assert.equal(downDay1.getMinute(), 0n))
        $(assert.equal(downDay1.getSecond(), 0n))
        $(assert.equal(downDay1.getMillisecond(), 0n))

        // Round down to nearest 7 days (epoch-based) -> March 14
        const downDay7 = $.let(roundDownDay(dayTestDate, 7n));
        $(assert.equal(downDay7.getDayOfMonth(), 14n)) // 7-day boundary from Unix epoch
        $(assert.equal(downDay7.getHour(), 0n))

        // Test roundUpDay: Should round up to end of day boundaries
        // Round up to nearest 1 day -> start of March 18
        const upDay1 = $.let(roundUpDay(dayTestDate, 1n));
        $(assert.equal(upDay1.getDayOfMonth(), 18n)) // Next day
        $(assert.equal(upDay1.getHour(), 0n)) // Start of day

        // Round up to nearest 7 days -> March 21 (next 7-day boundary from epoch)
        const upDay7 = $.let(roundUpDay(dayTestDate, 7n));
        $(assert.equal(upDay7.getDayOfMonth(), 21n))
        $(assert.equal(upDay7.getHour(), 0n))

        // Test roundNearestDay: Should round to closest boundary
        // For nearest 1 day: 2:30 PM is closer to end of day (10.5 hrs away) than start (14.5 hrs away)
        const nearDay1 = $.let(roundNearestDay(dayTestDate, 1n));
        $(assert.equal(nearDay1.getDayOfMonth(), 18n)) // Round up to March 18
        $(assert.equal(nearDay1.getHour(), 0n))

        // Test with morning time - should round to start of same day
        const morningDate = $.const(new Date("2024-03-17T08:30:00.000Z"), DateTimeType); // 8:30 AM
        const nearMorning = $.let(roundNearestDay(morningDate, 1n));
        $(assert.equal(nearMorning.getDayOfMonth(), 17n)) // Round down to March 17
        $(assert.equal(nearMorning.getHour(), 0n))

        // Test ISO week rounding East.functiontions (Monday boundaries)
        // Using March 17, 2024 (Sunday) 14:30 as test date
        const weekTestDate = $.const(new Date("2024-03-17T14:30:45.123Z"), DateTimeType);

        const roundDownWeek = $.let(East.DateTime.roundDownWeek);
        const roundUpWeek = $.let(East.DateTime.roundUpWeek);
        const roundNearestWeek = $.let(East.DateTime.roundNearestWeek);

        // Test roundDownWeek: Sunday should round down to Monday of same week
        // March 17, 2024 (Sunday) -> March 11, 2024 (Monday)
        const downWeek1 = $.let(roundDownWeek(weekTestDate, 1n));
        $(assert.equal(downWeek1.getYear(), 2024n))
        $(assert.equal(downWeek1.getMonth(), 3n))
        $(assert.equal(downWeek1.getDayOfMonth(), 11n)) // Monday March 11
        $(assert.equal(downWeek1.getDayOfWeek(), 1n)) // Should be Monday (1 in ISO)
        $(assert.equal(downWeek1.getHour(), 0n)) // Should clear to midnight
        $(assert.equal(downWeek1.getMinute(), 0n))
        $(assert.equal(downWeek1.getSecond(), 0n))
        $(assert.equal(downWeek1.getMillisecond(), 0n))

        // Test roundUpWeek: Sunday should round up to Monday of next week
        // March 17, 2024 (Sunday) -> March 18, 2024 (Monday)
        const upWeek1 = $.let(roundUpWeek(weekTestDate, 1n));
        $(assert.equal(upWeek1.getDayOfMonth(), 18n)) // Monday March 18
        $(assert.equal(upWeek1.getDayOfWeek(), 1n)) // Should be Monday
        $(assert.equal(upWeek1.getHour(), 0n))

        // Test roundNearestWeek: Sunday afternoon closer to next Monday
        // March 17, 2024 2:30 PM -> March 18, 2024 (Monday) - closer to next week
        const nearWeek1 = $.let(roundNearestWeek(weekTestDate, 1n));
        $(assert.equal(nearWeek1.getDayOfMonth(), 18n)) // Should round up to March 18
        $(assert.equal(nearWeek1.getDayOfWeek(), 1n)) // Should be Monday

        // Test with Monday to verify it stays unchanged
        const mondayDate = $.const(new Date("2024-03-11T10:30:00.000Z"), DateTimeType); // Monday
        const mondayDown = $.let(roundDownWeek(mondayDate, 1n));
        $(assert.equal(mondayDown.getDayOfMonth(), 11n)) // Should stay March 11
        $(assert.equal(mondayDown.getDayOfWeek(), 1n)) // Still Monday
        $(assert.equal(mondayDown.getHour(), 0n)) // But clear to midnight

        // Test 2-week rounding (bi-weekly boundaries)
        const biweeklyDown = $.let(roundDownWeek(weekTestDate, 2n));
        $(assert.equal(biweeklyDown.getDayOfWeek(), 1n)) // Should still be Monday
    });

    test("Month and year rounding", $ => {
        const roundDownMonth = $.let(East.DateTime.roundDownMonth);
        const roundDownYear = $.let(East.DateTime.roundDownYear);

        // Test roundDownMonth: March 17, 2024 -> March 1, 2024
        const monthTestDate = $.const(new Date("2024-03-17T14:30:45.123Z"), DateTimeType);
        const downMonth1 = $.let(roundDownMonth(monthTestDate, 1n));
        $(assert.equal(downMonth1.getYear(), 2024n))
        $(assert.equal(downMonth1.getMonth(), 3n)) // March
        $(assert.equal(downMonth1.getDayOfMonth(), 1n)) // 1st day of month
        $(assert.equal(downMonth1.getHour(), 0n)) // Midnight
        $(assert.equal(downMonth1.getMinute(), 0n))
        $(assert.equal(downMonth1.getSecond(), 0n))
        $(assert.equal(downMonth1.getMillisecond(), 0n))

        // Test roundDownMonth with 3-month step: March -> January (Q1 start)
        const quarterDown = $.let(roundDownMonth(monthTestDate, 3n));
        $(assert.equal(quarterDown.getMonth(), 1n)) // January (Q1 start)
        $(assert.equal(quarterDown.getDayOfMonth(), 1n))

        // Test roundDownMonth with 6-month step: March -> January (H1 start)
        const halfYearDown = $.let(roundDownMonth(monthTestDate, 6n));
        $(assert.equal(halfYearDown.getMonth(), 1n)) // January (H1 start)

        // Test roundDownYear: March 17, 2024 -> January 1, 2024
        const downYear1 = $.let(roundDownYear(monthTestDate, 1n));
        $(assert.equal(downYear1.getYear(), 2024n))
        $(assert.equal(downYear1.getMonth(), 1n)) // January
        $(assert.equal(downYear1.getDayOfMonth(), 1n)) // 1st day of year
        $(assert.equal(downYear1.getHour(), 0n)) // Midnight
        $(assert.equal(downYear1.getMinute(), 0n))
        $(assert.equal(downYear1.getSecond(), 0n))
        $(assert.equal(downYear1.getMillisecond(), 0n))

        // Test roundDownYear with 5-year step: 2024 -> 2020
        const fiveYearDown = $.let(roundDownYear(monthTestDate, 5n));
        $(assert.equal(fiveYearDown.getYear(), 2020n)) // 2020 (nearest 5-year boundary)
        $(assert.equal(fiveYearDown.getMonth(), 1n)) // January
        $(assert.equal(fiveYearDown.getDayOfMonth(), 1n))

        // Test with December date to verify year boundary handling
        const decemberDate = $.const(new Date("2024-12-25T18:30:00.000Z"), DateTimeType);
        const decDownMonth = $.let(roundDownMonth(decemberDate, 1n));
        $(assert.equal(decDownMonth.getYear(), 2024n))
        $(assert.equal(decDownMonth.getMonth(), 12n)) // December
        $(assert.equal(decDownMonth.getDayOfMonth(), 1n)) // 1st of December
    });

    test("Comparisons", $ => {
        const date1 = $.const(new Date("2024-01-01T00:00:00.000Z"), DateTimeType)
        const date2 = $.const(new Date("2024-01-01T00:00:00.000Z"), DateTimeType)
        const date3 = $.const(new Date("2024-01-02T00:00:00.000Z"), DateTimeType)
        const date4 = $.const(new Date("2023-12-31T23:59:59.999Z"), DateTimeType)

        // Equality tests
        $(assert.equal(date1, new Date("2024-01-01T00:00:00.000Z")))
        $(assert.notEqual(date1, new Date("2024-01-02T00:00:00.000Z")))

        // Ordering tests - later dates are greater
        $(assert.less(date4, date1)) // 2023-12-31 < 2024-01-01
        $(assert.less(date1, date3)) // 2024-01-01 < 2024-01-02
        $(assert.greater(date3, date1)) // 2024-01-02 > 2024-01-01
        $(assert.greater(date1, date4)) // 2024-01-01 > 2023-12-31

        // Less than or equal / Greater than or equal
        $(assert.lessEqual(date1, date2)) // same date
        $(assert.lessEqual(date1, date3)) // earlier date
        $(assert.greaterEqual(date1, date2)) // same date
        $(assert.greaterEqual(date3, date1)) // later date

        // Millisecond precision tests
        const ms1 = $.const(new Date("2024-01-01T00:00:00.000Z"), DateTimeType)
        const ms2 = $.const(new Date("2024-01-01T00:00:00.001Z"), DateTimeType)
        $(assert.less(ms1, ms2))
        $(assert.greater(ms2, ms1))

        // East.is, East.equal, East.less methods
        $(assert.equal(East.is(date1, date2), true)) // same timestamp
        $(assert.equal(East.is(date1, date3), false)) // different timestamp
        $(assert.equal(East.equal(date1, date2), true))
        $(assert.equal(East.equal(date1, date3), false))
        $(assert.equal(East.notEqual(date1, date3), true))
        $(assert.equal(East.less(date1, date3), true))
        $(assert.equal(East.less(date3, date1), false))
        $(assert.equal(East.lessEqual(date1, date2), true))
        $(assert.equal(East.lessEqual(date1, date3), true))
        $(assert.equal(East.greater(date3, date1), true))
        $(assert.equal(East.greaterEqual(date3, date1), true))

        // Instance method tests
        $(assert.equal(date1.equals(date2), true))
        $(assert.equal(date1.equals(date3), false))
        $(assert.equal(date1.notEquals(date3), true))
        $(assert.equal(date1.notEquals(date2), false))
        $(assert.equal(date1.lessThan(date3), true))
        $(assert.equal(date3.lessThan(date1), false))
        $(assert.equal(date1.lessThanOrEqual(date2), true))
        $(assert.equal(date1.lessThanOrEqual(date3), true))
        $(assert.equal(date3.greaterThan(date1), true))
        $(assert.equal(date1.greaterThan(date3), false))
        $(assert.equal(date3.greaterThanOrEqual(date1), true))
        $(assert.equal(date1.greaterThanOrEqual(date2), true))
    });

    test("Formatted printing", $ => {
        // Test basic ISO 8601 formats
        const date1 = $.const(new Date("2025-01-15T14:30:45.123Z"), DateTimeType);

        $(assert.equal(date1.printFormatted("YYYY-MM-DD"), "2025-01-15"));
        $(assert.equal(date1.printFormatted("YYYY-MM-DD HH:mm:ss"), "2025-01-15 14:30:45"));
        $(assert.equal(date1.printFormatted("YYYY-MM-DD HH:mm:ss.SSS"), "2025-01-15 14:30:45.123"));

        // Test 12-hour format with AM/PM
        const morning = $.const(new Date("2025-01-15T09:30:00.000Z"), DateTimeType);
        const afternoon = $.const(new Date("2025-01-15T14:30:00.000Z"), DateTimeType);

        $(assert.equal(morning.printFormatted("h:mm A"), "9:30 AM"));
        $(assert.equal(afternoon.printFormatted("h:mm A"), "2:30 PM"));
        $(assert.equal(morning.printFormatted("hh:mm a"), "09:30 am"));
        $(assert.equal(afternoon.printFormatted("hh:mm a"), "02:30 pm"));

        // Test month names
        const jan = $.const(new Date("2025-01-15T00:00:00.000Z"), DateTimeType);
        const dec = $.const(new Date("2025-12-25T00:00:00.000Z"), DateTimeType);

        $(assert.equal(jan.printFormatted("MMM"), "Jan"));
        $(assert.equal(jan.printFormatted("MMMM"), "January"));
        $(assert.equal(dec.printFormatted("MMMM D, YYYY"), "December 25, 2025"));

        // Test weekday names
        const wed = $.const(new Date("2025-01-15T00:00:00.000Z"), DateTimeType); // Wednesday

        $(assert.equal(wed.printFormatted("dd"), "We"));
        $(assert.equal(wed.printFormatted("ddd"), "Wed"));
        $(assert.equal(wed.printFormatted("dddd"), "Wednesday"));
        $(assert.equal(wed.printFormatted("dddd, MMMM D, YYYY"), "Wednesday, January 15, 2025"));

        // Test unpadded formats
        const date2 = $.const(new Date("2025-01-05T09:05:07.000Z"), DateTimeType);

        $(assert.equal(date2.printFormatted("M/D/YY"), "1/5/25"));
        $(assert.equal(date2.printFormatted("H:m:s"), "9:5:7"));

        // Test escaped literals
        $(assert.equal(date1.printFormatted("\\Y\\e\\a\\r: YYYY"), "Year: 2025"));
        $(assert.equal(date1.printFormatted("YYYY \\a\\t HH:mm"), "2025 at 14:30"));

        // Test complex real-world formats
        $(assert.equal(date1.printFormatted("ddd, MMM D, YYYY \\a\\t h:mm A"), "Wed, Jan 15, 2025 at 2:30 PM"));

        // Test midnight and noon edge cases
        const midnight = $.const(new Date("2025-01-15T00:00:00.000Z"), DateTimeType);
        const noon = $.const(new Date("2025-01-15T12:00:00.000Z"), DateTimeType);

        $(assert.equal(midnight.printFormatted("h A"), "12 AM"));
        $(assert.equal(noon.printFormatted("h A"), "12 PM"));
        $(assert.equal(midnight.printFormatted("HH:mm"), "00:00"));
        $(assert.equal(noon.printFormatted("HH:mm"), "12:00"));

        // Test year edge cases
        const y2000 = $.const(new Date("2000-01-01T00:00:00.000Z"), DateTimeType);
        const y2001 = $.const(new Date("2001-02-03T00:00:00.000Z"), DateTimeType);

        $(assert.equal(y2000.printFormatted("YYYY"), "2000"));
        $(assert.equal(y2000.printFormatted("YY"), "00"));
        $(assert.equal(y2001.printFormatted("YY"), "01"));

        // Test milliseconds padding
        const ms1 = $.const(new Date("2025-01-15T14:30:45.001Z"), DateTimeType);
        const ms50 = $.const(new Date("2025-01-15T14:30:45.050Z"), DateTimeType);

        $(assert.equal(ms1.printFormatted("SSS"), "001"));
        $(assert.equal(ms50.printFormatted("SSS"), "050"));

        // Test all weekdays
        const sun = $.const(new Date("2025-01-05T00:00:00.000Z"), DateTimeType); // Sunday
        const mon = $.const(new Date("2025-01-06T00:00:00.000Z"), DateTimeType); // Monday
        const tue = $.const(new Date("2025-01-07T00:00:00.000Z"), DateTimeType); // Tuesday
        const thu = $.const(new Date("2025-01-09T00:00:00.000Z"), DateTimeType); // Thursday
        const fri = $.const(new Date("2025-01-10T00:00:00.000Z"), DateTimeType); // Friday
        const sat = $.const(new Date("2025-01-11T00:00:00.000Z"), DateTimeType); // Saturday

        $(assert.equal(sun.printFormatted("dddd"), "Sunday"));
        $(assert.equal(mon.printFormatted("dddd"), "Monday"));
        $(assert.equal(tue.printFormatted("dddd"), "Tuesday"));
        $(assert.equal(wed.printFormatted("dddd"), "Wednesday"));
        $(assert.equal(thu.printFormatted("dddd"), "Thursday"));
        $(assert.equal(fri.printFormatted("dddd"), "Friday"));
        $(assert.equal(sat.printFormatted("dddd"), "Saturday"));

        // Test leap year
        const leapDay = $.const(new Date("2024-02-29T12:00:00.000Z"), DateTimeType);

        $(assert.equal(leapDay.printFormatted("YYYY-MM-DD"), "2024-02-29"));
        $(assert.equal(leapDay.printFormatted("MMMM D, YYYY"), "February 29, 2024"));

        // Test with constructed date
        const constructed = $.let(East.DateTime.fromComponents(2025n, 3n, 15n, 10n, 30n, 45n, 678n));

        $(assert.equal(constructed.printFormatted("YYYY-MM-DD HH:mm:ss.SSS"), "2025-03-15 10:30:45.678"));
    });

    test("Formatted parsing", $ => {
        // Test basic ISO 8601 formats
        const parsed1 = $.let(East.DateTime.parseFormatted("2025-01-15", "YYYY-MM-DD"));
        $(assert.equal(parsed1.getYear(), 2025n));
        $(assert.equal(parsed1.getMonth(), 1n));
        $(assert.equal(parsed1.getDayOfMonth(), 15n));
        $(assert.equal(parsed1.getHour(), 0n)); // Defaults to midnight
        $(assert.equal(parsed1.getMinute(), 0n));
        $(assert.equal(parsed1.getSecond(), 0n));

        const parsed2 = $.let(East.DateTime.parseFormatted("2025-01-15 14:30:45", "YYYY-MM-DD HH:mm:ss"));
        $(assert.equal(parsed2.getYear(), 2025n));
        $(assert.equal(parsed2.getMonth(), 1n));
        $(assert.equal(parsed2.getDayOfMonth(), 15n));
        $(assert.equal(parsed2.getHour(), 14n));
        $(assert.equal(parsed2.getMinute(), 30n));
        $(assert.equal(parsed2.getSecond(), 45n));

        const parsed3 = $.let(East.DateTime.parseFormatted("2025-01-15 14:30:45.123", "YYYY-MM-DD HH:mm:ss.SSS"));
        $(assert.equal(parsed3.getMillisecond(), 123n));

        // Test 12-hour format with AM/PM  - this requires full date
        const parsedAM = $.let(East.DateTime.parseFormatted("2025-01-15 9:30 AM", "YYYY-MM-DD h:mm A"));
        $(assert.equal(parsedAM.getHour(), 9n));
        $(assert.equal(parsedAM.getMinute(), 30n));

        const parsedPM = $.let(East.DateTime.parseFormatted("2025-01-15 2:30 PM", "YYYY-MM-DD h:mm A"));
        $(assert.equal(parsedPM.getHour(), 14n));
        $(assert.equal(parsedPM.getMinute(), 30n));

        // Test midnight and noon edge cases
        const parsedMidnight = $.let(East.DateTime.parseFormatted("2025-01-15 12 AM", "YYYY-MM-DD h A"));
        $(assert.equal(parsedMidnight.getHour(), 0n)); // 12 AM = midnight

        const parsedNoon = $.let(East.DateTime.parseFormatted("2025-01-15 12 PM", "YYYY-MM-DD h A"));
        $(assert.equal(parsedNoon.getHour(), 12n)); // 12 PM = noon

        // Test month names (full)
        const parsedMonthFull = $.let(East.DateTime.parseFormatted("January 15, 2025", "MMMM D, YYYY"));
        $(assert.equal(parsedMonthFull.getYear(), 2025n));
        $(assert.equal(parsedMonthFull.getMonth(), 1n));
        $(assert.equal(parsedMonthFull.getDayOfMonth(), 15n));

        // Test month names (short)
        const parsedMonthShort = $.let(East.DateTime.parseFormatted("Jan 15, 2025", "MMM D, YYYY"));
        $(assert.equal(parsedMonthShort.getMonth(), 1n));

        const parsedDec = $.let(East.DateTime.parseFormatted("December 25, 2025", "MMMM D, YYYY"));
        $(assert.equal(parsedDec.getMonth(), 12n));
        $(assert.equal(parsedDec.getDayOfMonth(), 25n));

        // Test month names case insensitive
        const parsedLowercase = $.let(East.DateTime.parseFormatted("january 15, 2025", "MMMM D, YYYY"));
        $(assert.equal(parsedLowercase.getMonth(), 1n));

        // Test weekday names (consumed but not validated)
        const parsedWeekday = $.let(East.DateTime.parseFormatted("Wednesday, January 15, 2025", "dddd, MMMM D, YYYY"));
        $(assert.equal(parsedWeekday.getYear(), 2025n));
        $(assert.equal(parsedWeekday.getMonth(), 1n));
        $(assert.equal(parsedWeekday.getDayOfMonth(), 15n));

        const parsedShortWeekday = $.let(East.DateTime.parseFormatted("Wed, Jan 15, 2025", "ddd, MMM D, YYYY"));
        $(assert.equal(parsedShortWeekday.getDayOfMonth(), 15n));

        // Test unpadded formats
        const parsedUnpadded = $.let(East.DateTime.parseFormatted("1/5/25", "M/D/YY"));
        $(assert.equal(parsedUnpadded.getYear(), 2025n));
        $(assert.equal(parsedUnpadded.getMonth(), 1n));
        $(assert.equal(parsedUnpadded.getDayOfMonth(), 5n));

        const parsedDoubleDigit = $.let(East.DateTime.parseFormatted("12/25/25", "M/D/YY"));
        $(assert.equal(parsedDoubleDigit.getMonth(), 12n));
        $(assert.equal(parsedDoubleDigit.getDayOfMonth(), 25n));

        // Test unpadded time components
        const parsedTime = $.let(East.DateTime.parseFormatted("9:5:7", "H:m:s"));
        $(assert.equal(parsedTime.getHour(), 9n));
        $(assert.equal(parsedTime.getMinute(), 5n));
        $(assert.equal(parsedTime.getSecond(), 7n));

        // Test year-only format (defaults to January 1st)
        const yearOnly = $.let(East.DateTime.parseFormatted("2025", "YYYY"));
        $(assert.equal(yearOnly.getYear(), 2025n));
        $(assert.equal(yearOnly.getMonth(), 1n));
        $(assert.equal(yearOnly.getDayOfMonth(), 1n));

        // Test with escaped literals
        const parsedLiteral = $.let(East.DateTime.parseFormatted("2025-01-15 at 14:30", "YYYY-MM-DD \\a\\t HH:mm"));
        $(assert.equal(parsedLiteral.getYear(), 2025n));
        $(assert.equal(parsedLiteral.getMonth(), 1n));
        $(assert.equal(parsedLiteral.getDayOfMonth(), 15n));
        $(assert.equal(parsedLiteral.getHour(), 14n));
        $(assert.equal(parsedLiteral.getMinute(), 30n));

        // Test complex real-world format
        const parsedComplex = $.let(East.DateTime.parseFormatted("Wed, Jan 15, 2025 at 2:30 PM", "ddd, MMM D, YYYY \\a\\t h:mm A"));
        $(assert.equal(parsedComplex.getYear(), 2025n));
        $(assert.equal(parsedComplex.getMonth(), 1n));
        $(assert.equal(parsedComplex.getDayOfMonth(), 15n));
        $(assert.equal(parsedComplex.getHour(), 14n));
        $(assert.equal(parsedComplex.getMinute(), 30n));

        // Test leap year date
        const parsedLeap = $.let(East.DateTime.parseFormatted("2024-02-29", "YYYY-MM-DD"));
        $(assert.equal(parsedLeap.getYear(), 2024n));
        $(assert.equal(parsedLeap.getMonth(), 2n));
        $(assert.equal(parsedLeap.getDayOfMonth(), 29n));

        // Test round-trip: parse and format
        const original = $.const(new Date("2025-01-15T14:30:45.123Z"), DateTimeType);
        const formatted = $.let(original.printFormatted("YYYY-MM-DD HH:mm:ss.SSS"));
        const roundTrip = $.let(East.DateTime.parseFormatted(formatted, "YYYY-MM-DD HH:mm:ss.SSS"));
        $(assert.equal(roundTrip, original));

        // Test all months
        const parsedJan = $.let(East.DateTime.parseFormatted("Jan 2025", "MMM YYYY"));
        $(assert.equal(parsedJan.getMonth(), 1n));
        const parsedFeb = $.let(East.DateTime.parseFormatted("Feb 2025", "MMM YYYY"));
        $(assert.equal(parsedFeb.getMonth(), 2n));
        const parsedMar = $.let(East.DateTime.parseFormatted("Mar 2025", "MMM YYYY"));
        $(assert.equal(parsedMar.getMonth(), 3n));
        const parsedApr = $.let(East.DateTime.parseFormatted("Apr 2025", "MMM YYYY"));
        $(assert.equal(parsedApr.getMonth(), 4n));
        const parsedMay = $.let(East.DateTime.parseFormatted("May 2025", "MMM YYYY"));
        $(assert.equal(parsedMay.getMonth(), 5n));
        const parsedJun = $.let(East.DateTime.parseFormatted("Jun 2025", "MMM YYYY"));
        $(assert.equal(parsedJun.getMonth(), 6n));
        const parsedJul = $.let(East.DateTime.parseFormatted("Jul 2025", "MMM YYYY"));
        $(assert.equal(parsedJul.getMonth(), 7n));
        const parsedAug = $.let(East.DateTime.parseFormatted("Aug 2025", "MMM YYYY"));
        $(assert.equal(parsedAug.getMonth(), 8n));
        const parsedSep = $.let(East.DateTime.parseFormatted("Sep 2025", "MMM YYYY"));
        $(assert.equal(parsedSep.getMonth(), 9n));
        const parsedOct = $.let(East.DateTime.parseFormatted("Oct 2025", "MMM YYYY"));
        $(assert.equal(parsedOct.getMonth(), 10n));
        const parsedNov = $.let(East.DateTime.parseFormatted("Nov 2025", "MMM YYYY"));
        $(assert.equal(parsedNov.getMonth(), 11n));
        const parsedDecMonth = $.let(East.DateTime.parseFormatted("Dec 2025", "MMM YYYY"));
        $(assert.equal(parsedDecMonth.getMonth(), 12n));

        // Test lowercase am/pm
        const parsedLowerAM = $.let(East.DateTime.parseFormatted("2025-01-15 9:30 am", "YYYY-MM-DD h:mm a"));
        $(assert.equal(parsedLowerAM.getHour(), 9n));
        const parsedLowerPM = $.let(East.DateTime.parseFormatted("2025-01-15 2:30 pm", "YYYY-MM-DD h:mm a"));
        $(assert.equal(parsedLowerPM.getHour(), 14n));
    });

    test("Formatted parsing errors", $ => {
        // Test invalid date (Feb 31)
        $(assert.throws(
            East.DateTime.parseFormatted("2025-02-31", "YYYY-MM-DD"),
            /Invalid date/
        ));

        // Test invalid leap year date (Feb 29 in non-leap year)
        $(assert.throws(
            East.DateTime.parseFormatted("2025-02-29", "YYYY-MM-DD"),
            /Invalid date/
        ));

        // Test month out of range
        $(assert.throws(
            East.DateTime.parseFormatted("2025-13-15", "YYYY-MM-DD"),
            /out of range/
        ));

        // Test day out of range
        $(assert.throws(
            East.DateTime.parseFormatted("2025-01-32", "YYYY-MM-DD"),
            /out of range/
        ));

        // Test hour 24-hour out of range
        $(assert.throws(
            East.DateTime.parseFormatted("24:00", "HH:mm"),
            /out of range/
        ));

        // Test hour 12-hour out of range
        $(assert.throws(
            East.DateTime.parseFormatted("13:00 PM", "hh:mm A"),
            /out of range/
        ));

        // Test minute out of range
        $(assert.throws(
            East.DateTime.parseFormatted("14:60", "HH:mm"),
            /out of range/
        ));

        // Test second out of range
        $(assert.throws(
            East.DateTime.parseFormatted("14:30:60", "HH:mm:ss"),
            /out of range/
        ));

        // Test literal mismatch
        $(assert.throws(
            East.DateTime.parseFormatted("2025/01/15", "YYYY-MM-DD"),
            /Expected literal/
        ));

        // Test trailing characters
        $(assert.throws(
            East.DateTime.parseFormatted("2025-01-15 extra", "YYYY-MM-DD"),
            /trailing characters/
        ));

        // Test unexpected end of input
        $(assert.throws(
            East.DateTime.parseFormatted("2025-01-15", "YYYY-MM-DD HH:mm:ss"),
            /(Unexpected end of input|Expected literal)/
        ));

        // Test expected 4-digit year
        $(assert.throws(
            East.DateTime.parseFormatted("25-01-15", "YYYY-MM-DD"),
            /4-digit year/
        ));

        // Test expected 2-digit month
        $(assert.throws(
            East.DateTime.parseFormatted("2025-1-15", "YYYY-MM-DD"),
            /2-digit month/
        ));
    });

    test("Comparison method aliases", $ => {
        const d1 = East.value(new Date("2024-01-01T00:00:00.000Z"));
        const d2 = East.value(new Date("2024-06-15T12:30:00.000Z"));

        // Test short aliases (eq, ne, gt, lt, gte, lte, ge, le)
        $(assert.equal(d1.eq(new Date("2024-01-01T00:00:00.000Z")), true));
        $(assert.equal(d1.eq(new Date("2024-06-15T12:30:00.000Z")), false));
        $(assert.equal(d1.ne(new Date("2024-06-15T12:30:00.000Z")), true));
        $(assert.equal(d1.ne(new Date("2024-01-01T00:00:00.000Z")), false));
        $(assert.equal(d2.gt(new Date("2024-01-01T00:00:00.000Z")), true));
        $(assert.equal(d1.gt(new Date("2024-06-15T12:30:00.000Z")), false));
        $(assert.equal(d1.lt(new Date("2024-06-15T12:30:00.000Z")), true));
        $(assert.equal(d2.lt(new Date("2024-01-01T00:00:00.000Z")), false));
        $(assert.equal(d1.gte(new Date("2024-01-01T00:00:00.000Z")), true));
        $(assert.equal(d2.gte(new Date("2024-01-01T00:00:00.000Z")), true));
        $(assert.equal(d1.lte(new Date("2024-06-15T12:30:00.000Z")), true));
        $(assert.equal(d2.ge(new Date("2024-01-01T00:00:00.000Z")), true));
        $(assert.equal(d1.le(new Date("2024-06-15T12:30:00.000Z")), true));

        // Test medium aliases (equal, notEqual, greater, less, greaterEqual, lessEqual)
        $(assert.equal(d1.equal(new Date("2024-01-01T00:00:00.000Z")), true));
        $(assert.equal(d1.notEqual(new Date("2024-06-15T12:30:00.000Z")), true));
        $(assert.equal(d2.greater(new Date("2024-01-01T00:00:00.000Z")), true));
        $(assert.equal(d1.less(new Date("2024-06-15T12:30:00.000Z")), true));
        $(assert.equal(d1.greaterEqual(new Date("2024-01-01T00:00:00.000Z")), true));
        $(assert.equal(d1.lessEqual(new Date("2024-06-15T12:30:00.000Z")), true));
    });
});
