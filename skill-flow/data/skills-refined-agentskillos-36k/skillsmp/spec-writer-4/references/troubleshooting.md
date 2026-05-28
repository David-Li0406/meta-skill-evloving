# Troubleshooting Guide

Quick reference for diagnosing and fixing common spec-writer script issues.

## Quick Diagnosis Flowchart

```
Script Error?
│
├─ "Invalid ID format" ────────────────────────────────────┐
│  └─ See: ID Format Issues                                │
│                                                            │
├─ "Not found in..." ────────────────────────────────────┐  │
│  └─ See: Cross-Reference Validation                     │  │
│                                                            │  │
├─ "Newlines break pipe format" ────────────────────────┐  │  │
│  └─ See: JSON Stdin Issues                            │  │  │
│                                                            │  │  │
├─ "Story is not marked as 'In Progress'" ─────────────┐  │  │  │
│  └─ See: Story Lifecycle Issues                       │  │  │  │
│                                                            │  │  │  │
├─ "Multiple stories marked as 'In Progress'" ─────────┐  │  │  │  │
│  └─ See: Story Status Conflicts                       │  │  │  │  │
│                                                            │  │  │  │  │
└─ Other error ────────────────────────────────────────┐  │  │  │  │  │
   └─ See: Script-Specific Issues                      │  │  │  │  │  │
                                                         │  │  │  │  │  │
                                                         v  v  v  v  v  v
                                                    Find detailed help below
```

---

## Common Error Categories

### 1. ID Format Issues

**Symptoms:**
- `ERROR: Invalid [entity] ID format: [ID]`
- `Expected format: [FORMAT]`

**Cause:**
Scripts now accept flexible ID formats but there may be confusion about valid formats.

**✅ Solution:**
All ID types accept multiple flexible formats that normalize automatically:

| Entity Type | Flexible Formats | Normalizes To |
|-------------|------------------|---------------|
| Decision | `D1`, `D01`, `d1`, `D-01` | `D1` |
| Question | `Q1`, `Q01`, `q1`, `Q-01` | `Q1` |
| Research | `R1`, `R01`, `r1`, `R-01` | `R1` |
| Iteration | `ITR1`, `ITR-001`, `itr-1` | `ITR-001` |
| Revision | `REV1`, `REV-001`, `rev-1` | `REV-001` |
| Functional Req | `FR5`, `FR-005`, `fr-5` | `FR-005` |
| Edge Case | `EC1`, `EC-01`, `ec-1` | `EC-01` |
| Success Criteria | `SC1`, `SC-001`, `sc-1` | `SC-001` |

**Examples:**
```bash
# All these work and normalize automatically:
find-decisions.py --id D1,D2,D3
find-decisions.py --id d01,d02,d03      # Same result
find-decisions.py --id D-001,D-002      # Same result

log-decision.py --questions "Q1, q02, Q-3"  # Normalizes to: Q1, Q2, Q3
```

---

### 2. Cross-Reference Validation

**Symptoms:**
- `⚠️  WARNING: Story [N] not found in STATE.md`
- `⚠️  WARNING: Question [Q#] not found in OPEN_QUESTIONS.md`
- `⚠️  WARNING: Decision [D#] not found in DECISIONS.md`
- Followed by: `Did you mean one of: ...?`

**Cause:**
Scripts now validate cross-references and provide fuzzy suggestions when referenced entities don't exist.

**✅ Solution:**

1. **Check the suggestions first** - The script provides the 5 closest matches
2. **Verify the entity exists** before referencing it
3. **Warnings don't block execution** - They're informational to catch typos

**Examples:**

❌ **Bad - Referencing non-existent story:**
```bash
log-decision.py --title "..." --stories "Story 99"
# WARNING: Story 99 not found in STATE.md
#          Did you mean one of: 1, 2, 3?
```

✅ **Good - Check STATE.md first:**
```bash
# 1. Check what stories exist
grep "^| [0-9]" discovery/STATE.md

# 2. Use correct story number
log-decision.py --title "..." --stories "Story 1"
```

❌ **Bad - Typo in question ID:**
```bash
log-research.py --topic "..." --questions "Q99"
# WARNING: Question Q99 not found in OPEN_QUESTIONS.md
#          Did you mean: Q9, Q8, Q7?
```

✅ **Good - Use fuzzy suggestion:**
```bash
log-research.py --topic "..." --questions "Q9"  # Use suggested Q9
```

