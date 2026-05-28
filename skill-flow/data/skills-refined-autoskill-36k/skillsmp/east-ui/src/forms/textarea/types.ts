/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    StringType,
    IntegerType,
    BooleanType,
    VariantType,
    NullType,
    FunctionType,
} from "@elaraai/east";

import { SizeType } from "../../style.js";
import type { SizeLiteral } from "../../style.js";
import { InputVariantType } from "../input/types.js";
import type { InputVariantLiteral } from "../input/types.js";

// Re-export InputVariantType for convenience
export { InputVariantType, type InputVariantLiteral } from "../input/types.js";

// ============================================================================
// Textarea Resize Type
// ============================================================================

/**
 * Resize behavior for Textarea component.
 *
 * @remarks
 * Controls how the textarea can be resized by the user.
 *
 * @property none - Cannot be resized
 * @property vertical - Can only be resized vertically
 * @property horizontal - Can only be resized horizontally
 * @property both - Can be resized in both directions
 */
export const TextareaResizeType = VariantType({
    /** Cannot be resized */
    none: NullType,
    /** Can only be resized vertically */
    vertical: NullType,
    /** Can only be resized horizontally */
    horizontal: NullType,
    /** Can be resized in both directions */
    both: NullType,
});

/**
 * Type representing the TextareaResize structure.
 */
export type TextareaResizeType = typeof TextareaResizeType;

/**
 * String literal type for resize values.
 */
export type TextareaResizeLiteral = "none" | "vertical" | "horizontal" | "both";

// ============================================================================
// Textarea Type
// ============================================================================

/**
 * Type for Textarea component data.
 *
 * @remarks
 * Textarea is a multi-line text input control for longer text content.
 *
 * @property value - Current text value
 * @property placeholder - Placeholder text when empty
 * @property variant - Visual style variant (outline, subtle, flushed)
 * @property size - Size of the textarea
 * @property resize - Resize behavior
 * @property rows - Number of visible text rows
 * @property disabled - Whether the textarea is disabled
 * @property readOnly - Whether the textarea is read-only
 * @property required - Whether the textarea is required
 * @property maxLength - Maximum number of characters
 * @property autoresize - Whether to auto-resize based on content
 * @property onValidate - Callback triggered for validation
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when textarea loses focus
 * @property onFocus - Callback triggered when textarea gains focus
 */
export const TextareaType = StructType({
    /** Current text value */
    value: StringType,
    /** Placeholder text when empty */
    placeholder: OptionType(StringType),
    /** Visual style variant */
    variant: OptionType(InputVariantType),
    /** Size of the textarea */
    size: OptionType(SizeType),
    /** Resize behavior */
    resize: OptionType(TextareaResizeType),
    /** Number of visible text rows */
    rows: OptionType(IntegerType),
    /** Whether the textarea is disabled */
    disabled: OptionType(BooleanType),
    /** Whether the textarea is read-only */
    readOnly: OptionType(BooleanType),
    /** Whether the textarea is required */
    required: OptionType(BooleanType),
    /** Maximum number of characters */
    maxLength: OptionType(IntegerType),
    /** Whether to auto-resize based on content */
    autoresize: OptionType(BooleanType),
    /** Whether the textarea is in invalid state */
    onValidate: OptionType(FunctionType([StringType], NullType)),
    /** Callback triggered when value changes */
    onChange: OptionType(FunctionType([StringType], NullType)),
    /** Callback triggered when textarea loses focus */
    onBlur: OptionType(FunctionType([], NullType)),
    /** Callback triggered when textarea gains focus */
    onFocus: OptionType(FunctionType([], NullType)),
});

/**
 * Type representing the Textarea structure.
 */
export type TextareaType = typeof TextareaType;

// ============================================================================
// Textarea Style Interface
// ============================================================================

/**
 * TypeScript interface for Textarea style options.
 *
 * @property placeholder - Placeholder text when empty
 * @property variant - Visual style variant (outline, subtle, flushed)
 * @property size - Size of the textarea
 * @property resize - Resize behavior
 * @property rows - Number of visible text rows
 * @property disabled - Whether the textarea is disabled
 * @property readOnly - Whether the textarea is read-only
 * @property invalid - Whether the textarea is in invalid state
 * @property required - Whether the textarea is required
 * @property maxLength - Maximum number of characters
 * @property autoresize - Whether to auto-resize based on content
 * @property onValidate - Callback triggered for validation
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when textarea loses focus
 * @property onFocus - Callback triggered when textarea gains focus
 */
export interface TextareaStyle {
    /** Placeholder text when empty */
    placeholder?: SubtypeExprOrValue<StringType>;
    /** Visual style variant (outline, subtle, flushed) */
    variant?: SubtypeExprOrValue<InputVariantType> | InputVariantLiteral;
    /** Size of the textarea */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Resize behavior */
    resize?: SubtypeExprOrValue<TextareaResizeType> | TextareaResizeLiteral;
    /** Number of visible text rows */
    rows?: SubtypeExprOrValue<IntegerType> | number;
    /** Whether the textarea is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Whether the textarea is read-only */
    readOnly?: SubtypeExprOrValue<BooleanType>;
    /** Whether the textarea is in invalid state */
    invalid?: SubtypeExprOrValue<BooleanType>;
    /** Whether the textarea is required */
    required?: SubtypeExprOrValue<BooleanType>;
    /** Maximum number of characters */
    maxLength?: SubtypeExprOrValue<IntegerType> | number;
    /** Whether to auto-resize based on content */
    autoresize?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered for validation */
    onValidate?: SubtypeExprOrValue<FunctionType<[StringType], NullType>>;
    /** Callback triggered when value changes */
    onChange?: SubtypeExprOrValue<FunctionType<[StringType], NullType>>;
    /** Callback triggered when textarea loses focus */
    onBlur?: SubtypeExprOrValue<FunctionType<[], NullType>>;
    /** Callback triggered when textarea gains focus */
    onFocus?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}
