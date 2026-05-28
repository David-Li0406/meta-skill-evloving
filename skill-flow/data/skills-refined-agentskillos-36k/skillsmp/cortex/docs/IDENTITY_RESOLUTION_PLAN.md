# Identity Resolution & PII Extraction Plan

## Overview

This document outlines the approach for intelligent identity resolution across communication channels in comms. The core insight: **people share their identifiers in messages all the time**. By extracting ALL PII from message content with LLM intelligence, we can build rich identity graphs that naturally merge when they accumulate enough overlapping facts.

**Prerequisites**: This plan assumes the Eve→Comms migration is complete, providing:
- `threads` table for chat/channel metadata
- `conversations` + `conversation_events` for flexible chunking
- `analysis_types` + `analysis_runs` + `facets` for generic analysis framework
- `embeddings` table for vector storage

---

## The Problem

We have contacts in different channels that are the same person but appear as separate entities:

| iMessage | Gmail | The Gap |
|----------|-------|---------|
| "Mom" (+17072268448) | jill@napageneralstore.com | Different name, different channel |
| "Dad" (+16508238440) | jim@napageneralstore.com | Different name, different channel |
| Nic Barradas (+15108629220) | nicbarradas@gmail.com | Same name, but not linked |

Traditional approaches fail:
- **Name matching**: "Mom" ≠ "Jill Brandt"
- **Embedding similarity**: Clusters by topic, not identity
- **Social graph alone**: Can't make the Dad → James Brandt jump
- **Regex extraction**: No context = false positives (whose email is this?)

---

## The Solution: Identity Graphs + PII Extraction

**One unified mechanism:** Extract ALL PII from every conversation using LLM intelligence that understands context and attribution.

### How It Works

1. **Start with what we know**: Each contact begins as an identity node with their primary identifier (phone, email)

2. **Extract PII from conversations**: Run comprehensive PII extraction on conversation chunks, capturing:
   - ALL identifiers (emails, phones, usernames)
   - Names (full name, nicknames)
   - Relationships
   - Locations, employers, ownership, and hundreds of other facts
   - **Crucially**: WHO each fact belongs to (self-disclosed vs mentioned)

3. **Build identity graphs**: Each extraction adds facts to the person's identity graph

4. **Merge on collisions**: When two identity graphs accumulate enough overlapping facts, they merge

5. **Create new nodes**: Third parties mentioned in conversations become new identity nodes, forming their own graphs until resolved

---

## Evidence We Found

Searching actual messages revealed direct self-identification:

```
Dad (+16508238440):
  "napageneral is my username"
  "the recovery email is my jim@napageneralstore.com"
  "LastPass has all my passwords. Napageneral@gmail.com"

Mom (+17072268448):
  "Look in jillbrandt12@gmail.com"

Uncle Scott (+18607294099):
  "send me an email to my office: scott@parsonsfinancial.com"
  "My username: scottjparsons007@gmail.com"
```

**This is direct evidence requiring LLM context to properly attribute.**

---

## Identifier Taxonomy (Refined)

In a personal context (~1-10k contacts), identifier "hardness" shifts:

### Hard Identifiers (1 match = merge candidate)
Single match is very strong evidence in a personal contact graph:
- `email_personal`, `email_work`
- `phone_mobile`, `phone_home`, `phone_work`
- `social_handle_*` (Twitter/X, Instagram, LinkedIn, etc.)
- `username_*` (platform-specific)
- `full_legal_name` (in personal graph, duplicates are rare)

### Compound Hard Identifiers (all parts match = merge)
Individual fields that become unique when combined:
- `full_name` + `birthdate`
- `full_name` + `employer` + `city`
- `first_name` + `spouse_name` + `children_count` + `city`
- `nickname` + `employer` + `profession`

### Correlating Identifiers (accumulate for scoring)
Multiple matches increase confidence:
- `employer_current` (weight: 0.20)
- `location_current` (weight: 0.15)
- `profession` (weight: 0.15)
- `spouse_first_name` (weight: 0.25)
- `school_attended` (weight: 0.15)
- `birthdate` (weight: 0.25)

### Enrichment Facts (profile only, never merge)
Build rich profiles but don't trigger identity matching:
- Hobbies, interests
- Preferences
- Personality traits
- Opinions, values
- Physical characteristics

### Shared/Joint Identifiers (flag, don't auto-merge)
Could legitimately belong to multiple people:
- `bank_account` (joint accounts)
- `address_home` (shared residence)
- `family_phone` (family plan)
- `business_email` (team@company.com)

