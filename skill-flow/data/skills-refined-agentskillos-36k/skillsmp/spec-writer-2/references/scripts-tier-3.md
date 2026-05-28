# Tier 3: Enhancement Scripts

Enhancement scripts for research logging, revisions, iteration tracking, and status monitoring. Read this reference when logging research findings, tracking revisions to graduated stories, logging iteration summaries, or getting quick status overview.

## Overview

**When to use these scripts:**
- Logging research findings
- Recording revisions to graduated stories
- Logging iteration summaries
- Finding iteration history
- Getting quick story status overview

**Scripts in this tier:**
1. log-research.py - Log research findings
2. add-revision.py - Record story revisions
3. log-iteration.py - Log iteration summaries
4. find-iterations.py - Find and filter iterations
5. story-status.sh - Quick status overview

---

## log-research.py

Log research to RESEARCH.md using template. Similar to log-decision.py but for research entries.

**Usage:**
```bash
log-research.py --topic TOPIC --purpose PURPOSE [OPTIONS]
log-research.py --from-stdin
```

**Options:**
- `--topic TEXT` - Research topic (required)
- `--purpose TEXT` - Why research was conducted
- `--approach TEXT` - How research was conducted
- `--findings TEXT` - Key findings
- `--patterns TEXT` - Industry patterns identified
- `--examples TEXT` - Relevant examples from products
- `--implications TEXT` - Implications for stories
- `--stories TEXT` - Stories informed (comma-separated)
- `--questions TEXT` - Related questions (comma-separated)
- `--from-stdin` - Read pipe-separated input
- `--discovery-path PATH` - Explicit discovery/ path

**Examples:**
```bash
# Full research entry
log-research.py \
  --topic "CI/CD Integration Patterns" \
  --purpose "Understand industry standards for polling vs webhooks" \
  --approach "Web search, documentation review, GitHub API research" \
  --findings "Most tools use 30-60 second polling for non-critical updates" \
  --patterns "Slack uses webhooks, GitHub uses polling + webhooks hybrid" \
  --implications "30-second polling is acceptable, can add webhooks later" \
  --stories "Story 2, Story 3" \
  --questions "Q15, Q18"

# Minimal research
log-research.py \
  --topic "Authentication Best Practices" \
  --purpose "Choose auth method" \
  --findings "JWT most common"

# Pipe-separated
echo "Auth patterns|Find best approach|JWT most common|Story 1|Q5" | \
  log-research.py --from-stdin
```

**Output:**
```
✓ Logged R5: CI/CD Integration Patterns
  Stories: Story 2, Story 3
  Questions: Q15, Q18
```

**Entry Format:**
```markdown
## R5: CI/CD Integration Patterns — 2026-01-19

**Purpose**: Understand industry standards for polling vs webhooks

**Approach**: Web search, documentation review, GitHub API research

**Findings**:
Most tools use 30-60 second polling for non-critical updates

**Industry Patterns**:
Slack uses webhooks, GitHub uses polling + webhooks hybrid

**Relevant Examples**:
[Examples from products]

**Implications**:
30-second polling is acceptable, can add webhooks later

**Stories Informed**: Story 2, Story 3

**Related Questions**: Q15, Q18

---
```

---

## add-revision.py

Add revision entry to REVISIONS.md when graduated stories need changes.

**Usage:**
```bash
add-revision.py --story-number NUMBER \\
                --change-type "Type of change" \\
                --trigger "What caused revision" \\
                --before "Content before" \\
                --after "Content after" \\
                [--decision D#]
```

**When to use:**
- Graduated story needs additional scenario
- Requirement modified after graduation
- Story scope adjusted based on new information

**Examples:**
```bash
# Add scenario to graduated story
add-revision.py \
  --story-number 1 \
  --change-type "Added acceptance scenario" \
  --trigger "Story 3 revealed edge case not covered" \
  --before "Scenarios 1-2 only" \
  --after "Added scenario 3 for edge case" \
  --decision D52

# Modify requirement
add-revision.py \
  --story-number 2 \
  --change-type "Modified FR-005" \
  --trigger "Story 5 revealed conflicting requirement" \
  --before "System MUST cache indefinitely" \
  --after "System MUST cache for 15 minutes" \
  --decision D58
```

**Output:**
```
✓ Logged REV-001: Story 1 - Added acceptance scenario
  Decision: D52
```

**Entry Format:**
```markdown
## REV-001: Story 1 - Added acceptance scenario — 2026-01-19

**Trigger**: Story 3 revealed edge case not covered

**Before**:
```
Scenarios 1-2 only
```

**After**:
```
Added scenario 3 for edge case
```

**Decision Reference**: D52

**User Confirmed**: Pending — [Date pending]

---
```

**Process:**
1. Use add-revision.py to log the revision
2. Manually update SPEC.md with the change
3. Manually update revision entry with confirmation date
4. Update SPEC.md appendix with revision summary

---

## log-iteration.py

