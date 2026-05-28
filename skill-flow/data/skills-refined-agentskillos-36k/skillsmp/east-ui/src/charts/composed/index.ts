/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    type TypeOf,
    ArrayType,
    DictType,
    East,
    Expr,
    LiteralValueType,
    none,
    some,
    StringType,
    StructType,
    variant,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    ChartBrushType,
    CurveType,
    BarLayoutType,
    StackOffsetType,
    MultiSeriesDataType,
    ReferenceLineType,
    ReferenceDotType,
    ReferenceAreaType,
    YAxisIdType,
    axisStyleToType,
    gridStyleToType,
    tooltipStyleToType,
    legendStyleToType,
    marginStyleToType,
    referenceLineStyleToType,
    referenceDotStyleToType,
    referenceAreaStyleToType,
    type ChartAxisStyle,
} from "../types.js";
import {
    ComposedSeriesType,
    type ComposedChartStyle,
    type ComposedChartMultiStyleMapped,
    type ComposedSeriesConfig,
    type ComposedChartStyleBase,
    type ComposedChartBrushStyle,
} from "./types.js";

// Re-export types
export {
    ComposedChartType,
    ComposedSeriesType,
    type ComposedChartStyle,
    type ComposedChartMultiStyle,
    type ComposedChartMultiStyleMapped,
    type ComposedSeriesConfig,
    type ComposedSeriesConfigFor,
    type ComposedChartStyleBase,
    type ComposedChartBrushStyle,
    type ComposedLineSeries,
    type ComposedAreaSeries,
    type ComposedAreaRangeSeries,
    type ComposedAreaRangeSeriesFor,
    type ComposedBarSeries,
    type ComposedScatterSeries,
    type ComposedSeriesBase,
} from "./types.js";

// ============================================================================
// Type Helpers
// ============================================================================

// Extract struct fields from array type
type ExtractStructFields<T> = T extends ArrayType<infer S>
    ? S extends StructType
        ? S["fields"]
        : never
    : never;

// Extract fields from data (handles SubtypeExprOrValue wrapping)
type DataFields<T extends SubtypeExprOrValue<ArrayType<StructType>>> = ExtractStructFields<TypeOf<T>>;

// All field keys as strings
type FieldKeys<Fields> = keyof Fields & string;

// ============================================================================
// Series Conversion Helpers
// ============================================================================

/**
 * Converts a TypeScript series config to an East variant value.
 */
