---
name: detecting-performance-regressions
description: Use this skill when you need to automatically detect performance regressions in a CI/CD pipeline by analyzing performance metrics against established baselines or thresholds.
---

# Skill body

## Overview

This skill automates the detection of performance regressions within a CI/CD pipeline. It utilizes methods such as baseline comparison, statistical analysis, and threshold violation checks to identify performance degradation, providing insights into potential performance bottlenecks.

## How It Works

1. **Analyze Performance Data**: Gather performance metrics from the CI/CD environment.
2. **Detect Regressions**: Employ methods like baseline comparison, statistical analysis, and threshold checks to identify regressions.
3. **Report Findings**: Generate a report summarizing detected performance regressions and their potential impact.

## When to Use This Skill

This skill activates when you need to:
- Identify performance regressions in a CI/CD pipeline.
- Analyze performance metrics for potential degradation.
- Compare current performance against historical baselines.

## Examples

### Example 1: Identifying a Response Time Regression

User request: "Detect performance regressions in the latest build. Specifically, check for increases in response time."

The skill will:
1. Analyze response time metrics from the latest build.
2. Compare the response times against a historical baseline.
3. Report any statistically significant increases in response time that exceed a defined threshold.

### Example 2: Detecting Throughput Degradation

User request: "Analyze throughput for performance regressions after the recent code merge."

The skill will:
1. Gather throughput data (requests per second) from the post-merge CI/CD run.
2. Compare the throughput to pre-merge values, looking for statistically significant drops.
3. Generate a report highlighting any throughput degradation.