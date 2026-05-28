/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { BufferWriter, readVarint, readZigzag, readFloat64LE, readStringUtf8Varint } from "./binary-utils.js";

// =============================================================================
// Varint tests
// =============================================================================

describe("Varint encoding/decoding", () => {
  test("varint(0) should be 1 byte: 0x00", () => {
    const writer = new BufferWriter(16);
    writer.writeVarint(0);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 1);
    assert.equal(bytes[0], 0x00);

    const [value, offset] = readVarint(bytes, 0);
    assert.equal(value, 0);
    assert.equal(offset, 1);
  });

  test("varint(127) should be 1 byte: 0x7F", () => {
    const writer = new BufferWriter(16);
    writer.writeVarint(127);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 1);
    assert.equal(bytes[0], 0x7F);

    const [value, _offset] = readVarint(bytes, 0);
    assert.equal(value, 127);
  });

  test("varint(128) should be 2 bytes: 0x80 0x01", () => {
    const writer = new BufferWriter(16);
    writer.writeVarint(128);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 2);
    assert.equal(bytes[0], 0x80);
    assert.equal(bytes[1], 0x01);

    const [value, offset] = readVarint(bytes, 0);
    assert.equal(value, 128);
    assert.equal(offset, 2);
  });

  test("varint(300) should round-trip", () => {
    const writer = new BufferWriter(16);
    writer.writeVarint(300);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 2);

    const [value, _offset] = readVarint(bytes, 0);
    assert.equal(value, 300);
  });

  test("varint(16383) should be 2 bytes", () => {
    const writer = new BufferWriter(16);
    writer.writeVarint(16383);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 2);

    const [value, _offset] = readVarint(bytes, 0);
    assert.equal(value, 16383);
  });

  test("varint(16384) should be 3 bytes", () => {
    const writer = new BufferWriter(16);
    writer.writeVarint(16384);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 3);

    const [value, _offset] = readVarint(bytes, 0);
    assert.equal(value, 16384);
  });

  test("varint(MAX_SAFE_INTEGER) should round-trip", () => {
    const writer = new BufferWriter(16);
    const large = Number.MAX_SAFE_INTEGER;
    writer.writeVarint(large);
    const bytes = writer.toUint8Array();

    const [value, _offset] = readVarint(bytes, 0);
    assert.equal(value, large);
  });

  test("writeVarint should reject negative numbers", () => {
    assert.throws(() => new BufferWriter(16).writeVarint(-1));
  });
});

// =============================================================================
// Zigzag tests
// =============================================================================

describe("Zigzag encoding/decoding", () => {
  test("zigzag(0) should be 1 byte: 0x00", () => {
    const writer = new BufferWriter(16);
    writer.writeZigzag(0n);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 1);
    assert.equal(bytes[0], 0x00);

    const [value, offset] = readZigzag(bytes, 0);
    assert.equal(value, 0n);
    assert.equal(offset, 1);
  });

  test("zigzag(-1) should be 1 byte: 0x01", () => {
    const writer = new BufferWriter(16);
    writer.writeZigzag(-1n);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 1);
    assert.equal(bytes[0], 0x01);

    const [value, _offset] = readZigzag(bytes, 0);
    assert.equal(value, -1n);
  });

  test("zigzag(1) should be 1 byte: 0x02", () => {
    const writer = new BufferWriter(16);
    writer.writeZigzag(1n);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 1);
    assert.equal(bytes[0], 0x02);

    const [value, _offset] = readZigzag(bytes, 0);
    assert.equal(value, 1n);
  });

  test("zigzag(-2) should be 1 byte: 0x03", () => {
    const writer = new BufferWriter(16);
    writer.writeZigzag(-2n);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 1);
    assert.equal(bytes[0], 0x03);

    const [value, _offset] = readZigzag(bytes, 0);
    assert.equal(value, -2n);
  });

  test("zigzag(2) should round-trip", () => {
    const writer = new BufferWriter(16);
    writer.writeZigzag(2n);
    const bytes = writer.toUint8Array();

    const [value, _offset] = readZigzag(bytes, 0);
    assert.equal(value, 2n);
  });

  test("zigzag(-128) should round-trip", () => {
    const writer = new BufferWriter(16);
    writer.writeZigzag(-128n);
    const bytes = writer.toUint8Array();

    const [value, _offset] = readZigzag(bytes, 0);
    assert.equal(value, -128n);
  });

  test("zigzag(max int64) should round-trip", () => {
    const writer = new BufferWriter(16);
    const large = 9223372036854775807n; // max int64
    writer.writeZigzag(large);
    const bytes = writer.toUint8Array();

    const [value, _offset] = readZigzag(bytes, 0);
    assert.equal(value, large);
  });

  test("zigzag(min int64) should round-trip", () => {
    const writer = new BufferWriter(16);
    const large = -9223372036854775808n; // min int64
    writer.writeZigzag(large);
    const bytes = writer.toUint8Array();

    const [value, _offset] = readZigzag(bytes, 0);
    assert.equal(value, large);
  });
});

