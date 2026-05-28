---
name: knowledge-query
description: Query the knowledge graph for learnings, patterns, and mistakes. Use when you need to find past learnings, avoid known mistakes, discover established patterns, or search for relevant knowledge before implementing features.
allowed-tools: Bash
---

# Knowledge Query Skill

Semantic search and structured queries over the knowledge graph containing learnings, patterns, and mistakes extracted from past work.

## When to Use

- Before implementing a feature (find relevant learnings)
- When encountering an unfamiliar code area (discover patterns)
- To avoid repeating past mistakes
- When researching how similar issues were solved
- To understand established patterns in a code area
- For semantic search across all stored knowledge
- To query knowledge by specific filters (code area, file, issue)

## MCP Tools (Preferred)

When the MCP server is available, use native tools:

| Tool              | Purpose                                                    |
| ----------------- | ---------------------------------------------------------- |
| `knowledge_query` | Query with filters (codeArea, file, keywords, issueNumber) |
| `knowledge_store` | Store learnings, patterns, mistakes                        |

These tools are automatically available when claude-knowledge MCP server is running.

## CLI Reference (Fallback)

When MCP tools are unavailable, use the checkpoint CLI:

```bash
bun run checkpoint knowledge <command> [args...]
```

## Commands

### Store Learning

Manually store a learning (note: most learnings are extracted automatically via session hooks):

```bash
bun run checkpoint knowledge store-learning <content> [options]
```

Options:

- `--code-area <area>` - Associated code area (e.g., "authentication", "badge-verification")
- `--file <path>` - Associated file path
- `--confidence <n>` - Confidence level (1-10, default: 7)

Example:

```bash
bun run checkpoint knowledge store-learning "Always validate badge expiration before issuing" --code-area badge-issuance --confidence 9
```

### Store Pattern

Record an established pattern:

```bash
bun run checkpoint knowledge store-pattern <name> <description> [options]
```

Options:

- `--code-area <area>` - Code area where pattern applies

Example:

```bash
bun run checkpoint knowledge store-pattern "credential-validation" "Use Zod schemas for all credential validation" --code-area validation
```

### Store Mistake

Record a mistake and how it was fixed:

```bash
bun run checkpoint knowledge store-mistake <description> <how-fixed> [options]
```

Options:

- `--file <path>` - File where mistake occurred

Example:

```bash
bun run checkpoint knowledge store-mistake "Forgot to verify signature before trusting issuer" "Added signature verification step before issuer validation" --file src/verification/verify.ts
```

### Query Knowledge

Structured query with specific filters (keyword-based):

```bash
bun run checkpoint knowledge query [options]
```

At least one filter required:

- `--code-area <area>` - Filter by code area
- `--file <path>` - Filter by file path
- `--text <keyword>` - Filter by keyword in content
- `--issue <n>` - Filter by source issue number
- `--limit <n>` - Max results (default: 10)

Example:

```bash
bun run checkpoint knowledge query --code-area badge-verification
bun run checkpoint knowledge query --file src/badges/verify.ts
bun run checkpoint knowledge query --issue 380 --limit 5
bun run checkpoint knowledge query --text "signature" --code-area cryptography
```

### Semantic Search

Search using natural language with vector similarity:

```bash
bun run checkpoint knowledge search <query-text> [options]
```

Options:

- `--limit <n>` - Max results (default: 5)
- `--threshold <n>` - Minimum similarity score 0-1 (default: 0.7)
- `--include-related` - Include related patterns and mistakes

Example:

```bash
bun run checkpoint knowledge search "how to validate badge signatures"
bun run checkpoint knowledge search "avoiding database race conditions" --threshold 0.8
bun run checkpoint knowledge search "JWT token handling" --include-related
```

### List Code Areas

Show all code areas with stored knowledge:

```bash
bun run checkpoint knowledge list-areas
```

Returns:

- List of code area names
- Count of learnings per area
- Recent activity

