/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Chart } from "../../src/index.js";

describeEast("Chart.Scatter", (test) => {
    // =========================================================================
    // Basic Scatter Charts
    // =========================================================================

    test("creates basic scatter chart", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
                { temp: 15, sales: 50 },
                { temp: 20, sales: 80 },
            ],
            { temp: { color: "teal.solid" } }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ScatterChart"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.size(), 1n));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.get(0n).name, "temp"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.get(0n).color.unwrap("some"), "teal.solid"));
    });

    test("creates scatter chart with array series spec", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            ["temp"]
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.size(), 1n));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.get(0n).name, "temp"));
    });

    test("creates scatter chart with x and y data keys", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            {
                xAxis: { dataKey: "temp" },
                yAxis: { dataKey: "sales" }
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").xDataKey.unwrap("some"), "temp"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").yDataKey.unwrap("some"), "sales"));
    });

    // =========================================================================
    // Multiple Series
    // =========================================================================

    test("creates scatter chart with multiple series", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { x: 10, y: 30, size: 5 },
                { x: 20, y: 40, size: 8 },
            ],
            {
                x: { color: "blue.solid", label: "X Position" },
                y: { color: "green.solid", label: "Y Position" },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.get(0n).name, "x"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.get(0n).label.unwrap("some"), "X Position"));
    });

    // =========================================================================
    // Axis Configuration
    // =========================================================================

    test("creates scatter chart with x-axis configuration", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            { xAxis: { dataKey: "temp", label: "Temperature" } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").xAxis.unwrap("some").dataKey.unwrap("some"), "temp"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").xAxis.unwrap("some").label.unwrap("some"), "Temperature"));
    });

    test("creates scatter chart with y-axis configuration", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            { yAxis: { dataKey: "sales", label: "Sales" } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").yAxis.unwrap("some").dataKey.unwrap("some"), "sales"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").yAxis.unwrap("some").label.unwrap("some"), "Sales"));
    });

    test("creates scatter chart with axis domain", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            {
                xAxis: { domain: [0, 50] },
                yAxis: { domain: [0, 100] }
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").xAxis.hasTag("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").yAxis.hasTag("some"), true));
    });

    // =========================================================================
    // Display Options
    // =========================================================================

    test("creates scatter chart with grid", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            { grid: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").grid.unwrap("some").show.unwrap("some"), true));
    });

    test("creates scatter chart with legend", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            { legend: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").legend.unwrap("some").show.unwrap("some"), true));
    });

    test("creates scatter chart with tooltip", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            { tooltip: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").tooltip.unwrap("some").show.unwrap("some"), true));
    });

    // =========================================================================
    // Point Size
    // =========================================================================

    test("creates scatter chart with custom point size", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            { pointSize: 8n }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").pointSize.unwrap("some"), 8n));
    });

    // =========================================================================
    // Margin
    // =========================================================================

    test("creates scatter chart with custom margin", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
            ],
            { temp: { color: "teal.solid" } },
            { margin: { top: 20n, right: 30n, bottom: 20n, left: 30n } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").margin.unwrap("some").top.unwrap("some"), 20n));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").margin.unwrap("some").left.unwrap("some"), 30n));
    });

    // =========================================================================
    // Complete Examples
    // =========================================================================

    test("creates complete scatter chart matching Chakra ScatterChartBasic example", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { temp: 10, sales: 30 },
                { temp: 15, sales: 50 },
                { temp: 20, sales: 80 },
            ],
            { temp: { color: "teal.solid" } },
            {
                xAxis: { dataKey: "temp" },
                yAxis: { dataKey: "sales" },
                grid: { show: true }
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ScatterChart"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.get(0n).color.unwrap("some"), "teal.solid"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").grid.unwrap("some").show.unwrap("some"), true));
    });

    test("creates complete multi-series scatter chart", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { x: 10, y: 30 },
                { x: 20, y: 40 },
            ],
            {
                x: { color: "blue.solid", label: "X Value" },
                y: { color: "green.solid", label: "Y Value" },
            },
            {
                xAxis: { domain: [0, 50] },
                yAxis: { domain: [0, 100] },
                tooltip: { show: true }
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").tooltip.unwrap("some").show.unwrap("some"), true));
    });
}, {   platformFns: TestImpl,});

describeEast("Chart.Scatter Pivot", (test) => {
    // =========================================================================
    // Pivot Key Support (Long/Pivoted Data Format)
    // =========================================================================

    test("creates chart with pivotKey", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { x: 10, category: "A", value: 30 },
                { x: 10, category: "B", value: 25 },
                { x: 20, category: "A", value: 50 },
                { x: 20, category: "B", value: 40 },
            ],
            { value: { color: "teal.solid" } },
            {
                xAxis: { dataKey: "x" },
                pivotKey: "category",
                valueKey: "value",
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ScatterChart"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").pivotKey.unwrap("some"), "category"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").valueKey.unwrap("some"), "value"));
    });

    test("creates chart without pivotKey (backward compat)", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { x: 10, y: 30 },
            ],
            { x: { color: "teal.solid" }, y: { color: "blue.solid" } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").pivotKey.hasTag("none"), true));
    });

    test("creates chart with pivotColors mapping", $ => {
        const chart = $.let(Chart.Scatter(
            [
                { x: 10, region: "North", sales: 30 },
                { x: 10, region: "South", sales: 25 },
            ],
            {
                sales: {
                    color: "blue.500",
                    pivotColors: new Map([
                        ["North", "blue.700"],
                        ["South", "blue.300"],
                    ]),
                },
            },
            {
                xAxis: { dataKey: "x" },
                pivotKey: "region",
                valueKey: "sales",
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").pivotKey.unwrap("some"), "region"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.get(0n).pivotColors.hasTag("some"), true));
    });
}, {   platformFns: TestImpl,});

describeEast("Chart.ScatterMulti", (test) => {
    test("creates scatter chart with multi-series data", $ => {
        const chart = $.let(Chart.ScatterMulti(
            {
                temperature: [
                    { x: 10, value: 30 },
                    { x: 20, value: 50 },
                ],
                humidity: [
                    { x: 10, value: 45 },
                    { x: 25, value: 60 },
                ],
            },
            {
                xAxis: { dataKey: "x" },
                valueKey: "value",
                series: {
                    temperature: { color: "teal.solid" },
                    humidity: { color: "blue.solid" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "ScatterChart"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").valueKey.unwrap("some"), "value"));
        $(Assert.equal(chart.unwrap().unwrap("ScatterChart").dataSeries.hasTag("some"), true));
    });
}, {   platformFns: TestImpl,});
