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

import { TextAlignType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import { HeadingType, HeadingSizeType, HeadingAsType, type HeadingStyle } from "./types.js";

// Re-export types
export { HeadingType, HeadingSizeType, HeadingAsType, type HeadingStyle } from "./types.js";

// ============================================================================
// Heading Component
// ============================================================================

/**
 * Creates a Heading component for semantic headings.
 *
 * @param value - The heading text
 * @param style - Optional styling configuration
 * @returns An East expression representing the heading component
 */
function createHeading(
    value: SubtypeExprOrValue<StringType>,
    style?: HeadingStyle
): ExprType<UIComponentType> {
    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), HeadingSizeType)
            : style.size)
        : undefined;

    const asValue = style?.as
        ? (typeof style.as === "string"
            ? East.value(variant(style.as, null), HeadingAsType)
            : style.as)
        : undefined;

    const textAlignValue = style?.textAlign
        ? (typeof style.textAlign === "string"
            ? East.value(variant(style.textAlign, null), TextAlignType)
            : style.textAlign)
        : undefined;

    return East.value(variant("Heading", {
        value: value,
        size: sizeValue ? variant("some", sizeValue) : variant("none", null),
        as: asValue ? variant("some", asValue) : variant("none", null),
        color: style?.color ? variant("some", style.color) : variant("none", null),
        textAlign: textAlignValue ? variant("some", textAlignValue) : variant("none", null),
    }), UIComponentType);
}

/**
 * Heading component for semantic HTML headings.
 *
 * @remarks
 * Use `Heading.Root(value, style)` to create headings with semantic HTML elements.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Heading, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Heading.Root("Welcome", {
 *         size: "2xl",
 *         as: "h1",
 *         color: "blue.600",
 *     });
 * });
 * ```
 */
export const Heading = {
    Root: createHeading,
    Types: {
        Heading: HeadingType,
        Size: HeadingSizeType,
        As: HeadingAsType,
    },
} as const;
