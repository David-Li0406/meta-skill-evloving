/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, Expr, IntegerType, SetType, StringType, some, none, DictType, BooleanType, StructType } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Set", (test) => {
    test("Set ops", $ => {
        $(assert.equal(East.value(new Set([]), SetType(IntegerType)).size(), 0n))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).size(), 3n))

        $(assert.equal(East.value(new Set([1n, 2n, 3n])).has(0n), false))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).has(1n), true))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).has(2n), true))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).has(3n), true))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).has(4n), false))

        $(assert.equal(East.Set.generate(6n, IntegerType, (_$, i) => i.add(1n)), new Set([1n, 2n, 3n, 4n, 5n, 6n])));
        $(assert.throws(East.Set.generate(6n, IntegerType, (_$, _i) => 0n)));
    });

    test("Set insert", $ => {
        const s = $.let(new Set([1n, 2n]), SetType(IntegerType))
        $(assert.equal(s.tryInsert(3n), true))       // Try insert new value
        $(assert.equal(s.tryInsert(1n), false))      // Try insert existing value
        $(assert.throws(s.insert(1n)))                // Insert existing value, error
        $(assert.equal(s.size(), 3n))                // Set should now have 3 elements
    });

    test("Set delete", $ => {
        const s = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType))
        $(assert.equal(s.tryDelete(2n), true))          // Delete existing value
        $(assert.equal(s.tryDelete(4n), false))         // Delete non-existing value (default: return false)
        $(assert.equal(s.size(), 2n))                // Set should now have 2 elements
        $(assert.equal(s.has(2n), false))            // Confirm value was deleted
        $(assert.equal(s.has(1n), true))             // Confirm other values remain
    });

    test("Set union", $ => {
        const s1 = $.let(new Set([1n, 2n]), SetType(IntegerType))
        const s2 = $.let(new Set([2n, 3n, 4n]), SetType(IntegerType))
        const result = s1.union(s2)
        
        $(assert.equal(result.size(), 4n))                // Union should have 4 elements (1, 2, 3, 4)
        $(assert.equal(result.has(1n), true))             // Should contain all elements from s1
        $(assert.equal(result.has(2n), true))             
        $(assert.equal(result.has(3n), true))             // Should contain all elements from s2
        $(assert.equal(result.has(4n), true))
        $(assert.equal(result.has(5n), false))            // Should not contain elements not in either set

        // Test union with empty set
        const empty = $.let(new Set<bigint>(), SetType(IntegerType))
        const union_with_empty = s1.union(empty)
        $(assert.equal(union_with_empty.size(), 2n))      // Union with empty should be unchanged
        $(assert.equal(union_with_empty.has(1n), true))   
        $(assert.equal(union_with_empty.has(2n), true))   

        // Test union with self
        const self_union = s1.union(s1.copy())
        $(assert.equal(self_union.size(), 2n))       // Union with self should be unchanged
        $(assert.equal(self_union.has(1n), true))
        $(assert.equal(self_union.has(2n), true))

        $(empty.unionInPlace(s1))                             // Merge s1 into empty set
        $(assert.equal(empty.size(), 2n))                  // Empty set should now have elements from s1
        $(assert.equal(empty.has(1n), true))   
        $(assert.equal(empty.has(2n), true))
    });

    test("Set intersection", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType))
        const s2 = $.let(new Set([2n, 3n, 4n]), SetType(IntegerType))
        const result = s1.intersection(s2)
        
        $(assert.equal(result.size(), 2n))                // Intersection should have 2 elements (2, 3)
        $(assert.equal(result.has(1n), false))            // 1 is only in s1
        $(assert.equal(result.has(2n), true))             // 2 is in both
        $(assert.equal(result.has(3n), true))             // 3 is in both
        $(assert.equal(result.has(4n), false))            // 4 is only in s2

        // Test intersection with empty set
        const empty = $.let(new Set<bigint>(), SetType(IntegerType))
        const intersection_with_empty = s1.intersection(empty)
        $(assert.equal(intersection_with_empty.size(), 0n))      // Intersection with empty should be empty

        // Test intersection with self
        const self_intersection = s1.intersection(s1)
        $(assert.equal(self_intersection.size(), 3n))            // Intersection with self should be unchanged
        $(assert.equal(self_intersection.has(1n), true))
        $(assert.equal(self_intersection.has(2n), true))
        $(assert.equal(self_intersection.has(3n), true))
    });

    test("Set difference", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType))
        const s2 = $.let(new Set([2n, 3n, 4n]), SetType(IntegerType))
        const result = s1.difference(s2)
        
        $(assert.equal(result.size(), 1n))                // Difference should have 1 element (1)
        $(assert.equal(result.has(1n), true))             // 1 is in s1 but not s2
        $(assert.equal(result.has(2n), false))            // 2 is in both (excluded)
        $(assert.equal(result.has(3n), false))            // 3 is in both (excluded)
        $(assert.equal(result.has(4n), false))            // 4 is only in s2 (excluded)

        // Test difference with empty set
        const empty = $.let(new Set<bigint>(), SetType(IntegerType))
        const diff_with_empty = s1.difference(empty)
        $(assert.equal(diff_with_empty.size(), 3n))       // Difference with empty should be unchanged
        $(assert.equal(diff_with_empty.has(1n), true))
        $(assert.equal(diff_with_empty.has(2n), true))
        $(assert.equal(diff_with_empty.has(3n), true))

        // Test difference with self
        const self_difference = s1.difference(s1)
        $(assert.equal(self_difference.size(), 0n))       // Difference with self should be empty
    });

    test("Set symmetric difference", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType))
        const s2 = $.let(new Set([2n, 3n, 4n, 5n]), SetType(IntegerType))
        const result = s1.symmetricDifference(s2)
        
        $(assert.equal(result.size(), 3n))                // Symmetric difference should have 3 elements (1, 4, 5)
        $(assert.equal(result.has(1n), true))             // 1 is only in s1
        $(assert.equal(result.has(2n), false))            // 2 is in both (excluded)
        $(assert.equal(result.has(3n), false))            // 3 is in both (excluded)
        $(assert.equal(result.has(4n), true))             // 4 is only in s2
        $(assert.equal(result.has(5n), true))             // 5 is only in s2

        // Test symmetric difference with empty set
        const empty = $.let(new Set<bigint>(), SetType(IntegerType))
        const symdiff_with_empty = s1.symmetricDifference(empty)
        $(assert.equal(symdiff_with_empty.size(), 3n))    // Symmetric difference with empty should be unchanged
        $(assert.equal(symdiff_with_empty.has(1n), true))
        $(assert.equal(symdiff_with_empty.has(2n), true))
        $(assert.equal(symdiff_with_empty.has(3n), true))

        // Test symmetric difference with self
        const self_symdiff = s1.symmetricDifference(s1)
        $(assert.equal(self_symdiff.size(), 0n))          // Symmetric difference with self should be empty
    });

    test("Set subset predicates", $ => {
        const s1 = $.let(new Set([1n, 2n]), SetType(IntegerType))          // {1, 2}
        const s2 = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType))      // {1, 2, 3}
        const s3 = $.let(new Set([2n, 3n, 4n]), SetType(IntegerType))      // {2, 3, 4}
        const empty = $.let(new Set<bigint>(), SetType(IntegerType))        // {}
        
        // Subset tests
        $(assert.equal(s1.isSubsetOf(s2), true))          // {1, 2} ⊆ {1, 2, 3}
        $(assert.equal(s2.isSubsetOf(s1), false))         // {1, 2, 3} ⊄ {1, 2}
        $(assert.equal(s1.isSubsetOf(s3), false))         // {1, 2} ⊄ {2, 3, 4}
        $(assert.equal(s1.isSubsetOf(s1), true))          // {1, 2} ⊆ {1, 2} (reflexive)
        $(assert.equal(empty.isSubsetOf(s1), true))       // {} ⊆ {1, 2} (empty set is subset of all sets)
        $(assert.equal(s1.isSubsetOf(empty), false))      // {1, 2} ⊄ {}

        // Superset tests  
        $(assert.equal(s2.isSupersetOf(s1), true))        // {1, 2, 3} ⊇ {1, 2}
        $(assert.equal(s1.isSupersetOf(s2), false))       // {1, 2} ⊅ {1, 2, 3}
        $(assert.equal(s3.isSupersetOf(s1), false))       // {2, 3, 4} ⊅ {1, 2}
        $(assert.equal(s1.isSupersetOf(s1), true))        // {1, 2} ⊇ {1, 2} (reflexive)
        $(assert.equal(s1.isSupersetOf(empty), true))     // {1, 2} ⊇ {} (all sets are superset of empty)
        $(assert.equal(empty.isSupersetOf(s1), false))    // {} ⊅ {1, 2}
    });

    test("Set disjoint predicates", $ => {
        const s1 = $.let(new Set([1n, 2n]), SetType(IntegerType))          // {1, 2}
        const s2 = $.let(new Set([3n, 4n]), SetType(IntegerType))          // {3, 4}
        const s3 = $.let(new Set([2n, 3n]), SetType(IntegerType))          // {2, 3}
        const empty = $.let(new Set<bigint>(), SetType(IntegerType))        // {}
        
        // Disjoint tests
        $(assert.equal(s1.isDisjointFrom(s2), true))      // {1, 2} and {3, 4} are disjoint
        $(assert.equal(s2.isDisjointFrom(s1), true))      // Symmetrical
        $(assert.equal(s1.isDisjointFrom(s3), false))     // {1, 2} and {2, 3} share element 2
        $(assert.equal(s3.isDisjointFrom(s1), false))     // Symmetrical
        $(assert.equal(s1.isDisjointFrom(s1), false))     // Set is not disjoint from itself (unless empty)
        $(assert.equal(empty.isDisjointFrom(s1), true))   // Empty set is disjoint from all sets
        $(assert.equal(s1.isDisjointFrom(empty), true))   // Symmetrical
        $(assert.equal(empty.isDisjointFrom(empty), true)) // Empty set is disjoint from itself
    });

    test("Printing", $ => {
        $(assert.equal(East.print(East.value(new Set<bigint>(), SetType(IntegerType))), "{}"))
        $(assert.equal(East.print(East.value(new Set([1n]), SetType(IntegerType))), "{1}"))
        $(assert.equal(East.print(East.value(new Set([1n, 2n, 3n]), SetType(IntegerType))), "{1,2,3}"))
        $(assert.equal(East.print(East.value(new Set([3n, 1n, 2n]), SetType(IntegerType))), "{1,2,3}"))
        $(assert.equal(East.print(East.value(new Set(["a", "c", "b"]), SetType(StringType))), "{\"a\",\"b\",\"c\"}"))
    });

    test("Parsing", $ => {
        $(assert.equal(East.value("{}").parse(SetType(IntegerType)), new Set<bigint>([])))
        $(assert.equal(East.value("{1}").parse(SetType(IntegerType)), new Set([1n])))
        $(assert.equal(East.value("{1,2,3}").parse(SetType(IntegerType)), new Set([1n, 2n, 3n])))
        $(assert.equal(East.value("{3,1,2}").parse(SetType(IntegerType)), new Set([1n, 2n, 3n])))
        $(assert.equal(East.value("{\"a\",\"b\",\"c\"}").parse(SetType(StringType)), new Set(["a", "b", "c"])))
        $(assert.throws(East.value("{1,2,}").parse(SetType(IntegerType))))
        $(assert.throws(East.value("{1,,2}").parse(SetType(IntegerType))))
        $(assert.throws(East.value("[1,2,3]").parse(SetType(IntegerType))))
    });

    test("Comparisons", $ => {
        $(assert.equal(East.value(new Set<bigint>(), SetType(IntegerType)), new Set<bigint>()))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])), new Set([3n, 1n, 2n])))
        $(assert.notEqual(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n, 4n])))
        $(assert.notEqual(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n])))

        $(assert.less(East.value(new Set<bigint>(), SetType(IntegerType)), new Set([1n])))
        $(assert.less(East.value(new Set([1n, 2n])), new Set([1n, 2n, 3n])))
        $(assert.less(East.value(new Set([1n, 2n])), new Set([1n, 3n])))
        $(assert.less(East.value(new Set([1n, 2n])), new Set([2n, 3n])))

        $(assert.lessEqual(East.value(new Set<bigint>(), SetType(IntegerType)), new Set<bigint>()))
        $(assert.lessEqual(East.value(new Set([1n, 2n])), new Set([1n, 2n])))
        $(assert.lessEqual(East.value(new Set([1n, 2n])), new Set([1n, 2n, 3n])))
        $(assert.lessEqual(East.value(new Set([1n, 2n])), new Set([1n, 3n])))

        $(assert.greater(East.value(new Set([1n])), new Set<bigint>()))
        $(assert.greater(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n])))
        $(assert.greater(East.value(new Set([1n, 3n])), new Set([1n, 2n])))
        $(assert.greater(East.value(new Set([2n, 3n])), new Set([1n, 2n])))

        $(assert.greaterEqual(East.value(new Set<bigint>(), SetType(IntegerType)), new Set<bigint>()))
        $(assert.greaterEqual(East.value(new Set([1n, 2n])), new Set([1n, 2n])))
        $(assert.greaterEqual(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n])))
        $(assert.greaterEqual(East.value(new Set([1n, 3n])), new Set([1n, 2n])))

        // Instance method tests
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).equals(new Set([1n, 2n, 3n])), true))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).equals(new Set([1n, 2n])), false))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).notEquals(new Set([1n, 2n])), true))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).notEquals(new Set([1n, 2n, 3n])), false))
    });

    test("Set map/filter/reduce/etc", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType))
        $(assert.equal(s1.copy(), new Set([1n, 2n, 3n])))

        // filter
        $(assert.equal(s1.filter(($, x) => East.equal(x.remainder(2n), 1n)), new Set([1n, 3n])))
        $(assert.equal(s1.filter(($, x) => East.greater(x, 3n)), new Set<bigint>()))

        // forEach
        const acc = $.let(0n, IntegerType)
        $(s1.forEach(($, x) => $.assign(acc, acc.add(x))))
        $(assert.equal(acc, 6n))

        // map
        const dict = s1.map(($, x) => East.print(x))
        $(assert.equal(dict, new Map([[1n, "1"], [2n, "2"], [3n, "3"]])))

        // reduce
        const sum = $.let(s1.reduce(($, acc, x) => acc.add(x), 0n))
        $(assert.equal(sum, 6n))
        const product = $.let(s1.reduce(($, acc, x) => acc.multiply(x), 1n))
        $(assert.equal(product, 6n))

        // common reductions
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).sum(), 6n))
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).sum(($, x) => x.add(1n)), 9n))
        $(assert.equal(East.value(new Set([1.0, 2.0, 3.0])).sum(), 6.0))
        $(assert.equal(East.value(new Set([1.0, 2.0, 3.0])).sum(($, x) => x.add(1.0)), 9.0))
        $(assert.equal(East.value(new Set([]), SetType(BooleanType)).every(), true))
        $(assert.equal(East.value(new Set([true])).every(), true))
        $(assert.equal(East.value(new Set([true, false])).every(), false))
        $(assert.equal(East.value(new Set([]), SetType(BooleanType)).some(), false))
        $(assert.equal(East.value(new Set([true])).some(), true))
        $(assert.equal(East.value(new Set([true, false])).some(), true))
    });

    test("Set filterMap", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n, 4n, 5n]), SetType(IntegerType))

        // Filter to even numbers and map to their string representation
        const result1 = s1.filterMap(($, x) =>
            East.equal(x.remainder(2n), 0n).ifElse(
                () => some(East.print(x)),
                () => none
            )
        )
        $(assert.equal(result1, new Map([[2n, "2"], [4n, "4"]])))

        // Filter to numbers > 3 and map to their square
        const result2 = s1.filterMap(($, x) =>
            East.greater(x, 3n).ifElse(
                () => some(x.multiply(x)),
                () => none
            )
        )
        $(assert.equal(result2, new Map([[4n, 16n], [5n, 25n]])))

        // Filter that excludes everything
        const result3 = s1.filterMap(($, x) =>
            East.greater(x, 10n).ifElse(
                () => some(x),
                () => none
            )
        )
        $(assert.equal(result3, East.value(new Map<bigint, bigint>(), DictType(IntegerType, IntegerType))))

        // Filter that includes everything
        const result4 = s1.filterMap(($, x) => East.value(true).ifElse(() => some(x.add(10n)), () => none))
        $(assert.equal(result4, new Map([[1n, 11n], [2n, 12n], [3n, 13n], [4n, 14n], [5n, 15n]])))
    });

    test("Set firstMap", $ => {
        // Empty set returns none
        $(assert.equal(East.value(new Set<bigint>(), SetType(IntegerType)).firstMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(East.print(x)), () => none)), none))

        // No matches returns none
        $(assert.equal(East.value(new Set([2n, 4n, 6n])).firstMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(East.print(x)), () => none)), none))

        // First match found - returns some with the first value (set iteration order is sorted)
        $(assert.equal(East.value(new Set([1n, 2n, 3n, 4n, 5n, 6n])).firstMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(East.print(x)), () => none)), some("1")))

        // Multiple matches - returns first some (tests early termination)
        $(assert.equal(East.value(new Set([2n, 4n, 5n, 7n, 9n])).firstMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(x.multiply(10n)), () => none)), some(50n)))

        // Type conversion case
        $(assert.equal(East.value(new Set([10n, 20n, 30n])).firstMap(($, x) => East.greater(x, 15n).ifElse(() => some(East.print(x)), () => none)), some("20")))
    });

    test("Set mapReduce", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n, 4n, 5n]), SetType(IntegerType))

        // Sum of squares: 1 + 4 + 9 + 16 + 25 = 55
        const result1 = s1.mapReduce(
            ($, x) => x.multiply(x),
            ($, a, b) => a.add(b)
        )
        $(assert.equal(result1, 55n))

        // Product of incremented values: 2 * 3 * 4 * 5 * 6 = 720
        const result2 = s1.mapReduce(
            ($, x) => x.add(1n),
            ($, a, b) => a.multiply(b)
        )
        $(assert.equal(result2, 720n))

        // Concatenate string representations
        const s2 = $.let(new Set([3n, 1n, 2n]), SetType(IntegerType))
        const result3 = s2.mapReduce(
            ($, x) => East.print(x),
            ($, a, b) => a.concat(b)
        )
        $(assert.equal(result3, "123"))

        // Find maximum by keeping larger value
        const result4 = s1.mapReduce(
            ($, x) => x,
            ($, a, b) => East.max(a, b)
        )
        $(assert.equal(result4, 5n))

        // Empty set should error
        const emptySet = $.let(new Set<bigint>(), SetType(IntegerType))
        $(assert.throws(emptySet.mapReduce(
            ($, x) => x,
            ($, a, b) => a.add(b)
        )))
    });

    test("Set forEach - iteration guard", $ => {
        const s = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType));
        $(assert.throws(s.forEach((_$, _x) => s.insert(4n))));
    });

    test("Set for loop - iteration guard", $ => {
        const s = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType));
        $(assert.throws(Expr.block($ => {
            $.for(s, (_$, _key) => s.insert(4n));
            return null;
        })));
    });

    test("Set toArray/toDict/toSet", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType))

        // toArray
        $(assert.equal(s1.toArray(), [1n, 2n, 3n]))
        $(assert.equal(s1.toArray(($, x) => x.add(1n)), [2n, 3n, 4n]))

        // toDict
        $(assert.equal(s1.toDict((_$, x) => East.print(x), (_$, x) => x.add(10n)), new Map([["1", 11n], ["2", 12n], ["3", 13n]])))
        $(assert.equal(s1.toDict((_$, x) => East.print(x)), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))
        $(assert.throws(s1.toDict((_$, _x) => 1n))) // key function not unique
        $(assert.equal(s1.toDict((_$, _x) => 1n, (_$, x) => x, (_$, acc, v) => acc.add(v)), new Map([[1n, 6n]]))) // key function not unique, but conflict handler provided

        // toSet
        $(assert.equal(s1.toSet((_$, x) => x.add(1n)), new Set([2n, 3n, 4n])))
        $(assert.equal(s1.toSet((_$, _x) => 1n), new Set([1n]))) // mapping function not unique
    });

    test("Set toSet with type change", $ => {
        // Test toSet projection to a different type (verifies bug fix for type_parameters)
        const PersonType = StructType({ name: StringType, age: IntegerType });
        const people = $.let(new Set([
            { name: "Alice", age: 30n },
            { name: "Bob", age: 25n },
            { name: "Charlie", age: 30n }
        ]), SetType(PersonType));

        // Project Struct → String (extract names)
        $(assert.equal(people.toSet(($, p) => p.name), new Set(["Alice", "Bob", "Charlie"])));

        // Project Struct → Integer (extract ages, with duplicates collapsed)
        $(assert.equal(people.toSet(($, p) => p.age), new Set([30n, 25n])));

        // Project Integer → String
        const nums = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType));
        $(assert.equal(nums.toSet(($, n) => East.print(n)), new Set(["1", "2", "3"])));
    });

    test("Set flattenToArray/flattenToDict/flatenToSet", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n]), SetType(IntegerType))

        // toArray
        $(assert.equal(s1.flattenToArray((_$, x) => East.Array.range(0n, x)), [0n, 0n, 1n, 0n, 1n, 2n]))

        // toSet
        $(assert.equal(s1.flattenToSet((_$, x) => East.Array.range(0n, x).toSet()), new Set([0n, 1n, 2n])))

        // toDict
        $(assert.throws(s1.flattenToDict((_$, x) => East.Array.range(0n, x).toDict(($, y) => East.print(y), (_$, y) => y.add(10n)))))
        $(assert.equal(s1.flattenToDict((_$, x) => East.Array.range(0n, x).toDict(($, y) => East.str`${x}:${y}`, (_$, _y) => x.add(10n))), new Map([["1:0", 11n], ["2:0", 12n], ["2:1", 12n], ["3:0", 13n], ["3:1", 13n], ["3:2", 13n]])))
        $(assert.equal(s1.flattenToDict((_$, x) => East.Array.range(0n, x).toDict(($, y) => East.print(y), (_$, _y) => x.add(10n)), (_$, y1, y2) => y1.add(y2)), new Map([["0", 36n], ["1", 25n], ["2", 13n]])))
    });

    test("groupReduce", $ => {
        const s1 = East.value(new Set<bigint>(), SetType(IntegerType));
        const s2 = East.value(new Set([1n, 2n, 3n]), SetType(IntegerType));

        // Empty set
        $(assert.equal(s1.groupReduce((_$, x) => x.remainder(2n), (_$, _k2) => 10n, (_$, a, b) => a.add(b)), new Map()))

        // Basic grouping by even/odd with custom init
        $(assert.equal(s2.groupReduce((_$, x) => x.remainder(2n), (_$, _k2) => 10n, (_$, a, b) => a.add(b)), new Map([[0n, 12n], [1n, 14n]])))
        // even: init=10, then 10+2=12
        // odd:  init=10, then 10+1+3=14

        // Single element per group - verifies initFn is called and element is added
        const s3 = East.value(new Set([1n, 2n]), SetType(IntegerType));
        $(assert.equal(
            s3.groupReduce((_$, x) => x, (_$, k) => k.multiply(10n), (_$, a, b) => a.add(b)),
            new Map([[1n, 11n], [2n, 22n]])
        ))
        // key 1: init=1*10=10, then 10+1=11
        // key 2: init=2*10=20, then 20+2=22

        // Verify initFn receives correct key and is used
        const s4 = East.value(new Set([1n, 2n]), SetType(IntegerType));
        $(assert.equal(
            s4.groupReduce((_$, x) => x, (_$, k) => k.multiply(100n), (_$, a, b) => a.add(b)),
            new Map([[1n, 101n], [2n, 202n]])
        ))
        // key 1: init=100, then 100+1=101
        // key 2: init=200, then 200+2=202

        // String keys with concatenation
        const s5 = East.value(new Set(["apple", "apricot", "banana", "berry"]), SetType(StringType));
        $(assert.equal(
            s5.groupReduce(
                (_$, word) => word.substring(0n, 1n),
                (_$, letter) => Expr.str`[${letter}]: `,
                (_$, acc, word) => Expr.str`${acc}${word}, `
            ),
            new Map([["a", "[a]: apple, apricot, "], ["b", "[b]: banana, berry, "]])
        ))
    })

    test("groupSize", $ => {
        const s1 = East.value(new Set<bigint>(), SetType(IntegerType));
        const s2 = East.value(new Set([1n, 2n, 3n, 1n, 2n]), SetType(IntegerType)); // Duplicates ignored in sets

        // Empty set
        $(assert.equal(s1.groupSize(), new Map()))
        $(assert.equal(s1.groupSize((_$, x) => x.remainder(2n)), new Map()))

        // Group by identity - count occurrences (sets have unique elements)
        $(assert.equal(s2.groupSize(), new Map([[1n, 1n], [2n, 1n], [3n, 1n]])))

        // Group by even/odd
        $(assert.equal(s2.groupSize((_$, x) => x.remainder(2n)), new Map([[0n, 1n], [1n, 2n]])))

        // Group strings by first letter
        const s3 = East.value(new Set(["apple", "apricot", "banana", "berry", "cherry"]), SetType(StringType));
        $(assert.equal(s3.groupSize((_$, w) => w.substring(0n, 1n)), new Map([["a", 2n], ["b", 2n], ["c", 1n]])))
    })

    test("groupEvery", $ => {
        const s1 = East.value(new Set<bigint>(), SetType(IntegerType));
        const s2 = East.value(new Set([1n, 2n, 3n, 4n, 5n, 6n]), SetType(IntegerType));

        // Empty set
        $(assert.equal(s1.groupEvery((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 0n)), new Map()))

        // Group by even/odd, check all are positive
        $(assert.equal(
            s2.groupEvery((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 0n)),
            new Map([[0n, true], [1n, true]])
        ))

        // Group by even/odd, check all are > 3
        $(assert.equal(
            s2.groupEvery((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 3n)),
            new Map([[0n, false], [1n, false]])
        ))

        // Check with all groups passing
        const s3 = East.value(new Set([5n, 7n, 9n, 4n, 6n, 8n]), SetType(IntegerType));
        $(assert.equal(
            s3.groupEvery((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 3n)),
            new Map([[0n, true], [1n, true]])
        ))
    })

    test("groupSome", $ => {
        const s1 = East.value(new Set<bigint>(), SetType(IntegerType));
        const s2 = East.value(new Set([1n, 2n, 3n, 4n, 5n, 6n]), SetType(IntegerType));

        // Empty set
        $(assert.equal(s1.groupSome((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 4n)), new Map()))

        // Group by even/odd, check if any are > 4
        $(assert.equal(
            s2.groupSome((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 4n)),
            new Map([[0n, true], [1n, true]])
        ))

        // Group by even/odd, check if any are > 10
        $(assert.equal(
            s2.groupSome((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 10n)),
            new Map([[0n, false], [1n, false]])
        ))

        // Check with some groups having matches
        const s3 = East.value(new Set([1n, 3n, 5n, 2n, 4n, 10n]), SetType(IntegerType));
        $(assert.equal(
            s3.groupSome((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 8n)),
            new Map([[0n, true], [1n, false]])
        ))
    })

    test("groupSum", $ => {
        const s1 = East.value(new Set<bigint>(), SetType(IntegerType));
        const s2 = East.value(new Set([1n, 2n, 3n, 4n, 5n, 6n]), SetType(IntegerType));

        // Empty set
        $(assert.equal(s1.groupSum((_$, x) => x.remainder(2n)), new Map()))

        // Group by even/odd, sum values
        $(assert.equal(
            s2.groupSum((_$, x) => x.remainder(2n)),
            new Map([[0n, 12n], [1n, 9n]])
        ))

        // Group by even/odd, sum with projection
        $(assert.equal(
            s2.groupSum((_$, x) => x.remainder(2n), (_$, x) => x.multiply(2n)),
            new Map([[0n, 24n], [1n, 18n]])
        ))

        // Test with floats
        const s3 = East.value(new Set([1.0, 2.0, 3.0, 4.0]));
        $(assert.equal(
            s3.groupSum((_$, x) => East.lessEqual(x, 2.0).ifElse(() => 0n, () => 1n)),
            new Map([[0n, 3.0], [1n, 7.0]])
        ))
    })

    test("groupMean", $ => {
        const s1 = East.value(new Set<bigint>(), SetType(IntegerType));
        const s2 = East.value(new Set([1n, 2n, 3n, 4n, 5n, 6n]), SetType(IntegerType));

        // Empty set
        $(assert.equal(s1.groupMean((_$, x) => x.remainder(2n)), new Map()))

        // Group by even/odd, compute mean
        $(assert.equal(
            s2.groupMean((_$, x) => x.remainder(2n)),
            new Map([[0n, 4.0], [1n, 3.0]])
        ))

        // Group by even/odd, mean with projection
        $(assert.equal(
            s2.groupMean((_$, x) => x.remainder(2n), (_$, x) => x.multiply(2n)),
            new Map([[0n, 8.0], [1n, 6.0]])
        ))
    })

    test("Equality method aliases", $ => {
        // Test short aliases (eq, ne)
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).eq(new Set([1n, 2n, 3n])), true));
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).eq(new Set([1n, 2n])), false));
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).ne(new Set([1n, 2n])), true));
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).ne(new Set([1n, 2n, 3n])), false));

        // Test medium aliases (equal, notEqual)
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).equal(new Set([1n, 2n, 3n])), true));
        $(assert.equal(East.value(new Set([1n, 2n, 3n])).notEqual(new Set([1n, 2n])), true));
    });
});
