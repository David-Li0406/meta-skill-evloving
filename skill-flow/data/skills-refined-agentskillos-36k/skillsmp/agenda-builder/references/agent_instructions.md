# Federal Engagement Orchestrator - Agent Instructions

*Complete behavioral guidelines for processing transcripts and managing engagement lifecycle*

## Core Operating Principles

### 1. Multi-Phase System
This skill handles **four distinct phases**:
- **Planning**: Process planning call → Generate agenda + tasks
- **Closeout**: Process engagement → Extract closeout data → Fill CEHub
- **Learning**: Query knowledge graph → Provide insights and patterns
- **Prospecting**: Generate sample agendas → Ground on successful patterns

### 2. Iterative Review (Planning & Closeout)
**NEVER auto-generate**. Always:
1. **Analyze** → Extract information
2. **Preview** → Show what was found
3. **Confirm** → User validates
4. **Refine** → Update based on feedback
5. **Generate** → Create files after approval

### 3. Knowledge Graph Integration
**ALWAYS store AND query**:
- Store every engagement in knowledge graph
- Query past engagements for grounding
- Learn patterns over time
- Provide data-driven recommendations

---

## Phase 1: Planning Call Processing

### Input Recognition
Trigger phrases:
- "Process planning call"
- "Generate agenda for [customer]"
- "Planning transcript for [customer]"

### Extraction Requirements

**Customer/Agency Name** (CRITICAL RULE):
- MUST be external organization
- NEVER "Microsoft", "Microsoft Innovation Hub", or internal names
- Examples: ✅ "ATF BATS" ❌ "Microsoft"

**Engagement Date**:
- Extract from transcript if mentioned
- Parse formats: "January 15", "01/15/2026", "next Friday"
- Convert to YYYY-MM-DD
- If not in transcript, ask user

**Engagement Type**:
- Discovery: "discovery", "initial", "kickoff"
- Architecture Review: "architecture", "technical", "design"
- POC: "poc", "proof of concept", "pilot"
- Executive Briefing: "executive", "leadership", "briefing"
- Deep Dive: "deep dive", "detailed", "technical session"

**Topics**:
- Extract from lists, time allocations, discussions
- Capture specific technologies, frameworks, requirements
- Use exact terminology from transcript

**Attendees**:
- Microsoft team members
- Customer team members
- Roles and titles

### Knowledge Graph Query (NEW!)

Before generating agenda, ALWAYS query knowledge graph:

```
1. Search for similar past engagements:
   - Same customer (if exists)
   - Same industry/agency type
   - Same engagement type
   - High success scores (>7)

2. Extract patterns:
   - What topics worked well?
   - What was the typical structure?
   - How long did topics take?
   - What challenges occurred?

3. Ground new agenda on these patterns
```

**Example**:
```
User: "Process FBI discovery planning call"

Claude internal process:
1. Extract: Customer=FBI, Type=Discovery
2. Query knowledge graph:
   - Find similar: DEA, ATF (law enforcement)
   - Find Discovery engagements with success>7
3. Extract patterns:
   - Compliance discussed early (100%)
   - Customer-led discovery works (85%)
   - Concrete demos early build credibility
4. Generate agenda incorporating these patterns
5. Show user what patterns were used
```

### Preview Generation

Show plain text preview including:

```
CUSTOMER: [Extracted name]
DATE: [Extracted or "Please provide"]
TYPE: [Engagement type]

🔍 GROUNDED ON PAST ENGAGEMENTS:
- [Similar engagement 1] (success: X)
- [Similar engagement 2] (success: Y)

COMMON SUCCESS PATTERNS FOUND:
- [Pattern 1]
- [Pattern 2]

PROPOSED AGENDA:
[Detailed agenda following patterns]

TASKS TIMELINE:
[All 15 tasks with calculated business day dates]

---
Confirm or correct?
```

### Agenda Generation Rules

**Sequence**:
1. Intro/Goals (15 min)
2. Discovery (60-90 min)
3. Custom topics (variable)
4. Lunch (1 hr for full-day)
5. More topics
6. Next Steps (20-30 min)

**Descriptions**:
- Standard items: Use consistent patterns with ASCII-safe punctuation
- Custom topics: Highly detailed with transcript terminology
- Include success factors from knowledge graph
- Use 'and' not '&', hyphens not em-dashes

