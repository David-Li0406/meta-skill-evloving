/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Text, Style } from "../../src/index.js";

describeEast("Text", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates text with string value", $ => {
        const text = $.let(Text.Root("Hello"));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Hello"));
    });

    // =========================================================================
    // Style Properties - Individual
    // =========================================================================

    test("creates text with color", $ => {
        const text = $.let(Text.Root("Colored", {
            color: "blue.500",
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Colored"));
        $(Assert.equal(text.unwrap().unwrap("Text").color.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").color.unwrap("some"), "blue.500"));
    });

    test("creates text with background", $ => {
        const text = $.let(Text.Root("Background", {
            background: "gray.100",
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Background"));
        $(Assert.equal(text.unwrap().unwrap("Text").background.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").background.unwrap("some"), "gray.100"));
    });

    test("creates text with fontWeight", $ => {
        const text = $.let(Text.Root("Bold", {
            fontWeight: Style.FontWeight("bold"),
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Bold"));
        $(Assert.equal(text.unwrap().unwrap("Text").fontWeight.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").fontWeight.unwrap("some").hasTag("bold"), true));
    });

    test("creates text with fontStyle", $ => {
        const text = $.let(Text.Root("Italic", {
            fontStyle: Style.FontStyle("italic"),
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Italic"));
        $(Assert.equal(text.unwrap().unwrap("Text").fontStyle.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").fontStyle.unwrap("some").hasTag("italic"), true));
    });

    test("creates text with textTransform", $ => {
        const text = $.let(Text.Root("uppercase", {
            textTransform: Style.TextTransform("uppercase"),
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "uppercase"));
        $(Assert.equal(text.unwrap().unwrap("Text").textTransform.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").textTransform.unwrap("some").hasTag("uppercase"), true));
    });

    test("creates text with textAlign", $ => {
        const text = $.let(Text.Root("Centered", {
            textAlign: Style.TextAlign("center"),
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Centered"));
        $(Assert.equal(text.unwrap().unwrap("Text").textAlign.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").textAlign.unwrap("some").hasTag("center"), true));
    });

    test("creates text with borderWidth", $ => {
        const text = $.let(Text.Root("Bordered", {
            borderWidth: Style.BorderWidth("thin"),
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Bordered"));
        $(Assert.equal(text.unwrap().unwrap("Text").borderWidth.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderWidth.unwrap("some").hasTag("thin"), true));
    });

    test("creates text with borderStyle", $ => {
        const text = $.let(Text.Root("Bordered", {
            borderStyle: Style.BorderStyle("solid"),
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Bordered"));
        $(Assert.equal(text.unwrap().unwrap("Text").borderStyle.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderStyle.unwrap("some").hasTag("solid"), true));
    });

    test("creates text with borderColor", $ => {
        const text = $.let(Text.Root("Bordered", {
            borderColor: "red.500",
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Bordered"));
        $(Assert.equal(text.unwrap().unwrap("Text").borderColor.hasTag("some"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderColor.unwrap("some"), "red.500"));
    });

    // =========================================================================
    // No Style - Defaults to None
    // =========================================================================

    test("creates text with no style - all options are none", $ => {
        const text = $.let(Text.Root("Plain"));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Plain"));
        $(Assert.equal(text.unwrap().unwrap("Text").color.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").background.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").fontWeight.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").fontStyle.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").textTransform.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").textAlign.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderWidth.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderStyle.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderColor.hasTag("none"), true));
    });

    // =========================================================================
    // Multiple Style Properties
    // =========================================================================

    test("creates text with multiple styles", $ => {
        const text = $.let(Text.Root("Styled", {
            color: "blue.500",
            fontWeight: Style.FontWeight("bold"),
            textAlign: Style.TextAlign("center"),
            background: "yellow.100",
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").value, "Styled"));
        $(Assert.equal(text.unwrap().unwrap("Text").color.unwrap("some"), "blue.500"));
        $(Assert.equal(text.unwrap().unwrap("Text").fontWeight.unwrap("some").hasTag("bold"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").textAlign.unwrap("some").hasTag("center"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").background.unwrap("some"), "yellow.100"));
        // Other styles should be none
        $(Assert.equal(text.unwrap().unwrap("Text").fontStyle.hasTag("none"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderWidth.hasTag("none"), true));
    });

    // =========================================================================
    // All Font Weights
    // =========================================================================

    test("supports all font weights", $ => {
        const normal = $.let(Text.Root("normal", { fontWeight: Style.FontWeight("normal") }));
        const bold = $.let(Text.Root("bold", { fontWeight: Style.FontWeight("bold") }));
        const semibold = $.let(Text.Root("semibold", { fontWeight: Style.FontWeight("semibold") }));
        const medium = $.let(Text.Root("medium", { fontWeight: Style.FontWeight("medium") }));
        const light = $.let(Text.Root("light", { fontWeight: Style.FontWeight("light") }));

        $(Assert.equal(normal.unwrap().unwrap("Text").fontWeight.unwrap("some").hasTag("normal"), true));
        $(Assert.equal(bold.unwrap().unwrap("Text").fontWeight.unwrap("some").hasTag("bold"), true));
        $(Assert.equal(semibold.unwrap().unwrap("Text").fontWeight.unwrap("some").hasTag("semibold"), true));
        $(Assert.equal(medium.unwrap().unwrap("Text").fontWeight.unwrap("some").hasTag("medium"), true));
        $(Assert.equal(light.unwrap().unwrap("Text").fontWeight.unwrap("some").hasTag("light"), true));
    });

    // =========================================================================
    // All Text Alignments
    // =========================================================================

    test("supports all text alignments", $ => {
        const left = $.let(Text.Root("left", { textAlign: Style.TextAlign("left") }));
        const center = $.let(Text.Root("center", { textAlign: Style.TextAlign("center") }));
        const right = $.let(Text.Root("right", { textAlign: Style.TextAlign("right") }));
        const justify = $.let(Text.Root("justify", { textAlign: Style.TextAlign("justify") }));

        $(Assert.equal(left.unwrap().unwrap("Text").textAlign.unwrap("some").hasTag("left"), true));
        $(Assert.equal(center.unwrap().unwrap("Text").textAlign.unwrap("some").hasTag("center"), true));
        $(Assert.equal(right.unwrap().unwrap("Text").textAlign.unwrap("some").hasTag("right"), true));
        $(Assert.equal(justify.unwrap().unwrap("Text").textAlign.unwrap("some").hasTag("justify"), true));
    });

    // =========================================================================
    // All Text Transforms
    // =========================================================================

    test("supports all text transforms", $ => {
        const uppercase = $.let(Text.Root("a", { textTransform: Style.TextTransform("uppercase") }));
        const lowercase = $.let(Text.Root("A", { textTransform: Style.TextTransform("lowercase") }));
        const capitalize = $.let(Text.Root("hello", { textTransform: Style.TextTransform("capitalize") }));
        const none = $.let(Text.Root("Hello", { textTransform: Style.TextTransform("none") }));

        $(Assert.equal(uppercase.unwrap().unwrap("Text").textTransform.unwrap("some").hasTag("uppercase"), true));
        $(Assert.equal(lowercase.unwrap().unwrap("Text").textTransform.unwrap("some").hasTag("lowercase"), true));
        $(Assert.equal(capitalize.unwrap().unwrap("Text").textTransform.unwrap("some").hasTag("capitalize"), true));
        $(Assert.equal(none.unwrap().unwrap("Text").textTransform.unwrap("some").hasTag("none"), true));
    });

    // =========================================================================
    // All Border Widths
    // =========================================================================

    test("supports all border widths", $ => {
        const noBorder = $.let(Text.Root("none", { borderWidth: Style.BorderWidth("none") }));
        const thin = $.let(Text.Root("thin", { borderWidth: Style.BorderWidth("thin") }));
        const medium = $.let(Text.Root("medium", { borderWidth: Style.BorderWidth("medium") }));
        const thick = $.let(Text.Root("thick", { borderWidth: Style.BorderWidth("thick") }));

        $(Assert.equal(noBorder.unwrap().unwrap("Text").borderWidth.unwrap("some").hasTag("none"), true));
        $(Assert.equal(thin.unwrap().unwrap("Text").borderWidth.unwrap("some").hasTag("thin"), true));
        $(Assert.equal(medium.unwrap().unwrap("Text").borderWidth.unwrap("some").hasTag("medium"), true));
        $(Assert.equal(thick.unwrap().unwrap("Text").borderWidth.unwrap("some").hasTag("thick"), true));
    });

    // =========================================================================
    // All Border Styles
    // =========================================================================

    test("supports all border styles", $ => {
        const solid = $.let(Text.Root("solid", { borderStyle: Style.BorderStyle("solid") }));
        const dashed = $.let(Text.Root("dashed", { borderStyle: Style.BorderStyle("dashed") }));
        const dotted = $.let(Text.Root("dotted", { borderStyle: Style.BorderStyle("dotted") }));
        const double_ = $.let(Text.Root("double", { borderStyle: Style.BorderStyle("double") }));
        const noBorder = $.let(Text.Root("none", { borderStyle: Style.BorderStyle("none") }));

        $(Assert.equal(solid.unwrap().unwrap("Text").borderStyle.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(dashed.unwrap().unwrap("Text").borderStyle.unwrap("some").hasTag("dashed"), true));
        $(Assert.equal(dotted.unwrap().unwrap("Text").borderStyle.unwrap("some").hasTag("dotted"), true));
        $(Assert.equal(double_.unwrap().unwrap("Text").borderStyle.unwrap("some").hasTag("double"), true));
        $(Assert.equal(noBorder.unwrap().unwrap("Text").borderStyle.unwrap("some").hasTag("none"), true));
    });

    // =========================================================================
    // Full Border Configuration
    // =========================================================================

    test("creates text with full border configuration", $ => {
        const text = $.let(Text.Root("Bordered", {
            borderWidth: Style.BorderWidth("medium"),
            borderStyle: Style.BorderStyle("solid"),
            borderColor: "gray.300",
        }));

        $(Assert.equal(text.unwrap().unwrap("Text").borderWidth.unwrap("some").hasTag("medium"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderStyle.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(text.unwrap().unwrap("Text").borderColor.unwrap("some"), "gray.300"));
    });
}, {   platformFns: TestImpl,});
