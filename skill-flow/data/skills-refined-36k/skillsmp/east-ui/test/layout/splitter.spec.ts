/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Splitter, Style, Text } from "../../src/index.js";

describeEast("Splitter", (test) => {
    // Helper to create a simple text component (already returns UIComponentType)

    // =========================================================================
    // Splitter.Panel - Basic Creation
    // =========================================================================

    test("creates panel with content and id only", $ => {
        const content = Text.Root("Hello");
        const panel = $.let(Splitter.Panel(content, { id: "panel1" }));

        $(Assert.equal(panel.id, "panel1"));
        $(Assert.equal(panel.content.unwrap().hasTag("Text"), true));
        $(Assert.equal(panel.minSize.hasTag("none"), true));
        $(Assert.equal(panel.maxSize.hasTag("none"), true));
        $(Assert.equal(panel.collapsible.hasTag("none"), true));
        $(Assert.equal(panel.defaultCollapsed.hasTag("none"), true));
    });

    test("creates panel with minSize", $ => {
        const content = Text.Root("Content");
        const panel = $.let(Splitter.Panel(content, { id: "panel1", minSize: 20 }));

        $(Assert.equal(panel.minSize.hasTag("some"), true));
        $(Assert.equal(panel.minSize.unwrap("some"), 20.0));
    });

    test("creates panel with maxSize", $ => {
        const content = Text.Root("Content");
        const panel = $.let(Splitter.Panel(content, { id: "panel1", maxSize: 80 }));

        $(Assert.equal(panel.maxSize.hasTag("some"), true));
        $(Assert.equal(panel.maxSize.unwrap("some"), 80.0));
    });

    test("creates panel with collapsible true", $ => {
        const content = Text.Root("Content");
        const panel = $.let(Splitter.Panel(content, { id: "panel1", collapsible: true }));

        $(Assert.equal(panel.collapsible.hasTag("some"), true));
        $(Assert.equal(panel.collapsible.unwrap("some"), true));
    });

    test("creates panel with collapsible false", $ => {
        const content = Text.Root("Content");
        const panel = $.let(Splitter.Panel(content, { id: "panel1", collapsible: false }));

        $(Assert.equal(panel.collapsible.hasTag("some"), true));
        $(Assert.equal(panel.collapsible.unwrap("some"), false));
    });

    test("creates panel with defaultCollapsed true", $ => {
        const content = Text.Root("Content");
        const panel = $.let(Splitter.Panel(content, { id: "panel1", defaultCollapsed: true }));

        $(Assert.equal(panel.defaultCollapsed.hasTag("some"), true));
        $(Assert.equal(panel.defaultCollapsed.unwrap("some"), true));
    });

    test("creates panel with all options", $ => {
        const content = Text.Root("Full Panel");
        const panel = $.let(Splitter.Panel(content, {
            id: "fullPanel",
            minSize: 15,
            maxSize: 85,
            collapsible: true,
            defaultCollapsed: false,
        }));

        $(Assert.equal(panel.id, "fullPanel"));
        $(Assert.equal(panel.minSize.unwrap("some"), 15.0));
        $(Assert.equal(panel.maxSize.unwrap("some"), 85.0));
        $(Assert.equal(panel.collapsible.unwrap("some"), true));
        $(Assert.equal(panel.defaultCollapsed.unwrap("some"), false));
    });

    // =========================================================================
    // Splitter.Root - Basic Creation
    // =========================================================================

    test("creates splitter with two panels", $ => {
        const panel1 = Splitter.Panel(Text.Root("Left"), { id: "left" });
        const panel2 = Splitter.Panel(Text.Root("Right"), { id: "right" });
        const splitter = $.let(Splitter.Root([panel1, panel2], [50, 50]));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").panels.size(), 2n));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").defaultSize.size(), 2n));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").style.hasTag("none"), true));
    });

    test("creates splitter with unequal default sizes", $ => {
        const panel1 = Splitter.Panel(Text.Root("Sidebar"), { id: "sidebar" });
        const panel2 = Splitter.Panel(Text.Root("Main"), { id: "main" });
        const splitter = $.let(Splitter.Root([panel1, panel2], [30, 70]));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").panels.size(), 2n));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").defaultSize.size(), 2n));
    });

    test("creates splitter with three panels", $ => {
        const panel1 = Splitter.Panel(Text.Root("Left"), { id: "left" });
        const panel2 = Splitter.Panel(Text.Root("Center"), { id: "center" });
        const panel3 = Splitter.Panel(Text.Root("Right"), { id: "right" });
        const splitter = $.let(Splitter.Root([panel1, panel2, panel3], [25, 50, 25]));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").panels.size(), 3n));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").defaultSize.size(), 3n));
    });

    // =========================================================================
    // Splitter.Root - Orientation
    // =========================================================================

    test("creates horizontal splitter", $ => {
        const panel1 = Splitter.Panel(Text.Root("Left"), { id: "left" });
        const panel2 = Splitter.Panel(Text.Root("Right"), { id: "right" });
        const splitter = $.let(Splitter.Root([panel1, panel2], [50, 50], { orientation: Style.Orientation("horizontal") }));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").style.hasTag("some"), true));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").style.unwrap("some").orientation.hasTag("some"), true));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").style.unwrap("some").orientation.unwrap("some").hasTag("horizontal"), true));
    });

    test("creates vertical splitter", $ => {
        const panel1 = Splitter.Panel(Text.Root("Top"), { id: "top" });
        const panel2 = Splitter.Panel(Text.Root("Bottom"), { id: "bottom" });
        const splitter = $.let(Splitter.Root([panel1, panel2], [60, 40], { orientation: Style.Orientation("vertical") }));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").style.unwrap("some").orientation.unwrap("some").hasTag("vertical"), true));
    });

    test("creates splitter with string orientation", $ => {
        const panel1 = Splitter.Panel(Text.Root("Left"), { id: "left" });
        const panel2 = Splitter.Panel(Text.Root("Right"), { id: "right" });
        const splitter = $.let(Splitter.Root([panel1, panel2], [50, 50], { orientation: "horizontal" }));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").style.unwrap("some").orientation.unwrap("some").hasTag("horizontal"), true));
    });

    // =========================================================================
    // Typical Use Cases
    // =========================================================================

    test("creates sidebar layout", $ => {
        const sidebar = Splitter.Panel(Text.Root("Sidebar"), {
            id: "sidebar",
            minSize: 15,
            maxSize: 40,
            collapsible: true,
        });
        const main = Splitter.Panel(Text.Root("Main Content"), {
            id: "main",
            minSize: 50,
        });

        const splitter = $.let(Splitter.Root([sidebar, main], [25, 75], { orientation: "horizontal" }));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").panels.size(), 2n));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").style.unwrap("some").orientation.unwrap("some").hasTag("horizontal"), true));
    });

    test("creates editor with terminal layout", $ => {
        const editor = Splitter.Panel(Text.Root("Code Editor"), {
            id: "editor",
            minSize: 30,
        });
        const terminal = Splitter.Panel(Text.Root("Terminal"), {
            id: "terminal",
            minSize: 10,
            collapsible: true,
        });

        const splitter = $.let(Splitter.Root([editor, terminal], [70, 30], { orientation: "vertical" }));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").panels.size(), 2n));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").style.unwrap("some").orientation.unwrap("some").hasTag("vertical"), true));
    });

    test("creates three-column layout", $ => {
        const left = Splitter.Panel(Text.Root("Left"), { id: "left", collapsible: true });
        const center = Splitter.Panel(Text.Root("Center"), { id: "center", minSize: 40 });
        const right = Splitter.Panel(Text.Root("Right"), { id: "right", collapsible: true });

        const splitter = $.let(Splitter.Root([left, center, right], [20, 60, 20], { orientation: "horizontal" }));

        $(Assert.equal(splitter.unwrap().unwrap("Splitter").panels.size(), 3n));
        $(Assert.equal(splitter.unwrap().unwrap("Splitter").defaultSize.size(), 3n));
    });
}, {   platformFns: TestImpl,});
