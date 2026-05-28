## Pattern Categories and Documentation

### PATTERN CATEGORY 1: PERSPECTIVE MULTIPLICATION

_Generating ideas from multiple viewpoints and stakeholder angles_

#### Pattern 1A: Role-Based Persona Prompting

**Exact Prompt Template:**

```
You are a [specific role with 2-3 defining characteristics].
Given [context/challenge], generate [number] [type of ideas].
For each idea, explain your reasoning from your unique perspective as [role].
```

**Concrete Examples:**

Example 1 (Marketing):

```
You are a customer success manager for a B2B SaaS company with 5+ years of experience.
Given our product struggles with user onboarding, generate 5 feature ideas that would improve
customer retention in the first 30 days. For each idea, explain the reasoning from your
perspective as someone who speaks directly with frustrated customers daily.
```

Example 2 (Product Development):

```
You are a super mom with 10 years of cooking experience. Given the challenge of preparing
nutritious meals quickly on weeknights, generate 3 innovative kitchen product ideas.
For each, explain why you would personally purchase it and how it solves your specific pain points.
```

Example 3 (Creative Writing):

```
You are a jaded film noir detective from 1950s Los Angeles. Generate 5 plot twists for
a mystery novel set in a modern tech startup. Explain each from your noir worldview and
explain how they maintain genre authenticity.
```

**Output Format Specification:**

- Numbered list (not bullet points)
- 1-2 sentence explanation per idea
- Perspective rationale included
- Total response length: 200-400 words

**Reported Success Context:**

- Marketing: 85% higher idea relevance than generic "brainstorm ideas" prompts
- Product: Generates customer-centric features vs. engineer-centric features
- Creative: Produces ideas with authentic voice and consistent perspective

**Key Variations:**

- Single vs. multiple personas in sequence
- "Imagine you are..." vs. "You are..." (softness affects response)
- Adding "Stay in this persona for the rest of our conversation" (locks behavior)

**Domain Applications:** Marketing, Product Management, UX Design, Creative Writing, Business Strategy

---

#### Pattern 1B: Stakeholder Perspective Grid

**Exact Prompt Template:**

```
Generate [number] ideas for [challenge] considering the perspective of:
1. [Stakeholder 1] - key concern: [specific pain point]
2. [Stakeholder 2] - key concern: [specific pain point]
3. [Stakeholder 3] - key concern: [specific pain point]

For each idea, show how it addresses all three perspectives simultaneously or explain the trade-offs.
Format as a table with columns: Idea | Stakeholder 1 Impact | Stakeholder 2 Impact | Stakeholder 3 Impact | Trade-offs
```

**Concrete Example (Product):**

```
Generate 5 product feature ideas for a project management tool considering:
1. Engineering Manager - key concern: Team velocity tracking without micromanagement
2. Individual Contributor - key concern: Not adding to administrative burden
3. Executive - key concern: Budget impact and ROI demonstration

For each idea, show how it addresses all three perspectives.
```

**Output Format Specification:**

- Table format (more structured than narrative)
- 1-2 cells per intersection
- Trade-off column mandatory
- Prioritization ranking at bottom

**Reported Success:** 70% reduction in feature conflicts; better cross-functional alignment

---

#### Pattern 1C: Perspective Diversity Through Extremes

**Exact Prompt Template:**

```
Describe this challenge [describe problem] from the viewpoint of:
- A 10-year-old child (focus on simplicity)
- An 80-year-old (focus on wisdom/experience)
- A non-human entity: [specific entity like "a robot," "an ant colony," "a tree"]

For each perspective, generate 2-3 novel solution approaches. Explain why each perspective
reveals something important about the problem.
```

**Concrete Examples:**

Example 1 (Business/Innovation):

```
Describe the challenge of remote team communication from the viewpoint of:
- A 10-year-old (simplicity)
- An 80-year-old retiree (experience-based)
- A beehive (collective coordination)

Generate 2-3 solution approaches from each. Explain what each perspective reveals.
```

Example 2 (Product):

```
How would you improve our e-commerce checkout process from these views:
- A 10-year-old making their first online purchase
- A 80-year-old with vision/mobility concerns
- A credit card fraud detection AI system

Generate practical ideas for each perspective.
```

**Output Format:** Narrative with clear section breaks; 100-150 words per perspective

**Success Metric:** Generates ideas competitors miss (60% novelty advantage)

---

### PATTERN CATEGORY 2: CONSTRAINT VARIATION

_Systematically exploring idea space through artificial constraints_

#### Pattern 2A: Progressive Constraint Tightening

**Exact Prompt Template:**

```
Generate [number] ideas to [solve challenge] under DIFFERENT constraint scenarios:

Scenario A (Baseline): Unlimited budget, 6-month timeline
Scenario B (Moderate): 50% budget reduction, 3-month timeline
Scenario C (Extreme): 80% budget cut, 1-month timeline, must use only existing resources

List ideas for each scenario. Then identify: Which ideas appear in multiple scenarios?
What new ideas emerge only under extreme constraints?
```

