# Ralph Agent Instructions — Identity Resolution

## Context

You are implementing the PII extraction and identity resolution system for `comms`. This adds:
- **person_facts** table (extracted PII linked to persons)
- **unattributed_facts** table (ambiguous data awaiting resolution)
- **merge_events** table (identity merge tracking)
- **PII extraction** as an analysis_type (uses existing analysis framework)
- **Resolution algorithm** (identifier-centric O(F) approach)
- **CLI commands** for extraction and resolution

**Prerequisites**: The Eve→Comms migration must be complete first. This system builds on:
- `conversations` table (chunked event groups)
- `analysis_types` + `analysis_runs` + `facets` tables (generic analysis framework)
- `threads` table (chat/channel metadata)

The detailed design is in `docs/IDENTITY_RESOLUTION_PLAN.md` — **READ THIS FIRST**.

## Key Files

- `docs/IDENTITY_RESOLUTION_PLAN.md` — **The PRD for identity resolution** (READ THIS)
- `prompts/pii-extraction-v1.prompt.md` — The LLM prompt for PII extraction
- `scripts/ralph-identity/prd.json` — User stories with acceptance criteria
- `scripts/ralph-identity/progress.txt` — Learnings and patterns
- `AGENTS.md` — Codebase patterns for this project
- `internal/db/schema.sql` — Current database schema

## Your Task

1. Read `docs/IDENTITY_RESOLUTION_PLAN.md` (the identity resolution spec)
2. Read `prompts/pii-extraction-v1.prompt.md` (the extraction prompt)
3. Read `scripts/ralph-identity/prd.json` for user stories
4. Read `scripts/ralph-identity/progress.txt` (especially Codebase Patterns at top)
5. Pick the highest priority story where `passes: false`
6. Implement that ONE story following the design doc
7. Run `go build ./cmd/comms` to verify it compiles
8. Run `go test ./...` if tests exist
9. Update AGENTS.md with learnings about this codebase
10. Commit: `feat: [US-XXX] - [Title]`
11. Update prd.json: set `passes: true` for completed story
12. Append learnings to progress.txt

## Key Design Decisions

### Identifier Taxonomy

```
HARD IDENTIFIERS (1 match = merge candidate):
  email_personal, email_work, phone_mobile, phone_home, phone_work,
  social_handle_*, username_*, full_legal_name

COMPOUND HARD (all parts match = merge):
  full_name + birthdate
  full_name + employer + city
  first_name + spouse_name + children_count + city

CORRELATING (accumulate for scoring):
  employer_current (0.20), location_current (0.15), profession (0.15),
  spouse_first_name (0.25), school_attended (0.15), birthdate (0.25)

ENRICHMENT (profile only, never merge):
  hobbies, interests, preferences, personality_traits

SHARED/JOINT (flag, don't auto-merge):
  bank_account, address_home, family_phone, business_email
```

### Resolution Algorithm (O(F) not O(P²))

```sql
-- Find collisions by grouping facts, NOT by comparing all person pairs
SELECT fact_value, GROUP_CONCAT(person_id) as persons, COUNT(*) as cnt
FROM person_facts 
WHERE fact_type = 'email_personal' AND is_hard_identifier = 1
GROUP BY fact_value
HAVING cnt > 1;
```

### Integration with Analysis Framework

PII extraction is an `analysis_type`. Output goes to `facets` table, then syncs to `person_facts`:

```
conversations → analysis_runs → facets (pii_*) → person_facts
```

### Professional: Owner vs Employer

```sql
-- IMPORTANT DISTINCTION:
employer_current = where you work FOR someone
business_owned = businesses you OWN (can be multiple)
business_role = Owner, Co-owner, Partner, Founder
```

## Schema Summary

