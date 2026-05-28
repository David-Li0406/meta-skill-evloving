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
    FloatType,
    IntegerType,
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
    CurveType,
    StackOffsetType,
    MultiSeriesDataType,
    ReferenceLineType,
    ReferenceDotType,
    ReferenceAreaType,
    YAxisIdType,
    type CurveLiteral,
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
// Area Chart Type
// ============================================================================

/**
 * Area chart component type.
 *
 * @remarks
 * Area charts display quantitative data with filled areas under line curves.
 * Supports stacking for showing part-to-whole relationships.
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
 * @property curveType - Line curve interpolation type
 * @property stacked - Enable stacking of series
 * @property stackOffset - Stack offset mode (none, expand, etc.)
 * @property grid - Grid configuration
 * @property tooltip - Tooltip configuration
 * @property legend - Legend configuration
 * @property margin - Chart margin configuration
 * @property fillOpacity - Fill opacity (0-1)
 * @property connectNulls - Connect line across null data points
 */
export const AreaChartType = StructType({
    data: ArrayType(DictType(StringType, LiteralValueType)),
    dataSeries: OptionType(MultiSeriesDataType),
    valueKey: OptionType(StringType),
    pivotKey: OptionType(StringType),
    series: ArrayType(ChartSeriesType),
    xAxis: OptionType(ChartAxisType),
    yAxis: OptionType(ChartAxisType),
    yAxis2: OptionType(ChartAxisType),
    curveType: OptionType(CurveType),
    stacked: OptionType(BooleanType),
    stackOffset: OptionType(StackOffsetType),
    grid: OptionType(ChartGridType),
    tooltip: OptionType(ChartTooltipType),
    legend: OptionType(ChartLegendType),
    margin: OptionType(ChartMarginType),
    brush: OptionType(ChartBrushType),
    fillOpacity: OptionType(FloatType),
    connectNulls: OptionType(BooleanType),
    referenceLines: OptionType(ArrayType(ReferenceLineType)),
    referenceDots: OptionType(ArrayType(ReferenceDotType)),
    referenceAreas: OptionType(ArrayType(ReferenceAreaType)),
});

/**
 * Type representing an area chart.
 */
export type AreaChartType = typeof AreaChartType;

// ============================================================================
// Area Chart Style
// ============================================================================

/**
 * Base style options shared by Area and AreaMulti charts.
 */
export interface AreaChartStyleBase<DataKey extends string = string> extends BaseChartStyle {
    /** X-axis configuration */
    xAxis?: ChartAxisStyle<DataKey>;
    /** Y-axis configuration (primary, left side) */
    yAxis?: ChartAxisStyle<DataKey>;
    /** Secondary Y-axis configuration (right side) */
    yAxis2?: ChartAxisStyle<DataKey>;
    /** Line curve interpolation type */
    curveType?: SubtypeExprOrValue<CurveType> | CurveLiteral;
    /** Enable stacking of series */
    stacked?: SubtypeExprOrValue<BooleanType>;
    /** Stack offset mode (none, expand for 100%, etc.) */
    stackOffset?: SubtypeExprOrValue<StackOffsetType> | StackOffsetLiteral;
    /** Fill opacity (0-1, applies to all series unless overridden per-series) */
    fillOpacity?: SubtypeExprOrValue<FloatType>;
    /** Connect line across null data points */
    connectNulls?: SubtypeExprOrValue<BooleanType>;
    /** Reference lines (horizontal/vertical lines at specific values) */
    referenceLines?: ReferenceLineStyle[];
    /** Reference dots (markers at specific x,y coordinates) */
    referenceDots?: ReferenceDotStyle[];
    /** Reference areas (highlighted rectangular regions) */
    referenceAreas?: ReferenceAreaStyle[];
}

/**
 * Brush configuration for Area charts with type-safe dataKey.
 *
 * @typeParam DataKey - Union of field keys from the data struct
 */
export interface AreaChartBrushStyle<DataKey extends string = string> extends ChartBrushStyleBase {
    /** Data key for brush labels (defaults to xAxis dataKey) */
    dataKey?: DataKey;
}

/**
 * Style for Area charts (single array form).
 *
 * @typeParam DataKey - Union of field keys from the data struct
 */
