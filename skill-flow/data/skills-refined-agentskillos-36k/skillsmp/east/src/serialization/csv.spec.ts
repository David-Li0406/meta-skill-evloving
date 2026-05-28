/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import assert from "node:assert/strict";

import {
  decodeCsvFor,
  encodeCsvFor,
  csvParseOptionsToValue,
  csvSerializeOptionsToValue,
  CsvError,
} from './csv.js';
import {
  StructType,
  StringType,
  IntegerType,
  FloatType,
  BooleanType,
  DateTimeType,
  BlobType,
  OptionType,
} from '../types.js';
import { variant } from '../containers/variant.js';
import { SortedMap } from '../containers/sortedmap.js';

const encoder = new TextEncoder();
const decoder = new TextDecoder();

// =============================================================================
// decodeCsvFor tests
// =============================================================================

describe('decodeCsvFor', () => {
  describe('basic parsing', () => {
    test('should parse simple CSV with header', () => {
      const PersonType = StructType({ name: StringType, age: IntegerType });
      const decode = decodeCsvFor(PersonType);

      const csv = encoder.encode("name,age\nAlice,30\nBob,25");
      const result = decode(csv);

      assert.deepEqual(result, [
        { name: "Alice", age: 30n },
        { name: "Bob", age: 25n },
      ]);
    });

    test('should parse CSV without header when hasHeader is false', () => {
      const PersonType = StructType({ name: StringType, age: IntegerType });
      const config = csvParseOptionsToValue({ hasHeader: false });
      const decode = decodeCsvFor(PersonType, config);

      const csv = encoder.encode("Alice,30\nBob,25");
      const result = decode(csv);

      assert.deepEqual(result, [
        { name: "Alice", age: 30n },
        { name: "Bob", age: 25n },
      ]);
    });

    test('should handle empty CSV', () => {
      const PersonType = StructType({ name: StringType });
      const decode = decodeCsvFor(PersonType);

      const csv = encoder.encode("name\n");
      const result = decode(csv);

      assert.deepEqual(result, []);
    });

    test('should skip UTF-8 BOM', () => {
      const PersonType = StructType({ name: StringType });
      const decode = decodeCsvFor(PersonType);

      // UTF-8 BOM + "name\nAlice"
      const csv = new Uint8Array([0xEF, 0xBB, 0xBF, ...encoder.encode("name\nAlice")]);
      const result = decode(csv);

      assert.deepEqual(result, [{ name: "Alice" }]);
    });
  });

  describe('field types', () => {
    test('should parse string fields', () => {
      const T = StructType({ value: StringType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\nhello\nworld");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: "hello" }, { value: "world" }]);
    });

    test('should parse integer fields', () => {
      const T = StructType({ value: IntegerType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\n42\n-123\n0");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: 42n }, { value: -123n }, { value: 0n }]);
    });

    test('should parse float fields', () => {
      const T = StructType({ value: FloatType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\n3.14\n-2.5\nInfinity\n-Infinity\nNaN");
      const result = decode(csv);

      assert.equal(result.length, 5);
      assert.equal(result[0]!.value, 3.14);
      assert.equal(result[1]!.value, -2.5);
      assert.equal(result[2]!.value, Infinity);
      assert.equal(result[3]!.value, -Infinity);
      assert.ok(Number.isNaN(result[4]!.value));
    });

    test('should parse boolean fields', () => {
      const T = StructType({ value: BooleanType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\ntrue\nfalse");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: true }, { value: false }]);
    });

    test('should parse datetime fields', () => {
      const T = StructType({ value: DateTimeType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\n2025-01-15T10:30:00.000Z");
      const result = decode(csv);

      assert.equal(result.length, 1);
      assert.ok(result[0]!.value instanceof Date);
      assert.equal(result[0]!.value.getUTCFullYear(), 2025);
      assert.equal(result[0]!.value.getUTCMonth(), 0);
      assert.equal(result[0]!.value.getUTCDate(), 15);
    });

    test('should parse blob fields as hex', () => {
      const T = StructType({ value: BlobType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\n0x48656c6c6f");
      const result = decode(csv);

      assert.equal(result.length, 1);
      assert.ok(result[0]!.value instanceof Uint8Array);
      assert.deepEqual([...result[0]!.value], [0x48, 0x65, 0x6c, 0x6c, 0x6f]);
    });
  });

  describe('optional fields', () => {
    test('should parse optional string as some when present', () => {
      const T = StructType({ value: OptionType(StringType) });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\nhello");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: variant("some", "hello") }]);
    });

    test('should parse optional string as none when empty', () => {
      const T = StructType({ value: OptionType(StringType) });
      const config = csvParseOptionsToValue({ skipEmptyLines: false });
      const decode = decodeCsvFor(T, config);

      // Two newlines: header row, then a data row with empty field
      const csv = encoder.encode("value\n\n");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: variant("none", null) }]);
    });

    test('should use custom nullStrings', () => {
      const T = StructType({ value: OptionType(StringType) });
      const config = csvParseOptionsToValue({ nullStrings: ["", "NULL", "N/A"] });
      const decode = decodeCsvFor(T, config);

      const csv = encoder.encode("value\nhello\nNULL\nN/A");
      const result = decode(csv);

      assert.deepEqual(result, [
        { value: variant("some", "hello") },
        { value: variant("none", null) },
        { value: variant("none", null) },
      ]);
    });

    test('should handle missing optional columns', () => {
      const T = StructType({ name: StringType, age: OptionType(IntegerType) });
      const decode = decodeCsvFor(T);

      // CSV only has 'name' column, 'age' is missing
      const csv = encoder.encode("name\nAlice");
      const result = decode(csv);

      assert.deepEqual(result, [{ name: "Alice", age: variant("none", null) }]);
    });
  });

  describe('delimiters and quoting', () => {
    test('should use custom delimiter', () => {
      const T = StructType({ a: StringType, b: StringType });
      const config = csvParseOptionsToValue({ delimiter: ";" });
      const decode = decodeCsvFor(T, config);

      const csv = encoder.encode("a;b\nhello;world");
      const result = decode(csv);

      assert.deepEqual(result, [{ a: "hello", b: "world" }]);
    });

    test('should handle quoted fields', () => {
      const T = StructType({ value: StringType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode('value\n"hello, world"\n"with ""quotes"""\n"multi\nline"');
      const result = decode(csv);

      assert.deepEqual(result, [
        { value: "hello, world" },
        { value: 'with "quotes"' },
        { value: "multi\nline" },
      ]);
    });

    test('should use custom quote character', () => {
      const T = StructType({ value: StringType });
      const config = csvParseOptionsToValue({ quoteChar: "'" });
      const decode = decodeCsvFor(T, config);

      const csv = encoder.encode("value\n'hello, world'");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: "hello, world" }]);
    });
  });

  describe('line endings', () => {
    test('should handle CRLF line endings', () => {
      const T = StructType({ value: StringType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\r\nhello\r\nworld");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: "hello" }, { value: "world" }]);
    });

    test('should handle LF line endings', () => {
      const T = StructType({ value: StringType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\nhello\nworld");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: "hello" }, { value: "world" }]);
    });

    test('should handle CR line endings', () => {
      const T = StructType({ value: StringType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\rhello\rworld");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: "hello" }, { value: "world" }]);
    });
  });

  describe('trimming and empty lines', () => {
    test('should skip empty lines by default', () => {
      const T = StructType({ value: StringType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\n\nhello\n\nworld\n");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: "hello" }, { value: "world" }]);
    });

    test('should not skip empty lines when skipEmptyLines is false', () => {
      const T = StructType({ value: OptionType(StringType) });
      const config = csvParseOptionsToValue({ skipEmptyLines: false });
      const decode = decodeCsvFor(T, config);

      const csv = encoder.encode("value\nhello\n\nworld");
      const result = decode(csv);

      // Empty line becomes a row with empty field -> none
      assert.equal(result.length, 3);
    });

    test('should trim fields when trimFields is true', () => {
      const T = StructType({ value: StringType });
      const config = csvParseOptionsToValue({ trimFields: true });
      const decode = decodeCsvFor(T, config);

      const csv = encoder.encode("value\n  hello  \n  world  ");
      const result = decode(csv);

      assert.deepEqual(result, [{ value: "hello" }, { value: "world" }]);
    });
  });

  describe('column mapping', () => {
    test('should map CSV headers to struct fields', () => {
      const T = StructType({ firstName: StringType, lastName: StringType });
      const config = csvParseOptionsToValue({
        columnMapping: new Map([["First Name", "firstName"], ["Last Name", "lastName"]])
      });
      const decode = decodeCsvFor(T, config);

      const csv = encoder.encode("First Name,Last Name\nAlice,Smith");
      const result = decode(csv);

      assert.deepEqual(result, [{ firstName: "Alice", lastName: "Smith" }]);
    });
  });

  describe('strict mode', () => {
    test('should error on extra columns in strict mode', () => {
      const T = StructType({ name: StringType });
      const config = csvParseOptionsToValue({ strict: true });
      const decode = decodeCsvFor(T, config);

      const csv = encoder.encode("name,extra\nAlice,foo");

      assert.throws(() => decode(csv), (e: Error) => {
        return e instanceof CsvError && e.message.includes("unexpected column");
      });
    });

    test('should not error on extra columns when not in strict mode', () => {
      const T = StructType({ name: StringType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("name,extra\nAlice,foo");
      const result = decode(csv);

      assert.deepEqual(result, [{ name: "Alice" }]);
    });
  });

  describe('error handling', () => {
    test('should error on missing required column', () => {
      const T = StructType({ name: StringType, age: IntegerType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("name\nAlice");

      assert.throws(() => decode(csv), (e: Error) => {
        return e instanceof CsvError && e.message.includes("missing required column");
      });
    });

    test('should error on null value for required field', () => {
      const T = StructType({ name: StringType });
      const config = csvParseOptionsToValue({ skipEmptyLines: false });
      const decode = decodeCsvFor(T, config);

      // Header followed by empty data row (two newlines)
      const csv = encoder.encode("name\n\n");

      assert.throws(() => decode(csv), (e: Error) => {
        return e instanceof CsvError && e.message.includes("null value for required field");
      });
    });

    test('should error on invalid integer', () => {
      const T = StructType({ value: IntegerType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\nabc");

      assert.throws(() => decode(csv), (e: Error) => {
        return e instanceof CsvError && e.message.includes("expected integer");
      });
    });

    test('should error on invalid boolean', () => {
      const T = StructType({ value: BooleanType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\nyes");

      assert.throws(() => decode(csv), (e: Error) => {
        return e instanceof CsvError && e.message.includes("expected 'true' or 'false'");
      });
    });

    test('should error on unclosed quote', () => {
      const T = StructType({ value: StringType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode('value\n"unclosed');

      assert.throws(() => decode(csv), (e: Error) => {
        return e instanceof CsvError && e.message.includes("unclosed quote");
      });
    });

    test('should include location in error message', () => {
      const T = StructType({ value: IntegerType });
      const decode = decodeCsvFor(T);

      const csv = encoder.encode("value\n123\nabc");

      assert.throws(() => decode(csv), (e: Error) => {
        return e instanceof CsvError && e.message.includes("row 2");
      });
    });
  });

  describe('frozen output', () => {
    test('should freeze output when frozen is true', () => {
      const T = StructType({ name: StringType });
      const decode = decodeCsvFor(T, undefined, true);

      const csv = encoder.encode("name\nAlice");
      const result = decode(csv);

      assert.ok(Object.isFrozen(result));
      assert.ok(Object.isFrozen(result[0]));
    });
  });
});

// =============================================================================
// encodeCsvFor tests
// =============================================================================

describe('encodeCsvFor', () => {
  describe('basic encoding', () => {
    test('should encode simple struct array', () => {
      const T = StructType({ name: StringType, age: IntegerType });
      const encode = encodeCsvFor(T);

      const result = encode([
        { name: "Alice", age: 30n },
        { name: "Bob", age: 25n },
      ]);

      assert.equal(decoder.decode(result), "name,age\r\nAlice,30\r\nBob,25");
    });

    test('should encode empty array', () => {
      const T = StructType({ name: StringType });
      const encode = encodeCsvFor(T);

      const result = encode([]);

      assert.equal(decoder.decode(result), "name");
    });

    test('should omit header when includeHeader is false', () => {
      const T = StructType({ name: StringType });
      const config = csvSerializeOptionsToValue({ includeHeader: false });
      const encode = encodeCsvFor(T, config);

      const result = encode([{ name: "Alice" }]);

      assert.equal(decoder.decode(result), "Alice");
    });
  });

  describe('field types', () => {
    test('should encode string fields', () => {
      const T = StructType({ value: StringType });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: "hello" }]);

      assert.equal(decoder.decode(result), "value\r\nhello");
    });

    test('should encode integer fields', () => {
      const T = StructType({ value: IntegerType });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: 42n }, { value: -123n }]);

      assert.equal(decoder.decode(result), "value\r\n42\r\n-123");
    });

    test('should encode float fields including special values', () => {
      const T = StructType({ value: FloatType });
      const encode = encodeCsvFor(T);

      const result = encode([
        { value: 3.14 },
        { value: Infinity },
        { value: -Infinity },
        { value: NaN },
      ]);

      assert.equal(decoder.decode(result), "value\r\n3.14\r\nInfinity\r\n-Infinity\r\nNaN");
    });

    test('should encode boolean fields', () => {
      const T = StructType({ value: BooleanType });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: true }, { value: false }]);

      assert.equal(decoder.decode(result), "value\r\ntrue\r\nfalse");
    });

    test('should encode datetime fields as ISO', () => {
      const T = StructType({ value: DateTimeType });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: new Date("2025-01-15T10:30:00.000Z") }]);

      assert.equal(decoder.decode(result), "value\r\n2025-01-15T10:30:00.000");
    });

    test('should encode blob fields as hex', () => {
      const T = StructType({ value: BlobType });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]) }]);

      assert.equal(decoder.decode(result), "value\r\n0x48656c6c6f");
    });
  });

  describe('optional fields', () => {
    test('should encode some values', () => {
      const T = StructType({ value: OptionType(StringType) });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: variant("some", "hello") }]);

      assert.equal(decoder.decode(result), "value\r\nhello");
    });

    test('should encode none values as nullString', () => {
      const T = StructType({ value: OptionType(StringType) });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: variant("none", null) }]);

      assert.equal(decoder.decode(result), "value\r\n");
    });

    test('should use custom nullString', () => {
      const T = StructType({ value: OptionType(StringType) });
      const config = csvSerializeOptionsToValue({ nullString: "NULL" });
      const encode = encodeCsvFor(T, config);

      const result = encode([{ value: variant("none", null) }]);

      assert.equal(decoder.decode(result), "value\r\nNULL");
    });
  });

  describe('quoting', () => {
    test('should quote fields containing delimiter', () => {
      const T = StructType({ value: StringType });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: "hello, world" }]);

      assert.equal(decoder.decode(result), 'value\r\n"hello, world"');
    });

    test('should quote fields containing newlines', () => {
      const T = StructType({ value: StringType });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: "hello\nworld" }]);

      assert.equal(decoder.decode(result), 'value\r\n"hello\nworld"');
    });

    test('should escape quotes within fields', () => {
      const T = StructType({ value: StringType });
      const encode = encodeCsvFor(T);

      const result = encode([{ value: 'say "hello"' }]);

      assert.equal(decoder.decode(result), 'value\r\n"say ""hello"""');
    });

    test('should always quote when alwaysQuote is true', () => {
      const T = StructType({ value: StringType });
      const config = csvSerializeOptionsToValue({ alwaysQuote: true });
      const encode = encodeCsvFor(T, config);

      const result = encode([{ value: "hello" }]);

      assert.equal(decoder.decode(result), '"value"\r\n"hello"');
    });
  });

  describe('custom options', () => {
    test('should use custom delimiter', () => {
      const T = StructType({ a: StringType, b: StringType });
      const config = csvSerializeOptionsToValue({ delimiter: ";" });
      const encode = encodeCsvFor(T, config);

      const result = encode([{ a: "hello", b: "world" }]);

      assert.equal(decoder.decode(result), "a;b\r\nhello;world");
    });

    test('should use custom newline', () => {
      const T = StructType({ value: StringType });
      const config = csvSerializeOptionsToValue({ newline: "\n" });
      const encode = encodeCsvFor(T, config);

      const result = encode([{ value: "a" }, { value: "b" }]);

      assert.equal(decoder.decode(result), "value\na\nb");
    });

    test('should use custom quote character', () => {
      const T = StructType({ value: StringType });
      const config = csvSerializeOptionsToValue({ quoteChar: "'", alwaysQuote: true });
      const encode = encodeCsvFor(T, config);

      const result = encode([{ value: "hello" }]);

      assert.equal(decoder.decode(result), "'value'\r\n'hello'");
    });
  });
});

