---
name: Skill Best Practices
description: This skill should be used when the user asks to "create a skill", "write SKILL.md", "what are skill best practices", "how to optimize a skill", "improve skill quality", or mentions skill development, trigger phrases, skill structure, or content quality. Provides comprehensive guidance for creating high-quality Claude Code skills following latest standards.
version: 0.1.0
---

# Skill Best Practices

## Overview

Create effective Claude Code skills that provide specialized knowledge and workflows. High-quality skills transform Claude from a general-purpose assistant into a domain expert equipped with procedural knowledge.

## Core Principles

### Progressive Disclosure

Use a three-level loading system to manage context efficiently:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<2,000 words)
3. **Bundled resources** - As needed (unlimited, loaded selectively)

Keep SKILL.md lean. Move detailed content to `references/` files.

### Strong Triggering

The `description` field determines when Claude activates the skill. Use specific, concrete phrases:

✅ **Good:**
```yaml
description: This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", "validate tool use", or mentions hook events
(PreToolUse, PostToolUse, Stop).
```

❌ **Bad:**
```yaml
description: Use this skill when working with hooks.
```

### Third-Person Descriptions

Always write descriptions in third person: "This skill should be used when..."

❌ **Avoid second person:** "Use this skill when you want to..."

### Imperative Writing Style

Write skill body instructions using imperative/infinitive form (verb-first):

✅ **Good:**
```markdown
Create the skill directory structure.
Validate the frontmatter syntax.
Check required fields.
```

❌ **Bad:**
```markdown
You should create the directory structure.
You need to validate the syntax.
```

## Skill Structure

### Required Components

Every skill must have:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown body
└── [Optional resources]
    ├── scripts/      - Executable utilities
    ├── references/   - Detailed documentation
    └── assets/       - Templates and output files
```

### YAML Frontmatter

Required fields:
- `name` - Skill name (Title Case)
- `description` - Third-person description with specific triggers

Optional fields:
- `version` - Skill version (semantic versioning)

Example:
```yaml
---
name: My Skill
description: This skill should be used when the user asks to "task 1",
"task 2", or "task 3".
version: 0.1.0
---
```

## Content Guidelines

### SKILL.md Body (Core Content)

Target 1,500-2,000 words maximum. Include:

**Essential Content:**
- Purpose and overview (what the skill does)
- Core concepts and terminology
- Essential procedures and workflows
- Quick reference tables
- Most common use cases
- Links to supporting resources

**Keep focused:** Move detailed patterns, advanced techniques, and comprehensive examples to `references/` files.

### References/ (Detailed Documentation)

Move to `references/` when content is:
- Detailed and comprehensive (2,000-5,000+ words)
- Advanced or specialized patterns
- API documentation and specifications
- Migration guides
- Edge cases and troubleshooting

**Benefits:**
- SKILL.md stays lean
- Details load only when needed
- Better context management
- Easier to maintain

**Never duplicate:** Information should live in either SKILL.md OR references/, not both.

### Examples/ (Working Code)

Store complete, runnable examples:
- Full scripts that work
- Configuration files
- Template code
- Real-world usage samples

Users can copy and adapt these directly.

### Scripts/ (Utilities)

Include executable tools when:
- The same code is repeatedly rewritten
- Deterministic reliability is needed
- Complex automation helps

Examples:
- Validation scripts
- Testing helpers
- Parsing utilities

## Trigger Phrase Optimization

### Be Specific and Concrete

List exact phrases users would say:

✅ **Good:**
```yaml
description: This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", "validate tool use", "implement prompt-based hooks",
or mentions hook events (PreToolUse, PostToolUse, Stop).
```

❌ **Bad:**
```yaml
description: Load when user needs hook help.
```

### Cover Variations

Include different ways users might ask:

```yaml
description: This skill should be used when the user asks to "create a skill",
"write a new skill", "add a skill to my plugin", "how do I create SKILL.md",
or mentions skill development, SKILL.md files, or skill best practices.
```

### Include Domain Context

Mention relevant concepts and terminology:

```yaml
description: This skill should be used when working with MCP servers,
mentions "add MCP integration", "configure stdio server", or discusses
Model Context Protocol, MCP tools, or server authentication.
```

## Content Quality Standards

### Writing Style

**Use imperative form throughout:**
- "Create the file structure"
- "Validate the syntax"
- "Configure the server"

**Never use second person:**
- ❌ "You should create..."
- ❌ "You need to validate..."

**Be objective and instructional:**
- Focus on what to do
- Avoid opinionated language
- Provide clear procedures

### Organization

**Structure SKILL.md with:**
1. Overview (what and why)
2. Core concepts
3. Essential procedures
4. Quick references
5. Links to detailed resources

**Use markdown features:**
- Headers (##, ###) for hierarchy
- Bullet points for lists
- Code blocks for examples
- Tables for quick reference

### Clarity

**Make content actionable:**
- Provide step-by-step procedures
- Include concrete examples
- Show expected outputs
- Reference supporting files

**Avoid ambiguity:**
- Be specific about requirements
- Define terms clearly
- Provide complete examples
- Note edge cases

## Common Mistakes

### Mistake 1: Weak Trigger Description

❌ **Problem:**
```yaml
description: Provides guidance for skills.
```

**Why:** Vague, no specific triggers, not third person.

✅ **Fix:**
```yaml
description: This skill should be used when the user asks to "create a skill",
"write SKILL.md", or mentions skill development, trigger phrases, or skill
structure.
```

### Mistake 2: Bloated SKILL.md

❌ **Problem:**
- SKILL.md has 8,000 words
- All documentation in one file
- Details always loaded into context

✅ **Fix:**
- Keep SKILL.md at 1,500-2,000 words
- Move detailed content to `references/`
- Use progressive disclosure

### Mistake 3: Second Person Writing

❌ **Problem:**
```markdown
You should start by creating the directory.
You need to configure the settings.
```

✅ **Fix:**
```markdown
Start by creating the directory.
Configure the settings before use.
```

### Mistake 4: Missing Resource References

❌ **Problem:**
SKILL.md doesn't mention `references/` files.

✅ **Fix:**
```markdown
## Additional Resources

