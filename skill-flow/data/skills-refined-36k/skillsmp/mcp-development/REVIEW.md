# MCP Code Review Checklist

## Security (CRITICAL)

- [ ] **SQL Injection**: All queries use parameters? Never string concatenation?
- [ ] **Input Validation**: All inputs validated with Zod?
- [ ] **Secrets**: Credentials in env vars? Nothing hardcoded?
- [ ] **Privilege**: Destructive operations blocked or protected?
- [ ] **Output Sanitization**: Sensitive data filtered?

```typescript
// BAD - SQL Injection
const query = `SELECT * FROM users WHERE name = '${name}'`;

// GOOD - Parameterized
request.input("name", sql.VarChar, name);
const query = "SELECT * FROM users WHERE name = @name";
```

## MCP Structure

- [ ] **McpServer**: Configured with name and version?
- [ ] **Transport**: Using StdioServerTransport?
- [ ] **Error Handling**: server.connect() has .catch()?
- [ ] **Registration Order**: Tools registered before connect()?

## Tool Design

- [ ] **Single Responsibility**: Each tool does one thing?
- [ ] **Naming**: Names are descriptive? (sql_select not query)
- [ ] **Description**: Clear for LLM to understand when to use?
- [ ] **Schema**: Each parameter has .describe()?
- [ ] **Return Format**: Returns content[] and structuredContent?

## Error Handling

- [ ] **Try/Catch**: Async operations wrapped?
- [ ] **Messages**: Errors informative but don't expose internals?
- [ ] **isError Flag**: Errors return `{ isError: true }`?

## Performance

- [ ] **Connection Pool**: Using pool, not individual connections?
- [ ] **Limits**: Queries have LIMIT? maxRows implemented?
- [ ] **Timeouts**: Operations have timeout?

## TypeScript

- [ ] **Strict Mode**: `"strict": true` in tsconfig?
- [ ] **No Any**: Avoids `any`? Explicit types?
- [ ] **Null Checks**: Optional chaining used?

## Logging

- [ ] **console.error**: Logs use stderr (not stdout)?
- [ ] **No Sensitive Data**: Logs don't expose passwords/tokens?

## Review Format

```markdown
### [SEVERITY] Short Description

**File**: path/to/file.ts:line
**Problem**: What's wrong
**Impact**: Consequence
**Fix**: How to correct

\`\`\`typescript
// Current
...

// Suggested
...
\`\`\`
```

Severities: CRITICAL, HIGH, MEDIUM, LOW, INFO
