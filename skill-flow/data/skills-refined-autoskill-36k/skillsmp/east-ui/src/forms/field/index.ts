/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType,
    BooleanType,
    variant,
    none,
    ArrayType,
    FloatType,
    DateTimeType,
    IntegerType,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { ControlRootType, FieldOrientationType, FieldType, type FieldStyle } from "./types.js";
import type { DateTimeInputStyle, FloatInputStyle, IntegerInputStyle, StringInputStyle } from "../input/types.js";
import { DateTimeInput_, FloatInput_, IntegerInput_, StringInput_ } from "../input/index.js";
import { createCheckbox_, type CheckboxStyle } from "../checkbox/index.js";
import { createSwitch_, type SwitchStyle } from "../switch/index.js";
import type { FileUploadStyle } from "../file-upload/types.js";
import { createFileUpload_ } from "../file-upload/index.js";
import type { SelectItemType, SelectStyle } from "../select/types.js";
import { createSelectRoot_ } from "../select/index.js";
import { createSlider_, type SliderStyle } from "../slider/index.js";
import type { TagsInputStyle } from "../tags-input/types.js";
import { createTagsInput_ } from "../tags-input/index.js";
import { createTextarea_, type TextareaStyle } from "../textarea/index.js";

// Re-export types
export { type FieldStyle, FieldType, ControlRootType, FieldOrientationType } from "./types.js";

// ============================================================================
// Field Function
// ============================================================================

/**
 * Creates a Field component wrapping a form control with label and messages.
 *
 * @param label - Label text for the field
 * @param control - The form control component (Input, Select, Checkbox, etc.)
 * @param style - Optional configuration for helper text, error text, and states
 * @returns An East expression representing the field component
 *
 * @remarks
 * Field provides a consistent way to present form controls with labels,
 * helper text, and validation messages. It wraps any form control component.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.StringInput(
 *         "Email",
 *         "",
 *         { placeholder: "Enter email", helperText: "We'll never share your email" }
 *     );
 * });
 * ```
 */
function createField(
    label: SubtypeExprOrValue<StringType>,
    control: ExprType<ControlRootType>,
    style?: FieldStyle
): ExprType<UIComponentType> {
    const toStringOption = (val: SubtypeExprOrValue<StringType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const toBoolOption = (val: SubtypeExprOrValue<BooleanType> | undefined) => {
        if (val === undefined) return variant("none", null);
        return variant("some", val);
    };

    const orientationValue = style?.orientation
        ? (typeof style.orientation === "string"
            ? East.value(variant(style.orientation, null), FieldOrientationType)
            : style.orientation)
        : undefined;
    return East.value(variant("Field", {
        label: label,
        control: control,
        helperText: toStringOption(style?.helperText),
        errorText: toStringOption(style?.errorText),
        required: toBoolOption(style?.required),
        disabled: toBoolOption(style?.disabled),
        invalid: toBoolOption(style?.invalid),
        readOnly: toBoolOption(style?.readOnly),
        orientation: orientationValue ? variant("some", orientationValue) : none,
    }), UIComponentType);
}

/**
 * Creates a Field with a Checkbox control.
 *
 * @param label - Label text for the field
 * @param checked - Initial checked state
 * @param style - Optional field and checkbox styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.Checkbox(
 *         "Accept terms",
 *         false,
 *         { helperText: "You must accept to continue" }
 *     );
 * });
 * ```
 */
function createCheckboxField(
    label: SubtypeExprOrValue<StringType>,
    checked: SubtypeExprOrValue<BooleanType>,
    style?: FieldStyle & CheckboxStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('Checkbox', createCheckbox_(checked, style)), ControlRootType);
    return createField(label, control, style);
}


/**
 * Creates a Field with a FileUpload control.
 *
 * @param label - Label text for the field
 * @param style - Optional field and file upload styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.FileUpload("Documents", {
 *         accept: "application/pdf",
 *         helperText: "Upload PDF files only",
 *     });
 * });
 * ```
 */
function createFileUploadField(
    label: SubtypeExprOrValue<StringType>,
    style?: FieldStyle & FileUploadStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('FileUpload', createFileUpload_(style)), ControlRootType);
    return createField(label, control, style);
}


/**
 * Creates a Field with a Select control.
 *
 * @param label - Label text for the field
 * @param value - Currently selected value
 * @param items - Array of select items
 * @param style - Optional field and select styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, Select, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.Select("Country", "", [
 *         Select.Item("us", "United States"),
 *         Select.Item("uk", "United Kingdom"),
 *     ], { helperText: "Select your country" });
 * });
 * ```
 */
