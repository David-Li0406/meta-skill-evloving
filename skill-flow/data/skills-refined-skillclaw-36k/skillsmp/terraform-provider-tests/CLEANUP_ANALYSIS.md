# Test Cleanup Analysis Feature

## Overview

The `analyze_gap.py` script now includes comprehensive test cleanup analysis to ensure tests properly clean up resources after execution.

## Cleanup Checks Added

### 1. **Robust CheckDestroy Verification**
Detects whether `CheckDestroy` functions actually verify deletion:
- ✅ Uses named CheckDestroy functions (e.g., `testAccCheckResourceDestroy`)
- ✅ Calls `verifyResourceDeleted()` helper
- ✅ Makes API cleanup calls (e.g., `client.CallJSONRPC...remove`)
- ✅ Contains verification logic (e.g., `if...still exists`)
- ⚠️ Warns if `CheckDestroy: nil` (no cleanup)
- ⚠️ Flags weak CheckDestroy (present but no verification logic)

### 2. **Cleanup-Friendly Naming**
Detects if tests use naming patterns that facilitate cleanup:
- ✅ `generateUniqueTestName()` - Unique timestamped names
- ✅ `citest-` prefix - Convention for CI test cleanup scripts
- ✅ Timestamp-based names - `test-resource-1234567890`
- ⚠️ Warns about hardcoded names (harder to clean up)

### 3. **External Resource Cleanup**
Detects if tests create external resources via API:
- ✅ Verifies cleanup when using `createTestBCMClient()`
- ⚠️ Warns if external resources created without robust cleanup

### 4. **CRUD Completeness**
- ⚠️ Warns if test creates resources but has no `CheckDestroy`

## Quality Score Impact

**Points Added:**
- +5 points for robust CheckDestroy
- +2 points for basic CheckDestroy (partial credit)
- +5 points for cleanup-friendly naming

**Penalties:**
- -3 points per cleanup issue (max -15 points)

## Report Sections

### Executive Summary
```markdown
**Cleanup Analysis:**
- **6/6** resources have robust cleanup verification
- **No cleanup issues detected** ✅
```

### Per-Test Analysis
```markdown
### resource_example_test.go
- **Quality score:** 100/100
- **Cleanup:** ✅ Robust
```

Or if issues exist:
```markdown
### resource_example_test.go
- **Quality score:** 75/100
- **Cleanup issues:** 2 ⚠️
  - Creates resources but missing CheckDestroy
  - Uses hardcoded resource names (harder to clean up)
```

### High Priority Recommendations
```markdown
**Test Cleanup Issues:**
- **`resource_example_test.go`**:
  - Creates resources but missing CheckDestroy
  - Uses hardcoded resource names
```

## Example Patterns

### Robust CheckDestroy
```go
func testAccCheckResourceDestroy(s *terraform.State) error {
    client := createTestBCMClient(&testing.T{})

    for _, rs := range s.RootModule().Resources {
        if rs.Type != "example_resource" {
            continue
        }

        deleted, err := verifyResourceDeleted(
            context.Background(),
            client,
            "Service",
            "getMethod",
            rs.Primary.ID,
            4, // retry count
        )

        if !deleted || err != nil {
            return fmt.Errorf("resource still exists: %s", rs.Primary.ID)
        }
    }

    return nil
}
```

### Cleanup-Friendly Naming
```go
// Option 1: Unique name generator
resourceName := generateUniqueTestName("test-resource")

// Option 2: citest prefix for automated cleanup
resourceName := fmt.Sprintf("citest-%s-%d", "resource", time.Now().Unix())
```

## Usage

```bash
# Generate cleanup analysis report
python3 analyze_gap.py ./internal/provider/ --output cleanup_report.md

# View cleanup issues
grep -A 10 "Cleanup Analysis" cleanup_report.md
```

## Benefits

1. **Prevent Resource Leaks**: Identify tests that don't clean up resources
2. **Improve CI/CD**: Ensure test environments don't accumulate orphaned resources
3. **Cost Optimization**: Reduce costs from leaked test resources
4. **Test Reliability**: Better test isolation through proper cleanup
5. **Compliance**: Meet requirements for automated cleanup in test environments

## Comparison: Before vs After

### Before
- ❌ No visibility into cleanup patterns
- ❌ Tests might leak resources
- ❌ No differentiation between robust and weak cleanup

### After
- ✅ Comprehensive cleanup analysis
- ✅ Identifies specific cleanup issues
- ✅ Grades cleanup robustness (Robust vs Basic)
- ✅ Provides actionable recommendations
- ✅ Tracks cleanup-friendly naming patterns
