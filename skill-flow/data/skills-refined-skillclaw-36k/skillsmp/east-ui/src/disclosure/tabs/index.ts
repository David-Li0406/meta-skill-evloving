/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    OptionType,
    StructType,
    StringType,
    BooleanType,
    ArrayType,
    variant,
} from "@elaraai/east";

import { ColorSchemeType, OrientationType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import {
    TabsVariantType,
    TabsVariant,
    TabsJustifyType,
    TabsActivationModeType,
    TabsSizeType,
    TabsStyleType,
    type TabsStyle,
    type TabsItemStyle,
} from "./types.js";

// Re-export types
export {
    TabsVariantType,
    TabsVariant,
    TabsJustifyType,
    TabsActivationModeType,
    TabsSizeType,
    TabsStyleType,
    type TabsVariantLiteral,
    type TabsJustifyLiteral,
    type TabsActivationModeLiteral,
    type TabsSizeLiteral,
    type TabsStyle,
    type TabsItemStyle,
} from "./types.js";

// ============================================================================
// Tabs Item Type
// ============================================================================

/**
 * Type for Tabs item data.
 *
 * @remarks
 * Each tab has a value (identifier), trigger (label text),
 * content (child components), and optional disabled state.
 *
 * @property value - Unique identifier for this tab
 * @property trigger - The tab label text
 * @property content - Array of child UI components for the tab panel
 * @property disabled - Whether this tab is disabled
 */
export const TabsItemType: StructType<{
    value: StringType,
    trigger: StringType,
    content: ArrayType<UIComponentType>,
    disabled: OptionType<BooleanType>,
}> = StructType({
    value: StringType,
    trigger: StringType,
    content: ArrayType(UIComponentType),
    disabled: OptionType(BooleanType),
});

/**
 * Type representing the TabsItem structure.
 */
export type TabsItemType = typeof TabsItemType;

// ============================================================================
// Tabs Root Type
// ============================================================================

/**
 * Type for Tabs component data.
 *
 * @remarks
 * Tabs display content in separate panels, with only one panel visible at a time.
 *
 * @property items - Array of tab items
 * @property value - Controlled selected tab value
 * @property defaultValue - Initial selected tab value
 * @property style - Optional styling configuration
 */
export const TabsRootType = StructType({
    items: ArrayType(TabsItemType),
    value: OptionType(StringType),
    defaultValue: OptionType(StringType),
    style: OptionType(TabsStyleType),
});

/**
 * Type representing the Tabs structure.
 */
export type TabsRootType = typeof TabsRootType;

// ============================================================================
// Tabs Item Function
// ============================================================================

/**
 * Creates a Tabs item with trigger and content children.
 *
 * @param value - Unique identifier for this tab
 * @param trigger - The tab label text
 * @param content - Array of child UI components for the tab panel
 * @param style - Optional item configuration
 * @returns An East expression representing the tabs item
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Tabs, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Tabs.Root([
 *         Tabs.Item("overview", "Overview", [Text.Root("Overview content")]),
 *         Tabs.Item("disabled", "Disabled Tab", [Text.Root("Disabled")], { disabled: true }),
 *     ]);
 * });
 * ```
 */
function createTabsItem(
    value: SubtypeExprOrValue<StringType>,
    trigger: SubtypeExprOrValue<StringType>,
    content: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: TabsItemStyle
): ExprType<TabsItemType> {
    const toBoolOption = (val: SubtypeExprOrValue<BooleanType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    return East.value({
        value: value,
        trigger: trigger,
        content: content,
        disabled: toBoolOption(style?.disabled),
    }, TabsItemType);
}

// ============================================================================
// Tabs Root Function
// ============================================================================

/**
 * Creates a Tabs component with items and optional styling.
 *
 * @param items - Array of Tabs items
 * @param style - Optional styling configuration
 * @returns An East expression representing the tabs component
 *
 * @remarks
 * Tabs are used to organize content into separate views where only one
 * view is visible at a time.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Tabs, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Tabs.Root([
 *         Tabs.Item("overview", "Overview", [Text.Root("Overview content")]),
 *         Tabs.Item("settings", "Settings", [Text.Root("Settings content")]),
 *     ], {
 *         defaultValue: "overview",
 *         variant: "line",
 *     });
 * });
 * ```
 */
function createTabsRoot(
    items: SubtypeExprOrValue<ArrayType<TabsItemType>>,
    style?: TabsStyle
): ExprType<UIComponentType> {
    const toBoolOption = (val: SubtypeExprOrValue<BooleanType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const toStringOption = (val: SubtypeExprOrValue<StringType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), TabsVariantType)
            : style.variant)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), TabsSizeType)
            : style.size)
        : undefined;

    const orientationValue = style?.orientation
        ? (typeof style.orientation === "string"
            ? East.value(variant(style.orientation, null), OrientationType)
            : style.orientation)
        : undefined;

    const activationModeValue = style?.activationMode
        ? (typeof style.activationMode === "string"
            ? East.value(variant(style.activationMode, null), TabsActivationModeType)
            : style.activationMode)
        : undefined;

    const justifyValue = style?.justify
        ? (typeof style.justify === "string"
            ? East.value(variant(style.justify, null), TabsJustifyType)
            : style.justify)
        : undefined;

    const colorPaletteValue = style?.colorPalette
        ? (typeof style.colorPalette === "string"
            ? East.value(variant(style.colorPalette, null), ColorSchemeType)
            : style.colorPalette)
        : undefined;

    return East.value(variant("Tabs", {
        items: items,
        value: toStringOption(style?.value),
        defaultValue: toStringOption(style?.defaultValue),
        style: style ? variant("some", East.value({
            variant: variantValue ? variant("some", variantValue) : variant("none", null),
            size: sizeValue ? variant("some", sizeValue) : variant("none", null),
            orientation: orientationValue ? variant("some", orientationValue) : variant("none", null),
            activationMode: activationModeValue ? variant("some", activationModeValue) : variant("none", null),
            fitted: toBoolOption(style.fitted),
            justify: justifyValue ? variant("some", justifyValue) : variant("none", null),
            lazyMount: toBoolOption(style.lazyMount),
            unmountOnExit: toBoolOption(style.unmountOnExit),
            colorPalette: colorPaletteValue ? variant("some", colorPaletteValue) : variant("none", null),
            onValueChange: style?.onValueChange !== undefined ? variant("some", style.onValueChange) : variant("none", null),
        }, TabsStyleType)) : variant("none", null),
    }), UIComponentType);
}

