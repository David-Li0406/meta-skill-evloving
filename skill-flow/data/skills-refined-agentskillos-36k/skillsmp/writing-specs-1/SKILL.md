---
name: writing-specs
description: Writes specification documents following SSOT principles. Use when creating, updating, or reviewing specs in specs/ directory.
---

# Writing Specifications Guide

This document defines how to write specification documents for a software project. Specs serve as the **Single Source of Truth (SSOT)** for how each component works.

## Core Concepts

### Terminology

| Term | Definition |
|------|------------|
| **Job to be Done (JTBD)** | High-level user need or outcome |
| **Topic of Concern** | A distinct aspect/component within a JTBD |
| **Spec** | Requirements doc for one topic of concern |
| **Task** | Unit of work derived from comparing specs to code |
| **Component** | Module, service, job, UI screen, or other unit |
| **Interface/Contract** | API surface: endpoints, events, public functions |
| **Non-functional Requirements** | Performance, security, reliability constraints |

### Relationships

```
1 JTBD → multiple topics of concern
1 topic of concern → 1 spec
1 spec → multiple tasks
```

**Example (CLI Tool):**
- JTBD: "Manage skills across AI agents"
- Topics: skill model, agent model, scanner, installation, removal
- Each topic → one spec file

**Example (Web Service):**
- JTBD: "Process customer payments"
- Topics: payment validation, payment processing, refund handling, receipt generation
- Each topic → one spec file

**Example (Library):**
- JTBD: "Parse configuration files"
- Topics: file loading, schema validation, type conversion, error reporting
- Each topic → one spec file

## The One-Sentence Rule

Every spec must pass the **"One Sentence Without And" test**.

### The Test

Can you describe the topic in one sentence without conjoining *distinct capabilities*?

**✓ Valid examples:**
- "The skill scanner discovers installed skills across agent directories."
- "Token authentication validates bearer tokens for API requests."
- "Email dispatcher sends queued emails with retry logic."
- "Query parser converts user query strings into an AST."

**✗ Invalid examples:**
- "The user system handles authentication, profiles, and billing." → 3 topics
- "CLI interface handles argument parsing and output formatting." → 2 topics
- "Payment service processes payments and sends receipts." → 2 topics

### Clarification on "And"

Avoid "and" that joins **separate responsibilities**. If removing one clause doesn't change the other's meaning, split.

**Allow "and" for tightly coupled sub-steps:**
- ✓ "Validates and normalizes email addresses" (single responsibility)
- ✓ "Parses and caches configuration" (if caching is integral to parsing)

**Split when independent:**
- ✗ "Validates input and logs metrics" → split into validation spec + observability spec

### When to Split

| Before (Too Broad) | After (Properly Scoped) |
|--------------------|-------------------------|
| `user-service.md` (auth + profile + billing) | `authentication.md`, `user-profile.md`, `billing.md` |
| `api-gateway.md` (routing + auth + rate-limit) | `request-routing.md`, `api-authentication.md`, `rate-limiting.md` |
| `cli-interface.md` (parsing + output) | `cli-schema.md`, `cli-output.md` |

## Spec File Structure

Every spec follows this template:

```markdown
# [Topic Name] Spec

## One-Sentence Description

[Single sentence describing the topic - must pass the "no and" test]

## Overview

[2-3 sentences providing context. What problem does this solve? Where does it fit in the architecture?]

## [Primary Technical Section]

[Main content varies by spec type - see "Primary Sections by Project Type"]

## [Additional Sections as Needed]

[Pick from optional sections based on relevance]

## Acceptance Criteria

[Observable outcomes that indicate correct behavior - used for test derivation]

## Error Handling

[What errors can occur and how they're handled]

## Dependencies

[What this component imports/uses]

## Used By

[What components use this]
```

## Primary Sections by Project Type

Choose the primary technical section based on your component type:

