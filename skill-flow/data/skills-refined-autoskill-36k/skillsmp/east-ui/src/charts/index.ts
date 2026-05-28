/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

/**
 * Charts components for data visualization.
 *
 * @remarks
 * Chart components describe data visualizations that can be rendered
 * using various charting libraries (e.g., Recharts for Cartesian charts,
 * Chakra-native for BarList and BarSegment).
 *
 * All charts are accessed via the `Chart` namespace:
 * - `Chart.Area` - filled area charts (single array, all series share data points)
 * - `Chart.AreaMulti` - filled area charts (multi-series with separate arrays, sparse data)
 * - `Chart.Bar` - bar charts (single array, all series share data points)
 * - `Chart.BarMulti` - bar charts (multi-series with separate arrays, sparse data)
 * - `Chart.Line` - line charts (single array, all series share data points)
 * - `Chart.LineMulti` - line charts (multi-series with separate arrays, sparse data)
 * - `Chart.Scatter` - scatter plots (single array, all series share data points)
 * - `Chart.ScatterMulti` - scatter plots (multi-series with separate arrays, sparse data)
 * - `Chart.Pie` - pie/donut charts
 * - `Chart.Radar` - radar/spider charts
 * - `Chart.BarList` - horizontal bar comparison (Chakra-native)
 * - `Chart.BarSegment` - proportional segments (Chakra-native)
 * - `Chart.Sparkline` - compact inline trend visualization
 *
 * @packageDocumentation
 */

// Shared types
export {
    ChartSeriesType,
    ChartSortType,
    ChartSortDirectionType,
    ChartAxisType,
    TickFormatType,
    CurveType,
    StackOffsetType,
    BarLayoutType,
    MultiSeriesDataType,
    ReferenceLineType,
    ReferenceDotType,
    ReferenceAreaType,
    ReferenceOverflowType,
    type ChartSeries,
    type ChartSort,
    type ChartAxis,
    type ChartSortDirectionLiteral,
    type CurveLiteral,
    type StackOffsetLiteral,
    type BarLayoutLiteral,
    type BaseChartStyle,
    type ReferenceLineStyle,
    type ReferenceDotStyle,
    type ReferenceAreaStyle,
    type ReferenceOverflowLiteral,
} from "./types.js";

// Area chart
import { createAreaChart, createAreaChartMulti, createAreaRangeChart, createAreaRangeChartMulti } from "./area/index.js";
export { AreaChartType, AreaRangeChartType, AreaRangeSeriesType, type AreaChartStyle, type AreaChartMultiStyle, type AreaChartSeriesConfig, type AreaRangeChartStyle, type AreaRangeChartMultiStyle, type AreaRangeSeriesConfig } from "./area/index.js";

// Bar chart
import { createBarChart, createBarChartMulti } from "./bar/index.js";
export { BarChartType, type BarChartStyle, type BarChartMultiStyle, type BarChartSeriesConfig } from "./bar/index.js";

// Line chart
import { createLineChart, createLineChartMulti } from "./line/index.js";
export { LineChartType, LineChartSeriesType, type LineChartStyle, type LineChartMultiStyle, type LineChartSeriesConfig } from "./line/index.js";

// Scatter chart
import { createScatterChart, createScatterChartMulti } from "./scatter/index.js";
export { ScatterChartType, type ScatterChartStyle, type ScatterChartMultiStyle, type ScatterChartSeriesConfig } from "./scatter/index.js";

// Pie chart
import { createPieChart } from "./pie/index.js";
export { PieChartType, PieSliceType, type PieChartStyle } from "./pie/index.js";

// Radar chart
import { createRadarChart } from "./radar/index.js";
export { RadarChartType, type RadarChartStyle } from "./radar/index.js";

// Bar list
import { createBarList } from "./bar-list/index.js";
export {
    BarListType,
    BarListItemType,
    type BarListStyle,
} from "./bar-list/index.js";

// Bar segment
import { createBarSegment } from "./bar-segment/index.js";
export {
    BarSegmentType,
    BarSegmentItemType,
    type BarSegmentStyle,
} from "./bar-segment/index.js";

// Sparkline (already implemented)
import { Sparkline } from "./sparkline/index.js";
export {
    SparklineType,
    SparklineChartType,
    type SparklineChartLiteral,
    type SparklineStyle,
} from "./sparkline/index.js";

// Composed chart
import { createComposedChart, createComposedChartMulti } from "./composed/index.js";
export {
    ComposedChartType,
    ComposedSeriesType,
    type ComposedChartStyle,
    type ComposedChartMultiStyle,
    type ComposedSeriesConfig,
    type ComposedChartStyleBase,
    type ComposedChartBrushStyle,
    type ComposedLineSeries,
    type ComposedAreaSeries,
    type ComposedAreaRangeSeries,
    type ComposedBarSeries,
    type ComposedScatterSeries,
    type ComposedSeriesBase,
} from "./composed/index.js";

