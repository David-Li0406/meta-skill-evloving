# Artifact Tracking Templates Index

Complete, ready-to-use templates for MeatyPrompts tracking artifacts.

## Files in This Directory

### Core Templates (4 types)

1. **progress-template.md** (6.5 KB)
   - Phase implementation progress tracking
   - Task management and blocker tracking
   - Success criteria and testing strategy
   - Usage: `.claude/progress/[prd-name]/phase-[N]-progress.md`

2. **context-template.md** (9.6 KB)
   - Implementation decisions and rationale
   - Architecture patterns and integration points
   - Gotchas, learnings, and technical patterns
   - Usage: `.claude/worknotes/[prd-name]/phase-[N]-context.md`

3. **bug-fix-template.md** (6.5 KB)
   - Monthly bug fix tracking
   - Severity grouping and root cause analysis
   - Component hotspot identification
   - Trend analysis and preventive recommendations
   - Usage: `.claude/worknotes/fixes/bug-fixes-tracking-MM-YY.md`

4. **observation-template.md** (11 KB)
   - Monthly observation and insight logging
   - Pattern discoveries, performance insights, architectural learnings, tools
   - High/medium/low impact categorization
   - Trend analysis and implementation checklist
   - Usage: `.claude/worknotes/observations/observation-log-MM-YY.md`

### Documentation

5. **README.md** (9.8 KB)
   - Complete guide to using all 4 templates
   - Quick start instructions
   - File naming conventions
   - Placeholder reference
   - Tips for effective use
   - Integration with tracking system

6. **TEMPLATES-INDEX.md** (this file)
   - Quick reference to all files in this directory

---

## Quick Start

### 1. Choose Your Template

| Task | Template | Location |
|------|----------|----------|
| Track phase progress | progress-template.md | `.claude/progress/[prd]/phase-[N]-progress.md` |
| Document phase learnings | context-template.md | `.claude/worknotes/[prd]/phase-[N]-context.md` |
| Log monthly bug fixes | bug-fix-template.md | `.claude/worknotes/fixes/bug-fixes-tracking-MM-YY.md` |
| Log monthly observations | observation-template.md | `.claude/worknotes/observations/observation-log-MM-YY.md` |

### 2. Copy Template to Destination

```bash
# Progress example
cp templates/progress-template.md .claude/progress/advanced-editing-v2/phase-1-progress.md

# Context example
cp templates/context-template.md .claude/worknotes/blocks-v2/phase-2-context.md

# Bug fix example
cp templates/bug-fix-template.md .claude/worknotes/fixes/bug-fixes-tracking-11-25.md

# Observation example
cp templates/observation-template.md .claude/worknotes/observations/observation-log-11-25.md
```

### 3. Fill in Placeholders

All templates use `[PLACEHOLDER]` format. Replace with actual values:

- `[PRD_ID]` → `advanced-editing-v2`
- `[PHASE_NUMBER]` → `1`, `2`, `3`
- `[MM-YY]` → `11-25`, `10-25`, `12-25`
- `[YYYY-MM-DD]` → `2025-11-15`
- `[AGENT_NAME]` → `ui-engineer`, `backend-developer`

### 4. Follow Section Guidance

Each template section includes:
- Inline comments explaining purpose
- Example content
- Clear instructions
- Related fields and links

### 5. Commit to Git

```bash
git add .claude/progress/[prd]/phase-[N]-progress.md
git commit -m "Create progress tracking for Phase N"
```

---

## Template Features

### YAML Frontmatter (All Templates)

- Machine-readable metadata for agent queries
- Critical fields for filtering and sorting
- Status, ownership, and counts
- Designed for 95-99% token efficiency

Example frontmatter:

```yaml
---
type: progress
prd: "advanced-editing-v2"
phase: 1
status: "in-progress"
overall_progress: 35
blockers: []  # Array of blocker objects
---
```

### Markdown Body (All Templates)

