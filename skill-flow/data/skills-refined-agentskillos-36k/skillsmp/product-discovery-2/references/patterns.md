# Product Discovery

## Patterns


---
  #### **Name**
Opportunity Assessment
  #### **Description**
Evaluating what problems are worth solving
  #### **When To Use**
Deciding what to explore
  #### **Implementation**
    ## Opportunity Assessment Framework
    
    ### 1. Opportunity Solution Tree
    
    ```
    Desired Outcome (business goal)
    └── Opportunity 1 (customer problem)
        ├── Solution A
        ├── Solution B
        └── Solution C
    └── Opportunity 2
        └── ...
    └── Opportunity 3
        └── ...
    ```
    
    ### 2. Opportunity Evaluation Criteria
    
    | Criterion | Question | Score (1-5) |
    |-----------|----------|-------------|
    | Frequency | How often does problem occur? | |
    | Intensity | How painful is the problem? | |
    | Willingness | Would they pay/switch? | |
    | Reach | How many customers affected? | |
    | Alignment | Does it serve our strategy? | |
    
    ### 3. Opportunity Sizing
    
    ```
    Market Opportunity =
      (Customers affected) ×
      (Frequency of problem) ×
      (Willingness to pay/switch)
    ```
    
    **Quick Sizing**
    - How many customers have this problem?
    - How often do they encounter it?
    - What's their current workaround?
    - How much time/money do they lose?
    
    ### 4. ICE Scoring
    
    | Factor | Definition | Score |
    |--------|------------|-------|
    | Impact | If solved, how big is the impact? | 1-10 |
    | Confidence | How sure are we this is real? | 1-10 |
    | Ease | How easy to solve? | 1-10 |
    
    Score = (Impact × Confidence × Ease) / 10
    
    ### 5. Opportunity Prioritization Matrix
    
    ```
               High Impact
                   │
       ┌───────────┼───────────┐
       │ Quick wins│ Big bets  │
       │           │           │
     Low──────────────────────High Effort
       │ Maybe     │ Avoid     │
       │ later     │           │
       └───────────┼───────────┘
               Low Impact
    ```
    

---
  #### **Name**
Customer Interview Mastery
  #### **Description**
Learning from customers effectively
  #### **When To Use**
Understanding customer problems
  #### **Implementation**
    ## Customer Interview Framework
    
    ### 1. Interview Types
    
    | Type | Purpose | When |
    |------|---------|------|
    | Exploratory | Understand problem space | Early discovery |
    | Evaluative | Test solutions | After ideation |
    | Continuous | Maintain understanding | Ongoing (weekly) |
    
    ### 2. Interview Structure
    
    ```
    Opening (2 min)
    - Thank them
    - Set expectations
    - Permission to record
    
    Context (5 min)
    - Their role
    - Their environment
    - Typical day/workflow
    
    Story (15 min)
    - Specific recent experience
    - What happened
    - What was hard
    
    Deep Dive (10 min)
    - Explore interesting threads
    - "Tell me more about..."
    - Uncover root causes
    
    Close (3 min)
    - Summary of what you heard
    - Next steps if any
    - Thank you
    ```
    
    ### 3. Question Types
    
    **DO Ask**
    - "Tell me about the last time you..."
    - "Walk me through how you..."
    - "What was the hardest part?"
    - "How do you currently handle..."
    - "What happened next?"
    
    **DON'T Ask**
    - "Would you use a product that..."
    - "Do you like this feature?"
    - "How much would you pay for..."
    - Leading questions
    - Yes/no questions
    
    ### 4. The Mom Test
    
    ```
    Rules from Rob Fitzpatrick:
    
    1. Talk about their life, not your idea
    2. Ask about specifics in the past
    3. Talk less, listen more
    4. Look for commitment/advancement
    5. Facts > opinions
    ```
    
    ### 5. Interview Note Template
    
    ```
    Date:
    Customer:
    Context:
    
    Key Problems Mentioned:
    1.
    2.
    3.
    
    Current Solutions/Workarounds:
    
    Interesting Quotes:
    -
    
    Surprises:
    
    Follow-up Questions:
    ```
    
    ### 6. Interview Volume
    
    | Confidence Level | Interviews Needed |
    |------------------|-------------------|
    | Directional | 5-8 |
    | Solid understanding | 12-15 |
    | High confidence | 20+ |
    | Quantitative validation | 50+ |
    

