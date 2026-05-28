# JSON Input Schemas Documentation

Comprehensive guide to using JSON input with spec-writer scripts for robust, maintainable automation.

## Table of Contents

1. [Why Use JSON Input?](#why-use-json-input)
2. [Quick Start](#quick-start)
3. [Schema Reference](#schema-reference)
   - [decision-input.json](#decision-inputjson)
   - [iteration-input.json](#iteration-inputjson)
   - [research-input.json](#research-inputjson)
4. [Usage Patterns](#usage-patterns)
5. [Migration Guide](#migration-guide)
6. [Validation and Errors](#validation-and-errors)

---

## Why Use JSON Input?

**JSON input is RECOMMENDED for:**
- ✅ Multiline content (paragraphs, lists, formatted text)
- ✅ Special characters (`|`, `"`, `\`, newlines, etc.)
- ✅ Structured data with clear validation
- ✅ Automation pipelines that generate structured data
- ✅ Complex content that's hard to escape in shell

**Pipe-separated input remains for:**
- Simple, single-line entries
- Quick manual additions
- Legacy scripts and automation

**Supported Scripts:**
- `log-decision.py` - Complex decision logging
- `log-iteration.py` - Iteration summaries with multiline activities
- `log-research.py` - Research findings with formatted content

---

## Quick Start

### Basic Usage

```bash
# Method 1: JSON from stdin (heredoc)
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Use JWT authentication",
  "context": "Need secure auth for API",
  "decision": "Implement JWT with RS256",
  "stories": "1, 3",
  "questions": "Q12, Q15"
}
EOF

# Method 2: JSON from file
log-decision.py --json-file decision.json

# Method 3: JSON piped from tool
jq -n '{title: "Test", context: "Context"}' | log-decision.py --from-json
```

### File-based Workflow

```bash
# 1. Create JSON file
cat > decision.json <<'EOF'
{
  "title": "Choose database system",
  "context": "Need to select primary database",
  "options_considered": "PostgreSQL, MySQL, MongoDB",
  "decision": "Use PostgreSQL",
  "rationale": "Best support for JSONB and full-text search",
  "stories": [1, 2],
  "questions": ["Q5", "Q8"]
}
EOF

# 2. Use the file
log-decision.py --json-file decision.json

# 3. Reuse/modify for similar entries
cp decision.json another-decision.json
# Edit another-decision.json
log-decision.py --json-file another-decision.json
```

---

## Schema Reference

### decision-input.json

**Used by:** `log-decision.py`

**Purpose:** Log decisions with full context, rationale, and cross-references.

**Required Fields:**
- `title` (string) - Short title for the decision
- `context` (string) - Why this decision is needed

**Optional Fields:**
- `decision` (string) - The decision made (can be added later)
- `options_considered` (string or array) - Options that were considered
- `rationale` (string) - Reasoning behind the decision
- `implications` (string) - Impact and consequences
- `stories` (integer, string, or array) - Related story numbers
- `questions` (string or array) - Related question IDs
- `tags` (string) - Comma-separated tags for categorization

**Field Formats:**

```json
{
  // Required
  "title": "Use JWT authentication",              // Simple string
  "context": "Need secure auth mechanism",         // Can be multiline

  // Optional - Simple strings
  "decision": "Implement JWT with RS256 signing",
  "rationale": "JWT provides stateless auth, easier to scale",
  "implications": "Must handle token refresh, key rotation complexity",
  "tags": "security, authentication",

  // Optional - String or Array
  "options_considered": "JWT, OAuth2, Session cookies",  // String
  "options_considered": ["JWT", "OAuth2", "Session"],    // OR Array

  // Optional - Story references (flexible)
  "stories": 1,                    // Single story number
  "stories": "1, 3, 5",            // OR Comma-separated string
  "stories": [1, 3, 5],            // OR Array

  // Optional - Question references (flexible)
  "questions": "Q12",              // Single ID
  "questions": "Q12, Q15, Q18",    // OR Comma-separated
  "questions": ["Q12", "Q15"]      // OR Array
}
```

**Complete Example:**

```json
{
  "title": "Use bidirectional dependency tracking",
  "context": "Both Feature Developers and Service Owners need visibility into dependencies",
  "options_considered": [
    "1. Outbound only - track what this service depends on",
    "2. Inbound only - track what depends on this service",
    "3. Bidirectional - track both directions",
    "4. Separate views - different UIs for each persona"
  ],
  "decision": "Use bidirectional tracking with role-based filtering",
  "rationale": "Serves both personas with single data model. Role-based filtering keeps UX focused.",
  "implications": "Need bidirectional queries, affects FR-001 and FR-003. May impact query performance at scale.",
  "stories": [1, 2],
  "questions": ["Q1", "Q3", "Q7"],
  "tags": "architecture, data-model"
}
```

**Usage:**

```bash
# From file
log-decision.py --json-file decision.json

# From stdin
cat decision.json | log-decision.py --from-json

# Inline heredoc
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Decision title",
  "context": "Why this decision is needed"
}
EOF
```

---

### iteration-input.json

**Used by:** `log-iteration.py`

**Purpose:** Log iteration summaries with multiline activities, outcomes, and cross-references.

**Required Fields:**
- `date_range` (string) - Date or date range (e.g., "2026-01-19" or "Jan 19-20")
- `phase` (string) - Discovery phase name
- `goals` (string) - Iteration goals (semicolon-separated)

**Optional Fields:**
- `activities` (string) - Activities performed (can be multiline)
- `outcomes` (string) - Key outcomes (can be multiline)
- `questions_added` (string) - Questions added (e.g., "Q1-Q5" or "Q9, Q12")
- `decisions_made` (string) - Decisions made (e.g., "D1, D2")
- `research_conducted` (string) - Research conducted (e.g., "R1, R3")
- `next_steps` (string) - Next steps (can be multiline)

**Field Formats:**

```json
{
  // Required
  "date_range": "2026-01-19",                    // Single date
  "date_range": "Jan 19-20",                     // OR Date range
  "phase": "Problem Exploration",                // Phase name
  "goals": "Goal 1; Goal 2; Goal 3",            // Semicolon-separated

  // Optional - Can be multiline
  "activities": "Activity 1\nActivity 2\nActivity 3",
  "outcomes": "Outcome 1\nOutcome 2",
  "next_steps": "Next step 1\nNext step 2",

  // Optional - ID lists (flexible, support ranges)
  "questions_added": "Q1-Q5",                    // Range
  "questions_added": "Q9, Q12, Q15",             // OR Comma-separated
  "decisions_made": "D1, D2, D5",                // Comma-separated
  "research_conducted": "R1-R3"                  // Range
}
```

**Complete Example:**

```json
{
  "date_range": "2026-01-19",
  "phase": "Problem Exploration",
  "goals": "Understand the problem space; Identify key personas; Define constraints",
  "activities": "Discovery research on industry patterns\nUser interviews with 5 engineers\nStakeholder meetings with product and architecture teams\nCompetitor analysis of 3 tools",
  "outcomes": "Problem statement drafted and validated\n3 personas identified (Feature Dev, Service Owner, Platform Team)\n2 hard constraints documented (must work with existing CI/CD)\n5 stories crystallized from research",
  "questions_added": "Q1-Q5",
  "decisions_made": "D1, D2",
  "research_conducted": "R1",
  "next_steps": "Transition to Story Crystallization phase\nBegin Story 1 development\nSchedule architecture review"
}
```

**Usage:**

```bash
# From file
log-iteration.py --json-file iteration.json

# From stdin with multiline content
cat <<'EOF' | log-iteration.py --from-json
{
  "date_range": "2026-01-19",
  "phase": "Problem Exploration",
  "goals": "Understand problem; Identify personas",
  "activities": "Discovery research\nUser interviews\nStakeholder meetings",
  "outcomes": "Problem statement drafted\n3 personas identified",
  "questions_added": "Q1-Q5",
  "decisions_made": "D1, D2"
}
EOF
```

---

### research-input.json

**Used by:** `log-research.py`

**Purpose:** Log research findings with multiline content and cross-references.

**Required Fields:**
- `topic` (string) - Research topic
- `purpose` (string) - Why research was conducted

**Optional Fields:**
- `approach` (string) - How research was conducted (can be multiline)
- `findings` (string) - Key findings (can be multiline)
- `patterns` (string) - Industry patterns identified (can be multiline)
- `examples` (string) - Relevant examples from products (can be multiline)
- `implications` (string) - Implications for stories (can be multiline)
- `stories` (string) - Stories informed (comma-separated)
- `questions` (string) - Related questions (comma-separated)

**Field Formats:**

```json
{
  // Required
  "topic": "CI/CD Integration Patterns",                 // Topic string
  "purpose": "Understand industry standards for...",      // Purpose string

  // Optional - Can all be multiline
  "approach": "Method 1\nMethod 2\nMethod 3",
  "findings": "Finding 1\nFinding 2",
  "patterns": "Pattern 1\nPattern 2",
  "examples": "Example 1\nExample 2",
  "implications": "Implication 1\nImplication 2",

  // Optional - References
  "stories": "Story 2, Story 3",                         // Comma-separated
  "questions": "Q15, Q18"                                // Comma-separated
}
```

**Complete Example:**

```json
{
  "topic": "CI/CD Integration Patterns",
  "purpose": "Understand industry standards for polling vs webhooks for CI/CD status updates",
  "approach": "Web search and documentation review\nGitHub API documentation analysis\nSlack and Jira integration research\nInterviews with 3 platform engineers",
  "findings": "Most tools use 30-60 second polling for non-critical updates\nWebhooks preferred for time-sensitive events\nHybrid approach common: polling with webhook override\nRate limiting important consideration",
  "patterns": "Slack: Webhooks for all events, fallback polling for missed events\nGitHub: Polling default, webhooks optional (requires public endpoint)\nJira: Polling with configurable intervals (15s-5min)\nCircleCI: Pure webhooks, no polling option",
  "examples": "GitHub status checks: 30s polling, webhook override available\nSlack notifications: Immediate webhook, 1min retry on failure\nJira sync: 1min polling default, 15s for premium",
  "implications": "30-second polling is acceptable for MVP\nCan add webhook support in Phase 2\nNeed rate limiting strategy (FR-005)\nMust handle missed updates gracefully (EC-03)",
  "stories": "Story 2, Story 3",
  "questions": "Q15, Q18"
}
```

**Usage:**

```bash
# From file
log-research.py --json-file research.json

# From stdin with multiline findings
cat <<'EOF' | log-research.py --from-json
{
  "topic": "Authentication Best Practices",
  "purpose": "Choose auth method for API",
  "findings": "JWT most common\nOAuth2 for third-party\nSession cookies for web apps",
  "implications": "Recommend JWT for our use case",
  "stories": "Story 1",
  "questions": "Q5"
}
EOF
```

---

## Usage Patterns

### Pattern 1: Template Files

Create reusable templates for common operations:

**templates/decision-template.json:**
```json
{
  "title": "",
  "context": "",
  "options_considered": [],
  "decision": "",
  "rationale": "",
  "implications": "",
  "stories": [],
  "questions": []
}
```

**Usage:**
```bash
cp templates/decision-template.json my-decision.json
# Edit my-decision.json
log-decision.py --json-file my-decision.json
```

---

### Pattern 2: Automated Generation

Generate JSON from tools/scripts:

```bash
# From jq
jq -n \
  --arg title "Auto-generated decision" \
  --arg context "From automation" \
  '{title: $title, context: $context}' | \
  log-decision.py --from-json

# From Python
python3 -c "
import json
data = {
    'title': 'Generated decision',
    'context': 'From Python script',
    'stories': [1, 2]
}
print(json.dumps(data))
" | log-decision.py --from-json

# From workflow file
cat workflow-output.json | jq '{
  title: .decision_title,
  context: .background,
  decision: .chosen_option
}' | log-decision.py --from-json
```

---

### Pattern 3: Batch Processing

Process multiple entries from a JSON array:

```bash
# decisions.json - array of decisions
[
  {"title": "Decision 1", "context": "Context 1"},
  {"title": "Decision 2", "context": "Context 2"},
  {"title": "Decision 3", "context": "Context 3"}
]

# Process each
jq -c '.[]' decisions.json | while read -r decision; do
  echo "$decision" | log-decision.py --from-json
done
```

---

### Pattern 4: Interactive Builder

Build JSON interactively:

```bash
#!/bin/bash
# decision-builder.sh

read -p "Title: " title
read -p "Context: " context
read -p "Decision: " decision
read -p "Stories (comma-separated): " stories

jq -n \
  --arg title "$title" \
  --arg context "$context" \
  --arg decision "$decision" \
  --arg stories "$stories" \
  '{title: $title, context: $context, decision: $decision, stories: $stories}' | \
  log-decision.py --from-json
```

---

## Migration Guide

### From Pipe-Separated to JSON

**Before (pipe-separated):**
```bash
echo "Use JWT|Need auth|JWT vs OAuth|JWT|Stateless|Token refresh|Story 1|Q5" | \
  log-decision.py --from-stdin
```

**After (JSON):**
```bash
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Use JWT",
  "context": "Need auth",
  "options_considered": "JWT vs OAuth",
  "decision": "JWT",
  "rationale": "Stateless",
  "implications": "Token refresh",
  "stories": "Story 1",
  "questions": "Q5"
}
EOF
```

**Migration Checklist:**
- ✅ Extract pipe-separated values into JSON fields
- ✅ Use arrays for lists instead of comma-separated strings (optional)
- ✅ Add newlines for multiline content
- ✅ No need to escape special characters
- ✅ Validate with `--from-json` flag

---

### Common Migration Scenarios

#### Scenario 1: Multiline Content

❌ **Bad (pipe-separated):**
```bash
# FAILS - newlines break format
echo "Title|Context with\nmultiple\nlines|Decision" | log-decision.py --from-stdin
```

✅ **Good (JSON):**
```bash
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Title",
  "context": "Context with\nmultiple\nlines",
  "decision": "Decision"
}
EOF
```

#### Scenario 2: Special Characters

❌ **Bad (pipe-separated):**
```bash
# FAILS - pipe characters break parsing
echo "Title|Context with | pipes|Decision" | log-decision.py --from-stdin
```

✅ **Good (JSON):**
```bash
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Title",
  "context": "Context with | pipes and special chars: @#$%",
  "decision": "Decision"
}
EOF
```

#### Scenario 3: Structured Lists

❌ **Bad (pipe-separated):**
```bash
echo "Title|Context|Option 1, Option 2, Option 3|Decision" | log-decision.py --from-stdin
```

✅ **Good (JSON with array):**
```bash
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Title",
  "context": "Context",
  "options_considered": [
    "Option 1: Description of first option",
    "Option 2: Description of second option",
    "Option 3: Description of third option"
  ],
  "decision": "Decision"
}
EOF
```

---

## Validation and Errors

### Schema Validation

Scripts automatically validate JSON against schemas:

```bash
# Valid JSON
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Valid",
  "context": "Has required fields"
}
EOF
# ✓ Success

# Invalid - missing required field
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Invalid"
}
EOF
# ERROR: JSON schema validation failed:
#   'context' is a required property
```

### Common Validation Errors

**Error: Missing Required Field**
```
ERROR: JSON schema validation failed:
  'context' is a required property
```
**Fix:** Add all required fields (`title` and `context` for decisions)

**Error: Invalid Field Type**
```
ERROR: JSON schema validation failed:
  'stories' should be string, integer, or array
```
**Fix:** Use correct format: `"stories": "1, 2"` or `"stories": [1, 2]`

**Error: Invalid JSON Syntax**
```
ERROR: Failed to parse JSON from stdin:
  Expecting ',' delimiter: line 5 column 3
```
**Fix:** Check JSON syntax (trailing commas, quotes, brackets)

### Debugging JSON

```bash
# Validate JSON syntax with jq
echo '{...}' | jq '.'

# Pretty-print for readability
cat decision.json | jq '.'

# Validate against schema (if you have jsonschema)
jsonschema -i decision.json schemas/decision-input.json
```

---

## Tips and Best Practices

### 1. Use Heredocs for Complex Content

✅ **Good:**
```bash
cat <<'EOF' | log-decision.py --from-json
{
  "title": "Complex decision",
  "context": "Multi-paragraph context with\n\nFormatting and special chars: @#$%"
}
EOF
```

**Note:** Use `<<'EOF'` (single quotes) to prevent shell expansion.

---

### 2. Store Reusable Templates

Create a `templates/` directory:
```
templates/
  ├── decision-template.json
  ├── iteration-template.json
  └── research-template.json
```

---

### 3. Validate Before Submitting

```bash
# Test with jq first
cat decision.json | jq '.' > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Then submit
log-decision.py --json-file decision.json
```

---

### 4. Use Arrays for Clarity

**Both valid:**
```json
{
  "stories": "1, 2, 3",           // Simple
  "stories": [1, 2, 3]            // Clear
}
```

Arrays are clearer for automation and tooling.

---

### 5. Combine with Version Control

```bash
# Store decision files
mkdir -p decisions/
cat > decisions/D001-auth-decision.json <<'EOF'
{...}
EOF

# Commit before applying
git add decisions/
git commit -m "Add D001 decision file"

# Apply
log-decision.py --json-file decisions/D001-auth-decision.json

# Commit result
git add discovery/
git commit -m "Log D001 to archive"
```

---

## Examples Repository

Complete working examples:

### Example 1: Simple Decision

**File: `examples/simple-decision.json`**
```json
{
  "title": "Use 30-second polling",
  "context": "Need update frequency for CI/CD status",
  "decision": "Poll every 30 seconds",
  "stories": "2"
}
```

```bash
log-decision.py --json-file examples/simple-decision.json
```

---

### Example 2: Complex Decision with All Fields

**File: `examples/complex-decision.json`**
```json
{
  "title": "Choose frontend framework",
  "context": "Need to select framework for new dashboard UI.\n\nRequirements:\n- Fast iteration\n- Strong TypeScript support\n- Good ecosystem",
  "options_considered": [
    "React: Most popular, huge ecosystem, steep learning curve",
    "Vue: Easier learning curve, smaller ecosystem",
    "Svelte: Best performance, smaller ecosystem, less TypeScript support"
  ],
  "decision": "Use React with TypeScript",
  "rationale": "Team already has React experience. TypeScript support is excellent. Ecosystem provides solutions for all our needs (routing, state management, testing).",
  "implications": "Steeper onboarding for new team members. Bundle size slightly larger than Svelte. Need to establish code patterns early (FR-015).",
  "stories": [3, 5, 7],
  "questions": ["Q12", "Q15", "Q18"],
  "tags": "frontend, architecture, tooling"
}
```

```bash
log-decision.py --json-file examples/complex-decision.json
```

---

### Example 3: Iteration Summary

**File: `examples/iteration-summary.json`**
```json
{
  "date_range": "Jan 19-20, 2026",
  "phase": "Problem Exploration",
  "goals": "Understand the problem space; Identify key personas; Define initial constraints",
  "activities": "Day 1:\n- Discovery research on industry patterns\n- User interviews with 5 engineers\n- Stakeholder meetings with product team\n\nDay 2:\n- Competitor analysis of 3 tools\n- Architecture review session\n- Story crystallization workshop",
  "outcomes": "✓ Problem statement drafted and validated\n✓ 3 personas identified and documented\n✓ 2 hard constraints defined\n✓ 5 initial stories crystallized\n✓ Priority ordering agreed",
  "questions_added": "Q1-Q5",
  "decisions_made": "D1, D2",
  "research_conducted": "R1",
  "next_steps": "1. Transition to Story Crystallization phase\n2. Begin Story 1 development\n3. Schedule architecture review for Week 2"
}
```

```bash
log-iteration.py --json-file examples/iteration-summary.json
```

---

### Example 4: Research Entry

**File: `examples/research-entry.json`**
```json
{
  "topic": "Authentication Patterns in SaaS Products",
  "purpose": "Understand industry best practices for API authentication to inform Story 1 implementation",
  "approach": "Reviewed documentation and implementation for:\n- GitHub (REST API)\n- Slack (Web API)\n- Stripe (API)\n- Auth0 (service)",
  "findings": "JWT with RS256 signing is industry standard\nToken expiry: 1 hour common, with refresh tokens\nRate limiting tied to token, not IP\nRevocation handled via token blocklist",
  "patterns": "Pattern 1: Short-lived access tokens (1h) + long-lived refresh (30d)\nPattern 2: API key + secret for server-to-server\nPattern 3: OAuth2 for third-party integrations",
  "examples": "GitHub: Personal access tokens, OAuth apps, GitHub Apps\nSlack: Bot tokens, user tokens, legacy tokens\nStripe: Secret keys (live/test), restricted keys",
  "implications": "Recommend Pattern 1 for our API\nNeed token rotation strategy (FR-008)\nMust handle revocation (EC-05)\nRate limiting per token (FR-012)",
  "stories": "Story 1, Story 3",
  "questions": "Q5, Q8, Q12"
}
```

```bash
log-research.py --json-file examples/research-entry.json
```

---

## Further Reading

- **Schema Files:** See `decision-input.json`, `iteration-input.json`, `research-input.json` for complete schema definitions
- **Troubleshooting:** See `references/troubleshooting.md` for common issues
- **Tier References:** See `references/scripts-tier-*.md` for script-specific documentation
- **JSON Schema:** [json-schema.org](https://json-schema.org/) for schema specification

---

**Last Updated:** 2026-01-20
**Version:** 2.0 (Initial JSON stdin support release)