### Specific Government/Financial IDs
Be explicit rather than grouping:
- `ssn` - Social Security Number
- `passport_number`
- `drivers_license_number`
- `tax_id` (EIN, ITIN)
- `voter_registration_id`
- `military_id`
- `crypto_wallet_address`

### Professional Distinctions
Important distinction: **employment vs ownership**:
- `employer_current` / `employer_past` - where you work FOR someone
- `business_owned` - businesses you OWN (array)
- `business_role` - Owner, Co-owner, Partner, Founder
- `business_invested` - investments/board seats
- `profession` - what you do (not where)

---

## The Extraction Pipeline

### Integration with Analysis Framework

PII extraction is an `analysis_type` in the post-migration schema:

```sql
INSERT INTO analysis_types (id, name, version, output_type, facets_config_json, prompt_template, ...)
VALUES (
  'pii_extraction_v1',
  'pii_extraction',
  '1.0.0',
  'structured',
  '{
    "extractions": [
      {"facet_type": "pii_email", "json_path": "$.persons[*].pii.contact_information.email_*", ...},
      {"facet_type": "pii_phone", "json_path": "$.persons[*].pii.contact_information.phone_*", ...},
      {"facet_type": "pii_full_name", "json_path": "$.persons[*].pii.core_identity.full_legal_name", ...},
      {"facet_type": "pii_employer", "json_path": "$.persons[*].pii.professional.employer_current", ...},
      {"facet_type": "pii_business_owned", "json_path": "$.persons[*].pii.professional.business_owned", ...},
      ... all PII types
    ]
  }',
  '<prompt from pii-extraction-v1.prompt.md>',
  'gemini-2.0-flash'
);
```

### Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PII EXTRACTION PIPELINE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT: Conversation (from conversations table)                     │
│  ├── Get events via conversation_events                             │
│  ├── Channel, thread, participants from conversation metadata       │
│  └── User identity for attribution                                  │
│                                                                     │
│  EXTRACTION (via analysis_runs):                                    │
│  ├── Create analysis_run (status='pending')                         │
│  ├── Call LLM with pii-extraction-v1 prompt                         │
│  ├── Parse structured JSON output                                   │
│  └── Update analysis_run (status='completed')                       │
│                                                                     │
│  OUTPUT (to facets table):                                          │
│  ├── Insert facets with facet_type='pii_*'                          │
│  ├── Link to person_id where attributable                           │
│  ├── Include confidence and metadata_json (evidence, source_type)   │
│  └── Flag sensitive facets in metadata                              │
│                                                                     │
│  IDENTITY UPDATE (post-extraction job):                             │
│  ├── Sync facets → person_facts (for resolution queries)            │
│  ├── Index hard identifiers → identities table                      │
│  ├── Create new person nodes for third parties                      │
│  └── Queue resolution check                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Why LLM-Only (No Regex Fast Pass)

Regex extraction without LLM context leads to false positives:
- "Send this to john@example.com" - Is this John's email or someone else's?
- Phone numbers in messages could be anyone's
- Context matters: "my email" vs "his email" vs "the support email"

The LLM understands:
- **Attribution**: Whose identifier is this?
- **Self-disclosure**: "my email is X" vs "contact X at Y"
- **Relationships**: "send this to mom's email"
- **Context**: Business vs personal, forwarding vs sharing

---

## Identity Resolution Algorithm

### Key Insight: Identifier-Centric (O(F) not O(P²))

**Bad approach** - compare all person pairs:
```
FOR each person P1:
  FOR each person P2:
    compare(P1, P2)  # O(P²) = millions of comparisons
```

**Good approach** - iterate through facts, find collisions:
```
FOR each fact_type in ORDER BY hardness DESC:
  GROUP facts BY fact_value
  FOR each group WHERE count > 1:
    # Multiple persons share this exact value
    process_collision(persons_in_group, fact_type)
```

This is O(F) where F = number of facts, not O(P²) where P = persons.

### Resolution Algorithm