**Owner Field Rules**:
- Microsoft-only sessions: `"Microsoft"`
- Collaborative sessions: `"All"` or `"Microsoft and [ActualCustomerName]"` (use real customer name)
- NEVER use generic "Customer" or "Microsoft & Customer"

**Quality Checks**:
✓ Customer = external org (NOT "Microsoft")
✓ Date extracted from transcript
✓ Title specific and transcript-driven
✓ Agenda sequence correct
✓ Descriptions detailed
✓ Business day calculations correct
✓ Patterns from knowledge graph applied

### Knowledge Graph Storage

After user confirms agenda, store:

```python
# Store/update customer
create_entity(
    type="Customer",
    name=customer_name,
    properties={
        "industry": industry,
        "agency_type": agency_type,
        "solution_areas": solution_areas,
        "hub_priorities": hub_priorities
    }
)

# Store engagement (planning phase)
create_entity(
    type="Engagement",
    name=f"{customer_name} - {date}",
    properties={
        "engagement_type": engagement_type,
        "date": date,
        "duration": duration,
        "topics_planned": topics,
        "status": "planned"
    }
)

# Link engagement to customer
create_relation(
    from_entity=engagement,
    to_entity=customer,
    relation_type="conducted_for"
)

# Store each topic
for topic in topics:
    # Create or update topic entity
    # Link to engagement
```

---

## Phase 2: Engagement Closeout Processing

### Input Recognition
Trigger phrases:
- "Process closeout"
- "Process engagement transcript"
- "Fill CEHub for [customer]"
- "Generate closeout for [engagement]"

### Extraction from Engagement Transcript

Extract these fields for CEHub:

**Basic Info** (from planning data if available):
- Customer name
- Engagement title
- Date of session (MM/DD/YYYY HH:MM:SS)
- Lead architect (default: "Brendon Colburn")
- Solution areas
- Industry
- Hub motion priorities

**Debrief Section** (analyze transcript):
- **Industry Insights**: New insights about industry/agency
  - Look for: Emerging trends, customer statements about their industry
  - If none: "No major new insights uncovered"

- **What Worked Well**: Success factors from the engagement
  - Look for: Positive reactions, demos that landed, approaches that worked
  - Include: Prep quality, execution highlights, customer engagement
  - Be specific: "Live demo of [X] with customer's actual data"

- **What Didn't Work**: Challenges and learnings
  - Look for: Technical issues, timing problems, missing prerequisites
  - Include: How it could be improved
  - If nothing major: "Minor timing adjustments needed"

**Outcomes Section**:
- **New Opportunities**: New projects/opportunities discovered
  - Look for: Adjacent use cases, expanded scope, new initiatives
  - Be specific about the opportunity

- **Customer Journey**: Next engagements agreed upon
  - Options: POC, Architecture Review, Production, Training, Other
  - Specify which one

- **Next Steps Guidance**: Specific next steps and timeframe
  - Action items with owners
  - Timeline for next engagement
  - Dependencies and prerequisites

- **Outcomes**: What was delivered
  - Use cases defined
  - Architecture documented
  - Code/configuration delivered
  - Next steps confirmed

### Closeout Preview

```
📊 CEHUB CLOSEOUT PREVIEW
═════════════════════════════════════════

ENGAGEMENT:
  Customer: [name]
  Title: [title]
  Date: [date]
  Architect: [name]

DEBRIEF:
  Industry Insights:
    [extracted]
  
  What Worked Well:
    [extracted]
  
  What Didn't Work:
    [extracted]

OUTCOMES:
  New Opportunities:
    [extracted]
  
  Customer Journey:
    [extracted]
  
  Next Steps:
    [extracted]
  
  Outcomes:
    [extracted]

═════════════════════════════════════════
Confirm? Or provide corrections?
```

### CEHub Form Filling

Two modes:

**Mode A: With Playwright MCP** (if configured):
```
User: "Fill CEHub form"

Claude:
1. Verify MCP is available
2. User navigates to form manually
3. Use fill_closeout_form tool with extracted data
4. Use field mapping from assets
5. Take screenshot for verification
6. Confirm completion
```

**Mode B: Copy/Paste Format** (if MCP not configured):
```
Claude:
Generate text in exact CEHub email format:

Microsoft Innovation Hub
Engagement Closeout

Customer: [name]
Engagement Title: [title]
...
[all fields]

User can copy/paste into CEHub manually
```

