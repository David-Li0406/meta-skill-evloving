---
name: continuous-learning
description: Use this skill to extract reusable patterns and insights from development sessions at their conclusion.
---

# Continuous Learning Skill

This skill is designed to capture reusable patterns and knowledge from development sessions, facilitating continuous learning and improvement.

## Trigger Conditions

- At the end of a session
- Discovery of new debugging techniques
- Resolution of complex issues
- Creation of reusable solutions
- Acquisition of project-specific knowledge

## Learning Pattern Types

### 1. Error Resolution Patterns

When resolving an error, document:
- Error message
- Root cause
- Solution
- Preventive measures

```markdown
## Error: Cannot read property 'xxx' of undefined

### Scenario
Accessing nested object properties

### Root Cause
Asynchronous data not fully loaded before access

### Solution
```typescript
// Use optional chaining
const value = obj?.nested?.property

// Or provide a default value
const value = obj?.nested?.property ?? defaultValue
```

### Prevention
- Always use optional chaining for potentially null properties
- Add loading state checks in components
```

### 2. Debugging Techniques

```markdown
## Technique: Debugging Next.js API Routes

### Scenario
API route returns unexpected results

### Technique
1. Add logging at the start of route.ts
```typescript
export async function GET(request: NextRequest) {
  console.log('[API] GET /api/xxx', {
    url: request.url,
    headers: Object.fromEntries(request.headers)
  })
  // ...
}
```

2. Use Postman/curl for direct testing
3. Check if middleware is intercepting
```

### 3. Workarounds

```markdown
## Workaround: Complex Queries Not Supported by Prisma

### Scenario
Need to execute SQL not natively supported by Prisma

### Workaround
```typescript
// Use $queryRaw to execute raw SQL
const result = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE LOWER(name) LIKE ${`%${search.toLowerCase()}%`}
`

// Or use $executeRaw for commands
await prisma.$executeRaw`
  UPDATE users SET updated_at = NOW()
  WHERE id = ${userId}
`
```

### Note
- Manual handling of SQL injection protection is required
- Return types need to be specified manually
```

### 4. Project-Specific Knowledge

```markdown
## Project: User Authentication Flow

### Flow
1. User submits credentials → POST /api/auth/login
2. Validate credentials → Check database
3. Generate JWT → Set httpOnly cookie
4. Return user information

### Key Files
- `src/app/api/auth/login/route.ts` - Login endpoint
- `src/lib/auth.ts` - Authentication utility functions
- `src/middleware.ts` - Route protection

### Considerations
- Token validity period is 7 days
- Refresh token at /api/auth/refresh
- Protected routes configured in middleware.ts
```

## Evaluation Checklist

At the end of a session, check for the following:

### Patterns Worth Documenting

```markdown
- [ ] Resolved a complex bug?
- [ ] Discovered a debugging technique?
- [ ] Created a reusable code snippet?
- [ ] Learned a new usage of a framework/library?
- [ ] Encountered and resolved a performance issue?
- [ ] Found a workaround?
- [ ] Gained project-specific knowledge?
```

### Patterns Not Worth Documenting

```markdown
- [ ] Simple typos
- [ ] One-time configuration issues
- [ ] Temporary external API failures
- [ ] Known simple problems
```

## Knowledge Base Structure

```
.claude/
└── learned/
    ├── errors/
    │   ├── prisma-connection-issues.md
    │   └── react-hydration-mismatch.md
    ├── debugging/
    │   ├── next-api-routes.md
    │   └── database-query-slow.md
    ├── workarounds/
    │   ├── prisma-raw-queries.md
    │   └── nextauth-custom-session.md
    ├── patterns/
    │   ├── error-handling.md
    │   └── api-response-format.md
    └── project/
        ├── auth-flow.md
        └── data-models.md
```

## Knowledge Document Template

```markdown
---
title: [Title]
category: [errors|debugging|workarounds|patterns|project]
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [Title]

## Scenario
[Describe the scenario in which this issue/pattern was encountered]

## Problem/Need
[Specific problem description or need statement]

## Solution
[Detailed solution, including code examples]

## Related Files
- `path/to/file.ts` - [Description]

## References
- [Link1](url)
- [Link2](url)

## Notes
[Points to consider when using this]
```

## Automation Scripts

### Session Evaluation Script

```bash
#!/bin/bash
# evaluate-session.sh
# Evaluate if there are extractable patterns at the end of a session

LEARNED_PATH="${HOME}/.claude/learned"
MIN_SESSION_LENGTH=${MIN_SESSION_LENGTH:-10}

# Get the number of session messages
message_count=$(grep -c '"type":"user"' "$CLAUDE_TRANSCRIPT_PATH" 2>/dev/null || echo "0")

# Skip short sessions
if [ "$message_count" -lt "$MIN_SESSION_LENGTH" ]; then
  echo "[Learning] Session too short ($message_count messages), skipping evaluation" >&2
  exit 0
fi

# Prompt evaluation
echo "[Learning] Session has $message_count messages - consider extracting reusable patterns" >&2
echo "[Learning] Check for:" >&2
echo "[Learning]   - Resolved complex bugs" >&2
echo "[Learning]   - New debugging techniques" >&2
echo "[Learning]   - Reusable code patterns" >&2
echo "[Learning]   - Project-specific knowledge" >&2
echo "[Learning] Save location: $LEARNED_PATH" >&2
```

### Configuration File

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": "~/.claude/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "debugging_techniques",
    "workarounds",
    "project_specific"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "external_api_issues"
  ]
}
```

## Best Practices

1. **Record Promptly** - Document solutions immediately after resolving issues.
2. **Structure** - Use a consistent template format.
3. **Specific Examples** - Include code examples and file paths.
4. **Regular Review** - Periodically organize and update the knowledge base.
5. **Team Sharing** - Share valuable knowledge with the team.
6. **Version Control** - Include the knowledge base in version control.
7. **Tagging** - Use tags for easier searching.
8. **Keep It Concise** - Only document valuable content.
9. **Update Outdated Information** - Timely updates for obsolete information.
10. **Contextualize Projects** - Record project-specific contexts.

---

**Remember**: Every debugging session is a learning opportunity. Document it, and you'll resolve similar issues faster next time.