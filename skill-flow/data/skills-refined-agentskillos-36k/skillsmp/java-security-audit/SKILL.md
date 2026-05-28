---
name: java-security-audit
description: Perform a defensive security audit for Java backend services: input validation, SSRF, deserialization risks, secrets hygiene, and authz correctness. Use before release, after incidents, or during pen-test remediation. Output a findings report with mitigations and tests.
license: CC-BY-4.0
compatibility:
  jdk: "any"
metadata:
  owner: security-platform
  version: "0.1.0"
  tags: [java, security, audit, owasp, asvs, ssrf, authz]
---

# Java Security Audit (Defensive Threat Review)

## Purpose

This skill is a defensive audit playbook. It helps you:

- identify security risks early
- produce a clear findings report (severity + mitigation)
- add tests to prevent regressions

It does NOT teach exploitation. Keep all work within approved security processes.

## Scope (focus areas)

1) Input validation & canonicalization
2) Authorization (authz) correctness
3) SSRF risk controls (defensive)
4) Unsafe deserialization risk controls
5) Secrets & sensitive data hygiene (logs, configs, repos)
6) Dependency/Supply-chain risks (basic SCA hygiene)

## When to use

- Before release / major feature launch
- After a security incident or bug report
- During pen-test remediation
- Whenever you introduce:
  - new endpoints, file upload, URL fetching, webhook, templating
  - new authz rules or roles
  - new serialization formats or object mappers
  - new dependencies

## Step-by-step audit workflow

### Step 1: Build a quick system map (30–60 minutes)

Record:

- entry points:
  - REST endpoints, gRPC methods, message handlers, scheduled jobs
- data stores:
  - DB tables/collections, caches, object storage
- sensitive assets:
  - PII, tokens, credentials, payment identifiers
- trust boundaries:
  - internal vs external callers
  - service-to-service calls
  - admin endpoints

Deliverable:

- a short “security context” note in the report

### Step 2: Apply OWASP Top 10 lens

Map features and entry points to common risk categories:

- Broken Access Control
- Injection
- Security Misconfiguration
- Identification and Authentication Failures
- etc.

Goal:

- ensure every entry point has an “OWASP pass”

### Step 3: Authorization review (authz correctness)

Checklist:

- Are authorization checks enforced server-side for every sensitive operation?
- Are “resource ownership” checks present (tenant/user scoping)?
- Do you rely on client-provided userId/tenantId? (Avoid)
- Are admin-only endpoints strongly protected and audited?
- Are default roles least-privilege?

Tests to add:

- negative tests for forbidden access
- tenant isolation tests

### Step 4: Input validation & injection defense

Checklist:

- Validate at boundaries:
  - request DTOs, headers, query params, path params
- Prefer allowlists:
  - known enum values
  - bounded lengths
  - regex with care (avoid catastrophic backtracking)
- For SQL:
  - use prepared statements / parameter binding
  - avoid string concatenation
- For templates:
  - avoid evaluating untrusted expressions
- For file upload:
  - validate content type + size + storage location
  - sanitize filenames

Tests to add:

- invalid payload tests
- boundary length tests
- injection regression tests (defensive assertions)

### Step 5: SSRF defensive review (URL fetching, webhooks, “download this” features)

Identify any code that:

- fetches URLs
- calls arbitrary endpoints based on user input
- resolves DNS for user-provided hosts
- supports redirects

Controls checklist:

- Allowlist domains or approved endpoints
- Block private IP ranges and link-local targets
- Enforce outbound proxy / egress policies if available
- Disable or strictly control redirects
- Normalize and parse URLs using safe libraries
- Add timeouts and size limits for responses

Tests to add:

- unit tests for URL validator logic
- integration tests using local stub server where appropriate

### Step 6: Deserialization defensive review

Identify:

- Java native serialization usage
- Object mapper configuration that can instantiate arbitrary classes
- Accepting polymorphic types from untrusted inputs

Controls checklist:

- Avoid Java native serialization for untrusted data
- Prefer safe formats (JSON with strict schema)
- If polymorphism is required:
  - use explicit allowlist of subtypes
  - disable default typing / unsafe features
- Validate input size and structure
- Add strict schema validation for payloads

Tests to add:

- ensure disallowed types are rejected
- ensure unknown fields are handled as intended (strict vs tolerant)

### Step 7: Secrets & sensitive data hygiene

Checklist:

- No secrets in repo (keys, tokens, passwords)
- No secrets in logs (redact)
- Config layering uses secret stores where possible
- Avoid returning sensitive data in error messages
- Ensure audit logging for security-sensitive actions (admin changes)

Add gates:

- secret scanning in CI
- dependency scanning where feasible

### Step 8: Dependency / supply chain quick pass

Checklist:

- Pin dependency versions
- Remove unused dependencies
- Monitor for known vulnerabilities (tooling dependent)
- Prefer official artifacts and verified sources

Deliverable:

- a short “dependency risk” section with actions

## Findings report template (copy/paste)

### Finding

- ID: SEC-XXX
- Title:
- Severity: (Critical/High/Medium/Low)
- OWASP mapping:
- Affected components:
- Description (defensive):
- Evidence (code references):
- Impact:
- Recommendation:
- Tests added:
- Owner / ETA:

## Definition of Done (DoD)

- [ ] System map exists (entry points + assets + trust boundaries)
- [ ] OWASP lens applied to all entry points
- [ ] Authz rules verified and tested
- [ ] Input validation present and tested
- [ ] SSRF and deserialization risks addressed where relevant
- [ ] Secrets hygiene verified; no sensitive logs
- [ ] Findings report written with mitigations and regression tests

## Guardrails

- Do not attempt exploitation or scanning outside approved environments
- Do not store secrets in prompts, logs, or screenshots
- Use least-privilege accounts for testing
- Prefer code fixes + tests over “document-only” mitigations

## Outputs / Artifacts

- `security/audit/<date>-<service>.md` findings report
- PR with:
  - mitigations (code changes)
  - regression tests
  - config hardening (as needed)
- CI updates (secret scanning / dependency scanning), if applicable

## References (official)

- OWASP Top 10: <https://owasp.org/www-project-top-ten/>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
- OWASP ASVS: <https://owasp.org/www-project-application-security-verification-standard/>
