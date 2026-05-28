---
name: java-contract-testing
description: Establish contract testing (OpenAPI + consumer-driven contracts) with compatibility gates to prevent breaking changes in microservices. Use when API evolution risks breaking consumers or when you need CI enforcement of backward compatibility.
license: CC-BY-4.0
compatibility:
  jdk: "17+"
  build: "Maven or Gradle"
  ci: "Any (GitHub Actions/GitLab/Jenkins)"
metadata:
  owner: backend-platform
  version: "0.1.0"
  tags: [java, contract-testing, openapi, pact, ci, microservices]
---

# Java Contract Testing (Compatibility Gates)

## What “contract testing” means here

A contract is an executable agreement between a provider and its consumers:

- REST: OpenAPI spec (provider contract-first) and/or consumer-driven contract tests
- Messaging: event schema + invariants (compatibility rules and verification)

This skill focuses on two complementary strategies:

1) Provider-driven contracts (OpenAPI as source of truth)
2) Consumer-driven contracts (Pact-style thinking)

Use one, or combine both in a mature platform.

## Scope

### In scope

- OpenAPI spec ownership, versioning, and breaking-change rules
- Consumer-driven contracts (Pact JVM style)
- CI “compatibility gates”:
  - fail PRs that introduce breaking changes
  - require provider verification against published consumer contracts
- Contract publishing and verification workflows

### Out of scope

- End-to-end tests across live services
- Performance/load testing

## When to use (Triggers)

- You have multiple consumers per service
- You ship frequently and want to prevent accidental breakages
- You experienced production incidents caused by API changes
- You need a “deploy safety check” for microservices

## Contract strategy decision guide

### Strategy A: OpenAPI-first (provider contract)

Pick when:

- REST API is primary integration surface
- You want one canonical API definition

You do:

- Maintain OpenAPI in repo
- Generate clients/stubs (optional)
- Validate implementation matches OpenAPI
- Use OpenAPI diff gate to detect breaking changes

### Strategy B: Consumer-driven (Pact)

Pick when:

- Many consumers evolve independently
- You want consumers to define the minimum they require

You do:

- Consumer tests produce contracts (pacts)
- Publish contracts to a broker/artifact store
- Provider verification runs against published contracts
- CI gate blocks deployment if verification fails (“can I deploy?” model)

### Strategy C: Hybrid (recommended for large orgs)

- OpenAPI as public contract + docs
- Pact to enforce real consumer expectations
- Both can coexist if governance is clear

## Versioning & compatibility rules (REST mindset)

Define and document rules such as:

- Non-breaking:
  - add optional response fields
  - add new endpoints
  - widen enum with backward-compatible behavior (case-by-case)
- Breaking:
  - remove fields or endpoints
  - change field type/meaning
  - change required/optional in incompatible direction
  - change error model semantics without version bump

Always encode rules into a gate:

- A tool-based diff gate (OpenAPI diff)
- A contract verification gate (Pact provider verification)

## Implementation workflow (Step-by-step)

### Step 1: Define contract storage layout

Recommended:

- `api/openapi/service.yaml` (or `openapi.yaml`)
- `contracts/` for pact files or DSL contracts
- `docs/api/` for rendered docs (optional)

### Step 2: Add contract checks to CI

Minimal gates:

- Gate 1 (PR): OpenAPI lint + breaking-change detection
- Gate 2 (PR/merge): Provider verification against consumer contracts
- Gate 3 (pre-deploy): “Can I deploy?” gate based on published verification status

### Step 3: Consumer-driven contract workflow (Pact JVM style)

Consumer side:

1) Write consumer tests that define interactions (requests + minimal expected responses)
2) Generate pact files
3) Publish pacts (broker or artifact registry)

Provider side:

1) Fetch latest relevant pacts from broker
2) Run provider verification tests (against real implementation)
3) Publish verification results back to broker
4) Gate deployments based on verification status

### Step 4: Provider-driven OpenAPI workflow

Provider side:

1) OpenAPI spec updated in PR
2) CI runs:
   - spec validation (syntax + lint)
   - compatibility diff against main branch spec
   - optionally: API conformance tests that validate endpoints align with spec
3) On merge, publish:
   - rendered docs
   - versioned spec artifact

Consumers:

- Generate client (optional) or validate request/response models against the spec

## Practical patterns (to avoid contract rot)

- Keep contracts minimal: specify only what is required
- Avoid over-constraining with transient details (timestamps, ids formatting) unless truly required
- Use stable error model conventions
- Treat contracts as “deploy gates”, not “documentation only”

## CI Gate templates (conceptual)

### Gate: PR compatibility (OpenAPI)

- Validate OpenAPI syntax + lint
- Compute diff vs base branch spec
- Fail if breaking changes found
- Output: diff report artifact

### Gate: Provider verification (Pact)

- Run provider verification suite in CI
- Publish verification results
- Fail PR if verification fails

### Gate: Deploy safety (Pact “can-i-deploy” style)

- Before deployment:
  - check whether current service version is safe to deploy given all published contracts
- Block deployment if unsafe

## Definition of Done (DoD)

- [ ] Contract exists in repo and is versioned
- [ ] PR gate blocks breaking changes (or requires version bump)
- [ ] Provider verification runs in CI
- [ ] Consumers can independently validate compatibility
- [ ] Contracts are discoverable (docs, broker, artifacts)

## Guardrails (What NOT to do)

- Never treat OpenAPI/pacts as “nice-to-have docs” without enforcement
- Never publish contracts without a verification workflow
- Avoid:
  - giant contracts that encode every possible response detail
  - skipping backward compatibility analysis (“just change it and hope”)

## Outputs / Artifacts

- OpenAPI spec in repo
- Pact contracts (consumer output)
- Provider verification test suite
- CI jobs: compatibility gate + verification gate
- Reports: breaking changes diff + verification status

## References (official docs)

- Pact docs (JVM / broker / concepts): <https://docs.pact.io/>
- Spring Cloud Contract docs (alternative JVM approach): <https://docs.spring.io/spring-cloud-contract/docs/current/reference/html/>
- OpenAPI Specification: <https://spec.openapis.org/>
