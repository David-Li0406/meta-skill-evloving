---
name: tracking-resource-usage
description: Use this skill when you need to monitor and optimize resource usage across an application stack, especially for insights into performance bottlenecks and cost optimization opportunities.
---

# Skill body

## Overview

This skill provides a comprehensive solution for monitoring and optimizing resource usage within an application. It leverages the resource-usage-tracker plugin to gather real-time metrics, identify performance bottlenecks, and suggest optimization strategies.

## How It Works

1. **Identify Resources**: The skill identifies the resources to be tracked based on the user's request and the application's configuration (CPU, memory, disk I/O, network I/O, etc.).
2. **Collect Metrics**: The plugin collects real-time metrics for the identified resources, providing a snapshot of current resource consumption.
3. **Analyze Data**: The skill analyzes the collected data to identify performance bottlenecks, resource imbalances, and potential optimization opportunities.
4. **Provide Recommendations**: Based on the analysis, the skill provides specific recommendations for optimizing resource allocation, right-sizing instances, and reducing costs.

## When to Use This Skill

This skill activates when you need to:
- Identify performance bottlenecks in an application.
- Optimize resource allocation to improve efficiency.
- Reduce cloud infrastructure costs by right-sizing instances.
- Monitor resource usage in real-time to detect anomalies.
- Track the impact of code changes on resource consumption.

## Examples

### Example 1: Identifying Memory Leaks

User request: "Track memory usage and identify potential memory leaks."

The skill will:
1. Activate the resource-usage-tracker plugin to monitor memory usage (heap, stack, RSS).
2. Analyze the memory usage data over time to detect patterns indicative of memory leaks.
3. Provide recommendations for identifying and resolving the memory leaks.

### Example 2: Optimizing Database Connection Pool

User request: "Optimize database connection pool utilization."

The skill will:
1. Activate the resource-usage-tracker plugin to monitor database connection metrics.
2. Analyze the connection usage patterns and provide recommendations for optimizing the connection pool.