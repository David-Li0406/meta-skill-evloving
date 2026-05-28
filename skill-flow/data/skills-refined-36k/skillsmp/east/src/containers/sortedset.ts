/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */
import sorted_btree from "sorted-btree";

// Deal with CJS default import
const BTree = sorted_btree.default;
type BTree<K, T> = sorted_btree.default<K, T>;

// Note: Enhanced SetIterator types from ES2024 aren't fully stabilized in TypeScript yet
// Using type assertions as temporary workaround until tooling catches up

/**
 * A sorted set implementation using a B-tree data structure.
 *
 * @typeParam K - The type of keys stored in the set
 *
 * @remarks
 * Implements the ES6 `Set` interface with additional capabilities:
 * - Maintains keys in sorted order based on a comparison function
 * - Supports {@link minKey} and {@link maxKey} for accessing extrema
 * - Provides range-based iteration starting from any key
 * - Implements ES2024 set operations (union, intersection, difference, etc.)
 * - Respects frozen state and throws errors on modification attempts
 *
 * Used to implement East's {@link SetType} with total ordering semantics.
 */
export class SortedSet<K> implements Set<K> {
    private btree: BTree<K, undefined>;

    /**
     * Creates a new SortedSet.
     *
     * @param values - Optional initial values to add to the set
     * @param compare - Optional comparison function for ordering keys
     *
     * @remarks
     * If no comparison function is provided, keys are compared using default ordering.
     */
    constructor(values?: Iterable<K>, private compare?: (a: K, b: K) => number) {
        this.btree = new BTree(undefined, compare);
        if (values !== undefined) {
            for (const value of values) {
                this.btree.set(value, undefined);
            }
        }
    }

    /** The number of elements in the set. */
    get size(): number {
        return this.btree.size;
    }

    /**
     * Adds a value to the set.
     *
     * @param value - The value to add
     * @returns This set for chaining
     * @throws {TypeError} When the set is frozen
     */
    add(value: K): this {
        if (Object.isFrozen(this)) {
            throw new TypeError("Cannot modify frozen SortedSet");
        }
        this.btree.set(value, undefined);
        return this;
    }

    /**
     * Removes all elements from the set.
     *
     * @throws {TypeError} When the set is frozen
     */
    clear(): void {
        if (Object.isFrozen(this)) {
            throw new TypeError("Cannot modify frozen SortedSet");
        }
        this.btree.clear();
    }

    /**
     * Removes a value from the set.
     *
     * @param value - The value to remove
     * @returns `true` if the value was present and removed, `false` otherwise
     * @throws {TypeError} When the set is frozen
     */
    delete(value: K): boolean {
        if (Object.isFrozen(this)) {
            throw new TypeError("Cannot modify frozen SortedSet");
        }
        return this.btree.delete(value);
    }

    /**
     * Checks if a value exists in the set.
     *
     * @param value - The value to check
     * @returns `true` if the value is present, `false` otherwise
     */
    has(value: K): boolean {
        return this.btree.has(value);
    }

    /**
     * Executes a callback for each value in the set, in sorted order.
     *
     * @param callbackfn - Function to execute for each element
     * @param thisArg - Value to use as `this` when executing the callback
     *
     * @remarks
     * The callback receives the value twice (for ES6 Set compatibility) and the set itself.
     */
    forEach(callbackfn: (value: K, value2: K, set: Set<K>) => void, thisArg?: any): void {
        for (const key of this.btree.keys()) {
            callbackfn.call(thisArg, key, key, this);
        }
    }

    /**
     * Returns a new set containing all elements from this set and another.
     *
     * @typeParam U - The type of elements in the other set
     * @param other - The set to union with
     * @returns A new {@link SortedSet} containing all elements from both sets
     */
    union<U>(other: ReadonlySetLike<U>): SortedSet<K | U> {
        // Note: ReadonlySetLike.keys() returns an Iterator<U> (not Iterable),
        // so we must consume it manually rather than using for..of.
        const result = new SortedSet<K | U>(undefined, this.compare as any);
        for (const key of this.btree.keys()) {
            result.add(key as K | U);
        }
        const it = other.keys();
        for (let n = it.next(); !n.done; n = it.next()) {
            result.add(n.value as K | U);
        }
        return result;
    }

    /**
     * Returns a new set containing only elements present in both sets.
     *
     * @typeParam U - The type of elements in the other set
     * @param other - The set to intersect with
     * @returns A new {@link SortedSet} containing common elements
     */
    intersection<U>(other: ReadonlySetLike<U>): SortedSet<K & U> {
        const result = new SortedSet<K & U>(undefined, this.compare as any);
        const it = other.keys();
        for (let n = it.next(); !n.done; n = it.next()) {
            const key = n.value as K & U;
            if (this.has(key)) {
                result.add(key);
            }
        }
        return result;
    }

