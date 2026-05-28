/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Tag, Style } from "../../src/index.js";

describeEast("Tag", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates tag with string label", $ => {
        const tag = $.let(Tag.Root("JavaScript"));

        $(Assert.equal(tag.unwrap().unwrap("Tag").label, "JavaScript"));
        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.hasTag("none"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").colorPalette.hasTag("none"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").size.hasTag("none"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").closable.hasTag("none"), true));
    });

    test("creates tag with expression label", $ => {
        const tag = $.let(Tag.Root("TypeScript"));

        $(Assert.equal(tag.unwrap().unwrap("Tag").label, "TypeScript"));
    });

    // =========================================================================
    // Variants
    // =========================================================================

    test("creates solid variant tag", $ => {
        const tag = $.let(Tag.Root("Featured", {
            variant: "solid",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.hasTag("some"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates subtle variant tag", $ => {
        const tag = $.let(Tag.Root("Category", {
            variant: "subtle",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates outline variant tag", $ => {
        const tag = $.let(Tag.Root("Label", {
            variant: "outline",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates tag with Style.StyleVariant helper", $ => {
        const tag = $.let(Tag.Root("Styled", {
            variant: Style.StyleVariant("solid"),
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.unwrap("some").hasTag("solid"), true));
    });

    // =========================================================================
    // Color Palettes
    // =========================================================================

    test("creates tag with blue color palette", $ => {
        const tag = $.let(Tag.Root("React", {
            colorPalette: "blue",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").colorPalette.hasTag("some"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates tag with green color palette", $ => {
        const tag = $.let(Tag.Root("Active", {
            colorPalette: "green",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").colorPalette.unwrap("some").hasTag("green"), true));
    });

    test("creates tag with cyan color palette", $ => {
        const tag = $.let(Tag.Root("Node.js", {
            colorPalette: "cyan",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").colorPalette.unwrap("some").hasTag("cyan"), true));
    });

    test("creates tag with Style.ColorScheme helper", $ => {
        const tag = $.let(Tag.Root("Premium", {
            colorPalette: Style.ColorScheme("purple"),
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates small tag", $ => {
        const tag = $.let(Tag.Root("SM", {
            size: "sm",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").size.hasTag("some"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium tag", $ => {
        const tag = $.let(Tag.Root("MD", {
            size: "md",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large tag", $ => {
        const tag = $.let(Tag.Root("LG", {
            size: "lg",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates extra large tag", $ => {
        const tag = $.let(Tag.Root("XL", {
            size: "xl",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").size.unwrap("some").hasTag("xl"), true));
    });

    test("creates tag with string literal size", $ => {
        const tag = $.let(Tag.Root("Sized", {
            size: "md",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").size.unwrap("some").hasTag("md"), true));
    });

    // =========================================================================
    // Closable
    // =========================================================================

    test("creates closable tag", $ => {
        const tag = $.let(Tag.Root("Removable", {
            closable: true,
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").closable.hasTag("some"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").closable.unwrap("some"), true));
    });

    test("creates non-closable tag explicitly", $ => {
        const tag = $.let(Tag.Root("Fixed", {
            closable: false,
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").closable.unwrap("some"), false));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates tag with all options", $ => {
        const tag = $.let(Tag.Root("Complete", {
            variant: "solid",
            colorPalette: "blue",
            size: "md",
            closable: true,
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").label, "Complete"));
        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").colorPalette.unwrap("some").hasTag("blue"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").closable.unwrap("some"), true));
    });

    test("creates programming language tag", $ => {
        const tag = $.let(Tag.Root("Python", {
            colorPalette: "yellow",
            variant: "subtle",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").label, "Python"));
        $(Assert.equal(tag.unwrap().unwrap("Tag").colorPalette.unwrap("some").hasTag("yellow"), true));
    });

    test("creates filter chip tag", $ => {
        const tag = $.let(Tag.Root("Technology", {
            colorPalette: "blue",
            closable: true,
            size: "sm",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").closable.unwrap("some"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates status tag", $ => {
        const tag = $.let(Tag.Root("In Progress", {
            colorPalette: "orange",
            variant: "solid",
            size: "sm",
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").label, "In Progress"));
        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates removable skill tag", $ => {
        const tag = $.let(Tag.Root("React", {
            colorPalette: "cyan",
            variant: "outline",
            closable: true,
        }));

        $(Assert.equal(tag.unwrap().unwrap("Tag").variant.unwrap("some").hasTag("outline"), true));
        $(Assert.equal(tag.unwrap().unwrap("Tag").closable.unwrap("some"), true));
    });
}, {   platformFns: TestImpl,});
