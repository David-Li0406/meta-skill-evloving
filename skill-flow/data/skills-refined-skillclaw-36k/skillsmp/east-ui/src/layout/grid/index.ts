/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    OptionType,
    StructType,
    ArrayType,
    variant,
    StringType,
    some,
    none,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    GridAutoFlowType,
    GridStyleType,
    type GridStyle,
} from "./types.js";
import {
    JustifyContentType,
    AlignItemsType,
} from "../../style.js";
import { Padding, PaddingType } from "../style.js";


// Re-export style types
export {
    GridStyleType,
    GridAutoFlowType,
    type GridStyle,
} from "./types.js";
export { GridAutoFlow } from "./types.js";

// ============================================================================
// Grid Item Type
// ============================================================================

/**
 * The concrete East type for Grid item data.
 *
 * @remarks
 * This struct type represents a single item within a Grid.
 * Each item has content (a UI component) and optional placement properties.
 *
 * @property content - The UI component to render in this grid cell
 * @property colSpan - Number of columns the item spans
 * @property rowSpan - Number of rows the item spans
 * @property colStart - Starting column line
 * @property colEnd - Ending column line
 * @property rowStart - Starting row line
 * @property rowEnd - Ending row line
 */
export const GridItemType: StructType<{
    content: UIComponentType,
    colSpan: OptionType<StringType>,
    rowSpan: OptionType<StringType>,
    colStart: OptionType<StringType>,
    colEnd: OptionType<StringType>,
    rowStart: OptionType<StringType>,
    rowEnd: OptionType<StringType>,
}> = StructType({
    content: UIComponentType,
    colSpan: OptionType(StringType),
    rowSpan: OptionType(StringType),
    colStart: OptionType(StringType),
    colEnd: OptionType(StringType),
    rowStart: OptionType(StringType),
    rowEnd: OptionType(StringType),
});

export interface GridItemStyle {
    colSpan?: SubtypeExprOrValue<StringType>;
    rowSpan?: SubtypeExprOrValue<StringType>;
    colStart?: SubtypeExprOrValue<StringType>;
    colEnd?: SubtypeExprOrValue<StringType>;
    rowStart?: SubtypeExprOrValue<StringType>;
    rowEnd?: SubtypeExprOrValue<StringType>;
}

/**
 * Type representing the Grid item structure.
 */
export type GridItemType = typeof GridItemType;

export function GridItem(
    content: SubtypeExprOrValue<UIComponentType>,
    style?: GridItemStyle
): ExprType<GridItemType> {
    const content_expr = East.value(content, UIComponentType);
    return East.value({
        content: content_expr,
        colSpan: style?.colSpan ? some(style.colSpan) : none,
        rowSpan: style?.rowSpan ? some(style.rowSpan) : none,
        colStart: style?.colStart ? some(style.colStart) : none,
        colEnd: style?.colEnd ? some(style.colEnd) : none,
        rowStart: style?.rowStart ? some(style.rowStart) : none,
        rowEnd: style?.rowEnd ? some(style.rowEnd) : none,
    }, GridItemType);
}

// ============================================================================
// Grid Root Function
// ============================================================================

/**
 * Creates a Grid container component with items and optional styling.
 *
 * @param items - Array of grid items created with Grid.Item
 * @param style - Optional styling configuration for the grid
 * @returns An East expression representing the styled grid component
 *
 * @remarks
 * Grid is a powerful layout component that uses CSS Grid for two-dimensional
 * layouts. It supports template definitions, gap configuration, alignment,
 * and automatic item placement.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Grid, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Grid.Root([
 *         Grid.Item(Text.Root("Cell 1")),
 *         Grid.Item(Text.Root("Cell 2")),
 *         Grid.Item(Text.Root("Cell 3")),
 *     ], {
 *         templateColumns: "repeat(3, 1fr)",
 *         gap: "4",
 *     });
 * });
 * ```
 */
