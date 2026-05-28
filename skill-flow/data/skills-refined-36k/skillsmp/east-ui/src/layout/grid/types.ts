/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    East,
    NullType,
    OptionType,
    StringType,
    StructType,
    variant,
    VariantType,
    type ExprType,
    type SubtypeExprOrValue,
} from "@elaraai/east";

import {
    AlignItemsType,
    JustifyContentType,
} from "../../style.js";
import type {
    AlignItemsLiteral,
    JustifyContentLiteral,
} from "../../style.js";
import { PaddingType } from "../style.js";

// ============================================================================
// Grid Auto Flow Type
// ============================================================================

/**
 * Grid auto flow variant type for controlling automatic item placement.
 *
 * @remarks
 * Create instances using the {@link GridAutoFlow} function.
 *
 * @property row - Place items row by row
 * @property column - Place items column by column
 * @property dense - Fill in holes in the grid with smaller items
 * @property row dense - Row flow with dense packing
 * @property column dense - Column flow with dense packing
 */
export const GridAutoFlowType = VariantType({
    row: NullType,
    column: NullType,
    dense: NullType,
    "row dense": NullType,
    "column dense": NullType,
});

/**
 * Type representing grid auto flow variant values.
 */
export type GridAutoFlowType = typeof GridAutoFlowType;

/**
 * String literal type for grid auto flow values.
 */
export type GridAutoFlowLiteral = "row" | "column" | "dense" | "row dense" | "column dense";

/**
 * Creates a grid auto flow variant expression.
 *
 * @param flow - The auto flow value
 * @returns An East expression representing the grid auto flow
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Grid, GridAutoFlow, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Grid.Root([
 *         Grid.Item(Text.Root("Cell 1")),
 *         Grid.Item(Text.Root("Cell 2")),
 *     ], {
 *         templateColumns: "repeat(2, 1fr)",
 *         autoFlow: GridAutoFlow("row"),
 *     });
 * });
 * ```
 */
export function GridAutoFlow(flow: "row" | "column" | "dense" | "row dense" | "column dense"): ExprType<GridAutoFlowType> {
    return East.value(variant(flow, null), GridAutoFlowType);
}

// ============================================================================
// Grid Style Type
// ============================================================================

/**
 * Grid style type containing all root-level style properties.
 *
 * @remarks
 * This struct defines the styling options for the Grid component.
 * All properties are optional and wrapped in {@link OptionType}.
 *
 * @property width - Width (Chakra UI size token or CSS value)
 * @property height - Height (Chakra UI size token or CSS value)
 * @property minHeight - Min height (Chakra UI size token or CSS value)
 * @property minWidth - Min width (Chakra UI size token or CSS value)
 * @property maxHeight - Max height (Chakra UI size token or CSS value)
 * @property maxWidth - Max width (Chakra UI size token or CSS value)
 * @property padding - Padding configuration
 * @property templateColumns - CSS grid-template-columns (e.g., "repeat(3, 1fr)")
 * @property templateRows - CSS grid-template-rows
 * @property templateAreas - CSS grid-template-areas
 * @property gap - Gap between grid items (Chakra spacing token)
 * @property columnGap - Gap between columns
 * @property rowGap - Gap between rows
 * @property justifyItems - Alignment of items along the inline (row) axis
 * @property alignItems - Alignment of items along the block (column) axis
 * @property justifyContent - Distribution of grid columns
 * @property alignContent - Distribution of grid rows
 * @property autoColumns - Size of implicitly-created columns
 * @property autoRows - Size of implicitly-created rows
 * @property autoFlow - How auto-placed items are inserted
 */
export const GridStyleType = StructType({
    width: OptionType(StringType),
    height: OptionType(StringType),
    minHeight: OptionType(StringType),
    minWidth: OptionType(StringType),
    maxHeight: OptionType(StringType),
    maxWidth: OptionType(StringType),
    padding: OptionType(PaddingType),
    templateColumns: OptionType(StringType),
    templateRows: OptionType(StringType),
    templateAreas: OptionType(StringType),
    gap: OptionType(StringType),
    columnGap: OptionType(StringType),
    rowGap: OptionType(StringType),
    justifyItems: OptionType(JustifyContentType),
    alignItems: OptionType(AlignItemsType),
    justifyContent: OptionType(JustifyContentType),
    alignContent: OptionType(AlignItemsType),
    autoColumns: OptionType(StringType),
    autoRows: OptionType(StringType),
    autoFlow: OptionType(GridAutoFlowType),
});

