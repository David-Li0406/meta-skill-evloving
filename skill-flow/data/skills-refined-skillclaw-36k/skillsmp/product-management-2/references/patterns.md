# Product Management

## Patterns


---
  #### **Name**
Jobs-to-be-Done Framework
  #### **Description**
Define features by the job users are trying to accomplish, not solutions
  #### **When**
Writing PRDs or prioritizing features
  #### **Example**
    Bad: "Users want a calendar integration"
    Good: "When planning their week, users need to see deadlines alongside meetings
    so they can allocate time realistically"
    
    Job statement format:
    When [situation], I want to [motivation], so I can [outcome]
    
    Benefits: Reveals real problem, opens solution space, focuses on outcome
    

---
  #### **Name**
RICE Prioritization
  #### **Description**
Score features by Reach, Impact, Confidence, Effort for objective ranking
  #### **When**
Prioritizing roadmap with multiple competing features
  #### **Example**
    Feature: Bulk editing
    - Reach: 2,000 users per quarter
    - Impact: 2 (moderate improvement, 0.5-3 scale)
    - Confidence: 80% (based on user research)
    - Effort: 4 person-weeks
    
    RICE Score = (2000 × 2 × 0.8) / 4 = 800
    
    Compare scores across features. Forces explicit reasoning about each dimension.
    Especially useful when stakeholders disagree on priorities
    

---
  #### **Name**
Working Backwards (Amazon)
  #### **Description**
Write press release and FAQ before building to clarify customer value
  #### **When**
Starting major feature or product initiative
  #### **Example**
    1. Write press release announcing the feature
       - What problem does it solve?
       - Who is it for?
       - What makes it different?
       - Customer quote showing value
    
    2. Write FAQ answering:
       - Why build this?
       - What alternatives exist?
       - How does it work?
       - What are the risks?
    
    Forces clarity on customer value before investing in solution.
    Bad ideas become obvious when you try to write the press release
    

---
  #### **Name**
Opportunity Solution Trees
  #### **Description**
Map user problems to solution ideas to ensure you're solving the right thing
  #### **When**
Doing discovery work or defining feature strategy
  #### **Example**
    Outcome: Increase activation rate from 40% to 60%
    └─ Opportunity: Users don't understand core value proposition
       ├─ Solution: Interactive onboarding tutorial
       ├─ Solution: Video explainer on signup
       └─ Solution: Better landing page messaging
    └─ Opportunity: Setup process is too complex
       ├─ Solution: Reduce required fields
       ├─ Solution: Allow skip and complete later
       └─ Solution: Import from existing tools
    
    Ensures you explore multiple opportunities and solutions before committing.
    Prevents jumping to solutions before understanding problem space
    

---
  #### **Name**
One-Way vs Two-Way Doors
  #### **Description**
Categorize decisions by reversibility to determine deliberation level
  #### **When**
Deciding how much process a decision needs
  #### **Example**
    Two-way doors (reversible, ship fast):
    - Changing button copy
    - Trying new onboarding flow (with feature flag)
    - Adjusting pricing for new customers only
    
    One-way doors (hard to reverse, deliberate):
    - Database architecture
    - Public API contracts
    - Removing features users depend on
    
    Two-way doors: Ship with minimal review, iterate based on data
    One-way doors: Get alignment, write RFC, deliberate carefully
    

---
  #### **Name**
North Star + Input Metrics
  #### **Description**
Define one outcome metric and the inputs that drive it
  #### **When**
Setting up metrics for a product area or feature
  #### **Example**
    North Star: Weekly Active Teams (value delivered)
    
    Input metrics (what drives North Star):
    - New team sign-ups (acquisition)
    - Activation rate (getting to first value)
    - Feature adoption rate (depth of usage)
    - Invite rate (viral growth)
    
    Track inputs weekly, north star monthly. Inputs are levers you can pull.
    If north star stagnates, diagnose which input is broken
    

## Anti-Patterns


---
  #### **Name**
Feature Factory
  #### **Description**
Shipping features without validating they solve user problems
  #### **Why**
    Teams measure output (features shipped) not outcomes (problems solved).
    Roadmap becomes list of feature requests. Success = shipping, not impact.
    Users get bloated product that does nothing well
    
  #### **Instead**
    Measure outcomes (retention, engagement, revenue) not output (features shipped).
    Before adding to roadmap, validate: What problem? How do we know? What's success?
    Kill features that don't move outcome metrics
    

---
  #### **Name**
Opinion-Driven Roadmap
  #### **Description**
Building what the loudest stakeholder wants without validation
  #### **Why**
    HiPPO (Highest Paid Person's Opinion) drives decisions. Features based on
    "I think users want..." or "Our CEO wants...". Results in features nobody uses
    
  #### **Instead**
    Require evidence: user research, data, or experiment results. When stakeholder
    requests feature, ask: "What problem? What evidence? What does success look like?"
    Build culture where conviction requires evidence
    

---
  #### **Name**
Scope Creep Acceptance
  #### **Description**
Letting features grow beyond original scope without re-prioritization
  #### **When**
During implementation, "while we're at it" additions accumulate
  #### **Why**
    Ship date slips. Complexity increases. Testing burden grows. Bug risk rises.
    Original feature vision gets lost in complexity
    
  #### **Instead**
    Define scope in PRD with clear MVP. When new requirements emerge, add to backlog
    for next iteration, don't extend current scope. Protect the ship date. Ship MVPs
    

---
  #### **Name**
Metric Maximization
  #### **Description**
Optimizing for single metric without considering broader impact
  #### **Why**
    "Increase sign-ups" → Growth hacks that attract wrong users → Retention tanks
    "Increase engagement" → Addictive patterns → User trust erodes
    Single metric focus creates unintended consequences
    
  #### **Instead**
    Use North Star + guardrail metrics. Optimize primary metric while ensuring
    secondary metrics don't degrade. Example: Increase sign-ups while maintaining
    activation rate and day-7 retention thresholds
    

---
  #### **Name**
Consensus-Driven Decisions
  #### **Description**
Requiring everyone to agree before making decisions
  #### **Why**
    Lowest common denominator features. Speed drops to pace of slowest stakeholder.
    Bold ideas get watered down. Product becomes forgettable
    
  #### **Instead**
    PM owns decision after gathering input. Stakeholders give input, PM synthesizes
    and decides. Disagree and commit culture. Speed over consensus
    

---
  #### **Name**
Requirements as Solutions
  #### **Description**
Writing PRDs that specify the solution instead of the problem
  #### **Why**
    Removes design and engineering from problem-solving. Misses better solutions.
    Team becomes order-takers instead of collaborators
    
  #### **Instead**
    PRD should define: problem, users affected, success metrics, constraints.
    Leave solution space open for design/eng to explore. Best products come from
    cross-functional collaboration on solutions
    