```sql
-- person_facts: extracted PII linked to persons
CREATE TABLE person_facts (
    id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL REFERENCES persons(id),
    category TEXT NOT NULL,
    fact_type TEXT NOT NULL,
    fact_value TEXT NOT NULL,
    confidence REAL DEFAULT 0.5,
    source_type TEXT NOT NULL,
    source_channel TEXT,
    source_conversation_id TEXT,
    source_facet_id TEXT,
    evidence TEXT,
    is_sensitive INTEGER DEFAULT 0,
    is_identifier INTEGER DEFAULT 0,
    is_hard_identifier INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    UNIQUE(person_id, category, fact_type, fact_value)
);

-- unattributed_facts: ambiguous data awaiting resolution  
CREATE TABLE unattributed_facts (
    id TEXT PRIMARY KEY,
    fact_type TEXT NOT NULL,
    fact_value TEXT NOT NULL,
    shared_by_person_id TEXT REFERENCES persons(id),
    source_event_id TEXT,
    source_conversation_id TEXT,
    context TEXT,
    possible_attributions TEXT,
    resolved_to_person_id TEXT REFERENCES persons(id),
    resolution_evidence TEXT,
    created_at INTEGER NOT NULL,
    resolved_at INTEGER
);

-- merge_events: identity merge tracking
CREATE TABLE merge_events (
    id TEXT PRIMARY KEY,
    source_person_id TEXT NOT NULL,
    target_person_id TEXT NOT NULL,
    merge_type TEXT NOT NULL,
    triggering_facts TEXT,
    similarity_score REAL,
    status TEXT DEFAULT 'pending',
    auto_eligible INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    resolved_at INTEGER,
    resolved_by TEXT
);
```

## Code Patterns

### Go Patterns for This Module

```go
// internal/identify/facts.go - fact management
func InsertFact(db *sql.DB, fact PersonFact) error
func GetFactsForPerson(db *sql.DB, personID string) ([]PersonFact, error)
func FindFactCollisions(db *sql.DB, factType string) ([]FactCollision, error)

// internal/identify/resolve.go - resolution algorithm
func RunResolution(db *sql.DB, opts ResolveOptions) (*ResolutionResult, error)
func DetectHardIDCollisions(db *sql.DB) ([]MergeCandidate, error)
func ScoreSoftIdentifiers(db *sql.DB) (map[PersonPair]float64, error)
func ExecuteMerge(db *sql.DB, mergeID string) error

// internal/extract/pii.go - extraction integration
func RunPIIExtraction(db *sql.DB, conversationID string) (*ExtractionResult, error)
func SyncFacetsToPersonFacts(db *sql.DB, analysisRunID string) error
```

### Fact Type Constants

```go
// Maintain consistency with these constants
const (
    FactTypeEmailPersonal = "email_personal"
    FactTypeEmailWork     = "email_work"
    FactTypePhoneMobile   = "phone_mobile"
    FactTypePhoneHome     = "phone_home"
    FactTypeFullName      = "full_legal_name"
    FactTypeEmployer      = "employer_current"
    FactTypeBusinessOwned = "business_owned"
    // ... etc
)

var HardIdentifiers = []string{
    FactTypeEmailPersonal, FactTypeEmailWork,
    FactTypePhoneMobile, FactTypePhoneHome,
    FactTypeFullName,
    // ... platform handles
}
```

## Progress Format

APPEND to progress.txt:

```
---

## [Date] - [Story ID]
- What was implemented
- Files changed
- **Learnings:**
  - Patterns discovered
  - Gotchas encountered
```

## Codebase Patterns

Add reusable patterns to the TOP of progress.txt:

```
## Codebase Patterns
- Use raw SQL, not ORM
- No __init__.py files needed
- modernc.org/sqlite for pure-Go SQLite
- JSON output support: --json flag
```

## Stop Condition

If ALL stories pass, reply:
`<promise>COMPLETE</promise>`

Otherwise end normally.

## Rules

1. **ONE story per iteration** — Do not implement multiple stories
2. **Build must pass** — `go build ./cmd/comms` must succeed before committing
3. **Follow design doc** — Use exact schema from IDENTITY_RESOLUTION_PLAN.md
4. **No placeholders** — Full implementations only
5. **Update progress.txt** — Capture learnings for future iterations
6. **Update AGENTS.md** — Document codebase patterns
7. **Commit message format** — `feat: [US-XXX] - [Title]`
8. **Raw SQL only** — NO ORMs for queries (user rule)
