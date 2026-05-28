---
name: detecting-performance-regressions
description: Use this skill to automatically detect performance regressions in a CI/CD pipeline by analyzing performance metrics against baselines or thresholds.
---

# Performance Regression Detector

This skill automates the detection of performance regressions within a CI/CD pipeline, providing insights into potential performance bottlenecks and helping maintain application performance.

## Overview

The skill utilizes methods such as baseline comparison, statistical analysis, and threshold violation checks to identify performance degradation.

## How It Works

1. **Analyze Performance Data**: Gather performance metrics from the CI/CD environment.
2. **Detect Regressions**: Employ baseline comparison, statistical analysis, and threshold checks to detect regressions.
3. **Report Findings**: Generate a report summarizing detected performance regressions and their potential impact.

## When to Use This Skill

Activate this skill when you need to:
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
3. Generate a report highlighting any throughput degradation, indicating a potential performance regression.

## Best Practices

- **Define Baselines**: Establish clear and representative performance baselines for accurate comparison.
- **Set Thresholds**: Configure appropriate thresholds for identifying significant performance regressions.
- **Monitor Key Metrics**: Focus on monitoring critical performance metrics relevant to the application's behavior.

## Integration

This skill can be integrated with other CI/CD tools to automatically trigger regression detection upon new builds or code merges. It can also be combined with reporting plugins to generate detailed performance reports.

## Prerequisites

- Historical performance baselines in a specified directory.
- Access to CI/CD performance metrics.
- Statistical analysis tools.
- Defined regression thresholds.

## Output

- Performance regression detection report.
- Statistical comparison with baselines.
- List of regressed metrics with severity.
- Visualization of performance trends.
- Recommendations for investigation.

## Error Handling

If regression detection fails:
- Verify baseline data availability.
- Check metrics collection configuration.
- Validate statistical analysis parameters.
- Ensure threshold definitions are valid.
- Review CI/CD integration setup.

## Resources

- Statistical process control for performance testing.
- CI/CD performance testing best practices.
- Regression detection algorithms.
- Performance monitoring strategies.