**Quick Checks:**
```bash
# Check what exists before referencing
grep "^\| [0-9]" discovery/STATE.md                    # Stories
grep "^\*\*Q[0-9]" discovery/OPEN_QUESTIONS.md          # Questions
grep "^## D[0-9]" discovery/archive/DECISIONS.md        # Decisions
grep "^## R[0-9]" discovery/archive/RESEARCH.md         # Research
```

---

### 3. JSON Stdin Issues

**Symptoms:**
- Pipe-separated input fails with multiline text
- Special characters break parsing
- `ERROR: Pipe-separated input requires: ...`

**Cause:**
Pipe-separated format (`|`) doesn't handle newlines, special characters, or complex text well.

**✅ Solution:**
Use JSON stdin for complex content (multiline, special chars, structured data).

**Migration Guide:**

❌ **Bad - Pipe-separated with multiline:**
```bash
echo "Title|Context with\nnewlines|Decision" | log-decision.py --from-stdin
# FAILS: Newlines break pipe format
```

✅ **Good - JSON handles multiline:**
```bash
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Title",
  "context": "Context with\nmultiple\nlines",
  "decision": "Decision"
}
EOF
```

❌ **Bad - Special chars in pipe format:**
```bash
echo "Title|Context with | pipes|Decision" | log-decision.py --from-stdin
# FAILS: Pipes inside text break parsing
```

✅ **Good - JSON handles special chars:**
```bash
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Title",
  "context": "Context with | pipes and special chars: @#$%",
  "decision": "Decision"
}
EOF
```

**JSON-Enabled Scripts:**
- `log-decision.py` - Use `--from-json` or `--json-file`
- `log-iteration.py` - Use `--from-json` or `--json-file`
- `log-research.py` - Use `--from-json` or `--json-file`

**JSON File Example:**
```bash
# decision.json
{
  "title": "Use bidirectional dependency tracking",
  "context": "Both Feature Developers and Service Owners need visibility",
  "decision": "Use bidirectional tracking",
  "rationale": "Serves both personas with single data model",
  "stories": "Story 1, Story 2",
  "questions": "Q1, Q3, Q7"
}

# Use it
log-decision.py --json-file decision.json
```

See: `schemas/README.md` for complete JSON documentation and schema reference.

---

### 4. Story Lifecycle Issues

**Symptoms:**
- `ERROR: Story [N] is not marked as 'In Progress' in STATE.md`
- `ERROR: Story [N] not ready for graduation`
- `ERROR: Story [N] details not found in STATE.md`

**Cause:**
Stories must follow a specific lifecycle: Queued → In Progress → In SPEC

**✅ Solution:**

**Story Lifecycle:**
```
1. ⏳ Queued        - Story identified, not started
2. 🔄 In Progress  - Story being developed (only ONE at a time)
3. ✅ In SPEC      - Story graduated to SPEC.md
```

**Required for graduation:**
1. Story status is "🔄 In Progress"
2. Story has "In-Progress Story Detail" section in STATE.md
3. At least one acceptance scenario exists
4. Priority is set (P1/P2/P3)

**Example Workflow:**
```bash
# 1. Set story to in progress
update-story-status.py --story-number 3 --status in_progress

# 2. Add details to "In-Progress Story Detail" in STATE.md manually
#    - Title
#    - Priority
#    - Draft Acceptance Scenarios

# 3. Graduate when ready
graduate-story.py --story-number 3

# If not ready, use --dry-run to preview
graduate-story.py --story-number 3 --dry-run
```

**Common Mistakes:**

❌ **Bad - Trying to graduate queued story:**
```bash
graduate-story.py --story-number 1
# ERROR: Story 1 is not marked as 'In Progress' in STATE.md
```

✅ **Good - Set to in progress first:**
```bash
update-story-status.py --story-number 1 --status in_progress
# Then add details to STATE.md
graduate-story.py --story-number 1
```

---

### 5. Story Status Conflicts

**Symptoms:**
- `ERROR: Story [N] is already 'In Progress'. Only one story can be in progress at a time.`
- `ERROR: Multiple stories marked as 'In Progress' (N)`

**Cause:**
The workflow enforces single-story focus - only ONE story can be "In Progress" at a time.

**✅ Solution:**

**Option 1 - Move old story to queued:**
```bash
# 1. Move current in-progress story back to queued
update-story-status.py --story-number 2 --status queued

# 2. Set new story to in progress
update-story-status.py --story-number 3 --status in_progress
```