// Import types for the namespace
import { ChartSeriesType, ChartSortType, ChartSortDirectionType, ChartAxisType, TickFormatType, CurveType, StackOffsetType, BarLayoutType, MultiSeriesDataType, ReferenceLineType, ReferenceDotType, ReferenceAreaType, ReferenceOverflowType, ChartSeries, ChartSort, StackOffset, BarLayout, NumberTickFormat, CurrencyTickFormat, PercentTickFormat, CompactTickFormat, UnitTickFormat, ScientificTickFormat, EngineeringTickFormat, DateTickFormat, TimeTickFormat, DateTimeTickFormat } from "./types.js";
import { AreaChartType, AreaRangeChartType, AreaRangeSeriesType } from "./area/index.js";
import { BarChartType } from "./bar/index.js";
import { LineChartType } from "./line/index.js";
import { ScatterChartType } from "./scatter/index.js";
import { PieChartType, PieSliceType } from "./pie/index.js";
import { RadarChartType } from "./radar/index.js";
import { BarListType, BarListItemType } from "./bar-list/index.js";
import { BarSegmentType, BarSegmentItemType } from "./bar-segment/index.js";
import { ComposedChartType, ComposedSeriesType } from "./composed/index.js";

// ============================================================================
// Chart Namespace
// ============================================================================

/**
 * Chart namespace providing access to all chart creation functions and types.
 *
 * @remarks
 * All chart components are accessed through this namespace:
 * - Factory functions create chart components (Area, Bar, Line, etc.)
 * - Types object contains all East types for serialization
 *
 * @example
 * ```ts
 * import { Chart } from "@elaraai/east-ui";
 *
 * // Create a line chart
 * const lineChart = Chart.Line(
 *   [{ month: "Jan", revenue: 186 }],
 *   [{ name: "revenue", color: "teal.solid" }],
 *   { xAxis: { dataKey: "month" }, showGrid: true }
 * );
 *
 * // Access types
 * const chartType = Chart.Types.LineChart;
 * ```
 */
