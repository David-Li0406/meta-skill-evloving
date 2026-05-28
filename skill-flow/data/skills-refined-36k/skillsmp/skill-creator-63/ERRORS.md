# Errors

This file is an example placeholder referenced by the Skill Creator skill.

## Error Taxonomy

- **User errors** (4xx): validation, auth, not found
- **Retryable errors**: timeouts, transient dependency failures
- **Non-retryable errors**: invariant violations, bad inputs

## API Error Shape

Define a consistent response structure:

- `code`: stable machine-readable identifier
- `message`: human-friendly summary
- `details`: optional structured fields
- `requestId`: correlation id

## Retries & Backoff

- Default retry policy for transient errors
- Exponential backoff with jitter
- Max attempts and timeout budgets

## Logging

- What to log (context, requestId)
- What not to log (secrets, PII)
