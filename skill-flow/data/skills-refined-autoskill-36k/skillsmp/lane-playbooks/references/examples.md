# OS Examples Reference

Structured examples from KYORA_AGENT_OS.md showing classification, owners, phases, and gates for common scenarios.

## Example 1: Cross-Stack Feature (Backend + Portal)

**Request**: "Add a new 'Low stock' widget to the dashboard and expose a backend endpoint for it."

| Field | Value |
|-------|-------|
| Type | feature |
| Scope | cross-stack |
| Risk | Medium |
| Primary Owner | Orchestrator |
| Supporting | Backend Lead, Web Lead, Backend Implementer, Web Implementer, QA |
| Lanes | Planning → Implementation → Review → Validation |

**Phases**:
- Phase 0: Define endpoint + response shape + error behavior
- Phase 1: Backend endpoint + tests (+ OpenAPI if required)
- Phase 2: Portal API client + query + widget UI + i18n keys + states
- Phase 3: Playwright smoke for dashboard + RTL check

**Gates**: Ask PO if schema changes or new deps required

**DoD**: Widget correct; RTL-safe; no hardcoded strings; relevant tests green

---

## Example 2: UI/UX Redesign

**Request**: "Revamp the Orders list page to feel cleaner and more mobile-friendly."

| Field | Value |
|-------|-------|
| Type | design |
| Scope | single-app (portal-web) |
| Risk | High |
| Primary Owner | Design/UX Lead |
| Supporting | Web Lead, i18n Lead, Web Implementer, QA |
| Lanes | Discovery → Planning → Implementation → Review → Validation |

**Gates**: PO approval for redesign scope and new UI primitives

**Tools**: Read existing patterns/components; Playwright + Chrome DevTools as needed

**DoD**: Page is simpler, mobile-first, RTL-safe, consistent components/tokens

---

## Example 3: Large Refactor (Phased)

**Request**: "Refactor customer search/filter logic across backend and portal; it's getting messy."

| Field | Value |
|-------|-------|
| Type | refactor |
| Scope | cross-stack |
| Risk | High |
| Primary Owner | Orchestrator |
| Supporting | Backend Lead, Web Lead, Shared/Platform Implementer, QA |
| Lanes | Planning (phased) → Implementation → Review → Validation |

**Phases**:
- Phase 0: Map current behavior + add/adjust tests
- Phase 1: Backend refactor behind compatible API
- Phase 2: Portal refactor (reuse query keys/patterns)
- Phase 3: Delete dead code + consistency pass

**Gates**: PO approval if behavior changes or contract breaks

**DoD**: Behavior preserved (unless approved); tests cover; no dead code

---

## Example 4: Bug Report Deferred into Tech Debt

**Request**: "Sometimes the dashboard numbers look wrong. Not urgent."

| Field | Value |
|-------|-------|
| Type | bug |
| Scope | unknown |
| Risk | Medium |
| Primary Owner | Orchestrator |
| Supporting | Data/Analytics Lead (if metrics), QA |
| Lanes | Discovery → Deferred/Backlog |

**Output**:
- Repro attempts + what data/logs are needed
- Suspected causes
- Structured backlog item PO can prioritize

---

## Example 5: Translation Rewrite

**Request**: "Rewrite the Arabic translations for onboarding screens to sound more natural."

| Field | Value |
|-------|-------|
| Type | i18n |
| Scope | portal-web |
| Risk | Medium |
| Primary Owner | i18n/Localization Lead |
| Supporting | Web Lead |
| Lanes | Planning-lite → Implementation → Review |

**Gates**: PO approval if meaning changes (not just phrasing)

**DoD**: Natural Arabic; keys consistent; no hardcoded strings

---

## Example 6: Content Writing (Marketing)

**Request**: "Write a short landing page section explaining Kyora's 'Cash in hand' benefit."

| Field | Value |
|-------|-------|
| Type | content |
| Scope | monorepo-wide (copy only) |
| Risk | Low |
| Primary Owner | Content/Marketing Lead |
| Supporting | i18n Lead (if Arabic version needed) |
| Lanes | Discovery (tone/claims) → Implementation (copy draft) → Review |

**Gates**: PO approval for any claims touching legal/tax promises

**DoD**: Simple, calm copy; no accounting jargon; ready for translation

---

## Quick Classification Reference

| Scenario | Type | Scope | Risk | Start Lane |
|----------|------|-------|------|------------|
| New endpoint + UI | feature | cross-stack | Medium | Planning |
| Bug with clear repro | bug | single-app | Low | Implementation |
| Bug unclear | bug | unknown | Medium | Discovery |
| UI redesign | design | single-app | High | Discovery |
| Large refactor | refactor | varies | High | Planning |
| Translation update | i18n | portal-web | Medium | Planning-lite |
| Marketing copy | content | monorepo-wide | Low | Discovery |
| CI/CD change | devops | monorepo-wide | Medium | Planning |

## Inference Triggers Reference

Auto-involve these roles based on risk axis:

| Risk Axis | Must Involve | PO Gate |
|-----------|--------------|---------|
| auth/session/RBAC | Backend Lead + Security | Yes |
| payments/billing | Backend Lead + Security | Yes |
| PII/privacy | Security + relevant Lead | Yes |
| schema/migrations | Backend Lead + QA | Yes |
| breaking API contract | Backend Lead + Web Lead | Yes |
| major UX redesign | Design/UX Lead + Web Lead | Yes |
| analytics semantics | Data/Analytics Lead | Yes |

## SSOT Reference

- Full examples: [KYORA_AGENT_OS.md#L881-L1008](../../../KYORA_AGENT_OS.md#L881-L1008)
