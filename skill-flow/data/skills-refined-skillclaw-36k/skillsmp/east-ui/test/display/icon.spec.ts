/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { Icon } from "../../src/display/icon/index.js";
import { describeEast as describe, Assert, TestImpl } from "@elaraai/east-node-std";

describe("Icon", (test) => {
    // =========================================================================
    // Icon.Root - Basic with prefix
    // =========================================================================

    test("creates solid icon with name", $ => {
        const icon = $.let(Icon.Root("fas", "user"));

        $(Assert.equal(icon.unwrap().unwrap("Icon").prefix, "fas"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "user"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").style.hasTag("none"), true));
    });

    test("creates regular icon", $ => {
        const icon = $.let(Icon.Root("far", "heart"));

        $(Assert.equal(icon.unwrap().unwrap("Icon").prefix, "far"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "heart"));
    });

    test("creates brands icon", $ => {
        const icon = $.let(Icon.Root("fab", "github"));

        $(Assert.equal(icon.unwrap().unwrap("Icon").prefix, "fab"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "github"));
    });

    test("creates folder icon", $ => {
        const icon = $.let(Icon.Root("fas", "folder"));

        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "folder"));
    });

    test("creates chevron icon", $ => {
        const icon = $.let(Icon.Root("fas", "chevron-right"));

        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "chevron-right"));
    });

    // =========================================================================
    // Icon.Root - Size
    // =========================================================================

    test("creates icon with xs size", $ => {
        const icon = $.let(Icon.Root("fas", "user", { size: "xs" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").size.unwrap("some").hasTag("xs"), true));
    });

    test("creates icon with sm size", $ => {
        const icon = $.let(Icon.Root("fas", "user", { size: "sm" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates icon with md size", $ => {
        const icon = $.let(Icon.Root("fas", "user", { size: "md" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").size.unwrap("some").hasTag("md"), true));
    });

    test("creates icon with lg size", $ => {
        const icon = $.let(Icon.Root("fas", "user", { size: "lg" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates icon with xl size", $ => {
        const icon = $.let(Icon.Root("fas", "user", { size: "xl" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").size.unwrap("some").hasTag("xl"), true));
    });

    test("creates icon with 2xl size", $ => {
        const icon = $.let(Icon.Root("fas", "user", { size: "2xl" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").size.unwrap("some").hasTag("2xl"), true));
    });

    // =========================================================================
    // Icon.Root - Color
    // =========================================================================

    test("creates icon with color", $ => {
        const icon = $.let(Icon.Root("fas", "heart", { color: "red.500" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").color.unwrap("some"), "red.500"));
    });

    test("creates icon with CSS color", $ => {
        const icon = $.let(Icon.Root("fas", "star", { color: "#FFD700" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").color.unwrap("some"), "#FFD700"));
    });

    // =========================================================================
    // Icon.Root - Color Palette
    // =========================================================================

    test("creates icon with blue color palette", $ => {
        const icon = $.let(Icon.Root("fas", "info", { colorPalette: "blue" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates icon with red color palette", $ => {
        const icon = $.let(Icon.Root("fas", "circle-exclamation", { colorPalette: "red" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").colorPalette.unwrap("some").hasTag("red"), true));
    });

    // =========================================================================
    // Icon.Root - Combined Styles
    // =========================================================================

    test("creates icon with all style properties", $ => {
        const icon = $.let(Icon.Root("fas", "check", {
            size: "lg",
            color: "green.500",
            colorPalette: "green",
        }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").prefix, "fas"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "check"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").size.unwrap("some").hasTag("lg"), true));
        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").color.unwrap("some"), "green.500"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").colorPalette.unwrap("some").hasTag("green"), true));
    });

    // =========================================================================
    // Icon.Root - Tree View Use Cases
    // =========================================================================

    test("creates folder-open icon for tree view", $ => {
        const icon = $.let(Icon.Root("far", "folder-open"));

        $(Assert.equal(icon.unwrap().unwrap("Icon").prefix, "far"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "folder-open"));
    });

    test("creates file icon for tree view", $ => {
        const icon = $.let(Icon.Root("far", "file", { size: "sm" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").prefix, "far"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "file"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates code file icon for tree view", $ => {
        const icon = $.let(Icon.Root("fas", "file-code", { color: "blue.500" }));

        $(Assert.equal(icon.unwrap().unwrap("Icon").name, "file-code"));
        $(Assert.equal(icon.unwrap().unwrap("Icon").style.unwrap("some").color.unwrap("some"), "blue.500"));
    });
}, {   platformFns: TestImpl,});