export const Chart = {
    /**
     * Creates an Area chart component from a single data array.
     *
     * @param data - Array of data points (each point has x-axis value + y-axis values)
     * @param series - Series specification: array of numeric field names, or object with config
     * @param style - Optional styling with type-safe xAxis.dataKey
     * @returns An East expression representing the area chart component
     *
     * @remarks
     * All series share the same data points. Series keys are numeric field names.
     * Use this when all series have values at the same x-axis points.
     * For sparse data where series don't share all points, use `Chart.AreaMulti`.
     *
     * @example Array form (just field names)
     * ```ts
     * Chart.Area(
     *     [
     *         { month: "Jan", revenue: 100n, profit: 50n },
     *         { month: "Feb", revenue: 200n, profit: 80n },
     *     ],
     *     ["revenue", "profit"],
     *     { xAxis: { dataKey: "month" } }
     * );
     * ```
     *
     * @example Object form (with per-series config)
     * ```ts
     * Chart.Area(
     *     data,
     *     { revenue: { color: "teal.solid" }, profit: { color: "purple.solid" } },
     *     { xAxis: { dataKey: "month" }, stacked: true }
     * );
     * ```
     */
    Area: createAreaChart,
    /**
     * Creates an Area chart component from multiple data arrays (one per series).
     *
     * @param data - Record mapping series names to their data arrays
     * @param style - Styling with type-safe xAxis.dataKey and valueKey
     * @returns An East expression representing the area chart component
     *
     * @remarks
     * Each series has its own data array, allowing sparse data where series
     * don't need to have values at every x-axis point.
     *
     * @example
     * ```ts
     * Chart.AreaMulti(
     *     {
     *         revenue: [
     *             { month: "Jan", value: 100n },
     *             { month: "Feb", value: 200n },
     *         ],
     *         profit: [
     *             { month: "Jan", value: 50n },
     *             { month: "Mar", value: 150n },
     *         ],
     *     },
     *     {
     *         xAxis: { dataKey: "month" },
     *         valueKey: "value",
     *         series: { revenue: { color: "teal.solid" } },
     *     }
     * );
     * ```
     */
    AreaMulti: createAreaChartMulti,
    /**
     * Creates an Area Range chart for displaying bands between low/high values.
     *
     * @param data - Array of data points (each point has x-axis value + low/high values per series)
     * @param series - Series specification with lowKey/highKey for each series
     * @param style - Optional styling with type-safe xAxis.dataKey
     * @returns An East expression representing the area range chart component
     *
     * @remarks
     * Area range charts display filled bands between two values (e.g., min/max, high/low).
     * Each series requires a lowKey and highKey to define the range bounds.
     * Use this when all series share the same data points.
     * For sparse data, use `Chart.AreaRangeMulti`.
     *
     * @example Single range series
     * ```ts
     * Chart.AreaRange(
     *     [
     *         { day: "05-01", low: -1, high: 10 },
     *         { day: "05-02", low: 2, high: 15 },
     *     ],
     *     { temperature: { lowKey: "low", highKey: "high", color: "teal.solid" } },
     *     { xAxis: { dataKey: "day" } }
     * );
     * ```
     *
     * @example Multiple range series
     * ```ts
     * Chart.AreaRange(
     *     [
     *         { day: "05-01", tempLow: -1, tempHigh: 10, humidLow: 30, humidHigh: 50 },
     *         { day: "05-02", tempLow: 2, tempHigh: 15, humidLow: 35, humidHigh: 55 },
     *     ],
     *     {
     *         temperature: { lowKey: "tempLow", highKey: "tempHigh", color: "teal.solid" },
     *         humidity: { lowKey: "humidLow", highKey: "humidHigh", color: "blue.solid" },
     *     },
     *     { xAxis: { dataKey: "day" }, legend: { show: true } }
     * );
     * ```
     */
    AreaRange: createAreaRangeChart,
    /**
     * Creates an Area Range chart from multiple data arrays (one per series).
     *
     * @param data - Record mapping series names to their data arrays
     * @param style - Styling with type-safe xAxis.dataKey and lowKey/highKey
     * @returns An East expression representing the area range chart component
     *
     * @remarks
     * Each series has its own data array with low/high values, allowing sparse data
     * where series don't need to have values at every x-axis point.
     *
     * @example
     * ```ts
     * Chart.AreaRangeMulti(
     *     {
     *         temperature: [
     *             { day: "05-01", low: -1, high: 10 },
     *             { day: "05-02", low: 2, high: 15 },
     *         ],
     *         humidity: [
     *             { day: "05-01", low: 30, high: 50 },
     *             // 05-02 missing - sparse data!
     *             { day: "05-03", low: 40, high: 60 },
     *         ],
     *     },
     *     {
     *         xAxis: { dataKey: "day" },
     *         lowKey: "low",
     *         highKey: "high",
     *         series: { temperature: { color: "teal.solid" } },
     *     }
     * );
     * ```
     */
    AreaRangeMulti: createAreaRangeChartMulti,
    /**
     * Creates a Bar chart component from a single data array.
     *
     * @param data - Array of data points (each point has x-axis value + y-axis values)
     * @param series - Series specification: array of numeric field names, or object with config
     * @param style - Optional styling with type-safe xAxis.dataKey
     * @returns An East expression representing the bar chart component
     *
     * @remarks
     * All series share the same data points. Series keys are numeric field names.
     * Use this when all series have values at the same x-axis points.
     * For sparse data where series don't share all points, use `Chart.BarMulti`.
     *
     * @example Array form (just field names)
     * ```ts
     * Chart.Bar(
     *     [
     *         { month: "Jan", revenue: 100n, profit: 50n },
     *         { month: "Feb", revenue: 200n, profit: 80n },
     *     ],
     *     ["revenue", "profit"],
     *     { xAxis: { dataKey: "month" } }
     * );
     * ```
     *
     * @example Object form (with per-series config)
     * ```ts
     * Chart.Bar(
     *     data,
     *     { revenue: { color: "teal.solid" }, profit: { color: "purple.solid" } },
     *     { xAxis: { dataKey: "month" }, stacked: true }
     * );
     * ```
     */
    Bar: createBarChart,
    /**
     * Creates a Bar chart component from multiple data arrays (one per series).
     *
     * @param data - Record mapping series names to their data arrays
     * @param style - Styling with type-safe xAxis.dataKey and valueKey
     * @returns An East expression representing the bar chart component
     *
     * @remarks
     * Each series has its own data array, allowing sparse data where series
     * don't need to have values at every x-axis point.
     *
     * @example
     * ```ts
     * Chart.BarMulti(
     *     {
     *         revenue: [
     *             { month: "Jan", value: 100n },
     *             { month: "Feb", value: 200n },
     *         ],
     *         profit: [
     *             { month: "Jan", value: 50n },
     *             { month: "Mar", value: 150n },
     *         ],
     *     },
     *     {
     *         xAxis: { dataKey: "month" },
     *         valueKey: "value",
     *         series: { revenue: { color: "teal.solid" } },
     *     }
     * );
     * ```
     */
    BarMulti: createBarChartMulti,
    /**
     * Creates a Line chart component from a single data array.
     *
     * @param data - Array of data points (each point has x-axis value + y-axis values)
     * @param series - Series specification: array of numeric field names, or object with config
     * @param style - Optional styling with type-safe xAxis.dataKey
     * @returns An East expression representing the line chart component
     *
     * @remarks
     * All series share the same data points. Series keys are numeric field names.
     * Use this when all series have values at the same x-axis points.
     * For sparse data where series don't share all points, use `Chart.LineMulti`.
     *
     * @example Array form (just field names)
     * ```ts
     * Chart.Line(
     *     [
     *         { month: "Jan", revenue: 100n, profit: 50n },
     *         { month: "Feb", revenue: 200n, profit: 80n },
     *     ],
     *     ["revenue", "profit"],
     *     { xAxis: { dataKey: "month" } }
     * );
     * ```
     *
     * @example Object form (with per-series config)
     * ```ts
     * Chart.Line(
     *     data,
     *     { revenue: { color: "teal.solid" }, profit: { color: "purple.solid" } },
     *     { xAxis: { dataKey: "month" }, showDots: true }
     * );
     * ```
     */
    Line: createLineChart,
    /**
     * Creates a Line chart component from multiple data arrays (one per series).
     *
     * @param data - Record mapping series names to their data arrays
     * @param style - Styling with type-safe xAxis.dataKey and valueKey
     * @returns An East expression representing the line chart component
     *
     * @remarks
     * Each series has its own data array, allowing sparse data where series
     * don't need to have values at every x-axis point.
     *
     * @example
     * ```ts
     * Chart.LineMulti(
     *     {
     *         revenue: [
     *             { month: "Jan", value: 100n },
     *             { month: "Feb", value: 200n },
     *         ],
     *         profit: [
     *             { month: "Jan", value: 50n },
     *             // Feb is missing - sparse data!
     *             { month: "Mar", value: 150n },
     *         ],
     *     },
     *     {
     *         xAxis: { dataKey: "month" },
     *         valueKey: "value",
     *         series: { revenue: { color: "teal.solid" } },
     *     }
     * );
     * ```
     */
    LineMulti: createLineChartMulti,
    /**
     * Creates a Scatter chart component from a single data array.
     *
     * @param data - Array of data points (each point has x + y values)
     * @param series - Series specification: array of numeric field names, or object with config
     * @param style - Optional styling with type-safe xDataKey and yDataKey
     * @returns An East expression representing the scatter chart component
     *
     * @remarks
     * All series share the same data points. Series keys are numeric field names.
     * For sparse data where series don't share all points, use `Chart.ScatterMulti`.
     *
     * @example Array form (just field names)
     * ```ts
     * Chart.Scatter(
     *     [
     *         { x: 10n, y: 30n },
     *         { x: 20n, y: 40n },
     *     ],
     *     ["y"],
     *     { xDataKey: "x", yDataKey: "y" }
     * );
     * ```
     *
     * @example Object form (with per-series config)
     * ```ts
     * Chart.Scatter(
     *     data,
     *     { y: { color: "purple.solid" } },
     *     { xDataKey: "x" }
     * );
     * ```
     */
    Scatter: createScatterChart,
    /**
     * Creates a Scatter chart component from multiple data arrays (one per series).
     *
     * @param data - Record mapping series names to their data arrays
     * @param style - Styling with type-safe xDataKey and valueKey
     * @returns An East expression representing the scatter chart component
     *
     * @remarks
     * Each series has its own data array, allowing sparse data where series
     * don't need to have values at every x-axis point.
     *
     * @example
     * ```ts
     * Chart.ScatterMulti(
     *     {
     *         series1: [
     *             { x: 10n, value: 30n },
     *             { x: 20n, value: 40n },
     *         ],
     *         series2: [
     *             { x: 15n, value: 35n },
     *             { x: 25n, value: 45n },
     *         ],
     *     },
     *     {
     *         xDataKey: "x",
     *         valueKey: "value",
     *         series: { series1: { color: "purple.solid" } },
     *     }
     * );
     * ```
     */
    ScatterMulti: createScatterChartMulti,
    /**
     * Creates a Pie or Donut chart component.
     *
     * @param data - Array of slice data
     * @param style - Optional styling configuration
     * @returns An East expression representing the pie chart component
     *
     * @remarks
     * Pie charts display proportional data as slices of a circle.
     * Set innerRadius for a donut chart appearance.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Chart, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Chart.Pie(
     *         [
     *             { name: "Chrome", value: 275n, color: "blue.solid" },
     *             { name: "Safari", value: 200n, color: "green.solid" },
     *         ],
     *         { showLabels: true }
     *     );
     * });
     * ```
     */
    Pie: createPieChart,
    /**
     * Creates a Radar chart component.
     *
     * @param data - Array of data points
     * @param series - Series configuration keyed by field names
     * @param style - Optional styling configuration
     * @returns An East expression representing the radar chart component
     *
     * @remarks
     * Radar charts display multivariate data on radial axes.
     * Useful for comparing multiple attributes across entities.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Chart, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Chart.Radar(
     *         [
     *             { subject: "Math", A: 120n, B: 110n },
     *             { subject: "English", A: 98n, B: 130n },
     *         ],
     *         {
     *             A: { color: "teal.solid" },
     *             B: { color: "purple.solid" },
     *         },
     *         { dataKey: "subject" }
     *     );
     * });
     * ```
     */
    Radar: createRadarChart,
    /**
     * Creates a BarList component (Chakra-native horizontal bars).
     *
     * @param data - Array of bar items with name, value, and optional color/href
     * @param style - Optional styling configuration
     * @returns An East expression representing the bar list component
     *
     * @remarks
     * BarList displays horizontal comparison bars with labels and values.
     * Native Chakra component, not Recharts-based.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Chart, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Chart.BarList(
     *         [
     *             { name: "Chrome", value: 275n },
     *             { name: "Safari", value: 200n },
     *         ],
     *         { colorPalette: "blue", showValue: true }
     *     );
     * });
     * ```
     */
    BarList: createBarList,
    /**
     * Creates a BarSegment component (proportional horizontal segments).
     *
     * @param data - Array of segment items with name, value, and optional color
     * @param style - Optional styling configuration
     * @returns An East expression representing the bar segment component
     *
     * @remarks
     * BarSegment displays proportional segments in a single horizontal bar.
     * Native Chakra component for showing percentage breakdowns.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Chart, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Chart.BarSegment(
     *         [
     *             { name: "Completed", value: 75n, color: "green.solid" },
     *             { name: "Remaining", value: 25n, color: "gray.solid" },
     *         ],
     *         { showLegend: true }
     *     );
     * });
     * ```
     */
    BarSegment: createBarSegment,
    /**
     * Creates a Composed chart component combining multiple chart types.
     *
     * @param data - Array of data points (each point has x-axis value + values for each series)
     * @param style - Style with per-series configuration, each specifying its chart type
     * @returns An East expression representing the composed chart component
     *
     * @remarks
     * Composed charts combine Line, Area, Bar, Scatter, and AreaRange in a single visualization.
     * Each series in the style.series object specifies its type (line, area, bar, scatter, area-range).
     *
     * @example Mixed bar and line chart
     * ```ts
     * Chart.Composed(
     *     [
     *         { month: "Jan", revenue: 186, profit: 80, trend: 150 },
     *         { month: "Feb", revenue: 305, profit: 120, trend: 200 },
     *     ],
     *     {
     *         xAxis: { dataKey: "month" },
     *         series: {
     *             revenue: { type: "bar", color: "teal.solid" },
     *             profit: { type: "line", color: "purple.solid", showDots: true },
     *             trend: { type: "area", color: "blue.solid", fillOpacity: 0.3 },
     *         },
     *     }
     * );
     * ```
     *
     * @example With confidence bands (area-range)
     * ```ts
     * Chart.Composed(
     *     [
     *         { day: "Mon", value: 100, low: 80, high: 120 },
     *         { day: "Tue", value: 150, low: 130, high: 170 },
     *     ],
     *     {
     *         xAxis: { dataKey: "day" },
     *         series: {
     *             value: { type: "line", color: "blue.solid" },
     *             confidence: { type: "area-range", lowKey: "low", highKey: "high", color: "blue.200", fillOpacity: 0.3 },
     *         },
     *     }
     * );
     * ```
     */
    Composed: createComposedChart,
    /**
     * Creates a Composed chart from multiple sparse data arrays (one per series).
     *
     * @param data - Record mapping series names to their data arrays
     * @param style - Style with valueKey and per-series configuration
     * @returns An East expression representing the composed chart component
     *
     * @remarks
     * Use ComposedMulti when series have different data points (sparse data).
     * Each series specifies its chart type in style.series.
     *
     * @example
     * ```ts
     * Chart.ComposedMulti(
     *     {
     *         revenue: [
     *             { month: "Jan", value: 100 },
     *             { month: "Feb", value: 200 },
     *         ],
     *         profit: [
     *             { month: "Jan", value: 50 },
     *             { month: "Mar", value: 150 }, // Feb missing - sparse
     *         ],
     *     },
     *     {
     *         xAxis: { dataKey: "month" },
     *         valueKey: "value",
     *         series: {
     *             revenue: { type: "bar", color: "teal.solid" },
     *             profit: { type: "line", color: "purple.solid" },
     *         },
     *     }
     * );
     * ```
     */
    ComposedMulti: createComposedChartMulti,

    /**
     * Helper function to create chart series configuration.
     *
     * @param config - Series configuration options
     * @returns A series configuration object
     *
     * @remarks
     * Used to define how a data field is rendered as a series in charts.
     */
    Series: ChartSeries,
    /**
     * Helper function to create chart sort configuration.
     *
     * @param config - Sort configuration options
     * @returns A sort configuration object
     *
     * @remarks
     * Used to sort data in BarList and BarSegment charts.
     */
    Sort: ChartSort,
    /**
     * Helper function to create stack offset configuration.
     *
     * @param offset - Stack offset type
     * @returns A stack offset variant
     *
     * @remarks
     * Controls how stacked series are offset (none, expand, wiggle, silhouette).
     */
    StackOffset,
    /**
     * Helper function to create bar layout configuration.
     *
     * @param layout - Bar layout type
     * @returns A bar layout variant
     *
     * @remarks
     * Controls bar orientation (horizontal or vertical).
     */
    BarLayout,

    /**
     * Tick format helpers for axis labels.
     *
     * @remarks
     * Provides type-safe formatters for different number and date formats.
     */
    TickFormat: {
        /** Format as plain number */
        Number: NumberTickFormat,
        /** Format as currency */
        Currency: CurrencyTickFormat,
        /** Format as percentage */
        Percent: PercentTickFormat,
        /** Format as compact number (K, M, B) */
        Compact: CompactTickFormat,
        /** Format with custom unit */
        Unit: UnitTickFormat,
        /** Format in scientific notation */
        Scientific: ScientificTickFormat,
        /** Format in engineering notation */
        Engineering: EngineeringTickFormat,
        /** Format as date */
        Date: DateTickFormat,
        /** Format as time */
        Time: TimeTickFormat,
        /** Format as date and time */
        DateTime: DateTimeTickFormat
    },

    /**
     * East types for all chart components and configuration.
     *
     * @remarks
     * Access these types for serialization or type-checking chart data structures.
     */
    Types: {
        /**
         * The concrete East type for chart series configuration.
         *
         * @remarks
         * Defines how a data field is rendered as a series in multi-series charts.
         * Mirrors Chakra's useChart series config.
         *
         * @property name - Data key name matching keys in data points (StringType)
         * @property color - Chakra color token e.g. "teal.solid" (OptionType<StringType>)
         * @property stackId - Stack group ID for stacking (OptionType<StringType>)
         * @property label - Display label, defaults to name (OptionType<StringType>)
         * @property stroke - Stroke/line color (OptionType<StringType>)
         * @property strokeWidth - Stroke width in pixels (OptionType<IntegerType>)
         * @property fill - Fill color (OptionType<StringType>)
         * @property fillOpacity - Fill opacity 0-1 (OptionType<FloatType>)
         * @property strokeDasharray - Dash pattern e.g. "5 5" (OptionType<StringType>)
         */
        Series: ChartSeriesType,
        /**
         * The concrete East type for chart sort configuration.
         *
         * @remarks
         * Used to sort data in BarList and BarSegment charts.
         *
         * @property by - Data key to sort by (StringType)
         * @property direction - Sort direction asc or desc (ChartSortDirectionType)
         */
        Sort: ChartSortType,
        /**
         * Sort direction variant type.
         *
         * @remarks
         * Controls ascending or descending sort order for charts.
         *
         * @property asc - Ascending order (smallest to largest)
         * @property desc - Descending order (largest to smallest)
         */
        SortDirection: ChartSortDirectionType,
        /**
         * The concrete East type for chart axis configuration.
         *
         * @remarks
         * Configures X and Y axis display on Cartesian charts.
         *
         * @property dataKey - Field name for axis values (OptionType<StringType>)
         * @property label - Axis label text (OptionType<StringType>)
         * @property tickFormat - Format for tick labels (OptionType<TickFormatType>)
         * @property hide - Whether to hide the axis (OptionType<BooleanType>)
         * @property domain - Axis domain min/max (OptionType<ArrayType<FloatType>>)
         * @property tickLine - Show tick lines (OptionType<BooleanType>)
         * @property axisLine - Show axis line (OptionType<BooleanType>)
         */
        Axis: ChartAxisType,
        /**
         * Tick format variant type for axis labels.
         *
         * @remarks
         * Provides type-safe number and date formatting options for axis ticks.
         *
         * @property Number - Plain number format with decimal places
         * @property Currency - Currency format with symbol and locale
         * @property Percent - Percentage format
         * @property Compact - Compact notation (K, M, B)
         * @property Unit - Custom unit suffix
         * @property Scientific - Scientific notation
         * @property Engineering - Engineering notation
         * @property Date - Date format
         * @property Time - Time format
         * @property DateTime - Date and time format
         */
        TickFormat: TickFormatType,
        /**
         * Curve type variant for line interpolation.
         *
         * @remarks
         * Controls how line segments are interpolated between data points.
         *
         * @property linear - Straight line segments
         * @property natural - Natural cubic spline (smooth)
         * @property monotone - Monotone cubic interpolation (no overshoot)
         * @property step - Step function (horizontal then vertical)
         * @property stepBefore - Step before the point
         * @property stepAfter - Step after the point
         */
        Curve: CurveType,
        /**
         * Stack offset variant type.
         *
         * @remarks
         * Controls how stacked series are offset relative to each other.
         *
         * @property none - No offset, standard stacking from zero
         * @property expand - Normalize to percentage (0-100%)
         * @property wiggle - Minimize deviation from center
         * @property silhouette - Center the baseline
         */
        StackOffset: StackOffsetType,
        /**
         * Bar layout variant type.
         *
         * @remarks
         * Controls the orientation of bars in bar charts.
         *
         * @property horizontal - Bars extend horizontally (category on Y axis)
         * @property vertical - Bars extend vertically (category on X axis)
         */
        BarLayout: BarLayoutType,
        /**
         * Multi-series data type for sparse/separate series arrays.
         *
         * @remarks
         * Used when data is passed as a record of arrays instead of a single array.
         * Each key is a series name, value is an array of data points.
         * This avoids the need for null values when series have different data points.
         */
        MultiSeriesData: MultiSeriesDataType,

        /**
         * The concrete East type for Area chart data.
         *
         * @remarks
         * Area charts display quantitative data with filled areas under line curves.
         * Supports stacking for showing part-to-whole relationships.
         *
         * @property data - Array of data points as Dict<String, LiteralValue>
         * @property series - Array of series configuration (ArrayType<ChartSeriesType>)
         * @property xAxis - X-axis configuration (OptionType<ChartAxisType>)
         * @property yAxis - Y-axis configuration (OptionType<ChartAxisType>)
         * @property curveType - Line curve interpolation (OptionType<CurveType>)
         * @property stacked - Enable stacking (OptionType<BooleanType>)
         * @property stackOffset - Stack offset mode (OptionType<StackOffsetType>)
         * @property grid - Grid configuration (OptionType<ChartGridType>)
         * @property tooltip - Tooltip configuration (OptionType<ChartTooltipType>)
         * @property legend - Legend configuration (OptionType<ChartLegendType>)
         * @property margin - Chart margin (OptionType<ChartMarginType>)
         * @property fillOpacity - Fill opacity 0-1 (OptionType<FloatType>)
         * @property connectNulls - Connect across nulls (OptionType<BooleanType>)
         */
        AreaChart: AreaChartType,
        /**
         * The concrete East type for Area Range chart data.
         *
         * @remarks
         * Area range charts display bands between low/high values (e.g., min/max, high/low).
         * Each series has a lowKey and highKey defining the range bounds.
         *
         * @property data - Array of data points as Dict<String, LiteralValue>
         * @property dataSeries - Record of arrays per series (for sparse data)
         * @property lowKey - Field name for lower bound (multi-series form)
         * @property highKey - Field name for upper bound (multi-series form)
         * @property series - Array of range series configuration (ArrayType<AreaRangeSeriesType>)
         * @property xAxis - X-axis configuration (OptionType<ChartAxisType>)
         * @property yAxis - Y-axis configuration (OptionType<ChartAxisType>)
         * @property curveType - Line curve interpolation (OptionType<CurveType>)
         * @property grid - Grid configuration (OptionType<ChartGridType>)
         * @property tooltip - Tooltip configuration (OptionType<ChartTooltipType>)
         * @property legend - Legend configuration (OptionType<ChartLegendType>)
         * @property margin - Chart margin (OptionType<ChartMarginType>)
         * @property fillOpacity - Fill opacity 0-1 (OptionType<FloatType>)
         * @property connectNulls - Connect across nulls (OptionType<BooleanType>)
         */
        AreaRangeChart: AreaRangeChartType,
        /**
         * The concrete East type for Area Range series configuration.
         *
         * @remarks
         * Defines how a range series is rendered in an area range chart.
         *
         * @property name - Series identifier (StringType)
         * @property lowKey - Field name for lower bound values (StringType)
         * @property highKey - Field name for upper bound values (StringType)
         * @property color - Chakra color token (OptionType<StringType>)
         * @property label - Display label (OptionType<StringType>)
         * @property fillOpacity - Fill opacity 0-1 (OptionType<FloatType>)
         * @property stroke - Stroke color (OptionType<StringType>)
         * @property strokeWidth - Stroke width in pixels (OptionType<IntegerType>)
         */
        AreaRangeSeries: AreaRangeSeriesType,
        /**
         * The concrete East type for Bar chart data.
         *
         * @remarks
         * Bar charts display categorical data with rectangular bars.
         * Supports horizontal/vertical layouts and stacking.
         *
         * @property data - Array of data points as Dict<String, LiteralValue>
         * @property series - Array of series configuration (ArrayType<ChartSeriesType>)
         * @property xAxis - X-axis configuration (OptionType<ChartAxisType>)
         * @property yAxis - Y-axis configuration (OptionType<ChartAxisType>)
         * @property layout - Bar direction (OptionType<BarLayoutType>)
         * @property stacked - Enable stacking (OptionType<BooleanType>)
         * @property stackOffset - Stack offset mode (OptionType<StackOffsetType>)
         * @property grid - Grid configuration (OptionType<ChartGridType>)
         * @property tooltip - Tooltip configuration (OptionType<ChartTooltipType>)
         * @property legend - Legend configuration (OptionType<ChartLegendType>)
         * @property margin - Chart margin (OptionType<ChartMarginType>)
         * @property barSize - Bar width/height in pixels (OptionType<IntegerType>)
         * @property barGap - Gap between bars (OptionType<IntegerType>)
         * @property radius - Rounded corner radius (OptionType<IntegerType>)
         */
        BarChart: BarChartType,
        /**
         * The concrete East type for Line chart data.
         *
         * @remarks
         * Line charts display data points connected by line segments.
         * Ideal for showing trends over time.
         *
         * @property data - Array of data points as Dict<String, LiteralValue>
         * @property series - Array of series configuration (ArrayType<ChartSeriesType>)
         * @property xAxis - X-axis configuration (OptionType<ChartAxisType>)
         * @property yAxis - Y-axis configuration (OptionType<ChartAxisType>)
         * @property curveType - Line curve interpolation (OptionType<CurveType>)
         * @property grid - Grid configuration (OptionType<ChartGridType>)
         * @property tooltip - Tooltip configuration (OptionType<ChartTooltipType>)
         * @property legend - Legend configuration (OptionType<ChartLegendType>)
         * @property margin - Chart margin (OptionType<ChartMarginType>)
         * @property showDots - Show dots at data points (OptionType<BooleanType>)
         * @property strokeWidth - Line stroke width (OptionType<IntegerType>)
         * @property connectNulls - Connect across nulls (OptionType<BooleanType>)
         */
        LineChart: LineChartType,
        /**
         * The concrete East type for Scatter chart data.
         *
         * @remarks
         * Scatter charts display individual data points on a coordinate plane.
         * Ideal for showing relationships between two variables.
         *
         * @property data - Array of data points as Dict<String, LiteralValue>
         * @property series - Array of series configuration (ArrayType<ChartSeriesType>)
         * @property xAxis - X-axis configuration (OptionType<ChartAxisType>)
         * @property yAxis - Y-axis configuration (OptionType<ChartAxisType>)
         * @property grid - Grid configuration (OptionType<ChartGridType>)
         * @property tooltip - Tooltip configuration (OptionType<ChartTooltipType>)
         * @property legend - Legend configuration (OptionType<ChartLegendType>)
         * @property margin - Chart margin (OptionType<ChartMarginType>)
         */
        ScatterChart: ScatterChartType,
        /**
         * The concrete East type for Pie chart data.
         *
         * @remarks
         * Pie charts display proportional data as slices of a circle.
         * Set innerRadius for a donut chart appearance.
         *
         * @property data - Array of pie slices (ArrayType<PieSliceType>)
         * @property innerRadius - Inner radius for donut chart (OptionType<IntegerType>)
         * @property outerRadius - Outer radius (OptionType<IntegerType>)
         * @property startAngle - Starting angle in degrees (OptionType<IntegerType>)
         * @property endAngle - Ending angle in degrees (OptionType<IntegerType>)
         * @property showLabels - Show slice labels (OptionType<BooleanType>)
         * @property tooltip - Tooltip configuration (OptionType<ChartTooltipType>)
         * @property legend - Legend configuration (OptionType<ChartLegendType>)
         */
        PieChart: PieChartType,
        /**
         * The concrete East type for Pie chart slice data.
         *
         * @remarks
         * Each slice represents a segment of the pie chart.
         *
         * @property name - Slice label (StringType)
         * @property value - Slice value (IntegerType or FloatType)
         * @property color - Slice color (OptionType<StringType>)
         */
        PieSlice: PieSliceType,
        /**
         * The concrete East type for Radar chart data.
         *
         * @remarks
         * Radar charts display multivariate data on radial axes.
         * Useful for comparing multiple attributes across entities.
         *
         * @property data - Array of data points as Dict<String, LiteralValue>
         * @property series - Array of series configuration (ArrayType<ChartSeriesType>)
         * @property dataKey - Field name for radial axis labels (StringType)
         * @property grid - Grid configuration (OptionType<ChartGridType>)
         * @property tooltip - Tooltip configuration (OptionType<ChartTooltipType>)
         * @property legend - Legend configuration (OptionType<ChartLegendType>)
         */
        RadarChart: RadarChartType,
        /**
         * The concrete East type for BarList data.
         *
         * @remarks
         * BarList displays horizontal comparison bars with labels and values.
         * Native Chakra component, not Recharts-based.
         *
         * @property data - Array of bar items (ArrayType<BarListItemType>)
         * @property colorPalette - Default color scheme (OptionType<ColorSchemeType>)
         * @property showValue - Show values next to bars (OptionType<BooleanType>)
         * @property sort - Sort configuration (OptionType<ChartSortType>)
         */
        BarList: BarListType,
        /**
         * The concrete East type for BarList item data.
         *
         * @remarks
         * Each item represents a bar in the BarList chart.
         *
         * @property name - Item label (StringType)
         * @property value - Item value (IntegerType or FloatType)
         * @property color - Item color (OptionType<StringType>)
         * @property href - Optional link URL (OptionType<StringType>)
         */
        BarListItem: BarListItemType,
        /**
         * The concrete East type for BarSegment data.
         *
         * @remarks
         * BarSegment displays proportional segments in a single horizontal bar.
         * Native Chakra component for showing percentage breakdowns.
         *
         * @property data - Array of segment items (ArrayType<BarSegmentItemType>)
         * @property showLegend - Show legend (OptionType<BooleanType>)
         * @property showValue - Show values on segments (OptionType<BooleanType>)
         */
        BarSegment: BarSegmentType,
        /**
         * The concrete East type for BarSegment item data.
         *
         * @remarks
         * Each item represents a segment in the BarSegment chart.
         *
         * @property name - Segment label (StringType)
         * @property value - Segment value (IntegerType or FloatType)
         * @property color - Segment color (OptionType<StringType>)
         */
        BarSegmentItem: BarSegmentItemType,
        /**
         * The concrete East type for Composed chart data.
         *
         * @remarks
         * Composed charts combine multiple chart types (Line, Area, Bar, Scatter, AreaRange)
         * in a single visualization. Each series specifies its chart type via the variant.
         *
         * @property data - Array of data points as Dict<String, LiteralValue>
         * @property dataSeries - Record of arrays per series for sparse data
         * @property valueKey - Field name for Y values in dataSeries form
         * @property series - Array of composed series (discriminated variant)
         * @property xAxis - X-axis configuration
         * @property yAxis - Y-axis configuration
         * @property layout - Bar direction for bar series
         * @property curveType - Curve interpolation for line/area series
         * @property stackOffset - Stack offset mode
         * @property grid - Grid configuration
         * @property tooltip - Tooltip configuration
         * @property legend - Legend configuration
         * @property margin - Chart margin
         * @property brush - Brush configuration
         * @property barSize - Bar width/height in pixels
         * @property barGap - Gap between bars
         * @property showDots - Show dots for line series (global default)
         * @property connectNulls - Connect line across null data points
         */
        ComposedChart: ComposedChartType,
        /**
         * The concrete East type for Composed series (discriminated variant).
         *
         * @remarks
         * A discriminated variant where each tag determines the chart type
         * and its associated configuration.
         *
         * @property line - Line series with dots, stroke options
         * @property area - Area series with fill, stacking options
         * @property areaRange - Area range series with lowKey/highKey for bands
         * @property bar - Bar series with fill, stacking, radius options
         * @property scatter - Scatter series with point size
         */
        ComposedSeries: ComposedSeriesType,
        /**
         * Reference line configuration type.
         *
         * @remarks
         * Draws horizontal or vertical lines at specific values.
         *
         * @property x - X value for vertical line
         * @property y - Y value for horizontal line
         * @property stroke - Line color
         * @property strokeWidth - Line width
         * @property strokeDasharray - Dash pattern
         * @property label - Label text
         * @property ifOverflow - Overflow behavior
         */
        ReferenceLine: ReferenceLineType,
        /**
         * Reference dot configuration type.
         *
         * @remarks
         * Marks specific x,y coordinates on the chart.
         *
         * @property x - X coordinate
         * @property y - Y coordinate
         * @property r - Radius
         * @property fill - Fill color
         * @property stroke - Stroke color
         * @property label - Label text
         * @property ifOverflow - Overflow behavior
         */
        ReferenceDot: ReferenceDotType,
        /**
         * Reference area configuration type.
         *
         * @remarks
         * Highlights rectangular regions on the chart.
         *
         * @property x1 - Left bound
         * @property x2 - Right bound
         * @property y1 - Bottom bound
         * @property y2 - Top bound
         * @property fill - Fill color
         * @property fillOpacity - Fill opacity
         * @property stroke - Stroke color
         * @property label - Label text
         * @property ifOverflow - Overflow behavior
         */
        ReferenceArea: ReferenceAreaType,
        /**
         * Reference overflow behavior type.
         *
         * @remarks
         * Controls what happens when reference annotations extend beyond chart bounds.
         *
         * @property discard - Don't render if outside bounds
         * @property hidden - Clip at chart boundary
         * @property visible - Render completely (may overflow)
         * @property extendDomain - Extend axis domain to include
         */
        ReferenceOverflow: ReferenceOverflowType,
    },
} as const;

// Keep Sparkline export for backwards compatibility
export { Sparkline };
