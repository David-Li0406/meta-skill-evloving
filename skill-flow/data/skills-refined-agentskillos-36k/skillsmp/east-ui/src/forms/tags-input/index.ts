/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    variant,
    StringType,
    ArrayType,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { SizeType, ColorSchemeType } from "../../style.js";
import {
    TagsInputRootType,
    TagsInputBlurBehaviorType,
    InputVariantType,
    type TagsInputStyle,
} from "./types.js";

// Re-export types
export {
    TagsInputRootType,
    TagsInputBlurBehaviorType,
    InputVariantType,
    type TagsInputStyle,
    type TagsInputBlurBehaviorLiteral,
    type InputVariantLiteral,
} from "./types.js";

// ============================================================================
// TagsInput Factory
// ============================================================================

/**
 * Creates a TagsInput component.
 *
 * @param value - Array of current tag values
 * @param style - Optional style and configuration options
 * @returns An East expression representing the TagsInput component
 *
 * @remarks
 * TagsInput is a multi-tag input control for entering and managing
 * a collection of string tags. It supports features like maximum tag count,
 * character limits, paste parsing, and editable tags.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { TagsInput, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return TagsInput.Root(["React", "TypeScript"], {
 *         placeholder: "Add tag...",
 *         max: 5n,
 *         colorPalette: "blue",
 *     });
 * });
 * ```
 */
export function createTagsInput_(
    value: SubtypeExprOrValue<ArrayType<typeof StringType>>,
    style?: TagsInputStyle
): ExprType<TagsInputRootType> {
    // Convert string literal variants to East values
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), InputVariantType)
            : style.variant)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), SizeType)
            : style.size)
        : undefined;

    const colorPaletteValue = style?.colorPalette
        ? (typeof style.colorPalette === "string"
            ? East.value(variant(style.colorPalette, null), ColorSchemeType)
            : style.colorPalette)
        : undefined;

    const blurBehaviorValue = style?.blurBehavior
        ? (typeof style.blurBehavior === "string"
            ? East.value(variant(style.blurBehavior, null), TagsInputBlurBehaviorType)
            : style.blurBehavior)
        : undefined;

    // Convert number to bigint for IntegerType fields
    const maxValue = style?.max !== undefined
        ? (typeof style.max === "number" ? BigInt(style.max) : style.max)
        : undefined;
    const maxLengthValue = style?.maxLength !== undefined
        ? (typeof style.maxLength === "number" ? BigInt(style.maxLength) : style.maxLength)
        : undefined;

    return East.value({
        value: value,
        defaultValue: style?.defaultValue !== undefined ? variant("some", style.defaultValue) : variant("none", null),
        max: maxValue !== undefined ? variant("some", maxValue) : variant("none", null),
        maxLength: maxLengthValue !== undefined ? variant("some", maxLengthValue) : variant("none", null),
        disabled: style?.disabled !== undefined ? variant("some", style.disabled) : variant("none", null),
        readOnly: style?.readOnly !== undefined ? variant("some", style.readOnly) : variant("none", null),
        invalid: style?.invalid !== undefined ? variant("some", style.invalid) : variant("none", null),
        editable: style?.editable !== undefined ? variant("some", style.editable) : variant("none", null),
        delimiter: style?.delimiter !== undefined ? variant("some", style.delimiter) : variant("none", null),
        addOnPaste: style?.addOnPaste !== undefined ? variant("some", style.addOnPaste) : variant("none", null),
        blurBehavior: blurBehaviorValue ? variant("some", blurBehaviorValue) : variant("none", null),
        allowOverflow: style?.allowOverflow !== undefined ? variant("some", style.allowOverflow) : variant("none", null),
        label: style?.label !== undefined ? variant("some", style.label) : variant("none", null),
        placeholder: style?.placeholder !== undefined ? variant("some", style.placeholder) : variant("none", null),
        size: sizeValue ? variant("some", sizeValue) : variant("none", null),
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
        colorPalette: colorPaletteValue ? variant("some", colorPaletteValue) : variant("none", null),
        onChange: style?.onChange !== undefined ? variant("some", style.onChange) : variant("none", null),
        onInputChange: style?.onInputChange !== undefined ? variant("some", style.onInputChange) : variant("none", null),
        onHighlightChange: style?.onHighlightChange !== undefined ? variant("some", style.onHighlightChange) : variant("none", null),
    }, TagsInputRootType);
}

function createTagsInput(
    value: SubtypeExprOrValue<ArrayType<typeof StringType>>,
    style?: TagsInputStyle
): ExprType<UIComponentType> {
    return East.value(variant("TagsInput", createTagsInput_(value, style)), UIComponentType);
}

// ============================================================================
// TagsInput Namespace Export
// ============================================================================

/**
 * TagsInput component for managing collections of string tags.
 *
 * @remarks
 * Use `TagsInput.Root(value, style)` to create a tags input, or access `TagsInput.Types.Root` for the East type.
 */
export const TagsInput = {
    /**
     * Creates a TagsInput component.
     *
     * @param value - Array of current tag values
     * @param style - Optional style and configuration options
     * @returns An East expression representing the TagsInput component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { TagsInput, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return TagsInput.Root(["React", "TypeScript"], {
     *         placeholder: "Add tag...",
     *         max: 5n,
     *     });
     * });
     * ```
     */
    Root: createTagsInput,
    Types: {
        /**
         * Type for TagsInput component data.
         *
         * @property value - Current array of tag strings
         * @property max - Maximum number of tags allowed
         * @property placeholder - Placeholder text
         */
        Root: TagsInputRootType,
        /**
         * Blur behavior options for TagsInput.
         *
         * @property add - Add current input as tag on blur
         * @property clear - Clear current input on blur
         */
        BlurBehavior: TagsInputBlurBehaviorType,
    },
} as const;
