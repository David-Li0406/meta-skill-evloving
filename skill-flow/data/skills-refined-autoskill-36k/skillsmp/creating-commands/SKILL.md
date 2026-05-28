---
name: creating-commands
description: Guide for creating effective custom slash commands. This skill should be used when users want to create a new slash command (or update an existing slash command) that provides quick, repeatable workflows with preflight checks, skill integration, and subagent delegation.
---

# Creating Effective Slash Commands

This skill provides comprehensive guidance for designing and implementing custom slash commands that are minimal, explicit, and leverage Claude Code's full capabilities including preflight checks, skill integration, and subagent delegation.

## When to Create a Slash Command vs Skill

**Use slash commands for:**
- Quick, frequently-used prompts requiring explicit invocation
- Simple workflows that fit in one file
- Repeatable tasks with clear, manual triggers
- Commands with direct control over execution timing

**Use skills for:**
- Complex capabilities requiring multiple files or scripts
- Automatic discovery based on context
- Comprehensive workflows with extensive validation
- Knowledge organized across multiple reference files

**Rule of thumb:** If it's getting complex (>200 lines or needs multiple resource files), it should be a skill instead.

## Command Creation Process

To create a command, follow the "Command Creation Process" in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Command with Concrete Examples

Skip this step only when the command's usage patterns are already clearly understood.

To create an effective command, clearly understand concrete examples of how the command will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building a command for atomic commits:

- "What commit workflow problems are you solving? Inconsistent messages, missing verification, unclear scope?"
- "Can you give examples of typical commit scenarios? Feature completion, bug fixes, refactoring?"
- "What validation should happen before committing? Git status, uncommitted changes, branch checks?"
- "When should this command trigger? User says '/commit', '/quick-commit [message]'?"
- "What commit format standards should be enforced? Conventional commits, co-authorship, message structure?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the command should support.

### Step 2: Planning the Command Structure

To turn concrete examples into an effective command, analyze each example by:

1. Considering what validations (preflight checks) are needed before execution
2. Identifying what context (git state, files, project info) is required
3. Determining which skills or subagents should be leveraged
4. Establishing success criteria for verification

Example: When building a `/quick-commit` command for "create atomic commit with message," the analysis shows:

1. **Preflight checks needed:** Git repository validation, uncommitted changes check, not on detached HEAD
2. **Context required:** Git status output, recent commit messages for format consistency
3. **Skills to leverage:** None needed for simple workflow
4. **Success criteria:** Commit created, message follows format, working directory clean

Example: When building a `/review-pr` command for "review pull request for quality," the analysis shows:

1. **Preflight checks needed:** GitHub CLI installed, valid PR number provided, PR exists
2. **Context required:** PR diff, PR description, related files changed
3. **Skills to leverage:** Code review patterns, security checks
4. **Success criteria:** Review posted with actionable feedback, summary provided to user

To establish the command structure, analyze each concrete example to identify:
- Required frontmatter fields (`allowed-tools`, `argument-hint`, `description`, `model`)
- Preflight validation checks
- Context gathering needs
- Task execution steps
- Success verification criteria

### Step 3: Draft the Command File

Commands are single markdown files with four required sections. Create the command file following this structure:

**File location:**
- Project commands: `.claude/commands/command-name.md`
- Personal commands: `~/.claude/commands/command-name.md`

**Command structure template:**

```markdown
---
allowed-tools: Bash(cmd1:*), Bash(cmd2:*), Read, Edit
argument-hint: <required> [optional]
description: Brief description under 10 words
model: sonnet
---

## Preflight Checks

- Check description: !`bash command`
- Another check: !`bash command`

## Context

- Context description: !`bash command`
- File context: @path/to/file.ext
- Skills to reference: @skill-name

## Task Instructions

Explicitly describe what Claude should do:

1. First step (use specific skill if applicable)
2. Second step (delegate to subagent if needed)
3. Final step with verification

## Success Criteria

- What should be true when complete
- How to verify the command succeeded
```

