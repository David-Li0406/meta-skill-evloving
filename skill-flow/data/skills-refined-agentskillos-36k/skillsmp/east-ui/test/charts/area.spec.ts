/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Chart } from "../../src/index.js";

describeEast("Chart.Area", (test) => {
    // =========================================================================
    // Basic Area Charts
    // =========================================================================

    test("creates basic area chart with single series", $ => {
        const chart = $.let(Chart.Area(
            [
                { "month": "January", "revenue": 186n },
                { "month": "February", "revenue": 305n },
                { "month": "March", "revenue": 237n },
            ],
            { revenue: { color: "teal.solid" } }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.size(), 1n));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.get(0n).name, "revenue"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.get(0n).color.unwrap("some"), "teal.solid"));
    });

    test("creates area chart with array series spec", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            ["revenue"]
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.size(), 1n));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.get(0n).name, "revenue"));
    });

    test("creates area chart with multiple series", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", windows: 186n, mac: 80n, linux: 120n },
                { month: "February", windows: 165n, mac: 95n, linux: 110n },
            ],
            {
                windows: { color: "teal.solid" },
                mac: { color: "purple.solid" },
                linux: { color: "blue.solid" },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.size(), 3n));
    });

    // =========================================================================
    // Stacked Area Charts
    // =========================================================================

    test("creates stacked area chart", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", windows: 186n, mac: 80n, linux: 120n },
            ],
            {
                windows: { color: "teal.solid", stackId: "a" },
                mac: { color: "purple.solid", stackId: "a" },
                linux: { color: "blue.solid", stackId: "a" },
            },
            { stacked: true }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").stacked.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.get(0n).stackId.unwrap("some"), "a"));
    });

    test("creates 100% stacked area chart with stackOffset expand", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", windows: 186n, mac: 80n },
            ],
            {
                windows: { color: "teal.solid" },
                mac: { color: "purple.solid" },
            },
            { stacked: true, stackOffset: "expand" }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").stacked.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").stackOffset.unwrap("some").hasTag("expand"), true));
    });

    // =========================================================================
    // Axis Configuration
    // =========================================================================

    test("creates area chart with x-axis dataKey", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { xAxis: { dataKey: "month" } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").xAxis.hasTag("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").xAxis.unwrap("some").dataKey.unwrap("some"), "month"));
    });

    test("creates area chart with y-axis percent tick format", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { yAxis: { tickFormat: "percent" } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").yAxis.hasTag("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").yAxis.unwrap("some").tickFormat.unwrap("some").hasTag("percent"), true));
    });

    // =========================================================================
    // Curve Types
    // =========================================================================

    test("creates area chart with natural curve", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { curveType: "natural" }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").curveType.unwrap("some").hasTag("natural"), true));
    });

    test("creates area chart with monotone curve", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { curveType: "monotone" }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").curveType.unwrap("some").hasTag("monotone"), true));
    });

    // =========================================================================
    // Display Options
    // =========================================================================

    test("creates area chart with grid", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { grid: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").grid.unwrap("some").show.unwrap("some"), true));
    });

    test("creates area chart with legend", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { legend: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").legend.unwrap("some").show.unwrap("some"), true));
    });

    test("creates area chart with tooltip", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { tooltip: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").tooltip.unwrap("some").show.unwrap("some"), true));
    });

    test("creates area chart with custom fill opacity", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { fillOpacity: 0.3 }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").fillOpacity.unwrap("some"), 0.3));
    });

    // =========================================================================
    // Margin
    // =========================================================================

    test("creates area chart with custom margin", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { margin: { top: 20n, right: 30n, bottom: 20n, left: 30n } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").margin.unwrap("some").top.unwrap("some"), 20n));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").margin.unwrap("some").left.unwrap("some"), 30n));
    });

    // =========================================================================
    // Brush
    // =========================================================================

    test("creates area chart with brush enabled", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
                { month: "February", revenue: 305n },
            ],
            { revenue: { color: "teal.solid" } },
            { xAxis: { dataKey: "month" }, brush: {} }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").brush.hasTag("some"), true));
    });

    test("creates area chart with brush configuration", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", revenue: 186n },
            ],
            { revenue: { color: "teal.solid" } },
            { brush: { dataKey: "month", height: 40n, startIndex: 0n, endIndex: 5n } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").brush.unwrap("some").dataKey.unwrap("some"), "month"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").brush.unwrap("some").height.unwrap("some"), 40n));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").brush.unwrap("some").startIndex.unwrap("some"), 0n));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").brush.unwrap("some").endIndex.unwrap("some"), 5n));
    });

    // =========================================================================
    // Complete Example
    // =========================================================================

    test("creates complete area chart matching Chakra example", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "January", windows: 186n, mac: 80n, linux: 120n },
                { month: "February", windows: 165n, mac: 95n, linux: 110n },
                { month: "March", windows: 190n, mac: 87n, linux: 125n },
            ],
            {
                windows: { color: "teal.solid", stackId: "a" },
                mac: { color: "purple.solid", stackId: "a" },
                linux: { color: "blue.solid", stackId: "a" },
            },
            {
                xAxis: { dataKey: "month" },
                stacked: true,
                stackOffset: "expand",
                grid: { show: true },
                tooltip: { show: true },
                legend: { show: true },
                fillOpacity: 0.2,
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.size(), 3n));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").grid.unwrap("some").show.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").fillOpacity.unwrap("some"), 0.2));
    });
}, {   platformFns: TestImpl,});

