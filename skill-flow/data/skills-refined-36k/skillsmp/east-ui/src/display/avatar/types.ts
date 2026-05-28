/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    StringType,
    OptionType,
    StructType,
} from "@elaraai/east";

import { ColorSchemeType, StyleVariantType, SizeType } from "../../style.js";
import type { ColorSchemeLiteral, StyleVariantLiteral, SizeLiteral } from "../../style.js";

// ============================================================================
// Avatar Type
// ============================================================================

/**
 * Type for Avatar component data.
 *
 * @remarks
 * Avatar displays user profile images or initials/icons as fallback.
 *
 * @property src - Image URL for the avatar
 * @property name - User name (used for initials fallback)
 * @property size - Size of the avatar
 * @property variant - Visual variant (solid, subtle, outline)
 * @property colorPalette - Color scheme for fallback avatar
 */
export const AvatarType = StructType({
    src: OptionType(StringType),
    name: OptionType(StringType),
    size: OptionType(SizeType),
    variant: OptionType(StyleVariantType),
    colorPalette: OptionType(ColorSchemeType),
});

/**
 * Type representing the Avatar structure.
 */
export type AvatarType = typeof AvatarType;

// ============================================================================
// Avatar Style
// ============================================================================

/**
 * TypeScript interface for Avatar style options.
 *
 * @property src - Image URL for the avatar
 * @property name - User name (used for initials fallback)
 * @property size - Size of the avatar
 * @property variant - Visual variant (solid, subtle, outline)
 * @property colorPalette - Color scheme for fallback avatar
 */
export interface AvatarStyle {
    /** Image URL for the avatar */
    src?: SubtypeExprOrValue<StringType>;
    /** User name (used for initials fallback) */
    name?: SubtypeExprOrValue<StringType>;
    /** Size of the avatar */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Visual variant (solid, subtle, outline) */
    variant?: SubtypeExprOrValue<StyleVariantType> | StyleVariantLiteral;
    /** Color scheme for fallback avatar */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
}
