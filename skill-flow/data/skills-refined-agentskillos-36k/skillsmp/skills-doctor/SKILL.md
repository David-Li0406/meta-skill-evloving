---
name: skills-doctor
description: Validate that the current VM has the right `agent-skills` installed for the repo you’re working in.
---

# skills-doctor

## Description

Validate that the current VM has the right `agent-skills` installed for the repo you’re working in.

This is a **soft** doctor: it reports issues and suggested fixes, but should not block work.

**Use when**:
- Agents are missing required skills (dx-doctor, lockfile-doctor, railway-doctor, etc.)
- You suspect `~/.agent/skills` is stale on a VM
- You want a quick “is my skills stack correct for this repo?” check

## How it works

- Picks a repo profile from `skill-profiles/` based on your repo’s `origin` remote URL.
- Checks that each required skill directory exists under `~/.agent/skills` (or `AGENT_SKILLS_DIR`).
- Prints a small actionable summary.

## Usage

```bash
# From inside a repo (prime-radiant-ai, affordabot, llm-common)
~/.agent/skills/skills-doctor/check.sh
```

Optional overrides:

```bash
export AGENT_SKILLS_DIR="$HOME/.agent/skills"
export SKILLS_DOCTOR_PROFILE="prime-radiant-ai"   # or affordabot, llm-common
~/.agent/skills/skills-doctor/check.sh
```

