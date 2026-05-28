---
name: skill-manager
description: |
  Meta-skill for creating, updating, and managing Claude Code skills. Use when:
  (1) discovering reusable knowledge that should be preserved as a skill,
  (2) an existing skill needs updating with new information or corrections,
  (3) user explicitly asks to "save as skill", "create a skill", or "update skill",
  (4) after debugging sessions that revealed non-obvious solutions,
  (5) when patterns emerge that would help in future similar situations.
  This skill handles the full lifecycle: creation, updates, and organization.
author: Claude Code
version: 1.0.0
date: 2026-01-21
---

# Skill Manager

A meta-skill for autonomously creating and maintaining Claude Code skills.

## When to Create a New Skill

Create a skill when ANY of these apply:

1. **Non-obvious debugging**: Solution required significant investigation
2. **Error resolution**: Fixed error where message was misleading or root cause wasn't obvious
3. **Workaround discovery**: Found workaround for tool/framework limitation
4. **Configuration insight**: Discovered setup that differs from standard patterns
5. **Reusable pattern**: Identified pattern that would help in similar projects
6. **User request**: User says "save as skill", "create a skill", etc.

## When to Update an Existing Skill

Update rather than create new when:

1. **New edge case**: Discovered additional scenario the skill should cover
2. **Better solution**: Found improved approach to the same problem
3. **Correction**: Original skill had inaccurate information
4. **Version update**: Underlying technology changed behavior
5. **Additional context**: More trigger conditions or symptoms identified

## Skill Creation Process

### Step 1: Check for Existing Skills

```bash
# List all skills
ls -la ~/.claude/skills/

# Search for related skills
grep -r "keyword" ~/.claude/skills/
```

### Step 2: Choose Location

- **User-global skills**: `~/.claude/skills/[skill-name]/SKILL.md`
- **Project-specific skills**: `.claude/skills/[skill-name]/SKILL.md`

### Step 3: Create Skill Directory

```bash
mkdir -p ~/.claude/skills/[skill-name]
```

### Step 4: Write SKILL.md

Use this template:

```markdown
---
name: [descriptive-kebab-case-name]
description: |
  [Precise description with: (1) exact use cases, (2) trigger conditions like
  specific error messages or symptoms, (3) what problem this solves. Include
  keywords for semantic matching.]
author: [author or "Claude Code"]
version: 1.0.0
date: [YYYY-MM-DD]
---

# [Skill Name]

## Problem
[Clear description of the problem]

## Context / Trigger Conditions
[When to use - include exact error messages, symptoms, scenarios]

## Solution
[Step-by-step solution]

## Verification
[How to verify it worked]

## Example
[Concrete example]

## Notes
[Caveats, edge cases, related considerations]

## References
[Links to docs, articles if applicable]
```

### Step 5: Write Effective Descriptions

The description is critical for discovery. Include:

- **Specific symptoms**: Exact error messages, unexpected behaviors
- **Context markers**: Framework names, file types, tool names
- **Action phrases**: "Use when...", "Helps with...", "Solves..."
- **Keywords**: Terms someone would search for

**Good example**:
```yaml
description: |
  Fix for NextResponse.redirect going to wrong host (localhost:8080) on Railway,
  Vercel, or containerized deployments. Use when: (1) redirects work locally but
  go to localhost in production, (2) console shows ERR_CONNECTION_REFUSED to
  localhost:8080, (3) using `new URL(path, request.url)` for redirects.
```

**Bad example**:
```yaml
description: Helps with redirect issues in Next.js
```

## Skill Update Process

### Step 1: Read Existing Skill

```bash
cat ~/.claude/skills/[skill-name]/SKILL.md
```

### Step 2: Determine Update Type

- **Minor**: Add edge case, clarify wording → increment patch (1.0.0 → 1.0.1)
- **Moderate**: New section, significant additions → increment minor (1.0.0 → 1.1.0)
- **Major**: Rewrite, breaking changes → increment major (1.0.0 → 2.0.0)

### Step 3: Update the Skill

- Update the `version` field
- Update the `date` field
- Add/modify content as needed
- Keep the changelog in Notes if significant

## Quality Checklist

Before saving, verify:

- [ ] Description has specific trigger conditions (error messages, symptoms)
- [ ] Solution has been verified to work
- [ ] Content is specific enough to be actionable
- [ ] Content is general enough to be reusable
- [ ] No sensitive info (credentials, internal URLs)
- [ ] Doesn't duplicate official documentation
- [ ] Version and date are set correctly

## Skill Organization

### Naming Conventions

Use kebab-case with descriptive names:
- `nextjs-request-url-proxy-redirect` ✓
- `fix-redirect` ✗ (too vague)
- `supabase-rls-service-role-bypass` ✓
- `db-stuff` ✗ (too vague)

### Directory Structure

```
~/.claude/skills/
├── skill-manager/
│   └── SKILL.md
├── nextjs-request-url-proxy-redirect/
│   └── SKILL.md
├── supabase-rls-patterns/
│   ├── SKILL.md
│   └── scripts/
│       └── check-rls.sql
└── [skill-name]/
    ├── SKILL.md
    └── scripts/  (optional helpers)
```

## Anti-Patterns

Avoid these mistakes:

1. **Over-extraction**: Not every task needs a skill
2. **Vague descriptions**: Won't surface when needed
3. **Unverified solutions**: Only extract what actually worked
4. **Documentation duplication**: Link to docs, don't recreate them
5. **Stale skills**: Always update version/date when modifying

## Autonomous Behavior

This skill should be invoked automatically when:

1. A debugging session reveals non-obvious knowledge
2. User explicitly requests skill creation/update
3. A pattern emerges that would benefit future work
4. An existing skill is found to be incomplete or incorrect

## Example: Creating a New Skill

```bash
# 1. Create directory
mkdir -p ~/.claude/skills/railway-env-var-debugging

# 2. Write SKILL.md with proper frontmatter and content
# 3. Verify skill is discoverable
ls ~/.claude/skills/
```

## Example: Updating an Existing Skill

```bash
# 1. Read current content
cat ~/.claude/skills/nextjs-request-url-proxy-redirect/SKILL.md

# 2. Edit with new information
# - Update version: 1.0.0 → 1.1.0
# - Update date
# - Add new section or modify existing

# 3. Save updated file
```

## Integration Notes

- Skills are loaded by Claude Code at startup
- Description field enables semantic search/matching
- Skills can reference other skills in their Notes section
- Project-specific skills in `.claude/skills/` override user-global ones
