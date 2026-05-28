---
name: claude-command-authoring
description: Use this skill when creating slash commands, writing command files, or when "/command", ".claude/commands", "$ARGUMENTS", or "create command" are mentioned.
---

# Claude Command Authoring

Create custom slash commands that extend Claude Code with reusable prompts and workflows.

## Commands vs Skills

**Critical distinction**:

| Aspect         | Commands (This Skill)                   | Skills                                 |
| -------------- | --------------------------------------- | -------------------------------------- |
| **Purpose**    | Reusable prompts invoked by users       | Capability packages auto-triggered     |
| **Invocation** | Explicit: `/command-name args`          | Automatic (model-triggered by context) |
| **Location**   | `commands/` directory                   | `skills/` directory with `SKILL.md`    |
| **Structure**  | Single `.md` file                       | Directory with resources               |
| **Arguments**  | `$1`, `$2`, `$ARGUMENTS`                | No argument system                     |

Commands are user-initiated. Skills are model-initiated.

---

## Quick Start

### Basic Command

Create `.claude/commands/review.md`:

```markdown
---
description: Review code for best practices and issues
---

Review the following code for:
- Code quality and readability
- Potential bugs or edge cases
- Performance considerations
- Security concerns
```

Use with: `/review`

### Command with Arguments

Create `.claude/commands/fix-issue.md`:

```markdown
---
description: Fix a specific GitHub issue
argument-hint: <issue-number>
---

Fix issue #$1 following our coding standards.
Review the issue, implement a fix, add tests, and create a commit.
```

Use with: `/fix-issue 123`

### Command with Context

Create `.claude/commands/commit.md`:

```markdown
---
description: Create git commit from staged changes
allowed-tools: Bash(git *)
---

## Context

Current branch: !`git branch --show-current`
Staged changes: !`git diff --staged`
Recent commits: !`git log --oneline -5`

## Task

Create a commit with a clear message based on the staged changes.
```

Use with: `/commit`

---

## Workflow Overview

1. **Discovery** - Define purpose, scope, and target users.
2. **Design** - Choose features and configurations for the commands.
3. **Implementation** - Write the command files in the appropriate directory.
4. **Testing** - Validate the commands to ensure they work as intended.
5. **Deployment** - Make the commands available for user invocation.