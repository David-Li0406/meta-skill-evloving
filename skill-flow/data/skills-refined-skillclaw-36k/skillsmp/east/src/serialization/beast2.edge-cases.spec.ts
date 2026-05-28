/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describe, test } from "node:test";
import assert from "node:assert/strict";
import {
  NullType, BooleanType, IntegerType, FloatType, StringType, DateTimeType, BlobType,
  ArrayType, SetType, DictType, StructType, VariantType, RefType,
  type EastType,
} from "../types.js";
import { encodeBeast2For, decodeBeast2, encodeBeast2ValueFor, decodeBeast2ValueFor } from "./beast2.js";
import { toEastTypeValue, type EastTypeValue } from "../type_of_type.js";
import { isTypeValueEqual } from "../compile.js";
import { variant } from "../containers/variant.js";
import { ref } from "../containers/ref.js";

function assertTypeEquals(actual: EastTypeValue, expected: EastType): void {
  assert.ok(isTypeValueEqual(actual, toEastTypeValue(expected)));
}

function roundTrip(type: EastType, value: any, mode: "raw" | "beast" = "raw") {
  if (mode === "raw") {
    const encoded = encodeBeast2ValueFor(type)(value);
    const [decoded, offset] = decodeBeast2ValueFor(type)(encoded, 0);
    assert.equal(encoded.length, offset);
    return decoded;
  } else if (mode === "beast") {
    const encoded = encodeBeast2For(type)(value);
    const { type: decodedType, value: decoded } = decodeBeast2(encoded);
    assertTypeEquals(decodedType, type);
    return decoded;
  } else {
    throw new Error(`Unknown mode: ${mode}`);
  }
}

// =============================================================================
// Extreme integer values
// =============================================================================

describe("Extreme integer values", () => {
  test("MIN_INT64 should round-trip", () => {
    const minInt64 = -9223372036854775808n;
    const decoded = roundTrip(IntegerType, minInt64);
    assert.equal(decoded, minInt64);
  });

  test("MAX_INT64 should round-trip", () => {
    const maxInt64 = 9223372036854775807n;
    const decoded = roundTrip(IntegerType, maxInt64);
    assert.equal(decoded, maxInt64);
  });

  test("Large positive integers should round-trip", () => {
    const values = [
      90071992547409919n,
      1000000000000000n,
      999999999999999n,
    ];
    for (const v of values) {
      const decoded = roundTrip(IntegerType, v);
      assert.equal(decoded, v);
    }
  });

  test("Large negative integers should round-trip", () => {
    const values = [
      -90071992547409919n,
      -1000000000000000n,
      -999999999999999n,
    ];
    for (const v of values) {
      const decoded = roundTrip(IntegerType, v);
      assert.equal(decoded, v);
    }
  });

  test("Powers of 2 should round-trip", () => {
    for (let i = 0; i < 60; i++) {
      const value = 1n << BigInt(i);
      const decoded = roundTrip(IntegerType, value);
      assert.equal(decoded, value);
    }
  });
});

// =============================================================================
// Special float values
// =============================================================================

describe("Special float values", () => {
  test("Positive and negative zero should round-trip", () => {
    const posZero = roundTrip(FloatType, 0);
    const negZero = roundTrip(FloatType, -0);
    assert.equal(posZero, 0);
    assert.equal(negZero, -0);
    assert.ok(Object.is(negZero, -0)); // Check it's truly -0
  });

  test("Very small numbers should round-trip", () => {
    const values = [1e-16, -1e-16, 1e-100, -1e-100, Number.MIN_VALUE];
    for (const v of values) {
      const decoded = roundTrip(FloatType, v);
      assert.ok(Math.abs(decoded - v) < 1e-200 || (v === 0 && decoded === 0));
    }
  });

  test("Very large numbers should round-trip", () => {
    const values = [1e8, -1e8, 1e100, -1e100, Number.MAX_VALUE];
    for (const v of values) {
      const decoded = roundTrip(FloatType, v);
      assert.equal(decoded, v);
    }
  });

  test("Infinities should round-trip", () => {
    assert.equal(roundTrip(FloatType, Infinity), Infinity);
    assert.equal(roundTrip(FloatType, -Infinity), -Infinity);
  });

  test("NaN should round-trip", () => {
    const decoded = roundTrip(FloatType, NaN);
    assert.ok(Number.isNaN(decoded));
  });

  test("Special values in all modes", () => {
    const values = [-Infinity, -1e8, -3.14, -1, -0, 0, 1, 3.14, 1e8, Infinity, NaN];
    for (const mode of ["raw", "beast"] as const) {
      for (const v of values) {
        const decoded = roundTrip(FloatType, v, mode);
        if (Number.isNaN(v)) {
          assert.ok(Number.isNaN(decoded));
        } else {
          assert.ok(Math.abs(decoded - v) < 0.0001 || decoded === v);
        }
      }
    }
  });
});

