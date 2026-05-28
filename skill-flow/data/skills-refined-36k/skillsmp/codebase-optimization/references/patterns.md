# Codebase Optimization

## Patterns


---
  #### **Name**
Strangler Fig
  #### **Description**
Gradually replace legacy system by routing traffic to new implementation
  #### **When**
Migrating from old system to new without big bang rewrite
  #### **Example**
    Phase 1: Build new auth module, route 1% traffic
    Phase 2: Monitor, fix issues, increase to 10%
    Phase 3: 50% traffic, compare behavior
    Phase 4: 100% traffic, old module retired
    Phase 5: Delete old code
    
    Benefits:
    - Always have working system
    - Gradual risk
    - Easy rollback
    

---
  #### **Name**
Characterization Testing
  #### **Description**
Document current behavior with tests before refactoring
  #### **When**
Refactoring code you don't fully understand
  #### **Example**
    // Before understanding the code, capture behavior
    test('calculatePrice current behavior', () => {
      expect(calculatePrice(100, 'premium')).toBe(85)
      expect(calculatePrice(100, 'basic')).toBe(100)
      expect(calculatePrice(0, 'premium')).toBe(0)
      expect(calculatePrice(-1, 'basic')).toBe(0) // Edge case!
    })
    
    // Now you know what to preserve when refactoring
    

---
  #### **Name**
Rule of Three
  #### **Description**
Don't abstract until you have three concrete examples
  #### **When**
Tempted to create abstraction from first use case
  #### **Example**
    1st occurrence: Just write the code
    2nd occurrence: Note the duplication
    3rd occurrence: NOW abstract the pattern
    
    "Duplication is far cheaper than the wrong abstraction"
    - Sandi Metz
    
    Signals of wrong abstraction:
    - Options/params growing
    - If/else for different cases
    - Callers working around it
    

---
  #### **Name**
Incremental Migration
  #### **Description**
Migrate systems piece by piece, never pause indefinitely
  #### **When**
Moving to new technology, database, or architecture
  #### **Example**
    Week 1: Migrate + remove Module A
    Week 2: Migrate + remove Module B
    Week 3: Migrate + remove Module C
    Week 4: Old system deleted
    
    Rules:
    - No new features on old system
    - Max 3 months for any migration
    - Timebox strictly
    - Track progress visibly
    

---
  #### **Name**
Optimization Loop
  #### **Description**
Measure, identify, validate, optimize, verify cycle
  #### **When**
Any performance work
  #### **Example**
    1. MEASURE: Profile the actual system
    2. IDENTIFY: Find the real bottleneck
    3. VALIDATE: Is it worth optimizing?
    4. OPTIMIZE: Make targeted change
    5. VERIFY: Measure improvement
    6. MONITOR: Watch for regressions
    
    Never skip step 1. Intuition about bottlenecks is often wrong.
    

## Anti-Patterns


---
  #### **Name**
Premature Optimization
  #### **Description**
Optimizing before measuring the actual problem
  #### **Why**
Wastes time, adds complexity, often makes things worse. Intuition is unreliable.
  #### **Instead**
Profile first. Target the 20% causing 80% of issues. Measure before and after.

---
  #### **Name**
Big Bang Rewrite
  #### **Description**
Rewriting large portions of codebase at once
  #### **Why**
70% fail or are abandoned. Take 3x longer than estimated. Team morale destroyed.
  #### **Instead**
Strangler fig pattern. Incremental migration. Small, bounded changes.

---
  #### **Name**
Optimization Without Tests
  #### **Description**
Refactoring without adequate test coverage
  #### **Why**
No safety net. Edge cases break. Don't know what you broke.
  #### **Instead**
Write characterization tests first. Test covers behavior before and after.

---
  #### **Name**
Premature Abstraction
  #### **Description**
Creating abstractions before patterns emerge
  #### **Why**
Wrong abstraction is worse than duplication. Harder to change later.
  #### **Instead**
Wait for three concrete examples. Extract, don't predict.

---
  #### **Name**
Optimization Coupling
  #### **Description**
Breaking module boundaries for performance
  #### **Why**
Trades future velocity for current speed. Technical debt with interest.
  #### **Instead**
Optimize within boundaries. Cache at interfaces, not internals.

---
  #### **Name**
Optimizing Vanity Metrics
  #### **Description**
Optimizing metrics that don't represent real user experience
  #### **Why**
Numbers improve while users suffer. Average hides tail latency.
  #### **Instead**
Use percentiles (p95, p99). Measure real users. Time to interactive, not load time.