    /**
     * Returns a new set containing elements in this set but not in another.
     *
     * @typeParam U - The type of elements in the other set
     * @param other - The set to subtract
     * @returns A new {@link SortedSet} with elements only in this set
     */
    difference<U>(other: ReadonlySetLike<U>): SortedSet<K> {
        const result = new SortedSet<K>(undefined, this.compare);
        for (const key of this.btree.keys()) {
            if (!other.has(key as unknown as U)) {
                result.add(key);
            }
        }
        return result;
    }

    /**
     * Returns a new set containing elements in either set but not both.
     *
     * @typeParam U - The type of elements in the other set
     * @param other - The set to compare with
     * @returns A new {@link SortedSet} with elements exclusive to each set
     */
    symmetricDifference<U>(other: ReadonlySetLike<U>): SortedSet<K | U> {
        const result = new SortedSet<K | U>(undefined, this.compare as any);
        for (const key of this.btree.keys()) {
            if (!other.has(key as unknown as U)) {
                result.add(key as K | U);
            }
        }
        const it = other.keys();
        for (let n = it.next(); !n.done; n = it.next()) {
            const key = n.value as K | U;
            if (!this.has(key as K)) {
                result.add(key);
            }
        }
        return result;
    }

    /**
     * Checks if this set is a subset of another set.
     *
     * @param other - The potential superset
     * @returns `true` if all elements of this set are in the other set
     */
    isSubsetOf(other: ReadonlySetLike<unknown>): boolean {
        for (const key of this.btree.keys()) {
            if (!other.has(key)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Checks if this set is a superset of another set.
     *
     * @param other - The potential subset
     * @returns `true` if all elements of the other set are in this set
     */
    isSupersetOf(other: ReadonlySetLike<unknown>): boolean {
        const it = other.keys();
        for (let n = it.next(); !n.done; n = it.next()) {
            if (!this.has(n.value as K)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Checks if this set has no elements in common with another set.
     *
     * @param other - The set to compare with
     * @returns `true` if the sets share no elements, `false` otherwise
     */
    isDisjointFrom(other: ReadonlySetLike<unknown>): boolean {
        for (const key of this.btree.keys()) {
            if (other.has(key)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Returns the smallest value in the set.
     *
     * @returns The minimum value, or `undefined` if the set is empty
     *
     * @remarks
     * This is an O(log n) operation due to the B-tree structure.
     */
    minKey(): K | undefined {
        return this.btree.minKey();
    }

    /**
     * Returns the largest value in the set.
     *
     * @returns The maximum value, or `undefined` if the set is empty
     *
     * @remarks
     * This is an O(log n) operation due to the B-tree structure.
     */
    maxKey(): K | undefined {
        return this.btree.maxKey();
    }

    /**
     * Returns an iterator over the set's keys in sorted order.
     *
     * @param firstKey - Optional starting key for range-based iteration
     * @returns An iterator yielding keys in sorted order
     *
     * @remarks
     * If `firstKey` is provided, iteration starts from that key (or the next key if not present).
     * This enables efficient range queries over sorted data.
     */
    keys(firstKey?: K | undefined): SetIterator<K> {
        return Iterator.from(this.btree.keys(firstKey)) as SetIterator<K>;
    }

    /**
     * Returns an iterator over the set's values in sorted order.
     *
     * @param firstKey - Optional starting key for range-based iteration
     * @returns An iterator yielding values in sorted order
     *
     * @remarks
     * Identical to {@link keys} for sets (values and keys are the same).
     */
    values(firstKey?: K | undefined): SetIterator<K> {
        return Iterator.from(this.btree.keys(firstKey)) as SetIterator<K>;
    }

    /**
     * Returns an iterator over the set's entries in sorted order.
     *
     * @param firstKey - Optional starting key for range-based iteration
     * @returns An iterator yielding `[key, key]` tuples in sorted order
     *
     * @remarks
     * For ES6 Set compatibility, entries are `[key, key]` tuples.
     * If `firstKey` is provided, iteration starts from that key.
     */
    entries(firstKey?: K | undefined): SetIterator<[K, K]> {
        const gen = (function* (btree: BTree<K, undefined>) {
            for (const key of btree.keys(firstKey)) {
                yield [key, key] as [K, K];
            }
        })(this.btree);
        return Iterator.from(gen) as SetIterator<[K, K]>;
    }

    /**
     * Returns an iterator over the set's values in sorted order.
     *
     * @returns An iterator yielding values in sorted order
     *
     * @remarks
     * Makes {@link SortedSet} iterable with `for...of` loops.
     */
    [Symbol.iterator](): SetIterator<K> {
        return Iterator.from(this.btree.keys()) as SetIterator<K>;
    }

    /** Returns the string tag for this object type. */
    get [Symbol.toStringTag](): string {
        return "SortedSet";
    }

}