### Reference Files
- **`references/structure-guide.md`** - Detailed structure standards
- **`references/trigger-patterns.md`** - Trigger phrase patterns

### Examples
- **`examples/good-skill.md`** - Example SKILL.md
```

## Skill Anatomy

### Minimal Skill

For simple knowledge without complex resources:

```
skill-name/
└── SKILL.md
```

Use when: Skill provides straightforward guidance, no utilities needed.

### Standard Skill (Recommended)

```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.md
```

Use when: Skill has detailed documentation or examples.

### Complete Skill

```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   ├── example1.md
│   └── example2.md
└── scripts/
    └── validate.sh
```

Use when: Complex domain with utilities and comprehensive docs.

## Quick Validation Checklist

Before finalizing a skill, verify:

**Structure:**
- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] Frontmatter has `name` and `description`
- [ ] Markdown body is substantial

**Description:**
- [ ] Uses third person ("This skill should be used when...")
- [ ] Includes specific trigger phrases
- [ ] Lists concrete scenarios

**Content:**
- [ ] Body uses imperative form (no "you should")
- [ ] SKILL.md is lean (1,500-2,000 words)
- [ ] Detailed content in references/

**Resources:**
- [ ] Referenced files exist
- [ ] Examples are complete
- [ ] Scripts are executable

**Progressive Disclosure:**
- [ ] Core content in SKILL.md
- [ ] Details in references/
- [ ] Code in examples/
- [ ] Utilities in scripts/

## Additional Resources

### Reference Files

For comprehensive guidance on specific aspects:

- **`references/structure-guide.md`** - Detailed structure and formatting standards
- **`references/trigger-patterns.md`** - Trigger phrase optimization patterns
- **`references/content-quality.md`** - Content quality checklist and standards
- **`references/common-mistakes.md`** - Common mistakes and how to fix them

These references provide in-depth coverage of each topic with examples and patterns.

### Examples

Study these skills as best practice examples:
- `plugin-dev/skills/hook-development/` - Progressive disclosure, utilities
- `plugin-dev/skills/agent-development/` - Strong triggers, references
- `plugin-dev/skills/skill-development/` - Meta-example (this skill)

## Implementation Workflow

Follow these steps when creating a skill:

1. **Understand Use Cases** - Identify concrete examples
2. **Plan Resources** - Determine scripts/references/examples needed
3. **Create Structure** - Make directories and SKILL.md
4. **Write SKILL.md** - Frontmatter + lean body in imperative form
5. **Add Resources** - Create references/, examples/, scripts/
6. **Validate** - Check description, style, organization
7. **Test** - Verify skill triggers on expected queries
8. **Iterate** - Improve based on usage

Focus on strong trigger descriptions, progressive disclosure, and imperative writing to create effective skills that load when needed and provide targeted guidance.
