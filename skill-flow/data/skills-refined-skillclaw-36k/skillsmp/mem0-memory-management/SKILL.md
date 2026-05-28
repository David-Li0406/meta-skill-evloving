---
name: mem0 Memory Management
description: This skill should be used when the user asks about "memory", "remember this", "what do you know about me", "recall", "forget this", "search memories", "save preference", or when Claude needs guidance on using mem0 tools effectively. Provides best practices for memory storage, retrieval, and organization.
version: 0.2.0
---

# mem0 Memory Management

Guidance for effectively using mem0 memory tools to provide personalized, context-aware assistance across sessions.

## CRITICAL: Memory Scope Detection

When storing memories, you MUST determine the correct scope using this two-stage decision process:

### Stage 1: Check for Explicit Scope Signals

**User-scoped (global) signals** - NO app_id:
- "globally", "global memory", "across all projects"
- "I prefer", "I like", "I always", "my preference"
- "remember about me", "for me personally"
- "in general", "as a rule"

**Project-scoped signals** - WITH app_id:
- "this project", "this repo", "this codebase"
- "here", "for this", "in this project"
- "this app", "this application"
- "for this repository"

**If explicit signal found → use that scope. Otherwise, proceed to Stage 2.**

### Stage 2: Analyze Content Type

**User-scoped content** (personal, applies everywhere) - NO app_id:
- Personal preferences: coding style, formatting, naming conventions
- Communication preferences: verbosity, explanation depth
- Tool preferences: editor, terminal, frameworks they generally prefer
- Personal information: name, role, expertise, background
- Work style: how they like to receive feedback, review process

**Project-scoped content** (specific to this codebase) - WITH app_id:
- Architecture decisions: patterns, structure, design choices
- Dependencies: what frameworks/libraries THIS project uses
- File locations: where specific code lives in THIS project
- API details: endpoints, schemas for THIS project
- Configuration: setup steps, environment for THIS project
- Project-specific conventions: naming, patterns unique to THIS codebase

### Stage 3: Default When Ambiguous

**Default to user-scoped (NO app_id)** when:
- No explicit signals found
- Content type is unclear
- Could reasonably apply to multiple projects

### Decision Flow Summary

```
User request → Check explicit signals
                    ↓
         Signal found? → YES → Use indicated scope
                    ↓ NO
         Analyze content type
                    ↓
         Clear content type? → YES → Use appropriate scope
                    ↓ NO
         Default to USER-SCOPED (no app_id)
```

### Examples

**User-scoped (NO app_id):**
```
User: "Remember I prefer TypeScript"
→ Personal preference, applies everywhere
→ add_memory(text="User prefers TypeScript")

User: "Save globally: I like 2-space indentation"
→ Explicit "globally" signal
→ add_memory(text="User prefers 2-space indentation")

User: "Remember my name is James"
→ Personal information
→ add_memory(text="User's name is James")
```

**Project-scoped (WITH app_id):**
```
User: "Remember this project uses Next.js"
→ Explicit "this project" signal
→ add_memory(text="Project uses Next.js", app_id="...")

User: "Save for this repo: API is at /api/v1"
→ Explicit "this repo" signal
→ add_memory(text="API endpoint is at /api/v1", app_id="...")

User: "Remember the auth middleware is in src/middleware/auth.ts"
→ Project-specific file location
→ add_memory(text="Auth middleware located at src/middleware/auth.ts", app_id="...")
```

## Getting the app_id

At session start, you receive:
```
[mem0] app_id="abc123..." available for project-scoped memories
```

Use this exact value when storing project-scoped memories. If no app_id message was received, all memories are user-scoped by default.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `add_memory` | Store new memories with scoping |
| `search_memories` | Semantic search across memories |
| `get_memories` | List memories with filters |
| `get_memory` | Retrieve single memory by ID |
| `update_memory` | Modify existing memory |
| `delete_memory` | Remove single memory |
| `delete_all_memories` | Bulk delete by scope |

## Searching Memories

When searching, consider both scopes:
- Search with `app_id` for project-specific memories
- Search without `app_id` for user preferences

For comprehensive results, you may need to search both scopes.

## Memory Content Guidelines

**Be concise**: One clear fact or preference per memory
```
Good: "User prefers verbose error messages with stack traces"
Bad: "The user said they want more information when there's an error..."
```

**Be specific**: Include concrete details
```
Good: "Project uses PostgreSQL 15 with TimescaleDB extension"
Bad: "Project uses a database"
```

**Include context**: Explain why, not just what
```
Good: "Authentication uses JWT with 24h expiry - chosen for stateless API design"
Bad: "Uses JWT"
```

## Privacy Considerations

- Never store credentials, API keys, or secrets
- Don't store content explicitly marked private
- Be cautious with personal information
- Ask before storing sensitive business information

## Quick Reference

| User Intent | Scope | Include app_id? |
|-------------|-------|-----------------|
| "I prefer X" | User | NO |
| "Remember about me" | User | NO |
| "Globally, I like X" | User | NO |
| "This project uses X" | Project | YES |
| "For this repo" | Project | YES |
| "The code here does X" | Project | YES |
| Ambiguous | User | NO (default) |
