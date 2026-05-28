---
name: coding-principles
description: Universal coding principles and best practices for maintainable software
license: MIT
compatibility: opencode
metadata:
    related_python_guidelines: For Python-specific implementation, use skill `python-guidelines`
    related_testing_strategy: For testing approaches, use skill `testing-strategy`
---

# Coding Principles

## What I Do

Provide universal coding principles and best practices that apply across programming languages and project types.

## Universal Coding Principles

### Code Quality Standards

**Maintainability:**

- Follow consistent naming conventions
- Use clear, descriptive variable names
- Keep functions focused and single-purpose
- Limit function complexity (cyclomatic complexity < 10)

**Readability:**

- Use consistent indentation and formatting
- Add meaningful comments for complex logic
- Document public APIs and interfaces
- Follow language-specific style guides

### Version Control Best Practices

```bash
# Universal git workflow
# Feature branches: feature/<name>
# Bug fixes: fix/<description>
# Documentation: docs/<topic>
# Releases: release/v<version>

# Commit message format
# Type: feat, fix, docs, style, refactor, perf, test, chore
# Scope: optional module/component
# Subject: imperative, present tense, <50 chars
# Body: optional detailed explanation
# Footer: optional breaking changes, issue references
```

### Boolean Flags Implementation

```python
# Universal boolean flag pattern
class FeatureFlags:
    def __init__(self, **flags):
        self._flags = flags

    def is_enabled(self, flag_name):
        return self._flags.get(flag_name, False)

    def enable(self, flag_name):
        self._flags[flag_name] = True

    def disable(self, flag_name):
        self._flags[flag_name] = False
```

## When to Use Me

Use this skill when:

- Establishing coding standards for new projects
- Onboarding new team members
- Creating cross-project consistency
- Implementing maintainable software practices

## Universal Examples

### Environment Variable Patterns

```python
# Universal environment variable handling
import os
from typing import Optional

def get_env_var(name: str, default: Optional[str] = None) -> str:
    """Get environment variable with validation"""
    value = os.environ.get(name, default)
    if value is None:
        raise ValueError(f"Required environment variable {name} not set")
    return value
```

### Error Handling Patterns

```python
# Universal error handling
def safe_operation(func, *args, **kwargs):
    """Execute function with universal error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        # Log error with context
        log_error(f"Operation {func.__name__} failed: {str(e)}")
        # Return graceful fallback
        return get_fallback_value(func)
```

## Best Practices

1. **Consistency**: Apply the same principles across all projects
2. **Documentation**: Document coding standards clearly
3. **Automation**: Use linters and formatters to enforce standards
4. **Review**: Implement code review processes

## Compatibility

Applies to:

- All programming languages
- Any software project type
- Cross-project standardization
- Organizational coding guidelines
