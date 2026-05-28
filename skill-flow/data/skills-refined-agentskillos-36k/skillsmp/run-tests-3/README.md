# Run Tests Skill

Automated testing with complete clean-build-test workflow for .NET solutions.

## Overview

This skill streamlines the testing process by:
1. Automatically finding your .NET solution
2. Cleaning the solution (fresh start)
3. Building the solution (Release configuration)
4. Discovering all test projects
5. Excluding performance tests
6. Running all tests (continues even if some fail)
7. Generating comprehensive reports with detailed failure information

## Quick Start

Simply say:
```
"Run tests"
```

The skill auto-activates and handles the complete workflow.

## The Problem This Solves

### Before (Manual Multi-Step Process)

```
You: "Let me clean the solution..."
You: dotnet clean MyApp.sln --configuration Debug
You: dotnet clean MyApp.sln --configuration Release
You: "Now build it..."
You: dotnet build MyApp.sln --configuration Release
You: "What test projects do I have again?"
You: dotnet sln list | grep Tests
You: "Ok, run the first one..."
You: dotnet test Project1.Tests
You: "Now the second..."
You: dotnet test Project2.Tests
You: "Wait, did the first one pass? Let me scroll back..."
You: "Which test failed? Where's that error message?"
Result: 10 minutes wasted, unclear results
```

### After (With This Skill)

```
You: "Run tests"
Skill: ✅ Complete workflow in one command
Result: Clean summary with all pass/fail details in < 1 minute
```

## How It Works

### Architecture

```
User Request
    ↓
[run-tests Skill] ← Auto-activates
    ↓
[test-runner Sub-agent] ← Executes workflow
    ↓
Clean → Build → Discover → Test → Report
```

### Complete Workflow

```
1. Find Solution
   ↓
2. Clean (Debug + Release)
   ↓
3. Build (Release)
   ↓
4. Discover Test Projects
   ↓
5. Filter Out Performance Tests
   ↓
6. Run Each Test Project
   ↓
7. Generate Comprehensive Report
```

## Components

### 1. Skill (This Directory)
**File**: `~/.claude/skills/run-tests/SKILL.md`

**Purpose**: Auto-activation and delegation

**Trigger Phrases**:
- "Run tests"
- "Test"
- "Run integration tests"
- "Clean, build and test"

### 2. Sub-agent
**File**: `~/.claude/agents/test-runner.md`

**Purpose**: Complete workflow execution

**Capabilities**:
- Solution discovery
- Clean and build
- Test project discovery
- Selective exclusions
- Comprehensive reporting

## Features

### Automatic Solution Discovery

**Searches**:
1. Current directory for `*.sln`
2. Parent directory for `*.sln`

**Multiple solutions**:
```
🔍 Found multiple solution files:
1. CodexForge.BCL.sln
2. CodexForge.All.sln

Which solution should I use?
```

### Clean-Build-Test Workflow

**Step 1: Clean**
```bash
dotnet clean MyApp.sln --configuration Debug
dotnet clean MyApp.sln --configuration Release
```

**Step 2: Build**
```bash
dotnet build MyApp.sln --configuration Release --verbosity minimal
```

Stops here if build fails - no point running tests on broken code.

**Step 3: Test**
```bash
# For each test project (excluding performance):
dotnet test Project.Tests --no-build --configuration Release --verbosity normal
```

### Smart Test Project Discovery

**Finds projects matching**:
- `*Tests.csproj`
- `*Test.csproj`

**Examples found**:
- `MyApp.Tests.csproj` ✅
- `MyApp.Infrastructure.Tests.csproj` ✅
- `MyApp.Integration.Tests.csproj` ✅
- `MyApp.UnitTest.csproj` ✅

### Automatic Performance Test Exclusion

**Excludes projects containing** (case-insensitive):
- `Performance`
- `Perf`
- `Benchmark`
- `LoadTest`
- `StressTest`

**Examples excluded**:
- `MyApp.Performance.Tests.csproj` ⏭️
- `MyApp.PerformanceTests.csproj` ⏭️
- `MyApp.Benchmarks.csproj` ⏭️
- `MyApp.LoadTests.csproj` ⏭️

**Included (NOT excluded)**:
- `MyApp.Integration.Tests` ✅
- `MyApp.E2E.Tests` ✅
- `MyApp.API.Tests` ✅
- `MyApp.UnitTests` ✅

