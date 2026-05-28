/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describe, test } from "node:test";
import assert from "node:assert/strict";
import {
  NullType, BooleanType, IntegerType, FloatType, StringType, DateTimeType,
  ArrayType, SetType, DictType, StructType, VariantType,
  type EastType,
} from "../types.js";
import { encodeBeast2For, decodeBeast2, MAGIC_BYTES } from "./beast2.js";
import { isTypeValueEqual, variant } from "../index.js";
import { toEastTypeValue, type EastTypeValue } from "../type_of_type.js";

function assertTypeEquals(actual: EastTypeValue, expected: EastType): void {
  assert.ok(isTypeValueEqual(actual, toEastTypeValue(expected)), `Expected ${JSON.stringify(expected)} but got ${JSON.stringify(actual)}`);
}

// =============================================================================
// Magic bytes tests
// =============================================================================

describe("Beast magic bytes", () => {
  test("MAGIC_BYTES should be 8 bytes", () => {
    assert.equal(MAGIC_BYTES.length, 8);
  });

  test("MAGIC_BYTES should start with 0x89", () => {
    assert.equal(MAGIC_BYTES[0], 0x89);
  });

  test("MAGIC_BYTES should contain 'East' (0x45 0x61 0x73 0x74)", () => {
    assert.equal(MAGIC_BYTES[1], 0x45); // 'E'
    assert.equal(MAGIC_BYTES[2], 0x61); // 'a'
    assert.equal(MAGIC_BYTES[3], 0x73); // 's'
    assert.equal(MAGIC_BYTES[4], 0x74); // 't'
  });

  test("MAGIC_BYTES should contain CRLF (0x0D 0x0A)", () => {
    assert.equal(MAGIC_BYTES[5], 0x0D); // CR
    assert.equal(MAGIC_BYTES[6], 0x0A); // LF
  });

  test("MAGIC_BYTES should have version byte 0x01", () => {
    assert.equal(MAGIC_BYTES[7], 0x01);
  });
});

// =============================================================================
// Primitive value encoding tests
// =============================================================================

describe("Beast primitive values", () => {
  test("null value should round-trip", () => {
    const encoded = encodeBeast2For(NullType)(null);
    assert.ok(encoded.length > MAGIC_BYTES.length);

    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, NullType);
    assert.equal(value, null);
  });

  test("boolean value should round-trip", () => {
    const encoded = encodeBeast2For(BooleanType)(true);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, BooleanType);
    assert.equal(value, true);
  });

  test("integer value should round-trip", () => {
    const encoded = encodeBeast2For(IntegerType)(42n);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, IntegerType);
    assert.equal(value, 42n);
  });

  test("negative integer should round-trip", () => {
    const encoded = encodeBeast2For(IntegerType)(-123n);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, IntegerType);
    assert.equal(value, -123n);
  });

  test("float value should round-trip", () => {
    const encoded = encodeBeast2For(FloatType)(3.14);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, FloatType);
    assert.ok(Math.abs(value - 3.14) < 0.0001);
  });

  test("string value should round-trip", () => {
    const encoded = encodeBeast2For(StringType)("hello world");
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, StringType);
    assert.equal(value, "hello world");
  });

  test("empty string should round-trip", () => {
    const encoded = encodeBeast2For(StringType)("");
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, StringType);
    assert.equal(value, "");
  });

  test("unicode string should round-trip", () => {
    const encoded = encodeBeast2For(StringType)("Hello 世界 🌍");
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, StringType);
    assert.equal(value, "Hello 世界 🌍");
  });

  test("DateTime value should round-trip", () => {
    const date = new Date("2024-01-15T10:30:00Z");
    const encoded = encodeBeast2For(DateTimeType)(date);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, DateTimeType);
    assert.equal(value.getTime(), date.getTime());
  });
});

// =============================================================================
// Array encoding tests
// =============================================================================

describe("Beast array values", () => {
  test("empty array should round-trip", () => {
    const arrayType = ArrayType(IntegerType);
    const encoded = encodeBeast2For(arrayType)([]);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, arrayType);
    assert.deepStrictEqual(value, []);
  });

  test("integer array should round-trip", () => {
    const arrayType = ArrayType(IntegerType);
    const encoded = encodeBeast2For(arrayType)([1n, 2n, 3n]);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, arrayType);
    assert.deepStrictEqual(value, [1n, 2n, 3n]);
  });

  test("string array should round-trip", () => {
    const arrayType = ArrayType(StringType);
    const encoded = encodeBeast2For(arrayType)(["foo", "bar", "baz"]);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, arrayType);
    assert.deepStrictEqual(value, ["foo", "bar", "baz"]);
  });

  test("nested array should round-trip", () => {
    const arrayType = ArrayType(ArrayType(IntegerType));
    const encoded = encodeBeast2For(arrayType)([[1n, 2n], [3n, 4n]]);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, arrayType);
    assert.deepStrictEqual(value, [[1n, 2n], [3n, 4n]]);
  });
});

// =============================================================================
// Set encoding tests
// =============================================================================

describe("Beast set values", () => {
  test("empty set should round-trip", () => {
    const setType = SetType(IntegerType);
    const encoded = encodeBeast2For(setType)(new Set());
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, setType);
    assert.ok(value instanceof Set);
    assert.equal(value.size, 0);
  });

  test("integer set should round-trip", () => {
    const setType = SetType(IntegerType);
    const encoded = encodeBeast2For(setType)(new Set([1n, 2n, 3n]));
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, setType);
    assert.ok(value instanceof Set);
    assert.deepStrictEqual([...value].sort(), [1n, 2n, 3n]);
  });

  test("string set should round-trip", () => {
    const setType = SetType(StringType);
    const encoded = encodeBeast2For(setType)(new Set(["foo", "bar", "baz"]));
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, setType);
    assert.ok(value instanceof Set);
    assert.deepStrictEqual([...value].sort(), ["bar", "baz", "foo"]);
  });
});

