---
name: context-compressor
description: Compress verbose text into token-efficient pseudo-code
allowed-tools: Read
model: sonnet
---

# Context Compressor

Convert verbose requirements into concise pseudo-code format.

## WHAT THIS DOES

Transforms long-winded descriptions into compact function-call syntax:

```text
Before (150 tokens):
"We need to build a user authentication system. It should support
multiple providers like Google and GitHub. Users should be able
to sign in with OAuth. We need JWT tokens that expire after 1 hour.
Also add refresh token support. Make sure passwords are hashed."

After (35 tokens):
implement_auth(
  type="oauth",
  providers=["google", "github"],
  tokens={"type": "jwt", "expiry": "1h", "refresh": true},
  password_hashing="bcrypt"
)
```

**Compression: 76% reduction**

## COMPRESSION RULES

### Rule 1: Extract Actions → Function Names

```text
"Build a REST API" → build_rest_api(...)
"Add user authentication" → add_authentication(...)
"Implement caching" → implement_caching(...)
```

### Rule 2: Extract Details → Parameters

```text
"Support Google and GitHub" → providers=["google", "github"]
"Expire after 1 hour" → expiry="1h"
"Use Redis for caching" → cache_type="redis"
```

### Rule 3: Group Related Info → Objects

```text
"JWT tokens that expire after 1 hour with refresh support"
→ tokens={"type": "jwt", "expiry": "1h", "refresh": true}
```

### Rule 4: Remove Filler Words

Remove: "we need to", "should", "make sure", "also", "it would be nice"

## OUTPUT FORMAT

```text
# Compressed Pseudo-Code

[function_call]

## Compression Stats

Original: [N] tokens
Compressed: [N] tokens
Reduction: [N]% ([N] tokens saved)
```

## EXAMPLE

### Input (Verbose)

```text
We're building a task management application. Users should be able
to create, read, update, and delete tasks. Each task has a title,
description, due date, and priority level. We need to implement
user authentication so only logged-in users can access their tasks.
Use JWT tokens for authentication. The API should be RESTful with
proper HTTP status codes. We also need to add input validation to
make sure task titles aren't empty and due dates are in the future.
Error messages should be user-friendly. Oh, and we should add rate
limiting to prevent abuse.

(125 tokens)
```

### Output (Compressed)

```text
# Compressed Pseudo-Code

build_task_management_app(
  features=["crud"],
  task_schema={
    "title": "string:required",
    "description": "string:optional",
    "due_date": "datetime:required",
    "priority": "enum:[low,medium,high]"
  },
  auth={
    "type": "jwt",
    "required": true
  },
  api={
    "type": "rest",
    "status_codes": "standard"
  },
  validation={
    "title": "not_empty",
    "due_date": "future_only"
  },
  error_handling="user_friendly_messages",
  rate_limiting="enabled"
)

## Compression Stats

Original: 125 tokens
Compressed: 68 tokens
Reduction: 46% (57 tokens saved)
```

## WHEN TO USE

Use compression when:

- User provides long descriptions
- Requirements are buried in prose
- Context window is filling up
- Need to summarize progress
- Documenting decisions compactly

## QUICK RULES

1. **Preserve all** semantic information
2. **Remove filler** words and phrases
3. **Group related** parameters into objects
4. **Use abbreviations** (auth, API, DB) where clear
5. **Show compression** stats (tokens saved)

## VERSION

**2.0.0** - Simplified (280 → 150 lines)