// =============================================================================
// Round-trip tests
// =============================================================================

describe('CSV round-trip', () => {
  test('should round-trip simple data', () => {
    const T = StructType({ name: StringType, age: IntegerType, active: BooleanType });
    const encode = encodeCsvFor(T);
    const decode = decodeCsvFor(T);

    const original = [
      { name: "Alice", age: 30n, active: true },
      { name: "Bob", age: 25n, active: false },
    ];

    const encoded = encode(original);
    const decoded = decode(encoded);

    assert.deepEqual(decoded, original);
  });

  test('should round-trip optional fields', () => {
    const T = StructType({ name: StringType, nickname: OptionType(StringType) });
    const encode = encodeCsvFor(T);
    const decode = decodeCsvFor(T);

    const original = [
      { name: "Alice", nickname: variant("some", "Ali") },
      { name: "Bob", nickname: variant("none", null) },
    ];

    const encoded = encode(original);
    const decoded = decode(encoded);

    assert.deepEqual(decoded, original);
  });

  test('should round-trip with special characters', () => {
    const T = StructType({ value: StringType });
    const encode = encodeCsvFor(T);
    const decode = decodeCsvFor(T);

    const original = [
      { value: "hello, world" },
      { value: 'with "quotes"' },
      { value: "multi\nline" },
    ];

    const encoded = encode(original);
    const decoded = decode(encoded);

    assert.deepEqual(decoded, original);
  });
});

