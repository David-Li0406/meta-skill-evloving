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
    IntegerType,
    FloatType,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    ChartBrushType,
    CurveType,
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
import type {
    LineChartStyle,
    LineChartMultiStyle,
    LineChartSeriesConfig,
    LineChartStyleBase,
    LineChartBrushStyle,
} from "./types.js";

// Re-export types
export {
    LineChartType,
    LineChartSeriesType,
    type LineChartStyle,
    type LineChartMultiStyle,
    type LineChartSeriesConfig,
    type LineChartStyleBase,
    type LineChartBrushStyle,
} from "./types.js";

// ============================================================================
// Type Helpers
// ============================================================================

// Numeric types that can be used as Y-axis values
type NumericEastType = IntegerType | FloatType;

// Extract struct fields from array type
type ExtractStructFields<T> = T extends ArrayType<infer S>
    ? S extends StructType
        ? S["fields"]
        : never
    : never;

// Extract fields from data (handles SubtypeExprOrValue wrapping)
type DataFields<T extends SubtypeExprOrValue<ArrayType<StructType>>> = ExtractStructFields<TypeOf<T>>;

// Extract only numeric field keys from a struct's fields
type NumericFieldKeys<Fields> = {
    [K in keyof Fields]: Fields[K] extends NumericEastType ? K : never
}[keyof Fields];

// All field keys as strings
type FieldKeys<Fields> = keyof Fields & string;

// ============================================================================
// Series Specification (like Table's ColumnSpec)
// ============================================================================

/**
 * Series specification for the Line chart API.
 *
 * @remarks
 * - **Array form**: Only numeric field keys allowed (e.g., `["revenue", "profit"]`)
 * - **Object form**: Numeric fields with optional per-series config
 */
type SeriesSpec<T extends SubtypeExprOrValue<ArrayType<StructType>>> =
    | NumericFieldKeys<DataFields<NoInfer<T>>>[]
    | { [K in NumericFieldKeys<DataFields<NoInfer<T>>>]?: LineChartSeriesConfig };

// ============================================================================
// Line Chart (Single Array Form)
// ============================================================================

/**
 * Creates a Line chart component from a single data array.
 *
 * @typeParam T - The array type containing data structs
 * @param data - Array of data points (each point has x-axis value + y-axis values)
 * @param series - Series specification: array of numeric field names, or object with config
 * @param style - Optional styling with type-safe xAxis.dataKey
 * @returns An East expression representing the line chart component
 *
 * @remarks
 * All series share the same data points. Series keys are numeric field names.
 * Use this when all series have values at the same x-axis points.
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
 *     { xAxis: { dataKey: "month" } }
 * );
 * ```
 */
export function createLineChart<T extends SubtypeExprOrValue<ArrayType<StructType>>>(
    data: T,
    series: SeriesSpec<T>,
    style?: LineChartStyle<FieldKeys<DataFields<T>>>
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

    // Normalize series to entries
    const seriesEntries: readonly (readonly [string, LineChartSeriesConfig | undefined])[] = Array.isArray(series)
        ? (series as string[]).map(key => [key, undefined] as const)
        : Object.entries(series) as [string, LineChartSeriesConfig | undefined][];

    return buildLineChart(data_mapped, undefined, seriesEntries, style);
}

// ============================================================================
// Line Chart Multi (Multi-Series with Separate Arrays)
// ============================================================================

