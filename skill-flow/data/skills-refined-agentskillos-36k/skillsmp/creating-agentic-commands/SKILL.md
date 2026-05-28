---
name: creating-agentic-commands
description: Create custom slash commands for workflow automation in OpenCode. Use when creating commands, automating workflows, or when user mentions slash commands, custom commands, /command patterns, or workflow automation.
---

# Create Agentic Commands

Create custom slash commands for workflow automation in OpenCode. Commands are prompt shortcuts that execute predefined prompts with arguments, shell output injection, and file references.

## When to Use Commands

Commands are **prompt shortcuts** that:

- Execute predefined prompts with optional arguments
- Inject shell output or file contents into prompts
- Specify which agent and model to use
- Run as isolated subtasks when needed
- Can be invoked in TUI (`/command`) or headless mode (`claude -p`)

### Commands vs Agents vs Skills

| Concept     | Purpose                  | Invocation           | Persistence             |
| ----------- | ------------------------ | -------------------- | ----------------------- |
| **Command** | Execute a workflow       | `/command-name`      | Immediate execution     |
| **Agent**   | Specialized AI assistant | `@agent-name` or Tab | Session-scoped behavior |
| **Skill**   | On-demand instructions   | Auto-loaded by agent | Loaded when needed      |

**Decision tree:**

```
Need automation?
├─ Prompt shortcut with shell/files? → Command
├─ Specialized AI behavior? → Agent (see creating-agentic-subagents skill)
├─ Reusable instructions for agent? → Skill (see creating-agentic-skills skill)
└─ Multi-step orchestrated workflow? → Command with subtask: true
```

## File Structure

**Project-specific (recommended):**

```
.opencode/command/{name}.md
```

**Global (all projects):**

```
~/.config/opencode/command/{name}.md
```

**Claude-compatible paths also work:**

```
.claude/commands/{name}.md
~/.claude/commands/{name}.md
```

**Naming conventions:**

- Lowercase with hyphens: `test.md`, `fix-style.md`, `test-coverage.md`
- Use action verbs: `test`, `build`, `analyze`, `create-component`
- File name becomes command: `test.md` → `/test`

## Configuration Formats

Commands can be defined in Markdown or JSON.

### Markdown Format (Recommended)

```markdown
---
description: Brief description shown in TUI
agent: build
subtask: true
---

Your prompt template goes here.
Can use $ARGUMENTS for user input.
Can use !`shell command` for dynamic content.
Can use @filename for file references.
```

### JSON Format

In `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "test": {
      "template": "Run tests with coverage.\n\n!`composer test`\n\nAnalyze results and suggest fixes.",
      "description": "Run tests with coverage report",
      "agent": "build"
    }
  }
}
```

## Configuration Options

| Option        | Required  | Description                                                 |
| ------------- | --------- | ----------------------------------------------------------- |
| `description` | Yes       | Brief description shown in TUI autocomplete                 |
| `template`    | JSON only | The prompt template (markdown uses body)                    |
| `agent`       | No        | Which agent executes: `build`, `plan`, or custom agent name |
| `subtask`     | No        | Set `true` to run as isolated subagent (separate context)   |
| `model`       | No        | Override model (omit unless user explicitly requests)       |

## Template Syntax

### Arguments

**All arguments as single string:**

```markdown
Create a React component named $ARGUMENTS with TypeScript support.
```

Usage: `/component Button` → `$ARGUMENTS` becomes `Button`

**Positional arguments:**

```markdown
Create a file named $1 in directory $2 with content: $3
```

Usage: `/create-file config.json src "{ \"key\": \"value\" }"`

### Shell Output Injection

Inject shell command output with `` !`command` ``:

```markdown
Here are the current test results:

!`npm test -- --coverage`

Based on these results, suggest improvements.
```

Commands run in project root. Output becomes part of the prompt.

### File References

Include file contents with `@filename`:

```markdown
Review the component in @src/components/Button.tsx.
Check for performance issues.
```

The file content gets included in the prompt automatically.

## Writing Effective Command Prompts

