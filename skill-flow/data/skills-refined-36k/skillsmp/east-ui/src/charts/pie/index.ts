/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType, type SubtypeExprOrValue, ArrayType, East, variant
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    tooltipStyleToType,
    legendStyleToType,
    marginStyleToType,
} from "../types.js";
import { PieSliceType, type PieChartStyle } from "./types.js";

// Re-export types
export { PieSliceType, PieChartType, type PieChartStyle } from "./types.js";

// ============================================================================
// Pie Chart Function
// ============================================================================

/**
 * Creates a Pie chart component.
 *
 * @param data - Array of pie slices
 * @param style - Optional styling configuration
 * @returns An East expression representing the pie chart component
 *
 * @remarks
 * Set innerRadius > 0 to create a donut chart.
 *
 * @example
 * ```ts
 * import { East, some } from "@elaraai/east";
 * import { Chart, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Chart.Pie(
 *         [
 *             { name: "Chrome", value: 275, color: some("blue.solid") },
 *             { name: "Safari", value: 200, color: some("green.solid") },
 *         ],
 *         { showLabels: true }
 *     );
 * });
 * ```
 */
export function createPieChart(
    data: SubtypeExprOrValue<ArrayType<typeof PieSliceType>>,
    style?: PieChartStyle
): ExprType<UIComponentType> {
    // Convert style properties
    const tooltipExpr = tooltipStyleToType(style?.tooltip);
    const legendExpr = legendStyleToType(style?.legend);
    const marginExpr = marginStyleToType(style?.margin);

    return East.value(variant("PieChart", {
        data: data,
        innerRadius: style?.innerRadius !== undefined ? variant("some", style.innerRadius) : variant("none", null),
        outerRadius: style?.outerRadius !== undefined ? variant("some", style.outerRadius) : variant("none", null),
        startAngle: style?.startAngle !== undefined ? variant("some", style.startAngle) : variant("none", null),
        endAngle: style?.endAngle !== undefined ? variant("some", style.endAngle) : variant("none", null),
        paddingAngle: style?.paddingAngle !== undefined ? variant("some", style.paddingAngle) : variant("none", null),
        showLabels: style?.showLabels !== undefined ? variant("some", style.showLabels) : variant("none", null),
        tooltip: tooltipExpr ? variant("some", tooltipExpr) : variant("none", null),
        legend: legendExpr ? variant("some", legendExpr) : variant("none", null),
        margin: marginExpr ? variant("some", marginExpr) : variant("none", null),
    }), UIComponentType);
}
