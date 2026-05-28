---
name: meta:skill-creator
description: Create new Claude Code skills with proper structure, validation, and best practices. Generates skills that follow Anthropic specifications and community patterns. Use when you need custom skills for specific workflows, either globally or per-project.
---

# Skill Creator

## Quick Start

### Step 1: Create the skill

```sh
mkdir -p .claude/skills/my-skill
```

```markdown
# .claude/skills/my-skill/SKILL.md

---

name: my-skill
description: Brief description of what this skill does. Use when [trigger phrases].

---

# My Skill

## Quick Start

[Minimal example to get started]

## Core Pattern

[Primary code example showing the happy path]

## Common Mistakes

| Mistake | Correct Pattern |
| ------- | --------------- |
| ...     | ...             |

## Delegation

- **Pattern discovery**: Use `Explore` agent

## Additional Resources

- For detailed patterns, see [reference.md](reference.md)
```

### Step 2: Validate (required)

**Always run validation after creating or modifying a skill:**

```sh
uv run .claude/skills/meta-skill-creator/scripts/validate-skill.py .claude/skills/my-skill
```

Fix any errors before committing. Warnings are optional but recommended to address.

## Skill Anatomy

### Directory Structure

```sh
.claude/skills/<skill-name>/
├── SKILL.md              # Main skill file (required, <500 lines)
├── reference.md          # Detailed patterns (optional, <500 lines)
├── <topic>.md            # Topic-specific docs (no limit)
└── scripts/
    └── validate.py       # Utility script (executed, not loaded)
```

### Splitting Large Reference Files

When `reference.md` exceeds 400 lines, split into topic-specific files:

```sh
# Before (inefficient - loads 800+ lines for any query)
.claude/skills/tanstack-start/
├── SKILL.md
└── reference.md          # 800 lines covering everything

# After (efficient - loads only relevant topic)
.claude/skills/tanstack-start/
├── SKILL.md              # Links to topic files
├── middleware.md         # ~150 lines
├── server-functions.md   # ~200 lines
├── api-routes.md         # ~100 lines
└── ssr-modes.md          # ~80 lines
```

> **Tip**: Keep `SKILL.md` under 500 lines for optimal performance. If your content exceeds this, split detailed reference material into separate files.

**Size thresholds:**

| File           | Limit                   | Action                        |
| -------------- | ----------------------- | ----------------------------- |
| `SKILL.md`     | 500 lines (warn at 400) | Split to reference.md         |
| `reference.md` | 500 lines               | Split into topic files        |
| Topic files    | No limit                | Already scoped to one subject |

### Progressive Disclosure

Skills share Claude's context window. To avoid overload, use **progressive disclosure**:

1. SKILL.md loads immediately when skill activates
2. Supporting files (reference.md, topic.md) load **only when Claude needs them**
3. Scripts execute without loading source into context

This means a 200-line SKILL.md + 500-line reference.md only uses ~200 lines upfront. Claude reads reference.md only when the task requires that detail.

### How Claude Discovers Files

Claude discovers supporting files **through links in your SKILL.md**:

```markdown
## Additional Resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

| File Type             | How Claude Uses It                         |
| --------------------- | ------------------------------------------ |
| Documentation (`.md`) | **Loaded** - Claude reads when needed      |
| Scripts               | **Executed** - Runs without reading source |

> **Tip**: Keep references one level deep. Link directly from SKILL.md to reference files. Deeply nested references (A → B → C) may result in Claude partially reading files.

### Utility Scripts (Zero-Context Execution)

Scripts execute without loading source into context - only output consumes tokens. Use for:

- Complex validation logic that's verbose to describe in prose
- Data processing that's more reliable as tested code
- Operations that benefit from consistency across uses

In SKILL.md, tell Claude to **run** the script (not read it):

```markdown
Run the validation script to check the input:

python scripts/validate.py input.pdf
```

See [reference.md](reference.md) for detailed script patterns.

## YAML Frontmatter

### Required Fields

```yaml
---
name: skill-name # Lowercase, numbers, hyphens only (max 64 chars). Must match directory name.
description: What it does. Use when [triggers]. (max 1024 chars)
---
```

### Optional Fields

| Field                      | Purpose                                         | Example                          |
| -------------------------- | ----------------------------------------------- | -------------------------------- |
| `allowed-tools`            | Tools usable without permission prompts         | `Read, Grep, Glob`               |
| `model`                    | Override conversation model                     | `claude-sonnet-4-20250514`       |
| `context`                  | Run in forked sub-agent context                 | `fork`                           |
| `agent`                    | Agent type when `context: fork`                 | `general-purpose`, `Explore`     |
| `hooks`                    | Lifecycle hooks (PreToolUse, PostToolUse, Stop) | See [reference.md](reference.md) |
| `user-invocable`           | Show in `/` slash menu (default: true)          | `false`                          |
| `disable-model-invocation` | Block Skill tool invocation (default: false)    | `true`                           |

### When to Use Optional Fields

**allowed-tools** - Restrict tool access:

- Skill should be read-only? → `Read, Grep, Glob`
- Skill runs specific scripts? → `Bash(python:*), Read`
- Skip permission prompts for common tools? → List them explicitly
- Default (no restriction): Omit field

**model** - Override conversation model:

- Skill needs advanced reasoning? → `claude-sonnet-4-20250514`
- Skill is simple/fast? → `claude-3-5-haiku-20241022`
- Cost-sensitive operations? → Use Haiku
- Default (inherit conversation model): Omit field

**context: fork** - Run in isolated sub-agent:

- Skill does complex multi-step work that would clutter main conversation? → `fork`
- Skill generates lots of intermediate output? → `fork`
- Skill needs its own conversation history? → `fork`
- Default (run in main context): Omit field

**agent** - Agent type for forked context (requires `context: fork`):

- Skill explores codebase? → `Explore`
- Skill plans implementation? → `Plan`
- Skill does general work? → `general-purpose` (default)
- Use custom agent? → Agent name from `.claude/agents/`

**user-invocable** - Show in `/` slash menu:

- Claude should auto-discover but users don't need to invoke directly? → `false`
- Internal standards/patterns applied automatically? → `false`
- Default (show in menu): Omit field or `true`

**disable-model-invocation** - Block Skill tool:

- Only users should invoke (dangerous operations)? → `true`
- Skill requires explicit user consent? → `true`
- Default (Claude can invoke via Skill tool): Omit field or `false`

**hooks** - Lifecycle handlers:

- Need validation before tool runs? → `PreToolUse`
- Need post-processing after tool? → `PostToolUse`
- Need cleanup when skill ends? → `Stop`
- Default (no hooks): Omit field

For detailed configuration examples, see [reference.md](reference.md).

### Skills and Subagents

**Subagents do NOT inherit skills.** To give a custom subagent access, list skills explicitly:

```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Review code for quality and best practices
skills: pr-review, security-check
---
```

The full content of each listed Skill is **injected into the subagent's context at startup** (not just made available for invocation).

> **Important**: Built-in agents (`Explore`, `Plan`, `general-purpose`) have NO skill access. Only custom subagents in `.claude/agents/` with an explicit `skills` field can use Skills.

## Description Writing

The description determines when Claude activates your skill. Optimize for discovery:

**Format:** `[Capability in 5-10 words]. Use for [keyword-packed trigger list].`

```yaml
# ✓ Good - brief capability + dense triggers
description: Drizzle ORM + PostgreSQL database layer. Use for db, database, query, schema, table, migrate, sql, postgres, drizzle, model, relation

# ✗ Bad - filler words waste space
description: Work with Drizzle ORM and PostgreSQL. Use when writing database queries, creating schemas, running migrations, or database operations.

# ✗ Bad - too vague
description: Helps with documents.
```

### Trigger Optimization

Pack the "Use for" section with terms users actually type:

| Include       | Examples                                   |
| ------------- | ------------------------------------------ |
| Abbreviations | db, auth, sql, config, env, deps           |
| Library names | drizzle, tanstack, shadcn, zod             |
| Synonyms      | table/schema/model, query/fetch/get        |
| Action verbs  | add, create, fix, debug, setup, configure  |
| Problem words | error, failing, broken, not working, issue |

> **How Claude discovers skills**: Claude uses semantic understanding, not keyword matching. Trigger words help Claude understand the _domain_ and _intent_ of your skill. "db" works because Claude knows it means database, not because it's looking for exact string matches.

### Before/After Examples

```yaml
# Auth skill - before
description: Implement authentication with Better Auth. Use when adding auth features, protecting routes, or working with sessions.

# Auth skill - after
description: Better Auth authentication. Use for auth, login, logout, session, user, signup, register, protect, middleware, password, oauth, social