// =============================================================================
// Config conversion tests
// =============================================================================

describe('csvParseOptionsToValue', () => {
  test('should convert empty options to all none', () => {
    const result = csvParseOptionsToValue({});

    assert.equal(result.delimiter.type, "none");
    assert.equal(result.quoteChar.type, "none");
    assert.equal(result.hasHeader.type, "none");
  });

  test('should convert provided options to some', () => {
    const result = csvParseOptionsToValue({
      delimiter: ";",
      hasHeader: false,
      nullStrings: ["", "NULL"],
    });

    assert.equal(result.delimiter.type, "some");
    assert.equal((result.delimiter as any).value, ";");
    assert.equal(result.hasHeader.type, "some");
    assert.equal((result.hasHeader as any).value, false);
    assert.equal(result.nullStrings.type, "some");
    assert.deepEqual((result.nullStrings as any).value, ["", "NULL"]);
  });

  test('should convert columnMapping Map to SortedMap', () => {
    const result = csvParseOptionsToValue({
      columnMapping: new Map([["a", "b"]]),
    });

    assert.equal(result.columnMapping.type, "some");
    assert.ok((result.columnMapping as any).value instanceof SortedMap);
  });
});

describe('csvSerializeOptionsToValue', () => {
  test('should convert empty options to all none', () => {
    const result = csvSerializeOptionsToValue({});

    assert.equal(result.delimiter.type, "none");
    assert.equal(result.quoteChar.type, "none");
    assert.equal(result.includeHeader.type, "none");
  });

  test('should convert provided options to some', () => {
    const result = csvSerializeOptionsToValue({
      delimiter: "\t",
      includeHeader: false,
      nullString: "N/A",
    });

    assert.equal(result.delimiter.type, "some");
    assert.equal((result.delimiter as any).value, "\t");
    assert.equal(result.includeHeader.type, "some");
    assert.equal((result.includeHeader as any).value, false);
    assert.equal(result.nullString.type, "some");
    assert.equal((result.nullString as any).value, "N/A");
  });
});
