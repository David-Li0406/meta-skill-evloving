---
name: code-refactoring
description: Use this skill when you need to improve code quality, maintainability, or design without changing functionality, such as when refactoring, cleaning code, or addressing technical debt.
---

# Refactoring Skill

Systematic guidance for improving code quality, maintainability, and design without changing functionality.

## Overview

This skill provides refactoring strategies for:
- **Extracting methods/functions** for better organization
- **Removing code duplication** (DRY principle)
- **Simplifying complex logic** and reducing cyclomatic complexity
- **Improving naming** and readability
- **Applying design patterns** appropriately
- **Reducing technical debt** while maintaining functionality

## When This Skill Applies

This skill activates when:
- Code is difficult to understand or maintain
- Functions/methods are too long or complex
- Similar code appears in multiple places
- Naming is unclear or inconsistent
- Design patterns could improve structure
- Technical debt needs to be reduced
- Performance optimizations are needed

## Refactoring Principles

### Core Rules

1. **Preserve Functionality**: Refactoring should NOT change behavior.
2. **Small Steps**: Make incremental changes with tests between each.
3. **Test Coverage**: Ensure tests pass before and after refactoring.
4. **Commit Often**: Save working state frequently.
5. **Document Why**: Explain reasons for significant changes.

### Red, Green, Refactor

```bash
# 1. Ensure tests pass (GREEN)
cargo test
npm test

# 2. Make small refactoring change
# 3. Run tests again (still GREEN)
cargo test
npm test

# 4. Commit if tests pass
git commit -m "refactor: extract material validation logic"

# Repeat
```

## Common Code Smells & Refactorings

### 1. Long Method/Function

**Smell:**
```rust
// ❌ 200+ line function doing multiple things
pub async fn create_formula_with_materials(
    &self,
    dto: CreateFormulaDto,
) -> Result<Formula> {
    // Function logic...
}
```

**Refactor - Extract Methods:**
```rust
// ✅ Broken into focused functions
pub async fn create_formula_with_materials(
    &self,
    dto: CreateFormulaDto,
) -> Result<Formula> {
    self.validate_formula_dto(&dto)?;
    self.check_duplicate_formula(&dto.name).await?;
    self.validate_materials(&dto.materials)?;
    self.insert_formula_with_materials(dto).await
}
```

### 2. Code Duplication (DRY Violation)

**Smell:**
```typescript
// ❌ Same validation logic repeated
function validateFormulaName(name: string): void {
    // Validation logic...
}

function validateMaterialName(name: string): void {
    // Validation logic...
}
```

**Refactor - Extract Common Function:**
```typescript
// ✅ Reusable validation function
function validateName(name: string, rule: ValidationRule): boolean {
    // Validation logic...
}
```

### 3. Complex Conditional Logic

**Smell:**
```rust
// ❌ Nested conditionals
pub async fn get_formula_materials(&self, formula_id: i64) -> Result<Vec<Material>> {
    // Logic...
}
```

**Refactor - Early Returns (Guard Clauses):**
```rust
// ✅ Flat structure with guard clauses
pub async fn get_formula_materials(&self, formula_id: i64) -> Result<Vec<Material>> {
    // Guard clauses
}
```

### 4. Magic Numbers/Strings

**Smell:**
```rust
// ❌ Magic numbers
pub fn calculate_discount(price: f64) -> f64 {
    // Logic...
}
```

**Refactor - Named Constants:**
```rust
// ✅ Self-documenting constants
pub const DISCOUNT_THRESHOLD_HIGH: f64 = 1000.0;
// Logic...
```

### 5. Large Interface/Class

**Smell:**
```rust
// ❌ God object doing too much
pub struct FormulaService {
    // Fields...
}
```

**Refactor - Single Responsibility:**
```rust
// ✅ Focused services with clear responsibilities
pub struct FormulaService {
    // Fields...
}
```

### 6. Feature Envy

**Smell:**
```rust
// ❌ Method that should be on another object
impl Formula {
    // Logic...
}
```

**Refactor - Move Method:**
```rust
// ✅ Method belongs on Material
impl Material {
    // Logic...
}
```

## Refactoring Workflow

### Step 1: Identify the Smell

Ask yourself:
- What makes this code hard to understand?
- What would make it easier to maintain?
- Is there duplication?
- Are there too many responsibilities?
- Is the naming unclear?

### Step 2: Write Tests (If None Exist)

```rust
#[test]
fn test_current_behavior() {
    // Test logic...
}
```

### Step 3: Apply Refactoring (Small Steps)

1. Make one small change.
2. Run tests.
3. If tests pass, commit.
4. Repeat.

### Step 4: Verify Behavior

```bash
# Run all tests
cargo test --all
npm test
```

### Step 5: Update Documentation

```markdown
## Refactoring Notes

### Date: Extract Validation Logic

**Problem**: Function was too long with mixed concerns.

**Solution**: Extracted validation logic into separate functions.

**Files Changed**: 
- `src/formula/service.rs`
```

## Refactoring Checklist

### Before Refactoring
- [ ] Tests exist and pass.
- [ ] Git working directory is clean.
- [ ] Understand current behavior.
- [ ] Have identified specific improvement.

### During Refactoring
- [ ] Make small, incremental changes.
- [ ] Run tests after each change.
- [ ] Commit often.
- [ ] Don't change behavior yet.

### After Refactoring
- [ ] All tests pass.
- [ ] Code is more readable.
- [ ] Duplication reduced.
- [ ] Complexity reduced.
- [ ] Documentation updated.

## Quick Reference

### Common Extract Refactorings

| Refactoring | Description | Shortcut |
|-------------|-------------|----------|
| Extract Method | Move code to new method/function | IDE: Extract function |
| Extract Variable | Complex expression → named variable | IDE: Introduce variable |
| Extract Constant | Magic value → named constant | Find/Replace |
| Inline Method | Simple method → inline it | IDE: Inline function |
| Rename | Better name for clarity | IDE: Rename symbol |
| Extract Interface | Common methods → interface | IDE: Extract interface |

### Rust-Specific Refactorings

```rust
// Use ? instead of match
result?
```

### React-Specific Refactorings

```typescript
// Use custom hooks for state logic
// Use React.memo for expensive components
// Use useMemo for expensive calculations
// Use useCallback for stable function references
// Extract components to reduce prop drilling
```