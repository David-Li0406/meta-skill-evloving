# Pre-PR Review Skill Documentation

## Overview

The **pre-pr-review** skill automates local CodeRabbit code reviews before creating pull requests. It runs a comprehensive scan, analyzes findings, presents a plan for fixes, applies changes systematically, runs tests, and commits only if all tests pass.

## Purpose

This workflow helps you:
- **Catch issues early** - Before they appear in GitHub PR reviews
- **Save time** - Automated fix application with safety checks
- **Maintain quality** - All fixes are tested before committing
- **Stay informed** - Always see a plan before changes are made

## When to Use

Run a local CodeRabbit review when:
1. ✅ You've finished work on a feature branch
2. ✅ All your changes are ready (committed or uncommitted)
3. ✅ You're about to push and create a PR
4. ✅ You want to catch issues before GitHub review

## How It Works

### Activation

Simply ask Claude Code to run a local CodeRabbit scan:

```
"Run local coderabbit scan"
"Do a local coderabbit review"
"Review my code before PR"
```

### Workflow Steps

1. **Scan** - Runs `coderabbit review --plain --base main --config CLAUDE.md`
2. **Save** - Results go to `.coderabbit/review.txt`
3. **Analyze** - Reads and categorizes all findings
4. **Plan** - Presents what will be fixed (even if not in plan mode)
5. **Fix** - Applies changes systematically
6. **Test** - Runs full test suite (`dotnet test`)
7. **Commit** - Only if all tests pass ✅
8. **Report** - Shows summary of what was done

### Safety Guarantees

🛡️ **Never commits failing tests**
- If any test fails, changes remain uncommitted
- You get a clear report of failures
- You can review and fix manually

🛡️ **Always shows a plan**
- You see what will be fixed before it happens
- Transparency in all changes
- Builds trust in the automation

🛡️ **Respects project patterns**
- Follows CLAUDE.md conventions
- Maintains existing code style
- Preserves architectural patterns

## Example Interactions

### Example 1: Clean Success

```
You: "Run local coderabbit scan"

Claude:
🔍 Running CodeRabbit scan against main branch...
   → Analyzing all changes (committed + uncommitted)
   → Saving results to .coderabbit/review.txt

📋 Found 8 issues:

PLAN:
1. src/Domain/User.cs:45
   • Add null check for email parameter
   • Severity: ⚠️ Warning

2. src/Application/UserService.cs:78
   • Extract magic number 100 to constant MaxUsersPerPage
   • Severity: 💡 Suggestion

3. tests/UserTests.cs:120
   • Improve assertion message: "User should be created with valid data"
   • Severity: 💡 Suggestion

[... 5 more items ...]

Proceeding with fixes...

✅ Applied 8 fixes

🧪 Running test suite...
   → dotnet test --no-build --verbosity normal
   → All 47 tests passed ✅

💾 Committing changes...
   → git add [modified files]
   → git commit -m "Address CodeRabbit review feedback

   - Added null checks for email parameters
   - Extracted magic numbers to constants
   - Improved test assertion messages
   - Fixed documentation typos
   - Removed unused usings

   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>"

✅ Local CodeRabbit review complete!
   → Ready to push and create PR
```

### Example 2: Tests Fail (Safety Stop)

```
You: "Run local coderabbit scan"

Claude:
🔍 Running CodeRabbit scan...
   → Found 3 issues

PLAN:
1. src/Domain/User.cs:67
   • Change email validation regex
2. src/Application/UserValidator.cs:34
   • Update validation rules for email
3. tests/UserTests.cs:88
   • Fix test data format

Applying fixes...

✅ Applied 3 fixes

🧪 Running test suite...
   → dotnet test --no-build --verbosity normal

❌ 2 tests failed:

   UserValidatorTests.ValidateEmail_WithPlusSign_ReturnsValid
   Expected: True
   Actual: False

   UserServiceTests.CreateUser_WithValidEmail_Succeeds
   Expected: Success
   Actual: ValidationError

🛑 Tests failed. Changes NOT committed.

The fixes are in your working directory for review.
Would you like me to analyze the test failures?
```

### Example 3: No Issues Found

```
You: "Run local coderabbit scan"

Claude:
🔍 Running CodeRabbit scan against main branch...
   → Analyzing all changes

✅ No issues found!

Your code looks great. Ready to create PR.
```

## Configuration

### CodeRabbit CLI

The skill uses these CodeRabbit CLI settings:

```bash
coderabbit review \
  --plain \              # Non-interactive output
  --base main \          # Compare against main branch
  --config CLAUDE.md     # Include project context
```

### Output Location

Reviews are saved to `.coderabbit/review.txt` in your project root:

```
your-project/
├── .coderabbit/
│   └── review.txt          # Latest scan results
├── .gitignore              # Already excludes .coderabbit/
└── CLAUDE.md               # Project context for scan
```

### Base Branch

Default: `main`

If your project uses a different base branch (e.g., `develop`), you can modify the sub-agent prompt or ask Claude to use a different base.

## Comparison with Other Workflows

### vs. coderabbit-workflow (GitHub PR reviews)

