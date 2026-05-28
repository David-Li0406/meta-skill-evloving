# Bug Fix Test Template

Use this template when creating regression tests for bug fixes.

## Test File Structure

```
[test-directory]/
└── [ticket-id].test.[ext]   # e.g., EMS-1234.test.ts
```

## Template

```typescript
/**
 * Regression tests for: [TICKET-ID]
 * Bug: [Brief description]
 * Root Cause: [From verified-rca.md]
 * 
 * These tests ensure the bug does not recur.
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('[TICKET-ID]: [Bug title]', () => {
  // ============================================
  // SETUP
  // ============================================
  
  beforeEach(() => {
    // Set up conditions that existed when bug occurred
  });
  
  afterEach(() => {
    // Clean up
  });

  // ============================================
  // REGRESSION TEST (Required)
  // ============================================
  
  it('should not [bug behavior]', () => {
    // Arrange: Recreate the exact bug condition
    // From bug-context.md "Steps to Reproduce"
    
    // Act: Trigger the bug scenario
    
    // Assert: Verify correct behavior
    // This assertion should FAIL on old code, PASS on fixed code
  });

  // ============================================
  // EDGE CASES (From RCA)
  // ============================================
  
  it('should handle [edge case 1 from RCA]', () => {
    // Related scenario identified in root cause analysis
  });
  
  it('should handle [edge case 2 from RCA]', () => {
    // Another related scenario
  });

  // ============================================
  // BOUNDARY CONDITIONS
  // ============================================
  
  it('should handle [boundary condition]', () => {
    // Test limits and boundaries
  });
});
```

## Checklist Before Committing

- [ ] Test file is in correct location
- [ ] Test describes the bug ticket ID
- [ ] Regression test uses exact reproduction steps
- [ ] Edge cases from RCA are covered
- [ ] All tests pass with fix applied
- [ ] Test names are descriptive
- [ ] No flaky/timing-dependent assertions
