# Feature Prioritization - Validations

## No Prioritization Criteria

### **Id**
no-criteria
### **Severity**
high
### **Type**
conceptual
### **Check**
Prioritization must use explicit criteria
### **Indicators**
  - Gut feel only
  - No framework used
### **Message**
Prioritization lacks explicit criteria.
### **Fix Action**
Define and publish prioritization criteria

## Everything High Priority

### **Id**
everything-priority
### **Severity**
high
### **Type**
conceptual
### **Check**
Force-ranking required, not all high priority
### **Indicators**
  - All P1
  - No clear ordering
### **Message**
Everything marked as priority - meaningless.
### **Fix Action**
Force-rank items; accept trade-offs

## Features Without Outcomes

### **Id**
no-outcomes
### **Severity**
medium
### **Type**
conceptual
### **Check**
Each priority should have expected outcome
### **Indicators**
  - Feature list without goals
  - No success metrics
### **Message**
Priority items lack outcome definition.
### **Fix Action**
Define success criteria for each prioritized item

## Unmaintainable Backlog

### **Id**
infinite-backlog
### **Severity**
medium
### **Type**
conceptual
### **Check**
Backlog should be manageable size
### **Indicators**
  - Hundreds of items
  - Items older than 6 months
### **Message**
Backlog too large to maintain.
### **Fix Action**
Aggressive cleanup; archive stale items

## Unstable Priorities

### **Id**
constant-changes
### **Severity**
high
### **Type**
conceptual
### **Check**
Priorities should be stable within commitment window
### **Indicators**
  - Multiple changes per sprint
  - Nothing ever finished
### **Message**
Priority changes too frequent.
### **Fix Action**
Establish commitment windows; require trade-off for changes

## All Tactical, No Strategic

### **Id**
no-strategic-balance
### **Severity**
medium
### **Type**
conceptual
### **Check**
Portfolio should include strategic investment
### **Indicators**
  - Only quick wins
  - No long-term initiatives
### **Message**
Missing strategic investment in prioritization.
### **Fix Action**
Allocate 20-30% to strategic initiatives

## Unclear Scope

### **Id**
scope-undefined
### **Severity**
medium
### **Type**
conceptual
### **Check**
Priority items must have defined scope
### **Indicators**
  - No 'out of scope' defined
  - Vague requirements
### **Message**
Priority items lack clear scope.
### **Fix Action**
Define in-scope and out-of-scope explicitly