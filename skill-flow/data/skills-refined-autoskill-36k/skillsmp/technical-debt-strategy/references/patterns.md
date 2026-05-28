# Technical Debt Strategy

## Patterns


---
  #### **Name**
Debt Registry
  #### **Description**
Maintain centralized tracking of all known technical debt
  #### **When**
Managing debt across growing codebase
  #### **Example**
    # tech-debt.md or issue tracker
    ## High Interest (Address This Quarter)
    - Auth system: No session invalidation on password change
      - Interest: 2hrs/week debugging ghost sessions
      - Payoff: 1 week refactor
      - Risk: Security incident
    
    ## Medium Interest (Address Next Quarter)
    - API client: No retry logic
      - Interest: 1hr/week handling timeouts
      - Payoff: 3 days
    

---
  #### **Name**
Boy Scout Refactoring
  #### **Description**
Improve code incrementally while working on related features
  #### **When**
Touching code with known debt during feature work
  #### **Example**
    # In feature branch
    1. Implement feature
    2. Refactor touched code (types, tests, naming)
    3. Commit separately: feat + refactor commits
    4. Debt paydown happens organically
    
    # Don't: block feature for unrelated refactor
    # Do: improve what you touch
    

---
  #### **Name**
Debt Impact Measurement
  #### **Description**
Quantify how debt slows velocity in business terms
  #### **When**
Prioritizing debt or requesting time for refactor
  #### **Example**
    Current state:
    - New features in auth: 5 days → 8 days (60% overhead)
    - Bugs per sprint touching auth: 3 avg
    - Developer satisfaction: 3/10
    
    After refactor:
    - New features: 5 days (baseline)
    - Bugs: 1 avg (↓66%)
    - Dev satisfaction: 7/10
    

---
  #### **Name**
Strangler Fig Pattern
  #### **Description**
Incrementally replace system by routing to new alongside old
  #### **When**
Large system needs replacement but cannot stop for rewrite
  #### **Example**
    1. Build new system alongside old
    2. Route 1% traffic to new (shadow mode)
    3. Compare outputs, fix discrepancies
    4. Gradually shift: 10% → 50% → 100%
    5. Remove old system
    
    # Enables: rollback at any point, learning in production
    

---
  #### **Name**
Debt Sprint Planning
  #### **Description**
Reserve capacity each sprint for debt paydown
  #### **When**
Preventing debt from accumulating unchecked
  #### **Example**
    Sprint capacity: 10 days
    - New features: 7 days (70%)
    - Debt paydown: 2 days (20%)
    - Bugs/support: 1 day (10%)
    
    # Prevents: debt compound, emergency refactors
    # Enables: sustainable velocity
    

---
  #### **Name**
Deprecation Roadmap
  #### **Description**
Phase out old APIs/patterns with clear timeline
  #### **When**
Replacing deprecated code with better pattern
  #### **Example**
    Phase 1 (Week 1): Announce deprecation
      - Add warnings to old API
      - Document migration path
      - Migration script available
    
    Phase 2 (Weeks 2-4): Support both
      - New code uses new API
      - Migrate high-value paths
    
    Phase 3 (Week 5): Remove old API
      - Breaking change, major version bump
    

## Anti-Patterns


---
  #### **Name**
Debt denial
  #### **Description**
Refusing to acknowledge shortcuts were taken
  #### **Example**
No tracking of known issues, pretending codebase is clean
  #### **Why Bad**
Debt compounds silently. Team knows, leadership surprised.
  #### **Fix**
Track all known debt. Regular debt reviews. Honest assessment.

---
  #### **Name**
Big bang rewrite
  #### **Description**
Starting from scratch to solve debt problems
  #### **Example**
Rewriting entire system because it has debt
  #### **Why Bad**
Rewrites usually take 2-3x longer. New system has new debt.
  #### **Fix**
Incremental migration. Strangler fig pattern. Prove value continuously.

---
  #### **Name**
Perfectionist paralysis
  #### **Description**
Refusing to ship anything with debt
  #### **Example**
Endless refactoring before features, gold-plating everything
  #### **Why Bad**
Shipping is learning. Perfect code for wrong product is waste.
  #### **Fix**
Ship with intentional debt. Track it. Pay it back when validated.

---
  #### **Name**
All debt is equal thinking
  #### **Description**
Not prioritizing which debt matters
  #### **Example**
Refactoring rarely-touched code while core paths are fragile
  #### **Why Bad**
Limited time. Some debt costs more interest than others.
  #### **Fix**
Prioritize by interest rate (pain frequency x severity).

---
  #### **Name**
Debt as excuse
  #### **Description**
Blaming debt for all problems when execution is the issue
  #### **Example**
We cannot ship anything because tech debt
  #### **Why Bad**
Teams always have some debt. High performers ship anyway.
  #### **Fix**
Distinguish real blockers from preferences. Ship incrementally.

---
  #### **Name**
Debt as Permanent State
  #### **Description**
Accepting debt as normal, never paying it down
  #### **Why**
Compounds until velocity approaches zero, no new features possible
  #### **Instead**
    Intentional debt has payback plan and timeline.
    Track interest cost. Pay down highest interest first.
    Reserve sprint capacity for debt reduction.
    

---
  #### **Name**
The Perfect Rewrite Fantasy
  #### **Description**
Planning to rewrite entire system "the right way"
  #### **Why**
Rewrites take 3x longer, new system has new debt, users suffer
  #### **Instead**
    Incremental migration (Strangler Fig).
    Extract and replace one component at a time.
    Prove value continuously, not after 6 months.
    

---
  #### **Name**
Refactor Without Business Case
  #### **Description**
Cannot articulate why refactor matters to product/business
  #### **Why**
Gets deprioritized, seen as developer preference
  #### **Instead**
    Translate to velocity: "Enables 2x faster shipping"
    Translate to risk: "Prevents 3am outages"
    Translate to revenue: "Unblocks enterprise feature"
    

---
  #### **Name**
Debt in Dark
  #### **Description**
Team knows about debt but leadership does not
  #### **Why**
No support for paying it down, resentment builds
  #### **Instead**
    Transparent debt tracking visible to leadership.
    Regular debt review in sprint planning.
    Communicate impact in business terms.
    

---
  #### **Name**
All or Nothing Thinking
  #### **Description**
Code must be perfect or is considered debt
  #### **Why**
Perfectionism prevents shipping, creates unnecessary refactors
  #### **Instead**
    Good enough is good enough.
    Optimize for change, not perfection.
    Debt is shortcuts with known tradeoffs, not imperfect code.
    

---
  #### **Name**
Copy-Paste Over Abstraction
  #### **Description**
Duplicating code to avoid touching fragile abstraction
  #### **Why**
Workarounds accumulate, problem gets worse, paralysis sets in
  #### **Instead**
    Tackle root cause: fix or replace fragile abstraction.
    Workarounds are interest payments. Track them.
    When interest exceeds principal, pay principal.
    