# Scope Creep Defense - Validations

## Missing Scope Definition

### **Id**
no-scope-document
### **Severity**
high
### **Type**
conceptual
### **Check**
Project should have defined scope
### **Indicators**
  - No scope document
  - Unclear boundaries
  - Everything is in scope
### **Message**
No scope definition exists.
### **Fix Action**
Create scope document with in/out of scope lists

## Additions Without Trade-offs

### **Id**
no-trade-offs
### **Severity**
high
### **Type**
conceptual
### **Check**
Every addition should have trade-off
### **Indicators**
  - Add this too
  - No impact assessment
  - Free additions
### **Message**
Additions made without trade-off analysis.
### **Fix Action**
Require impact assessment for every addition

## Scope Changed Without Process

### **Id**
scope-lock-broken
### **Severity**
medium
### **Type**
conceptual
### **Check**
Scope changes should follow process
### **Indicators**
  - Just add it
  - No approval
  - Informal change
### **Message**
Scope changed outside change control.
### **Fix Action**
Use formal change request process

## Everything is Priority 1

### **Id**
no-prioritization
### **Severity**
medium
### **Type**
conceptual
### **Check**
Requirements should be stack-ranked
### **Indicators**
  - All high priority
  - Everything is must-have
  - No ranking
### **Message**
No clear prioritization exists.
### **Fix Action**
Force stack rank, no ties allowed

## Adding Unrequested Features

### **Id**
gold-plating
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should only build what's requested
### **Indicators**
  - Also added
  - While I was there
  - Thought it would be nice
### **Message**
Adding features not in scope.
### **Fix Action**
Create ticket for extras, don't add to current work

## Project Has No End Date

### **Id**
eternal-project
### **Severity**
medium
### **Type**
conceptual
### **Check**
Project should have defined end state
### **Indicators**
  - Ongoing
  - No deadline
  - When it's done
### **Message**
No clear project end state.
### **Fix Action**
Define success criteria and deadline