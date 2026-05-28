/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { SortedSet } from './sortedset.js';

describe('SortedSet', () => {
    test('should create empty set', () => {
        const set = new SortedSet<number>();
        assert.equal(set.size, 0);
    });

    test('should create set from iterable', () => {
        const set = new SortedSet<number>([3, 1, 2]);
        assert.equal(set.size, 3);
        assert.equal(set.has(1), true);
        assert.equal(set.has(2), true);
        assert.equal(set.has(3), true);
    });

    test('should add values', () => {
        const set = new SortedSet<string>();
        set.add('a');
        set.add('b');
        assert.equal(set.has('a'), true);
        assert.equal(set.has('b'), true);
        assert.equal(set.size, 2);
    });

    test('should not add duplicate values', () => {
        const set = new SortedSet<number>();
        set.add(1);
        set.add(1);
        assert.equal(set.size, 1);
    });

    test('should check value existence with has', () => {
        const set = new SortedSet<string>();
        set.add('a');
        assert.equal(set.has('a'), true);
        assert.equal(set.has('b'), false);
    });

    test('should delete values', () => {
        const set = new SortedSet<string>();
        set.add('a');
        set.add('b');
        assert.equal(set.delete('a'), true);
        assert.equal(set.has('a'), false);
        assert.equal(set.size, 1);
        assert.equal(set.delete('a'), false);
    });

    test('should clear all values', () => {
        const set = new SortedSet<string>();
        set.add('a');
        set.add('b');
        set.clear();
        assert.equal(set.size, 0);
        assert.equal(set.has('a'), false);
        assert.equal(set.has('b'), false);
    });

    test('should iterate in sorted order', () => {
        const set = new SortedSet<number>();
        set.add(3);
        set.add(1);
        set.add(2);

        const values = Array.from(set.values());
        assert.deepEqual(values, [1, 2, 3]);

        const keys = Array.from(set.keys());
        assert.deepEqual(keys, [1, 2, 3]);

        const entries = Array.from(set.entries());
        assert.deepEqual(entries, [[1, 1], [2, 2], [3, 3]]);
    });

    test('should use custom comparator', () => {
        // Reverse order comparator
        const set = new SortedSet<number>(undefined, (a, b) => b - a);
        set.add(1);
        set.add(2);
        set.add(3);

        const values = Array.from(set.values());
        assert.deepEqual(values, [3, 2, 1]);
    });

    test('should get min and max values', () => {
        const set = new SortedSet<number>();
        assert.equal(set.minKey(), undefined);
        assert.equal(set.maxKey(), undefined);

        set.add(5);
        set.add(1);
        set.add(9);

        assert.equal(set.minKey(), 1);
        assert.equal(set.maxKey(), 9);
    });

    test('should iterate from specific key', () => {
        const set = new SortedSet<number>();
        set.add(1);
        set.add(2);
        set.add(3);
        set.add(4);

        const valuesFrom2 = Array.from(set.values(2));
        assert.deepEqual(valuesFrom2, [2, 3, 4]);

        const keysFrom3 = Array.from(set.keys(3));
        assert.deepEqual(keysFrom3, [3, 4]);

        const entriesFrom2 = Array.from(set.entries(2));
        assert.deepEqual(entriesFrom2, [[2, 2], [3, 3], [4, 4]]);
    });

    test('should work with forEach', () => {
        const set = new SortedSet<number>();
        set.add(2);
        set.add(1);
        set.add(3);

        const collected: number[] = [];
        set.forEach((value, value2, s) => {
            assert.equal(value, value2);
            assert.equal(s, set);
            collected.push(value);
        });

        assert.deepEqual(collected, [1, 2, 3]);
    });

    test('should be iterable with Symbol.iterator', () => {
        const set = new SortedSet<number>();
        set.add(3);
        set.add(1);
        set.add(2);

        const values = [...set];
        assert.deepEqual(values, [1, 2, 3]);
    });

    test('should have correct Symbol.toStringTag', () => {
        const set = new SortedSet<number>();
        assert.equal(set[Symbol.toStringTag], 'SortedSet');
        assert.equal(Object.prototype.toString.call(set), '[object SortedSet]');
    });

    test('should prevent modification when frozen', () => {
        const set = new SortedSet<string>();
        set.add('a');
        Object.freeze(set);

        assert.throws(() => set.add('b'), TypeError);
        assert.throws(() => set.delete('a'), TypeError);
        assert.throws(() => set.clear(), TypeError);

        // Read operations should still work
        assert.equal(set.has('a'), true);
        assert.equal(set.size, 1);
    });

    test('should compute union of sets', () => {
        const set1 = new SortedSet<number>([1, 2, 3]);
        const set2 = new Set<number>([3, 4, 5]);

        const union = set1.union(set2);

        assert.equal(union.size, 5);
        const values = Array.from(union);
        assert.deepEqual(values, [1, 2, 3, 4, 5]);
    });

    test('should compute intersection of sets', () => {
        const set1 = new SortedSet<number>([1, 2, 3, 4]);
        const set2 = new Set<number>([3, 4, 5, 6]);

        const intersection = set1.intersection(set2);

        assert.equal(intersection.size, 2);
        const values = Array.from(intersection);
        assert.deepEqual(values, [3, 4]);
    });

    test('should compute difference of sets', () => {
        const set1 = new SortedSet<number>([1, 2, 3, 4]);
        const set2 = new Set<number>([3, 4, 5, 6]);

        const difference = set1.difference(set2);

        assert.equal(difference.size, 2);
        const values = Array.from(difference);
        assert.deepEqual(values, [1, 2]);
    });

    test('should compute symmetric difference of sets', () => {
        const set1 = new SortedSet<number>([1, 2, 3, 4]);
        const set2 = new Set<number>([3, 4, 5, 6]);

        const symDiff = set1.symmetricDifference(set2);

        assert.equal(symDiff.size, 4);
        const values = Array.from(symDiff);
        assert.deepEqual(values, [1, 2, 5, 6]);
    });

    test('should check if set is subset of another', () => {
        const set1 = new SortedSet<number>([2, 3]);
        const set2 = new Set<number>([1, 2, 3, 4]);
        const set3 = new Set<number>([2, 5]);

        assert.equal(set1.isSubsetOf(set2), true);
        assert.equal(set1.isSubsetOf(set3), false);
        assert.equal(set1.isSubsetOf(set1), true);
    });

    test('should check if set is superset of another', () => {
        const set1 = new SortedSet<number>([1, 2, 3, 4]);
        const set2 = new Set<number>([2, 3]);
        const set3 = new Set<number>([2, 5]);

        assert.equal(set1.isSupersetOf(set2), true);
        assert.equal(set1.isSupersetOf(set3), false);
        assert.equal(set1.isSupersetOf(set1), true);
    });

    test('should check if sets are disjoint', () => {
        const set1 = new SortedSet<number>([1, 2, 3]);
        const set2 = new Set<number>([4, 5, 6]);
        const set3 = new Set<number>([3, 4, 5]);

        assert.equal(set1.isDisjointFrom(set2), true);
        assert.equal(set1.isDisjointFrom(set3), false);
    });

    test('should handle empty set operations', () => {
        const empty = new SortedSet<number>();
        const set = new SortedSet<number>([1, 2, 3]);

        assert.deepEqual(Array.from(empty.union(set)), [1, 2, 3]);
        assert.equal(empty.intersection(set).size, 0);
        assert.equal(empty.difference(set).size, 0);
        assert.deepEqual(Array.from(empty.symmetricDifference(set)), [1, 2, 3]);
        assert.equal(empty.isSubsetOf(set), true);
        assert.equal(empty.isSupersetOf(set), false);
        assert.equal(empty.isDisjointFrom(set), true);
    });

    test('should preserve sort order in set operations', () => {
        const set1 = new SortedSet<number>([5, 3, 1]);
        const set2 = new Set<number>([6, 4, 2]);

        const union = set1.union(set2);
        assert.deepEqual(Array.from(union), [1, 2, 3, 4, 5, 6]);
    });

    test('should work with string values', () => {
        const set = new SortedSet<string>();
        set.add('banana');
        set.add('apple');
        set.add('cherry');

        const values = Array.from(set);
        assert.deepEqual(values, ['apple', 'banana', 'cherry']);
    });

    test('should handle single element sets', () => {
        const set = new SortedSet<number>([42]);

        assert.equal(set.size, 1);
        assert.equal(set.has(42), true);
        assert.equal(set.minKey(), 42);
        assert.equal(set.maxKey(), 42);
        assert.deepEqual(Array.from(set), [42]);
    });
});