---
  #### **Name**
Assumption Mapping
  #### **Description**
Identifying and testing risky assumptions
  #### **When To Use**
Before building anything significant
  #### **Implementation**
    ## Assumption Testing Framework
    
    ### 1. Assumption Categories
    
    ```
    Desirability: Will customers want it?
    Viability: Can we make money?
    Feasibility: Can we build it?
    Usability: Can customers use it?
    ```
    
    ### 2. Assumption Mapping
    
    ```
               High Importance
                   │
       ┌───────────┼───────────┐
       │ Known     │ Test      │
       │ facts     │ ASAP      │
       │           │           │
     Low──────────────────────High Risk
       │ Ignore    │ Monitor   │
       │           │           │
       └───────────┼───────────┘
               Low Importance
    ```
    
    ### 3. Assumption Template
    
    | Assumption | Evidence | Risk | Test |
    |------------|----------|------|------|
    | Users want X | None | High | Customer interviews |
    | We can build Y | Team assessment | Medium | Spike |
    | Market pays $Z | Competitor pricing | Low | Pricing page test |
    
    ### 4. Testing Methods
    
    | Assumption Type | Test Method |
    |-----------------|-------------|
    | Problem exists | Customer interviews |
    | Frequency matters | Usage logs, surveys |
    | Will pay | Pricing page, pre-sales |
    | Can use it | Prototype testing |
    | Will adopt | Pilot, beta |
    
    ### 5. Riskiest Assumption Test (RAT)
    
    ```
    1. List all assumptions
    2. Rank by: Risk × Importance
    3. Identify #1 riskiest
    4. Design minimal test
    5. Run test, learn
    6. Repeat
    ```
    
    ### 6. Evidence Strength
    
    | Evidence | Strength |
    |----------|----------|
    | Someone paid | Very strong |
    | Clear commitment | Strong |
    | Behavior change | Strong |
    | Stated intent | Medium |
    | Opinion | Weak |
    | Assumption | None |
    

---
  #### **Name**
Continuous Discovery Habits
  #### **Description**
Making discovery a habit, not a phase
  #### **When To Use**
Establishing ongoing discovery practice
  #### **Implementation**
    ## Continuous Discovery
    
    ### 1. Weekly Cadence
    
    ```
    Minimum Viable Discovery:
    
    Every week:
    - 1 customer touchpoint (interview, observation)
    - Review usage data
    - Update opportunity map
    - Share learnings with team
    
    Time: ~3-4 hours/week
    ```
    
    ### 2. Discovery Types by Week
    
    | Week | Focus |
    |------|-------|
    | Week 1 | Customer interviews (problem) |
    | Week 2 | Prototype testing (solution) |
    | Week 3 | Data analysis (behavior) |
    | Week 4 | Synthesis and planning |
    
    ### 3. Discovery Touchpoints
    
    **Interview Opportunities**
    - Recent sign-ups
    - Recent churns
    - Power users
    - New segment entrants
    - Support ticket authors
    
    **Observation Opportunities**
    - Session recordings
    - Support calls
    - Sales calls
    - Customer meetings
    
    ### 4. Discovery Rituals
    
    **Weekly Discovery Share**
    - 15-minute team meeting
    - "Here's what we learned"
    - "Here's what we're testing"
    - Anyone can share insights
    
    **Monthly Discovery Synthesis**
    - Pattern recognition
    - Opportunity map update
    - Priority recalibration
    
    ### 5. Discovery-Delivery Balance
    
    ```
    Ratio by team phase:
    
    Early product: 70% discovery / 30% delivery
    Growing product: 40% discovery / 60% delivery
    Mature product: 20% discovery / 80% delivery
    
    Never 0% discovery.
    ```
    
    ### 6. Discovery Artifacts
    
    | Artifact | Purpose | Update Frequency |
    |----------|---------|------------------|
    | Opportunity map | Visualize problem space | Weekly |
    | Interview repository | Store learnings | After each interview |
    | Assumption tracker | Track risks | Weekly |
    | Customer personas | Understand segments | Monthly |
    