describeEast("Chart.Area Pivot", (test) => {
    // =========================================================================
    // Pivot Key Support (Long/Pivoted Data Format)
    // =========================================================================

    test("creates chart with pivotKey", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "Jan", category: "A", value: 100n },
                { month: "Jan", category: "B", value: 50n },
                { month: "Feb", category: "A", value: 120n },
                { month: "Feb", category: "B", value: 80n },
            ],
            { value: { color: "teal.solid" } },
            {
                xAxis: { dataKey: "month" },
                pivotKey: "category",
                valueKey: "value",
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").pivotKey.unwrap("some"), "category"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").valueKey.unwrap("some"), "value"));
    });

    test("creates chart without pivotKey (backward compat)", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "Jan", revenue: 100n, profit: 50n },
            ],
            { revenue: { color: "teal.solid" }, profit: { color: "blue.solid" } },
            { xAxis: { dataKey: "month" } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").pivotKey.hasTag("none"), true));
    });

    test("creates chart with pivotColors mapping", $ => {
        const chart = $.let(Chart.Area(
            [
                { month: "Jan", region: "North", sales: 100n },
                { month: "Jan", region: "South", sales: 80n },
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
                xAxis: { dataKey: "month" },
                pivotKey: "region",
                valueKey: "sales",
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaChart").pivotKey.unwrap("some"), "region"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.get(0n).pivotColors.hasTag("some"), true));
    });
}, {   platformFns: TestImpl,});

describeEast("Chart.AreaMulti", (test) => {
    test("creates area chart with multi-series data", $ => {
        const chart = $.let(Chart.AreaMulti(
            {
                revenue: [
                    { month: "January", value: 186n },
                    { month: "February", value: 305n },
                ],
                profit: [
                    { month: "January", value: 80n },
                    { month: "March", value: 150n },
                ],
            },
            {
                xAxis: { dataKey: "month" },
                valueKey: "value",
                series: {
                    revenue: { color: "teal.solid" },
                    profit: { color: "purple.solid" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").valueKey.unwrap("some"), "value"));
        $(Assert.equal(chart.unwrap().unwrap("AreaChart").dataSeries.hasTag("some"), true));
    });
}, {   platformFns: TestImpl,});

// ============================================================================
// Area Range Charts
// ============================================================================

describeEast("Chart.AreaRange", (test) => {
    test("creates basic area range chart with single series", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { "day": "05-01", "low": -1n, "high": 10n },
                { "day": "05-02", "low": 2n, "high": 15n },
                { "day": "05-03", "low": 3n, "high": 12n },
            ],
            { temperature: { lowKey: "low", highKey: "high", color: "teal.solid" } }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaRangeChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.size(), 1n));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.get(0n).name, "temperature"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.get(0n).lowKey, "low"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.get(0n).highKey, "high"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.get(0n).color.unwrap("some"), "teal.solid"));
    });

    test("creates area range chart with multiple series", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", tempLow: -1n, tempHigh: 10n, humidLow: 30n, humidHigh: 50n },
                { day: "05-02", tempLow: 2n, tempHigh: 15n, humidLow: 35n, humidHigh: 55n },
            ],
            {
                temperature: { lowKey: "tempLow", highKey: "tempHigh", color: "teal.solid" },
                humidity: { lowKey: "humidLow", highKey: "humidHigh", color: "blue.solid" },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaRangeChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.size(), 2n));
    });

    test("creates area range chart with x-axis configuration", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", low: -1n, high: 10n },
            ],
            { temperature: { lowKey: "low", highKey: "high" } },
            { xAxis: { dataKey: "day", label: "Date" } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").xAxis.hasTag("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").xAxis.unwrap("some").dataKey.unwrap("some"), "day"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").xAxis.unwrap("some").label.unwrap("some"), "Date"));
    });

    test("creates area range chart with curve type", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", low: -1n, high: 10n },
            ],
            { temperature: { lowKey: "low", highKey: "high" } },
            { curveType: "natural" }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").curveType.unwrap("some").hasTag("natural"), true));
    });

    test("creates area range chart with grid", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", low: -1n, high: 10n },
            ],
            { temperature: { lowKey: "low", highKey: "high" } },
            { grid: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").grid.unwrap("some").show.unwrap("some"), true));
    });

    test("creates area range chart with legend", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", low: -1n, high: 10n },
            ],
            { temperature: { lowKey: "low", highKey: "high" } },
            { legend: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").legend.unwrap("some").show.unwrap("some"), true));
    });

    test("creates area range chart with tooltip", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", low: -1n, high: 10n },
            ],
            { temperature: { lowKey: "low", highKey: "high" } },
            { tooltip: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").tooltip.unwrap("some").show.unwrap("some"), true));
    });

    test("creates area range chart with custom fill opacity", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", low: -1n, high: 10n },
            ],
            { temperature: { lowKey: "low", highKey: "high" } },
            { fillOpacity: 0.5 }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").fillOpacity.unwrap("some"), 0.5));
    });

    test("creates area range chart with series styling", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", low: -1n, high: 10n },
            ],
            {
                temperature: {
                    lowKey: "low",
                    highKey: "high",
                    color: "teal.solid",
                    label: "Temperature Range",
                    fillOpacity: 0.6,
                    stroke: "teal.700",
                    strokeWidth: 2n,
                }
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.get(0n).label.unwrap("some"), "Temperature Range"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.get(0n).fillOpacity.unwrap("some"), 0.6));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.get(0n).stroke.unwrap("some"), "teal.700"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.get(0n).strokeWidth.unwrap("some"), 2n));
    });

    test("creates complete area range chart", $ => {
        const chart = $.let(Chart.AreaRange(
            [
                { day: "05-01", tempLow: -1n, tempHigh: 10n, humidLow: 30n, humidHigh: 50n },
                { day: "05-02", tempLow: 2n, tempHigh: 15n, humidLow: 35n, humidHigh: 55n },
                { day: "05-03", tempLow: 3n, tempHigh: 12n, humidLow: 40n, humidHigh: 60n },
            ],
            {
                temperature: { lowKey: "tempLow", highKey: "tempHigh", color: "teal.solid" },
                humidity: { lowKey: "humidLow", highKey: "humidHigh", color: "blue.solid" },
            },
            {
                xAxis: { dataKey: "day" },
                curveType: "natural",
                grid: { show: true },
                tooltip: { show: true },
                legend: { show: true },
                fillOpacity: 0.4,
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaRangeChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").grid.unwrap("some").show.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").fillOpacity.unwrap("some"), 0.4));
    });
}, {   platformFns: TestImpl,});

