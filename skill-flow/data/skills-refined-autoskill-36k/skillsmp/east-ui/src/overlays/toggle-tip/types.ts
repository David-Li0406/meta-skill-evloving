/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    BooleanType,
    NullType,
    FunctionType,
} from "@elaraai/east";

import { PlacementType, type PlacementLiteral } from "../tooltip/types.js";

// Re-export PlacementType
export { PlacementType, type PlacementLiteral } from "../tooltip/types.js";

// ============================================================================
// ToggleTip Style Type
// ============================================================================

/**
 * Style type for ToggleTip component.
 *
 * @property placement - Position relative to trigger
 * @property hasArrow - Show arrow pointing to trigger
 * @property onOpenChange - Callback triggered when open state changes
 */
export const ToggleTipStyleType = StructType({
    placement: OptionType(PlacementType),
    hasArrow: OptionType(BooleanType),
    /** Callback triggered when open state changes */
    onOpenChange: OptionType(FunctionType([BooleanType], NullType)),
});

export type ToggleTipStyleType = typeof ToggleTipStyleType;

// ============================================================================
// ToggleTip Style Interface
// ============================================================================

/**
 * TypeScript interface for ToggleTip style options.
 *
 * @property placement - Position relative to trigger
 * @property hasArrow - Show arrow pointing to trigger
 * @property open - Controlled open state
 * @property defaultOpen - Initial open state
 * @property closeOnInteractOutside - Close when clicking outside
 * @property closeOnEscape - Close on escape key
 * @property onOpenChange - Callback triggered when open state changes
 */
export interface ToggleTipStyle {
    /** Position relative to trigger */
    placement?: SubtypeExprOrValue<PlacementType> | PlacementLiteral;
    /** Show arrow pointing to trigger */
    hasArrow?: SubtypeExprOrValue<BooleanType>;
    /** Controlled open state */
    open?: SubtypeExprOrValue<BooleanType>;
    /** Initial open state */
    defaultOpen?: SubtypeExprOrValue<BooleanType>;
    /** Close when clicking outside */
    closeOnInteractOutside?: SubtypeExprOrValue<BooleanType>;
    /** Close on escape key */
    closeOnEscape?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when open state changes */
    onOpenChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
}