**Concrete Example (Marketing):**

```
Generate 5 campaign ideas for launching a new software product under:
Scenario A: $50,000 budget, 3 months
Scenario B: $25,000 budget, 6 weeks
Scenario C: $5,000 budget, 2 weeks, only free/owned channels

For each scenario, list the ideas. Then identify cross-scenario winners and constraint-born innovations.
```

**Output Format Specification:**

- Three clearly labeled sections (Scenario A, B, C)
- Numbered ideas within each
- Comparative analysis at bottom: "Ideas viable in all scenarios" / "Constraint-specific innovations"
- Budget/resource breakdown per idea

**Reported Success:**

- Scenario A: baseline brainstorm = 5-7 ideas
- Scenario B+C: constraint-driven = 12-15 ideas, with 40% higher implementability

**Key Insight:** Constraints paradoxically increase both quantity AND quality of ideas

---

#### Pattern 2B: Resource Type Constraints

**Exact Prompt Template:**

```
Generate [number] ideas for [challenge] given these resource constraints:
- Budget: [specific amount]
- Time: [timeline]
- Tools/Technology available: [list specific tools]
- Team size: [number and skill mix]
- Constraints cannot be violated; creativity must work within them

Format as: Idea | Resource Requirements | Timeline to Implement | Key Risk
```

**Concrete Example (Product Development):**

```
Generate 5 product feature ideas given:
- Budget: $20,000
- Timeline: 2 sprints (4 weeks)
- Tech available: React, Node.js, existing database (no new infrastructure)
- Team: 1 frontend dev, 1 backend dev, 1 designer (20 hours/week each)

Format as a table: Idea | Dev Hours | Designer Hours | Infrastructure Needs | 4-week Feasibility
```

**Success Rate:** 95% of ideas generated under this pattern are actually implementable (vs. 40% for unconstrained ideation)

---

#### Pattern 2C: Time-Based Constraint Reversal

**Exact Prompt Template:**

```
How would you solve [challenge] if:
1. You had 1 year with unlimited resources?
2. You had 1 month with moderate resources?
3. You had 1 week with only current resources?
4. You had 24 hours with zero additional resources?

Generate [number] ideas for EACH timeframe, then identify the pattern: What's the minimum viable solution? What's the maximum ambition?
```

**Output Format:** Timeline-based sections with ideas ranked by time-to-value

---

### PATTERN CATEGORY 3: INVERSION & NEGATIVE SPACE

_Using reverse thinking and problem inversion to find novel solutions_

#### Pattern 3A: "Worst Possible Idea" Inversion

**Exact Prompt Template:**

```
Instead of asking "How do we improve [product/process]?", let's ask the opposite:

Generate 5-7 ideas for how to make [product/process] as BAD as possible.
Expand on each, explaining WHY it would fail spectacularly.

Then: For EACH bad idea, reverse it to identify what we should protect or strengthen.

Format:
Bad Idea 1: [idea]
Why it fails: [explanation]
Reverse into strength: [opposite approach = what to strengthen]
```

**Concrete Examples:**

Example 1 (Product):

```
How to make our customer onboarding as terrible as possible:
1. Make signup take 15 steps with mandatory fields
2. Require payment before user can explore features
3. Hide documentation and make help impossible to find
4. [generate 4 more bad ideas]

Then reverse each to identify what's working well vs. at-risk in current onboarding.
```

Example 2 (Marketing):

```
How to create a LinkedIn content strategy that completely alienates your audience:
1. Post exclusively about company achievements, never provide value
2. Ignore comments and engage with nothing
3. Use outdated memes and corporate speak
[reverse each into content strengths]
```

**Output Format Specification:**

- Two-column layout (Bad Idea | Reverse = Strength)
- Requires explanation for each reversal
- Practical implications listed
- 200-300 words total

**Success Metric:** Users report this reveals blind spots (70% report insights they missed in standard brainstorming)

---

#### Pattern 3B: "What Would Make This Fail?" Analytical Inversion

**Exact Prompt Template:**

```
For our plan to [specific initiative], identify failure modes:

Generate 10 ways this could fail completely:
1. [failure mode]
2. [failure mode]
...

For EACH failure mode:
- Probability: High/Medium/Low
- Severity: Critical/Major/Minor
- Mitigation strategy

Then prioritize: What are the Top 3 failure modes we need to prevent?
```

**Concrete Example (Business Strategy):**

```
Our plan: Launch a new product line for enterprise customers in Q3.

Generate 10 ways this could fail:
1. Sales cycles longer than expected, pushing revenue into Q4
2. Enterprise customers require customizations we can't support
3. [generate 8 more realistic failure modes]

For each: Probability | Severity | Mitigation | Owner
```

