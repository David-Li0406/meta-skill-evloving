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
    StringType,
    FloatType,
    OptionType,
    FunctionType,
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

import {
    ColorSchemeType,
    FontWeightType,
    FontStyleType,
    SizeType,
    type ColorSchemeLiteral,
} from "../../style.js";
import { IconSizeType } from "../../display/icon/types.js";
import { UIComponentType } from "../../component.js";
import {
    TableCellType,
    TableColumnType,
    type TableColumnConfig,
} from "../table/index.js";
import { Text } from "../../typography/index.js";

import {
    PlannerStyleType,
    SlotModeType,
    TableVariantType,
    TableSizeType,
    type PlannerStyle,
    EventClickEventType,
    EventDragEventType,
    EventResizeEventType,
    EventDeleteEventType,
    PlannerEventType,
    PlannerBoundaryType,
    EventPopoverTriggerType,
    EventPopoverContextType,
    ContentAlignType,
    EventLabelType,
    EventIconType,
    type EventLabel,
    type EventIcon,
} from "./types.js";

// Re-export types
export {
    PlannerStyleType,
    SlotModeType,
    type PlannerStyle,
    type SlotModeLiteral,
    EventClickEventType,
    EventDragEventType,
    EventResizeEventType,
    EventDeleteEventType,
    ResizeEdgeType,
    PlannerEventType,
    PlannerBoundaryType,
    type PlannerBoundary,
    EventPopoverTriggerType,
    type EventPopoverTriggerLiteral,
    EventPopoverContextType,
    ContentAlignType,
    EventLabelType,
    EventIconType,
    type EventLabel,
    type EventIcon,
    type ContentAlignLiteral,
} from "./types.js";

// ============================================================================
// Planner Row Type
// ============================================================================

/**
 * East type for an Planner row.
 *
 * @remarks
 * Each row has table cells (displayed on the left) and events (displayed on the right as slots).
 *
 * @property cells - Dict of column key to cell content (same as Table)
 * @property events - Array of events (with optional popover content)
 */
export const PlannerRowType = StructType({
    cells: DictType(StringType, TableCellType),
    events: ArrayType(PlannerEventType),
});

/**
 * Type representing the Planner row structure.
 */
export type PlannerRowType = typeof PlannerRowType;

// ============================================================================
// Planner Root Type
// ============================================================================

/**
 * Type for Planner component data.
 *
 * @remarks
 * Planner displays rows with integer-based events (slots).
 * The slot range is derived from the events' domain, with optional min/max overrides.
 *
 * @property rows - Array of Planner rows
 * @property columns - Array of column definitions (same as Table)
 * @property style - Optional styling configuration
 * @property eventPopover - Optional function to render popover content for events
 */
export const PlannerRootType = StructType({
    rows: ArrayType(PlannerRowType),
    columns: ArrayType(TableColumnType),
    style: OptionType(PlannerStyleType),
    eventPopover: OptionType(FunctionType([EventPopoverContextType], UIComponentType)),
});

/**
 * Type representing the Planner structure.
 */
export type PlannerRootType = typeof PlannerRootType;

// ============================================================================
// Event Input Interface
// ============================================================================

/**
 * Input interface for creating a Planner event.
 *
 * @remarks
 * This interface provides an ergonomic way to create events
 * by accepting both plain values and East expressions.
 *
 * @property start - Start slot (or single slot if mode=single)
 * @property end - End slot (only used if mode=span)
 * @property label - Optional label configuration
 * @property icon - Optional icon configuration
 * @property colorPalette - Optional color scheme for the event background
 * @property background - Optional background color (overrides colorPalette)
 * @property stroke - Optional stroke/border color (overrides colorPalette)
 * @property opacity - Optional opacity (0-1)
 */
export interface EventInput {
    /** Start slot (or single slot if mode=single) */
    start: SubtypeExprOrValue<FloatType>;
    /** End slot (only used if mode=span) */
    end?: SubtypeExprOrValue<FloatType>;
    /** Optional label configuration */
    label?: EventLabel;
    /** Optional icon configuration */
    icon?: EventIcon;
    /** Color scheme for the event background */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Background/fill color (overrides colorPalette) */
    background?: SubtypeExprOrValue<StringType>;
    /** Stroke/border color (overrides colorPalette) */
    stroke?: SubtypeExprOrValue<StringType>;
    /** Opacity (0-1) */
    opacity?: SubtypeExprOrValue<FloatType>;
}