### Comprehensive Failure Reporting

**For each failed test**:
- Test name
- Error message
- File location (path:line)
- Stack trace excerpt

**Example**:
```
❌ UserService_Should_Validate_Email

   Error: Expected: true, Actual: false
   Location: UserServiceTests.cs:45

   Stack Trace:
   at UserService.ValidateEmail(String email)
   at UserServiceTests.UserService_Should_Validate_Email()
```

### Continue on Failure

Tests continue running even if some fail:

```
[1/5] Infrastructure.Tests... ✅ PASSED
[2/5] Domain.Tests... ✅ PASSED
[3/5] Application.Tests... ❌ FAILED (2 failures)
[4/5] Integration.Tests... ✅ PASSED (continues despite #3 failure)
[5/5] API.Tests... ✅ PASSED
```

This gives you the **complete picture** rather than stopping at first failure.

## Example Workflows

### Scenario 1: All Tests Pass

```bash
# You've finished your feature
git status
# M  src/UserService.cs
# M  test/UserServiceTests.cs
```

```
You: "Run tests"

Skill Output:
🔍 Found solution: CodexForge.BCL.sln

🧹 Cleaning solution...
   ✅ Debug configuration cleaned
   ✅ Release configuration cleaned

🔨 Building solution...
   Microsoft (R) Build Engine version 17.8.0
   ...
   ✅ Build succeeded (3.2s)

🧪 Discovered test projects:

To Run (5):
  ✓ CodexForge.BCL.Infrastructure.Tests
  ✓ CodexForge.BCL.Domain.Tests
  ✓ CodexForge.BCL.Application.Tests
  ✓ CodexForge.BCL.Integration.Tests
  ✓ CodexForge.BCL.API.Tests

Excluded (3):
  ⏭️ CodexForge.BCL.Performance.Tests (performance)
  ⏭️ CodexForge.BCL.LoadTests (performance)
  ⏭️ CodexForge.BCL.Benchmarks (performance)

🧪 Running tests...

[1/5] CodexForge.BCL.Infrastructure.Tests...
   ✅ PASSED (247 tests, 12.3s)

[2/5] CodexForge.BCL.Domain.Tests...
   ✅ PASSED (89 tests, 4.2s)

[3/5] CodexForge.BCL.Application.Tests...
   ✅ PASSED (156 tests, 8.7s)

[4/5] CodexForge.BCL.Integration.Tests...
   ✅ PASSED (45 tests, 15.4s)

[5/5] CodexForge.BCL.API.Tests...
   ✅ PASSED (67 tests, 9.8s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ✅ ALL TESTS PASSED
Total Tests: 604
Passed: 604 (100%)
Failed: 0
Total Duration: 50.4s

✅ Safe to push and create PR!
```

**Next step**:
```
You: "Great! Create pull request"
```

### Scenario 2: Some Tests Fail

```
You: "Run tests"

Skill Output:
🔍 Found solution: CodexForge.BCL.sln

🧹 Cleaning solution...
   ✅ Cleaned

🔨 Building solution...
   ✅ Build succeeded (3.1s)

🧪 Running tests...

[1/5] Infrastructure.Tests...
   ✅ PASSED (247 tests, 12.3s)

[2/5] Domain.Tests...
   ✅ PASSED (89 tests, 4.2s)

[3/5] Application.Tests...
   ❌ FAILED (2 failures, 154 passed, 8.7s)

[4/5] Integration.Tests...
   ✅ PASSED (45 tests, 15.4s)

[5/5] API.Tests...
   ✅ PASSED (67 tests, 9.8s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Failed Tests (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ CodexForge.BCL.Application.Tests.UserServiceTests.UserService_Should_Validate_Email

   Error: Assert.True() Failure
          Expected: True
          Actual:   False

   Location: UserServiceTests.cs:45

   Stack Trace:
   at CodexForge.BCL.Application.Services.UserService.ValidateEmail(String email)
   at CodexForge.BCL.Application.Tests.UserServiceTests.UserService_Should_Validate_Email() in UserServiceTests.cs:line 45

❌ CodexForge.BCL.Application.Tests.OrderProcessorTests.OrderProcessor_Should_Handle_Null

   Error: System.NullReferenceException: Object reference not set to an instance of an object.

   Location: OrderProcessorTests.cs:78

   Stack Trace:
   at CodexForge.BCL.Application.Services.OrderProcessor.Process(Order order)
   at CodexForge.BCL.Application.Tests.OrderProcessorTests.OrderProcessor_Should_Handle_Null() in OrderProcessorTests.cs:line 78

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ❌ FAILED
Total Tests: 604
Passed: 602 (99.7%)
Failed: 2 (0.3%)
Total Duration: 50.4s

⚠️ Action Required: Fix 2 failing tests before pushing to PR
```