| Project Type | Primary Section | Key Content |
|--------------|-----------------|-------------|
| **Library** | Public API | Functions, types, behavioral contracts, thread-safety |
| **CLI Tool** | Commands / Options | Subcommands, flags, arguments, exit codes |
| **Web API / Service** | Endpoints | Routes, methods, auth, request/response schemas, status codes |
| **Microservice** | Service Contract | RPC/API, events produced/consumed, dependencies |
| **Background Job** | Job Behavior | Triggers, processing logic, retry policy, idempotency |
| **Mobile / UI** | User Flows | Screens, states, transitions, offline behavior |
| **Event Handler** | Event Contract | Event schema, ordering, idempotency, error handling |

## Section Guidelines

### One-Sentence Description

- Exactly one sentence
- No "and" connecting distinct capabilities
- No parenthetical scope expansion
- Use active verbs: "defines", "discovers", "manages", "creates", "validates", "processes"

**Good:**
```markdown
## One-Sentence Description

Token authentication validates bearer tokens for API requests.
```

**Bad:**
```markdown
## One-Sentence Description

Token authentication validates bearer tokens and manages user sessions and handles token refresh.
```

### Overview

- 2-3 sentences maximum
- Explain the "why" not just the "what"
- Reference the component's role in the larger system

```markdown
## Overview

The payment processor handles the core transaction logic for customer purchases. It validates payment methods, communicates with payment providers, and records transaction outcomes. Failed transactions trigger automatic retry with exponential backoff.
```

### Technical Sections

Name sections based on content type:

| Content Type | Section Name |
|--------------|--------------|
| Data models / Types | "Data Structures" or "Data Model" |
| Functions / Methods | "Functions", "API", or "Public Interface" |
| HTTP endpoints | "Endpoints" |
| Events / Messages | "Events" or "Message Contracts" |
| Step-by-step process | "[Action] Process" (e.g., "Payment Process") |
| Rules / Constraints | "[Topic] Rules" (e.g., "Validation Rules") |
| Configuration | "Configuration Options" |
| CLI flags | "Command Options" |
| Verifiable outcomes | "Acceptance Criteria" |

### Acceptance Criteria

Acceptance criteria define **observable, verifiable outcomes** that indicate the component works correctly. They become the foundation for test requirements during plan construction.

**Format requirements:**
- Must be a **bullet list** (not paragraphs or prose)
- Each bullet is one testable criterion
- Tasks copy bullets verbatim - format consistency enables this