// ============================================================================
// Event Factory Function
// ============================================================================

/**
 * Creates a Planner event.
 *
 * @param input - Event configuration
 * @returns An East expression representing the Planner event
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Planner, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Planner.Root(
 *         [{ name: "Alice", slot: 1n }],
 *         ["name"],
 *         row => [Planner.Event({
 *             start: row.slot,
 *             end: row.slot.add(2n),
 *             label: { value: "Task" },
 *             colorPalette: "blue",
 *         })]
 *     );
 * });
 * ```
 */
function createEvent(input: EventInput): ExprType<PlannerEventType> {
    // Build event colorPalette
    const colorPaletteValue = input.colorPalette
        ? (typeof input.colorPalette === "string"
            ? East.value(variant(input.colorPalette as any, null), ColorSchemeType)
            : input.colorPalette)
        : undefined;

    // Build label object if provided
    let labelValue = undefined;
    if (input.label) {
        const labelAlignValue = input.label.align
            ? (typeof input.label.align === "string"
                ? East.value(variant(input.label.align, null), ContentAlignType)
                : input.label.align)
            : undefined;

        const labelVerticalAlignValue = input.label.verticalAlign
            ? (typeof input.label.verticalAlign === "string"
                ? East.value(variant(input.label.verticalAlign, null), ContentAlignType)
                : input.label.verticalAlign)
            : undefined;

        const labelFontWeightValue = input.label.fontWeight
            ? (typeof input.label.fontWeight === "string"
                ? East.value(variant(input.label.fontWeight as any, null), FontWeightType)
                : input.label.fontWeight)
            : undefined;

        const labelFontStyleValue = input.label.fontStyle
            ? (typeof input.label.fontStyle === "string"
                ? East.value(variant(input.label.fontStyle as any, null), FontStyleType)
                : input.label.fontStyle)
            : undefined;

        const labelFontSizeValue = input.label.fontSize
            ? (typeof input.label.fontSize === "string"
                ? East.value(variant(input.label.fontSize as any, null), SizeType)
                : input.label.fontSize)
            : undefined;

        labelValue = East.value({
            value: input.label.value,
            align: labelAlignValue ? variant("some", labelAlignValue) : variant("none", null),
            verticalAlign: labelVerticalAlignValue ? variant("some", labelVerticalAlignValue) : variant("none", null),
            color: input.label.color ? variant("some", input.label.color) : variant("none", null),
            fontWeight: labelFontWeightValue ? variant("some", labelFontWeightValue) : variant("none", null),
            fontStyle: labelFontStyleValue ? variant("some", labelFontStyleValue) : variant("none", null),
            fontSize: labelFontSizeValue ? variant("some", labelFontSizeValue) : variant("none", null),
        }, EventLabelType);
    }

    // Build icon object if provided
    let iconValue = undefined;
    if (input.icon) {
        const iconAlignValue = input.icon.align
            ? (typeof input.icon.align === "string"
                ? East.value(variant(input.icon.align, null), ContentAlignType)
                : input.icon.align)
            : undefined;

        const iconSizeValue = input.icon.size
            ? (typeof input.icon.size === "string"
                ? East.value(variant(input.icon.size as any, null), IconSizeType)
                : input.icon.size)
            : undefined;

        const iconColorPaletteValue = input.icon.colorPalette
            ? (typeof input.icon.colorPalette === "string"
                ? East.value(variant(input.icon.colorPalette as any, null), ColorSchemeType)
                : input.icon.colorPalette)
            : undefined;

        iconValue = East.value({
            prefix: input.icon.prefix,
            name: input.icon.name,
            align: iconAlignValue ? variant("some", iconAlignValue) : variant("none", null),
            size: iconSizeValue ? variant("some", iconSizeValue) : variant("none", null),
            color: input.icon.color ? variant("some", input.icon.color) : variant("none", null),
            colorPalette: iconColorPaletteValue ? variant("some", iconColorPaletteValue) : variant("none", null),
        }, EventIconType);
    }

    return East.value({
        start: input.start,
        end: input.end ? variant("some", input.end) : variant("none", null),
        label: labelValue ? variant("some", labelValue) : variant("none", null),
        icon: iconValue ? variant("some", iconValue) : variant("none", null),
        colorPalette: colorPaletteValue ? variant("some", colorPaletteValue) : variant("none", null),
        background: input.background ? variant("some", input.background) : variant("none", null),
        stroke: input.stroke ? variant("some", input.stroke) : variant("none", null),
        opacity: input.opacity ? variant("some", input.opacity) : variant("none", null),
    }, PlannerEventType);
}

