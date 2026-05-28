---
name: context7
description: Retrieve up-to-date documentation and code examples for any library using Context7. Use this skill when looking up library documentation, API references, code examples, or when implementing features with external libraries. Also use when the user mentions a specific library version or needs current docs instead of training knowledge.
---

# Context7 Documentation Lookup

Retrieve current documentation and code examples for any programming library directly from the source.

**Prerequisite:** Set `CONTEXT7_API_KEY` environment variable.

## API Quick Reference

| Endpoint | Purpose |
| -------- | ------- |
| `/api/v2/libs/search` | Find libraries by name |
| `/api/v2/context` | Get documentation for a library |

## Usage

### Search Libraries

```bash
curl "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

Returns library IDs, descriptions, and metadata for matching libraries.

### Get Documentation

```bash
# JSON format (default)
curl "https://context7.com/api/v2/context?libraryId=/facebook/react&query=useEffect" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"

# Text format (for LLM prompts)
curl "https://context7.com/api/v2/context?libraryId=/facebook/react&query=useEffect&type=txt" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"

# Specific version
curl "https://context7.com/api/v2/context?libraryId=/vercel/next.js/v15.1.8&query=app%20router" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

## Workflow

Think step-by-step when using Context7:

1. **Search first** - Find the correct library ID using the search endpoint
2. **Query docs** - Use the library ID with the context endpoint to get relevant documentation
3. **Refine if needed** - Use specific queries or version parameters to narrow results

## When to Use Each Endpoint

| Use `/libs/search` | Use `/context` |
| ------------------ | -------------- |
| Finding library IDs | Querying documentation |
| Exploring available libraries | Getting code examples |
| Unknown or ambiguous library name | You have a library ID |

## Common Library IDs

| Library | ID |
| ------- | -- |
| React | `/facebook/react` |
| Next.js | `/vercel/next.js` |
| Prisma | `/prisma/prisma` |
| Supabase | `/supabase/supabase` |
| TailwindCSS | `/tailwindlabs/tailwindcss` |

## Rules

- Always search for the library ID first if unsure
- Use `type=txt` for LLM-friendly text output
- Include version in library ID for specific releases (e.g., `/vercel/next.js/v15.1.8`)
- URL-encode query parameters with spaces

## References

- [Search](references/search.md) - Finding libraries
- [Docs](references/docs.md) - Querying documentation
