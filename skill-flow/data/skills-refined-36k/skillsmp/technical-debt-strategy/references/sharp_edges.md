# Technical Debt Strategy - Sharp Edges

## Invisible Debt

### **Id**
invisible-debt
### **Summary**
Debt that exists but is not tracked anywhere
### **Severity**
high
### **Situation**
  Codebase has known issues. Everyone knows but nobody wrote them down.
  New engineer joins. Makes same mistakes. Debt compounds. Nobody has
  a complete picture.
  
### **Why**
  Untracked debt is forgotten debt. Until it breaks. Then it is urgent
  debt. Tracking makes debt visible, prioritizable, payable.
  
### **Solution**
  Debt tracking system:
  
  1. Debt register (spreadsheet, tickets, or dedicated tool)
  2. For each item: location, description, impact, estimated effort
  3. Regular review (monthly debt review meeting)
  4. Prioritization based on interest rate (pain x frequency)
  
  If it is not tracked, it does not exist for planning purposes.
  
### **Symptoms**
  - Known issues not documented
  - Same problems surprise the team repeatedly
  - No debt backlog
  - Cannot estimate debt impact
### **Detection Pattern**


## All Debt Equal

### **Id**
all-debt-equal
### **Summary**
Treating all technical debt as equally important
### **Severity**
high
### **Situation**
  50 items in debt backlog. Team picks randomly or by who complained
  loudest. Critical debt ignored while nice-to-fix debt gets attention.
  
### **Why**
  Debt has different interest rates. Some debt costs hours daily. Some
  costs minutes monthly. Paying down low-interest debt first is poor
  capital allocation.
  
### **Solution**
  Interest rate prioritization:
  
  For each debt item calculate:
  - Frequency: How often does this cause pain? (daily/weekly/monthly)
  - Severity: How much time lost per occurrence?
  - Risk: What is the worst case if this breaks?
  
  Interest = Frequency x Severity + Risk factor
  
  Pay highest interest first.
  
### **Symptoms**
  - Random debt prioritization
  - Low-impact items getting fixed
  - High-impact items neglected
  - No prioritization framework
### **Detection Pattern**


## Big Bang Rewrite

### **Id**
big-bang-rewrite
### **Summary**
Attempting complete rewrite instead of incremental improvement
### **Severity**
critical
### **Situation**
  System has debt. Leadership approves full rewrite. 18 months later,
  new system finally ships - with its own debt. Business lost 18 months
  of iteration.
  
### **Why**
  Rewrites almost always take longer than expected. New system has new
  problems. Business cannot wait 18 months. Incremental improvement is
  almost always better.
  
### **Solution**
  Strangler fig pattern:
  
  1. Identify the worst part of the system
  2. Build new version of just that part
  3. Route traffic to new version
  4. Repeat for next worst part
  5. Gradually strangle old system
  
  Value delivered continuously. Risk reduced. Learning incorporated.
  
### **Symptoms**
  - Proposing full rewrites
  - Long timelines with no incremental value
  - New system to replace old
  - No incremental migration path
### **Detection Pattern**


## Debt Denial

### **Id**
debt-denial
### **Summary**
Pretending the codebase has no significant debt
### **Severity**
high
### **Situation**
  Leadership asks about technical debt. Team says everything is fine.
  Actually everyone knows there are problems. One day production breaks
  badly. Shocked leadership, defensive team.
  
### **Why**
  Denial does not eliminate debt. It just makes it invisible until crisis.
  Honest assessment enables planning. Surprises destroy trust.
  
### **Solution**
  Regular debt audits:
  
  1. Engineering team rates codebase health honestly (1-10 per area)
  2. Document known issues without judgment
  3. Present to leadership with business impact
  4. Agree on acceptable debt level
  5. Review quarterly
  
  Transparency enables planning, denial enables disaster.
  
### **Symptoms**
  - Leadership unaware of debt
  - Team hiding known issues
  - Surprises when things break
  - No honest health assessment
### **Detection Pattern**


## Perfectionist Paralysis

### **Id**
perfectionist-paralysis
### **Summary**
Refusing to ship anything with technical debt
### **Severity**
high
### **Situation**
  Every feature needs to be perfect. Refactoring before shipping.
  Competitors ship in weeks, we ship in months. Market window closes.
  
### **Why**
  Strategic debt is a competitive advantage. Shipping fast with known
  shortcuts beats shipping slow with none. Pay it back when validated,
  not before.
  
### **Solution**
  Intentional debt approach:
  
  1. Ship with clearly documented shortcuts
  2. Track them in debt register
  3. Define payback trigger (validation, scale, stability need)
  4. Payback only when trigger hit
  
  Debt is a tool, not a sin. Use it wisely.
  
### **Symptoms**
  - Refactoring before validation
  - Slow shipping speed
  - Perfect code for unvalidated features
  - Fear of technical debt