**Guidelines:**
- Focus on **behavior** (what happens), not **implementation** (how it's built)
- Each criterion should be independently testable
- Use concrete, measurable terms
- Include an **observable** in each bullet (returns X, exits code Y, completes in Z seconds)

**Good criteria:**
```markdown
## Acceptance Criteria

- Scanning 1000 skill directories completes in under 2 seconds
- Modified SKILL.md files invalidate their cache entries
- `--no-cache` flag forces fresh scan regardless of cache state
- Broken symlinks are reported in scan results, not silently skipped
```

**Bad criteria:**
```markdown
## Acceptance Criteria

- Uses efficient data structures (implementation detail)
- Code is well-organized (subjective)
- Cache works properly (vague)
- Is secure (no observable)
- Handles errors gracefully (unmeasurable)
```

**Deriving criteria:**

Acceptance criteria are required. When writing or updating a spec, derive them from:
- Process steps that describe outcomes
- Error handling behavior
- API behavioral descriptions
- Non-functional requirements (performance, security)

Explicitly list the derived criteria in the Acceptance Criteria section.

> **Note for planning/implementation agents:** Deriving criteria is part of **writing specs**. During gap analysis and implementation, you must **not** derive or invent acceptance criteria. Copy verbatim from the spec's AC section and report missing/incomplete AC as Spec Issues.

### Data Structure Documentation

Use tables for type fields:

```markdown
## Data Model

### PaymentRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `amount` | `Money` | Yes | Payment amount with currency |
| `method` | `PaymentMethod` | Yes | Card, bank transfer, or wallet |
| `idempotency_key` | `String` | Yes | Client-provided unique key |
| `metadata` | `Map<String, String>` | No | Arbitrary key-value pairs |
```

### Function / API Documentation

Document public interfaces with signature and behavior:

**Example (Library function):**
```markdown
### `validate_email(input: &str) -> Result<Email, ValidationError>`

Validates and normalizes an email address.

**Behavior:**
- Trims whitespace
- Converts to lowercase
- Validates format per RFC 5322

**Errors:**
- `ValidationError::Empty` - input is blank
- `ValidationError::InvalidFormat` - doesn't match email pattern
```

**Example (HTTP endpoint):**
```markdown
### `POST /payments`

Creates a new payment.

**Authentication:** Bearer token required

**Request:**
| Field | Type | Required |
|-------|------|----------|
| `amount` | integer (cents) | Yes |
| `currency` | string (ISO 4217) | Yes |
| `source` | string (payment method ID) | Yes |

**Response (201):**
| Field | Type |
|-------|------|
| `id` | string |
| `status` | "pending" \| "succeeded" \| "failed" |

**Errors:**
- `400` - Invalid request body
- `402` - Payment failed
- `409` - Duplicate idempotency key
```

### Process Documentation

Use numbered steps for multi-step operations:

```markdown
## Payment Process

1. **Validate request** - Check required fields, validate amounts
2. **Check idempotency** - Return cached result if key exists
3. **Authorize payment** - Call payment provider API
4. **Record transaction** - Persist to database
5. **Emit event** - Publish `payment.completed` or `payment.failed`
6. **Return response** - Send result to caller
```

### Dependencies and Used By

Always include these sections for traceability:

```markdown
## Dependencies

- `PaymentProvider` - external payment gateway client
- `TransactionRepository` - database access for transactions
- `EventBus` - publishes payment events
- `IdempotencyStore` - caches idempotency keys

## Used By

- `CheckoutController` - initiates payments from checkout flow
- `SubscriptionService` - processes recurring payments
- `RefundService` - references original payment
```

## Optional Sections

Include these based on relevance to your component:

### Interface / Contract
- Endpoints, RPC methods, events, public functions
- Request/response schemas, payload formats
- Versioning and compatibility guarantees

### Data Model
- Entities, schemas, validation rules
- Database tables, indexes
- Migration considerations

### State and Invariants
- What must always be true
- Idempotency keys, uniqueness constraints
- Consistency requirements

### Security and Privacy
- Authentication and authorization requirements
- Secrets handling
- PII and data classification
- Threat considerations

### Performance and Limits
- Latency and throughput targets
- Payload size limits
- Rate limiting rules
- Resource budgets

### Reliability
- Retry policies and backoff
- Timeout configuration
- Circuit breaker behavior
- Failure modes and fallbacks

### Observability
- Key metrics to emit
- Log messages and levels
- Trace spans
- Alerting thresholds

### Compatibility
- API versioning strategy
- Deprecation policy
- Backward/forward compatibility

### Rollout Plan
- Feature flags
- Migration steps
- Monitoring during launch
- Rollback procedure

## Spec Categories

Organize specs into logical categories:

| Category | Examples |
|----------|----------|
| **Core Domain** | Data models, entities, business rules |
| **API / Interface** | Endpoints, commands, public functions |
| **Processing** | Jobs, workers, event handlers, workflows |
| **Infrastructure** | Configuration, caching, persistence |
| **Integration** | External services, third-party APIs |
| **Cross-Cutting** | Authentication, logging, error handling |
| **Build and Deploy** | Platform constraints, CI/CD, environments |

## Writing from Implementation

When creating specs from existing code:

### 1. Identify Public Surfaces

Focus on externally visible interfaces:
- Public functions, types, traits
- API endpoints, RPC methods
- CLI commands and flags
- Events produced or consumed
- Configuration options

### 2. Document Actual Behavior

**Do:**
- Document what the code actually does
- Include edge cases found in the code
- Note platform-specific behavior
- Reference error types and conditions

**Don't:**
- Document aspirational features
- Assume behavior without reading code
- Copy comments verbatim (rewrite for clarity)

### 3. Verify Accuracy

Cross-reference with:
- Unit tests (show expected behavior)
- Integration tests (show usage patterns)
- Error types (show failure modes)
- API documentation (if exists)

## Maintaining Specs

### When to Update

Update specs when:
- Adding new public API
- Changing function signatures or schemas
- Modifying behavior
- Adding error conditions
- Changing dependencies

### Accuracy Checks

Periodically verify:
- [ ] Every public interface is mapped to a spec
- [ ] One-sentence descriptions have no "and" (joining distinct concerns)
- [ ] "Used By" references point to real components
- [ ] Error conditions match actual implementation
- [ ] Dependencies list is current

### Architecture Mapping

Maintain a mapping in your SSOT index (e.g., `specs/README.md`):

```
specs/
├── Core Domain
│   ├── user-model.md           → src/models/user.ts
│   ├── payment-model.md        → src/models/payment.ts
│   └── error-types.md          → src/errors/
├── API
│   ├── auth-endpoints.md       → src/api/auth/
│   ├── payment-endpoints.md    → src/api/payments/
│   └── webhook-handlers.md     → src/webhooks/
├── ...
```

## Common Mistakes

### 1. Combining Multiple Concerns

**Wrong:** One spec covering payments, refunds, and receipts

**Right:** Separate specs for each capability

### 2. Vague One-Sentence Descriptions

**Wrong:** "Handles various payment operations"

**Right:** "Processes customer payments through external providers"

### 3. Missing Error Documentation

**Wrong:** Only documenting happy path

**Right:** Including all error variants and when they occur

### 4. Stale References

**Wrong:** Referencing endpoints or modules that don't exist

**Right:** Verifying all references against current codebase

### 5. Implementation Details in Overview

**Wrong:** Overview contains code examples and internal logic

**Right:** Overview explains purpose; details go in technical sections

### 6. Mixing Concerns in One Spec

**Wrong:** Security requirements scattered across all specs

**Right:** Dedicated cross-cutting specs (auth spec, error model spec) that others reference

## Example Specs

### Example: Library Function Spec

```markdown
# Email Validation Spec

## One-Sentence Description

Email validation verifies and normalizes email address inputs.

## Overview

This module provides email validation for user registration and contact forms. It enforces RFC 5322 format compliance and normalizes addresses to lowercase for consistent storage.

## Public API

### `validate(input: &str) -> Result<Email, ValidationError>`

Validates and normalizes an email address.

**Behavior:**
- Trims leading/trailing whitespace
- Converts to lowercase
- Validates format per RFC 5322 (simplified)
- Returns normalized `Email` type

### `Email` Type

| Field | Type | Description |
|-------|------|-------------|
| `local` | `String` | Part before @ |
| `domain` | `String` | Part after @ |

## Validation Rules

- Maximum length: 254 characters
- Must contain exactly one `@`
- Local part: 1-64 characters
- Domain: valid hostname format

## Acceptance Criteria

- Valid email "User@Example.COM" normalizes to "user@example.com"
- Email with leading/trailing whitespace is accepted after trimming
- Email exceeding 254 characters returns `TooLong` error
- Email without `@` returns `InvalidFormat` error
- Empty string returns `Empty` error

## Error Handling

| Error | Cause |
|-------|-------|
| `ValidationError::Empty` | Input is blank after trimming |
| `ValidationError::TooLong` | Exceeds 254 characters |
| `ValidationError::InvalidFormat` | Doesn't match email pattern |

## Dependencies

- `regex` - pattern matching

## Used By

- `UserRegistration` - validates signup emails
- `ContactForm` - validates contact submissions
- `NotificationService` - validates recipient addresses
```

### Example: HTTP API Spec

```markdown
# Payment Processing Spec

## One-Sentence Description

Payment processing handles customer transactions through external payment providers.

## Overview

This service orchestrates payment transactions from authorization through capture. It integrates with Stripe as the primary payment provider and maintains idempotency for safe retries.

## Endpoints

### `POST /v1/payments`

Creates a new payment.

**Authentication:** API key (header: `X-API-Key`)

**Request:**
```json
{
  "amount": 1000,
  "currency": "usd",
  "payment_method": "pm_xxx",
  "idempotency_key": "unique-key-123"
}
```

**Response (201):**
```json
{
  "id": "pay_xxx",
  "status": "succeeded",
  "amount": 1000,
  "currency": "usd"
}
```

**Errors:**
| Status | Code | Description |
|--------|------|-------------|
| 400 | `invalid_request` | Missing or invalid fields |
| 402 | `payment_failed` | Payment was declined |
| 409 | `idempotency_conflict` | Key reused with different params |

## Payment Process

1. Validate request schema
2. Check idempotency key → return cached result if exists
3. Create payment intent with Stripe
4. Store transaction record
5. Cache idempotency result
6. Emit `payment.completed` event
7. Return response

## Idempotency

- Keys are valid for 24 hours
- Same key + same params → returns cached result
- Same key + different params → returns 409 error

## Error Handling

- Provider errors are mapped to API error codes
- Transient failures trigger automatic retry (3 attempts, exponential backoff)
- All errors are logged with correlation ID

## Dependencies

- `StripeClient` - payment provider integration
- `PaymentRepository` - transaction persistence
- `IdempotencyCache` - Redis-backed key cache
- `EventPublisher` - emits payment events

## Used By

- `CheckoutController` - web checkout flow
- `MobilePaymentHandler` - mobile app payments
- `SubscriptionRenewal` - recurring charges
```

### Example: Background Job Spec

```markdown
# Email Dispatch Spec

## One-Sentence Description

Email dispatch sends queued emails through the configured email provider.

## Overview

This worker processes the email queue, sending messages through SendGrid. It implements retry with exponential backoff and ensures exactly-once delivery through idempotency tracking.

## Job Behavior

**Trigger:** Polls queue every 5 seconds (configurable)

**Processing:**
1. Dequeue batch of up to 10 messages
2. For each message:
   - Check if already sent (idempotency)
   - Render template with variables
   - Send via SendGrid API
   - Mark as sent or failed
3. Acknowledge processed messages

## Retry Policy

| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | 1 minute |
| 3 | 5 minutes |
| 4 | 30 minutes |
| 5 | Move to dead letter queue |

## Idempotency

- Each email has unique `message_id`
- Sent messages are tracked in Redis (TTL: 7 days)
- Duplicate delivery is prevented by checking before send

## Error Handling

| Error Type | Action |
|------------|--------|
| Rate limit (429) | Pause worker for 60s, retry |
| Invalid recipient | Mark failed, no retry |
| Provider error (5xx) | Retry with backoff |
| Template error | Mark failed, alert |

## Dependencies

- `EmailQueue` - SQS queue client
- `SendGridClient` - email provider
- `TemplateEngine` - renders email content
- `IdempotencyStore` - tracks sent messages

## Used By

- `NotificationService` - enqueues transactional emails
- `MarketingCampaigns` - enqueues bulk emails
```

## Checklist for New Specs

Before finalizing a spec, verify:

**Required sections:**
- [ ] One-Sentence Description - passes "no and" test
- [ ] Overview - 2-3 sentences
- [ ] Primary technical section - matches component type
- [ ] Acceptance Criteria - present and complete
- [ ] Error Handling - all error cases listed
- [ ] Dependencies - what this uses
- [ ] Used By - what uses this

**Acceptance Criteria quality:**
- [ ] Formatted as bullet list (not prose)
- [ ] Each bullet has one observable outcome
- [ ] No implementation details (how to build)
- [ ] No subjective terms (well-organized, clean, robust)
- [ ] No vague outcomes (works properly, handles correctly)
- [ ] Measurable where applicable (time, count, exit code)

**Integration:**
- [ ] File is added to SSOT index
- [ ] Architecture mapping is updated
- [ ] Cross-references to other specs are explicit

## Cross-Cutting Specs

For concerns that span multiple components, create dedicated cross-cutting specs:

| Spec | Covers |
|------|--------|
| `error-model.md` | Standard error types, codes, formats |
| `authentication.md` | Auth mechanisms, token formats, session handling |
| `authorization.md` | Permission model, role definitions, access control |
| `observability.md` | Logging standards, metrics, tracing conventions |
| `api-conventions.md` | Naming, versioning, pagination, rate limiting |

Other specs reference these rather than duplicating the content:

```markdown
## Security

See [authentication.md](authentication.md) for token validation requirements.
```
