/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Chart } from "../../src/index.js";
import { none, some } from "@elaraai/east";

describeEast("Chart.Pie", (test) => {
    // =========================================================================
    // Basic Pie Charts
    // =========================================================================

    test("creates basic pie chart", $ => {
        const chart = $.let(Chart.Pie([
            { name: "windows", value: 400, color: some("blue.solid") },
            { name: "mac", value: 300, color: some("orange.solid") },
            { name: "linux", value: 300, color: some("pink.solid") },
            { name: "other", value: 200, color: some("green.solid") },
        ]));

        $(Assert.equal(chart.unwrap().getTag(), "PieChart"));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.size(), 4n));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(0n).name, "windows"));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(0n).value, 400));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(0n).color.unwrap("some"), "blue.solid"));
    });

    test("creates pie chart with three slices", $ => {
        const chart = $.let(Chart.Pie([
            { name: "windows", value: 400, color: some("blue.solid") },
            { name: "mac", value: 300, color: some("orange.solid") },
            { name: "linux", value: 300, color: some("pink.solid") },
        ]));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.size(), 3n));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(0n).name, "windows"));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(1n).name, "mac"));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(2n).name, "linux"));
    });

    test("creates pie chart without colors (optional)", $ => {
        const chart = $.let(Chart.Pie([
            { name: "windows", value: 400, color: none },
            { name: "mac", value: 300, color: none },
        ]));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.size(), 2n));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(0n).color.hasTag("none"), true));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(1n).color.hasTag("none"), true));
    });

    // =========================================================================
    // Donut Charts (innerRadius > 0)
    // =========================================================================

    test("creates donut chart with inner radius", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
                { name: "mac", value: 300, color: some("orange.solid") },
            ],
            {
                innerRadius: 60,
                outerRadius: 80,
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").innerRadius.unwrap("some"), 60));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").outerRadius.unwrap("some"), 80));
    });

    test("creates large donut chart for centered text", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
                { name: "mac", value: 300, color: some("orange.solid") },
                { name: "linux", value: 300, color: some("pink.solid") },
                { name: "other", value: 200, color: some("green.solid") },
            ],
            {
                innerRadius: 80,
                outerRadius: 100,
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").innerRadius.unwrap("some"), 80));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").outerRadius.unwrap("some"), 100));
    });

    // =========================================================================
    // Angle Configuration
    // =========================================================================

    test("creates pie chart with custom start angle", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
            ],
            { startAngle: 90 }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").startAngle.unwrap("some"), 90));
    });

    test("creates pie chart with custom end angle", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
            ],
            { endAngle: 270 }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").endAngle.unwrap("some"), 270));
    });

    test("creates semi-circle pie chart", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
                { name: "mac", value: 300, color: some("orange.solid") },
            ],
            {
                startAngle: 180,
                endAngle: 0,
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").startAngle.unwrap("some"), 180));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").endAngle.unwrap("some"), 0));
    });

    // =========================================================================
    // Padding Angle
    // =========================================================================

    test("creates pie chart with padding angle", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
                { name: "mac", value: 300, color: some("orange.solid") },
            ],
            { paddingAngle: 5 }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").paddingAngle.unwrap("some"), 5));
    });

    // =========================================================================
    // Display Options
    // =========================================================================

    test("creates pie chart with labels", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
            ],
            { showLabels: true }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").showLabels.unwrap("some"), true));
    });

    test("creates pie chart with legend", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
            ],
            { legend: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").legend.unwrap("some").show.unwrap("some"), true));
    });

    test("creates pie chart with tooltip", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
            ],
            { tooltip: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").tooltip.unwrap("some").show.unwrap("some"), true));
    });

    // =========================================================================
    // Margin
    // =========================================================================

    test("creates pie chart with custom margin", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
            ],
            { margin: { top: 20n, right: 30n, bottom: 20n, left: 30n } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").margin.unwrap("some").top.unwrap("some"), 20n));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").margin.unwrap("some").left.unwrap("some"), 30n));
    });

    // =========================================================================
    // Complete Examples from Chakra Reference
    // =========================================================================

    test("creates complete pie chart matching Chakra PieChartBasic example", $ => {
        const chart = $.let(Chart.Pie([
            { name: "windows", value: 400, color: some("blue.solid") },
            { name: "mac", value: 300, color: some("orange.solid") },
            { name: "linux", value: 300, color: some("pink.solid") },
            { name: "other", value: 200, color: some("green.solid") },
        ]));

        $(Assert.equal(chart.unwrap().getTag(), "PieChart"));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.size(), 4n));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(0n).color.unwrap("some"), "blue.solid"));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(1n).color.unwrap("some"), "orange.solid"));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(2n).color.unwrap("some"), "pink.solid"));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.get(3n).color.unwrap("some"), "green.solid"));
    });

    test("creates complete pie chart with legend matching Chakra PieChartWithLegend example", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
                { name: "mac", value: 300, color: some("orange.solid") },
                { name: "linux", value: 300, color: some("pink.solid") },
            ],
            { legend: { show: true } }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").data.size(), 3n));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").legend.unwrap("some").show.unwrap("some"), true));
    });

    test("creates complete donut chart matching Chakra DonutChartBasic example", $ => {
        const chart = $.let(Chart.Pie(
            [
                { name: "windows", value: 400, color: some("blue.solid") },
                { name: "mac", value: 300, color: some("orange.solid") },
                { name: "linux", value: 300, color: some("pink.solid") },
                { name: "other", value: 200, color: some("green.solid") },
            ],
            {
                innerRadius: 60,
                outerRadius: 80,
                tooltip: { show: true },
            }
        ));

        $(Assert.equal(chart.unwrap().unwrap("PieChart").innerRadius.unwrap("some"), 60));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").outerRadius.unwrap("some"), 80));
        $(Assert.equal(chart.unwrap().unwrap("PieChart").tooltip.unwrap("some").show.unwrap("some"), true));
    });
}, {   platformFns: TestImpl,});
