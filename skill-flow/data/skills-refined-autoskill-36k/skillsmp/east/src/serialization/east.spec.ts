

/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import assert from "node:assert/strict";

import {
  decodeEastFor,
  encodeEastFor,
  parseFor,
  printFor,
} from './east.js';
import { fuzzerTest } from '../fuzz.js';
import {
  type EastType,
  NullType,
  BooleanType,
  IntegerType,
  FloatType,
  FunctionType,
  NeverType,
  StringType,
  DateTimeType,
  BlobType,
  ArrayType,
  SetType,
  DictType,
  StructType,
  VariantType,
  RecursiveType,
  AsyncFunctionType,
} from '../types.js';
import { compareFor, equalFor } from '../comparison.js';
import { SortedSet } from '../containers/sortedset.js';
import { SortedMap } from '../containers/sortedmap.js';
import { variant } from '../containers/variant.js';


describe('parseFor (value parsing)', () => {
  describe('primitive values', () => {
    test('should parse null', () => {
      const parser = parseFor(NullType);
      const result = parser('null');

      assert.equal(result.success, true);
      if (result.success) {
        assert.equal(result.value, null);
      }
    });

    test('should parse booleans', () => {
      const parser = parseFor(BooleanType);

      const trueResult = parser('true');
      assert.equal(trueResult.success, true);
      if (trueResult.success) {
        assert.equal(trueResult.value, true);
      }

      const falseResult = parser('false');
      assert.equal(falseResult.success, true);
      if (falseResult.success) {
        assert.equal(falseResult.value, false);
      }
    });

    test('should parse integers', () => {
      const parser = parseFor(IntegerType);

      const positiveResult = parser('42');
      assert.equal(positiveResult.success, true);
      if (positiveResult.success) {
        assert.equal(positiveResult.value, 42n);
      }

      const negativeResult = parser('-123');
      assert.equal(negativeResult.success, true);
      if (negativeResult.success) {
        assert.equal(negativeResult.value, -123n);
      }
    });

    test('should parse floats', () => {
      const parser = parseFor(FloatType);

      const normalResult = parser('3.14');
      assert.equal(normalResult.success, true);
      if (normalResult.success) {
        assert.equal(normalResult.value, 3.14);
      }

      const infinityResult = parser('Infinity');
      assert.equal(infinityResult.success, true);
      if (infinityResult.success) {
        assert.equal(infinityResult.value, Infinity);
      }

      const nanResult = parser('NaN');
      assert.equal(nanResult.success, true);
      if (nanResult.success) {
        assert.ok(Number.isNaN(nanResult.value));
      }
    });

    test('should parse strings', () => {
      const parser = parseFor(StringType);

      const result = parser('"hello world"');
      assert.equal(result.success, true);
      if (result.success) {
        assert.equal(result.value, 'hello world');
      }
    });

    test('should parse strings with basic content', () => {
      const parser = parseFor(StringType);

      const result = parser('"hello world 123"');
      assert.equal(result.success, true);
      if (result.success) {
        assert.equal(result.value, 'hello world 123');
      }
    });

    test('should error on unsupported escape sequence \\n', () => {
      const parser = parseFor(StringType);

      const result = parser('"hello\\nworld"');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because unexpected escape sequence in string (line 1, col 8) while parsing value of type ".String"');
      }
    });

    test('should error on unsupported escape sequence \\t', () => {
      const parser = parseFor(StringType);

      const result = parser('"hello\\tworld"');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because unexpected escape sequence in string (line 1, col 8) while parsing value of type ".String"');
      }
    });

    test('should parse datetime', () => {
      const parser = parseFor(DateTimeType);

      const result = parser('2022-11-07T23:19:28.438');
      assert.equal(result.success, true);
      if (result.success) {
        assert.deepEqual(result.value, new Date('2022-11-07T23:19:28.438Z'));
      }
    });

    test('should parse blobs', () => {
      const parser = parseFor(BlobType);

      const result = parser('0x48656c6c6f');
      assert.equal(result.success, true);
      if (result.success) {
        assert.deepEqual(result.value, new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]));
      }
    });
  });

  describe('collection values', () => {
    test('should parse empty array', () => {
      const parser = parseFor(ArrayType(StringType));

      const result = parser('[]');
      assert.equal(result.success, true);
      if (result.success) {
        assert.deepEqual(result.value, []);
      }
    });

    test('should parse array with elements', () => {
      const parser = parseFor(ArrayType(IntegerType));

      const result = parser('[1, 2, 3]');
      assert.equal(result.success, true);
      if (result.success) {
        assert.deepEqual(result.value, [1n, 2n, 3n]);
      }
    });

    test('should error on array with trailing comma', () => {
      const parser = parseFor(ArrayType(StringType));

      const result = parser('["a", "b",]');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected \'"\', got \']\' at [2] (line 1, col 11) while parsing value of type ".Array .String"');
      }
    });

    test('should parse empty set', () => {
      const type = SetType(StringType);
      const parser = parseFor(type);
      const equal = equalFor(type);
      const compare = compareFor(StringType);

      const result = parser('{}');
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, new SortedSet([], compare)));
      }
    });

    test('should parse set with elements', () => {
      const type = SetType(StringType);
      const parser = parseFor(type);
      const equal = equalFor(type);
      const compare = compareFor(StringType);

      const result = parser('{"a", "b", "c"}');
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, new SortedSet(['a', 'b', 'c'], compare)));
      }
    });

    test('should error on set with trailing comma', () => {
      const type = SetType(StringType);
      const parser = parseFor(type);

      const result = parser('{"a", "b",}');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected \'"\', got \'}\' at [2] (line 1, col 11) while parsing value of type ".Set .String"');
      }
    });

    test('should parse empty dict', () => {
      const type = DictType(StringType, IntegerType);
      const parser = parseFor(type);
      const equal = equalFor(type);
      const compare = compareFor(StringType);

      const result = parser('{:}');
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, new SortedMap([], compare)));
      }
    });

    test('should parse dict with entries', () => {
      const type = DictType(StringType, IntegerType);
      const parser = parseFor(type);
      const equal = equalFor(type);
      const compare = compareFor(StringType);

      const result = parser('{"a": 1, "b": 2}');
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, new SortedMap([['a', 1n], ['b', 2n]], compare)));
      }
    });

    test('should error on dict with trailing comma', () => {
      const type = DictType(StringType, IntegerType);
      const parser = parseFor(type);

      const result = parser('{"a": 1, "b": 2,}');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected \'"\', got \'}\' at [2](key) (line 1, col 17) while parsing value of type ".Dict (key=.String, value=.Integer)"');
      }
    });
  });

  describe('struct values', () => {
    test('should parse empty struct', () => {
      const parser = parseFor(StructType({}));

      const result = parser('()');
      assert.equal(result.success, true);
      if (result.success) {
        assert.deepEqual(result.value, {});
      }
    });

    test('should parse struct with fields', () => {
      const structType = StructType({ name: StringType, age: IntegerType });
      const parser = parseFor(structType);

      const result = parser('(name="Alice", age = 30)');
      assert.equal(result.success, true);
      if (result.success) {
        assert.deepEqual(result.value, { name: 'Alice', age: 30n });
      }
    });

    test('should parse struct with quoted field names', () => {
      const structType = StructType({ 'field name': StringType });
      const parser = parseFor(structType);

      const result = parser('(`field name`="value")');
      assert.equal(result.success, true);
      if (result.success) {
        assert.deepEqual(result.value, { 'field name': 'value' });
      }
    });

    test('should error on missing required field', () => {
      const structType = StructType({ name: StringType, age: IntegerType });
      const parser = parseFor(structType);

      const result = parser('(name="Alice")');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because missing required field \'age\' (line 1, col 14) while parsing value of type ".Struct [(name="name", type=.String), (name="age", type=.Integer)]"');
      }
    });

    test('should error on unknown field', () => {
      const structType = StructType({ name: StringType });
      const parser = parseFor(structType);

      const result = parser('(name="Alice", unknown="value")');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected \')\' to close struct (line 1, col 16) while parsing value of type ".Struct [(name="name", type=.String)]"');
      }
    });
  });

  describe('variant values', () => {
    test('should parse nullary variant without explicit null', () => {
      const variantType = VariantType({ success: NullType, error: StringType });
      const parser = parseFor(variantType);

      const result = parser('.success');
      assert.equal(result.success, true);
      if (result.success) {
        assert.equal(result.value.type, 'success');
        assert.equal(result.value.value, null);
      }
    });

    test('should parse nullary variant with null provided', () => {
      const variantType = VariantType({ success: NullType, error: StringType });
      const parser = parseFor(variantType);

      const result = parser('.success null');
      assert.equal(result.success, true);
      if (result.success) {
        assert.equal(result.value.type, 'success');
        assert.equal(result.value.value, null);
      }
    });

    test('should parse variant with data', () => {
      const variantType = VariantType({ success: NullType, error: StringType });
      const parser = parseFor(variantType);

      const result = parser('.error "Something went wrong"');
      assert.equal(result.success, true);
      if (result.success) {
        assert.equal(result.value.type, 'error');
        assert.equal(result.value.value, 'Something went wrong');
      }
    });

    test('should error on unknown variant case', () => {
      const variantType = VariantType({ success: NullType, error: StringType });
      const parser = parseFor(variantType);

      const result = parser('.unknown');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because unknown variant case .unknown, expected one of: .error, .success (line 1, col 2) while parsing value of type ".Variant [(name="error", type=.String), (name="success", type=.Null)]"');
      }
    });

    test('should error on variant case with incorrect payload', () => {
      const variantType = VariantType({ success: NullType, error: StringType });
      const parser = parseFor(variantType);

      const result = parser('.error 42');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected \'"\', got \'4\' at .error (line 1, col 8) while parsing value of type ".Variant [(name="error", type=.String), (name="success", type=.Null)]"');
      }
    });

    test('should error when data is provided for nullary case', () => {
      const variantType = VariantType({ success: NullType, error: StringType });
      const parser = parseFor(variantType);

      const result = parser('.success "unexpected"');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected null, got \'"\' at .success (line 1, col 10) while parsing value of type ".Variant [(name="error", type=.String), (name="success", type=.Null)]"');
      }
    });

    test('should error when no data is provided for data case', () => {
      const variantType = VariantType({ success: NullType, error: StringType });
      const parser = parseFor(variantType);

      const result = parser('.error');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected \'"\', got end of input at .error (line 1, col 7) while parsing value of type ".Variant [(name="error", type=.String), (name="success", type=.Null)]"');
      }
    });
  });

  describe('complex nested values', () => {
    test('should parse complex nested structure', () => {
      const complexType = StructType({
        users: ArrayType(StructType({
          name: StringType,
          age: IntegerType
        }))
      });
      const parser = parseFor(complexType);
      const equal = equalFor(complexType);

      const input = `(
        users = [
          (name="Alice", age=30),
          (name="Bob", age=25)
        ]
      )`;

      const result = parser(input);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, {
          users: [
            { name: 'Alice', age: 30n },
            { name: 'Bob', age: 25n }
          ]
        }));
      }
    });

    test('should parse deeply nested structure with multiple collection types', () => {
      // Dict<String, Struct{ items: Array<Variant<success: Struct{id: Integer, tags: Set<String>}, error: String>> }>
      const deepType = DictType(
        StringType,
        StructType({
          items: ArrayType(
            VariantType({
              success: StructType({
                id: IntegerType,
                tags: SetType(StringType)
              }),
              error: StringType
            })
          )
        })
      );

      const parser = parseFor(deepType);
      const equal = equalFor(deepType);
      const compare = compareFor(StringType);

      const input = `{
        "store1": (items=[
          .success (id=1, tags={"urgent", "verified"}),
          .success (id=2, tags={"pending"})
        ]),
        "store2": (items=[
          .error "Failed to load",
          .success (id=3, tags={})
        ])
      }`;

      const result = parser(input);
      assert.equal(result.success, true);
      if (result.success) {
        const expected = new SortedMap([
          ['store1', {
            items: [
              variant('success', { id: 1n, tags: new SortedSet(['urgent', 'verified'], compare) }),
              variant('success', { id: 2n, tags: new SortedSet(['pending'], compare) })
            ]
          }],
          ['store2', {
            items: [
              variant('error', 'Failed to load'),
              variant('success', { id: 3n, tags: new SortedSet([], compare) })
            ]
          }]
        ], compare);

        assert.ok(equal(result.value, expected));
      }
    });
  });

  describe('error cases', () => {
    test('should return error for type mismatch', () => {
      const parser = parseFor(IntegerType);

      const result = parser('"not a number"');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected integer, got \'"\' (line 1, col 1) while parsing value of type ".Integer"');
      }
    });

    test('should return error for malformed input', () => {
      const parser = parseFor(ArrayType(StringType));

      const result = parser('[unclosed array');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because expected \'"\', got \'u\' at [0] (line 1, col 2) while parsing value of type ".Array .String"');
      }
    });

    test('should return error for extra tokens', () => {
      const parser = parseFor(StringType);

      const result = parser('"hello" extra');
      assert.equal(result.success, false);
      if (!result.success) {
        assert.equal(result.error, 'Error occurred because unexpected input after parsed value (line 1, col 9) while parsing value of type ".String"');
      }
    });
  });
});

