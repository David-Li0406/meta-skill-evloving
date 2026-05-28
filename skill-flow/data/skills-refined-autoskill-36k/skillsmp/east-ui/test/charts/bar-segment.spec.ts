/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { some } from "@elaraai/east";
import { Chart } from "../../src/index.js";

describeEast("Chart.BarSegment", (test) => {
    // =========================================================================
    // Basic BarSegment
    // =========================================================================

    test("creates basic bar segment", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
            { name: "Direct", value: 100000, color: some("blue.solid") },
            { name: "Bing", value: 200000, color: some("orange.solid") },
        ]));

        $(Assert.equal(chart.unwrap().getTag(), "BarSegment"));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.size(), 3n));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.get(0n).name, "Google"));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.get(0n).value, 500000));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.get(0n).color.unwrap("some"), "teal.solid"));
    });

    test("creates bar segment with four items", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
            { name: "Direct", value: 100000, color: some("blue.solid") },
            { name: "Bing", value: 200000, color: some("orange.solid") },
            { name: "Yandex", value: 100000, color: some("purple.solid") },
        ]));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.size(), 4n));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.get(3n).name, "Yandex"));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.get(3n).color.unwrap("some"), "purple.solid"));
    });

    // =========================================================================
    // Sorting
    // =========================================================================

    test("creates bar segment with descending sort", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
            { name: "Direct", value: 100000, color: some("blue.solid") },
        ], {
            sort: { by: "value", direction: "desc" },
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").sort.hasTag("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").sort.unwrap("some").by, "value"));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").sort.unwrap("some").direction.hasTag("desc"), true));
    });

    test("creates bar segment with ascending sort", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
            { name: "Direct", value: 100000, color: some("blue.solid") },
        ], {
            sort: { by: "value", direction: "asc" },
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").sort.unwrap("some").direction.hasTag("asc"), true));
    });

    test("creates bar segment with sort by name", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
            { name: "Bing", value: 200000, color: some("orange.solid") },
        ], {
            sort: { by: "name", direction: "asc" },
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").sort.unwrap("some").by, "name"));
    });

    // =========================================================================
    // Display Options
    // =========================================================================

    test("creates bar segment with value display", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
        ], {
            showValue: true,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showValue.unwrap("some"), true));
    });

    test("creates bar segment without value display", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
        ], {
            showValue: false,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showValue.unwrap("some"), false));
    });

    test("creates bar segment with label display", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
        ], {
            showLabel: true,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showLabel.unwrap("some"), true));
    });

    test("creates bar segment without label display", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
        ], {
            showLabel: false,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showLabel.unwrap("some"), false));
    });

    // =========================================================================
    // Combined Display Options
    // =========================================================================

    test("creates bar segment with value and label display", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
            { name: "Bing", value: 200000, color: some("orange.solid") },
        ], {
            showValue: true,
            showLabel: true,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showValue.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showLabel.unwrap("some"), true));
    });

    // =========================================================================
    // Complete Examples from Chakra Reference
    // =========================================================================

    test("creates complete bar segment matching Chakra BarSegmentBasic example", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Google", value: 500000, color: some("teal.solid") },
            { name: "Direct", value: 100000, color: some("blue.solid") },
            { name: "Bing", value: 200000, color: some("orange.solid") },
            { name: "Yandex", value: 100000, color: some("purple.solid") },
        ], {
            sort: { by: "value", direction: "desc" },
            showValue: true,
            showLabel: true,
        }));

        $(Assert.equal(chart.unwrap().getTag(), "BarSegment"));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.size(), 4n));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").sort.unwrap("some").by, "value"));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").sort.unwrap("some").direction.hasTag("desc"), true));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showValue.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showLabel.unwrap("some"), true));
    });

    test("creates bar segment for traffic sources visualization", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Search", value: 450000, color: some("green.solid") },
            { name: "Social", value: 250000, color: some("blue.solid") },
            { name: "Email", value: 150000, color: some("orange.solid") },
            { name: "Direct", value: 100000, color: some("gray.solid") },
            { name: "Referral", value: 50000, color: some("purple.solid") },
        ], {
            sort: { by: "value", direction: "desc" },
            showValue: true,
            showLabel: true,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.size(), 5n));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.get(0n).name, "Search"));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.get(0n).value, 450000));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.get(0n).color.unwrap("some"), "green.solid"));
    });

    test("creates bar segment for budget allocation", $ => {
        const chart = $.let(Chart.BarSegment([
            { name: "Marketing", value: 35, color: some("teal.solid") },
            { name: "Development", value: 40, color: some("blue.solid") },
            { name: "Operations", value: 15, color: some("orange.solid") },
            { name: "Other", value: 10, color: some("gray.solid") },
        ], {
            showLabel: true,
        }));

        $(Assert.equal(chart.unwrap().unwrap("BarSegment").data.size(), 4n));
        $(Assert.equal(chart.unwrap().unwrap("BarSegment").showLabel.unwrap("some"), true));
    });
}, {   platformFns: TestImpl,});
