# Planner Component Design

## Overview

Planner is a grid-based scheduling component similar to Gantt but with an **integer axis** instead of dates. It displays rows with events that occupy slots (integer positions) on a horizontal axis.

## Key Differences from Gantt

| Feature | Gantt | Planner |
|---------|-------|--------------|
| X-axis | DateTime | Integer |
| Range | Derived from events + optional min/max dates | Derived from events + optional minSlot/maxSlot |
| Events | Task (span) or Milestone (point) | Event (configurable: single slot or span via slotMode) |
| Axis labels | Auto-formatted dates | Custom `FunctionType([IntegerType], StringType)` |
| Drag behavior | Move + resize with time snapping | Move + resize with slot snapping |
| Viewport | Dynamic zoom/pan | Always shows all slots, min-width with scroll |

## Use Cases

- Resource allocation grids (slots = resources or time periods)
- Shift scheduling (slots = shift numbers)
- Capacity planning (slots = capacity units)
- Step-based workflows (slots = workflow steps)
- Game/simulation turn planners (slots = turns)

## Component Structure

### Types

```typescript
// Slot mode - determines if events span multiple slots or occupy single slot
export const SlotModeType = VariantType({
    single: NullType,  // Each event occupies exactly one slot
    span: NullType,    // Events span from start to end slot (inclusive)
});

// Event type - simpler than Gantt (no milestone variant needed)
export const PlannerEventType = StructType({
    start: IntegerType,                    // Start slot (or single slot if mode=single)
    end: OptionType(IntegerType),          // End slot (only used if mode=span)
    label: OptionType(StringType),         // Optional label displayed on event
    colorPalette: OptionType(ColorSchemeType), // Optional color
});

// Row type - similar to Gantt
export const PlannerRowType = StructType({
    cells: DictType(StringType, TableCellType),  // Left-side table columns
    events: ArrayType(PlannerEventType),     // Events in this row
});

// Style type
export const PlannerStyleType = StructType({
    // Table styling (reused from Gantt/Table)
    variant: OptionType(TableVariantType),
    size: OptionType(TableSizeType),
    striped: OptionType(BooleanType),
    interactive: OptionType(BooleanType),
    stickyHeader: OptionType(BooleanType),
    showColumnBorder: OptionType(BooleanType),

    // Planner-specific
    slotMode: OptionType(SlotModeType),           // single or span (default: span)
    minSlot: OptionType(IntegerType),             // Optional min slot override (else derived from data)
    maxSlot: OptionType(IntegerType),             // Optional max slot override (else derived from data)
    slotLabel: OptionType(FunctionType([IntegerType], StringType)),  // Custom slot labels (required for display)
    slotMinWidth: OptionType(StringType),          // Min width per slot (CSS value, default "60px")
    colorPalette: OptionType(ColorSchemeType),     // Default event color

    // Slot line styling (vertical grid lines)
    slotLineStroke: OptionType(StringType),        // Line color (CSS color or Chakra token)
    slotLineWidth: OptionType(FloatType),          // Line width in pixels
    slotLineDash: OptionType(StringType),          // Dash pattern (e.g., "4 2" for dashed)
    slotLineOpacity: OptionType(FloatType),        // Line opacity (0-1)

    // Callbacks
    onCellClick: OptionType(FunctionType([TableCellClickEventType], NullType)),
    onRowClick: OptionType(FunctionType([TableRowClickEventType], NullType)),
    onEventClick: OptionType(FunctionType([EventClickEventType], NullType)),
    onEventDoubleClick: OptionType(FunctionType([EventClickEventType], NullType)),
    onEventDrag: OptionType(FunctionType([EventDragEventType], NullType)),       // Move event
    onEventResize: OptionType(FunctionType([EventResizeEventType], NullType)),   // Resize event
});
```

### Callback Event Types

```typescript
// Event click
export const EventClickEventType = StructType({
    rowIndex: IntegerType,
    eventIndex: IntegerType,
    start: IntegerType,
    end: IntegerType,           // Same as start if single-slot mode
});

// Event drag (move)
export const EventDragEventType = StructType({
    rowIndex: IntegerType,
    eventIndex: IntegerType,
    previousStart: IntegerType,
    previousEnd: IntegerType,
    newStart: IntegerType,
    newEnd: IntegerType,
});

// Event resize
export const EventResizeEventType = StructType({
    rowIndex: IntegerType,
    eventIndex: IntegerType,
    previousStart: IntegerType,
    previousEnd: IntegerType,
    newStart: IntegerType,
    newEnd: IntegerType,
    edge: VariantType({ start: NullType, end: NullType }),  // Which edge was dragged
});
```

## API Design

### Factory Functions