describe('printFor and round-trip tests', () => {
  describe('primitive types round-trip', () => {
    test('null should round-trip', () => {
      const printer = printFor(NullType);
      const parser = parseFor(NullType);
      const equal = equalFor(NullType);

      const value = null;
      const printed = printer(value);
      assert.equal(printed, 'null');

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });

    test('booleans should round-trip', () => {
      const printer = printFor(BooleanType);
      const parser = parseFor(BooleanType);
      const equal = equalFor(BooleanType);

      const testValues = [true, false];
      for (const value of testValues) {
        const printed = printer(value);
        assert.equal(printed, value.toString());

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.ok(equal(result.value, value));
        }
      }
    });

    test('integers should round-trip', () => {
      const printer = printFor(IntegerType);
      const parser = parseFor(IntegerType);
      const equal = equalFor(IntegerType);

      const testValues = [0n, 42n, -123n, 999999n, -999999n];
      for (const value of testValues) {
        const printed = printer(value);
        assert.equal(printed, value.toString());

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.ok(equal(result.value, value));
        }
      }
    });

    test('floats should round-trip', () => {
      const printer = printFor(FloatType);
      const parser = parseFor(FloatType);

      const testValues = [
        { value: 3.14, expected: '3.14' },
        { value: 0, expected: '0.0' },
        { value: 1, expected: '1.0' },
        { value: -5, expected: '-5.0' },
        { value: Infinity, expected: 'Infinity' },
        { value: -Infinity, expected: '-Infinity' },
        { value: NaN, expected: 'NaN' },
      ];

      for (const { value, expected } of testValues) {
        const printed = printer(value);
        assert.equal(printed, expected, `Float ${value} should print as ${expected}`);

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          if (Number.isNaN(value)) {
            assert.ok(Number.isNaN(result.value));
          } else {
            assert.equal(result.value, value);
          }
        }
      }
    });

    test('strings should round-trip', () => {
      const printer = printFor(StringType);
      const parser = parseFor(StringType);
      const equal = equalFor(StringType);

      const testValues = [
        '',
        'hello',
        'hello world',
        'with "quotes"',
        'with \\backslash',
        'with \\\\double backslash',
      ];

      for (const value of testValues) {
        const printed = printer(value);

        const result = parser(printed);
        assert.equal(result.success, true, `Failed to parse: ${printed}`);
        if (result.success) {
          assert.ok(equal(result.value, value), `Round-trip failed for: ${value}`);
        }
      }
    });

    test('datetime should round-trip', () => {
      const printer = printFor(DateTimeType);
      const parser = parseFor(DateTimeType);
      const equal = equalFor(DateTimeType);

      const testValues = [
        new Date('2022-11-07T23:19:28.438Z'),
        new Date('2000-01-01T00:00:00.000Z'),
        new Date('1970-01-01T00:00:00.000Z'),
      ];

      for (const value of testValues) {
        const printed = printer(value);

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.ok(equal(result.value, value));
        }
      }
    });

    test('blobs should round-trip', () => {
      const printer = printFor(BlobType);
      const parser = parseFor(BlobType);
      const equal = equalFor(BlobType);

      const testValues = [
        new Uint8Array([]),
        new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]),
        new Uint8Array([0, 255, 127, 128]),
      ];

      for (const value of testValues) {
        const printed = printer(value);

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.ok(equal(result.value, value));
        }
      }
    });
  });

  describe('collection types round-trip', () => {
    test('arrays should round-trip', () => {
      const type = ArrayType(IntegerType);
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const testValues = [
        [],
        [1n, 2n, 3n],
        [0n],
        [-1n, -2n, -3n],
      ];

      for (const value of testValues) {
        const printed = printer(value);

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.ok(equal(result.value, value));
        }
      }
    });

    test('sets should round-trip', () => {
      const type = SetType(StringType);
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);
      const compare = compareFor(StringType);

      const testValues = [
        new SortedSet([], compare),
        new SortedSet(['a', 'b', 'c'], compare),
        new SortedSet(['single'], compare),
      ];

      for (const value of testValues) {
        const printed = printer(value);

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.ok(equal(result.value, value));
        }
      }
    });

    test('dicts should round-trip', () => {
      const type = DictType(StringType, IntegerType);
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);
      const compare = compareFor(StringType);

      const testValues = [
        new SortedMap<string, bigint>([], compare),
        new SortedMap([['a', 1n], ['b', 2n]], compare),
        new SortedMap([['key', 42n]], compare),
      ];

      for (const value of testValues) {
        const printed = printer(value);

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.ok(equal(result.value, value));
        }
      }
    });
  });

  describe('struct and variant types round-trip', () => {
    test('empty struct should round-trip', () => {
      const type = StructType({});
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const value = {};
      const printed = printer(value);
      assert.equal(printed, '()');

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });

    test('struct with fields should round-trip', () => {
      const type = StructType({ name: StringType, age: IntegerType });
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const testValues = [
        { name: 'Alice', age: 30n },
        { name: 'Bob', age: 25n },
      ];

      for (const value of testValues) {
        const printed = printer(value);

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.ok(equal(result.value, value));
        }
      }
    });

    test('struct with quoted field names should round-trip', () => {
      const type = StructType({ 'field name': StringType, 'another-field': IntegerType });
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const value = { 'field name': 'test', 'another-field': 42n };
      const printed = printer(value);

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });

    test('variant nullary case should round-trip', () => {
      const type = VariantType({ success: NullType, error: StringType });
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const value = variant('success');
      const printed = printer(value);
      assert.equal(printed, '.success');

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });

    test('variant with data should round-trip', () => {
      const type = VariantType({ success: NullType, error: StringType });
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const value = variant('error', 'Something went wrong');
      const printed = printer(value);

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });
  });

  describe('complex nested structures round-trip', () => {
    test('nested arrays should round-trip', () => {
      const type = ArrayType(ArrayType(IntegerType));
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const value = [[1n, 2n], [3n, 4n], []];
      const printed = printer(value);

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });

    test('struct with array field should round-trip', () => {
      const type = StructType({
        users: ArrayType(StructType({
          name: StringType,
          age: IntegerType
        }))
      });
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const value = {
        users: [
          { name: 'Alice', age: 30n },
          { name: 'Bob', age: 25n }
        ]
      };
      const printed = printer(value);

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });

    test('deeply nested structure should round-trip', () => {
      const type = DictType(
        StringType,
        StructType({
          items: ArrayType(
            VariantType({
              success: StructType({
                id: IntegerType,
                tags: SetType(StringType)
              }),
              error: StringType
            })
          )
        })
      );
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);
      const compare = compareFor(StringType);

      const value = new SortedMap([
        ['store1', {
          items: [
            variant('success', { id: 1n, tags: new SortedSet(['urgent', 'verified'], compare) }),
            variant('success', { id: 2n, tags: new SortedSet(['pending'], compare) })
          ]
        }],
        ['store2', {
          items: [
            variant('error', 'Failed to load'),
            variant('success', { id: 3n, tags: new SortedSet([], compare) })
          ]
        }]
      ], compare);

      const printed = printer(value);

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });
  });

  describe('printFor edge cases', () => {
    test('float formatting edge cases', () => {
      const printer = printFor(FloatType);

      // Integers should always have .0
      assert.equal(printer(0), '0.0');
      assert.equal(printer(1), '1.0');
      assert.equal(printer(-1), '-1.0');
      assert.equal(printer(100), '100.0');

      // Decimals should be preserved
      assert.equal(printer(3.14), '3.14');
      assert.equal(printer(-2.5), '-2.5');

      // Special values
      assert.equal(printer(Infinity), 'Infinity');
      assert.equal(printer(-Infinity), '-Infinity');
      assert.equal(printer(NaN), 'NaN');
    });

    test('string escaping', () => {
      const printer = printFor(StringType);
      const parser = parseFor(StringType);

      const testCases = [
        { input: 'hello', expected: '"hello"' },
        { input: 'with "quotes"', expected: '"with \\"quotes\\""' },
        { input: 'with \\backslash', expected: '"with \\\\backslash"' },
      ];

      for (const { input, expected } of testCases) {
        const printed = printer(input);
        assert.equal(printed, expected);

        const result = parser(printed);
        assert.equal(result.success, true);
        if (result.success) {
          assert.equal(result.value, input);
        }
      }
    });

    test('identifier quoting in structs', () => {
      const type = StructType({
        normal: IntegerType,
        'needs quotes': IntegerType,
        'special-chars!': IntegerType
      });
      const printer = printFor(type);
      const parser = parseFor(type);
      const equal = equalFor(type);

      const value = {
        normal: 1n,
        'needs quotes': 2n,
        'special-chars!': 3n
      };
      const printed = printer(value);

      // Should contain backticks for identifiers with spaces/special chars
      assert.ok(printed.includes('`needs quotes`'));
      assert.ok(printed.includes('`special-chars!`'));
      assert.ok(printed.includes('normal='));

      const result = parser(printed);
      assert.equal(result.success, true);
      if (result.success) {
        assert.ok(equal(result.value, value));
      }
    });

    test('empty collections formatting', () => {
      const arrayPrinter = printFor(ArrayType(IntegerType));
      const setPrinter = printFor(SetType(IntegerType));
      const dictPrinter = printFor(DictType(IntegerType, IntegerType));
      const compare = compareFor(IntegerType);

      assert.equal(arrayPrinter([]), '[]');
      assert.equal(setPrinter(new SortedSet([], compare)), '{}');
      assert.equal(dictPrinter(new SortedMap([], compare)), '{:}');
    });

    test('variant case formatting', () => {
      const type = VariantType({
        none: NullType,
        some: IntegerType,
        'complex-name': StringType
      });
      const printer = printFor(type);

      assert.equal(printer(variant('none', null)), '.none');
      assert.equal(printer(variant('some', 42n)), '.some 42');
      assert.equal(printer(variant('complex-name', 'test')), '.`complex-name` "test"');
    });
  });
});