// ============================================================================
// Column Configuration
// ============================================================================

// Helper types to extract struct fields from array data type
type ExtractStructFields<T> = T extends ArrayType<infer S>
    ? S extends StructType
    ? S["fields"]
    : never
    : never;

type ExtractElement<T> = T extends ArrayType<infer E> ? E : never;

// Helper type to extract the row element type from an array type (always StructType due to constraint)
type ExtractRowType<T> = T extends ArrayType<infer S>
    ? S extends StructType
    ? S
    : StructType
    : StructType;

type DataFields<T extends SubtypeExprOrValue<ArrayType<StructType>>> = ExtractStructFields<TypeOf<T>>;

type RowElement<T extends SubtypeExprOrValue<ArrayType<StructType>>> = ExtractElement<TypeOf<T>>;

type DataRowType<T extends SubtypeExprOrValue<ArrayType<StructType>>> = ExtractRowType<TypeOf<T>>;

// Column specification can be array of keys or object config
type ColumnSpec<T extends SubtypeExprOrValue<ArrayType<StructType>>> =
    | (keyof DataFields<NoInfer<T>>)[]
    | { [K in keyof DataFields<NoInfer<T>>]?: TableColumnConfig<DataFields<NoInfer<T>>[K], DataRowType<NoInfer<T>>> };

// ============================================================================
// Main Planner Factory
// ============================================================================

/**
 * Creates an Planner component following the Table/Gantt pattern.
 *
 * @typeParam T - The struct type of each data row
 * @param data - Array of data structs
 * @param columns - Column specification for the left-side table columns
 * @param events - Function to extract events from each row
 * @param style - Optional Planner styling
 * @returns An East expression representing the Planner component
 *
 * @example
 * ```ts
 * import { East, IntegerType, StringType } from "@elaraai/east";
 * import { Planner, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Planner.Root(
 *         [
 *             { name: "Alice", start: 1n, end: 3n },
 *             { name: "Bob", start: 2n, end: 5n },
 *         ],
 *         ["name"],
 *         row => [Planner.Event({ start: row.start, end: row.end })],
 *         {
 *             slotLabel: East.function([IntegerType], StringType, ($, slot) => {
 *                 return East.str`Day ${slot}`;
 *             }),
 *         }
 *     );
 * });
 * ```
 */