function createSelectField(
    label: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<StringType>,
    items: SubtypeExprOrValue<ArrayType<SelectItemType>>,
    style?: FieldStyle & SelectStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('Select', createSelectRoot_(value, items, style)), ControlRootType);
    return createField(label, control, style);
}

/**
 * Creates a Field with a StringInput control.
 *
 * @param label - Label text for the field
 * @param value - Initial string value
 * @param style - Optional field and input styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.StringInput("Email", "", {
 *         placeholder: "Enter email",
 *         helperText: "We'll never share your email",
 *     });
 * });
 * ```
 */
function createStringInputField(
    label: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<StringType>,
    style?: FieldStyle & StringInputStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('StringInput', StringInput_(value, style)), ControlRootType);
    return createField(label, control, style);
}

/**
 * Creates a Field with a DateTimeInput control.
 *
 * @param label - Label text for the field
 * @param value - Initial datetime value
 * @param style - Optional field and datetime input styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.DateTimeInput("Birth Date", new Date(), {
 *         helperText: "Enter your date of birth",
 *     });
 * });
 * ```
 */
function createDatetimeInputField(
    label: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<DateTimeType>,
    style?: FieldStyle & DateTimeInputStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('DateTimeInput', DateTimeInput_(value, style)), ControlRootType);
    return createField(label, control, style);
}

/**
 * Creates a Field with a FloatInput control.
 *
 * @param label - Label text for the field
 * @param value - Initial float value
 * @param style - Optional field and float input styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.FloatInput("Price", 0.0, {
 *         min: 0,
 *         helperText: "Enter price in dollars",
 *     });
 * });
 * ```
 */
function createFloatInputField(
    label: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<FloatType>,
    style?: FieldStyle & FloatInputStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('FloatInput', FloatInput_(value, style)), ControlRootType);
    return createField(label, control, style);
}

/**
 * Creates a Field with an IntegerInput control.
 *
 * @param label - Label text for the field
 * @param value - Initial integer value
 * @param style - Optional field and integer input styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.IntegerInput("Quantity", 1n, {
 *         min: 1n,
 *         max: 100n,
 *         helperText: "Enter quantity",
 *     });
 * });
 * ```
 */
function createIntegerInputField(
    label: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<IntegerType>,
    style?: FieldStyle & IntegerInputStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('IntegerInput', IntegerInput_(value, style)), ControlRootType);
    return createField(label, control, style);
}

/**
 * Creates a Field with a Slider control.
 *
 * @param label - Label text for the field
 * @param value - Initial slider value
 * @param style - Optional field and slider styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.Slider("Volume", 50.0, {
 *         min: 0,
 *         max: 100,
 *         helperText: "Adjust volume level",
 *     });
 * });
 * ```
 */
function createSliderField(
    label: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<FloatType>,
    style?: FieldStyle & SliderStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('Slider', createSlider_(value, style)), ControlRootType);
    return createField(label, control, style);
}

/**
 * Creates a Field with a Switch control.
 *
 * @param label - Label text for the field
 * @param checked - Initial checked state
 * @param style - Optional field and switch styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.Switch("Enable notifications", true, {
 *         helperText: "Toggle to enable or disable",
 *     });
 * });
 * ```
 */
function createSwitchField(
    label: SubtypeExprOrValue<StringType>,
    checked: SubtypeExprOrValue<BooleanType>,
    style?: FieldStyle & SwitchStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('Switch', createSwitch_(checked, style)), ControlRootType);
    return createField(label, control, style);
}

/**
 * Creates a Field with a TagsInput control.
 *
 * @param label - Label text for the field
 * @param values - Initial array of tag values
 * @param style - Optional field and tags input styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.TagsInput("Skills", ["TypeScript", "React"], {
 *         helperText: "Add your skills",
 *     });
 * });
 * ```
 */
function createTags(
    label: SubtypeExprOrValue<StringType>,
    values: SubtypeExprOrValue<ArrayType<StringType>>,
    style?: FieldStyle & TagsInputStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('TagsInput', createTagsInput_(values, style)), ControlRootType);
    return createField(label, control, style);
}

/**
 * Creates a Field with a Textarea control.
 *
 * @param label - Label text for the field
 * @param value - Initial text value
 * @param style - Optional field and textarea styling
 * @returns An East expression representing the field component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Field, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Field.Textarea("Description", "", {
 *         placeholder: "Enter description",
 *         rows: 4,
 *         helperText: "Maximum 500 characters",
 *     });
 * });
 * ```
 */
