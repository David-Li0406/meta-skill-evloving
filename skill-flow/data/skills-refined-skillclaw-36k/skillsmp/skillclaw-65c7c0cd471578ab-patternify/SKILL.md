---
name: patternify
description: Use this skill when capturing reusable workflows from conversations, codifying decision heuristics, or when "patternify", "capture", or "codify workflow" are mentioned.
---

# Skill body

## When to Use
- Spotting repeated behavior worth codifying
- User explicitly wants to capture a workflow
- Recognizing orchestration sequences in conversation
- Identifying decision heuristics being applied

**NOT for:** one-off tasks, simple questions, well-documented existing patterns

## Pattern Types

| Type         | Purpose                     | Example                          |
|--------------|-----------------------------|----------------------------------|
| Workflow     | Multi-step sequences        | Debug → Test → Fix → Verify      |
| Orchestration| Tool coordination           | Git + Linear + PR automation     |
| Heuristic    | Decision rules              | "When X, do Y because Z"        |

### Definitions
- **Workflows:** Step-by-step processes with defined phases and transitions.
- **Orchestration:** Tool combinations that work together for a goal.
- **Heuristics:** Conditional logic and decision trees for common situations.

## Component Mapping

Match pattern type to implementation:

```text
Is it a multi-step process with phases?
├─ Yes → Does it need tool restrictions?
│        ├─ Yes → Skill (with allowed_tools)
│        └─ No → Skill
└─ No → Is it a simple entry point?
         ├─ Yes → Command (thin wrapper → Skill)
         └─ No → Is it autonomous/long-running?
                  ├─ Yes → Agent
                  └─ No → Is it reactive to events?
                           ├─ Yes → Hook
                           └─ No → Probably doesn't need codifying
```

### Composites
- **Skill + Command:** Skill holds logic, command provides entry point
- **Skill + Hook:** Skill holds logic, hook triggers automatically
- **Agent + Skill:** Agent orchestrates, skill provides methodology

## Specification

Pattern spec format (YAML):

```yaml
name: pattern-name
type: workflow | orchestration | heuristic
trigger: when to apply
phases:  # workflow
  - name: phase-name
    actions: [...]
    exit_criteria: condition
tools:   # orchestration
  - tool: name
    role: purpose
    sequence: order
rules:   # heuristic
  - condition: when
    action: what
    rationale: why
quality:
  specific: true | false
  repeatable: true | false
  valuable: true | false
  documented: true | false
  scoped: true | false
```

All five quality checks must pass before codifying.