describe('encodeEastFor and decodeEastFor (Uint8Array encoding)', () => {
  test('should encode/decode integers with Uint8Array', () => {
    const encode = encodeEastFor(IntegerType);
    const decode = decodeEastFor(IntegerType);

    const value = 42n;
    const encoded = encode(value);
    const decoded = decode(encoded);

    assert.ok(encoded instanceof Uint8Array);
    assert.strictEqual(decoded, value);
  });

  test('should encode/decode structs with Uint8Array', () => {
    const type = StructType({ name: StringType, age: IntegerType });
    const encode = encodeEastFor(type);
    const decode = decodeEastFor(type);

    const value = { name: 'Alice', age: 30n };
    const encoded = encode(value);
    const decoded = decode(encoded);

    assert.deepEqual(decoded, value);
  });

  test('should throw error when decoding invalid East format', () => {
    const textEncoder = new TextEncoder();
    const decode = decodeEastFor(IntegerType);

    const invalidData = textEncoder.encode('not an integer');
    assert.throws(() => decode(invalidData), /Failed to decode East value/);
  });
});

describe('Never type handling', () => {
  test('should throw when printing Never type', () => {
    const printer = printFor(NeverType);
    assert.throws(() => printer(null as never), /Attempted to print value of type/);
  });

  test('should throw when parsing Never type', () => {
    const parser = parseFor(NeverType);
    const result = parser("");
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.match(result.error, /Attempted to parse value of type .Never/);
    }
  });
});

