---
name: east-ui
description: "Type-safe UI component library for the East language. Use when writing East programs that define user interfaces with declarative components. Triggers for: (1) Writing East programs with @elaraai/east-ui, (2) Creating layouts with Box, Flex, Stack, Grid, (3) Forms with Input, Select, Checkbox, Switch, Slider, (4) Data display with Table, TreeView, DataList, Gantt, Planner, (5) Charts with Chart.Line, Chart.Bar, Chart.Area, Chart.Pie, Chart.Scatter, (6) Overlays with Dialog, Drawer, Popover, Menu, Tooltip, (7) State management with State.readTyped, State.writeTyped."
---

# East UI

Type-safe UI component library for the East language. Components return data structures describing UI layouts, enabling portable rendering across environments.

## Quick Start

```typescript
import { East } from "@elaraai/east";
import { Stack, Text, Button, UIComponentType } from "@elaraai/east-ui";

const MyComponent = East.function([], UIComponentType, $ => {
    return Stack.VStack([
        Text.Root("Hello, World!", { fontSize: "lg", fontWeight: "bold" }),
        Button.Root("Click Me", { variant: "solid", colorPalette: "blue" }),
    ], { gap: "4" });
});

const ir = MyComponent.toIR();
```

## Decision Tree: Which Component to Use

```
Task → What do you need?
    │
    ├─ Layout (arrange content)
    │   ├─ Box → .Root() - basic container with padding, margin, bg
    │   ├─ Flex → .Root() - flexbox with direction, justify, align
    │   ├─ Stack → .HStack(), .VStack() - simplified horizontal/vertical stacking
    │   ├─ Grid → .Root() - CSS grid with templateColumns, templateRows
    │   ├─ Separator → .Root() - visual divider (horizontal/vertical)
    │   └─ Splitter → .Root() - resizable panels
    │
    ├─ Typography (display text)
    │   ├─ Text → .Root() - basic text with fontSize, fontWeight, color
    │   ├─ Heading → .Root() - semantic heading with size (h1-h6)
    │   ├─ Code → .Root() - inline code
    │   ├─ CodeBlock → .Root() - syntax-highlighted code block
    │   ├─ Link → .Root() - clickable hyperlink
    │   ├─ Highlight → .Root() - highlighted text span
    │   ├─ Mark → .Root() - marked/annotated text
    │   └─ List → .Ordered(), .Unordered() - bulleted or numbered lists
    │
    ├─ Buttons (user actions)
    │   ├─ Button → .Root() - clickable button with variant, colorPalette, onClick
    │   └─ IconButton → .Root() - icon-only button
    │
    ├─ Forms (user input)
    │   ├─ Input → .String(), .Integer(), .Float(), .DateTime() - typed text inputs
    │   ├─ Textarea → .Root() - multi-line text input
    │   ├─ Select → .Root() - dropdown selection
    │   ├─ Checkbox → .Root() - boolean checkbox
    │   ├─ Switch → .Root() - toggle switch
    │   ├─ Slider → .Root() - range slider with min, max, step
    │   ├─ Field → .Root() - form field wrapper with label, error
    │   ├─ FileUpload → .Root() - file upload input
    │   └─ TagsInput → .Root() - tag input with add/remove
    │
    ├─ Collections (display data sets)
    │   ├─ Table → .Root() - data table with columns, sorting, selection
    │   ├─ DataList → .Root() - generic data list with items
    │   ├─ TreeView → .Root() - hierarchical tree with expand/collapse
    │   ├─ Gantt → .Root() - Gantt chart for scheduling/timelines
    │   └─ Planner → .Root() - event planner/calendar
    │
    ├─ Charts (visualize data)
    │   ├─ Cartesian Charts
    │   │   ├─ Chart.Line(), .LineMulti() - line chart (single/multi series)
    │   │   ├─ Chart.Bar(), .BarMulti() - bar chart (single/multi series)
    │   │   ├─ Chart.Area(), .AreaMulti() - area chart (single/multi series)
    │   │   └─ Chart.Scatter(), .ScatterMulti() - scatter plot (single/multi series)
    │   ├─ Proportional Charts
    │   │   ├─ Chart.Pie() - pie/donut chart
    │   │   └─ Chart.Radar() - radar/spider chart
    │   ├─ Native Charts
    │   │   ├─ Chart.BarList() - horizontal bar list
    │   │   └─ Chart.BarSegment() - segmented bar
    │   └─ Sparkline → inline trend visualization
    │
    ├─ Display (show information)
    │   ├─ Badge → .Root() - small badge label
    │   ├─ Tag → .Root() - tag with optional close button
    │   ├─ Avatar → .Root() - user avatar image/initials
    │   ├─ Icon → .Root() - FontAwesome or custom icon
    │   └─ Stat → .Root() - statistic with label, value, change
    │
    ├─ Feedback (user feedback)
    │   ├─ Alert → .Root() - alert message (info, success, warning, error)
    │   └─ Progress → .Root() - progress bar or circular progress
    │
    ├─ Disclosure (reveal content)
    │   ├─ Accordion → .Root() - expandable sections
    │   ├─ Tabs → .Root() - tabbed interface
    │   └─ Carousel → .Root() - image carousel
    │
    ├─ Overlays (floating content)
    │   ├─ Dialog → .Root() - modal dialog with actions
    │   ├─ Drawer → .Root() - side drawer panel
    │   ├─ Popover → .Root() - positioned popover
    │   ├─ Tooltip → .Root() - hover tooltip
    │   ├─ Menu → .Root() - context/dropdown menu
    │   ├─ HoverCard → .Root() - hover-triggered card
    │   ├─ ActionBar → .Root() - bottom action bar
    │   └─ ToggleTip → .Root() - toggle-triggered tooltip
    │
    ├─ Container (content wrapper)
    │   └─ Card → .Root() - card with header, body, footer
    │
    └─ State (reactive data)
        ├─ State.readTyped(key, type) - read typed state
        ├─ State.writeTyped(key, option, type) - write typed state
        ├─ State.initTyped(key, value, type) - initialize if not exists
        └─ State.has(key) - check if key exists
```