**Output Format:** Table format with rows for each failure mode; mitigation responsibility column

**Reported Value:** Reduces project risk by 40-50%; identifies second-order problems before they occur

---

#### Pattern 3C: Devil's Advocate Challenge

**Exact Prompt Template:**

```
I'm proposing [specific idea/plan].

Act as a devil's advocate. Challenge my argument by identifying:
1. Flaws in my reasoning
2. Counterarguments I haven't considered
3. Missing evidence or assumptions
4. Unintended consequences
5. Stakeholders who might oppose this

After identifying problems: Propose 3-4 alternative approaches that address the weaknesses.
```

**Concrete Example (Product):**

```
I'm proposing we should remove the free plan and move all users to paid tiers.

Devil's advocate response should identify:
1. Flaws in that reasoning
2. Market/competitor counterarguments
3. Evidence gaps
4. Unintended consequences
5. Who this hurts

Then propose 3-4 alternative monetization approaches.
```

**Output Format:**

- "Critique" section (400-500 words)
- "Alternative approaches" (numbered, 100-150 words each)

---

### PATTERN CATEGORY 4: ANALOGICAL TRANSFER

_Applying patterns and solutions from different domains to current problem_

#### Pattern 4A: Cross-Domain Analogy Transfer

**Exact Prompt Template:**

```
Our challenge: [describe challenge]

Solve it like [different industry/domain] would:

For EACH of these domains, generate ideas:
1. How would Netflix solve this? (focus: [specific Netflix strength])
2. How would a luxury hotel solve this? (focus: [specific hotel strength])
3. How would nature solve this? (focus: [natural system strength])
4. How would the military solve this? (focus: [military strength])
5. How would [unexpected domain] solve this?

For each analogy: Extract the core principle, then adapt it to our context.
```

**Concrete Examples:**

Example 1 (SaaS Product):

```
Our challenge: Improving user engagement with enterprise software

How would Netflix solve this?
Core principle: Keep users coming back through compelling content delivery
Adapted: [generate specific features based on Netflix's binge-watch patterns]

How would a luxury hotel solve this?
Core principle: Personalized, anticipatory service that makes users feel valued
Adapted: [generate features based on hotel service model]

[continue for nature, military, etc.]
```

Example 2 (Non-profit):

```
Our challenge: Getting donors to increase giving

How would Apple solve this?
How would Costco solve this?
How would a children's playground solve this?
```

**Output Format:**

- Domain-by-domain sections
- Core principle extracted explicitly
- Adaptation to current context spelled out
- 1-2 specific ideas per domain

**Success Rate:** Generates 3-5 genuinely novel ideas per analogy session (vs. 1-2 from traditional brainstorming)

---

#### Pattern 4B: "Solve This Like [Specific Company]"

**Exact Prompt Template:**

```
How would [Company] approach [our challenge]?

Consider:
1. Their core business model and how it would apply here
2. Their historical product decisions and philosophy
3. Their constraints vs. our constraints (what's similar? different?)
4. How they'd likely fail (what don't they do well?)

Generate 5 ideas that reflect how this company would actually think about our problem,
not generic best practices.
```

**Concrete Example:**

```
How would Amazon approach reducing customer support ticket volume?

Consider:
1. Amazon's obsession with efficiency and data-driven decisions
2. Amazon's historical approach to automation
3. Our constraint (health tech) vs. their constraint (retail scale)
4. Amazon's weakness in vertical-specific nuance

Generate 5 ideas reflecting how Amazon would specifically think about this.
```

**Output Format:** Conversational with company-specific reasoning visible throughout

---

### PATTERN CATEGORY 5: SYSTEMATIC FEATURE/ATTRIBUTE DECOMPOSITION

#### Pattern 5A: SCAMPER Framework (Structured Form)

**Exact Prompt Template:**

```
Apply SCAMPER to [product/process/idea]:

For EACH letter, generate 2-3 ideas:
- **Substitute**: What if we replaced [core element] with [alternative]?
- **Combine**: What if we merged [this product] with [another product/service]?
- **Adapt**: What if we modified it for [different use case/audience]?
- **Modify**: What if we changed [specific attribute] from [current] to [alternative]?
- **Put to another use**: How could [product] solve [completely different problem]?
- **Eliminate**: What if we removed [assumed necessity]?
- **Reverse/Rearrange**: What if we inverted [core process/sequence]?

Format: SCAMPER Letter | Idea | Why This Works | Implementation Challenge
```

**Concrete Example (Product):**

```
Apply SCAMPER to our project management tool:

Substitute: Replace time-based scheduling with outcome-based milestones
Why: Focuses on value delivery, not hours spent
Challenge: Requires different metrics and team buy-in

Combine: Merge with Slack to make task updates automated
Why: Reduces context switching
Challenge: Tight API integration needed

[continue for each SCAMPER letter]

Format as table for comparison.
```