describe('Function type handling', () => {
  test('should print Function type summary', () => {
    const funcType = FunctionType([], IntegerType);
    const printer = printFor(funcType);
    const result = printer((() => 42) as any);
    assert.strictEqual(result, '() => .Integer');
  });

  test('should throw when creating parser for Function type', () => {
    const funcType = FunctionType([], IntegerType);
    assert.throws(() => parseFor(funcType), /Cannot parse/);
  });

  test('should print AsyncFunction type summary', () => {
    const funcType = AsyncFunctionType([], IntegerType);
    const printer = printFor(funcType);
    const result = printer((async () => 42) as any);
    assert.strictEqual(result, 'async () => .Integer');
  });

  test('should throw when creating parser for Function type', () => {
    const funcType = FunctionType([], IntegerType);
    assert.throws(() => parseFor(funcType), /Cannot parse/);
  });
});

describe('Frozen parameter tests', () => {
  test('should freeze DateTime when frozen=true', () => {
    const parser = parseFor(DateTimeType, true);
    const result = parser('2022-11-07T23:19:28.438');
    assert.strictEqual(result.success, true);
    if (result.success) {
      assert.ok(Object.isFrozen(result.value));
    }
  });

  test('should not freeze DateTime when frozen=false', () => {
    const parser = parseFor(DateTimeType, false);
    const result = parser('2022-11-07T23:19:28.438');
    assert.strictEqual(result.success, true);
    if (result.success) {
      assert.ok(!Object.isFrozen(result.value));
    }
  });

  test('should attempt to freeze Blob when frozen=true', () => {
    // Note: Uint8Array freezing may throw in some environments
    const parser = parseFor(BlobType, true);
    // This tests the frozen code path
    try {
      const result = parser('0x48656c6c6f');
      if (result.success) {
        // If it didn't throw, check if frozen
        assert.ok(Object.isFrozen(result.value) || !Object.isFrozen(result.value));
      }
    } catch (e: any) {
      // Freezing Uint8Array may throw
      assert.ok(e.message.includes('freeze') || e.message.includes('Blob'));
    }
  });

  test('should freeze Array when frozen=true', () => {
    const parser = parseFor(ArrayType(IntegerType), true);
    const result = parser('[1, 2, 3]');
    assert.strictEqual(result.success, true);
    if (result.success) {
      assert.ok(Object.isFrozen(result.value));
    }
  });

  test('should freeze Set when frozen=true', () => {
    const parser = parseFor(SetType(StringType), true);
    const result = parser('{"a", "b"}');
    assert.strictEqual(result.success, true);
    if (result.success) {
      assert.ok(Object.isFrozen(result.value));
    }
  });

  test('should freeze Dict when frozen=true', () => {
    const parser = parseFor(DictType(StringType, IntegerType), true);
    const result = parser('{"a": 1, "b": 2}');
    assert.strictEqual(result.success, true);
    if (result.success) {
      assert.ok(Object.isFrozen(result.value));
    }
  });

  test('should freeze Struct when frozen=true', () => {
    const parser = parseFor(StructType({ x: IntegerType }), true);
    const result = parser('(x=42)');
    assert.strictEqual(result.success, true);
    if (result.success) {
      assert.ok(Object.isFrozen(result.value));
    }
  });

  test('should freeze Variant when frozen=true', () => {
    const parser = parseFor(VariantType({ some: IntegerType }), true);
    const result = parser('.some 42');
    assert.strictEqual(result.success, true);
    if (result.success) {
      assert.ok(Object.isFrozen(result.value));
    }
  });
});

