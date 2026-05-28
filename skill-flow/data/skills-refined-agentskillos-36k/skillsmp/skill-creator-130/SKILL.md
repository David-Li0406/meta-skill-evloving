---
name: Skill Creator
description: Meta-skill for creating high-quality Claude Code skills
version: 1.0.0
source: Adapted from anthropics/skills/skill-creator
---

# Skill Creator

## Purpose

Guide the creation of new Claude Code skills that:
- Follow best practices structure
- Include comprehensive documentation
- Are testable and maintainable
- Integrate with existing FrankX skills

## Skill Anatomy

```
.claude-skills/
└── [category]/
    └── [skill-name]/
        ├── SKILL.md          # Main skill file (required)
        ├── CLAUDE.md         # Memory context (auto-generated)
        ├── resources/        # Supporting files (optional)
        │   ├── templates/
        │   └── examples/
        └── scripts/          # Executable scripts (optional)
            └── helper.py
```

## SKILL.md Template

```markdown
---
name: [Human-Readable Name]
description: [One-line description of what this skill does]
version: 1.0.0
source: [Original source if adapted, or "Original"]
---

# [Skill Name]

## Purpose
[2-3 sentences explaining what this skill helps accomplish and why it matters]

## When to Use This Skill
- [Specific scenario 1]
- [Specific scenario 2]
- [Specific scenario 3]

## Core Concepts

### [Concept 1]
[Explanation with code examples if applicable]

### [Concept 2]
[Explanation with code examples if applicable]

## Patterns

### Pattern 1: [Name]
```[language]
// Code example
```

### Pattern 2: [Name]
```[language]
// Code example
```

## FrankX Application
[How this skill specifically applies to the FrankX project]

## Anti-Patterns
| Bad Practice | Better Approach |
|--------------|-----------------|
| [Anti-pattern 1] | [Correct approach] |
| [Anti-pattern 2] | [Correct approach] |

## Commands
```bash
# Relevant commands for this skill
```

## Related Skills
- `skill-name-1` - [How it relates]
- `skill-name-2` - [How it relates]

## Resources
- [Link to documentation]
- [Link to examples]
```

## Creation Checklist

### Before Creating

- [ ] Does a similar skill already exist?
- [ ] Is this knowledge needed repeatedly (3+ times)?
- [ ] Is there enough depth for a skill (500+ words)?
- [ ] Does it apply across multiple contexts?

### Structure Quality

- [ ] Clear, descriptive name (kebab-case)
- [ ] Accurate one-line description
- [ ] Comprehensive purpose section
- [ ] "When to Use" with specific scenarios
- [ ] Code examples that actually work
- [ ] FrankX-specific applications
- [ ] Related skills linked
- [ ] Anti-patterns documented

### Technical Quality

- [ ] Code examples tested
- [ ] No broken links
- [ ] Consistent formatting
- [ ] Proper YAML frontmatter
- [ ] Version number set

## Skill Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| `technical/` | Development tools & patterns | TDD, debugging, testing |
| `business/` | Enterprise & strategy | OCI, product management |
| `creative/` | Content & design | Brand, music, social |
| `personal/` | Self-development | Philosophy, fitness |
| `projects/` | Project-specific | Arcanea, daily ops |
| `soulbook/` | Life transformation | 7 pillars, life books |

## Skill Quality Rubric

### Level 1: Basic (Meets Minimum)
- Has SKILL.md with frontmatter
- Explains what the skill does
- Has at least one example

### Level 2: Good (Recommended)
- All Level 1 requirements
- Multiple code examples
- "When to Use" section
- Related skills linked

### Level 3: Excellent (Target)
- All Level 2 requirements
- Anti-patterns documented
- FrankX-specific guidance
- Tested code examples
- Commands section

### Level 4: Exceptional
- All Level 3 requirements
- Supporting resources/templates
- Integration with other skills
- Community-shareable quality

## Interactive Creation Flow

When creating a new skill:

### Step 1: Discovery
```
What domain does this skill cover?
> [User provides domain]

What specific problem does it solve?
> [User describes problem]

When would someone use this skill?
> [User gives scenarios]
```

### Step 2: Structure
```
Based on your answers, I'll create:
- Category: technical/
- Name: [suggested-name]
- Core concepts: [list]

Does this look right?
```

### Step 3: Content
```
Let me draft the skill content...
[Generate SKILL.md]

Review and refine:
- [ ] Is the purpose clear?
- [ ] Are examples accurate?
- [ ] Anything missing?
```

### Step 4: Integration
```
Updating README.md to include new skill...
Testing skill invocation...
Done! Use with: /skill [skill-name]
```

## Maintenance

### Regular Reviews
- Monthly: Check for outdated patterns
- Quarterly: Add new learnings
- Annually: Archive unused skills

### Version Updates
```yaml
# When to bump versions:
version: 1.0.0  # Initial release
version: 1.1.0  # New content added
version: 2.0.0  # Breaking changes/restructure
```

## When to Use This Skill

- Creating a new skill from scratch
- Improving an existing skill
- Reviewing skill quality
- Teaching others to create skills

## Related Skills

- `implementation-planning` - Plan skill creation
- `frankx-brand` - Ensure voice consistency
- `parallel-agents` - Create multiple skills concurrently
