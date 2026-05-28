/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under AGPL-3.0. See LICENSE file for details.
 */

/**
 * Warehouse Operations Dashboard
 *
 * Demonstrates East UI components in a business operations context.
 * This example shows how East can be used to build modern dashboards
 * for optimizing operational performance.
 */

import { East, StructType, StringType, IntegerType, FloatType, ArrayType } from "@elaraai/east";
import {
    UIComponentType,
    Stack,
    Text,
    Card,
    Table,
    Badge,
    Stat,
    Progress,
    Chart,
    Sparkline,
    Separator,
    Grid,
    Box,
} from "@elaraai/east-ui";

// ============================================================================
// Data Types
// ============================================================================

const OrderType = StructType({
    id: StringType,
    customer: StringType,
    product: StringType,
    quantity: IntegerType,
    revenue: FloatType,
    status: StringType,
    priority: StringType,
    fulfillmentRate: IntegerType,
});

const DailyMetricType = StructType({
    day: StringType,
    orders: IntegerType,
    revenue: FloatType,
});

const WarehouseZoneType = StructType({
    zone: StringType,
    utilization: IntegerType,
});

// ============================================================================
// Dashboard Component
// ============================================================================

const example = East.function(
    [],
    UIComponentType,
    $ => {
        // Sample order data
        const orders = $.const([
            { id: "ORD-4521", customer: "Acme Corp", product: "Industrial Sensors", quantity: 250n, revenue: 12500.0, status: "Delivered", priority: "Standard", fulfillmentRate: 100n },
            { id: "ORD-4522", customer: "TechFlow Inc", product: "Control Units", quantity: 50n, revenue: 8750.0, status: "In Transit", priority: "Express", fulfillmentRate: 75n },
            { id: "ORD-4523", customer: "GlobalMfg", product: "Power Modules", quantity: 100n, revenue: 15000.0, status: "Processing", priority: "Rush", fulfillmentRate: 25n },
            { id: "ORD-4524", customer: "SmartBuild", product: "IoT Gateways", quantity: 75n, revenue: 6375.0, status: "Pending", priority: "Standard", fulfillmentRate: 0n },
            { id: "ORD-4525", customer: "DataDynamics", product: "Edge Servers", quantity: 20n, revenue: 28000.0, status: "Delivered", priority: "Express", fulfillmentRate: 100n },
        ], ArrayType(OrderType));

        // Weekly metrics for charts
        const weeklyMetrics = $.const([
            { day: "Mon", orders: 45n, revenue: 52000.0 },
            { day: "Tue", orders: 62n, revenue: 71000.0 },
            { day: "Wed", orders: 58n, revenue: 64000.0 },
            { day: "Thu", orders: 71n, revenue: 89000.0 },
            { day: "Fri", orders: 84n, revenue: 102000.0 },
        ], ArrayType(DailyMetricType));

        // Warehouse zone utilization
        const zones = $.const([
            { zone: "Zone A - Receiving", utilization: 78n },
            { zone: "Zone B - Storage", utilization: 92n },
            { zone: "Zone C - Picking", utilization: 65n },
            { zone: "Zone D - Shipping", utilization: 88n },
        ], ArrayType(WarehouseZoneType));

        // Revenue sparkline data
        const revenueSparkline = [32.5, 41.2, 38.7, 52.1, 48.3, 61.0, 55.8, 72.4];

        // Calculate summary statistics
        const totalRevenue = $.const(orders.sum(($, order) => order.revenue));
        const avgFulfillment = $.const(orders.mean(($, order) => order.fulfillmentRate.toFloat()));

        return Stack.VStack([
            // Header
            Text.Root("Warehouse Operations Dashboard", {
                fontSize: "lg",
                fontWeight: "bold",
                color: "gray.800",
            }),
            Text.Root("Real-time visibility into fulfillment performance", {
                fontSize: "sm",
                color: "gray.500",
            }),

            Separator.Root({ orientation: "horizontal" }),

            // KPI Cards Row
            Grid.Root([
                Grid.Item(
                    Card.Root([
                        Stat.Root("Total Revenue", East.str`$${East.print(totalRevenue.divide(1000.0))}K`, {
                            helpText: "+12.5% vs last week",
                            indicator: "up",
                        }),
                        Sparkline.Root(revenueSparkline, {
                            type: "area",
                            color: "teal.500",
                            height: '40px',
                        },)],
                        { variant: "outline", })
                    ,
                    { colSpan: "1", }
                ),
                Grid.Item(
                    Card.Root([
                        Stat.Root("Active Orders", "6", {
                            helpText: "2 pending",
                        }),
                    ], { variant: "outline" }),
                    { colSpan: "1" }
                ),
                Grid.Item(
                    Card.Root([
                        Stat.Root("Fulfillment Rate", East.str`${East.print(avgFulfillment)}%`, {
                            helpText: "On-time delivery",
                            indicator: East.greater(avgFulfillment, 75.0).ifElse(
                                $ => Stat.Indicator("up"),
                                $ => Stat.Indicator("down")
                            ),
                        }),
                    ], { variant: "outline" }),
                    { colSpan: "1" }
                ),
            ], { templateColumns: "repeat(3, 1fr)", gap: "4" }),

            // Orders Table
            Card.Root([
                Text.Root("Recent Orders", { fontWeight: "semibold", fontSize: "md" }),
                Table.Root(orders, {
                    id: { header: "Order ID" },
                    customer: { header: "Customer" },
                    product: { header: "Product" },
                    quantity: { header: "Qty" },
                    revenue: {
                        header: "Revenue",
                        render: value => Text.Root(East.str`$${East.print(value)}`, {
                            fontWeight: "medium",
                        }),
                    },
                    status: {
                        header: "Status",
                        render: value => Badge.Root(value, {
                            variant: "subtle",
                            colorPalette: "blue",
                        }),
                    },
                    priority: {
                        header: "Priority",
                        render: value => Badge.Root(value, {
                            variant: "outline",
                            colorPalette: "gray",
                        }),
                    },
                }, {
                    variant: "line",
                    size: "sm",
                    striped: true,
                    interactive: true,
                }),
            ], { title: "Order Management", variant: "elevated" }),

            // Warehouse Utilization
            Card.Root([
                Text.Root("Warehouse Utilization", { fontWeight: "semibold", fontSize: "md" }),
                Stack.VStack([
                    Stack.VStack([
                        Stack.HStack([
                            Text.Root(zones.get(0n).zone, { fontSize: "sm" }),
                            Text.Root(East.str`${East.print(zones.get(0n).utilization)}%`, {
                                fontSize: "sm",
                                fontWeight: "medium",
                            }),
                        ], { justify: "space-between" }),
                        Progress.Root(zones.get(0n).utilization.toFloat(), { colorPalette: "yellow", size: "sm" }),
                    ], { gap: "1" }),
                    Stack.VStack([
                        Stack.HStack([
                            Text.Root(zones.get(1n).zone, { fontSize: "sm" }),
                            Text.Root(East.str`${East.print(zones.get(1n).utilization)}%`, {
                                fontSize: "sm",
                                fontWeight: "medium",
                                color: "red.600",
                            }),
                        ], { justify: "space-between" }),
                        Progress.Root(zones.get(1n).utilization.toFloat(), { colorPalette: "red", size: "sm" }),
                    ], { gap: "1" }),
                    Stack.VStack([
                        Stack.HStack([
                            Text.Root(zones.get(2n).zone, { fontSize: "sm" }),
                            Text.Root(East.str`${East.print(zones.get(2n).utilization)}%`, {
                                fontSize: "sm",
                                fontWeight: "medium",
                                color: "green.600",
                            }),
                        ], { justify: "space-between" }),
                        Progress.Root(zones.get(2n).utilization.toFloat(), { colorPalette: "green", size: "sm" }),
                    ], { gap: "1" }),
                    Stack.VStack([
                        Stack.HStack([
                            Text.Root(zones.get(3n).zone, { fontSize: "sm" }),
                            Text.Root(East.str`${East.print(zones.get(3n).utilization)}%`, {
                                fontSize: "sm",
                                fontWeight: "medium",
                            }),
                        ], { justify: "space-between" }),
                        Progress.Root(zones.get(3n).utilization.toFloat(), { colorPalette: "yellow", size: "sm" }),
                    ], { gap: "1" }),
                ], { gap: "3" }),
            ], { title: "Capacity Overview", variant: "elevated" }),

            // Charts Row
            Grid.Root([
                Grid.Item(
                    Card.Root([
                        Chart.Bar(weeklyMetrics, {
                            orders: { color: "blue.solid" },
                        }, {
                            xAxis: { dataKey: "day" },
                            grid: Chart.Grid({ show: true }),
                        }),
                    ], { title: "Orders by Day", variant: "outline" }),
                    { colSpan: "1" }
                ),
                Grid.Item(
                    Card.Root([
                        Chart.Area(weeklyMetrics, {
                            revenue: { color: "teal.solid" },
                        }, {
                            xAxis: { dataKey: "day" },
                            grid: Chart.Grid({ show: true }),
                        }),
                    ], { title: "Revenue Trend", variant: "outline" }),
                    { colSpan: "1" }
                ),
            ], { templateColumns: "repeat(2, 1fr)", gap: "4" }),

        ], { gap: "6", padding: "6" });
    }
);

export default example;
