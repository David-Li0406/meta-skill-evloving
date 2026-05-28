/**
 * Forms TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the forms module (Checkbox, Input, Select, Slider, Switch, etc.).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Checkbox.Root, Input.String.Root)
 */

import { East } from "@elaraai/east";
import { Checkbox, Field, FileUpload, Input, Select, Slider, Switch, TagsInput, Textarea, UIComponentType } from "../src/index.js";

// ============================================================================
// INPUT
// ============================================================================

// File: src/forms/input/index.ts
// Export: Input.String
const inputStringExample = East.function([], UIComponentType, $ => {
    return Input.String("John", {
        placeholder: "Enter name",
        variant: "outline",
    });
});
inputStringExample.toIR().compile([])();

// File: src/forms/input/index.ts
// Export: Input.Integer
const inputIntegerExample = East.function([], UIComponentType, $ => {
    return Input.Integer(25n, {
        min: 0n,
        max: 150n,
    });
});
inputIntegerExample.toIR().compile([])();

// File: src/forms/input/index.ts
// Export: Input.Float
const inputFloatExample = East.function([], UIComponentType, $ => {
    return Input.Float(19.99, {
        min: 0,
        precision: 2n,
    });
});
inputFloatExample.toIR().compile([])();

// File: src/forms/input/index.ts
// Export: Input.DateTime
const inputDateTimeExample = East.function([], UIComponentType, $ => {
    return Input.DateTime(new Date(), {
        format: "yyyy-MM-dd HH:mm",
    });
});
inputDateTimeExample.toIR().compile([])();

// File: src/forms/input/index.ts
// Export: Input.Variant
const inputVariantExample = East.function([], UIComponentType, $ => {
    return Input.String("", {
        variant: Input.Variant("outline"),
    });
});
inputVariantExample.toIR().compile([])();

// File: src/forms/input/types.ts
// Export: InputVariant
const inputVariantTypesExample = East.function([], UIComponentType, $ => {
    return Input.String("", {
        variant: Input.Variant("outline"),
    });
});
inputVariantTypesExample.toIR().compile([])();

// ============================================================================
// SELECT
// ============================================================================

// File: src/forms/select/index.ts
// Export: createSelectItem (private function)
const selectItemExample = East.function([], UIComponentType, $ => {
    return Select.Root("", [
        Select.Item("us", "United States"),
        Select.Item("restricted", "Restricted", { disabled: true }),
    ]);
});
selectItemExample.toIR().compile([])();

// File: src/forms/select/index.ts
// Export: createSelectRoot (private function)
const selectRootExample = East.function([], UIComponentType, $ => {
    return Select.Root("", [
        Select.Item("us", "United States"),
        Select.Item("uk", "United Kingdom"),
        Select.Item("ca", "Canada"),
    ], {
        placeholder: "Select a country",
    });
});
selectRootExample.toIR().compile([])();

// File: src/forms/select/index.ts
// Export: Select namespace
const selectNamespaceExample = East.function([], UIComponentType, $ => {
    return Select.Root("", [
        Select.Item("us", "United States"),
        Select.Item("uk", "United Kingdom"),
        Select.Item("ca", "Canada"),
    ], {
        placeholder: "Select a country",
    });
});
selectNamespaceExample.toIR().compile([])();

// ============================================================================
// SLIDER
// ============================================================================

// File: src/forms/slider/index.ts
// Export: createSlider (private function)
const sliderExample = East.function([], UIComponentType, $ => {
    return Slider.Root(50.0, {
        min: 0,
        max: 100,
        step: 5,
        colorPalette: "blue",
    });
});
sliderExample.toIR().compile([])();

// File: src/forms/slider/index.ts
// Export: Slider namespace
const sliderNamespaceExample = East.function([], UIComponentType, $ => {
    return Slider.Root(50.0, {
        min: 0,
        max: 100,
        step: 1,
        colorPalette: "blue",
    });
});
sliderNamespaceExample.toIR().compile([])();

// File: src/forms/slider/types.ts
// Export: SliderVariant
const sliderVariantExample = East.function([], UIComponentType, $ => {
    return Slider.Root(50.0, {
        variant: Slider.Variant("subtle"),
    });
});
sliderVariantExample.toIR().compile([])();

// ============================================================================
// CHECKBOX
// ============================================================================

