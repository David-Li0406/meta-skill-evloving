/**
 * Typography TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the typography module (Code, Text, Heading, Link, etc.).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Code.Root, Text.Root)
 */

import { East } from "@elaraai/east";
import { Code, CodeBlock, Heading, Highlight, Link, List, Mark, Text, UIComponentType } from "../src/index.js";

// ============================================================================
// CODE
// ============================================================================

// File: src/typography/code/index.ts
// Export: Code (namespace example)
const codeExample = East.function([], UIComponentType, $ => {
    return Code.Root("const x = 42", {
        colorPalette: "purple",
        variant: "surface",
    });
});
codeExample.toIR().compile([])();

// ============================================================================
// CODE BLOCK
// ============================================================================

// File: src/typography/code-block/index.ts
// Export: CodeBlock (namespace example)
const codeBlockExample = East.function([], UIComponentType, $ => {
    return CodeBlock.Root(
        `function hello() {\n  console.log("Hello!");\n}`,
        {
            language: "typescript",
            showLineNumbers: true,
            highlightLines: [2n],
        }
    );
});
codeBlockExample.toIR().compile([])();

// ============================================================================
// HEADING
// ============================================================================

// File: src/typography/heading/index.ts
// Export: Heading (namespace example)
const headingExample = East.function([], UIComponentType, $ => {
    return Heading.Root("Welcome", {
        size: "2xl",
        as: "h1",
        color: "blue.600",
    });
});
headingExample.toIR().compile([])();

// ============================================================================
// HIGHLIGHT
// ============================================================================

// File: src/typography/highlight/index.ts
// Export: Highlight (namespace example)
const highlightExample = East.function([], UIComponentType, $ => {
    return Highlight.Root(
        "Search results for: react components",
        ["react", "components"],
        { color: "yellow.200" }
    );
});
highlightExample.toIR().compile([])();

// ============================================================================
// LINK
// ============================================================================

// File: src/typography/link/index.ts
// Export: Link (namespace example)
const linkExample = East.function([], UIComponentType, $ => {
    return Link.Root("Visit our site", "https://example.com", {
        external: true,
        colorPalette: "blue",
    });
});
linkExample.toIR().compile([])();

// ============================================================================
// LIST
// ============================================================================

// File: src/typography/list/index.ts
// Export: List (namespace example)
const listExample = East.function([], UIComponentType, $ => {
    return List.Root([
        "First item",
        "Second item",
        "Third item",
    ], {
        variant: "unordered",
        gap: "2",
    });
});
listExample.toIR().compile([])();

// ============================================================================
// MARK
// ============================================================================

// File: src/typography/mark/index.ts
// Export: Mark (namespace example)
const markExample = East.function([], UIComponentType, $ => {
    return Mark.Root("Important text", {
        colorPalette: "yellow",
        variant: "subtle",
    });
});
markExample.toIR().compile([])();

// ============================================================================
// TEXT
// ============================================================================

// File: src/typography/text/index.ts
// Export: Text (namespace example)
const textExample = East.function([], UIComponentType, $ => {
    return Text.Root("Hello World", {
        color: "blue.500",
        fontWeight: "bold",
    });
});
textExample.toIR().compile([])();

console.log("Typography TypeDoc examples compiled and executed successfully!");