describeEast("Chart.AreaRangeMulti", (test) => {
    test("creates area range chart with multi-series data", $ => {
        const chart = $.let(Chart.AreaRangeMulti(
            {
                temperature: [
                    { day: "05-01", low: -1n, high: 10n },
                    { day: "05-02", low: 2n, high: 15n },
                ],
                humidity: [
                    { day: "05-01", low: 30n, high: 50n },
                    { day: "05-03", low: 40n, high: 60n },
                ],
            },
            {
                xAxis: { dataKey: "day" },
                lowKey: "low",
                highKey: "high",
                series: {
                    temperature: { color: "teal.solid" },
                    humidity: { color: "blue.solid" },
                },
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaRangeChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").lowKey.unwrap("some"), "low"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").highKey.unwrap("some"), "high"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").dataSeries.hasTag("some"), true));
    });

    test("creates area range multi chart with sparse data", $ => {
        const chart = $.let(Chart.AreaRangeMulti(
            {
                temperature: [
                    { day: "05-01", low: -1n, high: 10n },
                    { day: "05-02", low: 2n, high: 15n },
                    { day: "05-03", low: 3n, high: 12n },
                ],
                humidity: [
                    { day: "05-01", low: 30n, high: 50n },
                    // 05-02 missing - sparse data
                    { day: "05-03", low: 40n, high: 60n },
                ],
            },
            {
                xAxis: { dataKey: "day" },
                lowKey: "low",
                highKey: "high",
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "AreaRangeChart"));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").series.size(), 2n));
    });

    test("creates area range multi chart with styling options", $ => {
        const chart = $.let(Chart.AreaRangeMulti(
            {
                temperature: [
                    { day: "05-01", low: -1n, high: 10n },
                ],
            },
            {
                xAxis: { dataKey: "day" },
                lowKey: "low",
                highKey: "high",
                curveType: "monotone",
                grid: { show: true },
                legend: { show: true },
                tooltip: { show: true },
                fillOpacity: 0.3,
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").curveType.unwrap("some").hasTag("monotone"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").grid.unwrap("some").show.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("AreaRangeChart").fillOpacity.unwrap("some"), 0.3));
    });
}, {   platformFns: TestImpl,});
