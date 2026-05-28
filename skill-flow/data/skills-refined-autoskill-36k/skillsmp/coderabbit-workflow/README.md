# CodeRabbit Workflow Skill

Automated handling of CodeRabbit review cycles for GitHub Pull Requests.

## Overview

This skill streamlines the repetitive process of addressing CodeRabbit feedback by:
1. Automatically fetching only NEW comments (since your last commit)
2. Applying fixes systematically
3. Running tests to ensure nothing breaks
4. Only pushing if all tests pass
5. Creating detailed GitHub comments to close the feedback loop

## Quick Start

Simply say:
```
"Address latest issues raised by coderabbit on pull request #123"
```

The skill auto-activates and handles everything.

## The Problem This Solves

### Before (Manual Process)

```
You: Create PR #123
CodeRabbit: Posts 10 review comments
You: Manually read each comment
You: Apply fixes one by one
You: Run tests (maybe)
You: Commit and push
You: Forget to comment on GitHub
CodeRabbit: Posts 5 more comments
You: Accidentally re-fix old issues already addressed
```

### After (With This Skill)

```
You: Create PR #123
CodeRabbit: Posts 10 review comments
You: "Address coderabbit issues on PR #123"
Skill: ✅ Fetches new comments, applies fixes, tests pass, pushes, comments
CodeRabbit: Posts 5 more comments
You: "Address coderabbit issues on PR #123"
Skill: ✅ Only processes the 5 NEW comments (skips already-fixed)
```

## How It Works

### Architecture

```
User Request
    ↓
[coderabbit-workflow Skill] ← Auto-activates
    ↓
[coderabbit-fixer Sub-agent] ← Specialized executor
    ↓
[get-coderabbit-comments-with-timestamps.sh] ← Filters by time
    ↓
GitHub API → Only comments after last commit
```

### Step-by-Step Flow

1. **Skill Activation**: Detects "coderabbit" + "PR #" + action verb
2. **Delegates to Sub-agent**: Invokes `coderabbit-fixer` with PR number
3. **Get Timestamp**: Sub-agent fetches last commit time from git
4. **Fetch Comments**: Runs script with `--since` parameter to filter
5. **Apply Fixes**: Systematically addresses each comment
6. **Run Tests**: Executes `dotnet test` (or project-specific command)
7. **Safety Check**:
   - ✅ Tests pass → Commit, push, comment on GitHub
   - ❌ Tests fail → STOP, report failures, do NOT push
8. **GitHub Comment**: Tags @coderabbitai with detailed change summary

## Components

### 1. Enhanced Script
**File**: `~/source/cli-tools/bin/get-coderabbit-comments-with-timestamps.sh`

**Purpose**: Fetch CodeRabbit comments with optional timestamp filtering

**Usage**:
```bash
# Fetch all comments
get-coderabbit-comments-with-timestamps.sh 123

# Fetch only comments after a specific time
get-coderabbit-comments-with-timestamps.sh 123 --since "2025-10-23T10:30:00Z"
```

### 2. Sub-agent
**File**: `~/.claude/agents/coderabbit-fixer.md`

**Purpose**: Specialized agent for the entire fix-test-push-comment workflow

**Capabilities**:
- Full tool access
- Git operations
- Test execution
- GitHub API via `gh` CLI
- File editing

### 3. Skill (This Directory)
**File**: `~/.claude/skills/coderabbit-workflow/SKILL.md`

**Purpose**: Auto-activation and delegation

**Trigger Phrases**:
- "Address coderabbit issues on PR #123"
- "Fix coderabbit comments on pull request 456"
- "Handle latest coderabbit feedback for PR #789"

## Example Workflow

### Scenario: Iterative Review Cycle

```bash
# Initial PR creation
git checkout -b feat/new-feature
# ... make changes ...
git commit -m "Add new feature"
git push -u origin feat/new-feature
gh pr create --title "New Feature" --body "Description"
```

**CodeRabbit reviews and posts 8 comments**

```
You: "Address latest issues raised by coderabbit on PR #72"

Skill Output:
1. Fetching last commit timestamp...
   → 2025-10-23T10:30:00-07:00

2. Fetching new CodeRabbit comments from PR #72...
   → Found 8 new comments

3. Analyzing and applying fixes:
   ✓ src/Domain/User.cs:45 - Added null check
   ✓ src/Application/UserService.cs:78 - Extracted magic number
   ✓ src/Infrastructure/UserRepository.cs:112 - Fixed async/await
   ✓ tests/UserTests.cs:120 - Improved test assertion
   ✓ (4 more fixes...)

4. Running test suite...
   → All 247 tests passed ✅

5. Committing and pushing changes...
   → Committed: "Address CodeRabbit feedback from PR #72"
   → Pushed to origin/feat/new-feature

6. Creating GitHub comment...
   → Posted summary tagging @coderabbitai

✅ All CodeRabbit feedback addressed and pushed successfully!
```

**CodeRabbit does another review, posts 3 more comments**

```
You: "Address latest issues raised by coderabbit on PR #72"

Skill Output:
1. Fetching last commit timestamp...
   → 2025-10-23T11:15:00-07:00 (just pushed)

2. Fetching new CodeRabbit comments from PR #72...
   → Found 3 new comments (old 8 filtered out ✓)

3. Analyzing and applying fixes:
   ✓ src/Application/UserService.cs:90 - Simplified LINQ
   ✓ README.md:42 - Fixed typo
   ✓ src/Domain/User.cs:67 - Added XML documentation

4. Running test suite...
   → All 247 tests passed ✅

5. Committing and pushing changes...
   → Committed: "Address CodeRabbit feedback from PR #72"
   → Pushed to origin/feat/new-feature

6. Creating GitHub comment...
   → Posted summary tagging @coderabbitai

✅ All CodeRabbit feedback addressed and pushed successfully!
```