```typescript
// Create an event
Planner.Event({
    start: 1,
    end: 4,              // Optional - only for span mode
    label: "Task A",
    colorPalette: "blue",
})

// Create the component
Planner.Root(
    data,                // Array of row data
    columns,             // Column spec (same as Table/Gantt)
    row => [...events],  // Event builder function
    {
        // Range derived from event data, but can override:
        minSlot: 1n,                        // Optional: force minimum slot
        maxSlot: 10n,                       // Optional: force maximum slot
        slotMode: "span",                   // or "single"
        slotLabel: East.function([IntegerType], StringType, ($, slot) => {
            return East.str`Day ${slot}`;   // Custom labels (FunctionType)
        }),
        slotMinWidth: "80px",
        colorPalette: "blue",
        onEventDrag: event => { ... },
        onEventResize: event => { ... },
    }
)
```

### Usage Examples

#### Basic Usage (Span Mode)

```typescript
const schedule = Planner.Root(
    [
        { name: "Alice", task1Start: 1n, task1End: 3n },
        { name: "Bob", task1Start: 2n, task1End: 5n },
    ],
    ["name"],
    row => [
        Planner.Event({
            start: row.task1Start,
            end: row.task1End,
            label: "Working",
            colorPalette: "blue",
        }),
    ],
    {
        // Range auto-derived from events (1-5), but we can expand it:
        maxSlot: 7n,
        slotLabel: East.function([IntegerType], StringType, ($, slot) => {
            return East.str`Day ${slot}`;
        }),
    }
);
```

#### Single Slot Mode

```typescript
const allocation = Planner.Root(
    resources,
    ["name", "type"],
    row => row.allocations.map(($, slot) =>
        Planner.Event({
            start: slot,
            label: "Allocated",
            colorPalette: "green",
        })
    ),
    {
        minSlot: 1n,
        maxSlot: 12n,
        slotMode: "single",
        slotLabel: East.function([IntegerType], StringType, ($, slot) => {
            return East.str`Slot ${slot}`;
        }),
    }
);
```

#### With Callbacks

```typescript
const planner = Planner.Root(
    data,
    ["name"],
    row => [...],
    {
        minSlot: 0n,
        maxSlot: 23n,
        slotLabel: East.function([IntegerType], StringType, ($, slot) => {
            return East.str`${slot}:00`;
        }),
        slotMinWidth: "50px",
        onEventDrag: East.function([Planner.Types.DragEvent], NullType, ($, event) => {
            // Handle event move
            $(console.log(East.str`Moved from ${event.previousStart} to ${event.newStart}`));
            return null;
        }),
        onEventResize: East.function([Planner.Types.ResizeEvent], NullType, ($, event) => {
            // Handle event resize
            $(console.log(East.str`Resized: ${event.newStart} to ${event.newEnd}`));
            return null;
        }),
    }
);
```

## Visual Design

```
┌─────────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│  Name   │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  <- Slot labels (customizable)
├─────────┼─────┴─────┴─────┼─────┴─────┼─────┼─────┤
│  Alice  │ ████████████████│           │     │     │  <- Event spans slots 1-3
├─────────┼─────┼─────┬─────┴─────┴─────┴─────┼─────┤
│  Bob    │     │ ████████████████████████████│     │  <- Event spans slots 2-6
├─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│  Carol  │ ████│     │ ████│     │ ████│     │     │  <- Multiple single-slot events
└─────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

### Interaction

- **Drag to move**: Click and drag event to move it horizontally (snaps to slots)
- **Resize**: Drag left/right edges to expand/contract the event
- **Multiple events**: Events can overlap/stack within the same slot (rendered with slight vertical offset or stacking)

### Scrolling

- All slots are always rendered (no dynamic viewport like Gantt)
- `slotMinWidth` ensures each slot has minimum width
- Horizontal scroll appears when total width exceeds container

## Implementation Notes

### Renderer (React/Chakra)

The renderer should:
1. **Derive slot range**: Scan all events to find min/max slots, then apply optional minSlot/maxSlot overrides
2. **Calculate total grid width**: `slotCount * slotMinWidth`
3. **Render header row**: Call `slotLabel` function for each slot to get display text
4. For each row, render table cells (left) + event grid (right)
5. Events positioned absolutely within the grid based on start/end slots
6. Handle drag/resize with pointer events, snapping to nearest slot

### Differences from Gantt Renderer

- Integer math instead of time-based calculations (simpler)
- No dynamic viewport/zoom (always show all slots in derived range)
- Simpler snapping logic (integer slots vs time units)
- Events as filled cells rather than floating bars (more grid-like appearance)
- `slotLabel` is a FunctionType that must be called at render time for each slot

## File Structure

```
src/collections/event-planner/
  index.ts      # Planner namespace, factory functions
  types.ts      # PlannerEventType, PlannerStyleType, etc.
```

## Namespace Export

```typescript
export const Planner = {
    Root: createPlanner,
    Event: createEvent,
    Types: {
        Root: PlannerRootType,
        Row: PlannerRowType,
        Event: PlannerEventType,
        Style: PlannerStyleType,
        SlotMode: SlotModeType,
        ClickEvent: EventClickEventType,
        DragEvent: EventDragEventType,
        ResizeEvent: EventResizeEventType,
    },
} as const;
```
