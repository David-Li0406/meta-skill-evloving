# Common Workflows - Claude Code Documentation

Source: https://code.claude.com/docs/en/common-workflows

This page provides comprehensive guidance on common workflows with Claude Code. Here are the main sections:

## Understand New Codebases

### Get a Quick Codebase Overview
```bash
cd /path/to/project
claude
> give me an overview of this codebase
> explain the main architecture patterns used here
> what are the key data models?
> how is authentication handled?
```

**Tips:**
- Start with broad questions, then narrow down to specific areas
- Ask about coding conventions and patterns used in the project
- Request a glossary of project-specific terms

### Find Relevant Code
```bash
> find the files that handle user authentication
> how do these authentication files work together?
> trace the login process from front-end to database
```

## Fix Bugs Efficiently

```bash
> I'm seeing an error when I run npm test
> suggest a few ways to fix the @ts-ignore in user.ts
> update user.ts to add the null check you suggested
```

**Tips:**
- Tell Claude the command to reproduce the issue and get a stack trace
- Mention any steps to reproduce the error
- Let Claude know if the error is intermittent or consistent

## Refactor Code

```bash
> find deprecated API usage in our codebase
> suggest how to refactor utils.js to use modern JavaScript features
> refactor utils.js to use ES2024 features while maintaining the same behavior
> run tests for the refactored code
```

## Use Specialized Subagents

```bash
> /agents  # View available subagents
> review my recent code changes for security issues
> use the code-reviewer subagent to check the auth module
> have the debugger subagent investigate why users can't log in
```

**Creating custom subagents:**
```bash
> /agents
```
Then select "Create New subagent" and define:
- A unique identifier (e.g., `code-reviewer`, `api-designer`)
- When Claude should use this agent
- Which tools it can access
- A system prompt describing the agent's role

## Use Plan Mode for Safe Code Analysis

Plan Mode instructs Claude to create a plan by analyzing the codebase with read-only operations before making changes.

### When to use Plan Mode
- **Multi-step implementation**: When your feature requires edits to many files
- **Code exploration**: When you want to research the codebase thoroughly before changing anything
- **Interactive development**: When you want to iterate on the direction with Claude

### How to use Plan Mode

**Turn on Plan Mode during a session:**
- Press **Shift+Tab** to cycle through permission modes
- **Shift+Tab** twice: Normal Mode → Auto-Accept Mode → Plan Mode (`⏸ plan mode on`)

**Start a new session in Plan Mode:**
```bash
claude --permission-mode plan
```

**Run headless queries in Plan Mode:**
```bash
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### Example: Planning a Complex Refactor

```bash
claude --permission-mode plan
> I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.