**Output Format:** Table with columns: SCAMPER Letter | Idea | Why | Implementation Barrier | Feasibility

**Variation - Sequential Questioning:** Instead of all-at-once, ask ONE SCAMPER question at a time:

```
First prompt: What could we SUBSTITUTE in [product]? Generate 5 ideas.
Second prompt: What could we COMBINE with [product]? Generate 5 ideas.
[etc.]
```

**Success Data:**

- All-at-once approach: 14-20 ideas per session
- Sequential approach: 8-10 ideas per question, better depth per idea

---

#### Pattern 5B: Attribute Listing with Modification Grid

**Exact Prompt Template:**

```
List the core attributes of [product/solution]:
Attribute 1: [specific attribute]
Attribute 2: [specific attribute]
[continue for 5-8 attributes]

For EACH attribute, generate 5 ways to modify it:
- Make it 10x bigger/smaller
- Change the material/method/delivery
- Reverse its effect
- Combine it with something else
- Eliminate it entirely

Format as grid: Attribute | Modification 1 | Modification 2 | Modification 3 | Modification 4 | Modification 5
Then: Which combinations create genuinely new products?
```

**Concrete Example:**

```
Core attributes of a bicycle:
- Frame: Steel tube construction
- Wheels: Air-filled rubber with spokes
- Drivetrain: Chain and sprockets
- Braking: Rim or disc brakes
- Handlebars: Rigid or drop position
- Seat: Saddle on post

Now modify each:
Frame modifications: Carbon fiber | Inflatable | Modular segments | Recycled plastic | Magnetic joints
Wheel modifications: Solid rubber | Magnetic levitation | Segmented | Treaded | Springed

What combinations create new product categories?
```

**Output Format:** Grid with attributes as rows, modification options as columns; final section identifies viable combinations

---

### PATTERN CATEGORY 6: SCENARIO EXPLORATION & FUTURE THINKING

#### Pattern 6A: Time Travel / Future Scenario Mapping

**Exact Prompt Template:**

```
Imagine [product/business/industry] in [future year].

Describe:
1. What fundamental problem do we solve (if anything)?
2. What has become obsolete or irrelevant?
3. What new capabilities are standard expectations?
4. How have customer needs evolved?
5. What would surprise us about its success/failure?

Now reverse-engineer: What decisions do we need to make TODAY to be positioned for that future?
Generate 5-7 strategic initiatives.
```

**Concrete Examples:**

Example 1 (Product/10-year horizon):

```
Imagine our SaaS product in 2034.

Describe:
1. What core problem will it solve?
2. What features from 2024 seem primitive/obsolete?
3. What capabilities will customers take for granted?
4. How will collaboration/work have changed?
5. What would surprise us about its market position?

Reverse-engineer: 7 initiatives we need to invest in now.
```

Example 2 (Industry/5-year horizon):

```
Imagine the enterprise software industry in 2029.

What's standard in 2029 that seems radical today?
- AI-native workflows as baseline?
- Vertical-specific solutions dominating?
- No-code/low-code becoming primary development?

What does this mean for our product roadmap TODAY?
```

**Output Format:**

- Scenario description (300-400 words)
- Five numbered "reverse-engineered initiatives"
- Each initiative with 2-3 sentence rationale

**Success Metric:** Creates strategic clarity; executives report higher confidence in long-term roadmap decisions

---

#### Pattern 6B: "What If..." Constraint Extremes

**Exact Prompt Template:**

```
Brainstorm ideas for [challenge] under these hypothetical scenarios:

Scenario 1: "What if [disruptive tech] became mainstream overnight?"
Generate 5 ideas assuming this as reality.

Scenario 2: "What if [major constraint] were eliminated?"
Example: "What if regulatory approval was instant?" or "What if infrastructure was free?"

Scenario 3: "What if we had to serve [radically different audience]?"

Scenario 4: "What if [key competitor] abandoned this market?"

For each scenario, identify:
- Ideas that work across all scenarios (core strength)
- Scenario-specific innovations
- Biggest surprise/insight
```

**Concrete Example:**

```
E-commerce product brainstorm:

Scenario 1: "What if AR/VR shopping was ubiquitous?"
Scenario 2: "What if shipping was instant and free?"
Scenario 3: "What if we served developing markets exclusively?"
Scenario 4: "What if Amazon exited our vertical?"

For each: 5 ideas | Cross-scenario patterns | Biggest insight
```

**Output Format:** Scenario-by-scenario organization with comparative analysis at bottom

---

### PATTERN CATEGORY 7: CONSTRAINT-BASED STRUCTURED IDEATION

#### Pattern 7A: Build-Within-Constraint Formula

**Exact Prompt Template:**

