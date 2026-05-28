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
    StringType,
    FunctionType,
    variant,
} from "@elaraai/east";

import {
    ColorSchemeType,
    OrientationType,
    type ColorSchemeLiteral,
    type OrientationLiteral,
} from "../../style.js";

// ============================================================================
// Tabs Variant Type
// ============================================================================

/**
 * Variant types for Tabs visual style.
 *
 * @remarks
 * - line: Tabs with an underline indicator
 * - subtle: Light background on selected tab
 * - enclosed: Tabs with bordered container
 * - outline: Outlined tabs
 * - plain: No visible styling
 *
 * @property line - Tabs with an underline indicator
 * @property subtle - Light background on selected tab
 * @property enclosed - Tabs with bordered container
 * @property outline - Outlined tabs
 * @property plain - No visible styling
 */
export const TabsVariantType = VariantType({
    /** Tabs with an underline indicator */
    line: NullType,
    /** Light background on selected tab */
    subtle: NullType,
    /** Tabs with bordered container */
    enclosed: NullType,
    /** Outlined tabs */
    outline: NullType,
    /** No visible styling */
    plain: NullType,
});

/**
 * Type representing the TabsVariant structure.
 */
export type TabsVariantType = typeof TabsVariantType;

/**
 * String literal type for tabs variant values.
 */
export type TabsVariantLiteral = "line" | "subtle" | "enclosed" | "outline" | "plain";

/**
 * Helper function to create tabs variant values.
 *
 * @param v - The variant string
 * @returns An East expression representing the tabs variant
 */
export function TabsVariant(v: TabsVariantLiteral): ExprType<TabsVariantType> {
    return East.value(variant(v, null), TabsVariantType);
}

// ============================================================================
// Tabs Justify Type
// ============================================================================

/**
 * Justify options for tab list alignment.
 *
 * @property start - Align tabs to the start
 * @property center - Center the tabs
 * @property end - Align tabs to the end
 */
export const TabsJustifyType = VariantType({
    /** Align tabs to the start */
    start: NullType,
    /** Center the tabs */
    center: NullType,
    /** Align tabs to the end */
    end: NullType,
});

/**
 * Type representing the TabsJustify structure.
 */
export type TabsJustifyType = typeof TabsJustifyType;

/**
 * String literal type for tabs justify values.
 */
export type TabsJustifyLiteral = "start" | "center" | "end";

// ============================================================================
// Tabs Activation Mode Type
// ============================================================================

/**
 * Activation mode for keyboard navigation.
 *
 * @property automatic - Tab activates on focus
 * @property manual - Tab requires explicit activation
 */
export const TabsActivationModeType = VariantType({
    /** Tab activates on focus */
    automatic: NullType,
    /** Tab requires explicit activation */
    manual: NullType,
});

/**
 * Type representing the TabsActivationMode structure.
 */
export type TabsActivationModeType = typeof TabsActivationModeType;

/**
 * String literal type for tabs activation mode values.
 */
export type TabsActivationModeLiteral = "automatic" | "manual";

// ============================================================================
// Tabs Size Type
// ============================================================================

/**
 * Size options for Tabs component.
 *
 * @remarks
 * Chakra UI Tabs only supports sm, md, lg sizes (not xs).
 *
 * @property sm - Small tabs
 * @property md - Medium tabs (default)
 * @property lg - Large tabs
 */
export const TabsSizeType = VariantType({
    /** Small tabs */
    sm: NullType,
    /** Medium tabs (default) */
    md: NullType,
    /** Large tabs */
    lg: NullType,
});

/**
 * Type representing the TabsSize structure.
 */
export type TabsSizeType = typeof TabsSizeType;

/**
 * String literal type for tabs size values.
 */
export type TabsSizeLiteral = "sm" | "md" | "lg";

// ============================================================================
// Tabs Style Type
// ============================================================================

/**
 * Type for Tabs style properties.
 *
 * @property variant - Visual variant (line, subtle, enclosed, outline, plain)
 * @property size - Size of the tabs (sm, md, lg)
 * @property orientation - Layout direction (horizontal, vertical)
 * @property activationMode - Keyboard navigation behavior
 * @property fitted - Whether tabs take equal width
 * @property justify - Tab list alignment
 * @property lazyMount - Mount content only when selected
 * @property unmountOnExit - Unmount when deselected
 * @property colorPalette - Color scheme for the tabs
 * @property onValueChange - Callback triggered when selected tab changes
 */
export const TabsStyleType = StructType({
    variant: OptionType(TabsVariantType),
    size: OptionType(TabsSizeType),
    orientation: OptionType(OrientationType),
    activationMode: OptionType(TabsActivationModeType),
    fitted: OptionType(BooleanType),
    justify: OptionType(TabsJustifyType),
    lazyMount: OptionType(BooleanType),
    unmountOnExit: OptionType(BooleanType),
    colorPalette: OptionType(ColorSchemeType),
    onValueChange: OptionType(FunctionType([StringType], NullType)),
});

/**
 * Type representing the TabsStyle structure.
 */
export type TabsStyleType = typeof TabsStyleType;

// ============================================================================
// Style Interfaces
// ============================================================================

/**
 * TypeScript interface for Tabs item options.
 *
 * @property disabled - Whether this tab is disabled
 */
export interface TabsItemStyle {
    /** Whether this tab is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
}

/**
 * TypeScript interface for Tabs style options.
 *
 * @property variant - Visual variant (line, subtle, enclosed, outline, plain)
 * @property size - Size of the tabs (sm, md, lg)
 * @property orientation - Layout direction (horizontal, vertical)
 * @property activationMode - Keyboard navigation behavior
 * @property fitted - Whether tabs take equal width
 * @property justify - Tab list alignment
 * @property lazyMount - Mount content only when selected
 * @property unmountOnExit - Unmount when deselected
 * @property colorPalette - Color scheme for the tabs
 * @property defaultValue - Initial selected tab value
 * @property value - Controlled selected tab value
 * @property onValueChange - Callback triggered when selected tab changes
 */
export interface TabsStyle {
    /** Visual variant (line, subtle, enclosed, outline, plain) */
    variant?: SubtypeExprOrValue<TabsVariantType> | TabsVariantLiteral;
    /** Size of the tabs (sm, md, lg) */
    size?: SubtypeExprOrValue<TabsSizeType> | TabsSizeLiteral;
    /** Layout direction (horizontal, vertical) */
    orientation?: SubtypeExprOrValue<OrientationType> | OrientationLiteral;
    /** Keyboard navigation behavior */
    activationMode?: SubtypeExprOrValue<TabsActivationModeType> | TabsActivationModeLiteral;
    /** Whether tabs take equal width */
    fitted?: SubtypeExprOrValue<BooleanType>;
    /** Tab list alignment */
    justify?: SubtypeExprOrValue<TabsJustifyType> | TabsJustifyLiteral;
    /** Mount content only when selected */
    lazyMount?: SubtypeExprOrValue<BooleanType>;
    /** Unmount when deselected */
    unmountOnExit?: SubtypeExprOrValue<BooleanType>;
    /** Color scheme for the tabs */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Initial selected tab value */
    defaultValue?: SubtypeExprOrValue<typeof import("@elaraai/east").StringType>;
    /** Controlled selected tab value */
    value?: SubtypeExprOrValue<typeof import("@elaraai/east").StringType>;
    /** Callback triggered when selected tab changes */
    onValueChange?: SubtypeExprOrValue<FunctionType<[typeof StringType], NullType>>;
}
