# Example TDD Workflow: Bug Fix with Regression Test

This example demonstrates fixing a bug using TDD methodology.

## Bug Report

**Issue**: Nested label/goto doesn't work correctly when labels have the same name in different scopes.

**Reproduction**:
```lean
label result {
  let x = label result {
    goto(42, result)
  } in
  goto(x + 1, result)
}
```

**Expected**: `42` (inner goto takes precedence)
**Actual**: Error or wrong value

## Step 1: Reproduce Bug with Test (Red)

### Create Minimal Reproduction

```bash
# Create test that demonstrates the bug
cat > tests/golden/ir-eval/nested_label_same_name.ziku <<'EOF'
label result {
  let x = label result {
    goto(42, result)
  } in
  goto(x + 1, result)
}
EOF
```

### Add to Test Suite

```bash
# Edit tests/GoldenTest.lean
# Add "nested_label_same_name" to irEvalTests list
```

### Run Test (Should Fail)

```bash
lake test 2>&1 | grep -A 5 "nested_label_same_name"
```

**Expected Output**:
```
=== ir-eval tests ===
  ✗ nested_label_same_name
    Expected: 42
    Actual:   Error: ambiguous label 'result'
```

**Analysis**: Confirmed bug exists. Test fails as expected.

## Step 2: Understand the Bug

### Investigate Translation

```bash
# Check how label/goto is translated to IR
# Read Translate.lean
```

```lean
-- Current (buggy) implementation might be:
| .label pos name body =>
  -- Translates to μname.⟨body⟩
  -- Problem: name collision if nested
  translateToMu pos name body

| .goto pos expr name =>
  -- Jumps to label
  -- Problem: doesn't resolve scope
  translateToJump pos expr name
```

### Root Cause

Label names are not disambiguated in nested scopes. Inner label "result" and outer label "result" conflict.

## Step 3: Design Fix

**Solution**: Generate unique labels for nested scopes or implement proper scoping.

**Approach 1**: Alpha-rename labels to unique names
**Approach 2**: Use de Bruijn indices for labels
**Approach 3**: Keep scope stack and resolve at runtime

Choose **Approach 1** for simplicity.

## Step 4: Implement Fix (Green)

### Update Translation

Edit `Ziku/Translate.lean`:

```lean
-- Add unique name generation
def freshLabel (base : String) (st : TranslateState) : String × TranslateState :=
  let n := st.labelCounter
  let name := s!"{base}_{n}"
  let st' := { st with labelCounter := n + 1 }
  (name, st')

-- Update label translation
| .label pos name body => do
  let (uniqueName, st') ← freshLabel name <$> get
  set st'
  -- Use uniqueName instead of name
  translateWithUniqueLabel pos uniqueName body

-- Update goto translation to resolve to correct label
| .goto pos expr name => do
  -- Lookup name in scope
  let resolvedName ← resolveLabel name
  translateJump pos expr resolvedName
```

### Add Scope Tracking

```lean
-- Add to TranslateState
structure TranslateState where
  labelCounter : Nat := 0
  labelScope : List (String × String) := []  -- (original, unique)
  -- ... other fields

-- Push/pop scope when entering/exiting labels
def withLabelScope (original : String) (unique : String) (m : TranslateM α) : TranslateM α := do
  let st ← get
  set { st with labelScope := (original, unique) :: st.labelScope }
  let result ← m
  let st ← get
  set { st with labelScope := st.labelScope.tail! }
  pure result
```

### Run Test (Should Pass)

```bash
lake test
```

**Expected Output**:
```
=== ir-eval tests ===
  Created golden file: tests/golden/ir-eval/nested_label_same_name.golden
  ✓ nested_label_same_name
```

## Step 5: Add More Regression Tests

### Test Edge Cases

