---
name: java-api-design-rest
description: Design REST APIs with strong resource modeling, pagination, filtering, error model, and versioning; produce an OpenAPI draft and controller/service contracts. Use when adding new endpoints or redesigning existing APIs.
license: Apache-2.0
compatibility: "Framework-agnostic Java backend; outputs include OpenAPI."
metadata:
  version: "0.1.0"
  tags: ["java", "rest", "api-design", "openapi", "pagination", "errors"]
---

# Java REST API Design

## Scope

In scope:

- Resource modeling (nouns, hierarchies, relationships).
- Endpoint design: methods, status codes, idempotency guidance.
- Pagination/filtering/sorting patterns and response shapes.
- Error model using Problem Details (RFC 9457 style).
- Versioning strategy and backward-compatibility rules.
- Produce an OpenAPI draft and implementation contracts (controller/service interfaces).

Out of scope:

- UI/client implementation.
- Authn/Authz deep design (only surface-level hooks unless requested).
- Full production hardening (rate limiting, WAF, etc.) unless requested.

## When to use

- Adding new endpoint(s).
- Redesigning a legacy API with inconsistent patterns.
- Preparing for public API exposure or multiple consumers.
- Improving developer experience: predictable errors, pagination, and docs.

## Inputs (required context)

- Business capability and use-cases (what users do, not just fields).
- Existing API patterns in the repo (if any).
- Data model constraints (IDs, uniqueness, relationships).
- Non-functional constraints: latency, payload limits, caching, consistency.

## Procedure (contract-first)

1) Model resources
   - Identify primary resources (nouns) and stable identifiers.
   - Define sub-resources and relationships only when they have clear ownership.
   - Decide representation: full vs summary vs expandable fields.

2) Define endpoints + semantics
   - GET collection/item, POST create, PUT replace, PATCH partial update, DELETE.
   - Ensure idempotency requirements are explicit (especially POST).
   - Choose status codes intentionally.

3) Pagination and filtering
   - Choose a pagination strategy:
     - Cursor/token-based for large mutable collections (recommended).
     - Offset-based only when stable ordering and costs are acceptable.
   - Define request params and response shape (including next token).
   - Ensure sorting/filtering are consistent across pages.

4) Error model (Problem Details)
   - Standardize error responses with fields:
     - type, title, status, detail, instance
   - Define stable error codes and a mapping table from exceptions to problem types.

5) Versioning & compatibility
   - Prefer backward-compatible changes.
   - Define a versioning strategy (path/header/media-type) and rules for breaking changes.

6) Produce OpenAPI draft
   - Write OpenAPI paths, schemas, responses (including error responses).
   - Include examples and common error cases.

7) Define implementation contracts
   - Define controller signatures (request/response DTOs).
   - Define service layer contracts (business interfaces).
   - Add minimal tests or contract checks if required.

## Outputs / Artifacts

- OpenAPI draft (YAML/JSON) with:
  - endpoints, schemas, pagination, errors
- Controller/service contracts (interfaces or skeletons)
- A short API change note:
  - breaking changes? migration?

## Definition of Done (DoD)

- [ ] Resources and endpoints follow a consistent naming scheme.
- [ ] Pagination strategy is documented and implemented in OpenAPI.
- [ ] Error model is standardized and includes machine-readable fields.
- [ ] OpenAPI draft validates structurally (basic sanity).
- [ ] Example requests/responses exist for happy path + common errors.

## Guardrails

- Do not leak internal exceptions/stack traces to clients.
- Do not introduce breaking changes without versioning/migration plan.
- Do not use ad-hoc pagination shapes; keep it consistent across endpoints.
- Require explicit confirmation for non-idempotent operations.

## Common failure modes & fixes

- Endpoint becomes "action soup" (/doThing) → refactor into resource modeling.
- Pagination breaks with filtering/sorting → ensure stable ordering and token binding.
- Errors inconsistent → enforce Problem Details and a shared error registry.

## References

- Use `templates/openapi/` for starter OAS files.
- Use `templates/errors/` for Problem Details examples.
- Use `references/` for detailed REST checklists and versioning guidance.
