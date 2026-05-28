/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Mark } from "../../src/index.js";

describeEast("Mark", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates mark with string value", $ => {
        const mark = $.let(Mark.Root("Important"));

        $(Assert.equal(mark.unwrap().unwrap("Mark").value, "Important"));
    });

    test("creates mark with no style - all options are none", $ => {
        const mark = $.let(Mark.Root("Text"));

        $(Assert.equal(mark.unwrap().unwrap("Mark").value, "Text"));
        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.hasTag("none"), true));
        $(Assert.equal(mark.unwrap().unwrap("Mark").colorPalette.hasTag("none"), true));
    });

    // =========================================================================
    // Variants
    // =========================================================================

    test("creates subtle variant mark", $ => {
        const mark = $.let(Mark.Root("Subtle", {
            variant: "subtle",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.hasTag("some"), true));
        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates solid variant mark", $ => {
        const mark = $.let(Mark.Root("Solid", {
            variant: "solid",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates text variant mark", $ => {
        const mark = $.let(Mark.Root("Text", {
            variant: "text",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.unwrap("some").hasTag("text"), true));
    });

    test("creates plain variant mark", $ => {
        const mark = $.let(Mark.Root("Plain", {
            variant: "plain",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.unwrap("some").hasTag("plain"), true));
    });

    // =========================================================================
    // Color Palette
    // =========================================================================

    test("creates mark with yellow colorPalette", $ => {
        const mark = $.let(Mark.Root("Highlighted", {
            colorPalette: "yellow",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").colorPalette.hasTag("some"), true));
        $(Assert.equal(mark.unwrap().unwrap("Mark").colorPalette.unwrap("some"), "yellow"));
    });

    test("creates mark with green colorPalette", $ => {
        const mark = $.let(Mark.Root("Success", {
            colorPalette: "green",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").colorPalette.unwrap("some"), "green"));
    });

    test("creates mark with red colorPalette", $ => {
        const mark = $.let(Mark.Root("Error", {
            colorPalette: "red",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").colorPalette.unwrap("some"), "red"));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates mark with all options", $ => {
        const mark = $.let(Mark.Root("Featured", {
            variant: "solid",
            colorPalette: "blue",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").value, "Featured"));
        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(mark.unwrap().unwrap("Mark").colorPalette.unwrap("some"), "blue"));
    });

    test("creates warning mark", $ => {
        const mark = $.let(Mark.Root("Warning", {
            variant: "subtle",
            colorPalette: "orange",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").value, "Warning"));
        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.unwrap("some").hasTag("subtle"), true));
        $(Assert.equal(mark.unwrap().unwrap("Mark").colorPalette.unwrap("some"), "orange"));
    });

    test("creates info mark", $ => {
        const mark = $.let(Mark.Root("Note", {
            variant: "text",
            colorPalette: "cyan",
        }));

        $(Assert.equal(mark.unwrap().unwrap("Mark").value, "Note"));
        $(Assert.equal(mark.unwrap().unwrap("Mark").variant.unwrap("some").hasTag("text"), true));
    });
}, {   platformFns: TestImpl,});