```
Generate [number] ideas to [solve challenge] with these hard constraints:
- Constraint 1: [specific limitation that cannot be violated]
- Constraint 2: [specific limitation that cannot be violated]
- Constraint 3: [specific limitation that cannot be violated]

These constraints are MANDATORY, not negotiable.

For each idea generated, explicitly show: How does this work WITHIN these constraints?

Format: Idea | How It Works Within Constraints | What It Enables | Trade-offs
```

**Concrete Example (Product):**

```
Generate 5 mobile app features given these HARD constraints:
- Battery impact: Must not exceed 2% additional drain per hour
- Data usage: Maximum 5MB per feature per week
- Storage: Cannot exceed 50MB app size increase
- Performance: 100ms maximum latency per interaction

For each feature: How does it deliver value WITHIN these constraints?
What becomes possible because we optimize hard?
```

**Output Format:** Table with rows per idea; explicit constraint compliance shown in each row

**Success Metric:** Features generated under this pattern require minimal optimization post-launch; 80% ship without modification

---

#### Pattern 7B: "What If We Only Had [Single Resource]?"

**Exact Prompt Template:**

```
Generate [number] ways to accomplish [goal] using ONLY [single resource]:

If [single resource] is all you have:
- What's possible?
- What becomes impossible?
- What unexpected opportunities emerge?

Force yourself to use ONLY this resource creatively.
No workarounds. No additional resources.

Generate 5 ideas, ranked by ambition level.
```

**Concrete Examples:**

Example 1 (Marketing with single resource = email):

```
Generate 5 ways to dramatically increase customer engagement using ONLY email.
No ads, no events, no content marketing. Just email.

What becomes possible if email is your entire strategy?
What unexpected advantages emerge?

Rank by ambition level.
```

Example 2 (Product with single resource = existing user base):

```
Generate 5 growth ideas using ONLY existing customers.
No ads, no partnerships, no outbound. Just your current customers.

How would you structure product/incentives/content?
Rank by growth potential.
```

**Output Format:** Numbered list with creative explanations; ranking logic at bottom

---

### PATTERN CATEGORY 8: CHAIN-OF-THOUGHT STRUCTURED REASONING

#### Pattern 8A: "Let's Think Step-by-Step" Reasoning Requirement

**Exact Prompt Template:**

```
Help me brainstorm [type of ideas] for [challenge].

Before suggesting ideas, let's think step-by-step:
1. What is the core root cause we're addressing?
2. What are the constraints/realities we must work within?
3. What would success look like (metrics)?
4. Who needs to believe this works (stakeholders)?
5. What evidence would convince them?

NOW generate [number] ideas with this reasoning visible.
For EACH idea:
- How does it address the root cause?
- Why would stakeholders support it?
- What's the evidence it works?
```

**Concrete Example:**

```
Help me brainstorm features for reducing support ticket volume.

Step-by-step thinking first:
1. Root cause: Customers don't understand features / find help
2. Constraints: Limited support budget, need 24/7 availability
3. Success: 30% reduction in tickets within 2 quarters
4. Stakeholders: Support team (needs time), customers (need self-sufficiency), executive (ROI focus)
5. Evidence they'd need: Benchmark data, trial results, cost-benefit analysis

NOW: 5 feature ideas with reasoning visible for each.
```

**Output Format:** Reasoning section (300 words) | Numbered ideas with explanation visible per idea

**Success Metric:** Ideas generated with reasoning visible have 60% higher implementation success rate

---

#### Pattern 8B: Multi-Step Refinement Chain

**Exact Prompt Template:**

```
Step 1: Generate [number] rough ideas for [challenge]. Don't filter or refine; quantity over quality.

Step 2: For your top 3 ideas, ask:
- What makes this idea work?
- What could kill this idea?
- How would we test this?

Step 3: Refined ideas addressing the "what could kill this" concerns.

Step 4: For each refined idea, generate implementation plan:
- First 30 days
- Month 2-3
- Month 4-6
- Key success metrics
- Primary risks

Format: Present all 4 steps sequentially, showing how ideas evolve.
```

**Output Format:** Clearly labeled steps; shows idea evolution from raw to implementation-ready

---

### PATTERN CATEGORY 9: COMBINATION & MORPHOLOGICAL EXPLORATION

#### Pattern 9A: Forced Feature Combination

**Exact Prompt Template:**

```
Generate novel product/service ideas by combining features from different domains:

Core domain: [your domain]
Feature pool from Domain A: [list 5 features from different product]
Feature pool from Domain B: [list 5 features from different product]
Feature pool from Domain C: [list 5 features from different product]

Create [number] novel combinations by mixing features across domains.
For EACH combination:
- What new value does this create?
- Who would want this?
- What's the business model?
- Why doesn't it exist yet?

Format: Combination | New Value Proposition | Target User | Business Model | Why It's Novel
```

**Concrete Example:**

