/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Accordion, Text } from "../../src/index.js";

describeEast("Accordion", (test) => {
    // =========================================================================
    // Accordion.Item
    // =========================================================================

    test("creates item with string values", $ => {
        const item = $.let(Accordion.Item("item-1", "Section 1", [
            Text.Root("Content for section 1"),
        ]));

        $(Assert.equal(item.value, "item-1"));
        $(Assert.equal(item.trigger, "Section 1"));
        $(Assert.equal(item.disabled.hasTag("none"), true));
    });

    test("creates item with multiple children", $ => {
        const item = $.let(Accordion.Item(
            "item-2",
            "Section 2",
            [
                Text.Root("First line"),
                Text.Root("Second line"),
            ]
        ));

        $(Assert.equal(item.value, "item-2"));
        $(Assert.equal(item.trigger, "Section 2"));
    });

    test("creates disabled item", $ => {
        const item = $.let(Accordion.Item("disabled-item", "Disabled Section", [
            Text.Root("Cannot expand"),
        ], {
            disabled: true,
        }));

        $(Assert.equal(item.disabled.hasTag("some"), true));
        $(Assert.equal(item.disabled.unwrap("some"), true));
    });

    test("creates enabled item explicitly", $ => {
        const item = $.let(Accordion.Item("enabled-item", "Enabled Section", [
            Text.Root("Can expand"),
        ], {
            disabled: false,
        }));

        $(Assert.equal(item.disabled.unwrap("some"), false));
    });

    // =========================================================================
    // Accordion.Root - Basic Creation
    // =========================================================================

    test("creates accordion with items", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("a", "Section A", [Text.Root("Content A")]),
            Accordion.Item("b", "Section B", [Text.Root("Content B")]),
        ]));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.hasTag("none"), true));
    });

    test("creates accordion with single item", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("single", "Only Section", [Text.Root("Content")]),
        ]));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.hasTag("none"), true));
    });

    test("creates empty accordion", $ => {
        const accordion = $.let(Accordion.Root([]));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.hasTag("none"), true));
    });

    // =========================================================================
    // Accordion.Root - Multiple
    // =========================================================================

    test("creates accordion with multiple enabled", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("a", "A", [Text.Root("Content A")]),
            Accordion.Item("b", "B", [Text.Root("Content B")]),
        ], {
            multiple: true,
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.hasTag("some"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").multiple.hasTag("some"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").multiple.unwrap("some"), true));
    });

    test("creates accordion with multiple disabled", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("a", "A", [Text.Root("Content A")]),
        ], {
            multiple: false,
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").multiple.unwrap("some"), false));
    });

    // =========================================================================
    // Accordion.Root - Collapsible
    // =========================================================================

    test("creates collapsible accordion", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("item", "Section", [Text.Root("Content")]),
        ], {
            collapsible: true,
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.hasTag("some"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").collapsible.hasTag("some"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").collapsible.unwrap("some"), true));
    });

    test("creates non-collapsible accordion", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("item", "Section", [Text.Root("Content")]),
        ], {
            collapsible: false,
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").collapsible.unwrap("some"), false));
    });

    // =========================================================================
    // Accordion.Root - Variant
    // =========================================================================

    test("creates enclosed variant accordion", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("item", "Section", [Text.Root("Content")]),
        ], {
            variant: "enclosed",
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.hasTag("some"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.hasTag("some"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.unwrap("some").hasTag("enclosed"), true));
    });

    test("creates plain variant accordion", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("item", "Section", [Text.Root("Content")]),
        ], {
            variant: "plain",
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.unwrap("some").hasTag("plain"), true));
    });

    test("creates subtle variant accordion", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("item", "Section", [Text.Root("Content")]),
        ], {
            variant: "subtle",
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates accordion with AccordionVariant helper", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("item", "Section", [Text.Root("Content")]),
        ], {
            variant: Accordion.Variant("enclosed"),
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.unwrap("some").hasTag("enclosed"), true));
    });

    // =========================================================================
    // Accordion.Root - Combined Options
    // =========================================================================

    test("creates accordion with all options", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("a", "Section A", [Text.Root("Content A")]),
            Accordion.Item("b", "Section B", [Text.Root("Content B")]),
        ], {
            multiple: true,
            collapsible: true,
            variant: "enclosed",
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").multiple.unwrap("some"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").collapsible.unwrap("some"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.unwrap("some").hasTag("enclosed"), true));
    });

    test("creates FAQ accordion", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("q1", "What is East UI?", [Text.Root("East UI is a typed UI component library.")]),
            Accordion.Item("q2", "How do I install it?", [Text.Root("Run npm install @elaraai/east-ui")]),
            Accordion.Item("q3", "Is it open source?", [Text.Root("Yes, it is licensed under AGPL-3.0")]),
        ], {
            variant: "subtle",
            collapsible: true,
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").collapsible.unwrap("some"), true));
    });

    test("creates settings panel accordion", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("general", "General Settings", [Text.Root("General configuration options")]),
            Accordion.Item("advanced", "Advanced Settings", [Text.Root("Advanced configuration options")]),
            Accordion.Item("about", "About", [Text.Root("Version and license information")]),
        ], {
            variant: "enclosed",
            multiple: true,
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.unwrap("some").hasTag("enclosed"), true));
        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").multiple.unwrap("some"), true));
    });

    test("creates navigation accordion", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("products", "Products", [Text.Root("Product categories and listings")]),
            Accordion.Item("services", "Services", [Text.Root("Service offerings")]),
            Accordion.Item("support", "Support", [Text.Root("Help and documentation")]),
        ], {
            variant: "plain",
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").variant.unwrap("some").hasTag("plain"), true));
    });

    test("creates accordion with disabled item", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("active", "Active Section", [Text.Root("Can be expanded")]),
            Accordion.Item("disabled", "Disabled Section", [Text.Root("Cannot be expanded")], { disabled: true }),
        ], {
            collapsible: true,
        }));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.unwrap("some").collapsible.unwrap("some"), true));
    });

    test("creates simple accordion without options", $ => {
        const accordion = $.let(Accordion.Root([
            Accordion.Item("one", "First", [Text.Root("First content")]),
            Accordion.Item("two", "Second", [Text.Root("Second content")]),
            Accordion.Item("three", "Third", [Text.Root("Third content")]),
        ]));

        $(Assert.equal(accordion.unwrap().unwrap("Accordion").style.hasTag("none"), true));
    });

    test("creates accordion item with nested components", $ => {
        const item = $.let(Accordion.Item("nested", "Nested Content", [
            Text.Root("Line 1"),
            Text.Root("Line 2"),
            Text.Root("Line 3"),
        ]));

        $(Assert.equal(item.value, "nested"));
        $(Assert.equal(item.trigger, "Nested Content"));
    });
}, {   platformFns: TestImpl,});
