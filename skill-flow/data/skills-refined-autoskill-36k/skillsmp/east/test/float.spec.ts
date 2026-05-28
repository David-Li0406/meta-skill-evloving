/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, FloatType } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Float", (test) => {
    test("Arithmetic", $ => {
        $(assert.equal(East.value(10).negate(), -10));
        $(assert.equal(East.value(10).add(5), 15));
        $(assert.equal(East.value(10).subtract(5), 5));
        $(assert.equal(East.value(10).multiply(5), 50));
        $(assert.equal(East.value(10).divide(5), 2));
        $(assert.equal(East.value(10).remainder(5), 0));
        $(assert.equal(East.value(10).pow(5), 100_000));

        // Remainder with exact multiples - testing -0.0 behavior
        $(assert.equal(East.value(10.0).remainder(5.0), 0.0));
        $(assert.equal(East.value(-10.0).remainder(5.0), -0.0));
        $(assert.equal(East.value(10.0).remainder(-5.0), 0.0));
        $(assert.equal(East.value(-10.0).remainder(-5.0), -0.0));

        // Remainder with non-exact values (using between for floating point precision)
        $(assert.between(East.value(10.3).remainder(5.0), 0.2999999, 0.3000001));
        $(assert.between(East.value(-10.3).remainder(5.0), -0.3000001, -0.2999999));
        $(assert.equal(East.value(7.5).remainder(2.5), 0.0));
        $(assert.equal(East.value(-7.5).remainder(2.5), -0.0));
    });

    test("Mixed Integer/Float Arithmetic", $ => {
        // Float (LHS) with Integer (RHS) - using IntegerExpr
        $(assert.equal(East.value(10.0).add(East.value(5n)), 15.0));
        $(assert.equal(East.value(10.0).subtract(East.value(5n)), 5.0));
        $(assert.equal(East.value(10.0).multiply(East.value(5n)), 50.0));
        $(assert.equal(East.value(10.0).divide(East.value(5n)), 2.0));
        $(assert.equal(East.value(10.0).remainder(East.value(5n)), 0.0));
        $(assert.equal(East.value(10.0).pow(East.value(2n)), 100.0));

        // Float (LHS) with Integer (RHS) - using bigint literal
        $(assert.equal(East.value(10.0).add(5n), 15.0));
        $(assert.equal(East.value(10.0).subtract(5n), 5.0));
        $(assert.equal(East.value(10.0).multiply(5n), 50.0));
        $(assert.equal(East.value(10.0).divide(5n), 2.0));
        $(assert.equal(East.value(10.0).remainder(5n), 0.0));
        $(assert.equal(East.value(10.0).pow(2n), 100.0));

        // Integer (LHS) with Float (RHS) - using FloatExpr
        $(assert.equal(East.value(10n).add(East.value(5.0)), 15.0));
        $(assert.equal(East.value(10n).subtract(East.value(5.0)), 5.0));
        $(assert.equal(East.value(10n).multiply(East.value(5.0)), 50.0));
        $(assert.equal(East.value(10n).divide(East.value(5.0)), 2.0));
        $(assert.equal(East.value(10n).remainder(East.value(5.0)), 0.0));
        $(assert.equal(East.value(10n).pow(East.value(2.0)), 100.0));

        // Integer (LHS) with Float (RHS) - using number literal
        $(assert.equal(East.value(10n).add(5.0), 15.0));
        $(assert.equal(East.value(10n).subtract(5.0), 5.0));
        $(assert.equal(East.value(10n).multiply(5.0), 50.0));
        $(assert.equal(East.value(10n).divide(5.0), 2.0));
        $(assert.equal(East.value(10n).remainder(5.0), 0.0));
        $(assert.equal(East.value(10n).pow(2.0), 100.0));

        // Test with non-whole results
        $(assert.equal(East.value(10.0).divide(East.value(3n)), 10.0 / 3.0));
        $(assert.equal(East.value(10n).divide(East.value(3.0)), 10.0 / 3.0));
        $(assert.between(East.value(10.0).remainder(East.value(3n)), 0.9999999, 1.0000001));
        $(assert.between(East.value(10n).remainder(East.value(3.0)), 0.9999999, 1.0000001));

        // Test with negative values
        $(assert.equal(East.value(-10.0).add(East.value(5n)), -5.0));
        $(assert.equal(East.value(-10n).add(East.value(5.0)), -5.0));
        $(assert.equal(East.value(10.0).subtract(East.value(-5n)), 15.0));
        $(assert.equal(East.value(10n).subtract(East.value(-5.0)), 15.0));
        $(assert.equal(East.value(-10.0).multiply(East.value(-5n)), 50.0));
        $(assert.equal(East.value(-10n).multiply(East.value(-5.0)), 50.0));
    });

    test("Printing", $ => {
        $(assert.equal(East.print(East.value(0)), "0.0"));
        $(assert.equal(East.print(East.value(1)), "1.0"));
        $(assert.equal(East.print(East.value(1234)), "1234.0"));
        $(assert.equal(East.print(East.value(NaN)), "NaN"));
        $(assert.equal(East.print(East.value(Infinity)), "Infinity"));
        $(assert.equal(East.print(East.value(-1)), "-1.0"));
        $(assert.equal(East.print(East.value(-1234)), "-1234.0"));
        $(assert.equal(East.print(East.value(-Infinity)), "-Infinity"));
    });

    test("Comparisons", $ => {
        $(assert.equal(East.equal(East.value(10), 10), true));
        $(assert.equal(East.equal(East.value(10), 5), false));
        $(assert.equal(East.equal(East.value(-5), -5), true));

        $(assert.equal(East.less(East.value(5), 10), true));
        $(assert.equal(East.less(East.value(10), 5), false));
        $(assert.equal(East.less(East.value(10), 10), false));
        $(assert.equal(East.less(East.value(-10), -5), true));

        $(assert.equal(East.lessEqual(East.value(5), 10), true));
        $(assert.equal(East.lessEqual(East.value(10), 5), false));
        $(assert.equal(East.lessEqual(East.value(10), 10), true));

        $(assert.equal(East.greater(East.value(10), 5), true));
        $(assert.equal(East.greater(East.value(5), 10), false));
        $(assert.equal(East.greater(East.value(10), 10), false));
        $(assert.equal(East.greater(East.value(-5), -10), true));

        $(assert.equal(East.greaterEqual(East.value(10), 5), true));
        $(assert.equal(East.greaterEqual(East.value(5), 10), false));
        $(assert.equal(East.greaterEqual(East.value(10), 10), true));

        // Instance method tests
        $(assert.equal(East.value(10.0).equals(10.0), true));
        $(assert.equal(East.value(10.0).equals(5.0), false));
        $(assert.equal(East.value(10.0).notEquals(5.0), true));
        $(assert.equal(East.value(10.0).notEquals(10.0), false));
        $(assert.equal(East.value(5.0).lessThan(10.0), true));
        $(assert.equal(East.value(10.0).lessThan(5.0), false));
        $(assert.equal(East.value(5.0).lessThanOrEqual(10.0), true));
        $(assert.equal(East.value(10.0).lessThanOrEqual(10.0), true));
        $(assert.equal(East.value(10.0).greaterThan(5.0), true));
        $(assert.equal(East.value(5.0).greaterThan(10.0), false));
        $(assert.equal(East.value(10.0).greaterThanOrEqual(5.0), true));
        $(assert.equal(East.value(10.0).greaterThanOrEqual(10.0), true));
    });

    test("Parsing", $ => {
        $(assert.equal(East.value("0.0").parse(FloatType), 0));
        $(assert.equal(East.value("123.0").parse(FloatType), 123));
        $(assert.equal(East.value("-456.0").parse(FloatType), -456));
        $(assert.equal(East.value("1e20").parse(FloatType), 1e20));
        $(assert.equal(East.value("NaN").parse(FloatType), NaN));
        $(assert.equal(East.value("Infinity").parse(FloatType), Infinity));
        $(assert.equal(East.value("-Infinity").parse(FloatType), -Infinity));
        $(assert.equal(East.value("3.14159").parse(FloatType), 3.14159));
        $(assert.equal(East.value("-2.71828").parse(FloatType), -2.71828));
        $(assert.equal(East.value("0.0001").parse(FloatType), 0.0001));
        $(assert.equal(East.value("-0.0001").parse(FloatType), -0.0001));

        $(assert.throws(East.value("abc").parse(FloatType)));
        // $(assertEast.throws(Expr.from("12").parse(FloatType))); // TODO decide if this should throw or be tolerant?
        $(assert.equal(East.value("12").parse(FloatType), 12));
        $(assert.throws(East.value("").parse(FloatType)));
        $(assert.throws(East.value("123abc").parse(FloatType)));
        $(assert.throws(East.value("123e").parse(FloatType)));
        $(assert.throws(East.value(".0").parse(FloatType)));
        $(assert.throws(East.value("e10").parse(FloatType)));
    });

    test("Mathematical functions", $ => {
        // abs() tests
        $(assert.equal(East.value(5).abs(), 5));
        $(assert.equal(East.value(-5).abs(), 5));
        $(assert.equal(East.value(0).abs(), 0));

        // sign() tests
        $(assert.equal(East.value(5).sign(), 1));
        $(assert.equal(East.value(-5).sign(), -1));
        $(assert.equal(East.value(0).sign(), 0));

        $(assert.equal(East.value(4).sqrt(), 2));
        $(assert.equal(East.value(1).log(), 0));
        $(assert.equal(East.value(0).exp(), 1));
        $(assert.between(East.value(Math.PI / 2).sin(), 1 - 1e-10, 1 + 1e-10));
        $(assert.between(East.value(0).cos(), 1 - 1e-10, 1 + 1e-10));
        $(assert.between(East.value(Math.PI / 4).tan(), 1 - 1e-10, 1 + 1e-10));
    });

    test("Float to Integer conversion", $ => {
        // Basic conversions
        $(assert.equal(East.value(0.0).toInteger(), 0n));
        $(assert.equal(East.value(1.0).toInteger(), 1n));
        $(assert.equal(East.value(-1.0).toInteger(), -1n));
        $(assert.equal(East.value(42.0).toInteger(), 42n));
        $(assert.equal(East.value(-42.0).toInteger(), -42n));

        // Edge cases
        $(assert.equal(East.value(Number.MAX_SAFE_INTEGER).toInteger(), BigInt(Number.MAX_SAFE_INTEGER)));
        $(assert.equal(East.value(Number.MIN_SAFE_INTEGER).toInteger(), BigInt(Number.MIN_SAFE_INTEGER)));
        $(assert.throws(East.value(9223372036854775807.0).toInteger())); // i64 max, rounded up by f64 yields a number out of i64 range
        $(assert.equal(East.value(-9223372036854775808.0).toInteger(), -9223372036854775808n)); // i64 min

        // Erroneous cases
        $(assert.throws(East.value(3.7).toInteger()));
        $(assert.throws(East.value(1e20).toInteger()));
        $(assert.throws(East.value(-1e20).toInteger()));
        $(assert.throws(East.value(Infinity).toInteger()));
        $(assert.throws(East.value(-Infinity).toInteger()));
        $(assert.throws(East.value(NaN).toInteger()));
    });

    test("approxEqual", $ => {
        $(assert.equal(East.Float.approxEqual(1.0, 1.0, 0.001), true));
        $(assert.equal(East.Float.approxEqual(1.0, 1.0001, 0.001), true));
        $(assert.equal(East.Float.approxEqual(1.0, 1.1, 0.001), false));
        $(assert.equal(East.Float.approxEqual(-1.0, -1.0001, 0.001), true));
        $(assert.equal(East.Float.approxEqual(0.0, 0.0, 0.0), true));

        // Edge cases
        $(assert.equal(East.Float.approxEqual(Infinity, Infinity, 0.001), false));
        $(assert.equal(East.Float.approxEqual(-Infinity, -Infinity, 0.001), false));
        $(assert.equal(East.Float.approxEqual(NaN, NaN, 0.001), false));
        $(assert.equal(East.Float.approxEqual(1.0, Infinity, 1000.0), false));
    });

    test("roundFloor", $ => {
        $(assert.equal(East.Float.roundFloor(3.7), 3n));
        $(assert.equal(East.Float.roundFloor(3.0), 3n));
        $(assert.equal(East.Float.roundFloor(-3.7), -4n));
        $(assert.equal(East.Float.roundFloor(-3.0), -3n));
        $(assert.equal(East.Float.roundFloor(0.0), 0n));
        $(assert.equal(East.Float.roundFloor(0.9), 0n));
        $(assert.equal(East.Float.roundFloor(-0.9), -1n));

        // Edge cases
        $(assert.throws(East.Float.roundFloor(Infinity)));
        $(assert.throws(East.Float.roundFloor(-Infinity)));
        $(assert.throws(East.Float.roundFloor(NaN)));
    });

    test("roundCeil", $ => {
        $(assert.equal(East.Float.roundCeil(3.7), 4n));
        $(assert.equal(East.Float.roundCeil(3.0), 3n));
        $(assert.equal(East.Float.roundCeil(-3.7), -3n));
        $(assert.equal(East.Float.roundCeil(-3.0), -3n));
        $(assert.equal(East.Float.roundCeil(0.0), 0n));
        $(assert.equal(East.Float.roundCeil(0.1), 1n));
        $(assert.equal(East.Float.roundCeil(-0.1), 0n));

        // Edge cases
        $(assert.throws(East.Float.roundCeil(Infinity)));
        $(assert.throws(East.Float.roundCeil(-Infinity)));
        $(assert.throws(East.Float.roundCeil(NaN)));
    });

    test("roundHalf", $ => {
        $(assert.equal(East.Float.roundHalf(3.5), 4n));
        $(assert.equal(East.Float.roundHalf(3.4), 3n));
        $(assert.equal(East.Float.roundHalf(3.6), 4n));
        $(assert.equal(East.Float.roundHalf(-3.5), -4n));
        $(assert.equal(East.Float.roundHalf(-3.4), -3n));
        $(assert.equal(East.Float.roundHalf(0.0), 0n));
        $(assert.equal(East.Float.roundHalf(0.5), 1n));
        $(assert.equal(East.Float.roundHalf(-0.5), -1n));

        // Edge cases
        $(assert.throws(East.Float.roundHalf(Infinity)));
        $(assert.throws(East.Float.roundHalf(-Infinity)));
        $(assert.throws(East.Float.roundHalf(NaN)));
    });

    test("roundTrunc", $ => {
        $(assert.equal(East.Float.roundTrunc(3.7), 3n));
        $(assert.equal(East.Float.roundTrunc(3.0), 3n));
        $(assert.equal(East.Float.roundTrunc(-3.7), -3n));
        $(assert.equal(East.Float.roundTrunc(-3.0), -3n));
        $(assert.equal(East.Float.roundTrunc(0.0), 0n));

        // Edge cases
        $(assert.throws(East.Float.roundTrunc(Infinity)));
        $(assert.throws(East.Float.roundTrunc(-Infinity)));
        $(assert.throws(East.Float.roundTrunc(NaN)));
    });

    test("roundNearest", $ => {
        $(assert.equal(East.Float.roundNearest(10.0, 5.0), 10.0));
        $(assert.equal(East.Float.roundNearest(12.0, 5.0), 10.0));
        $(assert.equal(East.Float.roundNearest(13.0, 5.0), 15.0));
        $(assert.equal(East.Float.roundNearest(-12.0, 5.0), -10.0));
        $(assert.equal(East.Float.roundNearest(-13.0, 5.0), -15.0));
        $(assert.equal(East.Float.roundNearest(7.5, 5.0), 10.0));
        $(assert.equal(East.Float.roundNearest(0.0, 5.0), 0.0));
    });

    test("roundUp", $ => {
        $(assert.equal(East.Float.roundUp(10.0, 5.0), 10.0));
        $(assert.equal(East.Float.roundUp(12.0, 5.0), 15.0));
        $(assert.equal(East.Float.roundUp(11.0, 5.0), 15.0));
        $(assert.equal(East.Float.roundUp(-12.0, 5.0), -10.0));
        $(assert.equal(East.Float.roundUp(-10.0, 5.0), -10.0));
        $(assert.equal(East.Float.roundUp(0.0, 5.0), 0.0));
    });

    test("roundDown", $ => {
        $(assert.equal(East.Float.roundDown(10.0, 5.0), 10.0));
        $(assert.equal(East.Float.roundDown(12.0, 5.0), 10.0));
        $(assert.equal(East.Float.roundDown(14.9, 5.0), 10.0));
        $(assert.equal(East.Float.roundDown(-12.0, 5.0), -15.0));
        $(assert.equal(East.Float.roundDown(-10.0, 5.0), -10.0));
        $(assert.equal(East.Float.roundDown(0.0, 5.0), 0.0));
    });

    test("roundTruncate", $ => {
        $(assert.equal(East.Float.roundTruncate(12.0, 5.0), 10.0));
        $(assert.equal(East.Float.roundTruncate(14.9, 5.0), 10.0));
        $(assert.equal(East.Float.roundTruncate(-12.0, 5.0), -10.0));
        $(assert.equal(East.Float.roundTruncate(-14.9, 5.0), -10.0));
        $(assert.equal(East.Float.roundTruncate(10.0, 5.0), 10.0));
        $(assert.equal(East.Float.roundTruncate(0.0, 5.0), 0.0));
    });

    test("roundToDecimals", $ => {
        $(assert.equal(East.Float.roundToDecimals(3.14159, 2n), 3.14));
        $(assert.equal(East.Float.roundToDecimals(3.14159, 0n), 3.0));
        $(assert.equal(East.Float.roundToDecimals(3.14159, 4n), 3.1416));
        $(assert.equal(East.Float.roundToDecimals(-2.71828, 2n), -2.72));
        $(assert.equal(East.Float.roundToDecimals(1.5, 0n), 2.0));
    });

    test("printCommaSeperated", $ => {
        $(assert.equal(East.Float.printCommaSeperated(1234.56, 2n), "1,234.56"));
        $(assert.equal(East.Float.printCommaSeperated(1234.5, 2n), "1,234.50"));
        $(assert.equal(East.Float.printCommaSeperated(-1234.56, 2n), "-1,234.56"));
        $(assert.equal(East.Float.printCommaSeperated(0.0, 2n), "0.00"));
        $(assert.equal(East.Float.printCommaSeperated(42.0, 0n), "42"));
    });

    test("printCurrency", $ => {
        $(assert.equal(East.Float.printCurrency(1234.56), "$1,234.56"));
        $(assert.equal(East.Float.printCurrency(1234.5), "$1,234.50"));
        $(assert.equal(East.Float.printCurrency(-1234.56), "-$1,234.56"));
        $(assert.equal(East.Float.printCurrency(0.0), "$0.00"));
        $(assert.equal(East.Float.printCurrency(0.99), "$0.99"));
        $(assert.equal(East.Float.printCurrency(0.09), "$0.09"));
    });

    test("printFixed", $ => {
        $(assert.equal(East.Float.printFixed(3.14159, 2n), "3.14"));
        $(assert.equal(East.Float.printFixed(3.14159, 0n), "3"));
        $(assert.equal(East.Float.printFixed(3.14159, 4n), "3.1416"));
        $(assert.equal(East.Float.printFixed(-2.71828, 2n), "-2.72"));
        $(assert.equal(East.Float.printFixed(0.0, 2n), "0.00"));
        $(assert.equal(East.Float.printFixed(0.009, 2n), "0.01"));
    });

    test("printCompact", $ => {
        $(assert.equal(East.Float.printCompact(500.0), "5.0"));
        $(assert.equal(East.Float.printCompact(1500.0), "1.5K"));
        $(assert.equal(East.Float.printCompact(1500000.0), "1.5M"));
        $(assert.equal(East.Float.printCompact(1500000000.0), "1.5B"));
        $(assert.equal(East.Float.printCompact(-1500.0), "-1.5K"));
        $(assert.equal(East.Float.printCompact(0.0), "0.0"));
    });

    test("printPercentage", $ => {
        $(assert.equal(East.Float.printPercentage(0.1234, 2n), "12.34%"));
        $(assert.equal(East.Float.printPercentage(0.1234, 0n), "12.0%"));
        $(assert.equal(East.Float.printPercentage(1.0, 2n), "100.0%"));
        $(assert.equal(East.Float.printPercentage(-0.25, 2n), "-25.0%"));
        $(assert.equal(East.Float.printPercentage(0.0, 2n), "0.0%"));
    });

    test("Edge cases: NaN and Infinity for step-based rounding", $ => {
        // roundNearest with NaN/Infinity - should throw
        $(assert.throws(East.Float.roundNearest(NaN, 5.0)));
        $(assert.throws(East.Float.roundNearest(Infinity, 5.0)));
        $(assert.throws(East.Float.roundNearest(-Infinity, 5.0)));

        // roundUp with NaN/Infinity - should throw
        $(assert.throws(East.Float.roundUp(NaN, 5.0)));
        $(assert.throws(East.Float.roundUp(Infinity, 5.0)));
        $(assert.throws(East.Float.roundUp(-Infinity, 5.0)));

        // roundDown with NaN/Infinity - should throw
        $(assert.throws(East.Float.roundDown(NaN, 5.0)));
        $(assert.throws(East.Float.roundDown(Infinity, 5.0)));
        $(assert.throws(East.Float.roundDown(-Infinity, 5.0)));

        // roundTruncate with NaN/Infinity - should throw
        $(assert.throws(East.Float.roundTruncate(NaN, 5.0)));
        $(assert.throws(East.Float.roundTruncate(Infinity, 5.0)));
        $(assert.throws(East.Float.roundTruncate(-Infinity, 5.0)));

        // roundToDecimals with NaN/Infinity - should throw
        $(assert.throws(East.Float.roundToDecimals(NaN, 2n)));
        $(assert.throws(East.Float.roundToDecimals(Infinity, 2n)));
        $(assert.throws(East.Float.roundToDecimals(-Infinity, 2n)));
    });

    test("Comparison method aliases", $ => {
        // Test short aliases (eq, ne, gt, lt, gte, lte, ge, le)
        $(assert.equal(East.value(10.0).eq(10.0), true));
        $(assert.equal(East.value(10.0).eq(5.0), false));
        $(assert.equal(East.value(10.0).ne(5.0), true));
        $(assert.equal(East.value(10.0).ne(10.0), false));
        $(assert.equal(East.value(10.0).gt(5.0), true));
        $(assert.equal(East.value(5.0).gt(10.0), false));
        $(assert.equal(East.value(5.0).lt(10.0), true));
        $(assert.equal(East.value(10.0).lt(5.0), false));
        $(assert.equal(East.value(10.0).gte(10.0), true));
        $(assert.equal(East.value(10.0).gte(5.0), true));
        $(assert.equal(East.value(5.0).lte(10.0), true));
        $(assert.equal(East.value(10.0).ge(5.0), true));
        $(assert.equal(East.value(5.0).le(10.0), true));

        // Test medium aliases (equal, notEqual, greater, less, greaterEqual, lessEqual)
        $(assert.equal(East.value(10.0).equal(10.0), true));
        $(assert.equal(East.value(10.0).notEqual(5.0), true));
        $(assert.equal(East.value(10.0).greater(5.0), true));
        $(assert.equal(East.value(5.0).less(10.0), true));
        $(assert.equal(East.value(10.0).greaterEqual(10.0), true));
        $(assert.equal(East.value(5.0).lessEqual(10.0), true));
    });

    test("Arithmetic method aliases", $ => {
        $(assert.equal(East.value(10.0).plus(5.0), 15.0));
        $(assert.equal(East.value(10.0).sub(5.0), 5.0));
        $(assert.equal(East.value(10.0).minus(5.0), 5.0));
        $(assert.equal(East.value(10.0).mul(5.0), 50.0));
        $(assert.equal(East.value(10.0).times(5.0), 50.0));
        $(assert.equal(East.value(10.0).div(5.0), 2.0));
        $(assert.equal(East.value(10.0).mod(3.0), 1.0));
        $(assert.equal(East.value(10.0).rem(3.0), 1.0));
        $(assert.equal(East.value(10.0).modulo(3.0), 1.0));
    });

    test("Edge cases: NaN and Infinity for formatting functions", $ => {
        // printCommaSeperated with NaN/Infinity - should throw or handle gracefully
        $(assert.throws(East.Float.printCommaSeperated(NaN, 2n)));
        $(assert.throws(East.Float.printCommaSeperated(Infinity, 2n)));
        $(assert.throws(East.Float.printCommaSeperated(-Infinity, 2n)));

        // printCurrency with NaN/Infinity - should throw or handle gracefully
        $(assert.throws(East.Float.printCurrency(NaN)));
        $(assert.throws(East.Float.printCurrency(Infinity)));
        $(assert.throws(East.Float.printCurrency(-Infinity)));

        // printFixed with NaN/Infinity - should throw or handle gracefully
        $(assert.throws(East.Float.printFixed(NaN, 2n)));
        $(assert.throws(East.Float.printFixed(Infinity, 2n)));
        $(assert.throws(East.Float.printFixed(-Infinity, 2n)));

        // printCompact with NaN/Infinity - should throw or handle gracefully
        $(assert.throws(East.Float.printCompact(NaN)));
        $(assert.throws(East.Float.printCompact(Infinity)));
        $(assert.throws(East.Float.printCompact(-Infinity)));

        // printPercentage with NaN/Infinity - should throw or handle gracefully
        $(assert.throws(East.Float.printPercentage(NaN, 2n)));
        $(assert.throws(East.Float.printPercentage(Infinity, 2n)));
        $(assert.throws(East.Float.printPercentage(-Infinity, 2n)));
    });
});
