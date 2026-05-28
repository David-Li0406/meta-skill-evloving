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
    FlexDirectionType,
    JustifyContentType,
    AlignItemsType,
    FlexWrapType,
    OverflowType,
} from "../../style.js";
import type {
    FlexDirectionLiteral,
    JustifyContentLiteral,
    AlignItemsLiteral,
    FlexWrapLiteral,
    OverflowLiteral,
} from "../../style.js";
import { PaddingType, MarginType } from "../style.js";

// ============================================================================
// Flex Style
// ============================================================================

/**
 * Style configuration for Flex components.
 *
 * @remarks
 * All style properties are optional and accept either static values or East expressions
 * for dynamic styling. Size and spacing properties accept Chakra UI tokens or CSS values.
 * Flex is a Box with `display: flex` applied by default.
 *
 * @property direction - Flex direction (row, column, row-reverse, column-reverse)
 * @property wrap - Flex wrap behavior (nowrap, wrap, wrap-reverse)
 * @property justifyContent - Justify content for main axis alignment
 * @property alignItems - Align items for cross axis alignment
 * @property gap - Gap between children (Chakra UI spacing token or CSS value)
 * @property width - Width (Chakra UI size token or CSS value)
 * @property height - Height (Chakra UI size token or CSS value)
 * @property minHeight - Min height (Chakra UI size token or CSS value)
 * @property minWidth - Min width (Chakra UI size token or CSS value)
 * @property maxHeight - Max height (Chakra UI size token or CSS value)
 * @property maxWidth - Max width (Chakra UI size token or CSS value)
 * @property overflow - Overflow behavior for both axes (visible, hidden, scroll, auto)
 * @property overflowX - Horizontal overflow behavior (visible, hidden, scroll, auto)
 * @property overflowY - Vertical overflow behavior (visible, hidden, scroll, auto)
 * @property padding - Padding (Chakra UI spacing token or CSS value)
 * @property margin - Margin (Chakra UI spacing token or CSS value)
 * @property background - Background color (Chakra UI color token or CSS color)
 * @property color - Text color (Chakra UI color token or CSS color)
 * @property borderRadius - Border radius (Chakra UI radius token or CSS value)
 */
export type FlexStyle = {
    /** Flex direction (row, column, row-reverse, column-reverse) */
    direction?: SubtypeExprOrValue<FlexDirectionType> | FlexDirectionLiteral;
    /** Flex wrap behavior (nowrap, wrap, wrap-reverse) */
    wrap?: SubtypeExprOrValue<FlexWrapType> | FlexWrapLiteral;
    /** Justify content for main axis alignment */
    justifyContent?: SubtypeExprOrValue<JustifyContentType> | JustifyContentLiteral;
    /** Align items for cross axis alignment */
    alignItems?: SubtypeExprOrValue<AlignItemsType> | AlignItemsLiteral;
    /** Gap between children (Chakra UI spacing token or CSS value) */
    gap?: SubtypeExprOrValue<StringType>;
    /** Width (Chakra UI size token or CSS value) */
    width?: SubtypeExprOrValue<StringType>;
    /** Height (Chakra UI size token or CSS value) */
    height?: SubtypeExprOrValue<StringType>;
    /** Min height (Chakra UI size token or CSS value) */
    minHeight?: SubtypeExprOrValue<StringType>;
    /** Min width (Chakra UI size token or CSS value) */
    minWidth?: SubtypeExprOrValue<StringType>;
    /** Max height (Chakra UI size token or CSS value) */
    maxHeight?: SubtypeExprOrValue<StringType>;
    /** Max width (Chakra UI size token or CSS value) */
    maxWidth?: SubtypeExprOrValue<StringType>;
    /** Overflow behavior for both axes (visible, hidden, scroll, auto) */
    overflow?: SubtypeExprOrValue<OverflowType> | OverflowLiteral;
    /** Horizontal overflow behavior (visible, hidden, scroll, auto) */
    overflowX?: SubtypeExprOrValue<OverflowType> | OverflowLiteral;
    /** Vertical overflow behavior (visible, hidden, scroll, auto) */
    overflowY?: SubtypeExprOrValue<OverflowType> | OverflowLiteral;
    /** Padding configuration - use Padding() helper */
    padding?: SubtypeExprOrValue<PaddingType> | string;
    /** Margin configuration - use Margin() helper */
    margin?: SubtypeExprOrValue<MarginType> | string;
    /** Background color (Chakra UI color token or CSS color) */
    background?: SubtypeExprOrValue<StringType>;
    /** Text color (Chakra UI color token or CSS color) */
    color?: SubtypeExprOrValue<StringType>;
    /** Border radius (Chakra UI radius token or CSS value) */
    borderRadius?: SubtypeExprOrValue<StringType>;
    /** Border shorthand (CSS value, e.g., "1px solid gray.200") */
    border?: SubtypeExprOrValue<StringType>;
    /** Border color (Chakra UI color token or CSS color) */
    borderColor?: SubtypeExprOrValue<StringType>;
    /** Border width (CSS value, e.g., "1px", "2px") */
    borderWidth?: SubtypeExprOrValue<StringType>;
};

/**
 * The concrete East type for Flex component style data.
 *
 * @remarks
 * All properties are optional and wrapped in {@link OptionType}.
 * Flex is a Box with `display: flex` applied by default.
 *
 * @property direction - Flex direction (row, column, row-reverse, column-reverse)
 * @property wrap - Flex wrap behavior (nowrap, wrap, wrap-reverse)
 * @property justifyContent - Justify content for main axis alignment
 * @property alignItems - Align items for cross axis alignment
 * @property gap - Gap between children (Chakra UI spacing token or CSS value)
 * @property width - Width (Chakra UI size token or CSS value)
 * @property height - Height (Chakra UI size token or CSS value)
 * @property minHeight - Min height (Chakra UI size token or CSS value)
 * @property minWidth - Min width (Chakra UI size token or CSS value)
 * @property maxHeight - Max height (Chakra UI size token or CSS value)
 * @property maxWidth - Max width (Chakra UI size token or CSS value)
 * @property overflow - Overflow behavior for both axes (visible, hidden, scroll, auto)
 * @property overflowX - Horizontal overflow behavior (visible, hidden, scroll, auto)
 * @property overflowY - Vertical overflow behavior (visible, hidden, scroll, auto)
 * @property padding - Padding configuration
 * @property margin - Margin configuration
 * @property background - Background color (Chakra UI color token or CSS color)
 * @property color - Text color (Chakra UI color token or CSS color)
 * @property borderRadius - Border radius (Chakra UI radius token or CSS value)
 */
export const FlexStyleType = StructType({
    direction: OptionType(FlexDirectionType),
    wrap: OptionType(FlexWrapType),
    justifyContent: OptionType(JustifyContentType),
    alignItems: OptionType(AlignItemsType),
    gap: OptionType(StringType),
    width: OptionType(StringType),
    height: OptionType(StringType),
    minHeight: OptionType(StringType),
    minWidth: OptionType(StringType),
    maxHeight: OptionType(StringType),
    maxWidth: OptionType(StringType),
    overflow: OptionType(OverflowType),
    overflowX: OptionType(OverflowType),
    overflowY: OptionType(OverflowType),
    padding: OptionType(PaddingType),
    margin: OptionType(MarginType),
    background: OptionType(StringType),
    color: OptionType(StringType),
    borderRadius: OptionType(StringType),
    border: OptionType(StringType),
    borderColor: OptionType(StringType),
    borderWidth: OptionType(StringType),
});

/**
 * Type representing Flex style structure.
 */
export type FlexStyleType = typeof FlexStyleType;
