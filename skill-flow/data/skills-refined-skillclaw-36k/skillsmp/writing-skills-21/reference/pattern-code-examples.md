# Code Examples in Skills

Best practices for TypeScript/code that Claude should use.

## How It Works

Code blocks in skills serve as examples Claude follows. Use language tags for syntax highlighting.

## Best Practices

1. **Always use language tags**: Use `typescript` not bare code blocks
2. **Show input -> output pairs**: Concrete examples beat abstract descriptions
3. **Keep examples minimal**: Just enough to demonstrate the pattern
4. **Use realistic data**: Not `foo`, `bar` but actual domain terms

## Examples

**API response format:**

```yaml
---
name: api-formatter
description: Formats API responses consistently
---
# API Response Format

Always return responses in this shape:
```

```typescript
interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
}
```

**Example - Success:**

```typescript
const response: ApiResponse<User> = {
  success: true,
  data: { id: "123", name: "Alice" },
  error: null,
};
```

**Example - Error:**

```typescript
const response: ApiResponse<User> = {
  success: false,
  data: null,
  error: "User not found",
};
```

---

**Commit message format:**

```yaml
---
name: commit-formatter
description: Formats commit messages
---

# Commit Format

**Input:** Added user authentication with JWT
**Output:**
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware

**Input:** Fixed timezone bug in reports
**Output:**
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

## Links

- Docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