- Human-readable narrative content
- Detailed explanations and context
- Tables for quick reference and scanning
- Clear section hierarchy
- Examples where needed

---

## File Sizes & Structure

```
templates/
├── progress-template.md           (6.5 KB) - Compact yet comprehensive
├── context-template.md            (9.6 KB) - Largest due to detail needs
├── bug-fix-template.md            (6.5 KB) - Monthly tracking format
├── observation-template.md        (11 KB)  - Comprehensive insight tracking
├── README.md                      (9.8 KB) - Complete usage guide
└── TEMPLATES-INDEX.md             (this file)

Total: ~53 KB of templates and documentation
```

---

## Key Design Principles

### 1. Hybrid Format

All templates combine:
- **YAML Frontmatter**: Machine-readable metadata
- **Markdown Body**: Human-readable narrative
- **Tables**: Easy scanning and structure

### 2. Progressive Disclosure

- **Frontmatter**: Critical data for quick queries
- **Tables**: Summary-level information
- **Sections**: Detailed context and explanation

### 3. Token Efficiency

- ~95-99% token reduction for common queries
- Agents query YAML frontmatter, not prose
- Supporting files for detailed context (on-demand)

### 4. Git-Friendly

- Meaningful diffs show actual changes
- Formatting doesn't affect readability
- Append-only patterns for bug fixes and observations

### 5. AI Agent Optimized

- Structured YAML for programmatic access
- Clear links between related artifacts
- Index fields for cross-document queries
- "Quick Reference for AI Agents" sections

---

## Integration Points

### With Progress Tracking

Progress files track "what" and "where":
- Task status and blockers
- Success criteria and completion estimates
- File changes and testing strategy

### With Context Notes

Context files track "why" and "how":
- Architecture decisions and rationale
- Integration patterns and data flows
- Gotchas and lessons learned
- Technical debt and future work

### With Bug Fixes

Bug fix files track "problems" and "solutions":
- Monthly trending by severity
- Component hotspot identification
- Root cause patterns
- Preventive recommendations

### With Observations

Observation files track "insights" and "learnings":
- Pattern discoveries for reuse
- Performance optimization opportunities
- Architectural insights for system design
- Tool and technique improvements

---

## Related Documentation

See the `ai/` directory for comprehensive guides:

- `TRACKING-ARTIFACTS-DESIGN.md` - Complete specification
- `TRACKING-ARTIFACTS-QUICK-REFERENCE.md` - At-a-glance guide
- `TRACKING-ARTIFACTS-INDEX.md` - Full architectural overview
- `TRACKING-ARTIFACTS-MIGRATION-GUIDE.md` - Migration strategies
- `examples/progress-example.md` - Real working example
- `examples/context-example.md` - Real working example

---

## Support & Examples

### Working Examples

Real examples showing how templates are used in practice:

- `ai/examples/progress-example.md` - Complete progress file (16 KB)
- `ai/examples/context-example.md` - Complete context file (21 KB)
- `ai/examples/query-helpers.js` - Helper functions for querying

### Quick Reference

For rapid answers, see README.md sections:
- Quick Start Guide
- Template Structure Overview
- Placeholders Reference
- File Naming Conventions
- Tips for Effective Use

---

## Version Info

- **Created**: 2025-11-17
- **Version**: 1.0
- **Format**: YAML + Markdown hybrid
- **Target Audience**: AI Agents + Developers
- **Token Efficiency**: 95-99% reduction for common queries

---

## File Manifest

| File | Size | Type | Purpose |
|------|------|------|---------|
| progress-template.md | 6.5 KB | Template | Phase progress tracking |
| context-template.md | 9.6 KB | Template | Implementation context |
| bug-fix-template.md | 6.5 KB | Template | Monthly bug fix tracking |
| observation-template.md | 11 KB | Template | Monthly observations |
| README.md | 9.8 KB | Guide | Complete usage documentation |
| TEMPLATES-INDEX.md | this file | Index | Quick reference and manifest |
