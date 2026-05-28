/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    StringType,
    BooleanType,
    NullType,
    OptionType,
    StructType,
    VariantType,
    FunctionType,
    FloatType,
} from "@elaraai/east";

import { ColorSchemeType, StyleVariantType } from "../../style.js";
import type { ColorSchemeLiteral, StyleVariantLiteral } from "../../style.js";

// ============================================================================
// Tag Size Type
// ============================================================================

/**
 * Size variant type for Tag component.
 *
 * @remarks
 * Tag supports sm, md, lg, and xl sizes (no xs).
 *
 * @property sm - Small size
 * @property md - Medium size (default)
 * @property lg - Large size
 * @property xl - Extra large size
 */
export const TagSizeType = VariantType({
    sm: NullType,
    md: NullType,
    lg: NullType,
    xl: NullType,
});

/**
 * Type representing Tag size variant values.
 */
export type TagSizeType = typeof TagSizeType;

/**
 * String literal type for Tag sizes.
 */
export type TagSizeLiteral = "sm" | "md" | "lg" | "xl";

// ============================================================================
// Tag Type
// ============================================================================

/**
 * Type for Tag component data.
 *
 * @remarks
 * Tag is used for categorization, filtering, and labeling items.
 * Unlike Badge, Tags can be closable/removable.
 *
 * @property label - The tag text content
 * @property variant - Visual variant (solid, subtle, outline)
 * @property colorPalette - Color scheme for the tag
 * @property size - Size of the tag (sm, md, lg, xl)
 * @property closable - Whether the tag shows a close button
 * @property onClose - Callback triggered when close button is clicked
 * @property opacity - CSS opacity (0-1)
 * @property color - Custom text color (overrides colorPalette)
 * @property background - Custom background color (overrides colorPalette)
 */
export const TagType = StructType({
    label: StringType,
    variant: OptionType(StyleVariantType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(TagSizeType),
    closable: OptionType(BooleanType),
    onClose: OptionType(FunctionType([], NullType)),
    opacity: OptionType(FloatType),
    color: OptionType(StringType),
    background: OptionType(StringType),
});

/**
 * Type representing the Tag structure.
 */
export type TagType = typeof TagType;

// ============================================================================
// Tag Style
// ============================================================================

/**
 * TypeScript interface for Tag style options.
 *
 * @property variant - Visual variant (solid, subtle, outline)
 * @property colorPalette - Color scheme for the tag
 * @property size - Size of the tag (sm, md, lg, xl)
 * @property closable - Whether the tag shows a close button
 * @property onClose - Callback triggered when close button is clicked
 * @property opacity - CSS opacity (0-1)
 * @property color - Custom text color (overrides colorPalette)
 * @property background - Custom background color (overrides colorPalette)
 */
export interface TagStyle {
    /** Visual variant (solid, subtle, outline) */
    variant?: SubtypeExprOrValue<StyleVariantType> | StyleVariantLiteral;
    /** Color scheme for the tag */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the tag (sm, md, lg, xl) */
    size?: SubtypeExprOrValue<TagSizeType> | TagSizeLiteral;
    /** Whether the tag shows a close button */
    closable?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when close button is clicked */
    onClose?: SubtypeExprOrValue<FunctionType<[], NullType>>;
    /** CSS opacity (0-1) */
    opacity?: SubtypeExprOrValue<FloatType>;
    /** Custom text color (overrides colorPalette) */
    color?: SubtypeExprOrValue<StringType>;
    /** Custom background color (overrides colorPalette) */
    background?: SubtypeExprOrValue<StringType>;
}
