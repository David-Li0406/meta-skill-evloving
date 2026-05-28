# Tier 1: Essential Scripts

Core scripts for initializing and managing discovery workflow. Read this reference when starting a new spec or performing basic discovery operations.

## Overview

**When to use these scripts:**
- Initializing a new specification
- Adding questions during problem exploration
- Logging decisions as they're made
- Finding past decisions
- Getting next ID for any entity type
- Validating spec integrity

**Scripts in this tier:**
1. init-spec.sh - Initialize discovery/ directory
2. next-id.py - Get next sequential ID
3. add-question.py - Add questions to OPEN_QUESTIONS.md
4. find-decisions.py - Search decision log
5. log-decision.py - Log decisions
6. validate-spec.py - Validate cross-references and structure

---

## init-spec.sh

Initialize discovery/ directory structure with all templates at the project root.

**Usage:**
```bash
init-spec.sh <feature-name> --base-path <path>
```

**Example:**
```bash
./scripts/init-spec.sh payment-flow-redesign --base-path "${CLAUDE_WORKING_DIRECTORY}"
```

**Arguments:**
- `<feature-name>` - Name of the feature (required, used for placeholder replacement)
- `--base-path <path>` - Base directory where discovery/ will be created (optional, defaults to current directory)

**What it creates:**
- `<base-path>/discovery/SPEC.md` - Progressive deliverable
- `<base-path>/discovery/STATE.md` - Working memory
- `<base-path>/discovery/OPEN_QUESTIONS.md` - Current questions
- `<base-path>/discovery/archive/DECISIONS.md` - Decision log
- `<base-path>/discovery/archive/RESEARCH.md` - Research log
- `<base-path>/discovery/archive/ITERATIONS.md` - Iteration summaries
- `<base-path>/discovery/archive/REVISIONS.md` - Story revision history

**Placeholders replaced:**
- `{FEATURE_NAME}` → provided feature name
- `{DATE}` → current date (YYYY-MM-DD)
- `{TIMESTAMP}` → current UTC timestamp
- `{AUTHOR}` → from `git config user.name` or `$USER`

**Output:**
```
✓ Created discovery/ structure for: payment-flow-redesign

Files created:
  discovery/SPEC.md
  discovery/STATE.md
  discovery/OPEN_QUESTIONS.md
  discovery/archive/DECISIONS.md
  discovery/archive/RESEARCH.md
  discovery/archive/ITERATIONS.md
  discovery/archive/REVISIONS.md

Next steps:
  1. Review discovery/STATE.md and begin problem exploration
  2. Add questions with: scripts/add-question.py --question '...' --category blocking
  3. Log decisions and research as you progress
```

---

## next-id.py

Get next sequential ID for any entity type. Useful for automation or previewing next ID.

**Usage:**
```bash
next-id.py <entity_type> [--discovery-path PATH]
```

**Entity Types:**
- `decision` → D#
- `research` → R#
- `question` → Q#
- `functional_requirement` → FR-###
- `edge_case` → EC-##
- `success_criteria` → SC-###
- `revision` → REV-###
- `story` → #

**Examples:**
```bash
# From within discovery/
next-id.py question          # → Q1

# From parent directory
next-id.py decision --discovery-path discovery/    # → D1

# Use in scripts
NEXT_Q=$(next-id.py question)
echo "Next question will be: $NEXT_Q"
```

**Output:**
```
Q23
```

---

## add-question.py

Add question to OPEN_QUESTIONS.md with automatic ID generation and category emoji.

**Usage:**
```bash
add-question.py --question TEXT --category CATEGORY [OPTIONS]
add-question.py --from-stdin
```

**Categories:**
- `blocking` 🔴 - Must answer to proceed
- `clarifying` 🟡 - Helpful but not blocking
- `research` 🔵 - Requires investigation
- `watching` 🟠 - May affect graduated stories

**Options:**
- `--question TEXT` - Question text (required unless --from-stdin)
- `--category CATEGORY` - Question category (required unless --from-stdin)
- `--context TEXT` - Context explaining why needed
- `--story NUMBER` - Story number this relates to
- `--blocking TEXT` - What this question is blocking
- `--from-stdin` - Read pipe-separated input
- `--discovery-path PATH` - Explicit discovery/ path

**Examples:**
```bash
# Simple question
add-question.py \
  --question "How should we handle API rate limiting?" \
  --category blocking \
  --story 3

# With full context
add-question.py \
  --question "What export formats do users need?" \
  --category clarifying \
  --context "Story 5 includes export feature" \
  --story 5

# Pipe-separated for automation
# Format: question|category|context|story|blocking
echo "How to handle errors?|blocking|Needed for Story 3|3|Can't write scenarios" | \
  add-question.py --from-stdin
```

**Output:**
```
✓ Added Q23 to blocking category
  Question: How should we handle API rate limiting?
  Story: Story 3
```

---

## find-decisions.py

Search and filter decisions from DECISIONS.md with multiple output formats.

**Usage:**
```bash
find-decisions.py [OPTIONS]
```

**Options:**
- `--id ID[,ID...]` - Filter by decision ID(s)
- `--story NUMBER` - Filter by story number
- `--question Q#[,Q#...]` - Filter by question IDs
- `--keyword TEXT` - Search in title, context, rationale
- `--format FORMAT` - Output format: `table` (default), `summary`, `json`
- `--discovery-path PATH` - Explicit discovery/ path

