---
name: claude-skills-overview-2026
description: Reference guide for Claude Code skills system (January 2026). Use when creating, modifying, or understanding skills, SKILL.md format, frontmatter fields, hooks, context fork, or skill best practices.
---

# Claude Code Skills System - Complete Reference (January 2026)

Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`.

**Skills and slash commands are now unified** - they are the same system. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work identically. Skills are the recommended approach as they support additional features like supporting files and advanced frontmatter options.

---

## SKILL.md Complete Format

```yaml
---
name: skill-identifier
description: What this Skill does and when to use it
argument-hint: "[optional-arg]"
allowed-tools: Read, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
user-invocable: true
disable-model-invocation: false
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
---

# Skill Title

Your instructions here...
```

---

## All Frontmatter Fields

All fields are optional. Only `description` is recommended so Claude knows when to use the skill.

| Field                      | Required    | Type         | Max Length | Description                                                                                                                                           |
| -------------------------- | ----------- | ------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | No          | string       | 64 chars   | Display name for the skill. If omitted, uses the directory name. Lowercase letters, numbers, and hyphens only.                                        |
| `description`              | Recommended | string       | 1024 chars | What the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. |
| `argument-hint`            | No          | string       | —          | Hint shown during autocomplete to indicate expected arguments. Example: `[issue-number]` or `[filename] [format]`.                                    |
| `allowed-tools`            | No          | string/array | —          | Tools Claude can use without asking permission when this skill is active. Example: `Read, Grep, Glob, Bash(npm run:*)`                                |
| `model`                    | No          | string       | —          | Model to use when this skill is active. Example: `claude-opus-4-5-20251101`, `claude-sonnet-4-20250514`                                               |
| `context`                  | No          | string       | —          | Set to `fork` to run in a forked subagent context. See [Context Fork Behavior](#context-fork-behavior) for tool restrictions.                         |
| `agent`                    | No          | string       | —          | Which subagent type to use when `context: fork` is set. Options: `Explore`, `Plan`, `general-purpose`, or custom agent. Default: `general-purpose`    |
| `user-invocable`           | No          | boolean      | —          | Set to `false` to hide from the `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`.                              |
| `disable-model-invocation` | No          | boolean      | —          | Set to `true` to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with `/name`. Default: `false`. |
| `hooks`                    | No          | object       | —          | Hooks scoped to this skill's lifecycle. See [Hooks](/en/hooks) for configuration format. Events: `PreToolUse`, `PostToolUse`, `Stop`                  |

---

## Skill Tokenomics

Skills use progressive disclosure - only frontmatter loads initially (~100 tokens), full content loads on activation.

### Budget Constraints

| Resource                   | Limit         | Notes                               |
| -------------------------- | ------------- | ----------------------------------- |
| `name` field               | 64 chars      | Lowercase, numbers, hyphens only    |
| `description` field        | 1024 chars    | Critical for skill selection        |
| `<available_skills>` block | ~15,000 chars | Separate from global context window |
| Skills before truncation   | ~34-36        | Varies by description complexity    |

### YAML Multiline Bug

**Do NOT use YAML multiline indicators** (`>-`, `|`, `|-`) for descriptions. Claude Code's skill indexer does not parse them correctly - the description appears as ">-" instead of actual content.

```yaml
# WRONG - will show ">-" as description
description: >-
  This is a multiline
  description that breaks.

# WRONG - same problem
description: |
  This breaks too.

# CORRECT - single quoted string
description: 'This works correctly. Use single quotes for descriptions with special characters or keep on one line.'
```

### Truncation Behavior

When total skill metadata exceeds ~15,000 characters:

1. Skills are truncated from the `<available_skills>` block
2. Truncated skills cannot be auto-invoked by Claude
3. User can still invoke truncated skills explicitly with `/skill-name`

### Fallback Strategy

If you have many skills, embed pointers in CLAUDE.md as a safeguard:

```markdown
## Skills Available
- For debugging: use `/scientific-thinking` skill
- For delegation: use `/delegate` skill
```

This ensures Claude can find skills even if truncated from `<available_skills>`.

---

## String Substitutions

Skills support string substitution for dynamic values in the skill content:

| Variable               | Description                                                                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | All arguments passed when invoking the skill. If `$ARGUMENTS` is not present in the content, arguments are appended as `ARGUMENTS: <value>`. |
| `${CLAUDE_SESSION_ID}` | The current session ID. Useful for logging, creating session-specific files, or correlating skill output with sessions.                      |

---

## Dynamic Context Injection

The `!`command\`\` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself.

**Example**: This skill summarizes a pull request by fetching live PR data with the GitHub CLI:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh:*)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

**How it works**:

1. Each `!`command\`\` executes immediately (before Claude sees anything)
2. The output replaces the placeholder in the skill content
3. Claude receives the fully-rendered prompt with actual PR data

**This is preprocessing**, not something Claude executes. Claude only sees the final result.

**Source**: Official documentation at <https://code.claude.com/docs/en/skills.md> (section: "Inject dynamic context")

---

## Directory Structure

```
skill-name/
├── SKILL.md              # Required
├── references/           # Optional: docs loaded on demand
├── scripts/              # Optional: executed, not loaded into context
└── templates/            # Optional: reusable content
```

### Location Priority (Highest to Lowest)

1. **Managed/Enterprise** - System-level
2. **Personal** - `~/.claude/skills/`
3. **Project** - `.claude/skills/`
4. **Plugin** - Bundled with plugins

---

## Hooks in Skills

### Hook Events

- `PreToolUse`: Before tool executes
- `PostToolUse`: After successful execution
- `Stop`: When Skill finishes

### Hook Structure

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"           # Regex pattern
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true            # Run only once per session
```

### Hook I/O

