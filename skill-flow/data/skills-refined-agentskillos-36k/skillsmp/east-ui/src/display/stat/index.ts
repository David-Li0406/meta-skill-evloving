/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType,
    variant,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { StatType, StatIndicatorType, StatIndicator, type StatStyle } from "./types.js";

// Re-export types (only TypeScript interfaces, not East types - those go through Stat.Types)
export { type StatStyle, type StatIndicatorLiteral } from "./types.js";

// ============================================================================
// Stat Function
// ============================================================================

/**
 * Creates a Stat component with label, value, and optional trend info.
 *
 * @param label - The stat label/title
 * @param value - The main stat value
 * @param style - Optional styling configuration
 * @returns An East expression representing the stat component
 *
 * @remarks
 * Stat is used to display key metrics or KPIs with optional trend indicators
 * and help text describing changes.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Stat, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Stat.Root("Growth", "+23.36%", {
 *         helpText: "From last week",
 *         indicator: "up",
 *     });
 * });
 * ```
 */
function createStat(
    label: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<StringType>,
    style?: StatStyle
): ExprType<UIComponentType> {
    const toStringOption = (val: SubtypeExprOrValue<StringType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const indicatorValue = style?.indicator
        ? (typeof style.indicator === "string"
            ? East.value(variant(style.indicator, null), StatIndicatorType)
            : style.indicator)
        : undefined;

    return East.value(variant("Stat", {
        label: label,
        value: value,
        helpText: toStringOption(style?.helpText),
        indicator: indicatorValue ? variant("some", indicatorValue) : variant("none", null),
    }), UIComponentType);
}

/**
 * Stat component for displaying key metrics.
 *
 * @remarks
 * Use `Stat.Root(label, value, style)` to create a stat, or access `Stat.Types.Stat` for the East type.
 */
export const Stat = {
    /**
     * Creates a Stat component with label, value, and optional trend info.
     *
     * @param label - The stat label/title
     * @param value - The main stat value
     * @param style - Optional styling configuration
     * @returns An East expression representing the stat component
     *
     * @remarks
     * Stat is used to display key metrics or KPIs with optional trend indicators
     * and help text describing changes.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Stat, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Stat.Root("Growth", "+23.36%", {
     *         helpText: "From last week",
     *         indicator: "up",
     *     });
     * });
     * ```
     */
    Root: createStat,
    /**
     * Helper function to create stat indicator values.
     *
     * @param direction - The indicator direction ("up" or "down")
     * @returns An East expression representing the stat indicator
     *
     * @remarks
     * Use this helper to create indicator values programmatically. In most cases,
     * you can pass string literals directly to the style property.
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
    Indicator: StatIndicator,
    Types: {
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
        Stat: StatType,
        /**
         * Indicator types for Stat component.
         *
         * @remarks
         * Used to show trend direction.
         *
         * @property up - Positive trend (usually green)
         * @property down - Negative trend (usually red)
         */
        Indicator: StatIndicatorType,
    },
} as const;
