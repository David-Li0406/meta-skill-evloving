---
name: api-design
description: Use this skill when designing or reviewing APIs - REST, GraphQL, gRPC, or any programmatic interface. Applies API design thinking focused on contracts, ergonomics, and evolution to specifications, designs, and implementations.
version: 0.1.0
---

# API Design

## When to Apply

Use this skill when the system involves:
- Public or internal APIs
- REST, GraphQL, or gRPC services
- SDK or library interfaces
- Webhooks or callbacks
- API versioning and evolution
- Third-party integrations

## Mindset

API designers think from the consumer's perspective and design for the long term.

**Questions to always ask:**
- Who are the consumers? What are they trying to accomplish?
- What's the simplest way to do the common case?
- How will this evolve? What's the versioning strategy?
- What happens when things go wrong? How do consumers recover?
- Is this consistent with our other APIs?
- How do consumers discover and learn this API?
- What's the pagination strategy for lists?

**Assumptions to challenge:**
- "It mirrors our internal model" - Consumers don't care about your internals.
- "They'll read the docs" - APIs should be intuitive. Good docs are backup, not primary.
- "We can change it later" - Breaking changes are expensive. Design carefully upfront.
- "More options are better" - Complexity has cost. Start minimal.
- "REST requires X" - REST is flexible. Choose what serves consumers.
- "They'll handle errors" - Make errors actionable and recoverable.

## Practices

### Resource Design
Model resources around consumer needs, not internal tables. Use nouns for resources, verbs for actions (when necessary). Keep URLs predictable and hierarchical. **Don't** expose database structure, use verbs in resource names, or create deeply nested URLs.

### Consistency
Use consistent naming conventions. Same patterns for pagination, filtering, errors. Consistent use of HTTP methods and status codes. **Don't** have different conventions per endpoint, surprise consumers with inconsistencies, or use status codes incorrectly.

### Minimal Surface
Start with the minimum viable API. Add fields and endpoints based on real needs. Every addition is a commitment. **Don't** expose everything just in case, add optional parameters preemptively, or treat API surface as free.

### Error Responses
Return structured errors with code, message, and details. Make errors actionable (tell them what to do). Use appropriate HTTP status codes. Include request IDs for debugging. **Don't** return generic 500s, expose stack traces, or use 200 for errors.

### Pagination
Use cursor-based pagination for large or changing datasets. Include total counts only when cheap. Provide clear next/prev links. **Don't** use offset pagination for large datasets, return unbounded lists, or make pagination optional for lists.

### Versioning
Choose a strategy (URL path, header, content negotiation) and stick to it. Support old versions for documented periods. Communicate deprecation clearly. **Don't** change behavior without versioning, drop old versions without warning, or mix versioning strategies.

### Request/Response Design
Use consistent field naming (camelCase or snake_case, pick one). Include created/updated timestamps. Use ISO 8601 for dates. Nest related objects logically. **Don't** mix naming conventions, use ambiguous date formats, or return flat structures when hierarchy is clearer.

### Documentation
Document all endpoints, fields, and error codes. Provide examples for common use cases. Keep docs in sync with implementation. **Don't** have undocumented fields, examples that don't work, or let docs drift from reality.

## Vocabulary

Use precise terminology:

| Instead of | Say |
|------------|-----|
| "REST API" | "REST-ish" / "RESTful with X constraints" / "JSON over HTTP" |
| "versioned" | "URL versioned (/v1/)" / "header versioned" / "content negotiated" |
| "paginated" | "cursor-based" / "offset-based" / "keyset pagination" |
| "authenticated" | "Bearer token" / "API key" / "OAuth2" |
| "error" | "4xx client error" / "5xx server error" / "structured error response" |
| "fast" | "< 200ms p99" / "cacheable for X seconds" |

## SDD Integration

**During Specification:**
- Identify API consumers and their use cases
- Define the primary jobs-to-be-done
- Establish consistency requirements with existing APIs
- Clarify versioning and deprecation expectations

**During Design:**
- Design from consumer use cases, not internal models
- Document resource structure and relationships
- Specify error responses for each failure mode
- Plan pagination strategy for list endpoints
- Define versioning approach

**During Review:**
- Verify API serves consumer use cases simply
- Check consistency with existing API conventions
- Confirm error responses are actionable
- Validate pagination is appropriate for each list
- Ensure documentation matches implementation
