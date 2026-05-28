---
name: creating-alerting-rules
description: Use this skill when you need to create intelligent alerting rules for proactive performance monitoring, helping to define thresholds, routing, and escalation policies.
---

# Skill body

## Overview

This skill automates the creation of comprehensive alerting rules, reducing the manual effort required for performance monitoring. It guides you through defining alert categories, setting intelligent thresholds, and configuring routing and escalation policies. The skill also helps generate runbooks and establish alert testing procedures.

## How It Works

1. **Identify Alert Category**: Determine the type of alert to create (e.g., latency, error rate, resource utilization).
2. **Define Thresholds**: Set appropriate thresholds to avoid alert fatigue and ensure timely notification of performance issues.
3. **Configure Routing and Escalation**: Establish routing policies to direct alerts to the appropriate teams and escalation policies for timely response.
4. **Generate Runbook**: Create a basic runbook with steps to diagnose and resolve the alerted issue.

## When to Use This Skill

This skill activates when you need to:
- Implement performance monitoring for a new service.
- Refine existing alerting rules to reduce false positives.
- Create alerts for specific performance metrics, such as latency or error rate.

## Examples

### Example 1: Setting up Latency Alerts

User request: "create latency alerts for the payment service"

The skill will:
1. Prompt for latency thresholds (e.g., warning and critical).
2. Configure alerts to trigger when latency exceeds defined thresholds.

### Example 2: Creating Error Rate Alerts

User request: "set up alerting for error rate increases in the API gateway"

The skill will:
1. Request the baseline error rate and acceptable deviation.
2. Configure alerts to trigger when the error rate exceeds the defined deviation from the baseline.

## Best Practices

- **Threshold Selection**: Use historical data and statistical analysis to determine appropriate thresholds that minimize false positives and negatives.