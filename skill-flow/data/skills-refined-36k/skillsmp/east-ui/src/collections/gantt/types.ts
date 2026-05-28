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
    DateTimeType,
    FloatType,
    IntegerType,
    NullType,
    FunctionType
} from "@elaraai/east";

import { TableCellClickEventType, TableRowClickEventType, TableSortEventType } from "../table/types.js";

import {
    ColorSchemeType,
    type ColorSchemeLiteral,
} from "../../style.js";

// Import shared types from table
import {
    TableVariantType,
    TableSizeType,
    type TableVariantLiteral,
    type TableSizeLiteral,
} from "../table/types.js";

// Re-export table types used by Gantt
export {
    TableVariantType,
    TableSizeType,
    type TableVariantLiteral,
    type TableSizeLiteral,
} from "../table/types.js";

// ============================================================================
// Time Step Type
// ============================================================================

/**
 * Time step variant type for drag/duration snapping.
 *
 * @remarks
 * Each variant contains a float value representing the step size in that unit.
 *
 * @property minutes - Step size in minutes (e.g., 15 for 15-minute intervals)
 * @property hours - Step size in hours (e.g., 1 for hourly)
 * @property days - Step size in days (e.g., 1 for daily, 0.5 for half-day)
 * @property weeks - Step size in weeks (e.g., 1 for weekly)
 * @property months - Step size in months (e.g., 1 for monthly)
 */
export const TimeStepType = VariantType({
    minutes: FloatType,
    hours: FloatType,
    days: FloatType,
    weeks: FloatType,
    months: FloatType,
});

export type TimeStepType = typeof TimeStepType;

// ============================================================================
// Gantt Event Types
// ============================================================================

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
export const GanttTaskType = StructType({
    start: DateTimeType,
    end: DateTimeType,
    label: OptionType(StringType),
    progress: OptionType(FloatType),
    colorPalette: OptionType(ColorSchemeType),
});

/**
 * Type representing the Gantt task structure.
 */
export type GanttTaskType = typeof GanttTaskType;

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
export const GanttMilestoneType = StructType({
    date: DateTimeType,
    label: OptionType(StringType),
    colorPalette: OptionType(ColorSchemeType),
});

/**
 * Type representing the Gantt milestone structure.
 */
export type GanttMilestoneType = typeof GanttMilestoneType;

/**
 * Gantt event variant type.
 *
 * @remarks
 * Events can be either tasks (with duration) or milestones (single point).
 *
 * @property Task - A task spanning from start to end date
 * @property Milestone - A milestone at a specific date
 */
export const GanttEventType = VariantType({
    Task: GanttTaskType,
    Milestone: GanttMilestoneType,
});

/**
 * Type representing the Gantt event variant.
 */
export type GanttEventType = typeof GanttEventType;

// ============================================================================
// Gantt Callback Event Types
// ============================================================================

/**
 * Event data for task click events.
 *
 * @property rowIndex - Row index (0-based)
 * @property taskIndex - Task index within the row (0-based)
 * @property taskStart - Start date/time of the task
 * @property taskEnd - End date/time of the task
 */
export const GanttTaskClickEventType = StructType({
    rowIndex: IntegerType,
    taskIndex: IntegerType,
    taskStart: DateTimeType,
    taskEnd: DateTimeType,
});

export type GanttTaskClickEventType = typeof GanttTaskClickEventType;

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
export const GanttTaskDragEventType = StructType({
    rowIndex: IntegerType,
    taskIndex: IntegerType,
    previousStart: DateTimeType,
    previousEnd: DateTimeType,
    newStart: DateTimeType,
    newEnd: DateTimeType,
});

export type GanttTaskDragEventType = typeof GanttTaskDragEventType;

/**
 * Event data for task progress change events.
 *
 * @property rowIndex - Row index (0-based)
 * @property taskIndex - Task index within the row (0-based)
 * @property previousProgress - Previous progress value (0-100)
 * @property newProgress - New progress value (0-100)
 */
export const GanttTaskProgressChangeEventType = StructType({
    rowIndex: IntegerType,
    taskIndex: IntegerType,
    previousProgress: FloatType,
    newProgress: FloatType,
});

export type GanttTaskProgressChangeEventType = typeof GanttTaskProgressChangeEventType;

