/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Tabs, Text } from "../../src/index.js";

describeEast("Tabs", (test) => {
    // =========================================================================
    // Tabs.Item
    // =========================================================================

    test("creates item with string values", $ => {
        const item = $.let(Tabs.Item("tab-1", "Tab 1", [
            Text.Root("Content for tab 1"),
        ]));

        $(Assert.equal(item.value, "tab-1"));
        $(Assert.equal(item.trigger, "Tab 1"));
        $(Assert.equal(item.disabled.hasTag("none"), true));
    });

    test("creates item with multiple children", $ => {
        const item = $.let(Tabs.Item(
            "tab-2",
            "Tab 2",
            [
                Text.Root("First line"),
                Text.Root("Second line"),
            ]
        ));

        $(Assert.equal(item.value, "tab-2"));
        $(Assert.equal(item.trigger, "Tab 2"));
    });

    test("creates disabled item", $ => {
        const item = $.let(Tabs.Item("disabled-tab", "Disabled Tab", [
            Text.Root("Cannot select"),
        ], {
            disabled: true,
        }));

        $(Assert.equal(item.disabled.hasTag("some"), true));
        $(Assert.equal(item.disabled.unwrap("some"), true));
    });

    test("creates enabled item explicitly", $ => {
        const item = $.let(Tabs.Item("enabled-tab", "Enabled Tab", [
            Text.Root("Can select"),
        ], {
            disabled: false,
        }));

        $(Assert.equal(item.disabled.unwrap("some"), false));
    });

    // =========================================================================
    // Tabs.Root - Basic Creation
    // =========================================================================

    test("creates tabs with items", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "Tab A", [Text.Root("Content A")]),
            Tabs.Item("b", "Tab B", [Text.Root("Content B")]),
        ]));

        $(Assert.equal(tabs.unwrap().getTag(), "Tabs"));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.hasTag("none"), true));
    });

    test("creates tabs with single item", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("single", "Only Tab", [Text.Root("Content")]),
        ]));

        $(Assert.equal(tabs.unwrap().getTag(), "Tabs"));
    });

    test("creates empty tabs", $ => {
        const tabs = $.let(Tabs.Root([]));

        $(Assert.equal(tabs.unwrap().getTag(), "Tabs"));
    });

    // =========================================================================
    // Tabs.Root - Default Value
    // =========================================================================

    test("creates tabs with defaultValue", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content A")]),
            Tabs.Item("b", "B", [Text.Root("Content B")]),
        ], {
            defaultValue: "a",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").defaultValue.hasTag("some"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").defaultValue.unwrap("some"), "a"));
    });

    test("creates tabs with controlled value", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content A")]),
            Tabs.Item("b", "B", [Text.Root("Content B")]),
        ], {
            value: "b",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").value.hasTag("some"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").value.unwrap("some"), "b"));
    });

    // =========================================================================
    // Tabs.Root - Variants
    // =========================================================================

    test("creates tabs with line variant", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            variant: "line",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.hasTag("some"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").variant.hasTag("some"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").variant.unwrap("some").hasTag("line"), true));
    });

    test("creates tabs with subtle variant", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            variant: "subtle",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates tabs with enclosed variant", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            variant: "enclosed",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").variant.unwrap("some").hasTag("enclosed"), true));
    });

    test("creates tabs with outline variant", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            variant: "outline",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates tabs with plain variant", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            variant: "plain",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").variant.unwrap("some").hasTag("plain"), true));
    });

    // =========================================================================
    // Tabs.Root - Size
    // =========================================================================

    test("creates tabs with sm size", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            size: "sm",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates tabs with md size", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            size: "md",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").size.unwrap("some").hasTag("md"), true));
    });

    test("creates tabs with lg size", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            size: "lg",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").size.unwrap("some").hasTag("lg"), true));
    });

    // =========================================================================
    // Tabs.Root - Orientation
    // =========================================================================

    test("creates horizontal tabs", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            orientation: "horizontal",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").orientation.unwrap("some").hasTag("horizontal"), true));
    });

    test("creates vertical tabs", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            orientation: "vertical",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").orientation.unwrap("some").hasTag("vertical"), true));
    });

    // =========================================================================
    // Tabs.Root - Fitted
    // =========================================================================

    test("creates fitted tabs", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            fitted: true,
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").fitted.unwrap("some"), true));
    });

    // =========================================================================
    // Tabs.Root - Justify
    // =========================================================================

    test("creates tabs with start justify", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            justify: "start",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").justify.unwrap("some").hasTag("start"), true));
    });

    test("creates tabs with center justify", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            justify: "center",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").justify.unwrap("some").hasTag("center"), true));
    });

    test("creates tabs with end justify", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            justify: "end",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").justify.unwrap("some").hasTag("end"), true));
    });

    // =========================================================================
    // Tabs.Root - Lazy Mount
    // =========================================================================

    test("creates tabs with lazy mount", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            lazyMount: true,
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").lazyMount.unwrap("some"), true));
    });

    test("creates tabs with unmount on exit", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            unmountOnExit: true,
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").unmountOnExit.unwrap("some"), true));
    });

    // =========================================================================
    // Tabs.Root - Activation Mode
    // =========================================================================

    test("creates tabs with automatic activation", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            activationMode: "automatic",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").activationMode.unwrap("some").hasTag("automatic"), true));
    });

    test("creates tabs with manual activation", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            activationMode: "manual",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").activationMode.unwrap("some").hasTag("manual"), true));
    });

    // =========================================================================
    // Tabs.Root - Color Palette
    // =========================================================================

    test("creates tabs with blue color palette", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            colorPalette: "blue",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates tabs with green color palette", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("a", "A", [Text.Root("Content")]),
        ], {
            colorPalette: "green",
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").colorPalette.unwrap("some").hasTag("green"), true));
    });

    // =========================================================================
    // Tabs.Root - Complete Example
    // =========================================================================

    test("creates complete tabs with all options", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("overview", "Overview", [Text.Root("Overview content")]),
            Tabs.Item("settings", "Settings", [Text.Root("Settings content")]),
            Tabs.Item("billing", "Billing", [Text.Root("Billing content")], { disabled: true }),
        ], {
            defaultValue: "overview",
            variant: "enclosed",
            size: "md",
            fitted: true,
            colorPalette: "blue",
        }));

        $(Assert.equal(tabs.unwrap().getTag(), "Tabs"));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").defaultValue.unwrap("some"), "overview"));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").variant.unwrap("some").hasTag("enclosed"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").fitted.unwrap("some"), true));
    });

    test("creates vertical tabs with lazy loading", $ => {
        const tabs = $.let(Tabs.Root([
            Tabs.Item("profile", "Profile", [Text.Root("Profile content")]),
            Tabs.Item("security", "Security", [Text.Root("Security content")]),
        ], {
            orientation: "vertical",
            variant: "subtle",
            lazyMount: true,
            unmountOnExit: true,
        }));

        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").orientation.unwrap("some").hasTag("vertical"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").lazyMount.unwrap("some"), true));
        $(Assert.equal(tabs.unwrap().unwrap("Tabs").style.unwrap("some").unmountOnExit.unwrap("some"), true));
    });
}, {   platformFns: TestImpl,});
