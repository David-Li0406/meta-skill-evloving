/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, IntegerType } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Integer", (test) => {
    test("Arithmetic", $ => {
        $(assert.equal(East.value(10n).negate(), -10n));
        $(assert.equal(East.value(10n).add(5n), 15n));
        $(assert.equal(East.value(10n).subtract(5n), 5n));
        $(assert.equal(East.value(10n).multiply(5n), 50n));
        $(assert.equal(East.value(10n).divide(5n), 2n));
        $(assert.equal(East.value(10n).remainder(5n), 0n));
        $(assert.equal(East.value(10n).pow(5n), 100_000n));
    });

    test("Printing", $ => {
        $(assert.equal(East.print(East.value(0n)), "0"));
        $(assert.equal(East.print(East.value(1n)), "1"));
        $(assert.equal(East.print(East.value(1234n)), "1234"));
        $(assert.equal(East.print(East.value(9223372036854775807n)), "9223372036854775807"));
        $(assert.equal(East.print(East.value(-1n)), "-1"));
        $(assert.equal(East.print(East.value(-1234n)), "-1234"));
        $(assert.equal(East.print(East.value(-9223372036854775808n)), "-9223372036854775808"));

        const printCommaSeperated = $.let(East.Integer.printCommaSeperated);
        $(assert.equal(printCommaSeperated(0n), "0"));
        $(assert.equal(printCommaSeperated(1n), "1"));
        $(assert.equal(printCommaSeperated(12n), "12"));
        $(assert.equal(printCommaSeperated(123n), "123"));
        $(assert.equal(printCommaSeperated(1234n), "1,234"));
        $(assert.equal(printCommaSeperated(12345n), "12,345"));
        $(assert.equal(printCommaSeperated(123456n), "123,456"));
        $(assert.equal(printCommaSeperated(1234567n), "1,234,567"));
        $(assert.equal(printCommaSeperated(12345678n), "12,345,678"));
        $(assert.equal(printCommaSeperated(123456789n), "123,456,789"));
        $(assert.equal(printCommaSeperated(9223372036854775807n), "9,223,372,036,854,775,807"));
        $(assert.equal(printCommaSeperated(-1n), "-1"));
        $(assert.equal(printCommaSeperated(-1n), "-1"));
        $(assert.equal(printCommaSeperated(-12n), "-12"));
        $(assert.equal(printCommaSeperated(-123n), "-123"));
        $(assert.equal(printCommaSeperated(-1234n), "-1,234"));
        $(assert.equal(printCommaSeperated(-12345n), "-12,345"));
        $(assert.equal(printCommaSeperated(-123456n), "-123,456"));
        $(assert.equal(printCommaSeperated(-1234567n), "-1,234,567"));
        $(assert.equal(printCommaSeperated(-12345678n), "-12,345,678"));
        $(assert.equal(printCommaSeperated(-123456789n), "-123,456,789"));
        $(assert.equal(printCommaSeperated(-9223372036854775807n), "-9,223,372,036,854,775,807"));
        $(assert.equal(printCommaSeperated(-9223372036854775808n), "-9,223,372,036,854,775,808"));

        const printCompact = $.let(East.Integer.printCompact);
        $(assert.equal(printCompact(0n), "0"));
        $(assert.equal(printCompact(1n), "1"));
        $(assert.equal(printCompact(12n), "12"));
        $(assert.equal(printCompact(123n), "123"));
        $(assert.equal(printCompact(1034n), "1.03K"));
        $(assert.equal(printCompact(1234n), "1.23K"));
        $(assert.equal(printCompact(12345n), "12.3K"));
        $(assert.equal(printCompact(123456n), "123K"));
        $(assert.equal(printCompact(1234567n), "1.23M"));
        $(assert.equal(printCompact(12345678n), "12.3M"));
        $(assert.equal(printCompact(123456789n), "123M"));
        $(assert.equal(printCompact(1234567890n), "1.23B"));
        $(assert.equal(printCompact(12345678901n), "12.3B"));
        $(assert.equal(printCompact(123456789012n), "123B"));
        $(assert.equal(printCompact(1234567890123n), "1.23T"));
        $(assert.equal(printCompact(12345678901234n), "12.3T"));
        $(assert.equal(printCompact(123456789012345n), "123T"));
        $(assert.equal(printCompact(1234567890123456n), "1.23Q"));
        $(assert.equal(printCompact(12345678901234567n), "12.3Q"));
        $(assert.equal(printCompact(123456789012345678n), "123Q"));
        $(assert.equal(printCompact(1234567890123456789n), "1.23Qi"));
        $(assert.equal(printCompact(9223372036854775807n), "9.22Qi"));
        $(assert.equal(printCompact(-1n), "-1"));
        $(assert.equal(printCompact(-12n), "-12"));
        $(assert.equal(printCompact(-123n), "-123"));
        $(assert.equal(printCompact(-1034n), "-1.03K"));
        $(assert.equal(printCompact(-1234n), "-1.23K"));
        $(assert.equal(printCompact(-12345n), "-12.3K"));
        $(assert.equal(printCompact(-123456n), "-123K"));
        $(assert.equal(printCompact(-1234567n), "-1.23M"));
        $(assert.equal(printCompact(-12345678n), "-12.3M"));
        $(assert.equal(printCompact(-123456789n), "-123M"));
        $(assert.equal(printCompact(-1234567890n), "-1.23B"));
        $(assert.equal(printCompact(-12345678901n), "-12.3B"));
        $(assert.equal(printCompact(-123456789012n), "-123B"));
        $(assert.equal(printCompact(-1234567890123n), "-1.23T"));
        $(assert.equal(printCompact(-12345678901234n), "-12.3T"));
        $(assert.equal(printCompact(-123456789012345n), "-123T"));
        $(assert.equal(printCompact(-1234567890123456n), "-1.23Q"));
        $(assert.equal(printCompact(-12345678901234567n), "-12.3Q"));
        $(assert.equal(printCompact(-123456789012345678n), "-123Q"));
        $(assert.equal(printCompact(-1234567890123456789n), "-1.23Qi"));
        $(assert.equal(printCompact(-9223372036854775807n), "-9.22Qi"));
        $(assert.equal(printCompact(-9223372036854775808n), "-9.22Qi"));

        const printCompactSI = $.let(East.Integer.printCompactSI);
        $(assert.equal(printCompactSI(0n), "0"));
        $(assert.equal(printCompactSI(1n), "1"));
        $(assert.equal(printCompactSI(12n), "12"));
        $(assert.equal(printCompactSI(123n), "123"));
        $(assert.equal(printCompactSI(1034n), "1.03k"));
        $(assert.equal(printCompactSI(1234n), "1.23k"));
        $(assert.equal(printCompactSI(12345n), "12.3k"));
        $(assert.equal(printCompactSI(123456n), "123k"));
        $(assert.equal(printCompactSI(1234567n), "1.23M"));
        $(assert.equal(printCompactSI(12345678n), "12.3M"));
        $(assert.equal(printCompactSI(123456789n), "123M"));
        $(assert.equal(printCompactSI(1234567890n), "1.23G"));
        $(assert.equal(printCompactSI(12345678901n), "12.3G"));
        $(assert.equal(printCompactSI(123456789012n), "123G"));
        $(assert.equal(printCompactSI(1234567890123n), "1.23T"));
        $(assert.equal(printCompactSI(12345678901234n), "12.3T"));
        $(assert.equal(printCompactSI(123456789012345n), "123T"));
        $(assert.equal(printCompactSI(1234567890123456n), "1.23P"));
        $(assert.equal(printCompactSI(12345678901234567n), "12.3P"));
        $(assert.equal(printCompactSI(123456789012345678n), "123P"));
        $(assert.equal(printCompactSI(1234567890123456789n), "1.23E"));
        $(assert.equal(printCompactSI(9223372036854775807n), "9.22E"));
        $(assert.equal(printCompactSI(-1n), "-1"));
        $(assert.equal(printCompactSI(-12n), "-12"));
        $(assert.equal(printCompactSI(-123n), "-123"));
        $(assert.equal(printCompactSI(-1034n), "-1.03k"));
        $(assert.equal(printCompactSI(-1234n), "-1.23k"));
        $(assert.equal(printCompactSI(-12345n), "-12.3k"));
        $(assert.equal(printCompactSI(-123456n), "-123k"));
        $(assert.equal(printCompactSI(-1234567n), "-1.23M"));
        $(assert.equal(printCompactSI(-12345678n), "-12.3M"));
        $(assert.equal(printCompactSI(-123456789n), "-123M"));
        $(assert.equal(printCompactSI(-1234567890n), "-1.23G"));
        $(assert.equal(printCompactSI(-12345678901n), "-12.3G"));
        $(assert.equal(printCompactSI(-123456789012n), "-123G"));
        $(assert.equal(printCompactSI(-1234567890123n), "-1.23T"));
        $(assert.equal(printCompactSI(-12345678901234n), "-12.3T"));
        $(assert.equal(printCompactSI(-123456789012345n), "-123T"));
        $(assert.equal(printCompactSI(-1234567890123456n), "-1.23P"));
        $(assert.equal(printCompactSI(-12345678901234567n), "-12.3P"));
        $(assert.equal(printCompactSI(-123456789012345678n), "-123P"));
        $(assert.equal(printCompactSI(-1234567890123456789n), "-1.23E"));
        $(assert.equal(printCompactSI(-9223372036854775807n), "-9.22E"));
        $(assert.equal(printCompactSI(-9223372036854775808n), "-9.22E"));

        const printCompactComputing = $.let(East.Integer.printCompactComputing);
        $(assert.equal(printCompactComputing(0n), "0"));
        $(assert.equal(printCompactComputing(1n), "1"));
        $(assert.equal(printCompactComputing(12n), "12"));
        $(assert.equal(printCompactComputing(123n), "123"));
        $(assert.equal(printCompactComputing(1034n), "1.00ki"));
        $(assert.equal(printCompactComputing(1234n), "1.20ki"));
        $(assert.equal(printCompactComputing(12345n), "12.0ki"));
        $(assert.equal(printCompactComputing(123456n), "120ki"));
        $(assert.equal(printCompactComputing(1234567n), "1.17Mi"));
        $(assert.equal(printCompactComputing(12345678n), "11.7Mi"));
        $(assert.equal(printCompactComputing(123456789n), "117Mi"));
        $(assert.equal(printCompactComputing(1234567890n), "1.14Gi"));
        $(assert.equal(printCompactComputing(12345678901n), "11.4Gi"));
        $(assert.equal(printCompactComputing(123456789012n), "114Gi"));
        $(assert.equal(printCompactComputing(1234567890123n), "1.12Ti"));
        $(assert.equal(printCompactComputing(12345678901234n), "11.2Ti"));
        $(assert.equal(printCompactComputing(123456789012345n), "112Ti"));
        $(assert.equal(printCompactComputing(1234567890123456n), "1.09Pi"));
        $(assert.equal(printCompactComputing(12345678901234567n), "10.9Pi"));
        $(assert.equal(printCompactComputing(123456789012345678n), "109Pi"));
        $(assert.equal(printCompactComputing(1234567890123456789n), "1.07Ei"));
        $(assert.equal(printCompactComputing(9223372036854775807n), "7.99Ei"));
        $(assert.equal(printCompactComputing(-1n), "-1"));
        $(assert.equal(printCompactComputing(-12n), "-12"));
        $(assert.equal(printCompactComputing(-123n), "-123"));
        $(assert.equal(printCompactComputing(-1034n), "-1.00ki"));
        $(assert.equal(printCompactComputing(-1234n), "-1.20ki"));
        $(assert.equal(printCompactComputing(-12345n), "-12.0ki"));
        $(assert.equal(printCompactComputing(-123456n), "-120ki"));
        $(assert.equal(printCompactComputing(-1234567n), "-1.17Mi"));
        $(assert.equal(printCompactComputing(-12345678n), "-11.7Mi"));
        $(assert.equal(printCompactComputing(-123456789n), "-117Mi"));
        $(assert.equal(printCompactComputing(-1234567890n), "-1.14Gi"));
        $(assert.equal(printCompactComputing(-12345678901n), "-11.4Gi"));
        $(assert.equal(printCompactComputing(-123456789012n), "-114Gi"));
        $(assert.equal(printCompactComputing(-1234567890123n), "-1.12Ti"));
        $(assert.equal(printCompactComputing(-12345678901234n), "-11.2Ti"));
        $(assert.equal(printCompactComputing(-123456789012345n), "-112Ti"));
        $(assert.equal(printCompactComputing(-1234567890123456n), "-1.09Pi"));
        $(assert.equal(printCompactComputing(-12345678901234567n), "-10.9Pi"));
        $(assert.equal(printCompactComputing(-123456789012345678n), "-109Pi"));
        $(assert.equal(printCompactComputing(-1234567890123456789n), "-1.07Ei"));
        $(assert.equal(printCompactComputing(-9223372036854775807n), "-7.99Ei"));
        $(assert.equal(printCompactComputing(-9223372036854775808n), "-7.99Ei"));

    });

    test("Comparisons", $ => {
        $(assert.equal(East.equal(East.value(10n), 10n), true));
        $(assert.equal(East.equal(East.value(10n), 5n), false));
        $(assert.equal(East.equal(East.value(-5n), -5n), true));

        $(assert.equal(East.less(East.value(5n), 10n), true));
        $(assert.equal(East.less(East.value(10n), 5n), false));
        $(assert.equal(East.less(East.value(10n), 10n), false));
        $(assert.equal(East.less(East.value(-10n), -5n), true));

        $(assert.equal(East.lessEqual(East.value(5n), 10n), true));
        $(assert.equal(East.lessEqual(East.value(10n), 5n), false));
        $(assert.equal(East.lessEqual(East.value(10n), 10n), true));

        $(assert.equal(East.greater(East.value(10n), 5n), true));
        $(assert.equal(East.greater(East.value(5n), 10n), false));
        $(assert.equal(East.greater(East.value(10n), 10n), false));
        $(assert.equal(East.greater(East.value(-5n), -10n), true));

        $(assert.equal(East.greaterEqual(East.value(10n), 5n), true));
        $(assert.equal(East.greaterEqual(East.value(5n), 10n), false));
        $(assert.equal(East.greaterEqual(East.value(10n), 10n), true));

        // Instance method tests
        $(assert.equal(East.value(10n).equals(10n), true));
        $(assert.equal(East.value(10n).equals(5n), false));
        $(assert.equal(East.value(10n).notEquals(5n), true));
        $(assert.equal(East.value(10n).notEquals(10n), false));
        $(assert.equal(East.value(5n).lessThan(10n), true));
        $(assert.equal(East.value(10n).lessThan(5n), false));
        $(assert.equal(East.value(5n).lessThanOrEqual(10n), true));
        $(assert.equal(East.value(10n).lessThanOrEqual(10n), true));
        $(assert.equal(East.value(10n).greaterThan(5n), true));
        $(assert.equal(East.value(5n).greaterThan(10n), false));
        $(assert.equal(East.value(10n).greaterThanOrEqual(5n), true));
        $(assert.equal(East.value(10n).greaterThanOrEqual(10n), true));
    });

    test("Parsing", $ => {
        $(assert.equal(East.value("0").parse(IntegerType), 0n));
        $(assert.equal(East.value("123").parse(IntegerType), 123n));
        $(assert.equal(East.value("-456").parse(IntegerType), -456n));
        $(assert.equal(East.value("9223372036854775807").parse(IntegerType), 9223372036854775807n));

        $(assert.throws(East.value("abc").parse(IntegerType)));
        $(assert.throws(East.value("12.34").parse(IntegerType)));
        $(assert.throws(East.value("").parse(IntegerType)));
        $(assert.throws(East.value("123abc").parse(IntegerType)));
    });

    test("Mathematical functions", $ => {
        // abs() tests
        $(assert.equal(East.value(5n).abs(), 5n));
        $(assert.equal(East.value(-5n).abs(), 5n));
        $(assert.equal(East.value(0n).abs(), 0n));

        // sign() tests
        $(assert.equal(East.value(5n).sign(), 1n));
        $(assert.equal(East.value(-5n).sign(), -1n));
        $(assert.equal(East.value(0n).sign(), 0n));

        // log() tests
        $(assert.equal(East.value(1n).log(10n), 0n));
        $(assert.equal(East.value(10n).log(10n), 1n));
        $(assert.equal(East.value(100n).log(10n), 2n));
        $(assert.equal(East.value(1000n).log(10n), 3n));
        $(assert.equal(East.value(8n).log(2n), 3n));
        $(assert.equal(East.value(16n).log(2n), 4n));
        $(assert.equal(East.value(0n).log(10n), 0n)); // Special case: log(0) = 0
        $(assert.equal(East.value(10n).log(1n), 0n)); // Invalid base
    });

    test("Stdlib functions", $ => {
        const roundNearest = $.let(East.Integer.roundNearest);
        $(assert.equal(roundNearest(123n, 10n), 120n)); // Round down
        $(assert.equal(roundNearest(127n, 10n), 130n)); // Round up
        $(assert.equal(roundNearest(125n, 10n), 130n)); // Round up at midpoint
        $(assert.equal(roundNearest(120n, 10n), 120n)); // Already multiple
        $(assert.equal(roundNearest(0n, 10n), 0n));
        $(assert.equal(roundNearest(123n, 0n), 123n)); // Step = 0
        $(assert.equal(roundNearest(-123n, 10n), -120n)); // Negative numbers
        $(assert.equal(roundNearest(-127n, 10n), -130n)); // Negative numbers

        const roundUp = $.let(East.Integer.roundUp);
        $(assert.equal(roundUp(123n, 10n), 130n)); // Round up
        $(assert.equal(roundUp(127n, 10n), 130n)); // Round up
        $(assert.equal(roundUp(120n, 10n), 120n)); // Already multiple
        $(assert.equal(roundUp(0n, 10n), 0n));
        $(assert.equal(roundUp(-123n, 10n), -120n)); // Negative: towards zero
        $(assert.equal(roundUp(-127n, 10n), -120n)); // Negative: towards zero

        const roundDown = $.let(East.Integer.roundDown);
        $(assert.equal(roundDown(123n, 10n), 120n)); // Round down
        $(assert.equal(roundDown(127n, 10n), 120n)); // Round down
        $(assert.equal(roundDown(120n, 10n), 120n)); // Already multiple
        $(assert.equal(roundDown(0n, 10n), 0n));
        $(assert.equal(roundDown(-123n, 10n), -130n)); // Negative: away from zero
        $(assert.equal(roundDown(-127n, 10n), -130n)); // Negative: away from zero

        const roundTruncate = $.let(East.Integer.roundTruncate);
        $(assert.equal(roundTruncate(123n, 10n), 120n)); // Towards zero
        $(assert.equal(roundTruncate(127n, 10n), 120n)); // Towards zero
        $(assert.equal(roundTruncate(120n, 10n), 120n)); // Already multiple
        $(assert.equal(roundTruncate(0n, 10n), 0n));
        $(assert.equal(roundTruncate(-123n, 10n), -120n)); // Towards zero
        $(assert.equal(roundTruncate(-127n, 10n), -120n)); // Towards zero

        const digitCount = $.let(East.Integer.digitCount);
        $(assert.equal(digitCount(0n), 1n));
        $(assert.equal(digitCount(5n), 1n));
        $(assert.equal(digitCount(10n), 2n));
        $(assert.equal(digitCount(123n), 3n));
        $(assert.equal(digitCount(-123n), 3n)); // Excludes sign
        $(assert.equal(digitCount(9999n), 4n));

        const printOrdinal = $.let(East.Integer.printOrdinal);
        $(assert.equal(printOrdinal(1n), "1st"));
        $(assert.equal(printOrdinal(2n), "2nd"));
        $(assert.equal(printOrdinal(3n), "3rd"));
        $(assert.equal(printOrdinal(4n), "4th"));
        $(assert.equal(printOrdinal(11n), "11th")); // Special case
        $(assert.equal(printOrdinal(12n), "12th")); // Special case
        $(assert.equal(printOrdinal(13n), "13th")); // Special case
        $(assert.equal(printOrdinal(21n), "21st"));
        $(assert.equal(printOrdinal(22n), "22nd"));
        $(assert.equal(printOrdinal(23n), "23rd"));
        $(assert.equal(printOrdinal(101n), "101st"));
        $(assert.equal(printOrdinal(-1n), "-1st"));

        const printPercentage = $.let(East.Integer.printPercentage);
        $(assert.equal(printPercentage(0n), "0%"));
        $(assert.equal(printPercentage(25n), "25%"));
        $(assert.equal(printPercentage(50n), "50%"));
        $(assert.equal(printPercentage(100n), "100%"));
        $(assert.equal(printPercentage(-25n), "-25%"));
        $(assert.equal(printPercentage(1234n), "1234%"));

        
        $(assert.equal(East.Integer.printCurrency(1234n), "$1,234"));
        $(assert.equal(East.Integer.printCurrency(1234n), "$1,234"));
        $(assert.equal(East.Integer.printCurrency(-12345n), "-$12,345"));
        $(assert.equal(East.Integer.printCurrency(0n), "$0"));
    });

    test("Min, Max, and Clamp functions", $ => {
        // East.min tests
        $(assert.equal(East.min(East.value(5n), 10n), 5n));
        $(assert.equal(East.min(East.value(15n), 10n), 10n));
        $(assert.equal(East.min(East.value(-5n), -10n), -10n));
        $(assert.equal(East.min(East.value(-15n), -10n), -15n));
        $(assert.equal(East.min(East.value(0n), 0n), 0n));
        $(assert.equal(East.min(East.value(42n), 42n), 42n)); // Equal values

        // East.max tests
        $(assert.equal(East.max(East.value(5n), 10n), 10n));
        $(assert.equal(East.max(East.value(15n), 10n), 15n));
        $(assert.equal(East.max(East.value(-5n), -10n), -5n));
        $(assert.equal(East.max(East.value(-15n), -10n), -10n));
        $(assert.equal(East.max(East.value(0n), 0n), 0n));
        $(assert.equal(East.max(East.value(42n), 42n), 42n)); // Equal values

        // East.clamp tests
        $(assert.equal(East.clamp(East.value(5n), 1n, 10n), 5n)); // Within range
        $(assert.equal(East.clamp(East.value(15n), 1n, 10n), 10n)); // Above max
        $(assert.equal(East.clamp(East.value(-5n), 1n, 10n), 1n)); // Below min
        $(assert.equal(East.clamp(East.value(1n), 1n, 10n), 1n)); // Equal to min
        $(assert.equal(East.clamp(East.value(10n), 1n, 10n), 10n)); // Equal to max
        $(assert.equal(East.clamp(East.value(0n), -5n, 5n), 0n)); // Within range with negatives
        $(assert.equal(East.clamp(East.value(-10n), -5n, 5n), -5n)); // Below negative min
        $(assert.equal(East.clamp(East.value(10n), -5n, 5n), 5n)); // Above positive max

        // Edge cases
        $(assert.equal(East.clamp(East.value(42n), 42n, 42n), 42n)); // Min equals max
        $(assert.equal(East.clamp(East.value(100n), -100n, 200n), 100n)); // Large range

        // Test with variables
        const val1 = $.let(East.value(7n));
        const val2 = $.let(East.value(3n));
        const val3 = $.let(East.value(12n));

        $(assert.equal(East.min(val1, val2), 3n));
        $(assert.equal(East.max(val1, val2), 7n));
        $(assert.equal(East.clamp(val3, val2, val1), 7n)); // 12 clamped between 3 and 7
    });

    test("Comparison method aliases", $ => {
        // Test short aliases (eq, ne, gt, lt, gte, lte, ge, le)
        $(assert.equal(East.value(10n).eq(10n), true));
        $(assert.equal(East.value(10n).eq(5n), false));
        $(assert.equal(East.value(10n).ne(5n), true));
        $(assert.equal(East.value(10n).ne(10n), false));
        $(assert.equal(East.value(10n).gt(5n), true));
        $(assert.equal(East.value(5n).gt(10n), false));
        $(assert.equal(East.value(5n).lt(10n), true));
        $(assert.equal(East.value(10n).lt(5n), false));
        $(assert.equal(East.value(10n).gte(10n), true));
        $(assert.equal(East.value(10n).gte(5n), true));
        $(assert.equal(East.value(5n).gte(10n), false));
        $(assert.equal(East.value(10n).lte(10n), true));
        $(assert.equal(East.value(5n).lte(10n), true));
        $(assert.equal(East.value(10n).lte(5n), false));
        $(assert.equal(East.value(10n).ge(5n), true));
        $(assert.equal(East.value(5n).le(10n), true));

        // Test medium aliases (equal, notEqual, greater, less, greaterEqual, lessEqual)
        $(assert.equal(East.value(10n).equal(10n), true));
        $(assert.equal(East.value(10n).notEqual(5n), true));
        $(assert.equal(East.value(10n).greater(5n), true));
        $(assert.equal(East.value(5n).less(10n), true));
        $(assert.equal(East.value(10n).greaterEqual(10n), true));
        $(assert.equal(East.value(5n).lessEqual(10n), true));
    });

    test("Arithmetic method aliases", $ => {
        // Test aliases for arithmetic operations
        $(assert.equal(East.value(10n).plus(5n), 15n));
        $(assert.equal(East.value(10n).sub(5n), 5n));
        $(assert.equal(East.value(10n).minus(5n), 5n));
        $(assert.equal(East.value(10n).mul(5n), 50n));
        $(assert.equal(East.value(10n).times(5n), 50n));
        $(assert.equal(East.value(10n).div(5n), 2n));
        $(assert.equal(East.value(10n).mod(3n), 1n));
        $(assert.equal(East.value(10n).rem(3n), 1n));
        $(assert.equal(East.value(10n).modulo(3n), 1n));
    });

    test("Standalone function aliases", $ => {
        // Test aliases for standalone comparison functions
        $(assert.equal(East.equals(East.value(10n), 10n), true));
        $(assert.equal(East.eq(East.value(10n), 10n), true));
        $(assert.equal(East.notEquals(East.value(10n), 5n), true));
        $(assert.equal(East.ne(East.value(10n), 5n), true));
        $(assert.equal(East.lessThan(East.value(5n), 10n), true));
        $(assert.equal(East.lt(East.value(5n), 10n), true));
        $(assert.equal(East.greaterThan(East.value(10n), 5n), true));
        $(assert.equal(East.gt(East.value(10n), 5n), true));
        $(assert.equal(East.lessThanOrEqual(East.value(10n), 10n), true));
        $(assert.equal(East.lte(East.value(10n), 10n), true));
        $(assert.equal(East.le(East.value(10n), 10n), true));
        $(assert.equal(East.greaterThanOrEqual(East.value(10n), 10n), true));
        $(assert.equal(East.gte(East.value(10n), 10n), true));
        $(assert.equal(East.ge(East.value(10n), 10n), true));
    });

    test("Integer to Float conversion", $ => {
        // Basic conversions
        $(assert.equal(East.value(0n).toFloat(), 0.0));
        $(assert.equal(East.value(1n).toFloat(), 1.0));
        $(assert.equal(East.value(-1n).toFloat(), -1.0));
        $(assert.equal(East.value(42n).toFloat(), 42.0));
        $(assert.equal(East.value(-42n).toFloat(), -42.0));
        $(assert.equal(East.value(100n).toFloat(), 100.0));
        $(assert.equal(East.value(1000n).toFloat(), 1000.0));
        $(assert.equal(East.value(1000000n).toFloat(), 1000000.0));

        // Large integers (may lose precision beyond 2^53)
        $(assert.equal(East.value(9007199254740992n).toFloat(), 9007199254740992.0)); // 2^53, exact
        $(assert.equal(East.value(-9007199254740992n).toFloat(), -9007199254740992.0));

        // Test with variable
        const val = $.let(East.value(123n));
        $(assert.equal(val.toFloat(), 123.0));

        // Test with expression result
        $(assert.equal(East.value(10n).add(5n).toFloat(), 15.0));
    });
});
