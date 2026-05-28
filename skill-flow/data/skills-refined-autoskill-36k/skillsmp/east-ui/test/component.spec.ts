/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, TestImpl } from "@elaraai/east-node-std";
import {
    Box,
    Stack,
    Text,
    Badge,
    Separator,
    Stat,
    Alert,
    Progress,
    Tag,
    UIComponentType,
} from "../src/index.js";

describeEast("UIComponentType - Nested Components", (test) => {
    test("creates nested dashboard layout", $ => {
        // Build a dashboard: Box > VStack > [header row, separator, stats row, content, tags]
        $.let(Box.Root(
            [
                Stack.VStack([
                    // Header row: HStack with title + badge
                    Stack.HStack(
                        [
                            Text.Root("Dashboard"),
                            Badge.Root("Live", { colorPalette: "green", variant: "solid" }),
                        ],
                        { gap: "2" }
                    ),

                    // Separator
                    Separator.Root(),

                    // Stats row: HStack with multiple stats
                    Stack.HStack(
                        [
                            Stat.Root("Revenue", "$45,231", { indicator: "up" }),
                            Stat.Root("Users", "1,234"),
                            Stat.Root("Orders", "156", { indicator: "down" }),
                        ],
                        { gap: "6" }
                    ),

                    // Content section: Box with alert and progress
                    Box.Root(
                        [
                            Alert.Root("info", { title: "Welcome back!" }),
                            Progress.Root(75.0, { colorPalette: "blue" })
                        ],
                        { padding: Box.Padding({ top: "4", right: "4", bottom: "4", left: "4" }) }
                    ),

                    // Tags row
                    Stack.HStack(
                        [
                            Tag.Root("Analytics", { colorPalette: "blue" }),
                            Tag.Root("Reports", { colorPalette: "purple" }),
                            Tag.Root("Settings", { colorPalette: "gray" }),
                        ],
                        { gap: "2" }
                    ),

                ],
                    { gap: "4" }
                )
            ],
            { padding: Box.Padding({ top: "6", right: "6", bottom: "6", left: "6" }), background: "white" }
        ), UIComponentType);
    });
}, {   platformFns: TestImpl,});
