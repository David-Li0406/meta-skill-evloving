/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Chart } from "../../src/index.js";

describeEast("Chart.Composed", (test) => {
    // =========================================================================
    // Basic Composed Charts
    // =========================================================================

    test("creates composed chart with bar and line series", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", revenue: 186n, profit: 80n },
                { month: "Feb", revenue: 305n, profit: 120n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    revenue: { type: "bar", color: "teal.solid" },
                    profit: { type: "line", color: "purple.solid" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ComposedChart"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.size(), 2n));
    });

    test("creates composed chart with all series types", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", bars: 186n, lines: 80n, areas: 150n, dots: 100n },
                { month: "Feb", bars: 305n, lines: 120n, areas: 200n, dots: 150n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    bars: { type: "bar", color: "teal.solid" },
                    lines: { type: "line", color: "purple.solid", showDots: true },
                    areas: { type: "area", color: "blue.solid", fillOpacity: 0.3 },
                    dots: { type: "scatter", color: "orange.solid" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ComposedChart"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.size(), 4n));
    });

    // =========================================================================
    // Area Range in Composed Charts
    // =========================================================================

    test("creates composed chart with area-range for confidence bands", $ => {
        const chart = $.let(Chart.Composed(
            [
                { day: "Mon", value: 100n, low: 80n, high: 120n },
                { day: "Tue", value: 150n, low: 130n, high: 170n },
            ],
            {
                xAxis: { dataKey: "day" },
                series: {
                    value: { type: "line", color: "blue.solid" },
                    confidence: { type: "area-range", lowKey: "low", highKey: "high", color: "blue.200", fillOpacity: 0.3 },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ComposedChart"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.size(), 2n));
        // Check the area-range series has correct keys
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(1n).unwrap("areaRange").lowKey, "low"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(1n).unwrap("areaRange").highKey, "high"));
    });

    // =========================================================================
    // Line Series Options
    // =========================================================================

    test("creates composed chart with line series options", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", trend: 100n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    trend: { type: "line", color: "purple.solid", showDots: true, showLine: true, strokeDasharray: "5 5" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(0n).unwrap("line").showDots.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(0n).unwrap("line").showLine.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(0n).unwrap("line").strokeDasharray.unwrap("some"), "5 5"));
    });

    // =========================================================================
    // Area Series Options
    // =========================================================================

    test("creates composed chart with area series stacking", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", area1: 100n, area2: 80n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    area1: { type: "area", color: "teal.solid", fillOpacity: 0.5, stackId: "stack1" },
                    area2: { type: "area", color: "blue.solid", fillOpacity: 0.5, stackId: "stack1" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(0n).unwrap("area").stackId.unwrap("some"), "stack1"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(1n).unwrap("area").stackId.unwrap("some"), "stack1"));
    });

    // =========================================================================
    // Bar Series Options
    // =========================================================================

    test("creates composed chart with bar series stacking", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", bar1: 100n, bar2: 80n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    bar1: { type: "bar", color: "teal.solid", stackId: "bars" },
                    bar2: { type: "bar", color: "purple.solid", stackId: "bars" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(0n).unwrap("bar").stackId.unwrap("some"), "bars"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(1n).unwrap("bar").stackId.unwrap("some"), "bars"));
    });

    // =========================================================================
    // Chart-Level Options
    // =========================================================================

    test("creates composed chart with grid and tooltip", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", value: 100n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    value: { type: "line", color: "blue.solid" },
                },
                grid: { show: true },
                tooltip: { show: true },
                legend: { show: true },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").grid.unwrap("some").show.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").tooltip.unwrap("some").show.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").legend.unwrap("some").show.unwrap("some"), true));
    });

    test("creates composed chart with curve type", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", value: 100n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    value: { type: "line", color: "blue.solid" },
                },
                curveType: "natural",
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").curveType.unwrap("some").hasTag("natural"), true));
    });

    test("creates composed chart with bar size and gap", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", value: 100n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    value: { type: "bar", color: "teal.solid" },
                },
                barSize: 20n,
                barGap: 4n,
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").barSize.unwrap("some"), 20n));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").barGap.unwrap("some"), 4n));
    });
}, {   platformFns: TestImpl,});

