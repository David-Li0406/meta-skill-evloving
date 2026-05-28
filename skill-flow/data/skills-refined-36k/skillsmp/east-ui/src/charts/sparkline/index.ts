/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    ArrayType,
    FloatType,
    variant,
    StringType,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    SparklineType,
    SparklineChartType,
    type SparklineStyle,
} from "./types.js";

// Re-export types
export {
    SparklineType,
    SparklineChartType,
    type SparklineChartLiteral,
    type SparklineStyle,
} from "./types.js";

// ============================================================================
// Sparkline Function
// ============================================================================

/**
 * Creates a Sparkline component with data and optional styling.
 *
 * @param data - Array of numeric values to plot
 * @param style - Optional styling configuration
 * @returns An East expression representing the sparkline component
 *
 * @remarks
 * Sparkline is a compact inline chart for showing trends in data.
 * It's commonly used in tables, dashboards, and alongside statistics
 * to show historical values or trends without taking much space.
 *
 * @example
 * ```ts
 * import { Sparkline } from "@elaraai/east-ui";
 *
 * // Simple line sparkline
 * const trend = Sparkline.Root([1.2, 2.4, 1.8, 3.1, 2.9, 4.2]);
 *
 * // Styled area sparkline
 * const chart = Sparkline.Root([10, 20, 15, 25, 18, 30], {
 *   type: "area",
 *   color: "blue.500",
 *   width: "120px",
 *   height: "40px",
 * });
 *
 * // Access the type
 * const type = Sparkline.Types.Sparkline;
 * ```
 */
function createSparkline(
    data: SubtypeExprOrValue<ArrayType<FloatType>>,
    style?: SparklineStyle
): ExprType<UIComponentType> {

    const typeValue = style?.type
        ? (typeof style.type === "string"
            ? East.value(variant(style.type, null), SparklineChartType)
            : style.type)
        : undefined;

    const toStringOption = (val: SubtypeExprOrValue<StringType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    return East.value(variant("Sparkline", {
        data: data,
        type: typeValue ? variant("some", typeValue) : variant("none", null),
        color: toStringOption(style?.color),
        height: toStringOption(style?.height),
        width: toStringOption(style?.width),
    }), UIComponentType);
}

/**
 * Sparkline component for compact inline trend visualization.
 *
 * @remarks
 * Use `Sparkline.Root(data, style)` to create a sparkline, or access
 * `Sparkline.Types.Sparkline` for the East type.
 *
 * @example
 * ```ts
 * import { Sparkline } from "@elaraai/east-ui";
 *
 * // Create a sparkline
 * const trend = Sparkline.Root([1, 2, 1.5, 3, 2.5], {
 *   type: "area",
 *   color: "teal.500",
 * });
 *
 * // Access the type
 * const sparklineType = Sparkline.Types.Sparkline;
 * ```
 */
export const Sparkline = {
    /**
     * Creates a Sparkline component with data and optional styling.
     *
     * @param data - Array of numeric values to plot
     * @param style - Optional styling configuration
     * @returns An East expression representing the sparkline component
     *
     * @remarks
     * Sparkline is a compact inline chart for showing trends in data.
     * It's commonly used in tables, dashboards, and alongside statistics
     * to show historical values or trends without taking much space.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Sparkline, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Sparkline.Root(
     *         [1.2, 2.4, 1.8, 3.1, 2.9, 4.2],
     *         { type: "area", color: "teal.500" }
     *     );
     * });
     * ```
     */
    Root: createSparkline,
    Types: {
        /**
         * The concrete East type for Sparkline component data.
         *
         * @remarks
         * Sparkline is a compact inline chart for showing trends.
         * It displays an array of numeric values as a small visualization.
         *
         * @property data - Array of numeric values to plot (ArrayType<FloatType>)
         * @property type - Chart type line or area (OptionType<SparklineChartType>)
         * @property color - Line/fill color (OptionType<StringType>)
         * @property height - Height of the sparkline (OptionType<StringType>)
         * @property width - Width of the sparkline (OptionType<StringType>)
         */
        Sparkline: SparklineType,
        /**
         * Variant type for Sparkline chart appearance.
         *
         * @remarks
         * Determines how the sparkline data is visualized.
         *
         * @property line - Line chart connecting data points
         * @property area - Filled area chart below the line
         */
        ChartType: SparklineChartType,
    },
} as const;
