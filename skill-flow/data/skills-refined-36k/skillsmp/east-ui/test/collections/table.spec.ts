/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Table, Badge, Text, Stack } from "../../src/index.js";
import { East } from "@elaraai/east";

describeEast("Table", (test) => {
    // =========================================================================
    // Simple Array Syntax
    // =========================================================================

    test("creates table with array of field names (primitive fields only)", $ => {
        const table = $.let(Table.Root(
            [
                { name: "Alice", email: "alice@example.com" },
                { name: "Bob", email: "bob@example.com" },
            ],
            ["name", "email"]
        ));

        $(Assert.equal(table.unwrap().getTag(), "Table"));
        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
        $(Assert.equal(table.unwrap().unwrap("Table").rows.size(), 2n));
    });

    // =========================================================================
    // Object Syntax with Default Rendering
    // =========================================================================

    test("creates table with object config (no render - uses default)", $ => {
        const table = $.let(Table.Root(
            [
                { name: "Alice", email: "alice@example.com" },
                { name: "Bob", email: "bob@example.com" },
            ],
            {
                name: { header: "Name" },
                email: { header: "Email" },
            }
        ));

        $(Assert.equal(table.unwrap().getTag(), "Table"));
        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
    });

    test("creates table with column subset", $ => {
        // Only select some columns
        const table = $.let(Table.Root(
            [
                { name: "Alice", age: 30n, city: "NYC", other: true },
            ],
            {
                name: { header: "Name" },
                city: { header: "City" },
                // age and other are not included
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
    });

    test("creates table with non-string fields (auto converts to string)", $ => {
        const table = $.let(Table.Root(
            [
                { name: "Alice", age: 30n, active: true },
            ],
            {
                name: { header: "Name" },
                age: { header: "Age" },
                active: { header: "Active" },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 3n));
    });

    // =========================================================================
    // Column Configuration
    // =========================================================================

    test("creates table with custom headers", $ => {
        const table = $.let(Table.Root(
            [
                { firstName: "Alice", lastName: "Smith" },
            ],
            {
                firstName: { header: "First Name" },
                lastName: { header: "Last Name" },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.get(0n).header.unwrap("some"), "First Name"));
    });

    test("creates table with custom render for text alignment", $ => {
        const table = $.let(Table.Root(
            [
                { item: "Widget", price: "$99.99" },
            ],
            {
                item: { header: "Item" },
                price: { header: "Price", render: (value) => Text.Root(value, { textAlign: "right" }) },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
    });

    // =========================================================================
    // Custom Rendering
    // =========================================================================

    test("creates table with custom render for Badge", $ => {
        const table = $.let(Table.Root(
            [
                { name: "Alice", status: "Active" },
                { name: "Bob", status: "Pending" },
            ],
            {
                name: { header: "Name" },
                status: { header: "Status", render: value => Badge.Root(value, { variant: "solid" }) },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").rows.size(), 2n));
    });

    // =========================================================================
    // Styling
    // =========================================================================

    test("creates table with line variant", $ => {
        const table = $.let(Table.Root(
            [{ col: "value" }],
            { col: { header: "Column" } },
            { variant: "line" }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").style.unwrap("some").variant.unwrap("some").hasTag("line"), true));
    });

    test("creates striped table", $ => {
        const table = $.let(Table.Root(
            [{ col: "value" }],
            { col: { header: "Column" } },
            { striped: true }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").style.unwrap("some").striped.unwrap("some"), true));
    });

    test("creates table with size", $ => {
        const table = $.let(Table.Root(
            [{ col: "value" }],
            { col: { header: "Column" } },
            { size: "lg" }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").style.unwrap("some").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates table with all style options", $ => {
        const table = $.let(Table.Root(
            [{ name: "Alice", email: "alice@example.com" }],
            {
                name: { header: "Name" },
                email: { header: "Email" },
            },
            {
                variant: "outline",
                size: "md",
                striped: true,
                interactive: true,
                stickyHeader: true,
                colorPalette: "blue",
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
        $(Assert.equal(table.unwrap().unwrap("Table").style.unwrap("some").striped.unwrap("some"), true));
        $(Assert.equal(table.unwrap().unwrap("Table").style.unwrap("some").interactive.unwrap("some"), true));
    });

    // =========================================================================
    // Render with Row Access
    // =========================================================================

    test("render function receives row parameter to access other fields", $ => {
        const table = $.let(Table.Root(
            [
                { name: "Alice", status: "Active", role: "Admin" },
                { name: "Bob", status: "Inactive", role: "User" },
            ],
            {
                name: { header: "Name" },
                status: {
                    header: "Status",
                    render: (value, row) => Badge.Root(
                        East.str`${value} (${row.role})`,
                        { variant: "solid" }
                    ),
                },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").rows.size(), 2n));
        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
    });

    test("render function uses row field for conditional styling", $ => {
        const table = $.let(Table.Root(
            [
                { product: "Widget", price: 100n, inStock: true },
                { product: "Gadget", price: 250n, inStock: false },
            ],
            {
                product: { header: "Product" },
                price: {
                    header: "Price",
                    render: (value) => Text.Root(
                        East.str`$${value}`,
                    ),
                },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").rows.size(), 2n));
    });

    test("render function accesses multiple row fields", $ => {
        const table = $.let(Table.Root(
            [
                { firstName: "Alice", lastName: "Smith", department: "Engineering" },
            ],
            {
                firstName: {
                    header: "Full Name",
                    render: (value, row) => Text.Root(East.str`${value} ${row.lastName}`),
                },
                department: { header: "Department" },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
    });

    // =========================================================================
    // Real-World Examples
    // =========================================================================

    test("creates user table with mixed components", $ => {
        const table = $.let(Table.Root(
            [
                { name: "Alice Smith", email: "alice@example.com", role: "Admin" },
                { name: "Bob Jones", email: "bob@example.com", role: "User" },
            ],
            {
                name: { header: "Name" },
                email: { header: "Email" },
                role: { header: "Role", render: value => Badge.Root(value, { colorPalette: "blue" }) },
            },
            { variant: "line", striped: true }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").rows.size(), 2n));
        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 3n));
    });

    // =========================================================================
    // Complex Type Columns (require value function)
    // =========================================================================

    test("creates table with array field using value function", $ => {
        // Array fields require a value function to extract a sortable value
        const table = $.let(Table.Root(
            [
                { name: "Alice", tags: ["admin", "active"] },
                { name: "Bob", tags: ["user"] },
            ],
            {
                name: { header: "Name" },
                tags: {
                    header: "Tags",
                    // Extract array length as sortable integer value
                    value: (tags) => tags.size(),
                    render: (tags) => Stack.HStack(tags.map(($, tag) => Badge.Root(tag, { variant: "subtle" }))),
                },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
        $(Assert.equal(table.unwrap().unwrap("Table").rows.size(), 2n));
    });

    test("creates table with struct field using value function", $ => {
        // Struct fields require a value function to extract a sortable value
        const table = $.let(Table.Root(
            [
                { name: "Project A", metadata: { priority: 1n, owner: "Alice" } },
                { name: "Project B", metadata: { priority: 3n, owner: "Bob" } },
            ],
            {
                name: { header: "Name" },
                metadata: {
                    header: "Priority",
                    // Extract priority as sortable integer value (plain expression, not wrapped in variant)
                    value: (meta) => meta.priority,
                    render: (meta) => Text.Root(East.str`Priority: ${meta.priority}`),
                },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
        $(Assert.equal(table.unwrap().unwrap("Table").rows.size(), 2n));
    });

    test("creates table with array field extracting string value", $ => {
        // Extract first tag as string value for sorting
        const table = $.let(Table.Root(
            [
                { name: "Alice", skills: ["TypeScript", "React", "Node"] },
                { name: "Bob", skills: ["Python", "Django"] },
            ],
            {
                name: { header: "Name" },
                skills: {
                    header: "Primary Skill",
                    // Extract first skill as sortable string value (plain expression)
                    value: (skills) => skills.get(0n),
                    render: (skills) => Badge.Root(skills.get(0n), { variant: "subtle" }),
                },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 2n));
    });

    test("creates table mixing primitive and complex columns", $ => {
        // Mix of primitive fields (no value function needed) and complex fields (value function required)
        const table = $.let(Table.Root(
            [
                { id: 1n, name: "Alice", contact: { email: "alice@example.com", phone: "555-1234" } },
                { id: 2n, name: "Bob", contact: { email: "bob@example.com", phone: "555-5678" } },
            ],
            {
                id: { header: "ID" },  // Primitive - no value function needed
                name: { header: "Name" },  // Primitive - no value function needed
                contact: {
                    header: "Contact",
                    // Extract email as sortable string value (plain expression)
                    value: (contact) => contact.email,
                    render: (contact) => Text.Root(contact.email),
                },
            }
        ));

        $(Assert.equal(table.unwrap().unwrap("Table").columns.size(), 3n));
        $(Assert.equal(table.unwrap().unwrap("Table").rows.size(), 2n));
    });
}, {   platformFns: TestImpl,});
