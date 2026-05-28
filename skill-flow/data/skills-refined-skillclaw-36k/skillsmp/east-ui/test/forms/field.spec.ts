/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Field } from "../../src/index.js";

describeEast("Field", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates field with label and control", $ => {
        const field = $.let(Field.StringInput(
            "Email",
            "",
            { placeholder: "you@example.com" }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").label, "Email"));
        $(Assert.equal(field.unwrap().unwrap("Field").helperText.hasTag("none"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").errorText.hasTag("none"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").required.hasTag("none"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").disabled.hasTag("none"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").readOnly.hasTag("none"), true));
    });

    test("creates field with checkbox control", $ => {
        const field = $.let(Field.Checkbox(
            "Accept Terms",
            false
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").label, "Accept Terms"));
        // Verify control is a Checkbox
        $(Assert.equal(field.unwrap().unwrap("Field").control.hasTag("Checkbox"), true));
    });

    // =========================================================================
    // Helper Text
    // =========================================================================

    test("creates field with helper text", $ => {
        const field = $.let(Field.StringInput(
            "Email",
            "",
            { placeholder: "you@example.com", helperText: "We'll never share your email." }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").helperText.hasTag("some"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").helperText.unwrap("some"), "We'll never share your email."));
    });

    test("creates field with long helper text", $ => {
        const field = $.let(Field.StringInput(
            "Password",
            "",
            { helperText: "Must be at least 8 characters with one uppercase, one lowercase, and one number." }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").helperText.unwrap("some"), "Must be at least 8 characters with one uppercase, one lowercase, and one number."));
    });

    // =========================================================================
    // Error Text
    // =========================================================================

    test("creates field with error text", $ => {
        const field = $.let(Field.StringInput(
            "Email",
            "",
            { errorText: "Email is required" }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").errorText.hasTag("some"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").errorText.unwrap("some"), "Email is required"));
    });

    // =========================================================================
    // Required State
    // =========================================================================

    test("creates required field", $ => {
        const field = $.let(Field.StringInput(
            "Username",
            "",
            { placeholder: "Enter username", required: true }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").required.hasTag("some"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").required.unwrap("some"), true));
    });

    test("creates non-required field explicitly", $ => {
        const field = $.let(Field.StringInput(
            "Middle Name",
            "",
            { required: false }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").required.unwrap("some"), false));
    });

    // =========================================================================
    // Disabled State
    // =========================================================================

    test("creates disabled field", $ => {
        const field = $.let(Field.StringInput(
            "Email",
            "",
            { disabled: true }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").disabled.hasTag("some"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").disabled.unwrap("some"), true));
    });

    test("creates enabled field explicitly", $ => {
        const field = $.let(Field.StringInput(
            "Email",
            "",
            { disabled: false }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").disabled.unwrap("some"), false));
    });

    // =========================================================================
    // ReadOnly State
    // =========================================================================

    test("creates read-only field", $ => {
        const field = $.let(Field.StringInput(
            "Account ID",
            "",
            { readOnly: true }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").readOnly.hasTag("some"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").readOnly.unwrap("some"), true));
    });

    test("creates editable field explicitly", $ => {
        const field = $.let(Field.StringInput(
            "Email",
            "",
            { readOnly: false }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").readOnly.unwrap("some"), false));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates field with all options", $ => {
        const field = $.let(Field.StringInput(
            "Password",
            "",
            {
                placeholder: "Enter password",
                helperText: "Must be at least 8 characters",
                errorText: "Password is too short",
                required: true,
                disabled: false,
                readOnly: false,
            }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").label, "Password"));
        $(Assert.equal(field.unwrap().unwrap("Field").helperText.unwrap("some"), "Must be at least 8 characters"));
        $(Assert.equal(field.unwrap().unwrap("Field").errorText.unwrap("some"), "Password is too short"));
        $(Assert.equal(field.unwrap().unwrap("Field").required.unwrap("some"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").disabled.unwrap("some"), false));
        $(Assert.equal(field.unwrap().unwrap("Field").readOnly.unwrap("some"), false));
    });

    test("creates email field with validation", $ => {
        const field = $.let(Field.StringInput(
            "Email Address",
            "",
            {
                placeholder: "user@company.com",
                helperText: "Enter your work email",
                required: true,
            }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").label, "Email Address"));
        $(Assert.equal(field.unwrap().unwrap("Field").helperText.unwrap("some"), "Enter your work email"));
        $(Assert.equal(field.unwrap().unwrap("Field").required.unwrap("some"), true));
    });

    test("creates read-only display field", $ => {
        const field = $.let(Field.StringInput(
            "User ID",
            "",
            {
                readOnly: true,
                helperText: "This value cannot be changed",
            }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").readOnly.unwrap("some"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").helperText.unwrap("some"), "This value cannot be changed"));
    });

    test("creates disabled field with explanation", $ => {
        const field = $.let(Field.Checkbox(
            "Premium Feature",
            false,
            {
                disabled: true,
                helperText: "Upgrade to enable this feature",
            }
        ));

        $(Assert.equal(field.unwrap().unwrap("Field").disabled.unwrap("some"), true));
        $(Assert.equal(field.unwrap().unwrap("Field").helperText.unwrap("some"), "Upgrade to enable this feature"));
        $(Assert.equal(field.unwrap().unwrap("Field").control.hasTag("Checkbox"), true));
    });
}, {   platformFns: TestImpl,});
