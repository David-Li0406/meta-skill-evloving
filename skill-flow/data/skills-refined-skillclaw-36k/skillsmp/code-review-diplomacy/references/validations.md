# Code Review Diplomacy - Validations

## Harsh Review Language

### **Id**
harsh-language
### **Severity**
high
### **Type**
conceptual
### **Check**
Review comments should be constructive
### **Indicators**
  - Obviously wrong
  - You should know
  - Just do it this way
  - This is bad
### **Message**
Review language may be harsh.
### **Fix Action**
Reframe as observation and suggestion

## Feedback Without Context

### **Id**
no-explanation
### **Severity**
medium
### **Type**
conceptual
### **Check**
Comments should explain why
### **Indicators**
  - Change this
  - Wrong
  - No
  - No rationale given
### **Message**
Feedback lacks explanation.
### **Fix Action**
Add reasoning and suggestion

## Blocking on Minor Issues

### **Id**
blocking-trivial
### **Severity**
medium
### **Type**
conceptual
### **Check**
Only block on significant issues
### **Indicators**
  - Style blocking
  - Naming blocking
  - Formatting blocking
### **Message**
Blocking on trivial issue.
### **Fix Action**
Use [nit] or auto-format instead

## All Criticism, No Praise

### **Id**
no-positive-feedback
### **Severity**
low
### **Type**
conceptual
### **Check**
Reviews should include genuine praise
### **Indicators**
  - Only problems listed
  - No acknowledgment of good work
  - Zero positive comments
### **Message**
Review is all negative.
### **Fix Action**
Find something genuinely good to acknowledge

## Review Taking Too Long

### **Id**
review-too-slow
### **Severity**
medium
### **Type**
conceptual
### **Check**
Reviews should be timely
### **Indicators**
  - Days without response
  - PR aging
  - Blocked waiting
### **Message**
Review turnaround too slow.
### **Fix Action**
Set and honor review SLA

## Approval Without Review

### **Id**
rubber-stamp
### **Severity**
medium
### **Type**
conceptual
### **Check**
Reviews should be substantive
### **Indicators**
  - LGTM only
  - No comments on any PR
  - Instant approval
### **Message**
Review may not be substantive.
### **Fix Action**
Actually read code, leave meaningful feedback