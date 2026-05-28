/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    East,
    OptionType,
    StructType,
    ArrayType,
    variant,
    type SubtypeExprOrValue,
    some,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { BoxStyleType, type BoxStyle } from "./types.js";
import {
    DisplayType,
    FlexDirectionType,
    JustifyContentType,
    AlignItemsType,
    OverflowType,
} from "../../style.js";
import { Padding, PaddingType, Margin, MarginType } from "../style.js";

// Re-export style types
export { BoxStyleType, type BoxStyle } from "./types.js";

/**
 * The concrete East type for Box component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for a Box component.
 * Box is a container component that can hold child components.
 *
 * @property children - Array of child UI components
 * @property style - Optional styling configuration wrapped in OptionType
 */
export const BoxType: StructType<{
    children: ArrayType<UIComponentType>,
    style: OptionType<BoxStyleType>,
}> = StructType({
    children: ArrayType(UIComponentType),
    style: OptionType(BoxStyleType),
});

/**
 * Type representing the Box component structure.
 */
export type BoxType = typeof BoxType;

/**
 * Creates a Box container component with children and optional styling.
 *
 * @param children - Array of child UI components
 * @param style - Optional styling configuration for the box
 * @returns An East expression representing the styled box component
 *
 * @remarks
 * Box is the fundamental building block for layouts. It maps to a div element
 * and supports all common CSS layout properties through style configuration.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Box, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Box.Root([
 *         Text.Root("Hello"),
 *     ], {
 *         padding: "4",
 *         background: "gray.100",
 *     });
 * });
 * ```
 */
function createBox(
    children: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: BoxStyle
): ExprType<UIComponentType> {
    const displayValue = style?.display
        ? (typeof style.display === "string"
            ? East.value(variant(style.display, null), DisplayType)
            : style.display)
        : undefined;

    const flexDirectionValue = style?.flexDirection
        ? (typeof style.flexDirection === "string"
            ? East.value(variant(style.flexDirection, null), FlexDirectionType)
            : style.flexDirection)
        : undefined;

    const justifyContentValue = style?.justifyContent
        ? (typeof style.justifyContent === "string"
            ? East.value(variant(style.justifyContent, null), JustifyContentType)
            : style.justifyContent)
        : undefined;

    const alignItemsValue = style?.alignItems
        ? (typeof style.alignItems === "string"
            ? East.value(variant(style.alignItems, null), AlignItemsType)
            : style.alignItems)
        : undefined;

    const overflowValue = style?.overflow
        ? (typeof style.overflow === "string"
            ? East.value(variant(style.overflow, null), OverflowType)
            : style.overflow)
        : undefined;

    const overflowXValue = style?.overflowX
        ? (typeof style.overflowX === "string"
            ? East.value(variant(style.overflowX, null), OverflowType)
            : style.overflowX)
        : undefined;

    const overflowYValue = style?.overflowY
        ? (typeof style.overflowY === "string"
            ? East.value(variant(style.overflowY, null), OverflowType)
            : style.overflowY)
        : undefined;

    const paddingValue = style?.padding
        ? (typeof style.padding === "string"
            ? East.value({
                top: some(style.padding),
                right: some(style.padding),
                bottom: some(style.padding),
                left: some(style.padding)
            }, PaddingType)
            : style.padding)
        : undefined;

    const marginValue = style?.margin
        ? (typeof style.margin === "string"
            ? East.value({
                top: some(style.margin),
                right: some(style.margin),
                bottom: some(style.margin),
                left: some(style.margin)
            }, MarginType)
            : style.margin)
        : undefined;

    return East.value(variant("Box", {
        children: children,
        style: style ? variant("some", East.value({
            display: displayValue ? variant("some", displayValue) : variant("none", null),
            width: style.width ? variant("some", style.width) : variant("none", null),
            height: style.height ? variant("some", style.height) : variant("none", null),
            minHeight: style.minHeight ? variant("some", style.minHeight) : variant("none", null),
            minWidth: style.minWidth ? variant("some", style.minWidth) : variant("none", null),
            maxHeight: style.maxHeight ? variant("some", style.maxHeight) : variant("none", null),
            maxWidth: style.maxWidth ? variant("some", style.maxWidth) : variant("none", null),
            overflow: overflowValue ? variant("some", overflowValue) : variant("none", null),
            overflowX: overflowXValue ? variant("some", overflowXValue) : variant("none", null),
            overflowY: overflowYValue ? variant("some", overflowYValue) : variant("none", null),
            padding: paddingValue ? variant("some", paddingValue) : variant("none", null),
            margin: marginValue ? variant("some", marginValue) : variant("none", null),
            background: style.background ? variant("some", style.background) : variant("none", null),
            color: style.color ? variant("some", style.color) : variant("none", null),
            borderRadius: style.borderRadius ? variant("some", style.borderRadius) : variant("none", null),
            border: style.border ? variant("some", style.border) : variant("none", null),
            borderColor: style.borderColor ? variant("some", style.borderColor) : variant("none", null),
            borderWidth: style.borderWidth ? variant("some", style.borderWidth) : variant("none", null),
            flexDirection: flexDirectionValue ? variant("some", flexDirectionValue) : variant("none", null),
            justifyContent: justifyContentValue ? variant("some", justifyContentValue) : variant("none", null),
            alignItems: alignItemsValue ? variant("some", alignItemsValue) : variant("none", null),
            gap: style.gap ? variant("some", style.gap) : variant("none", null),
        }, BoxStyleType)) : variant("none", null),
    }), UIComponentType);
}

