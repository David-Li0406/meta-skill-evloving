# Conflict Analysis Workflow

For analyzing armed conflicts, security situations, and inter-state tensions using GDELT event data.

<when_to_use>
- User asks about ongoing conflicts, wars, or military operations
- Questions about tensions between specific countries or actors
- Requests to track escalation or de-escalation patterns
- Analysis of belligerents, allies, or mediators in a conflict
- Keywords: "conflict", "war", "military", "escalation", "ceasefire", "troops", "attack"
</when_to_use>

<agents>
- **conflict-analyst**: Primary analyst for conflict event interpretation
- **actor-mapper**: Maps relationships between conflict actors (belligerents, allies, mediators, proxies)
</agents>

<data_sources>
- **gdelt_events**: Primary source for conflict events
  - CAMEO codes 14-20 (protest, force, coercion, assault, fight, mass violence, unconventional mass violence)
  - Goldstein scale for intensity measurement (-10 to +10)
  - Actor1/Actor2 for participant identification
- **gdelt_gkg**: Supplementary themes and entity extraction
  - Themes: CONFLICT, MILITARY, TERROR, REBELLION
  - Persons/Organizations involved
</data_sources>

<research_phases>

## Phase 1: Event Collection
Spawn conflict-analyst to query gdelt_events:
```
Query gdelt_events for:
- Geographic focus: [REGION/COUNTRY]
- Date range: [TIMEFRAME]
- CAMEO root codes: 14, 15, 16, 17, 18, 19, 20
- Return: EventCode, Actor1Name, Actor2Name, GoldsteinScale, NumMentions, SourceURL
- Sort by: NumMentions DESC, GoldsteinScale ASC
```

## Phase 2: Actor Mapping
Spawn actor-mapper to analyze relationships:
```
From Phase 1 events, extract:
- Primary belligerents (most frequent Actor1/Actor2 pairs in hostile events)
- Allies (actors appearing together against common opponent)
- Mediators (actors appearing in CAMEO 04-06 events with belligerents)
- Proxies (non-state actors affiliated with state actors)

Build relationship graph with:
- Edge type: hostile/allied/neutral/mediating
- Edge weight: event frequency
```

## Phase 3: Escalation Analysis
Analyze Goldstein scale trends:
```
For each week/day in timeframe:
- Calculate average Goldstein score
- Count events by intensity tier:
  - Verbal hostility: -5 to -1
  - Material conflict: -7 to -5
  - High intensity: -10 to -7
- Identify inflection points (>20% change in weekly average)
```

## Phase 4: Narrative Context
Query gdelt_gkg for context:
```
Extract for key actors and events:
- Themes associated with conflict
- Tone analysis of coverage
- Geographic spread of reporting
```

</research_phases>

<gap_detection>
Flag for additional research if:
- Actor relationships are ambiguous (appears in both hostile and allied events)
- Goldstein trend shows sudden reversals without explanation
- Key actors appear with <10 events (insufficient data)
- Mediator activity detected but ceasefire negotiations not covered
- Proxy relationships implied but not confirmed by event patterns
- Time gaps >7 days in event coverage for active conflict
</gap_detection>

<output_format>
```markdown
# Conflict Assessment: [CONFLICT NAME]

**Analysis Period:** [START_DATE] to [END_DATE]
**Status:** [Active/Frozen/De-escalating/Escalating]
**Intensity Level:** [Low/Medium/High/Critical]

## Executive Summary
[2-3 sentence overview of conflict state and trajectory]

## Actor Map

### Belligerents
| Actor | Role | Event Count | Key Actions |
|-------|------|-------------|-------------|
| [Actor1] | Primary | [N] | [Summary] |

### Allied Actors
| Actor | Aligned With | Relationship Type |
|-------|--------------|-------------------|

### Mediators/Third Parties
| Actor | Role | Engagement Level |
|-------|------|------------------|

## Timeline & Escalation

### Goldstein Scale Trend
[Weekly/daily trend visualization description]
- Peak hostility: [DATE] (score: [N])
- Recent trend: [Rising/Stable/Falling]

### Key Inflection Points
1. [DATE]: [Event description] - [Impact on trajectory]

## Event Breakdown

### By Category (CAMEO)
| Code | Description | Count | % of Total |
|------|-------------|-------|------------|
| 19 | Fight | [N] | [%] |

### By Actor Pair
| Actor1 | Actor2 | Events | Avg Goldstein |
|--------|--------|--------|---------------|

## Escalation Indicators
- [ ] Military buildup detected
- [ ] Rhetoric intensification
- [ ] Third-party involvement changes
- [ ] Geographic spread of conflict

## Gaps & Uncertainties
- [List of data gaps or analytical uncertainties]

## Sources
- [Key sources with URLs]
```
</output_format>

<invocation>
```
Task(
  subagent_type: "deep-research:geo:conflict-analyst",
  prompt: "Analyze conflict: [CONFLICT/REGION]

  Timeframe: [DATE_RANGE]
  Focus actors: [OPTIONAL_ACTOR_LIST]

  Follow conflict-analysis workflow phases.
  Query gdelt_events for CAMEO 14-20 events.
  Map actor relationships.
  Track Goldstein scale trends.

  Output format: Conflict assessment with actor map and escalation analysis.",
  description: "Conflict analysis: [topic]"
)
```
</invocation>
