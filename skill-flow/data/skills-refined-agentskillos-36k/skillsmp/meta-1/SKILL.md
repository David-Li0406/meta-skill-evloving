---
name: meta
description: Meta - Agent System infrastructure for the ikigai project
---

# Meta - Agent System

Expert on the `.claude/` directory structure and agent infrastructure. Use this skillset when improving or extending the agent system, skills, skillsets, or commands.

**Depends on:** `cdd` skill for pipeline workflow knowledge.

## Directory Structure

```
.claude/
├── commands/   # Slash command definitions
├── library/    # Knowledge modules (skill directories with SKILL.md)
├── skillsets/  # Composite skill sets (JSON)
└── data/       # Runtime data (gitignored)
```

## Skills (`.claude/library/`)

Each skill is a directory containing `SKILL.md`. Loaded via `/load` or as part of skillsets.

**Conventions:**
- One domain per skill
- Keep concise (~20-100 lines)
- Subdirectories for groups: `patterns/`, `security/`, `refactoring/`

**Skill structure:**
```markdown
---
name: skill-name
description: Brief description
---

# Skill Name

Content here...
```

## Commands (`.claude/commands/`)

Markdown files defining slash commands. The content after `---` is the prompt.

**Command structure:**
```markdown
---
description: What the command does
---

Prompt template here. Use {{args}} for arguments.
```

## Skillsets (`.claude/skillsets/`)

JSON files listing skills to load together.

**Skillset structure:**
```json
{
  "preload": ["skill-a", "skill-b"],
  "advertise": ["optional-skill-c"]
}
```

- `preload`: Skills loaded automatically when skillset activates
- `advertise`: Skills mentioned but not loaded (load on demand)

**Current skillsets:**
- `researcher` - Research phase (goals, specs)
- `architect` - Plan phase (plan/, task breakdown)
- `developer` - Implementation (TDD, quality)
- `orchestrator` - Task execution
- `refactor` - Behavior-preserving refactoring
- `coverage` - 90% test coverage
- `debugger` - Troubleshooting
- `security` - Security review
- `meta` - Agent system management

## Best Practices

**Skills:**
- Focused scope, single domain
- Actionable guidance over theory
- Reference docs for depth, load on demand
- Both mechanical (how) and conceptual (why) layers

**Skillsets:**
- Match a workflow phase
- Minimal preload (only what's always needed)
- Advertise skills that might be needed

**Commands:**
- Brief description in frontmatter
- Handle missing args gracefully
- Clear usage examples

## Efficiency Principles

The agent system is designed for token efficiency:

1. **Skillsets are minimal** - Only preload skills needed for that workflow
2. **Load on demand** - Don't preload "just in case"
3. **Skills are focused** - One domain, ~20-100 lines
4. **Reference vs working knowledge** - Large docs in separate skills

See `cdd` skill for pipeline-specific efficiency principles.
