---
name: context7
description: Read when users ask about library documentation, need code examples, want API usage patterns, are learning a new framework, need syntax reference, or troubleshooting with library-specific information
---

# Context7 Documentation Fetcher

Fetch library documentation and code examples.

## Usage

```bash
bash ~/.cursor/skills/context7/scripts/fetch.sh <library-name> <query> [page]
```

**Library name format:** Prefer GitHub repo format (`owner/repo`) for precision. Examples:
- `facebook/react` (more specific than just `react`)
- `vercel/next.js`
- `prisma/prisma`
- `expressjs/express`

## Tips for Best Results

- Use specific, detailed queries rather than vague terms
- Include relevant context in the query (e.g., "useState hook with TypeScript" instead of just "state")

## Examples:
```bash
bash ~/.cursor/skills/context7/scripts/fetch.sh facebook/react "useState hook"
bash ~/.cursor/skills/context7/scripts/fetch.sh vercel/next.js "dynamic routes with parameters"
bash ~/.cursor/skills/context7/scripts/fetch.sh prisma/prisma "filtering and sorting query results"
bash ~/.cursor/skills/context7/scripts/fetch.sh facebook/react "useState hook" 2
```

The script returns code examples, API signatures, and important notes.
