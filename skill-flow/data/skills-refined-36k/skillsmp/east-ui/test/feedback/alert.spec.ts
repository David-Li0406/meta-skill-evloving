/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Alert } from "../../src/index.js";

describeEast("Alert", (test) => {
    // =========================================================================
    // Basic Creation with Status
    // =========================================================================

    test("creates info alert", $ => {
        const alert = $.let(Alert.Root("info"));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("info"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").title.hasTag("none"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").description.hasTag("none"), true));
    });

    test("creates warning alert", $ => {
        const alert = $.let(Alert.Root("warning"));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("warning"), true));
    });

    test("creates success alert", $ => {
        const alert = $.let(Alert.Root("success"));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("success"), true));
    });

    test("creates error alert", $ => {
        const alert = $.let(Alert.Root("error"));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("error"), true));
    });

    // =========================================================================
    // String Status Shorthand
    // =========================================================================

    test("creates info alert with string status", $ => {
        const alert = $.let(Alert.Root("info"));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("info"), true));
    });

    test("creates warning alert with string status", $ => {
        const alert = $.let(Alert.Root("warning"));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("warning"), true));
    });

    test("creates success alert with string status", $ => {
        const alert = $.let(Alert.Root("success"));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("success"), true));
    });

    test("creates error alert with string status", $ => {
        const alert = $.let(Alert.Root("error"));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("error"), true));
    });

    // =========================================================================
    // Title
    // =========================================================================

    test("creates alert with title", $ => {
        const alert = $.let(Alert.Root("success", {
            title: "Success!",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").title.hasTag("some"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").title.unwrap("some"), "Success!"));
    });

    test("creates alert with long title", $ => {
        const alert = $.let(Alert.Root("info", {
            title: "Important Information About Your Account",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").title.unwrap("some"), "Important Information About Your Account"));
    });

    // =========================================================================
    // Description
    // =========================================================================

    test("creates alert with description", $ => {
        const alert = $.let(Alert.Root("warning", {
            description: "Your session will expire soon.",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").description.hasTag("some"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").description.unwrap("some"), "Your session will expire soon."));
    });

    test("creates alert with title and description", $ => {
        const alert = $.let(Alert.Root("error", {
            title: "Error",
            description: "Failed to save changes. Please try again.",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").title.unwrap("some"), "Error"));
        $(Assert.equal(alert.unwrap().unwrap("Alert").description.unwrap("some"), "Failed to save changes. Please try again."));
    });

    // =========================================================================
    // Variant
    // =========================================================================

    test("creates solid variant alert", $ => {
        const alert = $.let(Alert.Root("success", {
            variant: "solid",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.hasTag("some"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates subtle variant alert", $ => {
        const alert = $.let(Alert.Root("info", {
            variant: "subtle",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates outline variant alert", $ => {
        const alert = $.let(Alert.Root("warning", {
            variant: "outline",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates alert with AlertVariant helper", $ => {
        const alert = $.let(Alert.Root("error", {
            variant: "solid",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.unwrap("some").hasTag("solid"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates alert with all options", $ => {
        const alert = $.let(Alert.Root("success", {
            title: "Changes Saved",
            description: "Your changes have been saved successfully.",
            variant: "subtle",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("success"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").title.unwrap("some"), "Changes Saved"));
        $(Assert.equal(alert.unwrap().unwrap("Alert").description.unwrap("some"), "Your changes have been saved successfully."));
        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates form submission success alert", $ => {
        const alert = $.let(Alert.Root("success", {
            title: "Form Submitted",
            description: "Thank you for your submission.",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("success"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").title.unwrap("some"), "Form Submitted"));
    });

    test("creates validation error alert", $ => {
        const alert = $.let(Alert.Root("error", {
            title: "Validation Error",
            description: "Please check the highlighted fields.",
            variant: "solid",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("error"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates update notification alert", $ => {
        const alert = $.let(Alert.Root("info", {
            title: "New Update Available",
            description: "Version 2.0 is now available. Click to update.",
            variant: "subtle",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("info"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates session expiry warning alert", $ => {
        const alert = $.let(Alert.Root("warning", {
            title: "Session Expiring",
            description: "Your session will expire in 5 minutes.",
            variant: "outline",
        }));

        $(Assert.equal(alert.unwrap().unwrap("Alert").status.hasTag("warning"), true));
        $(Assert.equal(alert.unwrap().unwrap("Alert").variant.unwrap("some").hasTag("outline"), true));
    });
}, {   platformFns: TestImpl,});
