# Claude Code: Best Practices Guide

Source: https://www.anthropic.com/engineering/claude-code-best-practices

## Overview
This comprehensive guide outlines effective patterns for using Claude Code, an agentic coding tool developed by Anthropic. As noted in the article, "Claude Code is intentionally low-level and unopinionated, providing close to raw model access without forcing specific workflows."

## 1. Customize Your Setup

### Create CLAUDE.md Files
Special files that Claude automatically integrates into context when starting conversations. Ideal content includes:
- Common bash commands with descriptions
- Core files and utility functions
- Code style guidelines
- Testing instructions
- Repository conventions (branching, merge strategies)
- Developer environment setup requirements
- Project-specific warnings or unexpected behaviors

The guide recommends keeping these files "concise and human-readable" and suggests checking them into version control to share across teams.

### Placement Options
- Root directory (checked in for team sharing, or `.local.md` for personal use)
- Parent directories (useful for monorepos)
- Child directories (Claude pulls in on demand)
- Home folder (`~/.claude/CLAUDE.md`) for all sessions

### Tuning CLAUDE.md Files
Files should be refined iteratively like production prompts. The document notes that teams at Anthropic sometimes "run CLAUDE.md files through the prompt improver" and use emphasis techniques like "IMPORTANT" or "YOU MUST" to improve model adherence.

### Tool Allowlists
Manage which actions Claude can perform by:
- Selecting "Always allow" during sessions
- Using the `/permissions` command
- Manually editing `.claude/settings.json` or `~/.claude.json`
- Adding CLI flags like `--allowedTools` for session-specific permissions

### GitHub Integration
Installing the `gh` CLI enables Claude to manage issues, pull requests, and comments more effectively than API-only approaches.

## 2. Give Claude More Tools

### Bash Tools
Claude inherits your shell environment, accessing custom scripts and utilities. Recommend documenting tool usage with examples and directing Claude to use `--help` flags for documentation.

### MCP (Model Context Protocol)
Claude Code functions as both MCP client and server, supporting:
- Project-specific configurations
- Global configurations
- Checked-in `.mcp.json` files for team-wide availability

Use the `--mcp-debug` flag when troubleshooting configuration issues.

### Custom Slash Commands
Store prompt templates in `.claude/commands` folder as Markdown files. These become available through the slash menu and support the `$ARGUMENTS` keyword for parameterized workflows.

Example use case: Creating `/project:fix-github-issue 1234` commands for automated issue resolution.

## 3. Common Workflows

### Explore, Plan, Code, Commit
1. Request Claude read relevant files without coding initially
2. Ask for a plan using thinking mode ("think" through "ultrathink" for progressively more computation)
3. Implement the solution with verification steps
4. Commit changes and update documentation

The guide emphasizes that "steps #1-#2 are crucial" for problems requiring deeper analysis.

### Test-Driven Development Workflow
1. Write tests based on expected input/output pairs
2. Verify tests fail (without implementation)
3. Commit tests
4. Implement code iteratively until all tests pass
5. Verify implementation doesn't overfit using subagents

### Visual Iteration Workflow
1. Provide screenshot capabilities (Puppeteer MCP, iOS simulator, or manual screenshots)
2. Share design mocks via paste or file paths
3. Iterate until Claude's output matches the reference

### Safe YOLO Mode
Use `--dangerously-skip-permissions` to bypass permission checks. Recommended practice: run in containers without internet access to minimize security risks from prompt injection or data exfiltration.

### Codebase Q&A
Use Claude for onboarding questions like:
- "How does logging work?"
- "What edge cases does this component handle?"
- "Why was this API designed this way?"

### Git Interactions
Claude effectively handles:
- Searching history to answer context questions
- Writing context-aware commit messages
- Complex operations (rebasing, conflict resolution, patch comparisons)

### GitHub Interactions
Claude can manage:
- Pull request creation with appropriate messages
- Code review comment implementation
- Build failure fixes
- Issue categorization and triage

### Jupyter Notebooks
Researchers can use Claude to read, write, and improve notebooks, with results including image interpretation for data exploration.

## 4. Optimize Your Workflow

### Specific Instructions
The guide contrasts poor instructions ("add tests for foo.py") with better ones ("write a new test case covering the edge case where the user is logged out, avoiding mocks").

### Visual References
Claude excels with:
- Screenshots (macOS: `cmd+ctrl+shift+4` to clipboard, then `ctrl+v` to paste)
- Drag-and-drop image uploads
- File path references
- Design mocks for UI development

### File References
Use tab-completion to quickly mention files or folders anywhere in your repository, helping Claude identify correct resources.

### URL Integration
Paste URLs alongside prompts for Claude to fetch and read. Use `/permissions` to allowlist domains and avoid repeated permission prompts.

### Course Correction Techniques
- Ask Claude to make plans before coding
- Press Escape to interrupt without losing context
- Double-tap Escape to edit previous prompts and explore alternatives
- Request Claude to undo changes

### Context Management
Use `/clear` between tasks to reset the context window and maintain focus on current objectives.

### Checklists for Complex Tasks
For migrations or bulk fixes, have Claude:
- Create a Markdown checklist of all tasks
- Work through items systematically
- Check off completed items

### Data Input Methods
- Copy and paste directly
- Pipe into Claude Code (e.g., `cat log.txt | claude`)
- Request Claude pull data via bash or tools
- Ask Claude to read files or fetch URLs

## 5. Headless Mode for Infrastructure

Use the `-p` flag with `--output-format stream-json` for non-interactive contexts like CI, pre-commit hooks, and build scripts.

### Use Cases
- **Issue triage**: Automatically label new GitHub issues
- **Linting**: Provide subjective code reviews beyond traditional linters, identifying typos, stale comments, and misleading names

## 6. Multi-Claude Workflows

### Parallel Verification
Have one Claude write code while another reviews or tests it, leveraging separate contexts for better results than single-instance approaches.

### Multiple Repository Checkouts
Create 3-4 separate git checkouts in different folders, opening each in separate terminal tabs for simultaneous parallel work.

### Git Worktrees
Lighter alternative to multiple checkouts: Use `git worktree add ../project-feature-a feature-a` to isolate multiple tasks without merge conflicts.

### Custom Harness with Headless Mode
Two patterns emerge:

**Fanning out**: Generate task lists, then loop through items calling Claude programmatically for each task (useful for large migrations or analyses).

**Pipelining**: Integrate Claude into data processing pipelines using `claude -p "<prompt>" --json | your_command`.

---

## Key Takeaways

The guide emphasizes that Claude Code's flexibility requires experimentation to develop effective personal workflows. Core principles include thorough planning before coding, providing clear iteration targets (tests, visuals, or specifications), and leveraging Claude's ability to integrate with existing development ecosystems through bash, MCP tools, and git workflows.
