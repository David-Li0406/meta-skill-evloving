# Knowledge Graph Integration Guide

## Overview

The Federal Engagement Orchestrator uses Claude's built-in knowledge graph (memory system) to create a **learning loop** that improves over time.

## Knowledge Graph Schema

### Entities

#### 1. Customer
```
- name (string): Customer/agency name
- industry (string): Government, Financial Services, etc.
- agency_type (string): Civilian, DoD, Intelligence, Contractor
- solution_areas (list): AI, Security, Cloud, etc.
- hub_priorities (list): Copilots, Differentiated AI, etc.
- relationship_strength (string): New, Engaged, Strategic
- notes (string): Important context about the customer
```

#### 2. Engagement
```
- customer (relation to Customer)
- date (string): YYYY-MM-DD
- engagement_type (string): Discovery, Architecture, POC, Executive, Deep Dive
- title (string): Engagement title
- duration (string): Half-day, Full-day, Multi-day
- topics_covered (list): List of topics discussed
- what_worked_well (string): Success factors
- what_didnt_work (string): Challenges and learnings
- new_opportunities (string): Opportunities discovered
- next_steps (string): Agreed upon next actions
- success_score (number): 1-10 derived from outcomes
- outcomes (string): Concrete outcomes achieved
```

#### 3. Topic
```
- title (string): Topic name
- description (string): Detailed description
- typical_duration (string): 30min, 45min, 1hr, etc.
- effectiveness (list): Which customer types it works well for
- prerequisites (list): What needs to be in place first
- related_technologies (list): Azure services, frameworks, etc.
- success_indicators (string): What makes this topic successful
```

#### 4. Pattern
```
- pattern_type (string): agenda_structure, topic_sequence, duration_allocation
- context (string): When this pattern applies
- description (string): What the pattern is
- success_rate (number): How often it leads to good outcomes
- examples (list): Engagement IDs that used this pattern
```

## Knowledge Graph Operations

### Storing Planning Data

After planning call processing:
```python
# Store customer if new
create_entity(
    type="Customer",
    name=customer_name,
    properties={
        "industry": industry,
        "agency_type": agency_type,
        "solution_areas": solution_areas
    }
)

# Store engagement
create_entity(
    type="Engagement",
    name=f"{customer_name} - {date}",
    properties={
        "engagement_type": engagement_type,
        "date": date,
        "topics_covered": topics,
        "duration": duration
    }
)

# Create relationship
create_relation(
    from_entity=engagement,
    to_entity=customer,
    relation_type="conducted_for"
)

# Store each topic discussed
for topic in topics:
    create_entity(
        type="Topic",
        name=topic.title,
        properties={
            "description": topic.description,
            "typical_duration": topic.duration
        }
    )
    
    create_relation(
        from_entity=engagement,
        to_entity=topic,
        relation_type="covered_topic"
    )
```

### Storing Closeout Data

After engagement completion:
```python
# Update engagement with outcomes
add_observations(
    entity=engagement,
    observations=[
        f"What worked well: {what_worked_well}",
        f"What didn't work: {what_didnt_work}",
        f"New opportunities: {new_opportunities}",
        f"Success score: {calculated_score}"
    ]
)

# Update topic effectiveness
for topic in topics_discussed:
    add_observations(
        entity=topic,
        observations=[
            f"Worked well for {customer_name} ({industry})",
            f"Duration was {actual_duration}",
            f"Effectiveness: {rating}"
        ]
    )
```

## Query Patterns for Learning

### 1. What works with specific customer types?

```
Query: "What topics work well with DoD customers?"

Knowledge Graph Search:
- Find all Engagements where customer.agency_type = "DoD"
- Filter by success_score > 7
- Extract topics_covered
- Rank by frequency and effectiveness
```

### 2. Ground new agendas on past successes

```
Query: "Generate agenda for FBI Discovery session"

Process:
1. Search for similar engagements:
   - customer.agency_type = "Law Enforcement" OR "Intelligence"
   - engagement_type = "Discovery"
   - success_score > 7

2. Extract common patterns:
   - Typical agenda structure
   - Topics that worked well
   - Duration allocations
   - Sequence of topics

3. Generate new agenda grounded on these patterns
```

### 3. Identify patterns across engagements

