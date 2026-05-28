/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    type DictType as DictTypeType,
    OptionType,
    StructType,
    ArrayType,
    BooleanType,
    IntegerType,
    FloatType,
    StringType,
    DictType,
    LiteralValueType,
} from "@elaraai/east";

import {
    ChartSeriesType,
    ChartAxisType,
    ChartGridType,
    ChartTooltipType,
    ChartLegendType,
    ChartMarginType,
    ChartBrushType,
    BarLayoutType,
    StackOffsetType,
    MultiSeriesDataType,
    ReferenceLineType,
    ReferenceDotType,
    ReferenceAreaType,
    YAxisIdType,
    type BarLayoutLiteral,
    type StackOffsetLiteral,
    type YAxisIdLiteral,
    type BaseChartStyle,
    type ChartBrushStyleBase,
    type ChartAxisStyle,
    type ReferenceLineStyle,
    type ReferenceDotStyle,
    type ReferenceAreaStyle,
} from "../types.js";

// ============================================================================
// Bar Chart Type
// ============================================================================

/**
 * Bar chart component type.
 *
 * @remarks
 * Bar charts display categorical data with rectangular bars.
 * Supports horizontal/vertical layouts and stacking.
 *
 * Supports two data formats:
 * - Single array: `data` contains all series in one array (series keys are field names)
 * - Multi-series: `dataSeries` contains separate arrays per series (for sparse data)
 *
 * @property data - Array of data points (single array form)
 * @property dataSeries - Record of arrays per series (multi-series form, for sparse data)
 * @property valueKey - Field name for Y values when using dataSeries
 * @property series - Series configuration for multi-series charts
 * @property xAxis - X-axis configuration
 * @property yAxis - Y-axis configuration
 * @property layout - Bar direction (horizontal = vertical bars, vertical = horizontal bars)
 * @property stacked - Enable stacking of series
 * @property stackOffset - Stack offset mode
 * @property grid - Grid configuration
 * @property tooltip - Tooltip configuration
 * @property legend - Legend configuration
 * @property margin - Chart margin configuration
 * @property barSize - Bar width/height in pixels
 * @property barGap - Gap between bars in pixels
 * @property radius - Rounded corner radius
 */
export const BarChartType = StructType({
    data: ArrayType(DictType(StringType, LiteralValueType)),
    dataSeries: OptionType(MultiSeriesDataType),
    valueKey: OptionType(StringType),
    pivotKey: OptionType(StringType),
    series: ArrayType(ChartSeriesType),
    xAxis: OptionType(ChartAxisType),
    yAxis: OptionType(ChartAxisType),
    yAxis2: OptionType(ChartAxisType),
    layout: OptionType(BarLayoutType),
    stacked: OptionType(BooleanType),
    stackOffset: OptionType(StackOffsetType),
    grid: OptionType(ChartGridType),
    tooltip: OptionType(ChartTooltipType),
    legend: OptionType(ChartLegendType),
    margin: OptionType(ChartMarginType),
    brush: OptionType(ChartBrushType),
    barSize: OptionType(IntegerType),
    barGap: OptionType(IntegerType),
    radius: OptionType(IntegerType),
    referenceLines: OptionType(ArrayType(ReferenceLineType)),
    referenceDots: OptionType(ArrayType(ReferenceDotType)),
    referenceAreas: OptionType(ArrayType(ReferenceAreaType)),
});

/**
 * Type representing a bar chart.
 */
export type BarChartType = typeof BarChartType;

// ============================================================================
// Bar Chart Style
// ============================================================================

/**
 * Base style options shared by Bar and BarMulti charts.
 */
