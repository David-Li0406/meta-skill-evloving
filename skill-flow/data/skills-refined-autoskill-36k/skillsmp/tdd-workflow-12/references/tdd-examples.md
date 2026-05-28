# TDD Examples from the Codebase

Real examples of TDD workflow from this project.

## Example 1: Adding a New Validation Function

### Scenario
Add a function to validate WSL distribution names.

### Step 1: Write the Test (RED)

```powershell
# In tools/pslib/utils.Tests.ps1

Describe "Test-ValidDistroName" {
    Context "When given valid distribution name" {
        It "Should return true for Ubuntu" {
            $result = Test-ValidDistroName -Name "Ubuntu"
            $result | Should -Be $true
        }
        
        It "Should return true for Debian" {
            $result = Test-ValidDistroName -Name "Debian"
            $result | Should -Be $true
        }
    }
    
    Context "When given invalid distribution name" {
        It "Should return false for empty string" {
            $result = Test-ValidDistroName -Name ""
            $result | Should -Be $false
        }
        
        It "Should return false for null" {
            $result = Test-ValidDistroName -Name $null
            $result | Should -Be $false
        }
    }
}
```

### Step 2: Run Tests - See RED

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit
```

Output:
```
[-] Test-ValidDistroName.When given valid distribution name.Should return true for Ubuntu 12ms
  CommandNotFoundException: The term 'Test-ValidDistroName' is not recognized
```

### Step 3: Implement Minimal Code (GREEN)

```powershell
# In tools/pslib/utils.ps1

function Test-ValidDistroName {
    param([string]$Name)
    
    if ([string]::IsNullOrWhiteSpace($Name)) {
        return $false
    }
    
    return $true
}
```

### Step 4: Run Tests - See GREEN

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit
```

Output:
```
[+] Test-ValidDistroName.When given valid distribution name.Should return true for Ubuntu 8ms
[+] Test-ValidDistroName.When given valid distribution name.Should return true for Debian 7ms
[+] Test-ValidDistroName.When given invalid distribution name.Should return false for empty string 9ms
[+] Test-ValidDistroName.When given invalid distribution name.Should return false for null 8ms
Tests completed in 156ms
Passed: 4 Failed: 0
```

### Step 5: Refactor (if needed)

Add error handling and parameter validation:

```powershell
function Test-ValidDistroName {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $false)]
        [AllowNull()]
        [AllowEmptyString()]
        [string]$Name
    )
    
    if ([string]::IsNullOrWhiteSpace($Name)) {
        return $false
    }
    
    # Could add more validation rules here
    # e.g., check against allowed characters, length limits, etc.
    
    return $true
}
```

### Step 6: Run Tests Again - Still GREEN

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit
```

All tests still pass.

### Step 7: Commit

```bash
git add tools/pslib/utils.ps1 tools/pslib/utils.Tests.ps1
git commit -m "feat: add Test-ValidDistroName function

- Validates WSL distribution names
- Returns false for null or empty strings
- Includes comprehensive unit tests"
```

## Example 2: Modifying Existing Function

### Scenario
Modify `Invoke-CommandLine` to support silent mode.

### Step 1: Read Existing Tests

Review current tests in `tools/pslib/utils.Tests.ps1`:
```powershell
Describe "Invoke-CommandLine" {
    It "Should execute command" {
        Mock Write-Host { }
        $result = Invoke-CommandLine -Command "echo test"
        $result | Should -Not -BeNullOrEmpty
    }
}
```

### Step 2: Add New Test for Silent Mode (RED)

```powershell
Describe "Invoke-CommandLine" {
    # ... existing tests ...
    
    Context "When Silent switch is used" {
        It "Should not output to console" {
            Mock Write-Host { }
            
            Invoke-CommandLine -Command "echo test" -Silent
            
            # Should not call Write-Host
            Should -Invoke Write-Host -Times 0
        }
    }
}
```

### Step 3: Run Tests - See RED

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit
```

Output:
```
[-] Invoke-CommandLine.When Silent switch is used.Should not output to console 15ms
  ParameterBindingException: A parameter cannot be found that matches parameter name 'Silent'
```

### Step 4: Update Implementation (GREEN)

```powershell
function Invoke-CommandLine {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,
        
        [Parameter(Mandatory = $false)]
        [switch]$StopAtError = $false,
        
        [Parameter(Mandatory = $false)]
        [switch]$Silent = $false  # New parameter
    )
    
    # Existing code...
    
    if (-not $Silent) {
        Write-Host $output
    }
    
    return $output
}
```

### Step 5: Run Tests - See GREEN

All tests pass, including new test.

### Step 6: Commit

```bash
git add tools/pslib/utils.ps1 tools/pslib/utils.Tests.ps1
git commit -m "feat: add Silent parameter to Invoke-CommandLine

- Suppresses console output when -Silent is used
- Useful for background operations
- Tests updated to verify behavior"
```

## Example 3: Bug Fix with TDD

### Scenario
Fix bug where `Get-WslDistroType` fails on distribution names with spaces.

### Step 1: Write Test that Reproduces Bug (RED)

```powershell
Describe "Get-WslDistroType" {
    # ... existing tests ...
    
    It "Should handle distribution names with spaces" {
        Mock Invoke-CommandLine { return "Ubuntu 22.04 LTS" }
        
        $result = Get-WslDistroType -DistroName "Ubuntu 22.04 LTS"
        
        $result | Should -Be "ubuntu"
    }
}
```

### Step 2: Run Test - See RED

Test fails because function doesn't handle spaces correctly.

### Step 3: Fix the Bug (GREEN)

```powershell
function Get-WslDistroType {
    param([string]$DistroName)
    
    # Fixed: properly quote the distribution name
    $command = "wsl -d `"$DistroName`" cat /etc/os-release"
    $output = Invoke-CommandLine -Command $command
    
    # Parse output to determine type
    # ...
}
```

### Step 4: Run Tests - See GREEN

Bug is fixed, all tests pass.

### Step 5: Commit

```bash
git add tools/pslib/wsl/wsl.ps1 tools/pslib/wsl.Tests.ps1
git commit -m "fix: handle WSL distribution names with spaces

- Properly quote distribution name in wsl command
- Test added to prevent regression"
```

## TDD Workflow Pattern Summary

For every change:

1. Write/update test (RED)
2. Run tests - confirm failure
3. Write/update code (GREEN)
4. Run tests - confirm pass
5. Refactor if needed
6. Run tests - confirm still pass
7. Commit test + code together

## Integration with Version Control

### Good Commit
```
feat: add distribution validation

- Added Test-ValidDistroName function
- Returns false for null/empty names
- Added comprehensive unit tests
```

Files changed:
- tools/pslib/utils.ps1 (implementation)
- tools/pslib/utils.Tests.ps1 (tests)

### Bad Commit (Don't Do This)
```
feat: add distribution validation
```

Files changed:
- tools/pslib/utils.ps1 (implementation only, no tests)

## Tips for Success

1. Keep RED phase short - write small tests
2. Keep GREEN phase short - write minimal code
3. Refactor fearlessly - tests protect you
4. Run tests frequently - every few minutes
5. Commit frequently - after each GREEN + REFACTOR cycle
6. Never commit without running tests
7. Never commit tests and implementation separately
