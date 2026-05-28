---
name: geopolitical
prefix: geo
triggers:
  - conflict, war, military, violence, escalation, ceasefire, troops, combat, weapons
  - sanctions, embargo, OFAC, trade restrictions, asset freeze, designation, tariffs, export controls
  - bilateral relations, alliances, networks, coalition, partnership, rivalry
  - media coverage, sentiment, narrative, perception, portrayal, tone, bias
  - GDELT, CAMEO, Goldstein scale, geopolitical
---

# Geopolitical Research Domain

Specialized domain for geopolitical research using GDELT data sources and domain-expert agents. Routes queries to appropriate analysis types: conflict, sanctions, actors, or narrative.

## Query Routing

| Query Signals | Route To | Primary Agent | Supporting Agent |
|---------------|----------|---------------|------------------|
| conflict, war, fighting, violence, military, attack, escalation, ceasefire, troops, combat, weapons | Conflict Analysis | `deep-research:geo:conflict-analyst` | `deep-research:geo:actor-mapper` |
| sanctions, embargo, OFAC, trade restrictions, asset freeze, designation, tariffs, export controls, enforcement | Sanctions Research | `deep-research:geo:sanctions-researcher` | `deep-research:geo:trend-analyst` |
| relationship, alliance, network, between X and Y, bilateral, coalition, partnership, rivalry | Actor Analysis | `deep-research:geo:actor-mapper` | `deep-research:geo:trend-analyst` |
| media, coverage, sentiment, narrative, perception, portrayal, tone, how is X reported, bias | Narrative Analysis | `deep-research:geo:sentiment-tracker` | `deep-research:geo:trend-analyst` |

For multi-dimensional queries, deploy multiple agent types in parallel.

## Worker Agents

### Conflict Analysis

```
Task(
  subagent_type: "deep-research:geo:conflict-analyst",
  prompt: "Analyze conflict dynamics for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Active conflicts and CAMEO event patterns
- Goldstein scale trends (escalation/de-escalation)
- Key belligerents and their recent actions
- Third-party actor involvement

Use GDELT MCP tools: gdelt_events, gdelt_actors, gdelt_gkg
Return structured findings with GDELT data citations.",
  description: "Conflict analysis: [topic]"
)
```

### Sanctions Research

```
Task(
  subagent_type: "deep-research:geo:sanctions-researcher",
  prompt: "Research sanctions for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Active sanctions regimes and recent designations
- Economic impact indicators
- Enforcement actions and violations
- Evasion patterns detected

Use GDELT MCP tools: gdelt_gkg, gdelt_doc, gdelt_trends
Cross-reference with official sources (OFAC, EU).
Return findings with quantitative data.",
  description: "Sanctions research: [topic]"
)
```

### Actor Mapping

```
Task(
  subagent_type: "deep-research:geo:actor-mapper",
  prompt: "Map actor relationships for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Key actors and their types (state, non-state, IGO, etc.)
- Bilateral relationship patterns (Goldstein averages)
- Alliance structures and coalitions
- Relationship trends over time

Use GDELT MCP tools: gdelt_events, gdelt_actors
Return network analysis with relationship metrics.",
  description: "Actor mapping: [topic]"
)
```

### Narrative Analysis

```
Task(
  subagent_type: "deep-research:geo:sentiment-tracker",
  prompt: "Analyze media sentiment for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Overall tone and polarity
- Sentiment by source country/region
- Narrative themes detected
- Media coverage disparities

Use GDELT MCP tools: gdelt_gkg, gdelt_doc
Return quantified sentiment analysis.",
  description: "Sentiment analysis: [topic]"
)

Task(
  subagent_type: "deep-research:geo:trend-analyst",
  prompt: "Analyze coverage trends for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Coverage volume timeline
- Key inflection points
- Historical pattern comparison
- Early warning indicators

Use GDELT MCP tools: gdelt_trends, gdelt_events
Return trend analysis with forecasting.",
  description: "Trend analysis: [topic]"
)
```

## Gap Detector

**Agent:** `deep-research:geo:gap-detector-geo`

**Dimensions:**

### Core (3x weight)
- **Temporal Coverage**: Historical context, current status, future trajectory
- **Actor Completeness**: All major stakeholders (state, non-state, IGO, civil society)
- **Data Source Diversity**: Events data, GKG data, news articles, quantitative data

### Supporting (2x weight)
- **Quantification**: Numerical claims backed by specific data
- **Geographic Coverage**: All affected regions, cross-border effects
- **Perspective Balance**: Multiple viewpoints, not just dominant narrative

### Contextual (1x weight)
- **Historical Precedents**: Relevant parallels and lessons
- **Expert Sources**: Think tank analysis, academic research, official sources
- **Timeline Coherence**: Logical sequence, clear cause-effect

**Coverage Threshold:** 70%

