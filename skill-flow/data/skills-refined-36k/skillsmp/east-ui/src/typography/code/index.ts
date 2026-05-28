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

import { SizeType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import { CodeType, CodeVariantType, type CodeStyle } from "./types.js";

// Re-export types
export { CodeType, CodeVariantType, type CodeStyle } from "./types.js";

// ============================================================================
// Code Component
// ============================================================================

/**
 * Creates a Code component for displaying inline code.
 *
 * @param value - The code text to display
 * @param style - Optional styling configuration
 * @returns An East expression representing the code component
 */
function createCode(
    value: SubtypeExprOrValue<StringType>,
    style?: CodeStyle
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), CodeVariantType)
            : style.variant)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), SizeType)
            : style.size)
        : undefined;

    return East.value(variant("Code", {
        value: value,
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
        colorPalette: style?.colorPalette ? variant("some", style.colorPalette) : variant("none", null),
        size: sizeValue ? variant("some", sizeValue) : variant("none", null),
    }), UIComponentType);
}

/**
 * Code component for displaying inline code snippets.
 *
 * @remarks
 * Use `Code.Root(value, style)` to create inline code display.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Code, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Code.Root("const x = 42", {
 *         colorPalette: "purple",
 *         variant: "surface",
 *     });
 * });
 * ```
 */
export const Code = {
    Root: createCode,
    Types: {
        Code: CodeType,
        Variant: CodeVariantType,
    },
} as const;
