/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, BooleanType } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Boolean", (test) => {
    test("Boolean operations", $ => {
        $(assert.equal(East.value(true).not(), false));
        $(assert.equal(East.value(false).not(), true));

        $(assert.equal(East.value(true).bitAnd(true), true));
        $(assert.equal(East.value(true).bitAnd(false), false));
        $(assert.equal(East.value(false).bitAnd(true), false));
        $(assert.equal(East.value(false).bitAnd(false), false));

        $(assert.equal(East.value(true).bitOr(true), true));
        $(assert.equal(East.value(true).bitOr(false), true));
        $(assert.equal(East.value(false).bitOr(true), true));
        $(assert.equal(East.value(false).bitOr(false), false));

        $(assert.equal(East.value(true).bitXor(true), false));
        $(assert.equal(East.value(true).bitXor(false), true));
        $(assert.equal(East.value(false).bitXor(true), true));
        $(assert.equal(East.value(false).bitXor(false), false));
    });

    test("Printing", $ => {
        $(assert.equal(East.print(East.value(true)), "true"));
        $(assert.equal(East.print(East.value(false)), "false"));
    });

    test("Comparisons", $ => {
        // Equality tests
        $(assert.equal(East.value(true), true));
        $(assert.equal(East.value(false), false));
        $(assert.notEqual(East.value(true), false));
        $(assert.notEqual(East.value(false), true));

        // Ordering tests - false < true in most boolean orderings
        $(assert.less(East.value(false), true));
        $(assert.greater(East.value(true), false));
        $(assert.lessEqual(East.value(false), false));
        $(assert.lessEqual(East.value(false), true));
        $(assert.lessEqual(East.value(true), true));
        $(assert.greaterEqual(East.value(true), true));
        $(assert.greaterEqual(East.value(true), false));
        $(assert.greaterEqual(East.value(false), false));

        // East.is, East.equal, East.less methods
        $(assert.equal(East.is(East.value(true), true), true));
        $(assert.equal(East.is(East.value(false), false), true));
        $(assert.equal(East.is(East.value(true), false), false));
        $(assert.equal(East.equal(East.value(true), true), true));
        $(assert.equal(East.equal(East.value(false), false), true));
        $(assert.equal(East.notEqual(East.value(true), false), true));
        $(assert.equal(East.less(East.value(false), true), true));
        $(assert.equal(East.less(East.value(true), false), false));
        $(assert.equal(East.lessEqual(East.value(false), true), true));
        $(assert.equal(East.lessEqual(East.value(true), true), true));
        $(assert.equal(East.greater(East.value(true), false), true));
        $(assert.equal(East.greaterEqual(East.value(true), false), true));

        // Instance method tests
        $(assert.equal(East.value(true).equals(true), true));
        $(assert.equal(East.value(true).equals(false), false));
        $(assert.equal(East.value(true).notEquals(false), true));
        $(assert.equal(East.value(true).notEquals(true), false));
    });

    test("Parsing", $ => {
        $(assert.equal(East.value("true").parse(BooleanType), true));
        $(assert.equal(East.value("false").parse(BooleanType), false));
        $(assert.throws(East.value("maybe").parse(BooleanType)));
    });

    test("Short-circuit .and() basic", $ => {
        // Basic short-circuit and
        $(assert.equal(East.value(true).and(_$ => true), true));
        $(assert.equal(East.value(true).and(_$ => false), false));
        $(assert.equal(East.value(false).and(_$ => true), false));
        $(assert.equal(East.value(false).and(_$ => false), false));
    });

    test("Short-circuit .or() basic", $ => {
        // Basic short-circuit or
        $(assert.equal(East.value(true).or(_$ => true), true));
        $(assert.equal(East.value(true).or(_$ => false), true));
        $(assert.equal(East.value(false).or(_$ => true), true));
        $(assert.equal(East.value(false).or(_$ => false), false));
    });

    test("Short-circuit .and() captures outer variable", $ => {
        const threshold = $.const(5n);
        const value = $.const(3n);
        // .and() closure captures 'threshold' from outer scope
        const result = $.let(East.greater(value, 0n).and(_$ => East.less(value, threshold)));
        $(assert.equal(result, true));
    });

    test("Short-circuit .or() captures outer variable", $ => {
        const lower = $.const(0n);
        const upper = $.const(10n);
        const value = $.const(15n);
        // .or() closure captures 'upper' from outer scope
        const result = $.let(East.less(value, lower).or(_$ => East.greater(value, upper)));
        $(assert.equal(result, true));
    });

    test("Nested .and()/.or() captures variables from multiple scopes", $ => {
        const a = $.const(5n);
        const b = $.const(10n);
        const _c = $.const(15n);
        const x = $.const(7n);
        // Nested: .and() inside .or(), both capturing outer variables
        const result = $.let(
            East.less(x, a).or(_$ =>
                East.greater(x, a).and(_$ => East.less(x, b))
            )
        );
        $(assert.equal(result, true)); // 7 > 5 && 7 < 10
    });

    test("Equality method aliases", $ => {
        // Test short aliases (eq, ne)
        $(assert.equal(East.value(true).eq(true), true));
        $(assert.equal(East.value(true).eq(false), false));
        $(assert.equal(East.value(true).ne(false), true));
        $(assert.equal(East.value(false).ne(false), false));

        // Test medium aliases (equal, notEqual)
        $(assert.equal(East.value(true).equal(true), true));
        $(assert.equal(East.value(true).notEqual(false), true));
    });
});
