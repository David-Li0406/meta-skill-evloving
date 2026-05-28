# Artifact Tracking Templates

Complete, ready-to-use templates for all 4 artifact types used in MeatyPrompts development tracking.

## Template Files

### 1. Progress Tracking Template
**File**: `progress-template.md`

**Purpose**: Track phase implementation progress, tasks, blockers, and completion status

**Use When**:
- Starting a new phase in a multi-phase PRD
- Need to track task status and blockers during implementation
- Want to communicate progress across sessions

**Location to Create**: `.claude/progress/[prd-name]/phase-[N]-progress.md`

**Key Sections**:
- YAML frontmatter with task counts, status, owners
- Phase overview and scope
- Success criteria checklist
- Task tracking table (ID, status, agent, estimate)
- Architecture context (current state, patterns)
- Blockers and dependencies
- Testing strategy
- Next session agenda

**Example Usage**:
```bash
cp progress-template.md ../.claude/progress/advanced-editing-v2/phase-1-progress.md
# Then replace all [PLACEHOLDER] values with actual content
```

---

### 2. Context Notes Template
**File**: `context-template.md`

**Purpose**: Document implementation decisions, architectural patterns, integration points, and learnings

**Use When**:
- Phase is complete and you want to document "why" decisions were made
- Future agents need to understand the rationale behind implementations
- Want to capture gotchas and lessons learned
- Need to document integration patterns for future reference

**Location to Create**: `.claude/worknotes/[prd-name]/phase-[N]-context.md`

**Key Sections**:
- YAML frontmatter with phase status, blockers, decisions
- Architecture decisions with rationale and tradeoffs
- Integration points and data flows
- Technical patterns used
- Critical gotchas and learnings
- Performance considerations
- Security and accessibility notes
- State management and testing strategy
- Incomplete work and technical debt

**Example Usage**:
```bash
cp context-template.md ../.claude/worknotes/blocks-v2/phase-2-context.md
# Then fill in decisions, patterns, and learnings discovered during Phase 2
```

---

### 3. Bug Fix Tracking Template
**File**: `bug-fix-template.md`

**Purpose**: Track significant bug fixes by month for trending and pattern analysis

**Use When**:
- Month ends and you want to document fixes for reference
- Need to track root causes and prevent recurrence
- Want to identify component hotspots and systemic issues
- Analyzing trends across months

**Location to Create**: `.claude/worknotes/fixes/bug-fixes-tracking-MM-YY.md`

**Naming Convention**: `bug-fixes-tracking-11-25.md` for November 2025

**Key Sections**:
- YAML frontmatter with fix counts by severity
- Summary of major themes
- Individual fix details (issue, root cause, files modified, impact)
- Fixes grouped by severity (Critical, High, Medium, Low)
- Fixes grouped by component
- Fixes grouped by category (frontend, backend, database, integration)
- Trend analysis (hotspots, root causes, recommendations)
- Preventive actions for next month

**Example Usage**:
```bash
cp bug-fix-template.md ../.claude/worknotes/fixes/bug-fixes-tracking-11-25.md
# Then add entries for each fix in chronological order within month
```

---

### 4. Observation Log Template
**File**: `observation-template.md`

**Purpose**: Track patterns, insights, learnings, and techniques discovered during development

**Use When**:
- Month ends and you want to capture patterns/learnings
- Agents need to apply lessons from previous work
- Want to identify recurring themes and high-impact insights
- Tracking performance opportunities and tooling improvements

**Location to Create**: `.claude/worknotes/observations/observation-log-MM-YY.md`

**Naming Convention**: `observation-log-11-25.md` for November 2025

**Key Sections**:
- YAML frontmatter with observation counts by category
- Summary of major themes and insights
- Pattern discoveries (recurring patterns found in code)
- Performance insights (optimization opportunities)
- Architectural learnings (system design insights)
- Tools & techniques (workflow improvements)
- Summary tables by category
- High/medium/low impact observations
- Trend analysis month-over-month
- Implementation checklist
- Quick reference for AI agent queries

**Example Usage**:
```bash
cp observation-template.md ../.claude/worknotes/observations/observation-log-11-25.md
# Then add entries throughout the month or at month-end
```

---

## Quick Start Guide

### For Developers

1. **Choose which template** you need based on your task
2. **Copy template** to appropriate location (see paths above)
3. **Replace placeholders** (marked with `[PLACEHOLDER]`)
4. **Follow section guidance** - each section has instructions
5. **Commit to git** when done

### For AI Agents

1. **Read YAML frontmatter** for machine-readable metadata
2. **Query by fields**: status, severity, component, category, impact
3. **Use tables** for quick lookups
4. **Follow "Related" links** to connected observations/decisions
5. **Check "Quick Reference"** sections for curated answers

---

## Template Structure Overview

