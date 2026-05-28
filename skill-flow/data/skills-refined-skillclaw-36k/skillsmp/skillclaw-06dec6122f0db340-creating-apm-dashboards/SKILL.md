---
name: creating-apm-dashboards
description: Use this skill when you need to create Application Performance Monitoring (APM) dashboards to visualize key metrics and monitor application health across platforms like Grafana and Datadog.
---

# Skill body

## Overview

This skill automates the creation of Application Performance Monitoring (APM) dashboards, providing a structured approach to visualizing critical application metrics. By defining key performance indicators and generating dashboard configurations, this skill simplifies the process of monitoring application health and performance.

## How It Works

1. **Identify Requirements**: Determine the specific metrics and visualizations needed for the APM dashboard based on the user's request.
2. **Define Dashboard Components**: Select relevant components such as golden signals (latency, traffic, errors, saturation), request metrics, resource utilization, database metrics, cache metrics, business metrics, and error tracking.
3. **Generate Configuration**: Create the dashboard configuration file based on the selected components and user preferences.
4. **Deploy Dashboard**: Deploy the generated configuration to the target monitoring platform (e.g., Grafana, Datadog).

## When to Use This Skill

This skill activates when you need to:
- Create a new APM dashboard for an application.
- Define key metrics and visualizations for monitoring application performance.
- Generate dashboard configurations for Grafana, Datadog, or other monitoring platforms.

## Examples

### Example 1: Creating a Grafana Dashboard

User request: "Create a Grafana dashboard for monitoring my web application's performance."

The skill will:
1. Identify the need for a Grafana dashboard focused on web application performance.
2. Define dashboard components including request rate, response times, error rates, and resource utilization (CPU, memory).
3. Generate a Grafana dashboard configuration file with pre-defined visualizations for these metrics.