---
name: text-search
description: Search for specific text within account files. Use to find mentions of topics, names, or terms across communications.
---

# Text Search

## When to use this skill

- Looking for specific mentions across communications
- Finding all references to a topic (e.g., "loss runs", "quote")
- Searching within a specific account's files
- Cross-account text searches

## How to use the tool

Call `search_files` with query and path:

```json
{
  "tool": "search_files",
  "args": {
    "query": "loss runs",
    "path": "mem/accounts/29041"
  }
}
```

## Tool response

Returns matching lines with file paths:

```json
[
  {
    "file": "mem/accounts/29041/sources/emails/email_339115/raw.txt",
    "line": 12,
    "content": "Please send us your loss runs for the past 3 years."
  }
]
```

## Search patterns

| Use Case | Path | Query |
|----------|------|-------|
| Within one account | `mem/accounts/29041` | search term |
| All emails for account | `mem/accounts/29041/sources/emails` | search term |
| All accounts | `mem/accounts` | search term |

## Tips

- Search is case-insensitive
- Use specific terms for better results
- Search `summary.md` files for quick overview
- Search `raw.txt` for exact quotes and details
