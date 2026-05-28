/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    NullType,
    OptionType,
    StructType,
    StringType,
    VariantType,
    variant,
} from "@elaraai/east";

import { SizeType, OverflowType } from "../../style.js";
import type { SizeLiteral, OverflowLiteral } from "../../style.js";

// ============================================================================
// Card Variant Type
// ============================================================================

/**
 * Variant types for Card visual style.
 *
 * @property elevated - Card with shadow/elevation
 * @property outline - Card with border outline
 * @property subtle - Card with subtle background
 */
export const CardVariantType = VariantType({
    /** Card with shadow/elevation */
    elevated: NullType,
    /** Card with border outline */
    outline: NullType,
    /** Card with subtle background */
    subtle: NullType,
});

/**
 * Type representing the CardVariant structure.
 */
export type CardVariantType = typeof CardVariantType;

/**
 * String literal type for card variant values.
 */
export type CardVariantLiteral = "elevated" | "outline" | "subtle";

/**
 * Helper function to create card variant values.
 *
 * @param v - The variant string ("elevated", "outline", "subtle")
 * @returns An East expression representing the card variant
 */
export function CardVariant(v: "elevated" | "outline" | "subtle"): ExprType<CardVariantType> {
    return East.value(variant(v, null), CardVariantType);
}

// ============================================================================
// Card Style Type
// ============================================================================

/**
 * Type for Card style properties.
 *
 * @property variant - Visual variant (elevated, outline, subtle)
 * @property size - Size of the card
 * @property height - Height (Chakra UI size token or CSS value)
 * @property minHeight - Min height (Chakra UI size token or CSS value)
 * @property maxHeight - Max height (Chakra UI size token or CSS value)
 * @property width - Width (Chakra UI size token or CSS value)
 * @property minWidth - Min width (Chakra UI size token or CSS value)
 * @property maxWidth - Max width (Chakra UI size token or CSS value)
 * @property flex - Flex property for grow/shrink behavior
 * @property overflow - Overflow behavior (visible, hidden, scroll, auto)
 */
export const CardStyleType = StructType({
    variant: OptionType(CardVariantType),
    size: OptionType(SizeType),
    height: OptionType(StringType),
    minHeight: OptionType(StringType),
    maxHeight: OptionType(StringType),
    width: OptionType(StringType),
    minWidth: OptionType(StringType),
    maxWidth: OptionType(StringType),
    flex: OptionType(StringType),
    overflow: OptionType(OverflowType),
});

/**
 * Type representing the CardStyle structure.
 */
export type CardStyleType = typeof CardStyleType;

// ============================================================================
// Card Style Interface
// ============================================================================

/**
 * TypeScript interface for Card style options.
 *
 * @property variant - Visual variant (elevated, outline, subtle)
 * @property size - Size of the card
 * @property height - Height (Chakra UI size token or CSS value)
 * @property minHeight - Min height (Chakra UI size token or CSS value)
 * @property maxHeight - Max height (Chakra UI size token or CSS value)
 * @property width - Width (Chakra UI size token or CSS value)
 * @property minWidth - Min width (Chakra UI size token or CSS value)
 * @property maxWidth - Max width (Chakra UI size token or CSS value)
 * @property flex - Flex property for grow/shrink behavior
 * @property overflow - Overflow behavior (visible, hidden, scroll, auto)
 */
export interface CardStyle {
    /** Visual variant (elevated, outline, subtle) */
    variant?: SubtypeExprOrValue<CardVariantType> | CardVariantLiteral;
    /** Size of the card */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Height (Chakra UI size token or CSS value) */
    height?: SubtypeExprOrValue<StringType>;
    /** Min height (Chakra UI size token or CSS value) */
    minHeight?: SubtypeExprOrValue<StringType>;
    /** Max height (Chakra UI size token or CSS value) */
    maxHeight?: SubtypeExprOrValue<StringType>;
    /** Width (Chakra UI size token or CSS value) */
    width?: SubtypeExprOrValue<StringType>;
    /** Min width (Chakra UI size token or CSS value) */
    minWidth?: SubtypeExprOrValue<StringType>;
    /** Max width (Chakra UI size token or CSS value) */
    maxWidth?: SubtypeExprOrValue<StringType>;
    /** Flex property for grow/shrink behavior (e.g., "1", "1 1 auto") */
    flex?: SubtypeExprOrValue<StringType>;
    /** Overflow behavior (visible, hidden, scroll, auto) */
    overflow?: SubtypeExprOrValue<OverflowType> | OverflowLiteral;
}
