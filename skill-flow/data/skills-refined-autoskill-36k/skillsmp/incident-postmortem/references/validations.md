# Incident Postmortem - Validations

## Blaming Language Detected

### **Id**
blame-language
### **Severity**
high
### **Type**
conceptual
### **Check**
Postmortem should be blameless
### **Indicators**
  - Person's name as cause
  - Human error
  - Should have known
  - Careless
### **Message**
Postmortem contains blaming language.
### **Fix Action**
Reframe to system causes

## Root Cause Too Shallow

### **Id**
shallow-root-cause
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should dig to systemic root cause
### **Indicators**
  - Human error
  - One-word cause
  - Stopped at first why
### **Message**
Root cause analysis may be too shallow.
### **Fix Action**
Apply Five Whys, reach system level

## Action Items Too Vague

### **Id**
vague-actions
### **Severity**
medium
### **Type**
conceptual
### **Check**
Actions should be specific and measurable
### **Indicators**
  - Improve X
  - Be more careful
  - Review process
  - No owner assigned
### **Message**
Action items are not specific enough.
### **Fix Action**
Make SMART: specific, measurable, assigned, time-bound

## Missing Action Follow-up

### **Id**
no-follow-up
### **Severity**
medium
### **Type**
conceptual
### **Check**
Actions should be tracked to completion
### **Indicators**
  - No deadline
  - No owner
  - No verification plan
### **Message**
Action items may not get completed.
### **Fix Action**
Assign owner, deadline, verification method

## Missing Incident Timeline

### **Id**
no-timeline
### **Severity**
low
### **Type**
conceptual
### **Check**
Postmortem should have timeline
### **Indicators**
  - No timeline
  - Vague timing
  - Missing key events
### **Message**
Incident timeline is missing or incomplete.
### **Fix Action**
Reconstruct timeline from logs and communications

## Only Negatives

### **Id**
no-what-went-well
### **Severity**
low
### **Type**
conceptual
### **Check**
Should acknowledge what went well
### **Indicators**
  - All problems
  - No successes noted
  - Only failures
### **Message**
Postmortem doesn't acknowledge what went well.
### **Fix Action**
Add section on what worked in the response