---
  #### **Name**
Prototype Testing
  #### **Description**
Testing solutions before building
  #### **When To Use**
Validating solution ideas
  #### **Implementation**
    ## Prototype Testing
    
    ### 1. Prototype Fidelity Levels
    
    | Level | Fidelity | Time to Build | Best For |
    |-------|----------|---------------|----------|
    | Paper | Very low | Minutes | Concept testing |
    | Wireframe | Low | Hours | Flow testing |
    | Interactive | Medium | Days | Usability testing |
    | Functional | High | Weeks | Feasibility + value |
    
    ### 2. What to Test
    
    **Concept Testing (Paper/Verbal)**
    - Does this resonate?
    - Do they understand it?
    - Would they want it?
    
    **Usability Testing (Interactive)**
    - Can they use it?
    - Where do they struggle?
    - What confuses them?
    
    **Value Testing (Functional)**
    - Does it solve the problem?
    - Is it better than current solution?
    - Would they switch?
    
    ### 3. Prototype Testing Script
    
    ```
    Setup:
    - This is a prototype, not finished
    - Thinking out loud helps
    - No wrong answers
    
    Task:
    - "Imagine you want to [goal]..."
    - "Show me how you'd do that"
    - Observe silently
    
    Debrief:
    - "What worked well?"
    - "What was confusing?"
    - "How does this compare to your current way?"
    ```
    
    ### 4. Sample Size
    
    | Test Type | Users Needed | Rationale |
    |-----------|--------------|-----------|
    | Usability | 5 | Find 80% of issues |
    | Concept | 8-12 | Pattern recognition |
    | Preference | 20+ | Reliable comparison |
    
    ### 5. Quick Prototype Tools
    
    | Need | Tools |
    |------|-------|
    | Wireframes | Balsamiq, Whimsical |
    | Interactive | Figma, Framer |
    | Functional | Webflow, no-code |
    | Fake door | Landing page |
    

## Anti-Patterns


---
  #### **Name**
Discovery Theater
  #### **Description**
Going through motions without learning
  #### **Why Bad**
    Wastes time without reducing risk.
    Creates false confidence.
    Check-the-box mentality.
    
  #### **What To Do Instead**
    Focus on genuine learning.
    Ask hard questions.
    Let evidence change your mind.
    

---
  #### **Name**
Confirmation Bias
  #### **Description**
Seeking evidence that confirms beliefs
  #### **Why Bad**
    Misses disconfirming evidence.
    Leads to building wrong thing.
    Wastes resources.
    
  #### **What To Do Instead**
    Seek disconfirming evidence.
    Ask "what would prove us wrong?"
    Listen for surprises.
    

---
  #### **Name**
Skipping to Solutions
  #### **Description**
Jumping to solutions before understanding problems
  #### **Why Bad**
    Solves wrong problems.
    Misses better solutions.
    Features without value.
    
  #### **What To Do Instead**
    Spend time in problem space.
    Generate multiple solutions.
    Test before building.
    

---
  #### **Name**
Discovery Phase Ending
  #### **Description**
Treating discovery as a phase that ends
  #### **Why Bad**
    Customer understanding decays.
    Market changes missed.
    Product-market fit erodes.
    
  #### **What To Do Instead**
    Continuous discovery habits.
    Weekly customer touchpoints.
    Never stop learning.
    

---
  #### **Name**
Only Asking Power Users
  #### **Description**
Research limited to existing heavy users
  #### **Why Bad**
    Misses acquisition blockers.
    Biased toward current patterns.
    Ignores potential customers.
    
  #### **What To Do Instead**
    Interview across user lifecycle.
    Include non-users and churned.
    Seek diverse perspectives.
    