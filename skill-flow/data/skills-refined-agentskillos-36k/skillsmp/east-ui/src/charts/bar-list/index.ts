/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    East,
    ArrayType,
    variant,
    type SubtypeExprOrValue,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    ChartSortType,
    simpleTickFormatToExpr,
} from "../types.js";
import {
    BarListItemType,
    type BarListStyle,
} from "./types.js";

// Re-export types
export {
    BarListItemType,
    BarListType,
    type BarListStyle,
} from "./types.js";

// ============================================================================
// Bar List Function
// ============================================================================

/**
 * Creates a Bar list component.
 *
 * @param data - Array of bar list items
 * @param style - Optional styling configuration
 * @returns An East expression representing the bar list component
 *
 * @remarks
 * Bar list is a Chakra-native chart for comparing categories.
 * Simpler than a full bar chart, ideal for leaderboards or rankings.
 *
 * @example
 * ```ts
 * import { East, none } from "@elaraai/east";
 * import { Chart, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Chart.BarList(
 *         [
 *             { name: "Chrome", value: 275, color: none },
 *             { name: "Safari", value: 200, color: none },
 *         ],
 *         { showValue: true }
 *     );
 * });
 * ```
 */
export function createBarList(
    data: SubtypeExprOrValue<ArrayType<typeof BarListItemType>>,
    style?: BarListStyle
): ExprType<UIComponentType> {

    const sortValue = style?.sort
        ? East.value({
            by: style.sort.by,
            direction: typeof style.sort.direction === "string"
                ? variant(style.sort.direction, null)
                : style.sort.direction,
        }, ChartSortType)
        : undefined;

    const valueFormatValue = style?.valueFormat
        ? (typeof style.valueFormat === "string"
            ? simpleTickFormatToExpr(style.valueFormat)
            : style.valueFormat)
        : undefined;

    return East.value(variant("BarList", {
        data: data,
        sort: sortValue ? variant("some", sortValue) : variant("none", null),
        showValue: style?.showValue !== undefined ? variant("some", style.showValue) : variant("none", null),
        showLabel: style?.showLabel !== undefined ? variant("some", style.showLabel) : variant("none", null),
        valueFormat: valueFormatValue ? variant("some", valueFormatValue) : variant("none", null),
        color: style?.color !== undefined ? variant("some", style.color) : variant("none", null),
    }), UIComponentType);
}
