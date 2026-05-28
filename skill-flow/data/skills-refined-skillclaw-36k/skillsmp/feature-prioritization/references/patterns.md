# Feature Prioritization

## Patterns


---
  #### **Name**
Prioritization Framework Selection
  #### **Description**
Choosing the right framework for the decision
  #### **When To Use**
Any prioritization decision
  #### **Implementation**
    ## Framework Selection Guide
    
    ### 1. Framework Overview
    
    | Framework | Best For | Key Factors |
    |-----------|----------|-------------|
    | RICE | Feature prioritization | Reach, Impact, Confidence, Effort |
    | ICE | Experiments | Impact, Confidence, Ease |
    | Value/Effort | Quick decisions | 2x2 matrix |
    | MoSCoW | Scope decisions | Must, Should, Could, Won't |
    | Kano | Customer satisfaction | Delighters, Performers, Basics |
    | Weighted Scoring | Complex decisions | Custom criteria |
    | Cost of Delay | Time-sensitive | Urgency and value decay |
    
    ### 2. RICE Framework
    
    ```
    Score = (Reach × Impact × Confidence) / Effort
    
    Reach: # of customers affected per quarter
    Impact: 3 = massive, 2 = high, 1 = medium, 0.5 = low
    Confidence: 100% = high, 80% = medium, 50% = low
    Effort: Person-months of work
    ```
    
    **Example**
    | Feature | Reach | Impact | Conf | Effort | Score |
    |---------|-------|--------|------|--------|-------|
    | Feature A | 5000 | 2 | 80% | 3 | 2667 |
    | Feature B | 2000 | 3 | 100% | 1 | 6000 |
    
    ### 3. Impact/Effort Matrix
    
    ```
               High Impact
                   │
       ┌───────────┼───────────┐
       │ Quick     │ Major     │
       │ Wins      │ Projects  │
       │ (Do now)  │ (Plan)    │
     Low──────────────────────High Effort
       │ Fill-ins  │ Avoid     │
       │ (Maybe)   │ (No)      │
       └───────────┼───────────┘
               Low Impact
    ```
    
    ### 4. Cost of Delay
    
    ```
    CD3 = Cost of Delay / Duration
    
    Cost of Delay includes:
    - Revenue lost per week
    - Customer churn risk
    - Competitive risk
    - Compliance deadlines
    
    Prioritize highest CD3 first.
    ```
    
    ### 5. Kano Model
    
    | Category | Effect on Satisfaction |
    |----------|------------------------|
    | Basic | Expected; absence causes dissatisfaction |
    | Performance | More is better, linear |
    | Delighter | Unexpected positive surprise |
    
    **Prioritization Rule**
    Basic > Performance > Delighter (usually)
    
    ### 6. When to Use What
    
    | Situation | Framework |
    |-----------|-----------|
    | Quarterly planning | RICE |
    | Sprint decisions | Value/Effort |
    | Release scoping | MoSCoW |
    | Growth experiments | ICE |
    | Time-sensitive | Cost of Delay |
    | Complex trade-offs | Weighted Scoring |
    

---
  #### **Name**
Roadmap Communication
  #### **Description**
Creating and communicating roadmaps
  #### **When To Use**
Planning and stakeholder alignment
  #### **Implementation**
    ## Roadmap Best Practices
    
    ### 1. Roadmap Types
    
    | Type | Audience | Timeframe | Detail |
    |------|----------|-----------|--------|
    | Now/Next/Later | Internal | 3-6 months | Low |
    | Theme-based | Leadership | 6-12 months | Themes, not features |
    | Feature-based | Delivery team | 1-3 months | High |
    | Portfolio | C-suite | 12+ months | Strategic bets |
    
    ### 2. Now/Next/Later Framework
    
    ```
    NOW (Committed)
    - Currently building
    - High confidence
    - Specific scope
    
    NEXT (Planned)
    - Coming soon
    - Medium confidence
    - May change
    
    LATER (Exploring)
    - Under consideration
    - Low confidence
    - Will change
    ```
    
    ### 3. Roadmap Content
    
    **Include**
    - Outcomes/goals, not just features
    - Strategic context (why)
    - Dependencies if critical
    - Confidence levels
    
    **Exclude**
    - Fixed dates (use timeframes)
    - Everything (be selective)
    - Implementation details
    - Commitments beyond capacity
    
    ### 4. Roadmap Presentation
    
    ```
    For each initiative:
    
    [Theme Name]
    Goal: What outcome we're driving
    Why now: Why this is prioritized
    Approach: High-level how
    Success: How we'll measure
    Confidence: High/Medium/Low
    ```
    
    ### 5. Roadmap Cadence
    
    | Activity | Frequency |
    |----------|-----------|
    | Internal review | Weekly |
    | Team update | Every sprint |
    | Stakeholder share | Monthly |
    | Major revision | Quarterly |
    
    ### 6. Managing Roadmap Requests
    
    ```
    When stakeholder requests addition:
    
    1. Understand the problem
    2. Assess against criteria
    3. Show trade-offs ("What would we deprioritize?")
    4. Decide transparently
    5. Document decision
    ```
    

