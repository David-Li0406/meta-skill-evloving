# Rule Patterns & Templates

This reference contains common patterns and templates for creating effective user rules.

## Table of Contents

1. [Coding Style Rules](#coding-style-rules)
2. [Language & Communication Rules](#language--communication-rules)
3. [Project Configuration Rules](#project-configuration-rules)
4. [Git & Version Control Rules](#git--version-control-rules)
5. [Naming Convention Rules](#naming-convention-rules)
6. [Security Rules](#security-rules)
7. [Testing Rules](#testing-rules)
8. [Documentation Rules](#documentation-rules)

---

## Coding Style Rules

### Async/Await Preference

```
Always use async/await syntax instead of .then() chains for Promise handling.
```

### Error Handling

```
Wrap all async operations in try-catch blocks and log errors with context.
```

### Import Organization

```
Organize imports in this order:
1. Built-in modules
2. External packages
3. Internal modules
4. Relative imports
Separate each group with a blank line.
```

### Function Style

```
Prefer arrow functions for callbacks and anonymous functions.
Use regular function declarations for named exports and methods.
```

### Early Returns

```
Use early returns to reduce nesting. Exit functions early when conditions aren't met.
```

---

## Language & Communication Rules

### Vietnamese Response

```
Respond in Vietnamese when the user writes in Vietnamese.
```

### Concise Responses

```
Keep responses concise and to the point. Avoid unnecessary explanations.
```

### Code Comments

```
Write code comments in English for consistency across the codebase.
```

### Technical Terms

```
Use English for technical terms even when responding in Vietnamese.
Example: "Sử dụng async/await thay vì Promise chains."
```

---

## Project Configuration Rules

### Environment Variables

```
All configuration values that may change between environments must be stored in environment variables, never hardcoded.
```

### File Structure

```
Follow this project structure:
- /app - Application code
- /lib - Shared utilities
- /types - TypeScript type definitions
- /tests - Test files
```

### Dependencies

```
Before adding a new npm package, check if the functionality exists in:
1. Built-in Node.js modules
2. Already installed packages
3. Simple custom implementation
```

### Framework Preference

```
Use [Framework Name] for [purpose]. Always follow official documentation patterns.
```

---

## Git & Version Control Rules

### Commit Message Format

```
Use conventional commits format:
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore
Example: feat(auth): add login functionality
```

### Branch Naming

```
Branch names follow: <type>/<ticket-id>-<short-description>
Example: feature/WL-123-add-wishlist-button
```

### PR Guidelines

```
Every PR must:
1. Have a clear description of changes
2. Include relevant tests
3. Pass all CI checks
4. Be reviewed by at least one team member
```

---

## Naming Convention Rules

### React Components

```
React component files and names use PascalCase.
Example: WishlistButton.tsx, UserProfile.tsx
```

### TypeScript Types

```
- Interfaces: prefix with 'I' or use descriptive names without prefix
- Types: use PascalCase
- Enums: use PascalCase, members in SCREAMING_SNAKE_CASE
```

### Variables & Functions

```
- Variables and functions: camelCase
- Constants: SCREAMING_SNAKE_CASE
- Private class members: prefix with underscore (_privateMethod)
```

### Database

```
- Table names: snake_case, plural (users, wishlist_items)
- Column names: snake_case (created_at, user_id)
- Foreign keys: <table>_id (user_id, product_id)
```

---

## Security Rules

### No Hardcoded Secrets

```
NEVER hardcode API keys, passwords, or secrets in code.
Always use environment variables or a secrets manager.
```

### Input Validation

```
Validate and sanitize all user inputs before processing.
Use zod or similar libraries for schema validation.
```

### SQL Injection Prevention

```
Never concatenate user input into SQL queries.
Always use parameterized queries or ORM methods.
```

### Authentication

```
All API endpoints must verify authentication unless explicitly marked as public.
```

---

## Testing Rules

### Test Coverage

```
All new functions must have corresponding unit tests.
Aim for minimum 80% code coverage.
```

### Test Naming

```
Test names should describe the expected behavior:
"should return user when valid ID is provided"
"should throw error when email is invalid"
```

### Mocking

```
Mock external dependencies (APIs, databases) in unit tests.
Use integration tests for testing actual external interactions.
```

---

## Documentation Rules

### Function Documentation

```
All exported functions must have JSDoc comments with:
- Description
- @param for each parameter
- @returns description
- @throws if applicable
```

### README Updates

```
Update README.md when:
- Adding new features
- Changing configuration
- Modifying setup steps
```

### Inline Comments

```
Add inline comments only for complex logic.
Code should be self-documenting through clear naming.
```

---

## Rule Writing Best Practices

### Be Specific

❌ Bad: "Write good code"
✅ Good: "Use descriptive variable names that indicate purpose (e.g., `userEmail` not `e`)"

### Be Actionable

❌ Bad: "Consider performance"
✅ Good: "Add database indexes for columns used in WHERE clauses"

### Include Examples

❌ Bad: "Use proper naming"
✅ Good: "Functions should be named as verb + noun: `getUserById`, `createWishlistItem`"

### Avoid Conflicts

Ensure rules don't contradict each other. If two rules might conflict, specify priority or conditions.

### Keep It Concise

Each rule should be one clear instruction. If complex, break into multiple rules.
