/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    StringType,
    BooleanType,
    NullType,
    FunctionType,
} from "@elaraai/east";

import { SizeType, ColorSchemeType } from "../../style.js";
import type { SizeLiteral, ColorSchemeLiteral } from "../../style.js";

// ============================================================================
// Switch Type
// ============================================================================

/**
 * Type for Switch component data.
 *
 * @remarks
 * Switch is a toggle control for boolean on/off states with optional label.
 *
 * @property checked - Whether the switch is on
 * @property label - Optional label text displayed next to the switch
 * @property disabled - Whether the switch is disabled
 * @property colorPalette - Color scheme for the switch
 * @property size - Size of the switch
 * @property onChange - Callback triggered when switch state changes
 */
export const SwitchType = StructType({
    checked: BooleanType,
    label: OptionType(StringType),
    disabled: OptionType(BooleanType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    onChange: OptionType(FunctionType([BooleanType], NullType)),
});

/**
 * Type representing the Switch structure.
 */
export type SwitchType = typeof SwitchType;

// ============================================================================
// Switch Style
// ============================================================================

/**
 * TypeScript interface for Switch style options.
 *
 * @property label - Optional label text displayed next to the switch
 * @property disabled - Whether the switch is disabled
 * @property colorPalette - Color scheme for the switch
 * @property size - Size of the switch
 * @property onChange - Callback triggered when switch state changes
 */
export interface SwitchStyle {
    /** Optional label text displayed next to the switch */
    label?: SubtypeExprOrValue<StringType>;
    /** Whether the switch is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Color scheme for the switch */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the switch */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Callback triggered when switch state changes (receives new checked value) */
    onChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
}
