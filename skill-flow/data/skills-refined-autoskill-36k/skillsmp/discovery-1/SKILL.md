---
name: discovery
description: Identify which repository contains the bug and which files are affected
---

# Discovery Skill

Identify which repository contains the bug and which files are affected.

## Purpose

Analyze error information and discover the relevant repository, files, and root cause of the issue.

## When to Use

- New task arrives from Sentry alert
- New task arrives from Jira ticket with AI-Fix label
- Manual trigger with error description

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `github.search_code` | Search for code across repositories |
| `github.get_file_contents` | Read file contents |
| `sentry.get_sentry_issue` | Get error details from Sentry |
| `sentry.get_sentry_event` | Get full stack traces |

## Process

### Step 1: Parse Error Information

Extract key information from the error:
- Error message/title
- Stack trace (if available)
- File paths mentioned
- Function/method names
- Package/module names

### Step 2: Repository Identification

Use the following heuristics:

1. **Stack trace analysis**: Extract file paths and match to known repos
2. **Keyword matching**: Match error context to repo descriptions
3. **Code search**: Use `github.search_code` to find matching code

```bash
# Search for unique function names
github.search_code("getCurrentUser")

# Search for unique error messages
github.search_code("Cannot read property 'id' of undefined")
```

### Step 3: File Identification

For the identified repository:

1. Search for files mentioned in stack trace
2. Search for files containing error-related code
3. Identify related test files

```bash
# Get file contents
github.get_file_contents("org/repo", "src/services/auth.ts")

# Find test files
github.search_code("auth.test.ts org:myorg")
```

### Step 4: Root Cause Analysis

1. Read the source code of affected files
2. Understand the code flow that leads to the error
3. Identify the specific issue (null check, type error, etc.)
4. Note any related files that might also need changes

## Output Format

```json
{
  "repository": "owner/repo-name",
  "confidence": 0.95,
  "affectedFiles": [
    "src/services/auth.ts",
    "src/services/auth.spec.ts"
  ],
  "rootCause": "Null pointer exception when user session expires",
  "reasoning": "Stack trace points to auth.ts line 45, session handling code",
  "relatedFiles": [
    "src/types/session.ts",
    "src/middleware/auth.ts"
  ],
  "suggestedApproach": "Add null check before accessing session.user property"
}
```

## Example Usage

### Input
```
Error: TypeError: Cannot read property 'id' of undefined
  at getCurrentUser (src/services/auth.ts:45)
  at authMiddleware (src/middleware/auth.ts:23)
```

### Process
1. Search for "getCurrentUser" in organization repositories
2. Find auth.ts in repo "myorg/api-server"
3. Read auth.ts to understand the code
4. Identify that session object is not validated before access
5. Find related test file auth.spec.ts

### Output
```json
{
  "repository": "myorg/api-server",
  "confidence": 0.98,
  "affectedFiles": ["src/services/auth.ts", "src/services/auth.spec.ts"],
  "rootCause": "Missing null check for session object before accessing user property",
  "reasoning": "Stack trace clearly points to auth.ts:45 where session.user.id is accessed without null check",
  "relatedFiles": ["src/types/session.ts", "src/middleware/auth.ts"],
  "suggestedApproach": "Add guard clause: if (!session?.user) return null"
}
```

## Confidence Scoring

| Confidence | Meaning |
|------------|---------|
| 0.9 - 1.0 | High confidence - exact match found |
| 0.7 - 0.9 | Good confidence - likely correct |
| 0.5 - 0.7 | Medium confidence - needs verification |
| < 0.5 | Low confidence - may need human help |

## Error Handling

| Situation | Action |
|-----------|--------|
| No matching repo found | Report this clearly, ask for more info |
| Multiple repos match | List candidates with confidence scores |
| Stack trace missing | Use error message and code search |
| Access denied | Report permission issue |

## Important

- **Be thorough** - read the actual code, don't guess
- **Check test files** - they often reveal expected behavior
- **Consider related files** - the fix may span multiple files
- **Report low confidence** - don't pretend to be certain when not
