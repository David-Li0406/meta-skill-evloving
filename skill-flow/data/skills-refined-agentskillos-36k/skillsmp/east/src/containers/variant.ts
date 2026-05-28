/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 *
 * @remarks
 */
export const variant_symbol = Symbol("variant");
export type variant_symbol = typeof variant_symbol;

/**
 * Represents a sum-type value with a type tag and associated value.
 *
 * @typeParam Type - The type of the discriminant tag
 * @typeParam Value - The type of the associated value
 *
 * @remarks
 * Variants are immutable and use nominal typing via the brand symbol.
 * This is the foundation for East's variant types (sum types).
 */
export type variant<Type = string, Value = any> = {
    /** The discriminant tag identifying which variant case this is */
    type: Type,
    /** The value associated with this variant case */
    value: Value,
    /** Brand symbol for nominal typing */
    [variant_symbol]: null,
};

/**
 * Constructs a sum-type value with a specific type tag and associated value.
 *
 * @typeParam Type - The string literal type of the discriminant tag
 * @typeParam Value - The type of the value to associate with this variant
 * @param type - The discriminant tag for this variant
 * @param value - The value to associate with this variant
 * @returns A branded variant object
 *
 * @example
 * ```ts
 * const success = variant("success", { data: [1, 2, 3] });
 * const error = variant("error", "Connection failed");
 * ```
 */
export function variant<Type extends string, Value = null>(type: Type, value: Value = null as Value): variant<Type, Value> {
    return {
        type,
        value,
        [variant_symbol]: null,
    };
};

/**
 * Deconstructs a variant by pattern matching on its type tag.
 *
 * @typeParam V - The variant type to match against, must have `type` and `value` properties
 * @typeParam Fs - Object type mapping each variant case to its handler function
 * @typeParam Default - The type of the default value when handler is optional
 *
 * @param variant - The variant to match against
 * @param fs - Object mapping type tags to handler functions
 * @param defaultValue - Optional default value if no handler matches
 * @returns The result of calling the matching handler function
 *
 * @remarks
 * This function has two overloads:
 * 1. All handlers required - returns the handler's return type
 * 2. Handlers optional with default - returns handler return type or default type
 *
 * The type system ensures exhaustive matching when all handlers are provided,
 * and allows partial matching when a default value is supplied.
 *
 * @example
 * ```ts
 * // Exhaustive matching (all cases required)
 * const result = match(maybeValue, {
 *   some: (v) => v * 2,
 *   none: () => 0
 * });
 *
 * // Partial matching with default
 * const result = match(response, {
 *   success: (data) => data.length
 * }, -1);
 * ```
 */
export function match<
    V extends { type: string, value: any },
    Fs extends { [K in V["type"]]: (value: (V & { type: K })["value"]) => any }
>(variant: V, fs: Fs, defaultValue?: any): ReturnType<Fs[V["type"]]>
export function match<
    V extends { type: string, value: any },
    Fs extends { [K in V["type"]]?: (value: (V & { type: K })["value"]) => any },
    Default extends any
>(variant: V, fs: Fs, defaultValue: Default): ReturnType<Exclude<Fs[keyof Fs], undefined>> | Default
export function match(e: variant, fs: { [K in string]: (value: never) => any }, d?: any) {
    const f = (fs as any)[e.type];
    if (f === undefined) return d;
    return f(e.value);
};

/**
 * Represents the absence of a value in an Option type.
 *
 * @remarks
 * This is a singleton value representing the "none" case of the Option pattern.
 */
export const none = variant("none", null);
export type none = typeof none;

/**
 * Wraps a value in the "some" case of an Option type.
 *
 * @typeParam T - The type of the value to wrap
 * @param value - The value to wrap
 * @returns A variant tagged as "some" containing the value
 *
 * @example
 * ```ts
 * const maybeNumber = some(42);
 * const result = match(maybeNumber, {
 *   some: (n) => n * 2,
 *   none: () => 0
 * }); // returns 84
 * ```
 */
export function some<T>(value: T) {
    return variant("some", value);
}
export type some<T> = variant<"some", T>;

/**
 * Represents an optional value that may be present (some) or absent (none).
 *
 * @typeParam T - The type of the value when present
 *
 * @remarks
 * This is East's standard approach to representing nullable values safely.
 * Use with the `match` function for exhaustive pattern matching.
 */
export type option<T> = none | some<T>;

/** Check if a value is a variant */
export function isVariant(v: any): v is variant {
    return typeof v === "object" && v !== null && v[variant_symbol] === null;
}