**Next steps**:
```
You: "Fix the email validation test - check UserServiceTests.cs:45"
[Review and fix the code]

You: "Run tests"
[Verify fixes work]
```

### Scenario 3: Build Failure

```
You: "Run tests"

Skill Output:
🔍 Found solution: CodexForge.BCL.sln

🧹 Cleaning solution...
   ✅ Cleaned

🔨 Building solution...
   src/UserService.cs(23,18): error CS1002: ; expected

   ❌ Build FAILED

Cannot run tests until build succeeds.

To see detailed build errors, run:
  dotnet build CodexForge.BCL.sln --verbosity detailed

Common issues:
- Compilation errors in code
- Missing NuGet packages (try: dotnet restore)
- Target framework mismatch
```

**Fix and retry**:
```
You: [Fix the syntax error]

You: "Run tests"
[Now builds and tests successfully]
```

### Scenario 4: Integration Tests Focus

```
You: "Run integration tests"

Skill Output:
🔍 Found solution: CodexForge.BCL.sln

🧹 Cleaning solution...
   ✅ Cleaned

🔨 Building solution...
   ✅ Build succeeded

🧪 Running tests...
   (Integration tests are included automatically)

[1/5] Infrastructure.Tests... ✅
[2/5] Domain.Tests... ✅
[3/5] Application.Tests... ✅
[4/5] Integration.Tests... ✅ (This one runs too!)
[5/5] API.Tests... ✅

✅ ALL TESTS PASSED (including integration tests)
```

**Note**: Integration tests are NOT excluded. They run by default unless they're also performance tests.

## Configuration

### Required: .NET Solution

Your project must have a `.sln` file:
```bash
ls *.sln
# CodexForge.BCL.sln
```

### Test Project Structure

**Standard structure**:
```
MySolution/
├── MySolution.sln
├── src/
│   ├── MyApp/
│   ├── MyApp.Domain/
│   └── MyApp.Infrastructure/
└── test/
    ├── MyApp.Tests/                    ✅ Runs
    ├── MyApp.Integration.Tests/        ✅ Runs
    ├── MyApp.API.Tests/                ✅ Runs
    └── MyApp.Performance.Tests/        ⏭️ Excluded
```

### Test Project Naming

**Will be discovered** (ends with Test/Tests):
- `MyApp.Tests.csproj`
- `MyApp.UnitTests.csproj`
- `MyApp.Integration.Tests.csproj`
- `MyApp.API.Test.csproj`

**Will be excluded** (performance keywords):
- `MyApp.Performance.Tests.csproj`
- `MyApp.PerformanceTests.csproj`
- `MyApp.Benchmarks.csproj`
- `MyApp.LoadTests.csproj`

### Build Configuration

**Default**: Release configuration
- Matches production build
- Better performance
- What you'll deploy

**Override**: Mention in request
```
You: "Run tests in Debug configuration"
```

## Memory Management

### MSBuild Process Cleanup

**Issue**: After running tests multiple times, MSBuild node processes accumulate in memory.

**Symptoms**:
```bash
ps aux | grep MSBuild.dll
# Shows 20-30 MSBuild.dll processes consuming 3-4GB RAM
```

**Solution**: This skill automatically handles cleanup:
1. Sets `MSBUILDDISABLENODEREUSE=1` to prevent node creation
2. Kills lingering MSBuild processes after test completion
3. Ensures clean slate for every test run

**Manual Cleanup** (if needed):
```bash
# Kill MSBuild nodes
pkill -f "MSBuild.dll"

# Or use dotnet command
dotnet build-server shutdown
```

**Why This Happens**:
- MSBuild uses persistent build nodes for performance
- Integration tests can spawn background services
- Without cleanup, processes accumulate over time

**Memory Impact**:
- Without cleanup: ~150MB per process × 20-30 processes = 3-4GB
- With cleanup: Clean slate after every run

## Troubleshooting

### No Solution Found

**Problem**: "No .NET solution file (.sln) found"

