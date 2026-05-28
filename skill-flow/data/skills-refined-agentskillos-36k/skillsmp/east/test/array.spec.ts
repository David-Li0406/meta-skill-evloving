/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { East, Expr, ArrayType, IntegerType, FloatType, StringType, BooleanType, BlobType, some, none, SetType, DictType, StructType, VariantType, NullType, variant, RecursiveType } from "../src/index.js";
import type { ExprType, option, SubtypeExprOrValue } from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Array", (test) => {
    test("Array ops", $ => {
        $(assert.equal(East.value([], ArrayType(IntegerType)).size(), 0n))
        $(assert.equal(East.value([1n, 2n, 3n]).size(), 3n))

        $(assert.equal(East.value([], ArrayType(IntegerType)).length(), 0n))
        $(assert.equal(East.value([1n, 2n, 3n]).length(), 3n))

        $(assert.equal(East.value([10n, 20n, 30n]).has(-1n), false))
        $(assert.equal(East.value([10n, 20n, 30n]).has(0n), true))
        $(assert.equal(East.value([10n, 20n, 30n]).has(1n), true))
        $(assert.equal(East.value([10n, 20n, 30n]).has(2n), true))
        $(assert.equal(East.value([10n, 20n, 30n]).has(3n), false))

        $(assert.throws(East.value([10n, 20n, 30n]).get(-1n)))
        $(assert.equal(East.value([10n, 20n, 30n]).get(0n), 10n))
        $(assert.equal(East.value([10n, 20n, 30n]).get(1n), 20n))
        $(assert.equal(East.value([10n, 20n, 30n]).get(2n), 30n))
        $(assert.throws(East.value([10n, 20n, 30n]).get(3n)))

        $(assert.equal(East.value([10n, 20n, 30n]).get(3n, _ => 40n), 40n))

        $(assert.equal(East.value([10n, 20n, 30n]).tryGet(2n), some(30n)))
        $(assert.equal(East.value([10n, 20n, 30n]).tryGet(3n), none))
    });

    test("Mutation", $ => {
        const a = $.let([], ArrayType(IntegerType))
        $(assert.equal(a, []))

        $(a.pushLast(1n))
        $(assert.equal(a, [1n]))

        $(a.pushLast(2n))
        $(assert.equal(a, [1n, 2n]))

        $(a.pushFirst(0n))
        $(assert.equal(a, [0n, 1n, 2n]))

        $(assert.equal(a.popFirst(), 0n))
        $(assert.equal(a, [1n, 2n]))

        $(assert.equal(a.popLast(), 2n))
        $(assert.equal(a, [1n]))

        $(a.merge(0n, East.value(10n), ($, existing, newValue) => existing.add(newValue)))
        $(assert.equal(a, [11n]))

        const a2 = $.let([1n, 2n, 3n]);
        $(a2.mergeAll(East.value([10n, 10n, 10n]), ($, existing, newValue) => existing.add(newValue)))
        $(assert.equal(a2, [11n, 12n, 13n]))


    });

    test("Sorting", $ => {
        const a = $.let([2n, 3n, 1n]);
        $(assert.equal(a.isSorted(), false))
        $(assert.equal(a.sort(), [1n, 2n, 3n]))
        $(assert.equal(a.sort(($, x) => x.negate()), [3n, 2n, 1n]))
        $(assert.equal(a.reverse(), [1n, 3n, 2n]))

        $(a.sortInPlace(($, x) => x.negate()))
        $(assert.equal(a, [3n, 2n, 1n]))
        $(assert.equal(a.isSorted(), false))
        $(assert.equal(a.isSorted(($, x) => x.negate()), true))
        $(a.sortInPlace())
        $(assert.equal(a, [1n, 2n, 3n]))
        $(assert.equal(a.isSorted(), true))
        $(assert.equal(a.isSorted(($, x) => x.negate()), false))
        $(a.reverseInPlace())
        $(assert.equal(a, [3n, 2n, 1n]))

        const a2 = $.let([1n, 3n, 3n, 3n, 4n]);
        $(assert.equal(a2.findSortedFirst(0n), 0n))
        $(assert.equal(a2.findSortedLast(0n), 0n))
        $(assert.equal(a2.findSortedRange(0n), { start: 0n, end: 0n }))

        $(assert.equal(a2.findSortedFirst(1n), 0n))
        $(assert.equal(a2.findSortedLast(1n), 1n))
        $(assert.equal(a2.findSortedRange(1n), { start: 0n, end: 1n }))

        $(assert.equal(a2.findSortedFirst(2n), 1n))
        $(assert.equal(a2.findSortedLast(2n), 1n))
        $(assert.equal(a2.findSortedRange(2n), { start: 1n, end: 1n }))

        $(assert.equal(a2.findSortedFirst(3n), 1n))
        $(assert.equal(a2.findSortedLast(3n), 4n))
        $(assert.equal(a2.findSortedRange(3n), { start: 1n, end: 4n }))

        $(assert.equal(a2.findSortedFirst(4n), 4n))
        $(assert.equal(a2.findSortedLast(4n), 5n))
        $(assert.equal(a2.findSortedRange(4n), { start: 4n, end: 5n }))

        $(assert.equal(a2.findSortedFirst(5n), 5n))
        $(assert.equal(a2.findSortedLast(5n), 5n))
        $(assert.equal(a2.findSortedRange(5n), { start: 5n, end: 5n }))
    });

    test("Bulk ops", $ => {
        $(assert.equal(East.Array.generate(6n, IntegerType, ($, i) => i.add(1n)), [1n, 2n, 3n, 4n, 5n, 6n]));

        $(assert.equal(East.Array.range(0n, 6n), [0n, 1n, 2n, 3n, 4n, 5n]));
        $(assert.equal(East.Array.range(0n, 6n, 2n), [0n, 2n, 4n]));
        $(assert.equal(East.Array.range(0n, 6n, -1n), []));
        $(assert.equal(East.Array.range(6n, 0n, -1n), [6n, 5n, 4n, 3n, 2n, 1n]));

        $(assert.equal(East.Array.linspace(0.0, 1.0, 5n), [0.0, 0.25, 0.5, 0.75, 1.0]));
        $(assert.equal(East.Array.linspace(1.0, 2.0, 3n), [1.0, 1.5, 2.0]));
        $(assert.equal(East.Array.linspace(1.0, 2.0, 1n), [1.0]));
        $(assert.equal(East.Array.linspace(1.0, 2.0, 0n), []));
        $(assert.equal(East.Array.linspace(1.0, 2.0, -1n), []));

        $(assert.equal(East.value([1n, 2n, 3n, 4n, 5n, 6n]).slice(0n, 3n), [1n, 2n, 3n]));
        $(assert.equal(East.value([1n, 2n, 3n, 4n, 5n, 6n]).getKeys([0n, 2n, 4n]), [1n, 3n, 5n]));
        // console.log($.statements[$.statements.length - 1])
        // console.log(($.statements[$.statements.length - 1] as any).try_body.statements)
        // console.log(($.statements[$.statements.length - 1] as any).try_body.statements[2].ifs)
        $(assert.equal(East.value([1n, 2n, 3n, 4n]).concat([5n, 6n]), [1n, 2n, 3n, 4n, 5n, 6n]));

        const a = $.let([1n, 2n, 3n], ArrayType(IntegerType))
        $(a.append([4n, 5n, 6n]))
        $(assert.equal(a, [1n, 2n, 3n, 4n, 5n, 6n]))

        const b = $.let([1n, 2n, 3n], ArrayType(IntegerType))
        $(b.prepend([4n, 5n, 6n]))
        $(assert.equal(b, [4n, 5n, 6n, 1n, 2n, 3n]))

        $(assert.equal(East.value([1n, 2n, 3n]).sum(), 6n))
        $(assert.equal(East.value([1n, 2n, 3n]).sum(($, x) => x.add(1n)), 9n))
        $(assert.equal(East.value([1n, 2n, 3n]).mean(), 2.0))
        $(assert.equal(East.value([1n, 2n, 3n]).mean(($, x) => x.add(1n)), 3.0))
        $(assert.equal(East.value([1.0, 2.0, 3.0]).sum(), 6.0))
        $(assert.equal(East.value([1.0, 2.0, 3.0]).sum(($, x) => x.add(1.0)), 9.0))
        $(assert.equal(East.value([1.0, 2.0, 3.0]).mean(), 2.0))
        $(assert.equal(East.value([1.0, 2.0, 3.0]).mean(($, x) => x.add(1.0)), 3.0))

        // Maximum tests
        $(assert.equal(East.value([1n, 2n, 3n]).maximum(), 3n))
        $(assert.equal(East.value([3n, 1n, 2n]).maximum(), 3n))
        $(assert.equal(East.value([5n]).maximum(), 5n))
        $(assert.equal(East.value([-3n, -1n, -2n]).maximum(), -1n))
        $(assert.equal(East.value([1n, 1n, 1n]).maximum(), 1n))
        $(assert.equal(East.value([1.0, 2.5, 1.5]).maximum(), 2.5))
        $(assert.equal(East.value(["a", "c", "b"]).maximum(), "c"))
        $(assert.throws(East.value([], ArrayType(IntegerType)).maximum()))

        // Maximum with projection
        $(assert.equal(East.value([1n, 2n, 3n]).maximum(($, x) => x.negate()), 1n))
        $(assert.equal(East.value([1n, 2n, 3n]).maximum(($, x) => x.remainder(2n)), 1n))

        // Minimum tests
        $(assert.equal(East.value([1n, 2n, 3n]).minimum(), 1n))
        $(assert.equal(East.value([3n, 1n, 2n]).minimum(), 1n))
        $(assert.equal(East.value([5n]).minimum(), 5n))
        $(assert.equal(East.value([-3n, -1n, -2n]).minimum(), -3n))
        $(assert.equal(East.value([1n, 1n, 1n]).minimum(), 1n))
        $(assert.equal(East.value([1.0, 2.5, 1.5]).minimum(), 1.0))
        $(assert.equal(East.value(["a", "c", "b"]).minimum(), "a"))
        $(assert.throws(East.value([], ArrayType(IntegerType)).minimum()))

        // Minimum with projection
        $(assert.equal(East.value([1n, 2n, 3n]).minimum(($, x) => x.negate()), 3n))
        $(assert.equal(East.value([1n, 2n, 3n]).minimum(($, x) => x.remainder(2n)), 2n))

        // Maximum with projection using index - find element where value+index is maximum
        $(assert.equal(East.value([10n, 5n, 3n]).maximum(($, x, i) => x.add(i)), 10n))  // 10+0=10, 5+1=6, 3+2=5 -> max is 10
        $(assert.equal(East.value([1n, 2n, 10n]).maximum(($, x, i) => x.add(i)), 10n)) // 1+0=1, 2+1=3, 10+2=12 -> max is 10

        // Minimum with projection using index - find element where value-index is minimum
        $(assert.equal(East.value([10n, 5n, 3n]).minimum(($, x, i) => x.subtract(i)), 3n))  // 10-0=10, 5-1=4, 3-2=1 -> min is 3
        $(assert.equal(East.value([10n, 9n, 1n]).minimum(($, x, i) => x.subtract(i)), 1n))  // 10-0=10, 9-1=8, 1-2=-1 -> min is 1

        // findMaximum tests
        $(assert.equal(East.value([], ArrayType(IntegerType)).findMaximum(), none))
        $(assert.equal(East.value([1n]).findMaximum(), some(0n)))
        $(assert.equal(East.value([1n, 2n, 3n]).findMaximum(), some(2n)))
        $(assert.equal(East.value([3n, 1n, 2n]).findMaximum(), some(0n)))
        $(assert.equal(East.value([1n, 3n, 2n]).findMaximum(), some(1n)))
        $(assert.equal(East.value([1n, 1n, 1n]).findMaximum(), some(0n)))  // First occurrence
        $(assert.equal(East.value([1.0, 2.5, 1.5]).findMaximum(), some(1n)))
        $(assert.equal(East.value(["a", "c", "b"]).findMaximum(), some(1n)))

        // findMaximum with projection
        $(assert.equal(East.value([1n, 2n, 3n]).findMaximum(($, x) => x.negate()), some(0n)))  // Max of negated is min of original
        $(assert.equal(East.value([10n, 5n, 3n]).findMaximum(($, x, i) => x.add(i)), some(0n))) // 10+0=10 is max

        // findMinimum tests
        $(assert.equal(East.value([], ArrayType(IntegerType)).findMinimum(), none))
        $(assert.equal(East.value([1n]).findMinimum(), some(0n)))
        $(assert.equal(East.value([1n, 2n, 3n]).findMinimum(), some(0n)))
        $(assert.equal(East.value([3n, 1n, 2n]).findMinimum(), some(1n)))
        $(assert.equal(East.value([2n, 1n, 3n]).findMinimum(), some(1n)))
        $(assert.equal(East.value([1n, 1n, 1n]).findMinimum(), some(0n)))  // First occurrence
        $(assert.equal(East.value([1.0, 2.5, 1.5]).findMinimum(), some(0n)))
        $(assert.equal(East.value(["a", "c", "b"]).findMinimum(), some(0n)))

        // findMinimum with projection
        $(assert.equal(East.value([1n, 2n, 3n]).findMinimum(($, x) => x.negate()), some(2n)))  // Min of negated is max of original
        $(assert.equal(East.value([10n, 5n, 3n]).findMinimum(($, x, i) => x.subtract(i)), some(2n))) // 3-2=1 is min

        $(assert.equal(East.value([], ArrayType(BooleanType)).every(), true))
        $(assert.equal(East.value([true]).every(), true))
        $(assert.equal(East.value([true, false]).every(), false))
        $(assert.equal(East.value([], ArrayType(BooleanType)).some(), false))
        $(assert.equal(East.value([true]).some(), true))
        $(assert.equal(East.value([true, false]).some(), true))
    });

    test("String join", $ => {
        $(assert.equal(East.value([], ArrayType(StringType)).stringJoin(", "), ""))
        $(assert.equal(East.value(["a"]).stringJoin(", "), "a"))
        $(assert.equal(East.value(["a", "b"]).stringJoin(", "), "a, b"))
        $(assert.equal(East.value(["a", "b", "c"]).stringJoin(", "), "a, b, c"))
    });

    test("forEach", $ => {
        const from_array = $.let([], ArrayType(StringType));
        const log_array = $.let([], ArrayType(StringType));

        $(from_array.forEach(($, x) => log_array.pushLast(x)));
        $(assert.equal(log_array, []));

        $.assign(log_array, []);
        $.assign(from_array, ["a", "b", "c"]);
        $(from_array.forEach(($, x) => log_array.pushLast(x)));
        $(assert.equal(log_array, ["a", "b", "c"]));

        const total = $.let(0n);
        // const sum_fn = func([StringType, IntegerType], NullType, ($, _x, i) => {
        //     $.assign(total, total.add(i));
        // });
        $.assign(from_array, []);
        $(from_array.forEach(($, _x, i) => $.assign(total, total.add(i))));
        $(assert.equal(total, 0n));

        $.assign(from_array, ["a", "b", "c"]);
        $.assign(total, 0n);
        $(from_array.forEach(($, _x, i) => $.assign(total, total.add(i))));
        $(assert.equal(total, 3n));
    });

    test("ForEach - iteration guard", $ => {
        const arr = $.let([1n, 2n, 3n]);
        $(assert.throws(arr.forEach((_$, _x) => arr.pushLast(4n))));
    });

    test("For loop - iteration guard", $ => {
        const arr = $.let([1n, 2n, 3n]);
        $(assert.throws(Expr.block($ => {
            $.for(arr, (_$, _key, _value) => arr.pushLast(4n));
            return null;
        })));
    });

    test("Map", $ => {
        $(assert.equal(East.value([], ArrayType(IntegerType)).map(($, x) => x.multiply(2n)), []))
        $(assert.equal(East.value([10n, 20n, 30n]).map(($, x) => x.multiply(2n)), [20n, 40n, 60n]))

        $(assert.equal(East.value([], ArrayType(IntegerType)).map(($, x, i) => x.multiply(i)), []))
        $(assert.equal(East.value([10n, 20n, 30n]).map(($, x, i) => x.multiply(i)), [0n, 20n, 60n]))
    });

    test("Filter", $ => {
        $(assert.equal(East.value([], ArrayType(IntegerType)).filter(($, x) => East.equal(x.remainder(20n), 0n)), []))
        $(assert.equal(East.value([10n, 20n, 30n]).filter(($, x) => East.equal(x.remainder(2n), 1n)), []))
        $(assert.equal(East.value([10n, 20n, 30n]).filter(($, x) => East.equal(x.remainder(20n), 0n)), [20n]))
        $(assert.equal(East.value([10n, 20n, 30n]).filter(($, x) => East.equal(x.remainder(10n), 0n)), [10n, 20n, 30n]))

        // Test that filter returns ArrayExpr and can chain .length()
        $(assert.equal(East.value([1n, 2n, 3n, 4n, 5n, 6n]).filter(($, x) => East.equal(x.remainder(2n), 0n)).length(), 3n))

        $(assert.equal(East.value([1n, 2n, 3n, 4n, 5n, 6n]).filterMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(Expr.print(x)), () => none)), ["1", "3", "5"]))
    });

    test("firstMap", $ => {
        // Empty array returns none
        $(assert.equal(East.value([], ArrayType(IntegerType)).firstMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(Expr.print(x)), () => none)), none))

        // No matches returns none
        $(assert.equal(East.value([2n, 4n, 6n]).firstMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(Expr.print(x)), () => none)), none))

        // First match found - returns some with the first value
        $(assert.equal(East.value([1n, 2n, 3n, 4n, 5n, 6n]).firstMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(Expr.print(x)), () => none)), some("1")))

        // Multiple matches - returns first some (tests early termination)
        $(assert.equal(East.value([2n, 4n, 5n, 7n, 9n]).firstMap(($, x) => East.equal(x.remainder(2n), 1n).ifElse(() => some(x.multiply(10n)), () => none)), some(50n)))

        // Type conversion case
        $(assert.equal(East.value([10n, 20n, 30n]).firstMap(($, x) => East.greater(x, 15n).ifElse(() => some(Expr.print(x)), () => none)), some("20")))
    });

    test("findFirst", $ => {
        // Empty array returns none
        $(assert.equal(East.value([], ArrayType(IntegerType)).findFirst(5n), none))

        // No matches returns none
        $(assert.equal(East.value([1n, 2n, 3n]).findFirst(5n), none))

        // First match found - returns some with index
        $(assert.equal(East.value([1n, 2n, 3n]).findFirst(2n), some(1n)))

        // Multiple matches - returns first index (tests early termination)
        $(assert.equal(East.value([5n, 10n, 5n, 20n, 5n]).findFirst(5n), some(0n)))

        // Match at end
        $(assert.equal(East.value([1n, 2n, 3n]).findFirst(3n), some(2n)))

        // Using projection function to find by transformed value
        $(assert.equal(East.value([10n, 20n, 30n]).findFirst(4n, ($, x) => x.divide(5n)), some(1n)))
        // $(assert.equal(East.value([10n, 20n, 30n]).findFirst(East.value(4n), ($, x) => x.divide(5n)), some(1n)))
        // $(assert.equal(East.value([10n, 20n, 30n]).findFirst(4n, East.function([IntegerType], IntegerType, ($, x) => x.divide(5n))), some(1n)))

        // No match with projection
        $(assert.equal(East.value([10n, 20n, 30n]).findFirst(100n, ($, x) => x.divide(5n)), none))
    });

    test("findAll", $ => {
        // Empty array returns empty array
        $(assert.equal(East.value([], ArrayType(IntegerType)).findAll(5n), []))

        // No matches returns empty array
        $(assert.equal(East.value([1n, 2n, 3n]).findAll(5n), []))

        // Single match - returns array with one index
        $(assert.equal(East.value([1n, 2n, 3n]).findAll(2n), [1n]))

        // Multiple matches - returns all indices
        $(assert.equal(East.value([5n, 10n, 5n, 20n, 5n]).findAll(5n), [0n, 2n, 4n]))

        // All elements match
        $(assert.equal(East.value([7n, 7n, 7n]).findAll(7n), [0n, 1n, 2n]))

        // Using projection function to find by transformed value
        $(assert.equal(East.value([10n, 20n, 30n, 40n]).findAll(4n, ($, x) => x.divide(10n)), [3n]))

        // Multiple matches with projection
        $(assert.equal(East.value([10n, 20n, 15n, 30n, 25n]).findAll(1n, ($, x) => x.remainder(2n)), [2n, 4n]))

        // No match with projection
        $(assert.equal(East.value([10n, 20n, 30n]).findAll(100n, ($, x) => x.divide(5n)), []))
    });

    test("Reduce", $ => {
        $(assert.equal(East.value([], ArrayType(IntegerType)).reduce(($, a, b) => a.add(b), 10n), 10n))

        $(assert.equal(East.value([1n, 2n, 3n]).reduce(($, a, b) => a.add(b), 10n), 16n))

        $(assert.throws(East.value([], ArrayType(IntegerType)).mapReduce(($, x) => x.multiply(2n), ($, a, b) => a.add(b))))

        $(assert.equal(East.value([1n, 2n, 3n]).mapReduce((_$, x, _i) => x.multiply(2n), ($, a, b) => a.add(b)), 12n))
    })

    test("Comparisons", $ => {
        $(assert.equal(East.value([], ArrayType(IntegerType)), []))
        $(assert.equal(East.value([1n, 2n, 3n]), [1n, 2n, 3n]))
        $(assert.notEqual(East.value([1n, 2n, 3n]), [1n, 2n, 4n]))
        $(assert.notEqual(East.value([1n, 2n, 3n]), [1n, 2n]))

        $(assert.less(East.value([], ArrayType(IntegerType)), [1n]))
        $(assert.less(East.value([1n, 2n]), [1n, 2n, 3n]))
        $(assert.less(East.value([1n, 2n]), [1n, 3n]))
        $(assert.less(East.value([1n, 2n]), [2n]))

        $(assert.lessEqual(East.value([], ArrayType(IntegerType)), []))
        $(assert.lessEqual(East.value([1n, 2n]), [1n, 2n]))
        $(assert.lessEqual(East.value([1n, 2n]), [1n, 2n, 3n]))
        $(assert.lessEqual(East.value([1n, 2n]), [1n, 3n]))

        $(assert.greater(East.value([1n]), East.value([], ArrayType(IntegerType))))
        $(assert.greater(East.value([1n, 2n, 3n]), [1n, 2n]))
        $(assert.greater(East.value([1n, 3n]), [1n, 2n]))
        $(assert.greater(East.value([2n]), [1n, 2n]))

        $(assert.greaterEqual(East.value([], ArrayType(IntegerType)), []))
        $(assert.greaterEqual(East.value([1n, 2n]), [1n, 2n]))
        $(assert.greaterEqual(East.value([1n, 2n, 3n]), [1n, 2n]))
        $(assert.greaterEqual(East.value([1n, 3n]), [1n, 2n]))

        // Instance method tests
        $(assert.equal(East.value([1n, 2n, 3n]).equals([1n, 2n, 3n]), true))
        $(assert.equal(East.value([1n, 2n, 3n]).equals([1n, 2n]), false))
        $(assert.equal(East.value([1n, 2n, 3n]).notEquals([1n, 2n]), true))
        $(assert.equal(East.value([1n, 2n, 3n]).notEquals([1n, 2n, 3n]), false))
    });

    test("toSet", $ => {
        $(assert.equal(East.value([], ArrayType(IntegerType)).toSet(), new Set()))
        $(assert.equal(East.value([1n, 2n, 3n]).toSet(), new Set([1n, 2n, 3n])))
        $(assert.equal(East.value([1n, 2n, 2n, 3n, 3n, 3n]).toSet(), new Set([1n, 2n, 3n])))

        $(assert.equal(East.value([], ArrayType(IntegerType)).toSet(($, x) => x.negate()), new Set()))
        $(assert.equal(East.value([1n, 2n, 3n]).toSet(($, x) => x.negate()), new Set([-1n, -2n, -3n])))
        $(assert.equal(East.value([1n, 2n, 2n, 3n, 3n, 3n]).toSet(($, x) => x.negate()), new Set([-1n, -2n, -3n])))

    });

    test("toDict", $ => {
        $(assert.equal(East.value([], ArrayType(IntegerType)).toDict(), new Map()))
        $(assert.equal(East.value([1n, 2n, 3n]).toDict(), new Map([[0n, 1n], [1n, 2n], [2n, 3n]])))
        $(assert.equal(East.value([1n, 2n, 2n, 3n, 3n, 3n]).toDict(), new Map([[0n, 1n], [1n, 2n], [2n, 2n], [3n, 3n], [4n, 3n], [5n, 3n]])))

        $(assert.equal(East.value([], ArrayType(IntegerType)).toDict((_$, _x, i) => East.print(i)), new Map()))
        $(assert.equal(East.value([1n, 2n, 3n]).toDict((_$, _x, i) => East.print(i)), new Map([["0", 1n], ["1", 2n], ["2", 3n]])))
        $(assert.equal(East.value([1n, 2n, 2n, 3n, 3n, 3n]).toDict((_$, _x, i) => East.print(i)), new Map([["0", 1n], ["1", 2n], ["2", 2n], ["3", 3n], ["4", 3n], ["5", 3n]])))

        $(assert.equal(East.value([], ArrayType(IntegerType)).toDict((_$, x, _i) => East.print(x)), new Map()))
        $(assert.equal(East.value([1n, 2n, 3n]).toDict((_$, x, _i) => East.print(x)), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))
        $(assert.throws(East.value([1n, 2n, 2n, 3n, 3n, 3n]).toDict((_$, x, _i) => East.print(x))))

        $(assert.equal(East.value([], ArrayType(IntegerType)).toDict((_$, _x, i) => East.print(i), (_$, x) => x.negate()), new Map()))
        $(assert.equal(East.value([1n, 2n, 3n]).toDict((_$, _x, i) => East.print(i), (_$, x) => x.negate()), new Map([["0", -1n], ["1", -2n], ["2", -3n]])))
        $(assert.equal(East.value([1n, 2n, 2n, 3n, 3n, 3n]).toDict((_$, _x, i) => East.print(i), (_$, x) => x.negate()), new Map([["0", -1n], ["1", -2n], ["2", -2n], ["3", -3n], ["4", -3n], ["5", -3n]])))

        $(assert.equal(East.value([], ArrayType(IntegerType)).toDict((_$, x, _i) => East.print(x), (_$, x) => x.negate()), new Map()))
        $(assert.equal(East.value([1n, 2n, 3n]).toDict((_$, x, _i) => East.print(x), (_$, x) => x.negate()), new Map([["1", -1n], ["2", -2n], ["3", -3n]])))
        $(assert.throws(East.value([1n, 2n, 2n, 3n, 3n, 3n]).toDict((_$, x, _i) => East.print(x), (_$, x) => x.negate())))

        $(assert.equal(East.value([], ArrayType(IntegerType)).toDict((_$, x, _i) => East.print(x), (_$, x) => x.negate(), (_$, x, y) => x.add(y)), new Map()))
        $(assert.equal(East.value([1n, 2n, 3n]).toDict((_$, x, _i) => East.print(x), (_$, x) => x.negate(), (_$, x, y) => x.add(y)), new Map([["1", -1n], ["2", -2n], ["3", -3n]])))
        $(assert.equal(East.value([1n, 2n, 2n, 3n, 3n, 3n]).toDict((_$, x, _i) => East.print(x), (_$, x) => x.negate(), (_$, x, y) => x.add(y)), new Map([["1", -1n], ["2", -4n], ["3", -9n]])))

    });

    test("flatMap", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        $(assert.equal(a1.flatMap((_$, x) => [x, x.add(10n)]), []))

        const a2 = East.value([1n, 2n, 3n], ArrayType(IntegerType));
        $(assert.equal(a2.flatMap((_$, x) => [x, x.add(10n)]), [1n, 11n, 2n, 12n, 3n, 13n]))
        $(assert.equal(a2.flatMap((_$, x) => [x]), [1n, 2n, 3n]))
        $(assert.equal(a2.flatMap((_$, _x) => []), []))

        const a3 = East.value([[1n, 2n, 3n]], ArrayType(ArrayType(IntegerType)));
        $(assert.equal(a3.flatMap(), [1n, 2n, 3n]))

        const a4 = East.value([[1n, 2n], [3n]], ArrayType(ArrayType(IntegerType)));
        $(assert.equal(a4.flatMap(), [1n, 2n, 3n]))

        const a5 = East.value([[1n, 2n], [3n], []], ArrayType(ArrayType(IntegerType)));
        $(assert.equal(a5.flatMap(), [1n, 2n, 3n]))
    });

    test("flattenToSet", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        $(assert.equal(a1.flattenToSet((_$, x) => new Set([x, x.add(10n)])), new Set()))

        const a2 = East.value([1n, 2n, 3n], ArrayType(IntegerType));
        $(assert.equal(a2.flattenToSet((_$, x) => new Set([x, x.add(10n)])), new Set([1n, 2n, 3n, 11n, 12n, 13n])))
        $(assert.equal(a2.flattenToSet((_$, x) => new Set([x])), new Set([1n, 2n, 3n])))
        $(assert.equal(a2.flattenToSet((_$, _x) => new Set()), new Set()))

        const a3 = East.value([new Set([1n, 2n, 3n])], ArrayType(SetType(IntegerType)));
        $(assert.equal(a3.flattenToSet(), new Set([1n, 2n, 3n])))

        const a4 = East.value([new Set([1n, 2n]), new Set([3n])], ArrayType(SetType(IntegerType)));
        $(assert.equal(a4.flattenToSet(), new Set([1n, 2n, 3n])))

        const a5 = East.value([new Set([1n, 2n]), new Set([3n]), new Set<bigint>()], ArrayType(SetType(IntegerType)));
        $(assert.equal(a5.flattenToSet(), new Set([1n, 2n, 3n])))

        const a6 = East.value([new Set([1n, 2n]), new Set([2n, 3n])], ArrayType(SetType(IntegerType)));
        $(assert.equal(a6.flattenToSet(), new Set([1n, 2n, 3n])))
    });

    test("flattenToDict", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        $(assert.equal(a1.flattenToDict((_$, x) => new Map([[East.print(x), x], [East.print(x.add(10n)), x.add(10n)]])), new Map()))

        const a2 = East.value([1n, 2n, 3n], ArrayType(IntegerType));
        $(assert.equal(a2.flattenToDict((_$, x) => new Map([[East.print(x), x], [East.print(x.add(10n)), x.add(10n)]])), new Map([["1", 1n], ["2", 2n], ["3", 3n], ["11", 11n], ["12", 12n], ["13", 13n]])))
        $(assert.equal(a2.flattenToDict((_$, x) => new Map([[East.print(x), x]])), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))
        $(assert.equal(a2.flattenToDict((_$, _x) => new Map()), new Map()))

        const a3 = East.value([new Map([["1", 1n], ["2", 2n], ["3", 3n]])], ArrayType(DictType(StringType, IntegerType)));
        $(assert.equal(a3.flattenToDict(), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))

        const a4 = East.value([new Map([["1", 1n], ["2", 2n]]), new Map([["3", 3n]])], ArrayType(DictType(StringType, IntegerType)));
        $(assert.equal(a4.flattenToDict(), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))

        const a5 = East.value([new Map([["1", 1n], ["2", 2n]]), new Map([["3", 3n]]), new Map<string, bigint>()], ArrayType(DictType(StringType, IntegerType)));
        $(assert.equal(a5.flattenToDict(), new Map([["1", 1n], ["2", 2n], ["3", 3n]])))

        const a6 = East.value([new Map([["1", 1n], ["2", 2n]]), new Map([["2", 20n], ["3", 3n]])], ArrayType(DictType(StringType, IntegerType)));
        $(assert.throws(a6.flattenToDict()))

        const a7 = East.value([new Map([["1", 1n], ["2", 2n]]), new Map([["2", 20n], ["3", 3n]])], ArrayType(DictType(StringType, IntegerType)));
        $(assert.equal(a7.flattenToDict(($, x) => x, ($, x1, x2) => x1.add(x2)), new Map([["1", 1n], ["2", 22n], ["3", 3n]])))
    });

    test("groupReduce", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupReduce((_$, x, _i) => x.remainder(2n), (_$, _k2) => 10n, (_$, a, b, _i) => a.add(b)), new Map()))

        // Basic grouping by even/odd with custom init
        $(assert.equal(a2.groupReduce((_$, x, _i) => x.remainder(2n), (_$, _k2) => 10n, (_$, a, b, _i) => a.add(b)), new Map([[0n, 12n], [1n, 14n]])))
        // even: init=10, then 10+2=12
        // odd:  init=10, then 10+1+3=14

        // Single element per group - verifies initFn is called and element is added
        const a3 = East.value([1n, 2n], ArrayType(IntegerType));
        $(assert.equal(
            a3.groupReduce((_$, x) => x, (_$, k) => k.multiply(10n), (_$, a, b) => a.add(b)),
            new Map([[1n, 11n], [2n, 22n]])
        ))
        // key 1: init=1*10=10, then 10+1=11
        // key 2: init=2*10=20, then 20+2=22

        // Verify initFn receives correct key and is used
        const a4 = East.value([1n, 1n, 2n, 2n, 2n], ArrayType(IntegerType));
        $(assert.equal(
            a4.groupReduce((_$, x) => x, (_$, k) => k.multiply(100n), (_$, a, b) => a.add(b)),
            new Map([[1n, 102n], [2n, 206n]])
        ))
        // key 1: init=100, then 100+1+1=102
        // key 2: init=200, then 200+2+2+2=206

        // String keys with concatenation
        const a5 = East.value(["apple", "apricot", "banana", "berry"], ArrayType(StringType));
        $(assert.equal(
            a5.groupReduce(
                (_$, word) => word.substring(0n, 1n),
                (_$, letter) => Expr.str`[${letter}]: `,
                (_$, acc, word) => Expr.str`${acc}${word}, `
            ),
            new Map([["a", "[a]: apple, apricot, "], ["b", "[b]: banana, berry, "]])
        ))
    })

    test("toDict with conflict handler (groupMapReduce pattern)", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.toDict((_$, x) => x.remainder(2n), (_$, x) => x, (_$, a, b, _k) => a.add(b)), new Map()))

        // Basic grouping by even/odd with sum
        $(assert.equal(a2.toDict((_$, x) => x.remainder(2n), (_$, x) => x, (_$, a, b, _k) => a.add(b)), new Map([[0n, 2n], [1n, 4n]])))
        // even: 2
        // odd:  1+3=4

        // Single element per group - no reduction, just mapped value
        const a3 = East.value([1n, 2n], ArrayType(IntegerType));
        $(assert.equal(
            a3.toDict((_$, x) => x, (_$, x) => x.multiply(10n), (_$, a, b, _k) => a.add(b)),
            new Map([[1n, 10n], [2n, 20n]])
        ))

        // Map to different type (integer to string) then concatenate
        const a4 = East.value([1n, 1n, 2n, 2n, 2n], ArrayType(IntegerType));
        $(assert.equal(
            a4.toDict(
                (_$, x) => x,
                (_$, x) => East.print(x),
                (_$, a, b, _k) => Expr.str`${a}, ${b}`
            ),
            new Map([[1n, "1, 1"], [2n, "2, 2, 2"]])
        ))

        // String keys with concatenation
        const a5 = East.value(["apple", "apricot", "banana", "berry"], ArrayType(StringType));
        $(assert.equal(
            a5.toDict(
                (_$, word) => word.substring(0n, 1n),
                (_$, word) => word,
                (_$, a, b, _k) => Expr.str`${a}, ${b}`
            ),
            new Map([["a", "apple, apricot"], ["b", "banana, berry"]])
        ))

        // Different reduce operation - multiply instead of add
        const a6 = East.value([2n, 3n, 2n, 3n, 3n], ArrayType(IntegerType));
        $(assert.equal(
            a6.toDict((_$, x) => x, (_$, x) => x, (_$, a, b, _k) => a.multiply(b)),
            new Map([[2n, 4n], [3n, 27n]])
        ))
        // key 2: 2*2=4
        // key 3: 3*3*3=27

        // Map then reduce with transformation
        const a7 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));
        $(assert.equal(
            a7.toDict(
                (_$, x) => x.remainder(3n),  // Group by mod 3: 0, 1, 2
                (_$, x) => x.multiply(x),     // Map to square
                (_$, a, b, _k) => a.add(b)    // Sum squares
            ),
            new Map([[0n, 45n], [1n, 17n], [2n, 29n]])
        ))
        // [1,2,3,4,5,6] % 3 = [1,2,0,1,2,0]
        // Group 0: 3, 6 -> squares: 9, 36 -> sum: 9+36=45
        // Group 1: 1, 4 -> squares: 1, 16 -> sum: 1+16=17
        // Group 2: 2, 5 -> squares: 4, 25 -> sum: 4+25=29
    })

    test("groupSize", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 1n, 2n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupSize(), new Map()))
        $(assert.equal(a1.groupSize((_$, x) => x.remainder(2n)), new Map()))

        // Group by identity - count occurrences
        $(assert.equal(a2.groupSize(), new Map([[1n, 2n], [2n, 2n], [3n, 1n]])))

        // Group by even/odd
        $(assert.equal(a2.groupSize((_$, x) => x.remainder(2n)), new Map([[0n, 2n], [1n, 3n]])))

        // Group strings by first letter
        const a3 = East.value(["apple", "apricot", "banana", "berry", "cherry"], ArrayType(StringType));
        $(assert.equal(a3.groupSize((_$, w) => w.substring(0n, 1n)), new Map([["a", 2n], ["b", 2n], ["c", 1n]])))
    })

    test("groupEvery", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupEvery((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 0n)), new Map()))

        // Group by even/odd, check all are positive
        $(assert.equal(
            a2.groupEvery((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 0n)),
            new Map([[0n, true], [1n, true]])
        ))

        // Group by even/odd, check all are > 3
        $(assert.equal(
            a2.groupEvery((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 3n)),
            new Map([[0n, false], [1n, false]])
        ))

        // Check with all groups passing
        const a3 = East.value([5n, 7n, 9n, 4n, 6n, 8n], ArrayType(IntegerType));
        $(assert.equal(
            a3.groupEvery((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 3n)),
            new Map([[0n, true], [1n, true]])
        ))
    })

    test("groupSome", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupSome((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 4n)), new Map()))

        // Group by even/odd, check if any are > 4
        $(assert.equal(
            a2.groupSome((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 4n)),
            new Map([[0n, true], [1n, true]])
        ))

        // Group by even/odd, check if any are > 10
        $(assert.equal(
            a2.groupSome((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 10n)),
            new Map([[0n, false], [1n, false]])
        ))

        // Check with some groups having matches
        const a3 = East.value([1n, 3n, 5n, 2n, 4n, 10n], ArrayType(IntegerType));
        $(assert.equal(
            a3.groupSome((_$, x) => x.remainder(2n), (_$, x) => East.greater(x, 8n)),
            new Map([[0n, true], [1n, false]])
        ))
    })

    test("groupFindAll", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 2n, 5n, 2n], ArrayType(IntegerType));
        // Empty array
        $(assert.equal(a1.groupFindAll((_$, x) => x.remainder(2n), 2n), new Map()))
        // Group by even/odd, find all occurrences of 2n
        $(assert.equal(
            a2.groupFindAll((_$, x) => x.remainder(2n), 2n),
            new Map([[0n, [1n, 3n, 5n]], [1n, []]])
        ))
        // Group by even/odd, find all occurrences of 5n
        $(assert.equal(
            a2.groupFindAll((_$, x) => x.remainder(2n), 5n),
            new Map([[0n, []], [1n, [4n]]])
        ))
        // Group by even/odd, find all where x*2 == 4
        $(assert.equal(
            a2.groupFindAll((_$, x) => x.remainder(2n), 4n, (_$, x) => x.multiply(2n)),
            new Map([[0n, [1n, 3n, 5n]], [1n, []]])
        ))
    })

    test("groupFindFirst", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));
        // Empty array
        $(assert.equal(a1.groupFindFirst((_$, x) => x.remainder(2n), 4n), new Map()))
        // Group by even/odd, find first occurrence of 4n
        $(assert.equal(
            a2.groupFindFirst((_$, x) => x.remainder(2n), 4n),
            new Map<bigint, option<bigint>>([[0n, some(3n)], [1n, none]])
        ))
        // Group by even/odd, find first occurrence of 5n
        $(assert.equal(
            a2.groupFindFirst((_$, x) => x.remainder(2n), 5n),
            new Map<bigint, option<bigint>>([[0n, none], [1n, some(4n)]])
        ))
        // Group by even/odd, find first where x*2 == 6
        $(assert.equal(
            a2.groupFindFirst((_$, x) => x.remainder(2n), 6n, (_$, x) => x.multiply(2n)),
            new Map<bigint, option<bigint>>([[0n, none], [1n, some(2n)]])
        ))
    })

    test("groupFindMinimum and groupFindMaximum", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupFindMinimum((_$, x) => x.remainder(2n)), new Map()))
        $(assert.equal(a1.groupFindMaximum((_$, x) => x.remainder(2n)), new Map()))

        // Group by even/odd, find index of minimum/maximum
        $(assert.equal(
            a2.groupFindMinimum((_$, x) => x.remainder(2n)),
            new Map([[0n, 1n], [1n, 0n]])
        ))
        $(assert.equal(
            a2.groupFindMaximum((_$, x) => x.remainder(2n)),
            new Map([[0n, 5n], [1n, 4n]])
        ))

        // With projection - find by negated value
        $(assert.equal(
            a2.groupFindMinimum((_$, x) => x.remainder(2n), (_$, x) => x.negate()),
            new Map([[0n, 5n], [1n, 4n]])
        ))
        $(assert.equal(
            a2.groupFindMaximum((_$, x) => x.remainder(2n), (_$, x) => x.negate()),
            new Map([[0n, 1n], [1n, 0n]])
        ))
    })

    test("groupSum", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupSum((_$, x) => x.remainder(2n)), new Map()))

        // Group by even/odd, sum elements
        $(assert.equal(
            a2.groupSum((_$, x) => x.remainder(2n)),
            new Map([[0n, 12n], [1n, 9n]])
        ))

        // Group by even/odd, sum with projection
        $(assert.equal(
            a2.groupSum((_$, x) => x.remainder(2n), (_$, x) => x.multiply(2n)),
            new Map([[0n, 24n], [1n, 18n]])
        ))

        // Test with floats
        const a3 = East.value([1.0, 2.0, 3.0, 4.0]);
        $(assert.equal(
            a3.groupSum((_$, x) => East.lessEqual(x, 2.0).ifElse(() => 0n, () => 1n)),
            new Map([[0n, 3.0], [1n, 7.0]])
        ))
    })

    test("groupMean", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupMean((_$, x) => x.remainder(2n)), new Map()))

        // Group by even/odd, compute mean
        $(assert.equal(
            a2.groupMean((_$, x) => x.remainder(2n)),
            new Map([[0n, 4.0], [1n, 3.0]])
        ))

        // Group by even/odd, mean with projection
        $(assert.equal(
            a2.groupMean((_$, x) => x.remainder(2n), (_$, x) => x.multiply(2n)),
            new Map([[0n, 8.0], [1n, 6.0]])
        ))
    })

    test("groupToArrays", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupToArrays((_$, x) => x.remainder(2n)), new Map()))

        // Group by even/odd, collect into arrays
        $(assert.equal(
            a2.groupToArrays((_$, x) => x.remainder(2n)),
            new Map([[0n, [2n, 4n, 6n]], [1n, [1n, 3n, 5n]]])
        ))

        // With projection
        $(assert.equal(
            a2.groupToArrays((_$, x) => x.remainder(2n), (_$, x) => x.multiply(10n)),
            new Map([[0n, [20n, 40n, 60n]], [1n, [10n, 30n, 50n]]])
        ))
    })

    test("groupToSets", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 1n, 2n, 3n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupToSets((_$, x) => x.remainder(2n)), new Map()))

        // Group by even/odd, collect into sets (removes duplicates)
        $(assert.equal(
            a2.groupToSets((_$, x) => x.remainder(2n)),
            new Map([[0n, new Set([2n])], [1n, new Set([1n, 3n])]])
        ))

        // With projection
        $(assert.equal(
            a2.groupToSets((_$, x) => x.remainder(2n), (_$, x) => x.multiply(10n)),
            new Map([[0n, new Set([20n])], [1n, new Set([10n, 30n])]])
        ))
    })

    test("groupMinimum and groupMaximum", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupMinimum((_$, x) => x.remainder(2n)), new Map()))
        $(assert.equal(a1.groupMaximum((_$, x) => x.remainder(2n)), new Map()))

        // Group by even/odd, find minimum/maximum element
        $(assert.equal(
            a2.groupMinimum((_$, x) => x.remainder(2n)),
            new Map([[0n, 2n], [1n, 1n]])
        ))
        $(assert.equal(
            a2.groupMaximum((_$, x) => x.remainder(2n)),
            new Map([[0n, 6n], [1n, 5n]])
        ))

        // With projection - find element with min/max projected value
        $(assert.equal(
            a2.groupMinimum((_$, x) => x.remainder(2n), (_$, x) => x.negate()),
            new Map([[0n, 6n], [1n, 5n]])
        ))
        $(assert.equal(
            a2.groupMaximum((_$, x) => x.remainder(2n), (_$, x) => x.negate()),
            new Map([[0n, 2n], [1n, 1n]])
        ))

        // Test with strings
        const a3 = East.value(["apple", "apricot", "banana", "berry"], ArrayType(StringType));
        $(assert.equal(
            a3.groupMinimum((_$, w) => w.substring(0n, 1n)),
            new Map([["a", "apple"], ["b", "banana"]])
        ))
        $(assert.equal(
            a3.groupMaximum((_$, w) => w.substring(0n, 1n)),
            new Map([["a", "apricot"], ["b", "berry"]])
        ))
    })

    test("groupToDicts - without conflict handler", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 4n, 5n, 6n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupToDicts((_$, x) => x.remainder(2n), (_$, x) => x), new Map()))

        // Group by even/odd, inner dict by element value
        $(assert.equal(
            a2.groupToDicts((_$, x) => x.remainder(2n), (_$, x) => x),
            new Map([
                [0n, new Map([[2n, 2n], [4n, 4n], [6n, 6n]])],
                [1n, new Map([[1n, 1n], [3n, 3n], [5n, 5n]])]
            ])
        ))

        // With value projection
        $(assert.equal(
            a2.groupToDicts((_$, x) => x.remainder(2n), (_$, x) => x, (_$, x) => x.multiply(10n)),
            new Map([
                [0n, new Map([[2n, 20n], [4n, 40n], [6n, 60n]])],
                [1n, new Map([[1n, 10n], [3n, 30n], [5n, 50n]])]
            ])
        ))

        // Duplicate key should throw
        const a3 = East.value([1n, 2n, 1n], ArrayType(IntegerType));
        $(assert.throws(a3.groupToDicts((_$, x) => x.remainder(2n), (_$, x) => x)))
    })

    test("groupToDicts - with conflict handler", $ => {
        const a1 = East.value([], ArrayType(IntegerType));
        const a2 = East.value([1n, 2n, 3n, 1n, 2n, 3n], ArrayType(IntegerType));

        // Empty array
        $(assert.equal(a1.groupToDicts((_$, x) => x.remainder(2n), (_$, x) => x, (_$, x) => x, (_$, a, b) => a.add(b)), new Map()))

        // Group by even/odd, inner dict by element value with sum on conflict
        $(assert.equal(
            a2.groupToDicts((_$, x) => x.remainder(2n), (_$, x) => x, (_$, x) => x, (_$, a, b) => a.add(b)),
            new Map([
                [0n, new Map([[2n, 4n]])],
                [1n, new Map([[1n, 2n], [3n, 6n]])]
            ])
        ))

        // With value projection and conflict resolution
        $(assert.equal(
            a2.groupToDicts(
                (_$, x) => x.remainder(2n),
                (_$, x) => x,
                (_$, x) => x.multiply(10n),
                (_$, a, b) => a.add(b)
            ),
            new Map([
                [0n, new Map([[2n, 40n]])],
                [1n, new Map([[1n, 20n], [3n, 60n]])]
            ])
        ))
    })

    // =========================================================================
    // encodeCsv tests
    // =========================================================================

    test("encodeCsv - basic encoding with header", $ => {
        const T = StructType({ name: StringType, age: IntegerType });
        const arr = $.let([
            { name: "Alice", age: 30n },
            { name: "Bob", age: 25n },
        ], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "name,age\r\nAlice,30\r\nBob,25"));
    });

    test("encodeCsv - empty array", $ => {
        const T = StructType({ name: StringType });
        const arr = $.let([], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "name"));
    });

    test("encodeCsv - string fields", $ => {
        const T = StructType({ value: StringType });
        const arr = $.let([{ value: "hello" }, { value: "world" }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "value\r\nhello\r\nworld"));
    });

    test("encodeCsv - integer fields", $ => {
        const T = StructType({ value: IntegerType });
        const arr = $.let([{ value: 42n }, { value: -123n }, { value: 0n }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "value\r\n42\r\n-123\r\n0"));
    });

    test("encodeCsv - float fields", $ => {
        const T = StructType({ value: FloatType });
        const arr = $.let([{ value: 3.14 }, { value: -2.5 }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "value\r\n3.14\r\n-2.5"));
    });

    test("encodeCsv - float special values", $ => {
        const T = StructType({ value: FloatType });
        const arr = $.let([
            { value: Infinity },
            { value: -Infinity },
            { value: NaN },
        ], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "value\r\nInfinity\r\n-Infinity\r\nNaN"));
    });

    test("encodeCsv - boolean fields", $ => {
        const T = StructType({ value: BooleanType });
        const arr = $.let([{ value: true }, { value: false }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "value\r\ntrue\r\nfalse"));
    });

    test("encodeCsv - blob fields as hex", $ => {
        const T = StructType({ value: BlobType });
        const arr = $.let([{ value: new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]) }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "value\r\n0x48656c6c6f"));
    });

    test("encodeCsv - optional field some", $ => {
        const T = StructType({ value: VariantType({ none: NullType, some: StringType }) });
        const arr = $.let([{ value: variant("some", "hello") }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "value\r\nhello"));
    });

    test("encodeCsv - optional field none", $ => {
        const T = StructType({ value: VariantType({ none: NullType, some: StringType }) });
        const arr = $.let([{ value: variant("none", null) }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), "value\r\n"));
    });

    test("encodeCsv - quote fields containing delimiter", $ => {
        const T = StructType({ value: StringType });
        const arr = $.let([{ value: "hello, world" }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), 'value\r\n"hello, world"'));
    });

    test("encodeCsv - quote fields containing newlines", $ => {
        const T = StructType({ value: StringType });
        const arr = $.let([{ value: "hello\nworld" }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), 'value\r\n"hello\nworld"'));
    });

    test("encodeCsv - escape quotes within fields", $ => {
        const T = StructType({ value: StringType });
        const arr = $.let([{ value: 'say "hello"' }], ArrayType(T));

        const result = $.let(arr.encodeCsv());

        $(assert.equal(result.decodeUtf8(), 'value\r\n"say ""hello"""'));
    });

    test("encodeCsv - custom delimiter", $ => {
        const T = StructType({ a: StringType, b: StringType });
        const arr = $.let([{ a: "hello", b: "world" }], ArrayType(T));

        const result = $.let(arr.encodeCsv({ delimiter: ";" }));

        $(assert.equal(result.decodeUtf8(), "a;b\r\nhello;world"));
    });

    test("encodeCsv - custom newline", $ => {
        const T = StructType({ value: StringType });
        const arr = $.let([{ value: "a" }, { value: "b" }], ArrayType(T));

        const result = $.let(arr.encodeCsv({ newline: "\n" }));

        $(assert.equal(result.decodeUtf8(), "value\na\nb"));
    });

    test("encodeCsv - without header", $ => {
        const T = StructType({ name: StringType });
        const arr = $.let([{ name: "Alice" }], ArrayType(T));

        const result = $.let(arr.encodeCsv({ includeHeader: false }));

        $(assert.equal(result.decodeUtf8(), "Alice"));
    });

    test("encodeCsv - custom null string", $ => {
        const T = StructType({ value: VariantType({ none: NullType, some: StringType }) });
        const arr = $.let([{ value: variant("none", null) }], ArrayType(T));

        const result = $.let(arr.encodeCsv({ nullString: "NULL" }));

        $(assert.equal(result.decodeUtf8(), "value\r\nNULL"));
    });

    test("encodeCsv - always quote", $ => {
        const T = StructType({ value: StringType });
        const arr = $.let([{ value: "hello" }], ArrayType(T));

        const result = $.let(arr.encodeCsv({ alwaysQuote: true }));

        $(assert.equal(result.decodeUtf8(), '"value"\r\n"hello"'));
    });

    test("encodeCsv - custom quote character", $ => {
        const T = StructType({ value: StringType });
        const arr = $.let([{ value: "hello" }], ArrayType(T));

        const result = $.let(arr.encodeCsv({ quoteChar: "'", alwaysQuote: true }));

        $(assert.equal(result.decodeUtf8(), "'value'\r\n'hello'"));
    });

    // =========================================================================
    // CSV round-trip tests
    // =========================================================================

    test("CSV round-trip - simple data", $ => {
        const T = StructType({ name: StringType, age: IntegerType, active: BooleanType });
        const original = $.let([
            { name: "Alice", age: 30n, active: true },
            { name: "Bob", age: 25n, active: false },
        ], ArrayType(T));

        const encoded = $.let(original.encodeCsv());
        const decoded = $.let(encoded.decodeCsv(T));

        $(assert.equal(decoded, original));
    });

    test("CSV round-trip - optional fields", $ => {
        const T = StructType({ name: StringType, nickname: VariantType({ none: NullType, some: StringType }) });
        const original = $.let([
            { name: "Alice", nickname: variant("some", "Ali") },
            { name: "Bob", nickname: variant("none", null) },
        ], ArrayType(T));

        const encoded = $.let(original.encodeCsv());
        const decoded = $.let(encoded.decodeCsv(T));

        $(assert.equal(decoded, original));
    });

    test("CSV round-trip - special characters", $ => {
        const T = StructType({ value: StringType });
        const original = $.let([
            { value: "hello, world" },
            { value: 'with "quotes"' },
            { value: "multi\nline" },
        ], ArrayType(T));

        const encoded = $.let(original.encodeCsv());
        const decoded = $.let(encoded.decodeCsv(T));

        $(assert.equal(decoded, original));
    });

    test("CSV round-trip - large number of rows", $ => {
        const T = StructType({ id: IntegerType, name: StringType, value: FloatType });
        const original = $.let(
            East.Array.generate(10000n, T, ($, i) => ({
                id: i,
                name: East.str`row_${i}`,
                value: i.toFloat().divide(10.0),
            }))
        );

        const encoded = $.let(original.encodeCsv());
        const decoded = $.let(encoded.decodeCsv(T));

        $(assert.equal(decoded, original));
    });

    // =========================================================================
    // Nested closure capture tests - these test that closures inside .some(),
    // .filter(), etc. can correctly capture variables from outer scopes
    // =========================================================================

    test(".some() captures outer variable", $ => {
        const threshold = $.const(5n);
        const arr = $.const([1n, 2n, 3n, 6n, 7n]);
        // .some() callback captures 'threshold' from outer scope
        const result = $.let(arr.some(($, v) => East.greater(v, threshold)));
        $(assert.equal(result, true)); // 6 > 5
    });

    test(".filter() captures outer variable", $ => {
        const threshold = $.const(3n);
        const arr = $.const([1n, 2n, 3n, 4n, 5n]);
        // .filter() callback captures 'threshold' from outer scope
        const result = $.let(arr.filter(($, v) => East.greater(v, threshold)));
        $(assert.equal(result, [4n, 5n]));
    });

    test(".some() with .or() nested closure capture", $ => {
        const lower = $.const(0n);
        const upper = $.const(10n);
        const arr = $.const([5n, 15n, 3n]);
        // .some() callback uses .or() which creates another closure
        // Both closures need to capture 'lower' and 'upper'
        const result = $.let(arr.some(($, v) =>
            East.less(v, lower).or(_$ => East.greater(v, upper))
        ));
        $(assert.equal(result, true)); // 15 > 10
    });

    test(".filter() with .and() nested closure capture", $ => {
        const lower = $.const(2n);
        const upper = $.const(8n);
        const arr = $.const([1n, 3n, 5n, 7n, 9n]);
        // .filter() callback uses .and() which creates another closure
        const result = $.let(arr.filter(($, v) =>
            East.greater(v, lower).and(_$ => East.less(v, upper))
        ));
        $(assert.equal(result, [3n, 5n, 7n])); // 2 < v < 8
    });

    test(".some() inside loop captures outer loop variable", $ => {
        const bounds = $.const([5n, 10n, 15n]); // lower bounds per iteration
        const values = $.const([3n, 12n, 20n]);
        const found_any = $.let(false);

        // Outer loop defines 'bound', inner .some() captures it
        $.for(bounds, ($, bound, _i) => {
            $.if(values.some(($, v) => East.greater(v, bound)), $ => {
                $.assign(found_any, true);
            });
        });
        $(assert.equal(found_any, true));
    });

    test("Nested .some() with multiple captured variables", $ => {
        const multiplier = $.const(2n);
        const offset = $.const(10n);
        const threshold = $.const(25n);
        const arr = $.const([5n, 10n, 15n]);
        // .some() callback captures multiplier, offset, threshold
        // and uses them in a complex expression
        const result = $.let(arr.some(($, v) =>
            East.greater(v.multiply(multiplier).add(offset), threshold)
        ));
        $(assert.equal(result, true)); // 15*2+10 = 40 > 25
    });

    test(".map() inside nested East.function captures from outer function", $ => {
        // This tests the pattern where:
        // - Outer function defines a variable
        // - Inner East.function is defined inside outer
        // - .map() callback inside inner function captures variable from OUTER function
        // This crosses TWO East.function boundaries
        const multiplier = $.const(2n);
        const arr = $.const([1n, 2n, 3n]);

        // Inner function that uses .map() capturing 'multiplier' from outer scope
        const inner_fn = $.let(East.function(
            [ArrayType(IntegerType)],
            ArrayType(IntegerType),
            ($, input) => {
                // .map() callback captures 'multiplier' from the OUTER test function
                const result = $.let(input.map(($, v) => v.multiply(multiplier)));
                return $.return(result);
            }
        ));

        const result = $.let(inner_fn(arr));
        $(assert.equal(result, [2n, 4n, 6n]));
    });

    test(".map() inside nested East.function captures multiple outer variables", $ => {
        // More complex case: multiple variables captured across function boundaries
        const scale = $.const(10n);
        const offset = $.const(5n);
        const arr = $.const([1n, 2n, 3n]);

        const transform_fn = $.let(East.function(
            [ArrayType(IntegerType)],
            ArrayType(IntegerType),
            ($, input) => {
                // Captures both 'scale' and 'offset' from outer function
                const result = $.let(input.map(($, v) => v.multiply(scale).add(offset)));
                return $.return(result);
            }
        ));

        const result = $.let(transform_fn(arr));
        $(assert.equal(result, [15n, 25n, 35n])); // 1*10+5, 2*10+5, 3*10+5
    });

    // =========================================================================
    // TypeOf RecursiveType preservation tests
    // This tests the fix for: when map() callback returns Expr<RecursiveType<...>>,
    // TypeOf should preserve the RecursiveType wrapper, not unwrap to VariantType
    //
    // Real-world use case:
    //   Stack.HStack(strings.map(($, s) => Badge.Root(s)), { gap: "1" })
    // Where Badge.Root returns Expr<UIComponentType> and UIComponentType is a RecursiveType
    // =========================================================================

    test("map() with function returning Expr<RecursiveType> preserves type", $ => {
        // Simplified UIComponentType - a recursive type wrapping a variant
        const ComponentType = RecursiveType(self => VariantType({
            Text: StructType({ content: StringType }),
            Badge: StructType({ label: StringType }),
            Stack: StructType({ children: ArrayType(self) }),
        }));

        // Simulates Badge.Root(label) - returns Expr<ComponentType>
        // This is a callable function expression that returns the RecursiveType
        const BadgeRoot = $.let(East.function([StringType], ComponentType, ($, label) => {
            return $.return(East.value(variant("Badge", { label }), ComponentType));
        }));

        // Simulates Stack.HStack(children) - accepts Array<ComponentType>
        const StackHStack = $.let(East.function([ArrayType(ComponentType)], ComponentType, ($, children) => {
            return $.return(East.value(variant("Stack", { children }), ComponentType));
        }));

        const createStack = (
            children: SubtypeExprOrValue<ArrayType<typeof ComponentType>>,
        ): ExprType<typeof ComponentType> => {
            return $.let(StackHStack(children));
        }

        // The actual use case: map strings to badges, then wrap in a stack
        const labels = $.let(["tag1", "tag2", "tag3"]);

        // This is the key test: BadgeRoot returns Expr<ComponentType> (a RecursiveType)
        // TypeOf should preserve RecursiveType, so badges should be ArrayExpr<ComponentType>
        const badges = $.let(labels.map(($, label) => BadgeRoot(label)));

        // This should type-check: StackHStack expects ArrayType(ComponentType)
        // If TypeOf incorrectly unwrapped RecursiveType to VariantType, this would fail
        const stack = $.let(StackHStack(badges));

        // Also test passing badges via a helper function
        const other_stack = $.let(createStack(badges));

        // The fact that the above line compiles is the test!
        // StackHStack expects ArrayType(ComponentType) and badges is ArrayExpr<ComponentType>
        // Verify runtime behavior matches expected value
        const expected = $.let(East.value(variant("Stack", {
            children: [
                variant("Badge", { label: "tag1" }),
                variant("Badge", { label: "tag2" }),
                variant("Badge", { label: "tag3" }),
            ]
        }), ComponentType));

        $(assert.equal(stack, expected));
        $(assert.equal(other_stack, expected));
        $(assert.equal(other_stack, stack));
    });

    test("Equality method aliases", $ => {
        // Test short aliases (eq, ne)
        $(assert.equal(East.value([1n, 2n, 3n]).eq([1n, 2n, 3n]), true));
        $(assert.equal(East.value([1n, 2n, 3n]).eq([1n, 2n]), false));
        $(assert.equal(East.value([1n, 2n, 3n]).ne([1n, 2n]), true));
        $(assert.equal(East.value([1n, 2n, 3n]).ne([1n, 2n, 3n]), false));

        // Test medium aliases (equal, notEqual)
        $(assert.equal(East.value([1n, 2n, 3n]).equal([1n, 2n, 3n]), true));
        $(assert.equal(East.value([1n, 2n, 3n]).notEqual([1n, 2n]), true));
    });
});
