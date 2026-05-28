---
name: context7
description: "Context7 MCP for up-to-date library/API docs and code examples. Use for code generation, setup/config steps, and library-specific questions. Load the mcporter skill to execute calls."
---

# Context7 MCP

Use Context7 for version-specific docs and code examples.

## When to use

- Library/API questions, setup/config steps
- Avoiding outdated or hallucinated APIs
- If repo docs are needed, try DeepWiki first

## Transport

- Remote HTTP: `https://mcp.context7.com/mcp` (configured as `context7` in MCP)
- If auth is required, set `CONTEXT7_API_KEY`

## Quick start

```bash
resolve-library-id query="react query" libraryName="@tanstack/react-query"
query-docs libraryId="/tanstack/react-query" query="invalidate a query"
```

## Notes

- If you already have a library ID (`/org/project` or `/org/project/version`), skip resolve.
- Otherwise call `resolve-library-id` before `query-docs`.
- Follow tool limits: max 3 calls per question (per tool rules).
- Prefer high reputation + higher snippet count when choosing a library ID.

## Query templates

See `assets/query-templates.json`.