export interface AreaChartStyle<DataKey extends string = string> extends AreaChartStyleBase<DataKey> {
    /** Field name containing series identifiers (enables pivot/long format data) */
    pivotKey?: DataKey;
    /** Field name for Y values (required when using pivotKey) */
    valueKey?: DataKey;
    /** Brush configuration for data range selection */
    brush?: AreaChartBrushStyle<DataKey>;
}

/**
 * Style for AreaMulti charts (multi-series with separate arrays).
 *
 * @typeParam DataKey - Union of field keys from series array structs
 * @typeParam NumericKey - Union of numeric field keys (for valueKey)
 * @typeParam SeriesKey - Union of series names (record keys)
 */
export interface AreaChartMultiStyle<
    DataKey extends string = string,
    NumericKey extends string = string,
    SeriesKey extends string = string
> extends AreaChartStyleBase<DataKey> {
    /** Field name containing Y values in each series array (must be numeric) */
    valueKey: NumericKey;
    /** Field name containing series identifiers (enables pivot/long format data within each record) */
    pivotKey?: DataKey;
    /** Per-series configuration (keyed by series name) */
    series?: { [K in SeriesKey]?: AreaChartSeriesConfig };
    /** Brush configuration for data range selection */
    brush?: AreaChartBrushStyle<DataKey>;
}

/**
 * Series configuration for Area charts.
 *
 * @remarks
 * Configures how a data field is rendered as a series in the area chart.
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
export interface AreaChartSeriesConfig {
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

// ============================================================================
// Area Range Chart Type
// ============================================================================

/**
 * Series configuration for range area charts.
 *
 * @property name - Series identifier
 * @property lowKey - Field name for lower bound values
 * @property highKey - Field name for upper bound values
 * @property color - Chakra color token
 * @property label - Display label
 * @property fillOpacity - Fill opacity (0-1)
 * @property stroke - Stroke color
 * @property strokeWidth - Stroke width in pixels
 */
export const AreaRangeSeriesType = StructType({
    name: StringType,
    lowKey: StringType,
    highKey: StringType,
    color: OptionType(StringType),
    label: OptionType(StringType),
    fillOpacity: OptionType(FloatType),
    stroke: OptionType(StringType),
    strokeWidth: OptionType(IntegerType),
    yAxisId: OptionType(YAxisIdType),
});

/**
 * Type representing area range series configuration.
 */
export type AreaRangeSeriesType = typeof AreaRangeSeriesType;

/**
 * Area range chart component type.
 *
 * @remarks
 * Area range charts display bands/ranges between two values (e.g., min/max, high/low).
 * Each data point has a lower and upper bound value.
 *
 * Supports two data formats:
 * - Single array: `data` contains all series in one array
 * - Multi-series: `dataSeries` contains separate arrays per series (for sparse data)
 *
 * @property data - Array of data points (single array form)
 * @property dataSeries - Record of arrays per series (multi-series form, for sparse data)
 * @property lowKey - Field name for lower bound values (for multi-series form)
 * @property highKey - Field name for upper bound values (for multi-series form)
 * @property series - Series configuration with lowKey/highKey per series
 * @property xAxis - X-axis configuration
 * @property yAxis - Y-axis configuration
 * @property curveType - Line curve interpolation type
 * @property grid - Grid configuration
 * @property tooltip - Tooltip configuration
 * @property legend - Legend configuration
 * @property margin - Chart margin configuration
 */
export const AreaRangeChartType = StructType({
    data: ArrayType(DictType(StringType, LiteralValueType)),
    dataSeries: OptionType(MultiSeriesDataType),
    lowKey: OptionType(StringType),
    highKey: OptionType(StringType),
    series: ArrayType(AreaRangeSeriesType),
    xAxis: OptionType(ChartAxisType),
    yAxis: OptionType(ChartAxisType),
    yAxis2: OptionType(ChartAxisType),
    curveType: OptionType(CurveType),
    grid: OptionType(ChartGridType),
    tooltip: OptionType(ChartTooltipType),
    legend: OptionType(ChartLegendType),
    margin: OptionType(ChartMarginType),
    fillOpacity: OptionType(FloatType),
    connectNulls: OptionType(BooleanType),
    referenceLines: OptionType(ArrayType(ReferenceLineType)),
    referenceDots: OptionType(ArrayType(ReferenceDotType)),
    referenceAreas: OptionType(ArrayType(ReferenceAreaType)),
});

