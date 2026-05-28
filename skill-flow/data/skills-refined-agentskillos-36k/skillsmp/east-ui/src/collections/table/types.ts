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
    NullType,
    IntegerType,
    FloatType,
    DateTimeType,
    ArrayType,
    FunctionType,
    EastTypeType,
    LiteralValueType,
} from "@elaraai/east";

import {
    ColorSchemeType,
    type ColorSchemeLiteral,
} from "../../style.js";

// ============================================================================
// Table Variant Types
// ============================================================================

/**
 * Table variant type for Chakra UI v3 table styling.
 *
 * @remarks
 * Create instances using the {@link TableVariant} function.
 *
 * @property line - Table with horizontal lines between rows
 * @property outline - Table with full border outline
 */
export const TableVariantType = VariantType({
    line: NullType,
    outline: NullType,
});

/**
 * Type representing table variant values.
 */
export type TableVariantType = typeof TableVariantType;

/**
 * String literal type for table variant values.
 */
export type TableVariantLiteral = "line" | "outline";

// ============================================================================
// Table Size Type
// ============================================================================

/**
 * Size options for Table component.
 *
 * @remarks
 * Chakra UI Table only supports sm, md, lg sizes (not xs).
 *
 * @property sm - Small table
 * @property md - Medium table (default)
 * @property lg - Large table
 */
export const TableSizeType = VariantType({
    /** Small table */
    sm: NullType,
    /** Medium table (default) */
    md: NullType,
    /** Large table */
    lg: NullType,
});

/**
 * Type representing the TableSize structure.
 */
export type TableSizeType = typeof TableSizeType;

/**
 * String literal type for table size values.
 */
export type TableSizeLiteral = "sm" | "md" | "lg";


// ============================================================================
// Primitive East Types (for type-safe column configuration)
// ============================================================================

/**
 * Union of primitive East types that can be directly rendered in table cells.
 *
 * @remarks
 * These types don't require a custom `value` function in column config
 * because they can be directly converted to LiteralValueType.
 */
export type PrimitiveEastType = BooleanType | IntegerType | FloatType | StringType | DateTimeType;

// ============================================================================
// Table Callback Event Types
// ============================================================================

/**
 * Event data for table row events.
 *
 * @property rowIndex - The row index (0-based)
 * @property columnKey - The column key
 * @property cellValue - The cell value as a LiteralValueType
 */
export const TableCellClickEventType = StructType({
    rowIndex: IntegerType,
    columnKey: StringType,
    cellValue: LiteralValueType,
});

export type TableCellClickEventType = typeof TableCellClickEventType;


/**
 * Event data for table row click.
 *
 * @property rowIndex - The row index (0-based)
 */
export const TableRowClickEventType = StructType({
    rowIndex: IntegerType,
});

export type TableRowClickEventType = typeof TableRowClickEventType;


/**
 * Event data for table row selection changes.
 *
 * @property rowIndex - The row index (0-based)
 * @property selected - Whether the row is selected
 * @property selectedRowsIndices - Array of selected row indices
 */
export const TableRowSelectionEventType = StructType({
    rowIndex: IntegerType,
    selected: BooleanType,
    selectedRowsIndices: ArrayType(IntegerType),
});

export type TableRowSelectionEventType = typeof TableRowSelectionEventType;

/**
 * Sort direction for table column.
 *
 * @property direction - Sort direction ("asc" or "desc")
 */
export const TableSortDirectionType = VariantType({
    asc: NullType,
    desc: NullType,
});

export type TableSortDirectionType = typeof TableSortDirectionType;


/**
 * Event data for table sort changes.
 *
 * @property columnKey - The column key being sorted
 * @property sortIndex - The sort index (for multi-column sorting)
 * @property sortDirection - The sort direction ("asc" or "desc")
 */
export const TableSortEventType = StructType({
    columnKey: StringType,
    sortIndex: IntegerType,
    sortDirection: TableSortDirectionType,
});

export type TableSortEventType = typeof TableSortEventType;

/**
 * Style type for the table root component.
 *
 * @remarks All properties are optional and wrapped in {@link OptionType}.
 * 
 * @property variant - Table variant (line or outline)
 * @property size - Table size (sm, md, lg)
 * @property striped - Whether to show zebra stripes on rows
 * @property interactive - Whether to highlight rows on hover
 * @property stickyHeader - Whether the header sticks when scrolling
 * @property showColumnBorder - Whether to show borders between columns
 * @property colorPalette - Color scheme for interactive hover
 * @property onCellClick - Callback triggered when a cell is clicked
 * @property onCellDoubleClick - Callback triggered when a cell is double-clicked
 * @property onRowClick - Callback triggered when a row is clicked
 * @property onRowDoubleClick - Callback triggered when a row is double-clicked
 * @property onSelectionChange - Callback triggered when row selection changes
 * @property onSortChange - Callback triggered when sort column/direction changes
 */
