# Feature Prioritization - Sharp Edges

## Framework Worship

### **Id**
framework-worship
### **Summary**
Over-relying on prioritization formulas
### **Severity**
medium
### **Situation**
Prioritization score doesn't match intuition
### **Why**
  Frameworks are tools, not truth.
  Garbage in, garbage out.
  Strategic context matters.
  
### **Solution**
  ## Balanced Framework Use
  
  ### Framework Limitations
  
  ```
  RICE score is only as good as:
  - Your reach estimates
  - Your impact guesses
  - Your confidence calibration
  - Your effort predictions
  
  All of these are uncertain.
  ```
  
  ### Framework + Judgment
  
  | Framework Says | But Consider |
  |----------------|--------------|
  | High score | Strategic fit? Timing? Dependencies? |
  | Low score | Hidden strategic value? Customer signal? |
  | Tie | What does gut say? Why? |
  
  ### When to Override
  
  ```
  Override framework when:
  - Strategic importance not captured
  - Market timing critical
  - Customer relationship at stake
  - Clear blocker to other priorities
  - Intuition strongly disagrees (investigate why)
  ```
  
  ### Calibration Practice
  
  | Check | Frequency |
  |-------|-----------|
  | Estimates vs actuals | Every quarter |
  | Framework results vs outcomes | Every quarter |
  | Where overrides happened | Monthly |
  
  ### Framework as Discussion Tool
  
  Best use of frameworks:
  - Structure the discussion
  - Surface assumptions
  - Enable comparison
  - NOT: auto-generate priority list
  
### **Symptoms**
  - But the score says...
  - Strategic items deprioritized
  - Framework gaming
### **Detection Pattern**
RICE|ICE|framework score

## Stakeholder Whiplash

### **Id**
stakeholder-whiplash
### **Summary**
Priorities changing constantly
### **Severity**
high
### **Situation**
Team can't finish anything due to shifting priorities
### **Why**
  No clear decision process.
  Everyone can reprioritize.
  Leadership changes mind.
  
### **Solution**
  ## Priority Stability
  
  ### Stability Rules
  
  ```
  Commitment Windows:
  - Sprint: Locked (no changes except emergency)
  - Month: Stable (rare changes)
  - Quarter: Mostly stable (roadmap items)
  
  Changes require:
  - Clear business reason
  - Trade-off acknowledged
  - Team informed properly
  ```
  
  ### Change Request Process
  
  ```
  Priority change request:
  
  1. Requestor fills out form:
     - What's changing
     - Why (business impact)
     - What to deprioritize
     - Urgency
  
  2. Review against criteria
  3. Decide with trade-off explicit
  4. Communicate to team
  5. Document in decision log
  ```
  
  ### Change Thresholds
  
  | Impact | Can Be Done By | Process |
  |--------|----------------|---------|
  | Minor (within sprint) | PM | Inform team |
  | Medium (roadmap item) | PM + stakeholders | Review meeting |
  | Major (strategy shift) | Leadership | Planning revision |
  
  ### Tracking Churn
  
  ```
  Measure:
  - # of priority changes per sprint
  - # of interrupted initiatives
  - Scope added mid-sprint
  
  Target: < 2 priority changes per quarter
  ```
  
  ### Push Back Template
  
  "I understand the urgency of [new request].
   If we do this now, we'd need to stop [current work].
   The trade-off is [consequences].
   Are you comfortable with that trade-off?"
  
### **Symptoms**
  - Multiple pivots per sprint
  - Nothing gets completed
  - Team frustration
### **Detection Pattern**
priority change|urgent|stop and switch

## Loudest Voice Wins

### **Id**
loudest-voice-wins
### **Summary**
Prioritizing based on who asks loudest
### **Severity**
high
### **Situation**
Squeaky wheel gets the grease
### **Why**
  Path of least resistance.
  Avoiding conflict.
  No objective criteria.
  
