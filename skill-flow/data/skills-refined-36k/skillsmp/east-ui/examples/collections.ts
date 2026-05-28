/**
 * Collections TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the collections module (DataList, Gantt, Table, TreeView).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., DataList.Root, DataList.Item, Gantt.Root, Table.Root, TreeView.Root)
 */

import { East, variant } from "@elaraai/east";
import { DataList, Gantt, Table, TreeView, UIComponentType } from "../src/index.js";

// ============================================================================
// DATA LIST
// ============================================================================

// File: src/collections/data-list/index.ts
// Export: DataListItem (private function)
const dataListItemExample = East.function([], UIComponentType, $ => {
    return DataList.Root([
        DataList.Item("Status", "Active"),
    ]);
});
dataListItemExample.toIR().compile([])();

// File: src/collections/data-list/index.ts
// Export: DataListRoot (private function)
const dataListRootExample = East.function([], UIComponentType, $ => {
    return DataList.Root([
        DataList.Item("Status", "Active"),
        DataList.Item("Created", "Jan 1, 2024"),
        DataList.Item("Updated", "Dec 15, 2024"),
    ], {
        orientation: "horizontal",
        variant: "bold",
    });
});
dataListRootExample.toIR().compile([])();

// File: src/collections/data-list/index.ts
// Export: DataList.Root
const dataListDotRootExample = East.function([], UIComponentType, $ => {
    return DataList.Root([
        DataList.Item("Name", "John Doe"),
        DataList.Item("Email", "john@example.com"),
        DataList.Item("Role", "Administrator"),
    ], {
        orientation: "horizontal",
    });
});
dataListDotRootExample.toIR().compile([])();

// File: src/collections/data-list/index.ts
// Export: DataList.Item
const dataListDotItemExample = East.function([], UIComponentType, $ => {
    return DataList.Root([
        DataList.Item("Status", "Active"),
        DataList.Item("Count", "42"),
    ]);
});
dataListDotItemExample.toIR().compile([])();

// File: src/collections/data-list/types.ts
// Export: DataListVariant
const dataListVariantExample = East.function([], UIComponentType, $ => {
    return DataList.Root([
        DataList.Item("Status", "Active"),
    ], {
        variant: variant('bold', null),
    });
});
dataListVariantExample.toIR().compile([])();

// ============================================================================
// GANTT
// ============================================================================

// File: src/collections/gantt/index.ts
// Export: createTask (private function)
const ganttTaskExample = East.function([], UIComponentType, $ => {
    return Gantt.Root(
        [{ name: "Task", start: new Date("2024-01-01"), end: new Date("2024-01-15") }],
        ["name"],
        row => [Gantt.Task({
            start: row.start,
            end: row.end,
            label: "Design Phase",
            progress: 75,
            colorPalette: "blue",
        })]
    );
});
ganttTaskExample.toIR().compile([])();

// File: src/collections/gantt/index.ts
// Export: createMilestone (private function)
const ganttMilestoneExample = East.function([], UIComponentType, $ => {
    return Gantt.Root(
        [{ name: "Launch", date: new Date("2024-02-01") }],
        ["name"],
        row => [Gantt.Milestone({
            date: row.date,
            label: "Design Complete",
            colorPalette: "green",
        })]
    );
});
ganttMilestoneExample.toIR().compile([])();

