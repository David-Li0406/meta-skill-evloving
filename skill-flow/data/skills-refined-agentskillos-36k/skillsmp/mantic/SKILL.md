---
name: mantic
description: Semantic code search using Mantic. Use when exploring codebases, finding feature implementations, understanding component functionality, locating definitions/references, or mapping architectural patterns. Use Mantic first before grep, find, or manual file exploration.
---

# Mantic Semantic Code Search

## Core Principle

Use Mantic as the initial discovery mechanism. Invoke `search_files` before attempting to read file lists, guess paths, or use grep/find.

## When to Use

- Finding where functionality is implemented
- Understanding how components work
- Locating definitions and references
- Exploring architecture and patterns
- Any codebase discovery task

## Search Strategy

1. **Natural language queries** - Use descriptive phrases, not just keywords
   - Good: "user authentication logic", "stripe payment processing"
   - Bad: "auth", "stripe"

2. **Trust relevance scores** - Higher scores indicate closer match to intent

3. **Search a lot of files** - Set the max results parameter to a high enough value
that you're confident you're finding all the relevant files (or don't set it at all).
Mantic is very fast so searching many files is cheap.

4. **Fall back gracefully** - Use grep/find if Mantic yields insufficient results

## Tools

- `search_files` - Primary search tool. Use `includeImpact: true` for blast radius analysis before changes.
- `analyze_intent` - Understand query category and extract keywords
- `session_start/end` - Track context across related queries; viewed files get boosted in future searches
- `session_record_view` - Record files viewed/modified for context carryover
