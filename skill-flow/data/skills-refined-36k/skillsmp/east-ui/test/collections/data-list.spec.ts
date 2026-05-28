/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { DataList } from "../../src/index.js";

describeEast("DataList", (test) => {
    // =========================================================================
    // DataList.Item
    // =========================================================================

    test("creates item with string label and value", $ => {
        const item = $.let(DataList.Item("Status", "Active"));

        $(Assert.equal(item.label, "Status"));
        $(Assert.equal(item.value, "Active"));
    });

    test("creates item with expression label and value", $ => {
        const item = $.let(DataList.Item(
            "Name",
            "John Doe"
        ));

        $(Assert.equal(item.label, "Name"));
        $(Assert.equal(item.value, "John Doe"));
    });

    test("creates item with mixed string and expression", $ => {
        const item = $.let(DataList.Item(
            "Role",
            "Administrator"
        ));

        $(Assert.equal(item.label, "Role"));
        $(Assert.equal(item.value, "Administrator"));
    });

    // =========================================================================
    // DataList.Root - Basic Creation
    // =========================================================================

    test("creates data list with items", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Name", "Alice"),
            DataList.Item("Email", "alice@example.com"),
        ]));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.hasTag("none"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").size.hasTag("none"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").variant.hasTag("none"), true));
    });

    test("creates data list with single item", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Status", "Active"),
        ]));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.hasTag("none"), true));
    });

    test("creates empty data list", $ => {
        const list = $.let(DataList.Root([]));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.hasTag("none"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").size.hasTag("none"), true));
    });

    // =========================================================================
    // DataList.Root - Orientation
    // =========================================================================

    test("creates horizontal data list", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Name", "Bob"),
        ], {
            orientation: "horizontal",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.hasTag("some"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.unwrap("some").hasTag("horizontal"), true));
    });

    test("creates vertical data list", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Status", "Active"),
        ], {
            orientation: "vertical",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.unwrap("some").hasTag("vertical"), true));
    });

    // =========================================================================
    // DataList.Root - Size
    // =========================================================================

    test("creates data list with sm size", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Label", "Value"),
        ], {
            size: "sm",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates data list with md size", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Label", "Value"),
        ], {
            size: "md",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").size.unwrap("some").hasTag("md"), true));
    });

    test("creates data list with lg size", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Label", "Value"),
        ], {
            size: "lg",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").size.unwrap("some").hasTag("lg"), true));
    });

    // =========================================================================
    // DataList.Root - Variant
    // =========================================================================

    test("creates data list with subtle variant", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Label", "Value"),
        ], {
            variant: "subtle",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").variant.hasTag("some"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates data list with bold variant", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Label", "Value"),
        ], {
            variant: "bold",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").variant.unwrap("some").hasTag("bold"), true));
    });

    test("creates data list with DataListVariant helper", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Label", "Value"),
        ], {
            variant: "bold",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").variant.unwrap("some").hasTag("bold"), true));
    });

    // =========================================================================
    // DataList.Root - Combined Options
    // =========================================================================

    test("creates data list with all options", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Name", "Alice"),
            DataList.Item("Role", "Admin"),
        ], {
            orientation: "horizontal",
            size: "md",
            variant: "bold",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.unwrap("some").hasTag("horizontal"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").variant.unwrap("some").hasTag("bold"), true));
    });

    test("creates user details data list", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Username", "alice_smith"),
            DataList.Item("Email", "alice@example.com"),
            DataList.Item("Status", "Active"),
            DataList.Item("Role", "Administrator"),
        ], {
            orientation: "vertical",
            variant: "subtle",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.unwrap("some").hasTag("vertical"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates product info data list", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("SKU", "PRD-12345"),
            DataList.Item("Price", "$99.99"),
            DataList.Item("Stock", "In Stock"),
        ], {
            size: "sm",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates order summary data list", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Order ID", "#ORD-2024-001"),
            DataList.Item("Date", "Dec 15, 2024"),
            DataList.Item("Total", "$245.00"),
            DataList.Item("Status", "Shipped"),
        ], {
            orientation: "horizontal",
            size: "lg",
            variant: "bold",
        }));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.unwrap("some").hasTag("horizontal"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").size.unwrap("some").hasTag("lg"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").variant.unwrap("some").hasTag("bold"), true));
    });

    test("creates metadata data list", $ => {
        const list = $.let(DataList.Root([
            DataList.Item("Created", "Jan 1, 2024"),
            DataList.Item("Modified", "Dec 20, 2024"),
            DataList.Item("Version", "1.2.3"),
        ]));

        $(Assert.equal(list.unwrap().unwrap("DataList").orientation.hasTag("none"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").size.hasTag("none"), true));
        $(Assert.equal(list.unwrap().unwrap("DataList").variant.hasTag("none"), true));
    });
}, {   platformFns: TestImpl,});
