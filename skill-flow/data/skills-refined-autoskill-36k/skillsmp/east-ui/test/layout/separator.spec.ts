/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Separator } from "../../src/index.js";

describeEast("Separator", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates separator with no options", $ => {
        const separator = $.let(Separator.Root());

        $(Assert.equal(separator.unwrap().unwrap("Separator").orientation.hasTag("none"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").variant.hasTag("none"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").size.hasTag("none"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").color.hasTag("none"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").label.hasTag("none"), true));
    });

    // =========================================================================
    // Orientation
    // =========================================================================

    test("creates horizontal separator", $ => {
        const separator = $.let(Separator.Root({
            orientation: "horizontal",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").orientation.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").orientation.unwrap("some").hasTag("horizontal"), true));
    });

    test("creates vertical separator", $ => {
        const separator = $.let(Separator.Root({
            orientation: "vertical",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").orientation.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").orientation.unwrap("some").hasTag("vertical"), true));
    });

    // =========================================================================
    // Variant (Line Style)
    // =========================================================================

    test("creates separator with solid variant", $ => {
        const separator = $.let(Separator.Root({
            variant: "solid",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").variant.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates separator with dashed variant", $ => {
        const separator = $.let(Separator.Root({
            variant: "dashed",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").variant.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").variant.unwrap("some").hasTag("dashed"), true));
    });

    test("creates separator with dotted variant", $ => {
        const separator = $.let(Separator.Root({
            variant: "dotted",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").variant.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").variant.unwrap("some").hasTag("dotted"), true));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates separator with small size", $ => {
        const separator = $.let(Separator.Root({
            size: "sm",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").size.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates separator with medium size", $ => {
        const separator = $.let(Separator.Root({
            size: "md",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").size.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").size.unwrap("some").hasTag("md"), true));
    });

    test("creates separator with large size", $ => {
        const separator = $.let(Separator.Root({
            size: "lg",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").size.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").size.unwrap("some").hasTag("lg"), true));
    });

    // =========================================================================
    // Color
    // =========================================================================

    test("creates separator with color", $ => {
        const separator = $.let(Separator.Root({
            color: "gray.300",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").color.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").color.unwrap("some"), "gray.300"));
    });

    test("creates separator with custom color", $ => {
        const separator = $.let(Separator.Root({
            color: "#e2e8f0",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").color.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").color.unwrap("some"), "#e2e8f0"));
    });

    // =========================================================================
    // Label
    // =========================================================================

    test("creates separator with label", $ => {
        const separator = $.let(Separator.Root({
            label: "OR",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").label.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").label.unwrap("some"), "OR"));
    });

    test("creates separator with long label", $ => {
        const separator = $.let(Separator.Root({
            label: "Continue with",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").label.hasTag("some"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").label.unwrap("some"), "Continue with"));
    });

    // =========================================================================
    // Multiple Properties
    // =========================================================================

    test("creates separator with multiple properties", $ => {
        const separator = $.let(Separator.Root({
            orientation: "horizontal",
            variant: "dashed",
            size: "md",
            color: "gray.400",
            label: "Section Break",
        }));

        $(Assert.equal(separator.unwrap().unwrap("Separator").orientation.unwrap("some").hasTag("horizontal"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").variant.unwrap("some").hasTag("dashed"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(separator.unwrap().unwrap("Separator").color.unwrap("some"), "gray.400"));
        $(Assert.equal(separator.unwrap().unwrap("Separator").label.unwrap("some"), "Section Break"));
    });

    // =========================================================================
    // Typical Use Cases
    // =========================================================================

    test("creates simple horizontal divider", $ => {
        const divider = $.let(Separator.Root({
            orientation: "horizontal",
        }));

        $(Assert.equal(divider.unwrap().unwrap("Separator").orientation.unwrap("some").hasTag("horizontal"), true));
    });

    test("creates labeled OR separator for forms", $ => {
        const orSeparator = $.let(Separator.Root({
            label: "OR",
            color: "gray.400",
        }));

        $(Assert.equal(orSeparator.unwrap().unwrap("Separator").label.unwrap("some"), "OR"));
        $(Assert.equal(orSeparator.unwrap().unwrap("Separator").color.unwrap("some"), "gray.400"));
    });

    test("creates vertical separator for side-by-side content", $ => {
        const verticalDivider = $.let(Separator.Root({
            orientation: "vertical",
            color: "gray.200",
        }));

        $(Assert.equal(verticalDivider.unwrap().unwrap("Separator").orientation.unwrap("some").hasTag("vertical"), true));
        $(Assert.equal(verticalDivider.unwrap().unwrap("Separator").color.unwrap("some"), "gray.200"));
    });

    test("creates styled section divider", $ => {
        const sectionDivider = $.let(Separator.Root({
            variant: "dotted",
            color: "blue.300",
            size: "sm",
        }));

        $(Assert.equal(sectionDivider.unwrap().unwrap("Separator").variant.unwrap("some").hasTag("dotted"), true));
        $(Assert.equal(sectionDivider.unwrap().unwrap("Separator").color.unwrap("some"), "blue.300"));
        $(Assert.equal(sectionDivider.unwrap().unwrap("Separator").size.unwrap("some").hasTag("sm"), true));
    });
}, {   platformFns: TestImpl,});
