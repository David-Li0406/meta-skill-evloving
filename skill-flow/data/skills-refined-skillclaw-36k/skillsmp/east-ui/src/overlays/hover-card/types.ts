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
    IntegerType,
    VariantType,
    FunctionType,
} from "@elaraai/east";

import { PlacementType, type PlacementLiteral } from "../tooltip/types.js";

// Re-export PlacementType
export { PlacementType, type PlacementLiteral } from "../tooltip/types.js";

// ============================================================================
// HoverCard Size Type
// ============================================================================

/**
 * Size variant type for HoverCard component.
 *
 * @property xs - Extra small padding
 * @property sm - Small padding
 * @property md - Medium padding (default)
 * @property lg - Large padding
 */
export const HoverCardSizeType = VariantType({
    xs: NullType,
    sm: NullType,
    md: NullType,
    lg: NullType,
});

export type HoverCardSizeType = typeof HoverCardSizeType;
export type HoverCardSizeLiteral = "xs" | "sm" | "md" | "lg";

// ============================================================================
// HoverCard Style Type
// ============================================================================

/**
 * Style type for HoverCard component.
 *
 * @property size - HoverCard size variant
 * @property placement - Position relative to trigger
 * @property hasArrow - Show arrow pointing to trigger
 * @property openDelay - Delay before opening (ms)
 * @property closeDelay - Delay before closing (ms)
 * @property onOpenChange - Callback triggered when open state changes
 */
export const HoverCardStyleType = StructType({
    size: OptionType(HoverCardSizeType),
    placement: OptionType(PlacementType),
    hasArrow: OptionType(BooleanType),
    openDelay: OptionType(IntegerType),
    closeDelay: OptionType(IntegerType),
    /** Callback triggered when open state changes */
    onOpenChange: OptionType(FunctionType([BooleanType], NullType)),
});

export type HoverCardStyleType = typeof HoverCardStyleType;

// ============================================================================
// HoverCard Style Interface
// ============================================================================

/**
 * TypeScript interface for HoverCard style options.
 *
 * @property size - HoverCard size variant
 * @property placement - Position relative to trigger
 * @property hasArrow - Show arrow pointing to trigger
 * @property openDelay - Delay before opening (ms)
 * @property closeDelay - Delay before closing (ms)
 * @property open - Controlled open state
 * @property defaultOpen - Initial open state
 * @property lazyMount - Delay mounting until first open
 * @property unmountOnExit - Unmount when closed
 * @property onOpenChange - Callback triggered when open state changes
 */
export interface HoverCardStyle {
    /** HoverCard size variant */
    size?: SubtypeExprOrValue<HoverCardSizeType> | HoverCardSizeLiteral;
    /** Position relative to trigger */
    placement?: SubtypeExprOrValue<PlacementType> | PlacementLiteral;
    /** Show arrow pointing to trigger */
    hasArrow?: SubtypeExprOrValue<BooleanType>;
    /** Delay before opening (ms) */
    openDelay?: SubtypeExprOrValue<IntegerType>;
    /** Delay before closing (ms) */
    closeDelay?: SubtypeExprOrValue<IntegerType>;
    /** Controlled open state */
    open?: SubtypeExprOrValue<BooleanType>;
    /** Initial open state */
    defaultOpen?: SubtypeExprOrValue<BooleanType>;
    /** Delay mounting until first open */
    lazyMount?: SubtypeExprOrValue<BooleanType>;
    /** Unmount when closed */
    unmountOnExit?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when open state changes */
    onOpenChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
}
