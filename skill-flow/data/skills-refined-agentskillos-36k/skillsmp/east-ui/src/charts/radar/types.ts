/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    ArrayType,
    FloatType,
    IntegerType,
    StringType,
    DictType,
    LiteralValueType,
} from "@elaraai/east";

import {
    ChartSeriesType,
    ChartGridType,
    ChartTooltipType,
    ChartLegendType,
    ChartMarginType,
    type BaseChartStyle,
} from "../types.js";

// ============================================================================
// Radar Chart Type
// ============================================================================

/**
 * Radar chart component type.
 *
 * @remarks
 * Radar charts display multivariate data on radial axes.
 * Each axis represents a different variable.
 *
 * @property data - Array of data points with values for each axis
 * @property series - Series configuration for multi-series charts
 * @property dataKey - Key for axis labels (e.g., "subject")
 * @property grid - Grid configuration
 * @property tooltip - Tooltip configuration
 * @property legend - Legend configuration
 * @property margin - Chart margin configuration
 * @property fillOpacity - Fill opacity (0-1)
 */
export const RadarChartType = StructType({
    data: ArrayType(DictType(StringType, LiteralValueType)),
    series: ArrayType(ChartSeriesType),
    dataKey: OptionType(StringType),
    grid: OptionType(ChartGridType),
    tooltip: OptionType(ChartTooltipType),
    legend: OptionType(ChartLegendType),
    margin: OptionType(ChartMarginType),
    fillOpacity: OptionType(FloatType),
});

/**
 * Type representing a radar chart.
 */
export type RadarChartType = typeof RadarChartType;

// ============================================================================
// Radar Chart Style
// ============================================================================

/**
 * TypeScript interface for Radar chart style options.
 *
 * @remarks
 * All properties are optional and accept either static values or East expressions.
 *
 * @property dataKey - Key for axis labels (e.g., "subject")
 * @property fillOpacity - Fill opacity (0-1)
 */
export interface RadarChartStyle extends BaseChartStyle {
    /** Key for axis labels (e.g., "subject") */
    dataKey?: SubtypeExprOrValue<StringType>;
    /** Fill opacity (0-1) */
    fillOpacity?: SubtypeExprOrValue<FloatType>;
}

/**
 * Series configuration for Radar charts.
 *
 * @remarks
 * Configures how a data field is rendered as a series in the radar chart.
 *
 * @property color - Chakra color token (e.g., "teal.solid", "blue.500")
 * @property label - Display label (defaults to name)
 * @property stroke - Stroke/line color (defaults to color)
 * @property strokeWidth - Stroke/line width in pixels
 * @property fill - Fill color (defaults to color)
 * @property fillOpacity - Fill opacity (0-1)
 * @property strokeDasharray - Dash pattern for dashed lines (e.g., "5 5")
 */
export interface RadarChartSeriesConfig {
    /** Chakra color token (e.g., "teal.solid", "blue.500") */
    color?: SubtypeExprOrValue<StringType>;
    /** Display label (defaults to name) */
    label?: SubtypeExprOrValue<StringType>;
    /** Stroke/line color (defaults to color) */
    stroke?: SubtypeExprOrValue<StringType>;
    /** Stroke/line width in pixels */
    strokeWidth?: SubtypeExprOrValue<IntegerType>;
    /** Fill color (defaults to color) */
    fill?: SubtypeExprOrValue<StringType>;
    /** Fill opacity (0-1) */
    fillOpacity?: SubtypeExprOrValue<FloatType>;
    /** Dash pattern for dashed lines (e.g., "5 5") */
    strokeDasharray?: SubtypeExprOrValue<StringType>;
    /** Rendering order (higher = rendered on top) */
    layerIndex?: SubtypeExprOrValue<IntegerType>;
}
