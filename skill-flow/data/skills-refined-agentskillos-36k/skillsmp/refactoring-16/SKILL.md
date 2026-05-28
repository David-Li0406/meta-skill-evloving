---
type: skill
name: Refactoring
description: Safe code refactoring with step-by-step approach
skillSlug: refactoring
phases: [E]
generated: 2026-01-20
status: filled
scaffoldVersion: "2.0.0"
---

# Refactoring Skill

## When to Use

Use this skill when:
- Improving code structure without changing functionality
- Eliminating code duplication
- Improving readability
- Optimizing performance through better structure

## Safe Refactoring Procedures

### 1. Extract Functions

**Before:**
```python
# Long function doing multiple things
def index_files(conn):
    # 50+ lines of logic
```

**After:**
```python
# Extract logical components
def process_pdf_file(filepath):
    """Process single PDF file."""
    
def save_document_to_db(cursor, doc_data):
    """Save document to database."""
```

### 2. Improve Function Organization

**Pattern from codebase:**
- Helper functions before main functions
- Related functions grouped together
- Clear separation of concerns

### 3. Reduce Duplication

**Example**: Classification logic extracted to separate function:
```python
def classify_document(filename, filepath):
    """Centralized classification logic."""
```

## Code Smell Detection

### Common Code Smells in Project

1. **Long Functions** (>50 lines)
   - Break into smaller functions
   - Example: `index_files()` could be split

2. **Repeated Patterns**
   - Extract to functions
   - Example: Error handling patterns

3. **Magic Numbers**
   - Extract to constants
   - Example: `MIN_TEXT_LENGTH = 10`

4. **Complex Conditionals**
   - Extract to named functions
   - Example: Classification logic

## Refactoring Patterns

### Extract Constants

**Before:**
```python
if len(text.strip()) < 10:
```

**After:**
```python
MIN_TEXT_LENGTH = 10
if len(text.strip()) < MIN_TEXT_LENGTH:
```

### Extract Helper Functions

**Pattern:**
- Small, focused functions
- Clear names
- Single responsibility

## Testing After Refactoring

**Required:**
- Run existing tests
- Verify functionality unchanged
- Test edge cases
- Validate performance

## Refactoring Checklist

- [ ] Functionality unchanged
- [ ] Tests pass after refactoring
- [ ] Code more readable
- [ ] No duplication introduced
- [ ] Performance maintained or improved
- [ ] Documentation updated if needed
