# Search Reference

## Endpoint

```
GET https://context7.com/api/v2/libs/search
```

## Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| `libraryName` | Yes | Library name to search for (e.g., "react", "nextjs") |
| `query` | Yes | Your question or task (used for relevance ranking) |

## Authentication

```bash
-H "Authorization: Bearer $CONTEXT7_API_KEY"
```

## Response Fields

| Field | Description |
| ----- | ----------- |
| `id` | Library ID for use with context endpoint |
| `name` | Display name |
| `description` | Brief description |
| `totalSnippets` | Number of code examples |
| `trustScore` | Source reputation score |
| `benchmarkScore` | Quality indicator (0-100) |
| `versions` | Available versions |

## Examples

```bash
# Search by library name
curl "https://context7.com/api/v2/libs/search?libraryName=react&query=hooks" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"

curl "https://context7.com/api/v2/libs/search?libraryName=prisma&query=database%20queries" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"

curl "https://context7.com/api/v2/libs/search?libraryName=tailwind&query=styling" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

## Selecting Results

When multiple results are returned, prefer libraries with:

1. Higher `benchmarkScore`
2. More `totalSnippets`
3. Higher `trustScore`

## Common Patterns

| Search | Expected ID |
| ------ | ----------- |
| `react` | `/facebook/react` |
| `next.js` | `/vercel/next.js` |
| `prisma` | `/prisma/prisma` |
| `supabase` | `/supabase/supabase` |
| `tailwind` | `/tailwindlabs/tailwindcss` |
