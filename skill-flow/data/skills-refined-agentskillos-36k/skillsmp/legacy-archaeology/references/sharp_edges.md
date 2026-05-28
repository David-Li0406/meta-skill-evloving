# Legacy Archaeology - Sharp Edges

## Chesterton Fence

### **Id**
chesterton-fence
### **Summary**
Removing code without understanding why it exists
### **Severity**
high
### **Situation**
"Dead code" turned out to be critical
### **Why**
  Didn't understand the context.
  Tested in wrong conditions.
  Edge case not obvious.
  
### **Solution**
  ## The Chesterton's Fence Rule
  
  ### The Principle
  
  ```
  "Don't remove a fence until you understand
  why it was put there."
  
  That weird code might be:
  - Handling an edge case
  - Workaround for a bug
  - Critical for specific users
  - Protection against race condition
  ```
  
  ### Before Removing
  
  | Step | Action |
  |------|--------|
  | 1. Git blame | Who wrote it, when, why |
  | 2. Search issues | Related bugs/tickets |
  | 3. Check tests | What does it protect |
  | 4. Ask around | Tribal knowledge |
  | 5. Monitor | Add logging before removing |
  
  ### Safe Removal Process
  
  ```
  1. ADD LOGGING
     Log when this code runs
     Wait one release cycle
  
  2. ANALYZE
     Does it ever run?
     What conditions trigger it?
  
  3. FEATURE FLAG
     Disable but don't remove
     Enable quick rollback
  
  4. REMOVE
     Only after monitoring shows safe
  ```
  
  ### Common "Dead Code" Traps
  
  | Looks Like | Actually Is |
  |------------|-------------|
  | Never called | Called via reflection |
  | Old feature | Used by one big customer |
  | Commented out | Needed for specific config |
  | Unused variable | Prevents garbage collection |
  
### **Symptoms**
  - Cleaned up dead code, broke production
  - Edge case failures
  - But that never runs!
  - Rollback after removal
### **Detection Pattern**
remove|dead code|unused|clean up

## Lost Context

### **Id**
lost-context
### **Summary**
Knowledge walks out the door
### **Severity**
high
### **Situation**
Original developers gone, no documentation
### **Why**
  No knowledge transfer.
  Documentation not prioritized.
  Tribal knowledge only.
  
### **Solution**
  ## Preserving and Recovering Knowledge
  
  ### When People Leave
  
  ```
  BEFORE THEY GO:
  
  □ Record their knowledge
  □ Document their systems
  □ Pair with replacement
  □ Write ADRs for decisions
  □ Create runbooks
  ```
  
  ### Knowledge Recovery
  
  | Source | Method |
  |--------|--------|
  | Git history | Read commit messages |
  | PR discussions | Search closed PRs |
  | Slack archives | Search by system name |
  | Email | Forward rules |
  | Old wikis | Check for snapshots |
  | The code | It's the source of truth |
  
  ### Building Knowledge Base
  
  ```
  AS YOU LEARN:
  
  1. Document in the repo (not wiki)
  2. Write "why" not "what"
  3. Link to related code
  4. Update when wrong
  5. Make discoverable
  ```
  
  ### Knowledge Mapping
  
  | System | Owner | Backup | Docs |
  |--------|-------|--------|------|
  | Auth | Alice | Bob | /docs/auth.md |
  | Payments | Bob | ? | None (risk!) |
  | Reports | Gone | ? | None (risk!) |
  
### **Symptoms**
  - Nobody knows how this works
  - Fear of changing certain systems
  - Single point of knowledge
  - Onboarding takes months
### **Detection Pattern**
nobody knows|only X knows|afraid to touch

## Wrong Assumptions

### **Id**
wrong-assumptions
### **Summary**
Assuming based on code appearance
### **Severity**
medium
### **Situation**
Behavior different from what code suggests
### **Why**
  Runtime vs static analysis.
  Configuration changes behavior.
  External state matters.
  
### **Solution**
  ## Validating Understanding
  
  ### Verify, Don't Assume
  
  ```
  DON'T:
  "This function returns X" (from reading)
  
  DO:
  "This function returns X" (from running)
  ```
  
  ### Validation Techniques
  
  | Method | When |
  |--------|------|
  | Add logging | Production behavior |
  | Write test | Specific hypothesis |
  | Debugger | Step through |
  | Trace request | Full flow |
  
  ### Common Wrong Assumptions
  
  | Assumption | Reality |
  |------------|---------|
  | Default value | Config overrides |
  | Dead path | Feature flagged on |
  | Sync call | Actually async |
  | Always runs | Conditional skip |
  | Simple logic | Inherited complexity |
  
  ### The Hypothesis Approach
  
  ```
  1. FORM HYPOTHESIS
     "I think X does Y"
  
  2. DESIGN TEST
     "If true, then Z should happen"
  
  3. RUN TEST
     Add log, run scenario
  
  4. VERIFY OR UPDATE
     Either confirmed or learned something
  ```
  
  ### Trust Ladder
  
  | Confidence | Source |
  |------------|--------|
  | Low | Reading code |
  | Medium | Reading tests |
  | High | Running tests |
  | Very High | Production logs |
  
### **Symptoms**
  - I thought it did X
  - Unexpected behavior
  - Works in test, fails in prod
  - Missing configuration
### **Detection Pattern**
thought|assumed|should have|expected

## Change Fear

### **Id**
change-fear
### **Summary**
Afraid to modify legacy code
### **Severity**
medium
### **Situation**
Code is frozen due to fear
### **Why**
  Unknown consequences.
  No tests.
  Previous changes broke things.
  
### **Solution**
  ## Safe Legacy Changes
  
  ### The Safety Net
  
  ```
  BEFORE CHANGING:
  
  1. Characterization tests
     - Test current behavior
     - Even if behavior is "wrong"
  
  2. Monitoring
     - Add metrics/logs
     - Baseline before change
  
  3. Feature flags
     - Toggle new vs old
     - Easy rollback
  
  4. Small changes
     - One thing at a time
     - Easy to debug
  ```
  
  ### Characterization Test Pattern
  
  ```javascript
  // Document current behavior, don't judge
  describe('CHARACTERIZATION: legacyFunction', () => {
    test('given X, returns Y', () => {
      // This documents reality, not intent
      const result = legacyFunction(X);
      expect(result).toBe(Y);
    });
  });
  ```
  
  ### Safe Modification Steps
  
  | Step | Purpose |
  |------|---------|
  | 1. Add test | Lock current behavior |
  | 2. Add logging | See actual usage |
  | 3. Small refactor | Improve readability |
  | 4. Feature flag | Safe toggle |
  | 5. Change | Actual modification |
  | 6. Monitor | Watch for regression |
  
  ### When to NOT Change
  
  | Signal | Action |
  |--------|--------|
  | Works, not understood | Document first |
  | Critical, no tests | Add tests first |
  | Being replaced soon | Leave it |
  | High risk, low value | Skip |
  
### **Symptoms**
  - Don't touch that
  - Code never updated
  - Fear of deployment
  - Workarounds instead of fixes
### **Detection Pattern**
don't touch|afraid|scary|we don't change