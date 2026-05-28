---
name: lumen
description: Use the lumen CLI for git diffs, AI-generated commit messages, change explanations, and git command generation. Triggers on diff viewing, commit drafting, code review, explaining git changes, or generating git commands.
---

# When to Use This Skill

**Proactively use this skill when:**
- User wants to view git diffs (staged, unstaged, commits, branches, PRs)
- User wants to generate a commit message for staged changes
- User wants to understand what changed in a commit or branch
- User wants to generate a git command from natural language
- User mentions code review or reviewing changes
- User wants to compare branches or commits

# Overview

`lumen` is a CLI tool providing:
- **Beautiful diff viewer** - Interactive TUI with syntax highlighting
- **AI commit messages** - Generate conventional commits from staged changes
- **Change explanations** - AI-powered explanations of diffs
- **Git command generation** - Natural language to git commands

# CLI Reference

## Visual Diff Viewer

```bash
lumen diff                              # View uncommitted changes
lumen diff HEAD~1                       # View specific commit
lumen diff main..feature/A              # Compare branches
lumen diff --pr 123                     # View GitHub PR
lumen diff https://github.com/owner/repo/pull/123
lumen diff --file src/main.rs           # Filter to specific files
lumen diff --watch                      # Auto-refresh on changes
lumen diff main..feature --stacked      # Review commits one-by-one
lumen diff --theme dracula              # Use specific theme
```

**Keybindings:**
- `j/k` or arrows: Navigate
- `{/}`: Jump between hunks
- `tab`: Toggle sidebar
- `space`: Mark file as viewed (syncs with GitHub on PRs)
- `e`: Open file in editor
- `i`: Add/edit annotation on hunk
- `I`: View all annotations
- `ctrl+h/l`: Previous/next commit (stacked mode)
- `?`: Show all keybindings

**Themes:** `dark`, `light`, `catppuccin-mocha`, `catppuccin-latte`, `dracula`, `nord`, `one-dark`, `gruvbox-dark`, `gruvbox-light`, `solarized-dark`, `solarized-light`

## Generate Commit Messages

```bash
lumen draft                             # Generate commit message for staged changes
lumen draft --context "match brand guidelines"  # Add context for better messages
lumen draft | xclip -selection c        # Copy to clipboard (Linux)
lumen draft | git commit -F -           # Commit directly with generated message
```

**Output format:** Conventional commit style (e.g., `feat(button.tsx): Update button color to blue`)

## Generate Git Commands

```bash
lumen operate "squash the last 3 commits into 1 with the message 'squashed commit'"
```

- Displays explanation of what the command does
- Shows warnings for dangerous operations
- Prompts for confirmation before execution

## Explain Changes

```bash
lumen explain                           # All uncommitted changes
lumen explain --staged                  # Only staged changes
lumen explain HEAD                      # Latest commit
lumen explain abc123f                   # Specific commit
lumen explain HEAD~3..HEAD              # Last 3 commits
lumen explain main..feature/A           # Branch comparison
lumen explain main...feature/A          # Branch comparison (merge base)
lumen explain --query "What's the performance impact?"  # Ask specific questions
lumen explain --list                    # Interactive commit selection (requires fzf)
```

## Configuration

```bash
lumen configure                         # Interactive AI provider setup
```

**Config locations (priority order):**
1. CLI flags (highest)
2. `--config <path>`
3. Project root `lumen.config.json`
4. `~/.config/lumen/lumen.config.json` (lowest)

**Example config:**
```json
{
  "provider": "claude",
  "model": "claude-sonnet-4-5-20250930",
  "theme": "catppuccin-mocha"
}
```

**AI Providers:** `openai`, `claude`, `gemini`, `groq`, `deepseek`, `xai`, `ollama`, `openrouter`, `vercel`

**Environment variables:**
- `LUMEN_AI_PROVIDER` - Provider name
- `LUMEN_API_KEY` - API key
- `LUMEN_AI_MODEL` - Model name
- `LUMEN_THEME` - Diff viewer theme

# Instructions for Claude

1. **For diff viewing** - Run `lumen diff` with appropriate arguments. This opens an interactive TUI the user navigates themselves.

2. **For commit messages** - Run `lumen draft` and show the output. User can pipe to clipboard or commit directly.

3. **For explanations** - Run `lumen explain` with the target (commit, range, etc.) and optional query.

4. **For git commands** - Run `lumen operate "description"` - this is interactive and prompts for confirmation.

5. **The diff viewer is standalone** - Works without AI configuration.

6. **AI features require setup** - If AI commands fail, suggest running `lumen configure`.

# Workflow Examples

## Quick commit with AI message

```bash
# Stage changes first
git add -p  # or specific files

# Generate and commit
lumen draft | git commit -F -
```

## Review a PR

```bash
lumen diff --pr 123
# Or with URL
lumen diff https://github.com/owner/repo/pull/123
```

## Understand recent changes

```bash
lumen explain HEAD~5..HEAD --query "What are the main changes and why?"
```

## Generate complex git command

```bash
lumen operate "undo my last commit but keep the changes"
# Output: git reset --soft HEAD~1 [y/N]
```

## Code review workflow

```bash
# View diff with annotations
lumen diff main..feature-branch

# In the TUI:
# - Navigate with j/k
# - Press 'i' to add comments on hunks
# - Press 'I' to view/export all annotations
# - Press 'space' to mark files as viewed
```

## Stacked review (commit by commit)

```bash
lumen diff main..feature --stacked
# Use ctrl+h/l to navigate between commits
```

# Error Handling

**AI features fail:**
```
Error: No API key configured
```
Solution: Run `lumen configure` to set up AI provider

**Diff viewer not showing:**
Check that you're in a git repository and have changes to show

**PR diff not working:**
Ensure `gh` CLI is authenticated (`gh auth login`)
