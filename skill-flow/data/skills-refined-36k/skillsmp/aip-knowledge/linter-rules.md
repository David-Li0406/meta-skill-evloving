# AIP Linter Rules Reference

The AIP reviewer includes 17 automated rules across 6 categories.

## Naming (AIP-122)

| Rule ID                    | Severity   | What It Checks                                                  |
| -------------------------- | ---------- | --------------------------------------------------------------- |
| `aip122/plural-resources`  | warning    | Resource paths use plural nouns                                 |
| `aip122/no-verbs`          | error      | Paths contain nouns, not verbs                                  |
| `aip122/consistent-casing` | warning    | Path segments use consistent casing (kebab, snake, camel)       |
| `aip122/nested-ownership`  | suggestion | Nested resource params have descriptive names (not just `{id}`) |

## Standard Methods (AIP-131 to 135)

| Rule ID                    | Severity   | What It Checks                                     |
| -------------------------- | ---------- | -------------------------------------------------- |
| `aip131/get-no-body`       | error      | GET requests have no request body                  |
| `aip133/post-returns-201`  | suggestion | POST returns 201 Created or 202 Accepted           |
| `aip134/patch-over-put`    | suggestion | PATCH available for partial updates (not just PUT) |
| `aip135/delete-idempotent` | warning    | DELETE has no body and uses standard status codes  |

## Pagination (AIP-158)

| Rule ID                      | Severity   | What It Checks                                      |
| ---------------------------- | ---------- | --------------------------------------------------- |
| `aip158/list-paginated`      | warning    | List endpoints have page_size and page_token params |
| `aip158/max-page-size`       | suggestion | page_size param has maximum constraint              |
| `aip158/response-next-token` | warning    | Paginated responses include next_page_token field   |

## Filtering (AIP-132, 160)

| Rule ID                | Severity   | What It Checks                            |
| ---------------------- | ---------- | ----------------------------------------- |
| `aip132/has-filtering` | suggestion | List endpoints document filter parameters |
| `aip132/has-ordering`  | suggestion | List endpoints support order_by parameter |

## Errors (AIP-193)

| Rule ID                       | Severity   | What It Checks                                            |
| ----------------------------- | ---------- | --------------------------------------------------------- |
| `aip193/schema-defined`       | warning    | Error schema defined in components                        |
| `aip193/responses-documented` | suggestion | Operations document error responses                       |
| `aip193/standard-codes`       | suggestion | Standard HTTP error codes used (400, 401, 403, 404, etc.) |

## Idempotency (AIP-155)

| Rule ID                  | Severity   | What It Checks                               |
| ------------------------ | ---------- | -------------------------------------------- |
| `aip155/idempotency-key` | suggestion | POST endpoints accept Idempotency-Key header |

## Skipping Rules

To skip specific rules during review:

```bash
aip-review spec.yaml --skip-rules aip158/max-page-size
aip-review spec.yaml --skip-rules aip122/plural-resources,aip193/standard-codes
```

## Topics Without Automated Rules

The following topics have detailed reference documentation but no automated linter rules yet:

- **Field Masks** (`field-masks.md`) - AIP-134 partial update patterns (only `aip134/patch-over-put` checks for PATCH availability)
- **Batch Operations** (`batch.md`) - AIP-231+ batch patterns
- **Long-Running Operations** (`lro.md`) - AIP-151, 155 async patterns
- **Proto → REST Mapping** (`rest-mapping.md`) - Translation guide
