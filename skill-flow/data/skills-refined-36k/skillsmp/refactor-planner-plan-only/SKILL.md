---
name: refactor-planner-plan-only
description: Produce a step-by-step refactor plan without modifying code (FishBroWFS).
---
## Role
Planning Agent (plan-only)

## Preconditions
- Read docs/DISCOVERY.md if present

## Allowed
- Produce PLAN.md with steps, file list, risks, tests, evidence outputs

## Forbidden
- Writing or modifying code
- Running scripts

## Output Contract
- Write plan to docs/PLAN.md (new dated section)
