/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    Expr,
    StructType,
    ArrayType,
    DictType,
    StringType, OptionType,
    variant,
    type TypeOf,
    some,
    none,
    type ValueTypeOf,
    FunctionType,
    NullType,
    toEastTypeValue,
    type EastType,
    type EastTypeValue,
    LiteralValueType,
    BooleanType,
    IntegerType,
    FloatType,
    DateTimeType,
    BlobType,
    isTypeValueEqual,
} from "@elaraai/east";

import {
    ColorSchemeType
} from "../../style.js";

import {
    TableVariantType,
    TableStyleType,
    TableColumnType,
    TableSizeType,
    type TableStyle,
    type PrimitiveEastType,
    TableCellClickEventType,
    TableRowClickEventType,
    TableRowSelectionEventType,
    TableSortEventType,
    TableSortDirectionType
} from "./types.js";
import { UIComponentType } from "../../component.js";
import { Text } from "../../typography/index.js";


// Re-export style types
export {
    TableVariantType,
    TableStyleType,
    TableColumnType,
    TableSizeType,
    type TableSizeLiteral,
    type TableStyle,
} from "./types.js";

/**
 * East type for a table cell.
 *
 * @remarks
 * Defines the type for a table cell.
 *
 * @property value - The cell value as a LiteralValueType (for sorting/filtering)
 * @property content - UI component content for the cell (for rendering)
 */
export const TableCellType: StructType<{
    value: LiteralValueType,
    content: UIComponentType,
}> = StructType({
    value: LiteralValueType,
    content: UIComponentType,
});


// ============================================================================
// Table Root Type
// ============================================================================

/**
 * Type for Table component data.
 *
 * @remarks
 * Table displays data in rows and columns with optional styling.
 *
 * @property rows - Array of row data (Dict mapping column keys to UI components)
 * @property columns - Array of column definitions
 * @property style - Optional styling configuration
 */
export const TableRootType = StructType({
    rows: ArrayType(DictType(StringType, TableCellType)),
    columns: ArrayType(TableColumnType),
    style: OptionType(TableStyleType),
});



/**
 * Type representing the Table structure.
 */
export type TableRootType = typeof TableRootType;

// ============================================================================
// Table (API following chart pattern)
// ============================================================================

/**
 * Base column configuration properties shared by all column types.
 *
 * @typeParam FieldType - The East type of the field being rendered
 * @typeParam RowType - The East struct type of the entire row
 */
interface TableColumnConfigBase<FieldType extends EastType = EastType, RowType extends StructType = StructType> {
    /** Column header text (defaults to column key if not provided) */
    header?: SubtypeExprOrValue<StringType>;
    /** Optional render function - defaults to Text.Root (with auto string conversion for non-strings) */
    render?: (value: ExprType<FieldType>, row: ExprType<RowType>) => ExprType<UIComponentType>;
    /** Optional cell click handler */
    onCellClick?: SubtypeExprOrValue<FunctionType<[TableCellClickEventType], NullType>>,
    /** Optional cell double-click handler */
    onCellDoubleClick?: SubtypeExprOrValue<FunctionType<[TableCellClickEventType], NullType>>,
    /** Optional sort change handler */
    onSortChange?: SubtypeExprOrValue<FunctionType<[TableSortEventType], NullType>>,
    /** Fixed column width (CSS value, e.g., "200px", "20%") */
    width?: SubtypeExprOrValue<StringType>;
    /** Minimum column width (CSS value) */
    minWidth?: SubtypeExprOrValue<StringType>;
    /** Maximum column width (CSS value) */
    maxWidth?: SubtypeExprOrValue<StringType>;
}


type CellType = NullType | BooleanType | IntegerType | FloatType | StringType | DateTimeType | BlobType;
/**
 * Column configuration for primitive fields (value function is optional).
 */
interface TableColumnConfigPrimitive<FieldType extends PrimitiveEastType = PrimitiveEastType, RowType extends StructType = StructType>
    extends TableColumnConfigBase<FieldType, RowType> {
    /** Optional function to extract a sortable/filterable value from the field */
    value?: (value: ExprType<FieldType>, row: ExprType<RowType>) => SubtypeExprOrValue<CellType>;
}

/**
 * Column configuration for complex fields (value function is required).
 */
