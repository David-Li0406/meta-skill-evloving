# Narrative Analysis Workflow

For analyzing media narratives, sentiment patterns, and coverage disparities across different source countries and outlets.

<when_to_use>
- User asks about media coverage or framing of events
- Questions about bias or perspective differences between countries
- Tracking sentiment trends around topics, entities, or events
- Analysis of propaganda, information warfare, or narrative competition
- Keywords: "coverage", "narrative", "sentiment", "framing", "bias", "propaganda", "media", "perception"
</when_to_use>

<agents>
- **sentiment-tracker**: Monitors tone and sentiment patterns across sources
- **trend-analyst**: Analyzes coverage volume, evolution, and comparative patterns
</agents>

<data_sources>
- **gdelt_gkg**: Primary source for tone and theme analysis
  - Tone: Document-level sentiment scores
  - Themes: Topic categorization
  - Source metadata: Country, domain
  - Entities: Persons, organizations, locations mentioned
- **gdelt_trends**: Coverage evolution tracking
  - Volume trends over time
  - Theme emergence and decay
  - Geographic spread of coverage
</data_sources>

<research_phases>

## Phase 1: Coverage Baseline
Spawn sentiment-tracker to establish baseline:
```
Query gdelt_gkg for:
- Topic: [SUBJECT]
- Date range: [TIMEFRAME]
- Extract:
  - Article count by source country
  - Average tone by source country
  - Tone distribution (positive/neutral/negative)
  - Top themes co-occurring with topic
```

## Phase 2: Sentiment Trend Analysis
Track sentiment evolution:
```
Query gdelt_gkg time series:
- Topic: [SUBJECT]
- Aggregate by: Day/Week
- Metrics:
  - Average tone
  - Tone variance
  - Volume
- Segment by: Source country/region

Identify:
- Sentiment inflection points
- Divergence between source countries
- Correlation with events
```

## Phase 3: Comparative Coverage Analysis
Spawn trend-analyst for cross-source comparison:
```
Compare coverage across source regions:
- Regions: [List - e.g., US, EU, Russia, China, Middle East]
- Metrics per region:
  - Volume (article count)
  - Tone (average, range)
  - Theme emphasis (which themes dominate)
  - Entity framing (how key actors are described)

Calculate:
- Coverage disparity index (volume differences)
- Sentiment gap (tone differences between regions)
- Frame divergence (theme emphasis differences)
```

## Phase 4: Narrative Mapping
Identify distinct narratives:
```
Cluster articles by:
- Dominant themes
- Tone profile
- Source region

For each cluster:
- Characterize narrative (1-2 sentences)
- Identify representative sources
- Map geographic distribution
- Track temporal evolution
```

## Phase 5: Event Correlation
Link narrative shifts to events:
```
Query gdelt_events for:
- Related events in timeframe
- Match to sentiment inflection points

For each inflection:
- Identify triggering event(s)
- Measure narrative impact (tone change magnitude)
- Track recovery/stabilization time
```

</research_phases>

<gap_detection>
Flag for additional research if:
- Source country coverage is highly imbalanced (>80% from one region)
- Tone scores show unusual uniformity (potential coordination)
- Key events show no corresponding sentiment shift (data gap)
- Narrative clusters overlap significantly (unclear framing distinctions)
- Major actor coverage is sparse (<20 articles for key entity)
- Time gaps in coverage >3 days for ongoing story
- Language/translation limitations affecting non-English sources
- Bot/automated content patterns detected
</gap_detection>

<output_format>
```markdown
# Narrative Analysis: [TOPIC]

**Analysis Period:** [START_DATE] to [END_DATE]
**Coverage Volume:** [N] articles from [N] source countries
**Dominant Sentiment:** [Positive/Neutral/Negative] (avg tone: [N])

## Executive Summary
[2-3 sentence overview of narrative landscape and key findings]

## Coverage Overview

### Volume by Source Region
| Region | Article Count | % of Total | Trend |
|--------|---------------|------------|-------|
| North America | [N] | [%] | [Up/Down/Stable] |
| Europe | [N] | [%] | [Trend] |
| Russia/CIS | [N] | [%] | [Trend] |
| China | [N] | [%] | [Trend] |
| Other | [N] | [%] | [Trend] |

### Theme Distribution
| Theme | Frequency | Primary Regions |
|-------|-----------|-----------------|

## Sentiment Analysis

### Overall Tone Trend
[Description of tone evolution over time]
- Starting tone: [N] on [DATE]
- Current tone: [N]
- Major shifts: [List with dates]

### Tone by Source Region
| Region | Avg Tone | Range | Characterization |
|--------|----------|-------|------------------|
| US | [N] | [min-max] | [Positive/Neutral/Negative] |
| Russia | [N] | [min-max] | [Characterization] |

### Sentiment Disparity
- Maximum tone gap: [N] between [Region A] and [Region B]
- Correlation coefficient: [N] (how aligned are regional sentiments)

## Narrative Clusters

### Narrative 1: [Name/Characterization]
- **Tone:** [Avg]
- **Primary sources:** [Regions/outlets]
- **Key themes:** [List]
- **Representative framing:** "[Example headline or frame]"
- **Volume trend:** [Rising/Falling/Stable]

### Narrative 2: [Name/Characterization]
[Same structure]

### Narrative 3: [Name/Characterization]
[Same structure]

## Entity Framing

### [Key Actor 1]
| Region | Tone | Dominant Frame | Example |
|--------|------|----------------|---------|

### [Key Actor 2]
[Same structure]

## Temporal Dynamics

### Inflection Points
| Date | Event | Tone Change | Recovery Time |
|------|-------|-------------|---------------|

### Coverage Lifecycle
- Emergence: [Date/trigger]
- Peak: [Date/level]
- Current phase: [Rising/Peak/Declining/Stable]

## Comparative Analysis

### Coverage Disparity Matrix
|  | US | EU | Russia | China |
|--|----|----|--------|-------|
| US | - | [similarity] | [similarity] | [similarity] |

### Key Divergences
1. [Topic/aspect]: [Region A] emphasizes [X], while [Region B] emphasizes [Y]

## Information Quality Indicators
- Source diversity: [High/Medium/Low]
- Bot/automation signals: [Detected/Not detected]
- Coordination patterns: [Observed/Not observed]

## Gaps & Limitations
- [Data gaps, coverage limitations, analytical caveats]

## Sources
- **High-tone sources:** [Examples]
- **Low-tone sources:** [Examples]
- **Balanced sources:** [Examples]
```
</output_format>

<invocation>
```
Task(
  subagent_type: "deep-research:geo:sentiment-tracker",
  prompt: "Analyze narratives around: [TOPIC]

  Timeframe: [DATE_RANGE]
  Focus regions: [OPTIONAL_REGION_LIST]
  Key actors: [OPTIONAL_ACTOR_LIST]

  Follow narrative-analysis workflow phases.
  Query gdelt_gkg for tone analysis.
  Query gdelt_trends for coverage evolution.
  Compare coverage across source countries.

  Output format: Narrative analysis with sentiment trends and coverage disparities.",
  description: "Narrative analysis: [topic]"
)

Task(
  subagent_type: "deep-research:geo:trend-analyst",
  prompt: "Analyze coverage trends for: [TOPIC]

  Timeframe: [DATE_RANGE]
  Compare regions: [REGION_LIST]

  Focus on:
  - Volume patterns
  - Theme emergence
  - Cross-regional comparison

  Coordinate with sentiment-tracker findings.",
  description: "Trend analysis: [topic]"
)
```
</invocation>