// File: src/forms/checkbox/index.ts
// Export: createCheckbox (private function)
const checkboxExample = East.function([], UIComponentType, $ => {
    return Checkbox.Root(true, {
        label: "Enable notifications",
        colorPalette: "blue",
        size: "md",
    });
});
checkboxExample.toIR().compile([])();

// File: src/forms/checkbox/index.ts
// Export: Checkbox.Root
const checkboxRootExample = East.function([], UIComponentType, $ => {
    return Checkbox.Root(true, {
        label: "Enable notifications",
        colorPalette: "blue",
        size: "md",
    });
});
checkboxRootExample.toIR().compile([])();

// ============================================================================
// FIELD
// ============================================================================

// File: src/forms/field/index.ts
// Export: createField (private function)
const fieldExample = East.function([], UIComponentType, $ => {
    return Field.StringInput(
        "Email",
        "",
        { placeholder: "Enter email", helperText: "We'll never share your email" }
    );
});
fieldExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.StringInput (createStringInputField)
const fieldStringInputExample = East.function([], UIComponentType, $ => {
    return Field.StringInput("Email", "", {
        placeholder: "Enter email",
        helperText: "We'll never share your email",
    });
});
fieldStringInputExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.Checkbox (createCheckboxField)
const fieldCheckboxExample = East.function([], UIComponentType, $ => {
    return Field.Checkbox(
        "Accept terms",
        false,
        { helperText: "You must accept to continue" }
    );
});
fieldCheckboxExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.FileUpload (createFileUploadField)
const fieldFileUploadExample = East.function([], UIComponentType, $ => {
    return Field.FileUpload("Documents", {
        accept: "application/pdf",
        helperText: "Upload PDF files only",
    });
});
fieldFileUploadExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.Select (createSelectField)
const fieldSelectExample = East.function([], UIComponentType, $ => {
    return Field.Select("Country", "", [
        Select.Item("us", "United States"),
        Select.Item("uk", "United Kingdom"),
    ], { helperText: "Select your country" });
});
fieldSelectExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.DateTimeInput (createDatetimeInputField)
const fieldDateTimeInputExample = East.function([], UIComponentType, $ => {
    return Field.DateTimeInput("Birth Date", new Date(), {
        helperText: "Enter your date of birth",
    });
});
fieldDateTimeInputExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.FloatInput (createFloatInputField)
const fieldFloatInputExample = East.function([], UIComponentType, $ => {
    return Field.FloatInput("Price", 0.0, {
        min: 0,
        helperText: "Enter price in dollars",
    });
});
fieldFloatInputExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.IntegerInput (createIntegerInputField)
const fieldIntegerInputExample = East.function([], UIComponentType, $ => {
    return Field.IntegerInput("Quantity", 1n, {
        min: 1n,
        max: 100n,
        helperText: "Enter quantity",
    });
});
fieldIntegerInputExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.Slider (createSliderField)
const fieldSliderExample = East.function([], UIComponentType, $ => {
    return Field.Slider("Volume", 50.0, {
        min: 0,
        max: 100,
        helperText: "Adjust volume level",
    });
});
fieldSliderExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.Switch (createSwitch)
const fieldSwitchExample = East.function([], UIComponentType, $ => {
    return Field.Switch("Enable notifications", true, {
        helperText: "Toggle to enable or disable",
    });
});
fieldSwitchExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.TagsInput (createTags)
const fieldTagsInputExample = East.function([], UIComponentType, $ => {
    return Field.TagsInput("Skills", ["TypeScript", "React"], {
        helperText: "Add your skills",
    });
});
fieldTagsInputExample.toIR().compile([])();

// File: src/forms/field/index.ts
// Export: Field.Textarea (createTextareaField)
const fieldTextareaExample = East.function([], UIComponentType, $ => {
    return Field.Textarea("Description", "", {
        placeholder: "Enter description",
        rows: 4,
        helperText: "Maximum 500 characters",
    });
});
fieldTextareaExample.toIR().compile([])();

// ============================================================================
// FILE UPLOAD
// ============================================================================

// File: src/forms/file-upload/index.ts
// Export: createFileUpload (private function)
const fileUploadExample = East.function([], UIComponentType, $ => {
    return FileUpload.Root({
        accept: "image/*",
        maxFiles: 5n,
    });
});
fileUploadExample.toIR().compile([])();