**Solutions**:
1. Check you're in solution directory: `ls *.sln`
2. Navigate to solution root
3. Check parent directory has .sln file

### Build Failed

**Problem**: "Build FAILED - Cannot run tests"

**Solutions**:
1. Fix compilation errors shown in output
2. Try `dotnet restore` to restore packages
3. Run `dotnet build` manually for detailed errors
4. Check for missing dependencies

### No Test Projects Found

**Problem**: "No test projects found in solution"

**Solutions**:
1. Ensure test projects exist
2. Name them with `Tests.csproj` or `Test.csproj` suffix
3. Add to solution: `dotnet sln add path/to/Tests.csproj`
4. Verify with: `dotnet sln list | grep Tests`

### All Projects Excluded

**Problem**: "All test projects were excluded (performance tests)"

**Cause**: All your test projects have performance keywords

**Solutions**:
1. For performance tests, use: "Run performance tests"
2. Rename projects if they're not actually performance tests
3. Check project names don't accidentally contain "Perf", "Performance", etc.

### Tests Take Too Long

**Problem**: Tests run for several minutes

**Possible causes**:
1. Integration tests hitting real databases/APIs
2. Too many tests in suite
3. Performance tests not properly excluded

**Solutions**:
1. Check excluded projects list
2. Optimize slow integration tests
3. Consider test parallelization
4. Run performance tests separately

## Advanced Usage

### Debug Configuration

```
You: "Run tests in Debug configuration"

Agent: Uses --configuration Debug for build and tests
```

### Specific Test Project

If you want to run just one project:
```
You: "Run tests for Infrastructure.Tests only"

Agent: Runs only that project (still cleans and builds solution first)
```

### After Fixing Specific Test

```
You: "Run tests"
[See UserService test fail]

You: [Fix UserServiceTests.cs:45]

You: "Run tests again"
[Verify fix works]
```

### Pre-Push Checklist

```
1. "Run tests" ← This skill
2. All pass? ✅
3. "Run performance tests" ← performance-testing skill
4. No regressions? ✅
5. "git push" or "Create PR"
```

## Integration with Other Workflows

### Full Feature Branch Workflow

```
Day 1:
- Develop feature
- "Run tests" ← Quick feedback

Day 2:
- Continue development
- "Run tests" ← Verify no regressions

Ready to push:
- "Run tests" ← Final check
- "Run performance tests" ← Check performance
- "Create pull request"

After CodeRabbit review:
- "Address coderabbit issues"
- "Run tests" ← Verify fixes
- Merge

After merge:
- "Clean up after merge"
```

### With CodeRabbit Workflow

```
You: "Address latest coderabbit issues on PR #123"
[CodeRabbit fixes applied]

You: "Run tests"
[Verify fixes didn't break anything]

[If tests pass, CodeRabbit workflow pushes]
```

### CI/CD Integration

Add to your CI pipeline:
```yaml
- name: Run Tests
  run: |
    dotnet clean
    dotnet build --configuration Release
    dotnet test --no-build --configuration Release
```

Or use Claude Code in CI:
```yaml
- name: Run Tests with Claude Code
  run: |
    claude-code "run tests"
```

## Best Practices

### 1. Run Before Every Push

```
You: [Make changes]
You: "Run tests"
You: [All pass ✅]
You: git push
```

Don't push without running tests!

### 2. Fix Failures Immediately

```
You: "Run tests"
[2 failures]
You: [Fix immediately]
You: "Run tests"
[All pass ✅]
```

Don't accumulate failing tests.

### 3. Read Failure Details

The sub-agent shows exact:
- Test name
- Error message
- File location
- Line number

Use this to fix quickly.

### 4. Separate Performance Tests

Regular tests (this skill):
- Quick (< 2 min)
- Run frequently
- Before every push

Performance tests (separate):
- Slower (2-10 min)
- Run less frequently
- Before major releases

### 5. Keep Tests Fast

If tests take > 5 minutes:
- Review integration test efficiency
- Check for accidentally included performance tests
- Consider test parallelization

## Tips

- **Use "Run tests" frequently** - Catch issues early
- **Integration tests included** - No need to specify separately
- **Performance tests excluded** - Use separate command for those
- **Fix all failures** - Don't push with broken tests
- **Read error locations** - Sub-agent tells you exactly where to look
- **Clean-build-test is one command** - No need to run separately

---

**Happy testing! 🧪✅**
