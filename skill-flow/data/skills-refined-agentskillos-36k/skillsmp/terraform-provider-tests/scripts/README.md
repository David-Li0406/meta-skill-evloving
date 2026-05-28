# Terraform Provider Tests - Scripts

This directory contains automation scripts for analyzing and testing Terraform provider code.

## Available Scripts

### 1. analyze_gap.py - Test Coverage Gap Analysis

**Purpose**: Automatically analyze test files to identify modernization gaps and generate comprehensive reports.

**Usage**:
```bash
python3 analyze_gap.py <test_directory> [--output report.md]
```

**Examples**:
```bash
# Analyze provider tests with timestamped report
python3 analyze_gap.py ./internal/provider/ --output ./ai_reports/tf_provider_tests_gap_$(date +%Y%m%d_%H%M%S).md

# Quick analysis with simple filename
python3 analyze_gap.py ./internal/provider/ --output ./ai_reports/tf_provider_tests_gap.md
```

**What It Detects**:
- ✅ Legacy test patterns (resource.TestCheckResourceAttr)
- ✅ Modern pattern adoption (statecheck.ExpectKnownValue)
- ✅ Missing drift detection tests
- ✅ Missing import tests
- ✅ Missing idempotency checks
- ✅ Required vs optional field coverage
- ✅ CRUD operation coverage

**Output**: Markdown report with executive summary, file-by-file analysis, and prioritized recommendations.

---

### 2. verify_compilation.sh - Fast Compilation Check

**Purpose**: Quickly verify test files compile without running tests. Useful for rapid validation after code changes.

**Usage**:
```bash
./verify_compilation.sh <test_directory>
```

**Example**:
```bash
./verify_compilation.sh ./internal/provider/
```

**What It Validates**:
- ✅ Go syntax correctness
- ✅ No compilation errors
- ✅ Import completeness
- ✅ Statistics (file count, test count)

**Output**: Success/failure with compilation statistics or detailed error messages.

**Time**: ~2-5 seconds (vs minutes for full test execution)

---

### 3. run_tests_parallel.sh - Parallel Test Execution (NEW)

**Purpose**: Run acceptance tests concurrently per file for significantly faster execution. Ideal for large test suites.

**Usage**:
```bash
./run_tests_parallel.sh [OPTIONS]
```

**Common Examples**:
```bash
# Run all acceptance tests (default: 4 concurrent files)
./run_tests_parallel.sh

# Run only resource tests with higher concurrency
./run_tests_parallel.sh --resources-only -c 8

# Run only data source tests
./run_tests_parallel.sh --data-sources-only

# Run tests matching specific pattern
./run_tests_parallel.sh -p "TestAccCMPartSoftwareImage"

# Run tests from specific file
./run_tests_parallel.sh -f resource_cmpart_softwareimage_test.go

# Verbose mode with detailed output
./run_tests_parallel.sh --verbose

# Custom directory and timeout
./run_tests_parallel.sh -d ./internal/provider -t 45m -c 6
```

**Options**:
- `-d, --dir DIR` - Test directory (default: ./internal/provider)
- `-p, --pattern PATTERN` - Test pattern to match (default: TestAcc)
- `-c, --concurrency N` - Max concurrent test files (default: 4)
- `-t, --timeout DURATION` - Timeout per test file (default: 30m)
- `-f, --file FILE` - Run only tests from specific file
- `--resources-only` - Run only resource tests
- `--data-sources-only` - Run only data source tests
- `--verbose` - Show detailed test output
- `--no-color` - Disable colored output
- `-h, --help` - Show help message

**Output**: Real-time progress with aggregated summary showing pass/fail counts, duration, and failed files.

**Performance**:
- Sequential: ~10-15 minutes for 15 test files
- Parallel (4 concurrent): ~2-4 minutes (4x-8x speedup)
- Parallel (8 concurrent): ~1-2 minutes (depends on system resources)

**Requirements**:
- GNU parallel (recommended) or xargs
- TF_ACC=1 environment variable
- BCM credentials (BCM_ENDPOINT, BCM_USERNAME, BCM_PASSWORD)