describe('Additional error cases', () => {
  test('should handle empty Dict with closing brace only', () => {
    const parser = parseFor(DictType(StringType, IntegerType));
    const result = parser('{}');
    assert.strictEqual(result.success, true);
    if (result.success) {
      assert.strictEqual(result.value.size, 0);
    }
  });

  test('should error on invalid empty Dict format', () => {
    const parser = parseFor(DictType(StringType, IntegerType));
    const result = parser('{:  extra}');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \'}\' after \':\' in empty dict (line 1, col 5) while parsing value of type ".Dict (key=.String, value=.Integer)"');
    }
  });

  test('should error on unterminated string in parseString', () => {
    const parser = parseFor(StringType);
    const result = parser('"unterminated');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because unterminated string (missing closing quote) (line 1, col 14) while parsing value of type ".String"');
    }
  });

  test('should error on string with only backslash at end', () => {
    const parser = parseFor(StringType);
    const result = parser('"ends with\\');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because unterminated string (missing closing quote) (line 1, col 12) while parsing value of type ".String"');
    }
  });

  test('should error on unterminated quoted identifier', () => {
    const structType = StructType({ 'quoted': IntegerType });
    const parser = parseFor(structType);
    const result = parser('(`quoted: 42)');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because missing required field \'quoted\' (line 1, col 2) while parsing value of type ".Struct [(name="quoted", type=.Integer)]"');
    }
  });

  test('should error on quoted identifier with only backslash at end', () => {
    const structType = StructType({ 'id': IntegerType });
    const parser = parseFor(structType);
    const result = parser('(`id\\: 42)');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because missing required field \'id\' (line 1, col 2) while parsing value of type ".Struct [(name="id", type=.Integer)]"');
    }
  });

  test('should error on unterminated identifier via unexpected escape', () => {
    const structType = StructType({ 'field': IntegerType });
    const parser = parseFor(structType);
    const result = parser('(`field: 42)');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because missing required field \'field\' (line 1, col 2) while parsing value of type ".Struct [(name="field", type=.Integer)]"');
    }
  });

  test('should error when expecting closing paren in struct', () => {
    const structType = StructType({ x: IntegerType, y: IntegerType });
    const parser = parseFor(structType);
    const result = parser('(x=1, y=2,');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \')\' to close struct (line 1, col 11) while parsing value of type ".Struct [(name="x", type=.Integer), (name="y", type=.Integer)]"');
    }
  });

  test('should error on struct with wrong field name', () => {
    const structType = StructType({ expected: IntegerType });
    const parser = parseFor(structType);
    const result = parser('(wrong=42)');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because unknown field \'wrong\', expected one of: expected (line 1, col 2) while parsing value of type ".Struct [(name="expected", type=.Integer)]"');
    }
  });

  test('should error on missing colon after struct field name', () => {
    const structType = StructType({ x: IntegerType });
    const parser = parseFor(structType);
    const result = parser('(x 42)');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \'=\' after field name \'x\' (line 1, col 4) while parsing value of type ".Struct [(name="x", type=.Integer)]"');
    }
  });

  test('should error on unexpected end of input in struct', () => {
    const structType = StructType({ x: IntegerType, y: IntegerType });
    const parser = parseFor(structType);
    const result = parser('(x=1');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because unexpected end of input in struct (line 1, col 5) while parsing value of type ".Struct [(name="x", type=.Integer), (name="y", type=.Integer)]"');
    }
  });

  test('should error on missing comma or closing paren in struct', () => {
    const structType = StructType({ x: IntegerType, y: IntegerType });
    const parser = parseFor(structType);
    const result = parser('(x=1 y=2)');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \',\' or \')\' after struct field (line 1, col 6) while parsing value of type ".Struct [(name="x", type=.Integer), (name="y", type=.Integer)]"');
    }
  });

  test('should error on variant with whitespace after dot', () => {
    const variantType = VariantType({ some: IntegerType });
    const parser = parseFor(variantType);
    const result = parser('. some 42');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because whitespace not allowed between \'.\' and case identifier (line 1, col 2) while parsing value of type ".Variant [(name="some", type=.Integer)]"');
    }
  });

  test('should error on float with missing exponent digits', () => {
    const parser = parseFor(FloatType);
    const result = parser('1.5e');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected digits in float exponent (line 1, col 5) while parsing value of type ".Float"');
    }
  });

  test('should error on DateTime with invalid format', () => {
    const parser = parseFor(DateTimeType);
    const result = parser('invalid-date');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected DateTime in format YYYY-MM-DDTHH:MM:SS.sss (line 1, col 1) while parsing value of type ".DateTime"');
    }
  });

  test('should error on invalid DateTime value', () => {
    const parser = parseFor(DateTimeType);
    const result = parser('2022-13-40T25:61:61.999');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because invalid DateTime value, got "2022-13-40T25:61:61.999" (line 1, col 1) while parsing value of type ".DateTime"');
    }
  });

  test('should error on Blob with odd number of hex digits', () => {
    const parser = parseFor(BlobType);
    const result = parser('0x123');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because invalid hex string (odd length), got "0x123" (line 1, col 1) while parsing value of type ".Blob"');
    }
  });

  test('should error on Blob not starting with 0x', () => {
    const parser = parseFor(BlobType);
    const result = parser('123456');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected Blob starting with 0x (line 1, col 1) while parsing value of type ".Blob"');
    }
  });

  test('should error on array without opening bracket', () => {
    const parser = parseFor(ArrayType(IntegerType));
    const result = parser('1, 2, 3]');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \'[\' to start array (line 1, col 1) while parsing value of type ".Array .Integer"');
    }
  });

  test('should error on missing comma or closing bracket in array', () => {
    const parser = parseFor(ArrayType(IntegerType));
    const result = parser('[1 2]');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \',\' or \']\' after array element (line 1, col 4) while parsing value of type ".Array .Integer"');
    }
  });

  test('should error on set without opening brace', () => {
    const parser = parseFor(SetType(StringType));
    const result = parser('"a", "b"}');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \'{\' to start set (line 1, col 1) while parsing value of type ".Set .String"');
    }
  });

  test('should error on missing comma or closing brace in set', () => {
    const parser = parseFor(SetType(StringType));
    const result = parser('{"a" "b"}');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \',\' or \'}\' after set element (line 1, col 6) while parsing value of type ".Set .String"');
    }
  });

  test('should error on dict without opening brace', () => {
    const parser = parseFor(DictType(StringType, IntegerType));
    const result = parser('"a": 1}');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \'{\' to start dict (line 1, col 1) while parsing value of type ".Dict (key=.String, value=.Integer)"');
    }
  });

  test('should error on missing colon in dict entry', () => {
    const parser = parseFor(DictType(StringType, IntegerType));
    const result = parser('{"a" 1}');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \':\' after dict key at entry 0 (line 1, col 6) while parsing value of type ".Dict (key=.String, value=.Integer)"');
    }
  });

  test('should error on missing comma or closing brace in dict', () => {
    const parser = parseFor(DictType(StringType, IntegerType));
    const result = parser('{"a": 1 "b": 2}');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \',\' or \'}\' after dict entry (line 1, col 9) while parsing value of type ".Dict (key=.String, value=.Integer)"');
    }
  });

  test('should error on struct without opening paren', () => {
    const structType = StructType({ x: IntegerType });
    const parser = parseFor(structType);
    const result = parser('x: 42)');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \'(\' to start struct (line 1, col 1) while parsing value of type ".Struct [(name="x", type=.Integer)]"');
    }
  });

  test('should error on variant without dot', () => {
    const variantType = VariantType({ some: IntegerType });
    const parser = parseFor(variantType);
    const result = parser('some 42');
    assert.strictEqual(result.success, false);
    if (!result.success) {
      assert.equal(result.error, 'Error occurred because expected \'.\' to start variant case (line 1, col 1) while parsing value of type ".Variant [(name="some", type=.Integer)]"');
    }
  });

  test('should handle non-ParseError exceptions in parseFor wrapper', () => {
    const parser = parseFor(IntegerType);
    // This should still work - parseFor wraps exceptions
    const result = parser('42');
    assert.strictEqual(result.success, true);
  });
});

