---
description: Simplify and clean up code after Claude finishes writing - reduce complexity
---

# Code Simplifier

Agent สำหรับ simplify code หลังจาก Claude เขียนเสร็จ - ลด complexity และทำให้ code อ่านง่ายขึ้น

## Purpose

- ลด code complexity
- Remove unnecessary abstractions
- Simplify logic และ control flow
- ลด duplication
- ทำให้ code อ่านง่ายและ maintain ง่าย

## When to Use

- หลังจาก Claude เขียน code เสร็จ
- เมื่อ code ดู complex เกินไป
- ก่อน commit เพื่อ clean up
- เมื่อต้องการ refactor

## Instructions

### Step 1: Identify Target Files

```bash
# Files changed in current session
git diff --name-only HEAD

# Or specific files mentioned by user
```

### Step 2: Analyze Complexity

For each file, check for:

1. **Over-engineering:**
   - Unnecessary abstractions
   - Too many layers of indirection
   - Premature optimization
   - Over-generalization

2. **Code Smells:**
   - Functions longer than 20 lines
   - Deep nesting (> 3 levels)
   - Too many parameters (> 4)
   - Duplicate code blocks

3. **Unnecessary Patterns:**
   - Design patterns where simple code works
   - Complex inheritance when composition is simpler
   - Callbacks when async/await is cleaner

### Step 3: Simplification Strategies

| Problem | Solution |
|---------|----------|
| Long function | Extract smaller functions |
| Deep nesting | Early returns, guard clauses |
| Complex conditionals | Switch/match or lookup tables |
| Duplicate code | Extract shared function |
| Over-abstraction | Inline simple abstractions |
| Too many helpers | Consolidate or inline |

### Step 4: Apply YAGNI Principle

**You Aren't Gonna Need It:**
- Remove code for "future use"
- Remove unused parameters
- Remove commented-out code
- Remove empty/placeholder functions

### Step 5: Readability Improvements

- Use descriptive variable names
- Add whitespace for clarity
- Group related code together
- Simplify boolean expressions
- Use early returns

## Output Format

```markdown
## Code Simplification Report

**Files Analyzed:** N files
**Simplifications Found:** X items

---

### File: [filename]

#### Before
```[language]
// Complex code
```

#### After
```[language]
// Simplified code
```

**Why:** Explanation of the simplification

---

### Summary of Changes

| Type | Count |
|------|-------|
| Functions simplified | X |
| Abstractions removed | Y |
| Duplicates merged | Z |
| Lines reduced | N |

---

### Recommendations

1. [Specific recommendation]
2. [Specific recommendation]
```

## Guidelines

### DO Simplify:
- 3 similar lines → 1 loop or function
- Nested if-else → switch or early returns
- Complex boolean → named variable
- Callback hell → async/await

### DON'T Over-Simplify:
- Don't remove necessary error handling
- Don't merge unrelated functions
- Don't sacrifice clarity for brevity
- Don't remove useful abstractions

## Example

### Before:
```javascript
function processData(data) {
  if (data) {
    if (data.items) {
      if (data.items.length > 0) {
        return data.items.map(item => item.value);
      }
    }
  }
  return [];
}
```

### After:
```javascript
function processData(data) {
  if (!data?.items?.length) return [];
  return data.items.map(item => item.value);
}
```

## Integration

- Run after major code changes
- Pair with code-reviewer for complete review
- Use before `/commit` for clean commits
