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
    FunctionType,
} from "@elaraai/east";

import { PlacementType, type PlacementLiteral } from "../tooltip/types.js";

// Re-export PlacementType for convenience
export { PlacementType, type PlacementLiteral } from "../tooltip/types.js";

// ============================================================================
// Menu Item Type
// ============================================================================

/**
 * Menu item variant type.
 *
 * @remarks
 * Menu items can be either an Item (clickable menu entry) or a Separator (visual divider).
 *
 * @property Item - A clickable menu item with value, label, and optional disabled state
 * @property Separator - A visual separator between menu items
 */
export const MenuItemType = VariantType({
    /** A clickable menu item */
    Item: StructType({
        /** Unique identifier for the item */
        value: StringType,
        /** Display text for the item */
        label: StringType,
        /** Whether the item is disabled */
        disabled: OptionType(BooleanType),
        /** Callback function when the item is selected */
        // onClick: FunctionType([], NullType, null),
    }),
    /** A visual separator between items */
    Separator: NullType,
});

/**
 * Type representing the MenuItem structure.
 */
export type MenuItemType = typeof MenuItemType;

// ============================================================================
// Menu Style Type
// ============================================================================

/**
 * Style type for Menu component.
 *
 * @remarks
 * Contains optional styling properties for the menu.
 *
 * @property placement - Where to position the menu relative to the trigger
 * @property onSelect - Callback triggered when a menu item is selected
 * @property onOpenChange - Callback triggered when open state changes
 */
export const MenuStyleType = StructType({
    placement: OptionType(PlacementType),
    /** Callback triggered when a menu item is selected */
    onSelect: OptionType(FunctionType([StringType], NullType)),
    /** Callback triggered when open state changes */
    onOpenChange: OptionType(FunctionType([BooleanType], NullType)),
});

/**
 * Type representing the MenuStyle structure.
 */
export type MenuStyleType = typeof MenuStyleType;

// ============================================================================
// Menu Style Interface
// ============================================================================

/**
 * TypeScript interface for Menu style options.
 *
 * @property placement - Where to position the menu relative to the trigger
 * @property onSelect - Callback triggered when a menu item is selected
 * @property onOpenChange - Callback triggered when open state changes
 */
export interface MenuStyle {
    /** Where to position the menu relative to the trigger */
    placement?: SubtypeExprOrValue<PlacementType> | PlacementLiteral;
    /** Callback triggered when a menu item is selected */
    onSelect?: SubtypeExprOrValue<FunctionType<[StringType], NullType>>;
    /** Callback triggered when open state changes */
    onOpenChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
}
