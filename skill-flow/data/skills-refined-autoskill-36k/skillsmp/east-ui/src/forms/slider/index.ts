/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    FloatType,
    variant,
    some,
    none,
} from "@elaraai/east";

import { SizeType, ColorSchemeType, OrientationType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import { SliderType, SliderVariantType, SliderVariant, type SliderStyle } from "./types.js";

// Re-export types
export {
    SliderType,
    SliderVariantType,
    SliderVariant,
    type SliderStyle,
    type SliderVariantLiteral,
} from "./types.js";

// ============================================================================
// Slider Function
// ============================================================================

/**
 * Creates a Slider component with value and optional styling.
 *
 * @param value - Current slider value
 * @param style - Optional styling configuration
 * @returns An East expression representing the slider component
 *
 * @remarks
 * Slider is used for selecting numeric values within a range. It supports
 * custom min/max bounds, step increments, and can be oriented horizontally
 * or vertically.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Slider, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Slider.Root(50.0, {
 *         min: 0,
 *         max: 100,
 *         step: 5,
 *         colorPalette: "blue",
 *     });
 * });
 * ```
 */
export function createSlider_(
    value: SubtypeExprOrValue<FloatType>,
    style?: SliderStyle
): ExprType<SliderType> {
    const orientationValue = style?.orientation
        ? (typeof style.orientation === "string"
            ? East.value(variant(style.orientation, null), OrientationType)
            : style.orientation)
        : undefined;

    const colorPaletteValue = style?.colorPalette
        ? (typeof style.colorPalette === "string"
            ? East.value(variant(style.colorPalette, null), ColorSchemeType)
            : style.colorPalette)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), SizeType)
            : style.size)
        : undefined;

    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), SliderVariantType)
            : style.variant)
        : undefined;

    return East.value({
        value: value,
        min: style?.min !== undefined ? some(style.min) : none,
        max: style?.max !== undefined ? some(style.max) : none,
        step: style?.step !== undefined ? some(style.step) : none,
        orientation: orientationValue ? some(orientationValue) : none,
        colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
        size: sizeValue ? some(sizeValue) : none,
        variant: variantValue ? some(variantValue) : none,
        disabled: style?.disabled !== undefined ? some(style.disabled) : none,
        onChange: style?.onChange ? some(style.onChange) : none,
        onChangeEnd: style?.onChangeEnd ? some(style.onChangeEnd) : none,
    }, SliderType);
}

function createSlider(
    value: SubtypeExprOrValue<FloatType>,
    style?: SliderStyle
): ExprType<UIComponentType> {
    return East.value(variant("Slider", createSlider_(value, style)), UIComponentType);
}

/**
 * Slider component for numeric range selection.
 *
 * @remarks
 * Use `Slider.Root(value, style)` to create a slider, or access `Slider.Types.Slider` for the East type.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Slider, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Slider.Root(50.0, {
 *         min: 0,
 *         max: 100,
 *         step: 1,
 *         colorPalette: "blue",
 *     });
 * });
 * ```
 */
export const Slider = {
    Root: createSlider,
    Variant: SliderVariant,
    Types: {
        Slider: SliderType,
        Variant: SliderVariantType,
    },
} as const;