/**
 * Box container component for flexible layouts.
 *
 * @remarks
 * Use `Box.Root(children, style)` to create a box, or access `Box.Types.Box` for the East type.
 */
export const Box = {
    /**
     * Creates a Box container component with children and optional styling.
     *
     * @param children - Array of child UI components
     * @param style - Optional styling configuration for the box
     * @returns An East expression representing the styled box component
     *
     * @remarks
     * Box is the fundamental building block for layouts. It maps to a div element
     * and supports all common CSS layout properties through style configuration.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Box, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Box.Root([
     *         Text.Root("Hello"),
     *     ], {
     *         padding: "4",
     *         background: "gray.100",
     *     });
     * });
     * ```
     */
    Root: createBox,
    /**
     * Creates padding configuration for layout components.
     *
     * @param top - Top padding (Chakra UI spacing token or CSS value)
     * @param right - Right padding (Chakra UI spacing token or CSS value)
     * @param bottom - Bottom padding (Chakra UI spacing token or CSS value)
     * @param left - Left padding (Chakra UI spacing token or CSS value)
     * @returns An East expression representing the padding configuration
     *
     * @remarks
     * Use this helper to create structured padding values for Box and Stack components.
     * You can also pass a plain string to the padding style property for uniform padding.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Box, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Box.Root([
     *         Text.Root("Padded content"),
     *     ], {
     *         padding: Box.Padding("4", "2", "4", "2"),
     *     });
     * });
     * ```
     */
    Padding,
    /**
     * Creates margin configuration for layout components.
     *
     * @param top - Top margin (Chakra UI spacing token or CSS value)
     * @param right - Right margin (Chakra UI spacing token or CSS value)
     * @param bottom - Bottom margin (Chakra UI spacing token or CSS value)
     * @param left - Left margin (Chakra UI spacing token or CSS value)
     * @returns An East expression representing the margin configuration
     *
     * @remarks
     * Use this helper to create structured margin values for Box and Stack components.
     * You can also pass a plain string to the margin style property for uniform margin.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Box, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Box.Root([
     *         Text.Root("Centered content"),
     *     ], {
     *         margin: Box.Margin("4", "auto", "4", "auto"),
     *     });
     * });
     * ```
     */
    Margin,
    Types: {
        /**
         * The concrete East type for Box component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Box component.
         * Box is a container component that can hold child components.
         *
         * @property children - Array of child UI components
         * @property style - Optional styling configuration wrapped in OptionType
         */
        Box: BoxType,
        /**
         * The concrete East type for Box component style data.
         *
         * @remarks
         * All properties are optional and wrapped in {@link OptionType}.
         *
         * @property display - CSS display property
         * @property width - Width (Chakra UI size token or CSS value)
         * @property height - Height (Chakra UI size token or CSS value)
         * @property padding - Padding configuration
         * @property margin - Margin configuration
         * @property background - Background color (Chakra UI color token or CSS color)
         * @property color - Text color (Chakra UI color token or CSS color)
         * @property borderRadius - Border radius (Chakra UI radius token or CSS value)
         * @property flexDirection - Flex direction for flex containers
         * @property justifyContent - Justify content for flex/grid containers
         * @property alignItems - Align items for flex/grid containers
         * @property gap - Gap between children (Chakra UI spacing token or CSS value)
         */
        Style: BoxStyleType,
        /**
         * The concrete East type for padding configuration.
         *
         * @remarks
         * This struct type defines padding for all four sides of a box.
         * Each side is optional and accepts Chakra UI spacing tokens or CSS values.
         *
         * @property top - Top padding (Chakra UI spacing token or CSS value)
         * @property right - Right padding (Chakra UI spacing token or CSS value)
         * @property bottom - Bottom padding (Chakra UI spacing token or CSS value)
         * @property left - Left padding (Chakra UI spacing token or CSS value)
         */
        Padding: PaddingType,
        /**
         * The concrete East type for margin configuration.
         *
         * @remarks
         * This struct type defines margin for all four sides of a box.
         * Each side is optional and accepts Chakra UI spacing tokens or CSS values.
         *
         * @property top - Top margin (Chakra UI spacing token or CSS value)
         * @property right - Right margin (Chakra UI spacing token or CSS value)
         * @property bottom - Bottom margin (Chakra UI spacing token or CSS value)
         * @property left - Left margin (Chakra UI spacing token or CSS value)
         */
        Margin: MarginType,
    },
} as const;
