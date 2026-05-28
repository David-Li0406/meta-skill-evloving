/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Textarea, Style } from "../../src/index.js";

describeEast("Textarea", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates textarea with value only", $ => {
        const textarea = $.let(Textarea.Root("Hello"));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").value, "Hello"));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").placeholder.hasTag("none"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").variant.hasTag("none"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").size.hasTag("none"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").resize.hasTag("none"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").rows.hasTag("none"), true));
    });

    test("creates textarea with empty value", $ => {
        const textarea = $.let(Textarea.Root(""));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").value, ""));
    });

    // =========================================================================
    // Placeholder
    // =========================================================================

    test("creates textarea with placeholder", $ => {
        const textarea = $.let(Textarea.Root("", {
            placeholder: "Enter description...",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").placeholder.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").placeholder.unwrap("some"), "Enter description..."));
    });

    // =========================================================================
    // Variant
    // =========================================================================

    test("creates textarea with outline variant", $ => {
        const textarea = $.let(Textarea.Root("", {
            variant: "outline",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").variant.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates textarea with subtle variant", $ => {
        const textarea = $.let(Textarea.Root("", {
            variant: "subtle",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates textarea with flushed variant", $ => {
        const textarea = $.let(Textarea.Root("", {
            variant: "flushed",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").variant.unwrap("some").hasTag("flushed"), true));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates textarea with size", $ => {
        const textarea = $.let(Textarea.Root("", {
            size: "md",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").size.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").size.unwrap("some").hasTag("md"), true));
    });

    test("supports all sizes", $ => {
        const xs = $.let(Textarea.Root("", { size: "xs" }));
        const sm = $.let(Textarea.Root("", { size: "sm" }));
        const md = $.let(Textarea.Root("", { size: "md" }));
        const lg = $.let(Textarea.Root("", { size: "lg" }));

        $(Assert.equal(xs.unwrap().unwrap("Textarea").size.unwrap("some").hasTag("xs"), true));
        $(Assert.equal(sm.unwrap().unwrap("Textarea").size.unwrap("some").hasTag("sm"), true));
        $(Assert.equal(md.unwrap().unwrap("Textarea").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(lg.unwrap().unwrap("Textarea").size.unwrap("some").hasTag("lg"), true));
    });

    test("supports Style.Size helper", $ => {
        const textarea = $.let(Textarea.Root("", {
            size: Style.Size("lg"),
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").size.unwrap("some").hasTag("lg"), true));
    });

    // =========================================================================
    // Resize
    // =========================================================================

    test("creates textarea with resize none", $ => {
        const textarea = $.let(Textarea.Root("", {
            resize: "none",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").resize.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").resize.unwrap("some").hasTag("none"), true));
    });

    test("creates textarea with resize vertical", $ => {
        const textarea = $.let(Textarea.Root("", {
            resize: "vertical",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").resize.unwrap("some").hasTag("vertical"), true));
    });

    test("creates textarea with resize horizontal", $ => {
        const textarea = $.let(Textarea.Root("", {
            resize: "horizontal",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").resize.unwrap("some").hasTag("horizontal"), true));
    });

    test("creates textarea with resize both", $ => {
        const textarea = $.let(Textarea.Root("", {
            resize: "both",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").resize.unwrap("some").hasTag("both"), true));
    });

    // =========================================================================
    // Rows
    // =========================================================================

    test("creates textarea with rows as number", $ => {
        const textarea = $.let(Textarea.Root("", {
            rows: 5,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").rows.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").rows.unwrap("some"), 5n));
    });

    test("creates textarea with rows as bigint", $ => {
        const textarea = $.let(Textarea.Root("", {
            rows: 10n,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").rows.unwrap("some"), 10n));
    });

    // =========================================================================
    // Max Length
    // =========================================================================

    test("creates textarea with maxLength as number", $ => {
        const textarea = $.let(Textarea.Root("", {
            maxLength: 500,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").maxLength.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").maxLength.unwrap("some"), 500n));
    });

    test("creates textarea with maxLength as bigint", $ => {
        const textarea = $.let(Textarea.Root("", {
            maxLength: 1000n,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").maxLength.unwrap("some"), 1000n));
    });

    // =========================================================================
    // Boolean Flags
    // =========================================================================

    test("creates disabled textarea", $ => {
        const textarea = $.let(Textarea.Root("", {
            disabled: true,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").disabled.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").disabled.unwrap("some"), true));
    });

    test("creates read-only textarea", $ => {
        const textarea = $.let(Textarea.Root("Read only content", {
            readOnly: true,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").readOnly.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").readOnly.unwrap("some"), true));
    });

    test("creates required textarea", $ => {
        const textarea = $.let(Textarea.Root("", {
            required: true,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").required.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").required.unwrap("some"), true));
    });

    test("creates auto-resizing textarea", $ => {
        const textarea = $.let(Textarea.Root("", {
            autoresize: true,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").autoresize.hasTag("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").autoresize.unwrap("some"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates textarea with all options", $ => {
        const textarea = $.let(Textarea.Root("Initial content", {
            placeholder: "Enter text...",
            variant: "outline",
            size: "md",
            resize: "vertical",
            rows: 6,
            maxLength: 1000,
            disabled: false,
            readOnly: false,
            required: true,
            autoresize: false,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").value, "Initial content"));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").placeholder.unwrap("some"), "Enter text..."));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").variant.unwrap("some").hasTag("outline"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").resize.unwrap("some").hasTag("vertical"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").rows.unwrap("some"), 6n));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").maxLength.unwrap("some"), 1000n));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").disabled.unwrap("some"), false));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").readOnly.unwrap("some"), false));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").required.unwrap("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").autoresize.unwrap("some"), false));
    });

    test("creates auto-resize textarea without fixed rows", $ => {
        const textarea = $.let(Textarea.Root("", {
            autoresize: true,
            placeholder: "Start typing...",
            variant: "subtle",
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").autoresize.unwrap("some"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").rows.hasTag("none"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates fixed-size textarea", $ => {
        const textarea = $.let(Textarea.Root("", {
            rows: 8,
            resize: "none",
            maxLength: 2000,
        }));

        $(Assert.equal(textarea.unwrap().unwrap("Textarea").rows.unwrap("some"), 8n));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").resize.unwrap("some").hasTag("none"), true));
        $(Assert.equal(textarea.unwrap().unwrap("Textarea").maxLength.unwrap("some"), 2000n));
    });
}, {   platformFns: TestImpl,});