Follow these proven patterns from Claude's agentic coding research:

### 1. Be Specific and Direct

Vague prompts produce vague results. Be explicit about what you want.

```markdown
# Poor

Run tests

# Better

Run the full test suite with coverage using `composer test`.
After tests complete:

1. If all tests pass and coverage >= 90%, report success
2. If tests fail, identify each failure with file:line and suggest fixes
3. If coverage < 90%, identify untested code paths
```

### 2. Use Structured Steps

Number steps. Use headers. Provide clear boundaries.

```markdown
Execute the quality workflow in order:

**Step 1: Format Code**
!`./vendor/bin/pint`
Wait for completion before proceeding.

**Step 2: Static Analysis**
!`./vendor/bin/phpstan analyse`
If errors found, fix them and re-run until clean.

**Step 3: Tests**
!`composer test`
All tests must pass before reporting success.
```

### 3. Handle All Outcomes

Commands should handle success, failure, and edge cases:

```markdown
!`git diff --cached`

Analyze staged changes:

- If no changes staged: Inform user and suggest `git add`
- If changes exist: Create a descriptive commit message
- If sensitive files detected (.env, credentials): WARN and do not commit
```

### 4. Include Verification Steps

Commands should verify their own success:

```markdown
After creating the component:

1. Verify the file exists at the expected path
2. Run TypeScript compilation to check for errors
3. If errors, fix them before reporting success
```

### 5. Enable Iteration Loops

For complex tasks, build in iteration:

```markdown
!`./vendor/bin/phpstan analyse`

If errors found:

1. Fix the first error
2. Re-run PHPStan
3. Repeat until all errors resolved
4. Report total errors fixed
```

### 6. Use Extended Thinking for Complex Tasks

For planning or complex analysis, prompt deeper reasoning:

```markdown
Think carefully about the architecture before implementing.

Analyze the current authentication system:
!`find app -name "*.php" -path "*Auth*" | head -20`

Create a detailed migration plan considering:

- Backward compatibility
- Database changes required
- Testing strategy
- Rollback procedures
```

## Command Patterns

### Pattern 1: Simple Automation

Basic shell command with analysis:

```markdown
---
description: Run all tests with coverage report
agent: build
---

Run the test suite with coverage:

!`composer test -- --coverage`

Analyze results:

- All pass + coverage >= 90%: Report success
- Tests fail: Identify failures, suggest fixes
- Coverage < 90%: Identify untested code
```

### Pattern 2: Code Generation

Create files following project patterns:

```markdown
---
description: Create a new Action class following domain patterns
agent: build
---

Create an Action class for: $ARGUMENTS

Follow existing patterns in the codebase:

1. Check app/Actions/ for naming conventions
2. Use `declare(strict_types=1);` and `final` class
3. Accept DTO parameter, return typed result
4. Single public `execute()` method

After creation:

- Show the complete file
- Suggest corresponding DTO if needed
- Provide Controller usage example
```

### Pattern 3: Multi-Step Workflow with Subtask

Isolated execution for complex workflows:

```markdown
---
description: Run all quality checks and fix issues
agent: build
subtask: true
---

Execute complete quality workflow:

**Step 1: Rector**
!`./vendor/bin/rector`
Fix issues found, then re-run until clean.

**Step 2: Pint**
!`./vendor/bin/pint`

**Step 3: PHPStan**
!`./vendor/bin/phpstan analyse`
Fix each error, re-run until clean.

**Step 4: Tests**
!`composer test -- --coverage`

**Final Report:**

- All checks passing
- Coverage: X%
- Errors fixed: N
```

### Pattern 4: Code Review (Using Subagent)

Delegate to specialized agent:

```markdown
---
description: Comprehensive code review of recent changes
agent: code-reviewer
subtask: true
---

Review changes from the last commit:

!`git diff HEAD~1`

Analyze for:

- Code quality and best practices
- Security vulnerabilities
- Performance concerns
- Test coverage gaps

Provide actionable feedback without making changes.
```

### Pattern 5: Iterative Fix Loop

Fix issues until clean:

