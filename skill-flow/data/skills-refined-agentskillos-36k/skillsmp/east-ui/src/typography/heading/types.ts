/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StringType,
    StructType,
    VariantType,
    NullType,
} from "@elaraai/east";

import { TextAlignType, type TextAlignLiteral } from "../../style.js";

// ============================================================================
// Heading Size Type
// ============================================================================

/**
 * Heading size type for typography scaling.
 *
 * @property xs - Extra small heading
 * @property sm - Small heading
 * @property md - Medium heading
 * @property lg - Large heading
 * @property xl - Extra large heading
 * @property 2xl - 2x large heading
 * @property 3xl - 3x large heading
 * @property 4xl - 4x large heading
 * @property 5xl - 5x large heading
 * @property 6xl - 6x large heading
 */
export const HeadingSizeType = VariantType({
    xs: NullType,
    sm: NullType,
    md: NullType,
    lg: NullType,
    xl: NullType,
    "2xl": NullType,
    "3xl": NullType,
    "4xl": NullType,
    "5xl": NullType,
    "6xl": NullType,
});

export type HeadingSizeType = typeof HeadingSizeType;
export type HeadingSizeLiteral = "xs" | "sm" | "md" | "lg" | "xl" | "2xl" | "3xl" | "4xl" | "5xl" | "6xl";

// ============================================================================
// Heading As Type
// ============================================================================

/**
 * Heading semantic level type.
 *
 * @property h1 - Level 1 heading (most important)
 * @property h2 - Level 2 heading
 * @property h3 - Level 3 heading
 * @property h4 - Level 4 heading
 * @property h5 - Level 5 heading
 * @property h6 - Level 6 heading (least important)
 */
export const HeadingAsType = VariantType({
    h1: NullType,
    h2: NullType,
    h3: NullType,
    h4: NullType,
    h5: NullType,
    h6: NullType,
});

export type HeadingAsType = typeof HeadingAsType;
export type HeadingAsLiteral = "h1" | "h2" | "h3" | "h4" | "h5" | "h6";

// ============================================================================
// Heading Type
// ============================================================================

/**
 * The concrete East type for Heading component data.
 *
 * @property value - The heading text
 * @property size - Visual size of the heading
 * @property as - Semantic HTML element (h1-h6)
 * @property color - Text color
 * @property textAlign - Text alignment
 */
export const HeadingType = StructType({
    value: StringType,
    size: OptionType(HeadingSizeType),
    as: OptionType(HeadingAsType),
    color: OptionType(StringType),
    textAlign: OptionType(TextAlignType),
});

export type HeadingType = typeof HeadingType;

// ============================================================================
// Heading Style
// ============================================================================

/**
 * Style configuration for Heading components.
 */
export type HeadingStyle = {
    /** Visual size of the heading */
    size?: SubtypeExprOrValue<HeadingSizeType> | HeadingSizeLiteral;
    /** Semantic HTML element (h1-h6) */
    as?: SubtypeExprOrValue<HeadingAsType> | HeadingAsLiteral;
    /** Text color */
    color?: SubtypeExprOrValue<StringType>;
    /** Text alignment */
    textAlign?: SubtypeExprOrValue<TextAlignType> | TextAlignLiteral;
};
