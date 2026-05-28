/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { TagsInput, Style } from "../../src/index.js";

describeEast("TagsInput", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates tags input with empty array", $ => {
        const tagsInput = $.let(TagsInput.Root([]));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").value.size(), 0n));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").label.hasTag("none"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").placeholder.hasTag("none"), true));
    });

    test("creates tags input with initial tags", $ => {
        const tagsInput = $.let(TagsInput.Root(["react", "typescript"]));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").value.size(), 2n));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").value.get(0n), "react"));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").value.get(1n), "typescript"));
    });

    test("creates tags input with single tag", $ => {
        const tagsInput = $.let(TagsInput.Root(["tag"]));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").value.size(), 1n));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").value.get(0n), "tag"));
    });

    // =========================================================================
    // Label and Placeholder
    // =========================================================================

    test("creates tags input with label", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            label: "Skills",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").label.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").label.unwrap("some"), "Skills"));
    });

    test("creates tags input with placeholder", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            placeholder: "Add skill...",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").placeholder.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").placeholder.unwrap("some"), "Add skill..."));
    });

    // =========================================================================
    // Constraints
    // =========================================================================

    test("creates tags input with max as number", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            max: 5,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").max.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").max.unwrap("some"), 5n));
    });

    test("creates tags input with max as bigint", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            max: 10n,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").max.unwrap("some"), 10n));
    });

    test("creates tags input with maxLength as number", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            maxLength: 20,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").maxLength.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").maxLength.unwrap("some"), 20n));
    });

    test("creates tags input with maxLength as bigint", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            maxLength: 50n,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").maxLength.unwrap("some"), 50n));
    });

    // =========================================================================
    // Boolean States
    // =========================================================================

    test("creates disabled tags input", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            disabled: true,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").disabled.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").disabled.unwrap("some"), true));
    });

    test("creates read-only tags input", $ => {
        const tagsInput = $.let(TagsInput.Root(["approved", "verified"], {
            readOnly: true,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").readOnly.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").readOnly.unwrap("some"), true));
    });

    test("creates invalid tags input", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            invalid: true,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").invalid.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").invalid.unwrap("some"), true));
    });

    // =========================================================================
    // Behavior Options
    // =========================================================================

    test("creates editable tags input", $ => {
        const tagsInput = $.let(TagsInput.Root(["editable"], {
            editable: true,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").editable.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").editable.unwrap("some"), true));
    });

    test("creates tags input with delimiter", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            delimiter: ",",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").delimiter.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").delimiter.unwrap("some"), ","));
    });

    test("creates tags input with space delimiter", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            delimiter: " ",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").delimiter.unwrap("some"), " "));
    });

    test("creates tags input with addOnPaste", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            addOnPaste: true,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").addOnPaste.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").addOnPaste.unwrap("some"), true));
    });

    test("creates tags input with clear blur behavior", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            blurBehavior: "clear",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").blurBehavior.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").blurBehavior.unwrap("some").hasTag("clear"), true));
    });

    test("creates tags input with add blur behavior", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            blurBehavior: "add",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").blurBehavior.unwrap("some").hasTag("add"), true));
    });

    test("creates tags input with allowOverflow", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            allowOverflow: true,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").allowOverflow.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").allowOverflow.unwrap("some"), true));
    });

    // =========================================================================
    // Variant
    // =========================================================================

    test("creates tags input with outline variant", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            variant: "outline",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").variant.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates tags input with subtle variant", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            variant: "subtle",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates tags input with flushed variant", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            variant: "flushed",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").variant.unwrap("some").hasTag("flushed"), true));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates tags input with size", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            size: "md",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").size.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").size.unwrap("some").hasTag("md"), true));
    });

    test("supports all sizes", $ => {
        const xs = $.let(TagsInput.Root([], { size: "xs" }));
        const sm = $.let(TagsInput.Root([], { size: "sm" }));
        const md = $.let(TagsInput.Root([], { size: "md" }));
        const lg = $.let(TagsInput.Root([], { size: "lg" }));

        $(Assert.equal(xs.unwrap().unwrap("TagsInput").size.unwrap("some").hasTag("xs"), true));
        $(Assert.equal(sm.unwrap().unwrap("TagsInput").size.unwrap("some").hasTag("sm"), true));
        $(Assert.equal(md.unwrap().unwrap("TagsInput").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(lg.unwrap().unwrap("TagsInput").size.unwrap("some").hasTag("lg"), true));
    });

    test("supports Style.Size helper", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            size: Style.Size("lg"),
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").size.unwrap("some").hasTag("lg"), true));
    });

    // =========================================================================
    // Color Palette
    // =========================================================================

    test("creates tags input with blue color palette", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            colorPalette: "blue",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").colorPalette.hasTag("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates tags input with red color palette", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            colorPalette: "red",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").colorPalette.unwrap("some").hasTag("red"), true));
    });

    test("creates tags input with green color palette", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            colorPalette: "green",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").colorPalette.unwrap("some").hasTag("green"), true));
    });

    test("supports Style.ColorScheme helper", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            colorPalette: Style.ColorScheme("purple"),
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates tags input with all options", $ => {
        const tagsInput = $.let(TagsInput.Root(["react", "typescript"], {
            label: "Technologies",
            placeholder: "Add technology...",
            max: 10,
            maxLength: 30,
            disabled: false,
            readOnly: false,
            invalid: false,
            editable: true,
            delimiter: ",",
            addOnPaste: true,
            blurBehavior: "add",
            allowOverflow: false,
            size: "md",
            variant: "outline",
            colorPalette: "blue",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").value.size(), 2n));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").label.unwrap("some"), "Technologies"));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").placeholder.unwrap("some"), "Add technology..."));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").max.unwrap("some"), 10n));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").maxLength.unwrap("some"), 30n));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").disabled.unwrap("some"), false));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").readOnly.unwrap("some"), false));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").invalid.unwrap("some"), false));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").editable.unwrap("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").delimiter.unwrap("some"), ","));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").addOnPaste.unwrap("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").blurBehavior.unwrap("some").hasTag("add"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").allowOverflow.unwrap("some"), false));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").variant.unwrap("some").hasTag("outline"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates basic skills input", $ => {
        const tagsInput = $.let(TagsInput.Root([], {
            label: "Skills",
            placeholder: "Add skill...",
            max: 5,
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").label.unwrap("some"), "Skills"));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").max.unwrap("some"), 5n));
    });

    test("creates comma-delimited tags input with paste support", $ => {
        const tagsInput = $.let(TagsInput.Root(["react", "typescript"], {
            label: "Technologies",
            delimiter: ",",
            addOnPaste: true,
            placeholder: "Type or paste tags...",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").delimiter.unwrap("some"), ","));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").addOnPaste.unwrap("some"), true));
    });

    test("creates read-only display tags", $ => {
        const tagsInput = $.let(TagsInput.Root(["approved", "verified"], {
            readOnly: true,
            variant: "subtle",
        }));

        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").value.size(), 2n));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").readOnly.unwrap("some"), true));
        $(Assert.equal(tagsInput.unwrap().unwrap("TagsInput").variant.unwrap("some").hasTag("subtle"), true));
    });
}, {   platformFns: TestImpl,});