### List Files

Show all files with stored knowledge:

```bash
bun run checkpoint knowledge list-files
```

Returns:

- List of file paths
- Count of learnings per file
- Associated code areas

### Stats

Show knowledge graph statistics:

```bash
bun run checkpoint knowledge stats
```

Returns:

- Total learnings
- Total patterns
- Total mistakes
- Knowledge by code area
- Knowledge by file
- Recent additions

## Example: Pre-Implementation Research

```bash
# 1. Find all knowledge about the code area
bun run checkpoint knowledge query --code-area badge-verification --limit 20

# 2. Search for similar features
bun run checkpoint knowledge search "badge signature verification"

# 3. Check for patterns in this area
bun run checkpoint knowledge list-areas

# 4. Look for mistakes to avoid
bun run checkpoint knowledge query --code-area badge-verification --text mistake
```

## Example: Semantic vs Keyword Search

**Keyword Query** (exact filter matching):

```bash
bun run checkpoint knowledge query --code-area authentication --text "JWT"
```

Returns only learnings that:

- Are tagged with code-area "authentication" AND
- Contain the exact text "JWT"

**Semantic Search** (natural language understanding):

```bash
bun run checkpoint knowledge search "handling authentication tokens"
```

Returns learnings similar to the query meaning, including:

- JWT handling
- Token validation
- Session management
- Auth middleware

Use semantic search for exploration, keyword query for precise filtering.

## Output Format

### Query Command

Returns JSON array of learnings:

```json
[
  {
    "id": "learning-123",
    "content": "Always validate JWT signature before trusting claims",
    "codeArea": "authentication",
    "file": "src/auth/jwt.ts",
    "confidence": 9,
    "sourceIssue": 380,
    "createdAt": "2025-01-10T14:32:00Z"
  }
]
```

### Search Command

Returns JSON array with similarity scores:

```json
[
  {
    "id": "learning-456",
    "content": "Use constant-time comparison for signature validation",
    "codeArea": "cryptography",
    "similarity": 0.89,
    "relatedPatterns": ["timing-attack-prevention"],
    "relatedMistakes": ["mistake-234"]
  }
]
```

### Store Commands

Return:

- `success`: Boolean
- `id`: ID of stored entity
- `type`: "learning" | "pattern" | "mistake"

### List Commands

Return arrays of:

- `name`: Code area or file path
- `count`: Number of knowledge entries
- `lastUpdated`: Most recent activity timestamp

### Stats Command

Returns:

```json
{
  "totalLearnings": 142,
  "totalPatterns": 23,
  "totalMistakes": 18,
  "byCodeArea": {
    "authentication": 34,
    "badge-verification": 28
  },
  "byFile": {
    "src/auth/jwt.ts": 12,
    "src/badges/verify.ts": 15
  },
  "recentCount": 8
}
```

## Integration with Session Hooks

Knowledge queries integrate with session lifecycle:

| Hook         | What It Does                                       |
| ------------ | -------------------------------------------------- |
| SessionStart | Automatically queries relevant learnings based on: |
|              | - Current issue number                             |
|              | - Code areas inferred from modified files          |
|              | - File paths being worked on                       |
| SessionEnd   | Automatically stores learnings extracted from:     |
|              | - Commit messages (conventional commits format)    |
|              | - Code areas touched during session                |
|              | - Patterns observed in implementation              |

**Note**: Automatic injection happens when hooks are wired to Claude Code (currently requires manual invocation via `checkpoint session-start`/`session-end`).

## When to Use Manual vs Automatic

**Automatic (via session hooks):**

- Knowledge injection at session start
- Learning extraction at session end
- Routine knowledge accumulation

**Manual (via this skill):**

- Mid-session research when you need more context
- Querying specific knowledge not included in auto-injection
- Storing one-off learnings or insights
- Exploring knowledge graph for patterns
- Checking what knowledge exists before writing
