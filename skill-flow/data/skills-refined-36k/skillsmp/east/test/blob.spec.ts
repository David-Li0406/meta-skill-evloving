/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import {
  East,
  Expr,
  NullType, BooleanType, IntegerType, FloatType, StringType, DateTimeType, BlobType,
  ArrayType, SetType, DictType, StructType, VariantType,
  variant,
  RecursiveType,
  ref,
  RefType,
} from "../src/index.js";
import { describeEast as describe, assertEast as assert } from "./platforms.spec.js";

await describe("Blob", (test) => {
  test("Array ops", $ => {
    $(assert.equal(East.value(Uint8Array.from([]), BlobType).size(), 0n));
    $(assert.equal(East.value(Uint8Array.from([1, 2, 3])).size(), 3n));
    $(assert.equal(East.value(Uint8Array.from([1, 2, 3])).getUint8(0n), 1n));
  });

  test("UTF-8 decoding/encoding", $ => {
    const hello_str = $.let(East.value("Hello", StringType));
    const hello_blob = $.let(East.value(Uint8Array.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]), BlobType));

    $(assert.equal(hello_str.encodeUtf8(), hello_blob));
    $(assert.equal(hello_blob.decodeUtf8(), hello_str));

    const invalid_utf8_blob = $.let(East.value(Uint8Array.from([0xff, 0xfe, 0xfd]), BlobType));

    $(assert.throws(invalid_utf8_blob.decodeUtf8()));
  });

  test("UTF-16 decoding/encoding", $ => {
    // Basic round-trip
    const hello_str = $.let(East.value("Hello", StringType));
    const hello_utf16_blob = $.let(East.value(
      Uint8Array.from([
        0xFF, 0xFE,       // BOM (LE)
        0x48, 0x00,       // 'H'
        0x65, 0x00,       // 'e'
        0x6C, 0x00,       // 'l'
        0x6C, 0x00,       // 'l'
        0x6F, 0x00,       // 'o'
      ]),
      BlobType
    ));

    $(assert.equal(hello_str.encodeUtf16(), hello_utf16_blob));
    $(assert.equal(hello_utf16_blob.decodeUtf16(), hello_str));

    // Emoji with surrogate pairs
    const emoji_str = $.let(East.value("A😀B", StringType));
    const emoji_utf16_blob = $.let(East.value(
      Uint8Array.from([
        0xFF, 0xFE,       // BOM (LE)
        0x41, 0x00,       // 'A'
        0x3D, 0xD8,       // high surrogate for 😀
        0x00, 0xDE,       // low surrogate for 😀
        0x42, 0x00,       // 'B'
      ]),
      BlobType
    ));

    $(assert.equal(emoji_str.encodeUtf16(), emoji_utf16_blob));
    $(assert.equal(emoji_utf16_blob.decodeUtf16(), emoji_str));

    // UTF-16 BE with BOM (auto-detect)
    const hello_be_blob = $.let(East.value(
      Uint8Array.from([
        0xFE, 0xFF,       // BOM (BE)
        0x00, 0x48,       // 'H'
        0x00, 0x65,       // 'e'
        0x00, 0x6C,       // 'l'
        0x00, 0x6C,       // 'l'
        0x00, 0x6F,       // 'o'
      ]),
      BlobType
    ));

    $(assert.equal(hello_be_blob.decodeUtf16(), hello_str));

    // UTF-16 LE without BOM (defaults to LE)
    const hello_no_bom_blob = $.let(East.value(
      Uint8Array.from([
        0x48, 0x00,       // 'H'
        0x65, 0x00,       // 'e'
        0x6C, 0x00,       // 'l'
        0x6C, 0x00,       // 'l'
        0x6F, 0x00,       // 'o'
      ]),
      BlobType
    ));

    $(assert.equal(hello_no_bom_blob.decodeUtf16(), hello_str));
  });

  // =========================================================================
  // Beast v1 - Primitive Types
  // =========================================================================

  test("Beast v1 - Null type", $ => {
    const value = $.let(East.value(null, NullType));
    const encoded = $.let(East.Blob.encodeBeast(value, 'v1'));

    // Exact byte verification
    const expected = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      8  // Null type tag
    ]), BlobType));
    $(assert.equal(encoded, expected));

    // Round-trip
    const decoded = $.let(encoded.decodeBeast(NullType, 'v1'));
    $(assert.equal(decoded, value));
  });

  test("Beast v1 - Boolean type", $ => {
    // Test false
    const falseVal = $.let(East.value(false, BooleanType));
    const encodedFalse = $.let(East.Blob.encodeBeast(falseVal, 'v1'));

    // Exact byte verification
    const expectedFalse = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      2,  // Boolean type tag
      0   // false
    ]), BlobType));
    $(assert.equal(encodedFalse, expectedFalse));

    // Round-trip
    const decodedFalse = $.let(encodedFalse.decodeBeast(BooleanType, 'v1'));
    $(assert.equal(decodedFalse, falseVal));

    // Test true
    const trueVal = $.let(East.value(true, BooleanType));
    const encodedTrue = $.let(East.Blob.encodeBeast(trueVal, 'v1'));

    // Exact byte verification
    const expectedTrue = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      2,  // Boolean type tag
      1   // true
    ]), BlobType));
    $(assert.equal(encodedTrue, expectedTrue));

    // Round-trip
    const decodedTrue = $.let(encodedTrue.decodeBeast(BooleanType, 'v1'));
    $(assert.equal(decodedTrue, trueVal));
  });

  test("Beast v1 - Integer type - basic values", $ => {
    // Zero
    const zero = $.let(East.value(0n, IntegerType));
    const encodedZero = $.let(East.Blob.encodeBeast(zero, 'v1'));

    // Exact byte verification
    const expectedZero = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      6, // Integer type tag
      128, 0, 0, 0, 0, 0, 0, 0 // sign-flipped 0
    ]), BlobType));
    $(assert.equal(encodedZero, expectedZero));

    // Round-trip
    const decodedZero = $.let(encodedZero.decodeBeast(IntegerType, 'v1'));
    $(assert.equal(decodedZero, zero));

    // Positive: 42
    const pos42 = $.let(East.value(42n, IntegerType));
    const encodedPos = $.let(East.Blob.encodeBeast(pos42, 'v1'));

    // Exact byte verification
    const expectedPos = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      6, // Integer type tag
      128, 0, 0, 0, 0, 0, 0, 42 // sign-flipped 42
    ]), BlobType));
    $(assert.equal(encodedPos, expectedPos));

    // Round-trip
    const decodedPos = $.let(encodedPos.decodeBeast(IntegerType, 'v1'));
    $(assert.equal(decodedPos, pos42));

    // Negative: -1
    const neg1 = $.let(East.value(-1n, IntegerType));
    const encodedNeg = $.let(East.Blob.encodeBeast(neg1, 'v1'));

    // Exact byte verification
    const expectedNeg = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      6, // Integer type tag
      127, 255, 255, 255, 255, 255, 255, 255 // sign-flipped -1
    ]), BlobType));
    $(assert.equal(encodedNeg, expectedNeg));

    // Round-trip
    const decodedNeg = $.let(encodedNeg.decodeBeast(IntegerType, 'v1'));
    $(assert.equal(decodedNeg, neg1));
  });

  test("Beast v1 - Integer type - boundary values", $ => {
    // Max int64: 9223372036854775807
    const maxInt = $.let(East.value(9223372036854775807n, IntegerType));
    const encodedMax = $.let(East.Blob.encodeBeast(maxInt, 'v1'));

    // Exact byte verification
    const expectedMax = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      6, // Integer type tag
      255, 255, 255, 255, 255, 255, 255, 255 // sign-flipped MAX
    ]), BlobType));
    $(assert.equal(encodedMax, expectedMax));

    // Round-trip
    const decodedMax = $.let(encodedMax.decodeBeast(IntegerType, 'v1'));
    $(assert.equal(decodedMax, maxInt));

    // Min int64: -9223372036854775808
    const minInt = $.let(East.value(-9223372036854775808n, IntegerType));
    const encodedMin = $.let(East.Blob.encodeBeast(minInt, 'v1'));

    // Exact byte verification
    const expectedMin = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      6, // Integer type tag
      0, 0, 0, 0, 0, 0, 0, 0 // sign-flipped MIN
    ]), BlobType));
    $(assert.equal(encodedMin, expectedMin));

    // Round-trip
    const decodedMin = $.let(encodedMin.decodeBeast(IntegerType, 'v1'));
    $(assert.equal(decodedMin, minInt));
  });

  test("Beast v1 - Float type - basic values", $ => {
    // Zero (positive)
    const zero = $.let(East.value(0.0, FloatType));
    const encodedZero = $.let(East.Blob.encodeBeast(zero, 'v1'));

    // Exact byte verification
    const expectedZero = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      5, // Float type tag
      128, 0, 0, 0, 0, 0, 0, 0 // sorted 0.0
    ]), BlobType));
    $(assert.equal(encodedZero, expectedZero));

    // Round-trip
    const decodedZero = $.let(encodedZero.decodeBeast(FloatType, 'v1'));
    $(assert.equal(decodedZero, zero));

    // Common value: 3.14
    const pi = $.let(East.value(3.14, FloatType));
    const encodedPi = $.let(East.Blob.encodeBeast(pi, 'v1'));

    // Exact byte verification
    const expectedPi = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      5, // Float type tag
      192, 9, 30, 184, 81, 235, 133, 31 // sorted 3.14
    ]), BlobType));
    $(assert.equal(encodedPi, expectedPi));

    // Round-trip
    const decodedPi = $.let(encodedPi.decodeBeast(FloatType, 'v1'));
    $(assert.equal(decodedPi, pi));

    // Negative: -1.5
    const negVal = $.let(East.value(-1.5, FloatType));
    const encodedNeg = $.let(East.Blob.encodeBeast(negVal, 'v1'));

    // Exact byte verification
    const expectedNeg = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      5, // Float type tag
      64, 7, 255, 255, 255, 255, 255, 255 // sorted -1.5
    ]), BlobType));
    $(assert.equal(encodedNeg, expectedNeg));

    // Round-trip
    const decodedNeg = $.let(encodedNeg.decodeBeast(FloatType, 'v1'));
    $(assert.equal(decodedNeg, negVal));
  });

  test("Beast v1 - Float type - special values", $ => {
    // Negative infinity
    const negInf = $.let(East.value(-Infinity, FloatType));
    const encodedNegInf = $.let(East.Blob.encodeBeast(negInf, 'v1'));

    // Exact byte verification
    const expectedNegInf = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      5, // Float type tag
      0, 15, 255, 255, 255, 255, 255, 255 // sorted -Infinity
    ]), BlobType));
    $(assert.equal(encodedNegInf, expectedNegInf));

    // Round-trip
    const decodedNegInf = $.let(encodedNegInf.decodeBeast(FloatType, 'v1'));
    $(assert.equal(decodedNegInf, negInf));

    // Positive infinity
    const posInf = $.let(East.value(Infinity, FloatType));
    const encodedPosInf = $.let(East.Blob.encodeBeast(posInf, 'v1'));

    // Exact byte verification
    const expectedPosInf = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      5, // Float type tag
      255, 240, 0, 0, 0, 0, 0, 0 // sorted Infinity
    ]), BlobType));
    $(assert.equal(encodedPosInf, expectedPosInf));

    // Round-trip
    const decodedPosInf = $.let(encodedPosInf.decodeBeast(FloatType, 'v1'));
    $(assert.equal(decodedPosInf, posInf));

    // NaN
    const nanVal = $.let(East.value(NaN, FloatType));
    const encodedNaN = $.let(East.Blob.encodeBeast(nanVal, 'v1'));

    // Exact byte verification
    const expectedNaN = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      5, // Float type tag
      255, 248, 0, 0, 0, 0, 0, 0 // sorted NaN
    ]), BlobType));
    $(assert.equal(encodedNaN, expectedNaN));

    // Round-trip
    const decodedNaN = $.let(encodedNaN.decodeBeast(FloatType, 'v1'));
    $(assert.equal(decodedNaN, nanVal));
  });

  test("Beast v1 - String type", $ => {
    // Empty string
    const empty = $.let(East.value("", StringType));
    const encodedEmpty = $.let(East.Blob.encodeBeast(empty, 'v1'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      10, // String type tag
      0 // null terminator
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(StringType, 'v1'));
    $(assert.equal(decodedEmpty, empty));

    // ASCII string: "hello"
    const hello = $.let(East.value("hello", StringType));
    const encodedHello = $.let(East.Blob.encodeBeast(hello, 'v1'));

    // Exact byte verification
    const expectedHello = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      10, // String type tag
      104, 101, 108, 108, 111, 0 // 'hello' + null terminator
    ]), BlobType));
    $(assert.equal(encodedHello, expectedHello));

    // Round-trip
    const decodedHello = $.let(encodedHello.decodeBeast(StringType, 'v1'));
    $(assert.equal(decodedHello, hello));

    // Unicode string
    const unicode = $.let(East.value("Hello 世界", StringType));
    const encodedUnicode = $.let(East.Blob.encodeBeast(unicode, 'v1'));

    // Exact byte verification
    const expectedUnicode = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      10, // String type tag
      72, 101, 108, 108, 111, 32, 228, 184, 150, 231, 149, 140, 0 // 'Hello 世界' + null
    ]), BlobType));
    $(assert.equal(encodedUnicode, expectedUnicode));

    // Round-trip
    const decodedUnicode = $.let(encodedUnicode.decodeBeast(StringType, 'v1'));
    $(assert.equal(decodedUnicode, unicode));

    // Emoji
    const emoji = $.let(East.value("😀", StringType));
    const encodedEmoji = $.let(East.Blob.encodeBeast(emoji, 'v1'));

    // Exact byte verification
    const expectedEmoji = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      10, // String type tag
      240, 159, 152, 128, 0 // '😀' + null
    ]), BlobType));
    $(assert.equal(encodedEmoji, expectedEmoji));

    // Round-trip
    const decodedEmoji = $.let(encodedEmoji.decodeBeast(StringType, 'v1'));
    $(assert.equal(decodedEmoji, emoji));
  });

  test("Beast v1 - DateTime type", $ => {
    // Unix epoch
    const epoch = $.let(East.value(new Date(0), DateTimeType));
    const encodedEpoch = $.let(East.Blob.encodeBeast(epoch, 'v1'));

    // Exact byte verification
    const expectedEpoch = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      3, // DateTime type tag
      128, 0, 0, 0, 0, 0, 0, 0 // sign-flipped epoch (0 ms)
    ]), BlobType));
    $(assert.equal(encodedEpoch, expectedEpoch));

    // Round-trip
    const decodedEpoch = $.let(encodedEpoch.decodeBeast(DateTimeType, 'v1'));
    $(assert.equal(decodedEpoch, epoch));

    // Specific date with milliseconds: 2024-01-15T10:30:00.123Z
    const specificDate = $.let(East.value(new Date("2024-01-15T10:30:00.123Z"), DateTimeType));
    const encodedDate = $.let(East.Blob.encodeBeast(specificDate, 'v1'));

    // Exact byte verification
    const expectedDate = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      3, // DateTime type tag
      128, 0, 1, 141, 12, 171, 196, 187 // sign-flipped timestamp
    ]), BlobType));
    $(assert.equal(encodedDate, expectedDate));

    // Round-trip
    const decodedDate = $.let(encodedDate.decodeBeast(DateTimeType, 'v1'));
    $(assert.equal(decodedDate, specificDate));
  });

  test("Beast v1 - Blob type", $ => {
    // Empty blob
    const empty = $.let(East.value(new Uint8Array([]), BlobType));
    const encodedEmpty = $.let(East.Blob.encodeBeast(empty, 'v1'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      1, // Blob type tag
      0, 0, 0, 0, 0, 0, 0, 0 // 8-byte big-endian length (0)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(BlobType, 'v1'));
    $(assert.equal(decodedEmpty, empty));

    // Small blob
    const small = $.let(East.value(new Uint8Array([1, 2, 3, 4, 5]), BlobType));
    const encodedSmall = $.let(East.Blob.encodeBeast(small, 'v1'));

    // Exact byte verification
    const expectedSmall = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      1, // Blob type tag
      0, 0, 0, 0, 0, 0, 0, 5, // 8-byte big-endian length (5)
      1, 2, 3, 4, 5 // blob data
    ]), BlobType));
    $(assert.equal(encodedSmall, expectedSmall));

    // Round-trip
    const decodedSmall = $.let(encodedSmall.decodeBeast(BlobType, 'v1'));
    $(assert.equal(decodedSmall, small));
  });

  // =========================================================================
  // Beast v1 - Collection Types
  // =========================================================================

  test("Beast v1 - Array type", $ => {
    // Empty array
    const emptyArray = $.let(East.value([], ArrayType(IntegerType)));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptyArray, 'v1'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      0, // Array type tag
      6, // Integer element type tag
      0  // terminator (empty array)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(ArrayType(IntegerType), 'v1'));
    $(assert.equal(decodedEmpty, emptyArray));

    // Integer array [1, 2, 3]
    const intArray = $.let(East.value([1n, 2n, 3n], ArrayType(IntegerType)));
    const encodedInt = $.let(East.Blob.encodeBeast(intArray, 'v1'));

    // Exact byte verification
    const expectedInt = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      0, // Array type tag
      6, // Integer element type tag
      1, 128, 0, 0, 0, 0, 0, 0, 1, // continuation + first element (1)
      1, 128, 0, 0, 0, 0, 0, 0, 2, // continuation + second element (2)
      1, 128, 0, 0, 0, 0, 0, 0, 3, // continuation + third element (3)
      0  // terminator
    ]), BlobType));
    $(assert.equal(encodedInt, expectedInt));

    // Round-trip
    const decodedInt = $.let(encodedInt.decodeBeast(ArrayType(IntegerType), 'v1'));
    $(assert.equal(decodedInt, intArray));

    // String array ["foo", "bar"]
    const strArray = $.let(East.value(["foo", "bar"], ArrayType(StringType)));
    const encodedStr = $.let(East.Blob.encodeBeast(strArray, 'v1'));

    // Exact byte verification
    const expectedStr = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      0, // Array type tag
      10, // String element type tag
      1, 102, 111, 111, 0, // continuation + 'foo' + null
      1, 98, 97, 114, 0,   // continuation + 'bar' + null
      0  // terminator
    ]), BlobType));
    $(assert.equal(encodedStr, expectedStr));

    // Round-trip
    const decodedStr = $.let(encodedStr.decodeBeast(ArrayType(StringType), 'v1'));
    $(assert.equal(decodedStr, strArray));
  });

  test("Beast v1 - Set type", $ => {
    // Empty set
    const emptySet = $.let(East.value(new Set([]), SetType(IntegerType)));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptySet, 'v1'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      9, // Set type tag
      6, // Integer element type tag
      0  // terminator (empty set)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(SetType(IntegerType), 'v1'));
    $(assert.equal(decodedEmpty, emptySet));

    // Integer set {1, 2, 3}
    const intSet = $.let(East.value(new Set([1n, 2n, 3n]), SetType(IntegerType)));
    const encodedInt = $.let(East.Blob.encodeBeast(intSet, 'v1'));

    // Exact byte verification
    const expectedInt = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      9, // Set type tag
      6, // Integer element type tag
      1, 128, 0, 0, 0, 0, 0, 0, 1, // continuation + first element (1)
      1, 128, 0, 0, 0, 0, 0, 0, 2, // continuation + second element (2)
      1, 128, 0, 0, 0, 0, 0, 0, 3, // continuation + third element (3)
      0  // terminator
    ]), BlobType));
    $(assert.equal(encodedInt, expectedInt));

    // Round-trip
    const decodedInt = $.let(encodedInt.decodeBeast(SetType(IntegerType), 'v1'));
    $(assert.equal(decodedInt, intSet));

    // String set {"foo", "bar", "baz"} - sorted as "bar", "baz", "foo"
    const strSet = $.let(East.value(new Set(["foo", "bar", "baz"]), SetType(StringType)));
    const encodedStr = $.let(East.Blob.encodeBeast(strSet, 'v1'));

    // Exact byte verification (sorted order: bar, baz, foo)
    const expectedStr = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      9, // Set type tag
      10, // String element type tag
      1, 98, 97, 114, 0,   // continuation + 'bar' + null (sorted first)
      1, 98, 97, 122, 0,   // continuation + 'baz' + null
      1, 102, 111, 111, 0, // continuation + 'foo' + null (sorted last)
      0  // terminator
    ]), BlobType));
    $(assert.equal(encodedStr, expectedStr));

    // Round-trip
    const decodedStr = $.let(encodedStr.decodeBeast(SetType(StringType), 'v1'));
    $(assert.equal(decodedStr, strSet));
  });

  test("Beast v1 - Dict type", $ => {
    // Empty dict
    const emptyDict = $.let(East.value(new Map(), DictType(StringType, IntegerType)));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptyDict, 'v1'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      4, // Dict type tag
      10, // String key type tag
      6, // Integer value type tag
      0  // terminator (empty dict)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(DictType(StringType, IntegerType), 'v1'));
    $(assert.equal(decodedEmpty, emptyDict));

    // String to integer dict {"a": 1, "b": 2}
    const dict = $.let(East.value(
      new Map([["a", 1n], ["b", 2n]]),
      DictType(StringType, IntegerType)
    ));
    const encodedDict = $.let(East.Blob.encodeBeast(dict, 'v1'));

    // Exact byte verification
    const expectedDict = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      4, // Dict type tag
      10, // String key type tag
      6, // Integer value type tag
      1, 97, 0, 128, 0, 0, 0, 0, 0, 0, 1, // continuation + key "a" + value 1
      1, 98, 0, 128, 0, 0, 0, 0, 0, 0, 2, // continuation + key "b" + value 2
      0  // terminator
    ]), BlobType));
    $(assert.equal(encodedDict, expectedDict));

    // Round-trip
    const decodedDict = $.let(encodedDict.decodeBeast(DictType(StringType, IntegerType), 'v1'));
    $(assert.equal(decodedDict, dict));
  });

  // =========================================================================
  // Beast v1 - Compound Types
  // =========================================================================

  test("Beast v1 - Struct type", $ => {
    // Empty struct
    const emptyStruct = $.let(East.value({}, StructType({})));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptyStruct, 'v1'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      11, // Struct type tag
      0   // terminator (empty struct)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(StructType({}), 'v1'));
    $(assert.equal(decodedEmpty, emptyStruct));

    // Simple struct with primitives: {name: "Alice", age: 30, active: true}
    const PersonType = StructType({
      name: StringType,
      age: IntegerType,
      active: BooleanType,
    });

    const person = $.let(East.value({
      name: "Alice",
      age: 30n,
      active: true,
    }, PersonType));

    const encoded = $.let(East.Blob.encodeBeast(person, 'v1'));

    // Exact byte verification (fields sorted alphabetically: active, age, name)
    const expectedPerson = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      11, // Struct type tag
      1, 110, 97, 109, 101, 0, 10, // continuation + "name" + String type
      1, 97, 103, 101, 0, 6,       // continuation + "age" + Integer type
      1, 97, 99, 116, 105, 118, 101, 0, 2, // continuation + "active" + Boolean type
      0,  // terminator for field definitions
      65, 108, 105, 99, 101, 0,    // "Alice" + null
      128, 0, 0, 0, 0, 0, 0, 30,   // 30 (sign-flipped)
      1   // true
    ]), BlobType));
    $(assert.equal(encoded, expectedPerson));

    // Round-trip
    const decoded = $.let(encoded.decodeBeast(PersonType, 'v1'));
    $(assert.equal(decoded.name, person.name));
    $(assert.equal(decoded.age, person.age));
    $(assert.equal(decoded.active, person.active));
  });

  test("Beast v1 - Variant type", $ => {
    const OptionType = VariantType({
      none: NullType,
      some: IntegerType,
    });

    // None case
    const noneVal = $.let(variant("none", null), OptionType);
    const encodedNone = $.let(East.Blob.encodeBeast(noneVal, 'v1'));

    // Exact byte verification
    const expectedNone = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      13, // Variant type tag
      1, 110, 111, 110, 101, 0, 8, // continuation + "none" + Null type
      1, 115, 111, 109, 101, 0, 6, // continuation + "some" + Integer type
      0,  // terminator for case definitions
      0   // tag index (0 = "none")
    ]), BlobType));
    $(assert.equal(encodedNone, expectedNone));

    // Round-trip
    const decodedNone = $.let(encodedNone.decodeBeast(OptionType, 'v1'));
    $(assert.equal(decodedNone, noneVal));

    // Some case
    const someVal = $.let(variant("some", 42n), OptionType);
    const encodedSome = $.let(East.Blob.encodeBeast(someVal, 'v1'));

    // Exact byte verification
    const expectedSome = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      13, // Variant type tag
      1, 110, 111, 110, 101, 0, 8, // continuation + "none" + Null type
      1, 115, 111, 109, 101, 0, 6, // continuation + "some" + Integer type
      0,  // terminator for case definitions
      1,  // tag index (1 = "some")
      128, 0, 0, 0, 0, 0, 0, 42 // value: 42 (sign-flipped)
    ]), BlobType));
    $(assert.equal(encodedSome, expectedSome));

    // Round-trip
    const decodedSome = $.let(encodedSome.decodeBeast(OptionType, 'v1'));
    $(assert.equal(decodedSome, someVal));

    // Variant with struct
    const ShapeType = VariantType({
      circle: StructType({ radius: FloatType }),
      rectangle: StructType({ width: FloatType, height: FloatType }),
    });

    const circle = $.let(variant("circle", { radius: 5.0 }), ShapeType);
    const encodedCircle = $.let(East.Blob.encodeBeast(circle, 'v1'));

    // Round-trip
    const decodedCircle = $.let(encodedCircle.decodeBeast(ShapeType, 'v1'));
    $(assert.equal(decodedCircle, circle));
  });

  // =========================================================================
  // Beast v1 - Complex Nested Structures
  // =========================================================================

  test("Beast v1 - Complex production-like struct", $ => {
    const RecordType = StructType({
      id: StringType,
      active: BooleanType,
      timestamp: DateTimeType,
      score: FloatType,
      count: IntegerType,
      tags: ArrayType(StringType),
      metadata: DictType(StringType, StringType),
    });

    const record = $.let(East.value({
      id: "rec-12345",
      active: true,
      timestamp: new Date("2024-01-15T10:30:00.000Z"),
      score: 95.5,
      count: 42n,
      tags: ["important", "verified"],
      metadata: new Map([["source", "api"], ["version", "2.0"]]),
    }, RecordType));

    const encoded = $.let(East.Blob.encodeBeast(record, 'v1'));

    // Exact byte verification
    const expected = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      11, // Struct type tag
      // Field definitions (sorted: active, count, id, metadata, score, tags, timestamp)
      1, 105, 100, 0, 10, // "id" + String type
      1, 97, 99, 116, 105, 118, 101, 0, 2, // "active" + Boolean type
      1, 116, 105, 109, 101, 115, 116, 97, 109, 112, 0, 3, // "timestamp" + DateTime type
      1, 115, 99, 111, 114, 101, 0, 5, // "score" + Float type
      1, 99, 111, 117, 110, 116, 0, 6, // "count" + Integer type
      1, 116, 97, 103, 115, 0, 0, 10, // "tags" + Array<String> type
      1, 109, 101, 116, 97, 100, 97, 116, 97, 0, 4, 10, 10, // "metadata" + Dict<String,String> type
      0, // terminator
      // Field values
      114, 101, 99, 45, 49, 50, 51, 52, 53, 0, // "rec-12345"
      1, // true
      128, 0, 1, 141, 12, 171, 196, 64, // timestamp
      192, 87, 224, 0, 0, 0, 0, 0, // 95.5
      128, 0, 0, 0, 0, 0, 0, 42, // 42
      1, 105, 109, 112, 111, 114, 116, 97, 110, 116, 0, // "important"
      1, 118, 101, 114, 105, 102, 105, 101, 100, 0, // "verified"
      0, // terminator
      1, 115, 111, 117, 114, 99, 101, 0, 97, 112, 105, 0, // "source" -> "api"
      1, 118, 101, 114, 115, 105, 111, 110, 0, 50, 46, 48, 0, // "version" -> "2.0"
      0 // terminator
    ]), BlobType));
    $(assert.equal(encoded, expected));

    // Round-trip
    const decoded = $.let(encoded.decodeBeast(RecordType, 'v1'));
    $(assert.equal(decoded.id, record.id));
    $(assert.equal(decoded.active, record.active));
    $(assert.equal(decoded.timestamp, record.timestamp));
    $(assert.equal(decoded.score, record.score));
    $(assert.equal(decoded.count, record.count));
    $(assert.equal(decoded.tags, record.tags));
    $(assert.equal(decoded.metadata, record.metadata));
  });

  test("Beast v1 - Deeply nested structures", $ => {
    // Array of dicts of arrays
    const deepType = ArrayType(DictType(StringType, ArrayType(IntegerType)));
    const deepValue = $.let(East.value([
      new Map([["a", [1n, 2n]], ["b", [3n]]]),
      new Map([["c", []]]),
    ], deepType));

    const encoded = $.let(East.Blob.encodeBeast(deepValue, 'v1'));

    // Exact byte verification
    const expected = $.let(East.value(new Uint8Array([
      69, 97, 115, 116, 0, 234, 87, 255, // v1 header
      0, // Array type tag
      4, 10, 0, 6, // Dict<String, Array<Integer>> type
      // First dict: {"a": [1, 2], "b": [3]}
      1, // continuation
      1, 97, 0, // key "a"
      1, 128, 0, 0, 0, 0, 0, 0, 1, // value: array element 1
      1, 128, 0, 0, 0, 0, 0, 0, 2, // value: array element 2
      0, // array terminator
      1, 98, 0, // key "b"
      1, 128, 0, 0, 0, 0, 0, 0, 3, // value: array element 3
      0, // array terminator
      0, // dict terminator
      // Second dict: {"c": []}
      1, // continuation
      1, 99, 0, // key "c"
      0, // empty array terminator
      0, // dict terminator
      0  // array terminator
    ]), BlobType));
    $(assert.equal(encoded, expected));

    // Round-trip
    const decoded = $.let(encoded.decodeBeast(deepType, 'v1'));
    $(assert.equal(decoded, deepValue));
  });

  // =========================================================================
  // Beast v1 - Error Handling
  // =========================================================================

  test("Beast v1 - Error handling - wrong type", $ => {
    const value = $.let(East.value(42n, IntegerType));
    const encoded = $.let(East.Blob.encodeBeast(value, 'v1'));

    // Try to decode integer as string
    $(assert.throws(encoded.decodeBeast(StringType, 'v1')));
  });

  test("Beast v1 - Error handling - invalid continuation byte", $ => {
    // Manually create array with invalid continuation byte (not 0x00 or 0x01)
    const invalidArray = $.let(East.value(new Uint8Array([0x02]), BlobType));

    $(assert.throws(invalidArray.decodeBeast(ArrayType(IntegerType), 'v1')));
  });

  test("Beast v1 - Error handling - invalid variant tag", $ => {
    const OptionType = VariantType({
      none: NullType,
      some: IntegerType,
    });

    // Create blob with invalid tag (2, but only 0 and 1 are valid)
    const invalidVariant = $.let(East.value(
      new Uint8Array([0x02, 0x00]),
      BlobType
    ));

    $(assert.throws(invalidVariant.decodeBeast(OptionType, 'v1')));
  });

  // =========================================================================
  // Beast v2 - Primitive Types
  // =========================================================================

  test("Beast v2 - Magic bytes verification", $ => {
    const value = $.let(East.value(42n, IntegerType));
    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));

    // Verify magic bytes: [0x89, 0x45, 0x61, 0x73, 0x74, 0x0D, 0x0A, 0x01]
    $(assert.equal(encoded.getUint8(0n), 0x89n)); // PNG-style magic byte
    $(assert.equal(encoded.getUint8(1n), 0x45n)); // 'E'
    $(assert.equal(encoded.getUint8(2n), 0x61n)); // 'a'
    $(assert.equal(encoded.getUint8(3n), 0x73n)); // 's'
    $(assert.equal(encoded.getUint8(4n), 0x74n)); // 't'
    $(assert.equal(encoded.getUint8(5n), 0x0Dn)); // CR
    $(assert.equal(encoded.getUint8(6n), 0x0An)); // LF
    $(assert.equal(encoded.getUint8(7n), 0x01n)); // version 1
  });

  test("Beast v2 - Null type", $ => {
    const value = $.let(East.value(null, NullType));
    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));

    // Exact byte verification
    const expected = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      10 // Null type tag
    ]), BlobType));
    $(assert.equal(encoded, expected));

    // Round-trip
    const decoded = $.let(encoded.decodeBeast(NullType, 'v2'));
    $(assert.equal(decoded, value));
  });

  test("Beast v2 - Boolean type", $ => {
    // Test false
    const falseVal = $.let(East.value(false, BooleanType));
    const encodedFalse = $.let(East.Blob.encodeBeast(falseVal, 'v2'));

    // Exact byte verification
    const expectedFalse = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      3,  // Boolean type tag
      0   // false
    ]), BlobType));
    $(assert.equal(encodedFalse, expectedFalse));

    // Round-trip
    const decodedFalse = $.let(encodedFalse.decodeBeast(BooleanType, 'v2'));
    $(assert.equal(decodedFalse, falseVal));

    // Test true
    const trueVal = $.let(East.value(true, BooleanType));
    const encodedTrue = $.let(East.Blob.encodeBeast(trueVal, 'v2'));

    // Exact byte verification
    const expectedTrue = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      3,  // Boolean type tag
      1   // true
    ]), BlobType));
    $(assert.equal(encodedTrue, expectedTrue));

    // Round-trip
    const decodedTrue = $.let(encodedTrue.decodeBeast(BooleanType, 'v2'));
    $(assert.equal(decodedTrue, trueVal));
  });

  test("Beast v2 - Integer type - zigzag encoding", $ => {
    // Zero (should be 1 byte varint)
    const zero = $.let(East.value(0n, IntegerType));
    const encodedZero = $.let(East.Blob.encodeBeast(zero, 'v2'));

    // Exact byte verification
    const expectedZero = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      8, // Integer type tag
      0  // zigzag(0) = 0
    ]), BlobType));
    $(assert.equal(encodedZero, expectedZero));

    // Round-trip
    const decodedZero = $.let(encodedZero.decodeBeast(IntegerType, 'v2'));
    $(assert.equal(decodedZero, zero));

    // -1 (zigzag encoded as 1)
    const neg1 = $.let(East.value(-1n, IntegerType));
    const encodedNeg1 = $.let(East.Blob.encodeBeast(neg1, 'v2'));

    // Exact byte verification
    const expectedNeg1 = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      8, // Integer type tag
      1  // zigzag(-1) = 1
    ]), BlobType));
    $(assert.equal(encodedNeg1, expectedNeg1));

    // Round-trip
    const decodedNeg1 = $.let(encodedNeg1.decodeBeast(IntegerType, 'v2'));
    $(assert.equal(decodedNeg1, neg1));

    // 1 (zigzag encoded as 2)
    const pos1 = $.let(East.value(1n, IntegerType));
    const encodedPos1 = $.let(East.Blob.encodeBeast(pos1, 'v2'));

    // Exact byte verification
    const expectedPos1 = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      8, // Integer type tag
      2  // zigzag(1) = 2
    ]), BlobType));
    $(assert.equal(encodedPos1, expectedPos1));

    // Round-trip
    const decodedPos1 = $.let(encodedPos1.decodeBeast(IntegerType, 'v2'));
    $(assert.equal(decodedPos1, pos1));

    // 42 (zigzag encoded as 84)
    const pos42 = $.let(East.value(42n, IntegerType));
    const encodedPos42 = $.let(East.Blob.encodeBeast(pos42, 'v2'));

    // Exact byte verification
    const expectedPos42 = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      8,  // Integer type tag
      84  // zigzag(42) = 84
    ]), BlobType));
    $(assert.equal(encodedPos42, expectedPos42));

    // Round-trip
    const decodedPos42 = $.let(encodedPos42.decodeBeast(IntegerType, 'v2'));
    $(assert.equal(decodedPos42, pos42));
  });

  test("Beast v2 - Integer type - boundary values", $ => {
    // Max int64
    const maxInt = $.let(East.value(9223372036854775807n, IntegerType));
    const encodedMax = $.let(East.Blob.encodeBeast(maxInt, 'v2'));

    // Exact byte verification
    const expectedMax = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      8, // Integer type tag
      254, 255, 255, 255, 255, 255, 255, 255, 255, 1 // zigzag(MAX) varint
    ]), BlobType));
    $(assert.equal(encodedMax, expectedMax));

    // Round-trip
    const decodedMax = $.let(encodedMax.decodeBeast(IntegerType, 'v2'));
    $(assert.equal(decodedMax, maxInt));

    // Min int64
    const minInt = $.let(East.value(-9223372036854775808n, IntegerType));
    const encodedMin = $.let(East.Blob.encodeBeast(minInt, 'v2'));

    // Exact byte verification
    const expectedMin = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      8, // Integer type tag
      255, 255, 255, 255, 255, 255, 255, 255, 255, 1 // zigzag(MIN) varint
    ]), BlobType));
    $(assert.equal(encodedMin, expectedMin));

    // Round-trip
    const decodedMin = $.let(encodedMin.decodeBeast(IntegerType, 'v2'));
    $(assert.equal(decodedMin, minInt));
  });

  test("Beast v2 - Float type", $ => {
    // Zero
    const zero = $.let(East.value(0.0, FloatType));
    const encodedZero = $.let(East.Blob.encodeBeast(zero, 'v2'));

    // Exact byte verification
    const expectedZero = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      6, // Float type tag
      0, 0, 0, 0, 0, 0, 0, 0 // 0.0 (little-endian IEEE 754)
    ]), BlobType));
    $(assert.equal(encodedZero, expectedZero));

    // Round-trip
    const decodedZero = $.let(encodedZero.decodeBeast(FloatType, 'v2'));
    $(assert.equal(decodedZero, zero));

    // 3.14
    const pi = $.let(East.value(3.14, FloatType));
    const encodedPi = $.let(East.Blob.encodeBeast(pi, 'v2'));

    // Exact byte verification
    const expectedPi = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      6, // Float type tag
      31, 133, 235, 81, 184, 30, 9, 64 // 3.14 (little-endian IEEE 754)
    ]), BlobType));
    $(assert.equal(encodedPi, expectedPi));

    // Round-trip
    const decodedPi = $.let(encodedPi.decodeBeast(FloatType, 'v2'));
    $(assert.equal(decodedPi, pi));

    // -Infinity
    const negInf = $.let(East.value(-Infinity, FloatType));
    const encodedNegInf = $.let(East.Blob.encodeBeast(negInf, 'v2'));

    // Exact byte verification
    const expectedNegInf = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      6, // Float type tag
      0, 0, 0, 0, 0, 0, 240, 255 // -Infinity (little-endian IEEE 754)
    ]), BlobType));
    $(assert.equal(encodedNegInf, expectedNegInf));

    // Round-trip
    const decodedNegInf = $.let(encodedNegInf.decodeBeast(FloatType, 'v2'));
    $(assert.equal(decodedNegInf, negInf));

    // Infinity
    const posInf = $.let(East.value(Infinity, FloatType));
    const encodedPosInf = $.let(East.Blob.encodeBeast(posInf, 'v2'));

    // Exact byte verification
    const expectedPosInf = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      6, // Float type tag
      0, 0, 0, 0, 0, 0, 240, 127 // Infinity (little-endian IEEE 754)
    ]), BlobType));
    $(assert.equal(encodedPosInf, expectedPosInf));

    // Round-trip
    const decodedPosInf = $.let(encodedPosInf.decodeBeast(FloatType, 'v2'));
    $(assert.equal(decodedPosInf, posInf));

    // NaN
    const nanVal = $.let(East.value(NaN, FloatType));
    const encodedNaN = $.let(East.Blob.encodeBeast(nanVal, 'v2'));

    // Exact byte verification
    const expectedNaN = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      6, // Float type tag
      0, 0, 0, 0, 0, 0, 248, 127 // NaN (little-endian IEEE 754)
    ]), BlobType));
    $(assert.equal(encodedNaN, expectedNaN));

    // Round-trip
    const decodedNaN = $.let(encodedNaN.decodeBeast(FloatType, 'v2'));
    $(assert.equal(decodedNaN, nanVal));
  });

  test("Beast v2 - String type", $ => {
    // Empty string
    const empty = $.let(East.value("", StringType));
    const encodedEmpty = $.let(East.Blob.encodeBeast(empty, 'v2'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      14, // String type tag
      0   // length varint (0)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(StringType, 'v2'));
    $(assert.equal(decodedEmpty, empty));

    // ASCII string: "hello"
    const hello = $.let(East.value("hello", StringType));
    const encodedHello = $.let(East.Blob.encodeBeast(hello, 'v2'));

    // Exact byte verification
    const expectedHello = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      14, // String type tag
      5,  // length varint (5)
      104, 101, 108, 108, 111 // 'hello' UTF-8
    ]), BlobType));
    $(assert.equal(encodedHello, expectedHello));

    // Round-trip
    const decodedHello = $.let(encodedHello.decodeBeast(StringType, 'v2'));
    $(assert.equal(decodedHello, hello));

    // Unicode: "Hello 世界"
    const unicode = $.let(East.value("Hello 世界", StringType));
    const encodedUnicode = $.let(East.Blob.encodeBeast(unicode, 'v2'));

    // Exact byte verification
    const expectedUnicode = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      14, // String type tag
      12, // length varint (12 UTF-8 bytes)
      72, 101, 108, 108, 111, 32, 228, 184, 150, 231, 149, 140 // 'Hello 世界' UTF-8
    ]), BlobType));
    $(assert.equal(encodedUnicode, expectedUnicode));

    // Round-trip
    const decodedUnicode = $.let(encodedUnicode.decodeBeast(StringType, 'v2'));
    $(assert.equal(decodedUnicode, unicode));

    // Emoji: "😀"
    const emoji = $.let(East.value("😀", StringType));
    const encodedEmoji = $.let(East.Blob.encodeBeast(emoji, 'v2'));

    // Exact byte verification
    const expectedEmoji = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      14, // String type tag
      4,  // length varint (4 UTF-8 bytes)
      240, 159, 152, 128 // '😀' UTF-8
    ]), BlobType));
    $(assert.equal(encodedEmoji, expectedEmoji));

    // Round-trip
    const decodedEmoji = $.let(encodedEmoji.decodeBeast(StringType, 'v2'));
    $(assert.equal(decodedEmoji, emoji));
  });

  test("Beast v2 - DateTime type", $ => {
    // Unix epoch
    const epoch = $.let(East.value(new Date(0), DateTimeType));
    const encodedEpoch = $.let(East.Blob.encodeBeast(epoch, 'v2'));

    // Exact byte verification
    const expectedEpoch = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      4, // DateTime type tag
      0  // zigzag(0) = 0
    ]), BlobType));
    $(assert.equal(encodedEpoch, expectedEpoch));

    // Round-trip
    const decodedEpoch = $.let(encodedEpoch.decodeBeast(DateTimeType, 'v2'));
    $(assert.equal(decodedEpoch, epoch));

    // Specific date: 2025-10-14T00:00:00.000Z
    const specificDate = $.let(East.value(new Date("2025-10-14T00:00:00.000Z"), DateTimeType));
    const encodedDate = $.let(East.Blob.encodeBeast(specificDate, 'v2'));

    // Exact byte verification
    const expectedDate = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      4, // DateTime type tag
      128, 144, 162, 128, 188, 102 // zigzag-encoded timestamp varint
    ]), BlobType));
    $(assert.equal(encodedDate, expectedDate));

    // Round-trip
    const decodedDate = $.let(encodedDate.decodeBeast(DateTimeType, 'v2'));
    $(assert.equal(decodedDate, specificDate));
  });

  test("Beast v2 - Blob type", $ => {
    // Empty blob
    const empty = $.let(East.value(new Uint8Array([]), BlobType));
    const encodedEmpty = $.let(East.Blob.encodeBeast(empty, 'v2'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      2, // Blob type tag
      0  // length varint (0)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(BlobType, 'v2'));
    $(assert.equal(decodedEmpty, empty));

    // Small blob [1, 2, 3, 4, 5]
    const small = $.let(East.value(new Uint8Array([1, 2, 3, 4, 5]), BlobType));
    const encodedSmall = $.let(East.Blob.encodeBeast(small, 'v2'));

    // Exact byte verification
    const expectedSmall = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      2, // Blob type tag
      5, // length varint (5)
      1, 2, 3, 4, 5 // blob data
    ]), BlobType));
    $(assert.equal(encodedSmall, expectedSmall));

    // Round-trip
    const decodedSmall = $.let(encodedSmall.decodeBeast(BlobType, 'v2'));
    $(assert.equal(decodedSmall, small));
  });

  // =========================================================================
  // Beast v2 - Collection Types
  // =========================================================================

  test("Beast v2 - Ref type", $ => {
    // Integer ref &1
    const intRef = $.let(East.value(ref(42n), RefType(IntegerType)));
    const encodedInt = $.let(East.Blob.encodeBeast(intRef, 'v2'));

    // Exact byte verification
    const expectedInt = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      12, // Ref type tag
      8, // Integer element type tag
      0, // inline marker varint(0)
      84, // zigzag(42)=84
    ]), BlobType));
    $(assert.equal(encodedInt, expectedInt));

    // Round-trip
    const decodedInt = $.let(encodedInt.decodeBeast(RefType(IntegerType), 'v2'));
    $(assert.equal(decodedInt, intRef));

    // String ref ["foo", "bar"]
    const strRef = $.let(East.value(ref("foo"), RefType(StringType)));
    const encodedStr = $.let(East.Blob.encodeBeast(strRef, 'v2'));

    // Exact byte verification
    const expectedStr = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      12, // Ref type tag
      14, // String element type tag
      0,  // inline marker varint(0)
      3, 102, 111, 111, // length(3) + 'foo'
    ]), BlobType));
    $(assert.equal(encodedStr, expectedStr));

    // Round-trip
    const decodedStr = $.let(encodedStr.decodeBeast(RefType(StringType), 'v2'));
    $(assert.equal(decodedStr, strRef));
  });

  test("Beast v2 - Array type", $ => {
    // Empty array
    const emptyArray = $.let(East.value([], ArrayType(IntegerType)));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptyArray, 'v2'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      0, // Array type tag
      8, // Integer element type tag
      0, // inline marker varint(0)
      0  // length varint (0)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(ArrayType(IntegerType), 'v2'));
    $(assert.equal(decodedEmpty, emptyArray));

    // Integer array [1, 2, 3]
    const intArray = $.let(East.value([1n, 2n, 3n], ArrayType(IntegerType)));
    const encodedInt = $.let(East.Blob.encodeBeast(intArray, 'v2'));

    // Exact byte verification
    const expectedInt = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      0, // Array type tag
      8, // Integer element type tag
      0, // inline marker varint(0)
      3, // length varint (3)
      2, 4, 6 // zigzag(1)=2, zigzag(2)=4, zigzag(3)=6
    ]), BlobType));
    $(assert.equal(encodedInt, expectedInt));

    // Round-trip
    const decodedInt = $.let(encodedInt.decodeBeast(ArrayType(IntegerType), 'v2'));
    $(assert.equal(decodedInt, intArray));

    // String array ["foo", "bar"]
    const strArray = $.let(East.value(["foo", "bar"], ArrayType(StringType)));
    const encodedStr = $.let(East.Blob.encodeBeast(strArray, 'v2'));

    // Exact byte verification
    const expectedStr = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      0,  // Array type tag
      14, // String element type tag
      0,  // inline marker varint(0)
      2,  // length varint (2)
      3, 102, 111, 111, // length(3) + 'foo'
      3, 98, 97, 114    // length(3) + 'bar'
    ]), BlobType));
    $(assert.equal(encodedStr, expectedStr));

    // Round-trip
    const decodedStr = $.let(encodedStr.decodeBeast(ArrayType(StringType), 'v2'));
    $(assert.equal(decodedStr, strArray));
  });

  test("Beast v2 - Set type", $ => {
    // Empty set
    const emptySet = $.let(East.value(new Set([]), SetType(IntegerType)));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptySet, 'v2'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      13, // Set type tag
      8,  // Integer element type tag
      0,  // inline marker varint(0)
      0   // length varint (0)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(SetType(IntegerType), 'v2'));
    $(assert.equal(decodedEmpty, emptySet));

    // Integer set {1, 2, 3}
    const intSet = $.let(East.value(new Set([1n, 2n, 3n]), SetType(IntegerType)));
    const encodedInt = $.let(East.Blob.encodeBeast(intSet, 'v2'));

    // Exact byte verification
    const expectedInt = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      13, // Set type tag
      8,  // Integer element type tag
      0,  // inline marker varint(0)
      3,  // length varint (3)
      2, 4, 6 // zigzag(1)=2, zigzag(2)=4, zigzag(3)=6
    ]), BlobType));
    $(assert.equal(encodedInt, expectedInt));

    // Round-trip
    const decodedInt = $.let(encodedInt.decodeBeast(SetType(IntegerType), 'v2'));
    $(assert.equal(decodedInt, intSet));

    // String set {"foo", "bar", "baz"} - sorted as "bar", "baz", "foo"
    const strSet = $.let(East.value(new Set(["foo", "bar", "baz"]), SetType(StringType)));
    const encodedStr = $.let(East.Blob.encodeBeast(strSet, 'v2'));

    // Exact byte verification (sorted order: bar, baz, foo)
    const expectedStr = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      13, // Set type tag
      14, // String element type tag
      0,  // inline marker varint(0)
      3,  // length varint (3)
      3, 98, 97, 114,   // length(3) + 'bar' (sorted first)
      3, 98, 97, 122,   // length(3) + 'baz'
      3, 102, 111, 111  // length(3) + 'foo' (sorted last)
    ]), BlobType));
    $(assert.equal(encodedStr, expectedStr));

    // Round-trip
    const decodedStr = $.let(encodedStr.decodeBeast(SetType(StringType), 'v2'));
    $(assert.equal(decodedStr, strSet));
  });

  test("Beast v2 - Dict type", $ => {
    // Empty dict
    const emptyDict = $.let(East.value(new Map(), DictType(StringType, IntegerType)));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptyDict, 'v2'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      5,  // Dict type tag
      14, // String key type tag
      8,  // Integer value type tag
      0,  // inline marker varint(0)
      0   // length varint (0)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(DictType(StringType, IntegerType), 'v2'));
    $(assert.equal(decodedEmpty, emptyDict));

    // String to integer dict {"a": 1, "b": 2}
    const dict = $.let(East.value(
      new Map([["a", 1n], ["b", 2n]]),
      DictType(StringType, IntegerType)
    ));
    const encodedDict = $.let(East.Blob.encodeBeast(dict, 'v2'));

    // Exact byte verification
    const expectedDict = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      5,  // Dict type tag
      14, // String key type tag
      8,  // Integer value type tag
      0,  // inline marker varint(0)
      2,  // length varint (2 entries)
      1, 97, // key: length(1) + 'a'
      2,     // value: zigzag(1) = 2
      1, 98, // key: length(1) + 'b'
      4      // value: zigzag(2) = 4
    ]), BlobType));
    $(assert.equal(encodedDict, expectedDict));

    // Round-trip
    const decodedDict = $.let(encodedDict.decodeBeast(DictType(StringType, IntegerType), 'v2'));
    $(assert.equal(decodedDict, dict));
  });

  // =========================================================================
  // Beast v2 - Compound Types
  // =========================================================================

  test("Beast v2 - Struct type", $ => {
    // Empty struct
    const emptyStruct = $.let(East.value({}, StructType({})));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptyStruct, 'v2'));

    // Exact byte verification
    const expectedEmpty = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      15, // Struct type tag
      0,  // inline marker
      0,  // field count varint (0)
    ]), BlobType));
    $(assert.equal(encodedEmpty, expectedEmpty));

    // Round-trip
    const decodedEmpty = $.let(encodedEmpty.decodeBeast(StructType({}), 'v2'));
    $(assert.equal(decodedEmpty, emptyStruct));

    // Simple struct: {name: "Bob", age: 25, active: false}
    const PersonType = StructType({
      name: StringType,
      age: IntegerType,
      active: BooleanType,
    });

    const person = $.let(East.value({
      name: "Bob",
      age: 25n,
      active: false,
    }, PersonType));

    const encoded = $.let(East.Blob.encodeBeast(person, 'v2'));

    // Exact byte verification (fields sorted: active, age, name)
    const expectedPerson = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      15, // Struct type tag
      0,  // inline marker
      3,  // field count varint (3)
      4, 110, 97, 109, 101, 14, // field: length(4) + 'name' + String type
      3, 97, 103, 101, 8,       // field: length(3) + 'age' + Integer type
      6, 97, 99, 116, 105, 118, 101, 3, // field: length(6) + 'active' + Boolean type
      3, 66, 111, 98, // value: name = length(3) + 'Bob'
      50,             // value: age = zigzag(25) = 50
      0               // value: active = false
    ]), BlobType));
    $(assert.equal(encoded, expectedPerson));

    // Round-trip
    const decoded = $.let(encoded.decodeBeast(PersonType, 'v2'));
    $(assert.equal(decoded.name, person.name));
    $(assert.equal(decoded.age, person.age));
    $(assert.equal(decoded.active, person.active));
  });

  test("Beast v2 - Variant type", $ => {
    const OptionType = VariantType({
      none: NullType,
      some: IntegerType,
    });

    // None case
    const noneVal = $.let(variant("none", null), OptionType);
    const encodedNone = $.let(East.Blob.encodeBeast(noneVal, 'v2'));

    // Exact byte verification
    const expectedNone = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      16, // Variant type tag
      0,  // inline marker
      2,  // case count varint (2)
      4, 110, 111, 110, 101, 10, // case: length(4) + "none" + Null type
      4, 115, 111, 109, 101, 8, // case: length(4) + "some" + Integer type
      0   // tag index (0 = "none")
    ]), BlobType));
    $(assert.equal(encodedNone, expectedNone));

    // Round-trip
    const decodedNone = $.let(encodedNone.decodeBeast(OptionType, 'v2'));
    $(assert.equal(decodedNone, noneVal));

    // Some case
    const someVal = $.let(variant("some", 42n), OptionType);
    const encodedSome = $.let(East.Blob.encodeBeast(someVal, 'v2'));

    // Exact byte verification
    const expectedSome = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      16, // Variant type tag
      0,  // inline marker
      2,  // case count varint (2)
      4, 110, 111, 110, 101, 10, // case: length(4) + "none" + Null type
      4, 115, 111, 109, 101, 8,  // case: length(4) + "some" + Integer type
      1,  // tag index (1 = "some")
      84  // value: zigzag(42) = 84
    ]), BlobType));
    $(assert.equal(encodedSome, expectedSome));

    // Round-trip
    const decodedSome = $.let(encodedSome.decodeBeast(OptionType, 'v2'));
    $(assert.equal(decodedSome, someVal));

    // Variant with struct
    const ShapeType = VariantType({
      circle: StructType({ radius: FloatType }),
      rectangle: StructType({ width: FloatType, height: FloatType }),
    });

    const circle = $.let(variant("circle", { radius: 5.0 }), ShapeType);
    const encodedCircle = $.let(East.Blob.encodeBeast(circle, 'v2'));
    const decodedCircle = $.let(encodedCircle.decodeBeast(ShapeType, 'v2'));
    $(assert.equal(decodedCircle, circle));
  });

  // =========================================================================
  // Beast v2 - Complex Nested Structures
  // =========================================================================

  test("Beast v2 - Complex production-like struct", $ => {
    const RecordType = StructType({
      id: StringType,
      active: BooleanType,
      timestamp: DateTimeType,
      score: FloatType,
      count: IntegerType,
      tags: ArrayType(StringType),
      metadata: DictType(StringType, StringType),
    });

    const record = $.let(East.value({
      id: "rec-67890",
      active: false,
      timestamp: new Date("2025-01-15T10:30:00.000Z"),
      score: 87.3,
      count: 99n,
      tags: ["production", "critical"],
      metadata: new Map([["env", "prod"], ["region", "us-west"]]),
    }, RecordType));

    const encoded = $.let(East.Blob.encodeBeast(record, 'v2'));

    // Exact byte verification
    const expected = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      15, // Struct type tag
      0,  // inline marker
      7,  // field count varint (7)
      // Field definitions (sorted: active, count, id, metadata, score, tags, timestamp)
      2, 105, 100, 14, // "id" + String type
      6, 97, 99, 116, 105, 118, 101, 3, // "active" + Boolean type
      9, 116, 105, 109, 101, 115, 116, 97, 109, 112, 4, // "timestamp" + DateTime type
      5, 115, 99, 111, 114, 101, 6, // "score" + Float type
      5, 99, 111, 117, 110, 116, 8, // "count" + Integer type
      4, 116, 97, 103, 115, 0, 14, // "tags" + Array<String> type
      8, 109, 101, 116, 97, 100, 97, 116, 97, 5, 14, 14, // "metadata" + Dict<String,String> type
      // Field values
      9, 114, 101, 99, 45, 54, 55, 56, 57, 48, // "rec-67890"
      0, // false
      128, 177, 154, 152, 141, 101, // timestamp (zigzag varint)
      51, 51, 51, 51, 51, 211, 85, 64, // 87.3 (little-endian float)
      198, 1, // 99 (zigzag)
      0, // inline marker for Array value
      2, // array length (2)
      10, 112, 114, 111, 100, 117, 99, 116, 105, 111, 110, // "production"
      8, 99, 114, 105, 116, 105, 99, 97, 108, // "critical"
      0, // inline marker for Dict value
      2, // dict length (2)
      3, 101, 110, 118, 4, 112, 114, 111, 100, // "env" -> "prod"
      6, 114, 101, 103, 105, 111, 110, 7, 117, 115, 45, 119, 101, 115, 116 // "region" -> "us-west"
    ]), BlobType));
    $(assert.equal(encoded, expected));

    // Round-trip
    const decoded = $.let(encoded.decodeBeast(RecordType, 'v2'));
    $(assert.equal(decoded.id, record.id));
    $(assert.equal(decoded.active, record.active));
    $(assert.equal(decoded.timestamp, record.timestamp));
    $(assert.equal(decoded.score, record.score));
    $(assert.equal(decoded.count, record.count));
    $(assert.equal(decoded.tags, record.tags));
    $(assert.equal(decoded.metadata, record.metadata));
  });

  test("Beast v2 - Deeply nested structures", $ => {
    // Array of dicts of arrays
    const deepType = ArrayType(DictType(StringType, ArrayType(IntegerType)));
    const deepValue = $.let(East.value([
      new Map([["x", [10n, 20n]], ["y", [30n]]]),
      new Map([["z", []]]),
    ], deepType));

    const encoded = $.let(East.Blob.encodeBeast(deepValue, 'v2'));

    // Exact byte verification
    const expected = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes
      0, // Array type tag
      5, 14, 0, 8, // Dict<String, Array<Integer>> type
      0, // inline marker for outer Array value
      2, // array length (2 dicts)
      // First dict: {"x": [10, 20], "y": [30]}
      0, // inline marker for Dict value
      2, // dict length (2 entries)
      1, 120, // key "x" (length 1 + 'x')
      0, // inline marker for Array value
      2, // array length (2)
      20, 40, // zigzag(10)=20, zigzag(20)=40
      1, 121, // key "y" (length 1 + 'y')
      0, // inline marker for Array value
      1, // array length (1)
      60, // zigzag(30)=60
      // Second dict: {"z": []}
      0, // inline marker for Dict value
      1, // dict length (1 entry)
      1, 122, // key "z" (length 1 + 'z')
      0, // inline marker for Array value
      0 // array length (0)
    ]), BlobType));
    $(assert.equal(encoded, expected));

    // Round-trip
    const decoded = $.let(encoded.decodeBeast(deepType, 'v2'));
    $(assert.equal(decoded, deepValue));
  });

  // =========================================================================
  // Beast v2 - Recursive types
  // =========================================================================
  test("Beast v2 - Recursive types - Linked list", $ => {
    const LinkedListType = RecursiveType(self => VariantType({
        nil: NullType,
        cons: StructType({
            head: BooleanType,
            tail: self
        })
    }));

    // Create some test values and check they infer correctly
    // This is a mixture of wrapping JavaScript values and East Exprs to ensure both work
    const list0 = $.let(variant("nil"), LinkedListType);
    const list1 = $.let(variant("cons", { head: true, tail: list0 }), LinkedListType);
    const list2 = $.let(variant("cons", { head: false, tail: list1 }), LinkedListType);

    const encoded0 = $.let(East.Blob.encodeBeast(list0, 'v2'));
    const encoded1 = $.let(East.Blob.encodeBeast(list1, 'v2'));
    const encoded2 = $.let(East.Blob.encodeBeast(list2, 'v2'));

    // Exact byte verification
    const expected0 = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes

      16, // Variant type tag
        0, // inline marker
        2, // case count varint (2)
        4, 99, 111, 110, 115, 15, // case: length(4) + "cons" + Struct type
          0, // inline marker
          2, // field count varint (2)
          4, 104, 101, 97, 100, 3,  // field: length(4) + "head" + Boolean type
          4, 116, 97, 105, 108, 11, // field: length(4) + "tail" + RecursiveType
            4, // recursion depth zigzag (2)
        3, 110, 105, 108, 10, // case: length(4) + "nil" + Null type

      1, // tag index (0 = "nil")
    ]), BlobType));

    const expected1 = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes

      16, // Variant type tag
        0, // inline marker
        2, // case count varint (2)
        4, 99, 111, 110, 115, 15, // case: length(4) + "cons" + Struct type
          0, // inline marker
          2, // field count varint (2)
          4, 104, 101, 97, 100, 3,  // field: length(4) + "head" + Boolean type
          4, 116, 97, 105, 108, 11, // field: length(4) + "tail" + RecursiveType
            4, // recursion depth zigzag (2)
        3, 110, 105, 108, 10, // case: length(4) + "nil" + Null type

      0, // tag index (1 = "cons")
        1, // head = true
        1, // tail = tag index (0 = "nil")
    ]), BlobType));

    const expected2 = $.let(East.value(new Uint8Array([
      137, 69, 97, 115, 116, 13, 10, 1, // v2 magic bytes

      16, // Variant type tag
        0, // inline marker
        2, // case count varint (2)
        4, 99, 111, 110, 115, 15, // case: length(4) + "cons" + Struct type
          0, // inline marker
          2, // field count varint (2)
          4, 104, 101, 97, 100, 3,  // field: length(4) + "head" + Boolean type
          4, 116, 97, 105, 108, 11, // field: length(4) + "tail" + RecursiveType
            4, // recursion depth zigzag (2)
        3, 110, 105, 108, 10, // case: length(4) + "nil" + Null type

      0, // tag index (1 = "cons")
        0, // head = false
        0, // tag index (1 = "cons")
          1, // head = true
          1, // tail = tag index (0 = "nil")
    ]), BlobType));

    // 0x89456173740d0a01 0f000204636f6e730e0002046865616402047461696c0a04036e696c09 01
    // 0x89456173740d0a01 0f000204636f6e730d0002046865616402047461696c0902036e696c09 01

    $(assert.equal(encoded0, expected0));
    $(assert.equal(encoded1, expected1));
    $(assert.equal(encoded2, expected2));

    // Round-trip
    const decoded0 = $.let(encoded0.decodeBeast(LinkedListType, 'v2'));
    $(assert.equal(decoded0, list0));

    const decoded1 = $.let(encoded1.decodeBeast(LinkedListType, 'v2'));
    $(assert.equal(decoded1, list1));

    const decoded2 = $.let(encoded2.decodeBeast(LinkedListType, 'v2'));
    $(assert.equal(decoded2, list2));
  });

  // =========================================================================
  // Beast v2 - Error Handling
  // =========================================================================

  test("Beast v2 - Error handling - wrong type", $ => {
    const value = $.let(East.value(42n, IntegerType));
    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));

    // Try to decode integer as string
    $(assert.throws(encoded.decodeBeast(StringType, 'v2')));
  });

  test("Beast v2 - Error handling - invalid magic bytes", $ => {
    // Create blob with wrong magic bytes
    const invalidMagic = $.let(East.value(
      new Uint8Array([0x00, 0x45, 0x61, 0x73, 0x74, 0x0D, 0x0A, 0x01, 0x02, 0x00]),
      BlobType
    ));

    $(assert.throws(invalidMagic.decodeBeast(IntegerType, 'v2')));
  });

  test("Beast v2 - Error handling - wrong version", $ => {
    // Create blob with wrong version byte
    const wrongVersion = $.let(East.value(
      new Uint8Array([0x89, 0x45, 0x61, 0x73, 0x74, 0x0D, 0x0A, 0x02, 0x02, 0x00]),
      BlobType
    ));

    $(assert.throws(wrongVersion.decodeBeast(IntegerType, 'v2')));
  });

  test("Beast v2 - Error handling - invalid variant tag", $ => {
    const OptionType = VariantType({
      none: NullType,
      some: IntegerType,
    });

    // Create blob with v2 magic bytes + type tags + invalid variant tag (2, but only 0 and 1 are valid)
    // Format: 8 magic bytes + variant type tag + null type tag + invalid tag (0x02) + null value
    const invalidVariant = $.let(East.value(
      new Uint8Array([
        0x89, 0x45, 0x61, 0x73, 0x74, 0x0D, 0x0A, 0x01, // Magic bytes
        0x08, // Variant type tag
        0x00, // Null type tag (for simplified variant)
        0x02, // Invalid tag (only 0 and 1 are valid)
        0x00, // Null value
      ]),
      BlobType
    ));

    $(assert.throws(invalidVariant.decodeBeast(OptionType, 'v2')));
  });

  // =========================================================================
  // Cross-version Compatibility Tests
  // =========================================================================

  test("Beast v1 vs v2 are not compatible", $ => {
    const person = $.let(East.value({
      name: "Charlie",
      age: 35n,
      active: true,
    }));

    const PersonType = StructType({
      name: StringType,
      age: IntegerType,
      active: BooleanType,
    });

    // Encode with v1, try to decode with v2 (should fail)
    const v1_encoded = $.let(East.Blob.encodeBeast(person, 'v1'));
    $(assert.throws(v1_encoded.decodeBeast(PersonType, 'v2')));

    // Encode with v2, try to decode with v1 (should fail)
    const v2_encoded = $.let(East.Blob.encodeBeast(person, 'v2'));
    $(assert.throws(v2_encoded.decodeBeast(PersonType, 'v1')));
  });

  // =========================================================================
  // Beast v2 - Backreference Tests (Mutable Aliasing)
  // =========================================================================

  test("Beast v2 - Backreference - same array appearing twice", $ => {
    // Create a struct where both fields reference the same array
    const sharedArray = $.let(East.value([1n, 2n, 3n], ArrayType(IntegerType)));
    const structType = StructType({
      first: ArrayType(IntegerType),
      second: ArrayType(IntegerType),
    });
    const value = $.let({
      first: sharedArray,
      second: sharedArray,
    });

    // Encode and decode
    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));
    const decoded = $.let(encoded.decodeBeast(structType, 'v2'));

    // Values should be equal
    $(assert.equal(decoded.first, East.value([1n, 2n, 3n], ArrayType(IntegerType))));
    $(assert.equal(decoded.second, East.value([1n, 2n, 3n], ArrayType(IntegerType))));

    // Both should reference the same array (backreference preserved identity)
    $(assert.is(decoded.first, decoded.second));
  });

  test("Beast v2 - Backreference - same set appearing twice", $ => {
    const sharedSet = $.let(East.value(new Set(["a", "b", "c"]), SetType(StringType)));
    const structType = StructType({
      first: SetType(StringType),
      second: SetType(StringType),
    });
    const value = $.let({
      first: sharedSet,
      second: sharedSet,
    });

    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));
    const decoded = $.let(encoded.decodeBeast(structType, 'v2'));

    // Both should reference the same set
    $(assert.is(decoded.first, decoded.second));
  });

  test("Beast v2 - Backreference - same dict appearing twice", $ => {
    const sharedDict = $.let(East.value(new Map([["key", 42n]]), DictType(StringType, IntegerType)));
    const structType = StructType({
      first: DictType(StringType, IntegerType),
      second: DictType(StringType, IntegerType),
    });
    const value = $.let({
      first: sharedDict,
      second: sharedDict,
    });

    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));
    const decoded = $.let(encoded.decodeBeast(structType, 'v2'));

    // Both should reference the same dict
    $(assert.is(decoded.first, decoded.second));
  });

  test("Beast v2 - Backreference - same ref appearing twice", $ => {
    const sharedRef = $.let(East.value(ref(42n), RefType(IntegerType)));
    const structType = StructType({
      first: RefType(IntegerType),
      second: RefType(IntegerType),
    });
    const value = $.let({
      first: sharedRef,
      second: sharedRef,
    });

    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));
    const decoded = $.let(encoded.decodeBeast(structType, 'v2'));

    // Both should reference the same ref
    $(assert.is(decoded.first, decoded.second));
  });

  test("Beast v2 - Backreference - deeply nested shared arrays", $ => {
    const sharedInner = $.let(East.value([100n], ArrayType(IntegerType)));
    const innerStructType = StructType({ nested: ArrayType(IntegerType) });
    const structType = StructType({
      a: innerStructType,
      b: innerStructType,
    });
    const value = $.let({
      a: { nested: sharedInner },
      b: { nested: sharedInner },
    });

    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));
    const decoded = $.let(encoded.decodeBeast(structType, 'v2'));

    // The nested arrays should be the same reference
    $(assert.is(decoded.a.nested, decoded.b.nested));
  });

  test("Beast v2 - Backreference - mutation affects both references", $ => {
    // This test verifies that backreferences truly share identity by testing mutation
    const sharedRef = $.let(East.value(ref(10n), RefType(IntegerType)));
    const structType = StructType({
      first: RefType(IntegerType),
      second: RefType(IntegerType),
    });
    const value = $.let({
      first: sharedRef,
      second: sharedRef,
    });

    const encoded = $.let(East.Blob.encodeBeast(value, 'v2'));
    const decoded = $.let(encoded.decodeBeast(structType, 'v2'));

    // Mutate through first reference
    $(decoded.first.update(East.value(99n)));

    // Second reference should see the mutation
    $(assert.equal(decoded.second.get(), 99n));
  });

  // =========================================================================
  // Format Overhead and Size Tests
  // =========================================================================

  test("Beast v2 - Format overhead", $ => {
    // Null should be minimal: 8 magic + 1 type tag
    const nullVal = $.let(East.value(null, NullType));
    const encodedNull = $.let(East.Blob.encodeBeast(nullVal, 'v2'));
    $(assert.equal(encodedNull.size(), 9n));

    // Boolean: 8 magic + 1 type tag + 1 value
    const boolVal = $.let(East.value(true, BooleanType));
    const encodedBool = $.let(East.Blob.encodeBeast(boolVal, 'v2'));
    $(assert.equal(encodedBool.size(), 10n));

    // Empty array: 8 magic + 2 type tags (Array + element) + 1 inline marker + 1 length
    const emptyArray = $.let(East.value([], ArrayType(IntegerType)));
    const encodedEmpty = $.let(East.Blob.encodeBeast(emptyArray, 'v2'));
    $(assert.equal(encodedEmpty.size(), 12n));
  });

  // ===========================================================================
  // CSV Decoding
  // ===========================================================================

  test("decodeCsv - simple struct with header", $ => {
    const PersonType = StructType({ name: StringType, age: IntegerType });
    const csv = $.let(East.value(
      new TextEncoder().encode("name,age\nAlice,30\nBob,25"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(PersonType));

    $(assert.equal(result.size(), 2n));
    $(assert.equal(result.get(0n).name, "Alice"));
    $(assert.equal(result.get(0n).age, 30n));
    $(assert.equal(result.get(1n).name, "Bob"));
    $(assert.equal(result.get(1n).age, 25n));
  });

  test("decodeCsv - empty CSV returns empty array", $ => {
    const T = StructType({ name: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode("name\n"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 0n));
  });

  test("decodeCsv - handles UTF-8 BOM", $ => {
    const T = StructType({ name: StringType });
    const csv = $.let(East.value(
      new Uint8Array([0xEF, 0xBB, 0xBF, ...new TextEncoder().encode("name\nAlice")]),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).name, "Alice"));
  });

  test("decodeCsv - integer fields", $ => {
    const T = StructType({ value: IntegerType });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\n42\n-123\n0"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 3n));
    $(assert.equal(result.get(0n).value, 42n));
    $(assert.equal(result.get(1n).value, -123n));
    $(assert.equal(result.get(2n).value, 0n));
  });

  test("decodeCsv - float fields", $ => {
    const T = StructType({ value: FloatType });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\n3.14\n-2.5\nInfinity\n-Infinity"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 4n));
    $(assert.equal(result.get(0n).value, 3.14));
    $(assert.equal(result.get(1n).value, -2.5));
    $(assert.equal(result.get(2n).value, East.value(Infinity)));
    $(assert.equal(result.get(3n).value, East.value(-Infinity)));
  });

  test("decodeCsv - boolean fields", $ => {
    const T = StructType({ value: BooleanType });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\ntrue\nfalse"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 2n));
    $(assert.equal(result.get(0n).value, true));
    $(assert.equal(result.get(1n).value, false));
  });

  test("decodeCsv - blob fields as hex", $ => {
    const T = StructType({ value: BlobType });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\n0x48656c6c6f"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));
    const expected = $.let(East.value(new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]), BlobType));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).value, expected));
  });

  test("decodeCsv - optional string with value", $ => {
    const T = StructType({ value: VariantType({ none: NullType, some: StringType }) });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\nhello"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(
      Expr.match(result.get(0n).value, { some: ($, v) => v, none: () => "" }),
      "hello"
    ));
  });

  test("decodeCsv - optional string empty is none", $ => {
    const T = StructType({ value: VariantType({ none: NullType, some: StringType }) });
    // Empty string after header creates one data row with empty value
    // Use skipEmptyLines: false to include the empty row
    const csv = $.let(East.value(
      new TextEncoder().encode("value\n\n"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T, { skipEmptyLines: false }));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).value.getTag(), "none"));
  });

  test("decodeCsv - missing optional column becomes none", $ => {
    const T = StructType({ name: StringType, nickname: VariantType({ none: NullType, some: StringType }) });
    const csv = $.let(East.value(
      new TextEncoder().encode("name\nAlice"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).name, "Alice"));
    $(assert.equal(result.get(0n).nickname.getTag(), "none"));
  });

  test("decodeCsv - quoted fields with comma", $ => {
    const T = StructType({ value: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode('value\n"hello, world"'),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).value, "hello, world"));
  });

  test("decodeCsv - escaped quotes", $ => {
    const T = StructType({ value: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode('value\n"say ""hello"""'),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).value, 'say "hello"'));
  });

  test("decodeCsv - multiline quoted field", $ => {
    const T = StructType({ value: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode('value\n"line1\nline2"'),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).value, "line1\nline2"));
  });

  test("decodeCsv - CRLF line endings", $ => {
    const T = StructType({ value: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\r\nhello\r\nworld"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T));

    $(assert.equal(result.size(), 2n));
    $(assert.equal(result.get(0n).value, "hello"));
    $(assert.equal(result.get(1n).value, "world"));
  });

  test("decodeCsv - custom delimiter", $ => {
    const T = StructType({ a: StringType, b: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode("a;b\nhello;world"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T, { delimiter: ";" }));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).a, "hello"));
    $(assert.equal(result.get(0n).b, "world"));
  });

  test("decodeCsv - without header", $ => {
    const T = StructType({ a: StringType, b: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode("hello,world"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T, { hasHeader: false }));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).a, "hello"));
    $(assert.equal(result.get(0n).b, "world"));
  });

  test("decodeCsv - custom null strings", $ => {
    const T = StructType({ value: VariantType({ none: NullType, some: StringType }) });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\nhello\nNULL\nN/A"),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T, { nullStrings: ["", "NULL", "N/A"] }));

    $(assert.equal(result.size(), 3n));
    $(assert.equal(result.get(0n).value.getTag(), "some"));
    $(assert.equal(
      Expr.match(result.get(0n).value, { some: ($, v) => v, none: () => "" }),
      "hello"
    ));
    $(assert.equal(result.get(1n).value.getTag(), "none"));
    $(assert.equal(result.get(2n).value.getTag(), "none"));
  });

  test("decodeCsv - trim fields", $ => {
    const T = StructType({ value: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\n  hello  "),
      BlobType
    ));

    const result = $.let(csv.decodeCsv(T, { trimFields: true }));

    $(assert.equal(result.size(), 1n));
    $(assert.equal(result.get(0n).value, "hello"));
  });

  test("decodeCsv - error on missing required column", $ => {
    const T = StructType({ name: StringType, age: IntegerType });
    const csv = $.let(East.value(
      new TextEncoder().encode("name\nAlice"),
      BlobType
    ));

    $(assert.throws(csv.decodeCsv(T)));
  });

  test("decodeCsv - error on null for required field", $ => {
    const T = StructType({ name: StringType });
    // Empty string after header creates one data row with empty value (null for required field)
    // Use skipEmptyLines: false to include the empty row
    const csv = $.let(East.value(
      new TextEncoder().encode("name\n\n"),
      BlobType
    ));

    $(assert.throws(csv.decodeCsv(T, { skipEmptyLines: false })));
  });

  test("decodeCsv - error on invalid integer", $ => {
    const T = StructType({ value: IntegerType });
    const csv = $.let(East.value(
      new TextEncoder().encode("value\nabc"),
      BlobType
    ));

    $(assert.throws(csv.decodeCsv(T)));
  });

  test("decodeCsv - error on unclosed quote", $ => {
    const T = StructType({ value: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode('value\n"unclosed'),
      BlobType
    ));

    $(assert.throws(csv.decodeCsv(T)));
  });

  test("decodeCsv - strict mode errors on extra columns", $ => {
    const T = StructType({ name: StringType });
    const csv = $.let(East.value(
      new TextEncoder().encode("name,extra\nAlice,foo"),
      BlobType
    ));

    $(assert.throws(csv.decodeCsv(T, { strict: true })));
  });

  test("Equality method aliases", $ => {
    const b1 = East.value(Uint8Array.from([1, 2, 3]));

    // Test short aliases (eq, ne)
    $(assert.equal(b1.eq(Uint8Array.from([1, 2, 3])), true));
    $(assert.equal(b1.eq(Uint8Array.from([1, 2])), false));
    $(assert.equal(b1.ne(Uint8Array.from([1, 2])), true));
    $(assert.equal(b1.ne(Uint8Array.from([1, 2, 3])), false));

    // Test medium aliases (equal, notEqual)
    $(assert.equal(b1.equal(Uint8Array.from([1, 2, 3])), true));
    $(assert.equal(b1.notEqual(Uint8Array.from([1, 2])), true));
  });
});
