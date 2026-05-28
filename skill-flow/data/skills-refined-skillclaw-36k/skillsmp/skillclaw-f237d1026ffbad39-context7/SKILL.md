---
name: context7
description: Use this skill to retrieve the latest documentation and code examples for any programming library or framework via the Context7 API. Activate it when you need current API references, usage patterns, or specific version information.
---

# Context7 Documentation Lookup

Context7 is a service that provides up-to-date documentation and code examples for programming libraries and frameworks. This skill helps prevent reliance on outdated training data by fetching the latest information directly from the source.

## When to Use

Use this skill in the following scenarios:
- When you need the latest documentation for a specific library or framework.
- When asking for code examples or usage patterns for library functions.
- When verifying correct usage of library APIs, especially if the information may have changed since your last training.
- When you require version-specific information about a library.

## Workflow

### Step 1: Resolve Library ID

First, obtain the Context7 library ID for the target library:

```bash
curl "https://context7.com/api/v2/libs/search?libraryName=LIBRARY_NAME&query=TOPIC" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Example:**
```bash
curl "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

### Step 2: Fetch Documentation

Once you have the library ID, use it to retrieve specific documentation:

```bash
curl "https://context7.com/api/v2/context?libraryId=LIBRARY_ID&query=SPECIFIC_QUERY" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

**Example:**
```bash
curl "https://context7.com/api/v2/context?libraryId=/facebook/react&query=useEffect" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

### Best Practices
- Always search for the library ID first if unsure.
- Use specific queries to narrow down results effectively.
- Be clear about the purpose of your query to get the most relevant documentation.

## Common Library IDs

| Library | ID |
| ------- | -- |
| React | `/facebook/react` |
| Next.js | `/vercel/next.js` |
| Vue.js | `/vuejs/vue` |
| Prisma | `/prisma/prisma` |
| Tailwind CSS | `/tailwindlabs/tailwindcss` |

## Important Notes
- Ensure that the `CONTEXT7_API_KEY` environment variable is set before making API calls.
- Avoid making more than three API calls per question to prevent unnecessary load and ensure efficiency.