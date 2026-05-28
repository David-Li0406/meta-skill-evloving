# Slash Command Creator Reference

Detailed templates, patterns, and examples for creating Claude Code slash commands.

## Command Templates

### Basic Command

```markdown
---
description: <What this command does>
---

# <Command Name>

<Brief explanation>

## Steps

1. <Action 1>
2. <Action 2>
3. <Action 3>

## Reference

- Use `<cli command>` for <purpose>
```

### Command with Arguments

Use `$ARGUMENTS` to accept dynamic input (or `$1`, `$2` for positional args):

```markdown
---
description: Review a pull request by number.
argument-hint: [PR number]
allowed-tools: Bash(gh:*), Read, Grep, Glob
---

Review pull request #$ARGUMENTS

## Steps

1. Fetch PR details with `gh pr view $ARGUMENTS`
2. Review changed files
3. Check for issues against project conventions
4. Provide structured feedback

## Output Format

\`\`\`markdown

## PR Review: #$ARGUMENTS

### Summary

[Brief assessment]

### Issues

- [Issue 1]
- [Issue 2]

### Verdict

[APPROVE / REQUEST CHANGES]
\`\`\`
```

Usage: `/review-pr 123`

### Guardrailed Command

For commands that modify state or have safety constraints:

```markdown
---
description: <What this command does>
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

<!-- MANAGED:START -->

**Guardrails**

- <Safety constraint 1>
- <Safety constraint 2>
- Do not <dangerous action> without confirmation
- Refer to `<reference>` for conventions

**Steps**

1. <Action with verification>
2. <Action with fallback>
3. <Final action with confirmation>

**Reference**

- Use `<command>` for <purpose>
- Check `<file>` if issues occur

<!-- MANAGED:END -->
```

### Multi-Phase Command

For complex workflows with distinct phases:

```markdown
---
description: Complete feature development workflow
argument-hint: [feature name]
---

# Feature Development: $ARGUMENTS

## Phase 1: Planning

1. Understand the requirement
2. Identify affected files
3. Create implementation plan

## Phase 2: Implementation

1. Create/modify necessary files
2. Follow project conventions
3. Add appropriate tests

## Phase 3: Verification

1. Run `pnpm typecheck`
2. Run `pnpm lint`
3. Run `pnpm test`

## Phase 4: Documentation

1. Update relevant documentation
2. Add inline comments where needed

## Output

Provide summary of changes made.
```

### Git Commit Command

```markdown
---
description: Create a conventional git commit
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*), Bash(git diff:*)
argument-hint: [optional message]
---

## Context

- Current status: !`git status`
- Current diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

## Steps

1. Analyze the changes shown above
2. Stage appropriate files
3. Create commit with conventional format: type(scope): description

## Format

Use these types: feat, fix, docs, style, refactor, perf, test, chore
```

## $ARGUMENTS Patterns

### Single Argument

```markdown
Create a new component named $ARGUMENTS

## Steps

1. Create `src/components/$ARGUMENTS.tsx`
```

### Multiple Arguments (Space-Separated)

```markdown
The arguments are: $ARGUMENTS

Parse as needed in your steps.
```

### Positional Arguments

```markdown
---
argument-hint: [type] [name]
---

Create a $1 named $2

## Steps

1. Determine template based on $1
2. Create file named $2
```

### Optional Arguments

```markdown
---
description: Build the project (optional: specific target)
argument-hint: [target]
---

Build target: $ARGUMENTS

## Steps

1. If $ARGUMENTS is empty, run `pnpm build`
2. Otherwise, run `pnpm build:$ARGUMENTS`
```

## Organizing Commands

### By Category (Subdirectories)

```text
.claude/commands/
├── git/
│   ├── commit.md          # Shows as "(project:git)"
│   ├── pr.md
│   └── sync.md
├── dev/
│   ├── feature.md         # Shows as "(project:dev)"
│   └── debug.md
└── docs/
    └── update.md          # Shows as "(project:docs)"
```

### Naming Conventions

| Pattern     | Example            | Use Case           |
| ----------- | ------------------ | ------------------ |
| `verb-noun` | `create-component` | Action commands    |
| `noun`      | `commit`           | Well-known actions |
| `verb`      | `review`           | Context-dependent  |

## Best Practices

### Clear Steps

```markdown
## Steps

1. **Analyze** - Examine the current state
2. **Plan** - Determine necessary changes
3. **Execute** - Make the changes
4. **Verify** - Confirm success
```

### Include Reference Commands

```markdown
## Reference

- Use `gh pr view` to inspect PR details
- Use `git diff` to see changes
- Use `pnpm test` to verify no regressions
```

### Provide Output Format

```markdown
## Output Format

\`\`\`markdown

## Result

**Status**: [Success/Failure]
**Changes Made**:

- [Change 1]
- [Change 2]

**Next Steps**:

- [Recommendation]
  \`\`\`
```

### Use File References

```markdown
Review the implementation considering:

- Main file: @src/utils/helpers.ts
- Tests: @src/utils/helpers.test.ts
- Types: @src/types/helpers.d.ts
```

## SlashCommand Tool Details

### Enabling Automatic Invocation

Reference commands in CLAUDE.md to encourage Claude to use them:

```markdown
When writing tests, run /write-unit-test to generate test files.
After fixing bugs, run /verify-fix to ensure the fix is complete.
```

### Permission Rules

| Rule                     | Matches                     |
| ------------------------ | --------------------------- |
| `SlashCommand:/commit`   | Only `/commit` with no args |
| `SlashCommand:/review:*` | `/review` with any args     |
| `SlashCommand:*`         | All slash commands          |

### Character Budget

The `SlashCommand` tool has a character budget for command descriptions:

- Default: 15,000 characters
- Custom: Set `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var
- When exceeded: Shows "M of N commands" in `/context`

## Complete Examples

### Code Review Command

```markdown
---
description: Review staged changes before commit
allowed-tools: Bash(git:*), Read, Grep, Glob
---

## Context

- Staged changes: !`git diff --cached`
- Modified files: !`git diff --cached --name-only`

## Steps

1. Review each changed file
2. Check against project conventions
3. Look for common issues
4. Provide feedback

## Output

\`\`\`markdown

## Review Summary

### Files Reviewed

- [file1.ts] - [status]
- [file2.ts] - [status]

### Issues

1. [file:line] - [issue description]

### Verdict

[READY TO COMMIT / NEEDS CHANGES]
\`\`\`
```

### Debug Helper Command

```markdown
---
description: Help debug an error message
argument-hint: [error message or file:line]
---

Debug: $ARGUMENTS

## Steps

1. Parse the error location from $ARGUMENTS
2. Read the relevant file and surrounding context
3. Search for related code patterns
4. Identify potential causes
5. Suggest fixes

## Output

\`\`\`markdown

## Debug Analysis

**Error**: [parsed error]
**Location**: [file:line]

### Root Cause

[explanation]

### Fix

[specific code changes]
\`\`\`
```