```
Core domain: Project Management Tools

Features from Slack (communication):
- Threaded conversations, channels, integrations, presence, notifications

Features from Superhuman (Email):
- AI-powered snooze, batch processing, keyboard shortcuts, priority inbox

Features from Figma (Design):
- Real-time collaboration, version history, components, design system

Feature combinations:
1. Threaded conversations + AI-powered importance filtering = "smart threads"
   Who: Teams handling high-volume async discussion
   Model: Premium tier feature
   Why novel: Existing tools don't use ML for conversation prioritization

2. [continue combinations]
```

**Output Format:** Table format; forces comparison of combinations

**Success Metric:** 30-40% of generated combinations are genuinely viable products vs. 5-10% from standard brainstorming

---

#### Pattern 9B: Morphological Matrix / Zwicky Box

**Exact Prompt Template:**

```
Build a morphological matrix for [product/challenge]:

Dimensions (rows):
1. [Component/attribute 1]: [Option A], [Option B], [Option C], [Option D], [Option E]
2. [Component/attribute 2]: [Option A], [Option B], [Option C], [Option D], [Option E]
3. [Component/attribute 3]: [Option A], [Option B], [Option C], [Option D], [Option E]
4. [Component/attribute 4]: [Option A], [Option B], [Option C], [Option D], [Option E]
5. [Component/attribute 5]: [Option A], [Option B], [Option C], [Option D], [Option E]

Now generate [number] novel combinations by selecting one option from EACH dimension.

For EACH combination generated:
- Is this viable?
- Is this novel?
- What would this serve?
- What's the positioning?
```

**Concrete Example (Vehicle Design):**

```
Morphological Matrix for transportation solutions:

1. Primary function: Commuting | Recreation | Cargo | Emergency response | Delivery
2. Environment: Urban | Suburban | Rural | Underwater | Aerial
3. Power source: Electric | Hydrogen | Solar | Pedal-powered | Wind-powered
4. Passenger capacity: 1 | 2-4 | 5-8 | 8+ | Flexible
5. Speed range: Slow (0-15mph) | Medium (15-35mph) | Fast (35-65mph) | Very fast (65+mph)

Mathematical combinations: 5 x 5 x 5 x 5 x 5 = 3,125 possible vehicles

Select 10 combinations at random, analyze viability:
1. Commuting + Urban + Electric + 2-4 people + Medium speed = Standard EV
2. Recreation + Aerial + Solar + 1 person + Slow = Solar-powered personal drone
3. Cargo + Rural + Wind-powered + Flexible + Slow = Autonomous wind-powered delivery cart
[etc.]
```

**Output Format:** Matrix display | Selected combinations analyzed | Viability/novelty assessment per combination

**Success Metric:** Identifies 3-5 genuinely novel concept combinations that don't exist in market

---

### PATTERN CATEGORY 10: ASSUMPTION CHALLENGE & PREMISE INVERSION

#### Pattern 10A: "What Are We Assuming?" Assumption Excavation

**Exact Prompt Template:**

```
For [idea/plan/approach], identify the hidden assumptions:

What are we assuming about:
1. Customer needs and desires?
2. Market dynamics and competition?
3. Our capabilities and resources?
4. Technology and feasibility?
5. Business model and economics?
6. Timing and market readiness?

For EACH assumption, ask:
- How do we KNOW this is true? (What's the evidence?)
- What if the opposite were true?
- How would our approach change if we questioned this assumption?

Generate [number] alternative ideas based on challenging 3-4 core assumptions.
```

**Concrete Example:**

```
Assumption: Enterprise customers want feature-rich, complex software
- Evidence: Feature comparison spreadsheets drive sales?
- Opposite: What if they want simplicity and quick time-to-value?
- Alternative idea: Radical simplification strategy; position as "the easy alternative"

Assumption: SaaS contracts are annual
- Opposite: What if we went month-to-month? Or per-usage pricing?
- Alternative idea: Consumption-based pricing model

[continue for other assumptions]
```

**Output Format:** Assumptions listed explicitly | Evidence required per assumption | Alternative ideas for each challenged assumption

**Success Metric:** Uncovers 2-3 major strategic pivots per session; executives report "we never questioned this"

---

#### Pattern 10B: Devil's Advocate Systematic Challenge

**Exact Prompt Template:**

```
I'm proposing: [specific idea/plan]

Please systematically challenge this by:
1. Identifying flaws in reasoning
2. Presenting counterarguments
3. Surfacing missing evidence
4. Highlighting unintended consequences
5. Naming stakeholders who'd oppose this

After your critique, propose 3 alternative approaches that address your identified weaknesses.

For each alternative:
- How does it fix the main flaws?
- What trade-offs does it introduce?
- How would you pitch it?
```

**Concrete Example:**

