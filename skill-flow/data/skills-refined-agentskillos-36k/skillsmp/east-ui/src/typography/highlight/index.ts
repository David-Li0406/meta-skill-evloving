/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    type ExprType,
    East,
    StringType,
    ArrayType,
    variant,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { HighlightType, type HighlightStyle } from "./types.js";

// Re-export types
export { HighlightType, type HighlightStyle } from "./types.js";

// ============================================================================
// Highlight Component
// ============================================================================

/**
 * Creates a Highlight component for highlighting text portions.
 *
 * @param value - The text containing content to highlight
 * @param query - String or array of strings to highlight
 * @param style - Optional styling configuration
 * @returns An East expression representing the highlight component
 */
function createHighlight(
    value: SubtypeExprOrValue<StringType>,
    query: SubtypeExprOrValue<ArrayType<StringType>> | string | string[],
    style?: HighlightStyle
): ExprType<UIComponentType> {
    // Normalize query to array
    const queryArray = typeof query === "string"
        ? [query]
        : Array.isArray(query)
            ? query
            : query;

    return East.value(variant("Highlight", {
        value: value,
        query: queryArray,
        color: style?.color ? variant("some", style.color) : variant("none", null),
    }), UIComponentType);
}

/**
 * Highlight component for highlighting portions of text.
 *
 * @remarks
 * Use `Highlight.Root(value, query, style)` to highlight matching text.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Highlight, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Highlight.Root(
 *         "Search results for: react components",
 *         ["react", "components"],
 *         { color: "yellow.200" }
 *     );
 * });
 * ```
 */
export const Highlight = {
    Root: createHighlight,
    Types: {
        Highlight: HighlightType,
    },
} as const;
