---
name: recall
description: "Search project memory for relevant context. Use to find past decisions, similar problems, or session history. Triggers on: recall, remember, what did we decide, find in memory, search memory, past sessions."
---

# Memory Recall

Search project memory to find relevant past context.

---

## The Job

1. Understand what the user is looking for
2. Search across memory sources
3. Return relevant context with references

---

## Memory Sources

Search in order of relevance:

### 1. Project Memory (`~/aiconfig/memory/projects/{project}/`)

- **context.json** - Current project state, tech stack, known issues
- **sessions.json** - Past session summaries and follow-ups
- **decisions.json** - Architectural Decision Records

### 2. Global Memory (`~/aiconfig/memory/global/`)

- **preferences.json** - Cross-project coding preferences
- **patterns.json** - Learned patterns and solutions

### 3. Vector Search (if available)

- LanceDB embeddings for semantic search
- "Find similar problems I've solved"

---

## Search Strategies

### By Topic

```
User: "What did we decide about authentication?"

Search:
1. decisions.json for title/context containing "auth"
2. sessions.json for decisions_made mentioning "auth"
3. context.json for relevant architecture notes
```

### By Time

```
User: "What did we do last session?"

Search:
1. sessions.json, sort by date, return most recent
```

### By File

```
User: "What changes have we made to the auth module?"

Search:
1. sessions.json for files_modified matching pattern
2. Return sessions that touched those files
```

### Semantic (with LanceDB)

```
User: "Have I solved a similar caching problem before?"

Search:
1. Embed the query
2. Vector search across session summaries and decisions
3. Return top matches with similarity scores
```

---

## Output Format

### For Decisions

```
Found 2 relevant decisions:

**ADR-003: Use Redis for session storage** (2025-01-10)
- Context: Need fast session lookups for auth
- Decision: Redis with 24h TTL
- Rationale: Sub-millisecond reads, built-in expiry

**ADR-007: JWT for API authentication** (2025-01-15)
- Context: API needs stateless auth
- Decision: Short-lived JWTs with refresh tokens
- Rationale: Scalable, no session storage needed
```

### For Sessions

```
Found 3 sessions mentioning "auth":

**2025-01-15** - Implemented JWT authentication
- Files: src/auth/jwt.ts, src/middleware/auth.ts
- Follow-up: Add refresh token rotation

**2025-01-12** - Set up user model
- Files: prisma/schema.prisma, src/models/user.ts
- Decisions: Used bcrypt for password hashing
```

### For Context

```
Current project context:

**Tech Stack**: Next.js, TypeScript, Prisma, PostgreSQL
**Current Focus**: Payment integration
**Known Issues**:
- Slow initial page load (investigating)
- Auth tokens not refreshing properly
```

---

## No Results

If nothing found:

```
No memory found for "{query}".

This could mean:
1. We haven't worked on this topic yet
2. It wasn't logged in a previous session
3. Try different search terms

Would you like to:
A) Search with different terms
B) Check global preferences
C) Start fresh (I'll help figure it out)
```

---

## Checklist

- [ ] Understood what user is looking for
- [ ] Searched relevant memory sources
- [ ] Returned context with clear references
- [ ] Offered alternatives if nothing found
