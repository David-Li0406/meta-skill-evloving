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
import { FlexStyleType, type FlexStyle } from "./types.js";
import {
    FlexDirectionType,
    JustifyContentType,
    AlignItemsType,
    FlexWrapType,
    OverflowType,
} from "../../style.js";
import { Padding, PaddingType, Margin, MarginType } from "../style.js";

// Re-export style types
export { FlexStyleType, type FlexStyle } from "./types.js";

/**
 * The concrete East type for Flex component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for a Flex component.
 * Flex is a container component with `display: flex` applied by default.
 *
 * @property children - Array of child UI components
 * @property style - Optional styling configuration wrapped in OptionType
 */
export const FlexType: StructType<{
    children: ArrayType<UIComponentType>,
    style: OptionType<FlexStyleType>,
}> = StructType({
    children: ArrayType(UIComponentType),
    style: OptionType(FlexStyleType),
});

/**
 * Type representing the Flex component structure.
 */
export type FlexType = typeof FlexType;

/**
 * Creates a Flex container component with children and optional styling.
 *
 * @param children - Array of child UI components
 * @param style - Optional styling configuration for the flex container
 * @returns An East expression representing the styled flex component
 *
 * @remarks
 * Flex is a convenience component that renders a Box with `display: flex` applied.
 * It provides easy access to flexbox layout properties like direction, wrap,
 * justifyContent, and alignItems.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Flex, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Flex.Root([
 *         Text.Root("Item 1"),
 *         Text.Root("Item 2"),
 *     ], {
 *         direction: "row",
 *         gap: "4",
 *         justifyContent: "space-between",
 *     });
 * });
 * ```
 */
function createFlex(
    children: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: FlexStyle
): ExprType<UIComponentType> {
    const directionValue = style?.direction
        ? (typeof style.direction === "string"
            ? East.value(variant(style.direction, null), FlexDirectionType)
            : style.direction)
        : undefined;

    const wrapValue = style?.wrap
        ? (typeof style.wrap === "string"
            ? East.value(variant(style.wrap, null), FlexWrapType)
            : style.wrap)
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

    return East.value(variant("Flex", {
        children: children,
        style: style ? variant("some", East.value({
            direction: directionValue ? variant("some", directionValue) : variant("none", null),
            wrap: wrapValue ? variant("some", wrapValue) : variant("none", null),
            justifyContent: justifyContentValue ? variant("some", justifyContentValue) : variant("none", null),
            alignItems: alignItemsValue ? variant("some", alignItemsValue) : variant("none", null),
            gap: style.gap ? variant("some", style.gap) : variant("none", null),
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
        }, FlexStyleType)) : variant("none", null),
    }), UIComponentType);
}

/**
 * Flex container component for flexbox layouts.
 *
 * @remarks
 * Use `Flex.Root(children, style)` to create a flex container, or access `Flex.Types.Flex` for the East type.
 * Flex is a convenience component that renders with `display: flex` applied by default.
 */
export const Flex = {
    /**
     * Creates a Flex container component with children and optional styling.
     *
     * @param children - Array of child UI components
     * @param style - Optional styling configuration for the flex container
     * @returns An East expression representing the styled flex component
     *
     * @remarks
     * Flex is a convenience component that renders a Box with `display: flex` applied.
     * It provides easy access to flexbox layout properties.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Flex, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Flex.Root([
     *         Text.Root("Item 1"),
     *         Text.Root("Item 2"),
     *     ], {
     *         direction: "row",
     *         gap: "4",
     *         alignItems: "center",
     *     });
     * });
     * ```
     */
    Root: createFlex,
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
     * Use this helper to create structured padding values for Flex components.
     * You can also pass a plain string to the padding style property for uniform padding.
     *
     * @example
     * ```ts
     * import { Flex, Padding } from "@elaraai/east-ui";
     *
     * // Structured padding
     * Flex.Root([...], {
     *   padding: Padding("4", "2", "4", "2"),
     * });
     *
     * // Uniform padding (shorthand)
     * Flex.Root([...], {
     *   padding: "4",
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
     * Use this helper to create structured margin values for Flex components.
     * You can also pass a plain string to the margin style property for uniform margin.
     *
     * @example
     * ```ts
     * import { Flex, Margin } from "@elaraai/east-ui";
     *
     * // Structured margin
     * Flex.Root([...], {
     *   margin: Margin("4", "auto", "4", "auto"),
     * });
     *
     * // Uniform margin (shorthand)
     * Flex.Root([...], {
     *   margin: "4",
     * });
     * ```
     */
    Margin,
    Types: {
        /**
         * The concrete East type for Flex component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Flex component.
         * Flex is a container component with `display: flex` applied by default.
         *
         * @property children - Array of child UI components
         * @property style - Optional styling configuration wrapped in OptionType
         */
        Flex: FlexType,
        /**
         * The concrete East type for Flex component style data.
         *
         * @remarks
         * All properties are optional and wrapped in {@link OptionType}.
         *
         * @property direction - Flex direction (row, column, row-reverse, column-reverse)
         * @property wrap - Flex wrap behavior (nowrap, wrap, wrap-reverse)
         * @property justifyContent - Justify content for main axis alignment
         * @property alignItems - Align items for cross axis alignment
         * @property gap - Gap between children
         * @property width - Width (Chakra UI size token or CSS value)
         * @property height - Height (Chakra UI size token or CSS value)
         * @property padding - Padding configuration
         * @property margin - Margin configuration
         * @property background - Background color (Chakra UI color token or CSS color)
         * @property color - Text color (Chakra UI color token or CSS color)
         * @property borderRadius - Border radius (Chakra UI radius token or CSS value)
         */
        Style: FlexStyleType,
        /**
         * The concrete East type for padding configuration.
         *
         * @remarks
         * This struct type defines padding for all four sides of a flex container.
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
         * This struct type defines margin for all four sides of a flex container.
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
