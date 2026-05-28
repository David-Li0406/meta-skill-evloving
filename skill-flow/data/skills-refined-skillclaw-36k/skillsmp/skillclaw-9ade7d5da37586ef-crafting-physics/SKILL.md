---
name: crafting-physics
description: Use this skill when you need to apply Sigil design physics to UI components, detecting effects and applying behavioral, animation, or material physics.
---

# Crafting Physics Skill

Design physics enforcement for UI components. Detects effects, applies physics, and validates compliance.

## Quick Reference

### Modes

| Mode    | Trigger                          | Purpose                               | Tokens  |
|---------|----------------------------------|---------------------------------------|---------|
| **Chisel** | Default, single component       | Generate/refine one component         | ~2,500  |
| **Hammer** | "build", "feature", multi-file | Full-stack with Loa orchestration     | ~4,000  |
| **Debug**  | "fix", "broken", "error"      | Systematic investigation               | ~3,600  |
| **Explore** | "how does", "?", understand   | Research and discovery                | ~2,000  |

### Effects

| Effect        | Sync        | Timing  | Confirmation |
|---------------|-------------|---------|--------------|
| Financial     | Pessimistic | 800ms   | Required      |
| Destructive   | Pessimistic | 600ms   | Required      |
| Soft Delete   | Optimistic  | 200ms   | Toast+Undo    |
| Standard      | Optimistic  | 200ms   | None          |
| Local State   | Immediate   | 100ms   | None          |

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
    ├── feedback-loop.md   # Signal collection (ACCEPT/MODIFY/REJECT)
    └── detection.md       # Effect detection algorithm
```

## Fragment Usage

Fragments are loaded via `{{fragment:name}}` syntax:

```
{{fragment:physics-table}}    # Insert physics lookup table
{{fragment:protected-caps}}   # Insert capability checklist
{{fragment:feedback-loop}}     # Insert feedback collection
{{fragment:detection}}         # Insert effect detection
```

## Token Budget

| Scenario            | Load                          | Est. Tokens |
|---------------------|-------------------------------|-------------|
| Simple component     | Chisel + physics-table        | ~3,000      |
| Financial component   |                               |             |