# Naming Conventions

Renames identifiers to match the project's established naming patterns.

## Detection Strategy

1. **Study existing conventions first**:
   ```bash
   grep -r "function " --include="*.ts" . | head -20
   grep -r "const " --include="*.ts" . | head -20
   ```

2. **Check for style guides**: Look for CONTRIBUTING.md, STYLE.md, or ESLint naming rules

3. **Match immediate context**: Functions in a file should match other functions in that file

## Common Conventions

### JavaScript/TypeScript

| Element | Convention |
|---------|------------|
| Variables | `camelCase` |
| Constants | `SCREAMING_SNAKE_CASE` or `camelCase` |
| Functions | `camelCase` |
| Classes | `PascalCase` |
| React Components | `PascalCase` |
| Interfaces/Types | `PascalCase` |
| Files (components) | `PascalCase.tsx` or `kebab-case.tsx` |
| Files (utilities) | `camelCase.ts` or `kebab-case.ts` |
| Hooks | `useCamelCase` |
| Event handlers | `handleEventName` or `onEventName` |
| Booleans | `is*`, `has*`, `should*`, `can*` |

### Python

| Element | Convention |
|---------|------------|
| Variables | `snake_case` |
| Constants | `SCREAMING_SNAKE_CASE` |
| Functions | `snake_case` |
| Classes | `PascalCase` |
| Modules | `snake_case` |
| Private | `_leading_underscore` |

### Go

| Element | Convention |
|---------|------------|
| Variables | `camelCase` |
| Exported | `PascalCase` (public) |
| Unexported | `camelCase` (private) |
| Packages | `lowercase` |
| Files | `snake_case.go` |
| Interfaces | Often end in `-er` |
| Acronyms | All caps: `HTTPServer` |

## Renaming Safely

Update ALL references:
- Definition site
- All import statements
- All usage sites
- String references (logs, error messages)
- Comments and documentation
- Test files
- Type definitions

```bash
# Verify after renaming
npx tsc --noEmit
grep -r "oldName" --include="*.ts" .
```

For file renames:
```bash
git mv old-name.ts new-name.ts
```

## Guidelines

- Only rename new code, not existing code that predates the branch
- Match sibling files' naming style
- Be careful with renamed exports that might be used externally
