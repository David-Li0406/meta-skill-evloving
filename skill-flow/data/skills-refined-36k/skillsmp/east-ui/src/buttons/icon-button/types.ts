/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    BooleanType,
    StringType,
    FunctionType,
    NullType,
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import type { SizeLiteral, ColorSchemeLiteral } from "../../style.js";
import { ButtonVariantType, type ButtonVariantLiteral } from "../button/types.js";

// Re-export ButtonVariantType for convenience
export { ButtonVariantType, type ButtonVariantLiteral } from "../button/types.js";

// ============================================================================
// IconButton Style Type
// ============================================================================

/**
 * Style type for IconButton component configuration.
 *
 * @remarks
 * IconButton shares the same style options as Button.
 *
 * @property variant - Button appearance variant (solid, subtle, outline, ghost)
 * @property colorPalette - Color scheme for the button
 * @property size - Size of the button (xs, sm, md, lg)
 * @property loading - Whether the button shows a loading state
 * @property disabled - Whether the button is disabled
 * @property onClick - Callback triggered when the button is clicked
 */
export const IconButtonStyleType = StructType({
    variant: OptionType(ButtonVariantType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    loading: OptionType(BooleanType),
    disabled: OptionType(BooleanType),
    onClick: OptionType(FunctionType([], NullType)),
});

/**
 * Type representing the IconButton style structure.
 */
export type IconButtonStyleType = typeof IconButtonStyleType;

/**
 * TypeScript interface for IconButton style options.
 *
 * @remarks
 * Use this interface when creating IconButton components.
 *
 * @property variant - Button appearance variant
 * @property colorPalette - Color scheme for theming
 * @property size - Size of the button
 * @property loading - Shows loading spinner when true
 * @property disabled - Disables button interaction when true
 * @property onClick - Callback triggered when the button is clicked
 */
export interface IconButtonStyle {
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
// IconButton Type
// ============================================================================

/**
 * The concrete East type for IconButton component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for an IconButton component.
 *
 * @property prefix - The Font Awesome icon prefix
 * @property name - The Font Awesome icon name
 * @property style - Optional styling configuration wrapped in OptionType
 */
export const IconButtonType = StructType({
    prefix: StringType,
    name: StringType,
    style: OptionType(IconButtonStyleType),
});

/**
 * Type representing the IconButton component structure.
 */
export type IconButtonType = typeof IconButtonType;
