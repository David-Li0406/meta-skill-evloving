/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { East } from "@elaraai/east";
import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Gantt, Text, Badge } from "../../src/index.js";

describeEast("Gantt", (test) => {
    // =========================================================================
    // Basic Gantt Creation
    // =========================================================================

    test("creates gantt with array of field names", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { name: "Design", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
                { name: "Development", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
            ],
            ["name"],
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        $(Assert.equal(gantt.unwrap().getTag(), "Gantt"));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 1n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 2n));
    });

    test("creates gantt with object column config", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { name: "Design", owner: "Alice", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
            ],
            {
                name: { header: "Task" },
                owner: { header: "Owner" },
            },
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 2n));
    });

    // =========================================================================
    // Task Events
    // =========================================================================

    test("creates task with start and end dates", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Task 1", start: new Date("2024-01-01"), end: new Date("2024-01-31") }],
            ["name"],
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        const events = gantt.unwrap().unwrap("Gantt").rows.get(0n).events;
        $(Assert.equal(events.size(), 1n));
        $(Assert.equal(events.get(0n).hasTag("Task"), true));
    });

    test("creates task with label", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Design", start: new Date("2024-01-01"), end: new Date("2024-01-15") }],
            ["name"],
            row => [Gantt.Task({ start: row.start, end: row.end, label: "Design Phase" })]
        ));

        const task = gantt.unwrap().unwrap("Gantt").rows.get(0n).events.get(0n).unwrap("Task");
        $(Assert.equal(task.label.unwrap("some"), "Design Phase"));
    });

    test("creates task with progress", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Development", start: new Date("2024-01-01"), end: new Date("2024-02-01") }],
            ["name"],
            row => [Gantt.Task({ start: row.start, end: row.end, progress: 0.75 })]
        ));

        const task = gantt.unwrap().unwrap("Gantt").rows.get(0n).events.get(0n).unwrap("Task");
        $(Assert.equal(task.progress.unwrap("some"), 0.75));
    });

    test("creates task with color palette", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Testing", start: new Date("2024-02-01"), end: new Date("2024-02-15") }],
            ["name"],
            row => [Gantt.Task({ start: row.start, end: row.end, colorPalette: "blue" })]
        ));

        const task = gantt.unwrap().unwrap("Gantt").rows.get(0n).events.get(0n).unwrap("Task");
        $(Assert.equal(task.colorPalette.unwrap("some").hasTag("blue"), true));
    });

    // =========================================================================
    // Milestone Events
    // =========================================================================

    test("creates milestone with date", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Release", date: new Date("2024-03-01"), start: new Date("2024-01-01"), end: new Date("2024-01-01") }],
            ["name"],
            row => [Gantt.Milestone({ date: row.date })]
        ));

        const events = gantt.unwrap().unwrap("Gantt").rows.get(0n).events;
        $(Assert.equal(events.size(), 1n));
        $(Assert.equal(events.get(0n).hasTag("Milestone"), true));
    });

    test("creates milestone with label", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Launch", date: new Date("2024-03-15"), start: new Date("2024-01-01"), end: new Date("2024-01-01") }],
            ["name"],
            row => [Gantt.Milestone({ date: row.date, label: "Product Launch" })]
        ));

        const milestone = gantt.unwrap().unwrap("Gantt").rows.get(0n).events.get(0n).unwrap("Milestone");
        $(Assert.equal(milestone.label.unwrap("some"), "Product Launch"));
    });

    test("creates milestone with color palette", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Deadline", date: new Date("2024-04-01"), start: new Date("2024-01-01"), end: new Date("2024-01-01") }],
            ["name"],
            row => [Gantt.Milestone({ date: row.date, colorPalette: "red" })]
        ));

        const milestone = gantt.unwrap().unwrap("Gantt").rows.get(0n).events.get(0n).unwrap("Milestone");
        $(Assert.equal(milestone.colorPalette.unwrap("some").hasTag("red"), true));
    });

    // =========================================================================
    // Multiple Events per Row
    // =========================================================================

    test("creates row with multiple events", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Project", start: new Date("2024-01-01"), end: new Date("2024-02-01"), milestone: new Date("2024-02-01") }],
            ["name"],
            row => [
                Gantt.Task({ start: row.start, end: row.end }),
                Gantt.Milestone({ date: row.milestone, label: "Complete" }),
            ]
        ));

        const events = gantt.unwrap().unwrap("Gantt").rows.get(0n).events;
        $(Assert.equal(events.size(), 2n));
        $(Assert.equal(events.get(0n).hasTag("Task"), true));
        $(Assert.equal(events.get(1n).hasTag("Milestone"), true));
    });

    // =========================================================================
    // Styling
    // =========================================================================

    test("creates gantt with line variant", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Task", start: new Date("2024-01-01"), end: new Date("2024-01-15") }],
            ["name"],
            row => [Gantt.Task({ start: row.start, end: row.end })],
            { variant: "line" }
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").style.unwrap("some").variant.unwrap("some").hasTag("line"), true));
    });

    test("creates gantt with showToday", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Task", start: new Date("2024-01-01"), end: new Date("2024-01-15") }],
            ["name"],
            row => [Gantt.Task({ start: row.start, end: row.end })],
            { showToday: true }
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").style.unwrap("some").showToday.unwrap("some"), true));
    });

    test("creates gantt with all style options", $ => {
        const gantt = $.let(Gantt.Root(
            [{ name: "Task", start: new Date("2024-01-01"), end: new Date("2024-01-15") }],
            ["name"],
            row => [Gantt.Task({ start: row.start, end: row.end })],
            {
                variant: "outline",
                size: "md",
                striped: true,
                interactive: true,
                stickyHeader: true,
                colorPalette: "blue",
                showToday: true,
            }
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").style.unwrap("some").striped.unwrap("some"), true));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").style.unwrap("some").showToday.unwrap("some"), true));
    });

    // =========================================================================
    // Real-World Examples
    // =========================================================================

    test("creates project timeline gantt", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { phase: "Planning", owner: "Alice", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
                { phase: "Design", owner: "Bob", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
                { phase: "Development", owner: "Charlie", start: new Date("2024-01-20"), end: new Date("2024-03-15") },
                { phase: "Testing", owner: "Diana", start: new Date("2024-03-01"), end: new Date("2024-03-30") },
            ],
            {
                phase: { header: "Phase" },
                owner: { header: "Owner" },
            },
            row => [
                Gantt.Task({ start: row.start, end: row.end, colorPalette: "blue" }),
            ],
            { variant: "line", striped: true, showToday: true }
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 4n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 2n));
    });

    test("creates gantt with tasks and milestones", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { name: "Sprint 1", start: new Date("2024-01-01"), end: new Date("2024-01-14"), release: new Date("2024-01-14") },
                { name: "Sprint 2", start: new Date("2024-01-15"), end: new Date("2024-01-28"), release: new Date("2024-01-28") },
            ],
            { name: { header: "Sprint" } },
            row => [
                Gantt.Task({ start: row.start, end: row.end, colorPalette: "teal" }),
                Gantt.Milestone({ date: row.release, label: "Release", colorPalette: "green" }),
            ]
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 2n));
        // Each row has 2 events (task + milestone)
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.get(0n).events.size(), 2n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.get(1n).events.size(), 2n));
    });

    // =========================================================================
    // Column Render with Row Field Access
    // =========================================================================

    test("column render function receives row parameter to access other fields", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { name: "Design", owner: "Alice", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
                { name: "Development", owner: "Bob", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
            ],
            {
                name: {
                    header: "Task",
                    render: (value, row) => Text.Root(East.str`${value} (${row.owner})`),
                },
            },
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 2n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 1n));
    });

    test("column render function uses row field for conditional styling", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { task: "Critical Bug", priority: "high", start: new Date("2024-01-01"), end: new Date("2024-01-05") },
                { task: "Minor Fix", priority: "low", start: new Date("2024-01-06"), end: new Date("2024-01-10") },
            ],
            {
                task: { header: "Task" },
                priority: {
                    header: "Priority",
                    render: (value) => Badge.Root(
                        value,
                    ),
                },
            },
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 2n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 2n));
    });

    test("column render function accesses multiple row fields", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { firstName: "Alice", lastName: "Smith", dept: "Eng", start: new Date("2024-01-01"), end: new Date("2024-02-01") },
            ],
            {
                firstName: {
                    header: "Full Name",
                    render: (value, row) => Text.Root(East.str`${value} ${row.lastName}`),
                },
                dept: { header: "Department" },
            },
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 1n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 2n));
    });

    // =========================================================================
    // Complex Type Columns (require value function)
    // =========================================================================

    test("creates gantt with array field using value function", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { name: "Design", tags: ["ui", "frontend"], start: new Date("2024-01-01"), end: new Date("2024-01-15") },
                { name: "Backend", tags: ["api", "db"], start: new Date("2024-01-10"), end: new Date("2024-02-01") },
            ],
            {
                name: { header: "Task" },
                tags: {
                    header: "Tags",
                    // Extract array length as sortable integer value
                    value: (tags) => tags.size(),
                    render: (tags) => Text.Root(East.str`${tags.size()} tags`),
                },
            },
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 2n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 2n));
    });

    test("creates gantt with struct field using value function", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { name: "Sprint 1", metadata: { priority: 1n, status: "active" }, start: new Date("2024-01-01"), end: new Date("2024-01-14") },
                { name: "Sprint 2", metadata: { priority: 3n, status: "pending" }, start: new Date("2024-01-15"), end: new Date("2024-01-28") },
            ],
            {
                name: { header: "Sprint" },
                metadata: {
                    header: "Priority",
                    // Extract priority as sortable integer value
                    value: (meta) => meta.priority,
                    render: (meta) => Text.Root(East.str`Priority: ${meta.priority}`),
                },
            },
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 2n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 2n));
    });

    test("creates gantt mixing primitive and complex columns", $ => {
        const gantt = $.let(Gantt.Root(
            [
                { id: 1n, name: "Project A", team: { lead: "Alice", size: 5n }, start: new Date("2024-01-01"), end: new Date("2024-02-01") },
                { id: 2n, name: "Project B", team: { lead: "Bob", size: 3n }, start: new Date("2024-02-01"), end: new Date("2024-03-01") },
            ],
            {
                id: { header: "ID" },  // Primitive - no value function needed
                name: { header: "Project" },  // Primitive - no value function needed
                team: {
                    header: "Team Lead",
                    // Extract lead name as sortable string value
                    value: (team) => team.lead,
                    render: (team) => Text.Root(team.lead),
                },
            },
            row => [Gantt.Task({ start: row.start, end: row.end })]
        ));

        $(Assert.equal(gantt.unwrap().unwrap("Gantt").columns.size(), 3n));
        $(Assert.equal(gantt.unwrap().unwrap("Gantt").rows.size(), 2n));
    });
}, {   platformFns: TestImpl,});
