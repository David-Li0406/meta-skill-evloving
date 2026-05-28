/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    ArrayType,
    StringType,
    FloatType,
    BooleanType,
} from "@elaraai/east";

import {
    ChartSortType,
    TickFormatType,
    type ChartSort,
    type SimpleTickFormatLiteral,
} from "../types.js";

// ============================================================================
// Bar List Item Type
// ============================================================================

/**
 * Bar list item data type.
 *
 * @remarks
 * Each item represents a horizontal bar with a name, value, and optional color.
 *
 * @property name - Item label
 * @property value - Numeric value (determines bar length)
 * @property color - Optional bar color
 */
export const BarListItemType = StructType({
    name: StringType,
    value: FloatType,
    color: OptionType(StringType),
});

/**
 * Type representing a bar list item.
 */
export type BarListItemType = typeof BarListItemType;

// ============================================================================
// Bar List Type
// ============================================================================

/**
 * Bar list component type.
 *
 * @remarks
 * Bar list is a Chakra-native chart for comparing categories
 * with horizontal bars. Simpler than a full bar chart.
 *
 * @property data - Array of bar list items
 * @property sort - Sort configuration
 * @property showValue - Show value text
 * @property showLabel - Show label text
 * @property valueFormat - Format for values (uses TickFormatType)
 * @property color - Default bar color
 */
export const BarListType = StructType({
    data: ArrayType(BarListItemType),
    sort: OptionType(ChartSortType),
    showValue: OptionType(BooleanType),
    showLabel: OptionType(BooleanType),
    valueFormat: OptionType(TickFormatType),
    color: OptionType(StringType),
});

/**
 * Type representing a bar list.
 */
export type BarListType = typeof BarListType;

// ============================================================================
// Bar List Style
// ============================================================================

/**
 * TypeScript interface for Bar list style options.
 *
 * @remarks
 * All properties are optional for configuring the bar list appearance.
 *
 * @property sort - Sort configuration for ordering bars
 * @property showValue - Show value text next to bars
 * @property showLabel - Show label text for bars
 * @property valueFormat - Format for values (use string literals or TickFormat helpers)
 * @property color - Default bar color (Chakra color token)
 */
export interface BarListStyle {
    /** Sort configuration */
    sort?: ChartSort;
    /** Show value text */
    showValue?: SubtypeExprOrValue<BooleanType>;
    /** Show label text */
    showLabel?: SubtypeExprOrValue<BooleanType>;
    /** Format for values - use string literals or TickFormat helpers */
    valueFormat?: SubtypeExprOrValue<TickFormatType> | SimpleTickFormatLiteral;
    /** Default bar color */
    color?: SubtypeExprOrValue<StringType>;
}
