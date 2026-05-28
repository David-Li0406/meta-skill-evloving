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
    ArrayType,
    VariantType,
    NullType,
    FunctionType,
} from "@elaraai/east";

import { SizeType } from "../../style.js";
import type { SizeLiteral } from "../../style.js";
import { ColorSchemeType } from "../../style.js";
import type { ColorSchemeLiteral } from "../../style.js";
import { InputVariantType } from "../input/types.js";
import type { InputVariantLiteral } from "../input/types.js";

// Re-export InputVariantType for convenience
export { InputVariantType, type InputVariantLiteral } from "../input/types.js";

// ============================================================================
// TagsInput Blur Behavior Type
// ============================================================================

/**
 * Blur behavior for TagsInput component.
 *
 * @remarks
 * Controls what happens when the input loses focus.
 *
 * @property clear - Clear the input on blur
 * @property add - Add the input text as a tag on blur
 */
export const TagsInputBlurBehaviorType = VariantType({
    /** Clear the input on blur */
    clear: NullType,
    /** Add the input text as a tag on blur */
    add: NullType,
});

/**
 * Type representing the TagsInputBlurBehavior structure.
 */
export type TagsInputBlurBehaviorType = typeof TagsInputBlurBehaviorType;

/**
 * String literal type for blur behavior values.
 */
export type TagsInputBlurBehaviorLiteral = "clear" | "add";

// ============================================================================
// TagsInput Type
// ============================================================================

/**
 * Type for TagsInput component data.
 *
 * @remarks
 * TagsInput is a multi-tag input control for entering and managing
 * a collection of string tags.
 *
 * @property value - Array of current tag values
 * @property defaultValue - Initial tag values
 * @property max - Maximum number of tags allowed
 * @property maxLength - Maximum characters per tag
 * @property disabled - Whether the input is disabled
 * @property readOnly - Whether the input is read-only
 * @property invalid - Whether the input is in invalid state
 * @property editable - Whether existing tags can be edited
 * @property delimiter - Separator for parsing pasted text
 * @property addOnPaste - Whether to parse pasted text into tags
 * @property blurBehavior - Action on blur (clear or add)
 * @property allowOverflow - Whether to allow exceeding max
 * @property label - Descriptive label
 * @property placeholder - Placeholder text for input
 * @property size - Size of the input
 * @property variant - Visual style variant
 * @property colorPalette - Color scheme for tags
 * @property onChange - Callback triggered when tags change
 * @property onInputChange - Callback triggered when input text changes
 * @property onHighlightChange - Callback triggered when highlighted tag changes
 */
export const TagsInputRootType = StructType({
    /** Array of current tag values */
    value: ArrayType(StringType),
    /** Initial tag values */
    defaultValue: OptionType(ArrayType(StringType)),

    /** Maximum number of tags allowed */
    max: OptionType(IntegerType),
    /** Maximum characters per tag */
    maxLength: OptionType(IntegerType),

    /** Whether the input is disabled */
    disabled: OptionType(BooleanType),
    /** Whether the input is read-only */
    readOnly: OptionType(BooleanType),
    /** Whether the input is in invalid state */
    invalid: OptionType(BooleanType),

    /** Whether existing tags can be edited */
    editable: OptionType(BooleanType),
    /** Separator for parsing pasted text */
    delimiter: OptionType(StringType),
    /** Whether to parse pasted text into tags */
    addOnPaste: OptionType(BooleanType),
    /** Action on blur (clear or add) */
    blurBehavior: OptionType(TagsInputBlurBehaviorType),
    /** Whether to allow exceeding max */
    allowOverflow: OptionType(BooleanType),

    /** Descriptive label */
    label: OptionType(StringType),
    /** Placeholder text for input */
    placeholder: OptionType(StringType),

    /** Size of the input */
    size: OptionType(SizeType),
    /** Visual style variant */
    variant: OptionType(InputVariantType),
    /** Color scheme for tags */
    colorPalette: OptionType(ColorSchemeType),

    /** Callback triggered when tags change */
    onChange: OptionType(FunctionType([ArrayType(StringType)], NullType)),
    /** Callback triggered when input text changes */
    onInputChange: OptionType(FunctionType([StringType], NullType)),
    /** Callback triggered when highlighted tag changes */
    onHighlightChange: OptionType(FunctionType([OptionType(StringType)], NullType)),
});

/**
 * Type representing the TagsInputRoot structure.
 */
export type TagsInputRootType = typeof TagsInputRootType;

// ============================================================================
// TagsInput Style Interface
// ============================================================================

/**
 * TypeScript interface for TagsInput style options.
 *
 * @property defaultValue - Initial tag values
 * @property max - Maximum number of tags allowed
 * @property maxLength - Maximum characters per tag
 * @property disabled - Whether the input is disabled
 * @property readOnly - Whether the input is read-only
 * @property invalid - Whether the input is in invalid state
 * @property editable - Whether existing tags can be edited
 * @property delimiter - Separator for parsing pasted text
 * @property addOnPaste - Whether to parse pasted text into tags
 * @property blurBehavior - Action on blur (clear or add)
 * @property allowOverflow - Whether to allow exceeding max
 * @property label - Descriptive label
 * @property placeholder - Placeholder text for input
 * @property size - Size of the input
 * @property variant - Visual style variant
 * @property colorPalette - Color scheme for tags
 * @property onChange - Callback triggered when tags change
 * @property onInputChange - Callback triggered when input text changes
 * @property onHighlightChange - Callback triggered when highlighted tag changes
 */
export interface TagsInputStyle {
    /** Initial tag values */
    defaultValue?: SubtypeExprOrValue<ArrayType<typeof StringType>> | string[];
    /** Maximum number of tags allowed */
    max?: SubtypeExprOrValue<IntegerType> | number;
    /** Maximum characters per tag */
    maxLength?: SubtypeExprOrValue<IntegerType> | number;
    /** Whether the input is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Whether the input is read-only */
    readOnly?: SubtypeExprOrValue<BooleanType>;
    /** Whether the input is in invalid state */
    invalid?: SubtypeExprOrValue<BooleanType>;
    /** Whether existing tags can be edited */
    editable?: SubtypeExprOrValue<BooleanType>;
    /** Separator for parsing pasted text */
    delimiter?: SubtypeExprOrValue<StringType>;
    /** Whether to parse pasted text into tags */
    addOnPaste?: SubtypeExprOrValue<BooleanType>;
    /** Action on blur (clear or add) */
    blurBehavior?: SubtypeExprOrValue<TagsInputBlurBehaviorType> | TagsInputBlurBehaviorLiteral;
    /** Whether to allow exceeding max */
    allowOverflow?: SubtypeExprOrValue<BooleanType>;
    /** Descriptive label */
    label?: SubtypeExprOrValue<StringType>;
    /** Placeholder text for input */
    placeholder?: SubtypeExprOrValue<StringType>;
    /** Size of the input */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Visual style variant */
    variant?: SubtypeExprOrValue<InputVariantType> | InputVariantLiteral;
    /** Color scheme for tags */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Callback triggered when tags change */
    onChange?: SubtypeExprOrValue<FunctionType<[ArrayType<typeof StringType>], NullType>>;
    /** Callback triggered when input text changes */
    onInputChange?: SubtypeExprOrValue<FunctionType<[typeof StringType], NullType>>;
    /** Callback triggered when highlighted tag changes */
    onHighlightChange?: SubtypeExprOrValue<FunctionType<[OptionType<typeof StringType>], NullType>>;
}
