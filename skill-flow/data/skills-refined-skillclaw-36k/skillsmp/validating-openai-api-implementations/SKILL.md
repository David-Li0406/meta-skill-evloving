---
name: validating-openai-api-implementations
description: Use to review OpenAI API integrations for correctness (endpoints, params, auth, response handling) and robustness.
---

## Review workflow

1. Identify the integration surface (SDK vs raw HTTP, endpoints used).
2. Verify authentication handling (no hard-coded secrets; env-based; safe logging).
3. Check request construction:
   - required parameters present
   - types and shapes correct
   - timeouts/retries reasonable
4. Check response handling:
   - error paths surfaced to caller
   - rate-limit/backoff behavior
   - schema changes handled defensively
5. Validate with a minimal smoke test (or dry-run) and document expected outputs.
