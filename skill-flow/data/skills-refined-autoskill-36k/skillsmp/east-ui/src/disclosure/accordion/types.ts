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
    BooleanType,
    VariantType,
    ArrayType,
    StringType,
    FunctionType,
    variant,
} from "@elaraai/east";

// ============================================================================
// Accordion Variant Type
// ============================================================================

/**
 * Variant types for Accordion visual style.
 *
 * @remarks
 * - enclosed: Bordered accordion with distinct boundaries
 * - plain: No visible borders or background
 * - subtle: Light background styling
 *
 * @property enclosed - Bordered accordion with distinct boundaries
 * @property plain - No visible borders or background
 * @property subtle - Light background styling
 */
export const AccordionVariantType = VariantType({
    /** Bordered accordion with distinct boundaries */
    enclosed: NullType,
    /** No visible borders or background */
    plain: NullType,
    /** Light background styling */
    subtle: NullType,
});

/**
 * Type representing the AccordionVariant structure.
 */
export type AccordionVariantType = typeof AccordionVariantType;

/**
 * String literal type for accordion variant values.
 */
export type AccordionVariantLiteral = "enclosed" | "plain" | "subtle";

/**
 * Helper function to create accordion variant values.
 *
 * @param v - The variant string ("enclosed", "plain", or "subtle")
 * @returns An East expression representing the accordion variant
 */
export function AccordionVariant(v: AccordionVariantLiteral): ExprType<AccordionVariantType> {
    return East.value(variant(v, null), AccordionVariantType);
}

// ============================================================================
// Accordion Style Type
// ============================================================================

/**
 * Type for Accordion style properties.
 *
 * @property multiple - Whether multiple items can be open at once
 * @property collapsible - Whether all items can be collapsed
 * @property variant - Visual variant (enclosed, plain, subtle)
 * @property onValueChange - Callback triggered when expanded items change
 */
export const AccordionStyleType = StructType({
    multiple: OptionType(BooleanType),
    collapsible: OptionType(BooleanType),
    variant: OptionType(AccordionVariantType),
    onValueChange: OptionType(FunctionType([ArrayType(StringType)], NullType)),
});

/**
 * Type representing the AccordionStyle structure.
 */
export type AccordionStyleType = typeof AccordionStyleType;

// ============================================================================
// Accordion Item Style Type
// ============================================================================

/**
 * Type for Accordion item style properties.
 *
 * @property disabled - Whether this item is disabled
 */
export const AccordionItemStyleType = StructType({
    disabled: OptionType(BooleanType),
});

/**
 * Type representing the AccordionItemStyle structure.
 */
export type AccordionItemStyleType = typeof AccordionItemStyleType;

// ============================================================================
// Style Interfaces
// ============================================================================

/**
 * TypeScript interface for Accordion item options.
 *
 * @property disabled - Whether this item is disabled
 */
export interface AccordionItemStyle {
    /** Whether this item is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
}

/**
 * TypeScript interface for Accordion style options.
 *
 * @property multiple - Whether multiple items can be open at once
 * @property collapsible - Whether all items can be collapsed
 * @property variant - Visual variant (enclosed, plain, or subtle)
 * @property onValueChange - Callback triggered when expanded items change
 */
export interface AccordionStyle {
    /** Whether multiple items can be open at once */
    multiple?: SubtypeExprOrValue<BooleanType>;
    /** Whether all items can be collapsed */
    collapsible?: SubtypeExprOrValue<BooleanType>;
    /** Visual variant (enclosed, plain, or subtle) */
    variant?: SubtypeExprOrValue<AccordionVariantType> | AccordionVariantLiteral;
    /** Callback triggered when expanded items change (receives array of expanded item values) */
    onValueChange?: SubtypeExprOrValue<FunctionType<[ArrayType<StringType>], NullType>>;
}
