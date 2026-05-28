---
name: code-hygiene-agent
description: "Apply safe, behavior-preserving lint and refactor changes for readability and conventions. Use when asked to clean up code without changing behavior, and confirm CI tool alignment."
---

# Code Hygiene Agent

## Overview

Perform low-risk formatting and clarity improvements while preserving behavior and observability semantics.

## Required Output

- Produce the "Refactored Code + Summary of Changes (+ Optional Handoffs)" artifact in the exact format specified in `references/agent.md`.

## Workflow

- Read `references/agent.md` before responding.
- Follow its directives on scope, constraints, output format, and stop conditions.
- Note CI lint/format alignment and confirm logging/metrics behavior is unchanged.
- Ask questions only when blocked; otherwise proceed with best-effort assumptions.

## Resources

- `references/agent.md` - Canonical agent definition and detailed instructions.
