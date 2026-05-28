# Qodana Local Review Skill

Automated local Qodana static code analysis workflow for catching code quality issues before creating pull requests.

## Overview

This skill provides a complete workflow for running Qodana static analysis locally using the Qodana CLI in native mode (without Docker). It automatically scans your code, presents a plan for fixes, applies changes, validates with tests, and commits only if everything passes.

## When to Use

Use this skill when you want to:
- Run Qodana analysis locally before creating a PR
- Catch code quality issues early in development
- Fix code smells, potential bugs, and style violations
- Validate changes don't introduce new quality issues

## How It Works

### Trigger Phrases

Simply say any of these:
- "Run local qodana scan"
- "Do a local qodana review"
- "Qodana scan"
- "Run qodana locally"
- "Analyze code with qodana"

### Workflow Steps

1. **Setup**: Creates `.qodana/` directory for results
2. **Scan**: Runs Qodana CLI in native mode against your code
3. **Parse**: Extracts issues from SARIF output
4. **Categorize**: Groups by severity (error, warning, suggestion)
5. **Present Plan**: Shows what will be fixed (you see this before any changes)
6. **Apply Fixes**: Makes systematic changes to address issues
7. **Run Tests**: Validates changes with `dotnet test`
8. **Commit**: Only if all tests pass (safe by design)
9. **Report**: Provides comprehensive summary

## Example Interactions

### Basic Usage

```
You: Run local qodana scan

Claude: I'll run a local Qodana analysis. Let me delegate to the qodana reviewer...

[Qodana scan executes]

🔍 Qodana Local Review Results

Found 15 issues across 8 files:

PLAN: Here's what I'll fix:

Critical (2):
  1. src/Domain/User.cs:45
     Possible null reference exception
     Fix: Add null check before property access

  2. src/Application/UserService.cs:120
     Potential SQL injection vulnerability
     Fix: Use parameterized queries

Warnings (8):
  3. src/Infrastructure/Repository.cs:78
     Missing ConfigureAwait(false) on async call
     Fix: Add .ConfigureAwait(false)

  [... more items ...]

Suggestions (5):
  [... suggestions ...]

Total fixes to apply: 15

Proceeding with fixes...

[Applies each fix]

✓ Fixed 15 issues

Running tests...
🧪 Test Results: All 604 tests passed ✅

Committing changes...
✅ Qodana review complete!

Summary:
- Scanned: All project files
- Found: 15 issues (2 critical, 8 warnings, 5 suggestions)
- Fixed: 15 issues
- Tests: All 604 tests passed ✅
- Committed: "Address Qodana code quality issues"

Review saved to: .qodana/results/qodana.sarif.json
HTML report: .qodana/results/report/index.html
```

### When Tests Fail

```
You: Run local qodana scan

[Scan and fixes applied]

Running tests...
🧪 Test Results: 3 tests failed ❌

🛑 Tests failed. Changes NOT committed.

Failed tests:
  - UserServiceTests.GetUser_ShouldReturnUser: Expected true but was false
  - UserRepositoryTests.Save_ShouldPersist: NullReferenceException
  - AuthServiceTests.Login_ValidCredentials: Timeout

The fixes are in your working directory for review.
You can:
1. Review the changes: git diff
2. Manually adjust the fixes
3. Run tests again: dotnet test
4. Commit when ready: git add . && git commit
```

## Prerequisites

### Required Tools

1. **Qodana CLI**:
   ```bash
   # macOS
   brew install jetbrains/utils/qodana

   # Windows
   winget install -e --id JetBrains.QodanaCLI

   # Linux
   curl -fsSL https://jb.gg/qodana-cli/install | bash
   ```

2. **.NET SDK**: Required for native mode
   ```bash
   dotnet --version  # Should show 9.0 or later
   ```

3. **Git**: For committing fixes

### Configuration

Qodana uses configuration from:
- `qodana.yaml` (project root) - Project-specific settings
- `.qodana/` directory - Results and cache
- Project CLAUDE.md - Context for analysis

Example `qodana.yaml`:
```yaml
version: "1.0"
linter: jetbrains/qodana-dotnet
exclude:
  - name: All
    paths:
      - .qodana
      - bin
      - obj
      - .temp
```

## Features

### Safety-First Design

