/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    OptionType,
    StructType,
    FloatType,
    BooleanType,
    NullType,
    VariantType,
    FunctionType,
    variant,
} from "@elaraai/east";

import { SizeType, ColorSchemeType, OrientationType } from "../../style.js";
import type { SizeLiteral, ColorSchemeLiteral, OrientationLiteral } from "../../style.js";

// ============================================================================
// Slider Variant Type
// ============================================================================

/**
 * Variant types for Slider visual style.
 *
 * @property outline - Slider with outlined track
 * @property subtle - Slider with subtle/filled track
 */
export const SliderVariantType = VariantType({
    /** Slider with outlined track */
    outline: NullType,
    /** Slider with subtle/filled track */
    subtle: NullType,
});

/**
 * Type representing the SliderVariant structure.
 */
export type SliderVariantType = typeof SliderVariantType;

/**
 * String literal type for slider variant values.
 */
export type SliderVariantLiteral = "outline" | "subtle";

/**
 * Helper function to create slider variant values.
 *
 * @param v - The variant string ("outline" or "subtle")
 * @returns An East expression representing the slider variant
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Slider, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Slider.Root(50.0, {
 *         variant: Slider.Variant("subtle"),
 *     });
 * });
 * ```
 */
export function SliderVariant(v: "outline" | "subtle"): ExprType<SliderVariantType> {
    return East.value(variant(v, null), SliderVariantType);
}

// ============================================================================
// Slider Type
// ============================================================================

/**
 * Type for Slider component data.
 *
 * @remarks
 * Slider is a form control for selecting a numeric value within a range.
 *
 * @property value - Current slider value
 * @property min - Minimum value (defaults to 0)
 * @property max - Maximum value (defaults to 100)
 * @property step - Step increment for value changes
 * @property orientation - Horizontal or vertical orientation
 * @property colorPalette - Color scheme for the slider
 * @property size - Size of the slider
 * @property variant - Visual variant (outline or subtle)
 * @property disabled - Whether the slider is disabled
 * @property onChange - Callback triggered when value changes (during drag)
 * @property onChangeEnd - Callback triggered when drag ends
 */
export const SliderType = StructType({
    value: FloatType,
    min: OptionType(FloatType),
    max: OptionType(FloatType),
    step: OptionType(FloatType),
    orientation: OptionType(OrientationType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    variant: OptionType(SliderVariantType),
    disabled: OptionType(BooleanType),
    onChange: OptionType(FunctionType([FloatType], NullType)),
    onChangeEnd: OptionType(FunctionType([FloatType], NullType)),
});

/**
 * Type representing the Slider structure.
 */
export type SliderType = typeof SliderType;

// ============================================================================
// Slider Style
// ============================================================================

/**
 * TypeScript interface for Slider style options.
 *
 * @property min - Minimum value (defaults to 0)
 * @property max - Maximum value (defaults to 100)
 * @property step - Step increment for value changes
 * @property orientation - Horizontal or vertical orientation
 * @property colorPalette - Color scheme for the slider
 * @property size - Size of the slider
 * @property variant - Visual variant (outline or subtle)
 * @property disabled - Whether the slider is disabled
 * @property onChange - Callback triggered when value changes (during drag)
 * @property onChangeEnd - Callback triggered when drag ends
 */
export interface SliderStyle {
    /** Minimum value (defaults to 0) */
    min?: SubtypeExprOrValue<FloatType>;
    /** Maximum value (defaults to 100) */
    max?: SubtypeExprOrValue<FloatType>;
    /** Step increment for value changes */
    step?: SubtypeExprOrValue<FloatType>;
    /** Horizontal or vertical orientation */
    orientation?: SubtypeExprOrValue<OrientationType> | OrientationLiteral;
    /** Color scheme for the slider */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the slider */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Visual variant (outline or subtle) */
    variant?: SubtypeExprOrValue<SliderVariantType> | SliderVariantLiteral;
    /** Whether the slider is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when value changes (during drag) */
    onChange?: SubtypeExprOrValue<FunctionType<[FloatType], NullType>>;
    /** Callback triggered when drag ends */
    onChangeEnd?: SubtypeExprOrValue<FunctionType<[FloatType], NullType>>;
}
