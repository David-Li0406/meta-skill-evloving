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
// Drawer Size Type
// ============================================================================

/**
 * Size variant type for Drawer component.
 *
 * @property xs - Extra small (20rem max width)
 * @property sm - Small (28rem max width)
 * @property md - Medium (32rem max width)
 * @property lg - Large (42rem max width)
 * @property xl - Extra large (56rem max width)
 * @property full - Full viewport
 */
export const DrawerSizeType = VariantType({
    xs: NullType,
    sm: NullType,
    md: NullType,
    lg: NullType,
    xl: NullType,
    full: NullType,
});

export type DrawerSizeType = typeof DrawerSizeType;
export type DrawerSizeLiteral = "xs" | "sm" | "md" | "lg" | "xl" | "full";

// ============================================================================
// Drawer Placement Type
// ============================================================================

/**
 * Placement variant type for Drawer component.
 *
 * @property start - Left side (RTL-aware)
 * @property end - Right side (RTL-aware)
 * @property top - Top edge
 * @property bottom - Bottom edge
 */
export const DrawerPlacementType = VariantType({
    start: NullType,
    end: NullType,
    top: NullType,
    bottom: NullType,
});

export type DrawerPlacementType = typeof DrawerPlacementType;
export type DrawerPlacementLiteral = "start" | "end" | "top" | "bottom";

// ============================================================================
// Drawer Style Type
// ============================================================================

/**
 * Style type for Drawer component.
 *
 * @property size - Drawer size variant
 * @property placement - Edge placement
 * @property contained - Render within parent container
 * @property onOpenChange - Callback triggered when open state changes
 * @property onExitComplete - Callback triggered when exit animation completes
 */
export const DrawerStyleType = StructType({
    size: OptionType(DrawerSizeType),
    placement: OptionType(DrawerPlacementType),
    contained: OptionType(BooleanType),
    /** Callback triggered when open state changes */
    onOpenChange: OptionType(FunctionType([BooleanType], NullType)),
    /** Callback triggered when exit animation completes */
    onExitComplete: OptionType(FunctionType([], NullType)),
});

export type DrawerStyleType = typeof DrawerStyleType;

// ============================================================================
// Drawer Style Interface
// ============================================================================

/**
 * TypeScript interface for Drawer style options.
 *
 * @property size - Drawer size variant
 * @property placement - Edge placement
 * @property contained - Render within parent container
 * @property title - Drawer title
 * @property description - Drawer description
 * @property open - Controlled open state
 * @property defaultOpen - Initial open state
 * @property closeOnInteractOutside - Close when clicking outside
 * @property closeOnEscape - Close on escape key
 * @property lazyMount - Delay mounting until first open
 * @property unmountOnExit - Unmount when closed
 * @property onOpenChange - Callback triggered when open state changes
 * @property onExitComplete - Callback triggered when exit animation completes
 */
export interface DrawerStyle {
    /** Drawer size variant */
    size?: SubtypeExprOrValue<DrawerSizeType> | DrawerSizeLiteral;
    /** Edge placement */
    placement?: SubtypeExprOrValue<DrawerPlacementType> | DrawerPlacementLiteral;
    /** Render within parent container */
    contained?: SubtypeExprOrValue<BooleanType>;
    /** Drawer title */
    title?: SubtypeExprOrValue<StringType>;
    /** Drawer description */
    description?: SubtypeExprOrValue<StringType>;
    /** Controlled open state */
    open?: SubtypeExprOrValue<BooleanType>;
    /** Initial open state */
    defaultOpen?: SubtypeExprOrValue<BooleanType>;
    /** Close when clicking outside */
    closeOnInteractOutside?: SubtypeExprOrValue<BooleanType>;
    /** Close on escape key */
    closeOnEscape?: SubtypeExprOrValue<BooleanType>;
    /** Delay mounting until first open */
    lazyMount?: SubtypeExprOrValue<BooleanType>;
    /** Unmount when closed */
    unmountOnExit?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when open state changes */
    onOpenChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
    /** Callback triggered when exit animation completes */
    onExitComplete?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}
