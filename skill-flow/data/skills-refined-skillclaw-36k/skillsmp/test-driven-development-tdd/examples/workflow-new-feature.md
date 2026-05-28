# Example TDD Workflow: Adding a New Feature

This example demonstrates adding a `for` loop construct to Ziku using TDD.

## Feature Specification

Add a `for` loop with syntax:
```
for i in range(0, 10) do
  i * 2
```

## Phase 1: Parser Tests (Red-Green-Refactor)

### Red: Write Failing Parser Test

```bash
# Create test file
cat > tests/golden/parser/for_loop_simple.ziku <<'EOF'
for i in range(0, 10) do
  i * 2
EOF

# Add to GoldenTest.lean
# In parserTests list, add: "for_loop_simple"

# Run tests - should fail with parse error
lake test
```

**Expected Output**:
```
=== parser tests ===
  ✗ for_loop_simple: Parse error: unexpected token 'for'
```

### Green: Implement Parser

Edit `Ziku/Parser.lean`:

```lean
-- Add to expression parser
def parseFor : Parser Expr := do
  skipWhitespace
  _ ← string "for"
  skipWhitespace
  ident ← parseIdent
  skipWhitespace
  _ ← string "in"
  skipWhitespace
  iter ← parseExpr
  skipWhitespace
  _ ← string "do"
  skipWhitespace
  body ← parseExpr
  let pos ← getPos
  -- Desugar to match/codata or keep as For node
  pure (Expr.for_ pos ident iter body)

-- Add For variant to Expr type in Ziku/Surface/Syntax.lean
-- | for_ (pos : SourcePos) (var : Ident) (iter : Expr) (body : Expr)
```

```bash
# Run tests - should pass and generate golden
lake test
```

**Expected Output**:
```
=== parser tests ===
  Created golden file: tests/golden/parser/for_loop_simple.golden
  ✓ for_loop_simple
```

### Refactor: Add More Parser Tests

```bash
# Test with nested for loops
cat > tests/golden/parser/for_loop_nested.ziku <<'EOF'
for i in range(0, 3) do
  for j in range(0, 3) do
    i * j
EOF

# Test with complex body
cat > tests/golden/parser/for_loop_complex.ziku <<'EOF'
for x in items do
  let y = x * 2 in
  y + 1
EOF

# Add to GoldenTest.lean: "for_loop_nested", "for_loop_complex"
lake test  # All should pass
```

## Phase 2: Type Inference Tests (Red-Green-Refactor)

### Red: Write Failing Inference Test

```bash
# Create inference test
cat > tests/golden/infer/for_loop_basic.ziku <<'EOF'
for i in range(0, 10) do
  i + 1
EOF

# Add to GoldenTest.lean inferTests: "for_loop_basic"
lake test
```

**Expected Output**:
```
=== infer tests ===
  ✗ for_loop_basic: Inference not implemented for For
```

### Green: Implement Type Inference

Edit `Ziku/Infer.lean`:

```lean
-- Add case for For
| .for_ pos var iter body => do
  -- Infer type of iterator expression
  iterTy ← infer iter
  -- Check iterator is iterable (for now, assume List or Range type)
  -- Bind variable with element type
  -- Infer body type
  -- Return unit or collection type
  -- (Implementation details depend on design)
  pure (Ty.unit pos)  -- Simplified
```

```bash
lake test  # Should pass
```

### Refactor: Add More Inference Tests

```bash
# Test type errors
cat > tests/golden/infer/for_loop_type_error.ziku <<'EOF'
for i in 42 do
  i + 1
EOF

# Add to inferTests: "for_loop_type_error"
lake test  # Should show type error in golden
```

## Phase 3: IR Evaluation Tests (Red-Green-Refactor)

### Red: Write Failing Evaluation Test

```bash
# Create evaluation test
cat > tests/golden/ir-eval/for_loop_sum.ziku <<'EOF'
let sum = 0 in
for i in range(0, 5) do
  sum + i
EOF

# Add to GoldenTest.lean irEvalTests: "for_loop_sum"
lake test
```

**Expected Output**:
```
=== ir-eval tests ===
  ✗ for_loop_sum: Translation error: For not implemented
```

### Green: Implement Translation and Evaluation

Edit `Ziku/Translate.lean`:

```lean
-- Add case for For
| .for_ pos var iter body =>
  -- Translate to recursive function or fold
  -- (Implementation depends on design)
  -- Simplified: desugar to fold
  translateFold pos var iter body
```

Edit `Ziku/IR/Eval.lean` if needed for new IR constructs.

```bash
lake test  # Should pass with correct result
```

**Expected Output**:
```
=== ir-eval tests ===
  Created golden file: tests/golden/ir-eval/for_loop_sum.golden
  ✓ for_loop_sum
```

### Refactor: Add More Evaluation Tests

```bash
# Test with accumulation
cat > tests/golden/ir-eval/for_loop_product.ziku <<'EOF'
let product = 1 in
for i in range(1, 6) do
  product * i
EOF

# Test with nested loops
cat > tests/golden/ir-eval/for_loop_nested_sum.ziku <<'EOF'
let sum = 0 in
for i in range(0, 3) do
  for j in range(0, 3) do
    sum + (i * j)
EOF

# Add to irEvalTests
lake test  # All should pass
```

## Phase 4: Final Refactoring

### Review Implementation

```bash
# Check all tests pass
lake test

# Review code for:
# - Duplication (extract common patterns)
# - Naming (clear variable names)
# - Comments (remove obvious ones, keep non-obvious)
# - Error messages (helpful and specific)
```

### Example Refactoring

Before:
```lean
-- Duplication in parseFor, parseWhile, parseMatch
def parseFor := do
  skipWhitespace
  _ ← string "for"
  skipWhitespace
  -- ...

def parseWhile := do
  skipWhitespace
  _ ← string "while"
  skipWhitespace
  -- ...
```

After:
```lean
-- Extract common pattern
def parseKeyword (kw : String) : Parser Unit := do
  skipWhitespace
  _ ← string kw
  skipWhitespace

def parseFor := do
  parseKeyword "for"
  ident ← parseIdent
  parseKeyword "in"
  -- ...
```

```bash
# Test after refactoring
lake test  # Should still be all green
```

## Commit

```bash
# Verify all tests pass
lake test

# Check git status
git status

# Commit with conventional commit message
git add .
git commit -m "feat(syntax): add for loop construct

- Add for loop parsing
- Implement type inference for loops
- Add IR translation and evaluation
- Include comprehensive test coverage

Tests: 12 new golden tests across parser, infer, ir-eval"
```

## Summary

This workflow demonstrated:

1. **Three-phase TDD**: Parser → Inference → Evaluation
2. **Red-Green-Refactor**: Each phase followed the cycle
3. **Incremental Progress**: Small steps with fast feedback
4. **Test Coverage**: Edge cases and error conditions
5. **Continuous Refactoring**: Cleaned code while tests stay green
6. **Golden Tests**: Leveraged automatic baseline generation

Test distribution: 4 parser + 3 infer + 5 ir-eval = 12 tests.
