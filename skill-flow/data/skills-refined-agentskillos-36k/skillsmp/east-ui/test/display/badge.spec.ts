/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Badge, Style } from "../../src/index.js";

describeEast("Badge", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates badge with string value", $ => {
        const badge = $.let(Badge.Root("New"));

        $(Assert.equal(badge.unwrap().unwrap("Badge").value, "New"));
        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.hasTag("none"), true));
        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.hasTag("none"), true));
        $(Assert.equal(badge.unwrap().unwrap("Badge").size.hasTag("none"), true));
    });

    test("creates badge with expression value", $ => {
        const badge = $.let(Badge.Root("Active"));

        $(Assert.equal(badge.unwrap().unwrap("Badge").value, "Active"));
    });

    test("creates badge with number text", $ => {
        const badge = $.let(Badge.Root("42"));

        $(Assert.equal(badge.unwrap().unwrap("Badge").value, "42"));
    });

    // =========================================================================
    // Variants
    // =========================================================================

    test("creates solid variant badge", $ => {
        const badge = $.let(Badge.Root("Sold", {
            variant: "solid",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.hasTag("some"), true));
        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates subtle variant badge", $ => {
        const badge = $.let(Badge.Root("Pending", {
            variant: "subtle",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates outline variant badge", $ => {
        const badge = $.let(Badge.Root("Draft", {
            variant: "outline",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates badge with Style.StyleVariant helper", $ => {
        const badge = $.let(Badge.Root("Featured", {
            variant: Style.StyleVariant("solid"),
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.unwrap("some").hasTag("solid"), true));
    });

    // =========================================================================
    // Color Palettes
    // =========================================================================

    test("creates badge with green color palette", $ => {
        const badge = $.let(Badge.Root("Active", {
            colorPalette: "green",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.hasTag("some"), true));
        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.unwrap("some").hasTag("green"), true));
    });

    test("creates badge with red color palette", $ => {
        const badge = $.let(Badge.Root("Sold", {
            colorPalette: "red",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.unwrap("some").hasTag("red"), true));
    });

    test("creates badge with blue color palette", $ => {
        const badge = $.let(Badge.Root("Featured", {
            colorPalette: "blue",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates badge with Style.ColorScheme helper", $ => {
        const badge = $.let(Badge.Root("Premium", {
            colorPalette: Style.ColorScheme("purple"),
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates extra small badge", $ => {
        const badge = $.let(Badge.Root("XS", {
            size: "xs",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").size.hasTag("some"), true));
        $(Assert.equal(badge.unwrap().unwrap("Badge").size.unwrap("some").hasTag("xs"), true));
    });

    test("creates small badge", $ => {
        const badge = $.let(Badge.Root("SM", {
            size: "sm",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium badge", $ => {
        const badge = $.let(Badge.Root("MD", {
            size: "md",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large badge", $ => {
        const badge = $.let(Badge.Root("LG", {
            size: "lg",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates badge with Style.Size helper", $ => {
        const badge = $.let(Badge.Root("Size", {
            size: Style.Size("md"),
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").size.unwrap("some").hasTag("md"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates badge with all options", $ => {
        const badge = $.let(Badge.Root("Active", {
            variant: "solid",
            colorPalette: "green",
            size: "sm",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").value, "Active"));
        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.unwrap("some").hasTag("green"), true));
        $(Assert.equal(badge.unwrap().unwrap("Badge").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates status badge", $ => {
        const badge = $.let(Badge.Root("Online", {
            colorPalette: "green",
            variant: "solid",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").value, "Online"));
        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.unwrap("some").hasTag("green"), true));
    });

    test("creates notification count badge", $ => {
        const badge = $.let(Badge.Root("99+", {
            colorPalette: "red",
            variant: "solid",
            size: "xs",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").value, "99+"));
        $(Assert.equal(badge.unwrap().unwrap("Badge").colorPalette.unwrap("some").hasTag("red"), true));
    });

    test("creates category tag badge", $ => {
        const badge = $.let(Badge.Root("Technology", {
            colorPalette: "blue",
            variant: "subtle",
            size: "sm",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").value, "Technology"));
        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates premium label badge", $ => {
        const badge = $.let(Badge.Root("PRO", {
            colorPalette: "purple",
            variant: "outline",
        }));

        $(Assert.equal(badge.unwrap().unwrap("Badge").value, "PRO"));
        $(Assert.equal(badge.unwrap().unwrap("Badge").variant.unwrap("some").hasTag("outline"), true));
    });
}, {   platformFns: TestImpl,});
