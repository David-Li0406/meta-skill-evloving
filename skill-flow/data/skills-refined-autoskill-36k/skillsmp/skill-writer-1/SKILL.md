---
name: skill-writer
description: Create and maintain well-structured Claude Code skills. Use when creating, updating, or improving skills in .claude/skills/.
---

# Skill Writer

Guide for creating and maintaining Agent Skills for Claude Code.

## When to Use

- Creating a new skill
- Improving an existing skill
- Adding resources to a skill

## Skill Structure

```
.claude/skills/[skill-name]/
├── SKILL.md              # Main skill file (required)
└── resources/            # Supporting files (optional)
    ├── patterns.md       # Code patterns
    ├── examples.md       # Working examples
    └── reference.md      # API reference
```

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: skill-name          # lowercase, hyphens, max 64 chars
description: Brief description of what this skill does and when to use it. Max 1024 chars.
---
```

### Content Structure

```markdown
# Skill Title

**Activation:** Keywords that trigger this skill

## Overview
Brief explanation of the skill's purpose.

## Key Patterns
Code patterns with examples.

## Common Tasks
Step-by-step for frequent operations.

## Resources
Link to resources/ files for deep dives.
```

## Writing Effective Skills

### 1. Clear Activation Triggers

Include keywords in the description and first section:
```markdown
**Activation:** FastAPI, SQLAlchemy, async Python, database operations
```

### 2. Concise Main File

- Keep SKILL.md under 500 lines
- Put detailed reference in resources/
- Focus on "what to do" not "what it is"

### 3. Working Examples

```python
# GOOD: Complete, copy-paste ready
@router.get("/items/{id}")
async def get_item(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Item:
    item = await db.get(Item, id)
    if not item:
        raise HTTPException(status_code=404)
    return item

# BAD: Pseudocode
def get_item(id):
    # query database
    # return item
```

### 4. Progressive Disclosure

Main file → Quick patterns
Resources → Deep dives, edge cases, full API

### 5. Actionable Instructions

```markdown
# GOOD
Use `selectinload()` to eager-load relationships:
```python
stmt = select(User).options(selectinload(User.posts))
```

# BAD
Consider using eager loading for better performance.
```

## Skill Activation

Claude Code activates skills automatically via **semantic matching** of the YAML frontmatter:

1. **name** - The skill identifier
2. **description** - Describes what the skill does and when to use it

When a user's prompt matches the description semantically, Claude loads and applies the skill.

**Best practices for descriptions:**
- Include specific keywords users would say
- Mention technologies/frameworks covered
- Keep under 1024 characters

Example:
```yaml
---
name: frontend-dev
description: Jinja2 SSR pages with HTMX for interactivity, Alpine.js for UI state, and Tailwind CSS for styling. React islands only for complex interactive components (SignalChainBuilder).
---
```

This activates when users mention "Jinja2 template", "HTMX", "Alpine.js", "Tailwind", etc.

## Skill Creation Checklist

- [ ] Created `SKILL.md` with frontmatter
- [ ] Description includes trigger keywords
- [ ] Examples are complete and tested
- [ ] Under 500 lines (use resources/ for more)
- [ ] Tested activation with relevant prompts

## Updating Existing Skills

1. Read current SKILL.md
2. Identify what's missing or outdated
3. Update patterns to latest versions
4. Add new examples if needed
5. Update description in frontmatter if activation triggers changed

## This Project's Skills

| Skill | Purpose | Key Technologies |
|-------|---------|------------------|
| backend-dev | API development | FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| frontend-dev | UI development | Jinja2, HTMX, Alpine.js, Tailwind |
| frontend-design | UI design principles | Visual patterns, color, typography |
| ui-design-system | Design tokens and styling | Color palette, spacing, shadows |
| playwright | Browser automation | Playwright, MCP tools |
| screenshot-eval | Screenshot evaluation | Error detection, visual verification |
| pipeline-dev | Audio/video processing | NAM, Pedalboard, FFmpeg |
| testing | Test development | pytest, fixtures, mocking |
| docker-infra | Container management | Docker, Docker Compose |
| micro-task-workflow | Task execution patterns | Context budget, escape protocols |
| worktree-cli | Worktree management | Git worktrees, Docker isolation |
| skill-writer | Skill creation | This skill |