// =============================================================================
// Blob edge cases
// =============================================================================

describe("Blob edge cases", () => {
  test("Empty blob should round-trip", () => {
    const blob = new Uint8Array([]);
    const decoded = roundTrip(BlobType, blob);
    assert.deepStrictEqual(decoded, blob);
  });

  test("Small blob should round-trip", () => {
    const blob = new Uint8Array([1, 3, 3, 7]);
    const decoded = roundTrip(BlobType, blob);
    assert.deepStrictEqual(decoded, blob);
  });

  test("Blob with all byte values (0-255) should round-trip", () => {
    const blob = new Uint8Array(256);
    for (let i = 0; i < 256; i++) {
      blob[i] = i;
    }
    const decoded = roundTrip(BlobType, blob);
    assert.deepStrictEqual(decoded, blob);
  });

  test("Large blob (1MB) should round-trip", () => {
    const size = 1024 * 1024; // 1MB
    const blob = new Uint8Array(size);
    for (let i = 0; i < size; i++) {
      blob[i] = i % 256;
    }
    const decoded = roundTrip(BlobType, blob);
    assert.equal(decoded.length, blob.length);
    assert.deepStrictEqual(decoded, blob);
  });
});

// =============================================================================
// DateTime edge cases
// =============================================================================

describe("DateTime edge cases", () => {
  test("Unix epoch should round-trip", () => {
    const epoch = new Date(0);
    const decoded = roundTrip(DateTimeType, epoch);
    assert.equal(decoded.getTime(), epoch.getTime());
  });

  test("Recent date with milliseconds should round-trip", () => {
    const date = new Date("2022-06-29T13:43:00.123Z");
    const decoded = roundTrip(DateTimeType, date);
    assert.equal(decoded.getTime(), date.getTime());
  });

  test("Far future date should round-trip", () => {
    const future = new Date("2100-12-31T23:59:59.999Z");
    const decoded = roundTrip(DateTimeType, future);
    assert.equal(decoded.getTime(), future.getTime());
  });

  test("Far past date should round-trip", () => {
    const past = new Date("1900-01-01T00:00:00.000Z");
    const decoded = roundTrip(DateTimeType, past);
    assert.equal(decoded.getTime(), past.getTime());
  });

  test("Negative timestamp should round-trip", () => {
    const negative = new Date(-1000000000000); // Before epoch
    const decoded = roundTrip(DateTimeType, negative);
    assert.equal(decoded.getTime(), negative.getTime());
  });
});

// =============================================================================
// String edge cases
// =============================================================================

describe("String edge cases", () => {
  test("Strings of varying lengths", () => {
    const strings = [
      "",
      "a",
      "ab",
      "abc",
      "a".repeat(100),
      "a".repeat(1000),
      "a".repeat(10000),
    ];
    for (const s of strings) {
      const decoded = roundTrip(StringType, s);
      assert.equal(decoded, s);
    }
  });

  test("UTF-8 strings", () => {
    const strings = [
      "いろはにほへとちりぬるを", // Japanese
      "Здравствуй мир", // Russian
      "مرحبا بالعالم", // Arabic
      "你好世界", // Chinese
      "🚀🌟💡🎉", // Emoji
      "Mixed: Hello 世界 🌍",
    ];
    for (const s of strings) {
      const decoded = roundTrip(StringType, s);
      assert.equal(decoded, s);
    }
  });

  test("Strings with special characters", () => {
    const strings = [
      "\n\r\t",
      "line1\nline2\rline3\tline4",
      "\0null byte in middle\0",
      "\"quotes\" and 'apostrophes'",
      "backslash\\test",
    ];
    for (const s of strings) {
      const decoded = roundTrip(StringType, s);
      assert.equal(decoded, s);
    }
  });
});

// =============================================================================
// Collection edge cases
// =============================================================================