describeEast("Chart.Composed Pivot", (test) => {
    // =========================================================================
    // Pivot Key Support (Long/Pivoted Data Format)
    // =========================================================================

    test("creates chart with pivotKey", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", category: "A", value: 100n },
                { month: "Jan", category: "B", value: 50n },
                { month: "Feb", category: "A", value: 120n },
                { month: "Feb", category: "B", value: 80n },
            ],
            {
                xAxis: { dataKey: "month" },
                pivotKey: "category",
                valueKey: "value",
                series: {
                    value: { type: "line", color: "teal.solid" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ComposedChart"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").pivotKey.unwrap("some"), "category"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").valueKey.unwrap("some"), "value"));
    });

    test("creates chart without pivotKey (backward compat)", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", revenue: 100n, profit: 50n },
            ],
            {
                xAxis: { dataKey: "month" },
                series: {
                    revenue: { type: "bar", color: "teal.solid" },
                    profit: { type: "line", color: "blue.solid" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").pivotKey.hasTag("none"), true));
    });

    test("creates chart with pivotColors in line series", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", region: "North", sales: 100n },
                { month: "Jan", region: "South", sales: 80n },
            ],
            {
                xAxis: { dataKey: "month" },
                pivotKey: "region",
                valueKey: "sales",
                series: {
                    sales: {
                        type: "line",
                        color: "blue.500",
                        pivotColors: new Map([
                            ["North", "blue.700"],
                            ["South", "blue.300"],
                        ]),
                    },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").pivotKey.unwrap("some"), "region"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(0n).unwrap("line").pivotColors.hasTag("some"), true));
    });

    test("creates chart with pivotColors in bar series", $ => {
        const chart = $.let(Chart.Composed(
            [
                { month: "Jan", region: "North", sales: 100n },
            ],
            {
                xAxis: { dataKey: "month" },
                pivotKey: "region",
                valueKey: "sales",
                series: {
                    sales: {
                        type: "bar",
                        color: "teal.500",
                        pivotColors: new Map([
                            ["North", "teal.700"],
                        ]),
                    },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.get(0n).unwrap("bar").pivotColors.hasTag("some"), true));
    });
}, {   platformFns: TestImpl,});

describeEast("Chart.ComposedMulti", (test) => {
    // =========================================================================
    // Multi-Series Composed Charts
    // =========================================================================

    test("creates composed multi chart with sparse data", $ => {
        const chart = $.let(Chart.ComposedMulti(
            {
                revenue: [
                    { month: "Jan", value: 100n },
                    { month: "Feb", value: 200n },
                ],
                profit: [
                    { month: "Jan", value: 50n },
                    { month: "Mar", value: 150n }, // sparse - Feb missing
                ],
            },
            {
                xAxis: { dataKey: "month" },
                series: {
                    revenue: { type: "bar", dataKey: "value", color: "teal.solid" },
                    profit: { type: "line", dataKey: "value", color: "purple.solid" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ComposedChart"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.size(), 2n));
    });

    test("creates composed multi chart with mixed types", $ => {
        const chart = $.let(Chart.ComposedMulti(
            {
                bars: [
                    { x: "A", value: 100n },
                    { x: "B", value: 200n },
                ],
                lines: [
                    { x: "A", value: 80n },
                    { x: "B", value: 150n },
                ],
                areas: [
                    { x: "A", value: 60n },
                    { x: "B", value: 120n },
                ],
            },
            {
                xAxis: { dataKey: "x" },
                series: {
                    bars: { type: "bar", dataKey: "value", color: "teal.solid" },
                    lines: { type: "line", dataKey: "value", color: "purple.solid", showDots: true },
                    areas: { type: "area", dataKey: "value", color: "blue.solid", fillOpacity: 0.3 },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ComposedChart"));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").series.size(), 3n));
        $(Assert.equal(chart.unwrap().unwrap("ComposedChart").dataSeries.hasTag("some"), true));
    });
}, {   platformFns: TestImpl,});
