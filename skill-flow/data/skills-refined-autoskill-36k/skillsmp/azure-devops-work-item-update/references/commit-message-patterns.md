# Commit Message Patterns for Work Item Extraction

Supported commit message formats for extracting Azure DevOps work item IDs.

---

## Supported Patterns

### Pattern 1: Conventional Commits with Work Item

**Format**: `<type>(#<id>): <description>`

**Examples**:
```
feat(#1234): Implement ConfigManager singleton
fix(#5678): Resolve null pointer exception in auth
docs(#9012): Update API documentation
refactor(#3456): Extract duplicate code into utility
test(#7890): Add unit tests for UserService
```

**Extraction**: Captures `1234`, `5678`, `9012`, etc.

**Recommended**: ✅ Yes - Clear, standard, includes context

---

### Pattern 2: Work Item at End

**Format**: `<description> (#<id>)`

**Examples**:
```
Implement ConfigManager singleton (#1234)
Fix null pointer exception in auth (#5678)
Update API documentation (#9012)
```

**Extraction**: Captures `1234`, `5678`, `9012`, etc.

**Recommended**: ✅ Yes - Common GitHub/DevOps style

---

### Pattern 3: Work Item with Brackets

**Format**: `<description> [#<id>]`

**Examples**:
```
Implement ConfigManager singleton [#1234]
Fix authentication bug [#5678]
```

**Extraction**: Captures `1234`, `5678`, etc.

**Recommended**: ⚠️ Okay - Less common but supported

---

### Pattern 4: Work Item at Beginning

**Format**: `#<id>: <description>`

**Examples**:
```
#1234: Implement ConfigManager singleton
#5678: Fix authentication bug
```

**Extraction**: Captures `1234`, `5678`, etc.

**Recommended**: ⚠️ Okay - Simple but lacks type information

---

### Pattern 5: Bare Work Item Reference

**Format**: `<description> #<id> <more description>`

**Examples**:
```
Implement #1234 ConfigManager singleton
Fix authentication #5678 null pointer issue
```

**Extraction**: Captures first number after `#`

**Recommended**: ❌ Not recommended - Ambiguous, could match issue numbers

---

## Multiple Work Items

If commit affects multiple work items:

**Recommended Format**:
```
feat(#1234,#5678): Implement shared authentication module

Updates both task #1234 and user story #5678
```

**Extraction**: Currently extracts only first work item (`1234`)

**Note**: For multiple work items, consider:
- Making separate commits for each work item
- Using commit body to reference additional work items
- Running batch update script to handle multiple references

---

## Commit Body References

Work items can also be referenced in commit body:

```
feat(#1234): Implement ConfigManager singleton

Implements singleton pattern as specified in ADR-018.

Related work items:
- Fixes #5678
- Closes #9012
- Relates to #3456
```

**Note**: Scripts currently extract from subject line only. Commit body extraction can be added if needed.

---

## Best Practices

### 1. Be Consistent

Pick one format and use it across the team:

**Good** (Consistent):
```
feat(#1234): Implement feature A
feat(#5678): Implement feature B
fix(#9012): Fix bug in feature A
```

**Bad** (Inconsistent):
```
feat(#1234): Implement feature A
Implement feature B (#5678)
#9012: Fix bug in feature A
```

---

### 2. Include Work Item ID in Every Commit

**Good**:
```
feat(#1234): Add validation to user input
test(#1234): Add tests for input validation
docs(#1234): Update validation documentation
```

All commits reference work item, enabling full traceability.

**Bad**:
```
Add validation to user input
Add tests
Update docs
```

No work item references, can't trace commits to work items.

---

### 3. Use Conventional Commit Types

**Recommended Types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style changes (formatting, etc.)
- `refactor` - Code refactoring
- `test` - Adding/updating tests
- `chore` - Build process, dependencies, etc.

**Example**:
```
feat(#1234): Implement user authentication
fix(#5678): Resolve session timeout issue
refactor(#9012): Extract shared validation logic
test(#3456): Add integration tests for API
```

---

### 4. Be Descriptive

**Good**:
```
feat(#1234): Implement ConfigManager as singleton pattern with thread safety
```

Clear what was done, easy to understand.

**Bad**:
```
feat(#1234): Update code
```

Vague, doesn't explain what changed.

---

## Git Hooks for Enforcement

### Commit Message Hook

Create `.git/hooks/commit-msg`:

```bash
#!/bin/bash

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# Check for work item reference
if ! echo "$commit_msg" | grep -qE '\(#[0-9]+\)|#[0-9]+|\[#[0-9]+\]'; then
    echo "Error: Commit message must include work item reference"
    echo "Examples:"
    echo "  feat(#1234): Description"
    echo "  Description (#1234)"
    echo "  #1234: Description"
    exit 1
fi

echo "✓ Work item reference found"
```

Make executable:
```bash
chmod +x .git/hooks/commit-msg
```

---

## Extraction Examples

### Example 1: Conventional Commit

**Input**:
```
feat(#1234): Implement ConfigManager singleton
```

**Extraction**:
```json
{
  "work_item_id": 1234,
  "commit_type": "feat",
  "description": "Implement ConfigManager singleton"
}
```

---

### Example 2: Work Item at End

**Input**:
```
Implement ConfigManager singleton (#1234)
```

**Extraction**:
```json
{
  "work_item_id": 1234,
  "description": "Implement ConfigManager singleton"
}
```

---

### Example 3: Multiple References (First Only)

**Input**:
```
feat(#1234): Implement shared module for #5678
```

**Extraction**:
```json
{
  "work_item_id": 1234,
  "note": "Additional reference #5678 in description"
}
```

---

## Testing Patterns

Test your commit messages:

```bash
# Test extraction
python scripts/extract_work_item_from_commit.py \
  --commit-message "feat(#1234): Test message"

# Expected output: work_item_id: 1234
```

---

## Migration from Other Systems

### From Jira

**Jira Format**: `ABC-1234: Description`

**Convert to**:
```
feat(#1234): Description [ABC-1234]
```

Include original Jira reference in brackets for reference.

---

### From GitHub Issues

**GitHub Format**: `Fixes #1234`

**Convert to**:
```
fix(#1234): Description

Fixes GitHub issue #1234
```

Reference GitHub issue in commit body.

---

**Last Updated**: 2025-01-21