// =============================================================================
// Float64 tests
// =============================================================================

describe("Float64 encoding/decoding", () => {
  test("float64(0.0) should be 8 bytes", () => {
    const writer = new BufferWriter(16);
    writer.writeFloat64LE(0.0);
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 8);

    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    const value = readFloat64LE(view, 0);
    assert.equal(value, 0.0);
  });

  test("float64(3.14) should round-trip approximately", () => {
    const writer = new BufferWriter(16);
    writer.writeFloat64LE(3.14);
    const bytes = writer.toUint8Array();

    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    const value = readFloat64LE(view, 0);
    assert.ok(Math.abs(value - 3.14) < 0.0001);
  });

  test("float64(-1.5) should round-trip", () => {
    const writer = new BufferWriter(16);
    writer.writeFloat64LE(-1.5);
    const bytes = writer.toUint8Array();

    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    const value = readFloat64LE(view, 0);
    assert.equal(value, -1.5);
  });

  test("float64(Infinity) should round-trip", () => {
    const writer = new BufferWriter(16);
    writer.writeFloat64LE(Infinity);
    const bytes = writer.toUint8Array();

    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    const value = readFloat64LE(view, 0);
    assert.equal(value, Infinity);
  });

  test("float64(-Infinity) should round-trip", () => {
    const writer = new BufferWriter(16);
    writer.writeFloat64LE(-Infinity);
    const bytes = writer.toUint8Array();

    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    const value = readFloat64LE(view, 0);
    assert.equal(value, -Infinity);
  });

  test("float64(NaN) should encode as canonical NaN", () => {
    const writer = new BufferWriter(16);
    writer.writeFloat64LE(NaN);
    const bytes = writer.toUint8Array();

    // Check canonical NaN encoding (0x7FF8000000000000 in little-endian)
    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    const bits = view.getBigUint64(0, true); // little-endian
    assert.equal(bits, 0x7ff8000000000000n);

    const value = readFloat64LE(view, 0);
    assert.ok(Number.isNaN(value));
  });

  test("readFloat64 should reject non-canonical NaN", () => {
    const bytes = new Uint8Array(8);
    const view = new DataView(bytes.buffer);
    view.setBigUint64(0, 0x7ff0000000000001n, true); // signaling NaN (little-endian)

    assert.throws(() => readFloat64LE(view, 0));
  });
});

// =============================================================================
// UTF-8 string tests
// =============================================================================

describe("UTF-8 string encoding/decoding", () => {
  test("empty string should be 1 byte (varint 0)", () => {
    const writer = new BufferWriter(16);
    writer.writeStringUtf8Varint("");
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 1);
    assert.equal(bytes[0], 0x00);

    const [str, offset] = readStringUtf8Varint(bytes, 0);
    assert.equal(str, "");
    assert.equal(offset, 1);
  });

  test("'hello' should be 6 bytes (1 length + 5 ASCII)", () => {
    const writer = new BufferWriter(16);
    writer.writeStringUtf8Varint("hello");
    const bytes = writer.toUint8Array();
    assert.equal(bytes.length, 6);
    assert.equal(bytes[0], 5);

    const [str, offset] = readStringUtf8Varint(bytes, 0);
    assert.equal(str, "hello");
    assert.equal(offset, 6);
  });

  test("Japanese characters should round-trip", () => {
    const writer = new BufferWriter(32);
    const input = "いろは"; // 3 Japanese characters
    writer.writeStringUtf8Varint(input);
    const bytes = writer.toUint8Array();

    const [str, _offset] = readStringUtf8Varint(bytes, 0);
    assert.equal(str, input);
  });

  test("mixed ASCII, CJK, emoji should round-trip", () => {
    const writer = new BufferWriter(32);
    const input = "Hello 世界 🌍"; // mix of ASCII, CJK, emoji
    writer.writeStringUtf8Varint(input);
    const bytes = writer.toUint8Array();

    const [str, _offset] = readStringUtf8Varint(bytes, 0);
    assert.equal(str, input);
  });
});

// =============================================================================
// BufferWriter auto-resize tests
// =============================================================================

describe("BufferWriter auto-resize", () => {
  test("should auto-resize for varint", () => {
    const writer = new BufferWriter(4); // very small initial capacity
    writer.writeVarint(1000); // should trigger resize
    const bytes = writer.toUint8Array();

    const [value, _offset] = readVarint(bytes, 0);
    assert.equal(value, 1000);
  });

  test("should auto-resize for strings", () => {
    const writer = new BufferWriter(4);
    writer.writeStringUtf8Varint("this is a longer string that exceeds initial capacity");
    const bytes = writer.toUint8Array();

    const [str, _offset] = readStringUtf8Varint(bytes, 0);
    assert.equal(str, "this is a longer string that exceeds initial capacity");
  });

  test("should grow beyond initial capacity for many writes", () => {
    const writer = new BufferWriter(4);
    for (let i = 0; i < 100; i++) {
      writer.writeVarint(i);
    }
    const bytes = writer.toUint8Array();
    assert.ok(bytes.length > 4);
  });
});
