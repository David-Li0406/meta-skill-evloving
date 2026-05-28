/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    type ExprType,
    East,
    StringType,
    variant,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { CodeBlockType, CodeLanguageType, type CodeBlockStyle, type CodeLanguage } from "./types.js";

// Re-export types
export { CodeBlockType, CodeLanguageType, type CodeBlockStyle, type CodeLanguage } from "./types.js";

// ============================================================================
// CodeBlock Component
// ============================================================================

/**
 * Creates a CodeBlock component for displaying code with syntax highlighting.
 *
 * @param code - The code content to display
 * @param style - Optional styling configuration
 * @returns An East expression representing the code block component
 */
function createCodeBlock(
    code: SubtypeExprOrValue<StringType>,
    style?: CodeBlockStyle
): ExprType<UIComponentType> {
    const showLineNumbersValue = style?.showLineNumbers !== undefined
        ? (typeof style.showLineNumbers === "boolean"
            ? style.showLineNumbers
            : style.showLineNumbers)
        : undefined;

    const showCopyButtonValue = style?.showCopyButton !== undefined
        ? (typeof style.showCopyButton === "boolean"
            ? style.showCopyButton
            : style.showCopyButton)
        : undefined;

    // Convert string language to variant
    const languageValue = style?.language !== undefined
        ? (typeof style.language === "string"
            ? East.value(variant(style.language as CodeLanguage, null), CodeLanguageType)
            : style.language)
        : undefined;

    return East.value(variant("CodeBlock", {
        code: code,
        language: languageValue !== undefined ? variant("some", languageValue) : variant("none", null),
        showLineNumbers: showLineNumbersValue !== undefined ? variant("some", showLineNumbersValue) : variant("none", null),
        highlightLines: style?.highlightLines ? variant("some", style.highlightLines) : variant("none", null),
        maxHeight: style?.maxHeight ? variant("some", style.maxHeight) : variant("none", null),
        showCopyButton: showCopyButtonValue !== undefined ? variant("some", showCopyButtonValue) : variant("none", null),
        wordWrap: style?.wordWrap !== undefined ? variant("some", style.wordWrap) : variant("none", null),
        title: style?.title ? variant("some", style.title) : variant("none", null),
    }), UIComponentType);
}

/**
 * CodeBlock component for displaying code blocks with syntax highlighting.
 *
 * @remarks
 * Use `CodeBlock.Root(code, style)` to create code blocks with optional
 * syntax highlighting, line numbers, and line highlighting.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { CodeBlock, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return CodeBlock.Root(
 *         `function hello() {\n  console.log("Hello!");\n}`,
 *         {
 *             language: "typescript",
 *             showLineNumbers: true,
 *             highlightLines: [2n],
 *         }
 *     );
 * });
 * ```
 */
export const CodeBlock = {
    Root: createCodeBlock,
    Types: {
        CodeBlock: CodeBlockType,
        Language: CodeLanguageType,
    },
} as const;
