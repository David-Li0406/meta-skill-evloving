---
name: phase-summary
description: Write or update phase summary documentation. Use when asked to create, write, or update a phase summary, document a phase, or summarize what was built in a phase.
---

# Phase Summary Writing Guide

When writing a phase summary, follow this exact structure with 12 sections.

## File Location

Save to: `docs/logs/PHASE_{X}_SUMMARY.md` (e.g., `PHASE_2I_SUMMARY.md`)

## Required Structure

### Header

```markdown
# Phase X: [Name]

**Status**: ✅ Completed / 📋 Planning / 🚧 In Progress
**Date**: [Month Day, Year] (use actual current date)
**Goal**: [One sentence - why does this phase exist?]
```

### Sections (in order)

1. **Overview** - 2-3 paragraphs + "Included in this phase" + "Explicitly excluded"
2. **Key Achievements** - Numbered list with inline references to ADRs/learning docs
3. **Database Schema** - Only if this phase added/modified schema
4. **API Endpoints** - Only if this phase added new endpoints
5. **Highlights** - Technical details, optimizations, quirks
6. **Testing & Validation** - Split manual vs automated
7. **Metrics** - Tables, counts, measurements
8. **Next Steps → Phase X+1** - Brief description + key features
9. **File Structure** - Tree diagram + key files with links
10. **Key Learnings** - Brief insights, link to learning docs
11. **References** - External URLs only (internal docs linked inline)

## Principles

- Use `---` dividers between sections
- Keep each item 1-3 bullets
- Inline refs for internal docs, end section for external URLs
- Use actual current date (check system context)
- No time estimates in Next Steps
- Omit sections that don't apply (e.g., no Database Schema if no DB changes)

## Example Section

```markdown
## Key Achievements

### 1. SSE Progress Endpoint
- Real-time streaming via `text/event-stream`
- JWT authentication via query parameter
- Reference: [ADR-016](../architecture/DECISIONS.md#adr-016-sse-for-real-time-progress-updates)

### 2. Frontend EventSource Connection
- React `useEffect` hook manages lifecycle
- Auto-reconnect on API Gateway timeout
```

## Before Writing

1. Check recent git commits: `git log --oneline -20`
2. Review existing phase summaries for style consistency
3. Identify key files changed in this phase
