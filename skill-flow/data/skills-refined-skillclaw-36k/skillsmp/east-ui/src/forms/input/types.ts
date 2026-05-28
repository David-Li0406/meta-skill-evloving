/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    East,
    VariantType,
    OptionType,
    StructType,
    StringType,
    IntegerType,
    FloatType,
    DateTimeType,
    BooleanType,
    NullType,
    FunctionType,
    variant,
    type SubtypeExprOrValue,
    ArrayType,
} from "@elaraai/east";
import {
  DateTimeFormatTokenType
} from "@elaraai/east/internal";

import { SizeType } from "../../style.js";
import type { SizeLiteral } from "../../style.js";

// ============================================================================
// Input Variant Type
// ============================================================================

/**
 * Variant type for Input appearance styles.
 *
 * @remarks
 * Create instances using the {@link InputVariant} function.
 *
 * @property outline - Outlined input with border (default)
 * @property subtle - Input with muted background
 * @property flushed - Underlined input without border
 */
export const InputVariantType = VariantType({
    outline: NullType,
    subtle: NullType,
    flushed: NullType,
});

/**
 * Type representing input variant values.
 */
export type InputVariantType = typeof InputVariantType;

/**
 * String literal type for input variant values.
 */
export type InputVariantLiteral = "outline" | "subtle" | "flushed";

/**
 * Creates an input variant expression.
 *
 * @param inputVariant - The input variant style
 * @returns An East expression representing the input variant
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Input, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Input.String("", {
 *         variant: Input.Variant("outline"),
 *     });
 * });
 * ```
 */
export function InputVariant(inputVariant: "outline" | "subtle" | "flushed"): ExprType<InputVariantType> {
    return East.value(variant(inputVariant, null), InputVariantType);
}

// ============================================================================
// String Input Type
// ============================================================================

/**
 * Type for String input component data.
 *
 * @property value - The current string value
 * @property placeholder - Placeholder text when empty
 * @property variant - Input appearance variant
 * @property size - Size of the input
 * @property maxLength - Maximum character count
 * @property pattern - Regex pattern for validation
 * @property disabled - Whether the input is disabled\
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when input loses focus
 * @property onFocus - Callback triggered when input gains focus
 */
export const StringInputType = StructType({
    value: StringType,
    placeholder: OptionType(StringType),
    variant: OptionType(InputVariantType),
    size: OptionType(SizeType),
    maxLength: OptionType(IntegerType),
    pattern: OptionType(StringType),
    disabled: OptionType(BooleanType),
    onChange: OptionType(FunctionType([StringType], NullType)),
    onBlur: OptionType(FunctionType([], NullType)),
    onFocus: OptionType(FunctionType([], NullType)),
});

export type StringInputType = typeof StringInputType;

/**
 * TypeScript interface for String input style options.
 *
 * @remarks
 * Use this interface when creating String input components.
 *
 * @property placeholder - Placeholder text when empty
 * @property variant - Input appearance variant
 * @property size - Size of the input
 * @property maxLength - Maximum character count
 * @property pattern - Regex pattern for validation
 * @property disabled - Whether the input is disabled
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when input loses focus
 * @property onFocus - Callback triggered when input gains focus
 */
export interface StringInputStyle {
    /** Placeholder text when empty */
    placeholder?: SubtypeExprOrValue<StringType>;
    /** Input appearance variant (outline, subtle, flushed) */
    variant?: SubtypeExprOrValue<InputVariantType> | InputVariantLiteral;
    /** Size of the input (xs, sm, md, lg) */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Maximum character count */
    maxLength?: SubtypeExprOrValue<IntegerType>;
    /** Regex pattern for validation */
    pattern?: SubtypeExprOrValue<StringType>;
    /** Whether the input is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when value changes */
    onChange?: SubtypeExprOrValue<FunctionType<[StringType], NullType>>;
    /** Callback triggered when input loses focus */
    onBlur?: SubtypeExprOrValue<FunctionType<[], NullType>>;
    /** Callback triggered when input gains focus */
    onFocus?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}