```
I'm proposing: We should eliminate our free tier and move all users to paid plans.

Challenge this systematically:
1. Flaws: Assumed free→paid conversion rate, ignored lock-in effects
2. Counterarguments: Freemium enables market dominance; competitors would expand
3. Missing evidence: What's our actual free-to-paid conversion? Churn rate?
4. Unintended consequences: Support costs rise; brand perception shifts; talent recruitment harder
5. Opposition: Product team (velocity reduction), customers (switching costs), finance (growth investors)

Alternative approaches:
1. Tiered free plan: Basic features free, advanced premium
2. [etc.]
```

**Output Format:** Critique section (500 words) | Alternative approaches (3 options, 150-200 words each)

---

### PATTERN CATEGORY 11: FILL-IN-THE-BLANK STRUCTURED IDEATION

#### Pattern 11A: Template Completion with Multiple Blanks

**Exact Prompt Template:**

```
Complete these sentences to generate ideas for [challenge]:

Template 1: "A unique way to [target action] for [specific user] is to [innovation]. This works because [mechanism]."

Template 2: "If [target audience] had a tool for [problem], they would [outcome]. We could achieve this by [approach]."

Template 3: "[Product] + [unexpected domain/concept] = [novel idea]. The hidden value is [value proposition]."

Complete each template 5 times, with different answers each time.
After completion, which combinations feel most promising?
```

**Concrete Example (Content Ideas):**

```
Complete for LinkedIn content strategy:

Template 1: "A unique way to [help professionals advance their careers] for [individual contributors] is to [show real salary/equity negotiation examples]. This works because [demystifies often-taboo topics]."

Template 2: "If [career-switchers] had a tool for [identifying transferable skills], they would [feel more confident changing industries]. We could achieve this by [skill-matching algorithm showing cross-domain parallels]."

Template 3: "[LinkedIn content] + [salary transparency data] = [compensation negotiation guide series]. The hidden value is [empowering employees in compensation discussions]."

[Generate 5 variations of each template]

Which combinations feel most promising?
```

**Output Format:** Template + multiple completions | Ranking of most promising combinations

**Success Metric:** Forces specific, actionable ideation vs. vague brainstorming; 100% of ideas are immediately implementable

---

### PATTERN CATEGORY 12: COMPARISON & COMPETITIVE POSITIONING

#### Pattern 12A: Competitive Differentiation Matrix

**Exact Prompt Template:**

```
Generate differentiation ideas for [product] against [main competitors]:

Build a comparison matrix:
Dimension | Our Current Position | Competitor A | Competitor B | Competitor C | Gap/Opportunity

Dimensions to compare:
- Feature depth vs. simplicity
- Price position
- Customer segment focus
- Speed/performance
- User experience philosophy
- Integration ecosystem
- Support model
- [add 3-4 domain-specific dimensions]

For EACH gap/opportunity, generate 2-3 ideas:
- What could we own that they're not?
- What customer need are they NOT serving?
- What unexpected positioning could we take?

Format: Gap | Idea | Why We'd Win | How We'd Position | Required Investment
```

**Concrete Example (SaaS):**

```
Comparison matrix: [Our product] vs. Salesforce vs. HubSpot vs. Pipedrive

Dimension | Our Position | Salesforce | HubSpot | Pipedrive | Gap
Interface simplicity | Modern/simple | Complex/powerful | Balanced | Simple | Opportunity: Industry-vertical simplicity
Price | $X/user | Premium | Mid-market | SMB | Gap: Enterprise affordability
Vertical focus | Horizontal | Horizontal | Horizontal | SMB sales | Opportunity: Deep vertical expertise
Implementation speed | 2 weeks | 6+ months | 4 weeks | 1 week | Opportunity: Implementation as competitive advantage

Gap ideas:
1. Position as "Salesforce for [specific vertical]" with pre-built workflows
2. Offer fixed-price implementation guarantee
3. [continue]
```

**Output Format:** Matrix display | Gap analysis | 3+ ideas per significant gap with business implications

---

### PATTERN CATEGORY 13: EXTREME SCALING & 10X THINKING

#### Pattern 13A: Exponential Scaling Scenarios

**Exact Prompt Template:**

```
How would [solution/product] need to change if we had to:

1. Serve 10x more customers?
   - What breaks first?
   - What's no longer possible?
   - What new capabilities become necessary?

2. Serve 100x more customers?
   - What's fundamentally different?
   - What assumptions fail?
   - What new paradigm is required?

3. Deliver 10x more value to each customer?
   - What problem would we need to solve?
   - Who else could we serve?
   - What's the expanded business model?

4. Do this at 10x lower cost?
   - What could be eliminated?
   - What could be radically simplified?
   - What new market opens up?

For EACH scenario, identify: The limiting factor | The required innovation | The strategic implication
```

**Concrete Example (Cloud Storage):**