Log iteration summary to ITERATIONS.md. Use this after completing a discovery cycle to record what was accomplished, what was learned, and next steps.

**Usage:**
```bash
log-iteration.py --date-range DATE --phase PHASE --goals GOALS [OPTIONS]
log-iteration.py --from-stdin
```

**Options:**
- `--date-range TEXT` - Date or date range (e.g., "2026-01-19" or "Jan 19-20") (required)
- `--phase TEXT` - Discovery phase name (required)
- `--goals TEXT` - Iteration goals (use semicolons to separate) (required)
- `--activities TEXT` - Activities performed
- `--outcomes TEXT` - Key outcomes
- `--questions-added TEXT` - Questions added (e.g., "Q1-Q5" or "Q9, Q12")
- `--decisions-made TEXT` - Decisions made (e.g., "D1, D2")
- `--research-conducted TEXT` - Research conducted (e.g., "R1, R3")
- `--next-steps TEXT` - Next steps
- `--from-stdin` - Read pipe-separated input
- `--discovery-path PATH` - Explicit discovery/ path

**Examples:**
```bash
# Full iteration entry
log-iteration.py \
  --date-range "2026-01-19" \
  --phase "Problem Exploration" \
  --goals "Understand problem; Identify personas; Define constraints" \
  --activities "Discovery research; User interviews; Stakeholder meetings" \
  --outcomes "Problem statement drafted; 3 personas identified; 2 constraints documented" \
  --questions-added "Q1-Q5" \
  --decisions-made "D1, D2" \
  --research-conducted "R1" \
  --next-steps "Transition to Story Crystallization"

# Minimal iteration
log-iteration.py \
  --date-range "2026-01-20" \
  --phase "Story Crystallization" \
  --goals "Define initial story backlog" \
  --outcomes "5 stories identified and prioritized"

# Pipe-separated
echo "2026-01-20|Story Crystallization|Define stories|Story backlog|5 stories|Q9-Q15|D1,D2|R1|Graduate stories" | \
  log-iteration.py --from-stdin
```

**Output:**
```
✓ Logged ITR-001: 2026-01-19 — Problem Exploration
  Outcomes: Problem statement drafted; 3 personas identified; 2 constraints documented
  Next: Transition to Story Crystallization
```

**Entry Format:**
```markdown
## ITR-001: 2026-01-19 — Problem Exploration

**Phase**: Problem Exploration

**Goals**:
Understand problem; Identify personas; Define constraints

**Activities**:
Discovery research; User interviews; Stakeholder meetings

**Key Outcomes**:
Problem statement drafted; 3 personas identified; 2 constraints documented

**Questions Added**: Q1-Q5

**Decisions Made**: D1, D2

**Research Conducted**: R1

**Next Steps**:
Transition to Story Crystallization

---
```

**When to log iterations:**
- After completing a discovery cycle (daily or every few days)
- When transitioning between phases
- After major milestones (e.g., story graduation)
- At the end of a sprint or time-box

---

## find-iterations.py

Find and filter iterations from ITERATIONS.md. Useful for reviewing past cycles, identifying patterns, or generating reports.

**Usage:**
```bash
find-iterations.py [--id ID] [--phase PHASE] [--keyword KEYWORD] [--format FORMAT]
```

**Options:**
- `--id TEXT` - Iteration ID(s) to find (comma-separated for multiple)
- `--phase TEXT` - Filter by phase name (case-insensitive regex)
- `--keyword TEXT` - Search by keyword in goals, outcomes, activities, or next steps
- `--format FORMAT` - Output format: table (default), summary, or json
- `--discovery-path PATH` - Explicit discovery/ path

**Examples:**
```bash
# Find specific iteration
find-iterations.py --id ITR-001

# Find all Problem Exploration iterations
find-iterations.py --phase "Problem Exploration"

# Search for iterations mentioning personas
find-iterations.py --keyword "personas"

# Multiple IDs in JSON format
find-iterations.py --id ITR-001,ITR-003 --format json

# Summary view of all iterations
find-iterations.py --format summary

# Find iterations in Story Crystallization phase
find-iterations.py --phase "Story" --format table
```

**Output Formats:**

Table (default):
```
| ID      | Date Range  | Phase              | Outcomes                           |
|---------|-------------|--------------------|------------------------------------|
| ITR-001 | 2026-01-19  | Problem Exploration| Problem statement drafted; 3 pe... |
| ITR-002 | Jan 19-20   | Story Crystallization | 5 stories identified and prioritized |
```

Summary:
```
ITR-001: 2026-01-19 — Problem Exploration
ITR-002: Jan 19-20 — Story Crystallization
```

JSON:
```json
[
  {
    "id": "ITR-001",
    "date_range": "2026-01-19",
    "phase": "Problem Exploration",
    "goals": "Understand problem; Identify personas",
    "outcomes": "Problem statement drafted; 3 personas identified",
    ...
  }
]
```

