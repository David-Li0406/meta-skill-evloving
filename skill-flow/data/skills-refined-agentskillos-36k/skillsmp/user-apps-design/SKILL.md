---
name: user-apps-design
description: Guardrails for BudgEat user-apps client UI changes. Prevent style drift by requiring the UI/UX entrypoint, using tokens/components, and keeping end-user UI Polish-only.
---

# User Apps Design

## Primary rule

Before changing user-apps UI: read the UI/UX entrypoint and follow its guardrails. Do not invent styling.

## When this applies

Use this skill when you are making changes to **user-apps client UI**, including:

- adding/modifying screens, layouts, components, or patterns
- changing colors, typography, spacing, or visual styling
- changing end-user visible copy/strings
- changing empty/loading/error UX on end-user screens

Excluded:

- backend/API/auth contract work (Query API payloads/endpoints/semantics; server-side session behavior)

## Required input (read this first)

You MUST read:

- `docs-ai/docs/initiatives/user-apps/features/app-foundation/ui-ux-entrypoint.md`

Do not proceed until you can restate the relevant guardrails for your change in one short paragraph.

## Non-negotiable rules

### 1) Do not invent styling (anti-drift)

- Do **not** pick new colors, fonts, radii, spacing steps, or component variants ad hoc.
- **Methodology**: Follow the **Atomic Design** principle (Atoms, Molecules, navigation) as documented in `apps/mobile/lib/core/widgets/README.md`.
- Prefer using the existing component/pattern inventory and token semantics referenced by the entrypoint doc.
- Avoid introducing “one-off” styling per screen or per component instance (that is how drift starts).

If you believe a new token/component/pattern is required:

- Stop and propose it explicitly (name + purpose + where it should live in docs).
- Do not “just choose values” as a workaround.

### 2) End-user UI is Polish-only

- Any end-user visible strings must be Polish.
- Follow: `docs-ai/docs/conventions/language-policy.md`

### 3) Preserve the core UX invariants

Do not change UI/UX invariants without an explicit spec decision.

Source of truth for the invariant list: `docs-ai/docs/initiatives/user-apps/features/app-foundation/ui-ux-entrypoint.md`

## Before you change UI (checklist)

- [ ] I read `docs-ai/docs/initiatives/user-apps/features/app-foundation/ui-ux-entrypoint.md`
- [ ] I can point to the specific source of truth for the styling/UX rule I’m touching (link-only; no duplication)
- [ ] I did not add new ad hoc style values (colors/fonts/etc.)
- [ ] End-user visible strings are Polish-only
- [ ] I re-validated the relevant UI/UX invariants from the entrypoint doc

## If the entrypoint seems wrong or missing something

Do not “fix” UX by inventing new styling or changing invariants ad hoc.

Instead:

- Stop and describe what is missing/contradictory in `docs-ai/docs/initiatives/user-apps/features/app-foundation/ui-ux-entrypoint.md`.
- Point to the closest authoritative doc that should be linked (contract pack, tokens, components, art direction, or policy).
- Propose the smallest update to the entrypoint doc (link-only, no long spec duplication), then wait for confirmation before proceeding with UI changes.
