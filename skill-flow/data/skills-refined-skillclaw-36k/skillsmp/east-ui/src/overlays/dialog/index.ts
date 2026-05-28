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
    variant,
    NullType,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    DialogSizeType,
    DialogPlacementType,
    DialogScrollBehaviorType,
    DialogMotionPresetType,
    DialogRoleType,
    DialogStyleType,
    type DialogStyle
} from "./types.js";

// Re-export types
export {
    DialogSizeType,
    DialogPlacementType,
    DialogScrollBehaviorType,
    DialogMotionPresetType,
    DialogRoleType,
    DialogStyleType,
    type DialogStyle,
} from "./types.js";
export type { DialogSizeLiteral, DialogPlacementLiteral, DialogScrollBehaviorLiteral, DialogMotionPresetLiteral, DialogRoleLiteral } from "./types.js";

// ============================================================================
// Dialog Type
// ============================================================================

/**
 * East StructType for Dialog component.
 *
 * @remarks
 * Dialog is a modal overlay with a trigger and body content.
 * The trigger can be any UI component, and body contains UI children.
 *
 * @property trigger - The UI component that opens the dialog
 * @property body - Array of UI components for dialog content
 * @property title - Optional dialog title
 * @property description - Optional dialog description
 * @property style - Optional style configuration
 */
export const DialogType: StructType<{
    trigger: UIComponentType,
    body: ArrayType<UIComponentType>,
    title: OptionType<StringType>,
    description: OptionType<StringType>,
    style: OptionType<DialogStyleType>,
}> = StructType({
    trigger: UIComponentType,
    body: ArrayType(UIComponentType),
    title: OptionType(StringType),
    description: OptionType(StringType),
    style: OptionType(DialogStyleType),
});

/**
 * Type alias for DialogType.
 */
export type DialogType = typeof DialogType;

// ============================================================================
// Dialog Open Input Type
// ============================================================================

/**
 * East StructType for programmatic dialog opening.
 *
 * @remarks
 * This type is used with {@link dialog_open} to programmatically open a dialog
 * without a trigger element. Unlike {@link DialogType}, this does not include
 * a trigger property.
 *
 * @property body - Array of UI components for dialog content
 * @property title - Optional dialog title
 * @property description - Optional dialog description
 * @property style - Optional style configuration
 */
export const DialogOpenInputType: StructType<{
    body: ArrayType<UIComponentType>,
    title: OptionType<StringType>,
    description: OptionType<StringType>,
    style: OptionType<DialogStyleType>,
}> = StructType({
    body: ArrayType(UIComponentType),
    title: OptionType(StringType),
    description: OptionType(StringType),
    style: OptionType(DialogStyleType),
});

/**
 * Type alias for DialogOpenInputType.
 */
export type DialogOpenInputType = typeof DialogOpenInputType;

// ============================================================================
// Dialog Function
// ============================================================================

/**
 * Creates a Dialog component with a trigger and body content.
 *
 * @param trigger - The UI component that opens the dialog
 * @param body - Array of UI components for dialog content
 * @param style - Optional styling configuration
 * @returns An East expression representing the dialog component
 *
 * @remarks
 * Dialog is a modal window that appears above the main content.
 * It captures focus and prevents interaction with the underlying page.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Dialog, Button, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Dialog.Root(
 *         Button.Root("Open Dialog"),
 *         [Text.Root("Dialog content here")],
 *         { title: "My Dialog" }
 *     );
 * });
 * ```
 */
function createDialog(
    trigger: SubtypeExprOrValue<UIComponentType>,
    body: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: DialogStyle
): ExprType<UIComponentType> {
    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), DialogSizeType)
            : style.size)
        : undefined;

    const placementValue = style?.placement
        ? (typeof style.placement === "string"
            ? East.value(variant(style.placement, null), DialogPlacementType)
            : style.placement)
        : undefined;

    const scrollBehaviorValue = style?.scrollBehavior
        ? (typeof style.scrollBehavior === "string"
            ? East.value(variant(style.scrollBehavior, null), DialogScrollBehaviorType)
            : style.scrollBehavior)
        : undefined;

    const motionPresetValue = style?.motionPreset
        ? (typeof style.motionPreset === "string"
            ? East.value(variant(style.motionPreset, null), DialogMotionPresetType)
            : style.motionPreset)
        : undefined;

    const roleValue = style?.role
        ? (typeof style.role === "string"
            ? East.value(variant(style.role, null), DialogRoleType)
            : style.role)
        : undefined;

    const hasStyle = sizeValue || placementValue || scrollBehaviorValue || motionPresetValue || roleValue ||
        style?.onOpenChange !== undefined || style?.onExitComplete !== undefined ||
        style?.onEscapeKeyDown !== undefined || style?.onInteractOutside !== undefined;

    return East.value(variant("Dialog", {
        trigger: trigger,
        body: body,
        title: style?.title !== undefined ? variant("some", style.title) : variant("none", null),
        description: style?.description !== undefined ? variant("some", style.description) : variant("none", null),
        style: hasStyle
            ? variant("some", East.value({
                size: sizeValue ? variant("some", sizeValue) : variant("none", null),
                placement: placementValue ? variant("some", placementValue) : variant("none", null),
                scrollBehavior: scrollBehaviorValue ? variant("some", scrollBehaviorValue) : variant("none", null),
                motionPreset: motionPresetValue ? variant("some", motionPresetValue) : variant("none", null),
                role: roleValue ? variant("some", roleValue) : variant("none", null),
                onOpenChange: style?.onOpenChange !== undefined ? variant("some", style.onOpenChange) : variant("none", null),
                onExitComplete: style?.onExitComplete !== undefined ? variant("some", style.onExitComplete) : variant("none", null),
                onEscapeKeyDown: style?.onEscapeKeyDown !== undefined ? variant("some", style.onEscapeKeyDown) : variant("none", null),
                onInteractOutside: style?.onInteractOutside !== undefined ? variant("some", style.onInteractOutside) : variant("none", null),
            }, DialogStyleType))
            : variant("none", null),
    }), UIComponentType);
}

