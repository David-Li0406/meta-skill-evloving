---
name: task-generator  
description: Generates engagement task timelines (T-28 to T+3) with business day calculations excluding weekends. Outputs Planner-ready CSV files. Use when generating tasks, creating timelines, or when user mentions task lists, Planner import, or business day calculations.
---

# Task Generator

Generates 15-task timelines with business day calculations.

## Usage

```bash
python scripts/business_days.py "[Customer]" "YYYY-MM-DD"
```

## Task Template

```
T-28: Schedule Internal Precall
T-22: Research customer
T-21: Execute Internal Precall
T-20: Draft Agenda
T-20: Schedule Customer Precall
T-14: Execute Customer Precall
T-14: Schedule internal resources
T-10: Validate Agenda with ATU
T-7: Validate Agenda with Customer
T-7: Prep Demos
T-3: Confirm all Customer pre-work
T-0: Send Satisfaction Survey
T+2: Conduct MSFT Debrief
T+2: Share Engagement Materials
T+3: Complete Engagement Close out form
```

## Business Day Rules

- Excludes weekends (Saturday/Sunday)
- T-28 = 28 business days BEFORE engagement
- T+2 = 2 business days AFTER engagement

Example (Engagement: Monday, Jan 20, 2026):
- T-28 → Wednesday, Dec 11, 2025
- T+2 → Wednesday, Jan 22, 2026

## CSV Output Format

```csv
Task Name,Assignment,Start date,Due date,Bucket,Progress,Priority,Labels
[Customer] - Draft Agenda,Brendon Colburn,12/23/2025,12/23/2025,2026-01-20 - [Customer],Not started,Medium,Add label
```

Import to Planner: "..." → "Import plan from Excel"

## Timeline Status

Shows current position:
- T-40+: Early (no tasks yet)
- T-28 to T-14: Active planning
- T-14 to T-0: Final prep
- T+1 to T+3: Follow-up
- T+4+: Complete

## Integration

Called by: engagement-initiator  
Standalone: Generate tasks without full engagement setup

## Reference

See [references/power_automate_flow.json](references/power_automate_flow.json) for original automation template.
