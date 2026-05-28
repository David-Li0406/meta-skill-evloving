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
} from "@elaraai/east";

// ============================================================================
// Mark Variant Type
// ============================================================================

/**
 * Mark variant type for different highlight styles.
 *
 * @property subtle - Subtle highlight effect
 * @property solid - Solid colored highlight
 * @property text - Text-color only highlight
 * @property plain - Plain mark styling
 */
export const MarkVariantType = VariantType({
    subtle: NullType,
    solid: NullType,
    text: NullType,
    plain: NullType,
});

export type MarkVariantType = typeof MarkVariantType;
export type MarkVariantLiteral = "subtle" | "solid" | "text" | "plain";

// ============================================================================
// Mark Type
// ============================================================================

/**
 * The concrete East type for Mark component data.
 *
 * @property value - The text to mark/highlight
 * @property variant - Visual style variant
 * @property colorPalette - Color scheme for the mark
 */
export const MarkType = StructType({
    value: StringType,
    variant: OptionType(MarkVariantType),
    colorPalette: OptionType(StringType),
});

export type MarkType = typeof MarkType;

// ============================================================================
// Mark Style
// ============================================================================

/**
 * Style configuration for Mark components.
 */
export type MarkStyle = {
    /** Visual style variant */
    variant?: SubtypeExprOrValue<MarkVariantType> | MarkVariantLiteral;
    /** Color palette (e.g., "yellow", "green") */
    colorPalette?: SubtypeExprOrValue<StringType>;
};
