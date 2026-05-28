# Decision Frameworks

## Patterns


---
  #### **Name**
Decision Classification
  #### **Description**
Categorizing decisions by type
  #### **When To Use**
Before any significant decision
  #### **Implementation**
    ## Decision Types
    
    ### 1. Reversibility Matrix
    
    | Type | Reversible? | Speed | Process |
    |------|-------------|-------|---------|
    | Type 1 | No/Hard | Slow | Full analysis |
    | Type 2 | Yes/Easy | Fast | Decide and learn |
    
    ```
    Type 1 (One-way doors):
    - Hard to reverse
    - High cost to undo
    - Examples: M&A, key hires, architecture
    
    Type 2 (Two-way doors):
    - Easy to reverse
    - Low cost to undo
    - Examples: Features, pricing, messaging
    
    Default: Treat as Type 2 unless proven Type 1.
    ```
    
    ### 2. Impact Assessment
    
    | Impact | Criteria |
    |--------|----------|
    | High | Affects strategy, customers, or >10% of resources |
    | Medium | Affects team, quarter goals, or 2-10% of resources |
    | Low | Affects day-to-day, individual work, <2% of resources |
    
    ### 3. Decision Framework Selection
    
    | Reversibility | Impact | Framework |
    |---------------|--------|-----------|
    | Hard | High | Full deliberation |
    | Hard | Medium | Structured analysis |
    | Easy | High | Quick deliberation |
    | Easy | Medium | Owner decides |
    | Easy | Low | Just decide |
    
    ### 4. Time Box by Type
    
    ```
    Decision time limits:
    
    Type 1 + High impact: 1-2 weeks max
    Type 1 + Medium impact: 3-5 days
    Type 2 + High impact: 1-3 days
    Type 2 + Medium impact: Same day
    Type 2 + Low impact: Now
    
    If taking longer, you're overthinking.
    ```
    

---
  #### **Name**
Decision Criteria Framework
  #### **Description**
Defining what matters
  #### **When To Use**
Clarifying decision criteria
  #### **Implementation**
    ## Defining Criteria
    
    ### 1. Criteria Identification
    
    ```
    Ask:
    - What would make this a success?
    - What would make this a failure?
    - What constraints must we honor?
    - What would we regret?
    
    List all factors, then prioritize.
    ```
    
    ### 2. Criteria Weighting
    
    | Category | Weight Range | Examples |
    |----------|--------------|----------|
    | Must-have | Pass/Fail | Legal compliance, safety |
    | Critical | 40-60% | Core business impact |
    | Important | 20-40% | Secondary benefits |
    | Nice-to-have | 0-20% | Marginal improvements |
    
    ### 3. Weighted Matrix
    
    ```
    Option Comparison:
    
    | Criteria | Weight | Option A | Option B | Option C |
    |----------|--------|----------|----------|----------|
    | Speed | 30% | 4 (1.2) | 3 (0.9) | 5 (1.5) |
    | Cost | 25% | 3 (0.75) | 5 (1.25) | 2 (0.5) |
    | Quality | 25% | 5 (1.25) | 3 (0.75) | 4 (1.0) |
    | Risk | 20% | 4 (0.8) | 4 (0.8) | 3 (0.6) |
    | Total | 100% | 4.0 | 3.7 | 3.6 |
    
    Note: Matrix informs, doesn't decide.
    ```
    
    ### 4. Criteria Validation
    
    ```
    Check your criteria:
    
    1. Are they independent? (Not double-counting)
    2. Are they measurable? (Can you score them?)
    3. Are they complete? (Covering what matters)
    4. Are they weighted honestly? (Not gamed)
    5. Would you accept the result?
    ```
    

---
  #### **Name**
Tradeoff Analysis
  #### **Description**
Understanding what you're giving up
  #### **When To Use**
When options have clear tradeoffs
  #### **Implementation**
    ## Analyzing Tradeoffs
    
    ### 1. Tradeoff Mapping
    
    ```
    For each option:
    
    What you GET:
    - [Benefit 1]
    - [Benefit 2]
    - [Benefit 3]
    
    What you GIVE UP:
    - [Cost 1]
    - [Cost 2]
    - [Cost 3]
    
    What you RISK:
    - [Risk 1]
    - [Risk 2]
    ```
    
    ### 2. Common Tradeoffs
    
    | Tradeoff | Dimension A | Dimension B |
    |----------|-------------|-------------|
    | Speed vs Quality | Launch faster | Launch better |
    | Control vs Scale | Manage tightly | Grow faster |
    | Simple vs Flexible | Easy to use | Handles edge cases |
    | Now vs Later | Immediate value | Future optionality |
    | Risk vs Reward | Safe bet | Big upside |
    
    ### 3. Regret Minimization
    
    ```
    Project forward:
    
    In 1 year, will I regret:
    - Not trying this?
    - Trying this?
    - Going slow?
    - Going fast?
    - The risk taken?
    - The risk not taken?
    
    Minimize regret, not risk.
    ```
    
    ### 4. Reversibility Check
    
    ```
    For each tradeoff:
    
    1. If wrong, can we reverse?
    2. How long until we know?
    3. What's the cost to reverse?
    4. What's the learning value?
    
    Reversible tradeoffs → bias toward action.
    Irreversible tradeoffs → bias toward caution.
    ```
    

