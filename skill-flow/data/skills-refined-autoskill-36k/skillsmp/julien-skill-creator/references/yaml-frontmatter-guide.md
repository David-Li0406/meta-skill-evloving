# YAML Frontmatter Guide

Complete guide to optional YAML frontmatter fields for Claude Code skills.

> **Last updated**: January 2026

## Table of Contents

- [Version Tracking & Licensing](#version-tracking--licensing)
- [Tool Restrictions (Security)](#tool-restrictions-security)
- [Invocation Control](#invocation-control)
- [Mode Field](#mode-field-mode-command)
- [Lifecycle Hooks](#lifecycle-hooks)
- [Triggers](#triggers-marketplace-extension)
- [Metadata](#metadata-optional)
- [Context Forking](#context-forking)
- [Complete Example](#complete-example)

---

## Version Tracking & Licensing

```yaml
version: "1.0.0"           # Semantic versioning (recommended for hot-reload)
license: Apache-2.0        # Apache-2.0, MIT, or proprietary
```

**When to use**: Always include `version` for tracking updates with hot-reload support.

**Benefits**:
- Hot-reload detects version changes
- Enables rollback capabilities
- Clear update tracking in logs

**Best practices**:
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Bump PATCH for bug fixes
- Bump MINOR for new features
- Bump MAJOR for breaking changes

---

## Tool Restrictions (Security)

```yaml
allowed-tools:             # Whitelist tools Claude can use
  - Read
  - Write
  - Bash
```

**When to use**: Security-sensitive operations (deployment, admin tasks). Limits exposure if skill is compromised.

**Common whitelists**:

| Use Case | Allowed Tools |
|----------|--------------|
| Read-only analysis | `[Read, Grep, Glob]` |
| Documentation | `[Read, Write, Edit]` |
| Deployment | `[Read, Bash]` |
| Development | `[Read, Write, Edit, Bash]` |

**Security benefits**:
- Prevents unauthorized file writes
- Limits command execution
- Reduces attack surface
- Enforces principle of least privilege

---

## Invocation Control

```yaml
user-invocable: true                # Can users call directly via /skill-name? (default: true)
disable-model-invocation: false     # Prevent auto-trigger? (default: false)
```

**When to use**:
- `user-invocable: false` for internal helper skills (only called by other skills)
- `disable-model-invocation: true` for destructive ops (production deploy, data deletion)

**Use cases**:

### user-invocable: false

Internal helper skill that should only be called by other skills:

```yaml
name: internal-validator
description: Internal validation helper
user-invocable: false  # Not in /slash menu
```

### disable-model-invocation: true

Prevent automatic triggering, require explicit user invocation:

```yaml
name: production-deploy
description: Deploy to production server
disable-model-invocation: true  # User must explicitly call it
```

**Safety pattern**: For destructive operations, combine both:

```yaml
user-invocable: true               # Can be invoked via /production-deploy
disable-model-invocation: true     # But won't auto-trigger on keywords
```

---

## Mode Field (Mode Command)

```yaml
mode: true  # Boolean - categorizes skill as "mode command"
```

**What it does**: When `mode: true`, the skill appears in a special "Mode Commands" section at the top of the skills list in Claude Code.

**When to use**: For skills that modify Claude's global behavior or context (e.g., "debug mode", "verbose mode", "strict mode").

### Example

```yaml
name: debug-mode
description: Enable verbose debugging output for all operations
mode: true  # Appears in "Mode Commands" section
```

**Note**: This is a boolean field, NOT `interactive|batch|autonomous` as previously documented.

---

## Lifecycle Hooks

Hooks can be embedded directly in skill frontmatter, scoped to the skill's lifecycle.

### Official Syntax

```yaml
hooks:
  - event: PostToolUse
    matcher:
      tool_name: "Edit|Write|MultiEdit"  # Pipe for OR matching
      file_paths: ["*.py", "src/**/*.ts"]  # Optional: filter by file
    command: "npm run lint"
    once: true  # Optional: run only once per session

  - event: Stop
    command: "./scripts/cleanup.sh"

  - event: PreToolUse
    matcher:
      tool_name: "Bash"
    command: "echo 'About to run bash command'"
```

**When to use**: Environment validation, audit logging, cleanup operations, automated testing.

### Available Events

| Event | Trigger | Common Use Cases |
|-------|---------|------------------|
| `PreToolUse` | Before tool execution | Validate environment, check permissions |
| `PostToolUse` | After tool execution | Run linters, log results, verify state |
| `Stop` | Skill termination | Cleanup temp files, close connections |
| `UserPromptSubmit` | User submits prompt | Add context, validate input |

### Matchers

- `tool_name`: Pattern for tool names (`"Edit"`, `"Edit|Write"`, `"*"` for all)
- `file_paths`: Glob patterns (`["*.py", "api/**/*.py"]`)
- MCP tools: Use prefix `mcp__<server>__<action>`

### The `once` Option

```yaml
hooks:
  - event: PostToolUse
    matcher:
      tool_name: "Write"
    command: "npm run build"
    once: true  # After first Write, hook is removed for this session
```

**Use case**: Run build once after first file write, not after every write.

### Example: Deployment Skill with Hooks

```yaml
name: hostinger-deploy
hooks:
  - event: PreToolUse
    matcher:
      tool_name: "Bash"
    command: "ssh -q hostinger 'echo ok' || exit 1"  # Validate SSH before Bash
  - event: PostToolUse
    matcher:
      tool_name: "Bash"
      file_paths: ["deploy/**"]
    command: "curl -s https://mysite.com/health"  # Health check after deploy
  - event: Stop
    command: "ssh hostinger 'exit'"  # Cleanup SSH connection
```

---

## Triggers (Marketplace Extension)

> **Important**: `triggers` is NOT an official Anthropic field. It's our custom extension for the Claude Code Marketplace keyword routing system.

### Official Approach (Anthropic)

Anthropic's official approach is to embed trigger keywords directly in the `description` field:

```yaml
name: pdf-processing
description: >
  Extract text and tables from PDF files, fill forms, merge documents.
  Use when working with PDF files or when the user mentions PDFs, forms,
  or document extraction.
```

### Our Extension (Marketplace Router)

Our marketplace uses a separate `triggers` field for the fast keyword router:

```yaml
triggers:
  # Keywords (1-2 words)
  - "keyword"
  - "mot-clé"

  # Action phrases (FR + EN)
  - "créer un fichier"
  - "create a file"

  # Problem phrases
  - "I need to..."
  - "comment faire pour..."
```

**ALWAYS include** 10-20 natural language triggers for skills in this marketplace.

### Why Both?

| Field | Purpose | Used By |
|-------|---------|---------|
| `description` | Official triggering mechanism | Claude's built-in skill discovery |
| `triggers` | Fast keyword routing | Our `fast-skill-router.js` hook |

**Best practice**: Include trigger keywords in BOTH `description` AND `triggers` for maximum compatibility.

### Trigger Writing Best Practices

See main SKILL.md Step 8 for complete methodology.

**Quick checklist**:
- ✓ 10-20 triggers (minimum 5, max 50)
- ✓ Bilingual (French + English)
- ✓ Natural language (not jargon)
- ✓ 3 categories: keywords, action phrases, problem phrases

---

## Metadata (Optional)

```yaml
metadata:
  author: "Your Name"
  category: "development"
  keywords: ["keyword1", "keyword2"]
```

**When to use**: Organization, attribution, categorization.

**Benefits**:
- Track authorship
- Enable category-based filtering
- Improve searchability
- Document skill purpose

---

## Context Forking

Run a skill in an isolated subagent context, keeping exploration results separate from the main conversation.

### Syntax

```yaml
---
name: codebase-analysis
description: Analyze entire codebase structure and patterns
context: fork        # Isolated subagent context
agent: Explore       # Use Explore agent type
model: haiku         # Use cheaper model for exploration
---
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `context` | string | `fork` to run in isolated subagent |
| `agent` | string | Agent type: `Explore`, `Plan`, `Bash`, etc. |
| `model` | string | `haiku`, `sonnet`, `opus`, or full model ID |

### When to Use

| Scenario | Recommendation |
|----------|----------------|
| Codebase exploration (>1000 files) | `context: fork` + `agent: Explore` + `model: haiku` |
| Research tasks | `context: fork` |
| Independent sub-tasks | `context: fork` |
| Main code modifications | Do NOT fork (needs main context) |

### Useful Combinations

```yaml
# Lightweight exploration
context: fork
agent: Explore
model: haiku

# Isolated planning
context: fork
agent: Plan
model: sonnet

# Heavy analysis
context: fork
model: opus
```

### Known Limitation

When a skill is invoked via the `Skill()` tool, `context: fork` may be ignored (GitHub issue #17283). The skill may run in the main context instead of spawning a subagent.

---

## Complete Example

```yaml
---
name: excel-report-generator
description: >
  Generates monthly Excel reports with charts and pivot tables from CSV data.
  Use when creating reports, analyzing sales data, or generating spreadsheets.
version: "1.2.0"
license: Apache-2.0
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
triggers:
  - "excel"
  - "report"
  - "créer un rapport"
  - "generate spreadsheet"
  - "analyze sales data"
  - "monthly report"
  - "graphique excel"
  - "pivot table"
  - "I need a report"
  - "comment créer un tableau"
metadata:
  author: "Julien"
  category: "analysis"
  keywords: ["excel", "reporting", "data-analysis"]
---
```

---

## When to Use Each Field

Quick reference table:

| Field | Use Case | Example Scenario |
|-------|----------|------------------|
| `version` | Always (recommended) | Track updates, enable hot-reload |
| `allowed-tools` | Security-sensitive ops | Limit to [Read, Bash] for deployment skill |
| `user-invocable: false` | Internal helper skills | Validation skill called only by other skills |
| `disable-model-invocation: true` | Manual-only workflows | Production deploy requiring explicit approval |
| `mode: true` | Mode commands | Skills that modify Claude's global behavior |
| `context: fork` | Isolated exploration | Large codebase analysis, research tasks |
| `agent` | Custom agent type | Use Explore for search, Plan for architecture |
| `model` | Cost optimization | Use haiku for exploration, opus for complex tasks |
| `hooks` | Lifecycle automation | Linting after writes, cleanup on stop |
| `triggers` | **ALWAYS** (marketplace) | Enable fast keyword routing (10-20 triggers) |
| `metadata` | Organization/attribution | Track authorship, categorize skills |

---

## Hot-Reload Support

With version field:
- Trigger changes reload automatically (no session restart needed)
- Version bumps detected and logged
- Skills in `~/.claude/skills/` or `.claude/skills/` are immediately available

**Recommended workflow**:
1. Update skill content
2. Bump version in YAML frontmatter
3. Save file
4. Changes detected and reloaded automatically

---

## Migration Guide

### Upgrading Existing Skills

**Minimal upgrade** (backward compatible):
```yaml
# Add these 2 fields only
version: "1.0.0"
license: Apache-2.0
```

**Recommended upgrade**:
```yaml
# Add version, license, and triggers
version: "1.0.0"
license: Apache-2.0
triggers:
  - "your"
  - "trigger"
  - "keywords"
```

**Full upgrade** (all optional fields):
```yaml
version: "1.0.0"
license: Apache-2.0
user-invocable: true
allowed-tools: [Read, Write, Bash]
context: fork  # Optional: for isolated execution
agent: Explore  # Optional: specify agent type
model: haiku  # Optional: specify model
hooks:
  - event: PostToolUse
    matcher:
      tool_name: "Write"
    command: "npm run lint"
triggers: [...]
metadata:
  author: "Your Name"
  category: "development"
```

---

## Validation Checklist

Before deploying skills:

- [ ] `name` is max 64 chars, lowercase + hyphens only
- [ ] `description` is non-empty, max 1024 chars, includes trigger keywords
- [ ] `version` follows semantic versioning (X.Y.Z)
- [ ] `license` is valid SPDX identifier (Apache-2.0, MIT, etc.)
- [ ] `allowed-tools` contains only valid tool names
- [ ] `mode` is boolean if used (not interactive/batch/autonomous)
- [ ] `context` is `fork` if used
- [ ] `agent` is valid agent type (Explore, Plan, Bash, etc.)
- [ ] `model` is valid (haiku, sonnet, opus, or full model ID)
- [ ] `hooks` use correct syntax with `matcher` and `command`
- [ ] `triggers` has 10-20 natural language entries (marketplace only)
- [ ] YAML syntax is valid (use yamllint)

---

## Resources

- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [GitHub anthropics/skills](https://github.com/anthropics/skills)