// ============================================================================
// Tabs Compound Component
// ============================================================================

/**
 * Tabs compound component for tabbed content panels.
 *
 * @remarks
 * Use `Tabs.Root` to create the container and `Tabs.Item` for each
 * tab panel. Tab content supports child UI components.
 */
export const Tabs = {
    /**
     * Creates a Tabs container with items and optional styling.
     *
     * @param items - Array of tab items created with Tabs.Item
     * @param style - Optional styling configuration
     * @returns An East expression representing the tabs component
     *
     * @remarks
     * Tabs organize content into separate panels where only one panel
     * is visible at a time. Supports various visual variants, sizes,
     * orientations, and activation modes.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Tabs, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Tabs.Root([
     *         Tabs.Item("tab1", "Overview", [Text.Root("Overview content")]),
     *         Tabs.Item("tab2", "Details", [Text.Root("Details content")]),
     *     ], {
     *         variant: "line",
     *         fitted: true,
     *     });
     * });
     * ```
     */
    Root: createTabsRoot,
    /**
     * Creates a Tabs item with trigger label and content.
     *
     * @param value - Unique identifier for this tab
     * @param trigger - The tab label text displayed in the tab list
     * @param content - Array of child UI components for the tab panel
     * @param style - Optional item configuration
     * @returns An East expression representing the tabs item
     *
     * @remarks
     * Each tab item has a unique value for identification, a trigger
     * text displayed in the tab list, and content shown when selected.
     * Items can be individually disabled.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Tabs, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Tabs.Root([
     *         Tabs.Item("overview", "Overview", [
     *             Text.Root("Overview content here"),
     *         ]),
     *         Tabs.Item("disabled", "Disabled Tab", [
     *             Text.Root("This tab is disabled"),
     *         ], {
     *             disabled: true,
     *         }),
     *     ], {
     *         defaultValue: "overview",
     *     });
     * });
     * ```
     */
    Item: createTabsItem,
    /**
     * Helper function to create tabs variant values.
     *
     * @param v - The variant string ("line", "subtle", "enclosed", "outline", "plain")
     * @returns An East expression representing the tabs variant
     *
     * @remarks
     * Use this helper to create variant values programmatically. In most cases,
     * you can pass string literals directly to the style property.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Tabs, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Tabs.Root([
     *         Tabs.Item("tab1", "Tab 1", [Text.Root("Content")]),
     *     ], {
     *         variant: Tabs.Variant("enclosed"),
     *     });
     * });
     * ```
     */
    Variant: TabsVariant,
    Types: {
        /**
         * The concrete East type for Tabs container data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Tabs
         * component. Tabs display content in separate panels, with only one panel
         * visible at a time. The container holds an array of tab items and
         * optional controlled/uncontrolled selection state.
         *
         * @property items - Array of tab items (TabsItemType)
         * @property value - Controlled selected tab value (OptionType<StringType>)
         * @property defaultValue - Initial selected tab value (OptionType<StringType>)
         * @property style - Optional styling configuration (OptionType<TabsStyleType>)
         */
        Root: TabsRootType,
        /**
         * The concrete East type for Tabs item data.
         *
         * @remarks
         * This struct type represents a single tab within the Tabs component.
         * Each item has a unique identifier, trigger text displayed in the tab
         * list, and content components shown when the tab is selected.
         *
         * @property value - Unique identifier for this tab (StringType)
         * @property trigger - The tab label text displayed in the tab list (StringType)
         * @property content - Array of child UI components for the panel (ArrayType<UIComponentType>)
         * @property disabled - Whether this tab is disabled (OptionType<BooleanType>)
         */
        Item: TabsItemType,
        /**
         * The concrete East type for Tabs style configuration.
         *
         * @remarks
         * This struct type defines the styling configuration for a Tabs component.
         * It controls visual appearance, layout, keyboard behavior, and
         * performance optimizations for tab content mounting.
         *
         * @property variant - Visual variant: line, subtle, enclosed, outline, plain (OptionType<TabsVariantType>)
         * @property size - Size of the tabs: sm, md, lg (OptionType<TabsSizeType>)
         * @property orientation - Layout direction: horizontal or vertical (OptionType<OrientationType>)
         * @property activationMode - Keyboard navigation: automatic or manual (OptionType<TabsActivationModeType>)
         * @property fitted - Whether tabs take equal width (OptionType<BooleanType>)
         * @property justify - Tab list alignment: start, center, end (OptionType<TabsJustifyType>)
         * @property lazyMount - Mount content only when tab is selected (OptionType<BooleanType>)
         * @property unmountOnExit - Unmount content when tab is deselected (OptionType<BooleanType>)
         * @property colorPalette - Color scheme for the tabs (OptionType<ColorSchemeType>)
         */
        Style: TabsStyleType,
        /**
         * Variant type for Tabs visual appearance styles.
         *
         * @remarks
         * This variant type provides type-safe visual style options for tabs.
         * Each variant affects how the tab list and selected indicator appear.
         *
         * @property line - Tabs with an underline indicator on the selected tab
         * @property subtle - Light background highlighting on the selected tab
         * @property enclosed - Tabs with a bordered container around the selected tab
         * @property outline - Outlined tabs with border around each tab
         * @property plain - No visible styling or indicator
         */
        Variant: TabsVariantType,
        /**
         * Size type for Tabs component dimensions.
         *
         * @remarks
         * This variant type provides type-safe size options for tabs.
         * Affects the padding, font size, and overall dimensions of the tab list.
         * Note: Chakra UI Tabs only supports sm, md, lg (not xs or xl).
         *
         * @property sm - Small tabs with compact padding
         * @property md - Medium tabs with standard padding (default)
         * @property lg - Large tabs with generous padding
         */
        Size: TabsSizeType,
        /**
         * Justify type for tab list alignment.
         *
         * @remarks
         * This variant type controls how tabs are aligned within the tab list
         * container. Useful when tabs don't fill the entire available width.
         *
         * @property start - Align tabs to the start (left in LTR, right in RTL)
         * @property center - Center the tabs horizontally
         * @property end - Align tabs to the end (right in LTR, left in RTL)
         */
        Justify: TabsJustifyType,
        /**
         * Activation mode type for keyboard navigation behavior.
         *
         * @remarks
         * This variant type controls how tabs respond to keyboard navigation.
         * Affects accessibility and user experience when navigating with
         * arrow keys.
         *
         * @property automatic - Tab content activates immediately when focused via keyboard
         * @property manual - Tab requires Enter/Space key press to activate after focus
         */
        ActivationMode: TabsActivationModeType,
    },
} as const;