/**
 * Event data for task duration change events (dragging task end).
 *
 * @property rowIndex - Row index (0-based)
 * @property taskIndex - Task index within the row (0-based)
 * @property previousEnd - Previous end date/time
 * @property newEnd - New end date/time
 */
export const GanttTaskDurationChangeEventType = StructType({
    rowIndex: IntegerType,
    taskIndex: IntegerType,
    previousEnd: DateTimeType,
    newEnd: DateTimeType,
});

export type GanttTaskDurationChangeEventType = typeof GanttTaskDurationChangeEventType;

/**
 * Event data for milestone click events.
 *
 * @property rowIndex - Row index (0-based)
 * @property milestoneIndex - Milestone index within the row (0-based)
 * @property milestoneDate - Date/time of the milestone
 */
export const GanttMilestoneClickEventType = StructType({
    rowIndex: IntegerType,
    milestoneIndex: IntegerType,
    milestoneDate: DateTimeType,
});

export type GanttMilestoneClickEventType = typeof GanttMilestoneClickEventType;

/**
 * Event data for milestone drag events.
 *
 * @property rowIndex - Row index (0-based)
 * @property milestoneIndex - Milestone index within the row (0-based)
 * @property previousDate - Previous date/time of the milestone
 * @property newDate - New date/time of the milestone
 */
export const GanttMilestoneDragEventType = StructType({
    rowIndex: IntegerType,
    milestoneIndex: IntegerType,
    previousDate: DateTimeType,
    newDate: DateTimeType,
});

export type GanttMilestoneDragEventType = typeof GanttMilestoneDragEventType;

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
 * @property onCellClick - Callback triggered when a cell is clicked
 * @property onCellDoubleClick - Callback triggered when a cell is double-clicked
 * @property onRowClick - Callback triggered when a row is clicked
 * @property onRowDoubleClick - Callback triggered when a row is double-clicked
 * @property onSortChange - Callback triggered when sorting changes
 * @property onTaskClick - Callback triggered when a task is clicked
 * @property onTaskDoubleClick - Callback triggered when a task is double-clicked
 * @property onTaskDrag - Callback triggered when a task is dragged/resized
 * @property onTaskDurationChange - Callback triggered when task duration changes (dragging task end)
 * @property onTaskProgressChange - Callback triggered when task progress changes
 * @property onMilestoneClick - Callback triggered when a milestone is clicked
 * @property onMilestoneDoubleClick - Callback triggered when a milestone is double-clicked
 * @property onMilestoneDrag - Callback triggered when a milestone is dragged
 * @property dragStep - Optional time step for drag snapping (e.g., variant("days", 1) for daily)
 * @property durationStep - Optional time step for duration change snapping
 *
 */
export const GanttStyleType = StructType({
    variant: OptionType(TableVariantType),
    size: OptionType(TableSizeType),
    striped: OptionType(BooleanType),
    interactive: OptionType(BooleanType),
    stickyHeader: OptionType(BooleanType),
    showColumnBorder: OptionType(BooleanType),
    colorPalette: OptionType(ColorSchemeType),
    showToday: OptionType(BooleanType),
    dragStep: OptionType(TimeStepType),
    durationStep: OptionType(TimeStepType),
    onCellClick: OptionType(FunctionType([TableCellClickEventType], NullType)),
    onCellDoubleClick: OptionType(FunctionType([TableCellClickEventType], NullType)),
    onRowClick: OptionType(FunctionType([TableRowClickEventType], NullType)),
    onRowDoubleClick: OptionType(FunctionType([TableRowClickEventType], NullType)),
    onSortChange: OptionType(FunctionType([TableSortEventType], NullType)),
    onTaskClick: OptionType(FunctionType([GanttTaskClickEventType], NullType)),
    onTaskDoubleClick: OptionType(FunctionType([GanttTaskClickEventType], NullType)),
    onTaskDrag: OptionType(FunctionType([GanttTaskDragEventType], NullType)),
    onTaskDurationChange: OptionType(FunctionType([GanttTaskDurationChangeEventType], NullType)),
    onTaskProgressChange: OptionType(FunctionType([GanttTaskProgressChangeEventType], NullType)),
    onMilestoneClick: OptionType(FunctionType([GanttMilestoneClickEventType], NullType)),
    onMilestoneDoubleClick: OptionType(FunctionType([GanttMilestoneClickEventType], NullType)),
    onMilestoneDrag: OptionType(FunctionType([GanttMilestoneDragEventType], NullType)),
});

