# Tier 2: High-Value Automation Scripts

Advanced workflow automation for story management and validation. Read this reference when graduating stories, managing story lifecycle, or performing research operations.

## Overview

**When to use these scripts:**
- Graduating stories from STATE.md to SPEC.md
- Changing story status
- Resolving questions
- Searching research log

**Scripts in this tier:**
1. graduate-story.py - Move story from STATE.md to SPEC.md
2. update-story-status.py - Change story status
3. resolve-question.py - Remove resolved questions
4. find-research.py - Search research log

---

## graduate-story.py

Graduate story from "In Progress" in STATE.md to graduated SPEC.md. This is the most complex script, performing validation, formatting, and updating both files atomically.

**Usage:**
```bash
graduate-story.py --story-number NUMBER [--dry-run]
```

**Pre-graduation Validation:**
- Story is marked as "🔄 In Progress" in STATE.md
- Story details exist in "In-Progress Story Detail" section
- At least one acceptance scenario present
- Priority set (P1/P2/P3)

**What it does:**
1. Extracts story from STATE.md "In-Progress Story Detail"
2. Validates story completeness
3. Formats story for SPEC.md with collapsible sections
4. Inserts into SPEC.md "User Scenarios & Testing"
5. Updates story status to "✅ In SPEC" in STATE.md
6. Sets confidence to 100%
7. Updates "Last Updated" date in SPEC.md
8. Creates backups before modifications

**Examples:**
```bash
# Graduate story 3
graduate-story.py --story-number 3

# Preview changes without applying
graduate-story.py --story-number 3 --dry-run
```

**Output:**
```
✓ Graduated Story 3: Service Dependency Visualization
  Priority: P1
  Scenarios: 3
  Updated SPEC.md and STATE.md
```

**Dry-run Output:**
```
DRY RUN - Would add the following to SPEC.md:

### User Story 3 - Service Dependency Visualization (Priority: P1)

**Revision**: v1.0

**Acceptance Scenarios**:
...

Would update Story 3 status to '✅ In SPEC' in STATE.md
```

---

## update-story-status.py

Update story status in STATE.md Story Status Overview table.

**Usage:**
```bash
update-story-status.py --story-number NUMBER --status STATUS
```

**Status Values:**
- `queued` → ⏳ Queued
- `in_progress` → 🔄 In Progress
- `in_spec` → ✅ In SPEC
- `new` → 🆕 New

**Validation:**
- When setting to `in_progress`, verifies no other story is already in progress
- Prevents multiple stories from being "In Progress" simultaneously

**Examples:**
```bash
# Mark story 3 as in progress
update-story-status.py --story-number 3 --status in_progress

# Move story back to queued
update-story-status.py --story-number 5 --status queued
```

**Output:**
```
✓ Updated Story 3 status to: 🔄 In Progress
```

**Error Output:**
```
ERROR: Story 2 is already 'In Progress'. Only one story can be in progress at a time. Set story 2 to 'queued' first.
```

---

## resolve-question.py

Remove resolved question from OPEN_QUESTIONS.md.

**Usage:**
```bash
resolve-question.py --question Q# [--note "Resolution note"]
```

**What it does:**
- Removes question entry and continuation lines
- Optionally adds resolution comment to file
- Maintains file formatting

**Note:** Questions can still be referenced after resolution (they appear in DECISIONS.md and RESEARCH.md).

**Examples:**
```bash
# Resolve question
resolve-question.py --question Q23

# Resolve with note
resolve-question.py --question Q23 --note "Resolved by D15"
```

**Output:**
```
✓ Resolved Q23
  Note: Resolved by D15
```

---

## find-research.py

Find and filter research from RESEARCH.md. Similar to find-decisions.py but for research entries.

**Usage:**
```bash
find-research.py [OPTIONS]
```

**Options:**
- `--id R#[,R#...]` - Filter by research ID(s)
- `--story NUMBER` - Filter by story number
- `--question Q#[,Q#...]` - Filter by question IDs
- `--keyword TEXT` - Search in topic, purpose, or findings
- `--format FORMAT` - Output format: `table` (default), `summary`, `json`
- `--discovery-path PATH` - Explicit discovery/ path

**Examples:**
```bash
# Find all research informing Story 1
find-research.py --story 1

# Find research on specific topic
find-research.py --keyword "CI/CD"

# Get research as JSON
find-research.py --id R5,R8 --format json
```

**Output:**
```
| ID | Topic                  | Date       | Stories |
|----|------------------------|------------|---------|
| R5 | CI/CD Integration      | 2026-01-18 | Story 2 |
| R8 | Industry Auth Patterns | 2026-01-18 | Story 1 |
```

---

## Workflow Example: Story Development to Graduation

Complete workflow for developing and graduating a story:

```bash
# 1. Set story to in progress
update-story-status.py --story-number 3 --status in_progress

# 2. Add blocking questions as you work
add-question.py --question "How to handle timeouts?" --category blocking --story 3
add-question.py --question "What error codes?" --category clarifying --story 3

# 3. Log decisions as they're made
log-decision.py \
  --title "Use 30-second timeout" \
  --context "Need timeout for API calls" \
  --decision "30 seconds with retry" \
  --stories "Story 3" \
  --questions "Q23"

# 4. Resolve blocking questions
resolve-question.py --question Q23 --note "Resolved by D5"

# 5. Preview graduation
graduate-story.py --story-number 3 --dry-run

# 6. Graduate when ready
graduate-story.py --story-number 3

# 7. Validate integrity
validate-spec.py
```

---

## Integration with Tier 1 Scripts

Tier 2 scripts build on Tier 1 foundations:

**Story Lifecycle:**
```bash
# Create story (manual STATE.md edit)
# ↓
update-story-status.py --story-number 3 --status in_progress
# ↓
add-question.py --question "..." --category blocking --story 3
log-decision.py --title "..." --stories "Story 3"
# ↓
resolve-question.py --question Q23
# ↓
graduate-story.py --story-number 3
# ↓
validate-spec.py
```

**Finding Context:**
```bash
# Find which decisions affected a graduated story
find-decisions.py --story 3

# Find research that informed it
find-research.py --story 3

# Combine to get full context
echo "Decisions:"
find-decisions.py --story 3 --format summary
echo ""
echo "Research:"
find-research.py --story 3 --format summary
```

---

## Error Scenarios and Recovery

**Multiple Stories In Progress:**
```bash
# Error
update-story-status.py --story-number 3 --status in_progress
# ERROR: Story 2 is already 'In Progress'...

# Fix: Move previous story back to queued
update-story-status.py --story-number 2 --status queued
update-story-status.py --story-number 3 --status in_progress
```

**Story Not Ready for Graduation:**
```bash
# Error
graduate-story.py --story-number 3
# ERROR: Story 3 is not marked as 'In Progress' in STATE.md

# Fix: Set correct status first
update-story-status.py --story-number 3 --status in_progress
graduate-story.py --story-number 3
```

**Invalid References After Graduation:**
```bash
# Graduate story
graduate-story.py --story-number 3

# Validate shows broken references
validate-spec.py
# ERROR: D99 referenced but not found

# Fix: Log the missing decision or update references
```