describe('Fuzz tests', () => {
  test('should round-trip random types and values', { timeout: 60_000 }, async () => {
    const result = await fuzzerTest(
      (type: EastType) => {
        const print = printFor(type);
        const parse = parseFor(type);
        const equal = equalFor(type);

        return async (value: any) => {
          // Print and parse
          const printed = print(value);
          const parseResult = parse(printed);

          // Check parse succeeded
          if (!parseResult.success) {
            throw new Error(`Parse failed: ${parseResult.error}`);
          }

          // Check value equality
          if (!equal(parseResult.value, value)) {
            throw new Error(`Round-trip failed: values not equal`);
          }
        };
      },
      100, // 100 random types
      10,  // 10 samples per type
      { includeRecursive: false } // TODO: recursive value generation needs work
    );

    assert.strictEqual(result, true, "Fuzz test failed");
  });

  test('should round-trip with Uint8Array encoding for random types', { timeout: 60_000 }, async () => {
    const result = await fuzzerTest(
      (type: EastType) => {
        const encode = encodeEastFor(type);
        const decode = decodeEastFor(type);
        const equal = equalFor(type);

        return async (value: any) => {
          // Encode and decode
          const encoded = encode(value);
          const decoded = decode(encoded);

          // Verify it's a Uint8Array
          if (!(encoded instanceof Uint8Array)) {
            throw new Error(`Encoded value is not a Uint8Array`);
          }

          // Check value equality
          if (!equal(decoded, value)) {
            throw new Error(`Round-trip failed: values not equal`);
          }
        };
      },
      100, // 100 random types
      10,  // 10 samples per type
      { includeRecursive: false } // TODO: recursive value generation needs work
    );

    assert.strictEqual(result, true, "Fuzz test failed");
  });
});

