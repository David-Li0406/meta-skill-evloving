# Tech Debt Negotiation - Validations

## Missing Business Impact

### **Id**
no-business-case
### **Severity**
high
### **Type**
conceptual
### **Check**
Debt should be framed in business terms
### **Indicators**
  - Just need to refactor
  - Code is messy
  - Technical reasons
### **Message**
No business case for debt work.
### **Fix Action**
Quantify impact: velocity, incidents, cost

## All Debt Equal Priority

### **Id**
no-prioritization
### **Severity**
medium
### **Type**
conceptual
### **Check**
Debt should be prioritized by impact
### **Indicators**
  - Everything is critical
  - All debt is bad
  - Need to fix everything
### **Message**
Debt not prioritized by impact.
### **Fix Action**
Rank by business impact, fix highest first

## Unbounded Debt Work

### **Id**
no-time-box
### **Severity**
medium
### **Type**
conceptual
### **Check**
Debt work should be time-boxed
### **Indicators**
  - Until it's done
  - However long it takes
  - Open-ended
### **Message**
Debt work has no time limit.
### **Fix Action**
Set specific time-box and scope

## No Before/After Metrics

### **Id**
no-measurement
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should measure improvement from debt work
### **Indicators**
  - Trust me, it's better
  - Code is cleaner now
  - No specific metrics
### **Message**
No measurable improvement tracked.
### **Fix Action**
Define metrics before, measure after

## Pure Technical Justification

### **Id**
tech-only-framing
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should translate to non-technical stakeholders
### **Indicators**
  - Technical debt
  - Code smell
  - Architecture issues
### **Message**
Technical framing won't convince business.
### **Fix Action**
Translate to money, time, risk

## All-or-Nothing Proposal

### **Id**
big-rewrite-ask
### **Severity**
high
### **Type**
conceptual
### **Check**
Should propose incremental improvements
### **Indicators**
  - Complete rewrite
  - Start from scratch
  - Replace everything
### **Message**
Big rewrite proposals usually fail.
### **Fix Action**
Propose incremental improvements instead