interface TableColumnConfigComplex<FieldType extends EastType = EastType, RowType extends StructType = StructType>
    extends TableColumnConfigBase<FieldType, RowType> {
    /** Required function to extract a sortable/filterable value from complex fields */
    value: (value: ExprType<FieldType>, row: ExprType<RowType>) => SubtypeExprOrValue<CellType>;
}

/**
 * Column configuration for the Table API.
 *
 * @typeParam FieldType - The East type of the field being rendered
 * @typeParam RowType - The East struct type of the entire row
 *
 * @remarks
 * For primitive fields (Boolean, Integer, Float, String, DateTime), the `value` function is optional.
 * For complex fields (Struct, Dict, Array, etc.), the `value` function is required to extract
 * a sortable/filterable value.
 */
export type TableColumnConfig<FieldType extends EastType = EastType, RowType extends StructType = StructType> =
    FieldType extends PrimitiveEastType
    ? TableColumnConfigPrimitive<FieldType, RowType>
    : TableColumnConfigComplex<FieldType, RowType>;

/**
 * Creates a Table component following the chart pattern.
 *
 * @typeParam T - The struct type of each data row
 * @param data - Array of data structs
 * @param columns - Column specification: array of field names, or object with optional config
 * @param style - Optional table styling
 * @returns An East expression representing the table component
 *
 * @remarks
 * Columns can be specified as a simple array of field names, or an object
 * with optional header and render configuration.
 *
 * When render is not provided, fields render as Text automatically:
 * - String fields: `Text.Root(value)`
 * - Other types: `Text.Root(East.str\`\${value}\`)` (auto string conversion)
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Table, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Table.Root(
 *         [
 *             { name: "Alice", age: 30n, role: "Admin" },
 *             { name: "Bob", age: 25n, role: "User" },
 *         ],
 *         ["name", "age", "role"],
 *         { variant: "line", striped: true }
 *     );
 * });
 * ```
 */

// Helper types to extract struct fields from array data type
type ExtractStructFields<T> = T extends ArrayType<infer S>
    ? S extends StructType
    ? S["fields"]
    : never
    : never;

// Helper type to extract the row element type from an array type (always StructType due to constraint)
type ExtractRowType<T> = T extends ArrayType<infer S>
    ? S extends StructType
    ? S
    : StructType
    : StructType;

type DataFields<T extends SubtypeExprOrValue<ArrayType<StructType>>> = ExtractStructFields<TypeOf<T>>;
type DataRowType<T extends SubtypeExprOrValue<ArrayType<StructType>>> = ExtractRowType<TypeOf<T>>;

// Helper type to extract only primitive field keys from a struct's fields
type PrimitiveFieldKeys<Fields> = {
    [K in keyof Fields]: Fields[K] extends PrimitiveEastType ? K : never
}[keyof Fields];

/**
 * Column specification for the Table API.
 *
 * @remarks
 * - **Array form**: Only primitive field keys allowed (e.g., `["name", "age"]`)
 * - **Object form**: All fields allowed, but complex fields require a `value` function
 */
type ColumnSpec<T extends SubtypeExprOrValue<ArrayType<StructType>>> =
    | PrimitiveFieldKeys<DataFields<NoInfer<T>>>[]
    | { [K in keyof DataFields<NoInfer<T>>]?: TableColumnConfig<DataFields<NoInfer<T>>[K], DataRowType<NoInfer<T>>> };

