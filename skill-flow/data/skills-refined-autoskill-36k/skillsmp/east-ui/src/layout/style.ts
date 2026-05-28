/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    type ExprType,
    OptionType,
    StringType,
    StructType,
    East,
    some,
    none,
} from "@elaraai/east";

// ============================================================================
// Padding Type
// ============================================================================

/**
 * Padding configuration with individual side control.
 *
 * @remarks
 * Allows specifying padding for each side independently using Chakra UI
 * spacing tokens or CSS values.
 *
 * @property top - Top padding
 * @property right - Right padding
 * @property bottom - Bottom padding
 * @property left - Left padding
 */
export const PaddingType = StructType({
    top: OptionType(StringType),
    right: OptionType(StringType),
    bottom: OptionType(StringType),
    left: OptionType(StringType),
});

/**
 * Type representing the Padding structure.
 */
export type PaddingType = typeof PaddingType;

/**
 * TypeScript interface for padding configuration.
 */
export interface PaddingConfig {
    /** Top padding (Chakra UI spacing token or CSS value) */
    top?: SubtypeExprOrValue<StringType>;
    /** Right padding (Chakra UI spacing token or CSS value) */
    right?: SubtypeExprOrValue<StringType>;
    /** Bottom padding (Chakra UI spacing token or CSS value) */
    bottom?: SubtypeExprOrValue<StringType>;
    /** Left padding (Chakra UI spacing token or CSS value) */
    left?: SubtypeExprOrValue<StringType>;
}

/**
 * Creates a padding configuration.
 *
 * @param padding - An object with individual sides
 * @returns An East expression representing the padding configuration
 *
 * @example
 * ```ts
 *
 * // Individual sides
 * Padding({ top: "2", bottom: "4" })
 *
 * // Horizontal/vertical shorthand
 * Padding({ top: "2", bottom: "2", left: "4", right: "4" })
 * ```
 */
export function Padding(padding: PaddingConfig): ExprType<PaddingType> {
    return East.value({
        top: padding.top !== undefined ? some(padding.top) : none,
        right: padding.right !== undefined ? some(padding.right) : none,
        bottom: padding.bottom !== undefined ? some(padding.bottom) : none,
        left: padding.left !== undefined ? some(padding.left) : none,
    }, PaddingType);
}

// ============================================================================
// Margin Type
// ============================================================================

/**
 * Margin configuration with individual side control.
 *
 * @remarks
 * Allows specifying margin for each side independently using Chakra UI
 * spacing tokens or CSS values.
 *
 * @property top - Top margin
 * @property right - Right margin
 * @property bottom - Bottom margin
 * @property left - Left margin
 */
export const MarginType = StructType({
    top: OptionType(StringType),
    right: OptionType(StringType),
    bottom: OptionType(StringType),
    left: OptionType(StringType),
});

/**
 * Type representing the Margin structure.
 */
export type MarginType = typeof MarginType;

/**
 * TypeScript interface for margin configuration.
 */
export interface MarginConfig {
    /** Top margin (Chakra UI spacing token or CSS value) */
    top?: SubtypeExprOrValue<StringType>;
    /** Right margin (Chakra UI spacing token or CSS value) */
    right?: SubtypeExprOrValue<StringType>;
    /** Bottom margin (Chakra UI spacing token or CSS value) */
    bottom?: SubtypeExprOrValue<StringType>;
    /** Left margin (Chakra UI spacing token or CSS value) */
    left?: SubtypeExprOrValue<StringType>;
}

/**
 * Creates a margin configuration.
 *
 * @param margin - An object with individual sides
 * @returns An East expression representing the margin configuration
 *
 * @example
 * ```ts
 * // Individual sides
 * Margin({ top: "2", bottom: "4" })
 *
 * // Horizontal/vertical shorthand
 * Margin({ top: "2", bottom: "2", left: "4", right: "4" })
 * ```
 */
export function Margin(margin: MarginConfig): ExprType<MarginType> {
    return East.value({
        top: margin.top !== undefined ? some(margin.top) : none,
        right: margin.right !== undefined ? some(margin.right) : none,
        bottom: margin.bottom !== undefined ? some(margin.bottom) : none,
        left: margin.left !== undefined ? some(margin.left) : none,
    }, MarginType);
}