function createTextareaField(
    label: SubtypeExprOrValue<StringType>,
    value: SubtypeExprOrValue<StringType>,
    style?: FieldStyle & TextareaStyle
): ExprType<UIComponentType> {
    const control = East.value(variant('Textarea', createTextarea_(value, style)), ControlRootType);
    return createField(label, control, style);
}


/**
 * Field component for wrapping form controls with labels and messages.
 *
 * @remarks
 * Use `Field.StringInput(label, value, style)`, `Field.Checkbox(label, checked, style)`,
 * or other specialized methods to create fields with integrated controls.
 */
export const Field = {
    /**
     * Creates a Field with a Checkbox control.
     *
     * @param label - Label text for the field
     * @param checked - Initial checked state
     * @param style - Optional field and checkbox styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.Checkbox("Accept terms", false, {
     *         helperText: "You must accept to continue",
     *     });
     * });
     * ```
     */
    Checkbox: createCheckboxField,
    /**
     * Creates a Field with a FileUpload control.
     *
     * @param label - Label text for the field
     * @param style - Optional field and file upload styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.FileUpload("Documents", {
     *         accept: "application/pdf",
     *         helperText: "Upload PDF files only",
     *     });
     * });
     * ```
     */
    FileUpload: createFileUploadField,
    /**
     * Creates a Field with a Select control.
     *
     * @param label - Label text for the field
     * @param value - Currently selected value
     * @param items - Array of select items
     * @param style - Optional field and select styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, Select, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.Select("Country", "", [
     *         Select.Item("us", "United States"),
     *         Select.Item("uk", "United Kingdom"),
     *     ], { helperText: "Select your country" });
     * });
     * ```
     */
    Select: createSelectField,
    /**
     * Creates a Field with a Slider control.
     *
     * @param label - Label text for the field
     * @param value - Initial slider value
     * @param style - Optional field and slider styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.Slider("Volume", 50.0, {
     *         min: 0,
     *         max: 100,
     *         helperText: "Adjust volume level",
     *     });
     * });
     * ```
     */
    Slider: createSliderField,
    /**
     * Creates a Field with a StringInput control.
     *
     * @param label - Label text for the field
     * @param value - Initial string value
     * @param style - Optional field and input styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.StringInput("Email", "", {
     *         placeholder: "Enter email",
     *         helperText: "We'll never share your email",
     *     });
     * });
     * ```
     */
    StringInput: createStringInputField,
    /**
     * Creates a Field with a DateTimeInput control.
     *
     * @param label - Label text for the field
     * @param value - Initial datetime value
     * @param style - Optional field and datetime input styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.DateTimeInput("Birth Date", new Date(), {
     *         helperText: "Enter your date of birth",
     *     });
     * });
     * ```
     */
    DateTimeInput: createDatetimeInputField,
    /**
     * Creates a Field with a FloatInput control.
     *
     * @param label - Label text for the field
     * @param value - Initial float value
     * @param style - Optional field and float input styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.FloatInput("Price", 0.0, {
     *         min: 0,
     *         helperText: "Enter price in dollars",
     *     });
     * });
     * ```
     */
    FloatInput: createFloatInputField,
    /**
     * Creates a Field with an IntegerInput control.
     *
     * @param label - Label text for the field
     * @param value - Initial integer value
     * @param style - Optional field and integer input styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.IntegerInput("Quantity", 1n, {
     *         min: 1n,
     *         max: 100n,
     *         helperText: "Enter quantity",
     *     });
     * });
     * ```
     */
    IntegerInput: createIntegerInputField,
    /**
     * Creates a Field with a Switch control.
     *
     * @param label - Label text for the field
     * @param checked - Initial checked state
     * @param style - Optional field and switch styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.Switch("Enable notifications", true, {
     *         helperText: "Toggle to enable or disable",
     *     });
     * });
     * ```
     */
    Switch: createSwitchField,
    /**
     * Creates a Field with a TagsInput control.
     *
     * @param label - Label text for the field
     * @param values - Initial array of tag values
     * @param style - Optional field and tags input styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.TagsInput("Skills", ["TypeScript", "React"], {
     *         helperText: "Add your skills",
     *     });
     * });
     * ```
     */
    TagsInput: createTags,
    /**
     * Creates a Field with a Textarea control.
     *
     * @param label - Label text for the field
     * @param value - Initial text value
     * @param style - Optional field and textarea styling
     * @returns An East expression representing the field component
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Field, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Field.Textarea("Description", "", {
     *         placeholder: "Enter description",
     *         rows: 4,
     *         helperText: "Maximum 500 characters",
     *     });
     * });
     * ```
     */
    Textarea: createTextareaField,
    Types: {
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
        Field: FieldType,
    },
} as const;
