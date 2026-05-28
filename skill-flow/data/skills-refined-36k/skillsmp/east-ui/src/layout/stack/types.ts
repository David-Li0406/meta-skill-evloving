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

/**
 * Style configuration for Stack components.
 *
 * @remarks
 * Stack is a layout component that arranges children in a single direction
 * (row or column) with configurable spacing and alignment.
 *
 * @property direction - Stack direction (row or column)
 * @property gap - Gap between children (Chakra UI spacing token or CSS value)
 * @property align - Cross-axis alignment
 * @property justify - Main-axis alignment
 * @property wrap - Flex wrap behavior
 * @property padding - Padding configuration
 * @property margin - Margin configuration
 * @property background - Background color (Chakra UI color token or CSS color)
 * @property width - Width (Chakra UI size token or CSS value)
 * @property height - Height (Chakra UI size token or CSS value)
 * @property minHeight - Min height (Chakra UI size token or CSS value)
 * @property minWidth - Min width (Chakra UI size token or CSS value)
 * @property maxHeight - Max height (Chakra UI size token or CSS value)
 * @property maxWidth - Max width (Chakra UI size token or CSS value)
 * @property overflow - Overflow behavior for both axes (visible, hidden, scroll, auto)
 * @property overflowX - Horizontal overflow behavior (visible, hidden, scroll, auto)
 * @property overflowY - Vertical overflow behavior (visible, hidden, scroll, auto)
 */
export type StackStyle = {
    /** Stack direction (row or column) */
    direction?: SubtypeExprOrValue<FlexDirectionType> | FlexDirectionLiteral;
    /** Gap between children (Chakra UI spacing token or CSS value) */
    gap?: SubtypeExprOrValue<StringType>;
    /** Cross-axis alignment */
    align?: SubtypeExprOrValue<AlignItemsType> | AlignItemsLiteral;
    /** Main-axis alignment */
    justify?: SubtypeExprOrValue<JustifyContentType> | JustifyContentLiteral;
    /** Flex wrap behavior */
    wrap?: SubtypeExprOrValue<FlexWrapType> | FlexWrapLiteral;
    /** Padding configuration - use Padding() helper */
    padding?: SubtypeExprOrValue<PaddingType> | string;
    /** Margin configuration - use Margin() helper */
    margin?: SubtypeExprOrValue<MarginType> | string;
    /** Background color (Chakra UI color token or CSS color) */
    background?: SubtypeExprOrValue<StringType>;
    /** Border radius (Chakra UI radius token or CSS value) */
    borderRadius?: SubtypeExprOrValue<StringType>;
    /** Border shorthand (CSS value, e.g., "1px solid gray.200") */
    border?: SubtypeExprOrValue<StringType>;
    /** Border color (Chakra UI color token or CSS color) */
    borderColor?: SubtypeExprOrValue<StringType>;
    /** Border width (CSS value, e.g., "1px", "2px") */
    borderWidth?: SubtypeExprOrValue<StringType>;
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
};

/**
 * The concrete East type for Stack component style data.
 *
 * @remarks
 * All properties are optional and wrapped in {@link OptionType}.
 *
 * @property direction - Stack direction (row or column)
 * @property gap - Gap between children (Chakra UI spacing token or CSS value)
 * @property align - Cross-axis alignment
 * @property justify - Main-axis alignment
 * @property wrap - Flex wrap behavior
 * @property padding - Padding configuration
 * @property margin - Margin configuration
 * @property background - Background color (Chakra UI color token or CSS color)
 * @property width - Width (Chakra UI size token or CSS value)
 * @property height - Height (Chakra UI size token or CSS value)
 * @property minHeight - Min height (Chakra UI size token or CSS value)
 * @property minWidth - Min width (Chakra UI size token or CSS value)
 * @property maxHeight - Max height (Chakra UI size token or CSS value)
 * @property maxWidth - Max width (Chakra UI size token or CSS value)
 * @property overflow - Overflow behavior for both axes (visible, hidden, scroll, auto)
 * @property overflowX - Horizontal overflow behavior (visible, hidden, scroll, auto)
 * @property overflowY - Vertical overflow behavior (visible, hidden, scroll, auto)
 */
export const StackStyleType = StructType({
    direction: OptionType(FlexDirectionType),
    gap: OptionType(StringType),
    align: OptionType(AlignItemsType),
    justify: OptionType(JustifyContentType),
    wrap: OptionType(FlexWrapType),
    padding: OptionType(PaddingType),
    margin: OptionType(MarginType),
    background: OptionType(StringType),
    borderRadius: OptionType(StringType),
    border: OptionType(StringType),
    borderColor: OptionType(StringType),
    borderWidth: OptionType(StringType),
    width: OptionType(StringType),
    height: OptionType(StringType),
    minHeight: OptionType(StringType),
    minWidth: OptionType(StringType),
    maxHeight: OptionType(StringType),
    maxWidth: OptionType(StringType),
    overflow: OptionType(OverflowType),
    overflowX: OptionType(OverflowType),
    overflowY: OptionType(OverflowType),
});

/**
 * Type representing Stack style structure.
 */
export type StackStyleType = typeof StackStyleType;