- **Test Validation**: Always runs tests before committing
- **No Forced Commits**: Stops if tests fail
- **Plan Presentation**: Shows changes before applying
- **Reversible**: Changes are in working directory (can be reset)

### Comprehensive Analysis

- **Multiple Severity Levels**: Critical, Warning, Suggestion, Info
- **Wide Coverage**: Code quality, bugs, vulnerabilities, style
- **SARIF Standard**: Industry-standard report format
- **Rich Reporting**: Console + SARIF + HTML reports

### Smart Workflow

- **Automatic Detection**: Skill activates on trigger phrases
- **Systematic Fixes**: Addresses issues one by one
- **Clear Communication**: Progress updates throughout
- **Detailed Reporting**: Summary with file locations

## Troubleshooting

### Qodana CLI Not Installed

```
❌ Qodana CLI not found

Please install:
  macOS:   brew install jetbrains/utils/qodana
  Windows: winget install -e --id JetBrains.QodanaCLI
  Linux:   curl -fsSL https://jb.gg/qodana-cli/install | bash

Then authenticate: qodana login
```

### .NET SDK Not Available

```
❌ .NET SDK not found (required for native mode)

Please ensure .NET 9.0+ is installed:
  dotnet --version

Download from: https://dotnet.microsoft.com/download
```

### Scan Failed

```
❌ Qodana scan failed

Check:
1. qodana.yaml configuration
2. Project builds successfully: dotnet build
3. Sufficient disk space in .qodana/
4. Logs: .qodana/results/log/idea.log
```

### Authentication Issues

```
❌ Qodana authentication failed

Re-authenticate:
  qodana login

Or set token:
  export QODANA_TOKEN=your-token-here
```

## Configuration Options

### Native Mode vs Docker

This skill uses **native mode** (no Docker):
- Faster startup
- Uses local .NET SDK
- Lower resource usage
- Requires Qodana CLI + .NET SDK

For Docker mode, see project CLAUDE.md.

### Scan Scope

By default, scans entire project. Customize in `qodana.yaml`:
```yaml
include:
  - name: All
    paths:
      - src/**/*.cs
```

### Severity Filtering

Adjust what gets fixed automatically (coming soon):
```yaml
failThreshold: 10
excludeInspections:
  - UnusedMember.Global
```

## Integration with Other Workflows

### Before Creating PR

```bash
# 1. Make your changes
# 2. Run Qodana scan
You: Run local qodana scan
# 3. Address issues automatically
# 4. Create PR
You: Create a PR
```

### With TDD Workflow

```bash
# 1. Write test (Red)
# 2. Implement feature (Green)
# 3. Run Qodana scan (Refactor + Quality)
You: Run local qodana scan
# 4. Tests validate refactoring
```

### Before Merge

```bash
# Final quality check before merging
You: Run local qodana scan
# Ensures no quality regressions introduced
```

## Advanced Usage

### Custom Baseline

Compare against a baseline to find only new issues:
```bash
# Generate baseline from main
git checkout main
qodana scan --save-report --results-dir .qodana/baseline
git checkout your-branch

# Compare (manual for now)
qodana compare --baseline .qodana/baseline
```

### Selective Fixing

Currently, the skill fixes all issues found. For selective fixing:
1. Run the scan
2. When tests fail or you want to review
3. Use `git add -p` to stage only desired changes
4. Commit manually

### Integration with CI/CD

This skill is for **local development only**. For CI/CD:
- See `.github/workflows/qodana.yml` in project
- Qodana Cloud integration: https://qodana.cloud

## Tips and Best Practices

1. **Run Frequently**: Catch issues early
2. **Before PRs**: Clean code before review
3. **Trust the Tests**: Let test failures guide you
4. **Review Plans**: Understand fixes before applying
5. **Iterate**: Fix critical issues first, suggestions later

## Related

- **Project CLAUDE.md** - Docker-based Qodana usage
- **CodeRabbit Workflow** - Similar pattern for PR reviews
- **Test Runner Skill** - Automated test execution

## Support

For issues or questions:
1. Check Qodana docs: https://www.jetbrains.com/help/qodana/
2. Review `.qodana/results/log/idea.log`
3. Check project CLAUDE.md for configuration
4. Review sub-agent: `~/.claude/agents/local-qodana-reviewer.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-11-03
**Requires**: Qodana CLI, .NET SDK 9.0+, Git