---
  #### **Name**
Stakeholder Alignment
  #### **Description**
Getting buy-in efficiently
  #### **When To Use**
Decisions affecting multiple stakeholders
  #### **Implementation**
    ## Stakeholder Alignment
    
    ### 1. RACI for Decisions
    
    | Role | Definition |
    |------|------------|
    | Responsible | Does the work, makes recommendation |
    | Accountable | Makes final decision (ONE person) |
    | Consulted | Input required before decision |
    | Informed | Notified after decision |
    
    ```
    Rules:
    - Only ONE Accountable person
    - Minimize Consulted (slows decisions)
    - Be clear who's Responsible
    - Don't skip Informed
    ```
    
    ### 2. Alignment Process
    
    | Step | Action |
    |------|--------|
    | 1. Frame | Define decision and criteria |
    | 2. Consult | Gather input from C stakeholders |
    | 3. Propose | R makes recommendation |
    | 4. Decide | A makes decision |
    | 5. Communicate | Inform I stakeholders |
    
    ### 3. Handling Disagreement
    
    ```
    If stakeholders disagree:
    
    1. Clarify: Same facts?
    2. Explore: Different values?
    3. Surface: Hidden concerns?
    4. Decide: A makes call
    5. Commit: Everyone supports
    
    "Disagree and commit" > endless debate.
    ```
    
    ### 4. Decision Documentation
    
    ```
    Decision Record:
    
    Decision: [What was decided]
    Date: [When]
    Decider: [Who was Accountable]
    Context: [Why this decision was needed]
    Options: [What was considered]
    Rationale: [Why this option]
    Tradeoffs: [What was given up]
    Review: [When to revisit]
    ```
    

---
  #### **Name**
Decision Velocity
  #### **Description**
Making decisions faster
  #### **When To Use**
When decisions are taking too long
  #### **Implementation**
    ## Increasing Decision Speed
    
    ### 1. Speed Blockers
    
    | Blocker | Solution |
    |---------|----------|
    | Unclear owner | Assign one Accountable |
    | Too many opinions | Reduce Consulted |
    | Analysis paralysis | Time-box research |
    | Fear of wrong | Embrace reversibility |
    | Waiting for certainty | Accept uncertainty |
    
    ### 2. Decision Deadlines
    
    ```
    Set explicit deadlines:
    
    "We will decide by [date]"
    "If no decision by [date], default is [X]"
    "We have [time] to gather input"
    
    Deadlines force decisions.
    ```
    
    ### 3. Default Options
    
    ```
    Pre-set defaults:
    
    If we can't decide → do nothing (or)
    If we can't decide → do X
    If we can't decide → flip coin
    
    Having a default prevents stalling.
    ```
    
    ### 4. Good Enough Standard
    
    | Situation | Good Enough Threshold |
    |-----------|----------------------|
    | Reversible decision | 60% confidence |
    | High-learning decision | 50% confidence |
    | Irreversible decision | 80% confidence |
    | Low-stakes decision | Any preference |
    
    ```
    Perfectionism kills speed.
    Good enough now > perfect later.
    Learn from doing, not analyzing.
    ```
    

## Anti-Patterns


---
  #### **Name**
Analysis Paralysis
  #### **Description**
Over-analyzing instead of deciding
  #### **Why Bad**
    Decisions stall.
    Opportunities pass.
    Team frustrated.
    
  #### **What To Do Instead**
    Time-box analysis.
    Set decision deadlines.
    Embrace uncertainty.
    

---
  #### **Name**
Consensus Seeking
  #### **Description**
Waiting for everyone to agree
  #### **Why Bad**
    Slowest person sets pace.
    Decisions diluted.
    Accountability unclear.
    
  #### **What To Do Instead**
    Clear ownership.
    Disagree and commit.
    One decision maker.
    

---
  #### **Name**
Reversibility Blindness
  #### **Description**
Treating reversible decisions as permanent
  #### **Why Bad**
    Over-caution.
    Missed learning.
    Slow iteration.
    
  #### **What To Do Instead**
    Classify decision type first.
    Bias toward action for Type 2.
    Learn through doing.
    