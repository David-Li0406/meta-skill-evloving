/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { CodeBlock } from "../../src/index.js";

describeEast("CodeBlock", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates code block with code string", $ => {
        const block = $.let(CodeBlock.Root("const x = 1;"));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").code, "const x = 1;"));
    });

    test("creates code block with no style - all options are none", $ => {
        const block = $.let(CodeBlock.Root("console.log('hello')"));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").code, "console.log('hello')"));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.hasTag("none"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").showLineNumbers.hasTag("none"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").highlightLines.hasTag("none"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").maxHeight.hasTag("none"), true));
    });

    test("creates code block with multiline code", $ => {
        const code = `function hello() {
  console.log("Hello!");
}`;
        const block = $.let(CodeBlock.Root(code));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").code, code));
    });

    // =========================================================================
    // Language
    // =========================================================================

    test("creates code block with typescript language", $ => {
        const block = $.let(CodeBlock.Root("const x: number = 1;", {
            language: "typescript",
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.hasTag("some"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.unwrap("some").hasTag("typescript"), true));
    });

    test("creates code block with javascript language", $ => {
        const block = $.let(CodeBlock.Root("const x = 1;", {
            language: "javascript",
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.unwrap("some").hasTag("javascript"), true));
    });

    test("creates code block with python language", $ => {
        const block = $.let(CodeBlock.Root("print('hello')", {
            language: "python",
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.unwrap("some").hasTag("python"), true));
    });

    test("creates code block with json language", $ => {
        const block = $.let(CodeBlock.Root('{ "key": "value" }', {
            language: "json",
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.unwrap("some").hasTag("json"), true));
    });

    // =========================================================================
    // Line Numbers
    // =========================================================================

    test("creates code block with line numbers enabled", $ => {
        const block = $.let(CodeBlock.Root("line 1\nline 2", {
            showLineNumbers: true,
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").showLineNumbers.hasTag("some"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").showLineNumbers.unwrap("some"), true));
    });

    test("creates code block with line numbers disabled", $ => {
        const block = $.let(CodeBlock.Root("code", {
            showLineNumbers: false,
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").showLineNumbers.unwrap("some"), false));
    });

    // =========================================================================
    // Highlight Lines
    // =========================================================================

    test("creates code block with single highlighted line", $ => {
        const block = $.let(CodeBlock.Root("line 1\nline 2\nline 3", {
            highlightLines: [2n],
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").highlightLines.hasTag("some"), true));
    });

    test("creates code block with multiple highlighted lines", $ => {
        const block = $.let(CodeBlock.Root("a\nb\nc\nd", {
            highlightLines: [1n, 3n],
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").highlightLines.hasTag("some"), true));
    });

    // =========================================================================
    // Max Height
    // =========================================================================

    test("creates code block with maxHeight", $ => {
        const block = $.let(CodeBlock.Root("// long code", {
            maxHeight: "400px",
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").maxHeight.hasTag("some"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").maxHeight.unwrap("some"), "400px"));
    });

    test("creates code block with percentage maxHeight", $ => {
        const block = $.let(CodeBlock.Root("code", {
            maxHeight: "50vh",
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").maxHeight.unwrap("some"), "50vh"));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates code block with all options", $ => {
        const code = `function hello() {
  console.log("Hello!");
}`;
        const block = $.let(CodeBlock.Root(code, {
            language: "typescript",
            showLineNumbers: true,
            highlightLines: [2n],
            maxHeight: "300px",
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").code, code));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.unwrap("some").hasTag("typescript"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").showLineNumbers.unwrap("some"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").highlightLines.hasTag("some"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").maxHeight.unwrap("some"), "300px"));
    });

    test("creates documentation code example", $ => {
        const code = `import { East } from "@elaraai/east";

const value = East.value(42);`;
        const block = $.let(CodeBlock.Root(code, {
            language: "typescript",
            showLineNumbers: true,
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.unwrap("some").hasTag("typescript"), true));
        $(Assert.equal(block.unwrap().unwrap("CodeBlock").showLineNumbers.unwrap("some"), true));
    });

    test("creates terminal output block", $ => {
        const output = `$ npm install
added 100 packages`;
        const block = $.let(CodeBlock.Root(output, {
            language: "bash",
        }));

        $(Assert.equal(block.unwrap().unwrap("CodeBlock").language.unwrap("some").hasTag("bash"), true));
    });
}, {   platformFns: TestImpl,});
