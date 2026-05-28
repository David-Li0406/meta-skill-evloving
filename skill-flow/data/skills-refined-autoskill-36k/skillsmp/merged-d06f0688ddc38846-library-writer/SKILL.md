---
name: library-writer
description: Use this skill when writing software libraries, packages, or modules following battle-tested patterns for clean, minimal, production-ready code.
---

# Library Writer

Write software libraries following battle-tested patterns from successful open-source maintainers. These patterns have been proven across hundreds of libraries with billions of downloads.

## Core Philosophy

**Simplicity over cleverness.** Aim for zero or minimal dependencies, explicit code over metaprogramming, and framework integration without framework coupling. The best library is the one you don't have to think about; it should:
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

```
# Only load framework integration if framework is present
if framework_is_loaded:
  load framework_integration
```

This allows the library to work in:
- Framework apps (with integration)
- Plain apps (without framework overhead)
- Test environments (isolated)

## Configuration Pattern

Use simple accessors, not Configuration objects:

```
Good:
  MyLib.api_key = "..."
  MyLib.timeout = 30
  MyLib.logger = custom_logger

Bad:
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
- Works with environment variables naturally
- Testable (just set the value)

### Configuration Defaults

Set sensible defaults immediately:

```
Module MyLib:
  timeout = 10           # Reasonable default
  logger = null          # Optional
  api_key = ENV["KEY"]   # From environment
```

## Error Handling

Simple hierarchy with informative messages:

```
Module MyLib:
  class Error (base error)
  class ConfigError (configuration problems)
  class ValidationError (invalid input)
  class ConnectionError (network issues)
```

### Error Design Principles

1. **Inherit from standard error class** - Works with existing error handling.
2. **Few error types** - Don't create an error for every situation.
3. **Informative messages** - Include what went wrong and how to fix it.
4. **Validate early** - Raise ArgumentError on bad input immediately.

## API Design Principles

### Class Macro Pattern

The signature pattern for libraries that enhance classes:

```
Usage:
  class Product:
    searchable(fields: ["name", "description"])

Implementation:
  def searchable(**options):
    validate_options(options)
    store_options(options)
    add_methods()
```

### Single Configuration Method

One method call should configure everything:

```
Good:
  class User:
    authenticatable()  # Adds all auth methods

Bad:
  class User:
    add_password_field()
    add_session_methods()
    add_remember_token()
    configure_encryption()
```

## Dependency Management

### Zero Runtime Dependencies (When Possible)

```
Good:
  # Use stdlib for common operations
  # Vendor small utilities if needed
  # No runtime dependencies in manifest

Bad:
  # Dependencies for things stdlib handles
  # Dependencies for "convenience"
  # Dependencies that pull in more dependencies
```

### Development Dependencies

Keep development dependencies separate:

```
Development only:
  - Test framework
  - Linting tools
  - Documentation generators
  - Debug utilities

Never in production:
  - These don't ship with the library
  - Users don't install them
```

### Lock Files

**Never commit lock files in libraries.** Lock files:
- Lock to specific versions you tested with
- Prevent users from getting compatible updates
- Cause conflicts with user's other dependencies

## Testing Philosophy

### Use Standard Test Framework

Every language has a standard test framework. Use it.

```
Python: pytest or unittest
JavaScript: Jest or Vitest
Go: testing stdlib
Rust: built-in test
Ruby: Minitest
```

### What to Test

```
1. Public API - Every public method
2. Edge cases - Empty input, null, large data
3. Error conditions - Invalid input, network failures
4. Configuration - Different config combinations
5. Integration - With frameworks (if applicable)
```

### Test Structure

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests with external systems
└── fixtures/       # Test data
```

## Anti-Patterns to Avoid

| Pattern | Problem | Alternative |
|---------|---------|-------------|
| Dynamic method generation | Hard to understand, debug | Define methods explicitly |
| Configuration objects | Unnecessary complexity | Simple accessors |
| Tight framework coupling | Limits library usage | Conditional loading |
| Many runtime dependencies | Bloat, conflicts, security | Use stdlib, vendor |
| Heavy DSLs | Learning curve, magic | Explicit method calls |
| Metaprogramming magic | Debugging nightmare | Clear, explicit code |
| Committing lock files | Version conflicts | Let users manage dependencies |

## Directory Structure

```
my-library/
├── lib/                    # Source code (or src/)
│   ├── my_library.ext      # Entry point
│   ├── my_library/         # Internal modules
│   │   ├── client.ext
│   │   ├── config.ext
│   │   └── errors.ext
│   └── my_library/integrations/  # Framework integrations
│       └── framework.ext
├── tests/                  # Test files
├── README.md               # Documentation
├── LICENSE                 # License file
└── [package manifest]      # package.json, setup.py, etc.
```

## Success Criteria

A well-designed library:
- Installs with one command
- Configures with simple assignment
- Works without framework (if applicable)
- Has zero or minimal dependencies
- Uses explicit, readable code
- Tests pass across supported versions
- Documents the public API clearly
- Handles errors informatively
- Doesn't break on upgrades