/**
 * Creates a Line chart component from multiple data arrays (one per series).
 *
 * @typeParam K - Union of series names (record keys)
 * @typeParam T - The array type containing data structs for each series
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
export function createLineChartMulti<
    K extends string,
    T extends SubtypeExprOrValue<ArrayType<StructType>>
>(
    data: Record<K, T>,
    style: LineChartMultiStyle<
        FieldKeys<DataFields<T>>,
        NumericFieldKeys<DataFields<T>> & string,
        K
    >
): ExprType<UIComponentType> {
    // Create empty data array (renderer will use dataSeries instead)
    const data_mapped = East.value([], ArrayType(DictType(StringType, LiteralValueType)));

    // Map each series array to Dict format
    const seriesDataMap = new Map<string, ExprType<ArrayType<DictType<typeof StringType, typeof LiteralValueType>>>>();

    for (const [seriesName, seriesData] of Object.entries(data) as [string, T][]) {
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

    // Build series entries from record keys and optional config
    const seriesEntries = Object.keys(data).map(key => [
        key,
        style.series?.[key as K]
    ] as const);

    return buildLineChart(data_mapped, dataSeries_mapped, seriesEntries, style, style.valueKey, style.pivotKey);
}

// ============================================================================
// Shared Chart Builder
// ============================================================================

function buildLineChart(
    data_mapped: ExprType<ArrayType<DictType<typeof StringType, typeof LiteralValueType>>>,
    dataSeries_mapped: ExprType<typeof MultiSeriesDataType> | undefined,
    seriesEntries: readonly (readonly [string, LineChartSeriesConfig | undefined])[],
    style?: LineChartStyleBase<string> & { brush?: LineChartBrushStyle<string>; pivotKey?: string; valueKey?: string },
    valueKey?: string,
    pivotKey?: string
): ExprType<UIComponentType> {
    const series_mapped = seriesEntries.map(([name, config]) => {
        // Convert yAxisId string literal to variant
        const yAxisIdValue = config?.yAxisId !== undefined
            ? (typeof config.yAxisId === "string"
                ? some(East.value(variant(config.yAxisId, null), YAxisIdType))
                : some(config.yAxisId))
            : none;

        // Convert pivotColors Map to East Dict
        const pivotColorsValue = config?.pivotColors !== undefined
            ? some(config.pivotColors)
            : none;

        return {
            name: name,
            dataKey: some(name), // dataKey defaults to series name
            color: config?.color !== undefined ? some(config.color) : none,
            stackId: none,
            label: config?.label !== undefined ? some(config.label) : none,
            stroke: config?.stroke !== undefined ? some(config.stroke) : none,
            strokeWidth: config?.strokeWidth !== undefined ? some(config.strokeWidth) : none,
            strokeDasharray: config?.strokeDasharray !== undefined ? some(config.strokeDasharray) : none,
            showDots: config?.showDots !== undefined ? some(config.showDots) : none,
            showLine: config?.showLine !== undefined ? some(config.showLine) : none,
            yAxisId: yAxisIdValue,
            pivotColors: pivotColorsValue,
            layerIndex: config?.layerIndex !== undefined ? some(config.layerIndex) : none,
        };
    });

    const curveValue = style?.curveType
        ? (typeof style.curveType === "string"
            ? East.value(variant(style.curveType, null), CurveType)
            : style.curveType)
        : undefined;

    // Convert axis styles to types
    const xAxisExpr = axisStyleToType(style?.xAxis as ChartAxisStyle | undefined);
    const yAxisExpr = axisStyleToType(style?.yAxis as ChartAxisStyle | undefined);
    const yAxis2Expr = axisStyleToType(style?.yAxis2 as ChartAxisStyle | undefined);

    // Convert other style properties
    const gridExpr = gridStyleToType(style?.grid);
    const tooltipExpr = tooltipStyleToType(style?.tooltip);
    const legendExpr = legendStyleToType(style?.legend);
    const marginExpr = marginStyleToType(style?.margin);

    // Build brush value
    const brushValue = style?.brush
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
    const referenceLinesExpr = style?.referenceLines?.length
        ? variant("some", East.value(style.referenceLines.map(referenceLineStyleToType), ArrayType(ReferenceLineType)))
        : variant("none", null);
    const referenceDotsExpr = style?.referenceDots?.length
        ? variant("some", East.value(style.referenceDots.map(referenceDotStyleToType), ArrayType(ReferenceDotType)))
        : variant("none", null);
    const referenceAreasExpr = style?.referenceAreas?.length
        ? variant("some", East.value(style.referenceAreas.map(referenceAreaStyleToType), ArrayType(ReferenceAreaType)))
        : variant("none", null);

    // Get pivotKey from parameter or style
    const effectivePivotKey = pivotKey ?? style?.pivotKey;
    // Get valueKey from parameter or style
    const effectiveValueKey = valueKey ?? style?.valueKey;

    return East.value(variant("LineChart", {
        data: data_mapped,
        dataSeries: dataSeries_mapped ? variant("some", dataSeries_mapped) : variant("none", null),
        valueKey: effectiveValueKey !== undefined ? variant("some", effectiveValueKey) : variant("none", null),
        pivotKey: effectivePivotKey !== undefined ? variant("some", effectivePivotKey) : variant("none", null),
        series: series_mapped,
        xAxis: xAxisExpr ? variant("some", xAxisExpr) : variant("none", null),
        yAxis: yAxisExpr ? variant("some", yAxisExpr) : variant("none", null),
        yAxis2: yAxis2Expr ? variant("some", yAxis2Expr) : variant("none", null),
        curveType: curveValue ? variant("some", curveValue) : variant("none", null),
        grid: gridExpr ? variant("some", gridExpr) : variant("none", null),
        tooltip: tooltipExpr ? variant("some", tooltipExpr) : variant("none", null),
        legend: legendExpr ? variant("some", legendExpr) : variant("none", null),
        margin: marginExpr ? variant("some", marginExpr) : variant("none", null),
        brush: brushValue,
        showDots: style?.showDots !== undefined ? variant("some", style.showDots) : variant("none", null),
        strokeWidth: style?.strokeWidth !== undefined ? variant("some", style.strokeWidth) : variant("none", null),
        connectNulls: style?.connectNulls !== undefined ? variant("some", style.connectNulls) : variant("none", null),
        referenceLines: referenceLinesExpr,
        referenceDots: referenceDotsExpr,
        referenceAreas: referenceAreasExpr,
    }), UIComponentType);
}
