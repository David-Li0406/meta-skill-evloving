---
name: claude
description: Large slice integration for org run claude requests. Use when asked to connect multiple parts of the product into a single coherent flow.
---

# Claude

## Overview

Integrate large slices across the app with minimal coupling and clear ownership.

## Workflow

### 1) Identify slice boundaries

- List all surfaces touched (API, UI, DB, docs).
- Claim locks for the relevant files in `docs/company/locks.md`.

### 2) Plan integration

- Define the minimal working vertical slice.
- Identify required dependencies and missing glue code.

### 3) Execute

- Implement in small, testable steps.
- Coordinate with other agents to avoid overlapping diffs.

### 4) Output

- Summarize the integration and any follow-ups.
