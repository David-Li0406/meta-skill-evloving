/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    VariantType,
    StringType,
    BooleanType,
    ArrayType,
    NullType,
    FunctionType,
} from "@elaraai/east";

// ============================================================================
// TreeView Variant Types
// ============================================================================

/**
 * TreeView variant type for visual styling.
 *
 * @remarks
 * Create instances using string literals or the variant function.
 *
 * @property subtle - Subtle background on hover/selection
 * @property solid - Solid background on hover/selection
 */
export const TreeViewVariantType = VariantType({
    subtle: NullType,
    solid: NullType,
});

/**
 * Type representing tree view variant values.
 */
export type TreeViewVariantType = typeof TreeViewVariantType;

/**
 * String literal type for tree view variant values.
 */
export type TreeViewVariantLiteral = "subtle" | "solid";

// ============================================================================
// TreeView Size Types
// ============================================================================

/**
 * TreeView size type for controlling node sizing.
 *
 * @remarks
 * TreeView uses its own size type (xs, sm, md) rather than the shared SizeType.
 *
 * @property xs - Extra small size
 * @property sm - Small size
 * @property md - Medium size (default)
 */
export const TreeViewSizeType = VariantType({
    xs: NullType,
    sm: NullType,
    md: NullType,
});

/**
 * Type representing tree view size values.
 */
export type TreeViewSizeType = typeof TreeViewSizeType;

/**
 * String literal type for tree view size values.
 */
export type TreeViewSizeLiteral = "xs" | "sm" | "md";

// ============================================================================
// TreeView Selection Mode
// ============================================================================

/**
 * TreeView selection mode type.
 *
 * @property single - Only one node can be selected at a time
 * @property multiple - Multiple nodes can be selected
 */
export const TreeViewSelectionModeType = VariantType({
    single: NullType,
    multiple: NullType,
});

/**
 * Type representing tree view selection mode values.
 */
export type TreeViewSelectionModeType = typeof TreeViewSelectionModeType;

/**
 * String literal type for tree view selection mode values.
 */
export type TreeViewSelectionModeLiteral = "single" | "multiple";

// ============================================================================
// TreeView Style Types
// ============================================================================

/**
 * Style type for the tree view root component.
 *
 * @remarks
 * All properties are optional and wrapped in {@link OptionType}.
 *
 * @property size - Tree view size (xs, sm, md)
 * @property variant - Visual variant (subtle or solid)
 * @property selectionMode - Selection behavior (single or multiple)
 * @property animateContent - Whether to animate expand/collapse
 * @property onExpandedChange - Callback for expanded nodes change
 * @property onSelectionChange - Callback for selected nodes change
 * @property onFocusChange - Callback for focused node change
 */
export const TreeViewStyleType = StructType({
    size: OptionType(TreeViewSizeType),
    variant: OptionType(TreeViewVariantType),
    selectionMode: OptionType(TreeViewSelectionModeType),
    animateContent: OptionType(BooleanType),
    onExpandedChange: OptionType(FunctionType([ArrayType(StringType)], NullType)),
    onSelectionChange: OptionType(FunctionType([ArrayType(StringType)], NullType)),
    onFocusChange: OptionType(FunctionType([OptionType(StringType)], NullType)),
});

/**
 * Type representing the tree view style structure.
 */
export type TreeViewStyleType = typeof TreeViewStyleType;

/**
 * TypeScript interface for tree view styling input.
 *
 * @remarks
 * Accepts both static values and East expressions.
 *
 * @property size - Tree view size (xs, sm, md)
 * @property variant - Visual variant (subtle or solid)
 * @property selectionMode - Selection behavior (single or multiple)
 * @property animateContent - Whether to animate expand/collapse
 * @property defaultExpandedValue - Initially expanded node values
 * @property defaultSelectedValue - Initially selected node values
 * @property label - Accessible label for the tree view
 * @property onExpandedChange - Callback for expanded nodes change
 * @property onSelectionChange - Callback for selected nodes change
 * @property onFocusChange - Callback for focused node change
 */
export interface TreeViewStyle {
    /** Tree view size (xs, sm, md) */
    size?: SubtypeExprOrValue<TreeViewSizeType> | TreeViewSizeLiteral;
    /** Visual variant (subtle or solid) */
    variant?: SubtypeExprOrValue<TreeViewVariantType> | TreeViewVariantLiteral;
    /** Selection behavior (single or multiple) */
    selectionMode?: SubtypeExprOrValue<TreeViewSelectionModeType> | TreeViewSelectionModeLiteral;
    /** Whether to animate expand/collapse */
    animateContent?: SubtypeExprOrValue<BooleanType>;
    /** Initially expanded node values */
    defaultExpandedValue?: SubtypeExprOrValue<ArrayType<typeof StringType>>;
    /** Initially selected node values */
    defaultSelectedValue?: SubtypeExprOrValue<ArrayType<typeof StringType>>;
    /** Accessible label for the tree view */
    label?: SubtypeExprOrValue<typeof StringType>;
    /** Callback for expanded nodes change */
    onExpandedChange?: SubtypeExprOrValue<FunctionType<[ArrayType<typeof StringType>], NullType>>;
    /** Callback for selected nodes change */
    onSelectionChange?: SubtypeExprOrValue<FunctionType<[ArrayType<typeof StringType>], NullType>>;
    /** Callback for focused node change */
    onFocusChange?: SubtypeExprOrValue<FunctionType<[OptionType<typeof StringType>], NullType>>;
}
