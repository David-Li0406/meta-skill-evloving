/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType, East, variant
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { SizeType, ColorSchemeType } from "../../style.js";
import {
    IconButtonStyleType,
    IconButtonType,
    ButtonVariantType,
    type IconButtonStyle,
} from "./types.js";

import type { IconName, IconPrefix } from "@fortawesome/fontawesome-common-types";

// Re-export types
export {
    IconButtonStyleType,
    IconButtonType,
    type IconButtonStyle,
} from "./types.js";

// ============================================================================
// IconButton Function
// ============================================================================

/**
 * Creates an IconButton component with an icon and optional styling.
 *
 * @param prefix - The Font Awesome icon prefix (e.g., "fas", "far")
 * @param name - The Font Awesome icon name (e.g., "xmark", "bars")
 * @param style - Optional styling configuration
 * @returns An East expression representing the icon button component
 *
 * @remarks
 * IconButton renders an icon within a button. It's useful for toolbar actions,
 * close buttons, and other icon-only interactive elements.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { IconButton, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return IconButton.Root("fas", "xmark", {
 *         variant: "ghost",
 *         colorPalette: "red",
 *     });
 * });
 * ```
 */
function createIconButton(
    prefix: IconPrefix,
    name: IconName,
    style?: IconButtonStyle
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

    const hasStyle = variantValue || colorPaletteValue || sizeValue ||
        style?.loading !== undefined || style?.disabled !== undefined || style?.onClick !== undefined;

    return East.value(variant("IconButton", {
        prefix: prefix,
        name: name,
        style: hasStyle
            ? variant("some", East.value({
                variant: variantValue ? variant("some", variantValue) : variant("none", null),
                colorPalette: colorPaletteValue ? variant("some", colorPaletteValue) : variant("none", null),
                size: sizeValue ? variant("some", sizeValue) : variant("none", null),
                loading: style?.loading !== undefined ? variant("some", style.loading) : variant("none", null),
                disabled: style?.disabled !== undefined ? variant("some", style.disabled) : variant("none", null),
                onClick: style?.onClick !== undefined ? variant("some", style.onClick) : variant("none", null),
            }, IconButtonStyleType))
            : variant("none", null),
    }), UIComponentType);
}

/**
 * IconButton component for icon-only buttons.
 *
 * @remarks
 * Use `IconButton.Root(prefix, name, style)` to create an icon button, or access `IconButton.Types` for East types.
 */
export const IconButton = {
    /**
     * Creates an IconButton component with an icon and optional styling.
     *
     * @param prefix - The Font Awesome icon prefix (e.g., "fas", "far")
     * @param name - The Font Awesome icon name (e.g., "xmark", "bars")
     * @param style - Optional styling configuration
     * @returns An East expression representing the icon button component
     *
     * @remarks
     * IconButton renders an icon within a button. It's useful for toolbar actions,
     * close buttons, and other icon-only interactive elements.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { IconButton, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return IconButton.Root("fas", "xmark");
     * });
     *
     * const styledExample = East.function([], UIComponentType, $ => {
     *     return IconButton.Root("fas", "bars", {
     *         variant: "ghost",
     *         size: "lg",
     *     });
     * });
     * ```
     */
    Root: createIconButton,
    Types: {
        /**
         * The concrete East type for IconButton component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for an IconButton component.
         *
         * @property prefix - The Font Awesome icon prefix
         * @property name - The icon name
         * @property style - Optional styling configuration wrapped in OptionType
         */
        IconButton: IconButtonType,
        /**
         * Style type for IconButton component configuration.
         *
         * @remarks
         * IconButton shares the same style options as Button.
         *
         * @property variant - Button appearance variant (solid, subtle, outline, ghost)
         * @property colorPalette - Color scheme for the button
         * @property size - Size of the button (xs, sm, md, lg)
         * @property loading - Whether the button shows a loading state
         * @property disabled - Whether the button is disabled
         * @property onClick - Callback triggered when the button is clicked
         */
        Style: IconButtonStyleType,
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