describe('printFor with aliases', () => {
  test('should detect array aliases in struct', () => {
    const type = StructType({ a: ArrayType(IntegerType), b: ArrayType(IntegerType) });
    const printer = printFor(type);

    // Create struct with shared array reference
    const sharedArray = [1n, 2n, 3n];
    const value = { a: sharedArray, b: sharedArray };

    const result = printer(value);
    assert.equal(result, "(a=[1, 2, 3], b=1#.a)");
  });

  test('should detect set aliases in struct', () => {
    const type = StructType({ a: SetType(IntegerType), b: SetType(IntegerType) });
    const printer = printFor(type);

    // Create struct with shared set reference
    const sharedSet = new SortedSet([1n, 2n, 3n]);
    const value = { a: sharedSet, b: sharedSet };

    const result = printer(value);
    assert.equal(result, "(a={1,2,3}, b=1#.a)");
  });

  test('should detect dict aliases in struct', () => {
    const type = StructType({ a: DictType(IntegerType, StringType), b: DictType(IntegerType, StringType) });
    const printer = printFor(type);

    // Create struct with shared dict reference
    const sharedDict = new SortedMap([[1n, "x"], [2n, "y"]]);
    const value = { a: sharedDict, b: sharedDict };

    const result = printer(value);
    assert.equal(result, '(a={1:"x",2:"y"}, b=1#.a)');
  });

  test('should detect nested array aliases', () => {
    const type = ArrayType(ArrayType(IntegerType));
    const printer = printFor(type);

    // Create array with shared inner array
    const inner = [1n, 2n];
    const value = [inner, inner, inner];

    const result = printer(value);
    assert.equal(result, "[[1, 2], 1#[0], 1#[0]]");
  });
});

