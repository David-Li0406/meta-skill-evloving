# Agent YAML Frontmatter Schema Reference

Complete specification for Claude Code agent frontmatter fields (January 2026).

---

## Required Fields

### name

- **Type**: string
- **Max Length**: 64 characters
- **Format**: lowercase letters, numbers, hyphens only
- **Purpose**: Unique identifier for the agent

```yaml
name: code-reviewer          # Good
name: Code_Reviewer          # Invalid - uppercase, underscores
name: my-super-awesome-long-agent-name-that-exceeds-the-limit  # Invalid - too long
```

### description

- **Type**: string
- **Max Length**: 1024 characters
- **Purpose**: Claude uses this to decide when to delegate tasks to this agent

**Required Elements:**

1. Action verbs (what it does)
2. Trigger phrases (when to use)
3. Domain keywords (topic areas)

```yaml
# Good - includes all elements
description: 'Review Python code for security vulnerabilities, performance issues, and PEP 8 compliance. Use when code changes are complete or when reviewing pull requests. Specializes in async/await patterns.'

# Bad - too vague
description: Helps with Python
```

### YAML Multiline Bug

**Do NOT use YAML multiline indicators** (`>-`, `|`, `|-`) for descriptions. Claude Code's indexer does not parse them correctly - the description appears as ">-" instead of actual content.

```yaml
# WRONG - will show ">-" as description
description: >-
  This is a multiline
  description that breaks.

# CORRECT - single quoted string
description: 'This works correctly. Use single quotes for descriptions with special characters or keep on one line.'
```

---

## Optional Fields

### model

- **Type**: string
- **Default**: sonnet (inherited from parent)
- **Options**: `sonnet`, `opus`, `haiku`, `inherit`

| Value     | Use Case                               |
| --------- | -------------------------------------- |
| `haiku`   | Fast, simple operations (search, read) |
| `sonnet`  | Balanced - most agents (default)       |
| `opus`    | Complex reasoning, difficult debugging |
| `inherit` | Match parent conversation model        |

```yaml
model: sonnet
```

#### When to Use `model: inherit`

The `inherit` option makes the agent use the same model as the parent conversation rather than a fixed model.

**Use `model: inherit` when:**

1. **Context-appropriate capability** - Agent should match user's model choice

   - User chose Opus for complex work → agent gets Opus
   - User chose Haiku for speed → agent gets Haiku
   - Agent adapts to conversation context

2. **User-controlled cost/capability trade-off** - Let user decide model via conversation settings

   - User sets model at conversation level
   - Agent respects that choice automatically
   - No need to change agent configuration

3. **Flexible workflows** - Agent is used in multiple contexts with different needs
   - Research phase (might use Haiku for speed)
   - Implementation phase (might use Opus for complexity)
   - Same agent, different requirements per context

**Use explicit model (`sonnet`, `opus`, `haiku`) when:**

1. **Task requires specific capability** - Agent needs minimum model capability

   - Complex debugging always needs `opus`
   - Simple file search always works with `haiku`
   - Task complexity is known and fixed

2. **Cost control** - Prevent unexpected high costs

   - Read-only analyzer should stay `haiku` even if parent uses Opus
   - Prevents accidental expensive operations

3. **Consistent behavior** - Agent must perform the same way every time
   - Production agents with SLAs
   - Agents where capability variance is unacceptable

**Decision Tree:**

```
Does the task REQUIRE a specific model capability?
├─ Yes → Use explicit model (opus/sonnet/haiku)
└─ No → Should the agent adapt to user's choice?
   ├─ Yes → Use `inherit`
   └─ No → Use `sonnet` (safe default)
```

**Examples:**

```yaml
# Inherit - adapts to conversation context
name: general-helper
model: inherit
description: Helps with various tasks matching conversation complexity

# Explicit Haiku - always fast and cheap
name: file-searcher
model: haiku
description: Search files for patterns (simple task)

# Explicit Opus - always maximum capability
name: architecture-reviewer
model: opus
description: Review system architecture for flaws (complex task)

# Explicit Sonnet - balanced default
name: code-writer
model: sonnet
description: Write production code (moderate complexity)
```