**Option 2 - Graduate the in-progress story:**
```bash
# 1. Finish current story
graduate-story.py --story-number 2

# 2. Set new story to in progress
update-story-status.py --story-number 3 --status in_progress
```

**Check current status:**
```bash
# Find which story is in progress
grep "🔄 In Progress" discovery/STATE.md
```

---

## Script-Specific Issues

### log-decision.py

**Issue:** Question IDs not normalizing
**Solution:**
```bash
# All these are equivalent and auto-normalize:
log-decision.py --questions "Q1, Q2, Q3"
log-decision.py --questions "q1, q2, q3"
log-decision.py --questions "Q-01, Q-02, Q-03"
```

**Issue:** Story reference gives warning
**Solution:** Check STATE.md Story Status Overview table for valid story numbers

**Issue:** Multiline context breaks pipe input
**Solution:** Use `--from-json` instead of `--from-stdin`

---

### log-iteration.py

**Issue:** ID lists with ranges not working
**Solution:** Ranges are fully supported:
```bash
log-iteration.py \
  --questions-added "Q1-Q5" \
  --decisions-made "D1, D2" \
  --research-conducted "R1-R3"
```

**Issue:** Complex multiline content
**Solution:** Use JSON input:
```bash
cat <<'EOF' | log-iteration.py --from-json
{
  "date_range": "2026-01-19",
  "phase": "Problem Exploration",
  "goals": "Goal 1; Goal 2; Goal 3",
  "activities": "Activity 1\nActivity 2\nActivity 3",
  "questions_added": "Q1-Q5",
  "decisions_made": "D1, D2"
}
EOF
```

---

### log-research.py

**Issue:** Question IDs not found
**Solution:** Verify questions exist first:
```bash
grep "^\*\*Q" discovery/OPEN_QUESTIONS.md
log-research.py --questions "Q15, Q18"  # Use existing IDs
```

**Issue:** Multiline findings/patterns
**Solution:** Use JSON input for complex content

---

### graduate-story.py

**Issue:** Story not found
**Solution:**
```bash
# Check STATE.md for valid story numbers
grep "^\| [0-9]" discovery/STATE.md

# Use correct number
graduate-story.py --story-number 3
```

**Issue:** Story not in progress
**Solution:**
```bash
update-story-status.py --story-number 3 --status in_progress
graduate-story.py --story-number 3
```

**Issue:** Story missing scenarios
**Solution:** Add "In-Progress Story Detail" section to STATE.md with:
- Title
- Priority
- Draft Acceptance Scenarios (at least one)

---

### find-* scripts (find-decisions.py, find-research.py, find-iterations.py)

**Issue:** No results found
**Solution:** Check filters independently:
```bash
# Bad - mixed filters
find-decisions.py --story 1 --question Q99  # May return nothing

# Good - check each filter
find-decisions.py --story 1          # See decisions for Story 1
find-decisions.py --question Q99     # See if Q99 has decisions
```

**Issue:** ID format not recognized
**Solution:** All flexible formats work:
```bash
find-decisions.py --id D1,D2,D3
find-decisions.py --id d01,d02,d03      # Same result
find-decisions.py --id D-001,D-002       # Same result
```

---

### SPEC.md table scripts (add-functional-requirement.py, add-edge-case.py, add-success-criteria.py)

**Issue:** Story reference warnings
**Solution:** Always check STATE.md first:
```bash
# Check valid stories
grep "^\| [0-9]" discovery/STATE.md

# Then add with correct references
add-functional-requirement.py \
  --requirement "System MUST..." \
  --stories "Story 1, Story 2"
```

**Issue:** ID format errors
**Solution:** Use flexible formats:
```bash
# All these work:
echo "FR-005|..." | add-functional-requirement.py --from-stdin
echo "fr5|..." | add-functional-requirement.py --from-stdin
echo "FR5|..." | add-functional-requirement.py --from-stdin
```

---

## Recovery Procedures

### Corrupted STATE.md or SPEC.md

**Symptoms:**
- Parse errors
- Validation failures
- Missing sections

**Solution:**
1. Check git history: `git log -- discovery/STATE.md`
2. Restore from backup: `git checkout HEAD~1 -- discovery/STATE.md`
3. Re-run validate-spec.py: `validate-spec.py`

### Duplicate IDs

**Symptoms:**
- `WARN: Decision IDs skip from D23 to D25`
- Duplicate entity warnings from validate-spec.py

