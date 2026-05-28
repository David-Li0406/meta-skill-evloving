/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, Expr, IntegerType, NullType, OptionType, variant, VariantType } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Variant", (test) => {
    test("Variant equality and type merging", $ => {
        $(assert.equal(East.value(true).ifElse(_$ => variant("some", 42n), _$ => variant("none", null)), variant("some", 42n)));
        $(assert.equal(East.value(false).ifElse(_$ => variant("some", 42n), _$ => variant("none", null)), variant("none", null)));
    });

    test("Match statement", $ => {
        const f = $.const(East.function([VariantType({ none: NullType, some: IntegerType })], IntegerType, ($, x) => {
            let ret = $.let(0n);
            $.match(x, {
                some: ($, data) => $.assign(ret, data),
            })
            $.return(ret);
        }));

        $(assert.equal(f(variant("some", 42n)), 42n));
        $(assert.equal(f(variant("none", null)), 0n));
    });

    test("Expressions", $ => {
        const v1 = $.let(variant("some", 42n), OptionType(IntegerType));
        const v2 = $.let(variant("none", null), OptionType(IntegerType));

        $(assert.equal(Expr.match(v1, { some: ($, data) => data, none: () => 0n }), 42n));
        $(assert.equal(Expr.match(v2, { some: ($, data) => data, none: () => 0n }), 0n));

        $(assert.equal(v1.getTag(), "some"));
        $(assert.equal(v2.getTag(), "none"));

        $(assert.equal(v1.hasTag("some"), true));
        $(assert.equal(v1.hasTag("none"), false));
        $(assert.equal(v2.hasTag("some"), false));
        $(assert.equal(v2.hasTag("none"), true));

        $(assert.equal(v1.unwrap("some", _$ => 0n), 42n));
        $(assert.equal(v1.unwrap("none", _$ => null), null));
        $(assert.equal(v2.unwrap("some", _$ => 0n), 0n));
        $(assert.equal(v2.unwrap("none", _$ => null), null));

        $(assert.equal(v1.unwrap("some"), 42n));
        $(assert.throws(v1.unwrap("none")));
        $(assert.throws(v2.unwrap("some")));
        $(assert.equal(v2.unwrap("none"), null));

        $(assert.equal(v1.unwrap(), 42n));
        $(assert.throws(v2.unwrap()));

        const v3 = $.let(variant("other", 3.14));

        $(assert.throws(v3.unwrap()));

        const ResultType = VariantType({ ok: IntegerType, error: IntegerType, pending: NullType });
        const r1 = $.let(variant("ok", 100n), ResultType);
        const r2 = $.let(variant("error", -1n), ResultType);
        const r3 = $.let(variant("pending", null), ResultType);

        // partial match: only some cases + default (2nd arg)
        $(assert.equal(v1.match({ some: (_$, val) => val }, _$ => 0n), 42n));
        $(assert.equal(v2.match({ some: (_$, val) => val }, _$ => 0n), 0n));
        $(assert.equal(v1.match({ none: _$ => -1n }, _$ => -1n), -1n));
        $(assert.equal(v2.match({ none: _$ => -1n }, _$ => -1n), -1n));
        $(assert.equal(r1.match({ ok: (_$, val) => val, error: (_$, val) => val }, _$ => 0n), 100n));
        $(assert.equal(r2.match({ ok: (_$, val) => val, error: (_$, val) => val }, _$ => 0n), -1n));
        $(assert.equal(r3.match({ ok: (_$, val) => val, error: (_$, val) => val }, _$ => 0n), 0n));

        // exhaustive match: all cases handled, no default (no 2nd arg)
        $(assert.equal(v1.match({ some: (_$, val) => val, none: _$ => 0n }), 42n));
        $(assert.equal(v2.match({ some: (_$, val) => val, none: _$ => 0n }), 0n));
        $(assert.equal(r1.match({ ok: (_$, val) => val, error: (_$, val) => val, pending: _$ => 0n }), 100n));
        $(assert.equal(r2.match({ ok: (_$, val) => val, error: (_$, val) => val, pending: _$ => 0n }), -1n));
        $(assert.equal(r3.match({ ok: (_$, val) => val, error: (_$, val) => val, pending: _$ => 0n }), 0n));
    });

    test("Comparisons", $ => {
        // Equality tests
        $(assert.equal(East.value(variant("none", null)), variant("none", null)));
        $(assert.equal(East.value(variant("some", 42n)), variant("some", 42n)));
        $(assert.notEqual(East.value(variant("some", 42n)), variant("some", 43n)));

        // Same tag, different values - ordering tests
        $(assert.less(East.value(variant("some", 10n)), variant("some", 20n)));
        $(assert.greater(East.value(variant("some", 20n)), variant("some", 10n)));

        // Less than or equal / Greater than or equal
        $(assert.lessEqual(East.value(variant("none", null)), variant("none", null)))
        $(assert.lessEqual(East.value(variant("some", 10n)), variant("some", 20n)))
        $(assert.greaterEqual(East.value(variant("some", 42n)), variant("some", 42n)))
        $(assert.greaterEqual(East.value(variant("some", 20n)), variant("some", 10n)))

        // East.is, East.equal, East.less methods
        $(assert.equal(East.is(East.value(variant("some", 42n)), variant("some", 42n)), true));
        $(assert.equal(East.is(East.value(variant("some", 42n)), variant("some", 43n)), false));
        $(assert.equal(East.equal(East.value(variant("some", 42n)), variant("some", 42n)), true));
        $(assert.equal(East.equal(East.value(variant("some", 42n)), variant("some", 43n)), false));
        $(assert.equal(East.notEqual(East.value(variant("some", 42n)), variant("some", 43n)), true));
        $(assert.equal(East.less(East.value(variant("some", 10n)), variant("some", 20n)), true));
        $(assert.equal(East.greater(East.value(variant("some", 20n)), variant("some", 10n)), true));
        $(assert.equal(East.lessEqual(East.value(variant("some", 10n)), variant("some", 20n)), true));
        $(assert.equal(East.greaterEqual(East.value(variant("some", 20n)), variant("some", 10n)), true));

        // Instance method tests
        $(assert.equal(East.value(variant("some", 42n)).equals(variant("some", 42n)), true));
        $(assert.equal(East.value(variant("some", 42n)).equals(variant("some", 43n)), false));
        $(assert.equal(East.value(variant("some", 42n)).notEquals(variant("some", 43n)), true));
        $(assert.equal(East.value(variant("some", 42n)).notEquals(variant("some", 42n)), false));

        // TODO: Add cross-type variant comparison tests once universal comparison functions are available
    });

    test("Equality method aliases", $ => {
        // Test short aliases (eq, ne)
        $(assert.equal(East.value(variant("some", 42n)).eq(variant("some", 42n)), true));
        $(assert.equal(East.value(variant("some", 42n)).eq(variant("some", 43n)), false));
        $(assert.equal(East.value(variant("some", 42n)).ne(variant("some", 43n)), true));
        $(assert.equal(East.value(variant("some", 42n)).ne(variant("some", 42n)), false));

        // Test medium aliases (equal, notEqual)
        $(assert.equal(East.value(variant("some", 42n)).equal(variant("some", 42n)), true));
        $(assert.equal(East.value(variant("some", 42n)).notEqual(variant("some", 43n)), true));
    });
});
