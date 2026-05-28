/**
 * TypeDoc Examples - All examples from component documentation
 *
 * This file contains compilable versions of all TypeDoc @example blocks.
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Button.Root, Stat.Types.Indicator)
 */

import { East, none, some } from "@elaraai/east";
import {
    // Buttons
    Button,
    IconButton,
    // Display
    Avatar,
    Badge,
    Icon,
    Stat,
    Tag,
    // Feedback
    Alert,
    Progress,
    // Forms
    Checkbox,
    Input,
    Select,
    Slider,
    Switch,
    Textarea,
    Field,
    Fieldset,
    FileUpload,
    TagsInput,
    // Layout
    Box,
    Stack,
    Grid,
    Separator,
    Splitter,
    // Typography
    Text,
    // Container
    Card,
    // Disclosure
    Accordion,
    Tabs,
    Carousel,
    // Overlays
    Dialog,
    Drawer,
    Popover,
    Tooltip,
    HoverCard,
    Menu,
    ToggleTip,
    ActionBar,
    // Collections
    DataList,
    Table,
    TreeView,
    Gantt,
    // Charts
    Chart,
    Sparkline,
    // Shared
    UIComponentType,
} from "../src/index.js";

// ============================================================================
// BUTTONS
// ============================================================================

// File: src/buttons/button/index.ts
// Export: Button.Root
const buttonRootExample = East.function([], UIComponentType, $ => {
    return Button.Root("Save", {
        variant: "solid",
        colorPalette: "blue",
        size: "md",
    });
});
buttonRootExample.toIR().compile([])();

// File: src/buttons/icon-button/index.ts
// Export: IconButton.Root
const iconButtonRootExample = East.function([], UIComponentType, $ => {
    return IconButton.Root("fas", "xmark");
});
iconButtonRootExample.toIR().compile([])();

const iconButtonStyledExample = East.function([], UIComponentType, $ => {
    return IconButton.Root("fas", "bars", {
        variant: "ghost",
        size: "lg",
    });
});
iconButtonStyledExample.toIR().compile([])();

// ============================================================================
// DISPLAY
// ============================================================================

// File: src/display/avatar/index.ts
// Export: Avatar.Root
const avatarRootExample = East.function([], UIComponentType, $ => {
    return Avatar.Root({
        name: "Jane Smith",
        colorPalette: "blue",
    });
});
avatarRootExample.toIR().compile([])();

// File: src/display/badge/index.ts
// Export: Badge.Root
const badgeRootExample = East.function([], UIComponentType, $ => {
    return Badge.Root("Active", {
        colorPalette: "green",
        variant: "solid",
    });
});
badgeRootExample.toIR().compile([])();

// File: src/display/icon/index.ts
// Export: Icon.Root
const iconRootExample = East.function([], UIComponentType, $ => {
    return Icon.Root("fas", "user");
});
iconRootExample.toIR().compile([])();

const iconStyledExample = East.function([], UIComponentType, $ => {
    return Icon.Root("fas", "heart", {
        color: "red.500",
        size: "xl",
    });
});
iconStyledExample.toIR().compile([])();

// File: src/display/stat/index.ts
// Export: Stat.Root
const statRootExample = East.function([], UIComponentType, $ => {
    return Stat.Root("Growth", "+23.36%", {
        helpText: "From last week",
        indicator: "up",
    });
});
statRootExample.toIR().compile([])();

// File: src/display/tag/index.ts
// Export: Tag.Root
const tagRootExample = East.function([], UIComponentType, $ => {
    return Tag.Root("Featured", {
        colorPalette: "blue",
        variant: "solid",
    });
});
tagRootExample.toIR().compile([])();

// ============================================================================
// FEEDBACK
// ============================================================================

// File: src/feedback/alert/index.ts
// Export: Alert.Root
const alertRootExample = East.function([], UIComponentType, $ => {
    return Alert.Root("warning", {
        title: "Warning",
        description: "Your session will expire in 5 minutes",
    });
});
alertRootExample.toIR().compile([])();

// File: src/feedback/progress/index.ts
// Export: Progress.Root
const progressRootExample = East.function([], UIComponentType, $ => {
    return Progress.Root(60.0, {
        colorPalette: "green",
        size: "md",
        striped: true,
    });
});
progressRootExample.toIR().compile([])();

// ============================================================================
// FORMS
// ============================================================================