export function createTable<T extends SubtypeExprOrValue<ArrayType<StructType>>>(
    data: T,
    columns: ColumnSpec<T>,
    style?: TableStyle
): ExprType<UIComponentType> {
    const data_expr = East.value(data) as ExprType<ArrayType<StructType>>;
    const field_types = Expr.type(data_expr).value.fields;

    // Normalize columns to object format
    // dataType: the original field type from the data struct
    // valueType: the type after applying value function (computed during row mapping)
    const columnEntries = Array.isArray(columns)
        ? (columns as string[]).map(key => [key, undefined] as const)
        : Object.entries(columns);

    const columns_obj = Object.fromEntries(columnEntries.map(([key, config]) => {
        const fieldType = field_types[key as keyof typeof field_types] as EastType;
        return [key, {
            ...config,
            dataType: toEastTypeValue(fieldType),
        }];
    })) as Record<string, TableColumnConfig & { dataType: EastTypeValue, valueType: EastTypeValue, }>;

    const rows_mapped = data_expr.map(($, datum) => {
        const cells = $.let(new Map(), DictType(StringType, StructType({
            value: LiteralValueType,
            content: UIComponentType,
        })));
        for (const [col_key, col_config] of Object.entries(columns_obj)) {
            const field_value = (datum as any)[col_key];
            const field_type = field_types[col_key];

            // Get cell value: use custom value function if provided, otherwise use field value directly
            // (for primitive types, this works; complex types require a value function)
            let cellValue;
            if ((col_config as any).value) {
                const customValue = East.value((col_config as any).value(field_value, datum as any));
                const customValueType = Expr.type(customValue) as EastType;
                cellValue = variant(customValueType.type as any, customValue);
            } else {
                cellValue = variant(field_type.type, field_value);
            }

            // get the value type tag from cellValue
            const valueTypeTag = cellValue.type as string;

            // check that the type is a valid LiteralValueType (primitive) tag
            if (
                valueTypeTag !== "Null" &&
                valueTypeTag !== "Boolean" &&
                valueTypeTag !== "Integer" &&
                valueTypeTag !== "Float" &&
                valueTypeTag !== "String" &&
                valueTypeTag !== "DateTime" &&
                valueTypeTag !== "Blob") {
                throw new Error(`Column "${col_key}" has value type "${valueTypeTag}" which is not a valid column type. Complex types require a value function that returns a primitive type.`);
            }

            // get the valueType as EastTypeValue
            const valueType = variant(valueTypeTag, null) as EastTypeValue;

            // if valueType in columns_obj is already defined, check it matches
            if (col_config.valueType !== undefined) {
                if (!isTypeValueEqual(col_config.valueType, valueType)) {
                    throw new Error(`Column "${col_key}" has inconsistent value types across rows: expected "${col_config.valueType.type}" but got "${valueTypeTag}"`);
                }
            } else {
                // set the valueType for this column
                (col_config as any).valueType = valueType;
            }

            $(cells.insert(col_key, {
                value: cellValue,
                content: East.value(
                    col_config.render ?
                        col_config.render(field_value, datum as any) :
                        Text.Root(East.str`${field_value}`, {
                            whiteSpace: "nowrap",
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                        }),
                    UIComponentType
                ),
            }));
        }
        return cells
    });

    // Create columns array from the columns config
    const columns_mapped: ValueTypeOf<ArrayType<typeof TableColumnType>> = []

    for (const [key, config] of Object.entries(columns_obj)) {
        columns_mapped.push({
            key: key,
            dataType: config.dataType,
            valueType: config.valueType,
            header: config?.header !== undefined ? some(config.header) : some(key) as any,
            width: config?.width !== undefined ? some(config.width) : none as any,
            minWidth: config?.minWidth !== undefined ? some(config.minWidth) : none as any,
            maxWidth: config?.maxWidth !== undefined ? some(config.maxWidth) : none as any,
        });
    }
    // Build the style object
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), TableVariantType)
            : style.variant)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), TableSizeType)
            : style.size)
        : undefined;

    const colorPaletteValue = style?.colorPalette
        ? (typeof style.colorPalette === "string"
            ? East.value(variant(style.colorPalette, null), ColorSchemeType)
            : style.colorPalette)
        : undefined;

    return East.value(variant("Table", {
        rows: rows_mapped,
        columns: columns_mapped as ValueTypeOf<typeof TableRootType>["columns"],
        style: style ? some(East.value({
            variant: variantValue ? some(variantValue) : none,
            size: sizeValue ? some(sizeValue) : none,
            striped: style.striped !== undefined ? some(style.striped) : none,
            interactive: style.interactive !== undefined ? some(style.interactive) : none,
            stickyHeader: style.stickyHeader !== undefined ? some(style.stickyHeader) : none,
            showColumnBorder: style.showColumnBorder !== undefined ? some(style.showColumnBorder) : none,
            colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
            onCellClick: style.onCellClick ? some(style.onCellClick) : none,
            onCellDoubleClick: style.onCellDoubleClick ? some(style.onCellDoubleClick) : none,
            onRowClick: style.onRowClick ? some(style.onRowClick) : none,
            onRowDoubleClick: style.onRowDoubleClick ? some(style.onRowDoubleClick) : none,
            onRowSelectionChange: style.onRowSelectionChange ? some(style.onRowSelectionChange) : none,
            onSortChange: style.onSortChange ? some(style.onSortChange) : none,
        }, TableStyleType)) : none,
    }), UIComponentType);
}

