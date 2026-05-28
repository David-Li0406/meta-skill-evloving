/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Menu, Button, Text } from "../../src/index.js";

describeEast("Menu", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates basic menu with button trigger", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Actions"),
            [
                Menu.Item("edit", "Edit"),
                Menu.Item("delete", "Delete"),
            ]
        ));

        $(Assert.equal(menu.unwrap().getTag(), "Menu"));
        $(Assert.equal(menu.unwrap().unwrap("Menu").trigger.unwrap().getTag(), "Button"));
        $(Assert.equal(menu.unwrap().unwrap("Menu").items.size(), 2n));
    });

    test("creates menu with text trigger", $ => {
        const menu = $.let(Menu.Root(
            Text.Root("Options"),
            [
                Menu.Item("view", "View"),
            ]
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").trigger.unwrap().getTag(), "Text"));
    });

    test("creates menu with default options", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Menu"),
            [Menu.Item("item", "Item")]
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.hasTag("none"), true));
    });

    // =========================================================================
    // Menu Items
    // =========================================================================

    test("creates menu item with value and label", $ => {
        const item = $.let(Menu.Item("save", "Save"));

        $(Assert.equal(item.getTag(), "Item"));
        $(Assert.equal(item.unwrap("Item").value, "save"));
        $(Assert.equal(item.unwrap("Item").label, "Save"));
        $(Assert.equal(item.unwrap("Item").disabled.hasTag("none"), true));
    });

    test("creates disabled menu item", $ => {
        const item = $.let(Menu.Item("locked", "Locked Action", true));

        $(Assert.equal(item.unwrap("Item").disabled.hasTag("some"), true));
        $(Assert.equal(item.unwrap("Item").disabled.unwrap("some"), true));
    });

    test("creates enabled menu item explicitly", $ => {
        const item = $.let(Menu.Item("enabled", "Enabled Action", false));

        $(Assert.equal(item.unwrap("Item").disabled.unwrap("some"), false));
    });

    test("creates menu separator", $ => {
        const separator = $.let(Menu.Separator());

        $(Assert.equal(separator.getTag(), "Separator"));
    });

    // =========================================================================
    // Menu with Separators
    // =========================================================================

    test("creates menu with separators", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("File"),
            [
                Menu.Item("new", "New"),
                Menu.Item("open", "Open"),
                Menu.Separator(),
                Menu.Item("save", "Save"),
                Menu.Separator(),
                Menu.Item("exit", "Exit"),
            ]
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").items.size(), 6n));
        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(0n).getTag(), "Item"));
        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(2n).getTag(), "Separator"));
        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(4n).getTag(), "Separator"));
    });

    // =========================================================================
    // Placement
    // =========================================================================

    test("creates menu with bottom placement", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Actions"),
            [Menu.Item("action", "Action")],
            { placement: "bottom" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.hasTag("some"), true));
        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.unwrap("some").hasTag("bottom"), true));
    });

    test("creates menu with bottom-start placement", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Actions"),
            [Menu.Item("action", "Action")],
            { placement: "bottom-start" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.unwrap("some").hasTag("bottom-start"), true));
    });

    test("creates menu with bottom-end placement", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Actions"),
            [Menu.Item("action", "Action")],
            { placement: "bottom-end" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.unwrap("some").hasTag("bottom-end"), true));
    });

    test("creates menu with top placement", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Actions"),
            [Menu.Item("action", "Action")],
            { placement: "top" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.unwrap("some").hasTag("top"), true));
    });

    test("creates menu with right placement", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Submenu"),
            [Menu.Item("action", "Action")],
            { placement: "right" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.unwrap("some").hasTag("right"), true));
    });

    test("creates menu with left placement", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Submenu"),
            [Menu.Item("action", "Action")],
            { placement: "left" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.unwrap("some").hasTag("left"), true));
    });

    // =========================================================================
    // Practical Examples
    // =========================================================================

    test("creates file menu", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("File"),
            [
                Menu.Item("new", "New File"),
                Menu.Item("open", "Open..."),
                Menu.Item("open-recent", "Open Recent"),
                Menu.Separator(),
                Menu.Item("save", "Save"),
                Menu.Item("save-as", "Save As..."),
                Menu.Separator(),
                Menu.Item("close", "Close"),
            ],
            { placement: "bottom-start" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").items.size(), 8n));
        $(Assert.equal(menu.unwrap().unwrap("Menu").trigger.unwrap().unwrap("Button").label, "File"));
    });

    test("creates context menu", $ => {
        const menu = $.let(Menu.Root(
            Text.Root("Right-click me"),
            [
                Menu.Item("cut", "Cut"),
                Menu.Item("copy", "Copy"),
                Menu.Item("paste", "Paste"),
                Menu.Separator(),
                Menu.Item("select-all", "Select All"),
            ]
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(0n).unwrap("Item").value, "cut"));
        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(3n).getTag(), "Separator"));
    });

    test("creates menu with disabled items", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Edit"),
            [
                Menu.Item("undo", "Undo", true),
                Menu.Item("redo", "Redo", true),
                Menu.Separator(),
                Menu.Item("cut", "Cut"),
                Menu.Item("copy", "Copy"),
                Menu.Item("paste", "Paste"),
            ],
            { placement: "bottom" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(0n).unwrap("Item").disabled.unwrap("some"), true));
        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(1n).unwrap("Item").disabled.unwrap("some"), true));
        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(3n).unwrap("Item").disabled.hasTag("none"), true));
    });

    test("creates user actions menu", $ => {
        const menu = $.let(Menu.Root(
            Button.Root("Account"),
            [
                Menu.Item("profile", "View Profile"),
                Menu.Item("settings", "Settings"),
                Menu.Separator(),
                Menu.Item("logout", "Log Out"),
            ],
            { placement: "bottom-end" }
        ));

        $(Assert.equal(menu.unwrap().unwrap("Menu").items.get(3n).unwrap("Item").value, "logout"));
        $(Assert.equal(menu.unwrap().unwrap("Menu").placement.unwrap("some").hasTag("bottom-end"), true));
    });
}, {   platformFns: TestImpl,});