// File: src/collections/gantt/index.ts
// Export: createGantt (private function)
const ganttRootExample = East.function([], UIComponentType, $ => {
    return Gantt.Root(
        [
            { name: "Design", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
            { name: "Development", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
        ],
        ["name"],
        row => [Gantt.Task({ start: row.start, end: row.end })],
        { showToday: true }
    );
});
ganttRootExample.toIR().compile([])();

// File: src/collections/gantt/index.ts
// Export: Gantt.Root
const ganttDotRootExample = East.function([], UIComponentType, $ => {
    return Gantt.Root(
        [
            { name: "Design", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
            { name: "Development", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
        ],
        ["name"],
        row => [Gantt.Task({ start: row.start, end: row.end })],
        { showToday: true }
    );
});
ganttDotRootExample.toIR().compile([])();

// File: src/collections/gantt/index.ts
// Export: Gantt.Task
const ganttDotTaskExample = East.function([], UIComponentType, $ => {
    return Gantt.Root(
        [{ name: "Task", start: new Date("2024-01-01"), end: new Date("2024-01-15") }],
        ["name"],
        row => [Gantt.Task({
            start: row.start,
            end: row.end,
            label: "Design Phase",
            progress: 75,
            colorPalette: "blue",
        })]
    );
});
ganttDotTaskExample.toIR().compile([])();

// File: src/collections/gantt/index.ts
// Export: Gantt.Milestone
const ganttDotMilestoneExample = East.function([], UIComponentType, $ => {
    return Gantt.Root(
        [{ name: "Launch", date: new Date("2024-02-01") }],
        ["name"],
        row => [Gantt.Milestone({
            date: row.date,
            label: "Launch",
            colorPalette: "green",
        })]
    );
});
ganttDotMilestoneExample.toIR().compile([])();

// ============================================================================
// TABLE
// ============================================================================

// File: src/collections/table/index.ts
// Export: createTable (private function)
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

// File: src/collections/table/index.ts
// Export: Table.Root
const tableDotRootExample = East.function([], UIComponentType, $ => {
    return Table.Root(
        [
            { name: "Alice", age: 30n, role: "Admin" },
            { name: "Bob", age: 25n, role: "User" },
        ],
        ["name", "age", "role"],
        { variant: "line", striped: true }
    );
});
tableDotRootExample.toIR().compile([])();

// ============================================================================
// TREE VIEW
// ============================================================================

// File: src/collections/tree-view/index.ts
// Export: TreeItem (private function)
const treeItemExample = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        TreeView.Item("readme", "README.md", { prefix: "far", name: "file" }),
        TreeView.Item("index", "index.ts", { prefix: "fas", name: "file-code", color: "blue.500" }),
    ]);
});
treeItemExample.toIR().compile([])();

// File: src/collections/tree-view/index.ts
// Export: TreeBranch (private function)
const treeBranchExample = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        TreeView.Branch("src", "src", [
            TreeView.Branch("components", "components", [
                TreeView.Item("button", "Button.tsx"),
            ]),
            TreeView.Item("index", "index.ts"),
        ], { prefix: "fas", name: "folder", color: "yellow.500" }),
    ]);
});
treeBranchExample.toIR().compile([])();

// File: src/collections/tree-view/index.ts
// Export: TreeViewRoot (private function)
const treeViewRootExample = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        TreeView.Branch("src", "src", [
            TreeView.Item("index", "index.ts"),
            TreeView.Item("utils", "utils.ts"),
        ]),
        TreeView.Item("package", "package.json"),
    ], {
        variant: "subtle",
        size: "sm",
    });
});
treeViewRootExample.toIR().compile([])();

// File: src/collections/tree-view/index.ts
// Export: TreeView.Root
const treeViewDotRootExample = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        TreeView.Branch("src", "src", [
            TreeView.Item("index", "index.ts"),
            TreeView.Item("utils", "utils.ts"),
        ]),
        TreeView.Item("package", "package.json"),
    ], {
        variant: "subtle",
        size: "sm",
    });
});
treeViewDotRootExample.toIR().compile([])();

// File: src/collections/tree-view/index.ts
// Export: TreeView.Item
const treeViewDotItemExample = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        TreeView.Item("readme", "README.md", { prefix: "far", name: "file" }),
        TreeView.Item("index", "index.ts", { prefix: "fas", name: "file-code", color: "blue.500" }),
    ]);
});
treeViewDotItemExample.toIR().compile([])();

// File: src/collections/tree-view/index.ts
// Export: TreeView.Branch
const treeViewDotBranchExample = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        TreeView.Branch("src", "src", [
            TreeView.Branch("components", "components", [
                TreeView.Item("button", "Button.tsx"),
            ]),
            TreeView.Item("index", "index.ts"),
        ], { prefix: "fas", name: "folder", color: "yellow.500" }),
    ]);
});
treeViewDotBranchExample.toIR().compile([])();

console.log("Collections TypeDoc examples compiled and executed successfully!");
