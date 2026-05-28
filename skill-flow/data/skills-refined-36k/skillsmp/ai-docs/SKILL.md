---
name: ai-docs
description: ALWAYS use this skill when writing AI documentation. Covers CLAUDE.md, AGENTS.md, system prompts, AI-targeted comments, and architecture docs for AI consumption.
---

# AI Documentation Skill

## Core Principles

| Do                                 | Don't                                    |
| ---------------------------------- | ---------------------------------------- |
| XML tags (`<rules>`, `<workflow>`) | Prose paragraphs                         |
| Templates: `{placeholder}`         | Vague instructions                       |
| Positive: "Do X"                   | Negative: "Don't Y" (unless prohibiting) |
| One task per prompt                | Overloaded prompts                       |
| Observable output                  | Internal instructions ("mentally X")     |
| Concrete examples                  | Abstract rules                           |
| <3000 tokens                       | Long verbose docs                        |
| TDD: tests first                   | Implementation first                     |

## Document Template

```markdown
<rules>
1. [Rule]: `good` not `bad`
</rules>

<workflow>
1. {step with placeholder}
2. [Decision] {cond} → {action}
</workflow>

<tools>
tool = gotcha or constraint
</tools>
```

## Writing Rules

```
Structure:    BAD "keep commits clear" → GOOD `{scope}: {msg}`
Positive:     BAD "Don't cd" → GOOD "Stay at repo root"
Concrete:     BAD "reasonably sized" → GOOD "~100 lines"
Observable:   BAD "mentally verify" → GOOD "output: Task, Constraints, Verify"
Decision:     [Decision] simple → exec | complex → breakdown
```

## Followable Workflows

AI docs should include **step-by-step workflows** AI can mechanically follow.

- Numbered steps, single action each
- `[Decision] {cond} → {action}` for branches
- `{placeholder}` for fill-ins

example:

```markdown
<workflow>
## Adding a NixOS Module
1. Create `modules/{home|nixos}/{name}/default.nix`
2. Add option: `my.{name}.enable = lib.mkEnableOption "{name}";`
3. [Decision] multiple configs → use collectFiles | single → inline
4. Import in parent default.nix
5. Verify: `nix flake check`
</workflow>
```

Anti-pattern: "Create appropriate module structure based on your judgment"

## Content & Length

**Include:** conventions, constraints, decision templates, tool gotchas
**Exclude:** generic best practices, tool docs, code explanations

| Doc       | Lines  |
| --------- | ------ |
| CLAUDE.md | 50-150 |
| Skills    | 50-100 |

## Checklist

1. XML tags? 2. `{placeholders}`? 3. Positive framing? 4. `[Decision]` markers? 5. Examples? 6. Under limit?
