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
    type ChartSort,
} from "../types.js";

// ============================================================================
// Bar Segment Item Type
// ============================================================================

/**
 * Bar segment item data type.
 *
 * @remarks
 * Each item represents a segment in the bar with a name, value, and color.
 *
 * @property name - Segment label
 * @property value - Numeric value (determines segment width)
 * @property color - Segment color (required for segments)
 */
export const BarSegmentItemType = StructType({
    name: StringType,
    value: FloatType,
    color: OptionType(StringType),
});

/**
 * Type representing a bar segment item.
 */
export type BarSegmentItemType = typeof BarSegmentItemType;

// ============================================================================
// Bar Segment Type
// ============================================================================

/**
 * Bar segment component type.
 *
 * @remarks
 * Bar segment displays proportional segments in a single horizontal bar.
 * Like a horizontal stacked bar showing part-to-whole relationships.
 *
 * @property data - Array of segment items
 * @property sort - Sort configuration
 * @property showValue - Show value text on segments
 * @property showLabel - Show label text on segments
 */
export const BarSegmentType = StructType({
    data: ArrayType(BarSegmentItemType),
    sort: OptionType(ChartSortType),
    showValue: OptionType(BooleanType),
    showLabel: OptionType(BooleanType),
});

/**
 * Type representing a bar segment.
 */
export type BarSegmentType = typeof BarSegmentType;

// ============================================================================
// Bar Segment Style
// ============================================================================

/**
 * TypeScript interface for Bar segment style options.
 *
 * @remarks
 * All properties are optional for configuring the bar segment appearance.
 *
 * @property sort - Sort configuration for ordering segments
 * @property showValue - Show value text on segments
 * @property showLabel - Show label text on segments
 */
export interface BarSegmentStyle {
    /** Sort configuration */
    sort?: ChartSort;
    /** Show value text on segments */
    showValue?: SubtypeExprOrValue<BooleanType>;
    /** Show label text on segments */
    showLabel?: SubtypeExprOrValue<BooleanType>;
}
