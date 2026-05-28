---
name: coderabbit-workflow
description: Use when the user asks to address, fix, or handle CodeRabbit review feedback on GitHub Pull Requests. Delegates to the specialized coderabbit-fixer sub-agent to fetch new comments, apply fixes, run tests, and push only if tests pass.
allowed-tools: ["Task"]
---

# CodeRabbit Workflow Skill

This skill provides automated handling of CodeRabbit review cycles on GitHub Pull Requests.

## When This Skill Activates

Use this skill when you detect the user wants to address CodeRabbit feedback. Common trigger phrases:

- "Address issues raised by coderabbit on PR #123"
- "Fix coderabbit comments on pull request 456"
- "Handle latest coderabbit feedback for PR #789"
- "Apply coderabbit suggestions from PR #42"
- "Address latest coderabbit review on PR #123"

**Key indicators**:
1. Mentions "coderabbit" or "code rabbit"
2. References a PR/pull request number
3. Indicates action: address, fix, handle, apply, resolve

## What This Skill Does

When activated, immediately delegate to the `coderabbit-fixer` sub-agent by using the Task tool:

```
Use the Task tool with:
- subagent_type: "coderabbit-fixer"
- description: "Fix CodeRabbit feedback on PR #<NUMBER>"
- prompt: "Address CodeRabbit feedback on pull request #<NUMBER>. Fetch comments created after the last commit, apply fixes, run tests, and push only if all tests pass."
```

## Why Delegate to Sub-agent?

The `coderabbit-fixer` sub-agent is specialized for this workflow and will:
1. Extract the PR number
2. Get the last commit timestamp
3. Fetch only NEW CodeRabbit comments (since last commit)
4. Apply fixes systematically
5. Run full test suite
6. **Only push if tests pass** ✅
7. Create detailed GitHub comment tagging @coderabbitai

## User Experience

**Before this skill:**
```
User: "Address coderabbit issues on PR #123"
Claude: [Asks clarifying questions, manually runs commands, may forget steps]
```

**With this skill:**
```
User: "Address coderabbit issues on PR #123"
Skill: [Auto-activates]
Sub-agent: [Fetches comments, applies fixes, runs tests, pushes, comments]
Result: ✅ Done automatically with safety checks
```

## Safety Features

The coderabbit-fixer sub-agent includes critical safety checks:
- **Never pushes failing tests** - Stops and reports if any test fails
- **Filters out old comments** - Only processes feedback from latest review
- **Detailed GitHub comments** - Provides transparency on what was fixed
- **Respects project patterns** - Follows BCL conventions and standards

## Supporting Files

This skill directory includes:
- `SKILL.md` (this file) - Skill definition and activation logic
- `README.md` - Detailed workflow documentation
- `examples/` - Example interactions and use cases

## Configuration

No configuration required. The skill uses:
- Script: `get-coderabbit-comments-with-timestamps.sh` (must be in PATH or ~/source/cli-tools/bin/)
- Sub-agent: `coderabbit-fixer` (must exist in ~/.claude/agents/)
- GitHub CLI: `gh` (must be authenticated)

## Troubleshooting

If the skill doesn't activate:
1. Check that the user's message includes both "coderabbit" and a PR number
2. Ensure the coderabbit-fixer sub-agent exists
3. Verify the script is executable and in PATH

If tests fail:
- The sub-agent will NOT push changes
- Review test failures and fix them manually, or ask the user for guidance
