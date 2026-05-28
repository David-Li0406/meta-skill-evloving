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
    FunctionType,
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import type { SizeLiteral, ColorSchemeLiteral } from "../../style.js";

// ============================================================================
// Button Variant Type
// ============================================================================

/**
 * Variant type for Button appearance styles.
 *
 * @remarks
 * Create instances using string literals like "solid", "outline", etc.
 *
 * @property solid - Solid filled button (default)
 * @property subtle - Subtle/light background button
 * @property outline - Outlined button with border
 * @property ghost - Transparent button, visible on hover
 */
export const ButtonVariantType = VariantType({
    solid: NullType,
    subtle: NullType,
    outline: NullType,
    ghost: NullType,
});

/**
 * Type representing button variant values.
 */
export type ButtonVariantType = typeof ButtonVariantType;

/**
 * String literal type for button variant values.
 */
export type ButtonVariantLiteral = "solid" | "subtle" | "outline" | "ghost";

// ============================================================================
// Button Style Type
// ============================================================================

/**
 * Style type for Button component configuration.
 *
 * @remarks
 * This struct type defines the styling configuration for a Button component.
 *
 * @property variant - Button appearance variant (solid, subtle, outline, ghost)
 * @property colorPalette - Color scheme for the button
 * @property size - Size of the button (xs, sm, md, lg)
 * @property loading - Whether the button shows a loading state
 * @property disabled - Whether the button is disabled
 * @property onClick - Callback triggered when the button is clicked
 */
export const ButtonStyleType = StructType({
    variant: OptionType(ButtonVariantType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    loading: OptionType(BooleanType),
    disabled: OptionType(BooleanType),
    onClick: OptionType(FunctionType([], NullType)),
});

/**
 * Type representing the Button style structure.
 */
export type ButtonStyleType = typeof ButtonStyleType;

/**
 * TypeScript interface for Button style options.
 *
 * @remarks
 * Use this interface when creating Button components.
 *
 * @property variant - Button appearance variant
 * @property colorPalette - Color scheme for theming
 * @property size - Size of the button
 * @property loading - Shows loading spinner when true
 * @property disabled - Disables button interaction when true
 * @property onClick - Callback triggered when the button is clicked
 */
export interface ButtonStyle {
    /** Button appearance variant (solid, subtle, outline, ghost) */
    variant?: SubtypeExprOrValue<ButtonVariantType> | ButtonVariantLiteral;
    /** Color scheme for theming */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the button */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Shows loading spinner when true */
    loading?: SubtypeExprOrValue<BooleanType>;
    /** Disables button interaction when true */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when the button is clicked */
    onClick?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}

// ============================================================================
// Button Type
// ============================================================================

/**
 * The concrete East type for Button component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for a Button component.
 *
 * @property label - The text displayed on the button
 * @property style - Optional styling configuration wrapped in OptionType
 */
export const ButtonType = StructType({
    label: StringType,
    style: OptionType(ButtonStyleType),
});

/**
 * Type representing the Button component structure.
 */
export type ButtonType = typeof ButtonType;
