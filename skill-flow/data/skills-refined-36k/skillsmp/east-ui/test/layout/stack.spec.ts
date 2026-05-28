/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Stack, Text, Style } from "../../src/index.js";

describeEast("Stack", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates stack with empty children", $ => {
        const stack = $.let(Stack.Root([]));

        $(Assert.equal(stack.unwrap().unwrap("Stack").children.size(), 0n));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.hasTag("none"), true));
    });

    test("creates stack with single text child", $ => {
        const textChild = Text.Root("Hello");
        const stack = $.let(Stack.Root([textChild]));

        $(Assert.equal(stack.unwrap().unwrap("Stack").children.size(), 1n));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.hasTag("none"), true));
    });

    test("creates stack with multiple text children", $ => {
        const child1 = Text.Root("First");
        const child2 = Text.Root("Second");
        const child3 = Text.Root("Third");
        const stack = $.let(Stack.Root([
            child1,
            child2,
            child3,
        ]));

        $(Assert.equal(stack.unwrap().unwrap("Stack").children.size(), 3n));
    });

    // =========================================================================
    // Style Properties - Individual
    // =========================================================================

    test("creates stack with direction", $ => {
        const stack = $.let(Stack.Root([], {
            direction: Style.FlexDirection("row"),
        }));

        $(Assert.equal(stack.unwrap().unwrap("Stack").style.hasTag("some"), true));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").direction.hasTag("some"), true));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("row"), true));
    });

    test("creates stack with gap", $ => {
        const stack = $.let(Stack.Root([], {
            gap: "4",
        }));

        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").gap.hasTag("some"), true));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").gap.unwrap("some"), "4"));
    });

    test("creates stack with align", $ => {
        const stack = $.let(Stack.Root([], {
            align: Style.AlignItems("center"),
        }));

        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").align.hasTag("some"), true));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").align.unwrap("some").hasTag("center"), true));
    });

    test("creates stack with justify", $ => {
        const stack = $.let(Stack.Root([], {
            justify: Style.JustifyContent("space-between"),
        }));

        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").justify.hasTag("some"), true));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").justify.unwrap("some").hasTag("space-between"), true));
    });

    test("creates stack with wrap", $ => {
        const stack = $.let(Stack.Root([], {
            wrap: Style.FlexWrap("wrap"),
        }));

        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").wrap.hasTag("some"), true));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").wrap.unwrap("some").hasTag("wrap"), true));
    });

    test("creates stack with padding", $ => {
        const stack = $.let(Stack.Root([], {
            padding: Stack.Padding({ top: "4", right: "4", bottom: "4", left: "4" }),
        }));

        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").padding.hasTag("some"), true));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").padding.unwrap("some").top.unwrap("some"), "4"));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").padding.unwrap("some").right.unwrap("some"), "4"));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").padding.unwrap("some").bottom.unwrap("some"), "4"));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").padding.unwrap("some").left.unwrap("some"), "4"));
    });

    test("creates stack with background", $ => {
        const stack = $.let(Stack.Root([], {
            background: "gray.100",
        }));

        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").background.hasTag("some"), true));
        $(Assert.equal(stack.unwrap().unwrap("Stack").style.unwrap("some").background.unwrap("some"), "gray.100"));
    });

    // =========================================================================
    // No Style - Defaults to None
    // =========================================================================

    test("creates stack with no style - style option is none", $ => {
        const stack = $.let(Stack.Root([]));

        $(Assert.equal(stack.unwrap().unwrap("Stack").style.hasTag("none"), true));
    });

    // =========================================================================
    // Multiple Style Properties
    // =========================================================================

    test("creates stack with multiple styles", $ => {
        const stack = $.let(Stack.Root([], {
            direction: 'row',
            gap: "4",
            align: 'center',
            justify: 'space-between',
            padding: "2",
            background: "gray.50",
        }));

        const style = stack.unwrap().unwrap("Stack").style.unwrap("some");
        $(Assert.equal(style.direction.unwrap("some").hasTag("row"), true));
        $(Assert.equal(style.gap.unwrap("some"), "4"));
        $(Assert.equal(style.align.unwrap("some").hasTag("center"), true));
        $(Assert.equal(style.justify.unwrap("some").hasTag("space-between"), true));
        $(Assert.equal(style.padding.unwrap("some").top.unwrap("some"), "2"));
        $(Assert.equal(style.background.unwrap("some"), "gray.50"));
        // Other styles should be none
        $(Assert.equal(style.wrap.hasTag("none"), true));
        $(Assert.equal(style.margin.hasTag("none"), true));
    });

    // =========================================================================
    // All Flex Directions
    // =========================================================================

    test("supports all flex directions", $ => {
        const row = $.let(Stack.Root([], { direction: Style.FlexDirection("row") }));
        const column = $.let(Stack.Root([], { direction: Style.FlexDirection("column") }));
        const rowReverse = $.let(Stack.Root([], { direction: Style.FlexDirection("row-reverse") }));
        const columnReverse = $.let(Stack.Root([], { direction: Style.FlexDirection("column-reverse") }));

        $(Assert.equal(row.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("row"), true));
        $(Assert.equal(column.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("column"), true));
        $(Assert.equal(rowReverse.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("row-reverse"), true));
        $(Assert.equal(columnReverse.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("column-reverse"), true));
    });

    // =========================================================================
    // All Flex Wrap Options
    // =========================================================================

    test("supports all flex wrap options", $ => {
        const nowrap = $.let(Stack.Root([], { wrap: Style.FlexWrap("nowrap") }));
        const wrap = $.let(Stack.Root([], { wrap: Style.FlexWrap("wrap") }));
        const wrapReverse = $.let(Stack.Root([], { wrap: Style.FlexWrap("wrap-reverse") }));

        $(Assert.equal(nowrap.unwrap().unwrap("Stack").style.unwrap("some").wrap.unwrap("some").hasTag("nowrap"), true));
        $(Assert.equal(wrap.unwrap().unwrap("Stack").style.unwrap("some").wrap.unwrap("some").hasTag("wrap"), true));
        $(Assert.equal(wrapReverse.unwrap().unwrap("Stack").style.unwrap("some").wrap.unwrap("some").hasTag("wrap-reverse"), true));
    });

    // =========================================================================
    // HStack (Horizontal Stack)
    // =========================================================================

    test("HStack creates horizontal stack", $ => {
        const hstack = $.let(Stack.HStack([]));

        $(Assert.equal(hstack.unwrap().unwrap("Stack").style.hasTag("some"), true));
        $(Assert.equal(hstack.unwrap().unwrap("Stack").style.unwrap("some").direction.hasTag("some"), true));
        $(Assert.equal(hstack.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("row"), true));
    });

    test("HStack with gap", $ => {
        const hstack = $.let(Stack.HStack([], {
            gap: "4",
        }));

        $(Assert.equal(hstack.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("row"), true));
        $(Assert.equal(hstack.unwrap().unwrap("Stack").style.unwrap("some").gap.unwrap("some"), "4"));
    });

    test("HStack with children and styling", $ => {
        const child1 = Text.Root("Left");
        const child2 = Text.Root("Right");
        const hstack = $.let(Stack.HStack([
            child1,
            child2,
        ], {
            gap: "4",
            align: Style.AlignItems("center"),
            justify: Style.JustifyContent("space-between"),
        }));

        $(Assert.equal(hstack.unwrap().unwrap("Stack").children.size(), 2n));
        const style = hstack.unwrap().unwrap("Stack").style.unwrap("some");
        $(Assert.equal(style.direction.unwrap("some").hasTag("row"), true));
        $(Assert.equal(style.gap.unwrap("some"), "4"));
        $(Assert.equal(style.align.unwrap("some").hasTag("center"), true));
        $(Assert.equal(style.justify.unwrap("some").hasTag("space-between"), true));
    });

    // =========================================================================
    // VStack (Vertical Stack)
    // =========================================================================

    test("VStack creates vertical stack", $ => {
        const vstack = $.let(Stack.VStack([]));

        $(Assert.equal(vstack.unwrap().unwrap("Stack").style.hasTag("some"), true));
        $(Assert.equal(vstack.unwrap().unwrap("Stack").style.unwrap("some").direction.hasTag("some"), true));
        $(Assert.equal(vstack.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("column"), true));
    });

    test("VStack with gap", $ => {
        const vstack = $.let(Stack.VStack([], {
            gap: "4",
        }));

        $(Assert.equal(vstack.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("column"), true));
        $(Assert.equal(vstack.unwrap().unwrap("Stack").style.unwrap("some").gap.unwrap("some"), "4"));
    });

    test("VStack with children and styling", $ => {
        const child1 = Text.Root("Top");
        const child2 = Text.Root("Bottom");
        const vstack = $.let(Stack.VStack([
            child1,
            child2,
        ], {
            gap: "4",
            align: Style.AlignItems("stretch"),
        }));

        $(Assert.equal(vstack.unwrap().unwrap("Stack").children.size(), 2n));
        const style = vstack.unwrap().unwrap("Stack").style.unwrap("some");
        $(Assert.equal(style.direction.unwrap("some").hasTag("column"), true));
        $(Assert.equal(style.gap.unwrap("some"), "4"));
        $(Assert.equal(style.align.unwrap("some").hasTag("stretch"), true));
    });

    // =========================================================================
    // Nested Stacks
    // =========================================================================

    test("creates nested stacks", $ => {
        const innerStack = Stack.HStack([
            Text.Root("Inner 1"),
            Text.Root("Inner 2"),
        ], {
            gap: "2",
        });

        const outerStack = $.let(Stack.VStack([
            innerStack,
            Text.Root("Outer Item"),
        ], {
            gap: "4",
        }));

        $(Assert.equal(outerStack.unwrap().unwrap("Stack").children.size(), 2n));
        $(Assert.equal(outerStack.unwrap().unwrap("Stack").style.unwrap("some").direction.unwrap("some").hasTag("column"), true));
        $(Assert.equal(outerStack.unwrap().unwrap("Stack").style.unwrap("some").gap.unwrap("some"), "4"));
    });

    // =========================================================================
    // Typical Use Cases
    // =========================================================================

    test("creates navigation bar layout", $ => {
        const logo = Text.Root("Logo");
        const nav1 = Text.Root("Home");
        const nav2 = Text.Root("About");
        const navBar = $.let(Stack.HStack([
            logo,
            nav1,
            nav2,
        ], {
            gap: "4",
            align: Style.AlignItems("center"),
            justify: Style.JustifyContent("space-between"),
            padding: Stack.Padding({ top: "4", right: "4", bottom: "4", left: "4" }),
            background: "white",
        }));

        $(Assert.equal(navBar.unwrap().unwrap("Stack").children.size(), 3n));
        const style = navBar.unwrap().unwrap("Stack").style.unwrap("some");
        $(Assert.equal(style.direction.unwrap("some").hasTag("row"), true));
        $(Assert.equal(style.justify.unwrap("some").hasTag("space-between"), true));
    });

    test("creates form layout", $ => {
        const label1 = Text.Root("Name:");
        const label2 = Text.Root("Email:");
        const formLayout = $.let(Stack.VStack([
            label1,
            label2,
        ], {
            gap: "4",
            align: Style.AlignItems("stretch"),
            width: "100%",
        }));

        $(Assert.equal(formLayout.unwrap().unwrap("Stack").children.size(), 2n));
        const style = formLayout.unwrap().unwrap("Stack").style.unwrap("some");
        $(Assert.equal(style.direction.unwrap("some").hasTag("column"), true));
        $(Assert.equal(style.align.unwrap("some").hasTag("stretch"), true));
        $(Assert.equal(style.width.unwrap("some"), "100%"));
    });
}, {   platformFns: TestImpl,});
