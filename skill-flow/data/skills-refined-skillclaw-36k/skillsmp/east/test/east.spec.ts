/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import {
    East,
    ArrayType,
    IntegerType,
    StringType,
    NullType,
    BooleanType,
    FloatType,
    DateTimeType,
    BlobType,
    SetType,
    DictType,
    StructType,
    VariantType,
    RecursiveType,
    some,
    none,
    OptionType,
    variant,
    printType,
    NeverType,
    RefType,
    ref
} from "../src/index.js";
import { EastTypeType, toEastTypeValue } from "../src/type_of_type.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

// Define a simple binary tree type
const TreeType = RecursiveType(self => VariantType({
    leaf: NullType,
    node: StructType({
        value: IntegerType,
        left: self,
        right: self
    })
}));

// Define a linked list type
const LinkedListType = RecursiveType(self => VariantType({
    nil: NullType,
    cons: StructType({
        head: IntegerType,
        tail: self
    })
}));

await describe("East", (test) => {
    test("value() with null", $ => {
        $(assert.equal(East.value(null), null));
    });

    test("value() with null and type", $ => {
        $(assert.equal(East.value(null, NullType), null));
    });

    test("value() with boolean", $ => {
        $(assert.equal(East.value(true), true));
        $(assert.equal(East.value(false), false));
    });

    test("value() with boolean and type", $ => {
        $(assert.equal(East.value(true, BooleanType), true));
        $(assert.equal(East.value(false, BooleanType), false));
    });

    test("value() with integer", $ => {
        $(assert.equal(East.value(42n), 42n));
    });

    test("value() with integer and type", $ => {
        $(assert.equal(East.value(42n, IntegerType), 42n));
    });

    test("value() with float", $ => {
        $(assert.equal(East.value(3.14), 3.14));
    });

    test("value() with float and type", $ => {
        $(assert.equal(East.value(3.14, FloatType), 3.14));
    });

    test("value() with string", $ => {
        $(assert.equal(East.value("hello"), "hello"));
    });

    test("value() with string and type", $ => {
        $(assert.equal(East.value("hello", StringType), "hello"));
    });

    test("value() with datetime", $ => {
        const date = new Date("2025-01-01T00:00:00Z");
        $(assert.equal(East.value(date), date));
    });

    test("value() with datetime and type", $ => {
        const date = new Date("2025-01-01T00:00:00Z");
        $(assert.equal(East.value(date, DateTimeType), date));
    });

    test("value() with blob", $ => {
        const blob = new Uint8Array([1, 2, 3, 4]);
        $(assert.equal(East.value(blob), blob));
    });

    test("value() with blob and type", $ => {
        const blob = new Uint8Array([1, 2, 3, 4]);
        $(assert.equal(East.value(blob, BlobType), blob));
    });

    test("value() with array", $ => {
        const arr = [1n, 2n, 3n];
        $(assert.equal(East.value(arr), arr));
    });

    test("value() with array and type", $ => {
        const arr = [1n, 2n, 3n];
        $(assert.equal(East.value(arr, ArrayType(IntegerType)), arr));
    });

    test("value() with set", $ => {
        const set = new Set([1n, 2n, 3n]);
        $(assert.equal(East.value(set), set));
    });

    test("value() with set and type", $ => {
        const set = new Set([1n, 2n, 3n]);
        $(assert.equal(East.value(set, SetType(IntegerType)), set));
    });

    test("value() with dict", $ => {
        const dict = new Map([["a", 1n], ["b", 2n]]);
        $(assert.equal(East.value(dict), dict));
    });

    test("value() with dict and type", $ => {
        const dict = new Map([["a", 1n], ["b", 2n]]);
        $(assert.equal(East.value(dict, DictType(StringType, IntegerType)), dict));
    });

    test("value() with struct", $ => {
        const struct = { x: 10n, y: 20n };
        $(assert.equal(East.value(struct), struct));
    });

    test("value() with struct and type", $ => {
        const struct = { x: 10n, y: 20n };
        $(assert.equal(East.value(struct, StructType({ x: IntegerType, y: IntegerType })), struct));
    });

    test("value() with variant", $ => {
        const v = variant("success", 42n);
        $(assert.equal(East.value(v, VariantType({ success: IntegerType, failure: StringType })), v));
    });

    test("value() with Expr values", $ => {
        const x = East.value(42n);
        const y = East.value(x);
        $(assert.equal(y, 42n));
    });

    test("value() with Expr and type checking", $ => {
        const x = East.value(42n);
        const y = East.value(x, IntegerType);
        $(assert.equal(y, 42n));
    });

    test("func() with explicit output type", $ => {
        const add = East.function([IntegerType, IntegerType], IntegerType, ($, x, y) => {
            return x.add(y);
        });
        $(assert.equal(add(5n, 10n), 15n));
    });

    test("func() with no return statement", $ => {
        const add = East.function([IntegerType, IntegerType], IntegerType, ($, x, y) => {
            return x.add(y);
        });
        $(assert.equal(add(5n, 10n), 15n));
    });

    test("func() with null output type", $ => {
        const arr = $.let([], ArrayType(IntegerType));
        const addToArr = East.function([IntegerType], NullType, ($, x) => {
            $(arr.pushLast(x));
        });
        $(addToArr(1n));
        $(addToArr(2n));
        $(assert.equal(arr, [1n, 2n]));
    });

    test("str() with simple string", $ => {
        $(assert.equal(East.str`hello`, "hello"));
    });

    test("str() with null interpolation", $ => {
        $(assert.equal(East.str`value: ${East.value(null)}`, "value: null"));
    });

    test("str() with boolean interpolation", $ => {
        $(assert.equal(East.str`${East.value(true)} and ${East.value(false)}`, "true and false"));
    });

    test("str() with integer interpolation", $ => {
        const x = East.value(42n);
        $(assert.equal(East.str`The answer is ${x}`, "The answer is 42"));
        $(assert.equal(East.str`${x} is the answer`, "42 is the answer"));
    });

    test("str() with float interpolation", $ => {
        $(assert.equal(East.str`pi is ${East.value(3.14)}`, "pi is 3.14"));
        $(assert.equal(East.str`special: ${East.value(NaN)}`, "special: NaN"));
        $(assert.equal(East.str`infinity: ${East.value(Infinity)}`, "infinity: Infinity"));
    });

    test("str() with string interpolation", $ => {
        $(assert.equal(East.str`hello ${"world"}`, "hello world"));
        $(assert.equal(East.str`${""}empty`, "empty"));
    });

    test("str() with datetime interpolation", $ => {
        const date = new Date("2025-01-01T12:34:56.789Z");
        $(assert.equal(East.str`Date: ${East.value(date)}`, "Date: 2025-01-01T12:34:56.789"));
    });

    test("str() with blob interpolation", $ => {
        $(assert.equal(East.str`blob: ${East.value(new Uint8Array([10, 20, 30]))}`, "blob: 0x0a141e"));
    });

    test("str() with array interpolation", $ => {
        $(assert.equal(East.str`array: ${East.value([1n, 2n, 3n])}`, "array: [1, 2, 3]"));
    });

    test("str() with set interpolation", $ => {
        $(assert.equal(East.str`set: ${East.value(new Set([1n, 2n]))}`, "set: {1,2}"));
    });

    test("str() with dict interpolation", $ => {
        $(assert.equal(East.str`dict: ${East.value(new Map([["a", 1n]]))}`, "dict: {\"a\":1}"));
    });

    test("str() with struct interpolation", $ => {
        $(assert.equal(East.str`point: ${East.value({ x: 1n, y: 2n })}`, "point: (x=1, y=2)"));
    });

    test("str() with variant interpolation", $ => {
        $(assert.equal(East.str`option: ${East.value(some(42n), OptionType(IntegerType))}`, "option: .some 42"));
        $(assert.equal(East.str`none: ${East.value(none, OptionType(IntegerType))}`, "none: .none"));
    });

    test("str() with multiple interpolations", $ => {
        const x = East.value(5n);
        const y = East.value(10n);
        $(assert.equal(East.str`${x} + ${y} = ${x.add(y)}`, "5 + 10 = 15"));
    });

    test("equal() with null", $ => {
        $(assert.equal(East.equal(East.value(null), null), true));
    });

    test("notEqual() with null", $ => {
        $(assert.equal(East.notEqual(East.value(null), null), false));
    });

    test("less() with null", $ => {
        $(assert.equal(East.less(East.value(null), null), false));
    });

    test("lessEqual() with null", $ => {
        $(assert.equal(East.lessEqual(East.value(null), null), true));
    });

    test("greater() with null", $ => {
        $(assert.equal(East.greater(East.value(null), null), false));
    });

    test("greaterEqual() with null", $ => {
        $(assert.equal(East.greaterEqual(East.value(null), null), true));
    });

    test("is() with null", $ => {
        $(assert.equal(East.is(East.value(null), null), true));
    });

    test("equal() with booleans", $ => {
        $(assert.equal(East.equal(East.value(true), true), true));
        $(assert.equal(East.equal(East.value(true), false), false));
        $(assert.equal(East.equal(East.value(false), false), true));
        $(assert.equal(East.equal(East.value(false), true), false));
    });

    test("notEqual() with booleans", $ => {
        $(assert.equal(East.notEqual(East.value(true), true), false));
        $(assert.equal(East.notEqual(East.value(true), false), true));
        $(assert.equal(East.notEqual(East.value(false), false), false));
        $(assert.equal(East.notEqual(East.value(false), true), true));
    });

    test("less() with booleans", $ => {
        $(assert.equal(East.less(East.value(false), true), true));
        $(assert.equal(East.less(East.value(true), false), false));
        $(assert.equal(East.less(East.value(false), false), false));
        $(assert.equal(East.less(East.value(true), true), false));
    });

    test("lessEqual() with booleans", $ => {
        $(assert.equal(East.lessEqual(East.value(false), true), true));
        $(assert.equal(East.lessEqual(East.value(true), false), false));
        $(assert.equal(East.lessEqual(East.value(false), false), true));
        $(assert.equal(East.lessEqual(East.value(true), true), true));
    });

    test("greater() with booleans", $ => {
        $(assert.equal(East.greater(East.value(true), false), true));
        $(assert.equal(East.greater(East.value(false), true), false));
        $(assert.equal(East.greater(East.value(false), false), false));
        $(assert.equal(East.greater(East.value(true), true), false));
    });

    test("greaterEqual() with booleans", $ => {
        $(assert.equal(East.greaterEqual(East.value(true), false), true));
        $(assert.equal(East.greaterEqual(East.value(false), true), false));
        $(assert.equal(East.greaterEqual(East.value(false), false), true));
        $(assert.equal(East.greaterEqual(East.value(true), true), true));
    });

    test("is() with booleans", $ => {
        $(assert.equal(East.is(East.value(true), true), true));
        $(assert.equal(East.is(East.value(false), false), true));
        $(assert.equal(East.is(East.value(true), false), false));
    });

    test("equal() with integers", $ => {
        $(assert.equal(East.equal(East.value(0n), 0n), true));
        $(assert.equal(East.equal(East.value(42n), 42n), true));
        $(assert.equal(East.equal(East.value(42n), 43n), false));
        $(assert.equal(East.equal(East.value(-1n), -1n), true));
    });

    test("notEqual() with integers", $ => {
        $(assert.equal(East.notEqual(East.value(0n), 0n), false));
        $(assert.equal(East.notEqual(East.value(42n), 42n), false));
        $(assert.equal(East.notEqual(East.value(42n), 43n), true));
    });

    test("less() with integers", $ => {
        $(assert.equal(East.less(East.value(1n), 2n), true));
        $(assert.equal(East.less(East.value(2n), 1n), false));
        $(assert.equal(East.less(East.value(1n), 1n), false));
        $(assert.equal(East.less(East.value(-1n), 0n), true));
    });

    test("lessEqual() with integers", $ => {
        $(assert.equal(East.lessEqual(East.value(1n), 2n), true));
        $(assert.equal(East.lessEqual(East.value(2n), 1n), false));
        $(assert.equal(East.lessEqual(East.value(1n), 1n), true));
    });

    test("greater() with integers", $ => {
        $(assert.equal(East.greater(East.value(2n), 1n), true));
        $(assert.equal(East.greater(East.value(1n), 2n), false));
        $(assert.equal(East.greater(East.value(1n), 1n), false));
    });

    test("greaterEqual() with integers", $ => {
        $(assert.equal(East.greaterEqual(East.value(2n), 1n), true));
        $(assert.equal(East.greaterEqual(East.value(1n), 2n), false));
        $(assert.equal(East.greaterEqual(East.value(1n), 1n), true));
    });

    test("is() with integers", $ => {
        $(assert.equal(East.is(East.value(42n), 42n), true));
        $(assert.equal(East.is(East.value(42n), 43n), false));
    });

    test("equal() with floats", $ => {
        $(assert.equal(East.equal(East.value(0.0), 0.0), true));
        $(assert.equal(East.equal(East.value(3.14), 3.14), true));
        $(assert.equal(East.equal(East.value(3.14), 3.15), false));
        $(assert.equal(East.equal(East.value(-1.5), -1.5), true));
    });

    test("notEqual() with floats", $ => {
        $(assert.equal(East.notEqual(East.value(0.0), 0.0), false));
        $(assert.equal(East.notEqual(East.value(3.14), 3.15), true));
    });

    test("less() with floats", $ => {
        $(assert.equal(East.less(East.value(1.0), 2.0), true));
        $(assert.equal(East.less(East.value(2.0), 1.0), false));
        $(assert.equal(East.less(East.value(1.0), 1.0), false));
        $(assert.equal(East.less(East.value(-1.5), 0.0), true));
    });

    test("lessEqual() with floats", $ => {
        $(assert.equal(East.lessEqual(East.value(1.0), 2.0), true));
        $(assert.equal(East.lessEqual(East.value(2.0), 1.0), false));
        $(assert.equal(East.lessEqual(East.value(1.0), 1.0), true));
    });

    test("greater() with floats", $ => {
        $(assert.equal(East.greater(East.value(2.0), 1.0), true));
        $(assert.equal(East.greater(East.value(1.0), 2.0), false));
        $(assert.equal(East.greater(East.value(1.0), 1.0), false));
    });

    test("greaterEqual() with floats", $ => {
        $(assert.equal(East.greaterEqual(East.value(2.0), 1.0), true));
        $(assert.equal(East.greaterEqual(East.value(1.0), 2.0), false));
        $(assert.equal(East.greaterEqual(East.value(1.0), 1.0), true));
    });

    test("is() with floats", $ => {
        $(assert.equal(East.is(East.value(3.14), 3.14), true));
        $(assert.equal(East.is(East.value(3.14), 3.15), false));
    });

    test("Float NaN edge cases - is and equal", $ => {
        // NaN == NaN for is
        $(assert.equal(East.is(East.value(NaN), NaN), true));
        $(assert.equal(East.is(East.value(NaN), 0.0), false));
        $(assert.equal(East.is(East.value(0.0), NaN), false));

        // NaN == NaN for equal
        $(assert.equal(East.equal(East.value(NaN), NaN), true));
        $(assert.equal(East.equal(East.value(NaN), 0.0), false));
    });

    test("Float NaN edge cases - notEqual", $ => {
        $(assert.equal(East.notEqual(East.value(NaN), NaN), false));
        $(assert.equal(East.notEqual(East.value(NaN), 0.0), true));
        $(assert.equal(East.notEqual(East.value(0.0), NaN), true));
    });

    test("Float NaN edge cases - ordering (NaN is greatest)", $ => {
        $(assert.equal(East.less(East.value(0.0), NaN), true));
        $(assert.equal(East.less(East.value(NaN), 0.0), false));
        $(assert.equal(East.less(East.value(NaN), NaN), false));
    });

    test("Float -0 vs +0 edge case (Object.is distinguishes them)", $ => {
        $(assert.equal(East.less(East.value(-0.0), 0.0), true));
        $(assert.equal(East.less(East.value(0.0), -0.0), false));
        $(assert.equal(East.equal(East.value(-0.0), 0.0), false)); // Object.is checks -0 vs 0 (they are different)
    });

    test("Float Infinity edge cases", $ => {
        $(assert.equal(East.less(East.value(1.0), Infinity), true));
        $(assert.equal(East.less(East.value(Infinity), 1.0), false));
        $(assert.equal(East.less(East.value(-Infinity), 0.0), true));
        $(assert.equal(East.less(East.value(Infinity), NaN), true)); // NaN is greater than Infinity
    });

    test("equal() with strings", $ => {
        $(assert.equal(East.equal(East.value(""), ""), true));
        $(assert.equal(East.equal(East.value("hello"), "hello"), true));
        $(assert.equal(East.equal(East.value("hello"), "world"), false));
    });

    test("notEqual() with strings", $ => {
        $(assert.equal(East.notEqual(East.value("hello"), "hello"), false));
        $(assert.equal(East.notEqual(East.value("hello"), "world"), true));
    });

    test("less() with strings", $ => {
        $(assert.equal(East.less(East.value("a"), "b"), true));
        $(assert.equal(East.less(East.value("b"), "a"), false));
        $(assert.equal(East.less(East.value("a"), "a"), false));
        $(assert.equal(East.less(East.value("abc"), "abd"), true));
        $(assert.equal(East.less(East.value("ab"), "abc"), true));
    });

    test("lessEqual() with strings", $ => {
        $(assert.equal(East.lessEqual(East.value("a"), "b"), true));
        $(assert.equal(East.lessEqual(East.value("b"), "a"), false));
        $(assert.equal(East.lessEqual(East.value("a"), "a"), true));
    });

    test("greater() with strings", $ => {
        $(assert.equal(East.greater(East.value("b"), "a"), true));
        $(assert.equal(East.greater(East.value("a"), "b"), false));
        $(assert.equal(East.greater(East.value("a"), "a"), false));
    });

    test("greaterEqual() with strings", $ => {
        $(assert.equal(East.greaterEqual(East.value("b"), "a"), true));
        $(assert.equal(East.greaterEqual(East.value("a"), "b"), false));
        $(assert.equal(East.greaterEqual(East.value("a"), "a"), true));
    });

    test("is() with strings", $ => {
        $(assert.equal(East.is(East.value("hello"), "hello"), true));
        $(assert.equal(East.is(East.value("hello"), "world"), false));
    });

    test("equal() with dates", $ => {
        const d1 = new Date("2025-01-01T00:00:00Z");
        const d2 = new Date("2025-01-01T00:00:00Z");
        const d3 = new Date("2025-01-02T00:00:00Z");
        $(assert.equal(East.equal(East.value(d1), d2), true));
        $(assert.equal(East.equal(East.value(d1), d3), false));
    });

    test("notEqual() with dates", $ => {
        const d1 = new Date("2025-01-01T00:00:00Z");
        const d2 = new Date("2025-01-02T00:00:00Z");
        $(assert.equal(East.notEqual(East.value(d1), d2), true));
    });

    test("less() with dates", $ => {
        const d1 = new Date("2025-01-01T00:00:00Z");
        const d2 = new Date("2025-01-02T00:00:00Z");
        $(assert.equal(East.less(East.value(d1), d2), true));
        $(assert.equal(East.less(East.value(d2), d1), false));
    });

    test("is() with dates", $ => {
        const d1 = new Date("2025-01-01T00:00:00Z");
        const d2 = new Date("2025-01-01T00:00:00Z");
        $(assert.equal(East.is(East.value(d1), d2), true));
    });

    test("equal() with blobs", $ => {
        const b1 = new Uint8Array([1, 2, 3]);
        const b2 = new Uint8Array([1, 2, 3]);
        const b3 = new Uint8Array([1, 2, 4]);
        $(assert.equal(East.equal(East.value(b1), b2), true));
        $(assert.equal(East.equal(East.value(b1), b3), false));
    });

    test("notEqual() with blobs", $ => {
        const b1 = new Uint8Array([1, 2, 3]);
        const b2 = new Uint8Array([1, 2, 4]);
        $(assert.equal(East.notEqual(East.value(b1), b2), true));
    });

    test("less() with blobs", $ => {
        const b1 = new Uint8Array([1, 2]);
        const b2 = new Uint8Array([1, 2, 3]);
        const b3 = new Uint8Array([1, 3]);
        $(assert.equal(East.less(East.value(b1), b2), true));
        $(assert.equal(East.less(East.value(b1), b3), true));
        $(assert.equal(East.less(East.value(b2), b1), false));
    });

    test("Blob different lengths edge cases", $ => {
        const blob1 = new Uint8Array([1, 2, 3]);
        const blob2 = new Uint8Array([1, 2]);
        const blob3 = new Uint8Array([1, 2, 4]);

        // Different lengths
        $(assert.equal(East.equal(East.value(blob1), blob2), false));
        $(assert.equal(East.notEqual(East.value(blob1), blob2), true));
        $(assert.equal(East.less(East.value(blob2), blob1), true)); // shorter is less
        $(assert.equal(East.less(East.value(blob1), blob2), false));

        // Same length, different values
        $(assert.equal(East.equal(East.value(blob1), blob3), false));
        $(assert.equal(East.less(East.value(blob1), blob3), true));
        $(assert.equal(East.less(East.value(blob3), blob1), false));
    });

    test("Blob lexical comparison loops", $ => {
        // Different bytes in middle - tests loop bodies
        const blob1 = new Uint8Array([1, 2, 3, 4]);
        const blob2 = new Uint8Array([1, 2, 5, 4]); // different at index 2

        $(assert.equal(East.less(East.value(blob1), blob2), true));
        $(assert.equal(East.lessEqual(East.value(blob1), blob2), true));
        $(assert.equal(East.greater(East.value(blob2), blob1), true));
        $(assert.equal(East.greaterEqual(East.value(blob2), blob1), true));
        $(assert.equal(East.notEqual(East.value(blob1), blob2), true));

        // Equal blobs
        const blob3 = new Uint8Array([1, 2, 3, 4]);
        $(assert.equal(East.less(East.value(blob1), blob3), false));
        $(assert.equal(East.lessEqual(East.value(blob1), blob3), true));
        $(assert.equal(East.greater(East.value(blob1), blob3), false));
        $(assert.equal(East.greaterEqual(East.value(blob1), blob3), true));
        $(assert.equal(East.notEqual(East.value(blob1), blob3), false));
    });

    test("Blob is() - tests loop body for value comparison", $ => {
        // Test the loop body that compares byte-by-byte
        const blob1 = new Uint8Array([1, 2, 3, 4, 5]);
        const blob2 = new Uint8Array([1, 2, 3, 4, 5]); // same values
        const blob3 = new Uint8Array([1, 2, 3, 9, 5]); // different at index 3

        $(assert.equal(East.is(East.value(blob1), blob2), true));
        $(assert.equal(East.is(East.value(blob1), blob3), false));
    });

    test("equal() with arrays", $ => {
        $(assert.equal(East.equal(East.value([]), []), true));
        $(assert.equal(East.equal(East.value([1n, 2n, 3n]), [1n, 2n, 3n]), true));
        $(assert.equal(East.equal(East.value([1n, 2n, 3n]), [1n, 2n, 4n]), false));
        $(assert.equal(East.equal(East.value([1n, 2n]), [1n, 2n, 3n]), false));
    });

    test("notEqual() with arrays", $ => {
        $(assert.equal(East.notEqual(East.value([1n, 2n, 3n]), [1n, 2n, 3n]), false));
        $(assert.equal(East.notEqual(East.value([1n, 2n, 3n]), [1n, 2n, 4n]), true));
    });

    test("less() with arrays", $ => {
        $(assert.equal(East.less(East.value([], ArrayType(IntegerType)), [1n]), true));
        $(assert.equal(East.less(East.value([1n, 2n]), [1n, 2n, 3n]), true));
        $(assert.equal(East.less(East.value([1n, 2n]), [1n, 3n]), true));
        $(assert.equal(East.less(East.value([1n, 2n]), [2n]), true));
        $(assert.equal(East.less(East.value([1n, 2n]), [1n, 2n]), false));
    });

    test("lessEqual() with arrays", $ => {
        $(assert.equal(East.lessEqual(East.value([]), []), true));
        $(assert.equal(East.lessEqual(East.value([1n, 2n]), [1n, 2n]), true));
        $(assert.equal(East.lessEqual(East.value([1n, 2n]), [1n, 2n, 3n]), true));
    });

    test("greater() with arrays", $ => {
        $(assert.equal(East.greater(East.value([1n]), []), true));
        $(assert.equal(East.greater(East.value([1n, 2n, 3n]), [1n, 2n]), true));
        $(assert.equal(East.greater(East.value([1n, 3n]), [1n, 2n]), true));
    });

    test("greaterEqual() with arrays", $ => {
        $(assert.equal(East.greaterEqual(East.value([]), []), true));
        $(assert.equal(East.greaterEqual(East.value([1n, 2n]), [1n, 2n]), true));
        $(assert.equal(East.greaterEqual(East.value([1n, 2n, 3n]), [1n, 2n]), true));
    });

    test("is() with arrays - identity vs value equality", $ => {
        const a1 = $.let([1n, 2n, 3n]);
        const a2 = a1; // same reference
        const a3 = $.let([1n, 2n, 3n]); // different array, same values

        // is() compares by identity for mutable types
        $(assert.equal(East.is(a1, a2), true)); // same object
        $(assert.equal(East.is(a1, a3), false)); // different objects

        // equal() compares by deep value equality for arrays
        $(assert.equal(East.equal(a1, a3), true)); // same values
        $(assert.equal(East.notEqual(a1, a3), false)); // same values
    });

    test("Array length comparisons (prefix)", $ => {
        const arr1 = East.value([1n, 2n]);
        const arr2 = East.value([1n, 2n, 3n]);

        // Prefix comparison
        $(assert.equal(East.less(arr1, arr2), true));
        $(assert.equal(East.lessEqual(arr1, arr2), true));
        $(assert.equal(East.greater(arr2, arr1), true));
        $(assert.equal(East.greaterEqual(arr2, arr1), true));
    });

    test("equal() with sets", $ => {
        $(assert.equal(East.equal(East.value(new Set()), new Set()), true));
        $(assert.equal(East.equal(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n, 3n])), true));
        $(assert.equal(East.equal(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n, 4n])), false));
        $(assert.equal(East.equal(East.value(new Set([1n, 2n])), new Set([1n, 2n, 3n])), false));
    });

    test("notEqual() with sets", $ => {
        $(assert.equal(East.notEqual(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n, 3n])), false));
        $(assert.equal(East.notEqual(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n, 4n])), true));
    });

    test("less() with sets", $ => {
        $(assert.equal(East.less(East.value(new Set([]), SetType(IntegerType)), East.value(new Set([1n]))), true));
        $(assert.equal(East.less(East.value(new Set([1n, 2n])), new Set([1n, 2n, 3n])), true));
        $(assert.equal(East.less(East.value(new Set([1n, 2n])), new Set([1n, 3n])), true));
        $(assert.equal(East.less(East.value(new Set([1n, 2n])), new Set([1n, 2n])), false));
    });

    test("lessEqual() with sets", $ => {
        $(assert.equal(East.lessEqual(East.value(new Set()), new Set()), true));
        $(assert.equal(East.lessEqual(East.value(new Set([1n, 2n])), new Set([1n, 2n])), true));
        $(assert.equal(East.lessEqual(East.value(new Set([1n, 2n])), new Set([1n, 2n, 3n])), true));
    });

    test("greater() with sets", $ => {
        $(assert.equal(East.greater(East.value(new Set([1n])), new Set()), true));
        $(assert.equal(East.greater(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n])), true));
    });

    test("greaterEqual() with sets", $ => {
        $(assert.equal(East.greaterEqual(East.value(new Set()), new Set()), true));
        $(assert.equal(East.greaterEqual(East.value(new Set([1n, 2n])), new Set([1n, 2n])), true));
        $(assert.equal(East.greaterEqual(East.value(new Set([1n, 2n, 3n])), new Set([1n, 2n])), true));
    });

    test("is() with sets - identity", $ => {
        const s1 = $.let(new Set([1n, 2n, 3n]));
        const s2 = s1;
        const s3 = $.let(new Set([1n, 2n, 3n]));
        $(assert.equal(East.is(s1, s2), true));
        $(assert.equal(East.is(s1, s3), false));
    });

    test("Set value comparisons edge cases", $ => {
        const set1 = new Set(['a', 'b', 'c']);
        const set2 = new Set(['a', 'b', 'c']);
        const set3 = new Set(['a', 'b', 'd']);
        const set4 = new Set(['a', 'b']);

        // Same values
        $(assert.equal(East.equal(East.value(set1, SetType(StringType)), set2), true));
        $(assert.equal(East.notEqual(East.value(set1, SetType(StringType)), set2), false));

        // Different values
        $(assert.equal(East.equal(East.value(set1, SetType(StringType)), set3), false));
        $(assert.equal(East.notEqual(East.value(set1, SetType(StringType)), set3), true));

        // Different sizes
        $(assert.equal(East.equal(East.value(set1, SetType(StringType)), set4), false));
        $(assert.equal(East.notEqual(East.value(set1, SetType(StringType)), set4), true));
    });

    test("Set prefix comparisons", $ => {
        // SortedSet maintains order
        const set1 = new Set([1n, 2n]);
        const set2 = new Set([1n, 2n, 3n]);
        const set3 = new Set([1n, 2n]);

        // Prefix: set1 < set2
        $(assert.equal(East.less(East.value(set1), set2), true));
        $(assert.equal(East.lessEqual(East.value(set1), set2), true));
        $(assert.equal(East.greater(East.value(set2), set1), true));
        $(assert.equal(East.greaterEqual(East.value(set2), set1), true));

        // Equal
        $(assert.equal(East.lessEqual(East.value(set1), set3), true));
        $(assert.equal(East.greaterEqual(East.value(set1), set3), true));
    });

    test("Set prefix where x.size > y.size", $ => {
        // x is longer and y is prefix
        const set1 = new Set([1n, 2n, 3n, 4n]);
        const set2 = new Set([1n, 2n, 3n]);

        $(assert.equal(East.greater(East.value(set1), set2), true));
    });

    test("Set greater() when all elements match", $ => {
        // Same size and all elements equal
        const set1 = new Set([1n, 2n, 3n]);
        const set2 = new Set([1n, 2n, 3n]);

        // Should return x.size > y.size which is false
        $(assert.equal(East.greater(East.value(set1), set2), false));
    });

    test("Set ordering with compound types (structs)", $ => {
        const setType = SetType(StructType({ x: IntegerType, y: IntegerType }));
        const set1 = East.value(new Set([{ x: 1n, y: 2n }]), setType);
        const set2 = East.value(new Set([{ x: 1n, y: 3n }]), setType);
        const set3 = East.value(new Set([{ x: 2n, y: 1n }]), setType);
        const set4 = East.value(new Set([{ x: 1n, y: 2n }, { x: 2n, y: 1n }]), setType);

        // set1 < set2 (y field differs in element)
        $(assert.equal(East.less(set1, set2), true));

        // set1 < set3 (x field differs in element)
        $(assert.equal(East.less(set1, set3), true));

        // set1 < set4 (set1 is prefix of set4)
        $(assert.equal(East.less(set1, set4), true));
    });

    test("Set ordering with variants", $ => {
        const setType = SetType(VariantType({ none: NullType, some: IntegerType }));
        const set1 = East.value(new Set([none]), setType);
        const set2 = East.value(new Set([some(1n)]), setType);
        const set3 = East.value(new Set([some(2n)]), setType);
        const set4 = East.value(new Set([none, some(1n)]), setType);

        // set1 < set2 (none < some)
        $(assert.equal(East.less(set1, set2), true));

        // set2 < set3 (same tag, value differs)
        $(assert.equal(East.less(set2, set3), true));

        // set1 < set4 (set1 is prefix)
        $(assert.equal(East.less(set1, set4), true));
    });

    test("equal() with dicts", $ => {
        $(assert.equal(East.equal(East.value(new Map()), new Map()), true));
        $(assert.equal(East.equal(East.value(new Map([["a", 1n], ["b", 2n]])), new Map([["a", 1n], ["b", 2n]])), true));
        $(assert.equal(East.equal(East.value(new Map([["a", 1n], ["b", 2n]])), new Map([["a", 1n], ["b", 3n]])), false));
        $(assert.equal(East.equal(East.value(new Map([["a", 1n]])), new Map([["a", 1n], ["b", 2n]])), false));
    });

    test("notEqual() with dicts", $ => {
        $(assert.equal(East.notEqual(East.value(new Map([["a", 1n], ["b", 2n]])), new Map([["a", 1n], ["b", 2n]])), false));
        $(assert.equal(East.notEqual(East.value(new Map([["a", 1n], ["b", 2n]])), new Map([["a", 1n], ["b", 3n]])), true));
    });

    test("less() with dicts", $ => {
        $(assert.equal(East.less(East.value(new Map(), DictType(StringType, IntegerType)), new Map([["a", 1n]])), true));
        $(assert.equal(East.less(East.value(new Map([["a", 1n]])), new Map([["a", 1n], ["b", 2n]])), true));
        $(assert.equal(East.less(East.value(new Map([["a", 1n]])), new Map([["b", 1n]])), true));
        $(assert.equal(East.less(East.value(new Map([["a", 1n]])), new Map([["a", 1n]])), false));
    });

    test("lessEqual() with dicts", $ => {
        $(assert.equal(East.lessEqual(East.value(new Map()), new Map()), true));
        $(assert.equal(East.lessEqual(East.value(new Map([["a", 1n]])), new Map([["a", 1n]])), true));
        $(assert.equal(East.lessEqual(East.value(new Map([["a", 1n]])), new Map([["a", 1n], ["b", 2n]])), true));
    });

    test("greater() with dicts", $ => {
        $(assert.equal(East.greater(East.value(new Map([["a", 1n]])), new Map()), true));
        $(assert.equal(East.greater(East.value(new Map([["a", 1n], ["b", 2n]])), new Map([["a", 1n]])), true));
    });

    test("greaterEqual() with dicts", $ => {
        $(assert.equal(East.greaterEqual(East.value(new Map()), new Map()), true));
        $(assert.equal(East.greaterEqual(East.value(new Map([["a", 1n]])), new Map([["a", 1n]])), true));
        $(assert.equal(East.greaterEqual(East.value(new Map([["a", 1n], ["b", 2n]])), new Map([["a", 1n]])), true));
    });

    test("is() with dicts - identity", $ => {
        const d1 = $.let(new Map([["a", 1n], ["b", 2n]]));
        const d2 = d1;
        const d3 = $.let(new Map([["a", 1n], ["b", 2n]]));
        $(assert.equal(East.is(d1, d2), true));
        $(assert.equal(East.is(d1, d3), false));
    });

    test("dict with compound type keys - order matters", $ => {
        const d1 = East.value(new Map([[{ x: 1n, y: 2n }, "a"], [{ x: 2n, y: 1n }, "b"]]), DictType(StructType({ x: IntegerType, y: IntegerType }), StringType));
        const d2 = East.value(new Map([[{ x: 1n, y: 2n }, "a"], [{ x: 2n, y: 1n }, "b"]]), DictType(StructType({ x: IntegerType, y: IntegerType }), StringType));
        $(assert.equal(d1, d2));

        // Different key order in struct definition
        const d3 = East.value(new Map([[{ x: 2n, y: 1n }, "b"], [{ x: 1n, y: 2n }, "a"]]), DictType(StructType({ x: IntegerType, y: IntegerType }), StringType));
        $(assert.equal(d1, d3));
    });

    test("dict comparison with compound keys", $ => {
        const d1 = East.value(new Map([[{ x: 1n, y: 2n }, "a"]]), DictType(StructType({ x: IntegerType, y: IntegerType }), StringType));
        const d2 = East.value(new Map([[{ x: 1n, y: 3n }, "a"]]), DictType(StructType({ x: IntegerType, y: IntegerType }), StringType));
        const d3 = East.value(new Map([[{ x: 2n, y: 1n }, "a"]]), DictType(StructType({ x: IntegerType, y: IntegerType }), StringType));

        // d1 < d2 (y field differs)
        $(assert.equal(East.less(d1, d2), true));

        // d1 < d3 (x field differs)
        $(assert.equal(East.less(d1, d3), true));
    });

    test("Dict value comparisons edge cases", $ => {
        const dict1 = new Map([['a', 1n], ['b', 2n]]);
        const dict2 = new Map([['a', 1n], ['b', 2n]]);
        const dict3 = new Map([['a', 1n], ['b', 3n]]);
        const dict4 = new Map([['a', 1n]]);
        const dict5 = new Map([['a', 1n], ['c', 2n]]);

        // Same values
        $(assert.equal(East.equal(East.value(dict1), dict2), true));
        $(assert.equal(East.notEqual(East.value(dict1), dict2), false));

        // Different values (same keys)
        $(assert.equal(East.equal(East.value(dict1), dict3), false));
        $(assert.equal(East.notEqual(East.value(dict1), dict3), true));

        // Different size
        $(assert.equal(East.equal(East.value(dict1), dict4), false));

        // Missing key
        $(assert.equal(East.equal(East.value(dict1), dict5), false));
        $(assert.equal(East.notEqual(East.value(dict1), dict5), true));
    });

    test("Dict prefix comparisons", $ => {
        const dict1 = new Map([['a', 1n]]);
        const dict2 = new Map([['a', 1n], ['b', 2n]]);
        const dict3 = new Map([['a', 1n]]);

        // Prefix: dict1 < dict2
        $(assert.equal(East.less(East.value(dict1), dict2), true));
        $(assert.equal(East.lessEqual(East.value(dict1), dict2), true));
        $(assert.equal(East.greater(East.value(dict2), dict1), true));
        $(assert.equal(East.greaterEqual(East.value(dict2), dict1), true));

        // Equal
        $(assert.equal(East.lessEqual(East.value(dict1), dict3), true));
        $(assert.equal(East.greaterEqual(East.value(dict1), dict3), true));
    });

    test("Dict prefix where x.size > y.size", $ => {
        // x is longer and y is prefix
        const dict1 = new Map([['a', 1n], ['b', 2n], ['c', 3n]]);
        const dict2 = new Map([['a', 1n], ['b', 2n]]);

        $(assert.equal(East.greater(East.value(dict1), dict2), true));
    });

    test("Dict greater() when all entries match", $ => {
        // Same size and all entries equal
        const dict1 = new Map([['a', 1n], ['b', 2n]]);
        const dict2 = new Map([['a', 1n], ['b', 2n]]);

        // Should return x.size > y.size which is false
        $(assert.equal(East.greater(East.value(dict1), dict2), false));
    });

    test("Dict ordering with compound struct keys", $ => {
        const dictType = DictType(StructType({ x: IntegerType, y: IntegerType }), StringType);

        // Dicts compared key by key in sorted order
        const d1 = East.value(new Map([[{ x: 1n, y: 2n }, "a"]]), dictType);
        const d2 = East.value(new Map([[{ x: 1n, y: 3n }, "a"]]), dictType);
        const d3 = East.value(new Map([[{ x: 2n, y: 1n }, "a"]]), dictType);

        // d1 < d2 (same x, y differs)
        $(assert.equal(East.less(d1, d2), true));

        // d1 < d3 (x differs, takes priority)
        $(assert.equal(East.less(d1, d3), true));

        // Multiple keys - sorted key order matters
        const d4 = East.value(new Map([[{ x: 1n, y: 1n }, "a"], [{ x: 2n, y: 1n }, "b"]]), dictType);
        const d5 = East.value(new Map([[{ x: 1n, y: 1n }, "a"], [{ x: 2n, y: 2n }, "b"]]), dictType);

        // d4 < d5 (second key differs)
        $(assert.equal(East.less(d4, d5), true));
    });

    test("Dict ordering with variant keys", $ => {
        const dictType = DictType(VariantType({ none: NullType, some: IntegerType }), StringType);

        const d1 = East.value(new Map([[none, "a"]]), dictType);
        const d2 = East.value(new Map([[some(1n), "a"]]), dictType);
        const d3 = East.value(new Map([[some(2n), "a"]]), dictType);

        // d1 < d2 (none < some)
        $(assert.equal(East.less(d1, d2), true));

        // d2 < d3 (same tag, value differs)
        $(assert.equal(East.less(d2, d3), true));
    });

    test("Dict ordering with compound struct values", $ => {
        const dictType = DictType(StringType, StructType({ x: IntegerType, y: IntegerType }));

        const d1 = East.value(new Map([["a", { x: 1n, y: 2n }]]), dictType);
        const d2 = East.value(new Map([["a", { x: 1n, y: 3n }]]), dictType);
        const d3 = East.value(new Map([["a", { x: 2n, y: 1n }]]), dictType);

        // Same key, values differ
        $(assert.equal(East.less(d1, d2), true));
        $(assert.equal(East.less(d1, d3), true));

        // Multiple entries - compared in sorted key order
        const d4 = East.value(new Map([["a", { x: 1n, y: 1n }], ["b", { x: 1n, y: 1n }]]), dictType);
        const d5 = East.value(new Map([["a", { x: 1n, y: 1n }], ["b", { x: 2n, y: 1n }]]), dictType);

        // Same first entry, second value differs
        $(assert.equal(East.less(d4, d5), true));
    });

    test("Dict ordering - keys compared before values", $ => {
        const dictType = DictType(StringType, IntegerType);

        // Even if first dict has larger value, keys determine order
        const d1 = East.value(new Map([["a", 100n]]), dictType);
        const d2 = East.value(new Map([["b", 1n]]), dictType);

        // d1 < d2 because "a" < "b" (keys matter more than values)
        $(assert.equal(East.less(d1, d2), true));

        // When keys are equal, values matter
        const d3 = East.value(new Map([["a", 1n]]), dictType);
        const d4 = East.value(new Map([["a", 2n]]), dictType);

        $(assert.equal(East.less(d3, d4), true));
    });

    test("equal() with structs", $ => {
        $(assert.equal(East.equal(East.value({ x: 1n, y: 2n }), { x: 1n, y: 2n }), true));
        $(assert.equal(East.equal(East.value({ x: 1n, y: 2n }), { x: 1n, y: 3n }), false));
        $(assert.equal(East.equal(East.value({ x: 1n, y: 2n }), { x: 2n, y: 2n }), false));
    });

    test("notEqual() with structs", $ => {
        $(assert.equal(East.notEqual(East.value({ x: 1n, y: 2n }), { x: 1n, y: 2n }), false));
        $(assert.equal(East.notEqual(East.value({ x: 1n, y: 2n }), { x: 1n, y: 3n }), true));
    });

    test("less() with structs - field order matters", $ => {
        $(assert.equal(East.less(East.value({ x: 1n, y: 2n }), { x: 1n, y: 3n }), true));
        $(assert.equal(East.less(East.value({ x: 1n, y: 2n }), { x: 2n, y: 1n }), true));
        $(assert.equal(East.less(East.value({ x: 1n, y: 2n }), { x: 1n, y: 2n }), false));
    });

    test("lessEqual() with structs", $ => {
        $(assert.equal(East.lessEqual(East.value({ x: 1n, y: 2n }), { x: 1n, y: 2n }), true));
        $(assert.equal(East.lessEqual(East.value({ x: 1n, y: 2n }), { x: 1n, y: 3n }), true));
    });

    test("greater() with structs", $ => {
        $(assert.equal(East.greater(East.value({ x: 1n, y: 3n }), { x: 1n, y: 2n }), true));
        $(assert.equal(East.greater(East.value({ x: 2n, y: 1n }), { x: 1n, y: 2n }), true));
        $(assert.equal(East.greater(East.value({ x: 1n, y: 2n }), { x: 1n, y: 2n }), false));
    });

    test("greaterEqual() with structs", $ => {
        $(assert.equal(East.greaterEqual(East.value({ x: 1n, y: 2n }), { x: 1n, y: 2n }), true));
        $(assert.equal(East.greaterEqual(East.value({ x: 1n, y: 3n }), { x: 1n, y: 2n }), true));
    });

    test("is() with structs", $ => {
        $(assert.equal(East.is(East.value({ x: 1n, y: 2n }), { x: 1n, y: 2n }), true));
        $(assert.equal(East.is(East.value({ x: 1n, y: 2n }), { x: 1n, y: 3n }), false));
    });

    test("Struct field mismatches", $ => {
        const struct1 = { a: 1n, b: 'hello' };
        const struct2 = { a: 1n, b: 'hello' };
        const struct3 = { a: 2n, b: 'hello' };
        const struct4 = { a: 1n, b: 'world' };

        // Same values
        $(assert.equal(East.equal(East.value(struct1), struct2), true));
        $(assert.equal(East.notEqual(East.value(struct1), struct2), false));

        // First field differs
        $(assert.equal(East.equal(East.value(struct1), struct3), false));
        $(assert.equal(East.notEqual(East.value(struct1), struct3), true));
        $(assert.equal(East.less(East.value(struct1), struct3), true));
        $(assert.equal(East.less(East.value(struct3), struct1), false));

        // Second field differs
        $(assert.equal(East.equal(East.value(struct1), struct4), false));
        $(assert.equal(East.less(East.value(struct1), struct4), true));
    });

    test("Struct field-by-field comparison", $ => {
        const struct1 = { a: 1n, b: 2n };
        const struct2 = { a: 1n, b: 3n };
        const struct3 = { a: 1n, b: 2n };

        // struct1 <= struct2
        $(assert.equal(East.lessEqual(East.value(struct1), struct2), true));
        $(assert.equal(East.greaterEqual(East.value(struct2), struct1), true));

        // struct1 == struct3
        $(assert.equal(East.lessEqual(East.value(struct1), struct3), true));
        $(assert.equal(East.greaterEqual(East.value(struct1), struct3), true));
    });

    test("Struct greater() with all fields equal", $ => {
        const struct1 = { x: 1n, y: 2n };
        const struct2 = { x: 1n, y: 2n };

        // All fields equal means not greater
        $(assert.equal(East.greater(East.value(struct1), struct2), false));
    });

    test("Struct field mismatch in is()", $ => {
        const struct1 = { x: 1n, y: 2n };
        const struct2 = { x: 1n, y: 3n }; // different y

        // is() checks all fields, returns false on first mismatch
        $(assert.equal(East.is(East.value(struct1), struct2), false));
    });

    test("equal() with variants", $ => {
        $(assert.equal(East.equal(East.value(some(5n), OptionType(IntegerType)), some(5n)), true));
        $(assert.equal(East.equal(East.value(some(5n), OptionType(IntegerType)), some(6n)), false));
        $(assert.equal(East.equal(East.value(some(5n), OptionType(IntegerType)), none), false));
        $(assert.equal(East.equal(East.value(none, OptionType(IntegerType)), none), true));
    });

    test("notEqual() with variants", $ => {
        $(assert.equal(East.notEqual(East.value(some(5n), OptionType(IntegerType)), some(5n)), false));
        $(assert.equal(East.notEqual(East.value(some(5n), OptionType(IntegerType)), some(6n)), true));
        $(assert.equal(East.notEqual(East.value(some(5n), OptionType(IntegerType)), none), true));
    });

    test("less() with variants - tag order matters", $ => {
        $(assert.equal(East.less(East.value(none, OptionType(IntegerType)), some(5n)), true));
        $(assert.equal(East.less(East.value(some(5n), OptionType(IntegerType)), none), false));
        $(assert.equal(East.less(East.value(some(5n), OptionType(IntegerType)), some(6n)), true));
        $(assert.equal(East.less(East.value(some(5n), OptionType(IntegerType)), some(5n)), false));
    });

    test("lessEqual() with variants", $ => {
        $(assert.equal(East.lessEqual(East.value(none), none), true));
        $(assert.equal(East.lessEqual(East.value(none, OptionType(IntegerType)), some(5n)), true));
        $(assert.equal(East.lessEqual(East.value(some(5n), OptionType(IntegerType)), some(5n)), true));
    });

    test("greater() with variants", $ => {
        $(assert.equal(East.greater(East.value(some(5n), OptionType(IntegerType)), none), true));
        $(assert.equal(East.greater(East.value(none, OptionType(IntegerType)), some(5n)), false));
        $(assert.equal(East.greater(East.value(some(6n), OptionType(IntegerType)), some(5n)), true));
    });

    test("greaterEqual() with variants", $ => {
        $(assert.equal(East.greaterEqual(East.value(none, OptionType(IntegerType)), none), true));
        $(assert.equal(East.greaterEqual(East.value(some(5n), OptionType(IntegerType)), none), true));
        $(assert.equal(East.greaterEqual(East.value(some(5n), OptionType(IntegerType)), some(5n)), true));
    });

    test("is() with variants", $ => {
        $(assert.equal(East.is(East.value(some(5n), OptionType(IntegerType)), some(5n)), true));
        $(assert.equal(East.is(East.value(some(5n), OptionType(IntegerType)), some(6n)), false));
        $(assert.equal(East.is(East.value(none, OptionType(IntegerType)), none), true));
    });

    test("Variant type mismatches", $ => {
        const v1 = none;
        const v2 = none;
        const v3 = some(5n);
        const v4 = some(10n);

        // Same type and value
        $(assert.equal(East.equal(East.value(v1, OptionType(IntegerType)), v2), true));
        $(assert.equal(East.notEqual(East.value(v1, OptionType(IntegerType)), v2), false));

        // Different type
        $(assert.equal(East.equal(East.value(v1, OptionType(IntegerType)), v3), false));
        $(assert.equal(East.notEqual(East.value(v1, OptionType(IntegerType)), v3), true));
        $(assert.equal(East.less(East.value(v1, OptionType(IntegerType)), v3), true)); // 'none' < 'some'
        $(assert.equal(East.less(East.value(v3, OptionType(IntegerType)), v1), false));

        // Same type, different value
        $(assert.equal(East.equal(East.value(v3, OptionType(IntegerType)), v4), false));
        $(assert.equal(East.less(East.value(v3, OptionType(IntegerType)), v4), true));
    });

    test("Variant lessEqual and greaterEqual", $ => {
        const vType = VariantType({ a: IntegerType, b: IntegerType });
        const v1 = East.value(variant('a', 5n), vType);
        const v2 = East.value(variant('b', 3n), vType);
        const v3 = East.value(variant('b', 5n), vType);
        const v4 = East.value(variant('b', 3n), vType);

        // v1 < v2 (by type)
        $(assert.equal(East.lessEqual(v1, v2), true));
        $(assert.equal(East.greaterEqual(v2, v1), true));

        // v2 < v3 (same type, by value)
        $(assert.equal(East.lessEqual(v2, v3), true));
        $(assert.equal(East.greaterEqual(v3, v2), true));

        // v2 == v4
        $(assert.equal(East.lessEqual(v2, v4), true));
        $(assert.equal(East.greaterEqual(v2, v4), true));
    });

    test("min() with null", $ => {
        $(assert.equal(East.min(East.value(null), null), null));
    });

    test("min() with booleans", $ => {
        $(assert.equal(East.min(East.value(false), true), false));
        $(assert.equal(East.min(East.value(true), false), false));
        $(assert.equal(East.min(East.value(true), true), true));
        $(assert.equal(East.min(East.value(false), false), false));
    });

    test("min() with integers", $ => {
        $(assert.equal(East.min(East.value(5n), 10n), 5n));
        $(assert.equal(East.min(East.value(10n), 5n), 5n));
        $(assert.equal(East.min(East.value(7n), 7n), 7n));
        $(assert.equal(East.min(East.value(-5n), -10n), -10n));
    });

    test("min() with floats", $ => {
        $(assert.equal(East.min(East.value(3.14), 2.71), 2.71));
        $(assert.equal(East.min(East.value(2.71), 3.14), 2.71));
        $(assert.equal(East.min(East.value(5.0), 5.0), 5.0));
    });

    test("min() with strings", $ => {
        $(assert.equal(East.min(East.value("b"), "a"), "a"));
        $(assert.equal(East.min(East.value("a"), "b"), "a"));
        $(assert.equal(East.min(East.value("hello"), "hello"), "hello"));
    });

    test("min() with datetimes", $ => {
        const d1 = new Date("2025-01-01T00:00:00Z");
        const d2 = new Date("2025-01-02T00:00:00Z");
        $(assert.equal(East.min(East.value(d1), d2), d1));
        $(assert.equal(East.min(East.value(d2), d1), d1));
        $(assert.equal(East.min(East.value(d1), d1), d1));
    });

    test("min() with blobs", $ => {
        const b1 = new Uint8Array([1, 2, 3]);
        const b2 = new Uint8Array([1, 2, 4]);
        $(assert.equal(East.min(East.value(b1), b2), b1));
        $(assert.equal(East.min(East.value(b2), b1), b1));
    });

    test("min() with arrays", $ => {
        $(assert.equal(East.min(East.value([1n, 2n]), [1n, 3n]), [1n, 2n]));
        $(assert.equal(East.min(East.value([1n, 3n]), [1n, 2n]), [1n, 2n]));
    });

    test("min() with sets", $ => {
        $(assert.equal(East.min(East.value(new Set([1n, 2n])), new Set([1n, 3n])), new Set([1n, 2n])));
        $(assert.equal(East.min(East.value(new Set([1n, 3n])), new Set([1n, 2n])), new Set([1n, 2n])));
    });

    test("min() with dicts", $ => {
        const d1 = new Map([["a", 1n], ["b", 2n]]);
        const d2 = new Map([["a", 1n], ["b", 3n]]);
        $(assert.equal(East.min(East.value(d1), d2), d1));
        $(assert.equal(East.min(East.value(d2), d1), d1));
    });

    test("min() with structs", $ => {
        $(assert.equal(East.min(East.value({ x: 1n, y: 2n }), { x: 1n, y: 3n }), { x: 1n, y: 2n }));
        $(assert.equal(East.min(East.value({ x: 1n, y: 3n }), { x: 1n, y: 2n }), { x: 1n, y: 2n }));
    });

    test("min() with variants", $ => {
        $(assert.equal(East.min(East.value(none, OptionType(IntegerType)), some(5n)), none));
        $(assert.equal(East.min(East.value(some(5n), OptionType(IntegerType)), none), none));
        $(assert.equal(East.min(East.value(some(5n), OptionType(IntegerType)), some(10n)), some(5n)));
    });

    test("max() with null", $ => {
        $(assert.equal(East.max(East.value(null), null), null));
    });

    test("max() with booleans", $ => {
        $(assert.equal(East.max(East.value(false), true), true));
        $(assert.equal(East.max(East.value(true), false), true));
        $(assert.equal(East.max(East.value(true), true), true));
        $(assert.equal(East.max(East.value(false), false), false));
    });

    test("max() with integers", $ => {
        $(assert.equal(East.max(East.value(5n), 10n), 10n));
        $(assert.equal(East.max(East.value(10n), 5n), 10n));
        $(assert.equal(East.max(East.value(7n), 7n), 7n));
        $(assert.equal(East.max(East.value(-5n), -10n), -5n));
    });

    test("max() with floats", $ => {
        $(assert.equal(East.max(East.value(3.14), 2.71), 3.14));
        $(assert.equal(East.max(East.value(2.71), 3.14), 3.14));
        $(assert.equal(East.max(East.value(5.0), 5.0), 5.0));
    });

    test("max() with strings", $ => {
        $(assert.equal(East.max(East.value("a"), "b"), "b"));
        $(assert.equal(East.max(East.value("b"), "a"), "b"));
        $(assert.equal(East.max(East.value("hello"), "hello"), "hello"));
    });

    test("max() with datetimes", $ => {
        const d1 = new Date("2025-01-01T00:00:00Z");
        const d2 = new Date("2025-01-02T00:00:00Z");
        $(assert.equal(East.max(East.value(d1), d2), d2));
        $(assert.equal(East.max(East.value(d2), d1), d2));
        $(assert.equal(East.max(East.value(d1), d1), d1));
    });

    test("max() with blobs", $ => {
        const b1 = new Uint8Array([1, 2, 3]);
        const b2 = new Uint8Array([1, 2, 4]);
        $(assert.equal(East.max(East.value(b1), b2), b2));
        $(assert.equal(East.max(East.value(b2), b1), b2));
    });

    test("max() with arrays", $ => {
        $(assert.equal(East.max(East.value([1n, 2n]), [1n, 3n]), [1n, 3n]));
        $(assert.equal(East.max(East.value([1n, 3n]), [1n, 2n]), [1n, 3n]));
    });

    test("max() with sets", $ => {
        $(assert.equal(East.max(East.value(new Set([1n, 2n])), new Set([1n, 3n])), new Set([1n, 3n])));
        $(assert.equal(East.max(East.value(new Set([1n, 3n])), new Set([1n, 2n])), new Set([1n, 3n])));
    });

    test("max() with dicts", $ => {
        const d1 = new Map([["a", 1n], ["b", 2n]]);
        const d2 = new Map([["a", 1n], ["b", 3n]]);
        $(assert.equal(East.max(East.value(d1), d2), d2));
        $(assert.equal(East.max(East.value(d2), d1), d2));
    });

    test("max() with structs", $ => {
        $(assert.equal(East.max(East.value({ x: 1n, y: 2n }), { x: 1n, y: 3n }), { x: 1n, y: 3n }));
        $(assert.equal(East.max(East.value({ x: 1n, y: 3n }), { x: 1n, y: 2n }), { x: 1n, y: 3n }));
    });

    test("max() with variants", $ => {
        $(assert.equal(East.max(East.value(none, OptionType(IntegerType)), some(5n)), some(5n)));
        $(assert.equal(East.max(East.value(some(5n), OptionType(IntegerType)), none), some(5n)));
        $(assert.equal(East.max(East.value(some(5n), OptionType(IntegerType)), some(10n)), some(10n)));
    });

    test("clamp() with null", $ => {
        $(assert.equal(East.clamp(East.value(null), null, null), null));
    });

    test("clamp() with booleans", $ => {
        $(assert.equal(East.clamp(East.value(false), false, true), false));
        $(assert.equal(East.clamp(East.value(true), false, true), true));
    });

    test("clamp() with integers", $ => {
        $(assert.equal(East.clamp(East.value(5n), 0n, 10n), 5n));
        $(assert.equal(East.clamp(East.value(-5n), 0n, 10n), 0n));
        $(assert.equal(East.clamp(East.value(15n), 0n, 10n), 10n));
        $(assert.equal(East.clamp(East.value(0n), 0n, 10n), 0n));
        $(assert.equal(East.clamp(East.value(10n), 0n, 10n), 10n));
    });

    test("clamp() with floats", $ => {
        $(assert.equal(East.clamp(East.value(5.0), 0.0, 10.0), 5.0));
        $(assert.equal(East.clamp(East.value(-5.0), 0.0, 10.0), 0.0));
        $(assert.equal(East.clamp(East.value(15.0), 0.0, 10.0), 10.0));
    });

    test("clamp() with strings", $ => {
        $(assert.equal(East.clamp(East.value("m"), "a", "z"), "m"));
        $(assert.equal(East.clamp(East.value("aaa"), "b", "y"), "b"));
        $(assert.equal(East.clamp(East.value("zzz"), "b", "y"), "y"));
    });

    test("clamp() with datetimes", $ => {
        const d1 = new Date("2025-01-01T00:00:00Z");
        const d2 = new Date("2025-01-15T00:00:00Z");
        const d3 = new Date("2025-01-31T00:00:00Z");
        $(assert.equal(East.clamp(East.value(d2), d1, d3), d2));
        $(assert.equal(East.clamp(East.value(new Date("2024-12-01T00:00:00Z")), d1, d3), d1));
        $(assert.equal(East.clamp(East.value(new Date("2025-02-15T00:00:00Z")), d1, d3), d3));
    });

    test("clamp() with blobs", $ => {
        const b1 = new Uint8Array([1, 2, 3]);
        const b2 = new Uint8Array([1, 2, 5]);
        const b3 = new Uint8Array([1, 2, 7]);
        $(assert.equal(East.clamp(East.value(b2), b1, b3), b2));
        $(assert.equal(East.clamp(East.value(new Uint8Array([1, 2, 2])), b1, b3), b1));
        $(assert.equal(East.clamp(East.value(new Uint8Array([1, 2, 9])), b1, b3), b3));
    });

    test("clamp() with arrays", $ => {
        $(assert.equal(East.clamp(East.value([1n, 5n]), [1n, 0n], [1n, 10n]), [1n, 5n]));
        $(assert.equal(East.clamp(East.value([0n, 5n]), [1n, 0n], [1n, 10n]), [1n, 0n]));
        $(assert.equal(East.clamp(East.value([1n, 15n]), [1n, 0n], [1n, 10n]), [1n, 10n]));
    });

    test("clamp() with sets", $ => {
        const s1 = new Set([1n, 2n]);
        const s2 = new Set([1n, 5n]);
        const s3 = new Set([1n, 8n]);
        $(assert.equal(East.clamp(East.value(s2), s1, s3), s2));
        $(assert.equal(East.clamp(East.value(new Set([1n, 0n])), s1, s3), s1));
        $(assert.equal(East.clamp(East.value(new Set([1n, 9n])), s1, s3), s3));
    });

    test("clamp() with dicts", $ => {
        const d1 = new Map([["a", 1n]]);
        const d2 = new Map([["a", 5n]]);
        const d3 = new Map([["a", 10n]]);
        $(assert.equal(East.clamp(East.value(d2), d1, d3), d2));
        $(assert.equal(East.clamp(East.value(new Map([["a", 0n]])), d1, d3), d1));
        $(assert.equal(East.clamp(East.value(new Map([["a", 15n]])), d1, d3), d3));
    });

    test("clamp() with structs", $ => {
        $(assert.equal(East.clamp(East.value({ x: 1n, y: 5n }), { x: 1n, y: 0n }, { x: 1n, y: 10n }), { x: 1n, y: 5n }));
        $(assert.equal(East.clamp(East.value({ x: 1n, y: -5n }), { x: 1n, y: 0n }, { x: 1n, y: 10n }), { x: 1n, y: 0n }));
        $(assert.equal(East.clamp(East.value({ x: 1n, y: 15n }), { x: 1n, y: 0n }, { x: 1n, y: 10n }), { x: 1n, y: 10n }));
    });

    test("clamp() with variants", $ => {
        $(assert.equal(East.clamp(East.value(some(5n), OptionType(IntegerType)), none, some(10n)), some(5n)));
        $(assert.equal(East.clamp(East.value(none, OptionType(IntegerType)), none, some(10n)), none));
        $(assert.equal(East.clamp(East.value(some(15n), OptionType(IntegerType)), none, some(10n)), some(10n)));
    });

    test("print() with null", $ => {
        $(assert.equal(East.print(East.value(null)), "null"));
    });

    test("print() with boolean", $ => {
        $(assert.equal(East.print(East.value(true)), "true"));
        $(assert.equal(East.print(East.value(false)), "false"));
    });

    test("print() with integer", $ => {
        $(assert.equal(East.print(East.value(42n)), "42"));
        $(assert.equal(East.print(East.value(-42n)), "-42"));
        $(assert.equal(East.print(East.value(0n)), "0"));
    });

    test("print() with float", $ => {
        $(assert.equal(East.print(East.value(3.14)), "3.14"));
        $(assert.equal(East.print(East.value(42.0)), "42.0"));
        $(assert.equal(East.print(East.value(-0.0)), "-0.0"));
        $(assert.equal(East.print(East.value(NaN)), "NaN"));
        $(assert.equal(East.print(East.value(Infinity)), "Infinity"));
        $(assert.equal(East.print(East.value(-Infinity)), "-Infinity"));
    });

    test("print() with string", $ => {
        $(assert.equal(East.print(East.value("hello")), "\"hello\""));
        $(assert.equal(East.print(East.value("")), "\"\""));
        $(assert.equal(East.print(East.value("hello world")), "\"hello world\""));
    });

    test("print() with datetime", $ => {
        const date = new Date("2025-01-01T12:34:56.789Z");
        $(assert.equal(East.print(East.value(date)), "2025-01-01T12:34:56.789"));
    });

    test("print() with blob", $ => {
        $(assert.equal(East.print(East.value(new Uint8Array([]))), "0x"));
        $(assert.equal(East.print(East.value(new Uint8Array([0, 1, 2, 255]))), "0x000102ff"));
        $(assert.equal(East.print(East.value(new Uint8Array([10, 20, 30]))), "0x0a141e"));
    });

    test("print() with ref", $ => {
        $(assert.equal(East.print(East.value(ref(42n))), "&42"));
    });

    test("print() with array", $ => {
        $(assert.equal(East.print(East.value([])), "[]"));
        $(assert.equal(East.print(East.value([1n, 2n, 3n])), "[1, 2, 3]"));
        $(assert.equal(East.print(East.value([1n])), "[1]"));
    });

    test("print() with set", $ => {
        $(assert.equal(East.print(East.value(new Set())), "{}"));
        $(assert.equal(East.print(East.value(new Set([1n, 2n, 3n]))), "{1,2,3}"));
        $(assert.equal(East.print(East.value(new Set([42n]))), "{42}"));
    });

    test("print() with dict", $ => {
        $(assert.equal(East.print(East.value(new Map())), "{:}"));
        $(assert.equal(East.print(East.value(new Map([["a", 1n], ["b", 2n]]))), "{\"a\":1,\"b\":2}"));
        $(assert.equal(East.print(East.value(new Map([[1n, "x"]]))), "{1:\"x\"}"));
    });

    test("print() with struct", $ => {
        $(assert.equal(East.print(East.value({ x: 1n, y: 2n })), "(x=1, y=2)"));
        $(assert.equal(East.print(East.value({ a: "hello", b: 42n })), "(a=\"hello\", b=42)"));
    });

    test("print() with variant", $ => {
        $(assert.equal(East.print(East.value(none, OptionType(IntegerType))), ".none"));
        $(assert.equal(East.print(East.value(some(42n), OptionType(IntegerType))), ".some 42"));
        $(assert.equal(East.print(East.value(variant("success", "ok"), VariantType({ success: StringType, failure: StringType }))), ".success \"ok\""));
    });

    test("Array aliases in struct", $ => {
        // Create a shared reference
        const sharedRef = $.let(ref(42n));
        const struct = $.let({ a: sharedRef, b: sharedRef });

        // Should print with alias reference
        const printed = $.let(East.print(struct));
        $(assert.equal(printed, "(a=&42, b=1#.a)"));

        // Parser should handle N#.path references
        const parsed = $.let(printed.parse(StructType({ a: RefType(IntegerType), b: RefType(IntegerType) })));
        $(assert.equal(parsed, struct));
    });

    test("Array aliases in struct", $ => {
        // Create a shared array
        const sharedArray = $.let([1n, 2n, 3n]);
        const struct = $.let({ a: sharedArray, b: sharedArray });

        // Should print with alias reference
        const printed = $.let(East.print(struct));
        $(assert.equal(printed, "(a=[1, 2, 3], b=1#.a)"));

        // Parser should handle N#.path references
        const parsed = $.let(printed.parse(StructType({ a: ArrayType(IntegerType), b: ArrayType(IntegerType) })));
        $(assert.equal(parsed, struct));
    });

    test("Set aliases in struct", $ => {
        // Create a shared set (using East.value to create a set from array)
        const sharedSet = $.let(East.value([1n, 2n, 3n]).toSet());
        const struct = $.let({ a: sharedSet, b: sharedSet });

        // Should print with alias reference
        const printed = $.let(East.print(struct));
        $(assert.equal(printed, "(a={1,2,3}, b=1#.a)"));

        // Parser should handle N#.path references
        const parsed = $.let(printed.parse(StructType({ a: SetType(IntegerType), b: SetType(IntegerType) })));
        $(assert.equal(parsed, struct));
    });

    test("Dict aliases in struct", $ => {
        // Create a shared dict
        const sharedDict = $.let(East.value(new Map([[1n, "x"], [2n, "y"]]), DictType(IntegerType, StringType)));
        const struct = $.let({ a: sharedDict, b: sharedDict });

        // Should print with alias reference
        const printed = $.let(East.print(struct));
        $(assert.equal(printed, "(a={1:\"x\",2:\"y\"}, b=1#.a)"));

        // Parser should handle N#.path references
        const parsed = $.let(printed.parse(StructType({ a: DictType(IntegerType, StringType), b: DictType(IntegerType, StringType) })));
        $(assert.equal(parsed, struct));
    });

    test("Nested array aliases", $ => {
        // Create arrays where inner array is shared
        const inner = $.let([1n, 2n]);
        const outer = $.let([inner, inner, inner]);

        // Should print with alias references
        const printed = $.let(East.print(outer));
        $(assert.equal(printed, "[[1, 2], 1#[0], 1#[0]]"));

        // Parser should handle N#[index] references
        const parsed = $.let(printed.parse(ArrayType(ArrayType(IntegerType))));
        $(assert.equal(parsed, outer));
    });


    test("Recursive type - tree without cycles", $ => {
        // Create a simple binary tree: node(1, leaf, leaf)
        const tree = $.let(East.value(variant("node", {
            value: 1n,
            left: variant("leaf"),
            right: variant("leaf")
        }), TreeType));

        // Should print without circular references
        const printed = $.let(East.print(tree));
        $(assert.equal(printed, ".node (value=1, left=.leaf, right=.leaf)"));

        // Parser should handle RecursiveType
        const parsed = $.let(printed.parse(TreeType));
        $(assert.equal(parsed, tree));
    });

    test("Recursive type - larger tree without cycles", $ => {
        // Create a tree: node(2, node(1, leaf, leaf), node(3, leaf, leaf))
        const left = $.let(variant("node", {
            value: 1n,
            left: variant("leaf"),
            right: variant("leaf")
        }), TreeType);
        const right = $.let(variant("node", {
            value: 3n,
            left: variant("leaf"),
            right: variant("leaf")
        }), TreeType);
        const tree = $.let(East.value(variant("node", {
            value: 2n,
            left,
            right
        }), TreeType));

        const printed = $.let(East.print(tree));
        $(assert.equal(printed, ".node (value=2, left=.node (value=1, left=.leaf, right=.leaf), right=.node (value=3, left=.leaf, right=.leaf))"));

        // Parser should handle RecursiveType
        const parsed = $.let(printed.parse(TreeType));
        $(assert.equal(parsed, tree));
    });


    test("Recursive type - linked list without cycles", $ => {
        // Create a simple linked list: cons(1, cons(2, cons(3, nil)))
        const list = $.let(East.value(variant("cons", {
            head: 1n,
            tail: variant("cons", {
                head: 2n,
                tail: variant("cons", {
                    head: 3n,
                    tail: variant("nil")
                })
            })
        }), LinkedListType));

        const printed = $.let(East.print(list));
        $(assert.equal(printed, ".cons (head=1, tail=.cons (head=2, tail=.cons (head=3, tail=.nil)))"));

        // Parser should handle RecursiveType
        const parsed = $.let(printed.parse(LinkedListType));
        $(assert.equal(parsed, list));
    });

    test("Recursive type - EastTypeType", $ => {
        const neverType = $.let(toEastTypeValue(NeverType), EastTypeType);
        const nullType = $.let(toEastTypeValue(NullType), EastTypeType);
        const booleanType = $.let(toEastTypeValue(BooleanType), EastTypeType);
        const integerType = $.let(toEastTypeValue(IntegerType), EastTypeType);
        const dateTimeType = $.let(toEastTypeValue(DateTimeType), EastTypeType);
        const stringType = $.let(toEastTypeValue(StringType), EastTypeType);
        const blobType = $.let(toEastTypeValue(BlobType), EastTypeType);
        const refType = $.let(toEastTypeValue(RefType(IntegerType)), EastTypeType);
        const arrayType = $.let(toEastTypeValue(ArrayType(IntegerType)), EastTypeType);
        const setType = $.let(toEastTypeValue(SetType(IntegerType)), EastTypeType);
        const dictType = $.let(toEastTypeValue(DictType(StringType, IntegerType)), EastTypeType);
        const structType = $.let(toEastTypeValue(StructType({ a: IntegerType, b: StringType })), EastTypeType);
        const variantType = $.let(toEastTypeValue(VariantType({ some: IntegerType, none: NullType })), EastTypeType);
        const eastTypeType = $.let(toEastTypeValue(EastTypeType), EastTypeType);

        $(assert.equal(East.print(neverType), printType(NeverType)));
        $(assert.equal(East.print(nullType), printType(NullType)));
        $(assert.equal(East.print(booleanType), printType(BooleanType)));
        $(assert.equal(East.print(integerType), printType(IntegerType)));
        $(assert.equal(East.print(dateTimeType), printType(DateTimeType)));
        $(assert.equal(East.print(stringType), printType(StringType)));
        $(assert.equal(East.print(blobType), printType(BlobType)));
        $(assert.equal(East.print(refType), printType(RefType(IntegerType))));
        $(assert.equal(East.print(arrayType), printType(ArrayType(IntegerType))));
        $(assert.equal(East.print(setType), printType(SetType(IntegerType))));
        $(assert.equal(East.print(dictType), printType(DictType(StringType, IntegerType))));
        $(assert.equal(East.print(structType), printType(StructType({ a: IntegerType, b: StringType }))));
        $(assert.equal(East.print(variantType), printType(VariantType({ some: IntegerType, none: NullType }))));
        $(assert.equal(East.print(eastTypeType), printType(EastTypeType)));
    })
});