function GridRoot(
    items: SubtypeExprOrValue<ArrayType<GridItemType>>,
    style?: GridStyle
): ExprType<UIComponentType> {
    const items_expr = East.value(items, ArrayType(GridItemType));
    const toStringOption = (value: SubtypeExprOrValue<StringType> | undefined) => {
        if (value === undefined) return variant("none", null);
        return variant("some", value);
    };

    const paddingValue = style?.padding
        ? (typeof style.padding === "string"
            ? East.value({
                top: some(style.padding),
                right: some(style.padding),
                bottom: some(style.padding),
                left: some(style.padding)
            }, PaddingType)
            : style.padding)
        : undefined;

    const justifyItemsValue = style?.justifyItems
        ? (typeof style.justifyItems === "string"
            ? East.value(variant(style.justifyItems, null), JustifyContentType)
            : style.justifyItems)
        : undefined;

    const alignItemsValue = style?.alignItems
        ? (typeof style.alignItems === "string"
            ? East.value(variant(style.alignItems, null), AlignItemsType)
            : style.alignItems)
        : undefined;

    const justifyContentValue = style?.justifyContent
        ? (typeof style.justifyContent === "string"
            ? East.value(variant(style.justifyContent, null), JustifyContentType)
            : style.justifyContent)
        : undefined;

    const alignContentValue = style?.alignContent
        ? (typeof style.alignContent === "string"
            ? East.value(variant(style.alignContent, null), AlignItemsType)
            : style.alignContent)
        : undefined;

    const autoFlowValue = style?.autoFlow
        ? (typeof style.autoFlow === "string"
            ? East.value(variant(style.autoFlow, null), GridAutoFlowType)
            : style.autoFlow)
        : undefined;
    return East.value(variant("Grid", {
        items: items_expr,
        style: style ?
            variant("some", {
                width: toStringOption(style.width),
                height: toStringOption(style.height),
                minHeight: toStringOption(style.minHeight),
                minWidth: toStringOption(style.minWidth),
                maxHeight: toStringOption(style.maxHeight),
                maxWidth: toStringOption(style.maxWidth),
                padding: paddingValue ? variant("some", paddingValue) : variant("none", null),
                templateColumns: toStringOption(style.templateColumns),
                templateRows: toStringOption(style.templateRows),
                templateAreas: toStringOption(style.templateAreas),
                gap: toStringOption(style.gap),
                columnGap: toStringOption(style.columnGap),
                rowGap: toStringOption(style.rowGap),
                justifyItems: justifyItemsValue ? variant("some", justifyItemsValue) : variant("none", null),
                alignItems: alignItemsValue ? variant("some", alignItemsValue) : variant("none", null),
                justifyContent: justifyContentValue ? variant("some", justifyContentValue) : variant("none", null),
                alignContent: alignContentValue ? variant("some", alignContentValue) : variant("none", null),
                autoColumns: toStringOption(style.autoColumns),
                autoRows: toStringOption(style.autoRows),
                autoFlow: autoFlowValue ? variant("some", autoFlowValue) : variant("none", null),
            }) :
            variant("none", null),
    }), UIComponentType);
}

export const GridType: StructType<{
    items: ArrayType<GridItemType>,
    style: OptionType<GridStyleType>,
}> = StructType({
    items: ArrayType(GridItemType),
    style: OptionType(GridStyleType),
})

// ============================================================================
// Grid Namespace Export
// ============================================================================

/**
 * Grid compound component for CSS Grid layouts.
 *
 * @remarks
 * Grid provides a two-dimensional layout system using CSS Grid.
 * Use `Grid.Root(items, style)` to create the container and `Grid.Item(content, style)` for each cell.
 */
export const Grid = {
    /**
     * Creates a Grid container component with items and optional styling.
     *
     * @param items - Array of grid items created with Grid.Item
     * @param style - Optional styling configuration for the grid
     * @returns An East expression representing the styled grid component
     *
     * @remarks
     * Grid is a powerful layout component that uses CSS Grid for two-dimensional
     * layouts. It supports template definitions, gap configuration, alignment,
     * and automatic item placement.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Grid, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Grid.Root([
     *         Grid.Item(Text.Root("Cell 1")),
     *         Grid.Item(Text.Root("Cell 2")),
     *         Grid.Item(Text.Root("Cell 3")),
     *     ], {
     *         templateColumns: "repeat(3, 1fr)",
     *         gap: "4",
     *     });
     * });
     * ```
     */
    Root: GridRoot,
    /**
     * Creates a Grid item with content and optional placement configuration.
     *
     * @param content - The UI component to render in this grid cell
     * @param style - Optional placement properties (colSpan, rowSpan, etc.)
     * @returns An East expression representing the grid item
     *
     * @remarks
     * Grid items can span multiple columns or rows and can be positioned explicitly
     * using colStart/colEnd and rowStart/rowEnd properties.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Grid, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Grid.Root([
     *         Grid.Item(Text.Root("Header"), { colSpan: 2n }),
     *         Grid.Item(Text.Root("Sidebar")),
     *         Grid.Item(Text.Root("Content")),
     *     ], {
     *         templateColumns: "repeat(2, 1fr)",
     *         gap: "4",
     *     });
     * });
     * ```
     */
    Item: GridItem,
    /**
     * Creates padding configuration for the Grid component.
     *
     * @param top - Top padding (Chakra UI spacing token or CSS value)
     * @param right - Right padding (Chakra UI spacing token or CSS value)
     * @param bottom - Bottom padding (Chakra UI spacing token or CSS value)
     * @param left - Left padding (Chakra UI spacing token or CSS value)
     * @returns An East expression representing the padding configuration
     *
     * @example
     * ```ts
     * Grid.Root([...], {
     *     padding: Grid.Padding("4", "2", "4", "2"),
     * });
     * ```
     */
    Padding,
    Types: {
        /**
         * The concrete East type for Grid component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Grid component.
         * Grid provides a two-dimensional layout system using CSS Grid.
         *
         * @property items - Array of grid items
         * @property style - Optional styling configuration wrapped in OptionType
         */
        Grid: GridType,
        /**
         * The concrete East type for Grid item data.
         *
         * @remarks
         * This struct type represents a single item within a Grid.
         * Each item has content (a UI component) and optional placement properties.
         *
         * @property content - The UI component to render in this grid cell
         * @property colSpan - Number of columns the item spans
         * @property rowSpan - Number of rows the item spans
         * @property colStart - Starting column line
         * @property colEnd - Ending column line
         * @property rowStart - Starting row line
         * @property rowEnd - Ending row line
         */
        Item: GridItemType,
        /**
         * Grid style type containing all root-level style properties.
         *
         * @remarks
         * This struct defines the styling options for the Grid component.
         * All properties are optional and wrapped in {@link OptionType}.
         *
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
        Style: GridStyleType,
    },
} as const;
