---
name: java-code-review-playbook
description: Apply a production-grade code review checklist for Java backend changes: layering, error handling, security, tests, observability, performance, and maintainability. Use when preparing a PR or reviewing one.
license: CC-BY-4.0
compatibility:
  jdk: "any"
metadata:
  owner: backend-platform
  version: "0.1.0"
  tags: [java, code-review, quality, security, observability]
---

# Java Code Review Playbook (Reviewer + Author)

## Goal

Turn code review into a reliable quality gate:

- detect correctness and design issues early
- enforce consistency and maintainability
- prevent security and reliability regressions
- ensure tests and observability exist

This playbook is optimized for:

- small diffs
- clear responsibility boundaries
- measurable acceptance criteria

## How to use in practice

### For authors (before requesting review)

- Run local checks (unit tests, formatting, static analysis)
- Provide a PR description that answers:
  - What problem does this solve?
  - Why this design?
  - What are the risks?
  - How was it tested?
  - What should reviewers focus on?

### For reviewers

Review in this order:

1) Intent & design (is the change the right one?)
2) Correctness (edge cases, concurrency, error paths)
3) Tests (do they prove the fix?)
4) Security & reliability (authz, validation, resource safety)
5) Observability (logs/metrics/traces)
6) Readability & style (only after the above)

## High-signal review checklist (the 80/20)

### A) Architecture & boundaries

- Does this belong in this module/layer?
- Are dependencies pointing the right direction?
- Are interfaces stable and cohesive?
- Is business logic isolated from IO frameworks?

### B) Correctness & invariants

- Are null/empty/invalid inputs handled?
- Are edge cases covered (pagination, overflow, timezones, precision)?
- Is concurrency safe (shared state, caches, retries)?
- Are transactions correctly bounded?

### C) Error handling

- Are exceptions mapped to a consistent error model?
- Do we return correct HTTP/gRPC status codes?
- Are retries limited and idempotent?
- Are timeouts explicit?

### D) Tests

- Does the change add/adjust tests that would fail without the fix?
- Are unit tests focused and fast?
- Are integration tests added only when necessary (IO/DB bugs)?
- Are tests deterministic (no sleeps)?

### E) Security

- Input validation exists at boundaries
- Authorization checks are enforced (not only authentication)
- No secrets in logs or code
- No unsafe deserialization / SSRF risk introduced

### F) Observability

- Logs:
  - structured, actionable, no PII
  - include correlation/request id where relevant
- Metrics:
  - counters/histograms for key operations
  - cardinality safe labels
- Traces:
  - spans around external calls and DB boundaries (where applicable)

### G) Performance & resource usage

- Any N+1 DB risks?
- Any unbounded memory growth?
- Any blocking calls on sensitive threads?
- Any accidental heavy work in hot paths?

### H) Maintainability

- Naming clarity and intent
- Complexity: functions and classes not doing too much
- Avoid duplicated logic
- Documentation or comments where future readers need them

## Comment style guidelines (to keep reviews healthy)

- Label comment types:
  - [BLOCKER] correctness/security/reliability
  - [SUGGESTION] improvement
  - [QUESTION] clarify intent
  - [NIT] minor style
- Prefer actionable suggestions:
  - “Change X because Y; here’s an example…”
- Avoid “taste wars”: enforce standards through rules, not opinions

## AI-assisted review (Cursor usage pattern)

If using Cursor/agent:

1) Provide context:
   - PR diff + key files only
2) Ask for a structured review:
   - list blockers first
   - then risks
   - then maintainability suggestions
3) Require evidence:
   - point to specific lines/files in diff
4) Never paste secrets/tokens into prompts

Suggested prompt snippet:

- “Review this diff. Focus on correctness, security, tests, and observability. List [BLOCKER] items first with file/line references, then [SUGGESTION]. Do not propose large rewrites.”

## Definition of Done (DoD) for PR approval

- [ ] Meets architecture boundaries
- [ ] Correctness verified (edge cases)
- [ ] Tests added/updated and meaningful
- [ ] Security and authz validated
- [ ] Observability adequate
- [ ] No obvious performance regressions
- [ ] Documentation updated if needed

## Outputs

- Review comments with categories and severity
- A prioritized fix list for the author
- Risk notes (what to monitor after deploy)

## References (official / widely accepted)

- OWASP secure review mindset and security checks: <https://cheatsheetseries.owasp.org/>
