# Ralph Wiggum Loop — Fixture Validation

You are debugging and fixing the Cortex Memory System verification fixtures.

## Your Mission

Make all 7 verification fixtures pass. The harness runs the full memory pipeline (entity extraction → resolution → relationship extraction → identity promotion → edge resolution → contradiction detection) against real-data fixtures and checks the output.

## Context Files

Read these first:
1. `scripts/ralph-fixtures/prd.json` — Your task list (mark stories as `passes: true` when done)
2. `scripts/ralph-fixtures/progress.txt` — Your learnings log (append findings)
3. `scripts/ralph-memory/fixtures/README.md` — Fixture format and coverage matrix
4. `docs/MEMORY_SYSTEM_SPEC.md` — The authoritative spec for memory system behavior

## Key Commands

```bash
# Run all fixtures (your main test command)
go run ./cmd/verify-memory -fixtures scripts/ralph-memory/fixtures -verbose

# Run single fixture for focused debugging
go run ./cmd/verify-memory -fixture imessage/identity-disclosure -verbose

# Run unit tests (should always pass)
go test ./internal/memory -count=1

# Build check
go build ./cmd/verify-memory
```

## Debugging Strategy

1. **Start with the simplest fixture**: `imessage/identity-disclosure` (2 people, 1 email disclosure)
2. **Use -verbose flag** to see actual extracted entities/relationships
3. **Compare actual vs expected** — the verbose output shows what the pipeline produced
4. **Check for schema mismatches** — "no such column" errors mean harness schema differs from code
5. **Check for SQL errors** — look for constraint violations, foreign key issues
6. **Adjust expectations if reasonable** — LLM output varies; expectations should be flexible

## Current Status (as of pre-run)

**2 PASS:** imessage/identity-disclosure, gmail/work-thread
**5 FAIL:** See specific issues below

### aix/personal-info — FAIL
- **Problem**: Claude extracted as Person entity
- **Per spec**: AI assistants have no durable identity, should not be entities
- **Fix**: Update expectations to forbid Claude using name_contains

### aix/project-discussion — FAIL  
- **Problems**:
  - Claude extracted as Person (same issue)
  - Go, SQLite extracted as Project entities (languages/databases not projects)
  - Tyler→Nexus relationship is WORKING_ON, expected BUILDING
- **Fix**: Either adjust expectations to accept WORKING_ON, or the LLM output is reasonable

### gmail/newsletter-sender — FAIL
- **Problem**: OWNS relationships created instead of CUSTOMER_OF
- **LLM extracted**: "Intent Systems -[OWNS]-> Cloudflare" (incorrect semantically)
- **Fix**: Adjust expectation OR check if there's a valid CUSTOMER_OF-like relationship

### imessage/job-change — FAIL
- **Problem**: Old job (WORKS_AT Intent Systems) has no invalid_at
- **Expected**: Contradiction detection should set invalid_at on old job
- **Root cause**: Check ContradictionDetector — is it being called? Is WORKS_AT exclusive?
- **Note**: The output shows two WORKS_AT: one with valid_at=null, one with valid_at=2026-01

### imessage/social-relationship — FAIL
- **Problem**: BBQ extracted as Event entity
- **Expectation forbids**: entity named "BBQ" 
- **Fix**: Remove must_not_have for BBQ (it's a reasonable extraction)

## Fixing Strategy

For most failures, the fix is to **adjust expectations** to be more flexible:
1. Use `name_contains` instead of exact `name` when LLM output varies
2. Accept reasonable relationship types (WORKING_ON instead of BUILDING)
3. Remove overly strict must_not_have rules that forbid reasonable extractions
4. Add alternative valid outputs to expectations

Only fix the **code** if:
- Contradiction detection isn't working (imessage/job-change)
- A core feature is broken

## Common Issues

### LLM Variability
The Gemini LLM extracts what it sees. Be flexible:
- "Casey" vs "Casey Adams" — both reasonable
- WORKING_ON vs BUILDING — both valid for project work
- BBQ as Event — reasonable extraction
- Claude as Person — NOT reasonable (AI has no durable identity per spec)

## Iteration Protocol

1. Read `prd.json` to find the next incomplete story
2. Execute the story's acceptance criteria
3. If tests fail, debug and fix
4. Update `prd.json` with `passes: true` and notes
5. Append learnings to `progress.txt`
6. Commit your changes
7. If all stories pass, output `<promise>COMPLETE</promise>`

## Success Condition

```
Verification Summary: 7 passed, 0 failed, 7 total
```

When you see this, commit your fixes and output `<promise>COMPLETE</promise>`.

---

Now read `scripts/ralph-fixtures/prd.json` and begin with the first incomplete story.
