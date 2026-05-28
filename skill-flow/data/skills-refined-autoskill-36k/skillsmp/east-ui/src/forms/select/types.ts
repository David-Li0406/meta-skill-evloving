/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    StringType,
    BooleanType,
    ArrayType,
    NullType,
    FunctionType,
} from "@elaraai/east";

import { SizeType } from "../../style.js";
import type { SizeLiteral } from "../../style.js";

// ============================================================================
// Select Item Type
// ============================================================================

/**
 * Type for Select item data.
 *
 * @remarks
 * Each item in a Select dropdown has a value and display label.
 *
 * @property value - The value submitted when this item is selected
 * @property label - The display text shown to the user
 * @property disabled - Whether this item is disabled
 */
export const SelectItemType = StructType({
    value: StringType,
    label: StringType,
    disabled: OptionType(BooleanType),
});

export type SelectItemType = typeof SelectItemType;

/**
 * TypeScript interface for Select item style options.
 *
 * @remarks
 * Use this interface when creating Select items with styling.
 *
 * @property disabled - Whether this item is disabled
 */
export interface SelectItemStyle {
    /** Whether this item is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
}

// ============================================================================
// Select Root Type
// ============================================================================

/**
 * Type for Select component data.
 *
 * @remarks
 * Select is a dropdown selection control for choosing from a list of options.
 *
 * @property value - Currently selected value (none if nothing selected)
 * @property items - Array of selectable items
 * @property placeholder - Placeholder text when nothing is selected
 * @property multiple - Whether multiple selection is allowed
 * @property disabled - Whether the select is disabled
 * @property size - Size of the select control
 * @property onChange - Callback triggered when selection changes (single select)
 * @property onChangeMultiple - Callback triggered when selection changes (multi-select)
 * @property onOpenChange - Callback triggered when dropdown opens/closes
 */
export const SelectRootType = StructType({
    value: OptionType(StringType),
    items: ArrayType(SelectItemType),
    placeholder: OptionType(StringType),
    multiple: OptionType(BooleanType),
    disabled: OptionType(BooleanType),
    size: OptionType(SizeType),
    onChange: OptionType(FunctionType([StringType], NullType)),
    onChangeMultiple: OptionType(FunctionType([ArrayType(StringType)], NullType)),
    onOpenChange: OptionType(FunctionType([BooleanType], NullType)),
});

export type SelectRootType = typeof SelectRootType;

/**
 * TypeScript interface for Select component style options.
 *
 * @remarks
 * Use this interface when creating Select components with styling.
 *
 * @property placeholder - Placeholder text when nothing is selected
 * @property multiple - Whether multiple selection is allowed
 * @property disabled - Whether the select is disabled
 * @property size - Size of the select control
 * @property onChange - Callback triggered when selection changes (single select)
 * @property onChangeMultiple - Callback triggered when selection changes (multi-select)
 * @property onOpenChange - Callback triggered when dropdown opens/closes
 */
export interface SelectStyle {
    /** Placeholder text when nothing is selected */
    placeholder?: SubtypeExprOrValue<StringType>;
    /** Whether multiple selection is allowed */
    multiple?: SubtypeExprOrValue<BooleanType>;
    /** Whether the select is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Size of the select control (xs, sm, md, lg) */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Callback triggered when selection changes (single select) */
    onChange?: SubtypeExprOrValue<FunctionType<[StringType], NullType>>;
    /** Callback triggered when selection changes (multi-select) */
    onChangeMultiple?: SubtypeExprOrValue<FunctionType<[ArrayType<StringType>], NullType>>;
    /** Callback triggered when dropdown opens/closes */
    onOpenChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
}