describe("Collection edge cases", () => {
  test("Large arrays should round-trip", () => {
    const largeArray = Array.from({ length: 10000 }, (_, i) => BigInt(i));
    const arrayType = ArrayType(IntegerType);
    const decoded = roundTrip(arrayType, largeArray);
    assert.equal(decoded.length, largeArray.length);
    assert.deepStrictEqual(decoded, largeArray);
  });

  test("Deeply nested arrays should round-trip", () => {
    let type: EastType = IntegerType;
    let value: any = 42n;
    // Create 10 levels of nesting
    for (let i = 0; i < 10; i++) {
      type = ArrayType(type);
      value = [value];
    }
    const decoded = roundTrip(type, value);
    assert.deepStrictEqual(decoded, value);
  });

  test("Large sets should round-trip", () => {
    const largeSet = new Set(Array.from({ length: 1000 }, (_, i) => `item_${i}`));
    const setType = SetType(StringType);
    const decoded = roundTrip(setType, largeSet);
    assert.equal(decoded.size, largeSet.size);
    assert.deepStrictEqual([...decoded].sort(), [...largeSet].sort());
  });

  test("Large dicts should round-trip", () => {
    const largeDict = new Map(
      Array.from({ length: 1000 }, (_, i) => [`key_${i}`, BigInt(i)])
    );
    const dictType = DictType(StringType, IntegerType);
    const decoded = roundTrip(dictType, largeDict);
    assert.equal(decoded.size, largeDict.size);
    for (const [k, v] of largeDict) {
      assert.equal(decoded.get(k), v);
    }
  });
});

// =============================================================================
// Complex real-world structures
// =============================================================================

describe("Complex real-world structures", () => {
  test("Complex struct with many fields should round-trip", () => {
    const complexType = StructType({
      A: DictType(StringType, IntegerType),
      B: BooleanType,
      C: StringType,
      D: StringType,
      E: DateTimeType,
      F: StringType,
      G: FloatType,
      H: FloatType,
      I: StringType,
      J: FloatType,
      K: NullType,
      L: StringType,
    });

    const complexValue = {
      A: new Map([["foo", 123n], ["bar", 456n]]),
      B: true,
      C: "35932005329",
      D: "ABCDE12345678",
      E: new Date("2022-03-01T00:00:00.000Z"),
      F: "A",
      G: -1.5,
      H: 3.14,
      I: "",
      J: 0.0,
      K: null,
      L: "",
    };

    const decoded = roundTrip(complexType, complexValue);
    assert.equal(decoded.B, complexValue.B);
    assert.equal(decoded.C, complexValue.C);
    assert.equal(decoded.D, complexValue.D);
    assert.equal(decoded.E.getTime(), complexValue.E.getTime());
    assert.equal(decoded.F, complexValue.F);
    assert.ok(Math.abs(decoded.G - complexValue.G) < 0.0001);
    assert.ok(Math.abs(decoded.H - complexValue.H) < 0.0001);
  });

  test("Nested variant with struct should round-trip in all modes", () => {
    const type = StructType({
      id: IntegerType,
      result: VariantType({
        error: StructType({ code: IntegerType, message: StringType }),
        success: StructType({ value: FloatType, timestamp: DateTimeType }),
      }),
    });

    const errorValue = {
      id: 1n,
      result: variant(
        "error",
        { code: 404n, message: "Not found" },
      ),
    };

    const successValue = {
      id: 2n,
      result: variant(
        "success",
        { value: 99.9, timestamp: new Date("2024-01-01T00:00:00Z") },
      ),
    };

    for (const mode of ["raw", "beast"] as const) {
      const decodedError = roundTrip(type, errorValue, mode);
      assert.equal(decodedError.id, 1n);
      assert.equal(decodedError.result.type, "error");
      assert.equal(decodedError.result.value.code, 404n);
      assert.equal(decodedError.result.value.message, "Not found");

      const decodedSuccess = roundTrip(type, successValue, mode);
      assert.equal(decodedSuccess.id, 2n);
      assert.equal(decodedSuccess.result.type, "success");
      assert.ok(Math.abs(decodedSuccess.result.value.value - 99.9) < 0.0001);
    }
  });

  test("Array of complex structs should round-trip", () => {
    const itemType = StructType({
      id: IntegerType,
      name: StringType,
      tags: SetType(StringType),
      metadata: DictType(StringType, StringType),
    });
    const arrayType = ArrayType(itemType);

    const arrayValue = [
      {
        id: 1n,
        name: "Item 1",
        tags: new Set(["tag1", "tag2"]),
        metadata: new Map([["key1", "value1"]]),
      },
      {
        id: 2n,
        name: "Item 2",
        tags: new Set(["tag3"]),
        metadata: new Map([["key2", "value2"], ["key3", "value3"]]),
      },
    ];

    const decoded = roundTrip(arrayType, arrayValue);
    assert.equal(decoded.length, 2);
    assert.equal(decoded[0].id, 1n);
    assert.equal(decoded[0].name, "Item 1");
    assert.equal(decoded[1].id, 2n);
  });
});

// =============================================================================
// Cross-mode consistency
// =============================================================================

