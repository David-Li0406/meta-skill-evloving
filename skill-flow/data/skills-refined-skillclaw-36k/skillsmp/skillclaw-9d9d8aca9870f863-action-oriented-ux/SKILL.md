---
name: action-oriented-ux
description: Use this skill when designing sales engagement interfaces and workflows that prioritize quick actions on leads, aiming for a time-to-action of under 2 minutes.
---

# Skill body

## Purpose

Design sales engagement interfaces, lead processing workflows, and outreach dashboards where the primary output is taking action on prioritized items. This skill is applicable in high-velocity sales environments, lead queues, or any interface requiring rapid decision-making.

## Core Philosophy: From Insight to Orchestration

Traditional dashboards often lead users to spend 80% of their time navigating and only 20% acting. Modern platforms aim to invert this ratio, allowing users to focus on execution rather than management.

### The "System of Action" Philosophy

| Decision | Legacy (User Decides) | Modern (System Decides) |
|----------|----------------------|------------------------|
| **Who** | Browse list, pick someone | AI-ranked priority queue |
| **When** | Check calendar, guess timing | Timing signals + decay |
| **What** | Write from scratch | Pre-drafted with variables |
| **How** | Choose channel | Recommended based on context |

**The user executes, not manages.**

## The 2-Minute Lead Loop

| Time | Activity |
|------|----------|
| 0:00-0:05 | System highlights the next prioritized lead (auto-selected, context pre-loaded) |
| 0:05-0:30 | User scans "Why now" signals + last touch |
| 0:30-1:30 | User reviews draft + edits 1-3 fields (opener, hook, CTA) |
| 1:30-2:00 | Send/log/advance with non-blocking feedback |

## Layout Architecture: The Three-Zone Model

### The Split-Screen Player

```
┌──────────┬─────────────────────────┬───────────────────┐
│  QUEUE   │        CONTEXT          │      ACTION       │
│  (Left)  │        (Centre)         │   (Right/Dock)    │
│  30-40%  │        40-50%           │      20-30%       │
└──────────┴─────────────────────────┴───────────────────┘
```

## Related Skills

- `adhd-interface-design` — For cognitive load patterns and focus modes
- `notification-system` — For alert delivery and batching
- `b2b-visualisation` — For signal badges and data display
- `uk-police-design-system` — For visual tokens and components