---
name: issue-parser
description: Extracts actionable information from GitHub issues for code exploration.
---

## Purpose

Parse issue title and body to identify:
- Error messages and stack traces
- File paths and line numbers
- Function/class names
- Technical terms (APIs, queries)
- Reproduction steps

## Usage

Include this file when analyzing issues:

```
Use lib/issue-parser to extract keywords from the issue
```

## Extraction Patterns

### 1. Error Messages

Lines starting with error indicators:
- `Error:`
- `Exception:`
- `Failed:`
- `Uncaught`
- `TypeError:`
- `ReferenceError:`

**Example:**
```
Error: Authentication token expired
TypeError: Cannot read property 'user' of undefined
```

**Extract:** `["Authentication token expired", "Cannot read property 'user' of undefined"]`

### 2. Code Blocks

Text within triple backticks:
````
```javascript
function login() {
  throw new Error("Timeout");
}
```
````

**Extract:** `["function login", "throw new Error", "Timeout"]`

### 3. File Paths

Patterns indicating files:
- Contains `/` and ends with extension: `src/auth/login.ts`
- Stack trace format: `at Object.<anonymous> (/path/file.js:123:45)`
- Relative paths: `./components/Button.tsx`

**Regex:** `([./\w-]+\/[\w.-]+\.(ts|js|py|go|rs|java|rb|php))`

**Example:**
```
The error occurs in src/auth/middleware.ts line 45
```

**Extract:** `["src/auth/middleware.ts"]`

### 4. Function/Class Names

CamelCase or PascalCase identifiers:
- `AuthenticationError`
- `handleLogin`
- `UserService`

**Regex:** `\b[A-Z][a-zA-Z0-9]*\b|\b[a-z]+[A-Z][a-zA-Z0-9]*\b`

**Example:**
```
The UserAuthenticator class throws an InvalidTokenError
```

**Extract:** `["UserAuthenticator", "InvalidTokenError"]`

### 5. Stack Traces

Multi-line stack traces with file:line:column format:

```
at login (/src/auth.ts:123:10)
at middleware (/src/server.ts:45:20)
at process (/node_modules/express/lib/router.js:284:15)
```

**Extract:**
- Files: `["src/auth.ts", "src/server.ts"]`
- Functions: `["login", "middleware"]`
- Lines: `["123", "45"]`

### 6. HTTP/API References

URLs and API endpoints:
- `https://api.example.com/v1/auth`
- `POST /api/users`
- `GET /health`

**Regex:** `(https?://[^\s]+)|((GET|POST|PUT|DELETE|PATCH)\s+/[\w/]+)`

## Implementation

```typescript
interface ParsedIssue {
  errors: string[];
  files: string[];
  functions: string[];
  stackTraces: StackTrace[];
  keywords: string[];
}

interface StackTrace {
  file: string;
  line: number;
  function: string;
}

function parseIssue(title: string, body: string): ParsedIssue {
  // Combine title and body
  const text = `${title}\n${body}`;

  // Extract patterns
  return {
    errors: extractErrors(text),
    files: extractFiles(text),
    functions: extractFunctions(text),
    stackTraces: extractStackTraces(text),
    keywords: extractKeywords(text)
  };
}
```

## Output Format

When using this parser, format extracted information as:

```markdown
**Extracted Information:**

**Error Messages:**
- Authentication token expired
- Cannot read property 'user' of undefined

**Files Referenced:**
- src/auth/middleware.ts (line 45)
- src/server.ts

**Functions/Classes:**
- AuthenticationError
- handleLogin
- UserService

**Keywords:**
- authentication, token, timeout, session
```

## Usage in handle-issue Command

```markdown
1. Fetch issue: \`gh issue view <number> --json title,body\`
2. Parse with this library: extract errors, files, functions
3. Pass to code-explorer: use extracted keywords for search
4. Generate plan: reference found locations
```

## Edge Cases

**Empty issue body:**
- Use only title
- Extract what's available
- Proceed with limited information

**No technical details:**
- Extract general terms
- Use broad search patterns
- May escalate to deep analysis

**Foreign language:**
- Focus on code blocks and technical terms (usually English)
- File paths and function names are language-agnostic

**Very long issues:**
- Prioritize first 1000 characters and code blocks
- Full analysis still possible, just focused extraction

## YAGNI Notes

**Not included (intentionally):**
- NLP/sentiment analysis
- Issue classification (bug vs feature)
- Priority detection
- Related issue linking

Keep it simple: extract technical keywords for code search.
