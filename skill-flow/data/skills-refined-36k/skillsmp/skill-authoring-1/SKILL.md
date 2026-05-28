---
name: skill-authoring
description: Create effective OpenCode agent skills. Use this skill when writing SKILL.md files, designing skill instructions, or helping others author skills for their projects or global config.
---

# Skill Authoring

This skill guides you through creating high-quality OpenCode agent skills. Skills are reusable instruction sets that agents load on-demand via the `skill` tool.

## What Skills Are

Skills are markdown files with YAML frontmatter that provide specialized knowledge and step-by-step guidance for specific tasks. They're discovered automatically from these locations:

- **Project-local**: `.opencode/skill/<name>/SKILL.md`
- **Global**: `~/.config/opencode/skill/<name>/SKILL.md`
- **Claude-compatible**: `.claude/skills/<name>/SKILL.md` (project or global)

OpenCode walks up from the working directory to the git worktree root, loading any matching skills along the way.

---

## File Structure

Every skill lives in its own folder with a `SKILL.md` file (all caps required):

```
.opencode/
  skill/
    my-skill-name/
      SKILL.md
```

---

## Required Frontmatter

Every `SKILL.md` must begin with YAML frontmatter containing at minimum:

```yaml
---
name: my-skill-name
description: Concise explanation of when and why to use this skill.
---
```

### Frontmatter Fields

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | 1-64 chars, lowercase alphanumeric with single hyphens, must match folder name |
| `description` | Yes | 1-1024 chars, specific enough for agents to choose correctly |
| `license` | No | License identifier (MIT, Apache-2.0, etc.) |
| `compatibility` | No | Tool compatibility hint (opencode, claude, etc.) |
| `metadata` | No | String-to-string map for custom data |

### Name Validation Rules

The `name` must:
- Be lowercase alphanumeric with single hyphen separators
- Not start or end with `-`
- Not contain consecutive `--`
- Match the containing directory name exactly

Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

**Valid**: `git-release`, `design-principles`, `effect`, `api-testing-v2`  
**Invalid**: `Git-Release`, `git--release`, `-git-release`, `git-release-`

---

## Writing Effective Descriptions

The description appears in the `<available_skills>` section that agents see. It determines whether an agent loads your skill, so craft it carefully.

### Description Best Practices

1. **Be specific about trigger conditions** - When should an agent use this?
2. **Mention key technologies/domains** - Help agents match context
3. **Keep it scannable** - Agents read many skill descriptions quickly
4. **Avoid generic claims** - "Best practices" is vague; "typed error handling with Effect" is specific

### Examples

**Weak description**:
```yaml
description: Helps with coding tasks and best practices.
```

**Strong description**:
```yaml
description: Write idiomatic Effect TypeScript code. Use this skill when working with Effect, @effect/* packages, or projects using Effect for error handling, services, layers, schemas, and functional programming patterns.
```

**Strong description**:
```yaml
description: Enforce a precise, minimal design system inspired by Linear, Notion, and Stripe. Use this skill when building dashboards, admin interfaces, or any UI that needs Jony Ive-level precision.
```

---

## Content Structure

After frontmatter, structure your skill content for maximum utility.

### Recommended Sections

1. **Overview** - Brief context about what this skill covers
2. **Research Strategy** (if applicable) - How to find authoritative information
3. **Core Patterns** - The main techniques/approaches to use
4. **Examples** - Concrete code or workflow examples
5. **Anti-Patterns** - What to avoid
6. **Reference** - Quick lookup tables, cheatsheets

### Writing Style

- **Imperative and direct** - "Use X for Y" not "You might consider using X"
- **Concrete examples** - Show code, not just describe it
- **Opinionated** - Skills should guide decisions, not present options neutrally
- **Scannable** - Use headers, lists, code blocks liberally

---

## Pattern: Research Instructions

For skills about technologies with external documentation, include research strategies:

```markdown
## Research Strategy

When you need [technology]-specific information, use these methods in parallel:

### 1. Search Official Documentation
Use the `tool_name` MCP tool to search official docs:
\`\`\`
tool_name({ query: "your search term" })
\`\`\`

### 2. Search Community Knowledge
The [technology] Discord/forum is indexed on AnswerOverflow:
\`\`\`
answeroverflow_search_answeroverflow({
  query: "your question",
  serverId: "server_id_here"
})
\`\`\`

### 3. Read Source Code Directly
Local source repositories provide authoritative information:
- `~/.llms/repo-name` - Description of what's here
```

