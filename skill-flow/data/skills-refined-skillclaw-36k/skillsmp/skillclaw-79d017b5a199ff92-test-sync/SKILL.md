---
name: test-sync
description: Use this skill when you need to maintain alignment between your test files and source code, detecting orphaned tests, obsolete assertions, and test-code misalignment.
---

# Skill body

## Purpose

Maintain alignment between test files and source code. Detect orphaned tests (code deleted but tests remain), missing tests, and implementation-coupled tests. Based on UTRefactor research showing automated test maintenance can achieve 89% smell reduction.

## Research Foundation

| Concept | Source | Reference |
|---------|--------|-----------|
| Test Refactoring | UTRefactor (ACM 2024) | [89% smell reduction](https://dl.acm.org/doi/10.1145/3715750) |
| Test Smells | Meszaros (2007) | "xUnit Test Patterns" |
| Test-Code Traceability | IEEE TSE | Test maintenance research |

## When This Skill Applies

- After major refactoring
- During test suite health audits
- When tests fail for deleted code
- Before releases (cleanup validation)
- When test count seems disconnected from codebase

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Find orphaned tests" | Detect tests for deleted code |
| "Sync tests with code" | Full alignment analysis |
| "Are my tests up to date?" | Test-code sync check |
| "Clean up test suite" | Find removable tests |
| "Test coverage gaps" | Find missing tests |

## Sync Analysis Types

### 1. Orphaned Test Detection

Tests that reference deleted or renamed code:

```python
def find_orphaned_tests(project_dir):
    """Find tests for code that no longer exists"""
    orphans = []

    for test_file in glob(f"{project_dir}/test/**/*.test.ts"):
        # Extract tested module from import/path
        tested_module = infer_tested_module(test_file)

        if not exists(tested_module):
            orphans.append({
                "test_file": test_file,
                "expected_source": tested_module,
                "status": "source_deleted"
            })

        # Check for unused test helpers
        for helper in extract_test_helpers(test_file):
            if not is_used_in_assertions(test_file, helper):
                orphans.append({
                    "test_file": test_file,
                    "item": helper,
                    "status": "unused_helper"
                })

    return orphans
```

### 2. Missing Test Detection

Source files without corresponding tests:

```python
def find_missing_tests(project_dir):
    """Find source files without tests"""
    missing = []

    for source_file in glob(f"{project_dir}/src/**/*.py"):
        test_file = f"test_{source_file.split('/')[-1]}"
        if not exists(test_file):
            missing.append({
                "source_file": source_file,
                "expected_test": test_file,
                "status": "missing_test"
            })

    return missing
```