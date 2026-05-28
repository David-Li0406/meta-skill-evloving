---
name: flow-next-prime
description: Use this skill when you need a comprehensive assessment of your codebase for agent and production readiness, providing targeted fixes and visibility into code health.
---

# Skill body

## Overview

The Flow Prime skill performs a thorough assessment of your codebase, inspired by Factory.ai's Agent Readiness framework. It evaluates 8 key pillars across 48 criteria, offering fixes for agent readiness issues while reporting on production readiness.

## Role

- **Readiness Assessor**: Evaluates the current state of the codebase.
- **Improvement Proposer**: Suggests targeted fixes to enhance agent readiness.

## Input

Full request: `$ARGUMENTS`

### Accepts:
- No arguments (scans the current repository)
- `--report-only` or `report only` (skips remediation, just shows the report)
- `--fix-all` or `fix all` (applies all agent readiness fixes without confirmation)
- Path to a different repository root

### Examples:
- `/flow-next:prime`
- `/flow-next:prime --report-only`
- `/flow-next:prime ~/other-project`

## The Eight Pillars

### Agent Readiness (Pillars 1-5) — Fixes Offered

| Pillar | What It Checks |
|--------|----------------|
| **1. Style & Validation** | Linters, formatters, type checking, pre-commit hooks |
| **2. Build System** | Build tools, commands, lock files, monorepo tooling |
| **3. Testing** | Test framework, commands, coverage, verification |
| **4. Documentation** | README, CLAUDE.md, setup docs, architecture |
| **5. Dev Environment** | .env.example, Docker, devcontainer, runtime version |

### Production Readiness (Pillars 6-8) — Report Only

| Pillar | What It Checks |
|--------|----------------|
| **6. Observability** | Logging, tracing, metrics, error tracking, health endpoints |
| **7. Security** | Branch protection, secret scanning, CODEOWNERS, Dependabot |
| **8. Workflow & Process** | CI/CD, PR processes |

## Why This Matters

Agents can waste significant time due to environmental issues, such as:
- Lack of pre-commit hooks leading to long CI waits.
- Undocumented environment variables causing confusion.
- Absence of a CLAUDE.md file that outlines project conventions.
- Missing test commands that prevent verification of changes.

The Flow Prime skill addresses these environmental problems, ensuring agents are ready to work efficiently.