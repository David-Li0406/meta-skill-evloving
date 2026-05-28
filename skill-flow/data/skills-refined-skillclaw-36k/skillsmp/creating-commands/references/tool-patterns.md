---
title: Tool Usage Patterns for Slash Commands
description: Concrete patterns for using Claude Code tools within slash commands. Covers Skill tool invocation, Task tool for subagents, TodoWrite for tracking, file operations, search tools, and tool combinations.
keywords: tool patterns, Skill tool, Task tool, TodoWrite, subagents, file operations, Read, Write, Edit, Grep, Glob, tool combinations
file-type: reference
skill: creating-commands
---

# Tool Usage Patterns for Slash Commands

This reference provides concrete patterns for using Claude Code tools within slash command workflows.

## Skill Tool - Invoking Skills

Use the Skill tool to explicitly invoke other skills within your command workflow.

### Basic Skill Invocation

```markdown
## Your Task

1. Invoke the creating-hooks skill to get guidance:
   ```
   Skill(command="creating-hooks")
   ```

2. Follow the skill's instructions to create the hook
```

### Multiple Skill Invocations

```markdown
## Your Task

1. First, use the creating-skills skill for structure:
   ```
   Skill(command="creating-skills")
   ```

2. Then use crafting-agentic-prompts for prompt optimization:
   ```
   Skill(command="crafting-agentic-prompts")
   ```

3. Apply insights from both skills to create the artifact
```

### Skill Invocation with Context

```markdown
## Your Task

Before creating the commit, invoke the committing-atomically skill:

```
Skill(command="committing-atomically")
```

The skill will handle:
- Analyzing staged changes
- Generating conventional commit message
- Creating the atomic commit
```

### When to Use Skill Tool

**Use explicit Skill() invocation when:**
- You need guaranteed execution of a skill's full workflow
- The skill has complex logic that should run autonomously
- You want the skill to handle a complete sub-task
- The skill provides specialized capabilities (e.g., committing, prompting)

**Use skill name reference instead when:**
- You just need to follow the skill's patterns/guidance
- You're adapting the skill's approach to your specific case
- You want Claude to decide whether to invoke or just reference

## Task Tool - Delegating to Subagents

Use the Task tool to delegate complex sub-tasks to specialized subagents.

### Basic Subagent Delegation

```markdown
## Your Task

1. Use the Task tool to launch an Explore subagent:
   ```
   Task(
     subagent_type="Explore",
     description="Find authentication patterns",
     prompt="Search the codebase for all authentication implementations.
             Use thoroughness level: medium.
             Find all files implementing user authentication and session management."
   )
   ```

2. Analyze the subagent's findings and proceed with implementation
```

### General-Purpose Subagent

```markdown
## Your Task

1. Delegate refactoring to a general-purpose subagent:
   ```
   Task(
     subagent_type="general-purpose",
     description="Refactor authentication module",
     prompt="Refactor the authentication module to use the new session API.
             Update all files that import from auth/legacy.
             Ensure all tests still pass.
             Return a summary of all changes made."
   )
   ```
```

### Explore Subagent with Thoroughness Levels

```markdown
## Your Task

### Quick exploration (fast, high-level)
```
Task(
  subagent_type="Explore",
  description="Quick codebase overview",
  prompt="Thoroughness: quick
          Find the main entry points for the API.
          Identify the core modules and their purposes."
)
```

### Medium exploration (balanced)
```
Task(
  subagent_type="Explore",
  description="Find error patterns",
  prompt="Thoroughness: medium
          Search for all error handling patterns.
          Check for consistent error handling across modules."
)
```

### Thorough exploration (comprehensive)
```
Task(
  subagent_type="Explore",
  description="Complete dependency analysis",
  prompt="Thoroughness: very thorough
          Map all dependencies for the authentication module.
          Find every import, every function call, every reference.
          Check for circular dependencies."
)
```
```

### Sequential Subagent Tasks

```markdown
## Your Task

1. **Phase 1 - Discovery**: Launch Explore subagent
   ```
   Task(
     subagent_type="Explore",
     description="Find all API endpoints",
     prompt="Thoroughness: medium. Find all files defining API endpoints."
   )
   ```

2. **Phase 2 - Analysis**: Wait for results, then launch another subagent
   ```
   Task(
     subagent_type="general-purpose",
     description="Analyze endpoint security",
     prompt="Review the endpoints found in Phase 1.
             Check each for authentication and authorization.
             Report any security issues."
   )
   ```

3. **Phase 3 - Implementation**: Apply findings from both subagents
```

### Parallel Subagent Execution

When multiple independent tasks can run simultaneously:

