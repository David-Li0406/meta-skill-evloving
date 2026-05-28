/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType, type SubtypeExprOrValue, type TypeOf, ArrayType, DictType, East, Expr, LiteralValueType, none, some, StringType, StructType, variant
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    gridStyleToType,
    tooltipStyleToType,
    legendStyleToType,
    marginStyleToType,
} from "../types.js";
import type { RadarChartStyle, RadarChartSeriesConfig } from "./types.js";

// Re-export types
export { RadarChartType, type RadarChartStyle, type RadarChartSeriesConfig } from "./types.js";

// ============================================================================
// Radar Chart Function
// ============================================================================

/**
 * Creates a Radar chart component.
 *
 * @param data - Array of data points
 * @param series - Series configuration keyed by field names from the data type
 * @param style - Optional styling configuration
 * @returns An East expression representing the radar chart component
 *
 * @remarks
 * Radar charts display multivariate data on radial axes.
 * Each axis represents a different variable.
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
export function createRadarChart<T extends SubtypeExprOrValue<ArrayType<StructType>>>(
    data: T,
    series: {
        [K in TypeOf<NoInfer<T>> extends ArrayType<StructType> ? keyof TypeOf<NoInfer<T>>["value"]["fields"] : never]?: RadarChartSeriesConfig
    },
    style?: RadarChartStyle
): ExprType<UIComponentType> {
    const data_expr = East.value(data) as ExprType<ArrayType<StructType>>;
    const data_mapped = data_expr.map(($, datum) => {
        const ret = $.let(new Map(), DictType(StringType, LiteralValueType));
        for (const [field_name, field_type] of Object.entries(Expr.type(data_expr).value.fields)) {
            $(ret.insert(field_name, variant(field_type.type, datum[field_name] as any)));
        }
        return ret
    });
    const series_mapped = Object.entries(series as Record<string, RadarChartSeriesConfig>).map(([name, config]) => ({
        name: name as string,
        dataKey: some(name), // dataKey defaults to series name
        color: config?.color !== undefined ? some(config.color) : none,
        stackId: none,
        label: config?.label !== undefined ? some(config.label) : none,
        stroke: config?.stroke !== undefined ? some(config.stroke) : none,
        strokeWidth: config?.strokeWidth !== undefined ? some(config.strokeWidth) : none,
        fill: config?.fill !== undefined ? some(config.fill) : none,
        fillOpacity: config?.fillOpacity !== undefined ? some(config.fillOpacity) : none,
        strokeDasharray: config?.strokeDasharray !== undefined ? some(config.strokeDasharray) : none,
        yAxisId: none, // Radar charts don't use Y-axis, but ChartSeriesType requires this field
        pivotColors: none, // Radar charts don't support pivot mode, but ChartSeriesType requires this field
        layerIndex: config?.layerIndex !== undefined ? some(config.layerIndex) : none,
    }));

    // Convert style properties
    const gridExpr = gridStyleToType(style?.grid);
    const tooltipExpr = tooltipStyleToType(style?.tooltip);
    const legendExpr = legendStyleToType(style?.legend);
    const marginExpr = marginStyleToType(style?.margin);

    return East.value(variant("RadarChart", {
        data: data_mapped,
        series: series_mapped,
        dataKey: style?.dataKey !== undefined ? variant("some", style.dataKey) : variant("none", null),
        grid: gridExpr ? variant("some", gridExpr) : variant("none", null),
        tooltip: tooltipExpr ? variant("some", tooltipExpr) : variant("none", null),
        legend: legendExpr ? variant("some", legendExpr) : variant("none", null),
        margin: marginExpr ? variant("some", marginExpr) : variant("none", null),
        fillOpacity: style?.fillOpacity !== undefined ? variant("some", style.fillOpacity) : variant("none", null),
    }), UIComponentType);
}