// ============================================================================
// Integer Input Type
// ============================================================================

/**
 * Type for Integer input component data.
 *
 * @property value - The current integer value
 * @property min - Minimum allowed value
 * @property max - Maximum allowed value
 * @property step - Step increment for stepper controls
 * @property variant - Input appearance variant
 * @property size - Size of the input
 * @property disabled - Whether the input is disabled
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when input loses focus
 * @property onFocus - Callback triggered when input gains focus
 */
export const IntegerInputType = StructType({
    value: IntegerType,
    min: OptionType(IntegerType),
    max: OptionType(IntegerType),
    step: OptionType(IntegerType),
    variant: OptionType(InputVariantType),
    size: OptionType(SizeType),
    disabled: OptionType(BooleanType),
    onChange: OptionType(FunctionType([IntegerType], NullType)),
    onBlur: OptionType(FunctionType([], NullType)),
    onFocus: OptionType(FunctionType([], NullType)),
});

export type IntegerInputType = typeof IntegerInputType;

/**
 * TypeScript interface for Integer input style options.
 *
 * @remarks
 * Use this interface when creating Integer input components.
 *
 * @property min - Minimum allowed value
 * @property max - Maximum allowed value
 * @property step - Step increment for stepper controls
 * @property variant - Input appearance variant
 * @property size - Size of the input
 * @property disabled - Whether the input is disabled
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when input loses focus
 * @property onFocus - Callback triggered when input gains focus
 */
export interface IntegerInputStyle {
    /** Minimum allowed value */
    min?: SubtypeExprOrValue<IntegerType>;
    /** Maximum allowed value */
    max?: SubtypeExprOrValue<IntegerType>;
    /** Step increment for stepper controls */
    step?: SubtypeExprOrValue<IntegerType>;
    /** Input appearance variant (outline, subtle, flushed) */
    variant?: SubtypeExprOrValue<InputVariantType> | InputVariantLiteral;
    /** Size of the input (xs, sm, md, lg) */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Whether the input is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when value changes */
    onChange?: SubtypeExprOrValue<FunctionType<[IntegerType], NullType>>;
    /** Callback triggered when input loses focus */
    onBlur?: SubtypeExprOrValue<FunctionType<[], NullType>>;
    /** Callback triggered when input gains focus */
    onFocus?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}

// ============================================================================
// Float Input Type
// ============================================================================

/**
 * Type for Float input component data.
 *
 * @property value - The current float value
 * @property min - Minimum allowed value
 * @property max - Maximum allowed value
 * @property step - Step increment for stepper controls
 * @property precision - Number of decimal places
 * @property variant - Input appearance variant
 * @property size - Size of the input
 * @property disabled - Whether the input is disabled
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when input loses focus
 * @property onFocus - Callback triggered when input gains focus
 */
export const FloatInputType = StructType({
    value: FloatType,
    min: OptionType(FloatType),
    max: OptionType(FloatType),
    step: OptionType(FloatType),
    precision: OptionType(IntegerType),
    variant: OptionType(InputVariantType),
    size: OptionType(SizeType),
    disabled: OptionType(BooleanType),
    onChange: OptionType(FunctionType([FloatType], NullType)),
    onBlur: OptionType(FunctionType([], NullType)),
    onFocus: OptionType(FunctionType([], NullType)),
});

export type FloatInputType = typeof FloatInputType;

/**
 * TypeScript interface for Float input style options.
 *
 * @remarks
 * Use this interface when creating Float input components.
 *
 * @property min - Minimum allowed value
 * @property max - Maximum allowed value
 * @property step - Step increment for stepper controls
 * @property precision - Number of decimal places
 * @property variant - Input appearance variant
 * @property size - Size of the input
 * @property disabled - Whether the input is disabled
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when input loses focus
 * @property onFocus - Callback triggered when input gains focus
 */
