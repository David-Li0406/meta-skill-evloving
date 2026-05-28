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
    some,
    none,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    AccordionVariantType,
    AccordionVariant,
    AccordionStyleType,
    AccordionItemStyleType,
    type AccordionStyle,
    type AccordionItemStyle,
} from "./types.js";

// Re-export types
export {
    AccordionVariantType,
    AccordionVariant,
    AccordionStyleType,
    AccordionItemStyleType,
    type AccordionVariantLiteral,
    type AccordionStyle,
    type AccordionItemStyle,
} from "./types.js";

// ============================================================================
// Accordion Item Type
// ============================================================================

/**
 * Type for Accordion item data.
 *
 * @remarks
 * Each item in an Accordion has a value (identifier), trigger (label),
 * content (child components), and optional disabled state.
 *
 * @property value - Unique identifier for this item
 * @property trigger - The clickable trigger/label text
 * @property content - Array of child UI components for the collapsible content
 * @property disabled - Whether this item is disabled
 */
export const AccordionItemType: StructType<{
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
 * Type representing the AccordionItem structure.
 */
export type AccordionItemType = typeof AccordionItemType;

// ============================================================================
// Accordion Root Type
// ============================================================================

/**
 * Type for Accordion component data.
 *
 * @remarks
 * Accordion displays collapsible content panels for presenting information
 * in a limited space.
 *
 * @property items - Array of accordion items
 * @property style - Optional styling configuration
 */
export const AccordionRootType = StructType({
    items: ArrayType(AccordionItemType),
    style: OptionType(AccordionStyleType),
});

/**
 * Type representing the Accordion structure.
 */
export type AccordionRootType = typeof AccordionRootType;

// ============================================================================
// Accordion Item Function
// ============================================================================

/**
 * Creates an Accordion item with trigger and content children.
 *
 * @param value - Unique identifier for this item
 * @param trigger - The clickable trigger/label text
 * @param content - Array of child UI components for the collapsible content
 * @param style - Optional item configuration
 * @returns An East expression representing the accordion item
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Accordion, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Accordion.Root([
 *         Accordion.Item("section-1", "Section 1", [
 *             Text.Root("Content for section 1"),
 *         ]),
 *         Accordion.Item("section-2", "Section 2", [
 *             Text.Root("Content for section 2"),
 *         ], { disabled: true }),
 *     ]);
 * });
 * ```
 */
function createAccordionItem(
    value: SubtypeExprOrValue<StringType>,
    trigger: SubtypeExprOrValue<StringType>,
    content: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: AccordionItemStyle
): ExprType<AccordionItemType> {
    return East.value({
        value: value,
        trigger: trigger,
        content: content,
        disabled: style?.disabled !== undefined ? some(style.disabled) : none,
    }, AccordionItemType);
}

// ============================================================================
// Accordion Root Function
// ============================================================================

/**
 * Creates an Accordion component with items and optional styling.
 *
 * @param items - Array of Accordion items
 * @param style - Optional styling configuration
 * @returns An East expression representing the accordion component
 *
 * @remarks
 * Accordion is used to display collapsible content panels, useful for FAQs,
 * settings panels, and navigation menus.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Accordion, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Accordion.Root([
 *         Accordion.Item("q1", "What is East UI?", [
 *             Text.Root("East UI is a typed UI library."),
 *         ]),
 *         Accordion.Item("q2", "How do I install it?", [
 *             Text.Root("Run npm install @elaraai/east-ui"),
 *         ]),
 *     ], {
 *         multiple: true,
 *         variant: "enclosed",
 *     });
 * });
 * ```
 */
function createAccordionRoot(
    items: SubtypeExprOrValue<ArrayType<AccordionItemType>>,
    style?: AccordionStyle
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), AccordionVariantType)
            : style.variant)
        : undefined;

    return East.value(variant("Accordion", {
        items: items,
        style: style ? some(East.value({
            multiple: style.multiple !== undefined ? some(style.multiple) : none,
            collapsible: style.collapsible !== undefined ? some(style.collapsible) : none,
            variant: variantValue ? some(variantValue) : none,
            onValueChange: style.onValueChange ? some(style.onValueChange) : none,
        }, AccordionStyleType)) : none,
    }), UIComponentType);
}

// ============================================================================
// Accordion Compound Component
// ============================================================================

/**
 * Accordion compound component for collapsible content panels.
 *
 * @remarks
 * Use `Accordion.Root` to create the container and `Accordion.Item` for each
 * collapsible panel. Item content supports child UI components.
 */
export const Accordion = {
    /**
     * Creates an Accordion container with items and optional styling.
     *
     * @param items - Array of accordion items created with Accordion.Item
     * @param style - Optional styling configuration
     * @returns An East expression representing the accordion component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Accordion, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Accordion.Root([
     *         Accordion.Item("section-1", "Section 1", [Text.Root("Content 1")]),
     *         Accordion.Item("section-2", "Section 2", [Text.Root("Content 2")]),
     *     ], {
     *         variant: "enclosed",
     *         collapsible: true,
     *     });
     * });
     * ```
     */
    Root: createAccordionRoot,
    /**
     * Creates an Accordion item with trigger and content.
     *
     * @param value - Unique identifier for the item
     * @param trigger - The text displayed in the accordion trigger/header
     * @param content - Array of child UI components shown when expanded
     * @param style - Optional item styling
     * @returns An East expression representing the accordion item
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Accordion, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Accordion.Root([
     *         Accordion.Item("faq-1", "What is East UI?", [
     *             Text.Root("East UI is a typed UI component library."),
     *         ]),
     *     ]);
     * });
     * ```
     */
    Item: createAccordionItem,
    /**
     * Helper function to create accordion variant values.
     *
     * @param v - The variant string ("enclosed", "subtle", "outline")
     * @returns An East expression representing the accordion variant
     */
    Variant: AccordionVariant,
    Types: {
        /**
         * The concrete East type for Accordion container data.
         *
         * @property items - Array of accordion items
         * @property style - Optional styling configuration
         */
        Root: AccordionRootType,
        /**
         * The concrete East type for Accordion item data.
         *
         * @property value - Unique identifier for the item
         * @property trigger - Header/trigger text
         * @property content - Array of child UI components
         * @property disabled - Whether the item is disabled
         */
        Item: AccordionItemType,
        /**
         * Style type for Accordion container.
         *
         * @property multiple - Allow multiple items open simultaneously
         * @property collapsible - Allow all items to be closed
         * @property variant - Visual variant
         */
        Style: AccordionStyleType,
        /**
         * Style type for individual Accordion items.
         */
        ItemStyle: AccordionItemStyleType,
        /**
         * Variant type for Accordion appearance styles.
         *
         * @property enclosed - Enclosed panel style
         * @property subtle - Subtle background style
         * @property outline - Outlined style
         */
        Variant: AccordionVariantType,
    },
} as const;