function createPlanner<T extends SubtypeExprOrValue<ArrayType<StructType>>>(
    data: T,
    columns: ColumnSpec<T>,
    events: (row: ExprType<RowElement<T>>) => SubtypeExprOrValue<ArrayType<PlannerEventType>>,
    style?: PlannerStyle,
    eventPopover?: SubtypeExprOrValue<FunctionType<[EventPopoverContextType], UIComponentType>>
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

    // Map each data row to an PlannerRow with cells and events
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
        const row_events = $.let(events(datum as any), ArrayType(PlannerEventType));

        return East.value({
            cells: cells,
            events: row_events,
        }, PlannerRowType);
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

    const slotModeValue = style?.slotMode
        ? (typeof style.slotMode === "string"
            ? East.value(variant(style.slotMode, null), SlotModeType)
            : style.slotMode)
        : undefined;

    const colorPaletteValue = style?.colorPalette
        ? (typeof style.colorPalette === "string"
            ? East.value(variant(style.colorPalette as any, null), ColorSchemeType)
            : style.colorPalette)
        : undefined;

    const eventPopoverTriggerValue = style?.eventPopoverTrigger
        ? (typeof style.eventPopoverTrigger === "string"
            ? East.value(variant(style.eventPopoverTrigger, null), EventPopoverTriggerType)
            : style.eventPopoverTrigger)
        : undefined;

    const styleValue = style ? East.value({
        variant: variantValue ? some(variantValue) : none,
        size: sizeValue ? some(sizeValue) : none,
        striped: style.striped !== undefined ? some(style.striped) : none,
        interactive: style.interactive !== undefined ? some(style.interactive) : none,
        stickyHeader: style.stickyHeader !== undefined ? some(style.stickyHeader) : none,
        showColumnBorder: style.showColumnBorder !== undefined ? some(style.showColumnBorder) : none,
        slotMode: slotModeValue ? some(slotModeValue) : none,
        minSlot: style.minSlot !== undefined ? some(style.minSlot) : none,
        maxSlot: style.maxSlot !== undefined ? some(style.maxSlot) : none,
        stepSize: style.stepSize !== undefined ? some(style.stepSize) : none,
        slotLabel: style.slotLabel ? some(style.slotLabel) : none,
        slotMinWidth: style.slotMinWidth ? some(style.slotMinWidth) : none,
        colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
        readOnly: style.readOnly !== undefined ? some(style.readOnly) : none,
        eventPopoverTrigger: eventPopoverTriggerValue ? some(eventPopoverTriggerValue) : none,
        slotLineStroke: style.slotLineStroke ? some(style.slotLineStroke) : none,
        slotLineWidth: style.slotLineWidth !== undefined ? some(style.slotLineWidth) : none,
        slotLineDash: style.slotLineDash ? some(style.slotLineDash) : none,
        slotLineOpacity: style.slotLineOpacity !== undefined ? some(style.slotLineOpacity) : none,
        boundaries: style.boundaries ? some(style.boundaries.map(b => East.value({
            x: b.x,
            stroke: b.stroke ? some(b.stroke) : none,
            strokeWidth: b.strokeWidth !== undefined ? some(b.strokeWidth) : none,
            strokeDash: b.strokeDash ? some(b.strokeDash) : none,
            strokeOpacity: b.strokeOpacity !== undefined ? some(b.strokeOpacity) : none,
        }, PlannerBoundaryType))) : none,
        onCellClick: style.onCellClick ? some(style.onCellClick) : none,
        onCellDoubleClick: style.onCellDoubleClick ? some(style.onCellDoubleClick) : none,
        onRowClick: style.onRowClick ? some(style.onRowClick) : none,
        onRowDoubleClick: style.onRowDoubleClick ? some(style.onRowDoubleClick) : none,
        onSortChange: style.onSortChange ? some(style.onSortChange) : none,
        onEventClick: style.onEventClick ? some(style.onEventClick) : none,
        onEventDoubleClick: style.onEventDoubleClick ? some(style.onEventDoubleClick) : none,
        onEventDrag: style.onEventDrag ? some(style.onEventDrag) : none,
        onEventResize: style.onEventResize ? some(style.onEventResize) : none,
        onEventAdd: style.onEventAdd ? some(style.onEventAdd) : none,
        onEventEdit: style.onEventEdit ? some(style.onEventEdit) : none,
        onEventDelete: style.onEventDelete ? some(style.onEventDelete) : none,
    }, PlannerStyleType) : undefined;

    const eventPopoverExpr = eventPopover ?
      some(East.value(eventPopover, FunctionType([EventPopoverContextType], UIComponentType))) :
      none;

    return East.value(variant("Planner", {
        rows: rows_mapped,
        columns: columns_mapped as ValueTypeOf<typeof PlannerRootType>["columns"],
        style: styleValue ? some(styleValue) : none,
        eventPopover: eventPopoverExpr,
    }), UIComponentType);
}

// ============================================================================
// Namespace Export
// ============================================================================

/** Type for the Planner namespace */
interface PlannerNamespace {
    Root: typeof createPlanner;
    Event: typeof createEvent;
    Types: {
        Root: typeof PlannerRootType;
        Row: typeof PlannerRowType;
        Event: typeof PlannerEventType;
        EventLabel: typeof EventLabelType;
        EventIcon: typeof EventIconType;
        ContentAlign: typeof ContentAlignType;
        Style: typeof PlannerStyleType;
        SlotMode: typeof SlotModeType;
        Boundary: typeof PlannerBoundaryType;
        ClickEvent: typeof EventClickEventType;
        DragEvent: typeof EventDragEventType;
        ResizeEvent: typeof EventResizeEventType;
        DeleteEvent: typeof EventDeleteEventType;
        EventPopoverTrigger: typeof EventPopoverTriggerType;
        EventPopoverContext: typeof EventPopoverContextType;
        Column: typeof TableColumnType;
        Cell: typeof TableCellType;
    };
}

/**
 * Planner namespace for creating integer-slot-based scheduling components.
 *
 * @remarks
 * Planner displays rows with integer-based events (slots).
 * Each row has table columns on the left and a slot grid with events on the right.
 * The API follows the Table/Gantt pattern for column configuration.
 */