# React skill - before
description: React hooks, performance, and state patterns. Use for useEffect decisions, memoization, derived state, re-render optimization, or bundle analysis.

# React skill - after
description: React hooks + performance patterns. Use for useEffect, useMemo, useCallback, memo, rerender, derived state, performance, bundle, optimize
```

## Validation

**Run validation after every skill change.** This catches common issues before they cause problems.

```sh
# Validate a skill directory
uv run .claude/skills/meta-skill-creator/scripts/validate-skill.py .claude/skills/my-skill

# Validate any component type
uv run .claude/skills/meta-skill-creator/scripts/validate-component.py skill .claude/skills/my-skill
uv run .claude/skills/meta-skill-creator/scripts/validate-component.py agent .claude/agents/my-agent.md
uv run .claude/skills/meta-skill-creator/scripts/validate-component.py command .claude/commands/my-cmd.md
```

### Automated Checks (Script)

| Check                 | What It Catches                                  |
| --------------------- | ------------------------------------------------ |
| Frontmatter structure | Missing `---`, missing name/description          |
| Description length    | Over 1024 characters                             |
| Trigger phrase        | Missing "Use for" or "Use when"                  |
| Vague terms           | "helps with", "works with", "handles", "manages" |
| Trigger density       | Fewer than 5 keywords after "Use for"            |
| Description conflicts | Multiple skills with >50% keyword overlap        |
| Line count            | SKILL.md over 500 lines, reference.md over 500   |
| Code blocks           | Missing language specifiers (MD040)              |
| Required sections     | Missing Common Mistakes, Delegation              |
| File linking          | Unlinked reference.md or examples.md             |
| Script permissions    | Non-executable scripts in scripts/               |

### Manual Review (Not Automated)

| Check              | What to Look For                                               |
| ------------------ | -------------------------------------------------------------- |
| Trigger relevance  | Do keywords match what users actually type?                    |
| Synonym coverage   | Include abbreviations (db, auth), library names, problem words |
| Capability clarity | First sentence clearly states what skill does?                 |
| Domain fit         | Triggers appropriate for skill's domain?                       |
| User intent match  | Would a user searching for X find this skill?                  |

## Common Mistakes

| Mistake                       | Impact                 | Correct Pattern                   |
| ----------------------------- | ---------------------- | --------------------------------- |
| Description too generic       | Won't auto-activate    | Include specific trigger keywords |
| SKILL.md over 500 lines       | Context overload       | Split to reference.md             |
| reference.md over 500 lines   | Loads all for any task | Split into topic files            |
| Code blocks without language  | MD040 lint failure     | Always specify: \`\`\`tsx         |
| Supporting files not linked   | Claude won't find them | Add explicit links                |
| Deeply nested references      | Partial loading        | Keep one level deep               |
| Scripts not executable        | Execution fails        | Run `chmod +x scripts/*.py`       |
| Missing external deps note    | Runtime errors         | List in description + body        |
| Built-in agents expect skills | Skills ignored         | Only custom subagents get access  |
| Blank line before frontmatter | YAML parse error       | `---` must be line 1              |

## Skill Locations

| Location   | Path                     | Scope                        |
| ---------- | ------------------------ | ---------------------------- |
| Enterprise | Managed settings         | All users (highest priority) |
| Personal   | `~/.claude/skills/`      | You, all projects            |
| Project    | `.claude/skills/`        | Anyone in repository         |
| Plugin     | `skills/` in plugin root | Plugin users                 |

**Priority**: Enterprise > Personal > Project > Plugin

## Troubleshooting

### Verify Skills Load

Ask Claude: "What Skills are available?"

### Skill Not Triggering

Fix vague descriptions. Include specific actions and trigger keywords.

### Skill Doesn't Load

1. Check file path: Must be exactly `SKILL.md` (case-sensitive)
2. Check YAML: `---` must be on line 1
3. Debug mode: `claude --debug`

## Delegation

- **After creating/modifying skills**: Run `uv run .claude/skills/meta-skill-creator/scripts/validate-skill.py <skill-dir>`
- **Code review**: Delegate to `code-reviewer` agent
- **Pattern discovery**: Use `Explore` agent

## Additional Resources

- For detailed configuration (hooks, allowed-tools, scripts): [reference.md](reference.md)
- For code example patterns: [reference.md](reference.md)

## References

- Official Skills Docs: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills.md)
- Best Practices: [docs.claude.com/.../best-practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- Architecture: [anthropic.com/engineering/...](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