```markdown
---
description: Fix all ESLint errors iteratively
agent: build
---

Run ESLint and fix all errors:

!`npm run lint`

If errors found:

1. Fix each error in order
2. Re-run lint after each fix
3. Continue until no errors remain
4. Report: "Fixed N errors in M files"

If no errors: Report "No ESLint errors found"
```

### Pattern 6: Headless/CI Compatible

Commands used in automation:

```markdown
---
description: Check code quality (CI-safe, no prompts)
agent: build
---

Run quality checks and report results:

!`composer run checks 2>&1`

Output format (for CI parsing):

- Line 1: PASS or FAIL
- Line 2+: Details of any failures

Do not ask questions. Do not make changes.
Report results only.
```

## Subtask Behavior

When `subtask: true`:

- Creates **isolated session** (separate context from main conversation)
- Uses specified agent's configuration
- Doesn't pollute main context with intermediate steps
- Navigate between sessions with `Leader+Left/Right`
- Forces agent to act as subagent even if `mode: primary`

Use subtasks for:

- Long-running operations
- Operations that generate lots of intermediate output
- Workflows you want to inspect separately
- Parallel operations (multiple subtasks can run)

## Built-in Commands

OpenCode includes these built-in commands:

| Command    | Description                                         |
| ---------- | --------------------------------------------------- |
| `/init`    | Initialize OpenCode for project (creates AGENTS.md) |
| `/undo`    | Undo last changes                                   |
| `/redo`    | Redo undone changes                                 |
| `/share`   | Share conversation                                  |
| `/help`    | Show help                                           |
| `/resume`  | Resume previous session                             |
| `/connect` | Configure providers                                 |

Custom commands with the same name override built-in commands.

## Anti-Patterns

### Avoid These

**Vague description:**

```yaml
description: Run tests # Does not explain what happens after
```

**No argument handling:**

```markdown
Create a component # No way to specify which component
```

**No error handling:**

```markdown
!`npm test`
Done! # Ignores test failures
```

**Unnecessarily specifying model:**

```yaml
model: anthropic/claude-sonnet-4-20250514 # Not needed unless requested
```

**Ambiguous paths:**

```markdown
Create file in components folder # Which components folder?
```

### Do This Instead

**Clear description:**

```yaml
description: Run all tests with coverage and suggest fixes for failures
```

**Proper argument handling:**

```markdown
Create a React component named $ARGUMENTS at resources/js/components/$ARGUMENTS.tsx
```

**Explicit error handling:**

```markdown
!`npm test`

If tests pass: Confirm success with coverage percentage
If tests fail: List each failure with file:line and suggest fixes
```

**Specific paths:**

```markdown
Create file at resources/js/components/$ARGUMENTS.tsx
```

## Quality Checklist

Before finalizing a command:

- [ ] Clear, action-oriented `description` field
- [ ] Template/body specifies expected inputs clearly
- [ ] Arguments handled with `$ARGUMENTS` or `$1`, `$2`, etc.
- [ ] Shell commands use `` !`command` `` syntax correctly
- [ ] File references use `@filename` syntax when needed
- [ ] All outcomes handled (success, failure, edge cases)
- [ ] Verification steps included where appropriate
- [ ] `subtask: true` set if isolation needed
- [ ] Agent selected appropriately (or omitted for default)
- [ ] Model field only included if user explicitly requested
- [ ] Tested in both TUI and headless mode if for CI

## Integrating with AGENTS.md

Commands work best when they complement your project's AGENTS.md rules:

```markdown
# AGENTS.md

## Custom Commands

This project uses custom commands in `.opencode/command/`:

- `/test` - Run tests with coverage analysis
- `/quality` - Complete quality check workflow
- `/fresh` - Reset database with seeders

When these commands exist, prefer using them over ad-hoc instructions.
```

## References

- `references/examples.md` - Complete production-ready command examples
- `references/agent-basics.md` - Quick agent reference for commands
- See `creating-agentic-subagents` skill for comprehensive agent patterns
- See `creating-agentic-skills` skill for on-demand instruction patterns
