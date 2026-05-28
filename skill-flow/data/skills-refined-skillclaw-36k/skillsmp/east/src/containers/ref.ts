/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 *
 * @remarks
 */
export const ref_symbol = Symbol("ref");
export type ref_symbol = typeof ref_symbol;

/**
 * Represents a mutable reference cell containing a value.
 *
 * @typeParam T - The type of the value contained in the ref-cell
 *
 * @remarks
 * Ref-cells are mutable containers with identity semantics.
 * They use nominal typing via the brand symbol and support aliasing in serialization.
 * Refs are invariant in the type system - you cannot substitute a `ref<Subtype>` for `ref<Supertype>`.
 */
export type ref<T = any> = {
    /** The mutable value contained in this ref-cell */
    value: T,
    /** Brand symbol for nominal typing */
    [ref_symbol]: null,
};

/**
 * Creates a new mutable reference cell containing the specified value.
 *
 * @typeParam T - The type of the value to store
 * @param value - The initial value to store in the ref-cell
 * @returns A branded ref-cell object
 *
 * @example
 * ```ts
 * const counter = ref(0);
 * setRef(counter, deref(counter) + 1);
 * console.log(deref(counter)); // 1
 * ```
 *
 * @example
 * ```ts
 * // Refs have identity semantics - multiple refs can point to the same object
 * const original = ref([1, 2, 3]);
 * const alias = original; // Same ref-cell
 * setRef(alias, [4, 5, 6]);
 * console.log(deref(original)); // [4, 5, 6]
 * ```
 */
export function ref<T>(value: T): ref<T> {
    return {
        value,
        [ref_symbol]: null,
    };
}

/**
 * Checks if a value is a ref-cell.
 *
 * @param v - The value to check
 * @returns `true` if the value is a ref-cell, `false` otherwise
 *
 * @example
 * ```ts
 * const r = ref(42);
 * console.log(isRef(r)); // true
 * console.log(isRef(42)); // false
 * console.log(isRef({ value: 42 })); // false
 * ```
 */
export function isRef(v: any): v is ref<unknown> {
    return typeof v === "object" && v !== null && v[ref_symbol] === null;
}

/**
 * Retrieves the current value from a ref-cell.
 *
 * @typeParam T - The type of the value in the ref-cell
 * @param r - The ref-cell to dereference
 * @returns The current value stored in the ref-cell
 *
 * @example
 * ```ts
 * const counter = ref(10);
 * console.log(deref(counter)); // 10
 * ```
 */
export function deref<T>(r: ref<T>): T {
    return r.value;
}

/**
 * Updates the value stored in a ref-cell.
 *
 * @typeParam T - The type of the value in the ref-cell
 * @param r - The ref-cell to update
 * @param value - The new value to store
 *
 * @remarks
 * This mutates the ref-cell in place. All aliases to the same ref-cell will see the updated value.
 *
 * @example
 * ```ts
 * const counter = ref(0);
 * setRef(counter, 1);
 * setRef(counter, deref(counter) + 1);
 * console.log(deref(counter)); // 2
 * ```
 *
 * @example
 * ```ts
 * // Aliasing - both variables point to the same ref-cell
 * const r1 = ref("hello");
 * const r2 = r1;
 * setRef(r2, "world");
 * console.log(deref(r1)); // "world"
 * ```
 */
export function setRef<T>(r: ref<T>, value: T): void {
    r.value = value;
}
