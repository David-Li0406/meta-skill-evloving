---
applyTo: "**/*.md,**/docs/**"
---

# Documentation Patterns

> Standards for generating consistent, high-quality documentation

## Structure Patterns

### Function/Method Documentation

```typescript
/**
 * [Brief one-line description]
 *
 * [Detailed explanation when needed - behavior, gotchas, when to use]
 *
 * @param paramName - Description (include type if not in signature)
 * @returns Description of return value
 * @throws {ErrorType} When this error occurs
 *
 * @example
 * // Practical usage
 * const result = functionName(input);
 */
```

### Class Documentation

```typescript
/**
 * [Brief description of class purpose]
 *
 * [When to use this class, key responsibilities]
 *
 * @example
 * const instance = new ClassName(config);
 * instance.doSomething();
 */
```

### Python Docstrings

```python
def function_name(param: str) -> Result:
    """Brief one-line description.
    
    Detailed explanation if needed.
    
    Args:
        param: Description of the parameter.
        
    Returns:
        Description of what is returned.
        
    Raises:
        ValueError: When input is invalid.
        
    Example:
        >>> function_name("input")
        Result(...)
    """
```

## README Structure

Every README should include:

1. **Title + Badge** — Project name, status badges
2. **Overview** — One paragraph explaining purpose
3. **Quick Start** — Minimal steps to get running
4. **Installation** — Detailed setup instructions
5. **Usage** — Common use cases with examples
6. **API Reference** — Link or inline docs for public API
7. **Contributing** — How to contribute
8. **License** — License information

## Style Guidelines

- **Active voice**: "This function returns..." not "A value is returned..."
- **Concise sentences**: Max 25 words
- **Code examples**: Every public function should have one
- **Error documentation**: Always document what can fail
- **Link related docs**: Cross-reference related functions/classes

## Anti-Patterns to Avoid

- ❌ "This function does what it says" — Be specific
- ❌ Documenting obvious parameters — Focus on non-obvious behavior
- ❌ Missing examples — Always include at least one
- ❌ Outdated documentation — Keep in sync with code
- ❌ Wall of text — Use structure, headings, lists
