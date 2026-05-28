/**
 * Layout TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the layout module (Box, Stack, Grid, Splitter, Flex, etc.).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Box.Root, Stack.Root)
 */

import { East } from "@elaraai/east";
import { Box, Button, Grid, GridAutoFlow, Separator, Splitter, Stack, Text, UIComponentType } from "../src/index.js";

// ============================================================================
// BOX
// ============================================================================

// File: src/layout/box/index.ts
// Export: createBox (private function)
const boxExample = East.function([], UIComponentType, $ => {
    return Box.Root([
        Text.Root("Hello"),
    ], {
        padding: "4",
        background: "gray.100",
    });
});
boxExample.toIR().compile([])();

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

// File: src/layout/box/index.ts
// Export: Box.Padding
const boxPaddingExample = East.function([], UIComponentType, $ => {
    return Box.Root([
        Text.Root("Padded content"),
    ], {
        padding: Box.Padding("4", "2", "4", "2"),
    });
});
boxPaddingExample.toIR().compile([])();

// File: src/layout/box/index.ts
// Export: Box.Margin
const boxMarginExample = East.function([], UIComponentType, $ => {
    return Box.Root([
        Text.Root("Centered content"),
    ], {
        margin: Box.Margin("4", "auto", "4", "auto"),
    });
});
boxMarginExample.toIR().compile([])();

// File: src/layout/box/index.ts
// Export: Box.Root (with flex layout)
const boxFlexExample = East.function([], UIComponentType, $ => {
    return Box.Root([
        Text.Root("Item 1"),
        Text.Root("Item 2"),
    ], {
        display: "flex",
        flexDirection: "column",
        gap: "4",
        padding: "4",
    });
});
boxFlexExample.toIR().compile([])();

// File: src/layout/box/index.ts
// Export: Box.Root (with overflow)
const boxOverflowExample = East.function([], UIComponentType, $ => {
    return Box.Root([
        Text.Root("Scrollable content"),
    ], {
        maxHeight: "200px",
        overflow: "auto",
    });
});
boxOverflowExample.toIR().compile([])();

// ============================================================================
// GRID
// ============================================================================

// File: src/layout/grid/index.ts
// Export: GridRoot (private function)
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

// File: src/layout/grid/index.ts
// Export: Grid.Root
const gridRootExample2 = East.function([], UIComponentType, $ => {
    return Grid.Root([
        Grid.Item(Text.Root("Cell 1")),
        Grid.Item(Text.Root("Cell 2")),
        Grid.Item(Text.Root("Cell 3")),
    ], {
        templateColumns: "repeat(3, 1fr)",
        gap: "4",
    });
});
gridRootExample2.toIR().compile([])();

// File: src/layout/grid/index.ts
// Export: Grid.Item
const gridItemExample = East.function([], UIComponentType, $ => {
    return Grid.Root([
        Grid.Item(Text.Root("Header"), { colSpan: "2" }),
        Grid.Item(Text.Root("Sidebar")),
        Grid.Item(Text.Root("Content")),
    ], {
        templateColumns: "repeat(2, 1fr)",
        gap: "4",
    });
});
gridItemExample.toIR().compile([])();

// File: src/layout/grid/types.ts
// Export: GridAutoFlow
const gridAutoFlowExample = East.function([], UIComponentType, $ => {
    return Grid.Root([
        Grid.Item(Text.Root("Cell 1")),
        Grid.Item(Text.Root("Cell 2")),
    ], {
        templateColumns: "repeat(2, 1fr)",
        autoFlow: GridAutoFlow("row"),
    });
});
gridAutoFlowExample.toIR().compile([])();

// ============================================================================
// SEPARATOR
// ============================================================================

// File: src/layout/separator/index.ts
// Export: createSeparator (private function)
const separatorExample = East.function([], UIComponentType, $ => {
    return Separator.Root({
        orientation: "horizontal",
        variant: "solid",
    });
});
separatorExample.toIR().compile([])();

// File: src/layout/separator/index.ts
// Export: Separator.Root
const separatorRootExample = East.function([], UIComponentType, $ => {
    return Separator.Root({
        orientation: "horizontal",
        variant: "solid",
    });
});
separatorRootExample.toIR().compile([])();

// File: src/layout/separator/index.ts
// Export: Separator.Root (with label)
const separatorLabelExample = East.function([], UIComponentType, $ => {
    return Separator.Root({
        label: "OR",
        variant: "dashed",
    });
});
separatorLabelExample.toIR().compile([])();