## Common Types

| Type | Definition | Description |
|------|------------|-------------|
| `UIComponentType` | `VariantType({ box, flex, text, button, ... })` | Recursive type for all UI components |
| `SizeType` | `VariantType({ xs, sm, md, lg, xl })` | Component size |
| `ColorSchemeType` | `VariantType({ gray, red, green, blue, ... })` | Color palette |
| `FontWeightType` | `VariantType({ normal, medium, semibold, bold })` | Text weight |
| `FlexDirectionType` | `VariantType({ row, column, row-reverse, column-reverse })` | Flex direction |
| `JustifyContentType` | `VariantType({ flex-start, flex-end, center, space-between, ... })` | Flex justify |
| `AlignItemsType` | `VariantType({ flex-start, flex-end, center, stretch })` | Flex align |

## Reference Documentation

- **[API Reference](./reference/api.md)** - Complete component signatures, props, and style types
- **[Examples](./reference/examples.md)** - Working code examples by use case
- **[Full Usage Guide](./USAGE.md)** - Comprehensive developer guide

## Available Components

| Category | Components |
|----------|------------|
| Layout | `Box`, `Flex`, `Stack`, `Grid`, `Separator`, `Splitter` |
| Typography | `Text`, `Heading`, `Code`, `CodeBlock`, `Link`, `Highlight`, `Mark`, `List` |
| Buttons | `Button`, `IconButton` |
| Forms | `Input`, `Textarea`, `Select`, `Checkbox`, `Switch`, `Slider`, `Field`, `FileUpload`, `TagsInput` |
| Collections | `Table`, `DataList`, `TreeView`, `Gantt`, `Planner` |
| Charts | `Chart.Line/Bar/Area/Scatter/Pie/Radar/BarList/BarSegment`, `Sparkline` |
| Display | `Badge`, `Tag`, `Avatar`, `Icon`, `Stat` |
| Feedback | `Alert`, `Progress` |
| Disclosure | `Accordion`, `Tabs`, `Carousel` |
| Overlays | `Dialog`, `Drawer`, `Popover`, `Tooltip`, `Menu`, `HoverCard`, `ActionBar`, `ToggleTip` |
| Container | `Card` |
| State | `State.readTyped`, `State.writeTyped`, `State.initTyped`, `State.has` |

## Common Patterns

### Basic Layout with Stack

```typescript
import { Stack, Text, Button, UIComponentType } from "@elaraai/east-ui";

const layout = East.function([], UIComponentType, $ => {
    return Stack.VStack([
        Text.Root("Title", { fontSize: "xl", fontWeight: "bold" }),
        Text.Root("Description text here"),
        Stack.HStack([
            Button.Root("Cancel", { variant: "outline" }),
            Button.Root("Submit", { variant: "solid", colorPalette: "blue" }),
        ], { gap: "2" }),
    ], { gap: "4", padding: "6" });
});
```

### Form with State

```typescript
import { East, IntegerType, variant } from "@elaraai/east";
import { Stack, Input, Button, Text, State, UIComponentType } from "@elaraai/east-ui";

const counter = East.function([], UIComponentType, $ => {
    $(State.initTyped("count", 0n, IntegerType)());
    const count = $.let($(State.readTyped("count", IntegerType)()));

    return Stack.VStack([
        Text.Root(East.str`Count: ${count.unwrap("some")}`, { fontSize: "lg" }),
        Button.Root("Increment", {
            colorPalette: "blue",
            onClick: (_$) => {
                $(_$.exec(State.writeTyped("count", variant("some", count.unwrap("some").add(1n)), IntegerType)()));
            },
        }),
    ], { gap: "4" });
});
```

### Data Table

```typescript
import { Table, UIComponentType } from "@elaraai/east-ui";

const dataTable = East.function([], UIComponentType, $ => {
    return Table.Root(
        [
            { id: 1n, name: "Alice", email: "alice@example.com" },
            { id: 2n, name: "Bob", email: "bob@example.com" },
        ],
        [
            { header: "ID", accessorKey: "id" },
            { header: "Name", accessorKey: "name" },
            { header: "Email", accessorKey: "email" },
        ],
        { variant: "line", showColumnBorder: true }
    );
});
```

### Line Chart

```typescript
import { Chart, UIComponentType } from "@elaraai/east-ui";

const chart = East.function([], UIComponentType, $ => {
    return Chart.Line(
        [
            { month: "Jan", revenue: 186.0, profit: 80.0 },
            { month: "Feb", revenue: 305.0, profit: 120.0 },
            { month: "Mar", revenue: 237.0, profit: 95.0 },
        ],
        { revenue: { color: "teal.solid" }, profit: { color: "purple.solid" } },
        { xAxis: { dataKey: "month" }, showLegend: true, showDots: true }
    );
});
```

### Dialog Overlay

```typescript
import { Dialog, Button, Text, UIComponentType } from "@elaraai/east-ui";

const dialogExample = East.function([], UIComponentType, $ => {
    return Dialog.Root({
        trigger: Button.Root("Open Dialog"),
        title: "Confirm Action",
        children: [Text.Root("Are you sure you want to proceed?")],
        footer: [
            Button.Root("Cancel", { variant: "outline" }),
            Button.Root("Confirm", { colorPalette: "blue" }),
        ],
    });
});
```