### **Detection Pattern**


## Pure Refactor Sprints

### **Id**
pure-refactor-sprints
### **Summary**
Dedicated sprints for refactoring with no feature value
### **Severity**
medium
### **Situation**
  One sprint is all refactoring. Product team frustrated. Two weeks pass
  with no visible progress. Refactoring regresses some behavior. Users
  unhappy.
  
### **Why**
  Pure refactor sprints lack context and accountability. Refactoring
  works best when attached to features that need the refactored code.
  Value is visible. Context is clear.
  
### **Solution**
  Refactor in context:
  
  1. Boy Scout Rule: Leave code better than you found it
  2. Attach refactoring to features that touch the area
  3. Small continuous improvement beats big isolated sprints
  4. Visible feature value alongside invisible debt paydown
  
### **Symptoms**
  - Dedicated refactoring sprints
  - No feature output for weeks
  - Regression from out-of-context changes
  - Product team frustration
### **Detection Pattern**


## Debt As Excuse

### **Id**
debt-as-excuse
### **Summary**
Using technical debt as excuse for not delivering
### **Severity**
high
### **Situation**
  Team cannot deliver anything on time. Reason given is always technical
  debt. Actually, other teams with similar debt are shipping. Debt is
  real, but it is also an excuse.
  
### **Why**
  All teams have debt. High performers ship anyway. Debt can be both
  real impediment and convenient excuse. Distinguishing requires honesty.
  
### **Solution**
  Honest assessment:
  
  1. What specifically is blocked by debt?
  2. What would we need to fix to unblock?
  3. Is there a workaround while we fix?
  4. Are we asking for fixes before validation?
  
  Debt is real, but shipping is still possible. Find the way.
  
### **Symptoms**
  - Cannot ship anything due to debt
  - Similar teams with similar debt are shipping
  - Debt blamed for all problems
  - No incremental path forward
### **Detection Pattern**


## Invisible Interest Payments

### **Id**
invisible-interest-payments
### **Summary**
Not tracking time spent working around debt
### **Severity**
medium
### **Situation**
  Team spends 20% of time on workarounds. Nobody tracks it. Cannot
  justify debt paydown. Feels like everything takes forever but unclear
  why.
  
### **Why**
  Interest payments are invisible unless tracked. Without data, cannot
  justify investment in paydown. Track workaround time to make the case.
  
### **Solution**
  Interest tracking:
  
  1. When working around a known issue, note time spent
  2. Aggregate by issue weekly
  3. Calculate monthly cost of each debt item
  4. Use data to prioritize paydown
  
  If workarounds cost 2 days/sprint, 2-week fix is paid back in 2 sprints.
  
### **Symptoms**
  - Cannot quantify debt impact
  - Hard to justify refactoring
  - Vague feeling everything is slow
  - No workaround time tracking
### **Detection Pattern**


## Accidental Debt Acceptance

### **Id**
accidental-debt-acceptance
### **Summary**
Treating accidental mess as acceptable strategic debt
### **Severity**
medium
### **Situation**
  Codebase is a mess. Team says it is technical debt. Actually it is
  poor engineering, not strategic tradeoffs. No one made a choice to
  take this debt.
  
### **Why**
  Strategic debt is a conscious choice with a payback plan. Accidental
  debt is mess that happened through neglect. They need different
  responses. Strategic debt is managed. Accidental debt needs skills
  improvement.
  
### **Solution**
  Distinguish debt types:
  
  Strategic: We chose to do X instead of Y because Z. Payback by date D.
  Accidental: We did not know better. Need training and standards.
  
  Strategic debt: Track and payback
  Accidental debt: Fix AND improve practices to prevent recurrence
  
### **Symptoms**
  - No record of debt decisions
  - Repeated similar mistakes
  - No clear tradeoff was made
  - Mess accepted as normal
### **Detection Pattern**


## No Business Translation

### **Id**
no-business-translation
### **Summary**
Describing debt in technical terms leadership does not understand
### **Severity**
medium
### **Situation**
  Engineering says: We have coupling issues and technical debt in the
  data layer. Leadership hears: Nerds complaining about code again.
  Nothing changes.
  
### **Why**
  Leadership cares about velocity, reliability, cost. Not code quality
  for its own sake. Translate debt to business impact to get buy-in.
  
### **Solution**
  Business translation:
  
  Technical: Auth system has coupling issues
  Business: Shipping auth changes takes 3x longer, costing us 2 weeks per feature
  
  Technical: Database needs refactoring
  Business: System goes down twice monthly, each outage costs $50K
  
  Always: What does this cost in time, money, or risk?
  
### **Symptoms**
  - Leadership ignores debt concerns
  - Technical language in business discussions
  - No buy-in for paydown
  - Debt framed as code quality
### **Detection Pattern**
