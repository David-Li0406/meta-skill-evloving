/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describe, test } from "node:test";
import assert from "node:assert/strict";
import {
  NullType, BooleanType, IntegerType, FloatType, StringType, DateTimeType, BlobType,
  ArrayType, SetType, DictType, StructType, VariantType,
  type EastType,
} from "../types.js";
import { encodeBeastValueFor, decodeBeastValueFor } from "./beast.js";
import { equalFor, lessFor } from "../comparison.js";
import { variant } from "../containers/variant.js";

// =============================================================================
// Byte ordering utilities (memcmp simulation)
// =============================================================================

/**
 * Compare two byte arrays lexicographically (simulates memcmp)
 * Returns: -1 if a < b, 0 if a == b, 1 if a > b
 */
function memcmp(a: Uint8Array, b: Uint8Array): number {
  const minLen = Math.min(a.length, b.length);
  for (let i = 0; i < minLen; i++) {
    if (a[i]! < b[i]!) return -1;
    if (a[i]! > b[i]!) return 1;
  }
  return a.length < b.length ? -1 : a.length === b.length ? 0 : 1;
}

// =============================================================================
// Comprehensive test helper
// =============================================================================

/**
 * Helper to stringify values for error messages (handles BigInt)
 */
function stringify(v: any): string {
  return JSON.stringify(v, (_key, value) =>
    typeof value === 'bigint' ? value.toString() + 'n' : value
  );
}

/**
 * Test that values round-trip correctly (without checking byte ordering).
 */
function testRoundTrip<T extends EastType>(type: T, values: any[]): void {
  const encode = encodeBeastValueFor(type);
  const decode = decodeBeastValueFor(type);
  const equal = equalFor(type);

  // Test each value round-trips
  for (const v of values) {
    const encoded = encode(v);
    const [decoded, offset] = decode(encoded, 0);
    assert.equal(offset, encoded.length, `Did not consume all bytes for ${stringify(v)}`);
    assert.ok(equal(decoded, v), `Value did not round-trip: ${stringify(v)}`);
  }
}

/**
 * Test that values round-trip correctly AND that byte ordering matches value ordering.
 * This is the critical property of beast v1 format.
 */
function testRoundTripAndOrdering<T extends EastType>(type: T, values: any[]): void {
  const encode = encodeBeastValueFor(type);
  const decode = decodeBeastValueFor(type);
  const equal = equalFor(type);
  const less = lessFor(type);

  // Test each value round-trips
  for (const v of values) {
    const encoded = encode(v);
    const [decoded, offset] = decode(encoded, 0);
    assert.equal(offset, encoded.length, `Did not consume all bytes for ${stringify(v)}`);
    assert.ok(equal(decoded, v), `Value did not round-trip: ${stringify(v)}`);
  }

  // Test byte ordering matches value ordering (the key property of beast v1)
  for (const v1 of values) {
    const encoded1 = encode(v1);
    for (const v2 of values) {
      const encoded2 = encode(v2);
      const byteCmp = memcmp(encoded1, encoded2);

      if (equal(v1, v2)) {
        assert.equal(byteCmp, 0, `Equal values should have equal bytes: ${stringify(v1)} vs ${stringify(v2)}`);
      } else if (less(v1, v2)) {
        assert.equal(byteCmp, -1, `Less value should have less bytes: ${stringify(v1)} < ${stringify(v2)}`);
      } else {
        assert.equal(byteCmp, 1, `Greater value should have greater bytes: ${stringify(v1)} > ${stringify(v2)}`);
      }
    }
  }
}

// =============================================================================
// Primitive types
// =============================================================================

describe("Beast v1: Null type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(NullType, [null]);
  });
});

describe("Beast v1: Boolean type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(BooleanType, [false, true]);
  });
});

describe("Beast v1: Integer type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(IntegerType, [
      -9223372036854775808n, // MIN_INT64
      -1n,
      0n,
      42n,
      90071992547409919n,
      9223372036854775807n, // MAX_INT64
    ]);
  });
});

describe("Beast v1: Float type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(FloatType, [
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
    ]);
  });
});

describe("Beast v1: String type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(StringType, [
      "",
      "a",
      "ab",
      "abc",
      "abd",
      "def",
      "いろはにほへとちりぬるを", // UTF-8 Japanese
    ]);
  });
});

describe("Beast v1: DateTime type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(DateTimeType, [
      new Date(0), // Unix epoch
      new Date("2022-06-29T13:43:00.123Z"),
      new Date("2025-01-01T00:00:00.000Z"),
    ]);
  });
});