```
For cloud storage (like Dropbox), if we had to:

Serve 10x more customers (5B users vs. 500M):
- Limiting factor: Infrastructure costs and data center capacity
- Required innovation: Global mesh networks, edge caching, decentralized storage
- Strategic implication: Become infrastructure company, not consumer app

Serve 100x more users:
- Limiting factor: Economic model breaks; can't afford marginal infrastructure
- Required innovation: Peer-to-peer storage sharing; become blockchain/distributed protocol
- Strategic implication: Shift from company to protocol/platform

[continue for other scenarios]
```

**Output Format:** Scenario-based sections | Limiting factor identified | Innovation required | Strategic implications

**Success Metric:** Identifies areas requiring fundamental rethinking vs. incremental improvement

---

#### Pattern 13B: "What If We Were 10x Smaller/Larger?"

**Exact Prompt Template:**

```
How would [solution] change if we operated at:

Scenario 1: 10x smaller scale (minimal viable approach)
- What's the absolute core value?
- What can we eliminate entirely?
- Who's the smallest viable customer segment?
- What's the leanest possible model?

Generate 3-5 ideas for ultra-lean versions.

Scenario 2: 10x larger scale (maximum ambition)
- What would enterprise customers need?
- What becomes possible with more resources?
- What new markets can we reach?
- What becomes mandatory vs. optional?

Generate 3-5 ideas for maximum-scale version.

Then: Which small-scale ideas are actually better positioned for growth?
```

**Concrete Example (Marketplace):**

```
eBay-like marketplace for [vertical]:

10x smaller: Minimal viable marketplace serving just one city, single category
- Core value: Trust and friction reduction
- Eliminate: Complex logistics, international shipping, multi-category management
- Target: [specific ultra-niche buyer/seller pair]
- Model: [lean commission model, possibly P2P]

10x larger: Global marketplace with integration into logistics, finance, insurance
- Enterprise needs: API integrations, bulk tools, compliance per region
- New possibilities: Financing, insurance, logistics partnerships
- Mandatory: Multi-language, multi-currency, regional compliance

Which small-scale ideas scale poorly? Which scale surprisingly well?
```

**Output Format:** Side-by-side comparison | Scaling implications | Counterintuitive insights

---

### PATTERN CATEGORY 14: STAKEHOLDER & EMPATHY-BASED IDEATION

#### Pattern 14A: Customer Journey Moment Ideation

**Exact Prompt Template:**

```
Map [customer type]'s journey with [product/service]:

Moment 1: Awareness - "I didn't know this problem existed"
- Generate 3 ideas for this moment: How do we create awareness?

Moment 2: Consideration - "I'm comparing options"
- Generate 3 ideas: How do we help them evaluate?

Moment 3: Decision - "I'm committing"
- Generate 3 ideas: How do we make decision easy?

Moment 4: Onboarding - "I'm getting started"
- Generate 3 ideas: How do we ensure success?

Moment 5: Value Realization - "I'm getting return on this"
- Generate 3 ideas: How do we amplify success?

Moment 6: Advocacy - "I'm telling others"
- Generate 3 ideas: How do we make them evangelize?

For EACH moment, consider:
- What does the customer actually need vs. what we think they need?
- What's the primary emotional state?
- What's the biggest friction point?
```

**Output Format:** Customer journey mapped with idea generation per moment; emotional state and friction identified per touchpoint

**Success Metric:** Identifies untapped moments where experiences can be improved; 70% of ideas from this pattern are incremental but high-impact

---

#### Pattern 14B: Empathy Persona Deep Dive

**Exact Prompt Template:**

```
Create a detailed empathy profile for [specific customer persona]:

1. Who are they? (Demographics, role, context)
2. What do they want? (Stated goals)
3. What do they NEED? (Unstated needs, problems they don't know they have)
4. What frustrates them? (Current experience problems)
5. What motivates them? (Incentives, aspirations)
6. What assumptions are they making? (How do they see the world?)
7. What would delight them? (Unexpected positive experiences)

Now, generate [number] product/service ideas that address their ACTUAL needs (not stated wants).

For EACH idea:
- How does it address unstated need?
- Why would it delight them specifically?
- How would they talk about it to peers?
```

**Concrete Example:**

```
Empathy profile for a new software engineer at a startup:

Who: 25-year-old, first tech job, wants to prove themselves
What they want: Learn quickly, ship features, get promoted
What they NEED: Psychological safety, mentorship, understanding of company politics
Frustrated by: Vague requirements, knowledge gaps, feeling like an imposter
Motivated by: Impact, learning, peer recognition
Assumptions: Senior engineers judge them constantly; they should know everything

Unstated need ideas:
1. "Reverse mentorship" tool where seniors ask juniors questions (empowerment + belonging)
2. "Confident commit" guide for common decisions (psychological safety)
3. [etc.]

Why would they spread these? Because they address the real source of anxiety, not just productivity.
```

**Output Format:** Empathy profile (detailed, 300+ words) | Ideas addressing unstated needs | How ideas create delight/advocacy

---
