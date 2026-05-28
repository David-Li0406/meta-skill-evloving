/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    StringType,
    NullType,
    BooleanType,
    VariantType,
    IntegerType,
    FunctionType,
} from "@elaraai/east";

// ============================================================================
// ActionBar Item Type
// ============================================================================

/**
 * Action bar item variant type.
 *
 * @property Action - A clickable action with value and label
 * @property Separator - A visual separator between actions
 */
export const ActionBarItemType = VariantType({
    Action: StructType({
        value: StringType,
        label: StringType,
        disabled: OptionType(BooleanType),
    }),
    Separator: NullType,
});

export type ActionBarItemType = typeof ActionBarItemType;

// ============================================================================
// ActionBar Style Type
// ============================================================================

/**
 * Style type for ActionBar component.
 *
 * @remarks
 * ActionBar has fixed styling - no size/variant options.
 *
 * @property onSelect - Callback triggered when an action is selected
 * @property onOpenChange - Callback triggered when open state changes
 */
export const ActionBarStyleType = StructType({
    /** Callback triggered when an action is selected */
    onSelect: OptionType(FunctionType([StringType], NullType)),
    /** Callback triggered when open state changes */
    onOpenChange: OptionType(FunctionType([BooleanType], NullType)),
});

export type ActionBarStyleType = typeof ActionBarStyleType;

// ============================================================================
// ActionBar Style Interface
// ============================================================================

/**
 * TypeScript interface for ActionBar style options.
 *
 * @property selectionCount - Selection count to display
 * @property selectionLabel - Label for selection (e.g., "items selected")
 * @property open - Controlled open state
 * @property defaultOpen - Initial open state
 * @property closeOnInteractOutside - Close when clicking outside
 * @property closeOnEscape - Close on escape key
 * @property onSelect - Callback triggered when an action is selected
 * @property onOpenChange - Callback triggered when open state changes
 */
export interface ActionBarStyle {
    /** Selection count to display */
    selectionCount?: SubtypeExprOrValue<IntegerType>;
    /** Label for selection (e.g., "items selected") */
    selectionLabel?: SubtypeExprOrValue<StringType>;
    /** Controlled open state */
    open?: SubtypeExprOrValue<BooleanType>;
    /** Initial open state */
    defaultOpen?: SubtypeExprOrValue<BooleanType>;
    /** Close when clicking outside */
    closeOnInteractOutside?: SubtypeExprOrValue<BooleanType>;
    /** Close on escape key */
    closeOnEscape?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when an action is selected */
    onSelect?: SubtypeExprOrValue<FunctionType<[StringType], NullType>>;
    /** Callback triggered when open state changes */
    onOpenChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
}