```bash
# Test triple nesting
cat > tests/golden/ir-eval/nested_label_triple.ziku <<'EOF'
label result {
  label result {
    label result {
      goto(42, result)
    }
  }
}
EOF

# Test different names (should still work)
cat > tests/golden/ir-eval/nested_label_different_names.ziku <<'EOF'
label outer {
  label inner {
    goto(42, inner)
  }
}
EOF

# Test goto to outer label
cat > tests/golden/ir-eval/nested_label_goto_outer.ziku <<'EOF'
label outer {
  let x = label inner {
    if 1 == 1 then
      goto(42, outer)
    else
      goto(0, inner)
  } in
  x + 1
}
EOF

# Add all to irEvalTests in GoldenTest.lean
```

### Run All Tests

```bash
lake test
```

**Expected Output**: All new tests should pass.

## Step 6: Verify No Regressions

### Run Full Test Suite

```bash
# Run all tests to ensure no existing tests broke
lake test
```

**Check for**:
- All parser tests still pass
- All infer tests still pass
- All ir-eval tests still pass (including old label tests)

If any existing test fails:
```bash
# Example: label_simple test now fails
  ✗ label_simple
    Expected: 42
    Actual:   43

# This means the fix broke something
# Debug and fix the implementation
# Re-run tests until all pass
```

## Step 7: Refactor (If Needed)

### Review Code Quality

```bash
# Check for duplication
# Check for clarity
# Check for edge cases
```

### Example Refactoring

Before:
```lean
-- Scattered label handling logic
def translateLabel := ...
def translateGoto := ...
def resolveName := ...
```

After:
```lean
-- Centralized label handling
namespace LabelScope
  def fresh := ...
  def push := ...
  def pop := ...
  def resolve := ...
end LabelScope

def translateLabel := LabelScope.push ...
def translateGoto := LabelScope.resolve ...
```

### Run Tests After Refactoring

```bash
lake test  # Should still be all green
```

## Step 8: Document and Commit

### Update Documentation

```lean
-- Add comment explaining the fix
-- In Translate.lean:
/--
Translate label expression with unique name generation.
Labels are alpha-renamed to avoid scope conflicts in nested labels.
See tests/golden/ir-eval/nested_label_same_name.ziku for example.
-/
def translateLabel := ...
```

### Commit Changes

```bash
# Verify tests pass
lake test

# Stage changes
git add tests/golden/ir-eval/nested_label_*.ziku
git add tests/GoldenTest.lean
git add Ziku/Translate.lean

# Commit with reference to issue
git commit -m "fix(translate): resolve nested label scope conflicts

Alpha-rename labels to unique names to prevent conflicts
when labels with the same name are nested.

Before: Inner label 'result' would conflict with outer 'result'
After: Each label gets unique name (result_0, result_1, etc.)

Fixes: nested label/goto bug
Tests: Added 4 regression tests for nested labels

🤖 Generated with Claude Code

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

## Verification

### Test the Fix Manually

```bash
# Create a test file
cat > /tmp/test_nested_label.ziku <<'EOF'
label result {
  let x = label result {
    goto(42, result)
  } in
  goto(x + 1, result)
}
EOF

# Run with REPL or eval
lake exe ziku /tmp/test_nested_label.ziku

# Expected output: 42
```

### Automated Verification

```bash
# The test suite now prevents regression
lake test

# If anyone breaks this in future:
# The nested_label_same_name test will fail
# Clear indication of what broke and why
```

## Summary

This workflow demonstrated:

1. **Reproduce First**: Created failing test before fix
2. **Red Phase**: Confirmed test fails with bug
3. **Understand**: Investigated root cause
4. **Minimal Fix**: Implemented simplest solution
5. **Green Phase**: Verified test passes
6. **Edge Cases**: Added more regression tests
7. **No Regressions**: Verified existing tests still pass
8. **Refactor**: Improved code structure
9. **Document**: Added comments and commit message
10. **Protect**: Tests now prevent this bug from recurring

**Key Principle**: Never fix a bug without a test that would have caught it.

**Value**: Bug fixed + 4 regression tests + improved code structure
