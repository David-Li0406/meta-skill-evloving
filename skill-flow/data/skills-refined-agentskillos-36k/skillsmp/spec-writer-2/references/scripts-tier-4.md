# Tier 4: Specialized Table Scripts

Specialized scripts for managing SPEC.md tables. Read this reference when adding or updating edge cases, functional requirements, or success criteria.

## Overview

**When to use these scripts:**
- Adding edge cases discovered during story development
- Extracting functional requirements from acceptance scenarios
- Defining success criteria for stories

**Scripts in this tier:**
1. add-edge-case.py - Add edge cases to Edge Cases table
2. add-functional-requirement.py - Add functional requirements to Requirements table
3. add-success-criteria.py - Add success criteria to Success Criteria table

**Common Pattern:**
All Tier 4 scripts follow the same pattern:
- Add new entries with auto-generated IDs
- Update existing entries by providing the ID
- Support pipe-separated input for automation
- Smart directory discovery
- Atomic file operations with backup

---

## add-edge-case.py

Add or update edge case in SPEC.md Edge Cases table.

**Usage:**
```bash
add-edge-case.py --scenario TEXT --handling TEXT --stories TEXT
add-edge-case.py --from-stdin
```

**Options:**
- `--id EC-##` - EC ID to update (omit for new entry)
- `--scenario TEXT` - Edge case scenario description
- `--handling TEXT` - How to handle this edge case
- `--stories TEXT` - Stories affected (comma-separated)
- `--from-stdin` - Read pipe-separated input
- `--discovery-path PATH` - Explicit discovery/ path

**Pipe-separated format:**
```
scenario|handling|stories              # New entry
EC-##|scenario|handling|stories        # Update existing
```

**Examples:**
```bash
# Add new edge case
add-edge-case.py \
  --scenario "Feature has zero dependencies" \
  --handling "Show clear message 'No dependencies configured'" \
  --stories "Story 1"

# Pipe-separated
echo "Zero dependencies|Show message|Story 1" | add-edge-case.py --from-stdin

# Update existing
echo "EC-01|Updated scenario|Updated handling|Story 1, Story 2" | \
  add-edge-case.py --from-stdin
```

**Output:**
```
✓ Added EC-01: Feature has zero dependencies
  Stories: Story 1
```

**Table Format:**
```markdown
## Edge Cases

| ID | Scenario | Handling | Stories Affected |
|----|----------|----------|------------------|
| EC-01 | Feature has zero dependencies | Show clear message | Story 1 |
| EC-02 | API timeout after 30 seconds | Retry with backoff | Story 2, 3 |
```

---

## add-functional-requirement.py

Add or update functional requirement in SPEC.md Requirements table.

**Usage:**
```bash
add-functional-requirement.py --requirement TEXT --stories TEXT [--confidence LEVEL]
add-functional-requirement.py --from-stdin
```

**Options:**
- `--id FR-###` - FR ID to update (omit for new entry)
- `--requirement TEXT` - Requirement text (should start with "System MUST/SHOULD")
- `--stories TEXT` - Stories this applies to (comma-separated)
- `--confidence LEVEL` - Confidence level: `✅ Confirmed` or `🔄 Draft` (default: Draft)
- `--from-stdin` - Read pipe-separated input
- `--discovery-path PATH` - Explicit discovery/ path

**Pipe-separated format:**
```
requirement|stories|confidence          # New entry
FR-###|requirement|stories|confidence   # Update existing
```

**Examples:**
```bash
# Add confirmed requirement
add-functional-requirement.py \
  --requirement "System MUST support up to 50 service dependencies" \
  --stories "Story 1" \
  --confidence "✅ Confirmed"

# Add draft requirement
add-functional-requirement.py \
  --requirement "System SHOULD cache test results for 15 minutes" \
  --stories "Story 2"

# Pipe-separated
echo "System MUST handle 429 responses|Story 2|✅ Confirmed" | \
  add-functional-requirement.py --from-stdin

# Update existing
echo "FR-005|Updated requirement text|Story 2|🔄 Draft" | \
  add-functional-requirement.py --from-stdin
```

