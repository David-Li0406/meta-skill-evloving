/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Highlight } from "../../src/index.js";

describeEast("Highlight", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates highlight with value and single query", $ => {
        const highlight = $.let(Highlight.Root("Hello World", ["World"]));

        $(Assert.equal(highlight.unwrap().unwrap("Highlight").value, "Hello World"));
    });

    test("creates highlight with multiple queries", $ => {
        const highlight = $.let(Highlight.Root("The quick brown fox", ["quick", "fox"]));

        $(Assert.equal(highlight.unwrap().unwrap("Highlight").value, "The quick brown fox"));
    });

    test("creates highlight with no style - color is none", $ => {
        const highlight = $.let(Highlight.Root("Search results", ["results"]));

        $(Assert.equal(highlight.unwrap().unwrap("Highlight").value, "Search results"));
        $(Assert.equal(highlight.unwrap().unwrap("Highlight").color.hasTag("none"), true));
    });

    // =========================================================================
    // Color
    // =========================================================================

    test("creates highlight with color", $ => {
        const highlight = $.let(Highlight.Root("Important text", ["Important"], {
            color: "yellow.200",
        }));

        $(Assert.equal(highlight.unwrap().unwrap("Highlight").color.hasTag("some"), true));
        $(Assert.equal(highlight.unwrap().unwrap("Highlight").color.unwrap("some"), "yellow.200"));
    });

    test("creates highlight with green color", $ => {
        const highlight = $.let(Highlight.Root("Success message", ["Success"], {
            color: "green.100",
        }));

        $(Assert.equal(highlight.unwrap().unwrap("Highlight").color.unwrap("some"), "green.100"));
    });

    // =========================================================================
    // Use Cases
    // =========================================================================

    test("creates search result highlight", $ => {
        const highlight = $.let(Highlight.Root(
            "React is a JavaScript library for building user interfaces",
            ["React", "JavaScript"],
            { color: "blue.100" }
        ));

        $(Assert.equal(highlight.unwrap().unwrap("Highlight").value, "React is a JavaScript library for building user interfaces"));
        $(Assert.equal(highlight.unwrap().unwrap("Highlight").color.unwrap("some"), "blue.100"));
    });

    test("creates keyword highlight", $ => {
        const highlight = $.let(Highlight.Root(
            "The error occurred at line 42",
            ["error"],
            { color: "red.100" }
        ));

        $(Assert.equal(highlight.unwrap().unwrap("Highlight").value, "The error occurred at line 42"));
        $(Assert.equal(highlight.unwrap().unwrap("Highlight").color.unwrap("some"), "red.100"));
    });

    test("creates empty query array", $ => {
        const highlight = $.let(Highlight.Root("No highlights", []));

        $(Assert.equal(highlight.unwrap().unwrap("Highlight").value, "No highlights"));
        $(Assert.equal(highlight.unwrap().unwrap("Highlight").color.hasTag("none"), true));
    });
}, {   platformFns: TestImpl,});
