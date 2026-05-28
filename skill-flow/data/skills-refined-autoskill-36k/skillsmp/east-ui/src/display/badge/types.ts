/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    StringType,
    FloatType,
} from "@elaraai/east";

import { SizeType, ColorSchemeType, StyleVariantType } from "../../style.js";
import type { SizeLiteral, ColorSchemeLiteral, StyleVariantLiteral } from "../../style.js";

// ============================================================================
// Badge Type
// ============================================================================

/**
 * Type for Badge component data.
 *
 * @remarks
 * Badge displays short labels, counts, or status indicators.
 *
 * @property value - The badge text content
 * @property variant - Visual variant (solid, subtle, outline)
 * @property colorPalette - Color scheme for the badge
 * @property size - Size of the badge
 * @property opacity - CSS opacity (0-1)
 * @property color - Custom text color (overrides colorPalette)
 * @property background - Custom background color (overrides colorPalette)
 */
export const BadgeType = StructType({
    value: StringType,
    variant: OptionType(StyleVariantType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    opacity: OptionType(FloatType),
    color: OptionType(StringType),
    background: OptionType(StringType),
});

/**
 * Type representing the Badge structure.
 */
export type BadgeType = typeof BadgeType;

// ============================================================================
// Badge Style
// ============================================================================

/**
 * TypeScript interface for Badge style options.
 *
 * @property variant - Visual variant (solid, subtle, outline)
 * @property colorPalette - Color scheme for the badge
 * @property size - Size of the badge
 * @property opacity - CSS opacity (0-1)
 * @property color - Custom text color (overrides colorPalette)
 * @property background - Custom background color (overrides colorPalette)
 */
export interface BadgeStyle {
    /** Visual variant (solid, subtle, outline) */
    variant?: SubtypeExprOrValue<StyleVariantType> | StyleVariantLiteral;
    /** Color scheme for the badge */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the badge */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** CSS opacity (0-1) */
    opacity?: SubtypeExprOrValue<FloatType>;
    /** Custom text color (overrides colorPalette) */
    color?: SubtypeExprOrValue<StringType>;
    /** Custom background color (overrides colorPalette) */
    background?: SubtypeExprOrValue<StringType>;
}