### Knowledge Graph Update

After closeout processing:

```python
# Update engagement with outcomes
add_observations(
    entity=engagement,
    observations=[
        f"Status: completed",
        f"What worked well: {what_worked_well}",
        f"What didn't work: {what_didnt_work}",
        f"New opportunities: {new_opportunities}",
        f"Success indicators: {derived_from_outcomes}"
    ]
)

# Calculate success score (1-10) based on:
# - New opportunities generated
# - Positive outcomes
# - Customer engagement level
# - Next steps clarity
success_score = calculate_success_score(closeout_data)

add_observations(
    entity=engagement,
    observations=[f"Success score: {success_score}"]
)

# Update topic effectiveness
for topic in topics_covered:
    add_observations(
        entity=topic,
        observations=[
            f"Used in {customer_name} ({industry}) - {engagement_type}",
            f"Effectiveness: {rating_from_what_worked}",
            f"Duration: {actual_duration}"
        ]
    )

# Identify patterns
if success_score >= 8:
    # This was a successful engagement
    # Extract what made it successful for pattern recognition
    create_entity(
        type="Pattern",
        name=f"Success pattern: {engagement_type} with {industry}",
        properties={
            "context": f"{industry}, {engagement_type}",
            "key_factors": extract_success_factors(closeout_data),
            "example_engagement": engagement_name
        }
    )
```

---

## Phase 3: Learning Loop Queries

### Query Types

**Type 1: What works with [customer type]?**
```
User: "What topics work well with DoD customers?"

Claude process:
1. Search knowledge graph:
   - Find engagements where industry="Government" AND agency_type="DoD"
   - Filter by success_score > 7
2. Extract topics from successful engagements
3. Calculate:
   - Inclusion rate (% of engagements that used it)
   - Average duration
   - Effectiveness rating
4. Identify anti-patterns (what didn't work)
5. Provide data-driven recommendations
```

**Type 2: Ground new agenda on past success**
```
User: "Generate agenda for [Customer] [Type]"

Claude process:
1. Find similar successful engagements:
   - Same/similar customer if exists
   - Same industry/agency type
   - Same engagement type
   - success_score > 7
2. Extract common patterns:
   - Agenda structure
   - Topic sequence
   - Duration allocations
   - What worked well
3. Generate new agenda incorporating patterns
4. Explain what patterns were used
```

**Type 3: Why did [engagement] succeed/fail?**
```
User: "What made the ATF BATS engagement successful?"

Claude process:
1. Retrieve engagement from knowledge graph
2. Show:
   - Success score and why
   - What worked well
   - Topics that were effective
   - Customer engagement indicators
3. Compare to similar engagements
4. Extract transferable lessons
```

**Type 4: Identify patterns**
```
User: "What makes architecture reviews successful?"

Claude process:
1. Find all engagements where type="Architecture Review"
2. Group by success_score (high vs low)
3. Compare and contrast:
   - Topics covered
   - Duration
   - Preparation factors
   - Attendee types
   - Follow-up actions
4. Extract patterns that correlate with success
5. Provide actionable recommendations
```

### Response Format for Insights

```
🧠 KNOWLEDGE GRAPH INSIGHTS
═══════════════════════════════════════

ANALYZED: [X] engagements matching criteria

HIGH SUCCESS FACTORS:
✓ [Factor 1] (appears in X% of successful engagements)
  Details: [specific information]
  Effectiveness: [rating]

✓ [Factor 2]
  ...

ANTI-PATTERNS (what to avoid):
✗ [Anti-pattern 1] (correlates with low success)
  Impact: [description]

✗ [Anti-pattern 2]
  ...

RECOMMENDATIONS:
Based on this analysis:
1. [Recommendation 1]
2. [Recommendation 2]

CONFIDENCE: [High/Medium/Low based on data volume]
Based on [X] engagements with avg success score [Y]
```

---

## Phase 4: Prospecting Agenda Generation

### Input Recognition
```
- "Generate sample agenda for [Customer]"
- "Create prospecting agenda"
- "What would a good [Type] agenda look like for [Industry]?"
```

### Generation Process

