/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import assert from "node:assert";
import { defaultValue, minimalValue } from "./default.js";
import {
    NeverType,
    NullType,
    BooleanType,
    IntegerType,
    FloatType,
    StringType,
    DateTimeType,
    BlobType,
    ArrayType,
    SetType,
    DictType,
    StructType,
    VariantType,
    FunctionType,
    AsyncFunctionType
} from "./types.js";

describe("defaultValue", () => {
    test("should throw for Never type", () => {
        assert.throws(() => defaultValue(NeverType), /Cannot create a default value of type .Never/);
    });

    test("should return null for Null type", () => {
        assert.strictEqual(defaultValue(NullType), null);
    });

    test("should return false for Boolean type", () => {
        assert.strictEqual(defaultValue(BooleanType), false);
    });

    test("should return 0n for Integer type", () => {
        assert.strictEqual(defaultValue(IntegerType), 0n);
    });

    test("should return 0.0 for Float type", () => {
        assert.strictEqual(defaultValue(FloatType), 0.0);
    });

    test("should return empty string for String type", () => {
        assert.strictEqual(defaultValue(StringType), "");
    });

    test("should return epoch date for DateTime type", () => {
        const result = defaultValue(DateTimeType);
        assert.ok(result instanceof Date);
        assert.strictEqual(result.getTime(), 0);
    });

    test("should return empty Uint8Array for Blob type", () => {
        const result = defaultValue(BlobType);
        assert.ok(result instanceof Uint8Array);
        assert.strictEqual(result.length, 0);
    });

    test("should return empty array for Array type", () => {
        const result = defaultValue(ArrayType(IntegerType));
        assert.ok(Array.isArray(result));
        assert.strictEqual(result.length, 0);
    });

    test("should return empty SortedSet for Set type", () => {
        const result = defaultValue(SetType(IntegerType));
        assert.ok(result instanceof Set);
        assert.strictEqual(result.size, 0);
    });

    test("should return empty SortedMap for Dict type", () => {
        const result = defaultValue(DictType(StringType, IntegerType));
        assert.ok(result instanceof Map);
        assert.strictEqual(result.size, 0);
    });

    test("should return struct with default field values for Struct type", () => {
        const type = StructType({
            name: StringType,
            age: IntegerType,
            active: BooleanType
        });

        const result = defaultValue(type);

        assert.deepStrictEqual(result, {
            name: "",
            age: 0n,
            active: false
        });
    });

    test("should return nested struct with default values", () => {
        const type = StructType({
            user: StructType({ name: StringType, age: IntegerType }),
            score: FloatType
        });
        const result = defaultValue(type);

        assert.deepStrictEqual(result, {
            user: { name: "", age: 0n },
            score: 0.0
        });
    });

    test("should return first variant case with default value for Variant type", () => {
        const type = VariantType({
            none: NullType,
            some: IntegerType
        });
        const result = defaultValue(type);

        // Should return the first case (none) with its default value (null)
        assert.strictEqual(result.type, "none");
        assert.strictEqual(result.value, null);
    });

    test("should throw for empty Variant type", () => {
        const type = VariantType({});
        assert.throws(() => defaultValue(type), /Cannot create a value of an empty variant/);
    });

    test("should throw for Function type", () => {
        const type = FunctionType([], NullType);
        assert.throws(() => defaultValue(type), /Cannot create a default value of type .Function/);
    });

    test("should throw for AsyncFunction type", () => {
        const type = AsyncFunctionType([], NullType);
        assert.throws(() => defaultValue(type), /Cannot create a default value of type .AsyncFunction/);
    });
});

describe("minimalValue", () => {
    test("should throw for Never type", () => {
        assert.throws(() => minimalValue(NeverType), /Cannot create a default value of type .Never/);
    });

    test("should return null for Null type", () => {
        assert.strictEqual(minimalValue(NullType), null);
    });

    test("should return false for Boolean type", () => {
        assert.strictEqual(minimalValue(BooleanType), false);
    });

    test("should return 0n for Integer type", () => {
        assert.strictEqual(minimalValue(IntegerType), 0n);
    });

    test("should return 0.0 for Float type", () => {
        assert.strictEqual(minimalValue(FloatType), 0.0);
    });

    test("should return empty string for String type", () => {
        assert.strictEqual(minimalValue(StringType), "");
    });

    test("should return epoch date for DateTime type", () => {
        const result = minimalValue(DateTimeType);
        assert.ok(result instanceof Date);
        assert.strictEqual(result.getTime(), 0);
    });

    test("should return empty Uint8Array for Blob type", () => {
        const result = minimalValue(BlobType);
        assert.ok(result instanceof Uint8Array);
        assert.strictEqual(result.length, 0);
    });

    test("should return empty array for Array type", () => {
        const result = minimalValue(ArrayType(IntegerType));
        assert.ok(Array.isArray(result));
        assert.strictEqual(result.length, 0);
    });

    test("should return empty SortedSet for Set type", () => {
        const result = minimalValue(SetType(StringType));
        assert.ok(result instanceof Set);
        assert.strictEqual(result.size, 0);
    });

    test("should return empty SortedMap for Dict type", () => {
        const result = minimalValue(DictType(IntegerType, StringType));
        assert.ok(result instanceof Map);
        assert.strictEqual(result.size, 0);
    });

    test("should return struct with minimal field values for Struct type", () => {
        const type = StructType({
            x: IntegerType,
            y: FloatType
        });
        const result = minimalValue(type);

        assert.deepStrictEqual(result, {
            x: 0n,
            y: 0.0
        });
    });

    test("should return first variant case with minimal value for Variant type", () => {
        const type = VariantType({
            a: IntegerType,
            b: StringType
        });
        const result = minimalValue(type);

        // Should return the first case (a) with its default value (0n)
        assert.strictEqual(result.type, "a");
        assert.strictEqual(result.value, 0n);
    });

    test("should throw for empty Variant type", () => {
        const type = VariantType({});
        assert.throws(() => minimalValue(type), /Cannot create a value of an empty variant/);
    });

    test("should throw for Function type", () => {
        const type = FunctionType([IntegerType], StringType);
        assert.throws(() => minimalValue(type), /Cannot create a default value of type .Function/);
    });

    test("should throw for AsyncFunction type", () => {
        const type = AsyncFunctionType([IntegerType], StringType);
        assert.throws(() => minimalValue(type), /Cannot create a default value of type .AsyncFunction/);
    });
});