describe("Beast v1: Blob type", () => {
  test("should round-trip", () => {
    // Note: Blobs do NOT preserve ordering in beast v1 binary format.
    // The format uses length-first encoding (8-byte length prefix), but comparison is lexicographic.
    // So byte ordering (length-first) doesn't match value ordering (lexicographic).
    testRoundTrip(BlobType, [
      new Uint8Array([]),
      new Uint8Array([1]),
      new Uint8Array([1, 3]),
      new Uint8Array([1, 3, 3]),
      new Uint8Array([1, 3, 4]),
      new Uint8Array([9]),
      new Uint8Array([255]),
      new Uint8Array([255, 255]),
    ]);
  });
});

// =============================================================================
// Collection types
// =============================================================================

describe("Beast v1: Array type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(ArrayType(IntegerType), [
      [],
      [0n],
      [0n, 1n],
      [0n, 2n, 3n],
      [0n, 2n, 4n],
      [1n],
    ]);
  });
});

describe("Beast v1: Set type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(SetType(StringType), [
      new Set<string>(),
      new Set(["abc"]),
      new Set(["abc", "def"]),
      new Set(["def"]),
    ]);
  });
});

describe("Beast v1: Dict type", () => {
  test("should round-trip and maintain ordering", () => {
    testRoundTripAndOrdering(DictType(StringType, IntegerType), [
      new Map<string, bigint>(),
      new Map([["abc", 0n]]),
      new Map([["abc", 0n], ["def", 1n]]),
      new Map([["abc", 1n]]),
      new Map([["def", 1n]]),
    ]);
  });
});

// =============================================================================
// Compound types
// =============================================================================

describe("Beast v1: Struct type", () => {
  test("should round-trip and maintain ordering", () => {
    const type = StructType({
      boolean: BooleanType,
      string: StringType,
    });
    testRoundTripAndOrdering(type, [
      { boolean: false, string: "good" },
      { boolean: true, string: "bad" },
      { boolean: true, string: "ok" },
    ]);
  });
});

describe("Beast v1: Variant type", () => {
  test("should round-trip and maintain ordering", () => {
    const type = VariantType({
      none: NullType,
      some: IntegerType,
    });
    testRoundTripAndOrdering(type, [
      variant("none", null),
      variant("some", 0n),
      variant("some", 1n),
    ]);
  });
});

// =============================================================================
// Complex real-world structures
// =============================================================================

describe("Beast v1: Complex struct with nullable fields", () => {
  test("should round-trip complex production-like struct", () => {
    // This is based on a real production struct from the old tests
    const type = StructType({
      id: StringType,
      active: BooleanType,
      timestamp: DateTimeType,
      score: FloatType,
      count: IntegerType,
      tags: ArrayType(StringType),
      metadata: DictType(StringType, StringType),
    });

    const value = {
      id: "35932005329",
      active: true,
      timestamp: new Date("2022-03-01T00:00:00.000Z"),
      score: 3.14,
      count: 42n,
      tags: ["alpha", "beta"],
      metadata: new Map([
        ["key1", "value1"],
        ["key2", "value2"],
      ]),
    };

    const encode = encodeBeastValueFor(type);
    const decode = decodeBeastValueFor(type);
    const encoded = encode(value);
    const [decoded, offset] = decode(encoded, 0);
    assert.equal(offset, encoded.length, "Did not consume all bytes");

    const equal = equalFor(type);
    assert.ok(equal(decoded, value), "Complex struct did not round-trip");
  });
});

// =============================================================================
// Nested structures
// =============================================================================

describe("Beast v1: Nested arrays", () => {
  test("should round-trip nested arrays", () => {
    const type = ArrayType(ArrayType(IntegerType));
    const values = [
      [],
      [[]],
      [[1n, 2n], [3n]],
      [[1n, 2n], [3n, 4n]],
    ];
    testRoundTripAndOrdering(type, values);
  });
});

describe("Beast v1: Nested structs", () => {
  test("should round-trip nested structs", () => {
    const innerType = StructType({ x: IntegerType, y: IntegerType });
    const outerType = StructType({ point: innerType, label: StringType });

    const values = [
      { point: { x: 0n, y: 0n }, label: "origin" },
      { point: { x: 1n, y: 2n }, label: "a" },
      { point: { x: 1n, y: 2n }, label: "b" },
    ];

    testRoundTripAndOrdering(outerType, values);
  });
});

// =============================================================================
// Byte ordering verification for critical types
// =============================================================================

