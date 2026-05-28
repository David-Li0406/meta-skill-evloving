---
name: status-reporting
description: Use this skill when checking project status, starting sessions, reviewing activity, or when "sitrep", "status report", or "what's changed" are mentioned.
---

# Status Reporting

Gather -> aggregate -> present pattern for comprehensive project status across VCS, PRs, issues, CI.

<when_to_use>

- Starting work sessions (context refresh)
- Checking project/team activity
- Understanding PR/stack relationships
- Quick status overview before planning
- Reviewing recent changes across systems
- Understanding blockers

NOT for: deep-dive into specific items, real-time monitoring, single-source queries

</when_to_use>

<core_pattern>

**Three-phase workflow**:

1. **Gather** - collect from multiple sources
2. **Aggregate** - combine, filter, cross-reference by time/stack/status
3. **Present** - format for scanning with actionable insights

Key principles:
- Multi-source integration (VCS + code review + issues + CI)
- Time-aware filtering (natural language -> query params)
- Stack-aware organization (group by branch hierarchy)
- Scannable output (visual indicators, relative times)
- Actionable insights (highlight blockers, failures)

</core_pattern>

<workflow>

**Phase 1: Parse Constraints**

Extract time from natural language:
- "last X hours" -> `-Xh`
- "past X days" / "last X days" -> `-Xd`
- "yesterday" -> `-1d`
- "this morning" / "today" -> `-12h`
- "this week" -> `-7d`
- "since {date}" -> calculate days back

Default: 7 days if unspecified.

**Phase 2: Gather Data**

Run parallel queries for each available source:

1. **VCS State** - branch/stack structure, recent commits, working dir status
2. **Code Review** - open PRs, CI status, review decisions, activity
3. **Issues** - recently updated, status, priority, assignments
4. **CI/CD** - pipeline runs, success/failure, error summaries

Skip unavailable sources gracefully.

**Phase 3: Aggregate**

Cross-reference and organize:
- Group PRs by stack position (if stack-aware)
- Filter all by time constraint
- Correlate issues with PRs/branches
- Identify blockers (failed CI, blocking reviews)
- Calculate relative timestamps

**Phase 4: Present**

Format for scanning:
- Hierarchical sections (VCS -> PRs -> Issues -> CI)
- Visual indicators (`✓` `✗` `⏳` for status)
- Relative timestamps for recency
- Highlight attention-needed items
- Include links for deep-dive

</workflow>