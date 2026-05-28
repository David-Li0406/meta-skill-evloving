---
name: agent-ops-api-review
description: Use this skill when you need to perform a thorough audit of API endpoints to ensure they align with their specifications and behave correctly.
---

# Skill body

## Purpose

Perform a **critical, thorough, evidence-based audit** of an API implementation and its endpoints. Verify that the API:
- Produces the **expected outcomes**
- Behaves correctly across success and failure paths
- Matches its **OpenAPI/Swagger contract**
- Has **adequate tests** to prove required behavior

**No credit without evidence.** Spec is not proof. Tests are not proof unless they assert required outcomes.

## Triggers

- Project contains API endpoints (REST, GraphQL, gRPC)
- OpenAPI/Swagger spec exists
- User requests API review
- `agent-ops-critical-review` detects API patterns

## Inputs

You will be given some or all of:
- Repository / codebase / diff
- OpenAPI/Swagger spec (file or generated)
- Unit test suite
- Optional: CI logs, runtime logs, sample requests/responses

If the OpenAPI spec is not available, identify where it should exist and treat missing spec as a finding.

## Non-Negotiable Rules

- **No credit without evidence**
- **Spec is not proof** — implementation must match it
- **Tests are not proof** unless they assert required outcomes and would fail on regression
- Every claim must cite **concrete locations** (files/endpoints/tests/spec paths)

## Mandatory Audit Outputs

### 1. Endpoint Inventory

List all endpoints, grouped by resource/domain:
- Method + route + auth requirement
- Request/response shape references (OpenAPI path refs if available)

### 2. Contract Alignment Matrix

For each endpoint:

| Endpoint | Spec Ref | Impl Ref | Tests Ref | Status |
|----------|----------|----------|-----------|--------|
| GET /users | paths./users.get | user_router.py:45 | test_users.py:12 | aligned |
| POST /users | paths./users.post | user_router.py:78 | — | untested |

Status values: `aligned | partially_aligned | misaligned | unverifiable`

### 3. Findings

Each finding must include:
- **Severity**: `must_fix | strongly_recommended | discuss`
- **Category**: Which audit axis (A1-A10)
- **Endpoint(s) affected**: List of endpoints related to the finding