### tools

- **Type**: string or array
- **Default**: Inherited from parent conversation
- **Purpose**: ALLOWLIST - only these tools available

```yaml
# String format (comma-separated)
tools: Read, Grep, Glob, Bash

# Array format
tools:
  - Read
  - Grep
  - Glob

# Pattern matching for specific commands
tools: Bash(git:*), Bash(npm:install)
```

**Available Tools**: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, WebSearch, WebFetch, Task, TodoWrite, Skill

### disallowedTools

- **Type**: string or array
- **Default**: none
- **Purpose**: DENYLIST - remove from inherited tools

```yaml
disallowedTools: Write, Edit, Bash
```

### permissionMode

- **Type**: string
- **Default**: `default`
- **Options**:

| Mode                | File Edits   | Bash Commands       | Description                |
| ------------------- | ------------ | ------------------- | -------------------------- |
| `default`           | Prompts user | Prompts user        | Normal permission behavior |
| `acceptEdits`       | Auto-accepts | Prompts destructive | Good for documentation     |
| `dontAsk`           | Auto-denies  | Auto-denies         | Read-only operation        |
| `bypassPermissions` | Skips all    | Skips all           | Dangerous - trusted only   |
| `plan`              | Disabled     | Disabled            | Planning mode, no writes   |

```yaml
permissionMode: acceptEdits
```

### skills

- **Type**: string or array
- **Default**: none (skills NOT inherited)
- **Purpose**: Load skill content into agent context

```yaml
# Comma-separated string
skills: python-development, testing-patterns, security-best-practices

# Array format
skills:
  - python-development
  - testing-patterns
```

**Important**: Agents do NOT inherit skills from parent conversation. Must explicitly list needed skills.

### hooks

- **Type**: object
- **Default**: none
- **Purpose**: Lifecycle hooks scoped to this agent

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          timeout: 5000
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
```

**Hook Events:**

- `PreToolUse` - Before tool executes (can block with exit 2)
- `PostToolUse` - After tool succeeds
- `PermissionRequest` - When permission needed
- `Stop` - When agent completes
- `SubagentStop` - When child agent completes

### color

- **Type**: string
- **Default**: none
- **Purpose**: Terminal output color for agent messages

```yaml
color: cyan      # Analysis agents
color: yellow    # Warning/optimization
color: green     # Success/validation
color: orange    # Audit/review
color: red       # Error handling
```

---

## Complete Example

```yaml
---
name: security-auditor
description: 'Audit code for security vulnerabilities including OWASP Top 10, injection risks, and authentication flaws. Use when reviewing security-sensitive code or before production deployment. Proactively invoked after changes to auth or data handling code.'
model: opus
tools: Read, Grep, Glob, Bash(git:log), Bash(git:diff)
disallowedTools: Write, Edit
permissionMode: dontAsk
skills: security-best-practices, owasp-guidelines
hooks:
  Stop:
    - hooks:
        - type: command
          command: "./scripts/log-audit.sh"
color: red
---
```

---

## Validation Rules

Before saving an agent, verify:

1. **name**

   - [ ] Lowercase only
   - [ ] Only letters, numbers, hyphens
   - [ ] Max 64 characters
   - [ ] Unique in project

2. **description**

   - [ ] Max 1024 characters
   - [ ] Contains action verbs
   - [ ] Contains trigger phrases
   - [ ] Contains relevant keywords

3. **model** (if specified)

   - [ ] Valid option: sonnet, opus, haiku, inherit

4. **tools** (if specified)

   - [ ] All tools are valid tool names
   - [ ] Pattern syntax correct for Bash restrictions

5. **skills** (if specified)

   - [ ] All skills exist in project

6. **permissionMode** (if specified)

   - [ ] Valid option with justification if bypassPermissions

7. **YAML syntax**
   - [ ] Valid YAML
   - [ ] Proper quoting for multiline strings
   - [ ] No trailing commas or syntax errors