```
RESOLVE_IDENTITIES():
  similarity_scores = {}  # (person1, person2) -> score
  
  # Phase 1: Hard identifier resolution
  FOR type IN ['email_personal', 'email_work', 'phone_mobile', 'phone_home',
               'full_legal_name', 'social_handle_twitter', 'social_handle_linkedin', ...]:
    
    collisions = SQL """
      SELECT fact_value, GROUP_CONCAT(person_id) as persons
      FROM person_facts
      WHERE fact_type = {type} AND is_identifier = 1
      GROUP BY fact_value
      HAVING COUNT(DISTINCT person_id) > 1
    """
    
    FOR each collision:
      persons = collision.persons.split(',')
      IF type IN HARD_IDENTIFIERS AND avg_confidence(persons, type) >= 0.8:
        # High confidence hard ID match
        CREATE merge_event(persons, type='hard_identifier', auto=TRUE)
      ELSE:
        CREATE merge_suggestion(persons, type, confidence)

  # Phase 2: Compound identifier resolution
  compound_matches = SQL """
    SELECT pf1.person_id as p1, pf2.person_id as p2
    FROM person_facts pf1
    JOIN person_facts pf2 ON pf1.fact_value = pf2.fact_value 
      AND pf1.person_id < pf2.person_id
    WHERE pf1.fact_type = 'full_name'
    GROUP BY pf1.person_id, pf2.person_id
    HAVING 
      SUM(CASE WHEN pf1.fact_type = 'birthdate' THEN 1 ELSE 0 END) > 0
      OR (SUM(CASE WHEN pf1.fact_type = 'employer_current' THEN 1 ELSE 0 END) > 0
          AND SUM(CASE WHEN pf1.fact_type = 'location_current' THEN 1 ELSE 0 END) > 0)
  """
  FOR each match:
    CREATE merge_suggestion(match.p1, match.p2, type='compound', confidence=0.85)

  # Phase 3: Soft identifier accumulation
  FOR type IN ['employer_current', 'location_current', 'profession', 
               'spouse_first_name', 'school_attended', 'birthdate']:
    weight = WEIGHTS[type]  # 0.15-0.25
    
    collisions = find_collisions(type)
    FOR each collision:
      FOR p1, p2 IN pairs(collision.persons):
        similarity_scores[(p1, p2)] += weight

  # Phase 4: Generate suggestions from accumulated scores
  FOR (p1, p2), score IN similarity_scores:
    IF score >= 0.6:
      matching_facts = get_shared_facts(p1, p2)
      CREATE merge_suggestion(p1, p2, matching_facts, confidence=score)

  # Phase 5: Execute auto-merges
  FOR each merge_event WHERE auto = TRUE:
    # Validate no conflicts
    IF has_conflicting_facts(source, target):
      DOWNGRADE to merge_suggestion
    ELSE:
      EXECUTE_MERGE(source, target)
      # Move all facts, identities from source to target
      # Mark source as merged_into target
```

### Handling Ambiguous Data

For data that can't be attributed (phone number sent with no context):

```sql
CREATE TABLE unattributed_facts (
    id TEXT PRIMARY KEY,
    fact_type TEXT NOT NULL,           -- "phone", "email", etc.
    fact_value TEXT NOT NULL,
    shared_by_person_id TEXT,          -- who sent it
    source_event_id TEXT,              -- the message
    source_conversation_id TEXT,
    context TEXT,                      -- any surrounding context
    possible_attributions TEXT,        -- JSON array of guesses
    
    resolved_to_person_id TEXT,        -- filled when we figure it out
    resolution_evidence TEXT,
    
    created_at INTEGER NOT NULL,
    resolved_at INTEGER
);
```

Later context can resolve these: "that's my sister's number" → attribute to sister.

---

## Data Model

### person_facts Table

```sql
CREATE TABLE person_facts (
    id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL REFERENCES persons(id),
    
    -- What fact
    category TEXT NOT NULL,         -- 'core_identity', 'contact', 'professional', etc.
    fact_type TEXT NOT NULL,        -- 'email_work', 'full_name', 'business_owned', etc.
    fact_value TEXT NOT NULL,       -- the actual value
    
    -- Confidence & Source
    confidence REAL DEFAULT 0.5,    -- 0.0-1.0
    source_type TEXT NOT NULL,      -- 'self_disclosed', 'mentioned', 'inferred', 'signature'
    source_channel TEXT,            -- 'imessage', 'gmail', etc.
    source_conversation_id TEXT,    -- conversation where extracted
    source_facet_id TEXT,           -- link to facets table
    evidence TEXT,                  -- quote from message
    
    -- Classification
    is_sensitive INTEGER DEFAULT 0,    -- SSN, medical, financial
    is_identifier INTEGER DEFAULT 0,   -- used for identity matching
    is_hard_identifier INTEGER DEFAULT 0,  -- triggers instant merge consideration
    
    -- Timestamps
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    
    UNIQUE(person_id, category, fact_type, fact_value)
);

CREATE INDEX idx_person_facts_person ON person_facts(person_id);
CREATE INDEX idx_person_facts_type ON person_facts(category, fact_type);
CREATE INDEX idx_person_facts_value ON person_facts(fact_value);
CREATE INDEX idx_person_facts_hard_id ON person_facts(fact_type, fact_value) 
    WHERE is_hard_identifier = 1;
```

