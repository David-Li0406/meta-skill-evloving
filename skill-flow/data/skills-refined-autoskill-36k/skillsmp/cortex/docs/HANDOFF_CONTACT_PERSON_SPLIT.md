---
title: Handoff - Contact/Person Split
status: in-progress
last_updated: 2026-01-23
---

# Handoff - Contact/Person Split

## Why this handoff
Chat UI is laggy. This summarizes current state, decisions, and next steps.

## Decisions
- Adopt contact/person split (contacts are endpoints; persons are humans).
- Big-bang migration, no dual-write.
- Keep Graphiti relationship style; add direction semantics only.
- Reject invalid phone aliases (if not valid phone number).

## Completed work

### Cortex commits
- `e26c55e` fix(sync): align Eve phone normalization
- `cd4fa6b` fix(memory): validate phone aliases and kinship direction

### Eve commit
- `17d65fd` fix(contacts): dedupe handles by identifier

### Reimport
- Eve: `eve init && eve sync` completed successfully
- Cortex: `cortex init && cortex sync --adapter imessage --full`

Validation after reimport:
- Eve duplicate phone identifiers: 0
- Eve numeric contact names: 1506
- Cortex numeric canonical names: 1506
- Unknown Contact count: 0

## Repo state

### Cortex
- Many uncommitted changes exist from earlier work (fixtures, verify-memory-live, etc).
- Needs scoping before any additional commits.

### Eve
- Repo was re-cloned from GitHub (old .git pointer was broken).
- Only dedupe + schema changes are local.

## Spec
- Drafted: `docs/CONTACT_PERSON_SPLIT_SPEC.md`

## Open questions
- Exact policy for unknown contacts (display_name and upgrade rules)
- How to expose contact vs person in UI and queries
- Migration sequencing and backfill rules

## Next steps
- Decide unknown contact policy
- Implement migration (contacts, contact_identifiers, person_contact_links)
- Update event_participants to contact_id
- Update queries and ingestion
- Reimport all channels

