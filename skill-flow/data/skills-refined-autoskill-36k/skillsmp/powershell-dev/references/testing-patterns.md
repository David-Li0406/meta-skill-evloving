# Pester Testing Patterns

Common testing patterns for PowerShell code in this project.

## Test File Structure

```powershell
BeforeAll {
    # Source the module being tested
    . "$PSScriptRoot/utils.ps1"
}

Describe "FunctionName" {
    Context "When condition A" {
        It "Should do behavior X" {
            # Arrange
            $input = "test"
            
            # Act
            $result = FunctionName -Parameter $input
            
            # Assert
            $result | Should -Be "expected"
        }
    }
    
    Context "When condition B" {
        It "Should do behavior Y" {
            # Test implementation
        }
    }
}
```

## Mocking External Commands

### Mock with Assert-MockCalled

```powershell
Describe "Invoke-CommandLine" {
    It "Should execute command" {
        Mock Write-Host { }
        
        Invoke-CommandLine -Command "test command"
        
        Should -Invoke Write-Host -Times 1
    }
}
```

### Mock with Return Values

```powershell
Describe "Get-WslDistroType" {
    It "Should return ubuntu for Ubuntu distro" {
        Mock Invoke-CommandLine { return "Ubuntu" }
        
        $result = Get-WslDistroType -DistroName "Ubuntu"
        
        $result | Should -Be "ubuntu"
    }
}
```

### Mock with Parameter Filters

```powershell
It "Should call wsl command with correct parameters" {
    Mock Invoke-CommandLine { return "output" } -ParameterFilter {
        $Command -like "*wsl --list*"
    }
    
    Get-WslDistros
    
    Should -Invoke Invoke-CommandLine -ParameterFilter {
        $Command -like "*wsl --list*"
    }
}
```

## Testing Error Conditions

### Should -Throw

```powershell
It "Should throw when parameter is null" {
    { FunctionName -Parameter $null } | Should -Throw
}

It "Should throw specific error message" {
    { FunctionName -Invalid } | Should -Throw "*specific error*"
}
```

### Should -Not -Throw

```powershell
It "Should not throw with valid input" {
    { FunctionName -Parameter "valid" } | Should -Not -Throw
}
```

## Testing File Operations

### Mock Test-Path

```powershell
It "Should create directory if not exists" {
    Mock Test-Path { return $false }
    Mock New-Item { }
    
    New-Directory -Path "C:\Test"
    
    Should -Invoke New-Item -Times 1
}

It "Should skip creation if directory exists" {
    Mock Test-Path { return $true }
    Mock New-Item { }
    
    New-Directory -Path "C:\Test"
    
    Should -Invoke New-Item -Times 0
}
```

### Mock File Content

```powershell
It "Should read configuration" {
    Mock Get-Content { return '{"key": "value"}' }
    
    $config = Read-Config -Path "config.json"
    
    $config.key | Should -Be "value"
}
```

## Testing CI vs Interactive Behavior

```powershell
Context "When running in CI" {
    BeforeEach {
        Mock Test-RunningInCIorTestEnvironment { return $true }
    }
    
    It "Should use automated path" {
        $result = Get-UserConfirmation "Proceed?"
        $result | Should -Be $true
    }
}

Context "When running interactively" {
    BeforeEach {
        Mock Test-RunningInCIorTestEnvironment { return $false }
        Mock Read-Host { return "y" }
    }
    
    It "Should prompt user" {
        $result = Get-UserConfirmation "Proceed?"
        Should -Invoke Read-Host -Times 1
    }
}
```

## Parameterized Tests

### TestCases

```powershell
It "Should handle various inputs: <Input>" -TestCases @(
    @{ Input = "test1"; Expected = "result1" }
    @{ Input = "test2"; Expected = "result2" }
    @{ Input = "test3"; Expected = "result3" }
) {
    param($Input, $Expected)
    
    $result = FunctionName -Parameter $Input
    $result | Should -Be $Expected
}
```

### ForEach

```powershell
Context "Input validation" {
    @("", $null, " ") | ForEach-Object {
        It "Should reject empty input: '$_'" {
            { FunctionName -Parameter $_ } | Should -Throw
        }
    }
}
```

## Testing Output

### Capture Write-Host

```powershell
It "Should output status message" {
    Mock Write-Host { }
    
    FunctionName
    
    Should -Invoke Write-Host -ParameterFilter {
        $Object -like "*Success*"
    }
}
```

### Capture Write-Error

```powershell
It "Should write error message" {
    Mock Write-Error { }
    
    FunctionName -Invalid
    
    Should -Invoke Write-Error -Times 1
}
```

## BeforeAll/AfterAll Pattern

```powershell
Describe "Integration Test" {
    BeforeAll {
        # Setup: Create test files, start services, etc.
        New-Item -Path "TestDrive:\test.txt" -ItemType File
    }
    
    AfterAll {
        # Cleanup: Remove test files, stop services, etc.
        Remove-Item -Path "TestDrive:\test.txt" -Force
    }
    
    It "Should use test file" {
        # Test implementation
    }
}
```

## BeforeEach/AfterEach Pattern

```powershell
Describe "Multiple Tests" {
    BeforeEach {
        # Setup before each test
        $script:testVar = "initial"
    }
    
    AfterEach {
        # Cleanup after each test
        $script:testVar = $null
    }
    
    It "Test 1" {
        $script:testVar | Should -Be "initial"
    }
    
    It "Test 2" {
        $script:testVar | Should -Be "initial"
    }
}
```

## Integration Test Patterns

### Tag-Based Separation

```powershell
Describe "Unit Tests" -Tag "Unit" {
    It "Should mock external calls" {
        Mock Invoke-CommandLine { return "mocked" }
        # Test with mocks
    }
}

Describe "Integration Tests" -Tag "Integration" {
    It "Should call real external commands" {
        # Test with real commands
    }
}
```

Run specific tags:
```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit
pwsh -File ".\test\bin\testrunner.ps1" -Integration
```

## PowerShell 5.1 Compatibility

### Avoid PS 6.0+ Features

```powershell
# Bad (PS 7.0+)
$result = $value ? "yes" : "no"

# Good (PS 5.1+)
$result = if ($value) { "yes" } else { "no" }
```

```powershell
# Bad (PS 7.0+)
$config = $userConfig ?? $defaultConfig

# Good (PS 5.1+)
$config = if ($null -ne $userConfig) { $userConfig } else { $defaultConfig }
```

## Best Practices

1. **Arrange-Act-Assert pattern** - Separate setup, execution, and verification
2. **One assertion per test** - Each test should verify one behavior
3. **Descriptive test names** - Use "Should do X when Y" format
4. **Mock external dependencies** - Isolate unit tests from external systems
5. **Test both success and failure paths** - Cover error conditions
6. **Use TestCases for similar tests** - Reduce duplication
7. **BeforeAll for expensive setup** - Share setup across tests
8. **Clean up in AfterAll** - Remove test artifacts
9. **Test on both PS 5.1 and 7.x** - Ensure compatibility
10. **Keep tests fast** - Mock slow operations in unit tests
