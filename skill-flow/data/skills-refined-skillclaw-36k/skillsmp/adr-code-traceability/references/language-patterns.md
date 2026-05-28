**Skill**: [ADR Code Traceability](../SKILL.md)

# Language-Specific ADR Reference Patterns

Standard patterns for referencing ADRs in code across different programming languages.

## Reference Format

**Standard**: `ADR: {adr-id}`

**Path Derivation**: From `ADR: 2025-12-01-my-feature` → `/docs/adr/2025-12-01-my-feature.md`

---

## Python

### New File (Module Header)

```python
"""
Module description here.

ADR: 2025-12-01-my-feature
"""

import ...
```

### Inline Comment

```python
# ADR: 2025-12-01-my-feature - reason for this choice
result = some_operation()
```

### Docstring Reference

```python
def my_function():
    """
    Function description.

    ADR: 2025-12-01-my-feature
    """
    pass
```

---

## TypeScript / JavaScript

### New File (JSDoc Header)

```typescript
/**
 * Module description here.
 *
 * @see ADR: 2025-12-01-my-feature
 */

import ...
```

### Inline Comment

```typescript
// ADR: 2025-12-01-my-feature - reason for this choice
const result = someOperation();
```

### Class/Function JSDoc

```typescript
/**
 * Class description.
 *
 * @see ADR: 2025-12-01-my-feature
 */
class MyClass {
  ...
}
```

---

## Rust

### New File (Module Documentation)

```rust
//! Module description here.
//!
//! ADR: 2025-12-01-my-feature

use ...;
```

### Inline Comment

```rust
// ADR: 2025-12-01-my-feature - reason for this choice
let result = some_operation();
```

### Doc Comment

```rust
/// Function description.
///
/// ADR: 2025-12-01-my-feature
fn my_function() {
    ...
}
```

---

## Go

### New File (Package Documentation)

```go
// Package mypackage provides ...
//
// ADR: 2025-12-01-my-feature
package mypackage

import ...
```

### Inline Comment

```go
// ADR: 2025-12-01-my-feature - reason for this choice
result := someOperation()
```

### Function Documentation

```go
// MyFunction does something.
//
// ADR: 2025-12-01-my-feature
func MyFunction() {
    ...
}
```

---

## Configuration Files

### YAML/JSON Comments

```yaml
# ADR: 2025-12-01-my-feature - configuration rationale
setting: value
```

### Markdown Documents

```markdown
<!-- ADR: 2025-12-01-my-feature -->

# Document Title
```

---

## Quick Reference Table

| Language   | New File Header                      | Inline Comment              |
| ---------- | ------------------------------------ | --------------------------- |
| Python     | `"""...\n\nADR: {adr-id}\n"""`       | `# ADR: {adr-id} - reason`  |
| TypeScript | `/** ... \n * @see ADR: {adr-id} */` | `// ADR: {adr-id} - reason` |
| Rust       | `//! ...\n//! ADR: {adr-id}`         | `// ADR: {adr-id} - reason` |
| Go         | `// Package ... \n// ADR: {adr-id}`  | `// ADR: {adr-id} - reason` |