// File: src/layout/separator/index.ts
// Export: Separator.Root (vertical)
const separatorVerticalExample = East.function([], UIComponentType, $ => {
    return Separator.Root({
        orientation: "vertical",
        size: "sm",
        color: "gray.300",
    });
});
separatorVerticalExample.toIR().compile([])();

// ============================================================================
// SPLITTER
// ============================================================================

// File: src/layout/splitter/index.ts
// Export: SplitterPanel (private function)
const splitterPanelExample = East.function([], UIComponentType, $ => {
    return Splitter.Root(
        [
            Splitter.Panel(Text.Root("Sidebar"), { id: "sidebar", minSize: 20 }),
            Splitter.Panel(Text.Root("Main"), { id: "main", collapsible: true }),
        ],
        [30.0, 70.0],
        { orientation: "horizontal" }
    );
});
splitterPanelExample.toIR().compile([])();

// File: src/layout/splitter/index.ts
// Export: SplitterRoot (private function)
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

// File: src/layout/splitter/index.ts
// Export: Splitter.Root
const splitterRootExample2 = East.function([], UIComponentType, $ => {
    return Splitter.Root(
        [
            Splitter.Panel(Text.Root("Left Panel"), { id: "left" }),
            Splitter.Panel(Text.Root("Right Panel"), { id: "right" }),
        ],
        [50.0, 50.0],
        { orientation: "horizontal" }
    );
});
splitterRootExample2.toIR().compile([])();

// File: src/layout/splitter/index.ts
// Export: Splitter.Panel
const splitterPanelExample2 = East.function([], UIComponentType, $ => {
    return Splitter.Root(
        [
            Splitter.Panel(Text.Root("Sidebar"), { id: "sidebar", minSize: 20 }),
            Splitter.Panel(Text.Root("Main"), { id: "main", collapsible: true }),
        ],
        [30.0, 70.0],
        { orientation: "horizontal" }
    );
});
splitterPanelExample2.toIR().compile([])();

// File: src/layout/splitter/index.ts
// Export: Splitter.Root (vertical orientation)
const splitterVerticalExample = East.function([], UIComponentType, $ => {
    return Splitter.Root(
        [
            Splitter.Panel(Text.Root("Top Panel"), { id: "top" }),
            Splitter.Panel(Text.Root("Bottom Panel"), { id: "bottom" }),
        ],
        [60.0, 40.0],
        { orientation: "vertical" }
    );
});
splitterVerticalExample.toIR().compile([])();

// ============================================================================
// STACK
// ============================================================================

// File: src/layout/stack/index.ts
// Export: createStack (private function)
const stackExample = East.function([], UIComponentType, $ => {
    return Stack.Root([
        Text.Root("Item 1"),
        Text.Root("Item 2"),
    ], {
        gap: "4",
        direction: "column",
    });
});
stackExample.toIR().compile([])();

// File: src/layout/stack/index.ts
// Export: createHStack (private function)
const hstackExample = East.function([], UIComponentType, $ => {
    return Stack.HStack([
        Button.Root("Cancel"),
        Button.Root("Submit", { colorPalette: "blue" }),
    ], {
        gap: "2",
    });
});
hstackExample.toIR().compile([])();

// File: src/layout/stack/index.ts
// Export: createVStack (private function)
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

// File: src/layout/stack/index.ts
// Export: Stack.HStack
const stackHStackExample = East.function([], UIComponentType, $ => {
    return Stack.HStack([
        Button.Root("Cancel"),
        Button.Root("Submit", { colorPalette: "blue" }),
    ], {
        gap: "2",
    });
});
stackHStackExample.toIR().compile([])();

// File: src/layout/stack/index.ts
// Export: Stack.VStack
const stackVStackExample = East.function([], UIComponentType, $ => {
    return Stack.VStack([
        Text.Root("Title"),
        Text.Root("Subtitle"),
    ], {
        gap: "1",
        align: "flex-start",
    });
});
stackVStackExample.toIR().compile([])();

// File: src/layout/stack/index.ts
// Export: Stack.Padding
const stackPaddingExample = East.function([], UIComponentType, $ => {
    return Stack.Root([
        Text.Root("Content"),
    ], {
        padding: Stack.Padding("4", "2", "4", "2"),
    });
});
stackPaddingExample.toIR().compile([])();

// File: src/layout/stack/index.ts
// Export: Stack.Margin
const stackMarginExample = East.function([], UIComponentType, $ => {
    return Stack.Root([
        Text.Root("Content"),
    ], {
        margin: Stack.Margin("4", "auto", "4", "auto"),
    });
});
stackMarginExample.toIR().compile([])();

console.log("Layout TypeDoc examples compiled and executed successfully!");