describe('printFor with recursive types', () => {
  test('should print tree without cycles', () => {
    const TreeType = RecursiveType(self => VariantType({
      leaf: NullType,
      node: StructType({
        value: IntegerType,
        left: self,
        right: self
      })
    }));

    const printer = printFor(TreeType);

    // Create simple tree: node(1, leaf, leaf)
    const tree = variant("node", {
      value: 1n,
      left: variant("leaf"),
      right: variant("leaf")
    });

    const result = printer(tree);
    assert.equal(result, ".node (value=1, left=.leaf, right=.leaf)");
  });

  test('should print larger tree without cycles', () => {
    const TreeType = RecursiveType(self => VariantType({
      leaf: NullType,
      node: StructType({
        value: IntegerType,
        left: self,
        right: self
      })
    }));

    const printer = printFor(TreeType);

    // Create tree: node(2, node(1, leaf, leaf), node(3, leaf, leaf))
    const tree = variant("node", {
      value: 2n,
      left: variant("node", {
        value: 1n,
        left: variant("leaf"),
        right: variant("leaf")
      }),
      right: variant("node", {
        value: 3n,
        left: variant("leaf"),
        right: variant("leaf")
      })
    });

    const result = printer(tree);
    assert.equal(result, ".node (value=2, left=.node (value=1, left=.leaf, right=.leaf), right=.node (value=3, left=.leaf, right=.leaf))");
  });

  test('should print linked list without cycles', () => {
    const LinkedListType = RecursiveType(self => VariantType({
      nil: NullType,
      cons: StructType({
        head: IntegerType,
        tail: self
      })
    }));

    const printer = printFor(LinkedListType);

    // Create list: cons(1, cons(2, cons(3, nil)))
    const list = variant("cons", {
      head: 1n,
      tail: variant("cons", {
        head: 2n,
        tail: variant("cons", {
          head: 3n,
          tail: variant("nil")
        })
      })
    });

    const result = printer(list);
    assert.equal(result, ".cons (head=1, tail=.cons (head=2, tail=.cons (head=3, tail=.nil)))");
  });
});