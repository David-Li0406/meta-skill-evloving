---
title: Contact/Person Split Spec
status: draft
owner: cortex
last_updated: 2026-01-23
---

# Contact/Person Split Spec

## Summary
Split "contact endpoints" from "people" across Cortex. A contact is a communication endpoint (phone, email, handle, device). A person is a real-world human identity. Endpoints can exist without a person. People can own multiple endpoints. This removes numeric-only names from the person graph, improves identity hygiene, and makes the system robust to reuse of phone numbers/emails over time.

This spec follows the code philosophy: optimize for long-term clarity, predictable behavior, and patterns that scale. The model should teach good habits and avoid shortcuts that will be copied.

## Goals
- Eliminate phone/email identifiers as person aliases.
- Represent unknown endpoints without inventing fake people.
- Keep deterministic endpoint dedupe and isolate fuzzy person resolution.
- Support ownership changes over time (reused numbers).
- Make the graph cleaner and more durable across channels.

## Non-Goals
- Preserve backwards compatibility with existing APIs without updates.
- Maintain dual-write. This is a big-bang migration.
- Solve all person resolution quality issues in this change.

## Definitions
- **Contact**: An endpoint used to communicate (phone/email/handle/device).
- **Identifier**: The normalized value of an endpoint (digits for phone, lowercase for email).
- **Person**: A real human identity.
- **Alias**: A name or nickname for a person (not a contact method).
- **Contact Link**: A relationship between a contact and a person, with confidence and time bounds.

## Data Model (Cortex)

### New Tables
```
contacts (
  id TEXT PRIMARY KEY,
  display_name TEXT,          -- best known label, not necessarily a person name
  source TEXT,                -- imessage/gmail/aix/x/etc
  created_at TEXT,
  updated_at TEXT
)

contact_identifiers (
  id TEXT PRIMARY KEY,
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  type TEXT NOT NULL,         -- phone/email/handle/device
  value TEXT NOT NULL,        -- raw value
  normalized TEXT NOT NULL,   -- canonical form for dedupe
  created_at TEXT,
  last_seen_at TEXT,
  UNIQUE(type, normalized)
)

person_contact_links (
  id TEXT PRIMARY KEY,
  person_id TEXT NOT NULL REFERENCES persons(id),
  contact_id TEXT NOT NULL REFERENCES contacts(id),
  confidence REAL DEFAULT 1.0,
  source_type TEXT,           -- deterministic/llm/inferred
  first_seen_at TEXT,
  last_seen_at TEXT,
  UNIQUE(person_id, contact_id)
)
```

### Existing Tables (updated meaning)
```
persons              -- remains for human identities
entity_aliases       -- name/nickname only (no phone/email here)
event_participants   -- will reference contact_id instead of person_id
```

## Ingestion by Channel

### iMessage (Eve)
- Eve writes contacts + identifiers (phone/email).
- Cortex imports Eve contacts into `contacts`.
- Cortex does NOT create a person unless a real name exists.

### Gmail
- Email addresses become `contacts` with `contact_identifiers(type=email)`.
- Sender/recipient endpoints are contacts first.
- A person may be linked if a real name is present in headers.

### Calendar
- Organizer/attendees become contacts (email).
- Persons linked only if name is known and stable.

### X / Social
- Handle becomes contact (type=handle).
- Person linked if the display name is stable and non-generic.

### AIX (AI Logs)
- User endpoint is a contact (type=human, source=aix).
- AI model/agent endpoint is a contact (type=ai, source=aix).
- Do not create a person for AI assistants.
- This keeps the split consistent without forcing person identities for AI.

### Nexus / Internal Logs
- System and tool identifiers become contacts.
- Persons only when explicit human names exist.

## Resolution Rules

### Contact Resolution (Deterministic)
- Normalize identifiers per type (phone/email/handle).
- Deduplicate by `(type, normalized)` at write time.

### Person Resolution (Fuzzy)
- Triggered only when a non-generic name exists.
- Person merges use aliases, embeddings, and LLM assistance.
- Contacts can be linked to persons later, with confidence scoring.

### Unknown Contacts
- Unknown endpoints are valid contacts with no person link.
- They remain stable across events and can be upgraded later.

## Pipeline Updates

1. **Event ingestion**
   - event_participants -> contact_id (not person_id)
2. **Memory extraction**
   - entities: only names/nicknames become person entities
   - identifiers (phone/email) become contact identifiers, not aliases
3. **Identity promotion**
   - only promotes name/nickname to aliases
   - phone/email go to contact_identifiers
4. **Query layer**
   - events show contacts; person resolution is layered on top

## Migration Plan (Big Bang)

1. Add new contact tables.
2. Backfill contacts from existing persons + identities:
   - create a contact for each identity
   - create person_contact_links with deterministic confidence
3. Rewrite event_participants to contact_id.
4. Remove phone/email from entity_aliases.
5. Update ingestion to write contacts.
6. Rebuild indexes and run full reimport.

No dual-write. Cutover happens once migration completes.

## Validation Checklist
- Duplicate contact identifiers = 0
- Person graph contains no numeric-only names
- All events have contact participants
- Known persons resolve consistently across channels

## Open Questions
- Confidence model for person_contact_links
- Policy for renaming contacts as names appear
- UI exposure for contact vs person

