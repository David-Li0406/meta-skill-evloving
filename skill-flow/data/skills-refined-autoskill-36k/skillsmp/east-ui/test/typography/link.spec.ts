/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Link } from "../../src/index.js";

describeEast("Link", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates link with value and href", $ => {
        const link = $.let(Link.Root("Click here", "https://example.com"));

        $(Assert.equal(link.unwrap().unwrap("Link").value, "Click here"));
        $(Assert.equal(link.unwrap().unwrap("Link").href, "https://example.com"));
    });

    test("creates link with no style - all options are none", $ => {
        const link = $.let(Link.Root("Link", "/about"));

        $(Assert.equal(link.unwrap().unwrap("Link").value, "Link"));
        $(Assert.equal(link.unwrap().unwrap("Link").href, "/about"));
        $(Assert.equal(link.unwrap().unwrap("Link").external.hasTag("none"), true));
        $(Assert.equal(link.unwrap().unwrap("Link").variant.hasTag("none"), true));
        $(Assert.equal(link.unwrap().unwrap("Link").colorPalette.hasTag("none"), true));
    });

    // =========================================================================
    // External
    // =========================================================================

    test("creates external link", $ => {
        const link = $.let(Link.Root("External", "https://google.com", {
            external: true,
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").external.hasTag("some"), true));
        $(Assert.equal(link.unwrap().unwrap("Link").external.unwrap("some"), true));
    });

    test("creates non-external link", $ => {
        const link = $.let(Link.Root("Internal", "/home", {
            external: false,
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").external.unwrap("some"), false));
    });

    // =========================================================================
    // Variants
    // =========================================================================

    test("creates underline variant link", $ => {
        const link = $.let(Link.Root("Underlined", "/page", {
            variant: "underline",
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").variant.hasTag("some"), true));
        $(Assert.equal(link.unwrap().unwrap("Link").variant.unwrap("some").hasTag("underline"), true));
    });

    test("creates plain variant link", $ => {
        const link = $.let(Link.Root("Plain", "/page", {
            variant: "plain",
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").variant.unwrap("some").hasTag("plain"), true));
    });

    // =========================================================================
    // Color Palette
    // =========================================================================

    test("creates link with colorPalette", $ => {
        const link = $.let(Link.Root("Colored", "/page", {
            colorPalette: "blue",
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").colorPalette.hasTag("some"), true));
        $(Assert.equal(link.unwrap().unwrap("Link").colorPalette.unwrap("some"), "blue"));
    });

    test("creates link with teal colorPalette", $ => {
        const link = $.let(Link.Root("Teal", "/page", {
            colorPalette: "teal",
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").colorPalette.unwrap("some"), "teal"));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates link with all options", $ => {
        const link = $.let(Link.Root("Documentation", "https://docs.example.com", {
            external: true,
            variant: "underline",
            colorPalette: "blue",
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").value, "Documentation"));
        $(Assert.equal(link.unwrap().unwrap("Link").href, "https://docs.example.com"));
        $(Assert.equal(link.unwrap().unwrap("Link").external.unwrap("some"), true));
        $(Assert.equal(link.unwrap().unwrap("Link").variant.unwrap("some").hasTag("underline"), true));
        $(Assert.equal(link.unwrap().unwrap("Link").colorPalette.unwrap("some"), "blue"));
    });

    test("creates navigation link", $ => {
        const link = $.let(Link.Root("Home", "/", {
            variant: "plain",
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").value, "Home"));
        $(Assert.equal(link.unwrap().unwrap("Link").href, "/"));
        $(Assert.equal(link.unwrap().unwrap("Link").variant.unwrap("some").hasTag("plain"), true));
    });

    test("creates social link", $ => {
        const link = $.let(Link.Root("GitHub", "https://github.com", {
            external: true,
            colorPalette: "gray",
        }));

        $(Assert.equal(link.unwrap().unwrap("Link").value, "GitHub"));
        $(Assert.equal(link.unwrap().unwrap("Link").external.unwrap("some"), true));
    });
}, {   platformFns: TestImpl,});