// File: src/forms/checkbox/index.ts
// Export: Checkbox.Root
const checkboxRootExample = East.function([], UIComponentType, $ => {
    return Checkbox.Root(true, {
        label: "Enable notifications",
        colorPalette: "blue",
        size: "md",
    });
});
checkboxRootExample.toIR().compile([])();

// File: src/forms/input/index.ts
// Export: Input.String
const inputStringExample = East.function([], UIComponentType, $ => {
    return Input.String("John", {
        placeholder: "Enter name",
        variant: "outline",
    });
});
inputStringExample.toIR().compile([])();

// Export: Input.Integer
const inputIntegerExample = East.function([], UIComponentType, $ => {
    return Input.Integer(25n, {
        min: 0n,
        max: 150n,
    });
});
inputIntegerExample.toIR().compile([])();

// Export: Input.Float
const inputFloatExample = East.function([], UIComponentType, $ => {
    return Input.Float(19.99, {
        min: 0,
        precision: 2n,
    });
});
inputFloatExample.toIR().compile([])();

// Export: Input.DateTime
const inputDateTimeExample = East.function([], UIComponentType, $ => {
    return Input.DateTime(new Date(), {
        showTime: true,
        format: "yyyy-MM-dd HH:mm",
    });
});
inputDateTimeExample.toIR().compile([])();

// File: src/forms/select/index.ts
// Export: Select.Root, Select.Item
const selectRootExample = East.function([], UIComponentType, $ => {
    return Select.Root("", [
        Select.Item("us", "United States"),
        Select.Item("uk", "United Kingdom"),
        Select.Item("ca", "Canada"),
    ], {
        placeholder: "Select a country",
    });
});
selectRootExample.toIR().compile([])();

// File: src/forms/slider/index.ts
// Export: Slider.Root
const sliderRootExample = East.function([], UIComponentType, $ => {
    return Slider.Root(50.0, {
        min: 0,
        max: 100,
        step: 1,
        colorPalette: "blue",
    });
});
sliderRootExample.toIR().compile([])();

// File: src/forms/switch/index.ts
// Export: Switch.Root
const switchRootExample = East.function([], UIComponentType, $ => {
    return Switch.Root(true, {
        label: "Dark mode",
        colorPalette: "blue",
    });
});
switchRootExample.toIR().compile([])();

// File: src/forms/textarea/index.ts
// Export: Textarea.Root
const textareaRootExample = East.function([], UIComponentType, $ => {
    return Textarea.Root("Hello world", {
        placeholder: "Enter description",
        rows: 4n,
    });
});
textareaRootExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.Root
const fieldRootExample = East.function([], UIComponentType, $ => {
    return Field.Root(
        "Email",
        Input.String("", { placeholder: "Enter email" }),
        { helperText: "We'll never share your email" }
    );
});
fieldRootExample.toIR().compile([])();

// File: src/forms/fieldset/index.ts
// Export: Fieldset.Root
const fieldsetRootExample = East.function([], UIComponentType, $ => {
    return Fieldset.Root([
        Field.Root("First Name", Input.String("", { placeholder: "First name" })),
        Field.Root("Last Name", Input.String("", { placeholder: "Last name" })),
    ], {
        legend: "Personal Information",
    });
});
fieldsetRootExample.toIR().compile([])();

// File: src/forms/file-upload/index.ts
// Export: FileUpload.Root
const fileUploadRootExample = East.function([], UIComponentType, $ => {
    return FileUpload.Root({
        accept: "image/*",
        maxFiles: 5n,
    });
});
fileUploadRootExample.toIR().compile([])();

// File: src/forms/tags-input/index.ts
// Export: TagsInput.Root
const tagsInputRootExample = East.function([], UIComponentType, $ => {
    return TagsInput.Root(["React", "TypeScript"], {
        placeholder: "Add tag...",
        max: 5n,
    });
});
tagsInputRootExample.toIR().compile([])();

// ============================================================================
// LAYOUT
// ============================================================================

// File: src/layout/box/index.ts
// Export: Box.Root
const boxRootExample = East.function([], UIComponentType, $ => {
    return Box.Root([
        Text.Root("Hello"),
    ], {
        padding: "4",
        background: "gray.100",
    });
});
boxRootExample.toIR().compile([])();

// File: src/layout/stack/index.ts
// Export: Stack.Root
const stackRootExample = East.function([], UIComponentType, $ => {
    return Stack.Root([
        Text.Root("Item 1"),
        Text.Root("Item 2"),
    ], {
        gap: "4",
        direction: "column",
    });
});
stackRootExample.toIR().compile([])();

