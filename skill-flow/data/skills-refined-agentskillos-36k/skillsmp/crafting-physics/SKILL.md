---
name: crafting-physics
description: Apply Sigil design physics to UI components - detects effect, applies behavioral/animation/material physics
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Crafting Physics Skill

Design physics enforcement for UI components. Detects effect, applies physics, validates compliance.

## Quick Reference

### Modes

| Mode | Trigger | Purpose | Tokens |
|------|---------|---------|--------|
| **Chisel** | Default, single component | Generate/refine one component | ~2,500 |
| **Hammer** | "build", "feature", multi-file | Full-stack with Loa orchestration | ~4,000 |
| **Debug** | "fix", "broken", "error" | Systematic investigation | ~3,600 |
| **Explore** | "how does", "?", understand | Research and discovery | ~2,000 |

### Effects

| Effect | Sync | Timing | Confirmation |
|--------|------|--------|--------------|
| Financial | Pessimistic | 800ms | Required |
| Destructive | Pessimistic | 600ms | Required |
| Soft Delete | Optimistic | 200ms | Toast+Undo |
| Standard | Optimistic | 200ms | None |
| Local State | Immediate | 100ms | None |

### Detection Priority

1. **Types** → `Currency`, `Wei`, `Token`, `BigInt` = Financial
2. **Keywords** → claim, delete, like, toggle (see `fragments/detection.md`)
3. **Context** → "with undo", "for wallet" modifies effect

## Directory Structure

```
.claude/skills/crafting-physics/
├── SKILL.md              # This file (quick reference)
├── index.yaml            # RLM routing configuration
├── modes/
│   ├── chisel.md         # Default: single-component workflow
│   ├── hammer.md         # Multi-file: Loa orchestration
│   ├── debug.md          # Diagnostic: systematic investigation
│   └── explore.md        # Research: understanding codebases
└── fragments/
    ├── physics-table.md  # Effect → Physics mapping
    ├── protected-caps.md # Non-negotiable capabilities
    ├── feedback-loop.md  # Signal collection (ACCEPT/MODIFY/REJECT)
    └── detection.md      # Effect detection algorithm
```

## Fragment Usage

Fragments are loaded via `{{fragment:name}}` syntax:

```
{{fragment:physics-table}}    # Insert physics lookup table
{{fragment:protected-caps}}   # Insert capability checklist
{{fragment:feedback-loop}}    # Insert feedback collection
{{fragment:detection}}        # Insert effect detection
```

## Token Budget

| Scenario | Load | Est. Tokens |
|----------|------|-------------|
| Simple component | Chisel + physics-table | ~3,000 |
| Financial component | Chisel + protected-caps | ~3,500 |
| Multi-file feature | Hammer | ~4,000 |
| Bug investigation | Debug | ~3,600 |
| Codebase research | Explore | ~2,000 |

**Target: ~85% reduction from 32k monolith**

## Protected Capabilities

Non-negotiable (see `fragments/protected-caps.md`):

- **Withdraw** → Always reachable (never hide behind loading)
- **Cancel** → Always visible (every flow needs escape)
- **Balance** → Always accurate (invalidate on mutation)
- **Touch target** → ≥44px minimum
- **Focus ring** → Always visible

## Mode Selection Algorithm

On `/craft` invocation, select mode using this priority:

```
1. Check iteration count (from craft-state.md)
   → iteration >= 3 AND same component → Debug mode

2. Check for error context
   → "fix", "broken", "error", "not working", "fails" → Debug mode

3. Check for exploration signals
   → Ends with "?" OR "how does", "what is", "explain" → Explore mode

4. Check for multi-file signals
   → "build feature", "implement", "refactor all", "across" → Hammer mode

5. Default
   → Chisel mode (single-component workflow)
```

### Mode Triggers (Detailed)

| Mode | Triggers | Priority |
|------|----------|----------|
| Debug | iteration >= 3, "fix", "broken", "error", "not working", error context present | 1 |
| Explore | "?", "how does", "what is", "why does", "explain", "understand" | 2 |
| Hammer | "build", "feature", "implement", "system", "refactor all", multi-file scope | 3 |
| Chisel | Default when no other mode matches | 4 |

## Continuation Behavior

On continuation within same session:

1. **Read craft-state.md** for current component, iteration, loaded fragments
2. **Skip already-loaded fragments** (except feedback-loop, always needed)
3. **Increment iteration count** in craft-state.md
4. **Check for loop patterns** - if iteration >= 3 with same issue, suggest escalation

### Fragment Skip Rules

| Fragment | Skip on Continuation? |
|----------|----------------------|
| physics-table | Yes, if effect unchanged |
| protected-caps | Yes, if already verified |
| detection | Yes, if effect determined |
| feedback-loop | Never skip (needed for signals) |

## Escalation Paths

```
Chisel → Hammer   (when scope grows to 2+ domains)
Debug  → Hammer   (when fix requires architecture changes)
Explore → Hammer  (when exploration reveals infrastructure needs)
```

## When NOT to Use /craft

- **Only animation wrong** → `/animate`
- **Only styling wrong** → `/style`
- **Only timing wrong** → `/behavior`
- **1-3 line change** → Edit tool directly
- **Non-UX code** → Backend logic, tests (physics don't apply)

## Taste Logging

All signals append to `grimoires/sigil/taste.md`:

| Signal | Weight | Trigger |
|--------|--------|---------|
| ACCEPT | +1 | User confirms, uses as-is |
| MODIFY | +5 | User edits generated code |
| REJECT | -3 | User says no, rewrites |

After 3+ similar modifications → apply learned preference automatically.