**Writing guidelines:**

- **Frontmatter:** Use restrictive `allowed-tools` (never bare `Bash`), concise `description` (~10 words), appropriate `model` (sonnet default, haiku for simple tasks)
- **Preflight Checks:** Use `!` prefix for bash commands, validate all prerequisites before execution
- **Context:** Gather git/project/file context with `!` commands and `@` references
- **Task Instructions:** Write in imperative form, specify exact steps, reference skills/subagents by name
- **Success Criteria:** Define measurable outcomes, provide verification commands

**Prompt Engineering for Task Instructions:** Command task instructions are prompts that Claude will execute. Invoke `Skill(command='crafting-agentic-prompts')` for guidance on writing effective agentic prompts including:

- Directive language and positive framing
- Tool usage optimization patterns
- Verbosity control and output formatting
- Long-horizon reasoning structures
- Proactive behavior triggers

This skill provides proven patterns for creating prompts that drive effective agent behavior.

For detailed patterns and examples, see reference files:
- `references/preflight-patterns.md` - Validation check patterns
- `references/context-patterns.md` - Context gathering patterns
- `references/tool-patterns.md` - Skill/Task/TodoWrite patterns
- `references/examples.md` - 8 production-ready command examples
- `references/advanced-patterns.md` - Complex scenarios (args, recovery, performance)

### Step 4: Validate and Iterate

Use the validation script with `--minimal` flag for rapid iteration during development:

```bash
python3 scripts/validate_command.py /path/to/command.md --minimal
```

**Iterative workflow:**

1. Draft command structure (frontmatter + sections + instructions)
2. Run `--minimal` validation
3. Fix errors and warnings incrementally
4. Repeat steps 2-3 until passing
5. Run full validation (without `--minimal`) for final check

**Use `--minimal` mode early and often.** It provides:
- One-line score summary with key metrics
- Only failures and warnings (no verbose passing checks)
- Actionable fix recommendations
- Fast feedback loop for quick iteration

**Desired outcome:** 100% pass rate (17/17 checks) before proceeding to quality review.

### Step 5: Quality Review

**Mandatory gate** before deployment. Two options:

**Option A: Self-review**
Follow `references/command-quality-review.md`:
1. Run automated pre-flight: `python3 scripts/validate_command.py /path/to/command.md` (must achieve 100%)
2. Conduct manual review of 6 quality categories using detailed checklists
3. Apply recommendation logic (APPROVE/NEEDS_REVISION/CONSIDER_DIFFERENT_TYPE)

**Option B: Use reviewer subagent**
```bash
Task(subagent_type="artifact-quality-reviewer", prompt="Review command at /path/to/command.md")
```
The subagent runs automated checks first, then conducts manual review following the same framework.

**Quality review categories:**
1. Frontmatter & Tool Restrictions
2. Preflight Checks
3. Context Gathering
4. Task Instructions & Prompt Quality
5. Success Criteria
6. Command Metrics & Artifact Type

**Target:** All categories score ≥4/5 for approval.

See `references/command-quality-review.md` for complete manual review workflow, scoring rubrics, and quality standards.

### Step 6: Test the Command

**IMPORTANT:** Commands may have side effects. Test with extreme caution.

**Safety assessment:**
1. Review `allowed-tools` frontmatter
2. Check for destructive operations (git commit, file writes, API calls)
3. Identify potential risks

**Safe testing patterns:**
- Commands with `Read, Grep, Glob` only → Safe to test
- Commands with `Edit, Write` → Test in isolated directory
- Commands with `Bash(git:*)` → Test in isolated git repo
- Commands with external APIs → Do NOT test without user approval

**Testing workflow (when safe):**
1. Verify command structure loads correctly
2. Invoke command with test arguments
3. Observe preflight checks execute properly
4. Verify context gathering succeeds
5. Confirm task execution follows instructions
6. Validate success criteria are met

