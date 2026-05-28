/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { variant } from './containers/variant.js';
import { compareFor, equalFor, greaterEqualFor, greaterFor, isFor, lessEqualFor, lessFor, notEqualFor } from './comparison.js';
import { ArrayType, AsyncFunctionType, BlobType, BooleanType, DateTimeType, DictType, type EastType, FloatType, FunctionType, IntegerType, NeverType, NullType, RecursiveType, SetType, StringType, StructType, type ValueTypeOf, VariantType } from './types.js';

describe('Comparison of EAST values', () => {
    function run<T extends EastType>(type: T, values: ValueTypeOf<T>[]) {
        const equal = equalFor(type);
        const less = lessFor(type);
        const compare = compareFor(type);

        for (let i = 0; i < values.length; i++) {
            const x = values[i]!;
            for (let j = 0; j < values.length; j++) {
                const y = values[j]!;
                assert.equal(equal(x, y), i == j);
                assert.equal(less(x, y), i < j);
                assert.equal(compare(x, y), i < j ? -1 : i == j ? 0 : 1);
            }
        }
    }

    test('should compare nulls', () => {
        const type = NullType;
        const values = [
            null,
        ];

        run(type, values);
    });

    test('should compare booleans', () => {
        const type = BooleanType;
        const values = [
            false,
            true,
        ];

        run(type, values);
    });

    test('should compare integers', () => {
        const type = IntegerType;
        const values = [
            -9223372036854775808n,
            -1n,
            0n,
            42n,
            90071992547409919n,
            9223372036854775807n,
        ];

        run(type, values);
    });

    test('should compare floats', () => {
        const type = FloatType;
        const values = [
            -Infinity,
            -1e8,
            -3.14,
            -1,
            -1e-8,
            -1e-16,
            -0,
            0,
            1e-16,
            1e-8,
            1,
            3.14,
            1e8,
            Infinity,
            NaN,
        ];

        run(type, values);
    });

    test('should compare dates', () => {
        const type = DateTimeType;
        const values = [
            new Date(0),
            new Date("2022-06-29T13:43:00.123Z"),
        ];

        run(type, values);
    });

    test('should compare strings', () => {
        const type = StringType;
        const values = [
            "",
            "a",
            "ab",
            "abc",
            "abd",
            "def",
            "いろはにほへとちりぬるを",
        ];

        run(type, values);
    });

    test('should compare arrays', () => {
        const type = ArrayType(IntegerType);
        const values = [
            [],
            [0n],
            [0n, 1n],
            [0n, 2n, 3n],
            [0n, 2n, 4n],
            [1n],
        ];

        run(type, values);
    });

    test('should compare sets', () => {
        const type = SetType(StringType);
        const values = [
            new Set<string>(),
            new Set(["abc"]),
            new Set(["abc", "def"]),
            new Set(["def"]),
        ];

        run(type, values);
    });

    test('should compare dicts', () => {
        const type = DictType(StringType, IntegerType);
        const values = [
            new Map<string, bigint>(),
            new Map([["abc", 0n]]),
            new Map([["abc", 0n], ["def", 1n]]),
            new Map([["abc", 1n]]),
            new Map([["def", 1n]]),
        ];

        run(type, values);
    });

    test('should compare structs', () => {
        const type = StructType({
            boolean: BooleanType,
            string: StringType,
        });

        const values = [
            { boolean: false, string: "good" },
            { boolean: true, string: "bad" },
            { boolean: true, string: "ok" },
        ];

        run(type, values);
    });

    test('should compare variants', () => {
        const type = VariantType({
            none: NullType,
            some: IntegerType,
        });

        const values: (variant<"none", null> | variant<"some", bigint>)[] = [
            variant("none", null),
            variant("some", 0n),
            variant("some", 1n),
        ];

        run(type, values);
    });

    test('should compare blobs', () => {
        const type = BlobType;

        const values: Uint8Array[] = [
            new Uint8Array([]),
            new Uint8Array([0, 0]),
            new Uint8Array([1]),
            new Uint8Array([2]),
        ];

        run(type, values);
    });

    test('should handle Never type comparisons', () => {
        const type = NeverType;
        const isCompare = isFor(type);
        const equalCompare = equalFor(type);
        const lessCompare = lessFor(type);

        assert.throws(() => isCompare(null as never, null as never), /Attempted to compare values of type \.Never/);
        assert.throws(() => equalCompare(null as never, null as never), /Attempted to compare values of type \.Never/);
        assert.throws(() => lessCompare(null as never, null as never), /Attempted to compare values of type \.Never/);
    });

    test('should handle Function type comparisons', () => {
        const type = FunctionType([], NullType);

        assert.throws(() => isFor(type), /Attempted to compare values of type \.Function/);
        assert.doesNotThrow(() => equalFor(type));
        assert.doesNotThrow(() => notEqualFor(type));
        assert.doesNotThrow(() => lessFor(type));
        assert.doesNotThrow(() => lessEqualFor(type));
        assert.doesNotThrow(() => greaterFor(type));
        assert.doesNotThrow(() => greaterEqualFor(type));
    });

    test('should handle AsyncFunction type comparisons', () => {
        const type = AsyncFunctionType([], NullType);

        assert.throws(() => isFor(type), /Attempted to compare values of type \.AsyncFunction/);
        assert.doesNotThrow(() => equalFor(type));
        assert.doesNotThrow(() => notEqualFor(type));
        assert.doesNotThrow(() => lessFor(type));
        assert.doesNotThrow(() => lessEqualFor(type));
        assert.doesNotThrow(() => greaterFor(type));
        assert.doesNotThrow(() => greaterEqualFor(type));
    });

    test('should handle Float NaN edge cases', () => {
        const type = FloatType;
        const isCompare = isFor(type);
        const equalCompare = equalFor(type);
        const notEqualCompare = notEqualFor(type);
        const lessCompare = lessFor(type);

        // NaN == NaN for isFor
        assert.equal(isCompare(NaN, NaN), true);
        assert.equal(isCompare(NaN, 0), false);
        assert.equal(isCompare(0, NaN), false);

        // NaN == NaN for equalFor
        assert.equal(equalCompare(NaN, NaN), true);
        assert.equal(equalCompare(NaN, 0), false);

        // notEqual with NaN
        assert.equal(notEqualCompare(NaN, NaN), false);
        assert.equal(notEqualCompare(NaN, 0), true);
        assert.equal(notEqualCompare(0, NaN), true);

        // NaN ordering (NaN is greatest)
        assert.equal(lessCompare(0, NaN), true);
        assert.equal(lessCompare(NaN, 0), false);
        assert.equal(lessCompare(NaN, NaN), false);

        // -0 vs +0 edge case (Object.is distinguishes them)
        assert.equal(lessCompare(-0, 0), true);
        assert.equal(lessCompare(0, -0), false);
        assert.equal(equalCompare(-0, 0), false); // Object.is checks -0 vs 0 (they are different)
    });

    test('should handle Blob different lengths', () => {
        const type = BlobType;
        const equalCompare = equalFor(type);
        const notEqualCompare = notEqualFor(type);
        const lessCompare = lessFor(type);

        const blob1 = new Uint8Array([1, 2, 3]);
        const blob2 = new Uint8Array([1, 2]);
        const blob3 = new Uint8Array([1, 2, 4]);

        // Different lengths
        assert.equal(equalCompare(blob1, blob2), false);
        assert.equal(notEqualCompare(blob1, blob2), true);
        assert.equal(lessCompare(blob2, blob1), true); // shorter is less
        assert.equal(lessCompare(blob1, blob2), false);

        // Same length, different values
        assert.equal(equalCompare(blob1, blob3), false);
        assert.equal(lessCompare(blob1, blob3), true);
        assert.equal(lessCompare(blob3, blob1), false);
    });

    test('should handle Array comparisons', () => {
        const type = ArrayType(IntegerType);
        const equalCompare = equalFor(type);
        const notEqualCompare = notEqualFor(type);
        const isCompare = isFor(type);

        const arr1 = [1n, 2n, 3n];
        const arr2 = [1n, 2n, 3n]; // different array, same values
        const arr3 = arr1; // same reference

        // isFor compares by identity for mutable types
        assert.equal(isCompare(arr1, arr2), false); // different objects
        assert.equal(isCompare(arr1, arr3), true); // same object

        // equalFor compares by deep value equality for arrays
        assert.equal(equalCompare(arr1, arr2), true); // same values
        assert.equal(equalCompare(arr1, arr3), true); // same object
        assert.equal(notEqualCompare(arr1, arr2), false); // same values
    });

    test('should handle Set value comparisons', () => {
        const type = SetType(StringType);
        const equalCompare = equalFor(type);
        const notEqualCompare = notEqualFor(type);

        const set1 = new Set(['a', 'b', 'c']);
        const set2 = new Set(['a', 'b', 'c']);
        const set3 = new Set(['a', 'b', 'd']);
        const set4 = new Set(['a', 'b']);

        // Same values
        assert.equal(equalCompare(set1, set2), true);
        assert.equal(notEqualCompare(set1, set2), false);

        // Different values
        assert.equal(equalCompare(set1, set3), false);
        assert.equal(notEqualCompare(set1, set3), true);

        // Different sizes
        assert.equal(equalCompare(set1, set4), false);
        assert.equal(notEqualCompare(set1, set4), true);
    });

    test('should handle Dict value comparisons', () => {
        const type = DictType(StringType, IntegerType);
        const equalCompare = equalFor(type);
        const notEqualCompare = notEqualFor(type);

        const dict1 = new Map([['a', 1n], ['b', 2n]]);
        const dict2 = new Map([['a', 1n], ['b', 2n]]);
        const dict3 = new Map([['a', 1n], ['b', 3n]]);
        const dict4 = new Map([['a', 1n]]);
        const dict5 = new Map([['a', 1n], ['c', 2n]]);

        // Same values
        assert.equal(equalCompare(dict1, dict2), true);
        assert.equal(notEqualCompare(dict1, dict2), false);

        // Different values (same keys)
        assert.equal(equalCompare(dict1, dict3), false);
        assert.equal(notEqualCompare(dict1, dict3), true);

        // Different size
        assert.equal(equalCompare(dict1, dict4), false);

        // Missing key
        assert.equal(equalCompare(dict1, dict5), false);
        assert.equal(notEqualCompare(dict1, dict5), true);
    });

    test('should handle Struct field mismatches', () => {
        const type = StructType({
            a: IntegerType,
            b: StringType,
        });
        const equalCompare = equalFor(type);
        const notEqualCompare = notEqualFor(type);
        const lessCompare = lessFor(type);

        const struct1 = { a: 1n, b: 'hello' };
        const struct2 = { a: 1n, b: 'hello' };
        const struct3 = { a: 2n, b: 'hello' };
        const struct4 = { a: 1n, b: 'world' };

        // Same values
        assert.equal(equalCompare(struct1, struct2), true);
        assert.equal(notEqualCompare(struct1, struct2), false);

        // First field differs
        assert.equal(equalCompare(struct1, struct3), false);
        assert.equal(notEqualCompare(struct1, struct3), true);
        assert.equal(lessCompare(struct1, struct3), true);
        assert.equal(lessCompare(struct3, struct1), false);

        // Second field differs
        assert.equal(equalCompare(struct1, struct4), false);
        assert.equal(lessCompare(struct1, struct4), true);
    });

    test('should handle Variant type mismatches', () => {
        const type = VariantType({
            none: NullType,
            some: IntegerType,
        });
        const equalCompare = equalFor(type);
        const notEqualCompare = notEqualFor(type);
        const lessCompare = lessFor(type);
        const compareCompare = compareFor(type);

        const v1 = variant('none', null);
        const v2 = variant('none', null);
        const v3 = variant('some', 5n);
        const v4 = variant('some', 10n);

        // Same type and value
        assert.equal(equalCompare(v1, v2), true);
        assert.equal(notEqualCompare(v1, v2), false);

        // Different type
        assert.equal(equalCompare(v1, v3), false);
        assert.equal(notEqualCompare(v1, v3), true);
        assert.equal(lessCompare(v1, v3), true); // 'none' < 'some'
        assert.equal(lessCompare(v3, v1), false);
        assert.equal(compareCompare(v1, v3), -1);
        assert.equal(compareCompare(v3, v1), 1);

        // Same type, different value
        assert.equal(equalCompare(v3, v4), false);
        assert.equal(lessCompare(v3, v4), true);
    });

    test('should handle Array length comparisons', () => {
        const type = ArrayType(IntegerType);
        const lessCompare = lessFor(type);
        const lessEqualCompare = lessEqualFor(type);
        const greaterCompare = greaterFor(type);
        const greaterEqualCompare = greaterEqualFor(type);

        const arr1 = [1n, 2n];
        const arr2 = [1n, 2n, 3n];

        // Prefix comparison
        assert.equal(lessCompare(arr1, arr2), true);
        assert.equal(lessEqualCompare(arr1, arr2), true);
        assert.equal(greaterCompare(arr2, arr1), true);
        assert.equal(greaterEqualCompare(arr2, arr1), true);
    });

    test('should handle Set prefix comparisons', () => {
        const type = SetType(IntegerType);
        const lessCompare = lessFor(type);
        const lessEqualCompare = lessEqualFor(type);
        const greaterCompare = greaterFor(type);
        const greaterEqualCompare = greaterEqualFor(type);
        const compareCompare = compareFor(type);

        // SortedSet maintains order
        const set1 = new Set([1n, 2n]);
        const set2 = new Set([1n, 2n, 3n]);
        const set3 = new Set([1n, 2n]);

        // Prefix: set1 < set2
        assert.equal(lessCompare(set1, set2), true);
        assert.equal(lessEqualCompare(set1, set2), true);
        assert.equal(greaterCompare(set2, set1), true);
        assert.equal(greaterEqualCompare(set2, set1), true);
        assert.equal(compareCompare(set1, set2), -1);
        assert.equal(compareCompare(set2, set1), 1);

        // Equal
        assert.equal(lessEqualCompare(set1, set3), true);
        assert.equal(greaterEqualCompare(set1, set3), true);
        assert.equal(compareCompare(set1, set3), 0);
    });

    test('should handle Dict prefix comparisons', () => {
        const type = DictType(StringType, IntegerType);
        const lessCompare = lessFor(type);
        const lessEqualCompare = lessEqualFor(type);
        const greaterCompare = greaterFor(type);
        const greaterEqualCompare = greaterEqualFor(type);
        const compareCompare = compareFor(type);

        const dict1 = new Map([['a', 1n]]);
        const dict2 = new Map([['a', 1n], ['b', 2n]]);
        const dict3 = new Map([['a', 1n]]);

        // Prefix: dict1 < dict2
        assert.equal(lessCompare(dict1, dict2), true);
        assert.equal(lessEqualCompare(dict1, dict2), true);
        assert.equal(greaterCompare(dict2, dict1), true);
        assert.equal(greaterEqualCompare(dict2, dict1), true);
        assert.equal(compareCompare(dict1, dict2), -1);
        assert.equal(compareCompare(dict2, dict1), 1);

        // Equal
        assert.equal(lessEqualCompare(dict1, dict3), true);
        assert.equal(greaterEqualCompare(dict1, dict3), true);
        assert.equal(compareCompare(dict1, dict3), 0);
    });

    test('should handle Struct field-by-field comparison', () => {
        const type = StructType({
            a: IntegerType,
            b: IntegerType,
        });
        const lessEqualCompare = lessEqualFor(type);
        const greaterEqualCompare = greaterEqualFor(type);

        const struct1 = { a: 1n, b: 2n };
        const struct2 = { a: 1n, b: 3n };
        const struct3 = { a: 1n, b: 2n };

        // struct1 <= struct2
        assert.equal(lessEqualCompare(struct1, struct2), true);
        assert.equal(greaterEqualCompare(struct2, struct1), true);

        // struct1 == struct3
        assert.equal(lessEqualCompare(struct1, struct3), true);
        assert.equal(greaterEqualCompare(struct1, struct3), true);
    });

    test('should handle Variant lessEqual and greaterEqual', () => {
        const type = VariantType({
            a: IntegerType,
            b: IntegerType,
        });
        const lessEqualCompare = lessEqualFor(type);
        const greaterEqualCompare = greaterEqualFor(type);

        const v1 = variant('a', 5n);
        const v2 = variant('b', 3n);
        const v3 = variant('b', 5n);
        const v4 = variant('b', 3n);

        // v1 < v2 (by type)
        assert.equal(lessEqualCompare(v1, v2), true);
        assert.equal(greaterEqualCompare(v2, v1), true);

        // v2 < v3 (same type, by value)
        assert.equal(lessEqualCompare(v2, v3), true);
        assert.equal(greaterEqualCompare(v3, v2), true);

        // v2 == v4
        assert.equal(lessEqualCompare(v2, v4), true);
        assert.equal(greaterEqualCompare(v2, v4), true);
    });

    test('should handle Null type comparisons', () => {
        const type = NullType;
        const isCompare = isFor(type);
        const equalCompare = equalFor(type);
        const lessCompare = lessFor(type);
        const lessEqualCompare = lessEqualFor(type);
        const greaterCompare = greaterFor(type);
        const greaterEqualCompare = greaterEqualFor(type);

        // All null values are equal
        assert.equal(isCompare(null, null), true);
        assert.equal(equalCompare(null, null), true);
        assert.equal(lessCompare(null, null), false);
        assert.equal(lessEqualCompare(null, null), true);
        assert.equal(greaterCompare(null, null), false);
        assert.equal(greaterEqualCompare(null, null), true);
    });

    test('should handle Blob lexical comparison loops', () => {
        const type = BlobType;
        const lessCompare = lessFor(type);
        const lessEqualCompare = lessEqualFor(type);
        const greaterCompare = greaterFor(type);
        const greaterEqualCompare = greaterEqualFor(type);
        const notEqualCompare = notEqualFor(type);

        // Different bytes in middle - tests loop bodies
        const blob1 = new Uint8Array([1, 2, 3, 4]);
        const blob2 = new Uint8Array([1, 2, 5, 4]); // different at index 2

        assert.equal(lessCompare(blob1, blob2), true);
        assert.equal(lessEqualCompare(blob1, blob2), true);
        assert.equal(greaterCompare(blob2, blob1), true);
        assert.equal(greaterEqualCompare(blob2, blob1), true);
        assert.equal(notEqualCompare(blob1, blob2), true);

        // Equal blobs
        const blob3 = new Uint8Array([1, 2, 3, 4]);
        assert.equal(lessCompare(blob1, blob3), false);
        assert.equal(lessEqualCompare(blob1, blob3), true);
        assert.equal(greaterCompare(blob1, blob3), false);
        assert.equal(greaterEqualCompare(blob1, blob3), true);
        assert.equal(notEqualCompare(blob1, blob3), false);
    });

    test('should handle Set and Dict identity with isFor', () => {
        // isFor uses Object.is for Set and Dict
        const setType = SetType(IntegerType);
        const dictType = DictType(StringType, IntegerType);

        const set1 = new Set([1n, 2n]);
        const set2 = new Set([1n, 2n]);
        const set3 = set1;

        const dict1 = new Map([['a', 1n]]);
        const dict2 = new Map([['a', 1n]]);
        const dict3 = dict1;

        const setIsCompare = isFor(setType);
        const dictIsCompare = isFor(dictType);

        // Different objects with same values
        assert.equal(setIsCompare(set1, set2), false);
        assert.equal(dictIsCompare(dict1, dict2), false);

        // Same reference
        assert.equal(setIsCompare(set1, set3), true);
        assert.equal(dictIsCompare(dict1, dict3), true);
    });

    test('should handle Struct field mismatch in isFor', () => {
        const type = StructType({ x: IntegerType, y: IntegerType });
        const isCompare = isFor(type);

        const struct1 = { x: 1n, y: 2n };
        const struct2 = { x: 1n, y: 3n }; // different y

        // isFor checks all fields, returns false on first mismatch
        assert.equal(isCompare(struct1, struct2), false);
    });

    test('should handle Never type in notEqualFor', () => {
        const type = NeverType;
        const notEqualCompare = notEqualFor(type);

        assert.throws(() => notEqualCompare(null as never, null as never), /Attempted to compare values of type \.Never/);
    });

    test('should handle Never type in lessEqualFor', () => {
        const type = NeverType;
        const lessEqualCompare = lessEqualFor(type);

        assert.throws(() => lessEqualCompare(null as never, null as never), /Attempted to compare values of type \.Never/);
    });

    test('should handle Never type in greaterEqualFor', () => {
        const type = NeverType;
        const greaterEqualCompare = greaterEqualFor(type);

        assert.throws(() => greaterEqualCompare(null as never, null as never), /Attempted to compare values of type \.Never/);
    });

    test('should handle Never type in greaterFor', () => {
        const type = NeverType;
        const greaterCompare = greaterFor(type);

        assert.throws(() => greaterCompare(null as never, null as never), /Attempted to compare values of type \.Never/);
    });

    test('should handle Set prefix where x.size > y.size', () => {
        const type = SetType(IntegerType);
        const greaterCompare = greaterFor(type);

        // x is longer and y is prefix
        const set1 = new Set([1n, 2n, 3n, 4n]);
        const set2 = new Set([1n, 2n, 3n]);

        assert.equal(greaterCompare(set1, set2), true);
    });

    test('should handle Dict prefix where x.size > y.size', () => {
        const type = DictType(StringType, IntegerType);
        const greaterCompare = greaterFor(type);

        // x is longer and y is prefix
        const dict1 = new Map([['a', 1n], ['b', 2n], ['c', 3n]]);
        const dict2 = new Map([['a', 1n], ['b', 2n]]);

        assert.equal(greaterCompare(dict1, dict2), true);
    });

    test('should handle Struct greaterFor with all fields equal', () => {
        const type = StructType({ x: IntegerType, y: IntegerType });
        const greaterCompare = greaterFor(type);

        const struct1 = { x: 1n, y: 2n };
        const struct2 = { x: 1n, y: 2n };

        // All fields equal means not greater
        assert.equal(greaterCompare(struct1, struct2), false);
    });

    test('should handle Blob isFor loop body for value comparison', () => {
        const type = BlobType;
        const isCompare = isFor(type);

        // Test the loop body that compares byte-by-byte
        const blob1 = new Uint8Array([1, 2, 3, 4, 5]);
        const blob2 = new Uint8Array([1, 2, 3, 4, 5]); // same values
        const blob3 = new Uint8Array([1, 2, 3, 9, 5]); // different at index 3

        assert.equal(isCompare(blob1, blob2), true);
        assert.equal(isCompare(blob1, blob3), false);
    });

    test('should handle Set greaterFor when all elements match', () => {
        const type = SetType(IntegerType);
        const greaterCompare = greaterFor(type);

        // Same size and all elements equal
        const set1 = new Set([1n, 2n, 3n]);
        const set2 = new Set([1n, 2n, 3n]);

        // Should return x.size > y.size which is false
        assert.equal(greaterCompare(set1, set2), false);
    });

    test('should handle Dict greaterFor when all entries match', () => {
        const type = DictType(StringType, IntegerType);
        const greaterCompare = greaterFor(type);

        // Same size and all entries equal
        const dict1 = new Map([['a', 1n], ['b', 2n]]);
        const dict2 = new Map([['a', 1n], ['b', 2n]]);

        // Should return x.size > y.size which is false
        assert.equal(greaterCompare(dict1, dict2), false);
    });

    test('should compare tree-shaped recursive data (binary tree)', () => {
        // Binary tree type: { value: Integer, left: Tree | null, right: Tree | null }
        const TreeType = RecursiveType(self =>
            VariantType({
                leaf: NullType,
                node: StructType({
                    value: IntegerType,
                    left: self,
                    right: self,
                }),
            })
        );

        const equalCompare = equalFor(TreeType);
        const notEqualCompare = notEqualFor(TreeType);
        const compare = compareFor(TreeType);

        // Leaf nodes
        const leaf = variant('leaf', null);
        assert.equal(equalCompare(leaf, leaf), true);
        assert.equal(notEqualCompare(leaf, leaf), false);
        assert.equal(compare(leaf, leaf), 0);

        // Simple nodes
        const node1 = variant('node', { value: 1n, left: leaf, right: leaf });
        const node2 = variant('node', { value: 1n, left: leaf, right: leaf });
        const node3 = variant('node', { value: 2n, left: leaf, right: leaf });

        assert.equal(equalCompare(node1, node2), true);
        assert.equal(equalCompare(node1, node3), false);
        assert.equal(notEqualCompare(node1, node3), true);
        assert.equal(compare(node1, node2), 0);
        assert.equal(compare(node1, node3), -1);
        assert.equal(compare(node3, node1), 1);

        // Nested tree structures
        const leftTree = variant('node', { value: 10n, left: leaf, right: leaf });
        const rightTree = variant('node', { value: 20n, left: leaf, right: leaf });
        const tree1 = variant('node', { value: 5n, left: leftTree, right: rightTree });
        const tree2 = variant('node', { value: 5n, left: leftTree, right: rightTree });
        const tree3 = variant('node', { value: 5n, left: rightTree, right: leftTree }); // swapped

        assert.equal(equalCompare(tree1, tree2), true);
        assert.equal(equalCompare(tree1, tree3), false);
        assert.equal(notEqualCompare(tree1, tree3), true);
        assert.equal(compare(tree1, tree2), 0);
        assert.equal(compare(tree1, tree3), -1); // leftTree < rightTree
        assert.equal(compare(tree3, tree1), 1);

        // Test lessFor, greaterFor, lessEqualFor, greaterEqualFor
        const less = lessFor(TreeType);
        const greater = greaterFor(TreeType);
        const lessEqual = lessEqualFor(TreeType);
        const greaterEqual = greaterEqualFor(TreeType);

        // Leaf nodes
        assert.equal(less(leaf, leaf), false);
        assert.equal(greater(leaf, leaf), false);
        assert.equal(lessEqual(leaf, leaf), true);
        assert.equal(greaterEqual(leaf, leaf), true);

        // Simple nodes
        assert.equal(less(node1, node2), false); // equal
        assert.equal(less(node1, node3), true);
        assert.equal(less(node3, node1), false);
        assert.equal(greater(node3, node1), true);
        assert.equal(greater(node1, node3), false);
        assert.equal(lessEqual(node1, node2), true);
        assert.equal(lessEqual(node1, node3), true);
        assert.equal(greaterEqual(node3, node1), true);

        // Nested structures
        assert.equal(less(tree1, tree3), true);
        assert.equal(less(tree3, tree1), false);
        assert.equal(greater(tree3, tree1), true);
        assert.equal(lessEqual(tree1, tree2), true); // equal
        assert.equal(greaterEqual(tree1, tree2), true); // equal

        // Test isFor (RecursiveType is immutable, so isFor uses structural equality)
        const is = isFor(TreeType);

        // Same object
        assert.equal(is(leaf, leaf), true);
        assert.equal(is(tree1, tree1), true);

        // Different objects, structurally equal (immutable type, so should be true)
        assert.equal(is(node1, node2), true);
        assert.equal(is(tree1, tree2), true);

        // Different values
        assert.equal(is(node1, node3), false);
        assert.equal(is(tree1, tree3), false);
        assert.equal(is(leaf, node1), false);
    });

    test('should compare tree-shaped recursive data (linked list)', () => {
        // Linked list type: { value: Integer, next: List | null }
        const ListType = RecursiveType(self =>
            VariantType({
                nil: NullType,
                cons: StructType({
                    value: IntegerType,
                    next: self,
                }),
            })
        );

        const equalCompare = equalFor(ListType);
        const compare = compareFor(ListType);

        // Empty lists
        const nil = variant('nil', null);
        assert.equal(equalCompare(nil, nil), true);
        assert.equal(compare(nil, nil), 0);

        // Single-element lists
        const list1 = variant('cons', { value: 1n, next: nil });
        const list2 = variant('cons', { value: 1n, next: nil });
        const list3 = variant('cons', { value: 2n, next: nil });

        assert.equal(equalCompare(list1, list2), true);
        assert.equal(equalCompare(list1, list3), false);
        assert.equal(compare(list1, list2), 0);
        assert.equal(compare(list1, list3), -1);
        assert.equal(compare(list3, list1), 1);

        // Multi-element lists
        const list4 = variant('cons', { value: 1n, next: variant('cons', { value: 2n, next: variant('cons', { value: 3n, next: nil }) }) });
        const list5 = variant('cons', { value: 1n, next: variant('cons', { value: 2n, next: variant('cons', { value: 3n, next: nil }) }) });
        const list6 = variant('cons', { value: 1n, next: variant('cons', { value: 2n, next: variant('cons', { value: 4n, next: nil }) }) });

        assert.equal(equalCompare(list4, list5), true);
        assert.equal(equalCompare(list4, list6), false);
        assert.equal(compare(list4, list5), 0);
        assert.equal(compare(list4, list6), -1); // 3 < 4
        assert.equal(compare(list6, list4), 1);

        // Test lessFor, greaterFor, lessEqualFor, greaterEqualFor
        const less = lessFor(ListType);
        const greater = greaterFor(ListType);
        const lessEqual = lessEqualFor(ListType);
        const greaterEqual = greaterEqualFor(ListType);

        // Empty lists
        assert.equal(less(nil, nil), false);
        assert.equal(greater(nil, nil), false);
        assert.equal(lessEqual(nil, nil), true);
        assert.equal(greaterEqual(nil, nil), true);

        // Single-element lists
        assert.equal(less(list1, list2), false); // equal
        assert.equal(less(list1, list3), true);
        assert.equal(less(list3, list1), false);
        assert.equal(greater(list3, list1), true);
        assert.equal(lessEqual(list1, list2), true);
        assert.equal(greaterEqual(list3, list1), true);

        // Multi-element lists
        assert.equal(less(list4, list5), false); // equal
        assert.equal(less(list4, list6), true);
        assert.equal(greater(list6, list4), true);
        assert.equal(lessEqual(list4, list5), true);
        assert.equal(greaterEqual(list4, list5), true);

        // Test isFor (RecursiveType is immutable, so isFor uses structural equality)
        const is = isFor(ListType);

        // Same object
        assert.equal(is(nil, nil), true);
        assert.equal(is(list1, list1), true);

        // Different objects, structurally equal
        assert.equal(is(list1, list2), true);
        assert.equal(is(list4, list5), true);

        // Different values
        assert.equal(is(list1, list3), false);
        assert.equal(is(list4, list6), false);
        assert.equal(is(nil, list1), false);
    });

    test('should compare DAG-shaped recursive data (shared subtrees)', () => {
        // Binary tree with shared subtrees (DAG, not a tree)
        const TreeType = RecursiveType(self =>
            VariantType({
                leaf: NullType,
                node: StructType({
                    value: IntegerType,
                    left: self,
                    right: self,
                }),
            })
        );

        const equalCompare = equalFor(TreeType);
        const compare = compareFor(TreeType);

        const leaf = variant('leaf', null);
        const sharedSubtree = variant('node', { value: 10n, left: leaf, right: leaf });

        // Two trees sharing the same subtree object
        const dag1 = variant('node', { value: 5n, left: sharedSubtree, right: sharedSubtree });
        const dag2 = variant('node', { value: 5n, left: sharedSubtree, right: sharedSubtree });

        // Fast path: same object reference
        assert.equal(equalCompare(dag1, dag1), true);
        assert.equal(compare(dag1, dag1), 0);

        // Different objects but structurally equal (including shared structure)
        assert.equal(equalCompare(dag1, dag2), true);
        assert.equal(compare(dag1, dag2), 0);

        // Different tree with same values but different structure
        const differentSubtree = variant('node', { value: 10n, left: leaf, right: leaf });
        const dag3 = variant('node', { value: 5n, left: differentSubtree, right: differentSubtree });
        assert.equal(equalCompare(dag1, dag3), true); // Structurally equal
        assert.equal(compare(dag1, dag3), 0);

        // Different values
        const dag4 = variant('node', { value: 5n, left: sharedSubtree, right: leaf });
        assert.equal(equalCompare(dag1, dag4), false);
        assert.equal(compare(dag1, dag4), 1); // dag1 has node on right, dag4 has leaf
        assert.equal(compare(dag4, dag1), -1);

        // Test lessFor, greaterFor, lessEqualFor, greaterEqualFor
        const less = lessFor(TreeType);
        const greater = greaterFor(TreeType);
        const lessEqual = lessEqualFor(TreeType);
        const greaterEqual = greaterEqualFor(TreeType);

        assert.equal(less(dag1, dag1), false); // same object
        assert.equal(lessEqual(dag1, dag1), true);
        assert.equal(greaterEqual(dag1, dag1), true);
        assert.equal(less(dag1, dag2), false); // equal
        assert.equal(lessEqual(dag1, dag2), true);
        assert.equal(less(dag4, dag1), true); // leaf < node
        assert.equal(greater(dag1, dag4), true);
        assert.equal(greaterEqual(dag1, dag4), true);

        // Test isFor (RecursiveType is immutable, so isFor uses structural equality)
        const is = isFor(TreeType);

        // Same object
        assert.equal(is(dag1, dag1), true);
        assert.equal(is(sharedSubtree, sharedSubtree), true);

        // Different objects, structurally equal (even with shared subtrees)
        assert.equal(is(dag1, dag2), true);
        assert.equal(is(dag1, dag3), true); // Different subtree objects but same structure

        // Different values
        assert.equal(is(dag1, dag4), false);
        assert.equal(is(leaf, dag1), false);
    });

    test('should compare circular recursive data (self-loop)', () => {
        // Linked list with cycles
        const ListType = RecursiveType(self =>
            VariantType({
                nil: NullType,
                cons: StructType({
                    value: IntegerType,
                    next: ArrayType(self), // note: should have exactly one value
                }),
            })
        );

        const equalCompare = equalFor(ListType);
        const compare = compareFor(ListType);

        // Create a circular list: A -> A
        const selfLoop: any = variant('cons', { value: 1n, next: [] });
        selfLoop.value.next.push(selfLoop);

        // Compare with itself
        assert.equal(equalCompare(selfLoop, selfLoop), true);
        assert.equal(compare(selfLoop, selfLoop), 0);

        // Create another identical circular list
        const selfLoop2: any = variant('cons', { value: 1n, next: [] });
        selfLoop2.value.next.push(selfLoop2);

        // Two different circular lists with same structure and values
        assert.equal(equalCompare(selfLoop, selfLoop2), true);
        assert.equal(compare(selfLoop, selfLoop2), 0); // Both cycle at same depth

        // Different value in cycle
        const selfLoop3: any = variant('cons', { value: 2n, next: [] });
        selfLoop3.value.next.push(selfLoop3);

        assert.equal(equalCompare(selfLoop, selfLoop3), false);
        assert.equal(compare(selfLoop, selfLoop3), -1); // 1 < 2
        assert.equal(compare(selfLoop3, selfLoop), 1);

        // Non-circular list vs circular list
        const nil = variant('nil', null);
        const nonCircular = variant('cons', { value: 1n, next: [nil] });
        assert.equal(compare(nonCircular, selfLoop), 1); // "nil" > "cons"
        assert.equal(compare(selfLoop, nonCircular), -1);

        // Test lessFor, greaterFor, lessEqualFor, greaterEqualFor
        const less = lessFor(ListType);
        const greater = greaterFor(ListType);
        const lessEqual = lessEqualFor(ListType);
        const greaterEqual = greaterEqualFor(ListType);

        // Same circular list
        assert.equal(less(selfLoop, selfLoop), false);
        assert.equal(greater(selfLoop, selfLoop), false);
        assert.equal(lessEqual(selfLoop, selfLoop), true);
        assert.equal(greaterEqual(selfLoop, selfLoop), true);

        // Two identical circular lists
        assert.equal(less(selfLoop, selfLoop2), false); // equal
        assert.equal(lessEqual(selfLoop, selfLoop2), true);
        assert.equal(greaterEqual(selfLoop, selfLoop2), true);

        // Different values in cycles
        assert.equal(less(selfLoop, selfLoop3), true); // 1 < 2
        assert.equal(less(selfLoop3, selfLoop), false);
        assert.equal(greater(selfLoop3, selfLoop), true);
        assert.equal(lessEqual(selfLoop, selfLoop3), true);
        assert.equal(greaterEqual(selfLoop3, selfLoop), true);

        // Non-circular vs circular
        assert.equal(less(nonCircular, selfLoop), false); // "nil" > "cons"
        assert.equal(greater(selfLoop, nonCircular), false);
        assert.equal(lessEqual(nonCircular, selfLoop), false);
        assert.equal(greaterEqual(selfLoop, nonCircular), false);

        // Test isFor (RecursiveType is immutable, so isFor uses structural equality with cycle detection)
        const is = isFor(ListType);

        // Same object
        assert.equal(is(selfLoop, selfLoop), true);
        assert.equal(is(nil, nil), true);

        // Different objects, structurally equal (different array identity)
        assert.equal(is(selfLoop, selfLoop2), false);

        // Different values in cycle
        assert.equal(is(selfLoop, selfLoop3), false);

        // Non-circular vs circular
        assert.equal(is(nonCircular, selfLoop), false);
        assert.equal(is(nil, selfLoop), false);
    });

    test('should compare circular recursive data (cycle in chain)', () => {
        // Linked list type
        const ListType = RecursiveType(self =>
            VariantType({
                nil: NullType,
                cons: StructType({
                    value: IntegerType,
                    next: ArrayType(self),
                }),
            })
        );

        const equalCompare = equalFor(ListType);
        const compare = compareFor(ListType);

        // Create a cycle: A(1) -> B(2) -> C(3) -> B(2) (cycle at depth 2)
        const nil = variant('nil', null);
        const nodeB: any = variant('cons', { value: 2n, next: [nil] });
        const nodeC = variant('cons', { value: 3n, next: [nodeB] });
        nodeB.value.next = [nodeC]; // Create the cycle
        const listA = variant('cons', { value: 1n, next: [nodeB] });

        // Compare with itself
        assert.equal(equalCompare(listA, listA), true);
        assert.equal(compare(listA, listA), 0);

        // Create another identical cyclic structure
        const nodeB2: any = variant('cons', { value: 2n, next: [nil] });
        const nodeC2 = variant('cons', { value: 3n, next: [nodeB2] });
        nodeB2.value.next = [nodeC2];
        const listA2 = variant('cons', { value: 1n, next: [nodeB2] });

        // Two different cyclic lists with same structure
        assert.equal(equalCompare(listA, listA2), true);
        assert.equal(compare(listA, listA2), 0); // Both cycle at same depth

        // Different cycle structure (cycle at different depth) Y(1) -> X(2) -> X(2)
        const nodeX: any = variant('cons', { value: 2n, next: [nil] });
        nodeX.value.next = [nodeX]; // Self-loop instead
        const listY = variant('cons', { value: 1n, next: [nodeX] });

        // Different cycle structure should not be equal
        assert.equal(equalCompare(listA, listY), false);
        // listA has B->C->B cycle, listY has X->X cycle
        // When comparing, X cycles earlier (at depth 1) while C is still acyclic
        // So listY is "more infinite", making listY > listA
        assert.equal(compare(listA, listY), 1);
        assert.equal(compare(listY, listA), -1);

        // Test lessFor, greaterFor, lessEqualFor, greaterEqualFor
        const less = lessFor(ListType);
        const greater = greaterFor(ListType);
        const lessEqual = lessEqualFor(ListType);
        const greaterEqual = greaterEqualFor(ListType);

        // Same list
        assert.equal(less(listA, listA), false);
        assert.equal(greater(listA, listA), false);
        assert.equal(lessEqual(listA, listA), true);
        assert.equal(greaterEqual(listA, listA), true);

        // Two identical cyclic structures
        assert.equal(less(listA, listA2), false); // equal
        assert.equal(lessEqual(listA, listA2), true);
        assert.equal(greaterEqual(listA, listA2), true);

        // Different cycle structures
        assert.equal(less(listA, listY), false); // listY < listA (2 < 3)
        assert.equal(less(listY, listA), true);
        assert.equal(greater(listA, listY), true);
        assert.equal(greater(listY, listA), false);
        assert.equal(lessEqual(listA, listY), false);
        assert.equal(lessEqual(listY, listA), true);
        assert.equal(greaterEqual(listA, listY), true);
        assert.equal(greaterEqual(listY, listA), false);

        // Test isFor (RecursiveType is immutable, so isFor uses structural equality with cycle detection)
        const is = isFor(ListType);

        // Same object
        assert.equal(is(listA, listA), true);

        // Different objects, structurally equal (different array identity)
        assert.equal(is(listA, listA2), false);

        // Different cycle structures
        assert.equal(is(listA, listY), false);
    });

    test('should compare circular recursive data (binary tree with cycle)', () => {
        // Binary tree type
        const TreeType = RecursiveType(self =>
            VariantType({
                leaf: NullType,
                node: StructType({
                    value: IntegerType,
                    left: ArrayType(self),
                    right: ArrayType(self),
                }),
            })
        );

        const equalCompare = equalFor(TreeType);
        const compare = compareFor(TreeType);

        const leaf = variant('leaf', null);

        // Create a tree with a cycle: root -> left -> root
        const root: any = variant('node', { value: 1n, left: [leaf], right: [leaf] });
        const leftChild = variant('node', { value: 2n, left: [root], right: [leaf] });
        root.value.left = [leftChild];

        // Compare with itself
        assert.equal(equalCompare(root, root), true);
        assert.equal(compare(root, root), 0);

        // Create another identical cyclic tree
        const root2: any = variant('node', { value: 1n, left: [leaf], right: [leaf] });
        const leftChild2 = variant('node', { value: 2n, left: [root2], right: [leaf] });
        root2.value.left = [leftChild2];

        // Two different cyclic trees with same structure
        assert.equal(equalCompare(root, root2), true);
        assert.equal(compare(root, root2), 0);

        // Different structure (no cycle)
        const root3 = variant('node', { value: 1n, left: [variant('node', { value: 2n, left: [leaf], right: [leaf] })], right: [leaf] });
        assert.equal(equalCompare(root, root3), false);
        assert.equal(compare(root, root3), 1); // cyclic > acyclic ("infinite" > finite)
        assert.equal(compare(root3, root), -1);

        // Test lessFor, greaterFor, lessEqualFor, greaterEqualFor
        const less = lessFor(TreeType);
        const greater = greaterFor(TreeType);
        const lessEqual = lessEqualFor(TreeType);
        const greaterEqual = greaterEqualFor(TreeType);

        // Same tree
        assert.equal(less(root, root), false);
        assert.equal(greater(root, root), false);
        assert.equal(lessEqual(root, root), true);
        assert.equal(greaterEqual(root, root), true);

        // Two identical cyclic trees
        assert.equal(less(root, root2), false); // equal
        assert.equal(lessEqual(root, root2), true);
        assert.equal(greaterEqual(root, root2), true);

        // Cyclic vs acyclic
        assert.equal(less(root3, root), true); // acyclic < cyclic
        assert.equal(less(root, root3), false);
        assert.equal(greater(root, root3), true);
        assert.equal(lessEqual(root3, root), true);
        assert.equal(greaterEqual(root, root3), true);

        // Test isFor (RecursiveType is immutable, so isFor uses structural equality with cycle detection)
        const is = isFor(TreeType);

        // Same object
        assert.equal(is(root, root), true);
        assert.equal(is(leaf, leaf), true);

        // Different objects, structurally equal (different array identity)
        assert.equal(is(root, root2), false);

        // Cyclic vs acyclic
        assert.equal(is(root, root3), false);
    });

    test('should compare nested recursive types (tree of lists)', () => {
        // Linked list type
        const ListType = RecursiveType(self =>
            VariantType({
                nil: NullType,
                cons: StructType({
                    value: IntegerType,
                    next: self,
                }),
            })
        );

        // Binary tree type containing lists at each node
        const TreeOfListsType = RecursiveType(self =>
            VariantType({
                leaf: NullType,
                node: StructType({
                    list: ListType,
                    left: self,
                    right: self,
                }),
            })
        );

        const equalCompare = equalFor(TreeOfListsType);
        const compare = compareFor(TreeOfListsType);

        // Create some lists
        const nil = variant('nil', null);
        const list1 = variant('cons', { value: 1n, next: variant('cons', { value: 2n, next: nil }) });
        const list2 = variant('cons', { value: 3n, next: nil });

        // Create trees containing these lists
        const leaf = variant('leaf', null);
        const tree1 = variant('node', {
            list: list1,
            left: variant('node', { list: list2, left: leaf, right: leaf }),
            right: leaf
        });

        const tree2 = variant('node', {
            list: list1,
            left: variant('node', { list: list2, left: leaf, right: leaf }),
            right: leaf
        });

        // Same structure
        assert.equal(equalCompare(tree1, tree2), true);
        assert.equal(compare(tree1, tree2), 0);

        // Different list content
        const tree3 = variant('node', {
            list: list2,  // Different list
            left: variant('node', { list: list2, left: leaf, right: leaf }),
            right: leaf
        });

        assert.equal(equalCompare(tree1, tree3), false);
        assert.equal(compare(tree1, tree3), -1); // list1 < list2 (starts with 1 vs 3)
        assert.equal(compare(tree3, tree1), 1);

        // Test lessFor, greaterFor, lessEqualFor, greaterEqualFor
        const less = lessFor(TreeOfListsType);
        const greater = greaterFor(TreeOfListsType);
        const lessEqual = lessEqualFor(TreeOfListsType);
        const greaterEqual = greaterEqualFor(TreeOfListsType);

        // Same tree
        assert.equal(less(tree1, tree1), false);
        assert.equal(greater(tree1, tree1), false);
        assert.equal(lessEqual(tree1, tree1), true);
        assert.equal(greaterEqual(tree1, tree1), true);

        // Equal trees
        assert.equal(less(tree1, tree2), false);
        assert.equal(lessEqual(tree1, tree2), true);
        assert.equal(greaterEqual(tree1, tree2), true);

        // Different list content
        assert.equal(less(tree1, tree3), true); // list1 < list2
        assert.equal(less(tree3, tree1), false);
        assert.equal(greater(tree3, tree1), true);
        assert.equal(lessEqual(tree1, tree3), true);
        assert.equal(greaterEqual(tree3, tree1), true);

        // Test isFor (RecursiveType is immutable, so isFor uses structural equality)
        const is = isFor(TreeOfListsType);

        // Same object
        assert.equal(is(tree1, tree1), true);
        assert.equal(is(leaf, leaf), true);

        // Different objects, structurally equal
        assert.equal(is(tree1, tree2), true);

        // Different list content
        assert.equal(is(tree1, tree3), false);
    });

    test('should throw for invalid type in isFor', () => {
        // Force execution of unreachable error path using invalid type
        const invalidType = { type: 'InvalidType' } as any;
        assert.throws(() => isFor(invalidType), /Unknown type encountered during type printing: InvalidType/);
    });

    test('should throw for invalid type in lessEqualFor', () => {
        // Force execution of unreachable error path using invalid type
        const invalidType = { type: 'InvalidType' } as any;
        assert.throws(() => lessEqualFor(invalidType), /Unknown type encountered during type printing: InvalidType/);
    });

    test('should throw for invalid type in greaterFor', () => {
        // Force execution of unreachable error path using invalid type
        const invalidType = { type: 'InvalidType' } as any;
        assert.throws(() => greaterFor(invalidType), /Unknown type encountered during type printing: InvalidType/);
    });
});