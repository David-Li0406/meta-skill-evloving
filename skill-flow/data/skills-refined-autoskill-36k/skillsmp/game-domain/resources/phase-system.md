# Phase System

Complete reference for the phase cycle in ActionPhase.

## Phase Types

```sql
phase_type CHECK (phase_type IN ('common_room', 'action', 'results'))
```

## Phase Cycle

COMMON ROOM → ACTION → RESULTS → (repeat)

## Phase Properties

- phase_number: Sequential (1, 2, 3, ...)
- is_active: Only ONE active phase per game
- start_time, end_time, deadline
- title, description

## Advancement Rules

**Common Room → Action**
- GM initiates
- Sets action deadline
- API: `POST /api/v1/phases/advance`

**Action → Results**
- Deadline reached OR GM advances
- Actions locked
- GM sees all submissions

**Results → Common Room**
- GM completes results
- Starts new cycle
- Phase number increments

---

**Back to**: [SKILL.md](../SKILL.md)
