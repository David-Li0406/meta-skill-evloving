/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Card, Text, Heading, Button, Stack, Style } from "../../src/index.js";

describeEast("Card", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates empty card", $ => {
        const card = $.let(Card.Root([]));

        $(Assert.equal(card.unwrap().unwrap("Card").header.hasTag("none"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").footer.hasTag("none"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.hasTag("none"), true));
    });

    test("creates card with text child", $ => {
        const card = $.let(Card.Root([
            Text.Root("Card content here"),
        ]));

        // body is an array of components
        $(Assert.equal(card.unwrap().unwrap("Card").header.hasTag("none"), true));
    });

    test("creates card with header", $ => {
        const card = $.let(Card.Root([], {
            header: Heading.Root("Card Title"),
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").header.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").header.unwrap("some").unwrap().unwrap("Heading").value, "Card Title"));
    });

    test("creates card with header and footer", $ => {
        const card = $.let(Card.Root([], {
            header: Heading.Root("Product Name"),
            footer: Button.Root("Buy Now"),
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").header.unwrap("some").unwrap().unwrap("Heading").value, "Product Name"));
        $(Assert.equal(card.unwrap().unwrap("Card").footer.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").footer.unwrap("some").unwrap().unwrap("Button").label, "Buy Now"));
    });

    // =========================================================================
    // Complex Header/Footer
    // =========================================================================

    test("creates card with VStack header", $ => {
        const card = $.let(Card.Root([
            Text.Root("Body content"),
        ], {
            header: Stack.VStack([
                Heading.Root("Title"),
                Text.Root("Description"),
            ]),
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").header.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").header.unwrap("some").unwrap().hasTag("Stack"), true));
    });

    test("creates card with HStack footer", $ => {
        const card = $.let(Card.Root([
            Text.Root("Body content"),
        ], {
            footer: Stack.HStack([
                Button.Root("Cancel", { variant: "outline" }),
                Button.Root("Save"),
            ]),
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").footer.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").footer.unwrap("some").unwrap().hasTag("Stack"), true));
    });

    // =========================================================================
    // Variant
    // =========================================================================

    test("creates elevated card", $ => {
        const card = $.let(Card.Root([], {
            variant: "elevated",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.unwrap("some").hasTag("elevated"), true));
    });

    test("creates outline card", $ => {
        const card = $.let(Card.Root([], {
            variant: "outline",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates subtle card", $ => {
        const card = $.let(Card.Root([], {
            variant: "subtle",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates card with CardVariant helper", $ => {
        const card = $.let(Card.Root([], {
            variant: Card.Variant("elevated"),
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.unwrap("some").hasTag("elevated"), true));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates small card", $ => {
        const card = $.let(Card.Root([], {
            size: "sm",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").size.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium card", $ => {
        const card = $.let(Card.Root([], {
            size: "md",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large card", $ => {
        const card = $.let(Card.Root([], {
            size: "lg",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates card with Style.Size helper", $ => {
        const card = $.let(Card.Root([], {
            size: Style.Size("md"),
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").size.unwrap("some").hasTag("md"), true));
    });

    // =========================================================================
    // Dimension Properties
    // =========================================================================

    test("creates card with height", $ => {
        const card = $.let(Card.Root([], {
            height: "400px",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").height.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").height.unwrap("some"), "400px"));
    });

    test("creates card with minHeight", $ => {
        const card = $.let(Card.Root([], {
            minHeight: "200px",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").minHeight.unwrap("some"), "200px"));
    });

    test("creates card with maxHeight", $ => {
        const card = $.let(Card.Root([], {
            maxHeight: "600px",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").maxHeight.unwrap("some"), "600px"));
    });

    test("creates card with width", $ => {
        const card = $.let(Card.Root([], {
            width: "300px",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").width.unwrap("some"), "300px"));
    });

    test("creates card with flex", $ => {
        const card = $.let(Card.Root([], {
            flex: "1",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").flex.unwrap("some"), "1"));
    });

    test("creates card with full height", $ => {
        const card = $.let(Card.Root([], {
            height: "100%",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").height.unwrap("some"), "100%"));
    });

    test("creates card with overflow", $ => {
        const card = $.let(Card.Root([], {
            overflow: "auto",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").overflow.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").overflow.unwrap("some").hasTag("auto"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates card with all options", $ => {
        const card = $.let(Card.Root([
            Text.Root("Main content goes here"),
        ], {
            header: Heading.Root("Full Card"),
            footer: Button.Root("Action"),
            variant: "elevated",
            size: "md",
            height: "400px",
            minHeight: "200px",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").header.unwrap("some").unwrap().unwrap("Heading").value, "Full Card"));
        $(Assert.equal(card.unwrap().unwrap("Card").footer.unwrap("some").unwrap().unwrap("Button").label, "Action"));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.unwrap("some").hasTag("elevated"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").size.unwrap("some").hasTag("md"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").height.unwrap("some"), "400px"));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").minHeight.unwrap("some"), "200px"));
    });

    test("creates product card", $ => {
        const card = $.let(Card.Root([
            Text.Root("$99.99"),
        ], {
            header: Stack.VStack([
                Heading.Root("Product Name"),
                Text.Root("Product category"),
            ]),
            footer: Button.Root("Add to Cart"),
            variant: "outline",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").header.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").footer.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates user profile card", $ => {
        const card = $.let(Card.Root([
            Text.Root("San Francisco, CA"),
        ], {
            header: Stack.VStack([
                Heading.Root("John Doe"),
                Text.Root("Software Engineer"),
            ]),
            variant: "elevated",
            size: "sm",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").header.hasTag("some"), true));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.unwrap("some").hasTag("elevated"), true));
    });

    test("creates info card", $ => {
        const card = $.let(Card.Root([
            Text.Root("Important details displayed here in the card body."),
        ], {
            header: Heading.Root("Information"),
            variant: "subtle",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").header.unwrap("some").unwrap().unwrap("Heading").value, "Information"));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates card with nested components", $ => {
        const card = $.let(Card.Root([
            Text.Root("First line"),
            Text.Root("Second line"),
        ], {
            header: Heading.Root("Multi-content Card"),
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").header.unwrap("some").unwrap().unwrap("Heading").value, "Multi-content Card"));
    });

    test("creates flexible card that fills container", $ => {
        const card = $.let(Card.Root([
            Text.Root("This card fills available space"),
        ], {
            header: Heading.Root("Flexible Card"),
            height: "100%",
            flex: "1",
            overflow: "auto",
        }));

        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").height.unwrap("some"), "100%"));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").flex.unwrap("some"), "1"));
        $(Assert.equal(card.unwrap().unwrap("Card").style.unwrap("some").overflow.unwrap("some").hasTag("auto"), true));
    });
}, {   platformFns: TestImpl,});