**Integration with log-iteration.py:**
```bash
# Log iteration
log-iteration.py --date-range "2026-01-19" --phase "Problem Exploration" --goals "..." --outcomes "..."

# Review what you logged
find-iterations.py --id ITR-001

# See all iterations in current phase
find-iterations.py --phase "Problem Exploration"

# Generate iteration report
find-iterations.py --format json > iteration-report.json
```

---

## story-status.sh

Quick overview of story states from STATE.md. Useful for daily standup or progress tracking.

**Usage:**
```bash
story-status.sh [--discovery-path PATH]
```

**What it displays:**
- Full Story Status Overview table from STATE.md
- Summary counts by status
- Progress percentage

**Examples:**
```bash
# From within discovery/
../scripts/story-status.sh

# From parent directory
scripts/story-status.sh --discovery-path discovery/
```

**Output:**
```
Story Status Overview
=====================

| # | Story | Priority | Status | Confidence | Blocked By |
|---|-------|----------|--------|------------|------------|
| 1 | Service Dependency Viz | P1 | ✅ In SPEC | 100% | - |
| 2 | Breaking Change Notif | P2 | ✅ In SPEC | 100% | - |
| 3 | Test Status Dashboard | P2 | 🔄 In Progress | 75% | Q23, Q25 |
| 4 | Impact Timeline View | P3 | ⏳ Queued | 20% | Story 3 |
| 5 | Cross-service Search | P2 | 🆕 New | 10% | - |

Summary:
  ✅ In SPEC: 2
  🔄 In Progress: 1
  ⏳ Queued: 1
  🆕 New: 1

Progress: 40% (2/5 stories completed)
```

**Use cases:**
- Daily progress check
- Sprint planning
- Team status updates
- Quick confidence assessment

---

## Workflow Example: Research to Decision to Revision

Complete workflow showing research informing decisions and triggering revisions:

```bash
# 1. Log research finding
log-research.py \
  --topic "Rate Limiting Patterns" \
  --purpose "Determine how to handle API rate limits" \
  --findings "Most APIs use 429 status with Retry-After header" \
  --stories "Story 3" \
  --questions "Q23"

# 2. Use research to make decision
log-decision.py \
  --title "Use exponential backoff for rate limits" \
  --context "Need strategy for API rate limiting" \
  --decision "Exponential backoff with Retry-After header" \
  --rationale "Based on R5 research, industry standard" \
  --stories "Story 3" \
  --questions "Q23"

# 3. Realize decision affects graduated Story 1
add-revision.py \
  --story-number 1 \
  --change-type "Added FR-012 for rate limiting" \
  --trigger "D15 established rate limiting strategy" \
  --before "No rate limiting requirement" \
  --after "Added FR-012: System MUST handle 429 responses" \
  --decision D15

# 4. Check impact
story-status.sh
find-decisions.py --story 1
```

---

## Integration Patterns

**Research → Decision Chain:**
```bash
# Research informs decision
log-research.py --topic "..." --findings "..." --stories "Story 2"
# ↓
log-decision.py --title "..." --rationale "Based on R5 findings" --stories "Story 2"
# ↓
# If affects graduated story:
add-revision.py --story-number 1 --decision D15
```

**Daily Workflow:**
```bash
# Morning: Check status
story-status.sh

# During work: Log as you go
log-research.py --topic "..." --findings "..."
log-decision.py --title "..." --decision "..."

# End of day: Validate and log iteration
validate-spec.py
log-iteration.py \
  --date-range "2026-01-19" \
  --phase "Story Crystallization" \
  --goals "..." \
  --outcomes "..." \
  --questions-added "Q10-Q15" \
  --decisions-made "D5, D6"

# If revisions needed:
add-revision.py --story-number N --change-type "..."
```

**Combining with Tier 1 & 2:**
```bash
# Complete story development cycle
update-story-status.py --story-number 3 --status in_progress
add-question.py --question "..." --category research --story 3
log-research.py --topic "..." --findings "..." --stories "Story 3" --questions "Q23"
log-decision.py --title "..." --stories "Story 3" --questions "Q23"
resolve-question.py --question Q23 --note "Resolved by D15, R5"
graduate-story.py --story-number 3
story-status.sh
```

---

## Tips

**Research Best Practices:**
- Log research as soon as you find insights
- Reference questions that prompted the research
- Note industry patterns for future reference
- Include concrete examples from real products

**Iteration Logging:**
- Log iterations after each discovery cycle (daily or every few days)
- Always include goals and outcomes - these provide the most value
- Reference related questions, decisions, and research for traceability
- Use iterations to identify patterns in your discovery process
- Review past iterations when planning next phase

**Revision Management:**
- Always link revisions to decisions
- Keep before/after clear and specific
- Get user confirmation before finalizing
- Update SPEC.md appendix after each revision

**Status Monitoring:**
- Run story-status.sh daily to track progress
- Use it in automation for team dashboards
- Pipe output to monitoring tools
- Include in CI/CD for spec validation gates