```
Query: "What makes architecture reviews successful?"

Process:
1. Find all Engagements where engagement_type = "Architecture Review"
2. Group by success_score (high vs low)
3. Compare:
   - Topics covered
   - Duration
   - Preparation (from what_worked_well)
   - Challenges (from what_didnt_work)
4. Extract patterns that correlate with success
```

### 4. Generate prospecting agendas

```
Query: "Create sample agenda for USAF to pitch AI capabilities"

Process:
1. Find engagements with:
   - customer.agency_type = "DoD"
   - solution_areas contains "AI"
   - new_opportunities generated (shows compelling pitch)

2. Extract:
   - Most compelling topics
   - Best sequence
   - Effective demonstrations
   - Success stories to reference

3. Generate prospecting agenda that follows proven patterns
```

## Usage in Claude Conversations

### Storing Data

```
You: "Store this engagement in the knowledge graph"

Claude: [After processing transcript]
✓ Stored Customer: ATF BATS (Government, Civilian Agency)
✓ Stored Engagement: ATF BATS Discovery - 2026-01-15
✓ Stored 5 Topics covered
✓ Created relationships
```

### Querying for Insights

```
You: "What topics should I include for a State Department discovery?"

Claude: [Queries knowledge graph]
Based on 3 past State Department engagements:
- Compliance & FedRAMP (100% inclusion, avg 45min, high effectiveness)
- Data Sovereignty (67% inclusion, avg 30min)
- Integration with existing systems (100% inclusion, avg 1hr)

Recommend including these as core topics.
```

### Grounding New Agendas

```
You: "Generate agenda for DHS Architecture Review"

Claude: [Searches similar engagements]
Found 2 similar successful engagements:
- CBP Architecture Review (success_score: 9)
- TSA Architecture Review (success_score: 8)

Common patterns:
- Start with security requirements (100% of successful engagements)
- Deep dive on integrations (avg 90min)
- Compliance walkthrough (avg 45min)

[Generates agenda following these patterns]
```

## Pattern Recognition Examples

### Pattern 1: Successful Discovery Structure

```
Pattern extracted from 10 high-scoring Discovery engagements:
1. Intro (15min)
2. Discovery (60-90min) - CRITICAL: Let customer talk first
3. Quick wins demo (30min) - Show something tangible early
4. Lunch (1hr)
5. Deep dive on 1-2 key challenges (90min)
6. Next steps (30min)

Success factors:
- Customer talks more than Microsoft in discovery phase
- Concrete demo early builds credibility
- Focus on 1-2 problems deeply vs 10 problems shallowly
```

### Pattern 2: Federal Agency Priorities

```
Pattern across all federal engagements:
- Security/Compliance ALWAYS comes up (100%)
- Cost considerations appear later (usually after seeing value)
- Integration with legacy systems is major concern (80%)
- Timeline pressures around fiscal year end (60%)

Recommendation: Front-load security/compliance discussion
```

### Pattern 3: What Doesn't Work

```
Anti-pattern from low-scoring engagements:
- Too many topics (>6 in half-day)
- Generic demos not tailored to customer
- Microsoft talking too much (>60% of discovery time)
- Skipping next steps/action items

These correlate with:
- Lower success_scores
- Fewer new_opportunities generated
- Vague next_steps
```

## Continuous Improvement

As more engagements are stored:

1. **Patterns become more accurate** - More data = better recommendations
2. **Customer-specific insights** - "FBI prefers X approach vs DEA prefers Y"
3. **Temporal patterns** - "Q4 engagements focus more on budget"
4. **Personal learnings** - "I'm most effective when I do X"

## Integration Points

### With Planning Processor
```
Input: Planning call transcript
Process: Extract metadata → Store in knowledge graph
Output: Agenda grounded on similar past engagements
```

### With Closeout Processor
```
Input: Engagement transcript
Process: Extract outcomes → Update knowledge graph
Output: Enhanced understanding of what works
```

### With Prospecting Generator
```
Input: "Generate sample agenda for [Customer Type]"
Process: Query patterns from knowledge graph
Output: Compelling agenda based on proven approaches
```

## Privacy & Data Management

- All data stored in your personal knowledge graph
- Not shared across Claude instances
- You can delete/modify entities anytime
- Can export for external analysis

## Future Enhancements

- **Sentiment analysis**: Track customer engagement during topics
- **Time prediction**: "This topic usually takes 45min with DoD"
- **Success prediction**: "This agenda structure has 85% success rate"
- **Automated insights**: Weekly summary of learnings