**Examples:**
```bash
# Find all decisions affecting Story 1
find-decisions.py --story 1

# Find decisions resolving specific questions
find-decisions.py --question Q12,Q15,Q23

# Search by keyword
find-decisions.py --keyword "notification"

# Get specific decisions as JSON
find-decisions.py --id D5,D8,D12 --format json

# Summary format (ID and title only)
find-decisions.py --story 2 --format summary
```

**Output Formats:**

**Table** (default):
```
| ID  | Title                              | Date       | Stories        |
|-----|-----------------------------------|------------|----------------|
| D15 | Use JWT for authentication        | 2026-01-18 | Story 1, 3     |
| D23 | 30-second polling for updates     | 2026-01-18 | Story 2        |
```

**Summary**:
```
D15: Use JWT for authentication
D23: 30-second polling for updates
```

**JSON**: Full decision objects with all fields.

---

## log-decision.py

Log decision to DECISIONS.md using template with automatic ID generation.

**Usage:**
```bash
log-decision.py --title TITLE --context CONTEXT [OPTIONS]
log-decision.py --from-stdin
```

**Options:**
- `--title TEXT` - Decision title (required)
- `--context TEXT` - Why decision was needed
- `--question TEXT` - Question being answered
- `--options TEXT` - Options considered
- `--decision TEXT` - Chosen decision
- `--rationale TEXT` - Why this was chosen
- `--implications TEXT` - Impacts and consequences
- `--stories TEXT` - Stories affected (comma-separated)
- `--questions TEXT` - Related questions (comma-separated)
- `--from-stdin` - Read pipe-separated input
- `--discovery-path PATH` - Explicit discovery/ path

**Examples:**
```bash
# Full decision entry
log-decision.py \
  --title "Use bidirectional dependency tracking" \
  --context "Both Feature Developers and Service Owners need visibility" \
  --question "Should we track outbound only or bidirectional?" \
  --options "1. Outbound only; 2. Bidirectional; 3. Separate views" \
  --decision "Use bidirectional tracking" \
  --rationale "Serves both personas with single data model" \
  --implications "Need bidirectional queries, affects FR-001 and FR-003" \
  --stories "Story 1, Story 2" \
  --questions "Q1, Q3, Q7"

# Minimal decision
log-decision.py \
  --title "Use REST API" \
  --context "Need API protocol" \
  --decision "REST with JSON"

# Pipe-separated for automation
# Format: title|context|options|decision|rationale|implications|stories|questions
echo "Use REST|Need API|REST vs GraphQL|REST|Simpler|Need API docs|Story 1|Q5" | \
  log-decision.py --from-stdin
```

**Output:**
```
✓ Logged D15: Use bidirectional dependency tracking
  Stories: Story 1, Story 2
  Questions: Q1, Q3, Q7
```

---

## validate-spec.py

Validate spec cross-references, IDs, and structure. Run this regularly to catch issues early.

**Usage:**
```bash
validate-spec.py [--discovery-path PATH]
```

**Validations Performed:**

1. **File Structure** - Required sections present in SPEC.md, STATE.md, OPEN_QUESTIONS.md
2. **Cross-References** - All D#, R#, Q#, Story #, FR-###, EC-##, SC-### references are valid
3. **ID Sequences** - No duplicate IDs, warn on gaps
4. **Story Status** - At most one story is "In Progress"

**Examples:**
```bash
# Validate from within discovery/
validate-spec.py

# Validate with explicit path
validate-spec.py --discovery-path ../discovery
```

**Output:**
```
Validating spec in: /path/to/discovery

Checking file structure...
Checking cross-references...

ERRORS (2):
  ERROR [SPEC.md]: D99 referenced but not found in archive/DECISIONS.md
  ERROR [STATE.md]: Multiple stories marked as 'In Progress' (2). Only one story should be in progress at a time.

WARNINGS (1):
  WARN [archive/DECISIONS.md]: Decision IDs skip from D23 to D25

✗ Validation failed with 2 error(s) and 1 warning(s)
```

**Exit Codes:**
- `0` - All validations passed
- `1` - Errors found
- `2` - Warnings only (no errors)

---

## Common Patterns

### Automation with Pipes

Scripts support pipe-separated input for batch operations:

```bash
# Batch add questions from file
while IFS='|' read -r question category context story; do
  echo "$question|$category|$context|$story" | add-question.py --from-stdin
done < questions.txt

# Log decisions from CSV
tail -n +2 decisions.csv | while IFS=',' read -r title context decision; do
  log-decision.py --title "$title" --context "$context" --decision "$decision"
done
```

### Script Chaining

```bash
# Get next ID and use it
NEXT_Q=$(next-id.py question)
echo "Adding question $NEXT_Q..."
add-question.py --question "..." --category blocking

# Find and process decisions
find-decisions.py --story 1 --format json | jq -r '.[].id' | while read id; do
  echo "Processing $id..."
done
```

### Directory Discovery

All scripts support three modes of finding `discovery/`:

1. **Explicit path**: `--discovery-path /path/to/discovery/`
2. **Current directory**: Run from within `discovery/`
3. **Auto-locate**: Searches parent directories

```bash
# From project root
scripts/next-id.py decision --discovery-path discovery/

# From within discovery/
cd discovery
../scripts/next-id.py decision

# From anywhere (auto-locate)
cd some/deep/subdirectory
../../scripts/next-id.py decision  # Finds discovery/ in parent
```

---

## Error Handling

All scripts follow consistent error handling:

**Exit Codes:**
- `0` - Success
- `1` - Error (validation failed, file not found, etc.)

**Error Output:**
```bash
# Errors go to stderr
./add-question.py --question "Test" 2> errors.log

# Check exit code
if ./next-id.py decision; then
  echo "Success"
else
  echo "Failed with code $?"
fi
```