**Critical Flags:**
- Major actor/stakeholder perspective completely missing
- Quantitative claims made without data sources
- Significant contradictions remain unresolved
- Critical temporal dimension missing

## Tools

### GDELT MCP Tools (Primary)
| Tool | Purpose | Key Use Cases |
|------|---------|---------------|
| `gdelt_events` | CAMEO-coded event queries | Conflict tracking, bilateral events, Goldstein scale analysis |
| `gdelt_gkg` | Global Knowledge Graph | Entity extraction, theme analysis, tone data |
| `gdelt_actors` | Actor relationship mapping | Bilateral relationships, actor profiles |
| `gdelt_trends` | Coverage trends over time | Volume tracking, tone trajectories |
| `gdelt_doc` | Full-text article search | Qualitative sources, specific article retrieval |
| `gdelt_cameo_lookup` | CAMEO code meanings | Decode event types, explain Goldstein scores |

### Supplemental Tools
- `WebSearch` - For sources not in GDELT
- `WebFetch` - Deep content from official/expert sources

## Output Sections

### Conflict Analysis Report

```markdown
# Geopolitical Research Report: [Title]

**Analysis Type:** Conflict Analysis
**Date:** [Timestamp]
**Coverage Score:** [X%]
**Confidence Level:** [High/Medium/Low]

---

## Executive Summary

[3-5 bullet points of key findings]

---

## Conflict Overview

### Active Conflicts

| Conflict | CAMEO Codes | Avg Goldstein | Trend | Intensity |
|----------|-------------|---------------|-------|-----------|
| [Name] | [Codes] | [Score] | [Direction] | [Level] |

### Key Actors

**Belligerents:**
[Actor profiles with CAMEO codes and recent actions]

**Third-Party Actors:**
[Mediators, suppliers, allies with their roles]

---

## Escalation/De-escalation Assessment

**Indicators Observed:**
- [Indicator 1]: [Status]
- [Indicator 2]: [Status]

**Current Trajectory:** [Assessment]

---

## Key Events Timeline

| Date | Event | Actors | CAMEO | Goldstein | Source |
|------|-------|--------|-------|-----------|--------|
| [Date] | [Description] | [Actors] | [Code] | [Score] | [Source] |

---

## Quantitative Metrics

**GDELT Event Statistics:**
- Total events analyzed: [N]
- Date range: [Range]
- Goldstein scale distribution: [Stats]
- Quad class breakdown: [Stats]

---

## Analysis and Implications

[Cross-cutting insights, patterns, risks]

---

## Confidence Assessment

- **Data Quality:** [Assessment]
- **Coverage Completeness:** [Assessment]
- **Analytical Confidence:** [Assessment]

---

## Sources

**GDELT Queries:**
1. [Query description and parameters]

**News/Expert Sources:**
1. [Title](URL) - [What it contributed]

---
*Research conducted using GDELT geopolitical analysis with [N] specialist agents over [M] iterations.*
```

### Sanctions Research Report

Use similar structure with sections for:
- Active Sanctions Regimes (table)
- Recent Designations/Removals
- Economic Impact Indicators (with data)
- Enforcement Actions
- Evasion Patterns Detected

### Actor Analysis Report

Use similar structure with sections for:
- Actor Profiles (table)
- Relationship Matrix (with Goldstein scores)
- Network Visualization Data
- Relationship Trends
- Power Dynamics Analysis

### Narrative Analysis Report

Use similar structure with sections for:
- Sentiment by Region/Source (table)
- Sentiment Timeline
- Narrative Themes Detected
- Coverage Disparities
- Trend Forecast

## Workflows

- `geopolitical/conflict-analysis.md` - Deep conflict analysis pattern
- `geopolitical/sanctions-research.md` - Sanctions regime investigation
- `geopolitical/narrative-analysis.md` - Media sentiment tracking

## GDELT Quick Reference

### CAMEO Conflict Codes (14-20)
- **14**: Protest - Demonstrations, strikes, boycotts
- **15**: Exhibit Force - Mobilize forces, show of force
- **16**: Reduce Relations - Reduce diplomatic relations, suspend aid
- **17**: Coerce - Threats, demands, ultimatums
- **18**: Assault - Physical attacks, abductions, property destruction
- **19**: Fight - Armed clashes, combat, skirmishes
- **20**: Mass Violence - Mass killings, ethnic cleansing, genocide

### Goldstein Scale
- **-10 to -5**: Highly conflictual (military attacks, mass violence)
- **-5 to -2**: Moderately conflictual (threats, sanctions, protests)
- **-2 to 0**: Mildly conflictual (verbal disputes, criticism)
- **0 to +2**: Neutral to mildly cooperative
- **+2 to +5**: Moderately cooperative (agreements, aid)
- **+5 to +10**: Highly cooperative (alliances, peace treaties)

### Quad Classes
- **1**: Verbal Cooperation
- **2**: Material Cooperation
- **3**: Verbal Conflict
- **4**: Material Conflict
