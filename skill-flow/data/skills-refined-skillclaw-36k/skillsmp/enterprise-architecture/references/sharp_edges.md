# Enterprise Architecture - Sharp Edges

## Ivory Tower Architecture

### **Id**
ivory-tower-architecture
### **Severity**
high
### **Summary**
Architecture team disconnected from development reality
### **Symptoms**
  - Architecture documents nobody follows
  - Developers work around official architecture
  - No feedback loop from implementation
### **Why**
  When architects sit separate from delivery teams, they create designs
  based on theoretical ideals rather than practical constraints. Teams
  ignore impractical mandates and create shadow architectures.
  
### **Gotcha**
  "The Enterprise Architecture team has mandated a 6-month review
   cycle for all technology decisions. Meanwhile, we need to ship
   in 2 weeks."
  
  # Teams will just ignore the process and accumulate tech debt!
  
### **Solution**
  1. Embed architects in delivery teams:
     - Rotate architects through product teams
     - Architects write code sometimes
     - Attend standups and retros
  
  2. Lightweight governance:
     - Self-service architecture review templates
     - Async reviews for standard patterns
     - Reserve sync reviews for novel decisions
  
  3. Feedback loops:
     - Track actual vs. intended architecture
     - Post-mortems inform future guidance
     - Architecture debt is visible
  

## Big Bang Transformation Failure

### **Id**
big-bang-transformation
### **Severity**
critical
### **Summary**
Attempting to replace everything at once leads to project failure
### **Symptoms**
  - Multi-year transformation timeline
  - All-or-nothing migration approach
  - No intermediate value delivery
### **Why**
  Large transformations fail because requirements change during execution,
  key people leave, budgets get cut, and complexity compounds. The longer
  the timeline, the higher the failure probability.
  
### **Gotcha**
  "We'll spend 18 months building the new platform, then migrate
   everything over a weekend. The old system will be decommissioned
   Monday."
  
  # Never works! Something always goes wrong at cutover.
  
### **Solution**
  1. Strangler Fig pattern:
     - Route specific traffic to new system
     - Incrementally migrate features
     - Old and new coexist during transition
  
  2. Define intermediate architectures:
     - Transition State 1: Core migrated
     - Transition State 2: Integrations migrated
     - Target State: Legacy decommissioned
  
  3. Measure progress:
     - Traffic percentage on new system
     - Feature parity checklist
     - Value delivered at each stage
  

## Bounded Context Violations

### **Id**
context-boundary-violation
### **Severity**
high
### **Summary**
Sharing databases or models across domain boundaries
### **Symptoms**
  - Multiple teams modifying same database tables
  - Shared library with domain logic
  - Changes in one domain break another
### **Why**
  When bounded contexts share implementation details, they become
  coupled. Changes require coordination across teams. This slows
  development and increases the risk of breaking changes.
  
### **Gotcha**
  "We'll just add a column to the customers table. The other team
   uses it too, but they'll be fine."
  
  # They won't be fine! Their queries will break.
  
### **Solution**
  1. Clear context boundaries:
     - Each context owns its data
     - Integration via events or APIs
     - No shared databases
  
  2. Anti-corruption layer:
     - Translate between context models
     - Don't leak internal structure
     - Version integration contracts
  
  3. Context mapping:
     - Document relationships between contexts
     - Define integration patterns
     - Assign ownership
  

## Architecture Review Bottleneck

### **Id**
governance-bottleneck
### **Severity**
high
### **Summary**
All decisions require architecture board approval
### **Symptoms**
  - Long wait times for architecture review
  - Teams waiting on approval to proceed
  - Architecture board overwhelmed
### **Why**
  Centralized review creates bottlenecks. Teams queue for approval
  while competitors ship. Eventually teams bypass the process entirely,
  defeating the purpose of governance.
  
### **Gotcha**
  "All technology decisions must go through the Architecture Review
   Board, which meets monthly."
  
  # Teams waiting 4-6 weeks for approval! They'll just do it anyway.
  
### **Solution**
  1. Tiered governance:
     - Tier 1: Team decides (standard patterns)
     - Tier 2: Architect advises (minor deviations)
     - Tier 3: ARB approves (novel or risky)
  
  2. Pre-approved patterns:
     - Reference architectures for common cases
     - Technology radar with recommended defaults
     - Self-service compliance checks
  
  3. Asynchronous review:
     - ADR (Architecture Decision Record) review
     - Comment period instead of meetings
     - Escalate only on objection
  