---

## Workflow Integration

### Typical Development Workflow

```bash
# 1. Analyze gaps in test coverage
python3 analyze_gap.py ./internal/provider/ --output gap_analysis.md

# 2. Make code changes to address gaps
# ... edit test files ...

# 3. Quick compilation check (fast feedback)
./verify_compilation.sh ./internal/provider/

# 4. Run tests in parallel (faster than sequential)
./run_tests_parallel.sh --verbose

# 5. Run specific tests that failed
./run_tests_parallel.sh -f resource_example_test.go --verbose
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
jobs:
  test:
    steps:
      - name: Verify Compilation
        run: ./scripts/verify_compilation.sh ./internal/provider/

      - name: Run Tests in Parallel
        run: ./scripts/run_tests_parallel.sh -c 8
        env:
          TF_ACC: 1
          BCM_ENDPOINT: ${{ secrets.BCM_ENDPOINT }}
          BCM_USERNAME: ${{ secrets.BCM_USERNAME }}
          BCM_PASSWORD: ${{ secrets.BCM_PASSWORD }}
```

---

## Performance Comparison

| Task | Sequential | Parallel (4) | Parallel (8) | Speedup |
|------|-----------|--------------|--------------|---------|
| 8 resource test files | ~12 min | ~3 min | ~2 min | 4-6x |
| 7 data source test files | ~8 min | ~2 min | ~1.5 min | 4-5x |
| Full suite (15 files) | ~20 min | ~5 min | ~3 min | 4-7x |

*Note: Actual times vary based on test complexity and system resources*

---

## Troubleshooting

### analyze_gap.py

**Issue**: `ModuleNotFoundError: No module named 're'`
- **Fix**: Using Python 3.6+ (re is built-in)

**Issue**: Report shows 0 files analyzed
- **Fix**: Verify test directory path is correct
- **Fix**: Ensure test files end with `_test.go`

### verify_compilation.sh

**Issue**: `Permission denied`
- **Fix**: `chmod +x verify_compilation.sh`

**Issue**: Compilation fails with missing imports
- **Fix**: Add required imports from error messages
- **Fix**: Check SKILL.md for required modern pattern imports

### run_tests_parallel.sh

**Issue**: `Permission denied`
- **Fix**: `chmod +x run_tests_parallel.sh`

**Issue**: `TF_ACC is not set`
- **Fix**: Export `TF_ACC=1` before running
- **Fix**: Set BCM credentials (BCM_ENDPOINT, BCM_USERNAME, BCM_PASSWORD)

**Issue**: Tests fail with "connection refused"
- **Fix**: Verify BCM_ENDPOINT is accessible
- **Fix**: Check network connectivity to BCM cluster

**Issue**: Slower than expected parallel execution
- **Fix**: Reduce concurrency if CPU-bound: `-c 2` or `-c 4`
- **Fix**: Increase concurrency if I/O-bound: `-c 8` or `-c 12`
- **Fix**: Check system resources (CPU, memory)

**Issue**: `parallel: command not found`
- **Fix**: Install GNU parallel: `apt-get install parallel` or `brew install parallel`
- **Fix**: Script will fallback to xargs automatically

---

## Dependencies

### analyze_gap.py
- Python 3.6+
- Standard library only (re, os, sys, argparse, datetime)

### verify_compilation.sh
- Bash 4.0+
- Go toolchain
- Standard Unix utilities (grep, wc, ls)

### run_tests_parallel.sh
- Bash 4.0+
- Go toolchain
- GNU parallel (recommended) or xargs
- Standard Unix utilities (find, grep, date, basename)

---

## Contributing

When adding new scripts:

1. **Add help text** - Include usage documentation in script header
2. **Add to README** - Document in this file
3. **Add to SKILL.md** - Update main skill documentation
4. **Add to workflow.md** - Update workflow reference
5. **Test thoroughly** - Verify with various inputs/edge cases
6. **Follow conventions** - Match style of existing scripts

---

## License

Copyright (c) HashiCorp, Inc.
SPDX-License-Identifier: MPL-2.0
