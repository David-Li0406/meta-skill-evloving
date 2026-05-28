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
// Checkbox Type
// ============================================================================

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
 * @property onChange - Callback triggered when checked state changes
 */
export const CheckboxType = StructType({
    checked: BooleanType,
    label: OptionType(StringType),
    indeterminate: OptionType(BooleanType),
    disabled: OptionType(BooleanType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    onChange: OptionType(FunctionType([BooleanType], NullType)),
});

/**
 * Type representing the Checkbox structure.
 */
export type CheckboxType = typeof CheckboxType;

// ============================================================================
// Checkbox Style
// ============================================================================

/**
 * TypeScript interface for Checkbox style options.
 *
 * @property label - Optional label text displayed next to the checkbox
 * @property indeterminate - Whether to show indeterminate state
 * @property disabled - Whether the checkbox is disabled
 * @property colorPalette - Color scheme for the checkbox
 * @property size - Size of the checkbox
 * @property onChange - Callback triggered when checked state changes
 */
export interface CheckboxStyle {
    /** Optional label text displayed next to the checkbox */
    label?: SubtypeExprOrValue<StringType>;
    /** Whether to show indeterminate state (partial selection) */
    indeterminate?: SubtypeExprOrValue<BooleanType>;
    /** Whether the checkbox is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Color scheme for the checkbox */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the checkbox */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Callback triggered when checked state changes (receives new checked value) */
    onChange?: SubtypeExprOrValue<FunctionType<[BooleanType], NullType>>;
}
