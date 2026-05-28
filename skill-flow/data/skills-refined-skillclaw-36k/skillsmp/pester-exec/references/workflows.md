# Advanced Pester Workflows

## Running Specific Test Files

```powershell
# PowerShell 7.x - specific file
pwsh -Command "Invoke-Pester -Path '.\path\to\script.Tests.ps1'"

# PowerShell 5.1 - specific file
powershell -Command "Invoke-Pester -Path '.\path\to\script.Tests.ps1'"

# Via testrunner with path
pwsh -File ".\test\bin\testrunner.ps1" -TestPath "tools\pslib\utils\utils.Tests.ps1"
```

## Pester Test Structure

```powershell
Describe "Function-Name" {
    Context "When condition or scenario" {
        It "Should do expected behavior" {
            # Arrange
            $input = "test"

            # Act
            $result = Function-Name -Parameter $input

            # Assert
            $result | Should -Be "expected"
        }
    }
}
```

## Mocking Patterns

### Basic Mock

```powershell
Mock Test-Path { return $true }
```

### Mock with Parameter Filter

```powershell
Mock Get-Item {
    @{ Value = "mocked" }
} -ParameterFilter { $Path -eq "Env:\VARIABLE" }
```

### Verify Mock Calls

```powershell
Should -Invoke Test-Path -Times 1
Should -Invoke Get-Command -Exactly -Times 2
```

### Mock External Commands

```powershell
Mock Invoke-CommandLine { return $true } -ParameterFilter {
    $Command -like "*scoop*"
}
```

## Setup and Teardown

```powershell
BeforeAll {
    # One-time setup for all tests in block
    $script:testData = @{}
}

AfterAll {
    # One-time cleanup after all tests
}

BeforeEach {
    # Runs before each It block
    $testInput = "fresh"
}

AfterEach {
    # Runs after each It block
}
```

## Testing CI vs Interactive Behavior

Use `Test-RunningInCIorTestEnvironment` from `tools/pslib/utils/utils.ps1`:

```powershell
# Test CI path
Context "In CI environment" {
    BeforeAll {
        Mock Test-RunningInCIorTestEnvironment { return $true }
    }
    It "Should auto-confirm" {
        # Test non-interactive behavior
    }
}

# Test interactive path
Context "In interactive environment" {
    BeforeAll {
        Mock Test-RunningInCIorTestEnvironment { return $false }
    }
    It "Should prompt user" {
        # Test interactive behavior
    }
}
```

## Writing New Tests (TDD)

### 1. Create Test File

Name: `<source-file>.Tests.ps1` (same directory as source)

### 2. Write Failing Test First

```powershell
Describe "New-Feature" {
    It "Should return expected value" {
        $result = New-Feature -Input "test"
        $result | Should -Be "expected"
    }
}
```

### 3. Run Test (Red)

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit
# Expected: test fails
```

### 4. Implement Feature (Green)

Write minimum code to pass the test.

### 5. Run Test Again

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit
# Expected: test passes
```

### 6. Refactor

Improve code while keeping tests green.

## Debugging Test Failures

### Increase Verbosity

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Verbosity Detailed
```

### Run Single Test

```powershell
pwsh -Command "Invoke-Pester -Path '.\file.Tests.ps1' -Output Detailed"
```

### Check Exit Codes

```powershell
# After Invoke-CommandLine
$LASTEXITCODE
```

### Inspect Mock Calls

```powershell
Should -Invoke Command-Name -ParameterFilter { $param -eq "value" }
```

## Test Coverage Best Practices

### Coverage Targets

- Test both success and failure paths
- Test edge cases and boundary conditions
- Test CI and interactive environment behavior separately
- Mock all external dependencies

### What to Mock

- File system operations (`Test-Path`, `Get-ChildItem`)
- Environment variables (`Get-Item Env:\*`)
- External commands (`Invoke-CommandLine`)
- User interaction (`Get-UserConfirmation`)
- Network operations

### What NOT to Mock

- The function under test
- Pure logic functions
- Data structures

## Integration Test Patterns

Integration tests (`*.Integration.Tests.ps1`) test real system interactions.

### WSL Integration Tests

```powershell
Describe "WSL Operations" -Skip:(-not (Get-Command wsl -ErrorAction SilentlyContinue)) {
    It "Should list distributions" {
        $result = Get-WslDistributions
        $result | Should -Not -BeNullOrEmpty
    }
}
```

### File System Integration Tests

```powershell
BeforeAll {
    $testDir = Join-Path $TestDrive "integration-test"
    New-Item -ItemType Directory -Path $testDir -Force
}

AfterAll {
    Remove-Item -Path $testDir -Recurse -Force -ErrorAction SilentlyContinue
}
```

## Common Assertions

```powershell
$result | Should -Be "exact"
$result | Should -BeExactly "case-sensitive"
$result | Should -BeLike "*pattern*"
$result | Should -Match "regex"
$result | Should -BeNullOrEmpty
$result | Should -Not -BeNullOrEmpty
$result | Should -BeTrue
$result | Should -BeFalse
$result | Should -Throw
$result | Should -HaveCount 3
$result | Should -Contain "item"
```