describe("Cross-mode consistency", () => {
  test("Same value should decode identically in all modes", () => {
    const type = StructType({
      int: IntegerType,
      float: FloatType,
      str: StringType,
      arr: ArrayType(IntegerType),
    });

    const value = {
      int: 42n,
      float: 3.14,
      str: "test",
      arr: [1n, 2n, 3n],
    };

    const rawDecoded = roundTrip(type, value, "raw");
    const beastDecoded = roundTrip(type, value, "beast");

    assert.deepStrictEqual(rawDecoded, value);
    assert.deepStrictEqual(beastDecoded, value);
  });
});

// =============================================================================
// Backreference tests (mutable aliasing)
// =============================================================================

describe("Backreference round-trip", () => {
  test("same array appearing twice should round-trip", () => {
    // Create a structure where the same array object appears twice
    const sharedArray = [1n, 2n, 3n];
    const structType = StructType({
      first: ArrayType(IntegerType),
      second: ArrayType(IntegerType),
    });
    const value = {
      first: sharedArray,
      second: sharedArray, // Same object reference - encoder will use backreference
    };

    const decoded = roundTrip(structType, value, "raw");
    assert.deepStrictEqual(decoded.first, [1n, 2n, 3n]);
    assert.deepStrictEqual(decoded.second, [1n, 2n, 3n]);
    // After decoding, both should reference the same array (backreference preserved identity)
    assert.strictEqual(decoded.first, decoded.second);
  });

  test("same set appearing twice should round-trip", () => {
    const sharedSet = new Set(["a", "b", "c"]);
    const structType = StructType({
      first: SetType(StringType),
      second: SetType(StringType),
    });
    const value = {
      first: sharedSet,
      second: sharedSet,
    };

    const decoded = roundTrip(structType, value, "raw");
    assert.deepStrictEqual([...decoded.first].sort(), ["a", "b", "c"]);
    assert.deepStrictEqual([...decoded.second].sort(), ["a", "b", "c"]);
    assert.strictEqual(decoded.first, decoded.second);
  });

  test("same dict appearing twice should round-trip", () => {
    const sharedDict = new Map([["key", 42n]]);
    const structType = StructType({
      first: DictType(StringType, IntegerType),
      second: DictType(StringType, IntegerType),
    });
    const value = {
      first: sharedDict,
      second: sharedDict,
    };

    const decoded = roundTrip(structType, value, "raw");
    assert.equal(decoded.first.get("key"), 42n);
    assert.equal(decoded.second.get("key"), 42n);
    assert.strictEqual(decoded.first, decoded.second);
  });

  test("deeply nested shared arrays should round-trip", () => {
    const sharedInner = [100n];
    const structType = StructType({
      a: StructType({ nested: ArrayType(IntegerType) }),
      b: StructType({ nested: ArrayType(IntegerType) }),
    });
    const value = {
      a: { nested: sharedInner },
      b: { nested: sharedInner },
    };

    const decoded = roundTrip(structType, value, "raw");
    assert.deepStrictEqual(decoded.a.nested, [100n]);
    assert.deepStrictEqual(decoded.b.nested, [100n]);
    assert.strictEqual(decoded.a.nested, decoded.b.nested);
  });

  test("shared array in beast mode should round-trip", () => {
    const sharedArray = [1n, 2n];
    const structType = StructType({
      first: ArrayType(IntegerType),
      second: ArrayType(IntegerType),
    });
    const value = {
      first: sharedArray,
      second: sharedArray,
    };

    // This tests the full beast2 format with type schema + value section
    const decoded = roundTrip(structType, value, "beast");
    assert.deepStrictEqual(decoded.first, [1n, 2n]);
    assert.deepStrictEqual(decoded.second, [1n, 2n]);
    assert.strictEqual(decoded.first, decoded.second);
  });

  test("same ref appearing twice should round-trip", () => {
    const sharedRef = ref(42n);
    const structType = StructType({
      first: RefType(IntegerType),
      second: RefType(IntegerType),
    });
    const value = {
      first: sharedRef,
      second: sharedRef,
    };

    const decoded = roundTrip(structType, value, "raw");
    assert.equal(decoded.first.value, 42n);
    assert.equal(decoded.second.value, 42n);
    assert.strictEqual(decoded.first, decoded.second);
  });

  test("same ref in beast mode should round-trip", () => {
    const sharedRef = ref("hello");
    const structType = StructType({
      first: RefType(StringType),
      second: RefType(StringType),
    });
    const value = {
      first: sharedRef,
      second: sharedRef,
    };

    const decoded = roundTrip(structType, value, "beast");
    assert.equal(decoded.first.value, "hello");
    assert.equal(decoded.second.value, "hello");
    assert.strictEqual(decoded.first, decoded.second);
  });
});
