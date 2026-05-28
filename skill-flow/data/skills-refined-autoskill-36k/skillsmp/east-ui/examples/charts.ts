/**
 * Charts TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the charts module (Area, Bar, Line, Scatter, Pie, Radar, BarList, BarSegment).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Chart.Area, Chart.Bar)
 */

import { East, none, some } from "@elaraai/east";
import { Chart, UIComponentType } from "../src/index.js";

// ============================================================================
// AREA CHART
// ============================================================================

// File: src/charts/area/index.ts
// Export: createAreaChart
const areaChartExample = East.function([], UIComponentType, $ => {
    return Chart.Area(
        [
            { month: "Jan", revenue: 186n, profit: 80n },
            { month: "Feb", revenue: 305n, profit: 120n },
        ],
        {
            revenue: { color: "teal.solid" },
            profit: { color: "purple.solid" },
        },
        { xAxis: { dataKey: "month" } }
    );
});
areaChartExample.toIR().compile([])();

// File: src/charts/index.ts
// Export: Chart.Area
const chartAreaExample = East.function([], UIComponentType, $ => {
    return Chart.Area(
        [
            { month: "Jan", revenue: 186n, profit: 80n },
            { month: "Feb", revenue: 305n, profit: 120n },
        ],
        {
            revenue: { color: "teal.solid" },
            profit: { color: "purple.solid" },
        },
        { xAxis: { dataKey: "month" } }
    );
});
chartAreaExample.toIR().compile([])();

// ============================================================================
// BAR CHART
// ============================================================================

// File: src/charts/index.ts
// Export: Chart.Bar
const chartBarExample = East.function([], UIComponentType, $ => {
    return Chart.Bar(
        [
            { category: "A", value: 100n },
            { category: "B", value: 200n },
        ],
        { value: { color: "blue.solid" } },
        { xAxis: { dataKey: "category" } }
    );
});
chartBarExample.toIR().compile([])();

// ============================================================================
// LINE CHART
// ============================================================================

// File: src/charts/index.ts
// Export: Chart.Line
const chartLineExample = East.function([], UIComponentType, $ => {
    return Chart.Line(
        [
            { month: "Jan", revenue: 186n, profit: 80n },
            { month: "Feb", revenue: 305n, profit: 120n },
        ],
        {
            revenue: { color: "teal.solid" },
            profit: { color: "purple.solid" },
        },
        {
            xAxis: { dataKey: "month" },
            showDots: true,
        }
    );
});
chartLineExample.toIR().compile([])();

// ============================================================================
// SCATTER CHART
// ============================================================================

// File: src/charts/index.ts
// Export: Chart.Scatter
const chartScatterExample = East.function([], UIComponentType, $ => {
    return Chart.Scatter(
        [
            { x: 10, y: 30 },
            { x: 20, y: 40 },
        ],
        { y: { color: "purple.solid" } },
        { xDataKey: "x", yDataKey: "y" }
    );
});
chartScatterExample.toIR().compile([])();

// ============================================================================
// PIE CHART
// ============================================================================

// File: src/charts/index.ts
// Export: Chart.Pie
const chartPieExample = East.function([], UIComponentType, $ => {
    return Chart.Pie(
        [
            { name: "Chrome", value: 275, color: some("blue.solid") },
            { name: "Safari", value: 200, color: some("green.solid") },
        ],
        { showLabels: true }
    );
});
chartPieExample.toIR().compile([])();

// ============================================================================
// RADAR CHART
// ============================================================================

// File: src/charts/index.ts
// Export: Chart.Radar
const chartRadarExample = East.function([], UIComponentType, $ => {
    return Chart.Radar(
        [
            { subject: "Math", A: 120n, B: 110n },
            { subject: "English", A: 98n, B: 130n },
        ],
        {
            A: { color: "teal.solid" },
            B: { color: "purple.solid" },
        },
        { dataKey: "subject" }
    );
});
chartRadarExample.toIR().compile([])();

// ============================================================================
// BAR LIST
// ============================================================================

// File: src/charts/index.ts
// Export: Chart.BarList
const chartBarListExample = East.function([], UIComponentType, $ => {
    return Chart.BarList(
        [
            { name: "Chrome", value: 275, color: none },
            { name: "Safari", value: 200, color: none },
        ],
        { showValue: true }
    );
});
chartBarListExample.toIR().compile([])();

// ============================================================================
// BAR SEGMENT
// ============================================================================

// File: src/charts/index.ts
// Export: Chart.BarSegment
const chartBarSegmentExample = East.function([], UIComponentType, $ => {
    return Chart.BarSegment(
        [
            { name: "Completed", value: 75, color: some("green.solid") },
            { name: "Remaining", value: 25, color: some("gray.solid") },
        ],
    );
});
chartBarSegmentExample.toIR().compile([])();

console.log("Charts TypeDoc examples compiled and executed successfully!");