export interface BarChartStyleBase<DataKey extends string = string> extends BaseChartStyle {
    /** X-axis configuration */
    xAxis?: ChartAxisStyle<DataKey>;
    /** Y-axis configuration (primary, left side) */
    yAxis?: ChartAxisStyle<DataKey>;
    /** Secondary Y-axis configuration (right side) */
    yAxis2?: ChartAxisStyle<DataKey>;
    /** Bar direction (horizontal = vertical bars, vertical = horizontal bars) */
    layout?: SubtypeExprOrValue<BarLayoutType> | BarLayoutLiteral;
    /** Enable stacking of series */
    stacked?: SubtypeExprOrValue<BooleanType>;
    /** Stack offset mode */
    stackOffset?: SubtypeExprOrValue<StackOffsetType> | StackOffsetLiteral;
    /** Bar width/height in pixels */
    barSize?: SubtypeExprOrValue<IntegerType>;
    /** Gap between bars in pixels */
    barGap?: SubtypeExprOrValue<IntegerType>;
    /** Rounded corner radius */
    radius?: SubtypeExprOrValue<IntegerType>;
    /** Reference lines (horizontal/vertical lines at specific values) */
    referenceLines?: ReferenceLineStyle[];
    /** Reference dots (markers at specific x,y coordinates) */
    referenceDots?: ReferenceDotStyle[];
    /** Reference areas (highlighted rectangular regions) */
    referenceAreas?: ReferenceAreaStyle[];
}

/**
 * Brush configuration for Bar charts with type-safe dataKey.
 *
 * @typeParam DataKey - Union of field keys from the data struct
 */
export interface BarChartBrushStyle<DataKey extends string = string> extends ChartBrushStyleBase {
    /** Data key for brush labels (defaults to xAxis dataKey) */
    dataKey?: DataKey;
}

/**
 * Style for Bar charts (single array form).
 *
 * @typeParam DataKey - Union of field keys from the data struct
 */
export interface BarChartStyle<DataKey extends string = string> extends BarChartStyleBase<DataKey> {
    /** Field name containing series identifiers (enables pivot/long format data) */
    pivotKey?: DataKey;
    /** Field name for Y values (required when using pivotKey) */
    valueKey?: DataKey;
    /** Brush configuration for data range selection */
    brush?: BarChartBrushStyle<DataKey>;
}

/**
 * Style for BarMulti charts (multi-series with separate arrays).
 *
 * @typeParam DataKey - Union of field keys from series array structs
 * @typeParam NumericKey - Union of numeric field keys (for valueKey)
 * @typeParam SeriesKey - Union of series names (record keys)
 */
export interface BarChartMultiStyle<
    DataKey extends string = string,
    NumericKey extends string = string,
    SeriesKey extends string = string
> extends BarChartStyleBase<DataKey> {
    /** Field name containing Y values in each series array (must be numeric) */
    valueKey: NumericKey;
    /** Field name containing series identifiers (enables pivot/long format data within each record) */
    pivotKey?: DataKey;
    /** Per-series configuration (keyed by series name) */
    series?: { [K in SeriesKey]?: BarChartSeriesConfig };
    /** Brush configuration for data range selection */
    brush?: BarChartBrushStyle<DataKey>;
}

/**
 * Series configuration for Bar charts.
 *
 * @remarks
 * Configures how a data field is rendered as a series in the bar chart.
 *
 * @property color - Chakra color token (e.g., "teal.solid", "blue.500")
 * @property stackId - Stack group ID (same stackId = stacked together)
 * @property label - Display label (defaults to field name)
 * @property stroke - Stroke/line color (defaults to color)
 * @property strokeWidth - Stroke/line width in pixels
 * @property fill - Fill color (defaults to color)
 * @property fillOpacity - Fill opacity (0-1)
 * @property strokeDasharray - Dash pattern for dashed lines (e.g., "5 5")
 */
export interface BarChartSeriesConfig {
    /** Chakra color token (e.g., "teal.solid", "blue.500") */
    color?: SubtypeExprOrValue<StringType>;
    /** Stack group ID (same stackId = stacked together) */
    stackId?: SubtypeExprOrValue<StringType>;
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
    /** Y-axis binding (left = primary yAxis, right = secondary yAxis2) */
    yAxisId?: SubtypeExprOrValue<YAxisIdType> | YAxisIdLiteral;
    /** Mapping of pivot key values to colors (used with pivotKey) */
    pivotColors?: SubtypeExprOrValue<DictTypeType<StringType, StringType>>;
    /** Rendering order (higher = rendered on top) */
    layerIndex?: SubtypeExprOrValue<IntegerType>;
}
