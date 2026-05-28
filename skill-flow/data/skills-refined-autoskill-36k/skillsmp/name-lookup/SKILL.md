---
name: name-lookup
description: Find accounts by company name using semantic search. Use when query mentions a specific company like "Sunny Days Childcare" or "ABC Corp".
---

# Name Lookup

## When to use this skill

- Query mentions a specific company name
- User asks "What's the status of [Company]?"
- User references an account by name (full or partial)

## How to use the tool

Call `lookup_account` with the company name:

```json
{
  "tool": "lookup_account",
  "args": {"query": "Sunny Days Childcare"}
}
```

## Tool response

Returns a list of matching accounts with similarity scores:

```json
[
  {
    "account_id": "29041",
    "name": "Sunny Days Childcare Center",
    "score": 0.92,
    "directory_path": "mem/accounts/29041"
  }
]
```

## Next steps after lookup

1. Use the `directory_path` to read `state.md` for current status
2. Navigate to `sources/` for communication history
3. Read `history.md` for recent changes
