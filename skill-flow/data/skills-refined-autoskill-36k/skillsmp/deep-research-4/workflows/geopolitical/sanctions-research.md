# Sanctions Research Workflow

For researching economic sanctions regimes, enforcement actions, and evasion patterns using GDELT news and knowledge graph data.

<when_to_use>
- User asks about sanctions on specific countries, entities, or individuals
- Questions about sanctions effectiveness or economic impact
- Research on sanctions enforcement or evasion
- Tracking new sanctions announcements or modifications
- Keywords: "sanctions", "embargo", "trade restrictions", "asset freeze", "export controls", "OFAC", "blacklist"
</when_to_use>

<agents>
- **sanctions-researcher**: Specialist in sanctions regimes, enforcement, and economic impact analysis
</agents>

<data_sources>
- **gdelt_gkg**: Primary source for sanctions themes and entities
  - Themes: ECON_SANCTIONS, TRADE_DISPUTE, ECON_TRADE, GOV_POLICY
  - Organizations: sanctioning bodies, target entities
  - Persons: sanctioned individuals, officials
  - Tone: sentiment around sanctions coverage
- **gdelt_doc**: News article analysis
  - Full-text search for sanctions announcements
  - Source country analysis for coverage bias
  - Temporal tracking of enforcement news
</data_sources>

<research_phases>

## Phase 1: Regime Identification
Query gdelt_gkg for sanctions landscape:
```
Query gdelt_gkg for:
- Target: [COUNTRY/ENTITY]
- Themes containing: SANCTION, EMBARGO, TRADE_RESTRICT
- Date range: [TIMEFRAME]
- Extract: Organizations, Persons, Locations, Tone
- Group by: Source country, Theme
```

## Phase 2: Announcement Tracking
Query gdelt_doc for sanctions news:
```
Search gdelt_doc for:
- Keywords: "sanctions" AND [TARGET]
- Filter by: official sources (gov domains, wire services)
- Extract:
  - Announcement dates
  - Sanctioning authority
  - Sanction type (asset freeze, trade ban, travel ban, sectoral)
  - Named targets
```

## Phase 3: Enforcement Analysis
Track enforcement patterns:
```
Query for enforcement-related coverage:
- Keywords: "sanctions violation", "enforcement", "penalty", "fine"
- AND [TARGET or SECTOR]
- Extract:
  - Enforcement actions
  - Penalties assessed
  - Entities involved
  - Enforcement agency
```

## Phase 4: Evasion Detection
Identify potential evasion patterns:
```
Query for evasion indicators:
- Keywords: "sanctions evasion", "circumvention", "front company", "shell company"
- OR: Trade anomalies with sanctioned entities
- Themes: CRIME_SMUGGLE, ECON_TRADE with sanctioned locations
- Extract:
  - Evasion methods reported
  - Third-party countries involved
  - Entities suspected of facilitation
```

## Phase 5: Economic Impact Assessment
Analyze coverage of sanctions effects:
```
Query gdelt_gkg for impact themes:
- Themes: ECON_* with [TARGET] location
- Tone analysis: Track sentiment over time
- Keywords: "economic impact", "currency", "inflation", "shortage"
- Extract:
  - Reported economic indicators
  - Sector-specific impacts
  - Humanitarian concerns
```

</research_phases>

<gap_detection>
Flag for additional research if:
- Sanctions type unclear (primary vs secondary, comprehensive vs targeted)
- Enforcement data sparse (<5 enforcement-related articles)
- Evasion patterns suggested but specific methods not identified
- Economic impact claims lack quantitative data
- Multiple sanctioning authorities with potentially conflicting regimes
- Recent policy changes not reflected in older analysis
- Key designations (SDN, SSI, Sectoral) not clearly mapped
</gap_detection>

<output_format>
```markdown
# Sanctions Regime Analysis: [TARGET]

**Analysis Period:** [START_DATE] to [END_DATE]
**Primary Sanctioning Authorities:** [List]
**Regime Type:** [Comprehensive/Targeted/Sectoral]

## Executive Summary
[2-3 sentence overview of sanctions regime and current status]

## Sanctions Landscape

### Active Programs
| Authority | Program Name | Type | Effective Date |
|-----------|--------------|------|----------------|
| US/OFAC | [Name] | [Type] | [Date] |
| EU | [Name] | [Type] | [Date] |

### Key Designations
| Entity/Person | Designation Type | Authority | Date |
|---------------|------------------|-----------|------|

## Timeline of Actions

### Recent Announcements
| Date | Authority | Action | Details |
|------|-----------|--------|---------|

### Coverage Volume Trend
[Description of news coverage volume over time]
- Peak coverage: [DATE] - [Event triggering coverage]
- Current coverage level: [High/Medium/Low]

## Enforcement

### Actions Taken
| Date | Agency | Target | Penalty | Violation Type |
|------|--------|--------|---------|----------------|

### Enforcement Patterns
- Primary enforcement focus: [Sector/Activity]
- Notable cases: [Summary]

## Evasion & Circumvention

### Reported Methods
1. [Method]: [Description and evidence]

### Third-Party Jurisdictions
| Country | Role | Evidence Level |
|---------|------|----------------|

## Economic Impact

### Macro Indicators Reported
| Indicator | Pre-Sanctions | Current | Source |
|-----------|---------------|---------|--------|

### Sector-Specific Effects
| Sector | Impact | Coverage Volume |
|--------|--------|-----------------|

### Humanitarian Considerations
- [Reported humanitarian impacts with sources]

## Coverage Analysis

### By Source Country
| Country | Article Count | Avg Tone | Dominant Frame |
|---------|---------------|----------|----------------|

### Sentiment Trend
- Overall tone: [Positive/Negative/Neutral]
- Trend: [Improving/Stable/Declining]

## Gaps & Uncertainties
- [Data gaps and analytical limitations]

## Key Sources
- Official: [Government/institutional sources]
- News: [Key media sources with URLs]
```
</output_format>

<invocation>
```
Task(
  subagent_type: "deep-research:geo:sanctions-researcher",
  prompt: "Research sanctions regime: [TARGET COUNTRY/ENTITY]

  Timeframe: [DATE_RANGE]
  Focus areas: [announcements/enforcement/evasion/impact]

  Follow sanctions-research workflow phases.
  Query gdelt_gkg for sanctions themes.
  Query gdelt_doc for sanctions news coverage.
  Track announcements, enforcement, and evasion patterns.

  Output format: Sanctions regime summary with economic impact analysis.",
  description: "Sanctions research: [target]"
)
```
</invocation>