> What about backward compatibility?
> How should we handle database migration?
```

### Configure Plan Mode as Default

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

## Let Claude Interview You

For large features, let Claude gather requirements through questions:

```bash
> Interview me about this feature before you start: user notification system
> Help me think through the requirements for authentication by asking questions
> Ask me clarifying questions to build out this spec: payment processing
```

Claude uses the `AskUserQuestion` tool to ask multiple-choice questions for gathering requirements and clarifying ambiguity before writing any code.

## Work with Tests

```bash
> find functions in NotificationsService.swift that are not covered by tests
> add tests for the notification service
> add test cases for edge conditions in the notification service
> run the new tests and fix any failures
```

Claude generates tests matching your project's existing patterns and conventions.

## Create Pull Requests

```bash
> summarize the changes I've made to the authentication module
> create a pr
> enhance the PR description with more context about the security improvements
> add information about how these changes were tested
```

## Handle Documentation

```bash
> find functions without proper JSDoc comments in the auth module
> add JSDoc comments to the undocumented functions in auth.js
> improve the generated documentation with more context and examples
> check if the documentation follows our project standards
```

## Work with Images

You can include images in conversations by:
1. Dragging and dropping into the Claude Code window
2. Copying and pasting with **Ctrl+V** (not Cmd+V)
3. Providing an image path

```bash
> What does this image show?
> Describe the UI elements in this screenshot
> Are there any problematic elements in this diagram?
> Here's a screenshot of the error. What's causing it?
> Generate CSS to match this design mockup
```

## Reference Files and Directories

Use `@` to quickly include files or directories:

```bash
> Explain the logic in @src/utils/auth.js
> What's the structure of @src/components?
> Show me the data from @github:repos/owner/repo/issues
```

## Use Extended Thinking (Thinking Mode)

Extended thinking is enabled by default, reserving up to 31,999 tokens for Claude to reason through complex problems step-by-step.

### Configure Thinking Mode

| Scope | How to Configure | Details |
|-------|-----------------|---------|
| **Toggle shortcut** | Press `Option+T` (macOS) or `Alt+T` (Windows/Linux) | Toggle for current session |
| **Global default** | Use `/config` | Sets default across all projects |
| **Limit token budget** | Set `MAX_THINKING_TOKENS` environment variable | Example: `export MAX_THINKING_TOKENS=10000` |

**View thinking process:**
Press `Ctrl+O` to toggle verbose mode and see internal reasoning as gray italic text.

### How Extended Thinking Token Budgets Work

- When **enabled**: Claude can use up to **31,999 tokens** from your output budget for thinking
- When **disabled**: Claude uses **0 tokens** for thinking
- You're charged for all thinking tokens used

## Resume Previous Conversations

```bash
claude --continue                    # Continue most recent conversation
claude --resume                      # Open conversation picker
claude --resume auth-refactor        # Resume by name
```

### Name Your Sessions

```bash
> /rename auth-refactor              # During a session
> /resume auth-refactor              # Resume by name later
```

### Use the Session Picker

```bash
/resume
```

**Keyboard shortcuts in picker:**

| Shortcut | Action |
|----------|--------|
| `↑` / `↓` | Navigate between sessions |
| `→` / `←` | Expand or collapse grouped sessions |
| `Enter` | Select and resume session |
| `P` | Preview session content |
| `R` | Rename session |
| `/` | Search to filter sessions |
| `A` | Toggle all projects view |
| `B` | Filter to current git branch |
| `Esc` | Exit picker |

## Run Parallel Claude Code Sessions with Git Worktrees

```bash
# Create a new worktree with a new branch
git worktree add ../project-feature-a -b feature-a

# Or create a worktree with an existing branch
git worktree add ../project-bugfix bugfix-123

# Navigate to your worktree
cd ../project-feature-a
claude

# List all worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../project-feature-a
```

## Use Claude as a Unix-style Utility

### Add Claude to Your Verification Process

```json
// package.json
{
  "scripts": {
    "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
  }
}
```

### Pipe In, Pipe Out

```bash
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

### Control Output Format

```bash
# Text format (default)
cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt

# JSON format
cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json

# Streaming JSON format
cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
```

## Create Custom Slash Commands

### Create Project-Specific Commands

```bash
mkdir -p .claude/commands
echo "Analyze the performance of this code and suggest three specific optimizations:" > .claude/commands/optimize.md
```

Then in Claude Code:
```bash
> /optimize
```

### Add Command Arguments with $ARGUMENTS

```bash
echo 'Find and fix issue #$ARGUMENTS. Follow these steps: 1. Understand the issue described in the ticket 2. Locate the relevant code in our codebase 3. Implement a solution that addresses the root cause 4. Add appropriate tests 5. Prepare a concise PR description' > .claude/commands/fix-issue.md
```

Usage:
```bash
> /fix-issue 123
```

### Create Personal Slash Commands

```bash
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities, focusing on:" > ~/.claude/commands/security-review.md
```

Then use across all projects:
```bash
> /security-review
```

## Ask Claude About Its Capabilities

Claude has built-in access to its documentation:

```bash
> can Claude Code create pull requests?
> how does Claude Code handle permissions?
> what slash commands are available?
> how do I use MCP with Claude Code?
> how do I configure Claude Code for Amazon Bedrock?
> what are the limitations of Claude Code?
```
