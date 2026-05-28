---
name: flight-compile
description: Compile atomic prompt from primed context with domain invariants. Use after /flight-prime to generate executable PROMPT.md.
---

## ⚠️ EXECUTION RULES (MANDATORY)

1. **EXECUTE EACH STEP** - Do not skip steps based on "prior context"
2. **USE TOOLS** - You MUST call Read/Bash tools, not recall from memory
3. **SHOW WORK** - Each step must produce visible tool output
4. **NO SHORTCUTS** - "I already read this" is NOT acceptable

### Anti-Patterns (DO NOT DO THESE)
- ❌ "I already read the domain files earlier"
- ❌ "From earlier analysis..."
- ❌ Summarizing steps without executing them
- ❌ Claiming knowledge from "this conversation"

---

# /flight-compile

Compile an atomic Flight prompt from primed context. Transforms research into an executable, self-contained prompt.

## Usage

```
/flight-compile
```

## Arguments

- None - Uses the most recent Prime Document (PRIME.md) from context

---

## Process

### 1. Gather Inputs

From the Prime Document, collect:
- Task summary
- Domains used
- Key constraints (MUST/NEVER/SHOULD)
- Files to create/modify
- External dependencies

### 2. Load Domain Invariants

For each domain listed in "Domains Loaded":

```bash
cat .flight/domains/[domain].md
```

Extract:
- All MUST rules (will fail validation if violated)
- All NEVER rules (hard failures)
- Relevant patterns with examples
- Error handling requirements

### 3. Load Template (if specified)

If the Prime Document references a template:

```bash
cat .flight/templates/[template].md
```

### 4. Build Atomic Prompt

Structure the prompt with these sections:

```markdown
# Task: [Name]

## Objective
[Clear, single-sentence goal]

## Context
[Relevant background from Prime Document]

## Invariants

### MUST
- [From domain files - required behaviors]

### NEVER
- [From domain files - forbidden patterns]

## Implementation Requirements

### Files to Create
- `path/to/file.js`: [purpose]

### Files to Modify
- `path/to/existing.js`: [changes needed]

## Patterns to Follow

[Code examples from domains or existing codebase]

## Acceptance Criteria

- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] All invariants satisfied
- [ ] Tests pass

## Error Handling

[From domain files - specific error codes and handling]

## Completion

When ALL acceptance criteria are met and tests pass, output:
COMPLETE

If blocked after significant effort, output:
BLOCKED: [reason]
```

### 5. Write PROMPT.md

Write the compiled prompt to `PROMPT.md` in the project root:

```bash
cat > PROMPT.md << 'EOF'
[compiled prompt content]
EOF
```

**This file contains the compiled prompt for execution.**

### 6. Update @fix_plan.md (if exists)

If `@fix_plan.md` exists, ensure the current task is tracked:

```markdown
## Current Priority

- [ ] [Task from this compile]

## Backlog

[existing items]
```

---

## Output: Compilation Report

After writing PROMPT.md, report:

```markdown
## Compiled Successfully

**PROMPT.md** updated with:
- Task: [name]
- Domains: [list]
- Invariants: [count] MUST, [count] NEVER
- Files to create: [count]
- Files to modify: [count]

**Ready for execution.**
```

---

## Quality Checks

Before finalizing, verify:

| Check | Requirement |
|-------|-------------|
| **Atomic** | Single clear objective |
| **Invariants** | All relevant MUST/NEVER rules included |
| **Testable** | Clear acceptance criteria |
| **Self-contained** | All context needed is in the prompt |
| **Completion signal** | Includes COMPLETE/BLOCKED output instructions |

---

## Critical Rules

1. **USE PRIME DOCUMENT** - Don't re-research; use what /flight-prime gathered
2. **INCLUDE ALL INVARIANTS** - Every MUST/NEVER from relevant domains
3. **ONE TASK PER COMPILE** - Keep prompts atomic and focused
4. **TESTABLE CRITERIA** - Every acceptance criterion must be verifiable
5. **SELF-CONTAINED** - Prompt executable without additional context
6. **COMPLETION SIGNALS** - Always include COMPLETE/BLOCKED instructions

---

## When to Use

| Situation | Use This? |
|-----------|-----------|
| Just ran /flight-prime | Yes |
| Have PRIME.md in context | Yes |
| Starting from scratch | No → Use `/flight-prime` first |
| Have code, need to validate | No → Use `/flight-validate` |
| Task is vague | No → Use `/flight-prd` first |

---

## Next Step

After generating PROMPT.md, implement the task then validate:

```
[implement the task following PROMPT.md]
/flight-validate
```

**Workflow**: `/flight-compile` → [implement] → `/flight-validate` → next task

| Response | Action |
|----------|--------|
| `proceed` or `p` | Implement the task following PROMPT.md |
| `review` | Display PROMPT.md contents |
| `edit` | Modify PROMPT.md before implementation |
