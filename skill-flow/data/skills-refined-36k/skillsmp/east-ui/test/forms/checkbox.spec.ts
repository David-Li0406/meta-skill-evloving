/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Checkbox, Style } from "../../src/index.js";

describeEast("Checkbox", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates checkbox with checked true", $ => {
        const checkbox = $.let(Checkbox.Root(true));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").checked, true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").label.hasTag("none"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").indeterminate.hasTag("none"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").disabled.hasTag("none"), true));
    });

    test("creates checkbox with checked false", $ => {
        const checkbox = $.let(Checkbox.Root(false));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").checked, false));
    });

    // =========================================================================
    // Label
    // =========================================================================

    test("creates checkbox with label", $ => {
        const checkbox = $.let(Checkbox.Root(false, {
            label: "Accept terms",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").label.hasTag("some"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").label.unwrap("some"), "Accept terms"));
    });

    test("creates checkbox with long label", $ => {
        const checkbox = $.let(Checkbox.Root(false, {
            label: "I agree to the terms and conditions and privacy policy",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").label.unwrap("some"), "I agree to the terms and conditions and privacy policy"));
    });

    // =========================================================================
    // Indeterminate State
    // =========================================================================

    test("creates indeterminate checkbox", $ => {
        const checkbox = $.let(Checkbox.Root(false, {
            indeterminate: true,
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").indeterminate.hasTag("some"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").indeterminate.unwrap("some"), true));
    });

    test("creates non-indeterminate checkbox explicitly", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            indeterminate: false,
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").indeterminate.unwrap("some"), false));
    });

    // =========================================================================
    // Disabled State
    // =========================================================================

    test("creates disabled checkbox", $ => {
        const checkbox = $.let(Checkbox.Root(false, {
            disabled: true,
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").disabled.hasTag("some"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").disabled.unwrap("some"), true));
    });

    test("creates enabled checkbox explicitly", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            disabled: false,
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").disabled.unwrap("some"), false));
    });

    // =========================================================================
    // Color Palettes
    // =========================================================================

    test("creates checkbox with blue color palette", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            colorPalette: "blue",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").colorPalette.hasTag("some"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates checkbox with green color palette", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            colorPalette: "green",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").colorPalette.unwrap("some").hasTag("green"), true));
    });

    test("creates checkbox with Style.ColorScheme helper", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            colorPalette: Style.ColorScheme("purple"),
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    // =========================================================================
    // Sizes
    // =========================================================================

    test("creates small checkbox", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            size: "sm",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").size.hasTag("some"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium checkbox", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            size: "md",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large checkbox", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            size: "lg",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates checkbox with Style.Size helper", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            size: Style.Size("md"),
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").size.unwrap("some").hasTag("md"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates checkbox with all options", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            label: "Enable feature",
            indeterminate: false,
            disabled: false,
            colorPalette: "blue",
            size: "md",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").checked, true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").label.unwrap("some"), "Enable feature"));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").indeterminate.unwrap("some"), false));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").disabled.unwrap("some"), false));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").colorPalette.unwrap("some").hasTag("blue"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").size.unwrap("some").hasTag("md"), true));
    });

    test("creates terms acceptance checkbox", $ => {
        const checkbox = $.let(Checkbox.Root(false, {
            label: "I accept the terms and conditions",
            colorPalette: "blue",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").checked, false));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").label.unwrap("some"), "I accept the terms and conditions"));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates select all checkbox with indeterminate", $ => {
        const checkbox = $.let(Checkbox.Root(false, {
            label: "Select all",
            indeterminate: true,
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").label.unwrap("some"), "Select all"));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").indeterminate.unwrap("some"), true));
    });

    test("creates disabled readonly checkbox", $ => {
        const checkbox = $.let(Checkbox.Root(true, {
            label: "Premium feature (upgrade required)",
            disabled: true,
            colorPalette: "gray",
        }));

        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").checked, true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").disabled.unwrap("some"), true));
        $(Assert.equal(checkbox.unwrap().unwrap("Checkbox").colorPalette.unwrap("some").hasTag("gray"), true));
    });
}, {   platformFns: TestImpl,});