function seriesConfigToVariant(name: string, config: ComposedSeriesConfig) {
    // Convert yAxisId string literal to variant
    const yAxisIdValue = config.yAxisId !== undefined
        ? (typeof config.yAxisId === "string"
            ? some(East.value(variant(config.yAxisId, null), YAxisIdType))
            : some(config.yAxisId))
        : none;

    switch (config.type) {
        case "line":
            return variant("line", {
                name,
                dataKey: some(config.dataKey ?? name), // defaults to series name
                color: config.color !== undefined ? some(config.color) : none,
                stackId: config.stackId !== undefined ? some(config.stackId) : none,
                label: config.label !== undefined ? some(config.label) : none,
                stroke: config.stroke !== undefined ? some(config.stroke) : none,
                strokeWidth: config.strokeWidth !== undefined ? some(config.strokeWidth) : none,
                strokeDasharray: config.strokeDasharray !== undefined ? some(config.strokeDasharray) : none,
                showDots: config.showDots !== undefined ? some(config.showDots) : none,
                showLine: config.showLine !== undefined ? some(config.showLine) : none,
                yAxisId: yAxisIdValue,
                pivotColors: config.pivotColors !== undefined ? some(config.pivotColors) : none,
                layerIndex: config.layerIndex !== undefined ? some(config.layerIndex) : none,
            });

        case "area":
            return variant("area", {
                name,
                dataKey: some(config.dataKey ?? name), // defaults to series name
                color: config.color !== undefined ? some(config.color) : none,
                stackId: config.stackId !== undefined ? some(config.stackId) : none,
                label: config.label !== undefined ? some(config.label) : none,
                stroke: config.stroke !== undefined ? some(config.stroke) : none,
                strokeWidth: config.strokeWidth !== undefined ? some(config.strokeWidth) : none,
                fill: config.fill !== undefined ? some(config.fill) : none,
                fillOpacity: config.fillOpacity !== undefined ? some(config.fillOpacity) : none,
                strokeDasharray: config.strokeDasharray !== undefined ? some(config.strokeDasharray) : none,
                yAxisId: yAxisIdValue,
                pivotColors: config.pivotColors !== undefined ? some(config.pivotColors) : none,
                layerIndex: config.layerIndex !== undefined ? some(config.layerIndex) : none,
            });

        case "area-range":
            return variant("areaRange", {
                name,
                lowKey: config.lowKey,
                highKey: config.highKey,
                color: config.color !== undefined ? some(config.color) : none,
                label: config.label !== undefined ? some(config.label) : none,
                fillOpacity: config.fillOpacity !== undefined ? some(config.fillOpacity) : none,
                stroke: config.stroke !== undefined ? some(config.stroke) : none,
                strokeWidth: config.strokeWidth !== undefined ? some(config.strokeWidth) : none,
                yAxisId: yAxisIdValue,
            });

        case "bar":
            return variant("bar", {
                name,
                dataKey: some(config.dataKey ?? name), // defaults to series name
                color: config.color !== undefined ? some(config.color) : none,
                stackId: config.stackId !== undefined ? some(config.stackId) : none,
                label: config.label !== undefined ? some(config.label) : none,
                stroke: config.stroke !== undefined ? some(config.stroke) : none,
                strokeWidth: config.strokeWidth !== undefined ? some(config.strokeWidth) : none,
                fill: config.fill !== undefined ? some(config.fill) : none,
                fillOpacity: config.fillOpacity !== undefined ? some(config.fillOpacity) : none,
                strokeDasharray: config.strokeDasharray !== undefined ? some(config.strokeDasharray) : none,
                yAxisId: yAxisIdValue,
                pivotColors: config.pivotColors !== undefined ? some(config.pivotColors) : none,
                layerIndex: config.layerIndex !== undefined ? some(config.layerIndex) : none,
            });

        case "scatter":
            return variant("scatter", {
                name,
                dataKey: some(config.dataKey ?? name), // defaults to series name
                color: config.color !== undefined ? some(config.color) : none,
                stackId: none, // scatter doesn't stack but ChartSeriesType has it
                label: config.label !== undefined ? some(config.label) : none,
                stroke: config.stroke !== undefined ? some(config.stroke) : none,
                strokeWidth: config.strokeWidth !== undefined ? some(config.strokeWidth) : none,
                fill: config.fill !== undefined ? some(config.fill) : none,
                fillOpacity: config.fillOpacity !== undefined ? some(config.fillOpacity) : none,
                strokeDasharray: none, // scatter doesn't use dashes
                yAxisId: yAxisIdValue,
                pivotColors: config.pivotColors !== undefined ? some(config.pivotColors) : none,
                layerIndex: config.layerIndex !== undefined ? some(config.layerIndex) : none,
            });
    }
}

// ============================================================================
// Composed Chart (Single Array Form)
// ============================================================================

