# East UI Examples

Working code examples organized by use case. For comprehensive documentation, see [USAGE.md](../USAGE.md).

---

## Table of Contents

- [Layout Examples](#layout-examples)
- [Form Examples](#form-examples)
- [Data Display Examples](#data-display-examples)
- [Chart Examples](#chart-examples)
- [State Management Examples](#state-management-examples)
- [Overlay Examples](#overlay-examples)

---

## Layout Examples

### Basic Page Layout

```typescript
import { East } from "@elaraai/east";
import { Box, Stack, Heading, Text, UIComponentType } from "@elaraai/east-ui";

const PageLayout = East.function([], UIComponentType, $ => {
    return Box.Root([
        Stack.VStack([
            Heading.Root("Page Title", { size: "xl" }),
            Text.Root("Welcome to the application."),
            Box.Root([
                Text.Root("Main content goes here."),
            ], { padding: "4", bg: "gray.50", borderRadius: "md" }),
        ], { gap: "4" }),
    ], { padding: "6", maxWidth: "1200px", margin: "0 auto" });
});
```

### Flex Layout with Sidebar

```typescript
import { Flex, Box, Stack, Text, UIComponentType } from "@elaraai/east-ui";

const SidebarLayout = East.function([], UIComponentType, $ => {
    return Flex.Root([
        // Sidebar
        Box.Root([
            Stack.VStack([
                Text.Root("Dashboard", { fontWeight: "bold" }),
                Text.Root("Settings"),
                Text.Root("Profile"),
            ], { gap: "2" }),
        ], { width: "250px", padding: "4", bg: "gray.100" }),

        // Main content
        Box.Root([
            Text.Root("Main content area"),
        ], { flex: "1", padding: "4" }),
    ], { minHeight: "100vh" });
});
```

### Grid Layout

```typescript
import { Grid, Box, Text, UIComponentType } from "@elaraai/east-ui";

const GridLayout = East.function([], UIComponentType, $ => {
    return Grid.Root([
        Box.Root([Text.Root("Item 1")], { bg: "blue.100", padding: "4" }),
        Box.Root([Text.Root("Item 2")], { bg: "green.100", padding: "4" }),
        Box.Root([Text.Root("Item 3")], { bg: "purple.100", padding: "4" }),
        Box.Root([Text.Root("Item 4")], { bg: "orange.100", padding: "4" }),
    ], { templateColumns: "repeat(2, 1fr)", gap: "4" });
});
```

---

## Form Examples

### Login Form

```typescript
import { East, StringType, variant } from "@elaraai/east";
import { Stack, Field, Input, Button, Heading, State, UIComponentType } from "@elaraai/east-ui";

const LoginForm = East.function([], UIComponentType, $ => {
    $(State.initTyped("email", "", StringType)());
    $(State.initTyped("password", "", StringType)());

    const email = $.let($(State.readTyped("email", StringType)()));
    const password = $.let($(State.readTyped("password", StringType)()));

    return Stack.VStack([
        Heading.Root("Login", { size: "lg" }),

        Field.Root(
            Input.String(email.unwrap("some"), {
                placeholder: "Email",
                onBlur: (_$, value) => {
                    $(_$.exec(State.writeTyped("email", variant("some", value), StringType)()));
                },
            }),
            { label: "Email", isRequired: true }
        ),

        Field.Root(
            Input.String(password.unwrap("some"), {
                placeholder: "Password",
                type: "password",
                onBlur: (_$, value) => {
                    $(_$.exec(State.writeTyped("password", variant("some", value), StringType)()));
                },
            }),
            { label: "Password", isRequired: true }
        ),

        Button.Root("Sign In", {
            colorPalette: "blue",
            width: "full",
            onClick: (_$) => {
                // Handle login
            },
        }),
    ], { gap: "4", width: "300px", padding: "6" });
});
```

### Settings Form with Multiple Inputs

```typescript
import { East, IntegerType, BooleanType, variant } from "@elaraai/east";
import { Stack, Field, Input, Switch, Slider, Select, Button, State, UIComponentType } from "@elaraai/east-ui";

const SettingsForm = East.function([], UIComponentType, $ => {
    $(State.initTyped("notifications", true, BooleanType)());
    $(State.initTyped("volume", 50n, IntegerType)());

    const notifications = $.let($(State.readTyped("notifications", BooleanType)()));
    const volume = $.let($(State.readTyped("volume", IntegerType)()));

    return Stack.VStack([
        Field.Root(
            Switch.Root({
                isChecked: notifications.unwrap("some"),
                onChange: (_$, checked) => {
                    $(_$.exec(State.writeTyped("notifications", variant("some", checked), BooleanType)()));
                },
            }),
            { label: "Enable Notifications" }
        ),

        Field.Root(
            Slider.Root({
                value: volume.unwrap("some"),
                min: 0,
                max: 100,
                step: 1,
                onChange: (_$, value) => {
                    $(_$.exec(State.writeTyped("volume", variant("some", value), IntegerType)()));
                },
            }),
            { label: "Volume", helperText: East.str`Current: ${volume.unwrap("some")}` }
        ),

        Field.Root(
            Select.Root([
                { value: "light", label: "Light" },
                { value: "dark", label: "Dark" },
                { value: "system", label: "System" },
            ], { placeholder: "Select theme" }),
            { label: "Theme" }
        ),

        Button.Root("Save Settings", { colorPalette: "green" }),
    ], { gap: "4" });
});
```

---

## Data Display Examples

### Data Table with Selection

```typescript
import { East } from "@elaraai/east";
import { Table, Badge, UIComponentType } from "@elaraai/east-ui";

const UsersTable = East.function([], UIComponentType, $ => {
    const users = [
        { id: 1n, name: "Alice Johnson", email: "alice@example.com", status: "active" },
        { id: 2n, name: "Bob Smith", email: "bob@example.com", status: "pending" },
        { id: 3n, name: "Carol White", email: "carol@example.com", status: "inactive" },
    ];

    return Table.Root(
        users,
        [
            { header: "ID", accessorKey: "id" },
            { header: "Name", accessorKey: "name" },
            { header: "Email", accessorKey: "email" },
            {
                header: "Status",
                accessorKey: "status",
                cell: (row) => Badge.Root(row.status, {
                    colorPalette: row.status === "active" ? "green" :
                                  row.status === "pending" ? "yellow" : "gray",
                }),
            },
        ],
        {
            variant: "line",
            showColumnBorder: true,
            striped: true,
            onRowClick: (_$, row) => {
                // Handle row click
            },
        }
    );
});
```

### Tree View Navigation

```typescript
import { East } from "@elaraai/east";
import { TreeView, UIComponentType } from "@elaraai/east-ui";

const FileTree = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        {
            id: "1",
            label: "src",
            children: [
                { id: "1-1", label: "components" },
                { id: "1-2", label: "utils" },
                { id: "1-3", label: "index.ts" },
            ],
        },
        {
            id: "2",
            label: "tests",
            children: [
                { id: "2-1", label: "unit" },
                { id: "2-2", label: "integration" },
            ],
        },
        { id: "3", label: "package.json" },
    ], {
        onSelect: (_$, node) => {
            // Handle selection
        },
    });
});
```

### Statistics Cards

```typescript
import { East } from "@elaraai/east";
import { Grid, Card, Stat, UIComponentType } from "@elaraai/east-ui";

const StatsDashboard = East.function([], UIComponentType, $ => {
    return Grid.Root([
        Card.Root({
            children: [
                Stat.Root({
                    label: "Total Revenue",
                    value: "$45,231",
                    change: 12.5,
                    changeType: "increase",
                }),
            ],
        }),
        Card.Root({
            children: [
                Stat.Root({
                    label: "Active Users",
                    value: "2,345",
                    change: 8.2,
                    changeType: "increase",
                }),
            ],
        }),
        Card.Root({
            children: [
                Stat.Root({
                    label: "Bounce Rate",
                    value: "24.5%",
                    change: 3.1,
                    changeType: "decrease",
                }),
            ],
        }),
    ], { templateColumns: "repeat(3, 1fr)", gap: "4" });
});
```

---

## Chart Examples

### Multi-Series Line Chart

```typescript
import { East } from "@elaraai/east";
import { Chart, UIComponentType } from "@elaraai/east-ui";

const RevenueChart = East.function([], UIComponentType, $ => {
    return Chart.Line(
        [
            { month: "Jan", revenue: 4000.0, expenses: 2400.0, profit: 1600.0 },
            { month: "Feb", revenue: 3000.0, expenses: 1398.0, profit: 1602.0 },
            { month: "Mar", revenue: 2000.0, expenses: 9800.0, profit: -7800.0 },
            { month: "Apr", revenue: 2780.0, expenses: 3908.0, profit: -1128.0 },
            { month: "May", revenue: 1890.0, expenses: 4800.0, profit: -2910.0 },
            { month: "Jun", revenue: 2390.0, expenses: 3800.0, profit: -1410.0 },
        ],
        {
            revenue: { color: "blue.solid", label: "Revenue" },
            expenses: { color: "red.solid", label: "Expenses" },
            profit: { color: "green.solid", label: "Profit" },
        },
        {
            xAxis: { dataKey: "month", label: "Month" },
            yAxis: { label: "Amount ($)" },
            showLegend: true,
            showGrid: true,
            showDots: true,
            height: 300,
        }
    );
});
```

### Bar Chart Comparison

```typescript
import { East } from "@elaraai/east";
import { Chart, UIComponentType } from "@elaraai/east-ui";

const SalesComparison = East.function([], UIComponentType, $ => {
    return Chart.Bar(
        [
            { product: "Widgets", q1: 120n, q2: 150n, q3: 180n, q4: 200n },
            { product: "Gadgets", q1: 80n, q2: 100n, q3: 130n, q4: 160n },
            { product: "Gizmos", q1: 200n, q2: 180n, q3: 220n, q4: 250n },
        ],
        {
            q1: { color: "blue.solid", label: "Q1" },
            q2: { color: "green.solid", label: "Q2" },
            q3: { color: "purple.solid", label: "Q3" },
            q4: { color: "orange.solid", label: "Q4" },
        },
        {
            xAxis: { dataKey: "product" },
            showLegend: true,
            height: 300,
        }
    );
});
```

### Pie Chart

```typescript
import { East } from "@elaraai/east";
import { Chart, UIComponentType } from "@elaraai/east-ui";

const MarketShare = East.function([], UIComponentType, $ => {
    return Chart.Pie(
        [
            { name: "Product A", value: 400, color: "blue.solid" },
            { name: "Product B", value: 300, color: "green.solid" },
            { name: "Product C", value: 200, color: "purple.solid" },
            { name: "Other", value: 100, color: "gray.solid" },
        ],
        {
            showLabels: true,
            showLegend: true,
            innerRadius: 60, // Makes it a donut chart
            height: 300,
        }
    );
});
```

---

## State Management Examples

### Counter with State

```typescript
import { East, IntegerType, variant } from "@elaraai/east";
import { Stack, Text, Button, State, UIComponentType } from "@elaraai/east-ui";

const Counter = East.function([], UIComponentType, $ => {
    $(State.initTyped("count", 0n, IntegerType)());
    const count = $.let($(State.readTyped("count", IntegerType)()));

    return Stack.VStack([
        Text.Root(East.str`Count: ${count.unwrap("some")}`, { fontSize: "2xl" }),
        Stack.HStack([
            Button.Root("-", {
                onClick: (_$) => {
                    $(_$.exec(State.writeTyped("count", variant("some", count.unwrap("some").subtract(1n)), IntegerType)()));
                },
            }),
            Button.Root("+", {
                onClick: (_$) => {
                    $(_$.exec(State.writeTyped("count", variant("some", count.unwrap("some").add(1n)), IntegerType)()));
                },
            }),
        ], { gap: "2" }),
    ], { gap: "4", align: "center" });
});
```

### Todo List with State

```typescript
import { East, StringType, ArrayType, StructType, variant } from "@elaraai/east";
import { Stack, Input, Button, List, State, UIComponentType } from "@elaraai/east-ui";

const TodoType = StructType({ id: IntegerType, text: StringType, done: BooleanType });
const TodoListType = ArrayType(TodoType);

const TodoList = East.function([], UIComponentType, $ => {
    $(State.initTyped("todos", [], TodoListType)());
    $(State.initTyped("newTodo", "", StringType)());

    const todos = $.let($(State.readTyped("todos", TodoListType)()));
    const newTodo = $.let($(State.readTyped("newTodo", StringType)()));

    return Stack.VStack([
        Stack.HStack([
            Input.String(newTodo.unwrap("some"), {
                placeholder: "Add a todo...",
                onBlur: (_$, value) => {
                    $(_$.exec(State.writeTyped("newTodo", variant("some", value), StringType)()));
                },
            }),
            Button.Root("Add", {
                colorPalette: "blue",
                onClick: (_$) => {
                    // Add todo logic
                },
            }),
        ], { gap: "2" }),

        List.Unordered(
            todos.unwrap("some").map(($, todo) => todo.text),
            {}
        ),
    ], { gap: "4" });
});
```

---

## Overlay Examples

### Confirmation Dialog

```typescript
import { East } from "@elaraai/east";
import { Dialog, Button, Text, Stack, UIComponentType } from "@elaraai/east-ui";

const DeleteConfirmation = East.function([], UIComponentType, $ => {
    return Dialog.Root({
        trigger: Button.Root("Delete Item", { colorPalette: "red" }),
        title: "Confirm Deletion",
        children: [
            Text.Root("Are you sure you want to delete this item? This action cannot be undone."),
        ],
        footer: [
            Button.Root("Cancel", { variant: "outline" }),
            Button.Root("Delete", {
                colorPalette: "red",
                onClick: (_$) => {
                    // Handle deletion
                },
            }),
        ],
        size: "md",
    });
});
```

### Settings Drawer

```typescript
import { East } from "@elaraai/east";
import { Drawer, Button, Stack, Field, Switch, Select, UIComponentType } from "@elaraai/east-ui";

const SettingsDrawer = East.function([], UIComponentType, $ => {
    return Drawer.Root({
        trigger: Button.Root("Settings", { variant: "outline" }),
        title: "Application Settings",
        placement: "right",
        children: [
            Stack.VStack([
                Field.Root(
                    Switch.Root({ isChecked: true }),
                    { label: "Dark Mode" }
                ),
                Field.Root(
                    Switch.Root({ isChecked: true }),
                    { label: "Notifications" }
                ),
                Field.Root(
                    Select.Root([
                        { value: "en", label: "English" },
                        { value: "es", label: "Spanish" },
                        { value: "fr", label: "French" },
                    ], { value: "en" }),
                    { label: "Language" }
                ),
            ], { gap: "4" }),
        ],
        footer: [
            Button.Root("Save", { colorPalette: "blue" }),
        ],
    });
});
```

### Context Menu

```typescript
import { East } from "@elaraai/east";
import { Menu, Box, Text, UIComponentType } from "@elaraai/east-ui";

const ContextMenuExample = East.function([], UIComponentType, $ => {
    return Menu.Root({
        trigger: Box.Root([
            Text.Root("Right-click me"),
        ], { padding: "4", bg: "gray.100", borderRadius: "md" }),
        items: [
            { label: "Copy", onClick: (_$) => { /* handle */ } },
            { label: "Paste", onClick: (_$) => { /* handle */ } },
            { type: "divider" },
            { label: "Delete", onClick: (_$) => { /* handle */ }, colorPalette: "red" },
        ],
    });
});
```

### Tooltip on Hover

```typescript
import { East } from "@elaraai/east";
import { Tooltip, Button, UIComponentType } from "@elaraai/east-ui";

const TooltipExample = East.function([], UIComponentType, $ => {
    return Tooltip.Root({
        trigger: Button.Root("Hover me"),
        content: "This is helpful information about the button.",
        placement: "top",
    });
});
```
