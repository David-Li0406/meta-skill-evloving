---
name: library-writer
description: Use this skill when writing software libraries, packages, or modules following battle-tested patterns for clean, minimal, production-ready code.
---

# Library Writer

Write software libraries following battle-tested patterns from the most successful open-source maintainers. These patterns have been proven across hundreds of libraries with billions of downloads.

## Core Philosophy

**Simplicity over cleverness.** Aim for zero or minimal dependencies, explicit code over metaprogramming, and framework integration without framework coupling. Every pattern serves production use cases.

**The best library is the one you don't have to think about.** It should:
- Install easily
- Configure simply
- Work as expected
- Not break on upgrades
- Have obvious documentation

## Entry Point Structure

Every library follows this pattern:

```
1. Dependencies (stdlib preferred)
2. Internal modules (relative imports)
3. Conditional framework loading (never require frameworks directly)
4. Module with config and errors
```

### Why This Order?

1. **Dependencies first** - Fail fast if dependencies are missing.
2. **Internal modules** - Load library components.
3. **Conditional framework** - Don't force framework on non-framework users.
4. **Config and errors** - Ready for use immediately.

### Conditional Framework Loading

Never require frameworks directly. Check if they exist first:

```python
# Only load framework integration if framework is present
if framework_is_loaded:
  load_framework_integration()
```

This allows the library to work:
- In framework apps (with integration)
- In plain apps (without framework overhead)
- In test environments (isolated)

## Configuration Pattern

Use simple accessors, not Configuration objects:

```python
# Good
MyLib.api_key = "..."
MyLib.timeout = 30
MyLib.logger = custom_logger

# Bad
MyLib.configure do |config|
  config.api_key = "..."
  config.timeout = 30
  config.logger = custom_logger
end
```

### Why Simple Accessors?

- Easier to understand (just assignment)
- Can be set from anywhere
- No DSL to learn
- Works with environment variables