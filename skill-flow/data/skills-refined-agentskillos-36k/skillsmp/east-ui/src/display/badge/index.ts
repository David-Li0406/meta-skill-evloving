/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType,
    variant,
} from "@elaraai/east";

import { SizeType, ColorSchemeType, StyleVariantType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import { BadgeType, type BadgeStyle } from "./types.js";

// Re-export types
export { BadgeType, type BadgeStyle } from "./types.js";

// ============================================================================
// Badge Function
// ============================================================================

/**
 * Creates a Badge component with value and optional styling.
 *
 * @param value - The badge text content
 * @param style - Optional styling configuration
 * @returns An East expression representing the badge component
 *
 * @remarks
 * Badge is used to display short labels, counts, or status indicators.
 * Common uses include notification counts, status labels, and category tags.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Badge, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Badge.Root("Active", {
 *         colorPalette: "green",
 *         variant: "solid",
 *     });
 * });
 * ```
 */
function createBadge(
    value: SubtypeExprOrValue<StringType>,
    style?: BadgeStyle
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), StyleVariantType)
            : style.variant)
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

    return East.value(variant("Badge", {
        value: value,
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
        colorPalette: colorPaletteValue ? variant("some", colorPaletteValue) : variant("none", null),
        size: sizeValue ? variant("some", sizeValue) : variant("none", null),
        opacity: style?.opacity !== undefined ? variant("some", style.opacity) : variant("none", null),
        color: style?.color ? variant("some", style.color) : variant("none", null),
        background: style?.background ? variant("some", style.background) : variant("none", null),
    }), UIComponentType);
}

/**
 * Badge component for displaying short labels, counts, or status indicators.
 *
 * @remarks
 * Use `Badge.Root(value, style)` to create a badge, or access `Badge.Types.Badge` for the East type.
 */
export const Badge = {
    /**
     * Creates a Badge component with value and optional styling.
     *
     * @param value - The badge text content
     * @param style - Optional styling configuration
     * @returns An East expression representing the badge component
     *
     * @remarks
     * Badge is used to display short labels, counts, or status indicators.
     * Common uses include notification counts, status labels, and category tags.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Badge, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Badge.Root("Active", {
     *         colorPalette: "green",
     *         variant: "solid",
     *     });
     * });
     * ```
     */
    Root: createBadge,
    Types: {
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
         */
        Badge: BadgeType,
    },
} as const;
