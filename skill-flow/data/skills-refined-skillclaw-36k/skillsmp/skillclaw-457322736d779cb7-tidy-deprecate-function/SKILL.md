---
name: tidy-deprecate-function
description: Use this skill when deprecating R functions or parameters, ensuring all necessary changes are made consistently, including adding lifecycle warnings, updating documentation, and modifying tests.
---

# Deprecate functions and function arguments

This skill guides you through the complete process of deprecating a function or parameter in R.

## Overview

1. Add a deprecation warning using `lifecycle::deprecate_warn()`.
2. Silence deprecation warnings in existing tests.
3. Add a lifecycle badge to documentation.
4. Add a bullet point to NEWS.md.
5. Create a test for the deprecation warning.

## Workflow

### Step 1: Determine deprecation version

Read the current version from DESCRIPTION and calculate the deprecation version:

- Current version format: `MAJOR.MINOR.PATCH.9000` (development).
- Deprecation version: Next minor release `MAJOR.(MINOR+1).0`.
- Example: If the current version is `2.5.1.9000`, the deprecation version is `2.6.0`.

### Step 2: Add `lifecycle::deprecate_warn()` call

Add the deprecation warning to the function:

```r
# For a deprecated function:
function_name <- function(...) {
  lifecycle::deprecate_warn("X.Y.0", "function_name()", "replacement_function()")
  # rest of function
}

# For a deprecated parameter:
function_name <- function(param1, deprecated_param = deprecated()) {
  if (lifecycle::is_present(deprecated_param)) {
    lifecycle::deprecate_warn("X.Y.0", "function_name(deprecated_param)")
  }
  # rest of function
}
```

Key points:

- The first argument is the deprecation version string (e.g., "2.6.0").
- The second argument describes what is deprecated (e.g., "function_name(param)").
- The optional third argument suggests a replacement.
- Use `lifecycle::is_present()` to check if a deprecated parameter was supplied.

### Step 3: Update tests

Find all existing tests that use the deprecated function or parameter and silence lifecycle warnings. Add at the beginning of test blocks that use the deprecated feature:

```r
test_that("existing test with deprecated feature", {
  withr::local_options(lifecycle_verbosity = "quiet")

  # existing test code
})
```

Then add a new test to verify the deprecation message in the appropriate test file (usually `tests/testthat/test-{name}.R`):

```r
test_that("function_name(deprecated_param) is deprecated", {
  expect_snapshot(. <- function_name(deprecated_param = "value"))
})
```