/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import { describe, test } from "node:test";
import assert from "node:assert/strict";

import { parseInferred } from './east.js';
import {
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
  NeverType,
  isTypeEqual,
} from '../types.js';

describe('parseInferred', () => {
  describe('primitive types', () => {
    test('should infer null', () => {
      const [type, value] = parseInferred('null');
      assert.ok(isTypeEqual(type, NullType));
      assert.equal(value, null);
    });

    test('should infer boolean true', () => {
      const [type, value] = parseInferred('true');
      assert.ok(isTypeEqual(type, BooleanType));
      assert.equal(value, true);
    });

    test('should infer boolean false', () => {
      const [type, value] = parseInferred('false');
      assert.ok(isTypeEqual(type, BooleanType));
      assert.equal(value, false);
    });

    test('should infer positive integer', () => {
      const [type, value] = parseInferred('42');
      assert.ok(isTypeEqual(type, IntegerType));
      assert.equal(value, 42n);
    });

    test('should infer negative integer', () => {
      const [type, value] = parseInferred('-123');
      assert.ok(isTypeEqual(type, IntegerType));
      assert.equal(value, -123n);
    });

    test('should infer float with decimal', () => {
      const [type, value] = parseInferred('3.14');
      assert.ok(isTypeEqual(type, FloatType));
      assert.equal(value, 3.14);
    });

    test('should infer float with exponent', () => {
      const [type, value] = parseInferred('1e6');
      assert.ok(isTypeEqual(type, FloatType));
      assert.equal(value, 1e6);
    });

    test('should infer float NaN', () => {
      const [type, value] = parseInferred('NaN');
      assert.ok(isTypeEqual(type, FloatType));
      assert.ok(Number.isNaN(value));
    });

    test('should infer float Infinity', () => {
      const [type, value] = parseInferred('Infinity');
      assert.ok(isTypeEqual(type, FloatType));
      assert.equal(value, Infinity);
    });

    test('should infer float -Infinity', () => {
      const [type, value] = parseInferred('-Infinity');
      assert.ok(isTypeEqual(type, FloatType));
      assert.equal(value, -Infinity);
    });

    test('should infer string', () => {
      const [type, value] = parseInferred('"hello world"');
      assert.ok(isTypeEqual(type, StringType));
      assert.equal(value, 'hello world');
    });

    test('should infer datetime', () => {
      const [type, value] = parseInferred('2025-01-15T14:30:45.123');
      assert.ok(isTypeEqual(type, DateTimeType));
      assert.ok(value instanceof Date);
      assert.equal(value.toISOString(), '2025-01-15T14:30:45.123Z');
    });

    test('should infer blob', () => {
      const [type, value] = parseInferred('0x00ff');
      assert.ok(isTypeEqual(type, BlobType));
      assert.ok(value instanceof Uint8Array);
      assert.deepEqual(value, new Uint8Array([0x00, 0xff]));
    });

    test('should infer empty blob', () => {
      const [type, value] = parseInferred('0x');
      assert.ok(isTypeEqual(type, BlobType));
      assert.ok(value instanceof Uint8Array);
      assert.equal(value.length, 0);
    });
  });

  describe('empty collections', () => {
    test('should infer empty array as Array<Never>', () => {
      const [type, value] = parseInferred('[]');
      assert.ok(isTypeEqual(type, ArrayType(NeverType)));
      assert.ok(Array.isArray(value));
      assert.equal(value.length, 0);
    });

    test('should infer empty set as Set<Never>', () => {
      const [type, value] = parseInferred('{}');
      assert.ok(isTypeEqual(type, SetType(NeverType)));
      assert.equal(value.size, 0);
    });

    test('should infer empty dict as Dict<Never, Never>', () => {
      const [type, value] = parseInferred('{:}');
      assert.ok(isTypeEqual(type, DictType(NeverType, NeverType)));
      assert.equal(value.size, 0);
    });

    test('should infer empty struct', () => {
      const [type, value] = parseInferred('()');
      assert.ok(isTypeEqual(type, StructType({})));
      assert.deepEqual(value, {});
    });
  });

  describe('arrays with type widening', () => {
    test('should infer homogeneous integer array', () => {
      const [type, value] = parseInferred('[1, 2, 3]');
      assert.ok(isTypeEqual(type, ArrayType(IntegerType)));
      assert.deepEqual(value, [1n, 2n, 3n]);
    });

    test('should infer homogeneous string array', () => {
      const [type, value] = parseInferred('["a", "b", "c"]');
      assert.ok(isTypeEqual(type, ArrayType(StringType)));
      assert.deepEqual(value, ['a', 'b', 'c']);
    });

    test('should error on mixed integer and float', () => {
      assert.throws(
        () => parseInferred('[1, 2.5]'),
        /incompatible array element types/
      );
    });

    test('should error on mixed string and integer', () => {
      assert.throws(
        () => parseInferred('[1, "hello"]'),
        /incompatible array element types/
      );
    });

    test('should infer nested arrays', () => {
      const [type, value] = parseInferred('[[1, 2], [3, 4]]');
      assert.ok(isTypeEqual(type, ArrayType(ArrayType(IntegerType))));
      assert.deepEqual(value, [[1n, 2n], [3n, 4n]]);
    });
  });

  describe('sets with type widening', () => {
    test('should infer homogeneous integer set', () => {
      const [type, value] = parseInferred('{1,2,3}');
      assert.ok(isTypeEqual(type, SetType(IntegerType)));
      assert.equal(value.size, 3);
      assert.ok(value.has(1n));
      assert.ok(value.has(2n));
      assert.ok(value.has(3n));
    });

    test('should infer homogeneous string set', () => {
      const [type, value] = parseInferred('{"a","b","c"}');
      assert.ok(isTypeEqual(type, SetType(StringType)));
      assert.equal(value.size, 3);
      assert.ok(value.has('a'));
      assert.ok(value.has('b'));
      assert.ok(value.has('c'));
    });

    test('should error on mixed types in set', () => {
      assert.throws(
        () => parseInferred('{1, "hello"}'),
        /incompatible set element types/
      );
    });
  });

  describe('dicts with type widening', () => {
    test('should infer homogeneous dict', () => {
      const [type, value] = parseInferred('{"a":1,"b":2}');
      assert.ok(isTypeEqual(type, DictType(StringType, IntegerType)));
      assert.equal(value.size, 2);
      assert.equal(value.get('a'), 1n);
      assert.equal(value.get('b'), 2n);
    });

    test('should error on mixed key types', () => {
      assert.throws(
        () => parseInferred('{1:"a","b":2}'),
        /incompatible dict types/
      );
    });

    test('should error on mixed value types', () => {
      assert.throws(
        () => parseInferred('{"a":1,"b":"hello"}'),
        /incompatible dict types/
      );
    });
  });

  describe('structs', () => {
    test('should infer simple struct', () => {
      const [type, value] = parseInferred('(x=1, y=2)');
      const expectedType = StructType({ x: IntegerType, y: IntegerType });
      assert.ok(isTypeEqual(type, expectedType));
      assert.deepEqual(value, { x: 1n, y: 2n });
    });

    test('should infer struct with mixed field types', () => {
      const [type, value] = parseInferred('(name="Alice", age=30, active=true)');
      const expectedType = StructType({
        name: StringType,
        age: IntegerType,
        active: BooleanType
      });
      assert.ok(isTypeEqual(type, expectedType));
      assert.deepEqual(value, { name: 'Alice', age: 30n, active: true });
    });

    test('should infer nested struct', () => {
      const [type, value] = parseInferred('(point=(x=1, y=2), label="A")');
      const expectedType = StructType({
        point: StructType({ x: IntegerType, y: IntegerType }),
        label: StringType
      });
      assert.ok(isTypeEqual(type, expectedType));
      assert.deepEqual(value, {
        point: { x: 1n, y: 2n },
        label: 'A'
      });
    });
  });

  describe('variants', () => {
    test('should infer variant with data', () => {
      const [type, value] = parseInferred('.some 42');
      const expectedType = VariantType({ some: IntegerType });
      assert.ok(isTypeEqual(type, expectedType));
      assert.equal(value.type, 'some');
      assert.equal(value.value, 42n);
    });

    test('should infer variant without data (null variant)', () => {
      const [type, value] = parseInferred('.none');
      const expectedType = VariantType({ none: NullType });
      assert.ok(isTypeEqual(type, expectedType));
      assert.equal(value.type, 'none');
      assert.equal(value.value, null);
    });

    test('should infer variant with struct data', () => {
      const [type, value] = parseInferred('.success (code=200, message="OK")');
      const expectedType = VariantType({
        success: StructType({ code: IntegerType, message: StringType })
      });
      assert.ok(isTypeEqual(type, expectedType));
      assert.equal(value.type, 'success');
      assert.deepEqual(value.value, { code: 200n, message: 'OK' });
    });
  });

  describe('error handling', () => {
    test('should error on ref types', () => {
      assert.throws(
        () => parseInferred('&42'),
        /ref types not supported in type inference/
      );
    });

    test('should error on circular references', () => {
      // This is a rough heuristic - actual circular ref syntax would be detected
      assert.throws(
        () => parseInferred('1#'),
        /circular references not supported in type inference/
      );
    });

    test('should error on unexpected input after value', () => {
      assert.throws(
        () => parseInferred('42 garbage'),
        /Unexpected input after parsed value/
      );
    });

    test('should provide location info in errors', () => {
      try {
        parseInferred('[1, "hello"]');
        assert.fail('Should have thrown');
      } catch (e: any) {
        assert.ok(e.message.includes('line 1'));
        assert.ok(e.message.includes('col'));
      }
    });

    test('should provide path info in errors', () => {
      try {
        parseInferred('[1, 2.5]');
        assert.fail('Should have thrown');
      } catch (e: any) {
        assert.ok(e.message.includes('[1]'));
      }
    });
  });

  describe('complex nested structures', () => {
    test('should infer array of structs', () => {
      const [type, value] = parseInferred('[(x=1, y=2), (x=3, y=4)]');
      const expectedType = ArrayType(StructType({ x: IntegerType, y: IntegerType }));
      assert.ok(isTypeEqual(type, expectedType));
      assert.deepEqual(value, [
        { x: 1n, y: 2n },
        { x: 3n, y: 4n }
      ]);
    });

    test('should infer dict with struct values', () => {
      const [type, value] = parseInferred('{"alice":(age=30, active=true),"bob":(age=25, active=false)}');
      const expectedType = DictType(
        StringType,
        StructType({ age: IntegerType, active: BooleanType })
      );
      assert.ok(isTypeEqual(type, expectedType));
      assert.deepEqual(value.get('alice'), { age: 30n, active: true });
      assert.deepEqual(value.get('bob'), { age: 25n, active: false });
    });

    test('should infer struct with variant field', () => {
      const [type, value] = parseInferred('(status=.success, code=200)');
      const expectedType = StructType({
        status: VariantType({ success: NullType }),
        code: IntegerType
      });
      assert.ok(isTypeEqual(type, expectedType));
      assert.equal(value.status.type, 'success');
      assert.equal(value.code, 200n);
    });
  });

  describe('whitespace handling', () => {
    test('should handle leading whitespace', () => {
      const [type, value] = parseInferred('  42  ');
      assert.ok(isTypeEqual(type, IntegerType));
      assert.equal(value, 42n);
    });

    test('should handle whitespace in arrays', () => {
      const [type, value] = parseInferred('[ 1 , 2 , 3 ]');
      assert.ok(isTypeEqual(type, ArrayType(IntegerType)));
      assert.deepEqual(value, [1n, 2n, 3n]);
    });

    test('should handle whitespace in structs', () => {
      const [type, value] = parseInferred('( x = 1 , y = 2 )');
      const expectedType = StructType({ x: IntegerType, y: IntegerType });
      assert.ok(isTypeEqual(type, expectedType));
      assert.deepEqual(value, { x: 1n, y: 2n });
    });
  });

  describe('frozen parameter', () => {
    test('should freeze arrays when frozen=true', () => {
      const [_type, value] = parseInferred('[1, 2, 3]', true);
      assert.ok(Object.isFrozen(value));
    });

    test('should freeze sets when frozen=true', () => {
      const [_type, value] = parseInferred('{1,2,3}', true);
      assert.ok(Object.isFrozen(value));
    });

    test('should freeze dicts when frozen=true', () => {
      const [_type, value] = parseInferred('{"a":1}', true);
      assert.ok(Object.isFrozen(value));
    });

    test('should freeze structs when frozen=true', () => {
      const [_type, value] = parseInferred('(x=1)', true);
      assert.ok(Object.isFrozen(value));
    });

    test('should not freeze when frozen=false', () => {
      const [_type, value] = parseInferred('[1, 2, 3]', false);
      assert.ok(!Object.isFrozen(value));
    });
  });
});
