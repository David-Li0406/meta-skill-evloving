# Verification Fixtures — Real Data for Memory System Testing

## Purpose

These fixtures use **real data** from Tyler's communication sources (iMessage, Gmail, AIX) to verify the memory system works correctly. Real data enables better "vibe eval" — you can look at the output and know if it makes sense.

## Directory Structure

```
fixtures/
├── README.md                    # This file
├── imessage/
│   ├── identity-disclosure/     # Casey shares email (HAS_EMAIL → alias)
│   │   ├── episode.json
│   │   └── expectations.yaml
│   ├── job-change/              # Tyler announces job change (valid_at/invalid_at)
│   │   ├── episode.json
│   │   └── expectations.yaml
│   └── social-relationship/     # Group chat with DATING relationship
│       ├── episode.json
│       └── expectations.yaml
├── gmail/
│   ├── newsletter-sender/       # Cloudflare invoice (Company, CUSTOMER_OF)
│   │   ├── episode.json
│   │   └── expectations.yaml
│   └── work-thread/             # Work email with signature parsing
│       ├── episode.json
│       └── expectations.yaml
└── aix/
    ├── personal-info/           # User shares birthdate, location, employer
    │   ├── episode.json
    │   └── expectations.yaml
    └── project-discussion/      # Project entities (Nexus, Cortex)
        ├── episode.json
        └── expectations.yaml
```

## Fixture Format

### episode.json

```json
{
  "id": "fixture-imessage-001",
  "source": "imessage",
  "channel": "imessage",
  "thread_id": "chat123456",
  "reference_time": "2026-01-22T10:30:00Z",
  "events": [
    {
      "id": "evt-001",
      "timestamp": "2026-01-22T10:30:00Z",
      "sender": "Casey Adams",
      "sender_identifier": "+1-555-123-4567",
      "content": "My new work email is casey@anthropic.com btw",
      "direction": "inbound"
    }
  ],
  "metadata": {
    "description": "Casey shares their work email in iMessage",
    "coverage_tags": ["identity_disclosure", "email", "self_disclosed"]
  }
}
```

### expectations.yaml

```yaml
# Fixture: Casey shares work email
description: "Casey self-discloses their work email"
source: imessage

entities:
  must_have:
    - name_contains: "Casey"
      entity_type: Person
      
  must_not_have:
    - name: "casey@anthropic.com"  # Emails are aliases, not entities
      entity_type: any

aliases:
  must_have:
    - entity_name_contains: "Casey"
      alias: "casey@anthropic.com"
      alias_type: email
      
relationships:
  must_not_have:
    # Identity relationships go to aliases, not relationships table
    - relation_type: HAS_EMAIL
      
episode_relationship_mentions:
  must_have:
    - extracted_fact_contains: "email"
      source_type: self_disclosed
      target_literal: "casey@anthropic.com"
```

## Coverage Matrix

Each fixture should test specific behaviors. Track coverage here:

| Fixture | Entity Types | Relationship Types | Resolution | Temporal | Identity |
|---------|--------------|-------------------|------------|----------|----------|
| imessage/identity-disclosure | Person | HAS_EMAIL | new entity | - | ✓ promote |
| imessage/job-change | Person, Company | WORKS_AT | resolve existing | valid_at, invalid_at | - |
| imessage/social-relationship | Person (4) | DATING | new entities | valid_at (6mo) | - |
| gmail/newsletter-sender | Company (2) | CUSTOMER_OF | new entities | - | - |
| gmail/work-thread | Person (3), Company | WORKS_AT | resolve | - | ✓ signature |
| aix/personal-info | Person, Company, Location | BORN_ON, LIVES_IN, WORKS_AT | - | date literal, valid_at | - |
| aix/project-discussion | Person (2), Project | BUILDING, WORKING_ON | - | STARTED_ON | - |

### Feature Coverage Summary

- **Identity Promotion**: imessage/identity-disclosure, gmail/work-thread (signature)
- **Temporal Literals**: aix/personal-info (BORN_ON), aix/project-discussion (STARTED_ON)
- **Temporal Bounds**: imessage/job-change (valid_at/invalid_at), aix/personal-info (valid_at)
- **Contradiction Detection**: imessage/job-change (old job invalidated)
- **Multi-Entity**: imessage/social-relationship (4 people), gmail/work-thread (3 people)
- **Company Extraction**: gmail/newsletter-sender, gmail/work-thread, aix/personal-info
- **Project Extraction**: aix/project-discussion
- **Location Extraction**: aix/personal-info

## How to Select Real Data

### From iMessage (via eve/imsg)
```bash
# Find messages where someone shares contact info
imsg search "my email" --limit 10
imsg search "my phone" --limit 10
imsg search "started at" --limit 10  # Job changes
```

### From Gmail (via gog)
```bash
# Find emails with identity info
gog gmail search "from:newsletter" --limit 5
gog gmail search "subject:invitation" --limit 5
```

### From AIX (cursor sessions)
```bash
# Look through recent sessions in ~/.aix/sessions/
ls -la ~/.aix/sessions/ | head -20
```

## Anonymization Guidelines

1. **Keep real structure** — Don't change relationship patterns
2. **Change identifiers** — Use fake emails/phones/addresses
3. **Keep names if comfortable** — Or use consistent pseudonyms
4. **Preserve dates** — Real temporal patterns matter

## Adding a New Fixture

1. Find real data that covers a gap in the coverage matrix
2. Create directory: `fixtures/{source}/{scenario-name}/`
3. Create `episode.json` with the episode data
4. Create `expectations.yaml` with assertions
5. Update coverage matrix in this README
6. Run verification harness to validate
