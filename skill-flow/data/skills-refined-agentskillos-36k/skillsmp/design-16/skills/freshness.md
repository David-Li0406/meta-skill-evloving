---
name: design-freshness
description: Check Design Ops freshness against agentic engineering landscape. USE WHEN freshness check, update design ops, check for updates, monthly review.
context: fork
---

# Design Freshness

Runs the Design Ops freshness check to ensure methodology stays current with agentic engineering best practices. Runs in isolated context due to heavy web research operations.

## Why Forked Context

- Web searches consume significant context with search results
- Research can span multiple sources (Anthropic docs, MCP, cookbook, etc.)
- Report generation is verbose — full analysis shouldn't bloat main conversation
- Returns concise summary to main context for action planning

## Usage

```
/design-freshness quick   # Check known sources only
/design-freshness full    # Full landscape research
/design-freshness         # Defaults to quick
```

## Modes

### Quick Mode (5-10 min)
- Check source health (are URLs still valid?)
- Scan known Tier 1 & 2 sources for updates
- Generate brief status report

### Full Mode (15-30 min)
- Complete web research for new developments
- Validate findings against Anthropic-anchored criteria
- Generate impact analysis
- Create prioritized action plan
- Update dashboard

## Execution

**Step 1: Gather Context**
```
Read current Design Ops state:
- templates/ (what PRP templates exist)
- tools/ (what automation exists)
- examples/ (what patterns are documented)
- docs/ (what guidance exists)
```

**Step 2: Research Landscape**
```
Research agentic engineering developments from [LAST_SCAN_DATE] to today.

REQUIRED SOURCES:
- Anthropic official: docs.anthropic.com, anthropic.com/research
- Anthropic Cookbook: github.com/anthropics/anthropic-cookbook
- Claude Code docs: Current best practices
- MCP updates: modelcontextprotocol.io

For each finding provide:
- Source URL
- Validation evidence
- Key innovation
- Relevance to Design Ops (1-10)
- Recommended action (adopt/watch/ignore)
```

**Step 3: Validate Against Framework**
```
Score each source:
1. Anthropic Alignment (0-3)
2. Traction (0-3)
3. Design Ops Fit (0-3)
4. Freshness (0-1)

Total /10. Only sources scoring ≥6 get recommended.
```

**Step 4: Generate Impact Analysis**
```
Compare findings against current Design Ops:
- VALIDATED: Design Ops already does this
- NEEDS UPDATE: Design Ops should change
- DEPRECATED: Design Ops should remove
- NEW ADDITIONS: Design Ops should add
```

**Step 5: Create Action Plan**
```
Write to docs/freshness/actions/YYYY-MM-actions.md:
- Quick Wins (< 1 hour)
- Short-term (1 day)
- Medium-term (1 week)
- Watch List (revisit next month)
```

**Step 6: Update Dashboard**
```
Update docs/freshness/dashboard.md:
- Last scan date
- Health score (0-100)
- Sources monitored
- Pending actions count
```

## Output Files

```
docs/freshness/
├── discoveries/YYYY-MM-raw.md       # Raw research findings
├── validated/YYYY-MM-validated.md   # Scored and filtered
├── impact/YYYY-MM-impact.md         # Gap analysis
├── actions/YYYY-MM-actions.md       # Prioritized todo list
├── reports/YYYY-MM-summary.md       # Executive summary
└── dashboard.md                     # Current state
```

## Return to Main Context

After completion, returns concise summary:
```
Freshness Check Complete
========================
Health Score: 85/100
Developments Found: 4
P1 Actions: 2
P2 Actions: 2

Top priorities:
1. Update SKILL.md schema for context: fork
2. Add MCP integration guidance

Full report: docs/freshness/reports/YYYY-MM-freshness-report.md
```

## Automation

Install monthly reminder:
```bash
./tools/freshness/install.sh
```

Triggered on 1st of each month at 10:00 AM via launchd.

---

*Forked skill — heavy research isolated from main context*
