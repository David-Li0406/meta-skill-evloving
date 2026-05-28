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
    DateTimeType,
    FloatType,
    variant,
    type ValueTypeOf,
    type TypeOf,
    some,
    none,
    toEastTypeValue,
    type EastType,
    type EastTypeValue,
    LiteralValueType,
    isTypeValueEqual,
} from "@elaraai/east";

import { ColorSchemeType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import {
    TableCellType,
    TableColumnType,
    type TableColumnConfig,
} from "../table/index.js";
import { Text } from "../../typography/index.js";

import {
    GanttEventType,
    GanttTaskType,
    GanttMilestoneType,
    GanttStyleType,
    TableVariantType,
    TableSizeType,
    type GanttStyle,
    GanttTaskClickEventType,
    GanttTaskDragEventType,
    GanttTaskDurationChangeEventType,
    GanttTaskProgressChangeEventType,
    GanttMilestoneClickEventType,
    GanttMilestoneDragEventType,
} from "./types.js";

// Re-export types
export {
    GanttEventType,
    GanttTaskType,
    GanttMilestoneType,
    GanttStyleType,
    TimeStepType,
    type GanttStyle,
} from "./types.js";

// ============================================================================
// Gantt Row Type
// ============================================================================

/**
 * East type for a Gantt row.
 *
 * @remarks
 * Each row has table cells (displayed on the left) and events (displayed on the right as a timeline).
 *
 * @property cells - Dict of column key to cell content (same as Table)
 * @property events - Array of events (Task or Milestone variants)
 */
export const GanttRowType = StructType({
    cells: DictType(StringType, TableCellType),
    events: ArrayType(GanttEventType),
});

/**
 * Type representing the Gantt row structure.
 */
export type GanttRowType = typeof GanttRowType;

// ============================================================================
// Gantt Root Type
// ============================================================================

/**
 * Type for Gantt component data.
 *
 * @remarks
 * Gantt displays rows with time-based events (tasks and milestones).
 * The time range is derived from the events' domain.
 *
 * @property rows - Array of Gantt rows
 * @property columns - Array of column definitions (same as Table)
 * @property style - Optional styling configuration
 */
export const GanttRootType = StructType({
    rows: ArrayType(GanttRowType),
    columns: ArrayType(TableColumnType),
    style: OptionType(GanttStyleType),
});

/**
 * Type representing the Gantt structure.
 */
export type GanttRootType = typeof GanttRootType;

// ============================================================================
// Task/Milestone Input Interfaces
// ============================================================================

/**
 * Input interface for creating a Task event.
 *
 * @property start - Start date/time of the task
 * @property end - End date/time of the task
 * @property label - Optional label to display on the task bar
 * @property progress - Optional progress percentage (0-100)
 * @property colorPalette - Optional color scheme for the task bar
 */
export interface TaskInput {
    start: SubtypeExprOrValue<DateTimeType>;
    end: SubtypeExprOrValue<DateTimeType>;
    label?: SubtypeExprOrValue<StringType>;
    progress?: SubtypeExprOrValue<FloatType>;
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | string;
}

/**
 * Input interface for creating a Milestone event.
 *
 * @property date - The date/time of the milestone
 * @property label - Optional label to display near the milestone
 * @property colorPalette - Optional color scheme for the milestone marker
 */
export interface MilestoneInput {
    date: SubtypeExprOrValue<DateTimeType>;
    label?: SubtypeExprOrValue<StringType>;
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | string;
}

// ============================================================================
// Factory Functions for Events
// ============================================================================

/**
 * Creates a Task event for a Gantt row.
 *
 * @param input - Task configuration
 * @returns An East expression representing the Task event
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Gantt, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Gantt.Root(
 *         [{ name: "Task", start: new Date("2024-01-01"), end: new Date("2024-01-15") }],
 *         ["name"],
 *         row => [Gantt.Task({
 *             start: row.start,
 *             end: row.end,
 *             label: "Design Phase",
 *             progress: 75,
 *             colorPalette: "blue",
 *         })]
 *     );
 * });
 * ```
 */
function createTask(input: TaskInput): ExprType<GanttEventType> {
    const colorPaletteValue = input.colorPalette
        ? (typeof input.colorPalette === "string"
            ? East.value(variant(input.colorPalette as any, null), ColorSchemeType)
            : input.colorPalette)
        : undefined;

    return East.value(variant("Task", {
        start: input.start,
        end: input.end,
        label: input.label ? variant("some", input.label) : variant("none", null),
        progress: input.progress ? variant("some", input.progress) : variant("none", null),
        colorPalette: colorPaletteValue ? variant("some", colorPaletteValue) : variant("none", null),
    }), GanttEventType);
}

/**
 * Creates a Milestone event for a Gantt row.
 *
 * @param input - Milestone configuration
 * @returns An East expression representing the Milestone event
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Gantt, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Gantt.Root(
 *         [{ name: "Launch", date: new Date("2024-02-01") }],
 *         ["name"],
 *         row => [Gantt.Milestone({
 *             date: row.date,
 *             label: "Design Complete",
 *             colorPalette: "green",
 *         })]
 *     );
 * });
 * ```
 */
function createMilestone(input: MilestoneInput): ExprType<GanttEventType> {
    const colorPaletteValue = input.colorPalette
        ? (typeof input.colorPalette === "string"
            ? East.value(variant(input.colorPalette as any, null), ColorSchemeType)
            : input.colorPalette)
        : undefined;

    return East.value(variant("Milestone", {
        date: input.date,
        label: input.label ? variant("some", input.label) : variant("none", null),
        colorPalette: colorPaletteValue ? variant("some", colorPaletteValue) : variant("none", null),
    }), GanttEventType);
}

// ============================================================================
// Gantt Column Configuration
// ============================================================================

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

// Column specification can be array of keys or object config
type ColumnSpec<T extends SubtypeExprOrValue<ArrayType<StructType>>> =
    | (keyof DataFields<NoInfer<T>>)[]
    | { [K in keyof DataFields<NoInfer<T>>]?: TableColumnConfig<DataFields<NoInfer<T>>[K], DataRowType<NoInfer<T>>> };

// ============================================================================
// Main Gantt Factory
// ============================================================================

/**
 * Creates a Gantt component following the Table pattern.
 *
 * @typeParam T - The struct type of each data row
 * @param data - Array of data structs
 * @param columns - Column specification for the left-side table columns
 * @param events - Function to extract events from each row
 * @param style - Optional Gantt styling
 * @returns An East expression representing the Gantt component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Gantt, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Gantt.Root(
 *         [
 *             { name: "Design", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
 *             { name: "Development", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
 *         ],
 *         ["name"],
 *         row => [Gantt.Task({ start: row.start, end: row.end })],
 *         { showToday: true }
 *     );
 * });
 * ```
 */
function createGantt<T extends SubtypeExprOrValue<ArrayType<StructType>>>(
    data: T,
    columns: ColumnSpec<T>,
    events: (row: ExprType<TypeOf<T> extends ArrayType<infer E> ? E : never>) => SubtypeExprOrValue<ArrayType<GanttEventType>>,
    style?: GanttStyle
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
    })) as Record<string, TableColumnConfig & { dataType: EastTypeValue; valueType: EastTypeValue }>;

    // Map each data row to a GanttRow with cells and events
    const rows_mapped = data_expr.map(($, datum) => {
        // Build cells dict (same as Table)
        const cells = $.let(new Map(), DictType(StringType, StructType({
            value: LiteralValueType,
            content: UIComponentType
        })));

        for (const [col_key, col_config] of Object.entries(columns_obj)) {
            const field_value = (datum as any)[col_key];
            const field_type = field_types[col_key];

            // Get cell value: use custom value function if provided, otherwise use field value directly
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
            if (valueTypeTag !== "Null" && valueTypeTag !== "Boolean" && valueTypeTag !== "Integer" &&
                valueTypeTag !== "Float" && valueTypeTag !== "String" && valueTypeTag !== "DateTime" &&
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

        // Get events from the row using the events function
        const row_events = events(datum as any);

        return East.value({
            cells: cells,
            events: row_events,
        }, GanttRowType);
    });

    // Create columns array from the columns config
    const columns_mapped: ValueTypeOf<ArrayType<typeof TableColumnType>> = [];
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

    // Build style value
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
            ? East.value(variant(style.colorPalette as any, null), ColorSchemeType)
            : style.colorPalette)
        : undefined;

    const styleValue = style ? East.value({
        variant: variantValue ? some(variantValue) : none,
        size: sizeValue ? some(sizeValue) : none,
        striped: style.striped !== undefined ? some(style.striped) : none,
        interactive: style.interactive !== undefined ? some(style.interactive) : none,
        stickyHeader: style.stickyHeader !== undefined ? some(style.stickyHeader) : none,
        showColumnBorder: style.showColumnBorder !== undefined ? some(style.showColumnBorder) : none,
        colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
        showToday: style.showToday !== undefined ? some(style.showToday) : none,
        dragStep: style.dragStep ? some(style.dragStep) : none,
        durationStep: style.durationStep ? some(style.durationStep) : none,
        onCellClick: style.onCellClick ? some(style.onCellClick) : none,
        onCellDoubleClick: style.onCellDoubleClick ? some(style.onCellDoubleClick) : none,
        onRowClick: style.onRowClick ? some(style.onRowClick) : none,
        onRowDoubleClick: style.onRowDoubleClick ? some(style.onRowDoubleClick) : none,
        onSortChange: style.onSortChange ? some(style.onSortChange) : none,
        onTaskClick: style.onTaskClick ? some(style.onTaskClick) : none,
        onTaskDoubleClick: style.onTaskDoubleClick ? some(style.onTaskDoubleClick) : none,
        onTaskDrag: style.onTaskDrag ? some(style.onTaskDrag) : none,
        onTaskDurationChange: style.onTaskDurationChange ? some(style.onTaskDurationChange) : none,
        onTaskProgressChange: style.onTaskProgressChange ? some(style.onTaskProgressChange) : none,
        onMilestoneClick: style.onMilestoneClick ? some(style.onMilestoneClick) : none,
        onMilestoneDoubleClick: style.onMilestoneDoubleClick ? some(style.onMilestoneDoubleClick) : none,
        onMilestoneDrag: style.onMilestoneDrag ? some(style.onMilestoneDrag) : none,
    }, GanttStyleType) : undefined;

    return East.value(variant("Gantt", {
        rows: rows_mapped,
        columns: columns_mapped as ValueTypeOf<typeof GanttRootType>["columns"],
        style: styleValue ? some(styleValue) : none,
    }), UIComponentType);
}