### **Solution**
  ## Objective Prioritization
  
  ### Make Criteria Explicit
  
  ```
  Published prioritization criteria:
  
  1. Strategic alignment (weight: 30%)
  2. Customer impact (weight: 25%)
  3. Revenue impact (weight: 20%)
  4. Effort required (weight: 15%)
  5. Urgency (weight: 10%)
  
  Anyone can understand how decisions are made.
  ```
  
  ### Request vs Priority
  
  | What They Say | What to Assess |
  |---------------|----------------|
  | "Urgent!" | What's the actual deadline? |
  | "Critical customer!" | Revenue at stake? Evidence? |
  | "Everyone wants this!" | How many? How badly? |
  | "Competitors have it!" | Do customers care? |
  
  ### Evidence Requirements
  
  ```
  To prioritize, requestor provides:
  
  - Problem statement
  - Affected customers (how many)
  - Business impact (quantified)
  - Current workaround
  - Urgency reason
  
  No evidence = no prioritization change
  ```
  
  ### Fairness Perception
  
  Even if you can't make everyone happy:
  - Process is transparent
  - Criteria are published
  - Decisions are explained
  - Anyone can see reasoning
  
  ### Pushing Back on Loud Voices
  
  "I hear the urgency. Help me understand:
   - How many customers affected?
   - What's the business impact?
   - What happens if we wait?"
  
### **Symptoms**
  - Same stakeholders always win
  - Quiet teams never get priority
  - Decisions feel political
### **Detection Pattern**
escalation|urgent|important stakeholder

## Ignoring Strategic Fit

### **Id**
ignoring-strategic-fit
### **Summary**
Prioritizing only by immediate value
### **Severity**
medium
### **Situation**
Roadmap is all quick wins, no strategic investment
### **Why**
  Short-term bias.
  Easier to justify.
  Pressure for immediate results.
  
### **Solution**
  ## Strategic Balance
  
  ### Investment Allocation
  
  ```
  Typical healthy balance:
  
  70% - Sustaining (current product/customers)
  20% - Strategic (future bets)
  10% - Exploration (learning, experiments)
  
  Adjust based on company stage.
  ```
  
  ### Strategic Project Protection
  
  ```
  Strategic initiatives get:
  - Protected time allocation
  - Longer measurement window
  - Different success criteria
  - Leadership sponsorship
  
  Don't compete with tactical on same criteria.
  ```
  
  ### Portfolio View
  
  | Category | This Quarter | Next Quarter |
  |----------|--------------|--------------|
  | Sustaining | [list] | [list] |
  | Strategic | [list] | [list] |
  | Exploration | [list] | [list] |
  
  Check: Is strategic getting attention?
  
  ### Avoiding Strategic Drift
  
  Monthly check:
  - Are strategic initiatives progressing?
  - Have they been deprioritized?
  - Is the balance right?
  
  ### Long-term vs Short-term Framing
  
  | Decision | Short-term | Long-term |
  |----------|------------|-----------|
  | [Feature X] | Low impact | Platform value |
  | [Feature Y] | High impact | Dead end |
  
  Include long-term view in evaluation.
  
### **Symptoms**
  - All tactical, no strategic
  - Strategic initiatives keep slipping
  - No progress on big bets
### **Detection Pattern**
strategic|long-term|investment

## Scope Creep

### **Id**
scope-creep
### **Summary**
Features growing beyond original scope
### **Severity**
medium
### **Situation**
Simple feature becomes complex project
### **Why**
  Good ideas added.
  Edge cases discovered.
  Stakeholders add requirements.
  
### **Solution**
  ## Scope Control
  
  ### Scope Definition Upfront
  
  ```
  Feature Brief includes:
  
  IN SCOPE:
  - [Specific functionality]
  - [Specific functionality]
  
  OUT OF SCOPE:
  - [Explicitly excluded]
  - [Explicitly excluded]
  
  SUCCESS CRITERIA:
  - [Measurable outcome]
  ```
  
  ### Scope Change Process
  
  ```
  When scope addition requested:
  
  1. Assess size (trivial, small, significant)
  2. Trivial: PM decides, informs
  3. Small: Team discusses impact
  4. Significant: Separate initiative or trade-off
  
  Never just add without considering impact.
  ```
  
  ### MVP Discipline
  
  ```
  For each feature, ask:
  - What's the smallest thing that delivers value?
  - What can we learn before building more?
  - What can we add later if successful?
  
  Version 1 < Version 2 < Version 3
  ```
  
  ### Scope Creep Signals
  
  | Signal | Response |
  |--------|----------|
  | "While we're here..." | "Separate item, prioritize later" |
  | "Just one more thing..." | "What do we cut instead?" |
  | "Edge case X..." | "Handle separately if significant" |
  
  ### Time-Boxing
  
  Alternative to scope control:
  - Fix time (2 weeks)
  - Flex scope (build what fits)
  - Ship, then iterate
  
### **Symptoms**
  - Estimates keep growing
  - Just one more thing
  - Features never ship
### **Detection Pattern**
scope|add|also want