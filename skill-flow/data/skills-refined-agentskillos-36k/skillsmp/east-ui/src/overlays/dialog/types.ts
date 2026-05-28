/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    NullType,
    BooleanType,
    VariantType,
    StringType,
    FunctionType,
} from "@elaraai/east";

// ============================================================================
// Dialog Size Type
// ============================================================================

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
export const DialogSizeType = VariantType({
    xs: NullType,
    sm: NullType,
    md: NullType,
    lg: NullType,
    xl: NullType,
    cover: NullType,
    full: NullType,
});

export type DialogSizeType = typeof DialogSizeType;
export type DialogSizeLiteral = "xs" | "sm" | "md" | "lg" | "xl" | "cover" | "full";

// ============================================================================
// Dialog Placement Type
// ============================================================================

/**
 * Placement variant type for Dialog component.
 *
 * @property center - Center of viewport
 * @property top - Top of viewport
 * @property bottom - Bottom of viewport
 */
export const DialogPlacementType = VariantType({
    center: NullType,
    top: NullType,
    bottom: NullType,
});

export type DialogPlacementType = typeof DialogPlacementType;
export type DialogPlacementLiteral = "center" | "top" | "bottom";

// ============================================================================
// Dialog Scroll Behavior Type
// ============================================================================

/**
 * Scroll behavior variant type for Dialog component.
 *
 * @property inside - Content scrolls inside dialog
 * @property outside - Positioner handles scrolling
 */
export const DialogScrollBehaviorType = VariantType({
    inside: NullType,
    outside: NullType,
});

export type DialogScrollBehaviorType = typeof DialogScrollBehaviorType;
export type DialogScrollBehaviorLiteral = "inside" | "outside";

// ============================================================================
// Dialog Motion Preset Type
// ============================================================================

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
export const DialogMotionPresetType = VariantType({
    scale: NullType,
    "slide-in-bottom": NullType,
    "slide-in-top": NullType,
    "slide-in-left": NullType,
    "slide-in-right": NullType,
    none: NullType,
});

export type DialogMotionPresetType = typeof DialogMotionPresetType;
export type DialogMotionPresetLiteral = "scale" | "slide-in-bottom" | "slide-in-top" | "slide-in-left" | "slide-in-right" | "none";

// ============================================================================
// Dialog Role Type
// ============================================================================

/**
 * ARIA role variant type for Dialog component.
 *
 * @property dialog - Standard dialog role
 * @property alertdialog - Alert dialog role for confirmations
 */
export const DialogRoleType = VariantType({
    dialog: NullType,
    alertdialog: NullType,
});

export type DialogRoleType = typeof DialogRoleType;
export type DialogRoleLiteral = "dialog" | "alertdialog";

// ============================================================================
// Dialog Style Type
// ============================================================================

/**
 * Style type for Dialog component.
 *
 * @property size - Dialog size variant
 * @property placement - Vertical positioning
 * @property scrollBehavior - Scroll behavior
 * @property motionPreset - Animation style
 * @property role - ARIA role
 * @property onOpenChange - Callback triggered when open state changes
 * @property onExitComplete - Callback triggered when exit animation completes
 * @property onEscapeKeyDown - Callback triggered when escape key is pressed
 * @property onInteractOutside - Callback triggered when clicking outside the dialog
 */
export const DialogStyleType = StructType({
    size: OptionType(DialogSizeType),
    placement: OptionType(DialogPlacementType),
    scrollBehavior: OptionType(DialogScrollBehaviorType),
    motionPreset: OptionType(DialogMotionPresetType),
    role: OptionType(DialogRoleType),
    /** Callback triggered when open state changes */
    onOpenChange: OptionType(FunctionType([BooleanType], NullType)),
    /** Callback triggered when exit animation completes */
    onExitComplete: OptionType(FunctionType([], NullType)),
    /** Callback triggered when escape key is pressed */
    onEscapeKeyDown: OptionType(FunctionType([], NullType)),
    /** Callback triggered when clicking outside the dialog */
    onInteractOutside: OptionType(FunctionType([], NullType)),
});

export type DialogStyleType = typeof DialogStyleType;

// ============================================================================
// Dialog Style Interface
// ============================================================================

/**
 * TypeScript interface for Dialog style options.
 *
 * @property size - Dialog size variant
 * @property placement - Vertical positioning
 * @property scrollBehavior - Scroll behavior
 * @property motionPreset - Animation style
 * @property role - ARIA role
 * @property title - Dialog title
 * @property description - Dialog description
 * @property open - Controlled open state
 * @property defaultOpen - Initial open state
 * @property modal - Enable modal mode
 * @property closeOnInteractOutside - Close when clicking outside
 * @property closeOnEscape - Close on escape key
 * @property preventScroll - Prevent body scroll
 * @property trapFocus - Trap focus inside dialog
 * @property lazyMount - Delay mounting until first open
 * @property unmountOnExit - Unmount when closed
 * @property onOpenChange - Callback triggered when open state changes
 * @property onExitComplete - Callback triggered when exit animation completes
 * @property onEscapeKeyDown - Callback triggered when escape key is pressed
 * @property onInteractOutside - Callback triggered when clicking outside the dialog
 */
export interface DialogStyle {
    /** Dialog size variant */
    size?: SubtypeExprOrValue<DialogSizeType> | DialogSizeLiteral;
    /** Vertical positioning */
    placement?: SubtypeExprOrValue<DialogPlacementType> | DialogPlacementLiteral;
    /** Scroll behavior */
    scrollBehavior?: SubtypeExprOrValue<DialogScrollBehaviorType> | DialogScrollBehaviorLiteral;
    /** Animation style */
    motionPreset?: SubtypeExprOrValue<DialogMotionPresetType> | DialogMotionPresetLiteral;
    /** ARIA role */
    role?: SubtypeExprOrValue<DialogRoleType> | DialogRoleLiteral;
    /** Dialog title */
    title?: SubtypeExprOrValue<StringType>;
    /** Dialog description */
    description?: SubtypeExprOrValue<StringType>;
    /** Controlled open state */
    open?: SubtypeExprOrValue<BooleanType>;
    /** Initial open state */
    defaultOpen?: SubtypeExprOrValue<BooleanType>;
    /** Enable modal mode */
    modal?: SubtypeExprOrValue<BooleanType>;
    /** Close when clicking outside */
    closeOnInteractOutside?: SubtypeExprOrValue<BooleanType>;
    /** Close on escape key */
    closeOnEscape?: SubtypeExprOrValue<BooleanType>;
    /** Prevent body scroll */
    preventScroll?: SubtypeExprOrValue<BooleanType>;
    /** Trap focus inside dialog */
    trapFocus?: SubtypeExprOrValue<BooleanType>;
    /** Delay mounting until first open */
    lazyMount?: SubtypeExprOrValue<BooleanType>;
    /** Unmount when closed */
    unmountOnExit?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when open state changes */
    onOpenChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
    /** Callback triggered when exit animation completes */
    onExitComplete?: SubtypeExprOrValue<FunctionType<[], NullType>>;
    /** Callback triggered when escape key is pressed */
    onEscapeKeyDown?: SubtypeExprOrValue<FunctionType<[], NullType>>;
    /** Callback triggered when clicking outside the dialog */
    onInteractOutside?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}
