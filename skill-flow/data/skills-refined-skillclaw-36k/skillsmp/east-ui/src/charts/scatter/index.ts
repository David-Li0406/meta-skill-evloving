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
    ScatterChartStyle,
    ScatterChartMultiStyle,
    ScatterChartSeriesConfig,
} from "./types.js";

// Re-export types
export {
    ScatterChartType,
    type ScatterChartStyle,
    type ScatterChartMultiStyle,
    type ScatterChartSeriesConfig,
} from "./types.js";

// ============================================================================
// Type Helpers
// ============================================================================

// Numeric types that can be used as axis values
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

// ============================================================================
// Series Specification
// ============================================================================

/**
 * Series specification for the Scatter chart API.
 *
 * @remarks
 * - **Array form**: Only numeric field keys allowed (e.g., `["y1", "y2"]`)
 * - **Object form**: Numeric fields with optional per-series config
 */
type SeriesSpec<T extends SubtypeExprOrValue<ArrayType<StructType>>> =
    | NumericFieldKeys<DataFields<NoInfer<T>>>[]
    | { [K in NumericFieldKeys<DataFields<NoInfer<T>>>]?: ScatterChartSeriesConfig };

// ============================================================================
// Scatter Chart (Single Array Form)
// ============================================================================

/**
 * Creates a Scatter chart component from a single data array.
 *
 * @typeParam T - The array type containing data structs
 * @param data - Array of data points (each point has x + y values)
 * @param series - Series specification: array of numeric field names, or object with config
 * @param style - Optional styling with type-safe xDataKey and yDataKey
 * @returns An East expression representing the scatter chart component
 *
 * @remarks
 * All series share the same data points. Series keys are numeric field names.
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
// All field keys as strings
type FieldKeys<Fields> = keyof Fields & string;

export function createScatterChart<T extends SubtypeExprOrValue<ArrayType<StructType>>>(
    data: T,
    series: SeriesSpec<T>,
    style?: ScatterChartStyle<NumericFieldKeys<DataFields<T>> & string, FieldKeys<DataFields<T>>>
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
    const seriesEntries: readonly (readonly [string, ScatterChartSeriesConfig | undefined])[] = Array.isArray(series)
        ? (series as string[]).map(key => [key, undefined] as const)
        : Object.entries(series) as [string, ScatterChartSeriesConfig | undefined][];

    return buildScatterChart(data_mapped, undefined, seriesEntries, style);
}

// ============================================================================
// Scatter Chart Multi (Multi-Series with Separate Arrays)
// ============================================================================

/**
 * Creates a Scatter chart component from multiple data arrays (one per series).
 *
 * @typeParam K - Union of series names (record keys)
 * @typeParam T - The array type containing data structs for each series
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
export function createScatterChartMulti<
    K extends string,
    T extends SubtypeExprOrValue<ArrayType<StructType>>
>(
    data: Record<K, T>,
    style: ScatterChartMultiStyle<
        NumericFieldKeys<DataFields<T>> & string,
        FieldKeys<DataFields<T>>,
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

    return buildScatterChart(data_mapped, dataSeries_mapped, seriesEntries, style, style.valueKey, style.pivotKey);
}

// ============================================================================
// Shared Chart Builder
// ============================================================================

function buildScatterChart(
    data_mapped: ExprType<ArrayType<DictType<typeof StringType, typeof LiteralValueType>>>,
    dataSeries_mapped: ExprType<typeof MultiSeriesDataType> | undefined,
    seriesEntries: readonly (readonly [string, ScatterChartSeriesConfig | undefined])[],
    style?: ScatterChartStyle<string, string> & { pivotKey?: string; valueKey?: string },
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
            stroke: none,
            strokeWidth: none,
            fill: config?.fill !== undefined ? some(config.fill) : none,
            fillOpacity: none,
            strokeDasharray: none,
            yAxisId: yAxisIdValue,
            pivotColors: pivotColorsValue,
            layerIndex: config?.layerIndex !== undefined ? some(config.layerIndex) : none,
        };
    });

    // Convert axis styles to types
    const xAxisExpr = axisStyleToType(style?.xAxis as ChartAxisStyle | undefined);
    const yAxisExpr = axisStyleToType(style?.yAxis as ChartAxisStyle | undefined);
    const yAxis2Expr = axisStyleToType(style?.yAxis2 as ChartAxisStyle | undefined);

    // Extract xDataKey and yDataKey from axis configs for the ScatterChartType
    const xDataKey = (style?.xAxis as ChartAxisStyle | undefined)?.dataKey;
    const yDataKey = (style?.yAxis as ChartAxisStyle | undefined)?.dataKey;

    // Convert other style properties
    const gridExpr = gridStyleToType(style?.grid);
    const tooltipExpr = tooltipStyleToType(style?.tooltip);
    const legendExpr = legendStyleToType(style?.legend);
    const marginExpr = marginStyleToType(style?.margin);

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

    return East.value(variant("ScatterChart", {
        data: data_mapped,
        dataSeries: dataSeries_mapped ? variant("some", dataSeries_mapped) : variant("none", null),
        valueKey: effectiveValueKey !== undefined ? variant("some", effectiveValueKey) : variant("none", null),
        pivotKey: effectivePivotKey !== undefined ? variant("some", effectivePivotKey) : variant("none", null),
        series: series_mapped,
        xAxis: xAxisExpr ? variant("some", xAxisExpr) : variant("none", null),
        yAxis: yAxisExpr ? variant("some", yAxisExpr) : variant("none", null),
        yAxis2: yAxis2Expr ? variant("some", yAxis2Expr) : variant("none", null),
        xDataKey: xDataKey !== undefined ? variant("some", xDataKey) : variant("none", null),
        yDataKey: yDataKey !== undefined ? variant("some", yDataKey) : variant("none", null),
        grid: gridExpr ? variant("some", gridExpr) : variant("none", null),
        tooltip: tooltipExpr ? variant("some", tooltipExpr) : variant("none", null),
        legend: legendExpr ? variant("some", legendExpr) : variant("none", null),
        margin: marginExpr ? variant("some", marginExpr) : variant("none", null),
        pointSize: style?.pointSize !== undefined ? variant("some", style.pointSize) : variant("none", null),
        referenceLines: referenceLinesExpr,
        referenceDots: referenceDotsExpr,
        referenceAreas: referenceAreasExpr,
    }), UIComponentType);
}
