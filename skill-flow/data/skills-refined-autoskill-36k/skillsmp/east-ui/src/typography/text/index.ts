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

import {
    BorderStyleType,
    BorderWidthType,
    FontStyleType,
    FontWeightType,
    OverflowType,
    SizeType,
    TextAlignType,
    TextOverflowType,
    TextTransformType,
    WhiteSpaceType,
} from "../../style.js";
import { UIComponentType } from "../../component.js";
import { TextType, type TextStyle } from "./types.js";

// Re-export types
export { TextType, type TextStyle } from "./types.js";

// ============================================================================
// Text Component
// ============================================================================

/**
 * Creates a Text component with a value and optional styling.
 *
 * @param value - The text value as a string or East expression
 * @param style - Optional styling configuration for the text
 * @returns An East expression representing the styled text component
 */
function createText(
    value: SubtypeExprOrValue<StringType>,
    style?: TextStyle
): ExprType<UIComponentType> {
    const fontWeightValue = style?.fontWeight
        ? (typeof style.fontWeight === "string"
            ? East.value(variant(style.fontWeight, null), FontWeightType)
            : style.fontWeight)
        : undefined;

    const fontStyleValue = style?.fontStyle
        ? (typeof style.fontStyle === "string"
            ? East.value(variant(style.fontStyle, null), FontStyleType)
            : style.fontStyle)
        : undefined;

    const fontSize = style?.fontSize
        ? (typeof style.fontSize === "string"
            ? East.value(variant(style.fontSize, null), SizeType)
            : style.fontSize)
        : undefined;

    const textTransformValue = style?.textTransform
        ? (typeof style.textTransform === "string"
            ? East.value(variant(style.textTransform, null), TextTransformType)
            : style.textTransform)
        : undefined;

    const textAlignValue = style?.textAlign
        ? (typeof style.textAlign === "string"
            ? East.value(variant(style.textAlign, null), TextAlignType)
            : style.textAlign)
        : undefined;

    const borderWidthValue = style?.borderWidth
        ? (typeof style.borderWidth === "string"
            ? East.value(variant(style.borderWidth, null), BorderWidthType)
            : style.borderWidth)
        : undefined;

    const borderStyleValue = style?.borderStyle
        ? (typeof style.borderStyle === "string"
            ? East.value(variant(style.borderStyle, null), BorderStyleType)
            : style.borderStyle)
        : undefined;

    const textOverflowValue = style?.textOverflow
        ? (typeof style.textOverflow === "string"
            ? East.value(variant(style.textOverflow, null), TextOverflowType)
            : style.textOverflow)
        : undefined;

    const whiteSpaceValue = style?.whiteSpace
        ? (typeof style.whiteSpace === "string"
            ? East.value(variant(style.whiteSpace, null), WhiteSpaceType)
            : style.whiteSpace)
        : undefined;

    const overflowValue = style?.overflow
        ? (typeof style.overflow === "string"
            ? East.value(variant(style.overflow, null), OverflowType)
            : style.overflow)
        : undefined;

    return East.value(variant("Text", {
        value: value,
        color: style?.color ? variant("some", style.color) : variant("none", null),
        background: style?.background ? variant("some", style.background) : variant("none", null),
        fontWeight: fontWeightValue ? variant("some", fontWeightValue) : variant("none", null),
        fontStyle: fontStyleValue ? variant("some", fontStyleValue) : variant("none", null),
        fontSize: fontSize ? variant("some", fontSize) : variant("none", null),
        textTransform: textTransformValue ? variant("some", textTransformValue) : variant("none", null),
        textAlign: textAlignValue ? variant("some", textAlignValue) : variant("none", null),
        textOverflow: textOverflowValue ? variant("some", textOverflowValue) : variant("none", null),
        whiteSpace: whiteSpaceValue ? variant("some", whiteSpaceValue) : variant("none", null),
        overflow: overflowValue ? variant("some", overflowValue) : variant("none", null),
        borderWidth: borderWidthValue ? variant("some", borderWidthValue) : variant("none", null),
        borderStyle: borderStyleValue ? variant("some", borderStyleValue) : variant("none", null),
        borderColor: style?.borderColor ? variant("some", style.borderColor) : variant("none", null),
    }), UIComponentType);
}

/**
 * Text component for displaying styled text content.
 *
 * @remarks
 * Use `Text.Root(value, style)` to create text, or access `Text.Types.Text` for the East type.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Text.Root("Hello World", {
 *         color: "blue.500",
 *         fontWeight: "bold",
 *     });
 * });
 * ```
 */
export const Text = {
    /**
     * Creates a Text component for displaying styled text content.
     *
     * @param value - The text string to display
     * @param style - Optional styling configuration
     * @returns An East expression representing the text component
     */
    Root: createText,
    Types: {
        /**
         * The concrete East type for Text component data.
         *
         * @property value - The text string content
         * @property color - Text color (Chakra UI color token or CSS color)
         * @property fontWeight - Font weight (normal, bold, semibold, etc.)
         * @property fontSize - Font size (xs, sm, md, lg, xl, etc.)
         * @property textAlign - Text alignment (left, center, right, justify)
         */
        Text: TextType,
    },
} as const;
