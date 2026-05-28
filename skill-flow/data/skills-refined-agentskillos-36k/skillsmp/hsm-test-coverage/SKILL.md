---
name: HSM Test Coverage
description: Analyze test coverage and identify gaps
version: 1.0.0
tags: [hsm, testing, coverage]
---

# HSM Test Coverage

Test coverage analysis for HSM modules.

## Usage

```
/hsm-coverage [module-number]
```

## What You Do

1. **Run Coverage:**
   ```bash
   cargo tarpaulin --all --out Lcov
   ```
   Or for specific module:
   ```bash
   cd crates/<module> && cargo tarpaulin --out Lcov
   ```

2. **Parse Results:**
   Extract:
   - Line coverage %
   - Branch coverage %
   - Uncovered lines/functions

3. **Compare Against Target:**
   Target: >90% line coverage per module

4. **Identify Gaps:**
   Report uncovered code paths with suggestions:
   ```
   Uncovered:
     src/asymmetric/rsa.rs:145-152   - Error handling for invalid key

   Suggested:
     - test_rsa_invalid_key_size()
     - test_rsa_error_recovery()
   ```

5. **Recommend Test Types:**
   - Unit tests for basic functionality
   - Property tests for invariants
   - Fuzz tests for robustness
   - Integration tests for workflows

## Target Coverage

All modules: >90% line coverage