**Output:**
```
✓ Added FR-001: System MUST support up to 50 service dependencies
  Stories: Story 1
  Confidence: ✅ Confirmed
```

**Table Format:**
```markdown
### Functional Requirements

| ID | Requirement | Stories | Confidence |
|----|-------------|---------|------------|
| FR-001 | System MUST support up to 50 dependencies | Story 1 | ✅ Confirmed |
| FR-002 | System MUST update within 30 seconds | Story 1, 2 | ✅ Confirmed |
| FR-003 | System SHOULD cache for 15 minutes | Story 2 | 🔄 Draft |
```

---

## add-success-criteria.py

Add or update success criteria in SPEC.md Success Criteria table.

**Usage:**
```bash
add-success-criteria.py --criterion TEXT --measurement TEXT --stories TEXT
add-success-criteria.py --from-stdin
```

**Options:**
- `--id SC-###` - SC ID to update (omit for new entry)
- `--criterion TEXT` - Success criterion description
- `--measurement TEXT` - How to measure this criterion (must be quantified)
- `--stories TEXT` - Stories this applies to (comma-separated)
- `--from-stdin` - Read pipe-separated input
- `--discovery-path PATH` - Explicit discovery/ path

**Pipe-separated format:**
```
criterion|measurement|stories            # New entry
SC-###|criterion|measurement|stories     # Update existing
```

**Examples:**
```bash
# Add success criteria
add-success-criteria.py \
  --criterion "Reduce integration bugs" \
  --measurement "60% reduction measured over 2 months post-launch" \
  --stories "Story 1, Story 3"

# Pipe-separated
echo "Bugs decrease|60% reduction over 2 months|Story 1, Story 3" | \
  add-success-criteria.py --from-stdin

# Update existing
echo "SC-001|Updated criterion|New measurement|Story 1, Story 2" | \
  add-success-criteria.py --from-stdin
```

**Output:**
```
✓ Added SC-001: Reduce integration bugs
  Stories: Story 1, Story 3
```

**Table Format:**
```markdown
## Success Criteria

| ID | Criterion | Measurement | Stories |
|----|-----------|-------------|---------|
| SC-001 | Reduce integration bugs | 60% reduction over 2 months | Story 1, 3 |
| SC-002 | Improve discovery time | < 5 min to identify dependencies | Story 1 |
```

---

## Workflow: Extracting from Stories

Common pattern for extracting requirements, edge cases, and success criteria from acceptance scenarios:

### Step 1: Develop Story

Develop story with detailed acceptance scenarios in STATE.md:

```markdown
## In-Progress Story Detail

### Story 1: Service Dependency Visualization (Priority: P1)

**Draft Acceptance Scenarios**:
1. **Given** developer views feature, **When** checking dependencies, **Then** see up to 50 services displayed
2. **Given** feature has zero dependencies, **When** viewing, **Then** see message "No dependencies"
3. **Given** API timeout, **When** loading, **Then** see error with retry option
```

### Step 2: Extract Functional Requirements

From scenario 1:
```bash
add-functional-requirement.py \
  --requirement "System MUST support up to 50 service dependencies per feature" \
  --stories "Story 1" \
  --confidence "✅ Confirmed"
```

From scenario 3:
```bash
add-functional-requirement.py \
  --requirement "System MUST handle API timeouts gracefully with retry" \
  --stories "Story 1" \
  --confidence "✅ Confirmed"
```

### Step 3: Extract Edge Cases

From scenario 2:
```bash
add-edge-case.py \
  --scenario "Feature has zero dependencies configured" \
  --handling "Display clear message: No dependencies configured" \
  --stories "Story 1"
```

From scenario 3:
```bash
add-edge-case.py \
  --scenario "API timeout after 30 seconds" \
  --handling "Show error message with retry button" \
  --stories "Story 1"
```

