/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    East,
    StringType,
    variant,
    some,
    none,
    type SubtypeExprOrValue
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import {
    CopyButtonType,
    CopyButtonStyleType,
    CopyButtonVariantType,
    type CopyButtonStyle,
} from "./types.js";

// Re-export types
export {
    CopyButtonType,
    CopyButtonStyleType,
    CopyButtonVariantType,
    type CopyButtonStyle,
    type CopyButtonVariantLiteral,
} from "./types.js";

// ============================================================================
// CopyButton Function
// ============================================================================

/**
 * Creates a CopyButton component that copies a value to the clipboard.
 *
 * @param value - The text value to copy to clipboard (required)
 * @param style - Optional styling configuration
 * @returns An East expression representing the copy button component
 *
 * @remarks
 * CopyButton is an interactive component for copying text to the clipboard.
 * It shows a copy icon by default and changes to a checkmark when copied.
 *
 * @example
 * ```ts
 * import { CopyButton } from "@elaraai/east-ui";
 *
 * // Simple copy button
 * const copyBtn = CopyButton.Root("text to copy");
 *
 * // Copy button with label
 * const labeledCopyBtn = CopyButton.Root("secret-key-123", { label: "Copy API Key" });
 *
 * // Copy button with styling
 * const styledCopyBtn = CopyButton.Root("https://example.com", {
 *   variant: "outline",
 *   colorPalette: "blue",
 *   size: "sm",
 * });
 * ```
 */
function createCopyButton(
    value: SubtypeExprOrValue<StringType>,
    style?: CopyButtonStyle & { label?: SubtypeExprOrValue<StringType> }
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), CopyButtonVariantType)
            : style.variant)
        : undefined;

    const colorPaletteValue = style?.colorPalette
        ? (typeof style.colorPalette === "string"
            ? East.value(variant(style.colorPalette, null), ColorSchemeType)
            : style.colorPalette)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), SizeType)
            : style.size)
        : undefined;

    return East.value(variant("CopyButton", {
        value: value,
        label: style?.label ? some(style.label) : none,
        style: style ? some(East.value({
            variant: variantValue ? some(variantValue) : none,
            colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
            size: sizeValue ? some(sizeValue) : none,
            disabled: style.disabled !== undefined ? some(style.disabled) : none,
            timeout: style.timeout !== undefined ? some(style.timeout) : none,
        }, CopyButtonStyleType)) : none,
    }), UIComponentType);
}

/**
 * CopyButton component for copying text to the clipboard.
 *
 * @remarks
 * Use `CopyButton.Root(value, style)` to create a copy button, or access `CopyButton.Types.CopyButton` for the East type.
 *
 * @example
 * ```ts
 * import { CopyButton } from "@elaraai/east-ui";
 *
 * // Create a copy button
 * const btn = CopyButton.Root("text to copy", { variant: "outline", colorPalette: "gray" });
 *
 * // With a label
 * const labeledBtn = CopyButton.Root("secret-value", { label: "Copy Secret" });
 *
 * // Access the type
 * const copyButtonType = CopyButton.Types.CopyButton;
 * ```
 */
export const CopyButton = {
    /**
     * Creates a CopyButton component that copies a value to the clipboard.
     *
     * @param value - The text value to copy to clipboard (required)
     * @param style - Optional styling configuration (including optional label)
     * @returns An East expression representing the copy button component
     */
    Root: createCopyButton,
    Types: {
        /**
         * The concrete East type for CopyButton component data.
         */
        CopyButton: CopyButtonType,
        /**
         * Style type for CopyButton component configuration.
         */
        Style: CopyButtonStyleType,
        /**
         * Variant type for CopyButton appearance styles.
         */
        Variant: CopyButtonVariantType,
    },
} as const;