// Export: Stack.HStack
const hstackExample = East.function([], UIComponentType, $ => {
    return Stack.HStack([
        Button.Root("Cancel"),
        Button.Root("Submit", { colorPalette: "blue" }),
    ], {
        gap: "2",
    });
});
hstackExample.toIR().compile([])();

// Export: Stack.VStack
const vstackExample = East.function([], UIComponentType, $ => {
    return Stack.VStack([
        Text.Root("Title"),
        Text.Root("Subtitle"),
    ], {
        gap: "1",
        align: "flex-start",
    });
});
vstackExample.toIR().compile([])();

// File: src/layout/grid/index.ts
// Export: Grid.Root, Grid.Item
const gridRootExample = East.function([], UIComponentType, $ => {
    return Grid.Root([
        Grid.Item(Text.Root("Cell 1")),
        Grid.Item(Text.Root("Cell 2")),
        Grid.Item(Text.Root("Cell 3")),
    ], {
        templateColumns: "repeat(3, 1fr)",
        gap: "4",
    });
});
gridRootExample.toIR().compile([])();

// File: src/layout/separator/index.ts
// Export: Separator.Root
const separatorRootExample = East.function([], UIComponentType, $ => {
    return Separator.Root({
        orientation: "horizontal",
        variant: "solid",
    });
});
separatorRootExample.toIR().compile([])();

// File: src/layout/splitter/index.ts
// Export: Splitter.Root, Splitter.Panel
const splitterRootExample = East.function([], UIComponentType, $ => {
    return Splitter.Root(
        [
            Splitter.Panel(Text.Root("Left Panel"), { id: "left" }),
            Splitter.Panel(Text.Root("Right Panel"), { id: "right" }),
        ],
        [50.0, 50.0],
        { orientation: "horizontal" }
    );
});
splitterRootExample.toIR().compile([])();

// ============================================================================
// TYPOGRAPHY
// ============================================================================

// File: src/typography/index.ts
// Export: Text.Root
const textRootExample = East.function([], UIComponentType, $ => {
    return Text.Root("Hello World", {
        color: "blue.500",
        fontWeight: "bold",
        textAlign: "center",
    });
});
textRootExample.toIR().compile([])();

// ============================================================================
// CONTAINER
// ============================================================================

// File: src/container/card/index.ts
// Export: Card.Root
const cardRootExample = East.function([], UIComponentType, $ => {
    return Card.Root([
        Text.Root("Card content here"),
        Button.Root("Action"),
    ], {
        title: "Card Title",
        description: "A brief description",
    });
});
cardRootExample.toIR().compile([])();

// ============================================================================
// DISCLOSURE
// ============================================================================

// File: src/disclosure/accordion/index.ts
// Export: Accordion.Root, Accordion.Item
const accordionRootExample = East.function([], UIComponentType, $ => {
    return Accordion.Root([
        Accordion.Item("section-1", "Section 1", [Text.Root("Content 1")]),
        Accordion.Item("section-2", "Section 2", [Text.Root("Content 2")]),
    ], {
        variant: "enclosed",
        collapsible: true,
    });
});
accordionRootExample.toIR().compile([])();

// File: src/disclosure/tabs/index.ts
// Export: Tabs.Root, Tabs.Item
const tabsRootExample = East.function([], UIComponentType, $ => {
    return Tabs.Root([
        Tabs.Item("tab1", "Overview", [Text.Root("Overview content")]),
        Tabs.Item("tab2", "Details", [Text.Root("Details content")]),
    ], {
        variant: "line",
        fitted: true,
    });
});
tabsRootExample.toIR().compile([])();

// File: src/disclosure/carousel/index.ts
// Export: Carousel.Root
const carouselRootExample = East.function([], UIComponentType, $ => {
    return Carousel.Root([
        Box.Root([Text.Root("Slide 1")]),
        Box.Root([Text.Root("Slide 2")]),
    ], {
        showControls: true,
        showIndicators: true,
    });
});
carouselRootExample.toIR().compile([])();

// ============================================================================
// OVERLAYS
// ============================================================================

// File: src/overlays/dialog/index.ts
// Export: Dialog.Root
const dialogRootExample = East.function([], UIComponentType, $ => {
    return Dialog.Root(
        Button.Root("Open Dialog"),
        [Text.Root("Dialog content here")],
        { title: "My Dialog" }
    );
});
dialogRootExample.toIR().compile([])();

