/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Tooltip, Button, Text } from "../../src/index.js";

describeEast("Tooltip", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates basic tooltip with button trigger", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover me"),
            "This is a tooltip"
        ));

        $(Assert.equal(tooltip.unwrap().getTag(), "Tooltip"));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").content, "This is a tooltip"));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").trigger.unwrap().getTag(), "Button"));
    });

    test("creates tooltip with text trigger", $ => {
        const tooltip = $.let(Tooltip.Root(
            Text.Root("Hover for info"),
            "Additional information"
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").content, "Additional information"));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").trigger.unwrap().getTag(), "Text"));
    });

    test("creates tooltip with default options", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Help"),
            "Help text"
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.hasTag("none"), true));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").hasArrow.hasTag("none"), true));
    });

    // =========================================================================
    // Placement
    // =========================================================================

    test("creates tooltip with top placement", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover"),
            "Tooltip above",
            { placement: "top" }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.hasTag("some"), true));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("top"), true));
    });

    test("creates tooltip with bottom placement", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover"),
            "Tooltip below",
            { placement: "bottom" }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("bottom"), true));
    });

    test("creates tooltip with left placement", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover"),
            "Tooltip left",
            { placement: "left" }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("left"), true));
    });

    test("creates tooltip with right placement", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover"),
            "Tooltip right",
            { placement: "right" }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("right"), true));
    });

    test("creates tooltip with top-start placement", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover"),
            "Tooltip top start",
            { placement: "top-start" }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("top-start"), true));
    });

    test("creates tooltip with bottom-end placement", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover"),
            "Tooltip bottom end",
            { placement: "bottom-end" }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("bottom-end"), true));
    });

    // =========================================================================
    // Arrow
    // =========================================================================

    test("creates tooltip with arrow", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover"),
            "Tooltip with arrow",
            { hasArrow: true }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").hasArrow.hasTag("some"), true));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").hasArrow.unwrap("some"), true));
    });

    test("creates tooltip without arrow", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Hover"),
            "Tooltip without arrow",
            { hasArrow: false }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").hasArrow.unwrap("some"), false));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates tooltip with placement and arrow", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Save"),
            "Save your changes",
            { placement: "bottom", hasArrow: true }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("bottom"), true));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").hasArrow.unwrap("some"), true));
    });

    test("creates tooltip with all options", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Delete"),
            "This action cannot be undone",
            { placement: "top", hasArrow: true }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").content, "This action cannot be undone"));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("top"), true));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").hasArrow.unwrap("some"), true));
    });

    // =========================================================================
    // Practical Examples
    // =========================================================================

    test("creates help tooltip on form field", $ => {
        const tooltip = $.let(Tooltip.Root(
            Text.Root("?"),
            "Enter your full legal name as it appears on your ID",
            { placement: "right", hasArrow: true }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").trigger.unwrap().unwrap("Text").value, "?"));
        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("right"), true));
    });

    test("creates action button tooltip", $ => {
        const tooltip = $.let(Tooltip.Root(
            Button.Root("Submit"),
            "Submit your application for review",
            { placement: "top" }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").trigger.unwrap().unwrap("Button").label, "Submit"));
    });

    test("creates info tooltip", $ => {
        const tooltip = $.let(Tooltip.Root(
            Text.Root("Terms & Conditions"),
            "Click to read our full terms and conditions",
            { placement: "bottom-start" }
        ));

        $(Assert.equal(tooltip.unwrap().unwrap("Tooltip").placement.unwrap("some").hasTag("bottom-start"), true));
    });
}, {   platformFns: TestImpl,});
