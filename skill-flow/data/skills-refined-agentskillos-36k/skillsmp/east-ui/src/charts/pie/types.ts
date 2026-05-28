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
    ChartTooltipType,
    ChartLegendType,
    ChartMarginType,
    type ChartTooltipStyle,
    type ChartLegendStyle,
    type ChartMarginStyle,
} from "../types.js";

// ============================================================================
// Pie Slice Type
// ============================================================================

/**
 * Pie slice data type.
 *
 * @remarks
 * Each slice represents a segment of the pie with a name, value, and color.
 *
 * @property name - Slice label
 * @property value - Numeric value for the slice
 * @property color - Chakra color token (e.g., "blue.solid")
 */
export const PieSliceType = StructType({
    name: StringType,
    value: FloatType,
    color: OptionType(StringType),
});

/**
 * Type representing a pie slice.
 */
export type PieSliceType = typeof PieSliceType;

// ============================================================================
// Pie Chart Type
// ============================================================================

/**
 * Pie chart component type.
 *
 * @remarks
 * Pie charts display proportional segments of a circle.
 * Set innerRadius > 0 to create a donut chart.
 *
 * @property data - Array of pie slices
 * @property innerRadius - Inner radius (0 = pie, >0 = donut)
 * @property outerRadius - Outer radius
 * @property startAngle - Start angle in degrees
 * @property endAngle - End angle in degrees
 * @property paddingAngle - Padding between slices in degrees
 * @property showLabels - Show slice labels
 * @property tooltip - Tooltip configuration
 * @property legend - Legend configuration
 * @property margin - Chart margin configuration
 */
export const PieChartType = StructType({
    data: ArrayType(PieSliceType),
    innerRadius: OptionType(FloatType),
    outerRadius: OptionType(FloatType),
    startAngle: OptionType(FloatType),
    endAngle: OptionType(FloatType),
    paddingAngle: OptionType(FloatType),
    showLabels: OptionType(BooleanType),
    tooltip: OptionType(ChartTooltipType),
    legend: OptionType(ChartLegendType),
    margin: OptionType(ChartMarginType),
});

/**
 * Type representing a pie chart.
 */
export type PieChartType = typeof PieChartType;

// ============================================================================
// Pie Chart Style
// ============================================================================

/**
 * TypeScript interface for Pie chart style options.
 *
 * @remarks
 * All properties are optional and accept either static values or East expressions.
 *
 * @property innerRadius - Inner radius (0 = pie, >0 = donut)
 * @property outerRadius - Outer radius
 * @property startAngle - Start angle in degrees
 * @property endAngle - End angle in degrees
 * @property paddingAngle - Padding between slices in degrees
 * @property showLabels - Show slice labels
 * @property tooltip - Tooltip configuration
 * @property legend - Legend configuration
 * @property margin - Chart margin configuration
 */
export interface PieChartStyle {
    /** Inner radius (0 = pie, >0 = donut) */
    innerRadius?: SubtypeExprOrValue<FloatType>;
    /** Outer radius */
    outerRadius?: SubtypeExprOrValue<FloatType>;
    /** Start angle in degrees */
    startAngle?: SubtypeExprOrValue<FloatType>;
    /** End angle in degrees */
    endAngle?: SubtypeExprOrValue<FloatType>;
    /** Padding between slices in degrees */
    paddingAngle?: SubtypeExprOrValue<FloatType>;
    /** Show slice labels */
    showLabels?: SubtypeExprOrValue<BooleanType>;
    /** Tooltip configuration */
    tooltip?: ChartTooltipStyle;
    /** Legend configuration */
    legend?: ChartLegendStyle;
    /** Chart margin configuration */
    margin?: ChartMarginStyle;
}
