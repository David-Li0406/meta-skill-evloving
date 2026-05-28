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

import { SizeType, type SizeLiteral } from "../../style.js";

// ============================================================================
// Code Variant Type
// ============================================================================

/**
 * Code variant type for different code display styles.
 *
 * @property subtle - Subtle background with colored text
 * @property surface - Surface-level styling
 * @property outline - Transparent background with colored border
 */
export const CodeVariantType = VariantType({
    subtle: NullType,
    surface: NullType,
    outline: NullType,
});

export type CodeVariantType = typeof CodeVariantType;
export type CodeVariantLiteral = "subtle" | "surface" | "outline";

// ============================================================================
// Code Type
// ============================================================================

/**
 * The concrete East type for Code component data.
 *
 * @property value - The code text to display
 * @property variant - Visual style variant
 * @property colorPalette - Color scheme for the code
 * @property size - Size of the code text
 */
export const CodeType = StructType({
    value: StringType,
    variant: OptionType(CodeVariantType),
    colorPalette: OptionType(StringType),
    size: OptionType(SizeType),
});

export type CodeType = typeof CodeType;

// ============================================================================
// Code Style
// ============================================================================

/**
 * Style configuration for Code components.
 */
export type CodeStyle = {
    /** Visual style variant */
    variant?: SubtypeExprOrValue<CodeVariantType> | CodeVariantLiteral;
    /** Color palette (e.g., "gray", "blue") */
    colorPalette?: SubtypeExprOrValue<StringType>;
    /** Size of the code text */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
};
