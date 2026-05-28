/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    FloatType,
    StringType,
    BooleanType,
    variant,
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import {
    ProgressType,
    ProgressVariantType,
    ProgressVariant,
    type ProgressStyle,
} from "./types.js";

// Re-export types
export {
    ProgressType,
    ProgressVariantType,
    ProgressVariant,
    type ProgressStyle,
    type ProgressVariantLiteral,
} from "./types.js";

// ============================================================================
// Progress Function
// ============================================================================

/**
 * Creates a Progress component with value and optional styling.
 *
 * @param value - Current progress value (between min and max)
 * @param style - Optional styling configuration
 * @returns An East expression representing the progress component
 *
 * @remarks
 * Progress is used to display the completion status of a task. It supports
 * striped and animated styles for visual feedback.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Progress, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Progress.Root(60.0, {
 *         colorPalette: "green",
 *         size: "md",
 *         striped: true,
 *     });
 * });
 * ```
 */
function createProgress(
    value: SubtypeExprOrValue<FloatType>,
    style?: ProgressStyle
): ExprType<UIComponentType> {
    const toFloatOption = (val: SubtypeExprOrValue<FloatType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const toBoolOption = (val: SubtypeExprOrValue<BooleanType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const toStringOption = (val: SubtypeExprOrValue<StringType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

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
            ? East.value(variant(style.variant, null), ProgressVariantType)
            : style.variant)
        : undefined;

    return East.value(variant("Progress", {
        value: value,
        min: toFloatOption(style?.min),
        max: toFloatOption(style?.max),
        colorPalette: colorPaletteValue ? variant("some", colorPaletteValue) : variant("none", null),
        size: sizeValue ? variant("some", sizeValue) : variant("none", null),
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
        striped: toBoolOption(style?.striped),
        animated: toBoolOption(style?.animated),
        label: toStringOption(style?.label),
        valueText: toStringOption(style?.valueText),
    }), UIComponentType);
}

/**
 * Progress component for displaying task completion status.
 *
 * @remarks
 * Use `Progress.Root(value, style)` to create a progress bar, or access `Progress.Types.Progress` for the East type.
 */
export const Progress = {
    /**
     * Creates a Progress component with value and optional styling.
     *
     * @param value - Current progress value (between min and max)
     * @param style - Optional styling configuration
     * @returns An East expression representing the progress component
     *
     * @remarks
     * Progress is used to display the completion status of a task. It supports
     * striped and animated styles for visual feedback.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Progress, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Progress.Root(60.0, {
     *         colorPalette: "green",
     *         size: "md",
     *         striped: true,
     *     });
     * });
     * ```
     */
    Root: createProgress,
    /**
     * Helper function to create progress variant values.
     *
     * @param v - The variant string ("outline" or "subtle")
     * @returns An East expression representing the progress variant
     */
    Variant: ProgressVariant,
    Types: {
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
        Progress: ProgressType,
        /**
         * Variant types for Progress visual style.
         *
         * @property outline - Progress bar with outlined track
         * @property subtle - Progress bar with subtle/filled track
         */
        Variant: ProgressVariantType,
    },
} as const;