// =============================================================================
// Dict encoding tests
// =============================================================================

describe("Beast dict values", () => {
  test("empty dict should round-trip", () => {
    const dictType = DictType(StringType, IntegerType);
    const encoded = encodeBeast2For(dictType)(new Map());
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, dictType);
    assert.ok(value instanceof Map);
    assert.equal(value.size, 0);
  });

  test("string-to-integer dict should round-trip", () => {
    const dictType = DictType(StringType, IntegerType);
    const dict = new Map([
      ["one", 1n],
      ["two", 2n],
      ["three", 3n],
    ]);
    const encoded = encodeBeast2For(dictType)(dict);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, dictType);
    assert.ok(value instanceof Map);
    assert.equal(value.get("one"), 1n);
    assert.equal(value.get("two"), 2n);
    assert.equal(value.get("three"), 3n);
  });
});

// =============================================================================
// Struct encoding tests
// =============================================================================

describe("Beast struct values", () => {
  test("simple struct should round-trip", () => {
    const structType = StructType({
      name: StringType,
      age: IntegerType,
      active: BooleanType,
    });
    const structValue = {
      name: "Alice",
      age: 30n,
      active: true,
    };
    const encoded = encodeBeast2For(structType)(structValue);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, structType);
    assert.deepStrictEqual(value, structValue);
  });

  test("nested struct should round-trip", () => {
    const structType = StructType({
      point: StructType({ x: IntegerType, y: IntegerType }),
      label: StringType,
    });
    const structValue = {
      point: { x: 10n, y: 20n },
      label: "origin",
    };
    const encoded = encodeBeast2For(structType)(structValue);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, structType);
    assert.deepStrictEqual(value, structValue);
  });
});

// =============================================================================
// Variant encoding tests
// =============================================================================

describe("Beast variant values", () => {
  test("variant none case should round-trip", () => {
    const variantType = VariantType({
      none: NullType,
      some: IntegerType,
    });
    const variantValue = variant("none", null);
    const encoded = encodeBeast2For(variantType)(variantValue);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, variantType);
    assert.equal(value.type, "none");
    assert.equal(value.value, null);
  });

  test("variant some case should round-trip", () => {
    const variantType = VariantType({
      none: NullType,
      some: IntegerType,
    });
    const variantValue = variant("some", 42n);
    const encoded = encodeBeast2For(variantType)(variantValue);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, variantType);
    assert.equal(value.type, "some");
    assert.equal(value.value, 42n);
  });

  test("variant with struct case should round-trip", () => {
    const variantType = VariantType({
      point: StructType({ x: IntegerType, y: IntegerType }),
      label: StringType,
    });
    const variantValue = variant("point", { x: 5n, y: 10n });
    const encoded = encodeBeast2For(variantType)(variantValue);
    const { type, value } = decodeBeast2(encoded);
    assertTypeEquals(type, variantType);
    assert.equal(value.type, "point");
    assert.deepStrictEqual(value.value, { x: 5n, y: 10n });
  });
});

// =============================================================================
// Error handling tests
// =============================================================================

describe("Beast error handling", () => {
  test("should reject data that's too short", () => {
    const shortData = new Uint8Array([0x89, 0x45, 0x61]); // Only 3 bytes
    assert.throws(() => decodeBeast2(shortData), /Data too short/);
  });

  test("should reject invalid magic bytes", () => {
    const invalidData = new Uint8Array([0x00, 0x45, 0x61, 0x73, 0x74, 0x0D, 0x0A, 0x01, 0x0A]);
    assert.throws(() => decodeBeast2(invalidData), /Invalid Beast magic bytes/);
  });

  test("should reject data with wrong version", () => {
    const wrongVersion = new Uint8Array([0x89, 0x45, 0x61, 0x73, 0x74, 0x0D, 0x0A, 0x02, 0x0A]);
    assert.throws(() => decodeBeast2(wrongVersion), /Invalid Beast magic bytes at offset 7/);
  });

  test("should reject truncated data", () => {
    const encoded = encodeBeast2For(IntegerType)(42n);
    const truncated = encoded.slice(0, encoded.length - 1);
    assert.throws(() => decodeBeast2(truncated));
  });
});

// =============================================================================
// Format overhead tests
// =============================================================================

describe("Beast format overhead", () => {
  test("overhead for null should be 8 bytes (magic) + 1 byte (type tag)", () => {
    const encoded = encodeBeast2For(NullType)(null);
    assert.equal(encoded.length, 9); // 8 magic + 1 type tag + 0 value
  });

  test("overhead for boolean should be 8 bytes (magic) + 1 byte (type tag)", () => {
    const encoded = encodeBeast2For(BooleanType)(true);
    assert.equal(encoded.length, 10); // 8 magic + 1 type tag + 1 value
  });

  test("overhead for simple integer should be minimal", () => {
    const encoded = encodeBeast2For(IntegerType)(0n);
    assert.equal(encoded.length, 10); // 8 magic + 1 type tag + 1 value (zigzag 0)
  });

  test("array type overhead should include element type", () => {
    const encoded = encodeBeast2For(ArrayType(IntegerType))([]);
    // 8 magic + 2 type tags (Array + Integer) + 1 inline marker + 1 length (0) = 12
    assert.equal(encoded.length, 12);
  });
});