All templates follow a consistent structure:

### YAML Frontmatter
- Machine-readable metadata for agent queries
- All array fields and counts for trending
- Status, ownership, and critical information
- Should be parsed and used for filtering/sorting

### Markdown Body
- Human-readable narrative content
- Detailed explanations and context
- Tables for quick reference
- Examples where helpful
- Clear sections with headers

---

## Placeholders Reference

### Common Placeholders

| Placeholder | Example | Notes |
|------------|---------|-------|
| `[PRD_ID]` | `advanced-editing-v2` | From PRD filename, lowercase with hyphens |
| `[PHASE_NUMBER]` | `1`, `2`, `3` | Integer, not string |
| `[PHASE_TITLE]` | `Prompt Creation Modal Enhancements` | From PRD implementation plan |
| `[YYYY-MM-DD]` | `2025-11-15` | ISO format for dates |
| `[MM-YY]` | `11-25` | Month-year for bug fixes and observations |
| `[AGENT_NAME]` | `ui-engineer`, `backend-developer` | From agent definitions |
| `[COUNT]` | `5`, `3` | Integer count, not percentage |
| `[0-100]` | `35` | Progress percentage |

### Status Values

**Progress Files**:
- `planning` - Not yet started
- `in-progress` - Active development
- `review` - Waiting for review
- `complete` - Finished
- `blocked` - Waiting on external dependency

**Context Files**:
- `complete` - Phase is complete
- `blocked` - Phase is blocked
- `in-progress` - Phase is active

**Bug/Observation Files**:
- Use date-based organization (monthly)

---

## File Naming Conventions

### Progress Files
```
.claude/progress/[prd-name]/phase-[N]-progress.md

Examples:
.claude/progress/advanced-editing-v2/phase-1-progress.md
.claude/progress/blocks-v2-implementation/phase-2-progress.md
.claude/progress/web-refactor/phase-3-progress.md
```

### Context Files
```
.claude/worknotes/[prd-name]/phase-[N]-context.md

Examples:
.claude/worknotes/blocks-v2-implementation/phase-1-context.md
.claude/worknotes/advanced-editing-v2/phase-2-context.md
```

### Bug Fix Files
```
.claude/worknotes/fixes/bug-fixes-tracking-MM-YY.md

Examples:
.claude/worknotes/fixes/bug-fixes-tracking-11-25.md
.claude/worknotes/fixes/bug-fixes-tracking-10-25.md
.claude/worknotes/fixes/bug-fixes-tracking-12-25.md
```

### Observation Files
```
.claude/worknotes/observations/observation-log-MM-YY.md

Examples:
.claude/worknotes/observations/observation-log-11-25.md
.claude/worknotes/observations/observation-log-10-25.md
.claude/worknotes/observations/observation-log-12-25.md
```

---

## Tips for Effective Use

### Progress Files
- Keep tasks in YAML frontmatter for easy querying
- Update `overall_progress` as tasks complete
- Note blockers immediately when they arise
- Document architecture context for continuity
- Use tables for easy scanning

### Context Files
- One context file per phase (not multiple)
- Document decisions immediately while fresh
- Include "why not" for rejected alternatives
- Link to specific file:line locations
- Group related decisions together

### Bug Fix Files
- Create one file per month (append throughout month)
- Include root cause analysis (not just "what" but "why")
- Note component hotspots for trending
- Track severity for prioritization
- Make recommendations to prevent recurrence

### Observation Files
- Brief entries (1-2 lines per observation)
- One file per month (append daily)
- Categorize clearly (patterns, performance, architecture, tools)
- Link to related code/decisions
- Flag high-impact observations for priority action

---

## Examples Reference

Working examples are provided in the `ai/examples/` directory:

- `ai/examples/progress-example.md` - Real progress file showing complete structure
- `ai/examples/context-example.md` - Real context file with architecture decisions
- `ai/examples/query-helpers.js` - Helper functions for querying YAML frontmatter

View these to understand how to structure actual content.

---

## Integration with Tracking System

These templates integrate with the MeatyPrompts tracking system:

- **Progress files** feed completion status to phase reviews
- **Context files** provide "why" context for future implementation
- **Bug fix files** enable trend analysis and hotspot identification
- **Observation files** capture learnings for architectural improvements

All files use consistent YAML frontmatter for machine-readable metadata.

---

## Questions & Support

For detailed guidance on each artifact type, see:

- **Design Specification**: `ai/TRACKING-ARTIFACTS-DESIGN.md`
- **Quick Reference**: `ai/TRACKING-ARTIFACTS-QUICK-REFERENCE.md`
- **Migration Guide**: `ai/TRACKING-ARTIFACTS-MIGRATION-GUIDE.md`
- **Full Index**: `ai/TRACKING-ARTIFACTS-INDEX.md`
