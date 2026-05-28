/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Button, Style } from "../../src/index.js";

describeEast("Button", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates button with label only", $ => {
        const button = $.let(Button.Root("Click me"));

        $(Assert.equal(button.unwrap().unwrap("Button").label, "Click me"));
        $(Assert.equal(button.unwrap().unwrap("Button").style.hasTag("none"), true));
    });

    test("creates button with different label", $ => {
        const button = $.let(Button.Root("Submit"));

        $(Assert.equal(button.unwrap().unwrap("Button").label, "Submit"));
    });

    // =========================================================================
    // Button Variants
    // =========================================================================

    test("creates solid button", $ => {
        const button = $.let(Button.Root("Solid", {
            variant: "solid",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates subtle button", $ => {
        const button = $.let(Button.Root("Subtle", {
            variant: "subtle",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates outline button", $ => {
        const button = $.let(Button.Root("Outline", {
            variant: "outline",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates ghost button", $ => {
        const button = $.let(Button.Root("Ghost", {
            variant: "ghost",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("ghost"), true));
    });

    test("creates button with string literal variant", $ => {
        const button = $.let(Button.Root("Helper", {
            variant: "outline",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
    });

    // =========================================================================
    // Color Palettes
    // =========================================================================

    test("creates button with blue color palette", $ => {
        const button = $.let(Button.Root("Blue", {
            colorPalette: "blue",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates button with red color palette", $ => {
        const button = $.let(Button.Root("Red", {
            colorPalette: "red",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.unwrap("some").hasTag("red"), true));
    });

    test("creates button with green color palette", $ => {
        const button = $.let(Button.Root("Green", {
            colorPalette: "green",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.unwrap("some").hasTag("green"), true));
    });

    test("creates button with Style.ColorScheme helper", $ => {
        const button = $.let(Button.Root("Teal", {
            colorPalette: Style.ColorScheme("teal"),
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.unwrap("some").hasTag("teal"), true));
    });

    // =========================================================================
    // Sizes
    // =========================================================================

    test("creates extra small button", $ => {
        const button = $.let(Button.Root("XS", {
            size: "xs",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").size.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").size.unwrap("some").hasTag("xs"), true));
    });

    test("creates small button", $ => {
        const button = $.let(Button.Root("Small", {
            size: "sm",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium button", $ => {
        const button = $.let(Button.Root("Medium", {
            size: "md",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large button", $ => {
        const button = $.let(Button.Root("Large", {
            size: "lg",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates button with Style.Size helper", $ => {
        const button = $.let(Button.Root("Sized", {
            size: Style.Size("md"),
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").size.unwrap("some").hasTag("md"), true));
    });

    // =========================================================================
    // Loading State
    // =========================================================================

    test("creates loading button", $ => {
        const button = $.let(Button.Root("Loading...", {
            loading: true,
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").loading.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").loading.unwrap("some"), true));
    });

    test("creates non-loading button explicitly", $ => {
        const button = $.let(Button.Root("Ready", {
            loading: false,
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").loading.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").loading.unwrap("some"), false));
    });

    // =========================================================================
    // Disabled State
    // =========================================================================

    test("creates disabled button", $ => {
        const button = $.let(Button.Root("Disabled", {
            disabled: true,
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").disabled.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").disabled.unwrap("some"), true));
    });

    test("creates enabled button explicitly", $ => {
        const button = $.let(Button.Root("Enabled", {
            disabled: false,
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").disabled.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").disabled.unwrap("some"), false));
    });

    // =========================================================================
    // Combined Styles
    // =========================================================================

    test("creates button with all style properties", $ => {
        const button = $.let(Button.Root("Full Style", {
            variant: "solid",
            colorPalette: "blue",
            size: "md",
            loading: false,
            disabled: false,
        }));

        const style = button.unwrap().unwrap("Button").style.unwrap("some");
        $(Assert.equal(style.variant.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(style.colorPalette.unwrap("some").hasTag("blue"), true));
        $(Assert.equal(style.size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(style.loading.unwrap("some"), false));
        $(Assert.equal(style.disabled.unwrap("some"), false));
    });

    test("creates primary action button", $ => {
        const button = $.let(Button.Root("Save Changes", {
            variant: "solid",
            colorPalette: "blue",
            size: "md",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").label, "Save Changes"));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates danger button", $ => {
        const button = $.let(Button.Root("Delete", {
            variant: "solid",
            colorPalette: "red",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.unwrap("some").hasTag("red"), true));
    });

    test("creates secondary action button", $ => {
        const button = $.let(Button.Root("Cancel", {
            variant: "outline",
            colorPalette: "gray",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.unwrap("some").hasTag("gray"), true));
    });

    test("creates icon-style ghost button", $ => {
        const button = $.let(Button.Root("...", {
            variant: "ghost",
            size: "sm",
        }));

        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.unwrap("some").hasTag("ghost"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });

    // =========================================================================
    // No Style Properties Set
    // =========================================================================

    test("button without style has none for all properties", $ => {
        const button = $.let(Button.Root("Plain"));

        $(Assert.equal(button.unwrap().unwrap("Button").style.hasTag("none"), true));
    });

    test("button with empty style object still has options", $ => {
        const button = $.let(Button.Root("Empty Style", {}));

        $(Assert.equal(button.unwrap().unwrap("Button").style.hasTag("some"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").variant.hasTag("none"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").colorPalette.hasTag("none"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").size.hasTag("none"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").loading.hasTag("none"), true));
        $(Assert.equal(button.unwrap().unwrap("Button").style.unwrap("some").disabled.hasTag("none"), true));
    });
}, {   platformFns: TestImpl,});
