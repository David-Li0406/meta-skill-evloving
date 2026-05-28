# Skill Reference

Project-specific patterns and frontmatter specifications.

## Frontmatter Specification

### Required Fields

```yaml
---
name: skill-name
description: What it does. Use when [context].
---
```

**name:**
- Max 64 characters
- Lowercase letters, numbers, hyphens only
- No XML tags
- No reserved words: "anthropic", "claude"

**description:**
- Max 1024 characters
- Non-empty
- No XML tags
- Third person ("Processes files", not "I process files")

### Optional Fields

```yaml
---
name: skill-name
description: What it does. Use when [context].
context: fork
agent: haiku
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Edit
hooks:
  PreToolUse:
    - command: echo "Before tool"
  PostToolUse:
    - command: echo "After tool"
  Stop:
    - command: echo "Skill completed"
---
```

| Field | Type | Description |
|-------|------|-------------|
| `context` | `fork` | Run skill in forked sub-agent context |
| `agent` | `haiku` \| `sonnet` \| `opus` | Specify agent type for execution |
| `user-invocable` | `boolean` | Show in slash command menu (default: true) |
| `allowed-tools` | `list` | Restrict tools available during skill execution |
| `hooks` | `object` | Lifecycle hooks scoped to skill |

### Hooks

Hooks execute shell commands at skill lifecycle events:

```yaml
hooks:
  PreToolUse:
    - command: ./scripts/before-tool.sh
      timeout: 5000
  PostToolUse:
    - command: ./scripts/after-tool.sh
  Stop:
    - command: ./scripts/cleanup.sh
```

**Hook types:**
- `PreToolUse` - Before each tool invocation
- `PostToolUse` - After each tool invocation
- `Stop` - When skill execution completes

### Allowed Tools

Restrict which tools the skill can use:

```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
```

Use YAML list syntax for cleaner declarations.

---

## Skill Categories

### Operational Skills

**Examples:** `spec-create`, `spec-archive`

**Characteristics:**
- Multi-step workflow modifying files/state
- Creates or moves files on disk
- Updates tracking documents
- Clear success criteria

**Pattern:**
```
1. Validate input
2. Gather context
3. Perform operations
4. Update indices
5. Report completion
```

### Generation Skills

**Examples:** `spec-issues-create`

**Characteristics:**
- Transform one format to another
- Generate structured output
- Often include helper scripts
- Reference authoritative framework docs

**Pattern:**
```
1. Validate source
2. Detect/parse input type
3. Apply templates
4. Generate output
5. Provide usage instructions
```

### Guidance Skills

**Examples:** `code-implement`, `code-debug`

**Characteristics:**
- Provide patterns and best practices
- Imperative style ("DO this", "DON'T do that")
- Code examples and snippets

**Pattern:**
```
- Core principles
- Do/Don't examples
- Code patterns
- Integration notes
```

---

## Progressive Disclosure

**Level 1 (Metadata):** Name + description loaded at startup
**Level 2 (SKILL.md):** Loaded when skill invoked
**Level 3 (Resources):** Loaded on-demand during execution

**Token budgets:**
- SKILL.md body: <500 lines (soft limit)
- Description: <1024 characters
- Name: <64 characters

---

## Command Delegation Pattern

Commands can delegate to skills for reusability:

**Command (~20 lines):**
```markdown
---
description: Create planning documents for task
---

## User Input

```text
$ARGUMENTS
```

## Task

Use the `spec-create` skill to create planning documents.

**Input:** `$ARGUMENTS` (optional - spec name)

Follow the spec-create skill workflow.

> **See**: `.claude/skills/spec-create/SKILL.md`
```

**Benefits:**
- Commands are thin wrappers
- Skills contain all logic
- Reusable across contexts

---

## Directory Conventions

**Project standard:**
```
.claude/skills/{skill-name}/
├── SKILL.md              # Main instructions (<500 lines)
├── templates/            # Document templates (.md)
├── scripts/              # Executable code (.sh, .py)
└── references/           # Extended documentation
```

**Official standard (also valid):**
```
skill-name/
├── SKILL.md
├── scripts/              # Executable code
├── references/           # Documentation for context
└── assets/               # Files used in output
```

---

## Anti-Patterns

**Don't:**
- Put trigger strings in description (use skill-rules.json)
- Exceed 500 lines in SKILL.md
- Duplicate comprehensive framework docs
- Use emojis (use text markers)
- Use Windows-style paths (`\` instead of `/`)
- Create deeply nested references
- Include information Claude already knows
- Use reserved words in name

**Do:**
- Keep SKILL.md focused and concise
- Extract templates to separate files
- Reference authoritative docs
- Use progressive disclosure
- Provide concrete examples
- Define clear success criteria
- Test with real usage

---

## Integration

### With Other Skills

Reference related skills in documentation:
```markdown
## Related
- `spec-validate` - Clarify requirements before creation
- `spec-archive` - Archive completed specs
```

### With Project Docs

Point to authoritative sources:
```markdown
> **See**: CLAUDE.md for project conventions
> **See**: .plan/issues/README.md for issue tracking
```

---

## Testing Checklist

After creating a skill:

1. **Discovery:** Does the description trigger correctly?
2. **Resources:** Can Claude find bundled files?
3. **Workflow:** Do steps complete successfully?
4. **Paths:** Do all links work?
5. **Models:** Does it work with Haiku/Sonnet/Opus?
