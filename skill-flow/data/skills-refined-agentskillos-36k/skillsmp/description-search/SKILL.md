---
name: description-search
description: Find accounts by attributes like stage, location, industry, or insurance type. Use for queries like "childcare centers in Texas" or "accounts in Quote stage".
---

# Description Search

## When to use this skill

- Query mentions attributes rather than specific names
- Finding accounts by location ("in Texas", "California accounts")
- Finding accounts by stage ("new leads", "quoted accounts")
- Finding accounts by industry ("restaurants", "childcare centers")
- Finding accounts by insurance type ("GL accounts", "workers comp")

## How to use the tool

Call `search_descriptions` with the attribute query:

```json
{
  "tool": "search_descriptions",
  "args": {"query": "childcare centers in Texas needing follow-up"}
}
```

## Tool response

Returns matching accounts ranked by relevance:

```json
[
  {
    "account_id": "29041",
    "name": "Sunny Days Childcare Center",
    "description": "Childcare center in Austin, TX. Stage: Quote Pitched...",
    "score": 0.85,
    "directory_path": "mem/accounts/29041"
  }
]
```

## Common query patterns

| Query Type | Example |
|------------|---------|
| By location | "accounts in Florida" |
| By stage | "new leads", "application received" |
| By industry | "restaurants", "contractors" |
| By status | "waiting for documents", "quote pending" |
| Combined | "retail businesses in California needing GL" |
