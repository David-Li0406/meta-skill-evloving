/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import sorted_btree from "sorted-btree";

// Deal with CJS default import
const BTree = sorted_btree.default;
type BTree<K, T> = sorted_btree.default<K, T>;

/**
 * A sorted map implementation using a B-tree data structure.
 *
 * @typeParam K - The type of keys in the map
 * @typeParam T - The type of values in the map
 *
 * @remarks
 * Implements the ES6 `Map` interface with additional capabilities:
 * - Maintains entries in sorted order by key based on a comparison function
 * - Supports {@link minKey} and {@link maxKey} for accessing key extrema
 * - Provides range-based iteration starting from any key
 * - Respects frozen state and throws errors on modification attempts
 * - Includes static {@link groupBy} method for aggregation operations
 *
 * Used to implement East's {@link DictType} with total ordering semantics.
 */
export class SortedMap<K, T> implements Map<K, T> {
    private btree: BTree<K, T>;

    /**
     * Creates a new SortedMap.
     *
     * @param values - Optional initial entries as `[key, value]` pairs
     * @param compare - Optional comparison function for ordering keys
     *
     * @remarks
     * If no comparison function is provided, keys are compared using default ordering.
     */
    constructor(values?: Iterable<[K,T]>, compare?: (a: K, b: K) => number) {
        this.btree = new BTree(undefined, compare);
        if (values !== undefined) {
            for (const [key, value] of values) {
                this.btree.set(key, value);
            }
        }
    }

    /** The number of key-value pairs in the map. */
    get size(): number {
        return this.btree.size;
    }

    /**
     * Retrieves the value associated with a key.
     *
     * @param key - The key to look up
     * @returns The associated value, or `undefined` if the key is not present
     */
    get(key: K): T | undefined {
        return this.btree.get(key);
    }

    /**
     * Associates a value with a key in the map.
     *
     * @param key - The key to set
     * @param value - The value to associate with the key
     * @returns This map for chaining
     * @throws {TypeError} When the map is frozen
     */
    set(key: K, value: T): this {
        if (Object.isFrozen(this)) {
            throw new TypeError("Cannot modify frozen SortedMap");
        }
        this.btree.set(key, value);
        return this;
    }

    /**
     * Removes all entries from the map.
     *
     * @throws {TypeError} When the map is frozen
     */
    clear(): void {
        if (Object.isFrozen(this)) {
            throw new TypeError("Cannot modify frozen SortedMap");
        }
        this.btree.clear();
    }

    /**
     * Removes a key-value pair from the map.
     *
     * @param value - The key to remove
     * @returns `true` if the key was present and removed, `false` otherwise
     * @throws {TypeError} When the map is frozen
     */
    delete(value: K): boolean {
        if (Object.isFrozen(this)) {
            throw new TypeError("Cannot modify frozen SortedMap");
        }
        return this.btree.delete(value);
    }

    /**
     * Checks if a key exists in the map.
     *
     * @param value - The key to check
     * @returns `true` if the key is present, `false` otherwise
     */
    has(value: K): boolean {
        return this.btree.has(value);
    }

    /**
     * Executes a callback for each entry in the map, in sorted order by key.
     *
     * @param callbackfn - Function to execute for each entry
     * @param thisArg - Value to use as `this` when executing the callback
     *
     * @remarks
     * The callback receives the value, key, and map (in that order for ES6 Map compatibility).
     */
    forEach(callbackfn: (value: T, key: K, set: Map<K, T>) => void, thisArg?: any): void {
        for (const [key, value] of this.btree.entries()) {
            callbackfn.call(thisArg, value, key, this);
        }
    }

    /**
     * Returns the smallest key in the map.
     *
     * @returns The minimum key, or `undefined` if the map is empty
     *
     * @remarks
     * This is an O(log n) operation due to the B-tree structure.
     */
    minKey(): K | undefined {
        return this.btree.minKey();
    }

    /**
     * Returns the largest key in the map.
     *
     * @returns The maximum key, or `undefined` if the map is empty
     *
     * @remarks
     * This is an O(log n) operation due to the B-tree structure.
     */
    maxKey(): K | undefined {
        return this.btree.maxKey();
    }

    /**
     * Returns an iterator over the map's keys in sorted order.
     *
     * @param firstKey - Optional starting key for range-based iteration
     * @returns An iterator yielding keys in sorted order
     *
     * @remarks
     * If `firstKey` is provided, iteration starts from that key (or the next key if not present).
     * This enables efficient range queries over sorted data.
     */
    keys(firstKey?: K | undefined): MapIterator<K> {
        return Iterator.from(this.btree.keys(firstKey)) as MapIterator<K>;
    }

    /**
     * Returns an iterator over the map's values in key-sorted order.
     *
     * @param firstKey - Optional starting key for range-based iteration
     * @returns An iterator yielding values in key-sorted order
     *
     * @remarks
     * Values are returned in the order of their sorted keys, not sorted by value.
     */
    values(firstKey?: K | undefined): MapIterator<T> {
        return Iterator.from(this.btree.values(firstKey)) as MapIterator<T>;
    }

    /**
     * Returns an iterator over the map's entries in sorted order by key.
     *
     * @param firstKey - Optional starting key for range-based iteration
     * @returns An iterator yielding `[key, value]` tuples in key-sorted order
     *
     * @remarks
     * If `firstKey` is provided, iteration starts from that key.
     */
    entries(firstKey?: K | undefined): MapIterator<[K, T]> {
        const gen = (function* (btree: BTree<K, T>): IterableIterator<[K, T]> {
            for (const [key, value] of btree.entries(firstKey)) {
                yield [key, value];
            }
        })(this.btree);
        return Iterator.from(gen) as MapIterator<[K, T]>;
    }

    /**
     * Returns an iterator over the map's entries in sorted order by key.
     *
     * @returns An iterator yielding `[key, value]` tuples in key-sorted order
     *
     * @remarks
     * Makes {@link SortedMap} iterable with `for...of` loops.
     */
    [Symbol.iterator](): MapIterator<[K, T]> {
        return Iterator.from(this.btree.entries()) as MapIterator<[K, T]>;
    }

    /** Returns the string tag for this object type. */
    get [Symbol.toStringTag](): string {
        return "SortedMap";
    }

    /**
     * Groups items into a sorted map based on a key selector function.
     *
     * @typeParam K - The type of keys to group by
     * @typeParam T - The type of items to group
     * @param items - The items to group
     * @param keySelector - Function that extracts the grouping key from each item
     * @param compare - Optional comparison function for ordering keys
     * @returns A {@link SortedMap} where each key maps to an array of items with that key
     *
     * @remarks
     * This is a convenient aggregation function similar to SQL's `GROUP BY`.
     * Items with the same key are collected into arrays in the order they appear.
     *
     * @example
     * ```ts
     * const people = [
     *   { name: "Alice", age: 30 },
     *   { name: "Bob", age: 25 },
     *   { name: "Charlie", age: 30 }
     * ];
     * const byAge = SortedMap.groupBy(people, p => p.age);
     * // Result: Map { 25 => [{name:"Bob",age:25}], 30 => [{name:"Alice",age:30}, {name:"Charlie",age:30}] }
     * ```
     */
    static groupBy<K, T>(items: Iterable<T>, keySelector: (item: T) => K, compare?: (a: K, b: K) => number): SortedMap<K, T[]> {
        const map = new SortedMap<K, T[]>(undefined, compare);
        for (const item of items) {
            const key = keySelector(item);
            const group = map.get(key);
            if (group === undefined) {
                map.set(key, [item]);
            } else {
                group.push(item);
            }
        }
        return map;
    }
}