| Feature | pre-pr-review | coderabbit-workflow |
|---------|---------------|---------------------|
| **When** | Before PR creation | After PR created |
| **Input** | Local CLI scan | GitHub PR comments |
| **Scope** | All changes vs main | Only new comments |
| **Output** | Local commit | Push + GitHub comment |
| **Plan** | Always shown | Not shown |

**Use pre-pr-review**: Before creating PR
**Use coderabbit-workflow**: After PR review feedback

### vs. Manual CodeRabbit CLI

| Feature | Manual CLI | pre-pr-review |
|---------|-----------|---------------|
| **Automation** | Manual | Fully automated |
| **Fix application** | Manual | Automatic |
| **Testing** | Manual | Automatic |
| **Commit** | Manual | Automatic (if tests pass) |
| **Plan** | N/A | Always shown |

**Use manual CLI**: For quick spot checks
**Use pre-pr-review**: For comprehensive pre-PR workflow

## Installation Requirements

### CodeRabbit CLI

```bash
# Install
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Authenticate
coderabbit auth login
```

### Verify Installation

```bash
coderabbit --version
# Should output version number
```

### Project Setup

Ensure `.coderabbit/` is in `.gitignore`:

```bash
# Check
grep -q "\.coderabbit/" .gitignore && echo "✅ Already excluded" || echo "❌ Add to .gitignore"

# Add if needed
echo ".coderabbit/" >> .gitignore
```

## Troubleshooting

### Skill Doesn't Activate

**Symptom**: Claude doesn't recognize your request for local review

**Solutions**:
1. Use trigger phrases: "run local coderabbit scan"
2. Avoid mentioning PR numbers (triggers different skill)
3. Include "local" or "locally" in your request

### CodeRabbit CLI Not Found

**Symptom**: Error: `coderabbit: command not found`

**Solution**:
```bash
# Install
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Verify
coderabbit --version

# If still not found, check PATH
echo $PATH | grep -q ".local/bin" || echo "Add ~/.local/bin to PATH"
```

### Tests Keep Failing

**Symptom**: Fixes applied but tests always fail

**Solutions**:
1. Review the specific test failures
2. Ask Claude: "Analyze why these tests are failing"
3. Fix tests manually or ask for guidance
4. Run tests before scan to ensure baseline is green

### Scan Takes Too Long

**Symptom**: CodeRabbit scan is slow or hangs

**Solutions**:
1. Ensure you're on a feature branch (not main)
2. Check your internet connection (CLI may need to download)
3. Try running manually to diagnose: `coderabbit review --plain --base main`

## Best Practices

### 1. Run Before Every PR

Make this part of your workflow:
```
git add .
git commit -m "Implement feature X"
[run local coderabbit scan]  ← Add this step
git push
gh pr create
```

### 2. Keep Baseline Green

Always ensure tests pass before running the scan:
```bash
dotnet test --no-build --verbosity normal
```

This way, if tests fail after fixes, you know the fixes caused the issue.

### 3. Review the Plan

Even though it's automated, always read the plan:
- Understand what will change
- Catch any potential issues
- Learn from CodeRabbit's suggestions

### 4. Trust the Safety Checks

If tests fail and the commit is blocked:
- This is protecting you from breaking changes
- Review the failures carefully
- Fix issues before re-running

### 5. Use Timestamped Reviews (Optional)

For historical tracking:
```bash
coderabbit review --plain --base main > .coderabbit/review-$(date +%Y%m%d-%H%M%S).txt 2>&1
```

The skill uses `review.txt` by default, but you can save timestamped versions manually.

## Tips & Tricks

### Quick Scan Without Auto-Fix

If you just want to see issues without applying fixes:
```
"Show me what coderabbit would find locally"
```

Claude will run the scan and show results without applying fixes.

### Selective Fix Application

If you want to fix only some issues:
```
"Run local coderabbit scan, but let me review before fixing"
```

Claude will present the plan and wait for your approval.

### Different Base Branch

If you need to compare against a different branch:
```
"Run local coderabbit scan against develop branch"
```

### Scan Specific Files

For targeted reviews:
```
"Run coderabbit on src/Domain/ files only"
```

## Integration with Other Workflows

### Pre-PR Checklist

```
1. ✅ Implement feature
2. ✅ Write tests
3. ✅ Run tests locally
4. ✅ Run local coderabbit scan ← This skill
5. ✅ Push to GitHub
6. ✅ Create PR
7. ✅ Address PR feedback (coderabbit-workflow skill)
8. ✅ Merge PR
9. ✅ Clean up branch (post-merge-cleanup skill)
```

### Combined with Manual Review

```
1. Run local coderabbit scan
2. Review results
3. Apply additional manual fixes
4. Run scan again to verify
5. Push and create PR
```

## Support

For issues or questions:
1. Check this README first
2. Review the SKILL.md file for activation logic
3. Review the sub-agent file (`~/.claude/agents/local-coderabbit-reviewer.md`)
4. Ask Claude: "Help me debug the pre-pr-review skill"

## Contributing

To improve this skill:
1. Update SKILL.md for activation logic changes
2. Update README.md (this file) for documentation changes
3. Update the sub-agent for workflow changes
4. Test thoroughly before committing
5. Document any new edge cases
