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
    NullType,
    BooleanType,
    VariantType,
    variant,
} from "@elaraai/east";

// ============================================================================
// Placement Type
// ============================================================================

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
export const PlacementType = VariantType({
    /** Centered above the trigger */
    top: NullType,
    /** Above, aligned to start */
    "top-start": NullType,
    /** Above, aligned to end */
    "top-end": NullType,
    /** Centered below the trigger */
    bottom: NullType,
    /** Below, aligned to start */
    "bottom-start": NullType,
    /** Below, aligned to end */
    "bottom-end": NullType,
    /** Centered to the left */
    left: NullType,
    /** Left, aligned to start */
    "left-start": NullType,
    /** Left, aligned to end */
    "left-end": NullType,
    /** Centered to the right */
    right: NullType,
    /** Right, aligned to start */
    "right-start": NullType,
    /** Right, aligned to end */
    "right-end": NullType,
});

/**
 * Type representing the Placement structure.
 */
export type PlacementType = typeof PlacementType;

/**
 * String literal type for placement values.
 */
export type PlacementLiteral =
    | "top" | "top-start" | "top-end"
    | "bottom" | "bottom-start" | "bottom-end"
    | "left" | "left-start" | "left-end"
    | "right" | "right-start" | "right-end";

/**
 * Helper function to create placement values.
 *
 * @param placement - The placement string
 * @returns An East expression representing the placement
 *
 * @remarks
 * Use this helper to create placement values programmatically.
 * In most cases, you can pass string literals directly to the style property.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Tooltip, Button, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Tooltip.Root(
 *         Button.Root("Hover"),
 *         "Help text",
 *         { placement: Tooltip.Placement("top") }
 *     );
 * });
 * ```
 */
export function Placement(placement: PlacementLiteral): ExprType<PlacementType> {
    return East.value(variant(placement, null), PlacementType);
}

// ============================================================================
// Tooltip Style Type
// ============================================================================

/**
 * Style type for Tooltip component.
 *
 * @remarks
 * Contains optional styling properties for the tooltip.
 *
 * @property placement - Where to position the tooltip
 * @property hasArrow - Whether to show an arrow pointing to the trigger
 */
export const TooltipStyleType = StructType({
    placement: OptionType(PlacementType),
    hasArrow: OptionType(BooleanType),
});

/**
 * Type representing the TooltipStyle structure.
 */
export type TooltipStyleType = typeof TooltipStyleType;

// ============================================================================
// Tooltip Style Interface
// ============================================================================

/**
 * TypeScript interface for Tooltip style options.
 *
 * @property placement - Where to position the tooltip
 * @property hasArrow - Whether to show an arrow pointing to the trigger
 */
export interface TooltipStyle {
    /** Where to position the tooltip */
    placement?: SubtypeExprOrValue<PlacementType> | PlacementLiteral;
    /** Whether to show an arrow pointing to the trigger */
    hasArrow?: SubtypeExprOrValue<BooleanType>;
}
