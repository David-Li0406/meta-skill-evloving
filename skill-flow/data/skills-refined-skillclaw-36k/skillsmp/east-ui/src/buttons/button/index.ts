/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    East,
    StringType, variant,
    some,
    none,
    type SubtypeExprOrValue
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import {
    ButtonType,
    ButtonStyleType,
    ButtonVariantType,
    type ButtonStyle,
} from "./types.js";

// Re-export types
export {
    ButtonType,
    ButtonStyleType,
    ButtonVariantType,
    type ButtonStyle,
    type ButtonVariantLiteral,
} from "./types.js";

// ============================================================================
// Button Function
// ============================================================================

/**
 * Creates a Button component with a label and optional styling.
 *
 * @param label - The text to display on the button
 * @param style - Optional styling configuration
 * @returns An East expression representing the styled button component
 *
 * @remarks
 * Button is an interactive component for triggering actions.
 * It supports multiple variants, color schemes, and sizes.
 *
 * @example
 * ```ts
 * import { Button } from "@elaraai/east-ui";
 *
 * // Simple button
 * const submitButton = Button.Root("Submit");
 *
 * // Button with styling
 * const primaryButton = Button.Root("Save", {
 *   variant: "solid",
 *   colorPalette: "blue",
 *   size: "md",
 * });
 *
 * // Loading button
 * const loadingButton = Button.Root("Processing...", {
 *   variant: "solid",
 *   colorPalette: "blue",
 *   loading: true,
 * });
 *
 * // Access the type
 * const buttonType = Button.Types.Button;
 * ```
 */
function createButton(
    label: SubtypeExprOrValue<StringType>,
    style?: ButtonStyle
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), ButtonVariantType)
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

    return East.value(variant("Button", {
        label: label,
        style: style ? some(East.value({
            variant: variantValue ? some(variantValue) : none,
            colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
            size: sizeValue ? some(sizeValue) : none,
            loading: style.loading !== undefined ? some(style.loading) : none,
            disabled: style.disabled !== undefined ? some(style.disabled) : none,
            onClick: style.onClick ? some(style.onClick) : none,
        }, ButtonStyleType)) : none,
    }), UIComponentType);
}

/**
 * Button component for triggering actions.
 *
 * @remarks
 * Use `Button.Root(label, style)` to create a button, or access `Button.Types.Button` for the East type.
 *
 * @example
 * ```ts
 * import { Button } from "@elaraai/east-ui";
 *
 * // Create a button
 * const btn = Button.Root("Click me", { variant: "solid", colorPalette: "blue" });
 *
 * // Access the type
 * const buttonType = Button.Types.Button;
 * ```
 */
export const Button = {
    /**
     * Creates a Button component with a label and optional styling.
     *
     * @param label - The text to display on the button
     * @param style - Optional styling configuration
     * @returns An East expression representing the styled button component
     *
     * @remarks
     * Button is an interactive component for triggering actions.
     * It supports multiple variants, color schemes, and sizes.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Button, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Button.Root("Save", {
     *         variant: "solid",
     *         colorPalette: "blue",
     *         size: "md",
     *     });
     * });
     * ```
     */
    Root: createButton,
    Types: {
        /**
         * The concrete East type for Button component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Button component.
         *
         * @property label - The text displayed on the button
         * @property style - Optional styling configuration wrapped in OptionType
         */
        Button: ButtonType,
        /**
         * Style type for Button component configuration.
         *
         * @remarks
         * This struct type defines the styling configuration for a Button component.
         *
         * @property variant - Button appearance variant (solid, subtle, outline, ghost)
         * @property colorPalette - Color scheme for the button
         * @property size - Size of the button (xs, sm, md, lg)
         * @property loading - Whether the button shows a loading state
         * @property disabled - Whether the button is disabled
         */
        Style: ButtonStyleType,
        /**
         * Variant type for Button appearance styles.
         *
         * @remarks
         * Create instances using string literals like "solid", "outline", etc.
         *
         * @property solid - Solid filled button (default)
         * @property subtle - Subtle/light background button
         * @property outline - Outlined button with border
         * @property ghost - Transparent button, visible on hover
         */
        Variant: ButtonVariantType,
    },
} as const;
