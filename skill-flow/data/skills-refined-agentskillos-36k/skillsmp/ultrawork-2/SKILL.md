---
name: ultrawork
description: "This skill should be used when the user has a large, complex task requiring: (1) multi-file or multi-step implementation, (2) major refactoring or architecture changes, (3) new feature spanning multiple components. This skill should NOT be used for simple fixes, single-file edits, or quick questions. Activates strict verification with planning, success criteria, and evidence collection."
---

# Ultrawork Mode

## Overview

Ultrawork enforces **verification-first development** - a strict mode where every completion claim requires concrete evidence.

### Core Principles

1. **No implementation without planning** - Explore codebase, design approach, decompose into tasks
2. **No completion without evidence** - Every criterion needs proof (command output, test results)
3. **No partial work accepted** - "Should work" or "basic implementation" triggers automatic rejection

### Workflow Phases

```
PLANNING → EXECUTION → VERIFICATION → COMPLETE
    ↑                        │
    └── (Ralph Loop on fail) ←┘
```

| Phase | Description | Key Outputs |
|-------|-------------|-------------|
| **Planning** | Explore → Design → Task decomposition | design.md, tasks/*.json |
| **Execution** | Workers implement tasks in parallel waves | Code changes, evidence |
| **Verification** | Verifier audits ALL evidence against criteria | PASS/FAIL decision |

---

## Activation

Start ultrawork with the `/ultrawork` command:

```bash
/ultrawork "your goal"         # Interactive: asks questions, user approves plan
/ultrawork --auto "your goal"  # Auto: decides autonomously, no confirmations
/ultrawork --plan-only "goal"  # Planning only, no execution
```

### Mode Selection

| Mode | Best For | User Interaction |
|------|----------|------------------|
| **Interactive** (default) | Complex features, unclear requirements | Questions + approval |
| **Auto** (`--auto`) | Well-defined tasks, CI/CD | None |
| **Plan-only** (`--plan-only`) | Design review before implementation | Planning only |

---

## When to Use

**USE ultrawork for:**
- Multi-file implementations (3+ files)
- Architecture changes or refactoring
- New features with design decisions
- Work requiring verification trails

**DON'T use ultrawork for:**
- Single-file edits or bug fixes
- Documentation updates
- Quick questions or exploration
- Tasks completable in < 5 minutes

---

## Zero Tolerance Rules

Verification automatically **FAILS** if output contains blocked patterns.

See `references/blocked-patterns.md` for complete list.

**Common blocked phrases:**
- "should work", "probably works"
- "basic implementation", "simplified version"
- "TODO", "FIXME", "not implemented"

---

## Evidence Requirements

Every completion claim requires concrete proof.

| Claim | Required Evidence |
|-------|-------------------|
| "Tests pass" | `npm test` output with exit code 0 |
| "Build succeeds" | Build command output with exit code 0 |
| "Feature works" | Demo, test output, or screenshot |
| "Bug fixed" | Before/after comparison |

See `references/verification-protocol.md` for detailed verification requirements.

---

## Session State

Each session has isolated state in `~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}/`.

See `references/state-schema.md` for complete schema documentation.

**Key files:**
- `session.json` - Phase, options, metadata
- `context.json` - Exploration summaries
- `exploration/*.md` - Detailed findings
- `tasks/*.json` - Task definitions and evidence

---

## Related Commands

| Command | Purpose |
|---------|---------|
| `/ultrawork-status` | Check current phase and progress |
| `/ultrawork-evidence` | View collected evidence log |
| `/ultrawork-clean` | Clean up sessions (interactive/all/stale) |
| `/ultrawork-exec` | Execute existing plan |
| `/ultrawork-plan` | Planning phase only |

---

## Additional Resources

### Reference Files

- **`references/blocked-patterns.md`** - Complete list of blocked phrases and why
- **`references/verification-protocol.md`** - Detailed verification requirements
- **`references/state-schema.md`** - Session and task JSON schemas
