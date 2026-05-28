---
name: writing-claude-skills
description: Create effective Agent Skills following the agentskills.io specification. Use when creating new skills, reviewing existing skills, or improving skill descriptions.
allowed-tools: Read, Grep, Glob
---

# Writing Agent Skills

Agent Skills are modular packages that extend AI agent capabilities. Skills are directories containing a `SKILL.md` file with YAML frontmatter and Markdown instructions.

## Progressive Disclosure

Skills load in three stages to optimize context:

1. **Discovery** (~50-100 tokens): Only names and descriptions at startup
2. **Activation** (<5000 tokens): Full SKILL.md when task matches description
3. **Execution**: Referenced files load only when needed

**Token budget**: Keep main SKILL.md under 500 lines. Move detailed content to supporting files.

## SKILL.md Structure

```yaml
---
name: skill-name-here
description: What it does. Use when [triggers]. Covers [keywords].
allowed-tools: Read, Grep, Glob # optional
---
[Markdown body with instructions, examples, guidelines]
```

## Required Fields

### name

1-64 characters, lowercase alphanumeric with hyphens. Must match parent directory name.

Include domain when capability could apply to multiple areas: `mcp-server-development` not `server-development`.

### description

Critical field--agents use this to decide when to activate.

**Pattern**: "[Capability]. Use when [triggers]. Covers [keywords]."

## Directory Structure

```
my-skill/
├── SKILL.md           # Required: metadata + instructions
├── scripts/           # Optional: executable code
├── references/        # Optional: extended documentation
└── assets/            # Optional: templates, data files
```

## Body Content

1. **Opening Context**: Brief purpose and activation triggers
2. **Philosophy**: Guide decision-making before prescriptive rules
3. **Guidelines**: Focused, actionable guidance with examples
4. **Anti-patterns**: What to avoid with examples
5. **Remember**: Core philosophy reminders

**Tone**: Bold, opinionated, directive. Use imperative mood.

## Content Principles

- **Actionable over theoretical**: Patterns to follow, not abstract concepts
- **Examples over explanation**: Show don't tell
- **Negative space**: What NOT to do matters
- **Token efficiency**: Every line must justify its context cost

## Common Mistakes

| Mistake                     | Fix                                       |
| --------------------------- | ----------------------------------------- |
| Overly broad scope          | Separate skills for each domain           |
| Missing activation triggers | Add "Use when..." with scenarios          |
| Just a list of rules        | Explain WHY before HOW                    |
| Redundant with tools        | Guide decision-making, not just run tools |

## Testing

- **Activation**: Verify skill loads for trigger words, not for unrelated work
- **Clarity**: Ask teammate "When would you use this?"
- **Effectiveness**: Compare results with and without skill

## Skills vs Agents

| Scenario                 | Skill | Agent |
| ------------------------ | ----- | ----- |
| Guidance during work     | Yes   | No    |
| Simple, frequent tasks   | Yes   | No    |
| Complex autonomous tasks | No    | Yes   |
| Multi-step orchestration | No    | Yes   |

## When to Create a Skill

Create when you see: repetitive instructions, generic outputs needing refinement, domain expertise gaps, consistency enforcement needs, repeated workflows.

## Remember

- **Specific beats generic** - In naming and content
- **Trigger words matter** - Include terms users naturally mention
- **One skill, one job** - Focus trumps comprehensiveness
- **Token efficiency** - Every line earns its place
- **Test activation** - Verify the skill loads when expected

Skills are prompt engineering at scale. Make every word count.
