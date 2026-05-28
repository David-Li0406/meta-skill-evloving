---
title: Sprint Setup
description: Sprint initialization including directory structure, workflow configuration, and SPRINT.yaml format.
keywords: initialization, directory, workflow, setup, configuration, SPRINT.yaml
skill: orchestrating-sprints
---

# Sprint Setup

## Directory Structure

```text
.claude/
  workflows/              # Reusable workflow templates
    sprint-default.yaml   # Standard sprint workflow
    feature-standard.yaml # Feature development workflow
    bugfix-workflow.yaml  # Bug fix workflow
  sprints/
    YYYY-MM-DD_sprint-name/
      SPRINT.yaml         # Sprint input (workflow + steps)
      PROGRESS.yaml       # Compiled execution state (generated)
      context/            # Cached context per step
        step-1-plan.md
        _shared.md
      artifacts/          # Generated outputs
        prs/
        commits/
```

## SPRINT.yaml Format

```yaml
# Workflow-based sprint definition
workflow: sprint-default          # Reference to .claude/workflows/
steps:
  - prompt: |
      Implement user authentication with JWT tokens.
      Requirements: login, logout, token refresh endpoints.
  - prompt: |
      Add rate limiting to API endpoints.
      Use sliding window algorithm.
  - workflow: bugfix-workflow     # Optional: override workflow per step
    prompt: |
      Fix memory leak in websocket handler.
```

## SPRINT.yaml Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflow` | string | Yes | Default workflow from `.claude/workflows/` |
| `steps` | list | Yes | Steps to process in sprint |
| `steps[].prompt` | string | Yes | Step description/prompt |
| `steps[].workflow` | string | No | Override workflow for this step |
| `steps[].id` | string | No | Custom step ID (auto-generated if omitted) |
| `sprint-id` | string | No | Sprint identifier |
| `name` | string | No | Human-readable sprint name |
| `config` | object | No | Optional configuration overrides |

## Workflow Directory

The `.claude/workflows/` directory contains reusable workflow templates:

| File | Purpose |
|------|---------|
| `sprint-default.yaml` | Standard sprint: prepare → development → QA → deploy |
| `feature-standard.yaml` | Feature workflow: planning → implement → test → document |
| `bugfix-workflow.yaml` | Bug fix: diagnose → fix → verify |

Create custom workflows by adding new `.yaml` files to this directory.

## Initialization

```bash
# Create sprint directory structure
mkdir -p .claude/sprints/$(date +%Y-%m-%d)_sprint-name/{context,artifacts}

# Create SPRINT.yaml with workflow reference
cat > .claude/sprints/.../SPRINT.yaml << 'EOF'
workflow: sprint-default
steps:
  - prompt: |
      Your first task description here.
EOF

# Compile to generate PROGRESS.yaml (done automatically by /run-sprint)
node compiler/dist/index.js .claude/sprints/...
```

## Best Practices

| Practice | Rationale |
|----------|-----------|
| Name by date + focus | `2024-01-15_auth-improvements` - easy to locate |
| 3-8 steps per sprint | Manageable scope, clear progress |
| One concern per step | Clear completion criteria |
| Use step-specific workflows | Override when step needs different phases |
| Preview with `--dry-run` | Validate compilation before execution |