// ============================================================================
// Dialog Open Platform Function
// ============================================================================

/**
 * Platform function to programmatically open a dialog.
 *
 * @remarks
 * Opens a dialog without requiring a trigger element. The dialog content,
 * title, description, and style are specified in the {@link DialogOpenInputType} parameter.
 * Pass `Dialog.Implementation` to `ir.compile()` to enable this functionality.
 *
 * @param input - The dialog configuration including body content and style
 * @returns Null
 *
 * @example
 * ```ts
 * import { East, NullType, variant } from "@elaraai/east";
 * import { Dialog, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const showAlert = East.function([], NullType, $ => {
 *     $(Dialog.open(East.value({
 *         body: [Text.Root("Are you sure?")],
 *         title: variant("some", "Confirm"),
 *         description: variant("none", null),
 *         style: variant("none", null),
 *     }, Dialog.Types.OpenInput)));
 * });
 * ```
 */
export const dialog_open = East.platform(
    "dialog_open", 
    [DialogOpenInputType], 
    NullType,
    {
        optional: true
    }
);

/**
 * Dialog component for modal overlays.
 *
 * @remarks
 * Use `Dialog.Root(trigger, body, style)` to create a dialog, or access `Dialog.Types` for East types.
 */
export const Dialog = {
    /**
     * Creates a Dialog component with a trigger and body content.
     *
     * @param trigger - The UI component that opens the dialog
     * @param body - Array of UI components for dialog content
     * @param style - Optional styling configuration
     * @returns An East expression representing the dialog component
     *
     * @remarks
     * Dialog is a modal window that appears above the main content.
     * It captures focus and prevents interaction with the underlying page.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Dialog, Button, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Dialog.Root(
     *         Button.Root("Open Dialog"),
     *         [Text.Root("Dialog content here")],
     *         { title: "My Dialog" }
     *     );
     * });
     * ```
     */
    Root: createDialog,
    /**
     * Platform function to programmatically open a dialog.
     *
     * @remarks
     * Opens a dialog without requiring a trigger element. Pass `Dialog.Implementation`
     * to `ir.compile()` to enable this functionality.
     *
     * @example
     * ```ts
     * import { East, NullType, variant } from "@elaraai/east";
     * import { Dialog, Text } from "@elaraai/east-ui";
     *
     * const showAlert = East.function([], NullType, $ => {
     *     $(Dialog.open(East.value({
     *         body: [Text.Root("Are you sure?")],
     *         title: variant("some", "Confirm"),
     *         description: variant("none", null),
     *         style: variant("none", null),
     *     }, Dialog.Types.OpenInput)));
     * });
     * ```
     */
    open: dialog_open,
    Types: {
        /**
         * East StructType for Dialog component.
         *
         * @remarks
         * Dialog is a modal overlay with a trigger and body content.
         * The trigger can be any UI component, and body contains UI children.
         *
         * @property trigger - The UI component that opens the dialog
         * @property body - Array of UI components for dialog content
         * @property title - Optional dialog title
         * @property description - Optional dialog description
         * @property style - Optional style configuration
         */
        Dialog: DialogType,
        /**
         * Style type for Dialog component.
         *
         * @property size - Dialog size variant
         * @property placement - Vertical positioning
         * @property scrollBehavior - Scroll behavior
         * @property motionPreset - Animation style
         * @property role - ARIA role
         */
        Style: DialogStyleType,
        /**
         * Size variant type for Dialog component.
         *
         * @property xs - Extra small (24rem max width)
         * @property sm - Small (28rem max width)
         * @property md - Medium (32rem max width)
         * @property lg - Large (42rem max width)
         * @property xl - Extra large (56rem max width)
         * @property cover - Full viewport with padding
         * @property full - Full viewport width
         */
        Size: DialogSizeType,
        /**
         * Placement variant type for Dialog component.
         *
         * @property center - Center of viewport
         * @property top - Top of viewport
         * @property bottom - Bottom of viewport
         */
        Placement: DialogPlacementType,
        /**
         * Scroll behavior variant type for Dialog component.
         *
         * @property inside - Content scrolls inside dialog
         * @property outside - Positioner handles scrolling
         */
        ScrollBehavior: DialogScrollBehaviorType,
        /**
         * Motion preset variant type for Dialog component.
         *
         * @property scale - Scale and fade animation
         * @property slide-in-bottom - Slide from bottom
         * @property slide-in-top - Slide from top
         * @property slide-in-left - Slide from left
         * @property slide-in-right - Slide from right
         * @property none - No animation
         */
        MotionPreset: DialogMotionPresetType,
        /**
         * ARIA role variant type for Dialog component.
         *
         * @property dialog - Standard dialog role
         * @property alertdialog - Alert dialog role for confirmations
         */
        Role: DialogRoleType,
        /**
         * East StructType for programmatic dialog opening.
         *
         * @remarks
         * Use this type with {@link Dialog.open} to programmatically open a dialog
         * without a trigger element.
         *
         * @property body - Array of UI components for dialog content
         * @property title - Optional dialog title
         * @property description - Optional dialog description
         * @property style - Optional style configuration
         */
        OpenInput: DialogOpenInputType,
    },
} as const;
