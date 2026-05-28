/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Switch, Style } from "../../src/index.js";

describeEast("Switch", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates switch with checked true", $ => {
        const sw = $.let(Switch.Root(true));

        $(Assert.equal(sw.unwrap().unwrap("Switch").checked, true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").label.hasTag("none"), true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").disabled.hasTag("none"), true));
    });

    test("creates switch with checked false", $ => {
        const sw = $.let(Switch.Root(false));

        $(Assert.equal(sw.unwrap().unwrap("Switch").checked, false));
    });

    // =========================================================================
    // Label
    // =========================================================================

    test("creates switch with label", $ => {
        const sw = $.let(Switch.Root(false, {
            label: "Enable notifications",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").label.hasTag("some"), true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").label.unwrap("some"), "Enable notifications"));
    });

    test("creates switch with long label", $ => {
        const sw = $.let(Switch.Root(false, {
            label: "Enable all email notifications for this account",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").label.unwrap("some"), "Enable all email notifications for this account"));
    });

    // =========================================================================
    // Disabled State
    // =========================================================================

    test("creates disabled switch", $ => {
        const sw = $.let(Switch.Root(false, {
            disabled: true,
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").disabled.hasTag("some"), true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").disabled.unwrap("some"), true));
    });

    test("creates enabled switch explicitly", $ => {
        const sw = $.let(Switch.Root(true, {
            disabled: false,
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").disabled.unwrap("some"), false));
    });

    // =========================================================================
    // Color Palettes
    // =========================================================================

    test("creates switch with blue color palette", $ => {
        const sw = $.let(Switch.Root(true, {
            colorPalette: "blue",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.hasTag("some"), true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates switch with green color palette", $ => {
        const sw = $.let(Switch.Root(true, {
            colorPalette: "green",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.unwrap("some").hasTag("green"), true));
    });

    test("creates switch with teal color palette", $ => {
        const sw = $.let(Switch.Root(true, {
            colorPalette: "teal",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.unwrap("some").hasTag("teal"), true));
    });

    test("creates switch with Style.ColorScheme helper", $ => {
        const sw = $.let(Switch.Root(true, {
            colorPalette: Style.ColorScheme("purple"),
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    // =========================================================================
    // Sizes
    // =========================================================================

    test("creates small switch", $ => {
        const sw = $.let(Switch.Root(true, {
            size: "sm",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").size.hasTag("some"), true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium switch", $ => {
        const sw = $.let(Switch.Root(true, {
            size: "md",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large switch", $ => {
        const sw = $.let(Switch.Root(true, {
            size: "lg",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates switch with Style.Size helper", $ => {
        const sw = $.let(Switch.Root(true, {
            size: Style.Size("md"),
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").size.unwrap("some").hasTag("md"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates switch with all options", $ => {
        const sw = $.let(Switch.Root(true, {
            label: "Dark mode",
            disabled: false,
            colorPalette: "blue",
            size: "md",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").checked, true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").label.unwrap("some"), "Dark mode"));
        $(Assert.equal(sw.unwrap().unwrap("Switch").disabled.unwrap("some"), false));
        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.unwrap("some").hasTag("blue"), true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").size.unwrap("some").hasTag("md"), true));
    });

    test("creates dark mode toggle switch", $ => {
        const sw = $.let(Switch.Root(false, {
            label: "Dark mode",
            colorPalette: "gray",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").checked, false));
        $(Assert.equal(sw.unwrap().unwrap("Switch").label.unwrap("some"), "Dark mode"));
        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.unwrap("some").hasTag("gray"), true));
    });

    test("creates notification settings switch", $ => {
        const sw = $.let(Switch.Root(true, {
            label: "Push notifications",
            colorPalette: "green",
            size: "sm",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").checked, true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").label.unwrap("some"), "Push notifications"));
        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.unwrap("some").hasTag("green"), true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates disabled premium feature switch", $ => {
        const sw = $.let(Switch.Root(false, {
            label: "Premium feature (upgrade required)",
            disabled: true,
            colorPalette: "gray",
        }));

        $(Assert.equal(sw.unwrap().unwrap("Switch").checked, false));
        $(Assert.equal(sw.unwrap().unwrap("Switch").disabled.unwrap("some"), true));
        $(Assert.equal(sw.unwrap().unwrap("Switch").colorPalette.unwrap("some").hasTag("gray"), true));
    });
}, {   platformFns: TestImpl,});
