# Slash Command Format Reference

## File Structure

```
.claude/commands/
├── simple-command.md          # /simple-command
├── grouped/
│   ├── task-a.md              # /grouped/task-a
│   └── task-b.md              # /grouped/task-b
└── my-workflow.md             # /my-workflow
```

## YAML Frontmatter

All fields are optional:

```yaml
---
description: What this command does (shown in /help)
argument-hint: <required-arg> [optional-arg]
allowed-tools: Bash(git:*), Read, Edit
model: claude-3-5-haiku-20241022
disable-model-invocation: true
---
```

### Field Details

**description**
- Displayed when user runs `/help`
- Keep concise (under 80 characters)

**argument-hint**
- Shown during tab-completion
- Convention: `<required>` and `[optional]`
- Examples: `<file>`, `[--verbose]`, `<action> [target]`

**allowed-tools**
- Comma-separated list of tools
- Pattern syntax: `ToolName(pattern:*)` or `ToolName`
- Examples:
  - `Bash(git:*)` - Allow all git commands
  - `Bash(npm run:*)` - Allow npm run scripts
  - `Read, Edit` - Allow file read and edit
  - `Bash(docker compose:*)` - Allow docker compose commands

**model**
- Override the default model
- Use model identifiers like:
  - Haiku models - Faster, cheaper
  - Sonnet models - Balanced
  - Opus models - Most capable
- Refer to official documentation for current model identifiers

**disable-model-invocation**
- When `true`, prevents Claude from invoking this command via SlashCommand tool
- Use for commands that should only be triggered by user

## Argument Syntax

### All Arguments

`$ARGUMENTS` captures everything after the command name:

```markdown
Analyze this file: $ARGUMENTS
```

Usage: `/analyze src/main.ts --verbose` -> `Analyze this file: src/main.ts --verbose`

### Positional Arguments

`$1`, `$2`, etc. for specific positions:

```markdown
Compare $1 with $2 and explain the differences.
```

Usage: `/compare old.ts new.ts` -> `Compare old.ts with new.ts and explain the differences.`

### Default Values

Handle missing arguments gracefully:

```markdown
Review the following code for $ARGUMENTS

If no specific focus area is provided, do a general code review covering:
- Code quality
- Performance
- Security
```

## Special Prefixes

### Bash Command Output (`!`)

Include output of a shell command:

```markdown
Current git status:
!git status

Based on the above, suggest next steps.
```

### File Content (`@`)

Include file contents:

```markdown
Review this configuration:
@tsconfig.json

Check for any issues or improvements.
```

## Examples

### Simple Command

```markdown
---
description: Quick code review
argument-hint: <file-or-description>
---

Review this code and provide feedback on:
- Readability
- Performance
- Best practices

$ARGUMENTS
```

### Command with Tool Permissions

```markdown
---
description: Run tests and fix failures
allowed-tools: Bash(npm test:*), Read, Edit
---

Run the test suite and fix any failing tests:

!npm test

If there are failures, analyze and fix them.
$ARGUMENTS
```

### Command with File Context

```markdown
---
description: Update component based on design system
argument-hint: <component-file>
---

Update this component to follow our design system:

Design tokens:
@src/styles/tokens.ts

Component to update:
@$1

Apply consistent styling patterns.
```

### Workflow Command

```markdown
---
description: Prepare PR for review
allowed-tools: Bash(git:*), Read
---

Prepare this branch for PR review:

1. Check current status:
!git status

2. Show recent commits:
!git log --oneline -5

3. Review the changes and suggest:
   - PR title
   - PR description
   - Any issues to address before merging

Focus: $ARGUMENTS
```

## Tips

1. **Test with edge cases** - Empty arguments, special characters, long inputs
2. **Use allowed-tools sparingly** - Only what's needed
3. **Provide context** - Help Claude understand the goal
4. **Be specific** - Vague prompts get vague results
5. **Chain commands** - Keep each command focused, combine in workflows
