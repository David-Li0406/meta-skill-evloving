/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StringType,
    StructType,
    VariantType,
    NullType,
    ArrayType,
} from "@elaraai/east";

// ============================================================================
// List Variant Type
// ============================================================================

/**
 * List variant type for ordered vs unordered lists.
 *
 * @property ordered - Numbered list (ol)
 * @property unordered - Bulleted list (ul)
 */
export const ListVariantType = VariantType({
    ordered: NullType,
    unordered: NullType,
});

export type ListVariantType = typeof ListVariantType;
export type ListVariantLiteral = "ordered" | "unordered";

// ============================================================================
// List Type
// ============================================================================

/**
 * The concrete East type for List component data.
 *
 * @property items - Array of list items
 * @property variant - Ordered or unordered list
 * @property gap - Spacing between items
 * @property colorPalette - Color scheme for list markers
 */
export const ListType = StructType({
    items: ArrayType(StringType),
    variant: OptionType(ListVariantType),
    gap: OptionType(StringType),
    colorPalette: OptionType(StringType),
});

export type ListType = typeof ListType;

// ============================================================================
// List Style
// ============================================================================

/**
 * Style configuration for List components.
 */
export type ListStyle = {
    /** Ordered or unordered list */
    variant?: SubtypeExprOrValue<ListVariantType> | ListVariantLiteral;
    /** Spacing between items */
    gap?: SubtypeExprOrValue<StringType>;
    /** Color palette for list markers */
    colorPalette?: SubtypeExprOrValue<StringType>;
};

