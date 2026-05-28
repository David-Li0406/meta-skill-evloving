---
name: standardized-branch-creation
description: Use this skill when you need to create standardized Git branches with consistent naming based on task descriptions, ensuring clarity and organization in your development workflow.
---

# Branch Workflow — Standardized Branch Creation

> Create working branches with consistent naming from task descriptions. Platform agnostic.

**Works with or without `aoc` CLI.** Uses standard git commands.

---

## Purpose

Standardize branch creation with:
1. **Type detection** — Auto-detect bug/feature/refactor from description.
2. **Issue ID extraction** — JIRA, GitHub, or internal issue references.
3. **Slug generation** — Short, URL-safe names from descriptions.
4. **Worktree setup** — Parallel development without branch switching.
5. **Clean branch integration** — Seamless handoff to selective-copy.

---

## CRITICAL: No Assumptions

> **NEVER assume. NEVER guess. ALWAYS ask.**

**Before creating ANY branch, confirm with user:**

| If unclear about... | ASK |
|---------------------|-----|
| Task description | "What is the task? Please include issue ID if available." |
| Source branch | "Which branch should I base this on? (e.g., develop, main)" |
| Branch type | "I detected this as a [type]. Is that correct?" |
| Issue ID | "I found [ID]. Is this the correct issue reference?" |
| Generated name | "I'll create branch `{name}`. Does this look right?" |

**If ANY of these are ambiguous:**
1. Stop.
2. Ask ONE question at a time.
3. Wait for explicit confirmation.
4. Only proceed when ALL inputs are confirmed.

**NEVER:**
- Guess the source branch.
- Assume `main` or `develop` without asking.
- Create a branch without showing the user the exact name first.
- Proceed if the task description is vague.

---

## Branch Naming Convention

```
Working branch: {type}/{ID}-{slug}-WB
Clean branch:   {type}/{ID}-{slug}
```

**Examples:**
| Task | Working Branch | Clean Branch |
|------|---------------|--------------|
| "GATS-0666: Add auth support" | `feature/GATS-0666-add-auth-WB` | `feature/GATS-0666-add-auth` |
| "Fix #123 login timeout" | `bugfix/123-login-timeout-WB` | `bugfix/123-login-timeout` |
| "Refactor database layer" | `refactor/db-layer-WB` | `refactor/db-layer` |

---

## Invocation

User says something like:
- "Create a branch for GATS-0666: Add authentication"
- "Start working on feature for issue #123"
- "I need a branch for refactoring the database layer."