---

## Pattern: Decision Frameworks

For skills that guide design/architecture decisions, provide clear frameworks:

```markdown
## Design Direction (REQUIRED)

**Before writing any code, commit to a direction.** Don't default.

### Think About Context

- **What does this product do?** Different domains need different approaches
- **Who uses it?** Power users vs. occasional users have different needs
- **What's the emotional job?** Trust? Efficiency? Delight?

### Choose a Direction

**Option A** - Description and when to use it. Think [example products].

**Option B** - Description and when to use it. Think [example products].

Pick one. Or blend two. But commit to a direction that fits the context.
```

---

## Pattern: Anti-Patterns

Explicitly document what NOT to do:

```markdown
## Anti-Patterns

### Never Do This
- Specific bad practice with why it's bad
- Another bad practice

### Always Question
- "Did I think about X, or did I default?"
- "Is this element Y?"
```

---

## Pattern: Tool Integration

If your skill involves specific MCP tools, document how to use them:

```markdown
## Using the X Tool

The `tool_name` tool provides Y functionality. Use it like this:

\`\`\`typescript
tool_name({
  parameter: "value",
  options: { nested: true }
})
\`\`\`

**When to use**: Description of appropriate scenarios
**When NOT to use**: Scenarios where this tool isn't the right choice
```

---

## Pattern: Authoritative Sources

For technical skills, list trusted sources:

```markdown
### Authoritative Sources

These individuals/sources are highly reliable. Their guidance can be trusted:
- Person Name (role/expertise)
- Official Documentation at URL
- Specific GitHub repo for reference implementations
```

---

## Skill Scope Guidelines

### Good Skill Scope

- **Technology-specific**: Effect, React, Tailwind, specific frameworks
- **Task-specific**: Git releases, API design, database migrations
- **Domain-specific**: Design systems, security practices, accessibility

### Avoid

- **Too broad**: "JavaScript best practices" (scope too large)
- **Too narrow**: "How to center a div" (just use the agent's general knowledge)
- **Redundant**: Don't duplicate what agents already know well

---

## Testing Your Skill

1. **Check discovery**: Run OpenCode and verify your skill appears in the skill tool description
2. **Test triggering**: Ask the agent something that should trigger your skill
3. **Verify loading**: The agent should call `skill({ name: "your-skill" })`
4. **Iterate on description**: If agents don't load it when they should, refine the description

---

## Permissions Configuration

Control skill access in `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

| Permission | Behavior |
|------------|----------|
| `allow` | Skill loads immediately |
| `deny` | Skill hidden from agent |
| `ask` | User prompted before loading |

---

## Complete Example

Here's a complete, well-structured skill:

```markdown
---
name: git-release
description: Create consistent releases and changelogs. Use this skill when preparing tagged releases, writing release notes, or automating version bumps.
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

# Git Release

This skill guides consistent release workflows for projects using GitHub releases.

## Process

1. **Gather changes** - Review merged PRs since last release
2. **Categorize** - Group by type (features, fixes, breaking changes)
3. **Version bump** - Determine semver increment based on changes
4. **Draft notes** - Write user-facing changelog
5. **Create release** - Use `gh release create` command

## Changelog Format

\`\`\`markdown
## What's New

### Features
- Brief description of feature (#PR)

### Fixes
- Brief description of fix (#PR)

### Breaking Changes
- What changed and migration path
\`\`\`

## Commands

Draft a release:
\`\`\`bash
gh release create v1.2.3 --title "v1.2.3" --notes-file CHANGELOG.md
\`\`\`

## Anti-Patterns

- Don't include internal/implementation PRs in user-facing notes
- Don't skip version bumps for breaking changes
- Don't release without reviewing the diff since last tag
```

---

## Checklist

Before finalizing your skill:

- [ ] `name` matches folder name exactly
- [ ] `name` follows validation rules (lowercase, hyphens, no consecutive hyphens)
- [ ] `description` is specific and actionable (1-1024 chars)
- [ ] File is named `SKILL.md` (all caps)
- [ ] Content is opinionated and directive
- [ ] Examples are concrete and copy-pasteable
- [ ] Anti-patterns section exists (if applicable)
- [ ] Skill tested in OpenCode and triggers correctly
