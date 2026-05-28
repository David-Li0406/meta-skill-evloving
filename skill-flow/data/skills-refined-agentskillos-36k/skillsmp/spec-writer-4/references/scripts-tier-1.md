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

Initialize discovery/ directory structure with all templates.

**Usage:**
```bash
init-spec.sh <feature-name> [--base-path <path>]
```

**Options:**
- `<feature-name>` - Name of the feature (required)
- `--base-path <path>` - Directory where discovery/ should be created (optional, defaults to current directory)

**Examples:**
```bash
# Create in current directory
./scripts/init-spec.sh payment-flow-redesign

# Create in specific project directory (RECOMMENDED when running from skill)
./scripts/init-spec.sh payment-flow-redesign --base-path /path/to/project

# Create in project root when skill is installed in .claude/skills/
./scripts/init-spec.sh payment-flow-redesign --base-path ../../..
```

**What it creates:**
- `discovery/SPEC.md` - Progressive deliverable
- `discovery/STATE.md` - Working memory
- `discovery/OPEN_QUESTIONS.md` - Current questions
- `discovery/archive/DECISIONS.md` - Decision log
- `discovery/archive/RESEARCH.md` - Research log
- `discovery/archive/ITERATIONS.md` - Iteration summaries
- `discovery/archive/REVISIONS.md` - Story revision history

**Placeholders replaced:**
- `{FEATURE_NAME}` → provided feature name
- `{DATE}` → current date (YYYY-MM-DD)
- `{TIMESTAMP}` → current UTC timestamp
- `{AUTHOR}` → from `git config user.name` or `$USER`

**Output:**
```
Creating discovery/ structure for: payment-flow-redesign
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
  1. cd discovery/
  2. Review STATE.md and begin problem exploration
  3. Add questions with: ../scripts/add-question.py --question '...' --category blocking
  4. Log decisions and research as you progress

Happy discovery! 🚀
```

**Common Usage Patterns:**

When running from within a Claude Code skill installed in `.claude/skills/spec-writer/`:
```bash
# Navigate to project root first
cd ../../../

# Or use --base-path to target project root
./.claude/skills/spec-writer/scripts/init-spec.sh my-feature --base-path .
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
- `--id ID[,ID...]` - Filter by decision ID(s) (flexible formats accepted)
- `--story NUMBER` - Filter by story number
- `--question Q#[,Q#...]` - Filter by question IDs (flexible formats accepted)
- `--keyword TEXT` - Search in title, context, rationale
- `--format FORMAT` - Output format: `table` (default), `summary`, `json`
- `--discovery-path PATH` - Explicit discovery/ path

**💡 ID Format Flexibility:**
- Decision IDs: `D1`, `D01`, `d1`, `D-01` all work (normalizes to `D1`)
- Question IDs: `Q5`, `Q05`, `q5`, `Q-05` all work (normalizes to `Q5`)
- Comma-separated lists accepted: `D1,D2,D3` or `D1, D2, D3`

**Examples:**
```bash
# Find all decisions affecting Story 1
find-decisions.py --story 1

# Find decisions resolving specific questions (flexible formats)
find-decisions.py --question Q12,Q15,Q23
find-decisions.py --question q12,q15,q23          # Same result
find-decisions.py --question Q-012,Q-015,Q-023    # Same result

# Search by keyword
find-decisions.py --keyword "notification"

# Get specific decisions as JSON (flexible ID formats)
find-decisions.py --id D5,D8,D12 --format json
find-decisions.py --id d5,d08,d12 --format json   # Same result

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

**Common Errors:**

❌ **Bad - Invalid ID format:**
```bash
find-decisions.py --id D99  # D99 doesn't exist
# Returns empty result
```

✅ **Good - Check available decisions first:**
```bash
# List all decisions to see what's available
find-decisions.py --format summary
# Then filter
find-decisions.py --id D9
```

❌ **Bad - Mixed filters that return nothing:**
```bash
find-decisions.py --story 1 --question Q99  # Q99 doesn't exist or isn't related to Story 1
# Returns empty result
```

✅ **Good - Check filters independently:**
```bash
find-decisions.py --story 1          # See decisions for Story 1
find-decisions.py --question Q99     # See if Q99 has any decisions
```

---

## log-decision.py

Log decision to DECISIONS.md using template with automatic ID generation.

**Usage:**
```bash
log-decision.py --title TITLE --context CONTEXT [OPTIONS]
log-decision.py --from-stdin                     # Pipe-separated (legacy)
log-decision.py --from-json                      # JSON from stdin (RECOMMENDED)
log-decision.py --json-file FILE                 # JSON from file (RECOMMENDED)
```

**Options:**
- `--title TEXT` - Decision title (required for non-JSON)
- `--context TEXT` - Why decision was needed
- `--question TEXT` - Question being answered
- `--options TEXT` - Options considered
- `--decision TEXT` - Chosen decision
- `--rationale TEXT` - Why this was chosen
- `--implications TEXT` - Impacts and consequences
- `--stories TEXT` - Stories affected (comma-separated)
- `--questions TEXT` - Related questions (comma-separated, flexible formats accepted)
- `--from-stdin` - Read pipe-separated input (legacy)
- `--from-json` - Read JSON from stdin (RECOMMENDED - handles multiline, special chars)
- `--json-file FILE` - Read JSON from file (RECOMMENDED)
- `--discovery-path PATH` - Explicit discovery/ path

**💡 ID Format Flexibility:**
Question IDs accept multiple formats: `Q1`, `Q01`, `q1`, `Q-01` all normalize to `Q1`

**Examples:**
```bash
# JSON input (RECOMMENDED for complex content)
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Use bidirectional dependency tracking",
  "context": "Both Feature Developers and Service Owners need visibility",
  "question": "Should we track outbound only or bidirectional?",
  "options": "1. Outbound only\n2. Bidirectional\n3. Separate views",
  "decision": "Use bidirectional tracking",
  "rationale": "Serves both personas with single data model",
  "implications": "Need bidirectional queries, affects FR-001 and FR-003",
  "stories": "Story 1, Story 2",
  "questions": "Q1, Q3, Q7"
}
EOF

# JSON from file
log-decision.py --json-file decision.json

# Full decision entry (args)
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

# Flexible question ID formats (all valid)
log-decision.py --title "..." --questions "Q1, q02, Q-3"  # Normalizes to: Q1, Q2, Q3
```

**Output:**
```
✓ Logged D15: Use bidirectional dependency tracking
  Stories: Story 1, Story 2
  Questions: Q1, Q3, Q7
⚠️  WARNING: Story 2 not found in STATE.md
    Did you mean one of: 1, 3, 4?
```

**Common Errors:**

❌ **Bad - Pipe-separated with multiline text:**
```bash
# FAILS: Newlines break pipe format
echo "Title|Context with\nnewlines|Decision" | log-decision.py --from-stdin
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

❌ **Bad - Wrong question ID format (typo):**
```bash
log-decision.py --title "..." --questions "Q99"  # Q99 doesn't exist
# ERROR: Question Q99 not found
#        Did you mean: Q9, Q8, Q7?
```

✅ **Good - Verify question exists first:**
```bash
find-decisions.py --question Q9  # Verify Q9 exists
log-decision.py --title "..." --questions "Q9"
```

❌ **Bad - Story reference typo:**
```bash
log-decision.py --title "..." --stories "Story 99"
# WARNING: Story 99 not found in STATE.md
#          Did you mean one of: 1, 2, 3?
```

✅ **Good - Check STATE.md for valid stories:**
```bash
# Check STATE.md Story Status Overview table first
log-decision.py --title "..." --stories "Story 1, Story 2"
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
