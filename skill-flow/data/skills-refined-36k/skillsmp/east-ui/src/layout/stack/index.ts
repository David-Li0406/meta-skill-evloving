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

import {
    FlexDirectionType,
    JustifyContentType,
    AlignItemsType,
    FlexWrapType,
    OverflowType,
} from "../../style.js";
import { UIComponentType } from "../../component.js";
import { StackStyleType, type StackStyle } from "./types.js";
import { Padding, PaddingType, Margin, MarginType } from "../style.js";

// Re-export style types
export { StackStyleType, type StackStyle } from "./types.js";

/**
 * The concrete East type for Stack component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for a Stack component.
 * Stack is a container component that arranges children in a single direction.
 *
 * @property children - Array of child UI components
 * @property style - Optional styling configuration wrapped in OptionType
 */
export const StackType: StructType<{
    children: ArrayType<UIComponentType>,
    style: OptionType<StackStyleType>,
}> = StructType({
    children: ArrayType(UIComponentType),
    style: OptionType(StackStyleType),
});

/**
 * Type representing the Stack component structure.
 */
export type StackType = typeof StackType;

/**
 * Creates a Stack container component with children and optional styling.
 *
 * @param children - Array of child UI components
 * @param style - Optional styling configuration for the stack
 * @returns An East expression representing the styled stack component
 *
 * @remarks
 * Stack arranges children in a single direction (row or column) with consistent
 * spacing. Use HStack for horizontal layout and VStack for vertical layout.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Stack, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Stack.Root([
 *         Text.Root("Item 1"),
 *         Text.Root("Item 2"),
 *     ], {
 *         gap: "4",
 *         direction: "column",
 *     });
 * });
 * ```
 */
function createStack(
    children: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: StackStyle
): ExprType<UIComponentType> {
    const directionValue = style?.direction
        ? (typeof style.direction === "string"
            ? East.value(variant(style.direction, null), FlexDirectionType)
            : style.direction)
        : undefined;

    const alignValue = style?.align
        ? (typeof style.align === "string"
            ? East.value(variant(style.align, null), AlignItemsType)
            : style.align)
        : undefined;

    const justifyValue = style?.justify
        ? (typeof style.justify === "string"
            ? East.value(variant(style.justify, null), JustifyContentType)
            : style.justify)
        : undefined;

    const wrapValue = style?.wrap
        ? (typeof style.wrap === "string"
            ? East.value(variant(style.wrap, null), FlexWrapType)
            : style.wrap)
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

    return East.value(variant("Stack", {
        children: children,
        style: style ? variant("some", East.value({
            direction: directionValue ? variant("some", directionValue) : variant("none", null),
            gap: style.gap ? variant("some", style.gap) : variant("none", null),
            align: alignValue ? variant("some", alignValue) : variant("none", null),
            justify: justifyValue ? variant("some", justifyValue) : variant("none", null),
            wrap: wrapValue ? variant("some", wrapValue) : variant("none", null),
            padding: paddingValue ? variant("some", paddingValue) : variant("none", null),
            margin: marginValue ? variant("some", marginValue) : variant("none", null),
            background: style.background ? variant("some", style.background) : variant("none", null),
            borderRadius: style.borderRadius ? variant("some", style.borderRadius) : variant("none", null),
            border: style.border ? variant("some", style.border) : variant("none", null),
            borderColor: style.borderColor ? variant("some", style.borderColor) : variant("none", null),
            borderWidth: style.borderWidth ? variant("some", style.borderWidth) : variant("none", null),
            width: style.width ? variant("some", style.width) : variant("none", null),
            height: style.height ? variant("some", style.height) : variant("none", null),
            minHeight: style.minHeight ? variant("some", style.minHeight) : variant("none", null),
            minWidth: style.minWidth ? variant("some", style.minWidth) : variant("none", null),
            maxHeight: style.maxHeight ? variant("some", style.maxHeight) : variant("none", null),
            maxWidth: style.maxWidth ? variant("some", style.maxWidth) : variant("none", null),
            overflow: overflowValue ? variant("some", overflowValue) : variant("none", null),
            overflowX: overflowXValue ? variant("some", overflowXValue) : variant("none", null),
            overflowY: overflowYValue ? variant("some", overflowYValue) : variant("none", null),
        }, StackStyleType)) : variant("none", null),
    }), UIComponentType);
}

/**
 * Creates a horizontal Stack (row direction).
 *
 * @param children - Array of child UI components
 * @param style - Optional styling configuration (direction is overridden to row)
 * @returns An East expression representing the horizontal stack component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Stack, Button, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Stack.HStack([
 *         Button.Root("Cancel"),
 *         Button.Root("Submit", { colorPalette: "blue" }),
 *     ], {
 *         gap: "2",
 *     });
 * });
 * ```
 */