export const TableStyleType = StructType({
    variant: OptionType(TableVariantType),
    size: OptionType(TableSizeType),
    striped: OptionType(BooleanType),
    interactive: OptionType(BooleanType),
    stickyHeader: OptionType(BooleanType),
    showColumnBorder: OptionType(BooleanType),
    colorPalette: OptionType(ColorSchemeType),
    onCellClick: OptionType(FunctionType([TableCellClickEventType], NullType)),
    onCellDoubleClick: OptionType(FunctionType([TableCellClickEventType], NullType)),
    onRowClick: OptionType(FunctionType([TableRowClickEventType], NullType)),
    onRowDoubleClick: OptionType(FunctionType([TableRowClickEventType], NullType)),
    onRowSelectionChange: OptionType(FunctionType([TableRowSelectionEventType], NullType)),
    onSortChange: OptionType(FunctionType([TableSortEventType], NullType)),
});

/**
 * Type representing the table style structure.
 */
export type TableStyleType = typeof TableStyleType;

/**
 * TypeScript interface for table root styling input.
 *
 * @remarks
 * Accepts both static values and East expressions.
 *
 * @property variant - Table variant (line or outline)
 * @property size - Table size (sm, md, lg)
 * @property striped - Whether to show zebra stripes on rows
 * @property interactive - Whether to highlight rows on hover
 * @property stickyHeader - Whether the header sticks when scrolling
 * @property showColumnBorder - Whether to show borders between columns
 * @property colorPalette - Color scheme for interactive hover
 * @property onCellClick - Callback triggered when a cell is clicked
 * @property onCellDoubleClick - Callback triggered when a cell is double-clicked
 * @property onRowClick - Callback triggered when a row is clicked
 * @property onRowDoubleClick - Callback triggered when a row is double-clicked
 * @property onSelectionChange - Callback triggered when row selection changes
 * @property onSortChange - Callback triggered when sort column/direction changes
 */
export interface TableStyle {
    /** Table variant (line or outline) */
    variant?: SubtypeExprOrValue<TableVariantType> | TableVariantLiteral;
    /** Table size (sm, md, lg) */
    size?: SubtypeExprOrValue<TableSizeType> | TableSizeLiteral;
    /** Whether to show zebra stripes on rows */
    striped?: SubtypeExprOrValue<BooleanType>;
    /** Whether to highlight rows on hover */
    interactive?: SubtypeExprOrValue<BooleanType>;
    /** Whether the header sticks when scrolling */
    stickyHeader?: SubtypeExprOrValue<BooleanType>;
    /** Whether to show borders between columns */
    showColumnBorder?: SubtypeExprOrValue<BooleanType>;
    /** Color scheme for interactive hover */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Callback triggered when a cell is clicked */
    onCellClick?: SubtypeExprOrValue<FunctionType<[TableCellClickEventType], NullType>>;
    /** Callback triggered when a cell is double-clicked */
    onCellDoubleClick?: SubtypeExprOrValue<FunctionType<[TableCellClickEventType], NullType>>;
    /** Callback triggered when a row is clicked */
    onRowClick?: SubtypeExprOrValue<FunctionType<[TableRowClickEventType], NullType>>;
    /** Callback triggered when a row is double-clicked */
    onRowDoubleClick?: SubtypeExprOrValue<FunctionType<[TableRowClickEventType], NullType>>;
    /** Callback triggered when row selection changes */
    onRowSelectionChange?: SubtypeExprOrValue<FunctionType<[TableRowSelectionEventType], NullType>>;
    /** Callback triggered when sort column/direction changes */
    onSortChange?: SubtypeExprOrValue<FunctionType<[TableSortEventType], NullType>>;
}

// ============================================================================
// Table Column Type (for serialization)
// ============================================================================

/**
 * East type for a table column definition.
 *
 * @remarks
 * Defines the header text and key for a column.
 *
 * @property key - The column key (field name)
 * @property type - The column value type as an EastTypeValue (supports any East type)
 * @property header - Optional header text for the column
 * @property width - Optional fixed width (CSS value, e.g., "200px", "20%")
 * @property minWidth - Optional minimum width (CSS value)
 * @property maxWidth - Optional maximum width (CSS value)
 */
export const TableColumnType = StructType({
    key: StringType,
    dataType: EastTypeType,
    valueType: EastTypeType,
    header: OptionType(StringType),
    width: OptionType(StringType),
    minWidth: OptionType(StringType),
    maxWidth: OptionType(StringType),
});

/**
 * Type representing the table column structure.
 */
export type TableColumnType = typeof TableColumnType;
