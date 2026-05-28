/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Avatar, Style } from "../../src/index.js";

describeEast("Avatar", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates empty avatar", $ => {
        const avatar = $.let(Avatar.Root());

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").src.hasTag("none"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").name.hasTag("none"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.hasTag("none"), true));
    });

    test("creates avatar with src", $ => {
        const avatar = $.let(Avatar.Root({
            src: "https://example.com/avatar.jpg",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").src.hasTag("some"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").src.unwrap("some"), "https://example.com/avatar.jpg"));
    });

    test("creates avatar with name", $ => {
        const avatar = $.let(Avatar.Root({
            name: "John Doe",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").name.hasTag("some"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").name.unwrap("some"), "John Doe"));
    });

    test("creates avatar with src and name", $ => {
        const avatar = $.let(Avatar.Root({
            src: "https://example.com/john.jpg",
            name: "John Doe",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").src.unwrap("some"), "https://example.com/john.jpg"));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").name.unwrap("some"), "John Doe"));
    });

    // =========================================================================
    // Size
    // =========================================================================

    test("creates extra small avatar", $ => {
        const avatar = $.let(Avatar.Root({
            size: "xs",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.hasTag("some"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("xs"), true));
    });

    test("creates small avatar", $ => {
        const avatar = $.let(Avatar.Root({
            size: "sm",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates medium avatar", $ => {
        const avatar = $.let(Avatar.Root({
            size: "md",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("md"), true));
    });

    test("creates large avatar", $ => {
        const avatar = $.let(Avatar.Root({
            size: "lg",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("lg"), true));
    });

    test("creates avatar with Size helper", $ => {
        const avatar = $.let(Avatar.Root({
            size: "lg",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("lg"), true));
    });

    // =========================================================================
    // Variant
    // =========================================================================

    test("creates solid variant avatar", $ => {
        const avatar = $.let(Avatar.Root({
            variant: "solid",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").variant.hasTag("some"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates subtle variant avatar", $ => {
        const avatar = $.let(Avatar.Root({
            variant: "subtle",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates outline variant avatar", $ => {
        const avatar = $.let(Avatar.Root({
            variant: "outline",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").variant.unwrap("some").hasTag("outline"), true));
    });

    test("creates avatar with Style.StyleVariant helper", $ => {
        const avatar = $.let(Avatar.Root({
            variant: Style.StyleVariant("solid"),
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").variant.unwrap("some").hasTag("solid"), true));
    });

    // =========================================================================
    // Color Palette
    // =========================================================================

    test("creates avatar with blue color palette", $ => {
        const avatar = $.let(Avatar.Root({
            colorPalette: "blue",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").colorPalette.hasTag("some"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").colorPalette.unwrap("some").hasTag("blue"), true));
    });

    test("creates avatar with purple color palette", $ => {
        const avatar = $.let(Avatar.Root({
            colorPalette: "purple",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    test("creates avatar with Style.ColorScheme helper", $ => {
        const avatar = $.let(Avatar.Root({
            colorPalette: Style.ColorScheme("green"),
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").colorPalette.unwrap("some").hasTag("green"), true));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates avatar with all options", $ => {
        const avatar = $.let(Avatar.Root({
            src: "https://example.com/profile.jpg",
            name: "Alice Smith",
            size: "lg",
            variant: "solid",
            colorPalette: "purple",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").src.unwrap("some"), "https://example.com/profile.jpg"));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").name.unwrap("some"), "Alice Smith"));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("lg"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").variant.unwrap("some").hasTag("solid"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").colorPalette.unwrap("some").hasTag("purple"), true));
    });

    test("creates user profile avatar", $ => {
        const avatar = $.let(Avatar.Root({
            src: "https://api.example.com/users/123/avatar",
            name: "Jane Wilson",
            size: "md",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").name.unwrap("some"), "Jane Wilson"));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("md"), true));
    });

    test("creates initials avatar", $ => {
        const avatar = $.let(Avatar.Root({
            name: "Bob Johnson",
            colorPalette: "blue",
            variant: "solid",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").src.hasTag("none"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").name.unwrap("some"), "Bob Johnson"));
    });

    test("creates small team member avatar", $ => {
        const avatar = $.let(Avatar.Root({
            name: "Team Member",
            size: "sm",
            colorPalette: "teal",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("sm"), true));
        $(Assert.equal(avatar.unwrap().unwrap("Avatar").colorPalette.unwrap("some").hasTag("teal"), true));
    });

    test("creates large profile header avatar", $ => {
        const avatar = $.let(Avatar.Root({
            src: "https://example.com/large-avatar.jpg",
            name: "Profile User",
            size: "lg",
        }));

        $(Assert.equal(avatar.unwrap().unwrap("Avatar").size.unwrap("some").hasTag("lg"), true));
    });
}, {   platformFns: TestImpl,});
