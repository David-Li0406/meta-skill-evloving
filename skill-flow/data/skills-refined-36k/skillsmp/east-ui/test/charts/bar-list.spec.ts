/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Chart } from "../../src/index.js";
import { none, some } from "@elaraai/east";

describeEast("Chart.BarList", (test) => {
    // =========================================================================
    // Basic BarList
    // =========================================================================

    test("creates basic bar list", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
            { name: "Direct", value: 100000, color: none },
            { name: "Bing", value: 200000, color: none },
        ]));

        $(Assert.equal(chart.unwrap().getTag(), "BarList"));
        $(Assert.equal(chart.unwrap().unwrap("BarList").data.size(), 3n));
        $(Assert.equal(chart.unwrap().unwrap("BarList").data.get(0n).name, "Google"));
        $(Assert.equal(chart.unwrap().unwrap("BarList").data.get(0n).value, 1200000));
    });

    test("creates bar list with many items", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
            { name: "Direct", value: 100000, color: none },
            { name: "Bing", value: 200000, color: none },
            { name: "Yahoo", value: 20000, color: none },
            { name: "ChatGPT", value: 1345000, color: none },
            { name: "Github", value: 100000, color: none },
            { name: "Yandex", value: 100000, color: none },
        ]));

        $(Assert.equal(chart.unwrap().unwrap("BarList").data.size(), 7n));
        $(Assert.equal(chart.unwrap().unwrap("BarList").data.get(4n).name, "ChatGPT"));
        $(Assert.equal(chart.unwrap().unwrap("BarList").data.get(4n).value, 1345000));
    });

    // =========================================================================
    // Sorting
    // =========================================================================

    test("creates bar list with descending sort", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
            { name: "Direct", value: 100000, color: none },
        ], {
            sort: { by: "value", direction: "desc" },
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").sort.hasTag("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("BarList").sort.unwrap("some").by, "value"));
        $(Assert.equal(chart.unwrap().unwrap("BarList").sort.unwrap("some").direction.hasTag("desc"), true));
    });

    test("creates bar list with ascending sort", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
            { name: "Direct", value: 100000, color: none },
        ], {
            sort: { by: "value", direction: "asc" },
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").sort.unwrap("some").direction.hasTag("asc"), true));
    });

    test("creates bar list with sort by name", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
            { name: "Bing", value: 200000, color: none },
        ], {
            sort: { by: "name", direction: "asc" },
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").sort.unwrap("some").by, "name"));
    });

    // =========================================================================
    // Display Options
    // =========================================================================

    test("creates bar list with value display", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
        ], {
            showValue: true,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").showValue.unwrap("some"), true));
    });

    test("creates bar list without value display", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
        ], {
            showValue: false,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").showValue.unwrap("some"), false));
    });

    test("creates bar list with label display", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
        ], {
            showLabel: true,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").showLabel.unwrap("some"), true));
    });

    // =========================================================================
    // Value Format
    // =========================================================================

    test("creates bar list with compact value format", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
        ], {
            valueFormat: "compact",
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").valueFormat.unwrap("some").hasTag("compact"), true));
    });

    test("creates bar list with percent value format", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Created", value: 120, color: none },
            { name: "Closed", value: 10, color: none },
        ], {
            valueFormat: "percent",
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").valueFormat.unwrap("some").hasTag("percent"), true));
    });

    test("creates bar list with currency value format", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Sales", value: 50000, color: none },
        ], {
            valueFormat: Chart.TickFormat.Currency({ currency: "USD" }),
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").valueFormat.unwrap("some").hasTag("currency"), true));
    });

    // =========================================================================
    // Color
    // =========================================================================

    test("creates bar list with custom color", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
        ], {
            color: "teal.subtle",
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").color.unwrap("some"), "teal.subtle"));
    });

    test("creates bar list with pink color", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Created", value: 120, color: none },
        ], {
            color: "pink.subtle",
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").color.unwrap("some"), "pink.subtle"));
    });

    // =========================================================================
    // Item-level Colors
    // =========================================================================

    test("creates bar list with item-level colors", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: some("teal.solid") },
            { name: "Direct", value: 100000, color: some("blue.solid") },
        ]));

        $(Assert.equal(chart.unwrap().unwrap("BarList").data.get(0n).color.unwrap("some"), "teal.solid"));
        $(Assert.equal(chart.unwrap().unwrap("BarList").data.get(1n).color.unwrap("some"), "blue.solid"));
    });

    // =========================================================================
    // Complete Examples from Chakra Reference
    // =========================================================================

    test("creates complete bar list matching Chakra BarListBasic example", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Google", value: 1200000, color: none },
            { name: "Direct", value: 100000, color: none },
            { name: "Bing", value: 200000, color: none },
            { name: "Yahoo", value: 20000, color: none },
            { name: "ChatGPT", value: 1345000, color: none },
            { name: "Github", value: 100000, color: none },
            { name: "Yandex", value: 100000, color: none },
        ], {
            sort: { by: "value", direction: "desc" },
            showValue: true,
            color: "teal.subtle",
        }));

        $(Assert.equal(chart.unwrap().getTag(), "BarList"));
        $(Assert.equal(chart.unwrap().unwrap("BarList").data.size(), 7n));
        $(Assert.equal(chart.unwrap().unwrap("BarList").sort.unwrap("some").by, "value"));
        $(Assert.equal(chart.unwrap().unwrap("BarList").sort.unwrap("some").direction.hasTag("desc"), true));
        $(Assert.equal(chart.unwrap().unwrap("BarList").showValue.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("BarList").color.unwrap("some"), "teal.subtle"));
    });

    test("creates funnel-style bar list matching Chakra BarListWithFormatter example", $ => {
        const chart = $.let(Chart.BarList([
            { name: "Created", value: 120, color: none },
            { name: "Initial Contact", value: 90, color: none },
            { name: "Booked Demo", value: 45, color: none },
            { name: "Closed", value: 10, color: none },
        ], {
            sort: { by: "value", direction: "desc" },
            showValue: true,
            valueFormat: "percent",
            color: "pink.subtle",
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarList").data.size(), 4n));
        $(Assert.equal(chart.unwrap().unwrap("BarList").valueFormat.unwrap("some").hasTag("percent"), true));
        $(Assert.equal(chart.unwrap().unwrap("BarList").color.unwrap("some"), "pink.subtle"));
    });
}, {   platformFns: TestImpl,});
