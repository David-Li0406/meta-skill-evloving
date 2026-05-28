---
name: gh-actions-scheduler
description: GitHub Actions workflows for FAA data pipelines. Use when automating AIRAC cycle updates, scheduling chart downloads, or building data release workflows. Includes AIRAC date calculations and workflow templates.
---

# GitHub Actions Scheduler

## Overview

Automate FAA data updates using GitHub Actions workflows aligned with AIRAC cycles.

## AIRAC Cycles

FAA publishes navigation data on 28-day cycles:
- **NASR/CIFP**: Every cycle (28 days)
- **Charts**: Every other cycle (56 days)
- **DOF**: Daily updates

## Quick Start

### Calculate Next AIRAC Date

```python
from calculate_airac import get_next_airac, get_cycle_id

next_date = get_next_airac()
cycle_id = get_cycle_id(next_date)
print(f"Next cycle: {cycle_id} on {next_date}")
```

### Generate Workflow

```python
from generate_workflow import generate_nasr_workflow

workflow = generate_nasr_workflow(
    cycle_dates=['2025-01-23', '2025-02-20', '2025-03-20'],
    output_artifact='aviation-data'
)
```

## Workflow Templates

| Template | Schedule | Description |
|----------|----------|-------------|
| `nasr-update.yml` | AIRAC cycle | Download and parse NASR data |
| `charts-update.yml` | 56 days | Download d-TPP chart PDFs |
| `obstacles-daily.yml` | Daily | Update DOF obstacle data |
| `release-data.yml` | AIRAC cycle | Create data release |

## 2025-2026 AIRAC Schedule

```
Cycle  Effective Date
2501   2025-01-23
2502   2025-02-20
2503   2025-03-20
2504   2025-04-17
2505   2025-05-15
2506   2025-06-12
2507   2025-07-10
2508   2025-08-07
2509   2025-09-04
2510   2025-10-02
2511   2025-10-30
2512   2025-11-27
2513   2025-12-25
2601   2026-01-22
```

## References

- Workflow patterns: `references/workflow_patterns.md`
- AIRAC cron expressions: `references/airac_crons.md`
- Artifact management: `references/artifact_management.md`

## Scripts

| Script | Description |
|--------|-------------|
| `generate_workflow.py` | Generate workflow YAML |
| `calculate_airac.py` | Calculate AIRAC dates |
