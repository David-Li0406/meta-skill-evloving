/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    StringType,
    BooleanType,
    StructType,
    OptionType,
    VariantType,
    NullType,
} from "@elaraai/east";
import { DateTimeInputType, FloatInputType, IntegerInputType, StringInputType } from "../input/types.js";
import { SelectRootType } from "../select/types.js";
import { FileUploadType } from "../file-upload/types.js";
import { SliderType } from "../slider/types.js";
import { SwitchType } from "../switch/types.js";
import { TagsInputRootType } from "../tags-input/types.js";
import { TextareaType } from "../textarea/types.js";
import { CheckboxType } from "../checkbox/types.js";

/**
 * Field orientation options for layout direction.
 * @remarks
 * Controls whether label and control are arranged vertically or horizontally.
 * 
 * @property vertical - Label above control
 * @property horizontal - Label beside control
 */
export const FieldOrientationType = VariantType({
    vertical: NullType,
    horizontal: NullType,
});

/**
 * Type representing the FieldOrientation structure.
 */
export type FieldOrientationType = typeof FieldOrientationType;

/**
 * String literal type for orientation values.
 */
export type FieldOrientationLiteral = "vertical" | "horizontal";

// ============================================================================
// Field Control Type
// ============================================================================

/**
 * Unified control type as a variant of all input types.
 *
 * @property Checkbox - Checkbox input
 * @property StringInput - String text input
 * @property IntegerInput - Integer number input
 * @property FloatInput - Float number input
 * @property DateTimeInput - Date/time picker input
 * @property FileUpload - File upload input
 * @property Select - Select dropdown input
 * @property Slider - Slider input
 * @property Switch - Switch/toggle input
 * @property TagsInput - Tags input
 * @property Textarea - Multi-line textarea input
 * 
 */
export const ControlRootType = VariantType({
    Checkbox: CheckboxType,
    StringInput: StringInputType,
    IntegerInput: IntegerInputType,
    FloatInput: FloatInputType,
    DateTimeInput: DateTimeInputType,
    FileUpload: FileUploadType,
    Select: SelectRootType,
    Slider: SliderType,
    Switch: SwitchType,
    TagsInput: TagsInputRootType,
    Textarea: TextareaType
});

export type ControlRootType = typeof ControlRootType;

// ============================================================================
// Field Type
// ============================================================================

/**
 * The concrete East type for Field component data.
 *
 * @remarks
 * Field wraps a form control (Input, Select, Checkbox, etc.) with
 * a label and optional helper/error text for form field presentation.
 *
 * @property label - Label text for the field
 * @property control - The form control component (Input, Select, etc.)
 * @property helperText - Optional descriptive help text
 * @property errorText - Optional validation error message
 * @property required - Whether the field is required
 * @property disabled - Whether the field is disabled
 * @property readOnly - Whether the field is read-only
 * @property orientation - Layout orientation of label and control
 */
export const FieldType = StructType({
    label: StringType,
    control: ControlRootType,
    helperText: OptionType(StringType),
    errorText: OptionType(StringType),
    required: OptionType(BooleanType),
    disabled: OptionType(BooleanType),
    invalid: OptionType(BooleanType),
    readOnly: OptionType(BooleanType),
    orientation: OptionType(FieldOrientationType),
});

/**
 * Type representing the Field component structure.
 */
export type FieldType = typeof FieldType;

// ============================================================================
// Field Style Interface
// ============================================================================

/**
 * TypeScript interface for Field configuration options.
 *
 * @remarks
 * Field wraps a form control (Input, Select, Checkbox, etc.) with
 * a label and optional helper/error text.
 *
 * @property helperText - Optional descriptive help text
 * @property errorText - Optional validation error message
 * @property required - Whether the field is required
 * @property disabled - Whether the field is disabled
 * @property invalid - Weather the field is invalid
 * @property readOnly - Whether the field is read-only
 * @property orientation - Layout orientation of label and control
 */
export interface FieldStyle {
    /** Optional descriptive help text */
    helperText?: SubtypeExprOrValue<StringType>;
    /** Optional validation error message */
    errorText?: SubtypeExprOrValue<StringType>;
    /** Whether the field is required */
    required?: SubtypeExprOrValue<BooleanType>;
    /** Whether the field is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Weather the field is invalid */
    invalid?: SubtypeExprOrValue<BooleanType>;
    /** Whether the field is read-only */
    readOnly?: SubtypeExprOrValue<BooleanType>;
    /** Layout orientation of label and control */
    orientation?: SubtypeExprOrValue<FieldOrientationType> | FieldOrientationLiteral;
}