/**
 * Type representing an area range chart.
 */
export type AreaRangeChartType = typeof AreaRangeChartType;

// ============================================================================
// Area Range Chart Style
// ============================================================================

/**
 * Series configuration for AreaRange charts.
 *
 * @remarks
 * Configures how a range series is rendered, specifying the low/high data keys.
 *
 * @property lowKey - Field name for lower bound values
 * @property highKey - Field name for upper bound values
 * @property color - Chakra color token (e.g., "teal.solid", "blue.500")
 * @property label - Display label (defaults to series name)
 * @property fillOpacity - Fill opacity (0-1)
 * @property stroke - Stroke color (defaults to color)
 * @property strokeWidth - Stroke width in pixels
 */
export interface AreaRangeSeriesConfig {
    /** Field name for lower bound values */
    lowKey: string;
    /** Field name for upper bound values */
    highKey: string;
    /** Chakra color token (e.g., "teal.solid", "blue.500") */
    color?: SubtypeExprOrValue<StringType>;
    /** Display label (defaults to series name) */
    label?: SubtypeExprOrValue<StringType>;
    /** Fill opacity (0-1) */
    fillOpacity?: SubtypeExprOrValue<FloatType>;
    /** Stroke color (defaults to color) */
    stroke?: SubtypeExprOrValue<StringType>;
    /** Stroke width in pixels */
    strokeWidth?: SubtypeExprOrValue<IntegerType>;
    /** Y-axis binding (left = primary yAxis, right = secondary yAxis2) */
    yAxisId?: SubtypeExprOrValue<YAxisIdType> | YAxisIdLiteral;
}

/**
 * Base style options shared by AreaRange and AreaRangeMulti charts.
 */
export interface AreaRangeChartStyleBase<DataKey extends string = string> extends BaseChartStyle {
    /** X-axis configuration */
    xAxis?: ChartAxisStyle<DataKey>;
    /** Y-axis configuration (primary, left side) */
    yAxis?: ChartAxisStyle<DataKey>;
    /** Secondary Y-axis configuration (right side) */
    yAxis2?: ChartAxisStyle<DataKey>;
    /** Line curve interpolation type */
    curveType?: SubtypeExprOrValue<CurveType> | CurveLiteral;
    /** Fill opacity (0-1, applies to all series unless overridden per-series) */
    fillOpacity?: SubtypeExprOrValue<FloatType>;
    /** Connect line across null data points */
    connectNulls?: SubtypeExprOrValue<BooleanType>;
    /** Reference lines (horizontal/vertical lines at specific values) */
    referenceLines?: ReferenceLineStyle[];
    /** Reference dots (markers at specific x,y coordinates) */
    referenceDots?: ReferenceDotStyle[];
    /** Reference areas (highlighted rectangular regions) */
    referenceAreas?: ReferenceAreaStyle[];
}

/**
 * Style for AreaRange charts (single array form).
 *
 * @typeParam DataKey - Union of field keys from the data struct
 * @typeParam SeriesKey - Union of series names
 */
export interface AreaRangeChartStyle<
    DataKey extends string = string,
    SeriesKey extends string = string
> extends AreaRangeChartStyleBase<DataKey> {
    /** Per-series configuration with lowKey/highKey */
    series?: { [K in SeriesKey]?: AreaRangeSeriesConfig };
}

/**
 * Style for AreaRangeMulti charts (multi-series with separate arrays).
 *
 * @typeParam DataKey - Union of field keys from series array structs
 * @typeParam SeriesKey - Union of series names (record keys)
 */
export interface AreaRangeChartMultiStyle<
    DataKey extends string = string,
    SeriesKey extends string = string
> extends AreaRangeChartStyleBase<DataKey> {
    /** Field name for lower bound values (shared across all series) */
    lowKey: string;
    /** Field name for upper bound values (shared across all series) */
    highKey: string;
    /** Per-series configuration (keyed by series name) */
    series?: { [K in SeriesKey]?: Omit<AreaRangeSeriesConfig, 'lowKey' | 'highKey'> };
}
