---
name: df:insights
description: Generate daily and weekly codebase activity summaries from Azure DevOps (PRs, work items), local git commits, and Confluence. Use when asked about "what happened", "codebase activity", "team summary", "pr summary", or to understand what's going on in a large codebase.
---

# Codebase Insights Skill

Generate activity summaries revealing what's happening in a codebase day-to-day and week-to-week.

## Data Sources

| Source           | Tool               | Data                                    |
| ---------------- | ------------------ | --------------------------------------- |
| Azure PRs        | `az repos pr list` | PRs opened, merged, reviewed            |
| Azure Work Items | `az boards query`  | Tickets started, completed, in progress |
| Local Git        | `git log`          | Commits in current repo                 |
| Confluence       | Atlassian MCP      | Recently modified pages                 |

## Workflow

### 1. Collect Data

Run collectors from the current repository directory:

```bash
# Azure PRs (last N days)
node ${CLAUDE_PLUGIN_ROOT}/skills/insights/collectors/azure-prs.js --days 7

# Azure work items (last N days)
node ${CLAUDE_PLUGIN_ROOT}/skills/insights/collectors/azure-workitems.js --days 7

# Local git commits (last N days)
node ${CLAUDE_PLUGIN_ROOT}/skills/insights/collectors/git-commits.js --days 7
```

**Confluence:** Search for recent pages using Atlassian MCP:

```
mcp__atlassian__rovo_search(query: "modified:>YYYY-MM-DD space_key")
```

Extract and save to `.insights/raw/confluence.json`:

```json
[
  {
    "id": "12345",
    "title": "Page Title",
    "space": "SPACE",
    "lastModified": "2025-01-08",
    "lastModifiedBy": "Author Name",
    "url": "https://..."
  }
]
```

Data saved to `.insights/raw/`.

### 2. Filter by Period

```bash
# For daily summary
node ${CLAUDE_PLUGIN_ROOT}/skills/insights/collectors/filter-by-date.js .insights/raw/commits.json --day 2025-01-08

# For weekly summary
node ${CLAUDE_PLUGIN_ROOT}/skills/insights/collectors/filter-by-date.js .insights/raw/commits.json --week 2025-01-08
```

### 3. Generate Summary

Use templates from `${CLAUDE_PLUGIN_ROOT}/skills/insights/templates/`:

- `daily-summary.md` - Daily activity report
- `weekly-summary.md` - Weekly activity report

### 4. Save Output

Reports saved to `.insights/`:

- Daily: `.insights/YYYY-MM-DD-insights.md`
- Weekly: `.insights/YYYY-WXX-insights.md`

## Commands

| Command                      | Description                             |
| ---------------------------- | --------------------------------------- |
| `/df:insights:daily [date]`  | Generate daily codebase summary         |
| `/df:insights:weekly [date]` | Generate weekly codebase summary        |
| `/df:insights:catchup`       | Download raw data since last collection |

### Monthly Review

For monthly reviews, use the significance-based formatter:

```bash
node ${CLAUDE_PLUGIN_ROOT}/skills/insights/collectors/format-review.mjs --month YYYY-MM
```

Or follow the `templates/monthly-review.md` template for AI-generated analysis focusing on:

- High-impact initiatives grouped by theme
- Effort estimation (HIGH/MEDIUM/LOW)
- Status tracking (Shipped/In Progress/Troubled)
- Top contributors by focus area

## Usage Examples

- "What happened in the codebase today?"
- "Summarize this week's activity"
- "Show me PR activity for the last 7 days"
- "What work items were completed this week?"

## Prerequisites

```bash
# Azure DevOps CLI configured
az devops configure --defaults organization=https://dev.azure.com/YOUR_ORG project=YOUR_PROJECT

# Authenticated
az login
```

## Confluence Integration

Requires Atlassian MCP server configured. During data collection, use `rovo_search` to find recently modified pages.

**Search query format:** `modified:>YYYY-MM-DD [space_key] [keywords]`

Collects metadata only: page title, space, last modified date, author. No full content.

Ensure Atlassian MCP is configured.

## Output Structure

```
.insights/
├── raw/
│   ├── prs.json           # Azure PRs
│   ├── workitems.json     # Azure work items
│   ├── commits.json       # Local git commits
│   └── confluence.json    # Confluence pages
├── 2025-01-08-insights.md # Daily reports
└── 2025-W02-insights.md   # Weekly reports
```

## Report Sections

### Daily Summary

- **Pull Requests**: Opened, merged, reviewed today
- **Commits**: By author, by area
- **Work Items**: State changes (started, completed)
- **Key Changes**: AI-synthesized summary

### Weekly Summary

- **Overview**: High-level activity summary
- **PR Activity**: Week's PRs with outcomes
- **Commit Themes**: Patterns and focus areas
- **Work Items**: Sprint progress, completions
- **Contributors**: Who worked on what
- **Highlights**: Notable achievements

### Monthly Review

- **High-Impact Initiatives**: Work grouped by theme with effort/status
- **Feature Completions**: What shipped and its impact
- **Top Contributors**: Who drove what areas
- **Themes Summary**: PR distribution across themes
- **Key Observations**: Merge rate, bottlenecks, concerns
