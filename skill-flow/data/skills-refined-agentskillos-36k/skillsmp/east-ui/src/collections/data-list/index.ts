/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    East,
    OptionType,
    StructType,
    StringType,
    ArrayType,
    variant,
    type SubtypeExprOrValue,
} from "@elaraai/east";

import { OrientationType } from "../../style.js";
import { DataListVariantType, DataListSizeType, type DataListStyle } from "./types.js";
import { UIComponentType } from "../../component.js";

// Re-export style types
export {
    DataListVariantType,
    DataListVariant,
    DataListSizeType,
    type DataListSizeLiteral,
    type DataListStyle,
} from "./types.js";

// ============================================================================
// DataList Item Type
// ============================================================================

/**
 * Type for DataList item data.
 *
 * @remarks
 * Each item in a DataList has a label and value pair.
 *
 * @property label - The term/label for this item
 * @property value - The definition/value for this item
 */
export const DataListItemType = StructType({
    label: StringType,
    value: StringType,
});

/**
 * Type representing the DataListItem structure.
 */
export type DataListItemType = typeof DataListItemType;

// ============================================================================
// DataList Root Type
// ============================================================================

/**
 * Type for DataList component data.
 *
 * @remarks
 * DataList displays a list of label-value pairs, similar to an HTML
 * description list (dl/dt/dd).
 *
 * @property items - Array of label-value items
 * @property orientation - Layout direction (horizontal or vertical)
 * @property size - Size of the data list
 * @property variant - Visual variant (subtle or bold)
 */
export const DataListRootType = StructType({
    items: ArrayType(DataListItemType),
    orientation: OptionType(OrientationType),
    size: OptionType(DataListSizeType),
    variant: OptionType(DataListVariantType),
});

/**
 * Type representing the DataList structure.
 */
export type DataListRootType = typeof DataListRootType;

// ============================================================================
// DataList Item Function
// ============================================================================

/**
 * Creates a DataList item with label and value.
 *
 * @param label - The term/label for this item
 * @param value - The definition/value for this item
 * @returns An East expression representing the data list item
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { DataList, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return DataList.Root([
 *         DataList.Item("Status", "Active"),
 *     ]);
 * });
 * ```
 */
function DataListItem(
    label: ExprType<StringType> | string,
    value: ExprType<StringType> | string
): ExprType<DataListItemType> {
    const labelExpr = typeof label === "string"
        ? East.value(label, StringType)
        : label;

    const valueExpr = typeof value === "string"
        ? East.value(value, StringType)
        : value;

    return East.value({
        label: labelExpr,
        value: valueExpr,
    }, DataListItemType);
}

// ============================================================================
// DataList Root Function
// ============================================================================

/**
 * Creates a DataList component with items and optional styling.
 *
 * @param items - Array of DataList items
 * @param style - Optional styling configuration
 * @returns An East expression representing the data list component
 *
 * @remarks
 * DataList is used to display structured label-value pairs, commonly used
 * for displaying metadata, details, or key-value information.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { DataList, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return DataList.Root([
 *         DataList.Item("Status", "Active"),
 *         DataList.Item("Created", "Jan 1, 2024"),
 *         DataList.Item("Updated", "Dec 15, 2024"),
 *     ], {
 *         orientation: "horizontal",
 *         variant: "bold",
 *     });
 * });
 * ```
 */
function DataListRoot(
    items: SubtypeExprOrValue<ArrayType<DataListItemType>>,
    style?: DataListStyle
): ExprType<UIComponentType>  {
    const orientationValue = style?.orientation
        ? (typeof style.orientation === "string"
            ? East.value(variant(style.orientation, null), OrientationType)
            : style.orientation)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), DataListSizeType)
            : style.size)
        : undefined;

    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), DataListVariantType)
            : style.variant)
        : undefined;

    return East.value(variant("DataList", {
        items: East.value(items, ArrayType(DataListItemType)),
        orientation: orientationValue ? variant("some", orientationValue) : variant("none", null),
        size: sizeValue ? variant("some", sizeValue) : variant("none", null),
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
    }), UIComponentType);
}

// ============================================================================
// DataList Compound Component
// ============================================================================

/**
 * DataList compound component for displaying label-value pairs.
 *
 * @remarks
 * Use `DataList.Root` to create the container and `DataList.Item` for each
 * label-value pair.
 */
export const DataList = {
    /**
     * Creates a DataList component with items and optional styling.
     *
     * @param items - Array of DataList items
     * @param style - Optional styling configuration
     * @returns An East expression representing the data list component
     *
     * @remarks
     * DataList is used to display structured label-value pairs, commonly used
     * for displaying metadata, details, or key-value information.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { DataList, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return DataList.Root([
     *         DataList.Item("Name", "John Doe"),
     *         DataList.Item("Email", "john@example.com"),
     *         DataList.Item("Role", "Administrator"),
     *     ], {
     *         orientation: "horizontal",
     *     });
     * });
     * ```
     */
    Root: DataListRoot,
    /**
     * Creates a DataList item with label and value.
     *
     * @param label - The term/label for this item
     * @param value - The definition/value for this item
     * @returns An East expression representing the data list item
     *
     * @remarks
     * Each DataList item represents a single label-value pair.
     * Items are typically created as an array passed to DataList.Root.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { DataList, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return DataList.Root([
     *         DataList.Item("Status", "Active"),
     *         DataList.Item("Count", "42"),
     *     ]);
     * });
     * ```
     */
    Item: DataListItem,
    Types: {
        /**
         * Type for DataList component data.
         *
         * @remarks
         * DataList displays a list of label-value pairs, similar to an HTML
         * description list (dl/dt/dd).
         *
         * @property items - Array of label-value items
         * @property orientation - Layout direction (horizontal or vertical)
         * @property size - Size of the data list
         * @property variant - Visual variant (subtle or bold)
         */
        Root: DataListRootType,
        /**
         * Type for DataList item data.
         *
         * @remarks
         * Each item in a DataList has a label and value pair.
         *
         * @property label - The term/label for this item
         * @property value - The definition/value for this item
         */
        Item: DataListItemType,
        /**
         * Variant types for DataList visual style.
         *
         * @remarks
         * - subtle: Light/subtle styling
         * - bold: Bold/emphasized styling
         */
        Variant: DataListVariantType,
        /**
         * Size options for DataList component.
         *
         * @remarks
         * Chakra UI DataList only supports sm, md, lg sizes (not xs).
         *
         * @property sm - Small data list
         * @property md - Medium data list (default)
         * @property lg - Large data list
         */
        Size: DataListSizeType,
    },
} as const;
