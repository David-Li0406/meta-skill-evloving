/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    East,
    variant,
} from "@elaraai/east";

import { SeparatorStyleType, SeparatorVariantType, type SeparatorStyle } from "./types.js";
import { UIComponentType } from "../../component.js";
import { OrientationType, SizeType } from "../../style.js";

// Re-export style types
export { SeparatorStyleType, SeparatorVariantType, type SeparatorStyle } from "./types.js";

/**
 * The concrete East type for Separator component data.
 *
 * @remarks
 * Separator is a leaf component (no children) that provides a visual divider.
 */
export const SeparatorType = SeparatorStyleType;

/**
 * Type representing the Separator component structure.
 */
export type SeparatorType = typeof SeparatorType;

/**
 * Creates a Separator component for visual division between content.
 *
 * @param style - Optional styling configuration for the separator
 * @returns An East expression representing the separator component
 *
 * @remarks
 * Separator is a simple visual divider. By default it's horizontal.
 * Use orientation to create vertical separators in flex row layouts.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Separator, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Separator.Root({
 *         orientation: "horizontal",
 *         variant: "solid",
 *     });
 * });
 * ```
 */
function createSeparator(
    style?: SeparatorStyle
): ExprType<UIComponentType> {
    const orientationValue = style?.orientation
        ? (typeof style.orientation === "string"
            ? East.value(variant(style.orientation, null), OrientationType)
            : style.orientation)
        : undefined;

    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), SeparatorVariantType)
            : style.variant)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), SizeType)
            : style.size)
        : undefined;

    return East.value(variant("Separator", {
        orientation: orientationValue ? variant("some", orientationValue) : variant("none", null),
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
        size: sizeValue ? variant("some", sizeValue) : variant("none", null),
        color: style?.color ? variant("some", style.color) : variant("none", null),
        label: style?.label ? variant("some", style.label) : variant("none", null),
    }), UIComponentType);
}

/**
 * Separator component for visual division between content.
 *
 * @remarks
 * Use `Separator.Root(style)` to create a separator, or access `Separator.Types.Separator` for the East type.
 */
export const Separator = {
    /**
     * Creates a Separator component for visual division between content.
     *
     * @param style - Optional styling configuration for the separator
     * @returns An East expression representing the separator component
     *
     * @remarks
     * Separator is a simple visual divider. By default it's horizontal.
     * Use orientation to create vertical separators in flex row layouts.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Separator, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Separator.Root({
     *         orientation: "horizontal",
     *         variant: "solid",
     *     });
     * });
     * ```
     */
    Root: createSeparator,
    Types: {
        /**
         * The concrete East type for Separator component data.
         *
         * @remarks
         * Separator is a leaf component (no children) that provides a visual divider.
         */
        Separator: SeparatorType,
        /**
         * The concrete East type for Separator component style data.
         *
         * @remarks
         * All properties are optional and wrapped in {@link OptionType}.
         *
         * @property orientation - Orientation (horizontal or vertical)
         * @property variant - Line style variant (solid, dashed, dotted)
         * @property size - Thickness size
         * @property color - Color (Chakra UI color token or CSS color)
         * @property label - Optional label text in the middle of the separator
         */
        Style: SeparatorStyleType,
    },
} as const;