/**
 * Creates a Composed chart component from a single data array.
 *
 * @typeParam T - The array type containing data structs
 * @param data - Array of data points (each point has x-axis value + y-axis values)
 * @param style - Style with series configuration (each series specifies its chart type)
 * @returns An East expression representing the composed chart component
 *
 * @remarks
 * Composed charts combine multiple chart types in a single visualization.
 * Each series in the style object specifies its type (line, area, bar, scatter, area-range).
 *
 * @example Mixed chart types
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
 * @example With area-range for confidence bands
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
export function createComposedChart<T extends SubtypeExprOrValue<ArrayType<StructType>>>(
    data: T,
    style: ComposedChartStyle<FieldKeys<DataFields<T>>, string>
): ExprType<UIComponentType> {
    const data_expr = East.value(data) as ExprType<ArrayType<StructType>>;
    const field_types = Expr.type(data_expr).value.fields;

    // Map each data row to a Dict<String, LiteralValueType>
    const data_mapped = data_expr.map(($, datum) => {
        const ret = $.let(new Map(), DictType(StringType, LiteralValueType));
        for (const [field_name, field_type] of Object.entries(field_types)) {
            $(ret.insert(field_name, variant(field_type.type, (datum as any)[field_name])));
        }
        return ret;
    });

    // Convert series entries to variant array
    const seriesEntries = Object.entries(style.series) as [string, ComposedSeriesConfig][];

    return buildComposedChart(data_mapped, undefined, seriesEntries, style);
}

// ============================================================================
// Composed Chart Multi (Multi-Series with Separate Arrays)
// ============================================================================

/**
 * Creates a Composed chart component from multiple data arrays (one per series).
 *
 * @typeParam K - Union of series names (record keys)
 * @typeParam T - The array type containing data structs for each series
 * @param data - Record mapping series names to their data arrays
 * @param style - Styling with valueKey and per-series configuration
 * @returns An East expression representing the composed chart component
 *
 * @remarks
 * Each series has its own data array, allowing sparse data where series
 * don't need to have values at every x-axis point. Each series specifies
 * its chart type.
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
 *             { month: "Mar", value: 150 }, // sparse - Feb missing
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
export function createComposedChartMulti<
    D extends Record<string, SubtypeExprOrValue<ArrayType<StructType>>>
>(
    data: D,
    style: ComposedChartMultiStyleMapped<D>
): ExprType<UIComponentType> {
    // Create empty data array (renderer will use dataSeries instead)
    const data_mapped = East.value([], ArrayType(DictType(StringType, LiteralValueType)));

    // Map each series array to Dict format
    const seriesDataMap = new Map<string, ExprType<ArrayType<DictType<typeof StringType, typeof LiteralValueType>>>>();

    for (const [seriesName, seriesData] of Object.entries(data) as [string, D[keyof D]][]) {
        const series_expr = East.value(seriesData) as ExprType<ArrayType<StructType>>;
        const field_types = Expr.type(series_expr).value.fields;

        const series_mapped = series_expr.map(($, datum) => {
            const ret = $.let(new Map(), DictType(StringType, LiteralValueType));
            for (const [field_name, field_type] of Object.entries(field_types)) {
                $(ret.insert(field_name, variant(field_type.type, (datum as any)[field_name])));
            }
            return ret;
        });

        seriesDataMap.set(seriesName, series_mapped);
    }

    const dataSeries_mapped = East.value(seriesDataMap, MultiSeriesDataType);

    // Build series entries from record keys and config
    const seriesEntries = Object.keys(data).map(key => [
        key,
        style.series[key as keyof D & string] ?? { type: "line" as const }
    ] as const);

    return buildComposedChart(
        data_mapped,
        dataSeries_mapped,
        seriesEntries as unknown as [string, ComposedSeriesConfig][],
        style as any,
        undefined,
        style.pivotKey as string | undefined
    );
}

// ============================================================================
// Shared Chart Builder
// ============================================================================

function buildComposedChart(
    data_mapped: ExprType<ArrayType<DictType<typeof StringType, typeof LiteralValueType>>>,
    dataSeries_mapped: ExprType<typeof MultiSeriesDataType> | undefined,
    seriesEntries: readonly [string, ComposedSeriesConfig][],
    style: ComposedChartStyleBase<string> & { brush?: ComposedChartBrushStyle<string> | undefined; pivotKey?: string | undefined; valueKey?: string | undefined },
    valueKey?: string | undefined,
    pivotKey?: string | undefined
): ExprType<UIComponentType> {
    // Convert series to variant array
    const series_mapped = seriesEntries.map(([name, config]) =>
        seriesConfigToVariant(name, config)
    );

    // Convert style options to East types
    const curveValue = style.curveType
        ? (typeof style.curveType === "string"
            ? East.value(variant(style.curveType, null), CurveType)
            : style.curveType)
        : undefined;

    const layoutValue = style.layout
        ? (typeof style.layout === "string"
            ? East.value(variant(style.layout, null), BarLayoutType)
            : style.layout)
        : undefined;

    const stackOffsetValue = style.stackOffset
        ? (typeof style.stackOffset === "string"
            ? East.value(variant(style.stackOffset, null), StackOffsetType)
            : style.stackOffset)
        : undefined;

    // Convert axis styles to types
    const xAxisExpr = axisStyleToType(style.xAxis as ChartAxisStyle | undefined);
    const yAxisExpr = axisStyleToType(style.yAxis as ChartAxisStyle | undefined);
    const yAxis2Expr = axisStyleToType(style.yAxis2 as ChartAxisStyle | undefined);

    // Convert other style properties
    const gridExpr = gridStyleToType(style.grid);
    const tooltipExpr = tooltipStyleToType(style.tooltip);
    const legendExpr = legendStyleToType(style.legend);
    const marginExpr = marginStyleToType(style.margin);

    // Build brush value
    const brushValue = style.brush
        ? variant("some", East.value({
            dataKey: style.brush.dataKey !== undefined ? some(style.brush.dataKey) : none,
            height: style.brush.height !== undefined ? some(style.brush.height) : none,
            travellerWidth: style.brush.travellerWidth !== undefined ? some(style.brush.travellerWidth) : none,
            startIndex: style.brush.startIndex !== undefined ? some(style.brush.startIndex) : none,
            endIndex: style.brush.endIndex !== undefined ? some(style.brush.endIndex) : none,
            stroke: style.brush.stroke !== undefined ? some(style.brush.stroke) : none,
            fill: style.brush.fill !== undefined ? some(style.brush.fill) : none,
        }, ChartBrushType))
        : variant("none", null);

    // Convert reference annotations
    const referenceLinesExpr = style.referenceLines?.length
        ? variant("some", East.value(style.referenceLines.map(referenceLineStyleToType), ArrayType(ReferenceLineType)))
        : variant("none", null);
    const referenceDotsExpr = style.referenceDots?.length
        ? variant("some", East.value(style.referenceDots.map(referenceDotStyleToType), ArrayType(ReferenceDotType)))
        : variant("none", null);
    const referenceAreasExpr = style.referenceAreas?.length
        ? variant("some", East.value(style.referenceAreas.map(referenceAreaStyleToType), ArrayType(ReferenceAreaType)))
        : variant("none", null);

    // Get pivotKey from parameter or style
    const effectivePivotKey = pivotKey ?? style.pivotKey;
    // Get valueKey from parameter or style
    const effectiveValueKey = valueKey ?? style.valueKey;

    return East.value(variant("ComposedChart", {
        data: data_mapped,
        dataSeries: dataSeries_mapped ? variant("some", dataSeries_mapped) : variant("none", null),
        valueKey: effectiveValueKey !== undefined ? variant("some", effectiveValueKey) : variant("none", null),
        pivotKey: effectivePivotKey !== undefined ? variant("some", effectivePivotKey) : variant("none", null),
        series: East.value(series_mapped, ArrayType(ComposedSeriesType)),
        xAxis: xAxisExpr ? variant("some", xAxisExpr) : variant("none", null),
        yAxis: yAxisExpr ? variant("some", yAxisExpr) : variant("none", null),
        yAxis2: yAxis2Expr ? variant("some", yAxis2Expr) : variant("none", null),
        layout: layoutValue ? variant("some", layoutValue) : variant("none", null),
        curveType: curveValue ? variant("some", curveValue) : variant("none", null),
        stackOffset: stackOffsetValue ? variant("some", stackOffsetValue) : variant("none", null),
        grid: gridExpr ? variant("some", gridExpr) : variant("none", null),
        tooltip: tooltipExpr ? variant("some", tooltipExpr) : variant("none", null),
        legend: legendExpr ? variant("some", legendExpr) : variant("none", null),
        margin: marginExpr ? variant("some", marginExpr) : variant("none", null),
        brush: brushValue,
        barSize: style.barSize !== undefined ? variant("some", style.barSize) : variant("none", null),
        barGap: style.barGap !== undefined ? variant("some", style.barGap) : variant("none", null),
        showDots: style.showDots !== undefined ? variant("some", style.showDots) : variant("none", null),
        connectNulls: style.connectNulls !== undefined ? variant("some", style.connectNulls) : variant("none", null),
        referenceLines: referenceLinesExpr,
        referenceDots: referenceDotsExpr,
        referenceAreas: referenceAreasExpr,
    }), UIComponentType);
}