/**
 * Table namespace following the chart pattern.
 *
 * @remarks
 * Pass data as an array of structs and configure columns with either
 * an array of field names or an object with optional header/render config.
 */
export const Table = {
    /**
     * Creates a Table component following the chart pattern.
     *
     * @typeParam T - The struct type of each data row
     * @param data - Array of data structs
     * @param columns - Column specification: array of field names, or object with optional config
     * @param style - Optional table styling
     * @returns An East expression representing the table component
     *
     * @remarks
     * Columns can be specified as a simple array of field names, or an object
     * with optional header and render configuration.
     *
     * When render is not provided, fields render as Text automatically:
     * - String fields: `Text.Root(value)`
     * - Other types: `Text.Root(East.str\`\${value}\`)` (auto string conversion)
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Table, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Table.Root(
     *         [
     *             { name: "Alice", age: 30n, role: "Admin" },
     *             { name: "Bob", age: 25n, role: "User" },
     *         ],
     *         ["name", "age", "role"],
     *         { variant: "line", striped: true }
     *     );
     * });
     * ```
     */
    Root: createTable,
    Types: {
        /**
         * Type for Table component data.
         *
         * @remarks
         * Table displays data in rows and columns with optional styling.
         *
         * @property rows - Array of row data (Dict mapping column keys to UI components)
         * @property columns - Array of column definitions
         * @property style - Optional styling configuration
         */
        Root: TableRootType,
        /**
         * Style type for the table root component.
         *
         * @remarks
         * All properties are optional and wrapped in {@link OptionType}.
         *
         * @property variant - Table variant (line or outline)
         * @property size - Table size (sm, md, lg)
         * @property striped - Whether to show zebra stripes on rows
         * @property interactive - Whether to highlight rows on hover
         * @property stickyHeader - Whether the header sticks when scrolling
         * @property showColumnBorder - Whether to show borders between columns
         * @property colorPalette - Color scheme for interactive hover
         */
        Style: TableStyleType,
        /**
         * East type for a table column definition.
         *
         * @remarks
         * Defines the header text and key for a column.
         *
         * @property key - The column key (field name)
         * @property type - The column value type
         * @property header - Optional header text for the column
         */
        Column: TableColumnType,
        /**
         * East type for a table cell.
         *
         * @remarks
         * Defines the type for a table cell.
         *
         * @property value - The cell value as a LiteralValueType
         * @property content - UI component content for the cell
         */
        Cell: TableCellType,
        /**
         * Type for cell values (LiteralValueType - supports any primitive East value).
         */
        Value: LiteralValueType,
        /**
         * Table variant type for Chakra UI v3 table styling.
         *
         * @remarks
         * Create instances using the {@link TableVariant} function.
         *
         * @property line - Table with horizontal lines between rows
         * @property outline - Table with full border outline
         */
        Variant: TableVariantType,
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
        Size: TableSizeType,
        /**
         * Event type for row click callbacks.
         *
         * @property rowIndex - The index of the clicked row
         */
        RowClickEvent: TableRowClickEventType,
        /**
         * Event type for cell click callbacks.
         *
         * @property rowIndex - The row index
         * @property columnKey - The column key
         * @property cellValue - The cell value
         */
        CellClickEvent: TableCellClickEventType,
        /**
         * Event type for row selection change callbacks.
         *
         * @property rowIndex - The row index
         * @property selected - Whether the row is selected
         * @property selectedRowsIndices - Array of all selected row indices
         */
        RowSelectionEvent: TableRowSelectionEventType,
        /**
         * Event type for sort change callbacks.
         *
         * @property columnKey - The column key being sorted
         * @property sortIndex - The sort index (for multi-column sorting)
         * @property sortDirection - The sort direction
         */
        SortEvent: TableSortEventType,
        /**
         * Sort direction type (asc or desc).
         */
        SortDirection: TableSortDirectionType,
    },
} as const;