// File: src/overlays/drawer/index.ts
// Export: Drawer.Root
const drawerRootExample = East.function([], UIComponentType, $ => {
    return Drawer.Root(
        Button.Root("Open Drawer"),
        [Text.Root("Drawer content")],
        { title: "Settings", placement: "end" }
    );
});
drawerRootExample.toIR().compile([])();

// File: src/overlays/popover/index.ts
// Export: Popover.Root
const popoverRootExample = East.function([], UIComponentType, $ => {
    return Popover.Root(
        Button.Root("Show Info"),
        [Text.Root("Popover content here")],
        { title: "Information" }
    );
});
popoverRootExample.toIR().compile([])();

// File: src/overlays/tooltip/index.ts
// Export: Tooltip.Root
const tooltipRootExample = East.function([], UIComponentType, $ => {
    return Tooltip.Root(
        Button.Root("Hover me"),
        "This is a helpful tooltip",
        { placement: "top" }
    );
});
tooltipRootExample.toIR().compile([])();

// File: src/overlays/hover-card/index.ts
// Export: HoverCard.Root
const hoverCardRootExample = East.function([], UIComponentType, $ => {
    return HoverCard.Root(
        Text.Root("@username"),
        [
            Avatar.Root({ name: "John Doe" }),
            Text.Root("Software Engineer"),
        ],
        { openDelay: 200n }
    );
});
hoverCardRootExample.toIR().compile([])();

// File: src/overlays/menu/index.ts
// Export: Menu.Root, Menu.Item, Menu.Separator
const menuRootExample = East.function([], UIComponentType, $ => {
    return Menu.Root(
        Button.Root("Actions"),
        [
            Menu.Item("edit", "Edit"),
            Menu.Separator(),
            Menu.Item("delete", "Delete"),
        ]
    );
});
menuRootExample.toIR().compile([])();

// File: src/overlays/toggle-tip/index.ts
// Export: ToggleTip.Root
const toggleTipRootExample = East.function([], UIComponentType, $ => {
    return ToggleTip.Root(
        IconButton.Root("fas", "circle-info"),
        "Click for more information about this feature"
    );
});
toggleTipRootExample.toIR().compile([])();

// File: src/overlays/action-bar/index.ts
// Export: ActionBar.Root, ActionBar.Action, ActionBar.Separator
const actionBarRootExample = East.function([], UIComponentType, $ => {
    return ActionBar.Root([
        ActionBar.Action("delete", "Delete"),
        ActionBar.Separator(),
        ActionBar.Action("archive", "Archive"),
    ], {
        selectionCount: 5n,
        selectionLabel: "items selected",
    });
});
actionBarRootExample.toIR().compile([])();

// ============================================================================
// COLLECTIONS
// ============================================================================

// File: src/collections/data-list/index.ts
// Export: DataList.Root, DataList.Item
const dataListRootExample = East.function([], UIComponentType, $ => {
    return DataList.Root([
        DataList.Item("Name", "John Doe"),
        DataList.Item("Email", "john@example.com"),
        DataList.Item("Role", "Administrator"),
    ], {
        orientation: "horizontal",
    });
});
dataListRootExample.toIR().compile([])();

// File: src/collections/table/index.ts
// Export: Table.Root
const tableRootExample = East.function([], UIComponentType, $ => {
    return Table.Root(
        [
            { name: "Alice", age: 30n, role: "Admin" },
            { name: "Bob", age: 25n, role: "User" },
        ],
        ["name", "age", "role"],
        { variant: "line", striped: true }
    );
});
tableRootExample.toIR().compile([])();

// File: src/collections/tree-view/index.ts
// Export: TreeView.Root, TreeView.Branch, TreeView.Item
const treeViewRootExample = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        TreeView.Branch("folder-1", "Documents", [
            TreeView.Item("file-1", "Report.pdf"),
            TreeView.Item("file-2", "Notes.txt"),
        ]),
        TreeView.Item("file-3", "README.md"),
    ]);
});
treeViewRootExample.toIR().compile([])();