**CodeRabbit is now happy, approves the PR! 🎉**

## Safety Features

### Critical: Never Push Failing Tests

The sub-agent will **STOP** if tests fail:

```
3. Analyzing and applying fixes:
   ✓ src/Domain/User.cs:45 - Added null check
   ✓ src/Application/UserService.cs:78 - Extracted magic number

4. Running test suite...
   ❌ 2 tests failed

⚠️  Applied fixes for CodeRabbit feedback, but tests are failing:

Failed tests:
  - UserTests.ShouldValidateEmail: Expected true but got false
  - UserServiceTests.ShouldCreateUser: NullReferenceException

Changes have NOT been committed or pushed. Please review the failures.
```

### Timestamp Filtering Prevents Re-work

By fetching only comments after the last commit, you avoid:
- Re-applying already-fixed issues
- Duplicate commits
- Confusion about what's been addressed
- Wasted time and API calls

### Detailed GitHub Comments

Every successful push creates a transparent comment:

```
@coderabbitai - Fixed issues from latest review:

• **src/Domain/User.cs:45**: Added null check before property access
• **src/Application/UserService.cs:78**: Extracted magic number 100 to constant MaxRetries
• **tests/UserTests.cs:120**: Improved test assertion message for clarity

All tests passing ✅
```

## Configuration Requirements

### Prerequisites

1. **GitHub CLI**: `gh` must be installed and authenticated
   ```bash
   gh auth status
   ```

2. **Script in PATH**: Enhanced script must be accessible
   ```bash
   which get-coderabbit-comments-with-timestamps.sh
   # Or exists at: ~/source/cli-tools/bin/get-coderabbit-comments-with-timestamps.sh
   ```

3. **Sub-agent**: Must exist at `~/.claude/agents/coderabbit-fixer.md`

4. **Git Repository**: Must be in a git repo with a PR

### Optional Configuration

None required! The skill works out of the box.

## Troubleshooting

### Skill Doesn't Activate

**Problem**: You say "fix coderabbit on PR 123" but nothing happens

**Solutions**:
- Include the word "coderabbit" explicitly
- Mention the PR number with # (e.g., "PR #123")
- Use action verbs like "address", "fix", "handle"

### Script Not Found

**Problem**: Error: `get-coderabbit-comments-with-timestamps.sh: command not found`

**Solutions**:
- Check PATH: `echo $PATH | grep cli-tools`
- Run with full path: The sub-agent tries `~/source/cli-tools/bin/` as fallback
- Make executable: `chmod +x ~/source/cli-tools/bin/get-coderabbit-comments-with-timestamps.sh`

### No Comments Found

**Problem**: "No new CodeRabbit comments found on PR #123"

**Possible Reasons**:
- CodeRabbit hasn't reviewed yet (check PR on GitHub)
- All comments are older than your last commit (already addressed!)
- Wrong PR number

### Tests Keep Failing

**Problem**: Fixes applied but tests fail, nothing gets pushed

**This is CORRECT behavior!** The skill protects you from breaking the build.

**What to do**:
1. Review the test failures reported by the sub-agent
2. Fix the tests manually or ask Claude Code for help
3. Once tests pass, try the workflow again

## Tips and Best Practices

### 1. Regular Review Cycles

Run the workflow after each CodeRabbit review:
```
CodeRabbit reviews → You: "Address coderabbit issues on PR #X" → Push → Repeat
```

### 2. Combine with Manual Review

For complex suggestions, review the changes before pushing:
```
You: "Address coderabbit issues on PR #X but show me changes before pushing"
```

### 3. Use with Other Workflows

This skill complements:
- `/review-pr` - Review your own PR before submitting
- `/commit` - Make commits during development
- Local CodeRabbit CLI reviews

### 4. Monitor GitHub Comments

Check the GitHub PR thread to see the detailed comments the skill posts. This creates an audit trail of what was fixed.

## Advanced Usage

### Custom Test Commands

If your project uses different test commands, you can temporarily modify the sub-agent or ask Claude Code:

```
You: "Address coderabbit issues on PR #123, but use 'npm test' instead of 'dotnet test'"
```

### Partial Fixes

If you want to fix only certain comments:

```
You: "Address coderabbit issues on PR #123, but only fix comments about null checks"
```

### Different Base Branch

If comparing against a branch other than `main`:

```
You: "Address coderabbit issues on PR #123, comparing against develop branch"
```

## File Locations

```
~/.claude/
├── agents/
│   └── coderabbit-fixer.md          # Sub-agent definition
└── skills/
    └── coderabbit-workflow/
        ├── SKILL.md                  # Skill activation logic
        └── README.md                 # This file

~/source/cli-tools/bin/
└── get-coderabbit-comments-with-timestamps.sh  # Script

~/.claude/CLAUDE.md                   # Global config (documents script)
```

## Contributing

To enhance this workflow:

1. **Script improvements**: Edit `~/source/cli-tools/bin/get-coderabbit-comments-with-timestamps.sh`
2. **Sub-agent logic**: Edit `~/.claude/agents/coderabbit-fixer.md`
3. **Activation triggers**: Edit `~/.claude/skills/coderabbit-workflow/SKILL.md`

All changes are local to your machine and take effect immediately.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the sub-agent logs in Claude Code
3. Test the script manually: `get-coderabbit-comments-with-timestamps.sh <PR_NUMBER>`
4. Verify GitHub CLI works: `gh pr view <PR_NUMBER>`

---

**Happy CodeRabbit-fixing! 🐰✨**