// ============================================================================
// Namespace Export
// ============================================================================

/**
 * Gantt namespace for creating Gantt chart components.
 *
 * @remarks
 * Gantt charts display time-based events (tasks and milestones) in rows.
 * Each row has table columns on the left and a timeline with events on the right.
 * The API follows the Table pattern for column configuration.
 */
export const Gantt = {
    /**
     * Creates a Gantt component following the Table pattern.
     *
     * @typeParam T - The struct type of each data row
     * @param data - Array of data structs
     * @param columns - Column specification for the left-side table columns
     * @param events - Function to extract events from each row
     * @param style - Optional Gantt styling
     * @returns An East expression representing the Gantt component
     *
     * @remarks
     * Gantt charts display time-based events (tasks and milestones) in rows.
     * Each row has table columns on the left and a timeline with events on the right.
     * The API follows the Table pattern for column configuration.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Gantt, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Gantt.Root(
     *         [
     *             { name: "Design", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
     *             { name: "Development", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
     *         ],
     *         ["name"],
     *         row => [Gantt.Task({ start: row.start, end: row.end })],
     *         { showToday: true }
     *     );
     * });
     * ```
     */
    Root: createGantt,
    /**
     * Creates a Task event for a Gantt row.
     *
     * @param input - Task configuration
     * @returns An East expression representing the Task event
     *
     * @remarks
     * Tasks represent work items that span a duration from start to end date.
     * Tasks can show progress and be styled with different colors.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Gantt, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Gantt.Root(
     *         [{ name: "Task", start: new Date("2024-01-01"), end: new Date("2024-01-15") }],
     *         ["name"],
     *         row => [Gantt.Task({
     *             start: row.start,
     *             end: row.end,
     *             label: "Design Phase",
     *             progress: 75,
     *             colorPalette: "blue",
     *         })]
     *     );
     * });
     * ```
     */
    Task: createTask,
    /**
     * Creates a Milestone event for a Gantt row.
     *
     * @param input - Milestone configuration
     * @returns An East expression representing the Milestone event
     *
     * @remarks
     * Milestones represent single points in time (e.g., deadlines, releases).
     * They appear as markers on the timeline rather than bars.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Gantt, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Gantt.Root(
     *         [{ name: "Launch", date: new Date("2024-02-01") }],
     *         ["name"],
     *         row => [Gantt.Milestone({
     *             date: row.date,
     *             label: "Launch",
     *             colorPalette: "green",
     *         })]
     *     );
     * });
     * ```
     */
    Milestone: createMilestone,
    Types: {
        /**
         * Type for Gantt component data.
         *
         * @remarks
         * Gantt displays rows with time-based events (tasks and milestones).
         * The time range is derived from the events' domain.
         *
         * @property rows - Array of Gantt rows
         * @property columns - Array of column definitions (same as Table)
         * @property style - Optional styling configuration
         */
        Root: GanttRootType,
        /**
         * East type for a Gantt row.
         *
         * @remarks
         * Each row has table cells (displayed on the left) and events (displayed on the right as a timeline).
         *
         * @property cells - Dict of column key to cell content (same as Table)
         * @property events - Array of events (Task or Milestone variants)
         */
        Row: GanttRowType,
        /**
         * Gantt event variant type.
         *
         * @remarks
         * Events can be either tasks (with duration) or milestones (single point).
         *
         * @property Task - A task spanning from start to end date
         * @property Milestone - A milestone at a specific date
         */
        Event: GanttEventType,
        /**
         * Task event data for Gantt charts.
         *
         * @remarks
         * Represents a task bar spanning from start to end date.
         *
         * @property start - Start date/time of the task
         * @property end - End date/time of the task
         * @property label - Optional label to display on the task bar
         * @property progress - Optional progress percentage (0-100)
         * @property colorPalette - Optional color scheme for the task bar
         */
        Task: GanttTaskType,
        /**
         * Milestone event data for Gantt charts.
         *
         * @remarks
         * Represents a single point in time milestone.
         *
         * @property date - The date/time of the milestone
         * @property label - Optional label to display near the milestone
         * @property colorPalette - Optional color scheme for the milestone marker
         */
        Milestone: GanttMilestoneType,
        /**
         * Style type for the Gantt component.
         *
         * @remarks
         * All properties are optional and wrapped in {@link OptionType}.
         * Reuses table styling properties where applicable.
         *
         * @property variant - Table variant (line or outline)
         * @property size - Table size (sm, md, lg)
         * @property striped - Whether to show zebra stripes on rows
         * @property interactive - Whether to highlight rows on hover
         * @property stickyHeader - Whether the header sticks when scrolling
         * @property showColumnBorder - Whether to show borders between columns
         * @property colorPalette - Default color scheme for events
         * @property showToday - Whether to show a today marker line
         */
        Style: GanttStyleType,
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
         * @property value - The cell value as a literal
         * @property content - Optional UI component content for the cell
         */
        Cell: TableCellType,
        /**
         * Event data for task click events.
         *
         * @property rowIndex - Row index (0-based)
         * @property taskIndex - Task index within the row (0-based)
         * @property taskStart - Start date/time of the task
         * @property taskEnd - End date/time of the task
         */
        TaskClickEvent: GanttTaskClickEventType,
        /**
         * Event data for task drag/resize events.
         *
         * @property rowIndex - Row index (0-based)
         * @property taskIndex - Task index within the row (0-based)
         * @property previousStart - Previous start date/time
         * @property previousEnd - Previous end date/time
         * @property newStart - New start date/time
         * @property newEnd - New end date/time
         */
        TaskDragEvent: GanttTaskDragEventType,
        /**
         * Event data for task progress change events.
         *
         * @property rowIndex - Row index (0-based)
         * @property taskIndex - Task index within the row (0-based)
         * @property previousProgress - Previous progress value (0-100)
         * @property newProgress - New progress value (0-100)
         */
        TaskProgressChangeEvent: GanttTaskProgressChangeEventType,
        /**
         * Event data for task duration change events.
         *
         * @property rowIndex - Row index (0-based)
         * @property taskIndex - Task index within the row (0-based)
         * @property previousEnd - Previous end date/time
         * @property newEnd - New end date/time
         */
        TaskDurationChangeEvent: GanttTaskDurationChangeEventType,
        /**
         * Event data for milestone click events.
         *
         * @property rowIndex - Row index (0-based)
         * @property milestoneIndex - Milestone index within the row (0-based)
         * @property milestoneDate - Date/time of the milestone
         */
        MilestoneClickEvent: GanttMilestoneClickEventType,
        /**
         * Event data for milestone drag events.
         *
         * @property rowIndex - Row index (0-based)
         * @property milestoneIndex - Milestone index within the row (0-based)
         * @property previousDate - Previous date/time of the milestone
         * @property newDate - New date/time of the milestone
         */
        MilestoneDragEvent: GanttMilestoneDragEventType,
    },
} as const;