---
  #### **Name**
Stakeholder Alignment
  #### **Description**
Getting buy-in on priorities
  #### **When To Use**
Planning cycles and priority changes
  #### **Implementation**
    ## Stakeholder Management
    
    ### 1. Stakeholder Mapping
    
    ```
               High Influence
                   │
       ┌───────────┼───────────┐
       │ Keep      │ Manage    │
       │ Satisfied │ Closely   │
       │           │           │
     Low──────────────────────High Interest
       │ Monitor   │ Keep      │
       │           │ Informed  │
       └───────────┼───────────┘
               Low Influence
    ```
    
    ### 2. Input Collection
    
    **Before Planning**
    - 1:1 conversations with key stakeholders
    - Input request form for structured feedback
    - Review business metrics and goals
    
    **During Planning**
    - Draft prioritization (PM-led)
    - Review with key stakeholders
    - Incorporate feedback
    - Finalize and share
    
    ### 3. Priority Disagreement
    
    ```
    When stakeholders disagree:
    
    1. Ensure shared understanding of goals
    2. Make criteria explicit
    3. Show data/evidence
    4. Clarify trade-offs
    5. Escalate if needed (with recommendation)
    ```
    
    ### 4. Saying No
    
    **The "No" Framework**
    ```
    "I understand [their goal].
     Here's why [alternative/no]:
     [Evidence/reasoning].
     What I'd suggest instead:
     [Alternative approach]."
    ```
    
    **Types of No**
    - Not now (prioritize later)
    - Not this way (different solution)
    - Not at all (doesn't fit strategy)
    
    ### 5. Communication Plan
    
    | Stakeholder | What They Need | Frequency |
    |-------------|----------------|-----------|
    | Executives | Strategic alignment | Monthly |
    | Sales | What's coming for customers | Monthly |
    | Support | Upcoming changes | Every release |
    | Engineering | Clear priorities | Weekly |
    

---
  #### **Name**
Backlog Management
  #### **Description**
Keeping backlog healthy and useful
  #### **When To Use**
Ongoing backlog hygiene
  #### **Implementation**
    ## Backlog Best Practices
    
    ### 1. Backlog Structure
    
    ```
    Backlog Tiers:
    
    Tier 1: Now (This sprint)
    - Fully refined
    - Ready to build
    - Clear acceptance criteria
    
    Tier 2: Next (Next 1-2 sprints)
    - Mostly refined
    - Scope understood
    - Needs detail
    
    Tier 3: Later (3+ sprints)
    - Rough idea
    - Needs discovery
    - May not happen
    ```
    
    ### 2. Backlog Grooming
    
    **Weekly Grooming**
    - Review Tier 1 readiness
    - Refine Tier 2 items
    - Promote/demote between tiers
    
    **Monthly Cleanup**
    - Archive stale items (6+ months untouched)
    - Re-prioritize Tier 3
    - Remove duplicates
    
    **Quarterly Purge**
    - Aggressive cleanup
    - Challenge everything in Tier 3
    - Align with roadmap
    
    ### 3. Backlog Size
    
    ```
    Healthy backlog size:
    - Tier 1: 2-3 sprints of work
    - Tier 2: 3-6 sprints of work
    - Tier 3: Minimal (ideas, not items)
    
    Total refined items: < 8-10 sprints
    
    Bigger = unmaintainable and demoralizing
    ```
    
    ### 4. Feature Request Handling
    
    ```
    Request comes in:
    
    1. Capture (don't lose it)
    2. Categorize (problem, feature, bug)
    3. Initial assess (quick value/effort)
    4. Merge if duplicate
    5. Decide: Tier 1/2/3 or Archive
    6. Communicate decision to requestor
    ```
    
    ### 5. Backlog Health Metrics
    
    | Metric | Healthy |
    |--------|---------|
    | Items added/week | Stable, not growing |
    | Items completed/week | ≥ Items added |
    | Avg age of Tier 3 | < 6 months |
    | % items refined | Tier 1: 100%, Tier 2: 70% |
    

---
  #### **Name**
Trade-off Analysis
  #### **Description**
Making difficult prioritization decisions
  #### **When To Use**
Hard either/or decisions
  #### **Implementation**
    ## Trade-off Decision Framework
    
    ### 1. Trade-off Types
    
    | Trade-off | Example |
    |-----------|---------|
    | Speed vs Quality | Ship fast with debt vs wait for solid |
    | Breadth vs Depth | More features vs better features |
    | Short vs Long term | Quick win vs strategic investment |
    | Revenue vs Retention | New sales vs existing customers |
    
    ### 2. Trade-off Analysis Template
    
    ```
    Decision: [Feature A vs Feature B]
    
    Option A:
    - Benefits: [list]
    - Risks: [list]
    - Opportunity cost: [what we give up]
    
    Option B:
    - Benefits: [list]
    - Risks: [list]
    - Opportunity cost: [what we give up]
    
    Recommendation: [choice]
    Reasoning: [why]
    Reversibility: [how hard to change later]
    ```
    
    ### 3. Reversibility Principle
    
    ```
    Easy to reverse (type 2 decisions):
    - Decide quickly
    - Bias toward action
    - Learn and adjust
    
    Hard to reverse (type 1 decisions):
    - Take more time
    - Gather more input
    - Be more deliberate
    ```
    
    ### 4. Opportunity Cost Thinking
    
    Every yes is a no to something else.
    
    Ask: "What are we not doing by doing this?"
    
    Make trade-offs explicit, not hidden.
    
    ### 5. Decision Documentation
    
    ```
    Decision Log Entry:
    
    Date:
    Decision:
    Options considered:
    Evidence used:
    Trade-offs accepted:
    Decision maker:
    Review date:
    ```
    

## Anti-Patterns


---
  #### **Name**
Priority Everything
  #### **Description**
Everything is high priority
  #### **Why Bad**
    If everything is priority, nothing is.
    Team overwhelmed.
    Nothing gets done well.
    
  #### **What To Do Instead**
    Force rank ruthlessly.
    Accept trade-offs.
    Focus on top 3-5.
    

---
  #### **Name**
HIPPO Prioritization
  #### **Description**
Highest Paid Person's Opinion wins
  #### **Why Bad**
    Not evidence-based.
    Team disempowered.
    Often wrong.
    
  #### **What To Do Instead**
    Data-informed decisions.
    Framework-based prioritization.
    Transparent criteria.
    

---
  #### **Name**
Feature Factory
  #### **Description**
Shipping features without measuring outcomes
  #### **Why Bad**
    No learning.
    Backlog never shrinks.
    Value not validated.
    
  #### **What To Do Instead**
    Outcome-focused roadmaps.
    Measure feature impact.
    Celebrate outcomes, not output.
    

---
  #### **Name**
Infinite Backlog
  #### **Description**
Backlog that only grows
  #### **Why Bad**
    Demoralizing.
    Unmaintainable.
    Full of stale items.
    
  #### **What To Do Instead**
    Regular backlog cleanup.
    Aggressive archiving.
    Small, focused backlog.
    

---
  #### **Name**
Roadmap Promises
  #### **Description**
Treating roadmap as commitments
  #### **Why Bad**
    Reduces agility.
    Sets false expectations.
    Punishes learning.
    
  #### **What To Do Instead**
    Roadmaps are plans, not promises.
    Communicate confidence levels.
    Update when learning requires.
    