/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    type ExprType,
    East,
    StringType,
    variant,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { MarkType, MarkVariantType, type MarkStyle } from "./types.js";

// Re-export types
export { MarkType, MarkVariantType, type MarkStyle } from "./types.js";

// ============================================================================
// Mark Component
// ============================================================================

/**
 * Creates a Mark component for highlighted text (like HTML mark element).
 *
 * @param value - The text to mark/highlight
 * @param style - Optional styling configuration
 * @returns An East expression representing the mark component
 */
function createMark(
    value: SubtypeExprOrValue<StringType>,
    style?: MarkStyle
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), MarkVariantType)
            : style.variant)
        : undefined;

    return East.value(variant("Mark", {
        value: value,
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
        colorPalette: style?.colorPalette ? variant("some", style.colorPalette) : variant("none", null),
    }), UIComponentType);
}

/**
 * Mark component for highlighted/marked text.
 *
 * @remarks
 * Use `Mark.Root(value, style)` to create marked text similar to HTML `<mark>`.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Mark, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Mark.Root("Important text", {
 *         colorPalette: "yellow",
 *         variant: "subtle",
 *     });
 * });
 * ```
 */
export const Mark = {
    Root: createMark,
    Types: {
        Mark: MarkType,
        Variant: MarkVariantType,
    },
} as const;
