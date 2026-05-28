/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    NullType,
    OptionType,
    StructType,
    StringType,
    VariantType,
} from "@elaraai/east";


import { ColorSchemeType, type ColorSchemeLiteral } from "../../style.js";

// Re-export Font Awesome types for convenience
export type { IconName, IconPrefix } from "@fortawesome/fontawesome-common-types";

// ============================================================================
// Icon Size Type
// ============================================================================

/**
 * Size options for Icon component.
 *
 * @remarks
 * Maps to Font Awesome size classes.
 *
 * @property xs - Extra small icon
 * @property sm - Small icon
 * @property md - Medium icon (default)
 * @property lg - Large icon
 * @property xl - Extra large icon
 * @property 2xl - 2x large icon
 */
export const IconSizeType = VariantType({
    /** Extra small icon */
    xs: NullType,
    /** Small icon */
    sm: NullType,
    /** Medium icon (default) */
    md: NullType,
    /** Large icon */
    lg: NullType,
    /** Extra large icon */
    xl: NullType,
    /** 2x large icon */
    "2xl": NullType,
});

/**
 * Type representing the IconSize structure.
 */
export type IconSizeType = typeof IconSizeType;

/**
 * String literal type for icon size values.
 */
export type IconSizeLiteral = "xs" | "sm" | "md" | "lg" | "xl" | "2xl";

// ============================================================================
// Icon Style Type (Font Awesome style/prefix)
// ============================================================================

/**
 * Font Awesome icon style/variant.
 *
 * @remarks
 * Determines which icon set to use.
 *
 * @property solid - Solid filled icons (fas)
 * @property regular - Regular outlined icons (far)
 * @property light - Light weight icons (fal) - requires FA Pro
 * @property thin - Thin weight icons (fat) - requires FA Pro
 * @property brands - Brand logos (fab)
 */
export const IconVariantType = VariantType({
    /** Solid filled icons (fas) */
    solid: NullType,
    /** Regular outlined icons (far) */
    regular: NullType,
    /** Light weight icons (fal) - requires FA Pro */
    light: NullType,
    /** Thin weight icons (fat) - requires FA Pro */
    thin: NullType,
    /** Brand logos (fab) */
    brands: NullType,
});

/**
 * Type representing the IconVariant structure.
 */
export type IconVariantType = typeof IconVariantType;

/**
 * String literal type for icon variant values.
 */
export type IconVariantLiteral = "solid" | "regular" | "light" | "thin" | "brands";

// ============================================================================
// Icon Style Type (component styling)
// ============================================================================

/**
 * Style type for the Icon component.
 *
 * @remarks
 * All properties are optional and wrapped in {@link OptionType}.
 *
 * @property size - Icon size (xs, sm, md, lg, xl, 2xl)
 * @property variant - Icon style/weight (solid, regular, light, thin, brands)
 * @property color - Icon color (CSS color or Chakra color token)
 * @property colorPalette - Color scheme for the icon
 */
export const IconStyleType = StructType({
    size: OptionType(IconSizeType),
    variant: OptionType(IconVariantType),
    color: OptionType(StringType),
    colorPalette: OptionType(ColorSchemeType),
});

/**
 * Type representing the IconStyle structure.
 */
export type IconStyleType = typeof IconStyleType;

/**
 * TypeScript interface for Icon style options.
 *
 * @property size - Icon size (xs, sm, md, lg, xl, 2xl)
 * @property variant - Icon style/weight (solid, regular, light, thin, brands)
 * @property color - Icon color (CSS color or Chakra color token)
 * @property colorPalette - Color scheme for the icon
 */
export interface IconStyle {
    /** Icon size (xs, sm, md, lg, xl, 2xl) */
    size?: SubtypeExprOrValue<IconSizeType> | IconSizeLiteral;
    /** Icon style/weight (solid, regular, light, thin, brands) */
    variant?: SubtypeExprOrValue<IconVariantType> | IconVariantLiteral;
    /** Icon color (CSS color or Chakra color token) */
    color?: SubtypeExprOrValue<StringType>;
    /** Color scheme for the icon */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
}

// ============================================================================
// Icon Type
// ============================================================================

/**
 * Type for Icon component data.
 *
 * @remarks
 * Icon displays a Font Awesome icon with optional styling.
 *
 * @property prefix - The Font Awesome prefix (e.g., "fas", "far", "fab")
 * @property name - The Font Awesome icon name (e.g., "user", "home", "chevron-right")
 * @property style - Optional styling configuration
 */
export const IconType = StructType({
    name: StringType,
    prefix: StringType,
    style: OptionType(IconStyleType),
});

/**
 * Type representing the Icon structure.
 */
export type IconType = typeof IconType;