// File: src/collections/gantt/index.ts
// Export: Gantt.Root, Gantt.Task
const ganttRootExample = East.function([], UIComponentType, $ => {
    return Gantt.Root(
        [
            { name: "Design", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
            { name: "Development", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
        ],
        { name: { header: "Task Name" } },
        row => [Gantt.Task({ start: row.start, end: row.end, colorPalette: "blue" })]
    );
});
ganttRootExample.toIR().compile([])();

// ============================================================================
// CHARTS
// ============================================================================

// File: src/charts/bar/index.ts
// Export: Chart.Bar
const barChartExample = East.function([], UIComponentType, $ => {
    return Chart.Bar(
        [
            { type: "Stock", allocation: 60 },
            { type: "Crypto", allocation: 45 },
            { type: "ETF", allocation: 12 },
        ],
        { allocation: { color: "teal.solid" } },
        { xAxis: Chart.Axis({ dataKey: "type" }) }
    );
});
barChartExample.toIR().compile([])();

// File: src/charts/line/index.ts
// Export: Chart.Line
const lineChartExample = East.function([], UIComponentType, $ => {
    return Chart.Line(
        [
            { month: "Jan", sales: 100 },
            { month: "Feb", sales: 150 },
            { month: "Mar", sales: 200 },
        ],
        { sales: { color: "blue.solid" } },
        { xAxis: Chart.Axis({ dataKey: "month" }) }
    );
});
lineChartExample.toIR().compile([])();

// File: src/charts/area/index.ts
// Export: Chart.Area
const areaChartExample = East.function([], UIComponentType, $ => {
    return Chart.Area(
        [
            { month: "Jan", revenue: 1000 },
            { month: "Feb", revenue: 1500 },
            { month: "Mar", revenue: 1200 },
        ],
        { revenue: { color: "green.solid", fillOpacity: 0.3 } },
        { xAxis: Chart.Axis({ dataKey: "month" }) }
    );
});
areaChartExample.toIR().compile([])();

// File: src/charts/pie/index.ts
// Export: Chart.Pie
const pieChartExample = East.function([], UIComponentType, $ => {
    return Chart.Pie([
        { name: "Desktop", value: 400, color: some("blue.solid") },
        { name: "Mobile", value: 300, color: some("orange.solid") },
        { name: "Tablet", value: 200, color: some("green.solid") },
    ]);
});
pieChartExample.toIR().compile([])();

// File: src/charts/scatter/index.ts
// Export: Chart.Scatter
const scatterChartExample = East.function([], UIComponentType, $ => {
    return Chart.Scatter(
        [
            { temp: 10, sales: 30 },
            { temp: 20, sales: 50 },
            { temp: 30, sales: 80 },
        ],
        { temp: { color: "purple.solid" } },
        { xDataKey: "temp", yDataKey: "sales" }
    );
});
scatterChartExample.toIR().compile([])();

// File: src/charts/radar/index.ts
// Export: Chart.Radar
const radarChartExample = East.function([], UIComponentType, $ => {
    return Chart.Radar(
        [
            { subject: "Math", score: 80 },
            { subject: "Science", score: 90 },
            { subject: "English", score: 70 },
        ],
        { score: { color: "teal.solid" } },
        { dataKey: "subject", fillOpacity: 0.5 }
    );
});
radarChartExample.toIR().compile([])();

// File: src/charts/bar-list/index.ts
// Export: Chart.BarList
const barListExample = East.function([], UIComponentType, $ => {
    return Chart.BarList([
        { name: "Google", value: 1200000, color: none },
        { name: "Direct", value: 100000, color: none },
        { name: "GitHub", value: 200000, color: none },
    ], {
        sort: { by: "value", direction: "desc" },
        showValue: true,
        color: "teal.subtle",
    });
});
barListExample.toIR().compile([])();

// File: src/charts/bar-segment/index.ts
// Export: Chart.BarSegment
const barSegmentExample = East.function([], UIComponentType, $ => {
    return Chart.BarSegment([
        { name: "Completed", value: 70, color: some("green.solid") },
        { name: "In Progress", value: 20, color: some("yellow.solid") },
        { name: "Not Started", value: 10, color: some("gray.solid") },
    ]);
});
barSegmentExample.toIR().compile([])();

// File: src/charts/sparkline/index.ts
// Export: Sparkline.Root
const sparklineExample = East.function([], UIComponentType, $ => {
    return Sparkline.Root([1.0, 3.0, 2.0, 4.0, 3.5, 5.0], {
        type: "line",
        color: "blue.500",
        width: "150px",
        height: "40px",
    });
});
sparklineExample.toIR().compile([])();

console.log("All TypeDoc examples compiled and executed successfully!");
