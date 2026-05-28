# GitHub Actions CI/CD Patterns

## Shell Selection Limitation

**IMPORTANT:** You CANNOT use matrix variables in the `shell` field of GitHub Actions steps. The `shell` field only accepts literal values, not matrix interpolation.

### Incorrect (Will Not Work)

```yaml
shell: ${{ matrix.shell }}  # This does NOT work
run: |
  Write-Output $PSVersionTable
  .\test\bin\testrunner.ps1
```

### Correct Approach

```yaml
shell: cmd  # Use a literal shell value
run: |
  # Invoke matrix shell within the command
  ${{ matrix.shell }} -Command "Write-Output $PSVersionTable; .\test\bin\init.ps1; .\test\bin\testrunner.ps1 -Coverage"
```

## Current Test Workflow Pattern

The project uses this pattern in `.github/workflows/test.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  test:
    name: Tests (${{ matrix.shell_name }})
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: windows-latest
            shell: pwsh
            shell_name: "Powershell 7.x"
            shell_label: PS7
          - os: windows-latest
            shell: powershell
            shell_name: "Powershell 5.x"
            shell_label: PS5
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Install Dependencies
        shell: cmd
        run: |
          ${{ matrix.shell }} -Command ".\test\bin\init.ps1"
      - name: Execute Tests
        continue-on-error: true
        shell: cmd
        run: |
          ${{ matrix.shell }} -Command ".\test\bin\testrunner.ps1 -Coverage"
      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        with:
          name: junit-results-${{ matrix.shell_label }}
          path: "**/junit.xml"
          if-no-files-found: error
      - name: Upload Coverage Reports
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.shell_label }}
          path: "test/out/coverage.xml"
          if-no-files-found: error

  report:
    name: Finalize Results
    needs: test
    runs-on: ubuntu-latest
    if: always()
    permissions:
      checks: write
      pull-requests: write
      contents: read
    steps:
      - name: Download All Results
        uses: actions/download-artifact@v4
        with:
          path: all-results
          pattern: junit-results-*
      - name: Publish and Evaluate Test Report
        uses: mikepenz/action-junit-report@v6
        with:
          report_paths: "all-results/**/junit.xml"
          detailed_summary: true
          include_passed: true
          fail_on_failure: true
          check_name: "Pester Test Results"
```

## Key Patterns

### Matrix Strategy for Multiple PowerShell Versions

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - shell: pwsh
        shell_label: PS7
      - shell: powershell
        shell_label: PS5
```

### Wrapper Shell Pattern

Uses `shell: cmd` as literal, then invokes the matrix shell:

```yaml
shell: cmd
run: |
  ${{ matrix.shell }} -Command ".\script.ps1"
```

### Artifact Upload Pattern

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: junit-results-${{ matrix.shell_label }}
    path: "**/junit.xml"
    if-no-files-found: error
```

### Continue on Error for Aggregation

```yaml
continue-on-error: true  # Essential for aggregating results later
```

### Report Job with Dependencies

```yaml
report:
  needs: test
  if: always()  # Run even if test job fails
```

## Test Initialization

Before running tests in CI, install dependencies:

```yaml
- name: Install Dependencies
  shell: cmd
  run: |
    ${{ matrix.shell }} -Command ".\test\bin\init.ps1"
```

The `init.ps1` script installs:

- Pester 5.7.1+
- PSScriptAnalyzer 1.24.0+
- Updates WSL (if available)

## Artifacts Generated

| Artifact | Path | Description |
|----------|------|-------------|
| JUnit XML | `test/out/junit.xml` | Test results for reporting |
| Coverage XML | `test/out/coverage.xml` | JaCoCo format coverage |
| Summary MD | `test/out/test-summary.md` | PR comment summary |

## Using mikepenz/action-junit-report

```yaml
- uses: mikepenz/action-junit-report@v6
  with:
    report_paths: "all-results/**/junit.xml"
    detailed_summary: true
    include_passed: true
    fail_on_failure: true
    check_name: "Pester Test Results"
```

This creates a check run with:

- Detailed test summary
- Pass/fail status
- Individual test results
