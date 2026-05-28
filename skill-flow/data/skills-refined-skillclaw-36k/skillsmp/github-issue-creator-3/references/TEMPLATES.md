# Issue Templates

Focused templates for GitHub issues. Keep issues high-level - implementation details belong in branch plans.

## Feature Template

```markdown
## Summary

<1-2 sentences: what capability and why it matters>

## User Story

**As a** <role>,
**I want** <capability>,
**So that** <benefit>.

## Scope

**Included:**
- <what's in scope>

**Not included:**
- <what's explicitly out of scope>

## Acceptance Criteria

- [ ] <User-visible outcome 1>
- [ ] <User-visible outcome 2>
- [ ] <User-visible outcome 3>

## Implementation

See branch plan: `docs/PLAN.md` in feature branch

## Notes

<Context, constraints, references - keep brief>
```

## Bug Template

```markdown
## Problem

<What's broken, from user perspective>

## Steps to Reproduce

1. <step>
2. <step>
3. <step>

## Expected vs Actual

- **Expected**: <what should happen>
- **Actual**: <what happens instead>

## Environment

- URL: <if applicable>
- Browser: <if frontend>
- User/Tenant: <if relevant>

## Screenshots

<if helpful>
```

## Task Template

```markdown
## Goal

<What we're trying to achieve and why>

## Scope

<What's included in this work>

## Done When

- [ ] <Outcome 1>
- [ ] <Outcome 2>

## Implementation

See branch plan: `docs/PLAN.md` in feature branch
```

---

## Examples

### Feature Example

**Title:** Add ETA display to consignment page

```markdown
## Summary

Show estimated delivery date on consignment pages so users can check delivery timing without navigating to the parent shipment.

## User Story

**As a** logistics manager,
**I want** to see the ETA on the consignment page,
**So that** I can quickly check delivery estimates while reviewing consignment details.

## Scope

**Included:**
- Display requested/planned/actual delivery dates in consignment tracking sidepanel
- Update when new tracking events arrive

**Not included:**
- Editing delivery dates from consignment page
- Email notifications for ETA changes

## Acceptance Criteria

- [ ] ETA dates visible on consignment detail page
- [ ] Dates match what's shown on parent shipment
- [ ] Updates reflect new tracking events

## Implementation

See branch plan: `docs/PLAN.md` in feature branch

## Notes

Similar layout to existing shipment sidepanel tracking section.
```

### Bug Example

**Title:** Consignment link ignores /test prefix in playground mode

```markdown
## Problem

In playground/test mode, clicking the consignment reference link leads to a 404 because the /test prefix is missing from the URL.

## Steps to Reproduce

1. Create a shipment in Test/Playground mode
2. Open shipment at URL like: `https://tenant.viyatest.it/test/shipment/{id}`
3. Navigate to Overview section
4. Click on Consignment Reference link in Tracking block

## Expected vs Actual

- **Expected**: Link navigates to `/test/consignment/{id}`
- **Actual**: Link navigates to `/consignment/{id}` (missing /test prefix), showing 404

## Environment

- URL: https://pr-tenant-stitch-integrations-2270.test.viyatest.it/test/shipment/{id}

## Screenshots

<screenshot>
```

### Task Example

**Title:** Remove deprecated /v3 API endpoints

```markdown
## Goal

Clean up legacy /v3 API endpoints that are no longer in use, reducing maintenance burden and codebase size.

## Scope

- Verify no traffic on /v3 endpoints (check Grafana, last 2 weeks)
- Remove endpoints from shipping service
- Remove corresponding legacy pages from viya-app

## Done When

- [ ] No /v3 endpoint traffic confirmed
- [ ] Endpoints removed and deployed
- [ ] Legacy pages removed and deployed

## Implementation

See branch plan: `docs/PLAN.md` in feature branch
```

---

## Writing Tips

### Good Acceptance Criteria
- ✅ "User can export reports as PDF"
- ✅ "Exported PDF includes all visible columns"
- ❌ "ExportService class is created"
- ❌ "API endpoint returns 200"

### Keep Issues Focused
- ONE issue per user-facing outcome
- Implementation details go in branch PLAN.md
- If you need 5+ checkboxes, consider if it's really one thing
