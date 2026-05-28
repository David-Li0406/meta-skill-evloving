---
name: aip-knowledge
description: This skill should be used when the user asks about "AIP rules", "API Improvement Proposals", "Google API guidelines", "AIP-158", "AIP-193", or any specific AIP number. Also use when user asks "how should I implement pagination", "what's the right error format", "how do I design a REST API following Google's standards", or needs guidance on errors, pagination, filtering, field masks, long-running operations, or batch operations in REST/OpenAPI APIs.
---

# AIP Knowledge

Quick reference for API Improvement Proposals adapted to REST/OpenAPI.

## How to Use This Skill

1. **For quick patterns**: Use the Quick Reference section below
2. **For detailed guidance**: Load the relevant reference file from the table
3. **For AIP rule violations**: See `linter-rules.md` for all 17 automated rules
4. **For deeper explanation**: Use the `aip-lookup` agent to fetch from google.aip.dev

## Reference Files

Load the relevant reference file based on the task:

| Topic                | Reference File    | When to Use                                      |
| -------------------- | ----------------- | ------------------------------------------------ |
| Error responses      | `errors.md`       | Designing error schema, reviewing error handling |
| Pagination           | `pagination.md`   | Adding pagination to list endpoints              |
| Filtering & sorting  | `filtering.md`    | Adding filter/order_by parameters                |
| Long-running ops     | `lro.md`          | Async operations, jobs, polling                  |
| Partial updates      | `field-masks.md`  | PATCH implementation, update semantics           |
| Batch operations     | `batch.md`        | Batch create/update/delete                       |
| Proto → REST mapping | `rest-mapping.md` | Translating AIP concepts to REST                 |
| Linter rules         | `linter-rules.md` | All 17 automated AIP rules with skip options     |

## Quick Reference

### Standard Methods → HTTP

| Method | HTTP   | Path              | Idempotent | Related Rules                                                          |
| ------ | ------ | ----------------- | ---------- | ---------------------------------------------------------------------- |
| Get    | GET    | `/resources/{id}` | Yes        | `aip131/get-no-body`                                                   |
| List   | GET    | `/resources`      | Yes        | `aip158/list-paginated`, `aip132/has-filtering`, `aip132/has-ordering` |
| Create | POST   | `/resources`      | No\*       | `aip133/post-returns-201`, `aip155/idempotency-key`                    |
| Update | PATCH  | `/resources/{id}` | Yes        | `aip134/patch-over-put`                                                |
| Delete | DELETE | `/resources/{id}` | Yes        | `aip135/delete-idempotent`                                             |

\*Use Idempotency-Key header for safe retries

### Naming Rules (AIP-122)

- `/users`, `/orders`, `/products` (plural nouns)
- `/user`, `/order` (singular - triggers `aip122/plural-resources`)
- `/getUsers`, `/createOrder` (verbs - triggers `aip122/no-verbs`)
- `/users/{id}/orders` (nested ownership)

### Pagination (AIP-158)

Request: `?page_size=20&page_token=xxx`

Response:

```json
{
  "data": [...],
  "next_page_token": "yyy"
}
```

### Error Response (AIP-193)

```json
{
  "error": {
    "code": "INVALID_ARGUMENT",
    "message": "Human-readable message",
    "details": [...],
    "request_id": "req_abc123"
  }
}
```

### Fetch AIPs On Demand

For detailed guidance, fetch from:

- `https://google.aip.dev/{number}` (e.g., `/158` for pagination)
- Only fetch when user needs deeper explanation