### unattributed_facts Table

```sql
CREATE TABLE unattributed_facts (
    id TEXT PRIMARY KEY,
    fact_type TEXT NOT NULL,
    fact_value TEXT NOT NULL,
    
    shared_by_person_id TEXT REFERENCES persons(id),
    source_event_id TEXT REFERENCES events(id),
    source_conversation_id TEXT REFERENCES conversations(id),
    context TEXT,
    possible_attributions TEXT,     -- JSON
    
    resolved_to_person_id TEXT REFERENCES persons(id),
    resolution_evidence TEXT,
    
    created_at INTEGER NOT NULL,
    resolved_at INTEGER
);

CREATE INDEX idx_unattributed_value ON unattributed_facts(fact_type, fact_value);
CREATE INDEX idx_unattributed_unresolved ON unattributed_facts(resolved_to_person_id) 
    WHERE resolved_to_person_id IS NULL;
```

### merge_events Table

```sql
CREATE TABLE merge_events (
    id TEXT PRIMARY KEY,
    source_person_id TEXT NOT NULL,
    target_person_id TEXT NOT NULL,
    merge_type TEXT NOT NULL,        -- 'hard_identifier', 'compound', 'soft_accumulation', 'manual'
    
    triggering_facts TEXT,           -- JSON array of facts that caused merge
    similarity_score REAL,
    
    status TEXT DEFAULT 'pending',   -- 'pending', 'accepted', 'rejected', 'executed'
    auto_eligible INTEGER DEFAULT 0, -- whether this can auto-execute
    
    created_at INTEGER NOT NULL,
    resolved_at INTEGER,
    resolved_by TEXT                 -- 'auto' or user identifier
);

CREATE INDEX idx_merge_events_status ON merge_events(status);
CREATE INDEX idx_merge_events_persons ON merge_events(source_person_id, target_person_id);
```

---

## CLI Interface

```bash
# Run PII extraction on conversations
comms extract pii [--channel imessage|gmail|all] [--since 7d] [--top N]
comms extract pii --conversation <conversation_id>
comms extract pii --person <person_id>

# View extraction status
comms extract status [--pending|--completed|--failed]

# Run identity resolution
comms identify resolve [--full|--incremental]
comms identify resolve --dry-run  # show what would merge

# View person's identity graph
comms person facts <person_id> [--include-evidence]
comms person profile <person_id>  # rich formatted view

# View merge suggestions
comms identify merges [--status pending|accepted|rejected]
comms identify merges --auto-eligible  # show what could auto-merge

# Accept/reject merges
comms identify accept <merge_id>
comms identify reject <merge_id>
comms identify accept --all-auto  # accept all auto-eligible

# Force merge two identities
comms identify merge <person_id_1> <person_id_2> [--force]

# View resolution stats
comms identify status
# Shows: persons, merges executed, pending suggestions, unattributed facts

# Resolve unattributed facts
comms identify unattributed [--unresolved]
comms identify attribute <fact_id> --person <person_id>
```

---

## Implementation Plan

### Phase 1: Schema & Infrastructure (US-030 - US-033)
- [ ] Add person_facts table to schema
- [ ] Add unattributed_facts table to schema
- [ ] Add merge_events table to schema
- [ ] Create fact insertion/query utilities in internal/identify/facts.go

### Phase 2: PII Extraction Analysis Type (US-034 - US-037)
- [ ] Register pii_extraction_v1 as analysis_type
- [ ] Implement extraction job runner (uses analysis framework)
- [ ] Build facet → person_facts sync job
- [ ] Handle third-party identity creation from extraction

### Phase 3: Resolution Algorithm (US-038 - US-042)
- [ ] Implement identifier collision detection (O(F) algorithm)
- [ ] Implement hard identifier merge logic
- [ ] Implement compound identifier matching
- [ ] Implement soft identifier scoring
- [ ] Build merge execution with conflict detection

### Phase 4: CLI Commands (US-043 - US-047)
- [ ] Add `comms extract pii` command
- [ ] Add `comms identify resolve` command
- [ ] Add `comms identify merges` commands
- [ ] Add `comms person facts/profile` commands
- [ ] Add `comms identify status` command

