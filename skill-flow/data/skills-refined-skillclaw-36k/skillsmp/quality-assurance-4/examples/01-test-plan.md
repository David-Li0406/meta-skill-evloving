# QA Test Plan (Web Service)

## Scope & Goals
- Service: Checkout API (cart, pricing, payments, orders).
- Goals: Prevent regressions on pricing/discounts, ensure payment reliability, validate authZ for roles, and maintain SLA p95 < 400ms.
- Out-of-scope: Legacy reporting endpoints (read-only, deprecated).

## Risks (Top)
- Discount/rounding errors on multi-currency carts.
- Payment retries causing double charges.
- Race conditions on inventory holds.
- Feature flags misconfigured across environments.

## Strategy
- **Levels**: Unit (critical logic), integration (API contracts + DB), E2E (checkout happy/critical paths).
- **Types**: Functional, security (authZ/input validation/secrets), performance smoke (latency/error-rate), accessibility (a11y basics on checkout page).
- **Environments**: Dev (fast), Staging (pre-prod data), Load (synthetic scale).
- **Data**: Carts with edge discounts, zero/negative qty, large totals, multiple currencies, guest vs logged-in, expired tokens.
- **Observability**: Logs with correlation IDs, tracing on checkout, metrics for errors/timeouts/retries.

## Test Design
- Happy path: guest checkout with card; logged-in with saved card.
- Negative: expired token, invalid CVV, inventory unavailable, discount code expired.
- Security: role checks (customer vs admin), missing/invalid JWT, input validation (strings/ints, limits, HTML/JS payloads).
- Performance smoke: p95 latency under 400ms for 10 RPS, error rate <1%.
- Accessibility (UI): form labels, focus order, keyboard-only flow, contrast on primary buttons.

## Quality Gates
- CI: lint + unit + integration required; coverage >= 80% lines/branches on checkout module.
- Security: secrets scan, SAST, dependency scan; no critical/high vulns open.
- Release: staging E2E (happy/critical) pass; no Sev1/Sev2 open; rollback plan validated; observability dashboards green.

## Ownership & Cadence
- QA lead: Assigns test cases and triage.
- Dev owners: Checkout, Payments, Pricing.
- Cadence: Daily status; triage twice per week; go/no-go review before release.

## Defect Handling
- Severity/priority matrix; repro with env + data + logs/traces.
- Add regression coverage for each escaped/critical bug.
- Track MTTR and escape rate; review flake list weekly.