/**
 * Type representing grid style values.
 */
export type GridStyleType = typeof GridStyleType;

/**
 * TypeScript interface for Grid component style options.
 *
 * @remarks
 * Use this interface when calling the Grid.Root function. All properties
 * accept East expressions for dynamic styling.
 *
 * @property width - Width (Chakra UI size token or CSS value)
 * @property height - Height (Chakra UI size token or CSS value)
 * @property minHeight - Min height (Chakra UI size token or CSS value)
 * @property minWidth - Min width (Chakra UI size token or CSS value)
 * @property maxHeight - Max height (Chakra UI size token or CSS value)
 * @property maxWidth - Max width (Chakra UI size token or CSS value)
 * @property padding - Padding configuration - use Padding() helper or string
 * @property templateColumns - CSS grid-template-columns (e.g., "repeat(3, 1fr)")
 * @property templateRows - CSS grid-template-rows
 * @property templateAreas - CSS grid-template-areas
 * @property gap - Gap between grid items (Chakra spacing token)
 * @property columnGap - Gap between columns
 * @property rowGap - Gap between rows
 * @property justifyItems - Alignment of items along the inline (row) axis
 * @property alignItems - Alignment of items along the block (column) axis
 * @property justifyContent - Distribution of grid columns
 * @property alignContent - Distribution of grid rows
 * @property autoColumns - Size of implicitly-created columns
 * @property autoRows - Size of implicitly-created rows
 * @property autoFlow - How auto-placed items are inserted
 */
export interface GridStyle {
    /** Width (Chakra UI size token or CSS value) */
    width?: SubtypeExprOrValue<StringType>;
    /** Height (Chakra UI size token or CSS value) */
    height?: SubtypeExprOrValue<StringType>;
    /** Min height (Chakra UI size token or CSS value) */
    minHeight?: SubtypeExprOrValue<StringType>;
    /** Min width (Chakra UI size token or CSS value) */
    minWidth?: SubtypeExprOrValue<StringType>;
    /** Max height (Chakra UI size token or CSS value) */
    maxHeight?: SubtypeExprOrValue<StringType>;
    /** Max width (Chakra UI size token or CSS value) */
    maxWidth?: SubtypeExprOrValue<StringType>;
    /** Padding configuration - use Padding() helper or string */
    padding?: SubtypeExprOrValue<PaddingType> | string;
    /** CSS grid-template-columns (e.g., "repeat(3, 1fr)") */
    templateColumns?: SubtypeExprOrValue<StringType>;
    /** CSS grid-template-rows */
    templateRows?: SubtypeExprOrValue<StringType>;
    /** CSS grid-template-areas */
    templateAreas?: SubtypeExprOrValue<StringType>;
    /** Gap between grid items (Chakra spacing token) */
    gap?: SubtypeExprOrValue<StringType>;
    /** Gap between columns */
    columnGap?: SubtypeExprOrValue<StringType>;
    /** Gap between rows */
    rowGap?: SubtypeExprOrValue<StringType>;
    /** Alignment of items along the inline (row) axis */
    justifyItems?: SubtypeExprOrValue<JustifyContentType> | JustifyContentLiteral;
    /** Alignment of items along the block (column) axis */
    alignItems?: SubtypeExprOrValue<AlignItemsType> | AlignItemsLiteral;
    /** Distribution of grid columns */
    justifyContent?: SubtypeExprOrValue<JustifyContentType> | JustifyContentLiteral;
    /** Distribution of grid rows */
    alignContent?: SubtypeExprOrValue<AlignItemsType> | AlignItemsLiteral;
    /** Size of implicitly-created columns */
    autoColumns?: SubtypeExprOrValue<StringType>;
    /** Size of implicitly-created rows */
    autoRows?: SubtypeExprOrValue<StringType>;
    /** How auto-placed items are inserted */
    autoFlow?: SubtypeExprOrValue<GridAutoFlowType> | GridAutoFlowLiteral;
}
