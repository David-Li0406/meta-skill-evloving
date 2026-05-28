/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Code, Style } from "../../src/index.js";

describeEast("Code", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates code with string value", $ => {
        const code = $.let(Code.Root("const x = 1"));

        $(Assert.equal(code.unwrap().unwrap("Code").value, "const x = 1"));
    });

    test("creates code with no style - all options are none", $ => {
        const code = $.let(Code.Root("hello"));

        $(Assert.equal(code.unwrap().unwrap("Code").value, "hello"));
        $(Assert.equal(code.unwrap().unwrap("Code").variant.hasTag("none"), true));
        $(Assert.equal(code.unwrap().unwrap("Code").colorPalette.hasTag("none"), true));
        $(Assert.equal(code.unwrap().unwrap("Code").size.hasTag("none"), true));
    });

    // =========================================================================
    // Variants
    // =========================================================================

    test("creates subtle variant code", $ => {
        const code = $.let(Code.Root("npm install", {
            variant: "subtle",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").variant.hasTag("some"), true));
        $(Assert.equal(code.unwrap().unwrap("Code").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates surface variant code", $ => {
        const code = $.let(Code.Root("npm install", {
            variant: "surface",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").variant.unwrap("some").hasTag("surface"), true));
    });

    test("creates outline variant code", $ => {
        const code = $.let(Code.Root("npm install", {
            variant: "outline",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").variant.unwrap("some").hasTag("outline"), true));
    });

    // =========================================================================
    // Color Palette
    // =========================================================================

    test("creates code with colorPalette", $ => {
        const code = $.let(Code.Root("const x = 1", {
            colorPalette: "blue",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").colorPalette.hasTag("some"), true));
        $(Assert.equal(code.unwrap().unwrap("Code").colorPalette.unwrap("some"), "blue"));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates extra small code", $ => {
        const code = $.let(Code.Root("xs", {
            size: "xs",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").size.hasTag("some"), true));
        $(Assert.equal(code.unwrap().unwrap("Code").size.unwrap("some").hasTag("xs"), true));
    });

    test("creates small code", $ => {
        const code = $.let(Code.Root("sm", {
            size: "sm",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium code", $ => {
        const code = $.let(Code.Root("md", {
            size: "md",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large code", $ => {
        const code = $.let(Code.Root("lg", {
            size: "lg",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates code with Style.Size helper", $ => {
        const code = $.let(Code.Root("size", {
            size: Style.Size("md"),
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").size.unwrap("some").hasTag("md"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates code with all options", $ => {
        const code = $.let(Code.Root("function hello() {}", {
            variant: "subtle",
            colorPalette: "purple",
            size: "sm",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").value, "function hello() {}"));
        $(Assert.equal(code.unwrap().unwrap("Code").variant.unwrap("some").hasTag("subtle"), true));
        $(Assert.equal(code.unwrap().unwrap("Code").colorPalette.unwrap("some"), "purple"));
        $(Assert.equal(code.unwrap().unwrap("Code").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates inline code snippet", $ => {
        const code = $.let(Code.Root("console.log()", {
            variant: "surface",
            colorPalette: "gray",
        }));

        $(Assert.equal(code.unwrap().unwrap("Code").value, "console.log()"));
        $(Assert.equal(code.unwrap().unwrap("Code").variant.unwrap("some").hasTag("surface"), true));
    });
}, {   platformFns: TestImpl,});
