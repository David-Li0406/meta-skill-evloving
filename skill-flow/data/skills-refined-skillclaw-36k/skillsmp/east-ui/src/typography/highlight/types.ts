/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StringType,
    StructType,
    ArrayType,
} from "@elaraai/east";

// ============================================================================
// Highlight Type
// ============================================================================

/**
 * The concrete East type for Highlight component data.
 *
 * @property value - The text containing content to highlight
 * @property query - String or array of strings to highlight within the text
 * @property color - Background color for highlighted portions
 */
export const HighlightType = StructType({
    value: StringType,
    query: ArrayType(StringType),
    color: OptionType(StringType),
});

export type HighlightType = typeof HighlightType;

// ============================================================================
// Highlight Style
// ============================================================================

/**
 * Style configuration for Highlight components.
 */
export type HighlightStyle = {
    /** Background color for highlighted text */
    color?: SubtypeExprOrValue<StringType>;
};
