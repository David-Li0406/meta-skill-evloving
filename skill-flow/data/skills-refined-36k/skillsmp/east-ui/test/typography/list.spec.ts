/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { List } from "../../src/index.js";

describeEast("List", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates list with string items", $ => {
        const list = $.let(List.Root(["Item 1", "Item 2", "Item 3"]));

        $(Assert.equal(list.unwrap().unwrap("List").variant.hasTag("none"), true));
    });

    test("creates list with no style - all options are none", $ => {
        const list = $.let(List.Root(["Item"]));

        $(Assert.equal(list.unwrap().unwrap("List").variant.hasTag("none"), true));
        $(Assert.equal(list.unwrap().unwrap("List").gap.hasTag("none"), true));
        $(Assert.equal(list.unwrap().unwrap("List").colorPalette.hasTag("none"), true));
    });

    test("creates list with single item", $ => {
        const list = $.let(List.Root(["Single"]));

        $(Assert.equal(list.unwrap().unwrap("List").variant.hasTag("none"), true));
    });

    // =========================================================================
    // Variants
    // =========================================================================

    test("creates unordered list", $ => {
        const list = $.let(List.Root(["A", "B"], {
            variant: "unordered",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").variant.hasTag("some"), true));
        $(Assert.equal(list.unwrap().unwrap("List").variant.unwrap("some").hasTag("unordered"), true));
    });

    test("creates ordered list", $ => {
        const list = $.let(List.Root(["First", "Second"], {
            variant: "ordered",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").variant.unwrap("some").hasTag("ordered"), true));
    });

    // =========================================================================
    // Gap
    // =========================================================================

    test("creates list with gap", $ => {
        const list = $.let(List.Root(["A", "B"], {
            gap: "4",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").gap.hasTag("some"), true));
        $(Assert.equal(list.unwrap().unwrap("List").gap.unwrap("some"), "4"));
    });

    test("creates list with large gap", $ => {
        const list = $.let(List.Root(["A", "B"], {
            gap: "8",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").gap.unwrap("some"), "8"));
    });

    // =========================================================================
    // Color Palette
    // =========================================================================

    test("creates list with colorPalette", $ => {
        const list = $.let(List.Root(["A", "B"], {
            colorPalette: "blue",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").colorPalette.hasTag("some"), true));
        $(Assert.equal(list.unwrap().unwrap("List").colorPalette.unwrap("some"), "blue"));
    });

    test("creates list with green colorPalette", $ => {
        const list = $.let(List.Root(["A", "B"], {
            colorPalette: "green",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").colorPalette.unwrap("some"), "green"));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates list with all options", $ => {
        const list = $.let(List.Root(
            ["Step 1", "Step 2", "Step 3"],
            {
                variant: "ordered",
                gap: "2",
                colorPalette: "gray",
            }
        ));

        $(Assert.equal(list.unwrap().unwrap("List").variant.unwrap("some").hasTag("ordered"), true));
        $(Assert.equal(list.unwrap().unwrap("List").gap.unwrap("some"), "2"));
        $(Assert.equal(list.unwrap().unwrap("List").colorPalette.unwrap("some"), "gray"));
    });

    test("creates feature list", $ => {
        const list = $.let(List.Root([
            "Fast performance",
            "Type safe",
            "Easy to use",
        ], {
            variant: "unordered",
            gap: "3",
            colorPalette: "green",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").variant.unwrap("some").hasTag("unordered"), true));
        $(Assert.equal(list.unwrap().unwrap("List").gap.unwrap("some"), "3"));
        $(Assert.equal(list.unwrap().unwrap("List").colorPalette.unwrap("some"), "green"));
    });

    test("creates empty list", $ => {
        const list = $.let(List.Root([]));

        $(Assert.equal(list.unwrap().unwrap("List").variant.hasTag("none"), true));
    });

    test("creates numbered steps list", $ => {
        const list = $.let(List.Root([
            "Install dependencies",
            "Configure settings",
            "Run the application",
        ], {
            variant: "ordered",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").variant.unwrap("some").hasTag("ordered"), true));
    });

    test("creates bullet point list", $ => {
        const list = $.let(List.Root([
            "Point one",
            "Point two",
            "Point three",
        ], {
            variant: "unordered",
            colorPalette: "gray",
        }));

        $(Assert.equal(list.unwrap().unwrap("List").variant.unwrap("some").hasTag("unordered"), true));
        $(Assert.equal(list.unwrap().unwrap("List").colorPalette.unwrap("some"), "gray"));
    });
}, {   platformFns: TestImpl,});
