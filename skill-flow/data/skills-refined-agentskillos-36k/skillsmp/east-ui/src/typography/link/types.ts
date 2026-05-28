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
    BooleanType,
} from "@elaraai/east";

// ============================================================================
// Link Variant Type
// ============================================================================

/**
 * Link variant type for different link styles.
 *
 * @property underline - Always show underline
 * @property plain - No underline by default
 */
export const LinkVariantType = VariantType({
    underline: NullType,
    plain: NullType,
});

export type LinkVariantType = typeof LinkVariantType;
export type LinkVariantLiteral = "underline" | "plain";

// ============================================================================
// Link Type
// ============================================================================

/**
 * The concrete East type for Link component data.
 *
 * @property value - The link text to display
 * @property href - URL the link points to
 * @property external - Whether to open in new tab
 * @property variant - Visual style variant
 * @property colorPalette - Color scheme for the link
 */
export const LinkType = StructType({
    value: StringType,
    href: StringType,
    external: OptionType(BooleanType),
    variant: OptionType(LinkVariantType),
    colorPalette: OptionType(StringType),
});

export type LinkType = typeof LinkType;

// ============================================================================
// Link Style
// ============================================================================

/**
 * Style configuration for Link components.
 */
export type LinkStyle = {
    /** Whether to open in new tab */
    external?: SubtypeExprOrValue<BooleanType> | boolean;
    /** Visual style variant */
    variant?: SubtypeExprOrValue<LinkVariantType> | LinkVariantLiteral;
    /** Color palette (e.g., "blue", "teal") */
    colorPalette?: SubtypeExprOrValue<StringType>;
};
