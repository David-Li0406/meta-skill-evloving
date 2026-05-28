---
name: run-tests
description: Use when the user asks to run tests or integration tests. Delegates to the test-runner sub-agent to execute the complete clean-build-test workflow for .NET solutions, automatically excluding performance tests and generating comprehensive reports.
allowed-tools: ["Task"]
---

# Run Tests Skill

This skill provides automated testing with the complete clean-build-test workflow for .NET solutions.

## When This Skill Activates

Use this skill when you detect the user wants to run tests. Common trigger phrases:

- "Run tests"
- "Test"
- "Run integration tests"
- "Run all tests"
- "Clean, build and test"
- "Execute tests"
- "Test the solution"

**Key indicators**:
1. Mentions "test" or "tests"
2. May mention "clean" or "build"
3. Implies running the test suite

**Important**: This skill is for regular tests (unit, integration, API). Performance tests are excluded and handled by the `performance-testing` skill.

## What This Skill Does

When activated, immediately delegate to the `test-runner` sub-agent by using the Task tool:

```
Use the Task tool with:
- subagent_type: "test-runner"
- description: "Run solution tests"
- prompt: "Run the complete test workflow: clean solution, build it, discover all test projects excluding performance tests, run all tests (continue even if some fail), and generate a comprehensive report with pass/fail details."
```

## Why Delegate to Sub-agent?

The `test-runner` sub-agent is specialized for this workflow and will:
1. **Find solution**: Automatically discovers .sln file
2. **Clean solution**: Cleans both Debug and Release configurations
3. **Build solution**: Builds in Release configuration
4. **Discover tests**: Finds all test projects in solution
5. **Exclude performance**: Automatically skips performance test projects
6. **Run all tests**: Executes all test projects (continues even if some fail)
7. **Comprehensive reporting**: Shows pass/fail with detailed error messages

## User Experience

**Before this skill:**
```
User: "Run tests"
User: [Manually runs dotnet clean]
User: [Manually runs dotnet build]
User: [Manually finds test projects]
User: [Manually runs each test project]
User: [Tries to remember which tests failed]
```

**With this skill:**
```
User: "Run tests"
Skill: [Auto-activates]
Sub-agent: [Cleans, builds, runs all tests, reports results]
Result: ✅ Clear summary with all pass/fail details
```

## Features

### Automatic Solution Discovery

Finds .sln file in:
- Current directory
- Parent directory

If multiple found, asks which to use.

### Complete Workflow

1. **Clean**: Both Debug and Release
2. **Build**: Release configuration (production-like)
3. **Test**: All test projects with --no-build

### Smart Exclusions

Automatically excludes projects containing:
- `Performance`
- `Perf`
- `Benchmark`
- `LoadTest`
- `StressTest`

**Included** (not excluded):
- Unit tests
- Integration tests
- API tests
- E2E tests

### Comprehensive Reporting

```
🧪 Test Execution Summary

Status: ❌ FAILED

✅ Infrastructure.Tests (247 passed)
✅ Domain.Tests (89 passed)
❌ Application.Tests (2 failed, 154 passed)

Failed Tests:
❌ UserService_Should_Validate_Email
   Error: Expected true, got false
   Location: UserServiceTests.cs:45

Overall: 602/604 passed (99.7%)
Action: Fix 2 failing tests before pushing
```

### Failure Handling

- **Continues running**: Even if some projects fail, runs all others
- **Detailed errors**: Shows exactly which tests failed and why
- **Location info**: File path and line number for each failure
- **Summary stats**: Total pass/fail counts and percentages

## Supporting Files

This skill directory includes:
- `SKILL.md` (this file) - Skill definition and activation logic
- `README.md` - Detailed workflow documentation and examples

## Configuration

### Required: .NET Solution

Must be in a directory with a .sln file (or parent directory).

### Test Project Naming

Test projects should end with:
- `Tests.csproj`
- `Test.csproj`

Examples:
- `MyApp.Tests.csproj` ✅
- `MyApp.Integration.Tests.csproj` ✅
- `MyApp.UnitTest.csproj` ✅

### Performance Test Projects

Name performance test projects with keywords:
- `Performance.Tests`
- `PerformanceTests`
- `Benchmarks`
- `LoadTests`

These will be automatically excluded.

## Troubleshooting

### No Solution Found

**Problem**: "No .NET solution file found"

**Solutions**:
- Ensure you're in the solution directory
- Check parent directory has .sln file
- Navigate to correct directory

### Build Failed

**Problem**: "Build FAILED - Cannot run tests"

**Solutions**:
- Fix compilation errors first
- Try `dotnet restore` for missing packages
- Check `dotnet build` output for details

### No Test Projects Found

**Problem**: "No test projects found in solution"

**Solutions**:
- Ensure test projects exist
- Name them with `Tests.csproj` suffix
- Add to solution: `dotnet sln add MyTests/MyTests.csproj`

### All Projects Excluded

**Problem**: "All test projects were excluded"

**Solutions**:
- Check project names - may all be performance tests
- For performance tests, use: "Run performance tests"
- Rename projects if incorrectly named

## Distinguishing from Performance Tests

### This Skill (Integration/Unit Tests)
**Trigger**: "Run tests", "Test", "Run integration tests"
**Runs**: Unit, Integration, API tests
**Excludes**: Performance, Benchmark, LoadTest projects
**Duration**: Typically 30s - 2min
**Purpose**: Verify functionality before pushing

### Performance Testing Skill
**Trigger**: "Run performance tests", "Check performance"
**Runs**: Performance, Benchmark, LoadTest projects
**Purpose**: Check for regressions, compare with baseline
**Duration**: Typically 2-10min

## Advanced Usage

### Run Specific Configuration

```
You: "Run tests in Debug configuration"

Agent: Uses --configuration Debug instead of Release
```

### After Fixing Failures

```
You: "Run tests"
[See 2 failures]

You: [Fix the failures]

You: "Run tests again"
[See all pass]
```

### Before Creating PR

```
You: "Run tests"
[All pass ✅]

You: "Great! Create PR"
```

### Combined with Other Workflows

```
You: "Run integration tests, then performance tests"

Agent:
[Runs this skill first for integration tests]
[Then runs performance-testing skill for perf tests]
```

## Integration with Other Workflows

### Pre-PR Workflow

```
Workflow: Fix code → Run tests → All pass → Create PR

You: "Run tests"
[All tests pass ✅]

You: "Create pull request"
[PR created with confidence]
```

### With CodeRabbit

```
Workflow: Address CodeRabbit issues → Run tests → Verify → Push

You: "Address latest coderabbit issues on PR #123"
[Fixes applied]

You: "Run tests"
[All pass ✅]

You: [CodeRabbit workflow pushes changes]
```

### Full Feature Branch Workflow

```
1. Develop feature
2. "Run tests" ← This skill
3. All pass → "Create PR"
4. CodeRabbit reviews
5. "Address coderabbit issues"
6. "Run tests" ← This skill again
7. Merge
8. "Clean up after merge"
```

## Tips

- **Run before every push** - Catch failures early
- **Integration tests included** - No need to specify
- **Performance tests separate** - Use different command
- **Fix all failures** - Don't push with failing tests
- **Read error details** - Sub-agent shows exact failure location