export interface FloatInputStyle {
    /** Minimum allowed value */
    min?: SubtypeExprOrValue<FloatType>;
    /** Maximum allowed value */
    max?: SubtypeExprOrValue<FloatType>;
    /** Step increment for stepper controls */
    step?: SubtypeExprOrValue<FloatType>;
    /** Number of decimal places */
    precision?: SubtypeExprOrValue<IntegerType>;
    /** Input appearance variant (outline, subtle, flushed) */
    variant?: SubtypeExprOrValue<InputVariantType> | InputVariantLiteral;
    /** Size of the input (xs, sm, md, lg) */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Whether the input is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when value changes */
    onChange?: SubtypeExprOrValue<FunctionType<[FloatType], NullType>>;
    /** Callback triggered when input loses focus */
    onBlur?: SubtypeExprOrValue<FunctionType<[], NullType>>;
    /** Callback triggered when input gains focus */
    onFocus?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}

// ============================================================================
// DateTime Input Type
// ============================================================================

/**
 * Variant type for DateTime format tokens.
 *
 * @remarks
 * Create instances using the {@link DateTimeFormatToken} function.
 */
export const DateTimePrecisionType = VariantType({
    date: NullType,
    time: NullType,
    datetime: NullType,
});
/** Variant type for DateTime precision options. */
export type DateTimePrecisionType = typeof DateTimePrecisionType;
/** String literal type for DateTime precision options. */
export type DateTimePrecisionLiteral = "date" | "time" | "datetime";

/**
 * Type for DateTime input component data.
 *
 * @property value - The current DateTime value
 * @property min - Minimum allowed date/time
 * @property max - Maximum allowed date/time
 * @property precision - Whether to show time picker
 * @property format - Display format token
 * @property variant - Input appearance variant
 * @property size - Size of the input
 * @property disabled - Whether the input is disabled
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when input loses focus
 * @property onFocus - Callback triggered when input gains focus
 */
export const DateTimeInputType = StructType({
    value: DateTimeType,
    min: OptionType(DateTimeType),
    max: OptionType(DateTimeType),
    precision: OptionType(DateTimePrecisionType),
    format: OptionType(ArrayType(DateTimeFormatTokenType)),
    variant: OptionType(InputVariantType),
    size: OptionType(SizeType),
    disabled: OptionType(BooleanType),
    onChange: OptionType(FunctionType([DateTimeType], NullType)),
    onBlur: OptionType(FunctionType([], NullType)),
    onFocus: OptionType(FunctionType([], NullType)),
});

export type DateTimeInputType = typeof DateTimeInputType;

/**
 * TypeScript interface for DateTime input style options.
 *
 * @remarks
 * Use this interface when creating DateTime input components.
 *
 * @property min - Minimum allowed date/time
 * @property max - Maximum allowed date/time
 * @property precision - Whether to show time picker
 * @property format - Display format token
 * @property variant - Input appearance variant
 * @property size - Size of the input
 * @property disabled - Whether the input is disabled
 * @property invalid - Whether the input value is invalid
 * @property onChange - Callback triggered when value changes
 * @property onBlur - Callback triggered when input loses focus
 * @property onFocus - Callback triggered when input gains focus
 */
export interface DateTimeInputStyle {
    /** Minimum allowed date/time */
    min?: SubtypeExprOrValue<DateTimeType>;
    /** Maximum allowed date/time */
    max?: SubtypeExprOrValue<DateTimeType>;
    /** Whether to show time picker */
    precision?: SubtypeExprOrValue<typeof DateTimePrecisionType> | DateTimePrecisionLiteral;
    /** Display format token */
    format?: SubtypeExprOrValue<ArrayType<typeof DateTimeFormatTokenType>> | string;
    /** Input appearance variant (outline, subtle, flushed) */
    variant?: SubtypeExprOrValue<InputVariantType> | InputVariantLiteral;
    /** Size of the input (xs, sm, md, lg) */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Whether the input is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when value changes */
    onChange?: SubtypeExprOrValue<FunctionType<[DateTimeType], NullType>>;
    /** Callback triggered when input loses focus */
    onBlur?: SubtypeExprOrValue<FunctionType<[], NullType>>;
    /** Callback triggered when input gains focus */
    onFocus?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}