// File: src/forms/file-upload/index.ts
// Export: FileUpload.Root
const fileUploadRootExample = East.function([], UIComponentType, $ => {
    return FileUpload.Root({
        accept: "image/*",
        maxFiles: 5n,
    });
});
fileUploadRootExample.toIR().compile([])();

// File: src/forms/file-upload/index.ts
// Export: FileUpload.Root (with all options)
const fileUploadFullExample = East.function([], UIComponentType, $ => {
    return FileUpload.Root({
        accept: "image/*",
        maxFiles: 3n,
        maxFileSize: 10n * 1024n * 1024n, // 10MB
        label: "Upload images",
        dropzoneText: "Drag images here",
        triggerText: "Browse",
    });
});
fileUploadFullExample.toIR().compile([])();

// File: src/forms/file-upload/index.ts
// Export: FileUpload.Root (mobile camera capture)
const fileUploadCaptureExample = East.function([], UIComponentType, $ => {
    return FileUpload.Root({
        accept: "image/*",
        capture: "environment",
        label: "Take photo",
    });
});
fileUploadCaptureExample.toIR().compile([])();

// ============================================================================
// TAGS-INPUT
// ============================================================================

// File: src/forms/tags-input/index.ts
// Export: createTagsInput_ (private function)
const tagsInputExample = East.function([], UIComponentType, $ => {
    return TagsInput.Root(["React", "TypeScript"], {
        placeholder: "Add tag...",
        max: 5n,
        colorPalette: "blue",
    });
});
tagsInputExample.toIR().compile([])();

// File: src/forms/tags-input/index.ts
// Export: TagsInput.Root
const tagsInputRootExample = East.function([], UIComponentType, $ => {
    return TagsInput.Root(["React", "TypeScript"], {
        placeholder: "Add tag...",
        max: 5n,
    });
});
tagsInputRootExample.toIR().compile([])();

// File: src/forms/tags-input/index.ts
// Export: TagsInput.Root (with callback)
const tagsInputCallbackExample = East.function([], UIComponentType, $ => {
    return TagsInput.Root(["initial"], {
        placeholder: "Add skill...",
        onChange: ($, _newTags) => {
            // Callback receives new array of tags
            $.return(null);
        },
    });
});
tagsInputCallbackExample.toIR().compile([])();

// ============================================================================
// TEXTAREA
// ============================================================================

// File: src/forms/textarea/index.ts
// Export: createTextarea_ (private function)
const textareaExample = East.function([], UIComponentType, $ => {
    return Textarea.Root("", {
        placeholder: "Enter description...",
        rows: 4n,
        maxLength: 500n,
    });
});
textareaExample.toIR().compile([])();

// File: src/forms/textarea/index.ts
// Export: Textarea.Root
const textareaRootExample = East.function([], UIComponentType, $ => {
    return Textarea.Root("Hello world", {
        placeholder: "Enter description",
        rows: 4n,
    });
});
textareaRootExample.toIR().compile([])();

// File: src/forms/textarea/index.ts
// Export: Textarea.Root (with callback)
const textareaCallbackExample = East.function([], UIComponentType, $ => {
    return Textarea.Root("", {
        placeholder: "Type here...",
        rows: 3n,
        onChange: ($, _newValue) => {
            // Callback receives new text value
            $.return(null);
        },
    });
});
textareaCallbackExample.toIR().compile([])();

// ============================================================================
// SWITCH
// ============================================================================

// File: src/forms/switch/index.ts
// Export: createSwitch_ (private function)
const switchExample = East.function([], UIComponentType, $ => {
    return Switch.Root(true, {
        label: "Dark mode",
        colorPalette: "blue",
        size: "md",
    });
});
switchExample.toIR().compile([])();

// File: src/forms/switch/index.ts
// Export: Switch.Root
const switchRootExample = East.function([], UIComponentType, $ => {
    return Switch.Root(true, {
        label: "Dark mode",
        colorPalette: "blue",
    });
});
switchRootExample.toIR().compile([])();

// File: src/forms/switch/index.ts
// Export: Switch.Root (with callback)
const switchCallbackExample = East.function([], UIComponentType, $ => {
    return Switch.Root(false, {
        label: "Enable notifications",
        colorPalette: "green",
        onChange: ($, _newValue) => {
            // Callback receives new checked value
            $.return(null);
        },
    });
});
switchCallbackExample.toIR().compile([])();

console.log("Forms TypeDoc examples compiled and executed successfully!");
