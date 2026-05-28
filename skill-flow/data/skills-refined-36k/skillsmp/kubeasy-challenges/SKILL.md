---
name: kubeasy-challenges
description: Manage Kubeasy Kubernetes learning challenges - create new challenges, review existing ones, or generate ideas from K8s documentation. Use when working with Kubeasy challenges in any capacity.
---

# Kubeasy Challenges

Unified skill for managing Kubeasy Kubernetes learning challenges.

## Workflow Selection

| User Intent | Reference to Read |
|-------------|-------------------|
| Create a new challenge | [references/create.md](references/create.md) |
| Review/test a challenge | [references/review.md](references/review.md) → spawns [agents/reviewer.md](agents/reviewer.md) |
| Generate challenge ideas | [references/ideas.md](references/ideas.md) |
| **Quick start / examples** | [references/prompts.md](references/prompts.md) |

## Common Resources

### MCP Tools

Always available via the Kubeasy MCP:

| Tool | Purpose |
|------|---------|
| `kubeasy:get_challenge_schema` | JSON schema for challenge.yaml + objectives |
| `kubeasy:get_challenges_types` | Available types (fix, build, migrate...) |
| `kubeasy:get_challenges_themes` | Available themes |
| `kubeasy:get_challenges` | List existing challenges (with filters) |

### Environment Paths

| Component | Path |
|-----------|------|
| Challenges repo | `/Users/paul/Workspace/kubeasy/challenges/` |
| CLI repo | `/Users/paul/Workspace/kubeasy/kubeasy-cli/` |
| CLI binary | `/Users/paul/Workspace/kubeasy/kubeasy-cli/kubeasy-cli` |
| API key | `/Users/paul/Workspace/kubeasy/api_key` |
| Challenge ideas | `/Users/paul/Workspace/kubeasy/challenges_ideas/` |

### Challenge Structure

```
<slug>/
├── challenge.yaml    # Metadata + objectives (required)
├── manifests/        # K8s manifests for broken state (required)
│   └── *.yaml
└── policies/         # Kyverno policies to prevent bypasses (optional)
    └── protect.yaml
```

### Repository Documentation

Read from the challenges repo before working:

| File | Content |
|------|---------|
| `CHALLENGE_GUIDELINES.md` | Philosophy, design principles, anti-patterns |

### Objective Types (Quick Reference)

| Type | Purpose |
|------|---------|
| `status` | Check resource conditions (Ready, Available) |
| `log` | Find strings in container logs |
| `event` | Detect forbidden K8s events (OOMKilled, Evicted) |
| `metrics` | Check restart count, replicas |
| `connectivity` | HTTP connectivity tests |

Full specs available via `kubeasy:get_challenge_schema`.

## Core Principles

From `CHALLENGE_GUIDELINES.md`:

1. **Mystery Preserving**: Never reveal root cause in descriptions
2. **Autonomy First**: Users solve with standard kubectl, no artificial constraints
3. **Validate Outcomes**: Check that it works, not how it was fixed
4. **Realism**: Mirror actual production incidents