/**
 * Type representing the Gantt style structure.
 */
export type GanttStyleType = typeof GanttStyleType;

/**
 * TypeScript interface for Gantt styling input.
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
 * @property colorPalette - Default color scheme for events
 * @property showToday - Whether to show a today marker line
 * @property dragStep - Optional time step for drag snapping
 * @property durationStep - Optional time step for duration change snapping
 * @property onCellClick - Callback triggered when a cell is clicked
 * @property onCellDoubleClick - Callback triggered when a cell is double-clicked
 * @property onRowClick - Callback triggered when a row is clicked
 * @property onRowDoubleClick - Callback triggered when a row is double-clicked
 * @property onSortChange - Callback triggered when sorting changes
 * @property onTaskClick - Callback triggered when a task is clicked
 * @property onTaskDoubleClick - Callback triggered when a task is double-clicked
 * @property onTaskDrag - Callback triggered when a task is dragged/resized
 * @property onTaskDurationChange - Callback triggered when task duration changes (dragging task end)
 * @property onTaskProgressChange - Callback triggered when task progress changes
 * @property onMilestoneClick - Callback triggered when a milestone is clicked
 * @property onMilestoneDoubleClick - Callback triggered when a milestone is double-clicked
 * @property onMilestoneDrag - Callback triggered when a milestone is dragged
 */
export interface GanttStyle {
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
    /** Default color scheme for events */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Whether to show a today marker line */
    showToday?: SubtypeExprOrValue<BooleanType>;
    /** Optional time step for drag snapping (e.g., variant("days", 1) for daily) */
    dragStep?: SubtypeExprOrValue<TimeStepType>;
    /** Optional time step for duration change snapping */
    durationStep?: SubtypeExprOrValue<TimeStepType>;
    /** Callback triggered when a cell is clicked */
    onCellClick?: SubtypeExprOrValue<FunctionType<[TableCellClickEventType], NullType>>;
    /** Callback triggered when a cell is double-clicked */
    onCellDoubleClick?: SubtypeExprOrValue<FunctionType<[TableCellClickEventType], NullType>>;
    /** Callback triggered when a row is clicked */
    onRowClick?: SubtypeExprOrValue<FunctionType<[TableRowClickEventType], NullType>>;
    /** Callback triggered when a row is double-clicked */
    onRowDoubleClick?: SubtypeExprOrValue<FunctionType<[TableRowClickEventType], NullType>>;
    /** Callback triggered when sorting changes */
    onSortChange?: SubtypeExprOrValue<FunctionType<[TableSortEventType], NullType>>;
    /** Callback triggered when a task is clicked */
    onTaskClick?: SubtypeExprOrValue<FunctionType<[GanttTaskClickEventType], NullType>>;
    /** Callback triggered when a task is double-clicked */
    onTaskDoubleClick?: SubtypeExprOrValue<FunctionType<[GanttTaskClickEventType], NullType>>;
    /** Callback triggered when a task is dragged/resized */
    onTaskDrag?: SubtypeExprOrValue<FunctionType<[GanttTaskDragEventType], NullType>>;
    /** Callback triggered when task duration changes (dragging task end) */
    onTaskDurationChange?: SubtypeExprOrValue<FunctionType<[GanttTaskDurationChangeEventType], NullType>>;
    /** Callback triggered when task progress changes */
    onTaskProgressChange?: SubtypeExprOrValue<FunctionType<[GanttTaskProgressChangeEventType], NullType>>;
    /** Callback triggered when a milestone is clicked */
    onMilestoneClick?: SubtypeExprOrValue<FunctionType<[GanttMilestoneClickEventType], NullType>>;
    /** Callback triggered when a milestone is double-clicked */
    onMilestoneDoubleClick?: SubtypeExprOrValue<FunctionType<[GanttMilestoneClickEventType], NullType>>;
    /** Callback triggered when a milestone is dragged */
    onMilestoneDrag?: SubtypeExprOrValue<FunctionType<[GanttMilestoneDragEventType], NullType>>;
}
