# Methodologies Detail Reference

**Full methodology content extracted from SKILL.md for reference purposes.**

---

## Table of Contents

1. [idea-generation](#idea-generation)
2. [paul-graham-questions](#paul-graham-questions)
3. [pain-point-research](#pain-point-research)
4. [niche-evaluation](#niche-evaluation)
5. [market-research-tam-sam-som](#market-research-tam-sam-som)
6. [trend-analysis](#trend-analysis)
7. [competitor-analysis](#competitor-analysis)
8. [competitive-intelligence](#competitive-intelligence)
9. [user-interviews](#user-interviews)
10. [jobs-to-be-done](#jobs-to-be-done)
11. [persona-building](#persona-building)
12. [problem-validation](#problem-validation)
13. [pain-point-mining](#pain-point-mining)
14. [niche-viability-scoring](#niche-viability-scoring)
15. [business-model-research](#business-model-research)
16. [value-proposition-design](#value-proposition-design)
17. [project-naming](#project-naming)
18. [domain-availability](#domain-availability)
19. [pricing-research](#pricing-research)
20. [customer-interview-framework](#customer-interview-framework)

---

## idea-generation

### Problem
Aspiring entrepreneurs struggle to find viable startup ideas that match their skills and interests.

### Framework

| P | Question | Exploration |
|---|----------|-------------|
| **Pain** | What frustrates you daily? | List 5 daily annoyances, rate severity 1-10 |
| **Passion** | What do you love doing? | Activities you'd do for free, hobbies |
| **Profession** | What's broken in your industry? | Insider knowledge of inefficiencies |
| **Process** | What workflow is inefficient? | Tasks taking 10x longer than needed |
| **Platform** | What can be improved on existing platform? | Missing integrations, poor UX |
| **People** | Who do you know with problems? | Friends, family, colleagues complaints |
| **Product** | What product do you wish existed? | Tools you'd pay for immediately |

**Scoring:**
- For each P, generate 3-5 ideas
- Score each: Market size (1-5) + Your fit (1-5) + Urgency (1-5)
- Top 3 scores proceed to validation

### Templates

**Ideation Worksheet:**
```markdown
## Pain Ideas
1. {idea} - Score: {X}/15 - Notes: {why interesting}
2. {idea} - Score: {X}/15

## Passion Ideas
1. {idea} - Score: {X}/15

## Profession Ideas
1. {idea} - Score: {X}/15
...

## Top 3 to Validate
1. {idea} from {P} - Total: {X}/15
2. {idea} from {P} - Total: {X}/15
3. {idea} from {P} - Total: {X}/15
```

### Examples

| P | Example Idea | Score |
|---|--------------|-------|
| Pain | Meeting scheduling across timezones | 12/15 |
| Passion | Teaching coding to kids | 9/15 |
| Profession | Medical billing automation | 14/15 |

### Agent
faion-research-agent (mode: ideas)

---

## paul-graham-questions

### Problem
Entrepreneurs miss obvious opportunities hiding in plain sight.

### Framework

**4 Questions:**
1. **What's tedious but necessary?**
   - Tasks everyone hates but must do
   - High frequency, low satisfaction

2. **What's surprisingly hard to do?**
   - Should be simple but isn't
   - Indicates market failure

3. **What do you find yourself building for yourself?**
   - Personal tools that could scale
   - Validates genuine need

4. **What would you pay for that doesn't exist?**
   - Identifies willingness to pay
   - Validates business model

**Exploration Process:**
1. Spend 30 min per question
2. Write stream-of-consciousness
3. Circle recurring themes
4. Cross-reference with daily activities

### Templates

**PG Questions Journal:**
```markdown
## Question 1: Tedious but Necessary
### List
- Expense reports
- Code reviews
- Meeting scheduling
- ...

### Themes
- Administrative overhead
- Communication friction

### Top Ideas
- Automated expense categorization
- AI code review assistant
```

### Examples

**Successful Companies from PG Questions:**
- Dropbox: "Sync files is tedious" -> Tedious but necessary
- Stripe: "Payments are hard" -> Surprisingly hard
- Notion: "I built my own wiki" -> Built for yourself

### Agent
faion-research-agent (mode: ideas)

---

## pain-point-research

### Problem
Entrepreneurs overlook problems they face daily because they've normalized them.

### Framework

**Mining Techniques:**

1. **Complaint Audit** (1 week)
   - Log every complaint you make
   - Note frequency and intensity
   - Categorize: work, personal, tools

2. **Workaround Inventory**
   - List all workarounds you've built
   - Spreadsheets, scripts, processes
   - Time spent maintaining them

3. **Tool Stack Analysis**
   - List all tools you use
   - Rate satisfaction 1-5
   - Identify gaps between tools

4. **Time Tracker**
   - Track where time goes for 3 days
   - Identify time sinks
   - Calculate cost of inefficiency

**Scoring:**
| Factor | Weight |
|--------|--------|
| Frequency | 30% |
| Intensity | 30% |
| Current solutions | 20% |
| Your ability to solve | 20% |

### Templates

**Pain Point Log:**
```markdown
| Date | Complaint | Category | Freq | Intensity | Notes |
|------|-----------|----------|------|-----------|-------|
| 01/18 | Can't find file | Tools | Daily | 7/10 | Slack + Drive + Email |
| 01/18 | Meeting ran over | Work | Weekly | 5/10 | No time boundaries |
```

### Examples

- "I can never find that one Slack message" -> Search tool idea
- "Updating all docs after API change" -> Auto-sync documentation
- "Switching between 10 tabs" -> Dashboard aggregator

### Agent
faion-research-agent (mode: ideas)

---

## niche-evaluation

### Problem
Too many ideas, no objective way to prioritize.

### Framework

**Scoring Dimensions:**

| Dimension | 1-2 | 3-4 | 5 |
|-----------|-----|-----|---|
| **Market Size** | <$10M | $10M-$100M | >$100M |
| **Competition** | Red ocean, 10+ | Moderate, 3-10 | Blue ocean, <3 |
| **Barriers** | High (capital, regulatory) | Medium | Low |
| **Monetization** | Unclear | Possible | Obvious |
| **Your Fit** | No relevant skills | Some skills | Perfect match |

**Process:**
1. Score each idea 1-5 on all dimensions
2. Weight dimensions (optional)
3. Calculate total (max 25)
4. Rank ideas

**Decision Thresholds:**
- 20-25: Strong proceed
- 15-19: Proceed with caution
- 10-14: Needs pivot
- <10: Pass

### Templates

**Scoring Matrix:**
```markdown
| Idea | Market | Competition | Barriers | Monetization | Fit | Total |
|------|--------|-------------|----------|--------------|-----|-------|
| A | 4 | 3 | 4 | 5 | 4 | 20 |
| B | 5 | 2 | 3 | 4 | 3 | 17 |
| C | 3 | 4 | 5 | 3 | 5 | 20 |
```

### Examples

**SaaS Idea Scored:**
- Market: $500M (5)
- Competition: 5 competitors (3)
- Barriers: Technical only (4)
- Monetization: SaaS model (5)
- Fit: Developer background (4)
- **Total: 21/25 -> Strong proceed**

### Agent
faion-research-agent (mode: niche)

---

## market-research-tam-sam-som

### Problem
Entrepreneurs can't quantify market opportunity or set realistic targets.

### Framework

**Definitions:**
- **TAM** (Total Addressable Market): Everyone who could buy
- **SAM** (Serviceable Addressable Market): Those you can reach
- **SOM** (Serviceable Obtainable Market): Realistic Year 1 target

**Calculation Methods:**

1. **Top-Down:**
   - Start with industry reports
   - Apply filters (geography, segment)
   - Risk: Often inflated

2. **Bottom-Up:**
   - Count potential customers
   - Multiply by price point
   - Risk: May miss segments

3. **Value Theory:**
   - Calculate value created
   - Apply capture rate (1-10%)
   - Most defensible

**SOM Reality Check:**
- Typical SOM = 1-5% of SAM in Year 1
- With unfair advantage: 5-10%
- With viral growth: 10-20%

### Templates

**Market Sizing:**
```markdown
## TAM
- Global market: $XX billion
- Growth: X% CAGR
- Source: {report name}

## SAM
- Geographic focus: {regions}
- Segment focus: {segments}
- SAM = $XX million

## SOM (Year 1)
- Target customers: X
- Average revenue: $Y
- SOM = $Z million
- % of SAM: X%

## Assumptions
1. {assumption 1}
2. {assumption 2}
```

### Examples

**HR SaaS:**
- TAM: $30B (global HR software)
- SAM: $500M (US SMB HR)
- SOM: $2M (500 customers x $4K)
- SOM % of SAM: 0.4%

### Agent
faion-research-agent (mode: market)

---

## trend-analysis

### Problem
Entrepreneurs miss timing opportunities or build for declining markets.

### Framework

**Trend Categories:**

| Category | Timeframe | Examples |
|----------|-----------|----------|
| Macro | 5-10 years | AI adoption, remote work |
| Industry | 2-5 years | No-code tools, creator economy |
| Micro | 6-24 months | Specific tech adoption |

**Analysis Framework:**

1. **Growth Drivers**
   - What accelerates this trend?
   - Technology, regulation, demographics

2. **Adoption Curve**
   - Where are we? (Innovators -> Early Adopters -> Majority)
   - Sweet spot: Early Majority

3. **Threats**
   - What could reverse this trend?
   - Competition, regulation, substitutes

4. **Timing Assessment**
   - Too early: Education cost too high
   - Just right: Market aware, solutions emerging
   - Too late: Established winners

### Templates

**Trend Analysis:**
```markdown
## Trend: {Name}

### Overview
- Stage: {Emerging | Growing | Mature | Declining}
- Growth rate: X% annually
- Market size: $X billion

### Drivers
1. {driver} - Impact: High/Medium/Low
2. {driver} - Impact: High/Medium/Low

### Threats
1. {threat} - Likelihood: High/Medium/Low
2. {threat} - Likelihood: High/Medium/Low

### Timing Assessment
- Current stage: Early Majority
- Window: 2-3 years
- Recommendation: {proceed/wait/pivot}
```

### Examples

**AI Coding Assistants (2026):**
- Stage: Early Majority
- Growth: 45% CAGR
- Window: Now optimal
- Threat: Large players (GitHub, OpenAI)

### Agent
faion-research-agent (mode: market)

---

## competitor-analysis

### Problem
Entrepreneurs underestimate competition or miss indirect competitors.

### Framework

**Competitor Types:**

| Type | Definition | Example |
|------|------------|---------|
| Direct | Same solution, same customer | Slack vs Teams |
| Indirect | Different solution, same problem | Slack vs Email |
| Substitute | Alternative approach entirely | Slack vs In-person |
| Potential | Could enter market | Apple into wearables |

**Mapping Process:**

1. **Identify all competitors** (aim for 15-20)
2. **Categorize by type**
3. **Assess each:**
   - Founded, funding, team size
   - Pricing model
   - Key features
   - Positioning

4. **Plot on matrix:**
   - X-axis: Price (low -> high)
   - Y-axis: Features (simple -> complex)

5. **Find whitespace**

### Templates

**Competitive Landscape:**
```markdown
## Direct Competitors

| Name | Founded | Funding | Pricing | Differentiator |
|------|---------|---------|---------|----------------|
| {name} | 2020 | $10M | $99/mo | Feature X |
| {name} | 2018 | $50M | $199/mo | Enterprise |

## Indirect Competitors

| Name | How they compete | Weakness |
|------|-----------------|----------|
| {name} | {explanation} | {gap} |

## Market Position Map

High Price
    |
    |     [Enterprise A]
    |                      [Our opportunity]
    |  [Competitor B]
    |
Low Price ---------------------- High Features

## Whitespace Identified
- {gap 1}: {description}
- {gap 2}: {description}
```

### Examples

**Project Management Tools:**
- Direct: Asana, Monday, ClickUp
- Indirect: Spreadsheets, Slack, Email
- Whitespace: AI-native PM for solopreneurs

### Agent
faion-research-agent (mode: competitors)

---

## competitive-intelligence

### Problem
Entrepreneurs don't know which features are missing in the market.

### Framework

**Analysis Process:**

1. **Feature Inventory**
   - List all features across top 5 competitors
   - Categorize: Core, Differentiator, Nice-to-have

2. **Feature Matrix**
   - Competitors as columns
   - Features as rows
   - Mark: Has (Y), Partial (P), Missing (N)

3. **Gap Identification**
   - Features no one has
   - Features only 1-2 have (opportunity)
   - Features everyone has (table stakes)

4. **Gap Validation**
   - Is this gap intentional (hard, unprofitable)?
   - Do customers want it? (check reviews)
   - Can we build it better?

### Templates

**Feature Matrix:**
```markdown
| Feature | Us | Comp A | Comp B | Comp C | Gap? |
|---------|-------|--------|--------|--------|------|
| Core 1 | Y | Y | Y | Y | No (table stakes) |
| Core 2 | Y | Y | P | Y | No |
| Diff 1 | Y | N | N | P | Yes - Opportunity |
| Diff 2 | P | Y | Y | N | Build out |
| Nice 1 | N | N | N | N | Validate demand |
```

**Gap Validation:**
```markdown
## Gap: {Feature Name}

### Evidence
- Reviews mentioning need: X
- Forum discussions: X links
- Search volume: X/month

### Why Competitors Don't Have It
- {reason}: Technical difficulty / Low priority / Not aware

### Our Advantage
- {why we can build it}

### Recommendation
- Pursue / Investigate / Skip
```

### Examples

**Email Marketing Tools Gap:**
- Gap: Native A/B testing for subject lines
- Evidence: 50+ feature requests in Mailchimp community
- Why missing: Requires ML infrastructure
- Our advantage: Have ML expertise

### Agent
faion-research-agent (mode: competitors)

---

## user-interviews

### Problem
Entrepreneurs build based on assumptions rather than validated user needs.

### Framework

**Interview Types:**

| Type | When | Goal | Questions |
|------|------|------|-----------|
| Problem | Early | Validate problem exists | Open-ended exploration |
| Solution | After problem validated | Test solution fit | Prototype feedback |
| Usability | With prototype | Test UX | Task-based |

**Interview Structure (45 min):**
1. Warm-up (5 min): Build rapport
2. Current state (10 min): How do they do it today?
3. Pain exploration (15 min): What's frustrating?
4. Solution probing (10 min): Would X help?
5. Wrap-up (5 min): Would they pay? Referrals?

**Golden Rules:**
- Talk less than 20% of the time
- Never pitch, only probe
- Ask about past behavior, not future intent
- Look for emotion (frustration, excitement)

**Sample Questions:**
- "Tell me about the last time you [problem]..."
- "What did you try? What happened?"
- "On a scale of 1-10, how frustrating is this?"
- "How much time/money does this cost you?"

### Templates

**Interview Script:**
```markdown
## Warm-up
"Thanks for joining. I'm researching [topic]. No sales pitch, just learning."

## Current State
"Walk me through how you currently [task]."
"What tools do you use?"
"How often do you do this?"

## Pain Exploration
"What's the most frustrating part?"
"Tell me about the last time it went wrong."
"What workarounds have you tried?"

## Solution Probing (show concept/prototype)
"Would something like this help?"
"What's missing?"
"Would you pay for this? How much?"

## Wrap-up
"Who else should I talk to?"
"Can I follow up in 2 weeks?"
```

### Examples

**Key Insights from 10 Interviews:**
- 8/10 mentioned same frustration
- Average time wasted: 3 hours/week
- Willingness to pay: $50-100/month
- Quote: "I would kill for this solution"

### Agent
faion-research-agent (mode: validate)

---

## jobs-to-be-done

### Problem
Features don't connect to real user motivations.

### Framework

**JTBD Statement:**
```
When I [situation/trigger],
I want to [motivation/action],
So I can [expected outcome/benefit].
```

**Job Dimensions:**

| Dimension | Question | Example |
|-----------|----------|---------|
| Functional | What task? | Send invoice |
| Emotional | How feel? | Confident, professional |
| Social | How perceived? | Reliable, organized |

**Job Mapping Process:**
1. Identify situation triggers
2. Map functional jobs
3. Uncover emotional jobs (harder)
4. Discover social jobs (hardest)
5. Prioritize by frequency + importance

**Hiring/Firing Framework:**
- Why do customers "hire" solutions?
- Why do they "fire" (abandon) solutions?
- What makes them switch?

### Templates

**JTBD Canvas:**
```markdown
## Job: {Name}

### Situation/Trigger
When I {situation}...

### Functional Job
I want to {action}...

### Emotional Job
So I can feel {emotion}...

### Social Job
And be seen as {perception}...

### Current Solutions
- {solution 1}: Hired because {reason}, fired because {reason}
- {solution 2}: Hired because {reason}, fired because {reason}

### Our Opportunity
We can {do X better} by {approach}
```

### Examples

**Invoicing Software JTBD:**
- Situation: When I finish a project for a client
- Functional: I want to send a professional invoice quickly
- Emotional: So I can feel confident I'll get paid
- Social: And be seen as a legitimate business

### Agent
faion-research-agent (mode: personas)

---

## persona-building

### Problem
Teams build for abstract "users" rather than specific people with distinct needs.

### Framework

**Persona Components:**

| Component | Description | Source |
|-----------|-------------|--------|
| Demographics | Age, role, income, location | Analytics, surveys |
| Behaviors | Tools used, habits, workflows | Interviews, observation |
| Pain Points | Top 3-5 frustrations | Interviews, support tickets |
| Goals | What success looks like | Interviews |
| Quote | Representative statement | Verbatim from interview |

**Persona Types:**

| Type | Priority | Focus |
|------|----------|-------|
| Primary | 1 | Design for this person |
| Secondary | 2 | Consider their needs |
| Negative | Exclude | Explicitly not for them |

**Creation Process:**
1. Conduct 5-10 user interviews
2. Identify patterns (cluster similar users)
3. Create 2-3 personas (not more)
4. Validate with team
5. Post visibly (always reference)

### Templates

**Persona Template:**
```markdown
# Persona: {Name} ({Type})

## Photo
[Stock photo representing this person]

## Demographics
- **Age:** 32
- **Role:** Product Manager at startup
- **Income:** $120K
- **Location:** San Francisco
- **Tech savviness:** High

## Behaviors
- Works 50+ hours/week
- Uses: Slack, Notion, Figma, Jira
- Checks phone first thing in morning
- Reads newsletters over coffee

## Pain Points
1. Too many tools, context switching
2. Stakeholder alignment meetings
3. Data scattered across systems

## Goals
- Ship features faster
- Better work-life balance
- Get promoted to Director

## Quote
"I spend more time coordinating than creating."

## Jobs To Be Done
- When I [situation], I want to [action], so I can [outcome]
```

### Examples

**SaaS Personas:**
1. Primary: "Startup Sarah" - PM at early-stage startup
2. Secondary: "Enterprise Eric" - PM at Fortune 500
3. Negative: "Agency Alex" - Freelance consultant

### Agent
faion-research-agent (mode: personas)

---

## problem-validation

### Problem
Entrepreneurs build solutions for problems that don't exist or aren't painful enough.

### Framework

**Validation Criteria:**

| Criterion | Threshold | How to Measure |
|-----------|-----------|----------------|
| **Frequency** | Weekly+ | "How often do you face this?" |
| **Intensity** | 7+/10 | "How painful is this? (1-10)" |
| **Willingness to Pay** | Yes | "Would you pay to solve this?" |
| **Search Behavior** | Exists | Check search volume |
| **Competition** | Exists | Someone trying to solve it |

**Evidence Types:**

| Type | Strength | Source |
|------|----------|--------|
| Verbatim quotes | Strong | Interviews |
| Forum discussions | Medium | Reddit, communities |
| Review complaints | Medium | App stores, G2 |
| Search volume | Medium | Google Trends, Ahrefs |
| Competitor existence | Weak | Market research |

**Validation Process:**
1. State the problem hypothesis
2. Define evidence needed
3. Collect evidence (10+ data points)
4. Assess against criteria
5. Decide: Proceed / Pivot / Kill

### Templates

**Problem Validation Report:**
```markdown
## Problem: {Statement}

### Hypothesis
{Who} struggles with {what} because {why}

### Evidence Collected

| Type | Source | Finding |
|------|--------|---------|
| Interview | User 1 | "I spend 3 hours/week on this" |
| Interview | User 2 | "Would pay $50/month" |
| Forum | Reddit | 50 upvotes on complaint post |
| Review | G2 | "Missing feature X" (repeated 10x) |
| Search | Google | "solve X problem" - 5K/month |

### Assessment

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Frequency | Weekly | Interviews |
| Intensity | 8/10 | Interviews |
| WTP | Yes | 4/5 would pay |
| Search | Medium | 5K/month |
| Competition | Yes | 3 competitors |

### Decision
**PROCEED** - Strong problem-solution fit
```

### Examples

**Validated Problem:**
- Hypothesis: Freelancers struggle tracking time across projects
- Evidence: 8/10 interviews confirmed, avg 5 hrs/week lost
- Decision: Proceed to solution validation

### Agent
faion-research-agent (mode: validate)

---

## pain-point-mining

### Problem
Entrepreneurs don't know where customers express frustrations.

### Framework

**Mining Sources:**

| Source | Search Strategy | Signal Strength |
|--------|-----------------|-----------------|
| Reddit | "r/{niche} + frustrating/hate/problem" | High (honest) |
| Twitter/X | "{product} sucks" OR "wish {product}" | High (real-time) |
| App Reviews | 1-3 star reviews | High (specific) |
| Forums | Product-specific communities | Medium |
| Quora | "{problem} solution" | Medium |
| LinkedIn | Industry discussions | Low (filtered) |

**Search Queries:**
```
"{keyword} frustrating" site:reddit.com
"{competitor} alternative" site:reddit.com
"{product} review" 1-star
"I wish {tool} could"
"hate using {tool}"
"looking for {solution}"
```

**Analysis Process:**
1. Collect 50+ pain point mentions
2. Categorize by theme
3. Count frequency per theme
4. Note intensity language
5. Identify gaps in solutions

### Templates

**Pain Point Mining Report:**
```markdown
## Topic: {Area}

### Sources Searched
- Reddit: r/x, r/y, r/z
- App Store: {app1}, {app2}
- Forums: {forum1}

### Pain Points Identified

| Theme | Frequency | Sample Quote | Intensity |
|-------|-----------|--------------|-----------|
| Slow sync | 23 mentions | "Takes forever to sync" | High |
| Missing feature X | 15 mentions | "Why doesn't it have X?" | Medium |
| Expensive | 12 mentions | "Not worth $99/month" | High |

### Key Insights
1. {insight 1}
2. {insight 2}

### Opportunity
{What solution addresses top pain points}
```

### Examples

**Project Management Pain Mining:**
- Top pain: "Too many clicks to create task" (35 mentions)
- Opportunity: One-click task creation from anywhere

### Agent
faion-research-agent (mode: pains)

---

## niche-viability-scoring

### Problem
Entrepreneurs can't objectively assess if a niche is worth pursuing.

### Framework

**5 Criteria Model:**

| Criterion | Weight | 1-3 | 4-6 | 7-10 |
|-----------|--------|-----|-----|------|
| Market Size | 25% | <$10M | $10-100M | >$100M |
| Competition | 20% | Red ocean (10+) | Moderate (3-10) | Blue ocean (<3) |
| Barriers | 20% | High (capital, regulatory) | Medium | Low |
| Profitability | 20% | Thin margins (<20%) | OK (20-40%) | High (>40%) |
| Your Fit | 15% | No relevant skills | Some skills | Perfect match |

**Scoring Process:**
1. Research each criterion
2. Score 1-10 with justification
3. Apply weights
4. Calculate weighted average
5. Compare to thresholds

**Decision Thresholds:**
- 7.5-10: Strong opportunity
- 5.5-7.4: Proceed with caution
- 3.5-5.4: Significant risks
- <3.5: Pass

### Templates

**Niche Viability Scorecard:**
```markdown
## Niche: {Name}

| Criterion | Score | Weight | Weighted | Justification |
|-----------|-------|--------|----------|---------------|
| Market Size | 7 | 25% | 1.75 | $80M SAM |
| Competition | 6 | 20% | 1.20 | 5 competitors |
| Barriers | 8 | 20% | 1.60 | Technical only |
| Profitability | 7 | 20% | 1.40 | SaaS margins |
| Your Fit | 9 | 15% | 1.35 | 10 yrs experience |
| **Total** | | | **7.30** | |

### Decision
**PROCEED WITH CAUTION** - Good opportunity, watch competition

### Risk Mitigation
- {risk 1}: {mitigation}
- {risk 2}: {mitigation}
```

### Examples

**AI Writing Tool Niche:**
- Market: 8 ($200M)
- Competition: 4 (crowded)
- Barriers: 6 (ML expertise needed)
- Profitability: 7 (SaaS)
- Fit: 8 (ML background)
- **Total: 6.5 -> Proceed with differentiation**

### Agent
faion-research-agent (mode: niche)

---

## business-model-research

### Problem
Entrepreneurs compete in crowded markets instead of creating new ones.

### Framework

**Red vs Blue Ocean:**

| Red Ocean | Blue Ocean |
|-----------|------------|
| Compete in existing market | Create uncontested space |
| Beat the competition | Make competition irrelevant |
| Exploit existing demand | Create new demand |
| Value-cost trade-off | Break value-cost trade-off |

**Four Actions Framework:**

| Action | Question | Result |
|--------|----------|--------|
| **Eliminate** | What factors can we eliminate? | Remove costly/unnecessary |
| **Reduce** | What can we reduce below standard? | Simplify |
| **Raise** | What can we raise above standard? | Differentiate |
| **Create** | What new factors can we create? | Innovate |

**Strategy Canvas:**
- X-axis: Key competing factors
- Y-axis: Offering level (low to high)
- Plot competitors and your new curve

### Templates

**Blue Ocean Canvas:**
```markdown
## Industry: {Name}

### Current Red Ocean Factors
| Factor | Industry Level | Customer Value |
|--------|---------------|----------------|
| Price | High | Medium |
| Features | Many | Low (unused) |
| Support | 24/7 | Low (rarely needed) |

### Four Actions

#### Eliminate
- {factor}: Why? {reason}

#### Reduce
- {factor}: From {X} to {Y}

#### Raise
- {factor}: From {X} to {Y}

#### Create
- {new factor}: {description}

### New Value Curve
[Strategy canvas visualization]

### Blue Ocean Opportunity
{Description of uncontested space}
```

### Examples

**Cirque du Soleil:**
- Eliminated: Animals, star performers, aisle concessions
- Reduced: Fun/humor, thrill/danger
- Raised: Unique venue, refined watching environment
- Created: Theme, artistic music/dance, multiple productions

### Agent
faion-research-agent (mode: niche)

---

## value-proposition-design

### Problem
Products don't clearly match customer needs.

### Framework

**Two Parts:**

**1. Customer Profile (right side):**
- Customer Jobs (tasks, problems)
- Pains (obstacles, risks)
- Gains (desired outcomes)

**2. Value Map (left side):**
- Products & Services (what we offer)
- Pain Relievers (how we reduce pains)
- Gain Creators (how we create gains)

**FIT = Pain Relievers address Pains + Gain Creators enable Gains**

**Prioritization:**
- Focus on pains rated 8+/10
- Focus on gains customers measure success by
- Ignore "nice to have" pains/gains

### Templates

**Value Proposition Canvas:**
```markdown
## Customer Segment: {Name}

### Customer Profile

#### Jobs
- Functional: {job}
- Emotional: {job}
- Social: {job}

#### Pains (ranked by intensity)
1. {pain} - 9/10
2. {pain} - 8/10
3. {pain} - 6/10

#### Gains (ranked by relevance)
1. {gain} - Essential
2. {gain} - Expected
3. {gain} - Desired

### Value Map

#### Products & Services
- {product/feature}
- {product/feature}

#### Pain Relievers
- {pain 1} -> {how we relieve it}
- {pain 2} -> {how we relieve it}

#### Gain Creators
- {gain 1} -> {how we create it}
- {gain 2} -> {how we create it}

### FIT Assessment
- Pain coverage: 2/3 top pains addressed
- Gain coverage: 2/3 top gains enabled
- **FIT Score: 80%**
```

### Examples

**Freelancer Invoicing Tool:**
- Pain: Takes too long to create invoice (9/10)
- Pain Reliever: Auto-generate from time tracking
- Gain: Get paid faster
- Gain Creator: Automated payment reminders

### Agent
faion-research-agent (mode: personas)

---

## project-naming

### Problem
Entrepreneurs struggle to find memorable, available names.

### Framework

**Naming Strategies:**

| Strategy | Description | Examples |
|----------|-------------|----------|
| **Descriptive** | What it does | Dropbox, YouTube |
| **Invented** | Made-up word | Spotify, Kodak |
| **Compound** | Two words combined | Facebook, Snapchat |
| **Metaphor** | Symbolic meaning | Amazon, Apple |
| **Portmanteau** | Blended words | Pinterest, Instagram |
| **Alliteration** | Same sound | PayPal, Coca-Cola |
| **Acronym** | Letters | IBM, NASA |

**Good Name Criteria:**
- Easy to spell
- Easy to pronounce
- Memorable
- Domain available (.com preferred)
- No trademark conflicts
- Works internationally

**Generation Process:**
1. Define brand attributes (3-5 adjectives)
2. List keywords (product, benefit, emotion)
3. Apply each strategy to keywords
4. Generate 20+ candidates
5. Check availability
6. Test with target audience

### Templates

**Naming Brief:**
```markdown
## Project: {Description}

### Brand Attributes
- {attribute 1}
- {attribute 2}
- {attribute 3}

### Keywords
- Product: {words}
- Benefits: {words}
- Emotions: {words}

### Name Candidates

| Name | Strategy | .com | Meaning |
|------|----------|------|---------|
| {name} | Descriptive | Y/N | {why} |
| {name} | Invented | Y/N | {why} |
| {name} | Compound | Y/N | {why} |

### Top 3 Recommendations
1. {name}: {reasoning}
2. {name}: {reasoning}
3. {name}: {reasoning}
```

### Examples

**Task Management Tool:**
- Attributes: Simple, fast, powerful
- Candidates: TaskFlow (compound), Tasko (invented), QuickTask (descriptive)
- Winner: TaskFlow (.com available, memorable)

### Agent
faion-research-agent (mode: names)

---

## domain-availability

### Problem
Great names are unusable due to domain/handle unavailability.

### Framework

**Check Priority:**

| Type | Priority | Importance |
|------|----------|------------|
| .com | 1 | Essential for credibility |
| .io | 2 | Acceptable for tech |
| .co | 3 | Alternative |
| GitHub | 1 | Essential for open source |
| Twitter/X | 2 | Important for marketing |
| LinkedIn | 3 | Nice to have |

**Availability Actions:**

| Status | Action |
|--------|--------|
| Available | Register immediately |
| Premium ($X) | Consider if <$5K |
| Taken (parked) | Check price, usually overpriced |
| Taken (active) | Move to next name |

**Alternative Strategies:**
- Add "get", "try", "use" prefix: getTaskFlow.com
- Add "app", "hq" suffix: taskflowhq.com
- Different TLD: taskflow.io
- Creative spelling: taskflw.com

### Templates

**Domain Check Report:**
```markdown
## Name: {name}

### Domain Availability

| Domain | Status | Price | Notes |
|--------|--------|-------|-------|
| {name}.com | Available | $12/yr | Register now |
| {name}.io | Taken | - | Active site |
| {name}.co | Premium | $2,500 | Parked |

### Social Handles

| Platform | Handle | Status |
|----------|--------|--------|
| Twitter | @{name} | Available |
| GitHub | {name} | Taken |
| LinkedIn | /company/{name} | Available |

### Trademark Check
- USPTO: No conflicts found
- Note: Not legal advice, consult attorney

### Recommendation
**Register {name}.com and @{name} immediately**

### Alternatives if Unavailable
1. get{name}.com
2. {name}app.com
3. {name}.io
```

### Examples

**TaskFlow Availability:**
- taskflow.com: Taken (active SaaS)
- gettaskflow.com: Available
- taskflow.io: Available
- @taskflow: Taken
- @gettaskflow: Available
- Recommendation: gettaskflow.com + @gettaskflow

### Agent
faion-domain-checker-agent

---

## pricing-research

### Problem
Entrepreneurs choose wrong pricing models that limit growth or revenue.

### Framework

**Pricing Models:**

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| **Freemium** | High volume, low marginal cost | Viral growth | Low conversion (2-5%) |
| **Subscription** | Recurring value | Predictable revenue | Churn risk |
| **Usage-based** | Variable consumption | Scales with value | Unpredictable revenue |
| **One-time** | Complete product | Simple | No recurring revenue |
| **Tiered** | Diverse segments | Captures more value | Complex |
| **Per-seat** | Team tools | Clear pricing | Resistance to add users |

**Selection Criteria:**

| Factor | Question |
|--------|----------|
| Value delivery | Continuous or one-time? |
| Usage patterns | Consistent or variable? |
| Customer type | Individual or team? |
| Competition | What do they charge? |
| Marginal cost | Cost to serve additional user? |

**Pricing Research:**
1. List top 5 competitors' pricing
2. Calculate value delivered
3. Survey willingness to pay (Van Westendorp)
4. Test with early users

### Templates

**Pricing Strategy:**
```markdown
## Product: {Name}

### Competitor Pricing

| Competitor | Model | Price Range | Notes |
|------------|-------|-------------|-------|
| {name} | Subscription | $X-Y/mo | |
| {name} | Freemium | Free-$X | |

### Value Analysis
- Cost of problem: $X/month
- Time saved: X hours/month
- Value captured: 10-20% of savings

### Recommended Model
**Tiered Subscription**

### Pricing Tiers

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| Free | $0 | {features} | Try before buy |
| Pro | $19/mo | {features} | Individuals |
| Team | $49/mo | {features} | Small teams |
| Enterprise | Custom | {features} | Large orgs |

### Justification
- Freemium drives awareness
- Pro captures 80% of revenue
- Enterprise for large accounts
```

### Examples

**SaaS Pricing Decision:**
- Model: Tiered subscription
- Free: 1 project, basic features
- Pro ($19): Unlimited projects
- Team ($49/user): Collaboration features
- Justification: Match competitor pricing, capture team value

### Agent
faion-research-agent (mode: pricing)

---

## customer-interview-framework

### Problem
Interviews fail to extract actionable insights due to poor questions and structure.

### Framework

**Interview Types:**

| Type | Stage | Goal | Duration |
|------|-------|------|----------|
| Discovery | Problem validation | Understand context | 30 min |
| Problem | Problem validation | Deep dive on pain | 45 min |
| Solution | Solution validation | Test concepts | 45 min |
| Usability | Product development | Test prototype | 60 min |

**Interview Flow:**

```
1. Warm-up (5 min)
   - Build rapport
   - Set expectations

2. Context (10 min)
   - Their role, background
   - Current situation

3. Deep dive (20 min)
   - Pain exploration
   - Past behavior
   - Emotional triggers

4. Concept test (10 min)
   - Show solution
   - Get reaction

5. Wrap-up (5 min)
   - Willingness to pay
   - Referrals
```

**Question Types:**

| Type | Purpose | Example |
|------|---------|---------|
| Open | Explore | "Tell me about..." |
| Probing | Go deeper | "Why is that?" |
| Clarifying | Understand | "Can you give an example?" |
| Summary | Confirm | "So you're saying..." |

**Anti-patterns:**
- Leading questions: "Don't you think X is great?"
- Future hypotheticals: "Would you use...?"
- Pitching: Explaining your solution too early
- Multiple questions: Asking 2+ questions at once

### Templates

**Interview Guide:**
```markdown
## Interview: {Type}

### Preparation
- Hypothesis to test: {hypothesis}
- Key questions: 5 max
- Recording setup: {yes/no}

### Script

#### Warm-up
"Thanks for joining. I'm researching [topic]. No right/wrong answers, just honest feedback."

#### Context
"Tell me about your role."
"Walk me through a typical day."

#### Deep Dive
"Tell me about the last time you [problem]."
"What happened? What did you do?"
"How did that make you feel?"
"What would you change?"

#### Concept Test
[Show prototype/concept]
"What do you think this is?"
"Would this help? How?"
"What's missing?"

#### Wrap-up
"Would you pay for this? How much?"
"Who else should I talk to?"

### Notes Template

| Question | Answer | Insight |
|----------|--------|---------|
| {question} | {verbatim} | {interpretation} |
```

### Examples

**Key Interview Insights:**
- 8/10 mentioned same frustration
- Verbatim: "I would pay $100 to not deal with this"
- Behavior: Currently using 3 tools as workaround
- Insight: Strong problem-solution fit

### Agent
faion-research-agent (mode: validate)

---

*Methodologies Detail Reference | Extracted from SKILL.md v1.1*
*20 detailed methodologies with templates and examples*
