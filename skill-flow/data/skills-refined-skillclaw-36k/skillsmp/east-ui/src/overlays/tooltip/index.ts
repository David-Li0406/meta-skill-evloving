/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType,
    BooleanType,
    OptionType,
    StructType,
    variant,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    PlacementType,
    Placement,
    TooltipStyleType,
    type TooltipStyle,
} from "./types.js";

// Re-export types
export {
    PlacementType,
    Placement,
    TooltipStyleType,
    type TooltipStyle,
    type PlacementLiteral,
} from "./types.js";

// ============================================================================
// Tooltip Type
// ============================================================================

/**
 * East StructType for Tooltip component.
 *
 * @remarks
 * Tooltip wraps a trigger element and displays content on hover.
 * The trigger can be any UI component.
 *
 * @property trigger - The UI component that triggers the tooltip on hover
 * @property content - The tooltip text content
 * @property placement - Optional placement position
 * @property hasArrow - Whether to show an arrow pointing to the trigger
 */
export const TooltipType: StructType<{
    trigger: UIComponentType,
    content: StringType,
    placement: OptionType<PlacementType>,
    hasArrow: OptionType<BooleanType>,
}> = StructType({
    trigger: UIComponentType,
    content: StringType,
    placement: OptionType(PlacementType),
    hasArrow: OptionType(BooleanType),
});

/**
 * Type alias for TooltipType.
 */
export type TooltipType = typeof TooltipType;

// ============================================================================
// Tooltip Function
// ============================================================================

/**
 * Creates a Tooltip component with a trigger element and content.
 *
 * @param trigger - The UI component that triggers the tooltip on hover
 * @param content - The tooltip text content
 * @param style - Optional styling configuration
 * @returns An East expression representing the tooltip component
 *
 * @remarks
 * Tooltip displays additional information when hovering over an element.
 * The trigger can be any UI component (button, text, icon, etc.).
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Tooltip, Button, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Tooltip.Root(
 *         Button.Root("Hover me"),
 *         "This is a helpful tip"
 *     );
 * });
 * ```
 */
function createTooltip(
    trigger: SubtypeExprOrValue<UIComponentType>,
    content: SubtypeExprOrValue<StringType>,
    style?: TooltipStyle
): ExprType<UIComponentType> {
    const placementValue = style?.placement
        ? (typeof style.placement === "string"
            ? East.value(variant(style.placement, null), PlacementType)
            : style.placement)
        : undefined;

    return East.value(variant("Tooltip", {
        trigger: trigger,
        content: content,
        placement: placementValue ? variant("some", placementValue) : variant("none", null),
        hasArrow: style?.hasArrow !== undefined ? variant("some", style.hasArrow) : variant("none", null),
    }), UIComponentType);
}

/**
 * Tooltip component for displaying additional information on hover.
 *
 * @remarks
 * Use `Tooltip.Root(trigger, content, style)` to create a tooltip, or access `Tooltip.Types` for East types.
 */
export const Tooltip = {
    /**
     * Creates a Tooltip component with a trigger and content text.
     *
     * @param trigger - The UI component that triggers the tooltip on hover
     * @param content - The tooltip text content
     * @param style - Optional styling configuration
     * @returns An East expression representing the tooltip component
     *
     * @remarks
     * Tooltip displays additional information when hovering over an element.
     * The trigger can be any UI component (button, text, icon, etc.).
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Tooltip, Button, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Tooltip.Root(
     *         Button.Root("Hover me"),
     *         "This is a helpful tooltip",
     *         { placement: "top" }
     *     );
     * });
     * ```
     */
    Root: createTooltip,
    /**
     * Helper function to create tooltip placement values.
     *
     * @param v - The placement string
     * @returns An East expression representing the placement variant
     *
     * @remarks
     * Use this helper to create placement values programmatically. In most cases,
     * you can pass string literals directly to the style property.
     */
    Placement: Placement,
    Types: {
        /**
         * The concrete East type for Tooltip component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Tooltip
         * component. Tooltip displays text content when hovering over a trigger element.
         *
         * @property trigger - The UI component that triggers the tooltip on hover (UIComponentType)
         * @property content - The tooltip text content (StringType)
         * @property placement - Optional placement position (OptionType<PlacementType>)
         * @property hasArrow - Whether to show an arrow pointing to the trigger (OptionType<BooleanType>)
         */
        Tooltip: TooltipType,
        /**
         * The concrete East type for Tooltip style configuration.
         *
         * @remarks
         * This struct type defines the styling configuration for a Tooltip component.
         * Contains optional placement and arrow settings.
         *
         * @property placement - Where the tooltip appears relative to trigger (OptionType<PlacementType>)
         * @property hasArrow - Show arrow pointing to trigger (OptionType<BooleanType>)
         */
        Style: TooltipStyleType,
        /**
         * Placement variant type for Tooltip positioning.
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
