---
name: analyzing-system-throughput
description: Use this skill when you need to analyze system throughput, identify performance bottlenecks, or optimize system performance for increased capacity.
---

# Skill body

## Overview

This skill enables Claude to analyze and optimize system throughput using the `throughput-analyzer` plugin. It provides insights into request handling, data processing, and resource utilization.

## How It Works

1. **Identify Critical Components**: Determine which system components are most relevant to throughput.
2. **Analyze Throughput Metrics**: Gather and analyze current throughput metrics for the identified components.
3. **Identify Limiting Factors**: Pinpoint the bottlenecks and constraints that hinder optimal throughput.
4. **Evaluate Scaling Strategies**: Explore potential scaling strategies and their impact on overall throughput.

## When to Use This Skill

This skill activates when you need to:
- Analyze system throughput to identify performance bottlenecks.
- Optimize system performance for increased capacity.
- Evaluate scaling strategies to improve throughput.

## Examples

### Example 1: Analyzing Web Server Throughput

User request: "Analyze the throughput of my web server and identify any bottlenecks."

The skill will:
1. Activate the `throughput-analyzer` plugin.
2. Analyze request throughput, data throughput, and resource saturation of the web server.
3. Provide a report identifying potential bottlenecks and optimization opportunities.

### Example 2: Optimizing Data Processing Pipeline

User request: "Optimize the throughput of my data processing pipeline."

The skill will:
1. Activate the `throughput-analyzer` plugin.
2. Analyze data throughput, queue processing, and concurrency limits of the data processing pipeline.
3. Suggest improvements to increase data processing rates and overall throughput.

## Best Practices

- **Component Selection**: Focus the analysis on the most throughput-critical components to avoid unnecessary overhead.
- **Metric Interpretation**: Carefully interpret the metrics to make informed decisions on optimizations.