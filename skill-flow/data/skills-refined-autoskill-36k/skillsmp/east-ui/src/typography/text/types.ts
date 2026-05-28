/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StringType,
    StructType,
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
import type {
    BorderStyleLiteral,
    BorderWidthLiteral,
    FontStyleLiteral,
    FontWeightLiteral,
    OverflowLiteral,
    SizeLiteral,
    TextAlignLiteral,
    TextOverflowLiteral,
    TextTransformLiteral,
    WhiteSpaceLiteral,
} from "../../style.js";

// ============================================================================
// Text Type
// ============================================================================

/**
 * The concrete East type for Text component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for a Text component.
 * All style properties are wrapped in OptionType to handle presence/absence.
 *
 * @property value - The text value
 * @property color - Optional text color (Chakra UI color token or CSS color)
 * @property background - Optional background color
 * @property fontWeight - Optional font weight variant
 * @property fontStyle - Optional font style variant
 * @property textTransform - Optional text transform variant
 * @property textAlign - Optional text alignment variant
 * @property borderWidth - Optional border width variant
 * @property borderStyle - Optional border style variant
 * @property borderColor - Optional border color
 */
export const TextType = StructType({
    value: StringType,
    color: OptionType(StringType),
    background: OptionType(StringType),
    fontWeight: OptionType(FontWeightType),
    fontStyle: OptionType(FontStyleType),
    fontSize: OptionType(SizeType),
    textTransform: OptionType(TextTransformType),
    textAlign: OptionType(TextAlignType),
    textOverflow: OptionType(TextOverflowType),
    whiteSpace: OptionType(WhiteSpaceType),
    overflow: OptionType(OverflowType),
    borderWidth: OptionType(BorderWidthType),
    borderStyle: OptionType(BorderStyleType),
    borderColor: OptionType(StringType),
});

/**
 * Type representing the Text component structure.
 */
export type TextType = typeof TextType;

// ============================================================================
// Text Style
// ============================================================================

/**
 * Style configuration for Text components.
 *
 * @remarks
 * All style properties are optional and accept either static values or East expressions
 * for dynamic styling. Color properties accept Chakra UI color tokens (e.g., "blue.500")
 * or CSS color values.
 *
 * @property color - Text color (Chakra UI color token or CSS color)
 * @property background - Background color
 * @property fontWeight - Font weight variant
 * @property fontStyle - Font style variant
 * @property textTransform - Text transform variant
 * @property textAlign - Horizontal text alignment
 * @property borderWidth - Border width for all sides
 * @property borderStyle - Border style for all sides
 * @property borderColor - Border color for all sides
 */
export type TextStyle = {
    /** Text color (Chakra UI color token or CSS color) */
    color?: SubtypeExprOrValue<StringType>;
    /** Background color */
    background?: SubtypeExprOrValue<StringType>;
    /** Font weight variant */
    fontWeight?: SubtypeExprOrValue<FontWeightType> | FontWeightLiteral;
    /** Font style variant */
    fontStyle?: SubtypeExprOrValue<FontStyleType> | FontStyleLiteral;
    /** Font size */
    fontSize?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Text transform variant */
    textTransform?: SubtypeExprOrValue<TextTransformType> | TextTransformLiteral;
    /** Horizontal text alignment */
    textAlign?: SubtypeExprOrValue<TextAlignType> | TextAlignLiteral;
    /** Text overflow behavior (clip or ellipsis) */
    textOverflow?: SubtypeExprOrValue<TextOverflowType> | TextOverflowLiteral;
    /** White space handling (normal, nowrap, pre, etc.) */
    whiteSpace?: SubtypeExprOrValue<WhiteSpaceType> | WhiteSpaceLiteral;
    /** Overflow behavior (visible, hidden, scroll, auto) */
    overflow?: SubtypeExprOrValue<OverflowType> | OverflowLiteral;
    /** Border width for all sides */
    borderWidth?: SubtypeExprOrValue<BorderWidthType> | BorderWidthLiteral;
    /** Border style for all sides */
    borderStyle?: SubtypeExprOrValue<BorderStyleType> | BorderStyleLiteral;
    /** Border color for all sides (Chakra UI color token or CSS color) */
    borderColor?: SubtypeExprOrValue<StringType>;
};
