---
name: typescript-coding-standards
description: TypeScript best practices, type system usage, and code quality standards
hooks:
  SessionStart:
    - type: command
      command: |
        if command -v yq &> /dev/null && [ -f ".claude/config.yaml" ]; then
          echo "=== Coding Standards ==="
          yq -o=json '.coding_standards' .claude/config.yaml 2>/dev/null || true
        fi
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: |
            FILE="${TOOL_INPUT_FILE_PATH:-}"
            [ -z "$FILE" ] && exit 0
            EXT="${FILE##*.}"
            case "$EXT" in
              ts|tsx|js|jsx) npx eslint "$FILE" --quiet 2>&1 | head -5 || true ;;
            esac
---

# TypeScript Coding Standards

## Principles

### Type Safety

- Enable strict mode in tsconfig.json
- Avoid 'any' type - use 'unknown' when type is truly uncertain
- Use const assertions for literal types (as const)
- Prefer type inference over explicit types when obvious
- Use discriminated unions for complex state modeling

### Naming Conventions

- Use PascalCase for types, interfaces, and classes
- Use camelCase for variables, functions, and properties
- Use UPPER_SNAKE_CASE for constants
- Prefix interfaces with 'I' only when necessary to avoid conflicts
- Use descriptive names that reveal intent

### Type Definitions

- Prefer interfaces for object types (extensible)
- Use type aliases for unions, intersections, and utilities
- Define types close to where they're used
- Export types from index files for library modules
- Use utility types (Partial, Pick, Omit, Record, etc.)

### Function Signatures

- Always specify return types for public functions
- Use optional parameters with default values sparingly
- Prefer function overloads for complex signatures
- Use generics for reusable, type-safe functions

### Error Handling

- Use typed errors with discriminated unions
- Prefer Result<T, E> pattern over throwing exceptions
- Document thrown exceptions in JSDoc comments
- Handle all error cases explicitly

## Best Practices

### Imports

- Use path aliases for cleaner imports (@/ prefix)
- Group imports: external -> internal -> relative
- Use named imports over default imports when possible
- Avoid circular dependencies

### Code Organization

- One component/class per file (exceptions for small helpers)
- Co-locate related files (component + styles + tests)
- Use index files for barrel exports
- Keep files under 300 lines when possible

### Documentation

- Use JSDoc comments for public APIs
- Document complex type definitions
- Explain non-obvious type assertions
- Keep comments up-to-date with code changes

## Anti-Patterns

### Avoid

- Type assertions (as Type) without justification
- Non-null assertions (!) without null checks
- Empty interfaces extending other types
- Excessive use of Pick/Omit (indicates poor type design)
- Magic numbers - use named constants
- Mutating function parameters

## Code Quality

### Linting

- Configure ESLint with TypeScript plugin
- Enable recommended TypeScript rules
- Use Prettier for consistent formatting
- Fix all linting errors before commit

### Testing

- Type test critical type utilities
- Test type narrowing logic
- Verify discriminated unions exhaustiveness