### Step 4: Define Success Criteria

Based on story value proposition:
```bash
add-success-criteria.py \
  --criterion "Reduce time to identify service dependencies" \
  --measurement "< 5 minutes from feature ID to full dependency graph" \
  --stories "Story 1"

add-success-criteria.py \
  --criterion "Reduce integration bugs from missing dependencies" \
  --measurement "60% reduction in dependency-related bugs over 2 months" \
  --stories "Story 1"
```

### Step 5: Graduate Story

```bash
graduate-story.py --story-number 1
```

The graduated story in SPEC.md will now reference:
- FR-001, FR-002 (functional requirements)
- EC-01, EC-02 (edge cases)
- SC-001, SC-002 (success criteria)

---

## Batch Operations

Extract multiple requirements from a list:

```bash
# From CSV file
cat requirements.csv
# "System MUST support X,Story 1,Confirmed"
# "System SHOULD cache Y,Story 2,Draft"

tail -n +2 requirements.csv | while IFS=',' read -r req story conf; do
  add-functional-requirement.py \
    --requirement "$req" \
    --stories "$story" \
    --confidence "$conf"
done
```

Parse scenarios and extract edge cases:

```bash
# From scenarios file (pipe-separated)
cat edge-cases.txt
# Zero dependencies|Show message|Story 1
# Timeout|Retry|Story 1,Story 2
# Invalid input|Validation error|Story 3

while IFS='|' read -r scenario handling stories; do
  echo "$scenario|$handling|$stories" | add-edge-case.py --from-stdin
done < edge-cases.txt
```

---

## Validation and Updates

**After adding entries:**
```bash
# Validate all references are correct
validate-spec.py

# Check what was added
grep "FR-" discovery/SPEC.md | tail -5
grep "EC-" discovery/SPEC.md | tail -5
grep "SC-" discovery/SPEC.md | tail -5
```

**Update existing entries:**
```bash
# Correct a requirement
echo "FR-005|System MUST cache for 30 minutes (not 15)|Story 2|✅ Confirmed" | \
  add-functional-requirement.py --from-stdin

# Update edge case handling
echo "EC-03|Timeout scenario|New handling with backoff|Story 1, Story 2" | \
  add-edge-case.py --from-stdin

# Revise success criteria measurement
echo "SC-001|Reduce bugs|Updated: 70% reduction over 3 months|Story 1, Story 3" | \
  add-success-criteria.py --from-stdin
```

---

## Integration with Other Tiers

**Tier 1: Foundation**
```bash
# Get next IDs
next-id.py functional_requirement  # → FR-015
next-id.py edge_case              # → EC-06
next-id.py success_criteria       # → SC-003
```

**Tier 2: Story Management**
```bash
# Extract during story development
update-story-status.py --story-number 3 --status in_progress
# ... develop acceptance scenarios ...
add-functional-requirement.py --requirement "..." --stories "Story 3"
add-edge-case.py --scenario "..." --handling "..." --stories "Story 3"
graduate-story.py --story-number 3
```

**Tier 3: Research and Decisions**
```bash
# Research informs requirements
log-research.py --topic "Rate limiting" --findings "Industry uses 429"
log-decision.py --title "Use 429 for rate limits" --stories "Story 2"
add-functional-requirement.py --requirement "System MUST return 429" --stories "Story 2"
```

---

## Tips

**Requirement Writing:**
- Use MUST for mandatory, SHOULD for nice-to-have
- Be specific and testable
- Reference decisions that led to the requirement
- Mark Draft until confirmed by user

**Edge Case Identification:**
- Think boundary conditions (zero, max, empty, null)
- Consider failure scenarios (timeouts, errors, unavailable)
- Test "what if" questions from acceptance scenarios
- Document handling strategy clearly

**Success Criteria:**
- Must be measurable with numbers
- Include time period for measurement
- Specify how to measure (survey, metrics, logs)
- Link to story value propositions
- Be realistic and achievable
