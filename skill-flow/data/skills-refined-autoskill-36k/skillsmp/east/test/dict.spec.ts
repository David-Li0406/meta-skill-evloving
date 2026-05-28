/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { ArrayType, BooleanType, DictType, East, Expr, IntegerType, none, SetType, some, StringType } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

const { str } = East;

await describe("Dict", (test) => {
    test("Dict ops", $ => {

        $(assert.equal(East.value(new Map(), DictType(IntegerType, StringType)).size(), 0n))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).size(), 3n))

        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).has(0n), false))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).has(1n), true))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).has(2n), true))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).has(3n), true))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).has(4n), false))

        $(assert.equal(East.Dict.generate(6n, IntegerType, StringType, (_$, i) => i.add(1n), (_$, i) => East.print(i)), new Map([[1n, "0"], [2n, "1"], [3n, "2"], [4n, "3"], [5n, "4"], [6n, "5"]])));
        $(assert.throws(East.Dict.generate(6n, IntegerType, StringType, (_$, i) => i.remainder(2n), ($, i) => East.print(i))));
        $(assert.equal(
            East.Dict.generate(
                6n,
                IntegerType,
                StringType,
                (_$, i) => i.remainder(2n),
                (_$, i) => East.print(i),
                (_$, v1, v2, _key) => str`${v1},${v2}`
            ),
            new Map([[0n, "0,2,4"], [1n, "1,3,5"]])
        ));

    });

    test("Printing", $ => {

        $(assert.equal(East.print(East.value(new Map<bigint, string>(), DictType(IntegerType, StringType))), "{:}"))
        $(assert.equal(East.print(East.value(new Map([[1n, "a"]]))), "{1:\"a\"}"))
        $(assert.equal(East.print(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]]))), "{1:\"a\",2:\"b\",3:\"c\"}"))
        $(assert.equal(East.print(East.value(new Map([[3n, "c"], [1n, "a"], [2n, "b"]]))), "{1:\"a\",2:\"b\",3:\"c\"}"))
        $(assert.equal(East.print(East.value(new Map([["x", 1n], ["y", 2n], ["z", 3n]]))), "{\"x\":1,\"y\":2,\"z\":3}"))

    });

    test("Parsing", $ => {

        $(assert.equal(East.value("{:}").parse(DictType(IntegerType, StringType)), new Map<bigint, string>()))
        $(assert.equal(East.value("{1:\"a\"}").parse(DictType(IntegerType, StringType)), new Map([[1n, "a"]])))
        $(assert.equal(East.value("{1:\"a\",2:\"b\",3:\"c\"}").parse(DictType(IntegerType, StringType)), new Map([[1n, "a"], [2n, "b"], [3n, "c"]])))
        $(assert.equal(East.value("{3:\"c\",1:\"a\",2:\"b\"}").parse(DictType(IntegerType, StringType)), new Map([[1n, "a"], [2n, "b"], [3n, "c"]])))
        $(assert.equal(East.value("{\"x\":1,\"y\":2,\"z\":3}").parse(DictType(StringType, IntegerType)), new Map([["x", 1n], ["y", 2n], ["z", 3n]])))
        $(assert.throws(East.value("{1:\"a\",}").parse(DictType(IntegerType, StringType))))
        $(assert.throws(East.value("{1:\"a\",,2:\"b\"}").parse(DictType(IntegerType, StringType))))
        $(assert.throws(East.value("[1:\"a\",2:\"b\"]").parse(DictType(IntegerType, StringType))))
        // $(expectError(Expr.from("{}").parse(DictType(IntegerType, StringType)))) // choosing to be permissive here
        $(assert.equal(East.value("{}").parse(DictType(IntegerType, StringType)), new Map<bigint, string>()))

    });

    test("Dict insert", $ => {

        const d = $.let(new Map([[1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType))
        $(d.insert(3n, "c"))            // Insert new value
        $(assert.equal(d.size(), 3n))    // Dict should now have 3 elements
        $(assert.equal(d.has(3n), true)) // Confirm new value was added
        $(assert.equal(d.get(3n), "c"))  // Get new value

    });

    test("Dict delete", $ => {

        const d = $.let(new Map([[1n, "a"], [2n, "b"], [3n, "c"]]), DictType(IntegerType, StringType))
        $(d.delete(2n)) // Delete existing value
        $(assert.equal(d.get(2n, () => "missing"), "missing"))
        $(assert.equal(d.size(), 2n))                    // Dict should now have 2 elements
        $(assert.equal(d.has(2n), false))                // Confirm value was deleted
        $(assert.equal(d.has(1n), true))                 // Confirm other values remain

        const d2 = $.let(new Map([[1n, "a"], [2n, "b"], [3n, "c"]]), DictType(IntegerType, StringType))
        $(assert.equal(d2.pop(2n), "b"))
        $(assert.throws(d2.pop(4n)))

    });

    test("Dict get", $ => {
        const d = $.let(new Map([[1n, "a"], [2n, "b"], [3n, "c"]]), DictType(IntegerType, StringType))
        $(assert.equal(d.get(1n, East.function([IntegerType], StringType, (_$, _key) => East.value("missing"))), "a"))                  // Get existing value
        $(assert.equal(d.get(2n, East.function([IntegerType], StringType, (_$, _key) => East.value("missing"))), "b"))                  // Get existing value
        $(assert.equal(d.get(3n, East.function([IntegerType], StringType, (_$, _key) => East.value("missing"))), "c"))                  // Get existing value

        // Test with custom missing handler
        $(assert.equal(d.get(4n, East.function([IntegerType], StringType, (_$, _key) => East.value("default"))), "default"))

    });

    test("Dict update", $ => {
        const d = $.let(new Map([[1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType))

        $(d.update(1n, "a_updated"))          // Update existing value
        $(assert.equal(d.get(1n), "a_updated"))          // Confirm value was updated

        $(assert.throws(d.update(3n, "created")))        // Create new value
        $(assert.equal(d.get(3n, () => "missing"), "missing"))            // Confirm value was notcreated
        $(assert.equal(d.size(), 2n))                    // Dict should still have 2 elements

        $(d.merge(1n, "_and_merged", ($, existing, value) => existing.concat(value)))   // Merge into existing value
        $(assert.equal(d.get(1n), "a_updated_and_merged"))          // Confirm value was updated

        $(assert.throws(d.merge(3n, "new_value", ($, existing, value) => existing.concat(value)))) // Merge into missing value
        $(assert.equal(d.get(3n, () => "missing"), "missing"))            // Confirm value was not created
        $(assert.equal(d.size(), 2n))                    // Dict should still have 2 elements

        // Test with custom missing handler
        $(d.merge(3n, "_and_merged", ($, existing, value) => existing.concat(value), () => "default_created")) // Merge into missing value with handler
        $(assert.equal(d.get(3n), "default_created_and_merged"))            // Confirm value was created
        $(assert.equal(d.size(), 3n))                    // Dict should now have 3 elements

        const d2 = $.let(new Map([[1n, "a"], [2n, "b"], [3n, "c"]]), DictType(IntegerType, StringType))
        $(assert.equal(d2.swap(2n, "B"), "b"))
        $(assert.equal(d2.get(2n), "B"))
        $(assert.throws(d2.swap(4n, "D")))
        $(assert.equal(d2.get(4n, () => "missing"), "missing"))
    });

    test("Merge, union, etc", $ => {
        const d1 = $.let(new Map([[1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType))
        const d2 = $.let(new Map([[2n, "B"], [3n, "C"]]), DictType(IntegerType, StringType))

        $(assert.throws(d1.unionInPlace(d2)))

        const d1b = $.let(new Map([[1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType))

        $(d1b.unionInPlace(d2, ($, v1, v2) => v1.concat("+").concat(v2)))
        $(assert.equal(d1b, new Map([[1n, "a"], [2n, "b+B"], [3n, "C"]])))

        const d3 = $.let(new Map([[1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType))
        const d4 = $.let(new Map([[2n, "B"], [3n, "C"]]), DictType(IntegerType, StringType))

        $(assert.throws(d3.mergeAll(d4, ($, v1, v2) => v1.concat("+").concat(v2))))
        $(assert.equal(d3, new Map([[1n, "a"], [2n, "b+B"]]))); // note that it won't realize the problem until it's edited key 2
        $(d3.mergeAll(d4, ($, v1, v2) => v1.concat("+").concat(v2), () => "default"))
        $(assert.equal(d3, new Map([[1n, "a"], [2n, "b+B+B"], [3n, "default+C"]])));
    });

    test("Comparisons", $ => {
        $(assert.equal(East.value(new Map<bigint, string>(), DictType(IntegerType, StringType)), new Map<bigint, string>()))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])), new Map([[3n, "c"], [1n, "a"], [2n, "b"]])))
        $(assert.notEqual(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])), new Map([[1n, "a"], [2n, "b"], [4n, "d"]])))
        $(assert.notEqual(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])), new Map([[1n, "a"], [2n, "b"]])))

        $(assert.less(East.value(new Map<bigint, string>(), DictType(IntegerType, StringType)), new Map([[1n, "a"]])))
        $(assert.less(East.value(new Map([[1n, "a"], [2n, "b"]])), new Map([[1n, "a"], [2n, "b"], [3n, "c"]])))
        $(assert.less(East.value(new Map([[1n, "a"], [2n, "b"]])), new Map([[1n, "a"], [3n, "c"]])))
        $(assert.less(East.value(new Map([[1n, "a"], [2n, "b"]])), new Map([[2n, "b"], [3n, "c"]])))

        $(assert.lessEqual(East.value(new Map<bigint, string>(), DictType(IntegerType, StringType)), new Map<bigint, string>()))
        $(assert.lessEqual(East.value(new Map([[1n, "a"], [2n, "b"]])), new Map([[1n, "a"], [2n, "b"]])))
        $(assert.lessEqual(East.value(new Map([[1n, "a"], [2n, "b"]])), new Map([[1n, "a"], [2n, "b"], [3n, "c"]])))
        $(assert.lessEqual(East.value(new Map([[1n, "a"], [2n, "b"]])), new Map([[1n, "a"], [3n, "c"]])))

        $(assert.greater(East.value(new Map([[1n, "a"]])), new Map<bigint, string>()))
        $(assert.greater(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])), new Map([[1n, "a"], [2n, "b"]])))
        $(assert.greater(East.value(new Map([[1n, "a"], [3n, "c"]])), new Map([[1n, "a"], [2n, "b"]])))
        $(assert.greater(East.value(new Map([[2n, "b"], [3n, "c"]])), new Map([[1n, "a"], [2n, "b"]])))

        $(assert.greaterEqual(East.value(new Map<bigint, string>(), DictType(IntegerType, StringType)), new Map<bigint, string>()))
        $(assert.greaterEqual(East.value(new Map([[1n, "a"], [2n, "b"]])), new Map([[1n, "a"], [2n, "b"]])))
        $(assert.greaterEqual(East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])), new Map([[1n, "a"], [2n, "b"]])))
        $(assert.greaterEqual(East.value(new Map([[1n, "a"], [3n, "c"]])), new Map([[1n, "a"], [2n, "b"]])))

        // Instance method tests
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).equals(new Map([[1n, "a"], [2n, "b"]])), true))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).equals(new Map([[1n, "a"]])), false))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).notEquals(new Map([[1n, "a"]])), true))
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).notEquals(new Map([[1n, "a"], [2n, "b"]])), false))
    });

    test("Dict keys/copy/filter/map/reduce/etc", $ => {
        // keys
        $(assert.equal(
            East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).keys(),
            new Set([1n, 2n, 3n])
        ))

        // getKeys
        $(assert.equal(
            East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).getKeys(new Set([2n, 3n])),
            new Map([[2n, "b"], [3n, "c"]])
        ))

        // forEach
        {
            const d1 = $.let(new Map([[1n, "a"], [2n, "b"], [3n, "c"]]), DictType(IntegerType, StringType))
            const result = $.let("")
            $(d1.forEach(($, value, key) => $.assign(result, str`${result}${key}:${value};`)))
            $(assert.equal(result, "1:a;2:b;3:c;"))
        }

        // copy
        const d1 = $.let(new Map([[1n, "a"], [2n, "b"], [3n, "c"]]), DictType(IntegerType, StringType))
        const d1_copy = $.let(d1.copy())
        $(assert.equal(d1, d1_copy))
        $(d1.insert(4n, "d"))
        $(assert.notEqual(d1, d1_copy))

        // map
        $(assert.equal(
            East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).map(($, value, key) => str`${key}:${value}`),
            new Map([[1n, "1:a"], [2n, "2:b"], [3n, "3:c"]])
        ))

        // filter
        $(assert.equal(
            East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).filter((_$, _value, key) => East.equal(key.remainder(2n), 1n)),
            new Map([[1n, "a"], [3n, "c"]])
        ))

        // filterMap
        $(assert.equal(
            East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"], [4n, "d"]])).filterMap(($, value, key) => East.equal(key.remainder(2n), 1n).ifElse(_$ => some(str`${key}:${value}`), _$ => none)),
            new Map([[1n, "1:a"], [3n, "3:c"]])
        ))

        // reduce
        $(assert.equal(
            East.value(new Map([[1n, "a"], [2n, "b"], [3n, "c"]])).reduce((_$, previous, value, key) => previous.concat(str`${key}:${value};`), ""),
            "1:a;2:b;3:c;"
        ))

        // common reductions
        $(assert.equal(East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n]])).sum(), 6n))
        $(assert.equal(East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n]])).sum(($, x) => x.add(1n)), 9n))
        $(assert.equal(East.value(new Map([["a", 1.0], ["b", 2.0], ["c", 3.0]])).sum(), 6.0))
        $(assert.equal(East.value(new Map([["a", 1.0], ["b", 2.0], ["c", 3.0]])).sum(($, x) => x.add(1.0)), 9.0))
        $(assert.equal(East.value(new Map(), DictType(StringType, BooleanType)).every(), true))
        $(assert.equal(East.value(new Map([["a", true]])).every(), true))
        $(assert.equal(East.value(new Map([["a", true], ["b", false]])).every(), false))
        $(assert.equal(East.value(new Map(), DictType(StringType, BooleanType)).some(), false))
        $(assert.equal(East.value(new Map([["a", true]])).some(), true))
        $(assert.equal(East.value(new Map([["a", true], ["b", false]])).some(), true))
    });

    test("Dict forEach - iteration guard", $ => {
        const d = $.let(new Map([[1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType));
        $(assert.throws(d.forEach((_$, _value, _key) => d.insert(3n, "c"))));
    });

    test("Dict for loop - iteration guard", $ => {
        const d = $.let(new Map([[1n, "a"], [2n, "b"]]), DictType(IntegerType, StringType));
        $(assert.throws(Expr.block($ => {
            $.for(d, (_$, _key, _value) => d.insert(3n, "c"));
            return null;
        })));
    });

    test("Dict toArray/toDict/toSet", $ => {
        const d1 = $.let(new Map([[1n, "a"], [2n, "b"], [3n, "c"]]), DictType(IntegerType, StringType))

        // toArray
        $(assert.equal(d1.toArray(), ["a", "b", "c"]))
        $(assert.equal(d1.toArray((_$, _x, k) => k.add(1n)), [2n, 3n, 4n]))

        // toSet
        $(assert.equal(d1.toSet((_$, _x, k) => k.add(1n)), new Set([2n, 3n, 4n])))
        $(assert.equal(d1.toSet((_$, _x, _k) => 1n), new Set([1n]))) // mapping function not unique

        // toDict
        $(assert.equal(d1.toDict((_$, x, _k) => x, (_$, _x, k) => k.add(10n)), new Map([["a", 11n], ["b", 12n], ["c", 13n]])))
        $(assert.equal(d1.toDict((_$, _x, k) => East.print(k)), new Map([["1", "a"], ["2", "b"], ["3", "c"]])))
        $(assert.throws(d1.toDict((_$, _x, _k) => 1n))) // key function not unique
        $(assert.equal(d1.toDict((_$, _x, _k) => 1n, (_$, _x, k) => k, (_$, acc, v) => acc.add(v)), new Map([[1n, 6n]]))) // key function not unique, but conflict handler provided
    });

    test("flattenToArray", $ => {
        const a1 = East.value(new Map(), DictType(StringType, IntegerType));
        $(assert.equal(a1.flattenToArray(($, x) => [x, x.add(10n)]), []))

        const a2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n]]), DictType(StringType, IntegerType));
        $(assert.equal(a2.flattenToArray((_$, x) => [x, x.add(10n)]), [1n, 11n, 2n, 12n, 3n, 13n]))
        $(assert.equal(a2.flattenToArray((_$, x) => [x]), [1n, 2n, 3n]))
        $(assert.equal(a2.flattenToArray((_$, _x) => []), []))

        const a3 = East.value(new Map([["a", [1n, 2n, 3n]]]), DictType(StringType, ArrayType(IntegerType)));
        $(assert.equal(a3.flattenToArray(), [1n, 2n, 3n]))

        const a4 = East.value(new Map([["a", [1n, 2n]], ["b", [3n]]]), DictType(StringType, ArrayType(IntegerType)));
        $(assert.equal(a4.flattenToArray(), [1n, 2n, 3n]))

        const a5 = East.value(new Map([["a", [1n, 2n]], ["b", [3n]], ["c", []]]), DictType(StringType, ArrayType(IntegerType)));
        $(assert.equal(a5.flattenToArray(), [1n, 2n, 3n]))
    });

    test("flattenToSet", $ => {
        const a1 = East.value(new Map(), DictType(StringType, IntegerType));
        $(assert.equal(a1.flattenToSet(($, x) => new Set([x, x.add(10n)])), new Set()))

        const a2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n]]), DictType(StringType, IntegerType));
        $(assert.equal(a2.flattenToSet((_$, x) => new Set([x, x.add(10n)])), new Set([1n, 2n, 3n, 11n, 12n, 13n])))
        $(assert.equal(a2.flattenToSet((_$, x) => new Set([x])), new Set([1n, 2n, 3n])))
        $(assert.equal(a2.flattenToSet((_$, _x) => new Set()), new Set()))

        const a3 = East.value(new Map([["a", new Set([1n, 2n, 3n])]]), DictType(StringType, SetType(IntegerType)));
        $(assert.equal(a3.flattenToSet(), new Set([1n, 2n, 3n])))

        const a4 = East.value(new Map([["a", new Set([1n, 2n])], ["b", new Set([3n])]]), DictType(StringType, SetType(IntegerType)));
        $(assert.equal(a4.flattenToSet(), new Set([1n, 2n, 3n])))

        const a5 = East.value(new Map([["a", new Set([1n, 2n])], ["b", new Set([3n])], ["c", new Set<bigint>()]]), DictType(StringType, SetType(IntegerType)));
        $(assert.equal(a5.flattenToSet(), new Set([1n, 2n, 3n])))

        const a6 = East.value(new Map([["a", new Set([1n, 2n])], ["b", new Set([2n, 3n])]]), DictType(StringType, SetType(IntegerType)));
        $(assert.equal(a6.flattenToSet(), new Set([1n, 2n, 3n])))
    });

    test("flattenToDict", $ => {
        const a1 = East.value(new Map(), DictType(StringType, IntegerType));
        $(assert.equal(a1.flattenToDict((_$, x) => new Map([[East.print(x), x], [East.print(x.add(10n)), x.add(10n)]])), new Map()))

        const a2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n]]), DictType(StringType, IntegerType));
        $(assert.equal(a2.flattenToDict((_$, x) => new Map([[East.print(x), x], [East.print(x.add(10n)), x.add(10n)]])), new Map([["1", 1n], ["2", 2n], ["3", 3n], ["11", 11n], ["12", 12n], ["13", 13n]])))
        $(assert.equal(a2.flattenToDict((_$, x) => new Map([[East.print(x), x]])), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))
        $(assert.equal(a2.flattenToDict((_$, _x) => new Map()), new Map()))

        const a3 = East.value(new Map([["a", new Map([["1", 1n], ["2", 2n], ["3", 3n]])]]), DictType(StringType, DictType(StringType, IntegerType)));
        $(assert.equal(a3.flattenToDict(), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))

        const a4 = East.value(new Map([["a", new Map([["1", 1n], ["2", 2n]])], ["b", new Map([["3", 3n]])]]), DictType(StringType, DictType(StringType, IntegerType)));
        $(assert.equal(a4.flattenToDict(), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))

        const a5 = East.value(new Map([["a", new Map([["1", 1n], ["2", 2n]])], ["b", new Map([["3", 3n]])], ["c", new Map<string, bigint>()]]), DictType(StringType, DictType(StringType, IntegerType)));
        $(assert.equal(a5.flattenToDict(), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))

        const a6 = East.value(new Map([["a", new Map([["1", 1n], ["2", 2n]])], ["b", new Map([["2", 20n], ["3", 3n]])]]), DictType(StringType, DictType(StringType, IntegerType)));
        $(assert.throws(a6.flattenToDict()))

        const a7 = East.value(new Map([["a", new Map([["1", 1n], ["2", 2n]])], ["b", new Map([["2", 20n], ["3", 3n]])]]), DictType(StringType, DictType(StringType, IntegerType)));
        $(assert.equal(a7.flattenToDict((_$, x) => x, (_$, x1, x2) => x1.add(x2)), new Map([["1", 1n], ["2", 22n], ["3", 3n]])))
    });

    test("groupSize", $ => {
        const d1 = East.value(new Map(), DictType(StringType, IntegerType));
        const d2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n], ["d", 1n], ["e", 2n]]), DictType(StringType, IntegerType));

        // Empty dictionary
        $(assert.equal(d1.groupSize(), new Map()))
        $(assert.equal(d1.groupSize((_$, v) => v.remainder(2n)), new Map()))

        // Group by identity - count occurrences of each value
        $(assert.equal(d2.groupSize(), new Map([[1n, 2n], [2n, 2n], [3n, 1n]])))

        // Group by even/odd
        $(assert.equal(d2.groupSize((_$, v) => v.remainder(2n)), new Map([[0n, 2n], [1n, 3n]])))

        // Group by key instead of value
        const d3 = East.value(new Map([["apple", 1n], ["apricot", 2n], ["banana", 3n], ["berry", 4n], ["cherry", 5n]]), DictType(StringType, IntegerType));
        $(assert.equal(d3.groupSize((_$, _v, k) => k.substring(0n, 1n)), new Map([["a", 2n], ["b", 2n], ["c", 1n]])))
    })

    test("groupEvery", $ => {
        const d1 = East.value(new Map(), DictType(StringType, IntegerType));
        const d2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n], ["d", 4n], ["e", 5n], ["f", 6n]]), DictType(StringType, IntegerType));

        // Empty dictionary
        $(assert.equal(d1.groupEvery((_$, v) => v.remainder(2n), (_$, v) => East.greater(v, East.value(0n))), new Map()))

        // Group by even/odd, check all are positive
        $(assert.equal(
            d2.groupEvery((_$, v) => v.remainder(2n), (_$, v) => East.greater(v, East.value(0n))),
            new Map([[0n, true], [1n, true]])
        ))

        // Group by even/odd, check all are > 3
        $(assert.equal(
            d2.groupEvery((_$, v) => v.remainder(2n), (_$, v) => East.greater(v, East.value(3n))),
            new Map([[0n, false], [1n, false]])
        ))

        // Check with all groups passing
        const d3 = East.value(new Map([["a", 5n], ["b", 7n], ["c", 9n], ["d", 4n], ["e", 6n], ["f", 8n]]), DictType(StringType, IntegerType));
        $(assert.equal(
            d3.groupEvery((_$, v) => v.remainder(2n), (_$, v) => East.greater(v, East.value(3n))),
            new Map([[0n, true], [1n, true]])
        ))
    })

    test("groupSome", $ => {
        const d1 = East.value(new Map(), DictType(StringType, IntegerType));
        const d2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n], ["d", 4n], ["e", 5n], ["f", 6n]]), DictType(StringType, IntegerType));

        // Empty dictionary
        $(assert.equal(d1.groupSome((_$, v) => v.remainder(2n), (_$, v) => East.greater(v, East.value(4n))), new Map()))

        // Group by even/odd, check if any are > 4
        $(assert.equal(
            d2.groupSome((_$, v) => v.remainder(2n), (_$, v) => East.greater(v, East.value(4n))),
            new Map([[0n, true], [1n, true]])
        ))

        // Group by even/odd, check if any are > 10
        $(assert.equal(
            d2.groupSome((_$, v) => v.remainder(2n), (_$, v) => East.greater(v, East.value(10n))),
            new Map([[0n, false], [1n, false]])
        ))

        // Check with some groups having matches
        const d3 = East.value(new Map([["a", 1n], ["b", 3n], ["c", 5n], ["d", 2n], ["e", 4n], ["f", 10n]]), DictType(StringType, IntegerType));
        $(assert.equal(
            d3.groupSome((_$, v) => v.remainder(2n), (_$, v) => East.greater(v, East.value(8n))),
            new Map([[0n, true], [1n, false]])
        ))
    })

    test("groupSum", $ => {
        const d1 = East.value(new Map(), DictType(StringType, IntegerType));
        const d2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n], ["d", 4n], ["e", 5n], ["f", 6n]]), DictType(StringType, IntegerType));

        // Empty dictionary
        $(assert.equal(d1.groupSum((_$, v) => v.remainder(2n)), new Map()))

        // Group by even/odd, sum values
        $(assert.equal(
            d2.groupSum((_$, v) => v.remainder(2n)),
            new Map([[0n, 12n], [1n, 9n]])
        ))

        // Group by even/odd, sum with projection
        $(assert.equal(
            d2.groupSum((_$, v) => v.remainder(2n), (_$, v) => v.multiply(2n)),
            new Map([[0n, 24n], [1n, 18n]])
        ))

        // Test with floats
        const d3 = East.value(new Map([["a", 1.0], ["b", 2.0], ["c", 3.0], ["d", 4.0]]));
        $(assert.equal(
            d3.groupSum((_$, v) => East.lessEqual(v, East.value(2.0)).ifElse(() => 0n, () => 1n)),
            new Map([[0n, 3.0], [1n, 7.0]])
        ))
    })

    test("groupMean", $ => {
        const d1 = East.value(new Map(), DictType(StringType, IntegerType));
        const d2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n], ["d", 4n], ["e", 5n], ["f", 6n]]), DictType(StringType, IntegerType));

        // Empty dictionary
        $(assert.equal(d1.groupMean((_$, v) => v.remainder(2n)), new Map()))

        // Group by even/odd, compute mean
        $(assert.equal(
            d2.groupMean((_$, v) => v.remainder(2n)),
            new Map([[0n, 4.0], [1n, 3.0]])
        ))

        // Group by even/odd, mean with projection
        $(assert.equal(
            d2.groupMean((_$, v) => v.remainder(2n), (_$, v) => v.multiply(2n)),
            new Map([[0n, 8.0], [1n, 6.0]])
        ))
    })

    test("groupReduce", $ => {
        const d1 = East.value(new Map(), DictType(StringType, IntegerType));
        const d2 = East.value(new Map([["a", 1n], ["b", 2n], ["c", 3n]]), DictType(StringType, IntegerType));

        // Empty dictionary
        $(assert.equal(d1.groupReduce((_$, v, _k) => v.remainder(2n), (_$, _k2) => 10n, (_$, a, b, _k) => a.add(b)), new Map()))

        // Basic grouping by even/odd with custom init
        $(assert.equal(d2.groupReduce((_$, v, _k) => v.remainder(2n), (_$, _k2) => 10n, (_$, a, b, _k) => a.add(b)), new Map([[0n, 12n], [1n, 14n]])))
        // even: init=10, then 10+2=12
        // odd:  init=10, then 10+1+3=14

        // Single element per group - verifies initFn is called and element is added
        const d3 = East.value(new Map([["a", 1n], ["b", 2n]]), DictType(StringType, IntegerType));
        $(assert.equal(
            d3.groupReduce((_$, v) => v, (_$, k) => k.multiply(10n), (_$, a, b) => a.add(b)),
            new Map([[1n, 11n], [2n, 22n]])
        ))
        // key 1: init=1*10=10, then 10+1=11
        // key 2: init=2*10=20, then 20+2=22

        // Verify initFn receives correct key and is used
        const d4 = East.value(new Map([["a", 1n], ["b", 1n], ["c", 2n], ["d", 2n], ["e", 2n]]), DictType(StringType, IntegerType));
        $(assert.equal(
            d4.groupReduce((_$, v) => v, (_$, k) => k.multiply(100n), (_$, a, b) => a.add(b)),
            new Map([[1n, 102n], [2n, 206n]])
        ))
        // key 1: init=100, then 100+1+1=102
        // key 2: init=200, then 200+2+2+2=206

        // String keys with concatenation
        const d5 = East.value(new Map([["apple", 5n], ["apricot", 7n], ["banana", 3n], ["berry", 8n]]), DictType(StringType, IntegerType));
        $(assert.equal(
            d5.groupReduce(
                (_$, _v, k) => k.substring(0n, 1n),
                (_$, letter) => Expr.str`[${letter}]: `,
                (_$, acc, v, k) => Expr.str`${acc}${k}=${Expr.print(v)}, `
            ),
            new Map([["a", "[a]: apple=5, apricot=7, "], ["b", "[b]: banana=3, berry=8, "]])
        ))
    })

    test("Equality method aliases", $ => {
        // Test short aliases (eq, ne)
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).eq(new Map([[1n, "a"], [2n, "b"]])), true));
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).eq(new Map([[1n, "a"]])), false));
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).ne(new Map([[1n, "a"]])), true));
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).ne(new Map([[1n, "a"], [2n, "b"]])), false));

        // Test medium aliases (equal, notEqual)
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).equal(new Map([[1n, "a"], [2n, "b"]])), true));
        $(assert.equal(East.value(new Map([[1n, "a"], [2n, "b"]])).notEqual(new Map([[1n, "a"]])), true));
    });
});
