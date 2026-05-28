const { test, describe } = require('node:test');
const assert = require('node:assert');
const { generateId, parseTags, isValidStatus, isValidPriority, isValidEffort } = require('../lib/utils.cjs');

describe('utils', () => {
  test('generateId creates padded ID', () => {
    assert.strictEqual(generateId(1), 't-001');
    assert.strictEqual(generateId(42), 't-042');
    assert.strictEqual(generateId(999), 't-999');
  });

  test('parseTags splits comma-separated string', () => {
    assert.deepStrictEqual(parseTags('a,b,c'), ['a', 'b', 'c']);
    assert.deepStrictEqual(parseTags('a, b , c'), ['a', 'b', 'c']);
    assert.deepStrictEqual(parseTags(''), []);
    assert.deepStrictEqual(parseTags(null), []);
  });

  test('isValidStatus validates status values', () => {
    assert.strictEqual(isValidStatus('pending'), true);
    assert.strictEqual(isValidStatus('in_progress'), true);
    assert.strictEqual(isValidStatus('completed'), true);
    assert.strictEqual(isValidStatus('blocked'), true);
    assert.strictEqual(isValidStatus('invalid'), false);
  });

  test('isValidPriority validates priority values', () => {
    assert.strictEqual(isValidPriority('low'), true);
    assert.strictEqual(isValidPriority('medium'), true);
    assert.strictEqual(isValidPriority('high'), true);
    assert.strictEqual(isValidPriority('critical'), true);
    assert.strictEqual(isValidPriority('invalid'), false);
  });

  test('isValidEffort validates effort values', () => {
    assert.strictEqual(isValidEffort('S'), true);
    assert.strictEqual(isValidEffort('M'), true);
    assert.strictEqual(isValidEffort('L'), true);
    assert.strictEqual(isValidEffort('XL'), true);
    assert.strictEqual(isValidEffort('invalid'), false);
  });
});
