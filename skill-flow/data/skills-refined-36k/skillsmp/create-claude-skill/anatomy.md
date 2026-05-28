# Skill Anatomy

This document provides detailed guidance on structuring skills for maximum effectiveness.

## Directory Structure

```
.claude/skills/your-skill/
├── SKILL.md              # Required: Main entry point
├── reference/            # Optional: Reference documentation
│   ├── patterns.md       # Common patterns
│   └── api.md            # API documentation
├── examples/             # Optional: Example implementations
│   ├── basic.md          # Simple example
│   └── advanced.md       # Complex example
├── templates/            # Optional: Starter templates
│   └── starter.md        # Copy-paste template
└── scripts/              # Optional: Executable code
    ├── helper.js         # Utility scripts
    └── validator.ts      # Validation tools
```

## SKILL.md Structure

### 1. YAML Frontmatter (Required)

```yaml
---
name: Skill Name
description: One-sentence description that helps Claude decide when to use this skill. Include trigger phrases.
---
```

**Name guidelines:**
- Use hyphenated-lowercase format
- Keep it short and descriptive
- Match the folder name

**Description guidelines:**
- Be specific about when this skill should activate
- Include key phrases users might say
- Mention the primary use case

### 2. Title and Role (Recommended)

```markdown
# Skill Name

You are an expert at [domain]. Your task is [primary purpose].
```

### 3. Purpose Section (Recommended)

```markdown
## When to Use This Skill

Use this skill when:
- [Specific scenario 1]
- [Specific scenario 2]
- [Specific scenario 3]
```

### 4. Core Instructions (Required)

The main body should contain:
- Step-by-step procedures for common tasks
- Key rules and constraints
- Decision trees for different scenarios

### 5. References to Supporting Files (Optional)

```markdown
## Detailed Reference

For more details on [topic]:
@.claude/skills/your-skill/reference/topic.md

Or instruct Claude to read:
Read: .claude/skills/your-skill/reference/topic.md
```

### 6. Quick Reference (Recommended)

```markdown
## Quick Reference

| Task | Action |
|------|--------|
| [Common task 1] | [Brief instruction] |
| [Common task 2] | [Brief instruction] |
```

## Progressive Disclosure Patterns

### Pattern 1: Topic-Based Splitting

Split by topic when content is largely independent:

```
SKILL.md           → Core workflow
database.md        → Database operations
api.md             → API integration
testing.md         → Testing procedures
```

### Pattern 2: Depth-Based Splitting

Split by detail level:

```
SKILL.md           → Overview and common cases
advanced.md        → Advanced techniques
edge-cases.md      → Rare scenarios
troubleshooting.md → Problem resolution
```

### Pattern 3: Scenario-Based Splitting

Split by use case:

```
SKILL.md           → Entry point and routing
creating.md        → Creating new items
updating.md        → Modifying existing items
deleting.md        → Removal procedures
```

## Code in Skills

### When to Include Code

Include code when:
- Operations are better handled by traditional code (sorting, parsing, etc.)
- Deterministic reliability is required
- Complex calculations are involved
- External tools need to be invoked

### Code Organization

```
scripts/
├── README.md           # Explain what each script does
├── helper.js           # Utility functions
├── validator.ts        # Input validation
└── sync.js             # Database synchronization
```

### Code as Documentation vs. Execution

Be clear about intent:

**For execution:**
```markdown
Run the validation script:
```bash
node .claude/skills/your-skill/scripts/validator.js
```

**For reference:**
```markdown
See the pattern in `.claude/skills/your-skill/scripts/helper.js` for implementation details.
```

## Templates

Templates help users get started quickly:

```
templates/
├── SKILL-template.md   # Starter SKILL.md
├── component.tsx       # Component template
└── config.json         # Configuration template
```

Reference templates explicitly:
```markdown
Copy the template from `.claude/skills/your-skill/templates/starter.md`
```

## Examples

Examples show expected outcomes:

```
examples/
├── basic/
│   ├── input.md        # What the user provides
│   └── output.md       # What Claude produces
└── advanced/
    ├── input.md
    └── output.md
```

## File Size Guidelines

| File | Recommended Size |
|------|-----------------|
| SKILL.md | 50-200 lines |
| Supporting docs | 50-300 lines each |
| Scripts | As needed |
| Templates | Minimal |

## Linking Conventions

### Using @ References

```markdown
@.claude/skills/your-skill/reference.md
```

### Using Read Instructions

```markdown
Read: .claude/skills/your-skill/reference.md
```

### Inline File Paths

```markdown
See `.claude/skills/your-skill/reference.md` for details.
```

Choose the convention that best matches how Claude should interact with the content.
