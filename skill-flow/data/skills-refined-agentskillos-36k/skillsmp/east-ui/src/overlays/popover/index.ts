/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType, OptionType,
    StructType,
    ArrayType,
    variant
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    PopoverSizeType,
    PopoverStyleType,
    type PopoverStyle, PlacementType
} from "./types.js";

// Re-export types
export {
    PopoverSizeType,
    PopoverStyleType,
    type PopoverStyle,
    PlacementType,
} from "./types.js";
export type { PopoverSizeLiteral, PlacementLiteral } from "./types.js";

// ============================================================================
// Popover Type
// ============================================================================

/**
 * East StructType for Popover component.
 *
 * @remarks
 * Popover is a floating panel that appears near a trigger element.
 * It can contain interactive content and is controlled via click.
 *
 * @property trigger - The UI component that opens the popover
 * @property body - Array of UI components for popover content
 * @property title - Optional popover title
 * @property description - Optional popover description
 * @property style - Optional style configuration
 */
export const PopoverType: StructType<{
    trigger: UIComponentType,
    body: ArrayType<UIComponentType>,
    title: OptionType<StringType>,
    description: OptionType<StringType>,
    style: OptionType<PopoverStyleType>,
}> = StructType({
    trigger: UIComponentType,
    body: ArrayType(UIComponentType),
    title: OptionType(StringType),
    description: OptionType(StringType),
    style: OptionType(PopoverStyleType),
});

/**
 * Type alias for PopoverType.
 */
export type PopoverType = typeof PopoverType;

// ============================================================================
// Popover Function
// ============================================================================

/**
 * Creates a Popover component with a trigger and body content.
 *
 * @param trigger - The UI component that opens the popover
 * @param body - Array of UI components for popover content
 * @param style - Optional styling configuration
 * @returns An East expression representing the popover component
 *
 * @remarks
 * Popover displays rich interactive content in a floating panel.
 * Unlike Tooltip, it's controlled via click and can contain form elements.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Popover, Button, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Popover.Root(
 *         Button.Root("Edit"),
 *         [Text.Root("Edit your profile")],
 *         { title: "Edit Profile" }
 *     );
 * });
 * ```
 */
function createPopover(
    trigger: SubtypeExprOrValue<UIComponentType>,
    body: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: PopoverStyle
): ExprType<UIComponentType> {
    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), PopoverSizeType)
            : style.size)
        : undefined;

    const placementValue = style?.placement
        ? (typeof style.placement === "string"
            ? East.value(variant(style.placement, null), PlacementType)
            : style.placement)
        : undefined;

    const hasStyle = sizeValue || placementValue || style?.hasArrow !== undefined ||
        style?.gutter !== undefined || style?.onOpenChange !== undefined;

    return East.value(variant("Popover", {
        trigger: trigger,
        body: body,
        title: style?.title !== undefined ? variant("some", style.title) : variant("none", null),
        description: style?.description !== undefined ? variant("some", style.description) : variant("none", null),
        style: hasStyle
            ? variant("some", East.value({
                size: sizeValue ? variant("some", sizeValue) : variant("none", null),
                placement: placementValue ? variant("some", placementValue) : variant("none", null),
                hasArrow: style?.hasArrow !== undefined ? variant("some", style.hasArrow) : variant("none", null),
                gutter: style?.gutter !== undefined ? variant("some", style.gutter) : variant("none", null),
                onOpenChange: style?.onOpenChange !== undefined ? variant("some", style.onOpenChange) : variant("none", null),
            }, PopoverStyleType))
            : variant("none", null),
    }), UIComponentType);
}

/**
 * Popover component for floating interactive content.
 *
 * @remarks
 * Use `Popover.Root(trigger, body, style)` to create a popover, or access `Popover.Types` for East types.
 */
export const Popover = {
    /**
     * Creates a Popover component with a trigger and body content.
     *
     * @param trigger - The UI component that opens the popover
     * @param body - Array of UI components for popover content
     * @param style - Optional styling configuration
     * @returns An East expression representing the popover component
     *
     * @remarks
     * Popover displays rich interactive content in a floating panel.
     * Unlike Tooltip, it's controlled via click and can contain form elements.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Popover, Button, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Popover.Root(
     *         Button.Root("Show Info"),
     *         [Text.Root("Popover content here")],
     *         { title: "Information" }
     *     );
     * });
     * ```
     */
    Root: createPopover,
    Types: {
        /**
         * The concrete East type for Popover component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Popover
         * component. Popover is a floating panel that appears near a trigger element
         * and can contain interactive content.
         *
         * @property trigger - The UI component that opens the popover (UIComponentType)
         * @property body - Array of UI components for popover content (ArrayType<UIComponentType>)
         * @property title - Optional popover title (OptionType<StringType>)
         * @property description - Optional popover description (OptionType<StringType>)
         * @property style - Optional style configuration (OptionType<PopoverStyleType>)
         */
        Popover: PopoverType,
        /**
         * The concrete East type for Popover style configuration.
         *
         * @remarks
         * This struct type defines the styling configuration for a Popover component.
         * Controls the popover size, positioning, and visual appearance.
         *
         * @property size - Popover size variant: xs, sm, md, lg (OptionType<PopoverSizeType>)
         * @property placement - Position relative to trigger (OptionType<PlacementType>)
         * @property hasArrow - Show arrow pointing to trigger (OptionType<BooleanType>)
         * @property gutter - Gap between trigger and popover (OptionType<IntegerType>)
         */
        Style: PopoverStyleType,
        /**
         * Size variant type for Popover component dimensions.
         *
         * @remarks
         * This variant type provides type-safe size options for popovers.
         * Affects the padding and maximum width of the popover container.
         *
         * @property xs - Extra small popover with minimal padding
         * @property sm - Small popover with compact padding
         * @property md - Medium popover with standard padding (default)
         * @property lg - Large popover with generous padding
         */
        Size: PopoverSizeType,
        /**
         * Placement variant type for Popover positioning.
         *
         * @remarks
         * Controls where the popover appears relative to its trigger element.
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