**When NOT to functionally test:**
- Destructive operations (delete, force push, production changes)
- External API calls
- Commands requiring specific environment state
- Uncertain about safety

→ Structure validation only in these cases

### Step 7: Deploy and Iterate

After passing quality review and testing, the command is ready for use.

**Deployment locations:**
- **Project commands:** `.claude/commands/` - Committed to git, shared with team
- **Personal commands:** `~/.claude/commands/` - Available across all projects

**Iteration workflow:**
1. Use the command on real tasks
2. Notice struggles or inefficiencies
3. Identify how frontmatter, checks, or instructions should be updated
4. Implement changes with validation (`--minimal` mode)
5. Re-run quality review if significant changes
6. Test and deploy updated version

## Core Principles for Command Design

1. **Be Explicit**: Specify exactly what Claude should do, step by step
2. **Use Preflight Checks**: Validate context before execution with bash commands (using `!` prefix)
3. **Leverage Skills**: Reference specific skills by name when appropriate
4. **Delegate to Subagents**: Specify which subagents to use for complex sub-tasks
5. **Keep It Minimal**: Single-file, focused on one clear workflow (<200 lines)
6. **Restrict Tools**: Use `allowed-tools` to limit command capabilities for safety

## Essential Frontmatter Fields

### allowed-tools

Specify exactly which tools the command can use. **Be restrictive for safety.**

Patterns:
- `Bash(git add:*)` - Specific git command with any arguments
- `Bash(git add:*), Bash(git commit:*)` - Multiple specific commands
- `Read, Grep, Glob` - Read-only file operations
- `Read, Edit` - Can read and edit, but not create files
- `Read, Write, Edit, TodoWrite` - Full file manipulation plus task tracking
- `Task` - Can launch subagents

**Important:** Do NOT use `Bash` alone - always specify which bash commands are allowed.

### argument-hint

Show users what arguments are expected. This appears during autocomplete.

Patterns:
- `[file]` - Single optional argument
- `<pr-number>` - Single required argument (use angle brackets)
- `[message]` - Optional text argument
- `add [tag] | remove [tag] | list` - Multiple command modes
- `<from> <to>` - Multiple required arguments

### description

Keep it **under 10 words**. This appears in `/help` output.

Good examples:
- "Create atomic commit with conventional format"
- "Review code for security and performance"
- "Scaffold new feature with tests and docs"

### model

Use specific models for specific tasks:
- `sonnet` - Default, best for most tasks
- `haiku` - Fast, for simple/cheap tasks

### disable-model-invocation

Set to `true` to prevent the `SlashCommand` tool from invoking this command automatically:
- `disable-model-invocation: true` - User must invoke manually
- Only set this when specifically asked to

## Common Mistakes

❌ **Too vague** - "Do the thing with $ARGUMENTS"
✅ **Explicit** - Use specific skills/subagents with numbered steps

❌ **No preflight checks** - Commands fail at runtime
✅ **Validated** - Check git repo, file existence, dependencies first

❌ **Overly permissive** - `allowed-tools: Bash`
✅ **Restrictive** - `Bash(git add:*), Bash(git commit:*), Read, Edit`

## References

- `references/preflight-patterns.md` - Validation checks (file existence, git, dependencies)
- `references/context-patterns.md` - Information gathering (git, project, code)
- `references/tool-patterns.md` - Skill/Task/TodoWrite/file operations
- `references/examples.md` - 8 production-ready examples
- `references/advanced-patterns.md` - Complex scenarios (args, recovery, performance)
- `references/command-quality-review.md` - Comprehensive quality review framework

## Summary

Effective slash commands are:
- **Minimal**: Single-file, focused on one task (<200 lines)
- **Explicit**: Clear instructions with specific workflows
- **Validated**: Preflight checks before execution, quality review before deployment
- **Integrated**: Reference skills and subagents by name
- **Restricted**: Limited tool access for safety
- **Tested**: Verified with real usage before sharing

**Remember:** If it's getting complex, it should probably be a skill instead!