- Receives JSON via stdin (session info, tool name, parameters)
- Exit 0: Success
- Exit 2: Blocking error (prevents tool, shows stderr)
- Other: Non-blocking error

---

## Context Fork Behavior

Add `context: fork` to your frontmatter when you want a skill to run in isolation. The skill content becomes the prompt that drives the subagent. It won't have access to your conversation history.

**WARNING**: `context: fork` only makes sense for skills with explicit instructions. If your skill contains guidelines like "use these API conventions" without a task, the subagent receives the guidelines but no actionable prompt, and returns without meaningful output.

### Agent Types

```yaml
context: fork
agent: Explore
```

| Agent             | Model    | Tools                      | Use Case                     |
| ----------------- | -------- | -------------------------- | ---------------------------- |
| `Explore`         | Haiku    | File/web/MCP (read-only)   | Fast codebase analysis       |
| `Plan`            | Inherits | File/web/MCP (read-only)   | Research before planning     |
| `general-purpose` | Inherits | File/web/MCP + Bash/system | Complex operations (default) |
| Custom            | Custom   | Custom                     | Project-specific work        |

### Tool Restrictions in Forked Contexts

**VERIFIED BEHAVIOR** (experimentally confirmed 2026-01-22):

When `context: fork` is set, the forked subagent has access to:

- File operations: Read, Write, Edit, Grep, Glob
- Web operations: WebSearch, WebFetch
- MCP tools (if configured)
- Bash and other system tools (depending on agent type)

**The Task tool is NOT available in forked contexts.** This means forked skills cannot delegate to other subagents. If you need hierarchical delegation (subagent delegates to another subagent), the parent must run in the main context (no `context: fork`), not in a forked context.

**Source**: Experimental verification on 2026-01-22. Official documentation at <https://code.claude.com/docs/en/skills.md> does not explicitly document this restriction.

### Skills vs Subagents

Skills and subagents work together in two directions:

| Approach                     | System prompt                             | Task                        | Also loads                   |
| ---------------------------- | ----------------------------------------- | --------------------------- | ---------------------------- |
| Skill with `context: fork`   | From agent type (`Explore`, `Plan`, etc.) | SKILL.md content            | CLAUDE.md                    |
| Subagent with `skills` field | Subagent's markdown body                  | Claude's delegation message | Preloaded skills + CLAUDE.md |

With `context: fork`, you write the task in your skill and pick an agent type to execute it. For the inverse (defining a custom subagent that uses skills as reference material), see the Sub-Agents documentation.

---

## Description Best Practices

**Good**:

```yaml
description: Extract text and tables from PDFs, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, extraction.
```

**Bad**:

```yaml
description: Helps with documents
```

**Template**:

```
[Action 1], [Action 2], [Action 3]. Use when [situation 1], [situation 2],
or when the user mentions [keywords].
```

---

## Examples

### Simple Skill

```yaml
---
name: commit-messages
description: Generate conventional commit messages from git diffs. Use when writing commits.
---

# Commit Messages

1. Run `git diff --staged`
2. Determine type (feat, fix, docs)
3. Write message under 50 chars
4. Use imperative mood
```

### Tool-Restricted

```yaml
---
name: safe-reader
description: Read files without changes. Use for code review.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Safe Reader

ONLY read files. Never modify.
```

### Forked Context

```yaml
---
name: deep-research
description: Thorough codebase research. Use for complex investigations.
context: fork
agent: Explore
---

# Deep Research

Runs in isolated context to avoid polluting main conversation.
```

### With Hooks

```yaml
---
name: secure-ops
description: Audit-logged file operations.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
---

# Secure Operations

All modifications logged and validated.
```

### Hidden from Users

```yaml
---
name: internal-standards
description: Auto-apply code review standards.
user-invocable: false
---

Claude invokes this, users don't see it in menu.
```

### User-Only (No Auto-Invoke)

```yaml
---
name: deploy-production
description: Deploy to production.
disable-model-invocation: true
---

Only runs when user types `/deploy-production`.
```

---

## Skills vs Other Features

**Note**: Skills and slash commands are now the same system. Files in `.claude/commands/` still work but skills are recommended.

| Feature         | Invocation            | Use Case                                     |
| --------------- | --------------------- | -------------------------------------------- |
| **Skills**      | Claude decides OR `/` | Specialized knowledge/workflows, auto-invoke |
| **CLAUDE.md**   | Always loaded         | Project-wide instructions                    |
| **Subagents**   | Claude delegates      | Isolated complex operations                  |
| **MCP Servers** | Claude calls          | External tools/data                          |
| **Hooks**       | Tool events           | Automate actions                             |

---

## Installation

**Marketplace**:

```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**Manual**: Copy to `~/.claude/skills/` or `.claude/skills/`

**Hot Reload**: Changes apply immediately without restart.

---

## Recent Updates (2.1+)

- **Unified skills and commands** - `.claude/commands/` files now work as skills, skills recommended
- **Dynamic context injection** - `!`command\`\` syntax for preprocessing shell command output
- **`argument-hint` field** - Show autocomplete hints for expected arguments
- **Optional name/description** - If omitted, uses directory name and first paragraph
- **`once: true` for hooks** - Run only once per session
- **`${CLAUDE_SESSION_ID}`** - Session-scoped operations
- **15,000 character budget** for skill metadata
- **`context: fork`** with agent selection
- **Hot reload** - immediate updates without restart

---

## Sources

- **Primary**: [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills.md) (accessed 2026-01-22)
- **Standards**: [Agent Skills Open Standard](https://agentskills.io)
- **Examples**: [anthropics/skills](https://github.com/anthropics/skills)
- **Blog**: [Anthropic Engineering Blog - Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Experimental**: Context fork tool restrictions verified 2026-01-22
