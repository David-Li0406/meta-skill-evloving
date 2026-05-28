# Example: Backend Work Classification

## User Request
"Add a webhook endpoint that processes Stripe payments"

## Classification Output

### Keyword Analysis

| Keyword | Found | Weight |
|---------|-------|--------|
| webhook | ✅ | +3 BACKEND |
| endpoint | ✅ | +3 BACKEND |
| API | ❌ | - |
| Stripe | ✅ | +2 BACKEND (payment) |
| payments | ✅ | +2 BACKEND |

### Work Type Decision

```yaml
work_type: BACKEND
confidence: 0.95
reasoning: |
  - "webhook" and "endpoint" are strong backend indicators
  - "Stripe" and "payments" indicate server-side processing
  - No UI/component keywords detected
```

### Skills to Invoke

```yaml
skills_to_invoke:
  discipline:
    - superpowers:brainstorming
    - superpowers:test-driven-development
    - superpowers:verification-before-completion
  domain_specific:
    - architecture-patterns  # For Clean Architecture
  agents:
    - schema-validator  # If database involved
```

### Output to auto-context.yaml

```yaml
work_type: BACKEND
detected_at: "2025-01-18T10:00:00Z"
keywords_found:
  - webhook
  - endpoint
  - Stripe
  - payments
skills_to_invoke:
  discipline:
    - superpowers:brainstorming
    - superpowers:test-driven-development
  domain_specific:
    - architecture-patterns
special_considerations:
  - payment_processing: true  # Triggers extra security review
  - webhook_verification: true  # Stripe signature validation needed
```
