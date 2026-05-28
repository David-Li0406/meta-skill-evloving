# Integration Domain Invariants

Extends: [[system-invariants]]
Domain: APIs, webhooks, third-party services, external integrations

---

## When to Use

Load this domain for:
- REST/GraphQL APIs
- Webhook implementations
- Third-party service integrations
- OAuth/authentication flows
- Payment gateway integrations
- External data sources

---

## Domain Invariants (27-30)

### 27. API Versioning Must Be Explicit

**Principle**: Every API endpoint must declare version and deprecation strategy

**Violation**: Unversioned endpoints, implicit breaking changes

**Examples**:
- ❌ "Create user endpoint"
- ❌ "Update API response format"
- ❌ "Add new field to payload"
- ✅ "POST /v2/users: version_header(X-API-Version) + sunset_date(v1: 2025-06-01) + migration_guide_url"
- ✅ "Response format change: v2_only + v1_unchanged + 90_day_deprecation_notice + changelog_entry"
- ✅ "New field: additive_only + nullable_for_backwards_compat + documented_in_changelog"

**Enforcement**: API changes must specify: version + backwards_compatibility + deprecation_timeline → Otherwise REJECT

---

### 28. Rate Limits Must Be Declared

**Principle**: Every external call must specify rate handling

**Violation**: Unbounded API calls, no backoff strategy

**Examples**:
- ❌ "Call external API"
- ❌ "Fetch data from service"
- ❌ "Send webhook notifications"
- ✅ "External API: 100_req/min + exponential_backoff(1s,2s,4s,max_30s) + circuit_breaker(5_failures) + fallback(cached_data)"
- ✅ "Data fetch: rate_limit_aware + 429_handling(retry_after_header) + queue_overflow(drop_oldest)"
- ✅ "Webhooks: batch_max_100 + retry_3x_with_backoff + dead_letter_queue + manual_retry_ui"

**Enforcement**: External calls must specify: rate_limit + backoff_strategy + failure_handling → Otherwise REJECT

---

### 29. Idempotency Must Be Guaranteed

**Principle**: Retryable operations must produce same result

**Violation**: Non-idempotent mutations, duplicate side effects

**Examples**:
- ❌ "Create order on submit"
- ❌ "Send confirmation email"
- ❌ "Charge payment"
- ✅ "Create order: idempotency_key(client_generated_uuid) + dedup_window(24h) + same_response_on_retry"
- ✅ "Confirmation email: idempotency_key(order_id+email_type) + sent_flag_check + no_duplicate_sends"
- ✅ "Payment charge: idempotency_key(order_id) + stripe_idempotency_header + verify_before_retry"

**Enforcement**: Mutating operations must specify: idempotency_mechanism + dedup_strategy + retry_behavior → Otherwise REJECT

---

### 30. Timeout Budgets Must Be Allocated

**Principle**: Request chains must have explicit timeout distribution

**Violation**: Unbounded waits, timeout cascades

**Examples**:
- ❌ "Call service A then B then C"
- ❌ "Wait for external response"
- ❌ "Aggregate from multiple sources"
- ✅ "Chain A→B→C: total_budget(5s) → A(2s) → B(2s) → C(1s) + fail_fast_on_timeout + partial_response_ok"
- ✅ "External response: timeout(3s) + cancel_on_timeout + return_cached_or_error"
- ✅ "Multi-source aggregation: parallel_fetch + per_source_timeout(2s) + return_available_on_any_timeout"

**Enforcement**: Request chains must specify: total_budget + per_hop_allocation + timeout_behavior → Otherwise REJECT

---

## Integration-Specific Sub-Invariants

### 30a. Authentication Token Management

- Tokens must have explicit expiry handling
- Refresh logic must be proactive (before expiry)
- Failed refresh must trigger re-authentication flow
- Token storage must be secure (never in logs/URLs)

### 30b. Webhook Delivery Guarantees

- Delivery semantics must be declared (at-least-once, at-most-once)
- Signature verification required for incoming webhooks
- Payload schema versioning required
- Retry policy must be documented

### 30c. Error Response Standards

- Error responses must follow consistent schema
- Error codes must be documented and stable
- User-facing vs internal errors must be distinguished
- Correlation IDs required for debugging

### 30d. Contract Testing

- API contracts must be testable (OpenAPI, GraphQL schema)
- Breaking changes must fail contract tests
- Consumer-driven contracts for critical integrations
- Mock servers for development/testing

---

## Quick Reference

| # | Invariant | Key Test |
|---|-----------|----------|
| 27 | API Versioning Must Be Explicit | Endpoints have version + deprecation plan |
| 28 | Rate Limits Must Be Declared | External calls have limits + backoff |
| 29 | Idempotency Must Be Guaranteed | Mutations have idempotency keys |
| 30 | Timeout Budgets Must Be Allocated | Chains have time budgets per hop |

---

*Domain: Integration*
*Invariants: 27-30 (plus sub-invariants)*
*Use with: Core invariants 1-10*
*Often combined with: data-architecture.md*
