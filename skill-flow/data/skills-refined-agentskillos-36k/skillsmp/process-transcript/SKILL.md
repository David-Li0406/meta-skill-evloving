---
name: process-transcript
description: Process a VTT transcript into a comprehensive, multi-tab HTML dashboard using specialized analysis agents. Use when the user provides a .vtt file, has a transcript to process, or mentions a meeting recording. This is the PRIMARY skill for handling transcripts.
allowed-tools: Read, Write, Bash, Glob
---

# Process Transcript to Dashboard (Advanced)

Convert a .vtt meeting transcript into a comprehensive, deployed HTML dashboard using multiple specialized analyzers.

## CRITICAL: What This Skill Does

1. ✅ Orchestrates **6 specialized analysis agents**
2. ✅ Runs **consolidation** to ensure consistency
3. ✅ Creates a **multi-tab HTML dashboard** with rich insights
4. ✅ Deploys to **surge.sh**
5. ✅ Returns a **public URL**

## NEVER DO

- ❌ Create markdown (.md) files
- ❌ Skip any analysis phase
- ❌ Skip the consolidation step
- ❌ Generate a simple single-page summary
- ❌ Skip the deployment

## Pipeline Steps

### Step 1: Setup
- Determine project name and date
- Create folder structure
- Copy transcript to `projects/{project}/transcripts/{date}.vtt`

### Step 2: Run Analysis Agents (IN PARALLEL if possible)

Delegate to each specialized agent in `.claude/agents/`:

1. **timeline-analyzer** → `analysis/timeline.json`
   - Identifies meeting segments (review, retro, planning)
   - Creates timeline with timestamps and summaries

2. **people-analyzer** → `analysis/people.json`
   - Analyzes each participant's contributions
   - Calculates speaking time vs. value contributed
   - Provides constructive feedback

3. **insights-generator** → `analysis/insights.json`
   - Finds non-obvious patterns and observations
   - Identifies risks, opportunities, team health signals
   - Generates ad-hoc creative insights

4. **analytics-generator** → `analysis/analytics.json`
   - Produces data-driven metrics and statistics
   - Creates chart-ready data
   - Calculates efficiency scores

5. **longitudinal-analyzer** → `analysis/longitudinal.json`
   - Compares with previous meetings (if available)
   - Identifies trends and patterns over time
   - Tracks improvement and recurring issues

6. **scrum-analyzer** → `analysis/scrum.json`
   - Analyzes scrum methodology compliance and ceremony effectiveness
   - Evaluates scrum role fulfillment (PO, SM, Dev Team)
   - Identifies scrum anti-patterns and health metrics
   - Provides agile coaching recommendations

### Step 3: CONSOLIDATION (Critical Quality Step)

Run the **consolidator** agent to:

1. **Normalize names**
   - Create canonical name mapping
   - If "Alice" is identified as "Product Owner", use "Alice" everywhere
   - Replace role references with actual names where known

2. **Cross-reference validation**
   - Verify consistency between agent outputs
   - Resolve metric discrepancies
   - Link action items to owners

3. **Deduplicate**
   - Remove redundant insights
   - Merge duplicate action items
   - Consolidate repeated quotes

4. **Enrich data**
   - Connect decisions to timeline segments
   - Link insights to relevant participants
   - Add IDs for cross-referencing

5. **Quality check**
   - Flag unidentified participants
   - Note action items without owners
   - Document all changes made

Output: `analysis/consolidated.json`

### Step 4: Generate Multi-Tab Dashboard

Create `projects/{project}/dashboards/{date}/index.html` using the **consolidated** data:

#### Tab 1: Overview
- Meeting summary
- Key decisions (with timeline refs)
- Action items with owners (canonical names)
- Quick stats

#### Tab 2: Timeline
- Visual timeline of meeting segments
- Duration bars
- Key moments highlighted
- Participants (by canonical name)
- Energy level indicators

#### Tab 3: People & Roles
- Participant cards (canonical names with roles as subtitle)
- Speaking time visualization
- Value contribution ratings
- Strengths and feedback for each person
- Team dynamics summary

#### Tab 4: Insights
- Ad-hoc observations
- Risk signals
- Opportunity spotting
- Team health indicators
- Notable quotes (attributed to canonical names)

#### Tab 5: Analytics
- Charts and graphs (using Chart.js)
- Time breakdown pie chart
- Participation bar chart (canonical names)
- Sentiment analysis
- Efficiency scores

#### Tab 6: Trends (if historical data exists)
- Week-over-week comparisons
- Recurring themes
- Improvement tracking
- Trajectory visualizations

### Step 5: Deploy to Surge.sh
```bash
cd projects/{project}/dashboards/{date}
surge . {project}-{date}.surge.sh
```

### Step 6: Report Success
```
✓ Analysis complete:
  - Timeline: 5 segments identified
  - People: 6 participants analyzed  
  - Insights: 8 observations generated
  - Analytics: 12 metrics calculated
  - Trends: Compared with 3 previous meetings
  - Scrum: 3 ceremonies analyzed, 2 anti-patterns detected

✓ Consolidation:
  - Normalized 12 name references
  - Merged 2 duplicate action items
  - Identified 2 unidentified speakers
  - Quality score: 92/100

✓ Dashboard generated: projects/{project}/dashboards/{date}/index.html
✓ Deployed to: https://{project}-{date}.surge.sh
```

## File Structure

```
projects/{project}/
├── transcripts/{date}.vtt
├── analysis/
│   ├── timeline.json          # From timeline-analyzer
│   ├── people.json            # From people-analyzer
│   ├── insights.json          # From insights-generator
│   ├── analytics.json         # From analytics-generator
│   ├── longitudinal.json      # From longitudinal-analyzer
│   ├── scrum.json            # From scrum-analyzer
│   └── consolidated.json      # From consolidator (USED FOR DASHBOARD)
└── dashboards/{date}/
    └── index.html             # THE DELIVERABLE
```

## Dashboard Quality Standards

The dashboard should be:
- **Consistent** - Same names/terms throughout all tabs
- **Beautiful** - Modern, polished design with Tailwind CSS
- **Interactive** - Tabs, hover effects, expandable sections
- **Data-rich** - Charts, metrics, visualizations
- **Actionable** - Clear next steps and recommendations
- **Insightful** - Goes beyond obvious observations
- **Human** - Recognizes individual contributions by name

## Technology Stack

- Tailwind CSS (CDN) - Styling
- Chart.js (CDN) - Data visualizations
- Alpine.js (CDN) - Tab interactivity
- Vanilla JS - Additional interactions

## Consolidation Examples

### Name Normalization
```
BEFORE (inconsistent):
- Timeline: "Product Owner presented..."
- People: "Alice spoke for 15 minutes..."
- Action Items: "PO to follow up..."

AFTER (consolidated):
- Timeline: "Alice (Product Owner) presented..."
- People: "Alice spoke for 15 minutes..."
- Action Items: "Alice to follow up..."
```

### Cross-Reference
```
BEFORE (disconnected):
- Decision: "Decided to postpone feature X"
- Timeline: Segment 3 mentions postponement
- Person: Bob raised the concern

AFTER (connected):
- Decision: "Decided to postpone feature X" 
  - Decided during: Segment 3 (Sprint Planning)
  - Raised by: Bob
  - Related insight: Technical debt concern #2
```