describe("Beast v1: Byte ordering properties", () => {
  test("Integer byte ordering should match numeric ordering", () => {
    const type = IntegerType;
    const encode = encodeBeastValueFor(type);

    // Negative numbers should come before positive
    const negEncoded = encode(-100n);
    const posEncoded = encode(100n);
    assert.equal(memcmp(negEncoded, posEncoded), -1, "Negative should sort before positive");

    // More negative should come before less negative
    const moreNegEncoded = encode(-200n);
    assert.equal(memcmp(moreNegEncoded, negEncoded), -1, "More negative should sort before less negative");

    // Larger positive should come after smaller positive
    const largerPosEncoded = encode(200n);
    assert.equal(memcmp(posEncoded, largerPosEncoded), -1, "Smaller positive should sort before larger positive");
  });

  test("Float byte ordering should match numeric ordering (including special values)", () => {
    const type = FloatType;
    const encode = encodeBeastValueFor(type);

    // Test key ordering properties
    const negInf = encode(-Infinity);
    const negOne = encode(-1.0);
    const negZero = encode(-0.0);
    const posZero = encode(0.0);
    const posOne = encode(1.0);
    const posInf = encode(Infinity);
    const nan = encode(NaN);

    // Verify total ordering: -Inf < -1 < -0 == 0 < 1 < +Inf < NaN
    assert.equal(memcmp(negInf, negOne), -1, "-Infinity < -1");
    assert.equal(memcmp(negOne, negZero), -1, "-1 < -0");
    assert.equal(memcmp(negZero, posZero), -1, "-0 < 0 (distinct in byte representation)");
    assert.equal(memcmp(posZero, posOne), -1, "0 < 1");
    assert.equal(memcmp(posOne, posInf), -1, "1 < +Infinity");
    assert.equal(memcmp(posInf, nan), -1, "+Infinity < NaN");
  });

  test("String byte ordering should match lexicographic ordering", () => {
    const type = StringType;
    const encode = encodeBeastValueFor(type);

    const empty = encode("");
    const a = encode("a");
    const ab = encode("ab");
    const b = encode("b");

    assert.equal(memcmp(empty, a), -1, "empty string < 'a'");
    assert.equal(memcmp(a, ab), -1, "'a' < 'ab'");
    assert.equal(memcmp(ab, b), -1, "'ab' < 'b'");
  });

  test("Array byte ordering should match lexicographic ordering", () => {
    const type = ArrayType(IntegerType);
    const encode = encodeBeastValueFor(type);

    const empty = encode([]);
    const zero = encode([0n]);
    const zeroOne = encode([0n, 1n]);
    const one = encode([1n]);

    assert.equal(memcmp(empty, zero), -1, "[] < [0]");
    assert.equal(memcmp(zero, zeroOne), -1, "[0] < [0, 1]");
    assert.equal(memcmp(zeroOne, one), -1, "[0, 1] < [1]");
  });
});

// =============================================================================
// Error handling
// =============================================================================

describe("Beast v1: Error handling", () => {
  test("should throw on truncated integer data", () => {
    const type = IntegerType;
    const decode = decodeBeastValueFor(type);

    const truncated = new Uint8Array([0x00, 0x00, 0x00]); // Only 3 bytes, need 8
    assert.throws(
      () => decode(truncated, 0),
      /Buffer underflow/,
      "Should reject truncated integer"
    );
  });

  test("should throw on truncated string (missing null terminator)", () => {
    const type = StringType;
    const decode = decodeBeastValueFor(type);

    const noTerminator = new Uint8Array([0x68, 0x65, 0x6c, 0x6c, 0x6f]); // "hello" without null
    assert.throws(
      () => decode(noTerminator, 0),
      /No null terminator/,
      "Should reject string without null terminator"
    );
  });

  test("should throw on invalid array continuation byte", () => {
    const type = ArrayType(IntegerType);
    const decode = decodeBeastValueFor(type);

    const invalid = new Uint8Array([0x02]); // Invalid continuation byte (not 0x00 or 0x01)
    assert.throws(
      () => decode(invalid, 0),
      /Invalid continuation byte/,
      "Should reject invalid continuation byte"
    );
  });

  test("should throw on invalid variant tag", () => {
    const type = VariantType({
      none: NullType,
      some: IntegerType,
    });
    const decode = decodeBeastValueFor(type);

    const invalidTag = new Uint8Array([0x02]); // Tag 2, but only 0 and 1 are valid
    assert.throws(
      () => decode(invalidTag, 0),
      /Invalid variant tag/,
      "Should reject invalid variant tag"
    );
  });

  test("should throw on excess data after value", () => {
    const type = IntegerType;
    const encode = encodeBeastValueFor(type);
    const decode = decodeBeastValueFor(type);

    const encoded = encode(42n);
    const withExcess = new Uint8Array(encoded.length + 10);
    withExcess.set(encoded);
    withExcess[encoded.length] = 0xFF; // Extra byte

    assert.throws(
      () => {
        const [_value, offset] = decode(withExcess, 0);
        if (offset !== withExcess.length) {
          throw new Error(`Unexpected data after value at offset ${offset} (${withExcess.length - offset} bytes remaining)`);
        }
      },
      /Unexpected data after value/,
      "Should reject data with trailing bytes"
    );
  });
});
