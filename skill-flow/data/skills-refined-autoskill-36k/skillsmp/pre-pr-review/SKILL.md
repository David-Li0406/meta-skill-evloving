---
name: pre-pr-review
description: Use when the user asks for a local CodeRabbit review before creating a pull request. Delegates to the specialized local-coderabbit-reviewer sub-agent to run the scan, analyze results, present a plan for fixes, apply changes, run tests, and commit only if all tests pass.
allowed-tools: ["Task"]
---

# Pre-PR Review Skill

This skill provides automated local CodeRabbit reviews before creating pull requests, with systematic fix application and safety validation.

## When This Skill Activates

Use this skill when you detect the user wants a local CodeRabbit review. Common trigger phrases:

- "Run local coderabbit scan"
- "Do a local coderabbit review"
- "Local CodeRabbit review"
- "CodeRabbit scan before PR"
- "Review my code locally"
- "Run coderabbit locally"

**Key indicators**:
1. Mentions "coderabbit" or "code rabbit"
2. Mentions "local", "locally", or "before PR"
3. Does NOT include a PR number (that would trigger coderabbit-workflow skill)

## What This Skill Does

When activated, immediately delegate to the `local-coderabbit-reviewer` sub-agent by using the Task tool:

```
Use the Task tool with:
- subagent_type: "local-coderabbit-reviewer"
- description: "Run local CodeRabbit review"
- prompt: "Run a local CodeRabbit review against main branch. Scan all changes (committed + uncommitted), analyze results, present a plan for fixes, apply changes, run tests, and commit only if all tests pass."
```

## Why Delegate to Sub-agent?

The `local-coderabbit-reviewer` sub-agent is specialized for this workflow and will:
1. Run CodeRabbit CLI scan (`--plain --base main --config CLAUDE.md`)
2. Save results to `.coderabbit/review.txt`
3. Read and analyze all findings
4. **Present a plan** for implementing fixes (even if not in plan mode)
5. Apply fixes systematically
6. Run full test suite
7. **Only commit if tests pass** ✅
8. **Stop if tests fail** (no commit) ❌

## User Experience

**Before this skill:**
```
User: "Run local coderabbit scan"
Claude: [Manually runs command, asks what to do with results, may skip steps]
```

**With this skill:**
```
User: "Run local coderabbit scan"
Skill: [Auto-activates]
Sub-agent: [Scans → Analyzes → Plans → Fixes → Tests → Commits]
Result: ✅ Done automatically with plan presentation and safety checks
```

## Safety Features

The local-coderabbit-reviewer sub-agent includes critical safety checks:
- **Never commits failing tests** - Stops and reports if any test fails
- **Always presents plan** - Shows what will be fixed before making changes
- **Respects project patterns** - Follows BCL conventions and standards
- **Comprehensive scan** - Reviews all changes (committed + uncommitted)

## Differences from coderabbit-workflow

| Feature | coderabbit-workflow | pre-pr-review |
|---------|---------------------|---------------|
| **Trigger** | "Fix CodeRabbit on PR #123" | "Run local coderabbit scan" |
| **Input source** | GitHub PR comments | Local CLI scan |
| **Timestamp filtering** | Yes (only new comments) | No (full scan) |
| **Plan presentation** | No | Yes (always) |
| **GitHub comment** | Yes | No |
| **Push to remote** | Yes | No (local only) |

## Supporting Files

This skill directory includes:
- `SKILL.md` (this file) - Skill definition and activation logic
- `README.md` - Detailed workflow documentation and examples

## Configuration

No configuration required. The skill uses:
- CodeRabbit CLI: `coderabbit` (must be installed and authenticated)
- Sub-agent: `local-coderabbit-reviewer` (must exist in ~/.claude/agents/)
- Output directory: `.coderabbit/` (created if doesn't exist)
- Base branch: `main` (configurable in sub-agent if needed)

## Troubleshooting

### If the skill doesn't activate:
1. Check that the user's message includes "coderabbit" + "local" keywords
2. Ensure there's no PR number (that triggers coderabbit-workflow instead)
3. Verify the local-coderabbit-reviewer sub-agent exists
4. Confirm CodeRabbit CLI is installed (`coderabbit --version`)

### If CodeRabbit CLI is not installed:
The sub-agent will detect this and provide installation instructions:
```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit auth login
```

### If tests fail:
- The sub-agent will NOT commit changes
- Review test failures and fix them manually, or ask the user for guidance
- Changes remain in working directory for manual review

## Example Interactions

### Success Case

```
User: "Run local coderabbit scan"

Agent:
1. Running CodeRabbit scan against main branch...
   → Saving results to .coderabbit/review.txt

2. Analyzing 12 findings...

3. PLAN: Here's what I'll fix:
   • src/Domain/User.cs:45 - Add null check for email parameter
   • src/Application/UserService.cs:78 - Extract magic number 100 to constant
   • tests/UserTests.cs:120 - Improve test assertion message
   [... 9 more items ...]

   Proceed with fixes? [User confirms or plan mode auto-proceeds]

4. Applying fixes systematically...
   ✓ Fixed 12 issues

5. Running test suite...
   → All tests passed ✅

6. Committing changes...
   → Committed: "Address CodeRabbit review feedback"

✅ Local CodeRabbit review complete! Ready to create PR.
```

### Failure Case (Tests Fail)

```
User: "Run local coderabbit scan"

Agent:
1. Running CodeRabbit scan...
   → Found 5 issues

2. Presenting plan...
   [Shows what will be fixed]

3. Applying fixes...
   ✓ Fixed 5 issues

4. Running test suite...
   ❌ 2 tests failed:

   UserServiceTests.CreateUser_WithInvalidEmail_ThrowsException
   UserServiceTests.UpdateUser_WhenNotFound_ReturnsError

🛑 Tests failed. Changes NOT committed.

Please review the failures. The fixes are in your working directory.
```

## Best Practices

1. **Run before every PR** - Catch issues early before GitHub review
2. **Review the plan** - Understand what will change before it happens
3. **Trust the safety checks** - If tests fail, there's a reason
4. **Keep .coderabbit/ local** - Already in .gitignore, no need to commit
5. **Use timestamped files** - For history: `.coderabbit/review-$(date).txt`
