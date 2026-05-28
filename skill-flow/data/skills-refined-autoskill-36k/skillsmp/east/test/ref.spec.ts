/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, IntegerType, ref, RefType } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Ref", (test) => {
    test("Construct, get, set", $ => {
        $(assert.equal(East.value(ref(42n)).get(), 42n));

        const r1 = $.let(East.value(ref(0n)));
        const r2 = $.let(r1);
        $(assert.equal(r1.get(), 0n));
        $(assert.equal(r2.get(), 0n));

        $(r1.update(East.value(100n)));
        $(assert.equal(r1.get(), 100n));
        $(assert.equal(r2.get(), 100n));

        $(r1.merge(r2.get(), ($, i1, i2) => i1.add(i2)))
        $(assert.equal(r1.get(), 200n));
        $(assert.equal(r2.get(), 200n));
    });

    test("Comparisons", $ => {
        const r = $.let(East.value(ref(10n)));
        const r2 = $.let(East.value(ref(20n)));
        const r3 = $.let(r);

        // is
        $(assert.is(East.equal(r, r3), true));
        $(assert.is(East.equal(r, r2), false));

        // equal
        $(assert.equal(East.equal(r, r2), false));
        $(assert.equal(East.equal(r, r3), true));

        // not equal
        $(assert.equal(East.notEqual(r, r2), true));
        $(assert.equal(East.notEqual(r, r3), false));

        // less than
        $(assert.equal(East.less(r, r2), true));
        $(assert.equal(East.less(r2, r), false));

        // less than or equal
        $(assert.equal(East.lessEqual(r, r2), true));
        $(assert.equal(East.lessEqual(r2, r), false));
        $(assert.equal(East.lessEqual(r, r3), true));

        // greater than
        $(assert.equal(East.greater(r2, r), true));
        $(assert.equal(East.greater(r, r2), false));

        // greater than or equal
        $(assert.equal(East.greaterEqual(r2, r), true));
        $(assert.equal(East.greaterEqual(r, r2), false));
        $(assert.equal(East.greaterEqual(r, r3), true));
    });

    test("Printing", $ => {
        $(assert.equal(East.print(East.value(ref(42n))), "&42"));
    });

    test("Parsing", $ => {
        $(assert.equal(East.value("&42").parse(RefType(IntegerType)), ref(42n)));
        $(assert.equal(East.value("& 42").parse(RefType(IntegerType)), ref(42n)));
        
        $(assert.throws(East.value("42").parse(RefType(IntegerType))));
        $(assert.throws(East.value("&").parse(RefType(IntegerType))));
        $(assert.throws(East.value("").parse(RefType(IntegerType))));
        $(assert.throws(East.value("&3.14").parse(RefType(IntegerType))));
    });
});
