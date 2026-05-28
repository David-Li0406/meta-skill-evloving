/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    type ExprType,
    StringType,
    NullType,
    OptionType,
    StructType,
    VariantType,
    East,
    variant,
} from "@elaraai/east";

// ============================================================================
// Stat Indicator Type
// ============================================================================

/**
 * Indicator types for Stat component.
 *
 * @remarks
 * Used to show trend direction.
 *
 * @property up - Positive trend (usually green)
 * @property down - Negative trend (usually red)
 */
export const StatIndicatorType = VariantType({
    /** Positive/increasing trend */
    up: NullType,
    /** Negative/decreasing trend */
    down: NullType,
});

/**
 * Type representing the StatIndicator structure.
 */
export type StatIndicatorType = typeof StatIndicatorType;

/**
 * String literal type for stat indicator values.
 */
export type StatIndicatorLiteral = "up" | "down";

/**
 * Helper function to create stat indicator values.
 *
 * @param direction - The indicator direction ("up" or "down")
 * @returns An East expression representing the stat indicator
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Stat, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Stat.Root("Revenue", "$45,231", {
 *         helpText: "+20.1%",
 *         indicator: Stat.Indicator("up"),
 *     });
 * });
 * ```
 */
export function StatIndicator(direction: "up" | "down"): ExprType<StatIndicatorType> {
    return East.value(variant(direction, null), StatIndicatorType);
}

// ============================================================================
// Stat Type
// ============================================================================

/**
 * Type for Stat component data.
 *
 * @remarks
 * Stat displays a key metric with optional label, help text, and trend indicator.
 *
 * @property label - The stat label/title
 * @property value - The main stat value
 * @property helpText - Optional help text or trend description
 * @property indicator - Optional trend indicator (up/down)
 */
export const StatType = StructType({
    label: StringType,
    value: StringType,
    helpText: OptionType(StringType),
    indicator: OptionType(StatIndicatorType),
});

/**
 * Type representing the Stat structure.
 */
export type StatType = typeof StatType;

// ============================================================================
// Stat Style
// ============================================================================

/**
 * TypeScript interface for Stat style options.
 *
 * @property helpText - Optional help text or trend description
 * @property indicator - Optional trend indicator (up/down)
 */
export interface StatStyle {
    /** Optional help text or trend description */
    helpText?: SubtypeExprOrValue<StringType>;
    /** Optional trend indicator (up/down) */
    indicator?: SubtypeExprOrValue<StatIndicatorType> | StatIndicatorLiteral;
}
