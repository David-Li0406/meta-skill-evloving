/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    BooleanType,
    variant,
    some,
    none,
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import { CheckboxType, type CheckboxStyle } from "./types.js";

// Re-export types
export { CheckboxType, type CheckboxStyle } from "./types.js";

// ============================================================================
// Checkbox Function
// ============================================================================

/**
 * Creates a Checkbox component with checked state and optional styling.
 *
 * @param checked - Whether the checkbox is checked
 * @param style - Optional styling configuration
 * @returns An East expression representing the checkbox component
 *
 * @remarks
 * Checkbox is a form control for boolean selections. It supports labels,
 * indeterminate state for partial selections, and various sizes and colors.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Checkbox, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Checkbox.Root(true, {
 *         label: "Enable notifications",
 *         colorPalette: "blue",
 *         size: "md",
 *     });
 * });
 * ```
 */
export function createCheckbox_(
    checked: SubtypeExprOrValue<BooleanType>,
    style?: CheckboxStyle
): ExprType<CheckboxType> {
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

    return East.value( {
        checked: checked,
        label: style?.label ? some(style.label) : none,
        indeterminate: style?.indeterminate !== undefined ? some(style.indeterminate) : none,
        disabled: style?.disabled !== undefined ? some(style.disabled) : none,
        colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
        size: sizeValue ? some(sizeValue) : none,
        onChange: style?.onChange ? some(style.onChange) : none,
    }, CheckboxType);
}

function createCheckbox(
    checked: SubtypeExprOrValue<BooleanType>,
    style?: CheckboxStyle
): ExprType<UIComponentType> {
    return East.value(variant("Checkbox", createCheckbox_(checked, style)), UIComponentType);
}

/**
 * Checkbox component for boolean form selections.
 *
 * @remarks
 * Use `Checkbox.Root(checked, style)` to create a checkbox, or access `Checkbox.Types.Checkbox` for the East type.
 */
export const Checkbox = {
    /**
     * Creates a Checkbox component with checked state and optional styling.
     *
     * @param checked - Whether the checkbox is checked
     * @param style - Optional styling configuration
     * @returns An East expression representing the checkbox component
     *
     * @remarks
     * Checkbox is a form control for boolean selections. It supports labels,
     * indeterminate state for partial selections, and various sizes and colors.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Checkbox, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Checkbox.Root(true, {
     *         label: "Enable notifications",
     *         colorPalette: "blue",
     *         size: "md",
     *     });
     * });
     * ```
     */
    Root: createCheckbox,
    Types: {
        /**
         * Type for Checkbox component data.
         *
         * @remarks
         * Checkbox is a form control for boolean selections with optional label.
         *
         * @property checked - Whether the checkbox is checked
         * @property label - Optional label text displayed next to the checkbox
         * @property indeterminate - Whether to show indeterminate state (partial selection)
         * @property disabled - Whether the checkbox is disabled
         * @property colorPalette - Color scheme for the checkbox
         * @property size - Size of the checkbox
         */
        Checkbox: CheckboxType,
    },
} as const;