```markdown
## Your Task

Launch these subagents in parallel (use multiple Task calls in one message):

1. **Subagent A** - Find components:
   ```
   Task(
     subagent_type="Explore",
     description="Find React components",
     prompt="Thoroughness: quick. Find all React component files."
   )
   ```

2. **Subagent B** - Find tests:
   ```
   Task(
     subagent_type="Explore",
     description="Find test files",
     prompt="Thoroughness: quick. Find all test files."
   )
   ```

3. **Subagent C** - Find docs:
   ```
   Task(
     subagent_type="Explore",
     description="Find documentation",
     prompt="Thoroughness: quick. Find all markdown documentation."
   )
   ```

After all complete, synthesize the results.
```

### Subagent Best Practices

**Clear prompts:**
- Specify thoroughness level for Explore subagents
- Define exactly what the subagent should return
- Provide context about what you'll do with the results

**Appropriate thoroughness:**
- `quick` - High-level overview, fast results (use for discovery)
- `medium` - Balanced depth and speed (use for most tasks)
- `very thorough` - Comprehensive analysis (use for critical tasks)

**Tool requirements:**
- Subagents require `Task` in allowed-tools
- Consider what tools the subagent might need

## TodoWrite Tool - Task Tracking

Use TodoWrite to track progress through multi-step command workflows.

### Basic Task List

```markdown
## Your Task

1. Create task list using TodoWrite:
   ```
   TodoWrite(todos=[
     {content: "Analyze codebase structure", status: "in_progress", activeForm: "Analyzing codebase structure"},
     {content: "Generate documentation", status: "pending", activeForm: "Generating documentation"},
     {content: "Create examples", status: "pending", activeForm: "Creating examples"},
     {content: "Write to file", status: "pending", activeForm: "Writing to file"}
   ])
   ```

2. Work through each task, updating status as you go
```

### Progressive Task Updates

```markdown
## Your Task

1. Create initial task list (all pending except first)

2. **Before starting each task**: Mark as in_progress
   ```
   TodoWrite(todos=[
     {content: "Previous task", status: "completed", activeForm: "..."},
     {content: "Current task", status: "in_progress", activeForm: "Working on current task"},
     {content: "Next task", status: "pending", activeForm: "..."}
   ])
   ```

3. **After completing each task**: Mark as completed, move to next
   ```
   TodoWrite(todos=[
     {content: "Previous task", status: "completed", activeForm: "..."},
     {content: "Current task", status: "completed", activeForm: "Worked on current task"},
     {content: "Next task", status: "in_progress", activeForm: "Working on next task"}
   ])
   ```
```

### Dynamic Task Discovery

```markdown
## Your Task

1. Start with high-level tasks:
   ```
   TodoWrite(todos=[
     {content: "Explore codebase", status: "in_progress", activeForm: "Exploring codebase"},
     {content: "Fix issues found", status: "pending", activeForm: "Fixing issues"}
   ])
   ```

2. After exploration, expand the task list with specific issues:
   ```
   TodoWrite(todos=[
     {content: "Explore codebase", status: "completed", activeForm: "Explored codebase"},
     {content: "Fix missing error handling in auth.ts", status: "in_progress", activeForm: "Fixing error handling"},
     {content: "Fix unused import in utils.ts", status: "pending", activeForm: "Fixing unused import"},
     {content: "Fix type error in api.ts", status: "pending", activeForm: "Fixing type error"}
   ])
   ```

3. Complete each specific task
```

### Task List Best Practices

**Content field:**
- Use imperative form: "Run tests", "Fix errors"
- Be specific: "Fix TypeScript error in auth.ts:42" not "Fix errors"

**ActiveForm field:**
- Use present continuous: "Running tests", "Fixing errors"
- Matches the status: if in_progress, activeForm describes current action

**Status management:**
- Only ONE task should be "in_progress" at a time
- Mark tasks "completed" immediately after finishing
- Keep task list updated throughout execution

## SlashCommand Tool - Invoking Other Commands

Use the SlashCommand tool to invoke other slash commands from within a command.

### Basic Command Invocation

```markdown
## Your Task

1. First run the review command:
   ```
   SlashCommand(command="/review src/")
   ```

2. Wait for review to complete

3. If review passes, run the test command:
   ```
   SlashCommand(command="/test")
   ```

4. If tests pass, proceed with commit
```

### Command Composition

```markdown
## Your Task

This meta-command orchestrates multiple specialized commands:

1. `/review` - Check code quality
   ```
   SlashCommand(command="/review")
   ```

2. `/test` - Verify functionality
   ```
   SlashCommand(command="/test")
   ```

3. `/commit` - Create atomic commit
   ```
   SlashCommand(command="/commit")
   ```

4. `/pr` - Create pull request
   ```
   SlashCommand(command="/pr")
   ```

Each step must succeed before proceeding.
```

### Conditional Command Execution

```markdown
## Your Task

1. Check if changes are substantial:
   - If >50 files or >500 lines: Run `/review` first
   - If smaller: Skip review, proceed to commit

2. Based on review outcome:
   - If issues found: Report to user, stop
   - If clean: Proceed with `/commit`
```

## File Operation Tools

### Read Tool

