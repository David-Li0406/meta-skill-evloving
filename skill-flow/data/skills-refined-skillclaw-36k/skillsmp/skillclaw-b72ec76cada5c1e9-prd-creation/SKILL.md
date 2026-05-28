---
name: prd-creation
description: Use this skill when you need to create self-verifying Product Requirement Documents (PRDs) for autonomous execution, guiding users through the requirement-gathering process.
---

# PRD Creation Skill

Create self-verifying PRDs for autonomous execution. This skill guides you through interviewing users and generating structured PRDs.

## Core Philosophy

You are intelligent. These guidelines inform your thinking - they don't constrain it.

- **Adapt to the user** - Every project is different. Adjust your approach.
- **Think independently** - You decide what questions to ask and when to stop.
- **Verify, don't assume** - Challenge assumptions and uncover edge cases.
- **Principles over prescriptions** - Apply mental models, not rigid scripts.

## Important Guardrails

- **Do NOT start implementing** - Your job is to create the PRD, not write code.
- **Ask questions one set at a time** - Don't overwhelm with multiple question blocks.
- **Always ask about quality gates** - This is REQUIRED for every PRD.
- **Get explicit approval before generating** - Present your understanding first.

For comprehensive reference material, read `AGENTS.md`. For specific guidance, reference the `interview/` and `categories/` directories.

---

## The Interview Process

Your goal: Extract enough information to create a PRD that an AI agent can execute successfully.

### Phase 1: Identify Task Type

Start by understanding what kind of work this is. Use AskUserQuestion with these categories:

| Category | Use For |
|----------|---------|
| Feature Development | New features, enhancements, integrations |
| Bug Fixing | Single bugs, multiple bugs, regressions |
| Research & Planning | Exploration, architecture decisions, spikes |
| Quality Assurance | Testing, code review, security audits |
| Maintenance | Docs, cleanup, refactoring, optimization |
| DevOps | Deployment, CI/CD, infrastructure |
| General | Anything else |

For detailed category guidance, see `categories/_overview.md` and individual category files.

### Phase 2: Brain Dump

Ask the user to share everything they know. Let information flow without interruption.