function createHStack(
    children: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: Omit<StackStyle, "direction">
): ExprType<UIComponentType> {
    return createStack(children, {
        ...style,
        direction: East.value(variant("row", null), FlexDirectionType),
    });
}

/**
 * Creates a vertical Stack (column direction).
 *
 * @param children - Array of child UI components
 * @param style - Optional styling configuration (direction is overridden to column)
 * @returns An East expression representing the vertical stack component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Stack, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Stack.VStack([
 *         Text.Root("Title"),
 *         Text.Root("Subtitle"),
 *     ], {
 *         gap: "1",
 *         align: "flex-start",
 *     });
 * });
 * ```
 */
function createVStack(
    children: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: Omit<StackStyle, "direction">
): ExprType<UIComponentType> {
    return createStack(children, {
        ...style,
        direction: East.value(variant("column", null), FlexDirectionType),
    });
}

/**
 * Stack container component for flex-based layouts.
 *
 * @remarks
 * Use `Stack.Root(children, style)` for general stack, `Stack.HStack()` for horizontal, `Stack.VStack()` for vertical.
 */
export const Stack = {
    /**
     * Creates a Stack container with flex layout.
     *
     * @param children - Array of child UI components
     * @param style - Optional styling configuration
     * @returns An East expression representing the stack component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Stack, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Stack.Root([
     *         Text.Root("Item 1"),
     *         Text.Root("Item 2"),
     *     ], {
     *         gap: "4",
     *         direction: "column",
     *     });
     * });
     * ```
     */
    Root: createStack,
    /**
     * Creates a horizontal Stack (row direction).
     *
     * @param children - Array of child UI components
     * @param style - Optional styling configuration
     * @returns An East expression representing the horizontal stack
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Stack, Button, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Stack.HStack([
     *         Button.Root("Cancel"),
     *         Button.Root("Submit", { colorPalette: "blue" }),
     *     ], {
     *         gap: "2",
     *     });
     * });
     * ```
     */
    HStack: createHStack,
    /**
     * Creates a vertical Stack (column direction).
     *
     * @param children - Array of child UI components
     * @param style - Optional styling configuration
     * @returns An East expression representing the vertical stack
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Stack, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Stack.VStack([
     *         Text.Root("Title"),
     *         Text.Root("Subtitle"),
     *     ], {
     *         gap: "1",
     *         align: "flex-start",
     *     });
     * });
     * ```
     */
    VStack: createVStack,
    /**
     * Creates padding configuration for layout components.
     *
     * @param top - Top padding (Chakra UI spacing token or CSS value)
     * @param right - Right padding
     * @param bottom - Bottom padding
     * @param left - Left padding
     * @returns An East expression representing the padding configuration
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Stack, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Stack.Root([
     *         Text.Root("Content"),
     *     ], {
     *         padding: Stack.Padding("4", "2", "4", "2"),
     *     });
     * });
     * ```
     */
    Padding,
    /**
     * Creates margin configuration for layout components.
     *
     * @param top - Top margin (Chakra UI spacing token or CSS value)
     * @param right - Right margin
     * @param bottom - Bottom margin
     * @param left - Left margin
     * @returns An East expression representing the margin configuration
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Stack, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Stack.Root([
     *         Text.Root("Content"),
     *     ], {
     *         margin: Stack.Margin("4", "auto", "4", "auto"),
     *     });
     * });
     * ```
     */
    Margin,
    Types: {
        /**
         * The concrete East type for Stack component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Stack component.
         * Stack arranges children in a flex container with configurable direction and spacing.
         *
         * @property children - Array of child UI components
         * @property style - Optional styling configuration wrapped in OptionType
         */
        Stack: StackType,
        /**
         * Style type for Stack component configuration.
         *
         * @remarks
         * This struct type defines the styling configuration for a Stack component.
         *
         * @property direction - Flex direction (row, column, row-reverse, column-reverse)
         * @property gap - Spacing between children (Chakra UI spacing token)
         * @property align - Cross-axis alignment (flex-start, center, flex-end, stretch)
         * @property justify - Main-axis alignment (flex-start, center, flex-end, space-between)
         * @property wrap - Whether items should wrap (nowrap, wrap, wrap-reverse)
         */
        Style: StackStyleType,
        /**
         * Type for padding configuration.
         *
         * @remarks
         * Allows specifying individual padding values for each side.
         *
         * @property top - Top padding value
         * @property right - Right padding value
         * @property bottom - Bottom padding value
         * @property left - Left padding value
         */
        Padding: PaddingType,
        /**
         * Type for margin configuration.
         *
         * @remarks
         * Allows specifying individual margin values for each side.
         *
         * @property top - Top margin value
         * @property right - Right margin value
         * @property bottom - Bottom margin value
         * @property left - Left margin value
         */
        Margin: MarginType,
    },
} as const;
