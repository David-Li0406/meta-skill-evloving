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
    ArrayType,
    variant,
} from "@elaraai/east";

import { SizeType, OverflowType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import { CardStyleType, CardVariantType, CardVariant, type CardStyle } from "./types.js";

// Re-export types
export { CardStyleType, CardVariantType, CardVariant, type CardStyle, type CardVariantLiteral } from "./types.js";

// ============================================================================
// Card Type
// ============================================================================

/**
 * The concrete East type for Card component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for a Card component.
 * Card is a container component that can hold child components in its body,
 * with optional header and footer sections.
 *
 * @property header - Optional header component (use Stack for multiple elements)
 * @property body - Array of child UI components for the main content
 * @property footer - Optional footer component (use Stack for multiple elements)
 * @property style - Optional styling configuration wrapped in OptionType
 */
export const CardType: StructType<{
    header: OptionType<UIComponentType>,
    body: ArrayType<UIComponentType>,
    footer: OptionType<UIComponentType>,
    style: OptionType<CardStyleType>,
}> = StructType({
    header: OptionType(UIComponentType),
    body: ArrayType(UIComponentType),
    footer: OptionType(UIComponentType),
    style: OptionType(CardStyleType),
});

/**
 * Type representing the Card component structure.
 */
export type CardType = typeof CardType;

// ============================================================================
// Card Options Interface
// ============================================================================

/**
 * TypeScript interface for Card options (header, footer, and style).
 *
 * @property header - Optional header component (single UIComponentType, use Stack for multiple)
 * @property footer - Optional footer component (single UIComponentType, use Stack for multiple)
 */
export interface CardOptions extends CardStyle {
    /** Optional header component (use Stack/HStack/VStack for multiple elements) */
    header?: ExprType<UIComponentType>;
    /** Optional footer component (use Stack/HStack/VStack for multiple elements) */
    footer?: ExprType<UIComponentType>;
}

// ============================================================================
// Card Function
// ============================================================================

/**
 * Creates a Card container component with children and optional styling.
 *
 * @param children - Array of child UI components for the card body
 * @param options - Optional configuration including header, footer, and styling
 * @returns An East expression representing the styled card component
 *
 * @remarks
 * Card is a container for grouping related content together. It supports
 * optional header and footer sections, and contains child components in its body.
 * For multiple elements in header/footer, wrap them in a Stack component.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Card, Text, Button, Heading, HStack, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Card.Root([
 *         Text.Root("Card content here"),
 *     ], {
 *         header: Heading.Root("Card Title"),
 *         footer: HStack.Root([
 *             Button.Root("Cancel", { variant: "outline" }),
 *             Button.Root("Save"),
 *         ]),
 *         variant: "elevated",
 *         height: "100%",
 *         flex: "1",
 *     });
 * });
 * ```
 */
function createCard(
    children: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    options?: CardOptions
): ExprType<UIComponentType> {
    const variantValue = options?.variant
        ? (typeof options.variant === "string"
            ? East.value(variant(options.variant, null), CardVariantType)
            : options.variant)
        : undefined;

    const sizeValue = options?.size
        ? (typeof options.size === "string"
            ? East.value(variant(options.size, null), SizeType)
            : options.size)
        : undefined;

    const overflowValue = options?.overflow
        ? (typeof options.overflow === "string"
            ? East.value(variant(options.overflow, null), OverflowType)
            : options.overflow)
        : undefined;

    const toStringOption = (val: SubtypeExprOrValue<typeof import("@elaraai/east").StringType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const hasStyle = options?.variant !== undefined ||
        options?.size !== undefined ||
        options?.height !== undefined ||
        options?.minHeight !== undefined ||
        options?.maxHeight !== undefined ||
        options?.width !== undefined ||
        options?.minWidth !== undefined ||
        options?.maxWidth !== undefined ||
        options?.flex !== undefined ||
        options?.overflow !== undefined;

    return East.value(variant("Card", {
        header: options?.header ? variant("some", options.header) : variant("none", null),
        body: children,
        footer: options?.footer ? variant("some", options.footer) : variant("none", null),
        style: hasStyle ? variant("some", East.value({
            variant: variantValue ? variant("some", variantValue) : variant("none", null),
            size: sizeValue ? variant("some", sizeValue) : variant("none", null),
            height: toStringOption(options?.height),
            minHeight: toStringOption(options?.minHeight),
            maxHeight: toStringOption(options?.maxHeight),
            width: toStringOption(options?.width),
            minWidth: toStringOption(options?.minWidth),
            maxWidth: toStringOption(options?.maxWidth),
            flex: toStringOption(options?.flex),
            overflow: overflowValue ? variant("some", overflowValue) : variant("none", null),
        }, CardStyleType)) : variant("none", null),
    }), UIComponentType);
}

/**
 * Card container component for grouping related content.
 *
 * @remarks
 * Use `Card.Root(children, options)` to create a card, or access `Card.Types.Card` for the East type.
 *
 * @example
 * ```ts
 * // Simple card with body only
 * Card.Root([Text.Root("Content")])
 *
 * // Card with header
 * Card.Root([Text.Root("Content")], {
 *     header: Heading.Root("Title"),
 * })
 *
 * // Card with header and footer
 * Card.Root([Text.Root("Content")], {
 *     header: VStack.Root([
 *         Heading.Root("Title"),
 *         Text.Root("Description"),
 *     ]),
 *     footer: Button.Root("Action"),
 *     variant: "elevated",
 * })
 *
 * // Card that fills available space
 * Card.Root([...], {
 *     height: "100%",
 *     flex: "1",
 * })
 * ```
 */
export const Card = {
    /**
     * Creates a Card container component with children and optional styling.
     *
     * @param children - Array of child UI components for the body
     * @param options - Optional configuration including header, footer, and styling
     * @returns An East expression representing the card component
     *
     * @remarks
     * Card is a container component that groups related content with optional
     * header and footer sections. Use Stack components for multiple elements
     * in header/footer.
     *
     * @example
     * ```ts
     * Card.Root([
     *     Text.Root("Main content"),
     * ], {
     *     header: Heading.Root("Card Title"),
     *     footer: HStack.Root([
     *         Button.Root("Cancel", { variant: "outline" }),
     *         Button.Root("Save"),
     *     ]),
     *     variant: "elevated",
     *     minHeight: "200px",
     * });
     * ```
     */
    Root: createCard,
    /**
     * Helper function to create card variant values.
     *
     * @param v - The variant string ("elevated", "outline", "subtle")
     * @returns An East expression representing the card variant
     */
    Variant: CardVariant,
    Types: {
        /**
         * The concrete East type for Card component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Card component.
         *
         * @property header - Optional header component
         * @property body - Array of child UI components
         * @property footer - Optional footer component
         * @property style - Optional styling configuration
         */
        Card: CardType,
        /**
         * Style type for Card component configuration.
         *
         * @remarks
         * This struct type defines the styling configuration for a Card.
         *
         * @property variant - Visual variant (elevated, outline, subtle)
         * @property size - Size of the card (sm, md, lg)
         * @property height - Height (Chakra token or CSS value)
         * @property minHeight - Min height (Chakra token or CSS value)
         * @property maxHeight - Max height (Chakra token or CSS value)
         * @property width - Width (Chakra token or CSS value)
         * @property minWidth - Min width (Chakra token or CSS value)
         * @property maxWidth - Max width (Chakra token or CSS value)
         * @property flex - Flex property for grow/shrink behavior
         * @property overflow - Overflow behavior
         */
        Style: CardStyleType,
        /**
         * Variant type for Card appearance styles.
         *
         * @property elevated - Card with shadow elevation
         * @property outline - Card with border outline
         * @property subtle - Card with subtle background
         */
        Variant: CardVariantType,
    },
} as const;
