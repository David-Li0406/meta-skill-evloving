/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType,
    ArrayType,
    variant,
    some,
    none,
} from "@elaraai/east";

import { SizeType } from "../../style.js";
import {
    SelectItemType,
    SelectRootType,
    type SelectItemStyle,
    type SelectStyle,
} from "./types.js";
import { UIComponentType } from "../../component.js";

// Re-export types
export {
    SelectItemType,
    SelectRootType,
    type SelectItemStyle,
    type SelectStyle,
} from "./types.js";

// ============================================================================
// Select Item Function
// ============================================================================

/**
 * Creates a SelectItem with value, label, and optional styling.
 *
 * @param value - The value submitted when this item is selected
 * @param label - The display text shown to the user
 * @param style - Optional styling configuration
 * @returns An East expression representing the select item
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Select, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Select.Root("", [
 *         Select.Item("us", "United States"),
 *         Select.Item("restricted", "Restricted", { disabled: true }),
 *     ]);
 * });
 * ```
 */
function createSelectItem(
    value: SubtypeExprOrValue<StringType>,
    label: SubtypeExprOrValue<StringType>,
    style?: SelectItemStyle
): ExprType<SelectItemType> {
    return East.value({
        value: value,
        label: label,
        disabled: style?.disabled !== undefined ? some(style.disabled) : none,
    }, SelectItemType);
}

// ============================================================================
// Select Root Function
// ============================================================================

/**
 * Creates a Select component with value, items, and optional styling.
 *
 * @param value - Currently selected value (null/undefined for no selection)
 * @param items - Array of selectable items
 * @param style - Optional styling configuration
 * @returns An East expression representing the select component
 *
 * @remarks
 * Select is a dropdown control for choosing from predefined options.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Select, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Select.Root("", [
 *         Select.Item("us", "United States"),
 *         Select.Item("uk", "United Kingdom"),
 *         Select.Item("ca", "Canada"),
 *     ], {
 *         placeholder: "Select a country",
 *     });
 * });
 * ```
 */
export function createSelectRoot_(
    value: SubtypeExprOrValue<StringType>,
    items: SubtypeExprOrValue<ArrayType<SelectItemType>>,
    style?: SelectStyle
): ExprType<SelectRootType> {
    const toStringOption = (val: SubtypeExprOrValue<StringType> | null | undefined) => {
        if (val === undefined || val === null || val === "") return none;
        return some(val);
    };

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), SizeType)
            : style.size)
        : undefined;

    return East.value({
        value: toStringOption(value),
        items: East.value(items, ArrayType(SelectItemType)),
        placeholder: toStringOption(style?.placeholder),
        multiple: style?.multiple !== undefined ? some(style.multiple) : none,
        disabled: style?.disabled !== undefined ? some(style.disabled) : none,
        size: sizeValue ? some(sizeValue) : none,
        onChange: style?.onChange ? some(style.onChange) : none,
        onChangeMultiple: style?.onChangeMultiple ? some(style.onChangeMultiple) : none,
        onOpenChange: style?.onOpenChange ? some(style.onOpenChange) : none,
    }, SelectRootType);
}

function createSelectRoot(
    value: SubtypeExprOrValue<StringType>,
    items: SubtypeExprOrValue<ArrayType<SelectItemType>>,
    style?: SelectStyle
): ExprType<UIComponentType> {
    return East.value(variant("Select", createSelectRoot_(value, items, style)), UIComponentType);
}

// ============================================================================
// Select Compound Component
// ============================================================================

/**
 * Select compound component for dropdown selection.
 *
 * @remarks
 * Use `Select.Root` to create the select container and `Select.Item` for each
 * option in the dropdown.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Select, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Select.Root("", [
 *         Select.Item("us", "United States"),
 *         Select.Item("uk", "United Kingdom"),
 *         Select.Item("ca", "Canada"),
 *     ], {
 *         placeholder: "Select a country",
 *     });
 * });
 * ```
 */
export const Select = {
    Root: createSelectRoot,
    Item: createSelectItem,
    Types: {
        Root: SelectRootType,
        Item: SelectItemType,
    },
} as const;