**Solution:**
1. Run validation: `validate-spec.py`
2. Fix duplicates manually in archive/ files
3. Re-run validation to confirm

### Multiple Stories In Progress

**Symptoms:**
- `ERROR: Multiple stories marked as 'In Progress' (N)`

**Solution:**
```bash
# Find all in-progress stories
grep "🔄 In Progress" discovery/STATE.md

# Move all but one to queued
update-story-status.py --story-number 2 --status queued
update-story-status.py --story-number 3 --status queued

# Leave only one in progress
update-story-status.py --story-number 1 --status in_progress
```

---

## Quick Reference Cards

### When to use JSON stdin

✅ **Use JSON when:**
- Content has newlines or multiple paragraphs
- Content has special characters (`|`, `"`, `\`, etc.)
- You're automating with structured data
- You need clear, validated input

❌ **Use args/pipe when:**
- Simple, single-line content
- Quick manual entries
- No special characters

**Scripts with JSON support:**
- `log-decision.py` (RECOMMENDED for complex decisions)
- `log-iteration.py` (RECOMMENDED for multiline activities)
- `log-research.py` (RECOMMENDED for multiline findings)

---

### ID Format Quick Reference

**Remember:** All formats auto-normalize! Just use what's natural.

```bash
# These are all equivalent:
--questions "Q1, Q2, Q3"
--questions "q1, q2, q3"
--questions "Q-01, Q-02, Q-03"
--questions "Q01, Q02, Q03"

# Ranges work too:
--questions "Q1-Q5"          # Q1, Q2, Q3, Q4, Q5
--decisions "D10-D15"        # D10, D11, D12, D13, D14, D15
```

---

### Validation Quick Checks

```bash
# Before referencing entities, verify they exist:

# Stories
grep "^\| [0-9]" discovery/STATE.md

# Questions
grep "^\*\*Q[0-9]" discovery/OPEN_QUESTIONS.md

# Decisions
grep "^## D[0-9]" discovery/archive/DECISIONS.md

# Research
grep "^## R[0-9]" discovery/archive/RESEARCH.md

# Run full validation
validate-spec.py
```

---

## Getting More Help

1. **Check script help**: All scripts support `--help`
   ```bash
   log-decision.py --help
   ```

2. **Check tier references**: See `references/scripts-tier-*.md` for detailed documentation

3. **Check schemas**: See `schemas/README.md` for JSON input documentation

4. **Run validation**: Use `validate-spec.py` to catch issues early

5. **Check git history**: Scripts create atomic commits - use git to track changes
   ```bash
   git log --oneline -- discovery/
   git diff HEAD~1 -- discovery/STATE.md
   ```

---

## Common Success Patterns

### Pattern: Full Story Development Cycle

```bash
# 1. Start story
update-story-status.py --story-number 3 --status in_progress

# 2. Log questions as you discover them
add-question.py --question "How should we handle timeouts?" --category blocking --story 3

# 3. Research answers (use JSON for complex content)
cat <<'EOF' | log-research.py --from-json
{
  "topic": "Timeout Handling Patterns",
  "purpose": "Answer Q15 about timeout strategy",
  "findings": "Industry standard is 30 seconds with exponential backoff",
  "stories": "Story 3",
  "questions": "Q15"
}
EOF

# 4. Make decisions (use JSON for complex rationale)
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Use 30-second timeout with exponential backoff",
  "context": "Need timeout strategy for API calls",
  "decision": "30-second timeout, max 3 retries with exponential backoff",
  "rationale": "Industry standard, balances responsiveness with reliability",
  "stories": "Story 3",
  "questions": "Q15"
}
EOF

# 5. Resolve answered questions
resolve-question.py --question Q15 --note "Resolved by D23"

# 6. Add requirements
add-functional-requirement.py \
  --requirement "System MUST timeout API calls after 30 seconds" \
  --stories "Story 3" \
  --confidence "✅ Confirmed"

# 7. Graduate story
graduate-story.py --story-number 3

# 8. Log iteration summary (use JSON for multiline content)
cat <<'EOF' | log-iteration.py --from-json
{
  "date_range": "2026-01-19",
  "phase": "Story 3 Development",
  "goals": "Complete Story 3; Address timeout handling",
  "questions_added": "Q15",
  "decisions_made": "D23",
  "research_conducted": "R8",
  "outcomes": "Story 3 graduated with timeout handling strategy"
}
EOF
```

---

**Last Updated:** 2026-01-20
**Version:** 2.0 (with JSON stdin and ID normalization support)
