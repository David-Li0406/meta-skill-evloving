# Frontmatter Reference

Complete documentation for YAML frontmatter fields in Claude Code slash commands.

## Required vs Optional

All frontmatter fields are optional. However, `description` is required for:
- Model invocation (Claude auto-triggering the command)
- Appearing in `/help` output

## Fields

### allowed-tools

Specifies which tools the command can use. Without this, the command inherits tools from the current conversation.

**Syntax:**
```yaml
allowed-tools: Tool1, Tool2, Tool3
# or as array
allowed-tools: ["Tool1", "Tool2", "Tool3"]
```

**Bash with wildcards:**
```yaml
# Allow specific command patterns
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*)

# Allow all git commands
allowed-tools: Bash(git:*)

# Allow specific gh commands
allowed-tools: Bash(gh issue view:*), Bash(gh issue list:*), Bash(gh pr create:*)
```

**Common tool names:**
- `Bash` - Shell command execution
- `Read` - Read file contents
- `Write` - Write to files
- `Edit` - Edit files
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `Task` - Create subagent tasks
- `TodoWrite` - Write todo items

**Example combinations:**
```yaml
# Git workflow
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*)

# GitHub CLI operations
allowed-tools: Bash(gh issue:*), Bash(gh pr:*), Bash(gh api:*)

# Code review
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Task"]

# File operations only
allowed-tools: Read, Write, Edit, Glob
```

### description

Brief description shown in `/help` and used by Claude to determine when to auto-invoke.

**Best practices:**
- Keep concise (one line)
- Start with action verb
- Include key trigger words

**Examples:**
```yaml
description: Create a git commit
description: Find duplicate GitHub issues
description: Comprehensive PR review using specialized agents
description: Cleans up all git branches marked as [gone]
```

### argument-hint

Shows expected arguments in autocomplete UI.

**Syntax:**
```yaml
argument-hint: "[issue-number]"
argument-hint: "[branch-name] [commit-type]"
argument-hint: "add [tagId] | remove [tagId] | list"
argument-hint: "[review-aspects]"
```

**Displayed as:**
```
/fix-issue [issue-number]
/commit [branch-name] [commit-type]
```

### model

Override the session model for this command.

**Valid values:**
```yaml
model: claude-haiku-4-5      # Fastest, cost-effective
model: claude-sonnet-4-5     # Balanced
model: claude-opus-4-5       # Most capable
```

**Use cases:**
- Use `claude-haiku-4-5` for simple git operations (faster, cheaper)
- Use `claude-opus-4-5` for complex reasoning tasks
- Omit to inherit session model

**Example:**
```yaml
---
model: claude-haiku-4-5
allowed-tools: Bash(git add:*), Bash(git commit:*)
description: Create a quick git commit
---
```

### disable-model-invocation

Prevents Claude from auto-invoking this command via the SlashCommand tool.

**Values:**
```yaml
disable-model-invocation: true   # Only manual invocation
disable-model-invocation: false  # Allow model invocation (default)
```

**Use when:**
- Command has destructive side effects
- Command requires explicit user intent
- Command is experimental or dangerous

## Complete Examples

### Minimal Command
```yaml
---
description: Analyze code for security issues
---
```

### Git Workflow Command
```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(gh pr create:*)
description: Commit, push, and open a PR
---
```

### Optimized Fast Command
```yaml
---
model: claude-haiku-4-5
allowed-tools: Bash(git add:*), Bash(git commit:*)
description: Quick commit with auto-generated message
---
```

### Complex Review Command
```yaml
---
description: "Comprehensive PR review using specialized agents"
argument-hint: "[review-aspects]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Task"]
---
```

### Protected Command
```yaml
---
description: Deploy to production (dangerous)
allowed-tools: Bash(deploy:*)
disable-model-invocation: true
---
```

## Frontmatter Validation

Common errors to avoid:

1. **Missing `---` delimiters:**
   ```yaml
   # Wrong
   description: My command
   
   # Correct
   ---
   description: My command
   ---
   ```

2. **Invalid YAML syntax:**
   ```yaml
   # Wrong - unquoted special characters
   description: Analyze: find issues
   
   # Correct - quoted
   description: "Analyze: find issues"
   ```

3. **Bash tool without pattern:**
   ```yaml
   # Less secure - allows any bash command
   allowed-tools: Bash
   
   # Better - restricted to specific commands
   allowed-tools: Bash(git:*)
   ```
