/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Chart } from "../../src/index.js";

describeEast("Chart.Radar", (test) => {
    // =========================================================================
    // Basic Radar Charts
    // =========================================================================

    test("creates basic radar chart with single series", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 130 },
                { month: "February", windows: 120 },
                { month: "March", windows: 75 },
            ],
            { windows: { color: "teal.solid" } }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "RadarChart"));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.size(), 1n));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.get(0n).name, "windows"));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.get(0n).color.unwrap("some"), "teal.solid"));
    });

    test("creates radar chart with dataKey", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 130 },
            ],
            { windows: { color: "teal.solid" } },
            { dataKey: "month" }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").dataKey.unwrap("some"), "month"));
    });

    // =========================================================================
    // Multiple Series
    // =========================================================================

    test("creates radar chart with multiple series", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 30, mac: 100 },
                { month: "February", windows: 50, mac: 80 },
            ],
            {
                windows: { color: "teal.solid" },
                mac: { color: "orange.solid" },
            },
            { dataKey: "month" }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.get(0n).name, "windows"));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.get(1n).name, "mac"));
    });

    test("creates skills comparison radar chart", $ => {
        const chart = $.let(Chart.Radar(
            [
                { subject: "Math", current: 80, target: 90 },
                { subject: "Science", current: 95, target: 85 },
                { subject: "English", current: 70, target: 80 },
            ],
            {
                current: { color: "teal.solid" },
                target: { color: "orange.solid" },
            },
            { dataKey: "subject" }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").dataKey.unwrap("some"), "subject"));
    });

    // =========================================================================
    // Display Options
    // =========================================================================

    test("creates radar chart with grid", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 130 },
            ],
            { windows: { color: "teal.solid" } },
            { grid: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").grid.unwrap("some").show.unwrap("some"), true));
    });

    test("creates radar chart with legend", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 130 },
            ],
            { windows: { color: "teal.solid" } },
            { legend: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").legend.unwrap("some").show.unwrap("some"), true));
    });

    test("creates radar chart with tooltip", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 130 },
            ],
            { windows: { color: "teal.solid" } },
            { tooltip: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").tooltip.unwrap("some").show.unwrap("some"), true));
    });

    // =========================================================================
    // Fill Opacity
    // =========================================================================

    test("creates radar chart with custom fill opacity", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 130 },
            ],
            { windows: { color: "teal.solid" } },
            { fillOpacity: 0.5 }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").fillOpacity.unwrap("some"), 0.5));
    });

    test("creates radar chart with low fill opacity for overlapping series", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 30, mac: 100 },
            ],
            {
                windows: { color: "teal.solid" },
                mac: { color: "orange.solid" },
            },
            { fillOpacity: 0.2 }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").fillOpacity.unwrap("some"), 0.2));
    });

    // =========================================================================
    // Margin
    // =========================================================================

    test("creates radar chart with custom margin", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 130 },
            ],
            { windows: { color: "teal.solid" } },
            { margin: { top: 20n, right: 30n, bottom: 20n, left: 30n } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").margin.unwrap("some").top.unwrap("some"), 20n));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").margin.unwrap("some").left.unwrap("some"), 30n));
    });

    // =========================================================================
    // Complete Examples
    // =========================================================================

    test("creates complete radar chart matching Chakra RadarChartBasic example", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 130 },
                { month: "February", windows: 120 },
                { month: "March", windows: 75 },
            ],
            { windows: { color: "teal.solid" } },
            {
                dataKey: "month",
                grid: { show: true },
                fillOpacity: 0.5
            }
        ));

        $(Assert.equal(chart.unwrap().getTag(), "RadarChart"));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.get(0n).name, "windows"));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").dataKey.unwrap("some"), "month"));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").grid.unwrap("some").show.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").fillOpacity.unwrap("some"), 0.5));
    });

    test("creates complete multi-series radar chart matching Chakra RadarChartMultiple example", $ => {
        const chart = $.let(Chart.Radar(
            [
                { month: "January", windows: 30, mac: 100 },
                { month: "February", windows: 50, mac: 80 },
                { month: "March", windows: 70, mac: 60 },
            ],
            {
                windows: { color: "teal.solid" },
                mac: { color: "orange.solid" },
            },
            {
                dataKey: "month",
                grid: { show: true },
                legend: { show: true },
                fillOpacity: 0.2
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("RadarChart").series.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").grid.unwrap("some").show.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").legend.unwrap("some").show.unwrap("some"), true));
        $(Assert.equal(chart.unwrap().unwrap("RadarChart").fillOpacity.unwrap("some"), 0.2));
    });
}, {   platformFns: TestImpl,});