```
1. Identify customer type/industry from request
2. Query knowledge graph for:
   - Successful engagements with similar customers
   - Topics that generated new opportunities
   - Engagement structures that worked well
3. Synthesize patterns into prospecting agenda
4. Focus on:
   - Compelling value proposition
   - Proven successful topics
   - Clear path to pilot/POC
   - Addresses known pain points
5. Explain what patterns were used
```

### Prospecting Agenda Format

```
[CUSTOMER TYPE] [ENGAGEMENT TYPE]
Prospecting Agenda

🎯 OBJECTIVE: [Clear value proposition based on patterns]

⏰ PROPOSED DURATION: [Based on similar successful engagements]

📋 AGENDA:

1. [Time] | [Topic]
   [Description with focus on customer value]
   💡 Based on: [Pattern from past engagement]

2. [Time] | [Topic]
   [Description]
   💡 Based on: [Pattern]

...

🔑 SUCCESS FACTORS (from past engagements):
- [Factor 1] (from [X] successful engagements)
- [Factor 2]
- [Factor 3]

📊 THIS STRUCTURE:
- Used in [X] successful engagements
- Average success score: [Y]
- Led to new opportunities in [Z%] of cases

🎯 RECOMMENDED NEXT STEPS:
[Clear path to pilot/POC based on patterns]
```

---

## Business Day Calculations (All Phases)

### Task Template
```
T-28: Schedule Internal Precall
T-22: Research customer
T-21: Execute Internal Precall
T-20: Draft Agenda
T-20: Schedule Customer Precall
T-14: Execute Customer Precall
T-14: Schedule internal resources
T-10: Validate Agenda with ATU
T-7: Validate Agenda with Customer
T-7: Prep Demos
T-3: Confirm all Customer pre-work
T-0: Send Satisfaction Survey
T+2: Conduct MSFT Debrief
T+2: Share Engagement Materials
T+3: Complete Engagement Close out form
```

### Calculation Rules
- **Excludes weekends** (Saturday/Sunday)
- **T-28 = 28 business days BEFORE** engagement
- **T+2 = 2 business days AFTER** engagement
- Count forward/backward skipping weekends

### CSV Format for Planner
```csv
Task Name,Assignment,Start date,Due date,Bucket,Progress,Priority,Labels
[Customer] - [Task],Brendon Colburn,MM/DD/YYYY,MM/DD/YYYY,[Date] - [Customer],Not started,Medium,Add label
```

---

## Critical Rules Summary

### Planning Phase
✓ Customer = external org (NEVER "Microsoft")
✓ Date extracted from transcript
✓ Query knowledge graph for patterns
✓ Ground agenda on successful past engagements
✓ Show preview before generation
✓ Store in knowledge graph after confirmation

### Closeout Phase
✓ Extract all CEHub fields from transcript
✓ Be specific in "what worked well"
✓ Honest in "what didn't work"
✓ Calculate success score
✓ Update knowledge graph with outcomes
✓ Identify patterns for future learning

### Learning Phase
✓ Query knowledge graph for data-driven insights
✓ Provide confidence levels based on data volume
✓ Extract actionable recommendations
✓ Compare successful vs unsuccessful patterns
✓ Show specific examples

### Prospecting Phase
✓ Ground on successful engagements only
✓ Focus on topics that generated opportunities
✓ Clear value proposition
✓ Path to pilot/POC
✓ Explain what patterns were used

---

## File Management

### Planning Outputs
```
/engagements/[CUSTOMER]-[DATE]/
  ├── planning_transcript.docx
  ├── agenda.docx
  ├── tasks.csv
  └── engagement_summary.json
```

### Closeout Outputs
```
/engagements/[CUSTOMER]-[DATE]/
  ├── engagement_transcript.docx
  ├── closeout_data.json
  ├── closeout_email.txt
  └── cehub_screenshot.png (if MCP used)
```

---

## Success Metrics to Track

### Engagement Quality
- Success scores over time
- New opportunities per engagement
- Pattern adherence rate

### Efficiency
- Time to agenda generation
- Time to closeout completion
- Knowledge graph query speed

### Learning
- Pattern accuracy
- Recommendation adoption rate
- Prospecting conversion rate

---

## Continuous Improvement

System gets smarter with each engagement:
- More patterns identified
- Better recommendations
- Higher success prediction accuracy
- Personalized insights

After 10 engagements: Basic patterns
After 25 engagements: Strong pattern recognition
After 50+ engagements: Predictive insights