export const Planner: PlannerNamespace = {
    /**
     * Creates an Planner component following the Table/Gantt pattern.
     *
     * @typeParam T - The struct type of each data row
     * @param data - Array of data structs
     * @param columns - Column specification for the left-side table columns
     * @param events - Function to extract events from each row
     * @param style - Optional Planner styling
     * @returns An East expression representing the Planner component
     *
     * @remarks
     * Planner displays rows with integer-based events (slots).
     * Each row has table columns on the left and a slot grid with events on the right.
     * The slot range is derived from event data with optional min/max overrides.
     *
     * @example
     * ```ts
     * import { East, IntegerType, StringType } from "@elaraai/east";
     * import { Planner, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Planner.Root(
     *         [
     *             { name: "Alice", start: 1n, end: 3n },
     *             { name: "Bob", start: 2n, end: 5n },
     *         ],
     *         ["name"],
     *         row => [Planner.Event({ start: row.start, end: row.end })],
     *         {
     *             slotLabel: East.function([IntegerType], StringType, ($, slot) => {
     *                 return East.str`Day ${slot}`;
     *             }),
     *         }
     *     );
     * });
     * ```
     */
    Root: createPlanner,
    /**
     * Creates a Planner event.
     *
     * @param input - Event configuration with start, end, label, colorPalette
     * @returns An East expression representing the Planner event
     */
    Event: createEvent,
    Types: {
        /**
         * Type for Planner component data.
         *
         * @property rows - Array of Planner rows
         * @property columns - Array of column definitions
         * @property style - Optional styling configuration
         */
        Root: PlannerRootType,
        /**
         * East type for an Planner row.
         *
         * @property cells - Dict of column key to cell content
         * @property events - Array of events
         */
        Row: PlannerRowType,
        /**
         * Event data for Planner.
         *
         * @property start - Start slot
         * @property end - End slot (optional, for span mode)
         * @property label - Optional label configuration
         * @property icon - Optional icon configuration
         * @property colorPalette - Optional color scheme
         */
        Event: PlannerEventType,
        /**
         * Label configuration for Planner events.
         *
         * @property value - The label text (required)
         * @property align - Position within the event (start, center, end)
         * @property color - Text color
         * @property fontWeight - Font weight
         * @property fontStyle - Font style
         * @property fontSize - Font size
         */
        EventLabel: EventLabelType,
        /**
         * Icon configuration for Planner events.
         *
         * @property prefix - Font Awesome prefix (fas, far, fab, etc.)
         * @property name - Font Awesome icon name
         * @property align - Position within the event (start, center, end)
         * @property size - Icon size
         * @property color - Icon color
         * @property colorPalette - Color scheme for the icon
         */
        EventIcon: EventIconType,
        /**
         * Alignment for content within an event.
         *
         * @property start - Align to the start (left)
         * @property center - Align to center
         * @property end - Align to the end (right)
         */
        ContentAlign: ContentAlignType,
        /**
         * Style type for the Planner component.
         */
        Style: PlannerStyleType,
        /**
         * Slot mode variant type.
         *
         * @property single - Each event occupies one slot
         * @property span - Events span from start to end
         */
        SlotMode: SlotModeType,
        /**
         * Boundary data for vertical lines at specific slot positions.
         *
         * @property x - Slot position for the boundary line
         * @property stroke - Line color
         * @property strokeWidth - Line width in pixels
         * @property strokeDash - Dash pattern
         * @property strokeOpacity - Line opacity (0-1)
         */
        Boundary: PlannerBoundaryType,
        /**
         * Event data for event click events.
         */
        ClickEvent: EventClickEventType,
        /**
         * Event data for event drag (move) events.
         */
        DragEvent: EventDragEventType,
        /**
         * Event data for event resize events.
         */
        ResizeEvent: EventResizeEventType,
        /**
         * Event data for event delete events.
         */
        DeleteEvent: EventDeleteEventType,
        /**
         * Trigger variant type for event popover.
         *
         * @property click - Popover appears when event is clicked
         * @property hover - Popover appears when hovering over event
         */
        EventPopoverTrigger: EventPopoverTriggerType,
        /**
         * Context passed to the eventPopover function.
         *
         * @property rowIndex - Row index (0-based)
         * @property eventIndex - Event index within the row
         * @property start - Start slot of the event
         * @property end - End slot of the event
         * @property label - Event label (if any)
         * @property colorPalette - Event color palette (if any)
         */
        EventPopoverContext: EventPopoverContextType,
        /**
         * East type for a table column definition.
         */
        Column: TableColumnType,
        /**
         * East type for a table cell.
         */
        Cell: TableCellType,
    },
};
