/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Progress, Style } from "../../src/index.js";

describeEast("Progress", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates progress with value only", $ => {
        const progress = $.let(Progress.Root(50.0));

        $(Assert.equal(progress.unwrap().unwrap("Progress").value, 50.0));
        $(Assert.equal(progress.unwrap().unwrap("Progress").min.hasTag("none"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").max.hasTag("none"), true));
    });

    test("creates progress with different value", $ => {
        const progress = $.let(Progress.Root(75.0));

        $(Assert.equal(progress.unwrap().unwrap("Progress").value, 75.0));
    });

    test("creates progress at zero", $ => {
        const progress = $.let(Progress.Root(0.0));

        $(Assert.equal(progress.unwrap().unwrap("Progress").value, 0.0));
    });

    test("creates progress at full", $ => {
        const progress = $.let(Progress.Root(100.0));

        $(Assert.equal(progress.unwrap().unwrap("Progress").value, 100.0));
    });

    // =========================================================================
    // Min/Max Range
    // =========================================================================

    test("creates progress with min", $ => {
        const progress = $.let(Progress.Root(50.0, {
            min: 0,
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").min.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").min.unwrap("some"), 0.0));
    });

    test("creates progress with max", $ => {
        const progress = $.let(Progress.Root(50.0, {
            max: 100,
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").max.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").max.unwrap("some"), 100.0));
    });

    test("creates progress with min and max", $ => {
        const progress = $.let(Progress.Root(50.0, {
            min: 0,
            max: 100,
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").min.unwrap("some"), 0.0));
        $(Assert.equal(progress.unwrap().unwrap("Progress").max.unwrap("some"), 100.0));
    });

    // =========================================================================
    // Color Palettes
    // =========================================================================

    test("creates progress with blue color palette", $ => {
        const progress = $.let(Progress.Root(50.0, {
            colorPalette: "blue",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").colorPalette.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates progress with green color palette", $ => {
        const progress = $.let(Progress.Root(50.0, {
            colorPalette: "green",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").colorPalette.unwrap("some").hasTag("green"), true));
    });

    test("creates progress with Style.ColorScheme helper", $ => {
        const progress = $.let(Progress.Root(50.0, {
            colorPalette: Style.ColorScheme("purple"),
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates small progress", $ => {
        const progress = $.let(Progress.Root(50.0, {
            size: "sm",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").size.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium progress", $ => {
        const progress = $.let(Progress.Root(50.0, {
            size: "md",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large progress", $ => {
        const progress = $.let(Progress.Root(50.0, {
            size: "lg",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates progress with Style.Size helper", $ => {
        const progress = $.let(Progress.Root(50.0, {
            size: Style.Size("md"),
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").size.unwrap("some").hasTag("md"), true));
    });

    // =========================================================================
    // Variant
    // =========================================================================

    test("creates outline variant progress", $ => {
        const progress = $.let(Progress.Root(50.0, {
            variant: "outline",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").variant.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates subtle variant progress", $ => {
        const progress = $.let(Progress.Root(50.0, {
            variant: "subtle",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates progress with ProgressVariant helper", $ => {
        const progress = $.let(Progress.Root(50.0, {
            variant: "subtle",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").variant.unwrap("some").hasTag("subtle"), true));
    });

    // =========================================================================
    // Striped and Animated
    // =========================================================================

    test("creates striped progress", $ => {
        const progress = $.let(Progress.Root(50.0, {
            striped: true,
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").striped.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").striped.unwrap("some"), true));
    });

    test("creates non-striped progress explicitly", $ => {
        const progress = $.let(Progress.Root(50.0, {
            striped: false,
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").striped.unwrap("some"), false));
    });

    test("creates animated progress", $ => {
        const progress = $.let(Progress.Root(50.0, {
            animated: true,
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").animated.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").animated.unwrap("some"), true));
    });

    test("creates striped and animated progress", $ => {
        const progress = $.let(Progress.Root(50.0, {
            striped: true,
            animated: true,
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").striped.unwrap("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").animated.unwrap("some"), true));
    });

    // =========================================================================
    // Label and ValueText
    // =========================================================================

    test("creates progress with label", $ => {
        const progress = $.let(Progress.Root(50.0, {
            label: "Upload Progress",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").label.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").label.unwrap("some"), "Upload Progress"));
    });

    test("creates progress with valueText", $ => {
        const progress = $.let(Progress.Root(75.0, {
            valueText: "75%",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").valueText.hasTag("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").valueText.unwrap("some"), "75%"));
    });

    test("creates progress with label and valueText", $ => {
        const progress = $.let(Progress.Root(60.0, {
            label: "Download",
            valueText: "60 MB / 100 MB",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").label.unwrap("some"), "Download"));
        $(Assert.equal(progress.unwrap().unwrap("Progress").valueText.unwrap("some"), "60 MB / 100 MB"));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates progress with all options", $ => {
        const progress = $.let(Progress.Root(75.0, {
            min: 0,
            max: 100,
            colorPalette: "blue",
            size: "md",
            variant: "subtle",
            striped: true,
            animated: true,
            label: "Progress",
            valueText: "75%",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").value, 75.0));
        $(Assert.equal(progress.unwrap().unwrap("Progress").min.unwrap("some"), 0.0));
        $(Assert.equal(progress.unwrap().unwrap("Progress").max.unwrap("some"), 100.0));
        $(Assert.equal(progress.unwrap().unwrap("Progress").colorPalette.unwrap("some").hasTag("blue"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").variant.unwrap("some").hasTag("subtle"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").striped.unwrap("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").animated.unwrap("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").label.unwrap("some"), "Progress"));
        $(Assert.equal(progress.unwrap().unwrap("Progress").valueText.unwrap("some"), "75%"));
    });

    test("creates upload progress bar", $ => {
        const progress = $.let(Progress.Root(45.0, {
            colorPalette: "blue",
            label: "Uploading...",
            valueText: "45%",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").value, 45.0));
        $(Assert.equal(progress.unwrap().unwrap("Progress").label.unwrap("some"), "Uploading..."));
    });

    test("creates loading indicator", $ => {
        const progress = $.let(Progress.Root(30.0, {
            striped: true,
            animated: true,
            colorPalette: "green",
            size: "sm",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").striped.unwrap("some"), true));
        $(Assert.equal(progress.unwrap().unwrap("Progress").animated.unwrap("some"), true));
    });

    test("creates completion progress", $ => {
        const progress = $.let(Progress.Root(100.0, {
            colorPalette: "green",
            label: "Complete!",
            valueText: "100%",
        }));

        $(Assert.equal(progress.unwrap().unwrap("Progress").value, 100.0));
        $(Assert.equal(progress.unwrap().unwrap("Progress").colorPalette.unwrap("some").hasTag("green"), true));
    });
}, {   platformFns: TestImpl,});
