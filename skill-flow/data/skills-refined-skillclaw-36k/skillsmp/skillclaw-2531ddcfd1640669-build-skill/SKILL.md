---
name: build-skill
description: Use this skill when creating effective skills for OpenCode agents, providing guidance on format, naming conventions, and validation.
---

# Building Skills

Skills extend agent capabilities with specialized knowledge, workflows, and tools.

## Quick Start

Create a minimal viable skill in 30 seconds:

```bash
mkdir my-skill && cat > my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: Does X when Y happens. Use for Z tasks.
---

# My Skill

Instructions go here.
EOF
```

Place the skill in `.opencode/skills/` (project) or `~/.config/opencode/skills/` (global).

## Skill Type Decision Tree

```
What are you building?
├─ Instructions only → Simple skill (SKILL.md only)
│   Example: code-review guidelines, commit message format
│
├─ Domain knowledge → Reference-heavy skill (+ references/)
│   Example: API docs, database schemas, company policies
│
├─ Repeatable automation → Script-heavy skill (+ scripts/)
│   Example: PDF processing, data validation, file conversion
│
├─ Complex multi-step workflow → Multi-file skill (all directories)
│   Example: release process, deployment pipeline
│
└─ Large platform → Progressive skill
    Example: AWS, GCP, Cloudflare (60+ products)
```

## When to Create a Skill

Create a skill when:

- Same instructions are repeated across conversations.
- Domain knowledge model lacks (schemas, internal APIs, company policies).
- Workflow requires 3+ steps with a specific order.
- Code is rewritten repeatedly for the same task.
- The team needs shared procedural knowledge.

## When NOT to Create a Skill

| Scenario                   | Do Instead                          |
| -------------------------- | ----------------------------------- |
| Single-use instructions    | AGENTS.md or inline in conversation |
| Model already knows domain | Don't add redundant context         |
| < 3 steps, no reuse       | Inline instructions                 |
| Highly variable workflow   | Higher-freedom guidelines           |
| Just want to store files   | Use regular directories             |

## Reading Order

| Task                    | Files to Read               |
| ----------------------- | --------------------------- |
| New skill from scratch  | anatomy.md → frontmatter.md |
| Optimize existing skill | progressive-disclosure.md   |
| Add scripts/resources   | bundled-resources.md        |
| Find skill pattern      | patterns.md                 |
| Debug/fix skill        | gotchas.md                  |