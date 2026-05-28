---
name: inspire-monitoring-observability
description: Inspire team logging standards, alerting guidelines, and monitoring setup. Use when implementing observability or debugging production issues.
user-invocable: false
allowed-tools: Read
---

# Inspire Team Monitoring & Observability Context

When this skill is activated, load the following monitoring documentation:

## Required Context Files

Read these files to understand the Inspire team's observability practices:

1. **Logging Standards**: `./references/logging-standards.md`
   - Log levels and usage
   - Structured logging format
   - Sensitive data handling

2. **Alerting Guidelines**: `./references/alerting-guidelines.md`
   - Alert severity levels
   - Escalation procedures
   - On-call expectations

3. **Monitoring Setup**: `./references/monitoring-setup.md`
   - Metrics to track
   - Dashboard setup
   - Health checks

## Instructions

Before responding to monitoring questions:
1. Use the Read tool to load relevant files above
2. Follow the team's logging standards
3. Reference alerting guidelines for incident response

## When to Load This Context

- Adding logging to code
- Setting up alerts
- Debugging production issues
- Creating dashboards
