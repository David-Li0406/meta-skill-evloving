/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    ArrayType,
    StringType,
    FloatType,
    VariantType,
    NullType,
} from "@elaraai/east";

// ============================================================================
// Sparkline Chart Type
// ============================================================================

/**
 * Variant type for Sparkline chart appearance.
 *
 * @remarks
 * Determines how the sparkline data is visualized.
 *
 * @property line - Line chart connecting data points
 * @property area - Filled area chart below the line
 */
export const SparklineChartType = VariantType({
    line: NullType,
    area: NullType,
});

/**
 * Type representing sparkline chart variant values.
 */
export type SparklineChartType = typeof SparklineChartType;

/**
 * String literal type for sparkline chart values.
 */
export type SparklineChartLiteral = "line" | "area";

// ============================================================================
// Sparkline Type
// ============================================================================

/**
 * Type for Sparkline component data.
 *
 * @remarks
 * Sparkline is a compact inline chart for showing trends.
 * It displays an array of numeric values as a small visualization.
 *
 * @property data - Array of numeric values to plot
 * @property type - Chart type (line or area)
 * @property color - Line/fill color (Chakra color token or CSS color)
 * @property height - Height of the sparkline
 * @property width - Width of the sparkline
 */
export const SparklineType = StructType({
    data: ArrayType(FloatType),
    type: OptionType(SparklineChartType),
    color: OptionType(StringType),
    height: OptionType(StringType),
    width: OptionType(StringType),
});

/**
 * Type representing the Sparkline structure.
 */
export type SparklineType = typeof SparklineType;

// ============================================================================
// Sparkline Style
// ============================================================================

/**
 * TypeScript interface for Sparkline style options.
 *
 * @property type - Chart type (line or area)
 * @property color - Line/fill color (Chakra color token or CSS color)
 * @property height - Height of the sparkline
 * @property width - Width of the sparkline
 */
export interface SparklineStyle {
    /** Chart type (line or area) */
    type?: SubtypeExprOrValue<SparklineChartType> | SparklineChartLiteral;
    /** Line/fill color (Chakra color token or CSS color) */
    color?: SubtypeExprOrValue<StringType>;
    /** Height of the sparkline */
    height?: SubtypeExprOrValue<StringType>;
    /** Width of the sparkline */
    width?: SubtypeExprOrValue<StringType>;
}
