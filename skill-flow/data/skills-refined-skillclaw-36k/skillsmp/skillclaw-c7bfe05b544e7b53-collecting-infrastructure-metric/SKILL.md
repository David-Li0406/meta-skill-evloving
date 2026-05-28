---
name: collecting-infrastructure-metrics
description: Use this skill when you need to collect and analyze performance metrics across various infrastructure components to monitor system health and optimize resource utilization.
---

# Skill body

## Overview

This skill automates the process of setting up infrastructure metrics collection. It identifies key performance indicators (KPIs) across various infrastructure layers, configures agents to collect these metrics, and assists in setting up central aggregation and visualization.

## How It Works

1. **Identify Infrastructure Layers**: Determine the infrastructure layers to monitor (compute, storage, network, containers, load balancers, databases).
2. **Configure Metrics Collection**: Set up agents (Prometheus, Datadog, CloudWatch) to collect metrics from the identified layers.
3. **Aggregate Metrics**: Configure central aggregation of the collected metrics for analysis and visualization.
4. **Create Dashboards**: Generate infrastructure dashboards for health monitoring, performance analysis, and capacity tracking.

## When to Use This Skill

This skill activates when you need to:
- Monitor the performance of your infrastructure.
- Identify bottlenecks in your system.
- Set up dashboards for real-time monitoring.

## Examples

### Example 1: Setting up basic monitoring

User request: "Collect infrastructure metrics for my web server."

The skill will:
1. Identify compute, storage, and network layers relevant to the web server.
2. Configure Prometheus to collect CPU, memory, disk I/O, and network bandwidth metrics.

### Example 2: Troubleshooting database performance

User request: "I'm seeing slow database queries. Can you help me monitor the database performance?"

The skill will:
1. Identify the database layer and relevant metrics such as connection pool usage, replication lag, and cache hit rates.
2. Configure Datadog to collect these metrics and create a dashboard to visualize performance trends.

## Best Practices

- **Agent Selection**: Choose the appropriate agent (Prometheus, Datadog, CloudWatch) based on your existing infrastructure and monitoring needs.