---
name: db-health-check
description: Run database security and performance checks and produce a health report. Use when the user asks for db security, performance, or health checks.
---
# Database Health Check

## Quick Start

1. Run security and performance checks.
2. Generate a consolidated report.
3. Summarize findings and remediation steps.

## Steps

- Use repo scripts:
  - `scripts/check-database-security.js`
  - `scripts/check-database-performance.js`
  - `scripts/generate-health-report.js`
- Reference `docs/DATABASE_PIPELINE.md` for expected output and thresholds.

## Output

- Report with issues grouped by severity.
- Clear remediation references (indexes, RLS, function `search_path`).
