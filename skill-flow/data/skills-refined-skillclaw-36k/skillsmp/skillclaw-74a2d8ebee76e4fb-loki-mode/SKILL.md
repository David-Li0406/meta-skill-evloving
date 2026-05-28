---
name: loki-mode
description: Use this skill when you need to orchestrate a multi-agent autonomous startup system that takes a product from PRD to fully deployed with zero human intervention.
---

# Skill body

## Overview
Loki Mode is a multi-agent autonomous startup system designed to manage various specialized agents across multiple domains, including engineering, QA, DevOps, security, data/ML, business operations, marketing, HR, and customer success. It automates the entire process from product requirements document (PRD) to a revenue-generating product.

## Features
- **Task Tool**: Dispatch subagents for various tasks.
- **Parallel Code Review**: Involves three specialized reviewers for efficient code assessment.
- **Severity-Based Issue Triage**: Automatically prioritizes issues based on severity.
- **Distributed Task Queue**: Manages tasks with dead letter handling.
- **Automatic Deployment**: Deploys to cloud providers without human intervention.
- **A/B Testing**: Facilitates testing of different versions of the product.
- **Customer Feedback Loops**: Integrates user feedback into the development process.
- **Incident Response**: Automatically responds to incidents.
- **Circuit Breakers and Self-Healing**: Ensures system reliability and recovery.
- **Rate Limit Handling**: Uses distributed state checkpoints and auto-resume with exponential backoff.

## Quick Reference

### Critical First Steps (Every Turn)
1. **READ** `.loki/CONTINUITY.md` - Your working memory + "Mistakes & Learnings"
2. **RETRIEVE** relevant memories from `.loki/memory/` (episodic patterns, anti-patterns)
3. **CHECK** `.loki/state/orchestrator.json` - Current phase/metrics
4. **REVIEW** `.loki/queue/pending.json` - Next tasks
5. **FOLLOW** RARV cycle: REASON, ACT, REFLECT, **VERIFY** (test your work!)
6. **OPTIMIZE** Opus=planning, Sonnet=development, Haiku=unit tests/monitoring - 10+ Haiku agents in parallel
7. **TRACK** efficiency metrics: tokens, time, agent count per task
8. **CONSOLIDATE** after task: Update episodic memory, extract patterns to semantic memory

### Key Files (Priority Order)
| File | Purpose | Update When |
|------|---------|-------------|
| `.loki/CONTINUITY.md` | Working memory - what am I doing NOW? | Every turn |
| `.loki/memory/semantic/` | Generalized patterns & anti-patterns | After task completion |
| `.loki/memory/episodic/` | Specific interaction traces | After each action |
| `.loki/metrics/efficiency/` | Task efficiency scores & rewards | After each task |
| `.loki/specs/openapi.yaml` | API spec - source of truth | Architecture changes |
| `CLAUDE.md` | Project context - architecture & patterns | Significant changes |
| `.loki/queue/*.json` | Task states | Every task change |

### Decision Tree: What To Do Next?
```
START
  |
  +-- Read CONTINUITY.md ----------+
  |                                |
  +--
```