# Scope Creep Defense - Sharp Edges

## Death By Additions

### **Id**
death-by-additions
### **Summary**
Project dies from accumulated small additions
### **Severity**
high
### **Situation**
Endless "tiny" requests kill the project
### **Why**
  Each addition seems small.
  Nobody tracks total impact.
  Deadline stays fixed.
  
### **Solution**
  ## Death by a Thousand Additions
  
  ### The Accumulation Problem
  
  ```
  Day 1: "This is a 2-week project"
  
  Week 1: "Just add login" (+3 days)
  Week 2: "Also need export" (+2 days)
  Week 3: "One more field" (+1 day)
  Week 4: "Small UI tweak" (+1 day)
  Week 5: "Quick integration" (+3 days)
  
  Reality: 2-week project → 5 weeks
  ```
  
  ### Tracking Total Impact
  
  | Metric | Track |
  |--------|-------|
  | Original scope | Days estimated |
  | Additions | Running total of +days |
  | Current scope | Original + additions |
  | Deadline delta | Current scope - original |
  
  ### Making Additions Visible
  
  ```
  FOR EVERY REQUEST:
  
  "This adds [X days] to our timeline.
   We're now at [Y days] total additions.
   Original deadline is now [Z] behind.
  
   Do we adjust deadline or cut something?"
  ```
  
  ### The Addition Budget
  
  | Rule | Why |
  |------|-----|
  | 10% buffer | For legitimate additions |
  | Trade-off required | No free additions |
  | Weekly audit | Surface total impact |
  | Deadline sacred | Or explicitly moved |
  
### **Symptoms**
  - Deadline slipping repeatedly
  - "Just one more" pattern
  - Team overtime
  - Quality suffering
### **Detection Pattern**
just add|quick addition|while you're there|one more

## Stakeholder Hijack

### **Id**
stakeholder-hijack
### **Summary**
Powerful stakeholder derails project
### **Severity**
high
### **Situation**
Executive request overrides everything
### **Why**
  Hard to say no to power.
  "Urgent" trumps "important."
  Political dynamics.
  
### **Solution**
  ## Handling Executive Requests
  
  ### The Reality
  
  ```
  When an executive says "add X":
  
  - They may not know the trade-offs
  - They often think it's simpler than it is
  - They may forget they asked
  - But ignoring them is risky
  ```
  
  ### The Response Framework
  
  | Step | Action |
  |------|--------|
  | 1. Acknowledge | "I understand this is important to you" |
  | 2. Clarify | "Let me make sure I understand what you need" |
  | 3. Impact | "Here's what this would mean for [project]" |
  | 4. Options | "We could A, B, or C" |
  | 5. Document | "Let me send you a summary for approval" |
  
  ### Making Trade-offs Visible
  
  ```
  EMAIL TEMPLATE:
  
  Subject: [Request] - Impact Assessment
  
  You requested: [X]
  
  Impact on current project:
  - Timeline: +[Y] weeks
  - What gets delayed: [Z]
  
  Options:
  A. Add it, delay launch by [Y] weeks
  B. Add it, cut [other feature]
  C. Add it to v2
  
  Please confirm your preference.
  ```
  
  ### The Paper Trail
  
  | Always | Why |
  |--------|-----|
  | Email confirmation | Proof of request |
  | Impact documented | No surprise later |
  | Decision recorded | Accountability |
  | Shared with team | Transparency |
  
### **Symptoms**
  - Surprise requirements
  - CEO said so
  - No documentation
  - Team confused
### **Detection Pattern**
exec wants|urgent request|priority change|from leadership

## Requirements Churn

### **Id**
requirements-churn
### **Summary**
Requirements change faster than development
### **Severity**
high
### **Situation**
Can't finish anything because specs keep changing
### **Why**
  No decision finality.
  Customer or stakeholder uncertainty.
  Fear of commitment.
  
### **Solution**
  ## Stopping Requirements Churn
  
  ### Freeze Windows
  
  ```
  DEFINE FREEZE PERIODS:
  
  ┌─────────────────────────────────────────┐
  │ Sprint 1 │ FREEZE │ Sprint 2 │ FREEZE  │
  └──────────┴────────┴──────────┴─────────┘
        ↑                    ↑
     Changes          Changes
     collected        collected
     for Sprint 2     for Sprint 3
  ```
  
  ### The Commitment Point
  
  | Stage | Flexibility |
  |-------|-------------|
  | Discovery | High - explore options |
  | Design | Medium - refine approach |
  | Development | Low - only critical |
  | Testing | Minimal - bugs only |
  | Release | None - frozen |
  
  ### Churn Cost Visibility
  
  ```
  When requirements change mid-sprint:
  
  "This change will:
   - Throw away [X hours] of work
   - Add [Y hours] of rework
   - Risk [Z] quality issues
  
   If we wait for next sprint:
   - No work thrown away
   - Full planning time
   - Higher quality result"
  ```
  
  ### Root Cause Address
  
  | Symptom | Real Problem | Fix |
  |---------|--------------|-----|
  | "We didn't think of X" | Incomplete discovery | Better upfront work |
  | "Customer changed mind" | No commitment | Get sign-off |
  | "We learned something" | Valid learning | Plan for it |
  | "Exec wants change" | Political | See stakeholder pattern |
  
### **Symptoms**
  - Rework every sprint
  - Never finishing features
  - Team frustration
  - Specs always changing
### **Detection Pattern**
requirements changed|new direction|actually|pivot

## Gold Plating

### **Id**
gold-plating
### **Summary**
Team adds unrequested features
### **Severity**
medium
### **Situation**
Developers building more than asked
### **Why**
  Perfectionism.
  "While I'm in there."
  Interesting > important.
  
### **Solution**
  ## Preventing Gold Plating
  
  ### What It Looks Like
  
  ```
  ASKED FOR:
  - Login button
  
  DELIVERED:
  - Login button
  - Remember me checkbox
  - Social login options
  - Password strength meter
  - Forgot password flow
  - Two-factor auth
  
  "But it's better this way!"
  (Also: 3 weeks late)
  ```
  
  ### Definition of Done
  
  | Instead of | Use |
  |------------|-----|
  | "Done when good" | Checklist of requirements |
  | "Complete" | Specific acceptance criteria |
  | "Finished" | Story points/scope document |
  
  ### The Question Test
  
  ```
  Before adding anything:
  
  "Is this in the requirements?"
  
  NO → Create new ticket
       Do not add
       Stay focused
  ```
  
  ### Culture Shift
  
  | Old Mindset | New Mindset |
  |-------------|-------------|
  | More is better | Focused is better |
  | Anticipate needs | Respond to needs |
  | Complete solution | Minimum viable |
  | Perfect | Shippable |
  
### **Symptoms**
  - Features nobody asked for
  - Taking longer than estimated
  - Scope creep from within
  - I added a few things
### **Detection Pattern**
while I was there|also added|thought it would be nice|bonus