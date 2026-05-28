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
import { SwitchType, type SwitchStyle } from "./types.js";

// Re-export types
export { SwitchType, type SwitchStyle } from "./types.js";

// ============================================================================
// Switch Function
// ============================================================================

/**
 * Creates a Switch component with checked state and optional styling.
 *
 * @param checked - Whether the switch is on
 * @param style - Optional styling configuration
 * @returns An East expression representing the switch component
 *
 * @remarks
 * Switch is a toggle control for binary on/off states. Unlike Checkbox,
 * it represents immediate action toggles rather than form selections.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Switch, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Switch.Root(true, {
 *         label: "Dark mode",
 *         colorPalette: "blue",
 *         size: "md",
 *     });
 * });
 * ```
 */
export function createSwitch_(
    checked: SubtypeExprOrValue<BooleanType>,
    style?: SwitchStyle
): ExprType<SwitchType> {
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

    return East.value({
        checked: checked,
        label: style?.label ? some(style.label) : none,
        disabled: style?.disabled !== undefined ? some(style.disabled) : none,
        colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
        size: sizeValue ? some(sizeValue) : none,
        onChange: style?.onChange ? some(style.onChange) : none,
    }, SwitchType);
}

function createSwitch(
    checked: SubtypeExprOrValue<BooleanType>,
    style?: SwitchStyle
): ExprType<UIComponentType> {
    return East.value(variant("Switch", createSwitch_(checked, style)), UIComponentType);
}

/**
 * Switch component for boolean toggle states.
 *
 * @remarks
 * Use `Switch.Root(checked, style)` to create a switch, or access `Switch.Types.Switch` for the East type.
 */
export const Switch = {
    /**
     * Creates a Switch component with checked state and optional styling.
     *
     * @param checked - Whether the switch is on
     * @param style - Optional styling configuration
     * @returns An East expression representing the switch component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Switch, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Switch.Root(true, {
     *         label: "Dark mode",
     *         colorPalette: "blue",
     *     });
     * });
     * ```
     */
    Root: createSwitch,
    Types: {
        /**
         * The concrete East type for Switch component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Switch component.
         *
         * @property checked - Whether the switch is on
         * @property label - Optional label text displayed next to the switch
         * @property disabled - Whether the switch is disabled
         * @property colorPalette - Color scheme for the switch
         * @property size - Size of the switch
         * @property onChange - Callback triggered when switch state changes
         */
        Switch: SwitchType,
    },
} as const;
