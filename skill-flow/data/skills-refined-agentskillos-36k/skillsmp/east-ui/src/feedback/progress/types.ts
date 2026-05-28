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
    StringType,
    BooleanType,
    NullType,
    VariantType,
    variant,
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import type { SizeLiteral, ColorSchemeLiteral } from "../../style.js";

// ============================================================================
// Progress Variant Type
// ============================================================================

/**
 * Variant types for Progress visual style.
 *
 * @remarks
 * Controls the visual appearance of the progress bar track.
 *
 * @property outline - Progress bar with outlined track
 * @property subtle - Progress bar with subtle/filled track
 */
export const ProgressVariantType = VariantType({
    /** Progress bar with outlined track */
    outline: NullType,
    /** Progress bar with subtle/filled track */
    subtle: NullType,
});

/**
 * Type representing the ProgressVariant structure.
 */
export type ProgressVariantType = typeof ProgressVariantType;

/**
 * String literal type for progress variant values.
 */
export type ProgressVariantLiteral = "outline" | "subtle";

/**
 * Helper function to create progress variant values.
 *
 * @param v - The variant string ("outline" or "subtle")
 * @returns An East expression representing the progress variant
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Progress, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Progress.Root(50.0, {
 *         variant: Progress.Variant("subtle"),
 *     });
 * });
 * ```
 */
export function ProgressVariant(v: "outline" | "subtle"): ExprType<ProgressVariantType> {
    return East.value(variant(v, null), ProgressVariantType);
}

// ============================================================================
// Progress Type
// ============================================================================

/**
 * Type for Progress component data.
 *
 * @remarks
 * Progress displays the completion status of a task or operation.
 *
 * @property value - Current progress value (between min and max)
 * @property min - Minimum value (defaults to 0)
 * @property max - Maximum value (defaults to 100)
 * @property colorPalette - Color scheme for the progress bar
 * @property size - Size of the progress bar
 * @property variant - Visual variant (outline or subtle)
 * @property striped - Whether to show striped pattern
 * @property animated - Whether to animate the progress bar
 * @property label - Optional label text
 * @property valueText - Optional text showing current value
 */
export const ProgressType = StructType({
    value: FloatType,
    min: OptionType(FloatType),
    max: OptionType(FloatType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    variant: OptionType(ProgressVariantType),
    striped: OptionType(BooleanType),
    animated: OptionType(BooleanType),
    label: OptionType(StringType),
    valueText: OptionType(StringType),
});

/**
 * Type representing the Progress structure.
 */
export type ProgressType = typeof ProgressType;

// ============================================================================
// Progress Style
// ============================================================================

/**
 * TypeScript interface for Progress style options.
 *
 * @property min - Minimum value (defaults to 0)
 * @property max - Maximum value (defaults to 100)
 * @property colorPalette - Color scheme for the progress bar
 * @property size - Size of the progress bar
 * @property variant - Visual variant (outline or subtle)
 * @property striped - Whether to show striped pattern
 * @property animated - Whether to animate the progress bar
 * @property label - Optional label text
 * @property valueText - Optional text showing current value
 */
export interface ProgressStyle {
    /** Minimum value (defaults to 0) */
    min?: SubtypeExprOrValue<FloatType>;
    /** Maximum value (defaults to 100) */
    max?: SubtypeExprOrValue<FloatType>;
    /** Color scheme for the progress bar */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the progress bar */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Visual variant (outline or subtle) */
    variant?: SubtypeExprOrValue<ProgressVariantType> | ProgressVariantLiteral;
    /** Whether to show striped pattern */
    striped?: SubtypeExprOrValue<BooleanType>;
    /** Whether to animate the progress bar */
    animated?: SubtypeExprOrValue<BooleanType>;
    /** Optional label text */
    label?: SubtypeExprOrValue<StringType>;
    /** Optional text showing current value */
    valueText?: SubtypeExprOrValue<StringType>;
}