```markdown
## Your Task

1. Read the configuration file:
   ```
   Read(file_path="/absolute/path/to/config.json")
   ```

2. Analyze the configuration and determine next steps
```

### Write Tool

```markdown
## Your Task

1. Create the new component file:
   ```
   Write(
     file_path="/absolute/path/to/component.tsx",
     content="[generated component code]"
   )
   ```

2. Verify the file was created:
   - Check with: `ls -lh /absolute/path/to/component.tsx`
```

### Edit Tool

```markdown
## Your Task

1. Update the imports in the file:
   ```
   Edit(
     file_path="/absolute/path/to/file.ts",
     old_string="import { old } from 'old-module'",
     new_string="import { new } from 'new-module'"
   )
   ```

2. Verify the edit was successful
```

### File Tool Best Practices

**Paths:**
- Always use absolute paths, not relative
- Use `$ARGUMENTS` for user-provided paths, but resolve to absolute

**Read before Write/Edit:**
- Always Read files before Writing (for existing files)
- Always Read files before Editing
- Tools will error if you skip this step

**Verification:**
- After Write: Verify with `ls -lh path` or `cat path`
- After Edit: Verify changes with Read or `git diff`

## Search Tools

### Grep Tool

```markdown
## Your Task

1. Search for all TODO comments:
   ```
   Grep(
     pattern="TODO:",
     path="./src",
     output_mode="content",
     -n=true
   )
   ```

2. For each TODO found, create a task
```

### Glob Tool

```markdown
## Your Task

1. Find all test files:
   ```
   Glob(pattern="**/*.test.ts")
   ```

2. Read each test file and analyze coverage
```

### Search Best Practices

**Grep:**
- Use `output_mode="content"` to see matching lines
- Use `output_mode="files_with_matches"` for just file paths
- Use `-n=true` to include line numbers
- Use `-i=true` for case-insensitive search

**Glob:**
- Use `**/*.ext` for recursive search
- Use `*.ext` for current directory only
- Returns files sorted by modification time

## Bash Tool Patterns

For preflight checks and context gathering, see:
- `references/preflight-patterns.md` - Validation patterns
- `references/context-patterns.md` - Information gathering patterns

### Quick Reference

**Preflight checks (validation):**
```markdown
## Preflight Checks

- Git repo exists: !`git rev-parse --git-dir 2>/dev/null && echo "yes" || echo "no"`
- Files exist: !`test -f path && echo "exists" || echo "missing"`
```

**Context gathering (information):**
```markdown
## Context

- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
```

## Tool Combination Patterns

### Skill + Subagent

```markdown
## Your Task

1. Invoke the creating-commands skill for guidance:
   ```
   Skill(command="creating-commands")
   ```

2. Use Explore subagent to find similar commands:
   ```
   Task(
     subagent_type="Explore",
     description="Find similar command patterns",
     prompt="Thoroughness: medium.
             Search for commands with similar structure to what we're building."
   )
   ```

3. Draft the command using insights from both
```

### TodoWrite + Subagent

```markdown
## Your Task

1. Create task list:
   ```
   TodoWrite(todos=[
     {content: "Explore codebase", status: "in_progress", activeForm: "Exploring codebase"},
     {content: "Implement changes", status: "pending", activeForm: "Implementing changes"},
     {content: "Test changes", status: "pending", activeForm: "Testing changes"}
   ])
   ```

2. Launch Explore subagent for first task:
   ```
   Task(
     subagent_type="Explore",
     description="Explore authentication patterns",
     prompt="..."
   )
   ```

3. Mark exploration complete and move to implementation:
   ```
   TodoWrite(todos=[
     {content: "Explore codebase", status: "completed", activeForm: "Explored codebase"},
     {content: "Implement changes", status: "in_progress", activeForm: "Implementing changes"},
     ...
   ])
   ```
```

### Read + Edit + Bash Verification

```markdown
## Your Task

1. Read the current file:
   ```
   Read(file_path="/path/to/file.ts")
   ```

2. Make the necessary changes:
   ```
   Edit(
     file_path="/path/to/file.ts",
     old_string="...",
     new_string="..."
   )
   ```

3. Verify with git diff:
   - Run: `git diff /path/to/file.ts`
   - Confirm changes are correct

4. Run tests to verify nothing broke:
   - Run: `npm test /path/to/file.test.ts`
```

## Summary

**Tool selection guide:**

- **Skill tool**: Need to execute another skill's full workflow
- **Task tool**: Need to delegate complex sub-tasks to subagents
- **TodoWrite**: Multi-step workflow requiring progress tracking
- **SlashCommand**: Need to invoke other slash commands
- **Read/Write/Edit**: File operations (always use absolute paths)
- **Grep/Glob**: Search operations (prefer over bash grep/find)
- **Bash**: Preflight checks, context gathering, verification

**Best practices:**
- Use explicit tool invocations for clarity
- Combine tools for powerful workflows
- Always track progress with TodoWrite for complex commands
- Verify operations after file changes
- Use appropriate subagent thoroughness levels