### Phase 5: Channel Extraction (US-048 - US-050)
- [ ] Run extraction on iMessage conversations
- [ ] Run extraction on Gmail threads
- [ ] Cross-channel resolution sweep

### Phase 6: PII Post-Processing Pipeline (Accuracy + Scale)
- [ ] Store raw extraction output in staging (raw JSON + minimal metadata)
- [ ] Enforce a strict key allowlist (reject unknown keys, log for review)
- [ ] Add alias mapping for common drift keys (attractors)
- [ ] Canonicalize fact values prior to insertion
- [ ] Deduplicate facts using normalized values (before resolution)
- [ ] Split Tier 1 identifiers vs Tier 2 enrichment
- [ ] Only Tier 1 enters collision detection and matching
- [ ] Gate third-party creation: require >=1 identifier-grade fact
- [ ] Keep third-party mentions in staging if identifier-grade is missing
- [ ] Add prompt guardrails: ignore speaker labels for full_legal_name

### Phase 7: Ontology from Corpus (Iterative)
- [ ] Export all observed keys + counts from extracted corpus
- [ ] Embed keys + sample values and cluster to propose canonical ontology
- [ ] Pick canonical keys and update prompt schema + key map
- [ ] Repeat with larger samples until ontology stabilizes
- [ ] Add runtime telemetry for new/unrecognized keys

### Phase 8: Conversation Chunking Experiments
- [ ] Compare 50-100 message chunks vs 500 vs monthly/quarterly
- [ ] Track identifier recall, third-party rate, collision group size
- [ ] Manually spot-check precision on each chunk size

---

## Cost Analysis

| Operation | LLM Calls | Cost Estimate |
|-----------|-----------|---------------|
| Extract top 100 iMessage contacts | ~200 | $4-8 |
| Extract top 100 Gmail contacts | ~200 | $4-8 |
| Extract AIX sessions | ~50 | $1-2 |
| **Initial full extraction** | ~450 | **$10-18** |

Incremental: Only new conversations, ~$0.50-1/week for active user.

---

## Quality Metrics

### Baseline Snapshot (2026-01-14, current dataset)
- Total facts: 24,336
- Identifier-grade facts: 2,238 (hard: 678, soft: 1,560)
- Enrichment facts: 22,098
- Distinct fact types: 1,175
- Conversations with facts: 2,443
- Avg facts per conversation: 9.96 (max: 45)
- Name collision groups (count, max size):
  - full_legal_name: 20 groups (max 11)
  - full_name: 24 groups (max 39)
  - given_name: 159 groups (max 174)
  - family_name: 28 groups (max 55)
- Handle/email collision groups (count, max size):
  - email_personal: 2 groups (max 4)
  - phone_mobile: 11 groups (max 5)
  - social_twitter: 11 groups (max 2)
  - social_instagram: 4 groups (max 2)
  - social_linkedin: 1 group (max 2)
- Top drift keys (not in prompt schema): relationship_to_primary, evidence, context, full_name, relationship_to_user, nickname, relationship_to_group, relationship, role, dietary_preferences, location, digital_identity

```sql
-- Resolution completeness
SELECT 
  (SELECT COUNT(*) FROM persons WHERE merged_into IS NULL) as active_persons,
  (SELECT COUNT(*) FROM persons WHERE merged_into IS NOT NULL) as merged_persons,
  (SELECT COUNT(*) FROM person_facts) as total_facts,
  (SELECT COUNT(*) FROM person_facts WHERE is_hard_identifier = 1) as hard_identifiers,
  (SELECT COUNT(*) FROM merge_events WHERE status = 'pending') as pending_merges,
  (SELECT COUNT(*) FROM unattributed_facts WHERE resolved_to_person_id IS NULL) as unresolved_facts;

-- Cross-channel linkage
SELECT 
  p.id,
  p.canonical_name,
  COUNT(DISTINCT pf.source_channel) as channels_linked
FROM persons p
JOIN person_facts pf ON p.id = pf.person_id
WHERE p.merged_into IS NULL
GROUP BY p.id
ORDER BY channels_linked DESC;
```

---

## Related Documents

- **PII Extraction Prompt**: `/prompts/pii-extraction-v1.prompt.md`
- **Schema Design Analysis**: `/docs/SCHEMA_DESIGN_ANALYSIS.md`
- **Eve Migration Analysis**: `/docs/EVE_COMMS_MIGRATION_ANALYSIS.md`
