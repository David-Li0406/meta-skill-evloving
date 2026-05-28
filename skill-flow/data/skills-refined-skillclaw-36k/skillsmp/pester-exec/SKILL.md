---
name: pester-exec
description: Execute Pester tests for PowerShell code in this project. Use this skill when: (1) Running unit tests, (2) Running integration tests, (3) Running tests with code coverage, (4) Running tests on specific files or paths, (5) Running tests on both PowerShell 5.1 and 7.x, (6) Executing pre-commit test checks, (7) Troubleshooting test failures, or any Pester-related testing task.
---

# Pester Test Execution

Execute Pester tests for PowerShell code in this project.

## Quick Reference

### Standard Test Commands

```bash
# Unit tests only (fast feedback)
pwsh -File ".\test\bin\testrunner.ps1" -Unit

# Integration tests only
pwsh -File ".\test\bin\testrunner.ps1" -Integration

# All tests (unit + integration)
pwsh -File ".\test\bin\testrunner.ps1"

# With code coverage
pwsh -File ".\test\bin\testrunner.ps1" -Coverage
pwsh -File ".\test\bin\testrunner.ps1" -Unit -Coverage
pwsh -File ".\test\bin\testrunner.ps1" -Integration -Coverage

# Specific test path
pwsh -File ".\test\bin\testrunner.ps1" -TestPath "tools\pslib\utils\utils.Tests.ps1"

# PowerShell 5.1 compatibility
powershell -File ".\test\bin\testrunner.ps1" -Unit
powershell -File ".\test\bin\testrunner.ps1"
```

### Test Types

| Type | Pattern | Purpose |
|------|---------|---------|
| Unit | `*.Tests.ps1` | Fast, isolated tests with mocked dependencies |
| Integration | `*.Integration.Tests.ps1` | Tests interacting with real systems (WSL, file system) |

## Development Workflow

### Local Development (Recommended)

1. Run unit tests first for fast feedback
2. Run integration tests when necessary or before committing
3. Both suites must pass before pushing

### Pre-Commit Checks (Mandatory)

Before every commit:

1. Run unit tests: `pwsh -File ".\test\bin\testrunner.ps1" -Unit`
2. Run integration tests if integration points were modified
3. Linting runs automatically with tests (PSScriptAnalyzer)

**Never commit if:**

- Any unit test fails
- Any integration test fails
- Function changes lack corresponding test updates

### TDD Workflow (Red-Green-Refactor)

1. Update tests to expect new behavior (Red)
2. Run tests - confirm they fail
3. Update implementation (Green)
4. Run tests - confirm they pass
5. Commit tests and implementation together

## Output and Reports

| Output | Location | Description |
|--------|----------|-------------|
| JUnit XML | `test/out/junit.xml` | Test results for CI |
| Coverage XML | `test/out/coverage.xml` | JaCoCo format coverage |
| Summary MD | `test/out/test-summary.md` | Markdown summary for PR comments |

## Test Infrastructure

### testrunner.ps1 Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-Unit` | switch | Run only unit tests |
| `-Integration` | switch | Run only integration tests |
| `-Coverage` | switch | Enable code coverage |
| `-TestPath` | string[] | Custom paths to search |
| `-Verbosity` | string | Output verbosity (Detailed, Normal, Minimal) |
| `-Filter` | string | Pester tag filter |
| `-ExcludePattern` | string | Pattern to exclude files |

### init.ps1

Installs test dependencies:

- Pester 5.7.1+
- PSScriptAnalyzer 1.24.0+

Run before first test execution: `pwsh -File ".\test\bin\init.ps1"`

## PowerShell Version Compatibility

All tests must pass on both PowerShell 5.1 and 7.x.

**Avoid these PowerShell 6.0+ features:**

- `ErrorMessage` parameter in `ValidateScript`
- Ternary operator `? :`
- Null-coalescing operators `??`, `??=`

**Always test on both versions before PR:**

```bash
pwsh -File ".\test\bin\testrunner.ps1"
powershell -File ".\test\bin\testrunner.ps1"
```

## AI Agent Patterns

See [references/ai-agent-patterns.md](references/ai-agent-patterns.md) for:

- Path quoting rules when calling PowerShell from Bash
- PowerShell piping patterns (avoid bash-to-PowerShell pipes)
- Error prevention guidelines

## Advanced Workflows

See [references/workflows.md](references/workflows.md) for:

- Running specific test files
- Debugging test failures
- Pester test structure and mocking patterns
- Writing new tests (TDD approach)

## CI/CD Integration

See [references/github-actions.md](references/github-actions.md) for:

- GitHub Actions workflow patterns
- Matrix strategy for multiple PowerShell versions
- Shell selection limitations and workarounds
