/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    VariantType,
    OptionType,
    StructType,
    StringType,
    BooleanType,
    NullType,
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import type { SizeLiteral, ColorSchemeLiteral } from "../../style.js";

// ============================================================================
// CopyButton Variant Type
// ============================================================================

/**
 * Variant type for CopyButton appearance styles.
 *
 * @remarks
 * Create instances using string literals like "solid", "outline", etc.
 *
 * @property solid - Solid filled button (default)
 * @property subtle - Subtle/light background button
 * @property outline - Outlined button with border
 * @property ghost - Transparent button, visible on hover
 */
export const CopyButtonVariantType = VariantType({
    solid: NullType,
    subtle: NullType,
    outline: NullType,
    ghost: NullType,
});

/**
 * Type representing copy button variant values.
 */
export type CopyButtonVariantType = typeof CopyButtonVariantType;

/**
 * String literal type for copy button variant values.
 */
export type CopyButtonVariantLiteral = "solid" | "subtle" | "outline" | "ghost";

// ============================================================================
// CopyButton Style Type
// ============================================================================

/**
 * Style type for CopyButton component configuration.
 *
 * @remarks
 * This struct type defines the styling configuration for a CopyButton component.
 *
 * @property variant - Button appearance variant (solid, subtle, outline, ghost)
 * @property colorPalette - Color scheme for the button
 * @property size - Size of the button (xs, sm, md, lg)
 * @property disabled - Whether the button is disabled
 * @property timeout - Duration in ms to show "copied" state (default: 2000)
 */
export const CopyButtonStyleType = StructType({
    variant: OptionType(CopyButtonVariantType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    disabled: OptionType(BooleanType),
    timeout: OptionType(StringType),
});

/**
 * Type representing the CopyButton style structure.
 */
export type CopyButtonStyleType = typeof CopyButtonStyleType;

/**
 * TypeScript interface for CopyButton style options.
 *
 * @remarks
 * Use this interface when creating CopyButton components.
 *
 * @property variant - Button appearance variant
 * @property colorPalette - Color scheme for theming
 * @property size - Size of the button
 * @property disabled - Disables button interaction when true
 * @property timeout - Duration in ms to show "copied" state (default: 2000)
 */
export interface CopyButtonStyle {
    /** Button appearance variant (solid, subtle, outline, ghost) */
    variant?: SubtypeExprOrValue<CopyButtonVariantType> | CopyButtonVariantLiteral;
    /** Color scheme for theming */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the button */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Disables button interaction when true */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Duration in ms to show "copied" state (default: 2000) */
    timeout?: SubtypeExprOrValue<StringType>;
}

// ============================================================================
// CopyButton Type
// ============================================================================

/**
 * The concrete East type for CopyButton component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for a CopyButton component.
 *
 * @property value - The text value to copy to clipboard (required)
 * @property label - Optional label text to display on the button
 * @property style - Optional styling configuration wrapped in OptionType
 */
export const CopyButtonType = StructType({
    value: StringType,
    label: OptionType(StringType),
    style: OptionType(CopyButtonStyleType),
});

/**
 * Type representing the CopyButton component structure.
 */
export type CopyButtonType = typeof CopyButtonType;
