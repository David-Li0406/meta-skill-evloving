/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East, OptionType,
    StructType,
    ArrayType,
    variant
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    HoverCardSizeType,
    HoverCardStyleType,
    type HoverCardStyle, PlacementType
} from "./types.js";

// Re-export types
export {
    HoverCardSizeType,
    HoverCardStyleType,
    type HoverCardStyle,
    PlacementType,
} from "./types.js";
export type { HoverCardSizeLiteral, PlacementLiteral } from "./types.js";

// ============================================================================
// HoverCard Type
// ============================================================================

/**
 * East StructType for HoverCard component.
 *
 * @remarks
 * HoverCard displays rich content when hovering over a trigger element.
 * Similar to Tooltip but with more structured content (e.g., user profiles).
 *
 * @property trigger - The UI component that shows the hover card on hover
 * @property body - Array of UI components for hover card content
 * @property style - Optional style configuration
 */
export const HoverCardType: StructType<{
    trigger: UIComponentType,
    body: ArrayType<UIComponentType>,
    style: OptionType<HoverCardStyleType>,
}> = StructType({
    trigger: UIComponentType,
    body: ArrayType(UIComponentType),
    style: OptionType(HoverCardStyleType),
});

/**
 * Type alias for HoverCardType.
 */
export type HoverCardType = typeof HoverCardType;

// ============================================================================
// HoverCard Function
// ============================================================================

/**
 * Creates a HoverCard component with a trigger and body content.
 *
 * @param trigger - The UI component that shows the hover card on hover
 * @param body - Array of UI components for hover card content
 * @param style - Optional styling configuration
 * @returns An East expression representing the hover card component
 *
 * @remarks
 * HoverCard displays rich preview content when hovering over an element.
 * Ideal for user profile previews, link previews, or contextual information.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { HoverCard, Text, Avatar, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return HoverCard.Root(
 *         Text.Root("@username"),
 *         [
 *             Avatar.Root({ name: "John Doe" }),
 *             Text.Root("Software Engineer"),
 *         ],
 *         { openDelay: 200n }
 *     );
 * });
 * ```
 */
function createHoverCard(
    trigger: SubtypeExprOrValue<UIComponentType>,
    body: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: HoverCardStyle
): ExprType<UIComponentType> {
    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), HoverCardSizeType)
            : style.size)
        : undefined;

    const placementValue = style?.placement
        ? (typeof style.placement === "string"
            ? East.value(variant(style.placement, null), PlacementType)
            : style.placement)
        : undefined;

    const hasStyle = sizeValue || placementValue || style?.hasArrow !== undefined ||
        style?.openDelay !== undefined || style?.closeDelay !== undefined || style?.onOpenChange !== undefined;

    return East.value(variant("HoverCard", {
        trigger: trigger,
        body: body,
        style: hasStyle
            ? variant("some", East.value({
                size: sizeValue ? variant("some", sizeValue) : variant("none", null),
                placement: placementValue ? variant("some", placementValue) : variant("none", null),
                hasArrow: style?.hasArrow !== undefined ? variant("some", style.hasArrow) : variant("none", null),
                openDelay: style?.openDelay !== undefined ? variant("some", style.openDelay) : variant("none", null),
                closeDelay: style?.closeDelay !== undefined ? variant("some", style.closeDelay) : variant("none", null),
                onOpenChange: style?.onOpenChange !== undefined ? variant("some", style.onOpenChange) : variant("none", null),
            }, HoverCardStyleType))
            : variant("none", null),
    }), UIComponentType);
}

/**
 * HoverCard component for rich hover previews.
 *
 * @remarks
 * Use `HoverCard.Root(trigger, body, style)` to create a hover card, or access `HoverCard.Types` for East types.
 */
export const HoverCard = {
    /**
     * Creates a HoverCard component with a trigger and body content.
     *
     * @param trigger - The UI component that shows the hover card on hover
     * @param body - Array of UI components for hover card content
     * @param style - Optional styling configuration
     * @returns An East expression representing the hover card component
     *
     * @remarks
     * HoverCard displays rich preview content when hovering over an element.
     * Ideal for user profile previews, link previews, or contextual information.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { HoverCard, Text, Avatar, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return HoverCard.Root(
     *         Text.Root("@username"),
     *         [
     *             Avatar.Root({ name: "John Doe" }),
     *             Text.Root("Software Engineer"),
     *         ],
     *         { openDelay: 200n }
     *     );
     * });
     * ```
     */
    Root: createHoverCard,
    Types: {
        /**
         * East StructType for HoverCard component.
         *
         * @remarks
         * HoverCard displays rich content when hovering over a trigger element.
         * Similar to Tooltip but with more structured content (e.g., user profiles).
         *
         * @property trigger - The UI component that shows the hover card on hover
         * @property body - Array of UI components for hover card content
         * @property style - Optional style configuration
         */
        HoverCard: HoverCardType,
        /**
         * Style type for HoverCard component.
         *
         * @property size - HoverCard size variant
         * @property placement - Position relative to trigger
         * @property hasArrow - Show arrow pointing to trigger
         * @property openDelay - Delay before opening (ms)
         * @property closeDelay - Delay before closing (ms)
         */
        Style: HoverCardStyleType,
        /**
         * Size variant type for HoverCard component.
         *
         * @property xs - Extra small padding
         * @property sm - Small padding
         * @property md - Medium padding (default)
         * @property lg - Large padding
         */
        Size: HoverCardSizeType,
        /**
         * Placement options for Tooltip positioning.
         *
         * @remarks
         * Controls where the tooltip appears relative to its trigger element.
         * Supports all cardinal directions with start/end variations.
         *
         * @property top - Centered above the trigger
         * @property top-start - Above, aligned to start
         * @property top-end - Above, aligned to end
         * @property bottom - Centered below the trigger
         * @property bottom-start - Below, aligned to start
         * @property bottom-end - Below, aligned to end
         * @property left - Centered to the left
         * @property left-start - Left, aligned to start
         * @property left-end - Left, aligned to end
         * @property right - Centered to the right
         * @property right-start - Right, aligned to start
         * @property right-end - Right, aligned to end
         */
        Placement: PlacementType,
    },
} as const;
