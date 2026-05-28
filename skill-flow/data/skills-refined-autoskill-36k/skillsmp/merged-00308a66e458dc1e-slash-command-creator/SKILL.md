---
name: slash-command-creator
description: Use this skill when creating or updating Claude Code slash commands, automating workflows, or seeking guidance on command structure and best practices.
---

# Slash Command Creator

Create custom slash commands for Claude Code to automate frequently-used prompts.

## Overview

Slash commands are markdown files stored in `.claude/commands/` (project-level) or `~/.claude/commands/` (global/user-level) that get expanded into prompts when invoked. They're ideal for:

- Repetitive workflows (code review, PR submission, CI fixing)
- Multi-step processes that need consistency
- Agent delegation patterns
- Project-specific automation

## Command Structure

Every slash command is a markdown file with optional YAML frontmatter:

```markdown
---
description: Brief description shown in /help (required)
argument-hint: <placeholder> (optional, if command takes arguments)
---

# Command Title

[Detailed instructions for the agent to execute autonomously]
```

## Command Creation Workflow

### Step 1: Determine Location

**Auto-detect the appropriate location:**

1. Check git repository status: `git rev-parse --is-inside-work-tree 2>/dev/null`
2. Default location:
   - If in git repo → Project-level: `.claude/commands/`
   - If not in git repo → Global: `~/.claude/commands/`
3. Allow user override:
   - If user explicitly mentions "global" or "user-level" → Use `~/.claude/commands/`
   - If user explicitly mentions "project" or "project-level" → Use `.claude/commands/`

Report the chosen location to the user before proceeding.

### Step 2: Show Command Patterns

Help the user understand different command types. Load **references/patterns.md** to see available patterns:

- **Workflow Automation** - Analyze → Act → Report
- **Iterative Fixing** - Run → Parse → Fix → Repeat
- **Agent Delegation** - Context → Delegate → Iterate
- **Simple Execution** - Run command with args

Ask the user: "Which pattern is closest to what you want to create?" This helps frame the conversation.

### Step 3: Gather Command Information

Ask the user for key information:

#### A. Command Name and Purpose

Ask:

- "What should the command be called?" (for filename)
- "What does this command do?" (for description field)

Guidelines:

- Command names MUST be kebab-case (hyphens, NOT underscores)
- File names match command names: `my-command.md` → invoked as `/my-command`
- Description should be concise, action-oriented (appears in `/help` output)

#### B. Arguments

Ask:

- "Does this command take any arguments?"
- "Are arguments required or optional?"
- "What should arguments represent?"

If command takes arguments:

- Add `argument-hint: <placeholder>` to frontmatter
- Use `<angle-brackets>` for required arguments
- Use `[square-brackets]` for optional arguments

#### C. Workflow Steps

Ask:

- "What are the specific steps this command should follow?"
- "What order should they happen in?"
- "What tools or commands should be used?"

Gather details about:

- Initial analysis or checks to perform
- Main actions to take
- How to handle results
- Success criteria
- Error handling approach

#### D. Tool Restrictions and Guidance

Ask:

- "Should this command use any specific agents or tools?"
- "Are there any tools or operations it should avoid?"
- "Should it read any specific files for context?"

### Step 4: Generate Optimized Command

Create the command file with agent-optimized instructions. Load **references/best-practices.md** for:

- Template structure
- Best practices for agent execution
- Writing style guidelines
- Quality checklist

Key principles:

- Use imperative/infinitive form (verb-first instructions)
- Be explicit and specific
- Include expected outcomes
- Provide concrete examples
- Define clear error handling

### Step 5: Create the Command File

1. Determine full file path:
   - Project: `.claude/commands/[command-name].md`
   - Global: `~/.claude/commands/[command-name].md`

2. Ensure directory exists:

   ```bash
   mkdir -p [directory-path]
   ```

3. Write the command file using the Write tool

4. Confirm with user:
   - Report the file location
   - Summarize what the command does
   - Explain how to use it: `/command-name [arguments]`

### Step 6: Test and Iterate (Optional)

If the user wants to test:

1. Suggest testing: `You can test this command by running: /command-name [arguments]`
2. Be ready to iterate based on feedback
3. Update the file with improvements as needed

## Command Locations

| Scope    | Path                    | Shown as           |
|----------|-------------------------|-------------------|
| Project  | `.claude/commands/`     | (project)         |
| Personal | `~/.claude/commands/`   | (user)            |

## YAML Frontmatter Options

| Field                     | Purpose                                | Required |
|---------------------------|----------------------------------------|----------|
| `description`             | Brief description for /help            | Yes      |
| `allowed-tools`           | Tools the command can use              | No       |
| `argument-hint`           | Expected arguments hint                | No       |
| `model`                   | Specific model to use                  | No       |
| `disable-model-invocation`| Prevent SlashCommand tool invocation   | No       |

## Common Patterns

### Arguments

**All arguments** - `$ARGUMENTS`:
```markdown
Fix issue #$ARGUMENTS following our coding standards
# /fix-issue 123 → "Fix issue #123 following..."
```

**Positional** - `$1`, `$2`, etc.:
```markdown
Review PR #$1 with priority $2
# /review 456 high → "Review PR #456 with priority high"
```

### Bash Execution

Slash commands can execute shell commands before running. This requires the allowed-tools frontmatter field.

### File References

Include file contents with `@` prefix:

```markdown
Review the implementation in @src/utils/helpers.js

Compare @src/old-version.js with @src/new-version.js
```

## Validation

Run the validator to check command structure:

```sh
uv run .claude/skills/meta-command-creator/scripts/validate-command.py .claude/commands/my-command.md
```

### Checklist

- [ ] File location: `.claude/commands/<name>.md`
- [ ] YAML frontmatter has `description`
- [ ] Steps are numbered and actionable
- [ ] $ARGUMENTS handled correctly (if used)
- [ ] `allowed-tools` included if using `!` bash execution
- [ ] All code blocks have language specifiers
- [ ] Guardrails section for state-changing commands
- [ ] Output format specified

## Summary

When creating a command:

1. **Detect location** (project vs global)
2. **Show patterns** to frame the conversation
3. **Gather information** (name, purpose, arguments, steps, tools)
4. **Generate optimized command** with agent-executable instructions
5. **Create file** at appropriate location
6. **Confirm and iterate** as needed

Focus on creating commands that agents can execute autonomously, with clear steps, explicit tool usage, and proper error handling.