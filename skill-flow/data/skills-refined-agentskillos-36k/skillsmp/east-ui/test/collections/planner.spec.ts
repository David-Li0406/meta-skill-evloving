/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { East, FloatType, StringType } from "@elaraai/east";
import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Planner, Text, Badge } from "../../src/index.js";

describeEast("Planner", (test) => {
    // =========================================================================
    // Basic Event Creation
    // =========================================================================

    test("creates event with start only", $ => {
        const event = $.let(Planner.Event({
            start: 1.0,
        }));

        $(Assert.equal(event.start, 1.0));
        $(Assert.equal(event.end.hasTag("none"), true));
        $(Assert.equal(event.label.hasTag("none"), true));
        $(Assert.equal(event.colorPalette.hasTag("none"), true));
    });

    test("creates event with start and end", $ => {
        const event = $.let(Planner.Event({
            start: 1.0,
            end: 5.0,
        }));

        $(Assert.equal(event.start, 1.0));
        $(Assert.equal(event.end.hasTag("some"), true));
        $(Assert.equal(event.end.unwrap("some"), 5.0));
    });

    test("creates event with label", $ => {
        const event = $.let(Planner.Event({
            start: 1.0,
            end: 3.0,
            label: { value: "Task A" },
        }));

        $(Assert.equal(event.label.hasTag("some"), true));
        $(Assert.equal(event.label.unwrap("some").value, "Task A"));
    });

    test("creates event with colorPalette", $ => {
        const event = $.let(Planner.Event({
            start: 1.0,
            end: 3.0,
            colorPalette: "blue",
        }));

        $(Assert.equal(event.colorPalette.hasTag("some"), true));
        $(Assert.equal(event.colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates event with all options", $ => {
        const event = $.let(Planner.Event({
            start: 2.0,
            end: 6.0,
            label: { value: "Important Task" },
            colorPalette: "green",
        }));

        $(Assert.equal(event.start, 2.0));
        $(Assert.equal(event.end.unwrap("some"), 6.0));
        $(Assert.equal(event.label.unwrap("some").value, "Important Task"));
        $(Assert.equal(event.colorPalette.unwrap("some").hasTag("green"), true));
    });

    // =========================================================================
    // Planner Root Creation
    // =========================================================================

    test("creates basic planner", $ => {
        const planner = $.let(Planner.Root(
            [
                { name: "Alice", start: 1.0, end: 3.0 },
                { name: "Bob", start: 2.0, end: 5.0 },
            ],
            ["name"],
            row => [Planner.Event({ start: row.start, end: row.end })],
        ));

        $(Assert.equal(planner.unwrap().hasTag("Planner"), true));
    });

    test("creates planner with style", $ => {
        const planner = $.let(Planner.Root(
            [
                { name: "Task 1", slot: 1.0 },
            ],
            ["name"],
            row => [Planner.Event({ start: row.slot })],
            {
                slotMode: "single",
            }
        ));

        $(Assert.equal(planner.unwrap().hasTag("Planner"), true));
        $(Assert.equal(planner.unwrap().unwrap("Planner").style.hasTag("some"), true));
        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotMode.hasTag("some"), true));
        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotMode.unwrap("some").hasTag("single"), true));
    });

    test("creates planner with span mode", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0, end: 5.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start, end: row.end })],
            {
                slotMode: "span",
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotMode.unwrap("some").hasTag("span"), true));
    });

    test("creates planner with minSlot and maxSlot", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 3.0, end: 5.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start, end: row.end })],
            {
                minSlot: 1.0,
                maxSlot: 10.0,
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").minSlot.unwrap("some"), 1.0));
        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").maxSlot.unwrap("some"), 10.0));
    });

    test("creates planner with slotMinWidth", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                slotMinWidth: "80px",
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotMinWidth.unwrap("some"), "80px"));
    });

    test("creates planner with slotLabel function", $ => {
        const labelFn = East.function([FloatType], StringType, ($, slot) => {
            return East.str`Day ${slot}`;
        });

        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                slotLabel: labelFn,
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotLabel.hasTag("some"), true));
    });

    // =========================================================================
    // Slot Line Styling
    // =========================================================================

    test("creates planner with slot line stroke", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                slotLineStroke: "gray.200",
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotLineStroke.unwrap("some"), "gray.200"));
    });

    test("creates planner with slot line width", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                slotLineWidth: 2.0,
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotLineWidth.unwrap("some"), 2.0));
    });

    test("creates planner with slot line dash", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                slotLineDash: "4 2",
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotLineDash.unwrap("some"), "4 2"));
    });

    test("creates planner with slot line opacity", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                slotLineOpacity: 0.5,
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").slotLineOpacity.unwrap("some"), 0.5));
    });

    // =========================================================================
    // Table Styling
    // =========================================================================

    test("creates planner with table variant", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                variant: "outline",
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates planner with size", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                size: "sm",
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates planner with striped", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                striped: true,
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").striped.unwrap("some"), true));
    });

    test("creates planner with interactive", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                interactive: true,
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").interactive.unwrap("some"), true));
    });

    test("creates planner with stickyHeader", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                stickyHeader: true,
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").stickyHeader.unwrap("some"), true));
    });

    // =========================================================================
    // Multiple Events Per Row
    // =========================================================================

    test("creates planner with multiple events per row", $ => {
        const planner = $.let(Planner.Root(
            [
                { name: "Alice", slot1: 1.0, slot2: 3.0, slot3: 5.0 },
            ],
            ["name"],
            row => [
                Planner.Event({ start: row.slot1, label: { value: "Event 1" } }),
                Planner.Event({ start: row.slot2, label: { value: "Event 2" } }),
                Planner.Event({ start: row.slot3, label: { value: "Event 3" } }),
            ],
        ));

        $(Assert.equal(planner.unwrap().hasTag("Planner"), true));
    });

    // =========================================================================
    // Column Configuration
    // =========================================================================

    test("creates planner with multiple columns", $ => {
        const planner = $.let(Planner.Root(
            [
                { name: "Task A", category: "Development", start: 1.0, end: 3.0 },
                { name: "Task B", category: "Design", start: 2.0, end: 4.0 },
            ],
            ["name", "category"],
            row => [Planner.Event({ start: row.start, end: row.end })],
        ));

        $(Assert.equal(planner.unwrap().hasTag("Planner"), true));
    });

    test("creates planner with column config object", $ => {
        const planner = $.let(Planner.Root(
            [
                { name: "Task A", priority: 1.0 },
            ],
            {
                name: { header: "Task Name" },
                priority: { header: "Priority" },
            },
            row => [Planner.Event({ start: row.priority })],
        ));

        $(Assert.equal(planner.unwrap().hasTag("Planner"), true));
    });

    // =========================================================================
    // Color Palette
    // =========================================================================

    test("creates planner with default colorPalette", $ => {
        const planner = $.let(Planner.Root(
            [{ name: "Task", start: 1.0 }],
            ["name"],
            row => [Planner.Event({ start: row.start })],
            {
                colorPalette: "purple",
            }
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").style.unwrap("some").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    // =========================================================================
    // Column Render with Row Field Access
    // =========================================================================

    test("column render function receives row parameter to access other fields", $ => {
        const planner = $.let(Planner.Root(
            [
                { name: "Alice", role: "Developer", start: 1.0, end: 3.0 },
                { name: "Bob", role: "Designer", start: 2.0, end: 5.0 },
            ],
            {
                name: {
                    header: "Name",
                    render: (value, row) => Text.Root(East.str`${value} (${row.role})`),
                },
            },
            row => [Planner.Event({ start: row.start, end: row.end })],
        ));

        $(Assert.equal(planner.unwrap().hasTag("Planner"), true));
        $(Assert.equal(planner.unwrap().unwrap("Planner").rows.size(), 2n));
        $(Assert.equal(planner.unwrap().unwrap("Planner").columns.size(), 1n));
    });

    test("column render function uses row field for conditional styling", $ => {
        const planner = $.let(Planner.Root(
            [
                { task: "Bug Fix", priority: "high", start: 1.0, end: 3.0 },
                { task: "Feature", priority: "low", start: 2.0, end: 4.0 },
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
            row => [Planner.Event({ start: row.start, end: row.end })],
        ));

        $(Assert.equal(planner.unwrap().hasTag("Planner"), true));
        $(Assert.equal(planner.unwrap().unwrap("Planner").rows.size(), 2n));
        $(Assert.equal(planner.unwrap().unwrap("Planner").columns.size(), 2n));
    });

    test("column render function accesses multiple row fields", $ => {
        const planner = $.let(Planner.Root(
            [
                { firstName: "Alice", lastName: "Smith", department: "Eng", start: 1.0, end: 5.0 },
            ],
            {
                firstName: {
                    header: "Full Name",
                    render: (value, row) => Text.Root(East.str`${value} ${row.lastName}`),
                },
                department: { header: "Department" },
            },
            row => [Planner.Event({ start: row.start, end: row.end })],
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").rows.size(), 1n));
        $(Assert.equal(planner.unwrap().unwrap("Planner").columns.size(), 2n));
    });

    // =========================================================================
    // Complex Type Columns (require value function)
    // =========================================================================

    test("creates planner with array field using value function", $ => {
        const planner = $.let(Planner.Root(
            [
                { name: "Alice", skills: ["TypeScript", "React"], start: 1.0, end: 3.0 },
                { name: "Bob", skills: ["Python", "Django", "FastAPI"], start: 2.0, end: 5.0 },
            ],
            {
                name: { header: "Name" },
                skills: {
                    header: "Skills",
                    // Extract array length as sortable integer value
                    value: (skills) => skills.size(),
                    render: (skills) => Text.Root(East.str`${skills.size()} skills`),
                },
            },
            row => [Planner.Event({ start: row.start, end: row.end })],
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").columns.size(), 2n));
        $(Assert.equal(planner.unwrap().unwrap("Planner").rows.size(), 2n));
    });

    test("creates planner with struct field using value function", $ => {
        const planner = $.let(Planner.Root(
            [
                { name: "Task A", info: { priority: 1n, category: "urgent" }, start: 1.0, end: 3.0 },
                { name: "Task B", info: { priority: 3n, category: "normal" }, start: 2.0, end: 4.0 },
            ],
            {
                name: { header: "Task" },
                info: {
                    header: "Priority",
                    // Extract priority as sortable integer value
                    value: (info) => info.priority,
                    render: (info) => Text.Root(East.str`P${info.priority}`),
                },
            },
            row => [Planner.Event({ start: row.start, end: row.end })],
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").columns.size(), 2n));
        $(Assert.equal(planner.unwrap().unwrap("Planner").rows.size(), 2n));
    });

    test("creates planner mixing primitive and complex columns", $ => {
        const planner = $.let(Planner.Root(
            [
                { id: 1n, name: "Alice", contact: { email: "alice@example.com", phone: "555-1234" }, start: 1.0, end: 3.0 },
                { id: 2n, name: "Bob", contact: { email: "bob@example.com", phone: "555-5678" }, start: 2.0, end: 5.0 },
            ],
            {
                id: { header: "ID" },  // Primitive - no value function needed
                name: { header: "Name" },  // Primitive - no value function needed
                contact: {
                    header: "Email",
                    // Extract email as sortable string value
                    value: (contact) => contact.email,
                    render: (contact) => Text.Root(contact.email),
                },
            },
            row => [Planner.Event({ start: row.start, end: row.end })],
        ));

        $(Assert.equal(planner.unwrap().unwrap("Planner").columns.size(), 3n));
        $(Assert.equal(planner.unwrap().unwrap("Planner").rows.size(), 2n));
    });
}, {   platformFns: TestImpl,});
