# Demo Day Theater - Validations

## Demo Without Backup

### **Id**
no-backup
### **Severity**
high
### **Type**
conceptual
### **Check**
Demo should have fallback options
### **Indicators**
  - No backup plan
  - Only live demo
  - No recording
### **Message**
Demo has no backup if live fails.
### **Fix Action**
Create video backup and screenshot fallback

## Unrehearsed Demo

### **Id**
no-rehearsal
### **Severity**
medium
### **Type**
conceptual
### **Check**
Demo should be rehearsed
### **Indicators**
  - First time running through
  - Haven't practiced
  - Winging it
### **Message**
Demo hasn't been rehearsed.
### **Fix Action**
Run full demo at least 3 times before presenting

## Wrong Technical Level

### **Id**
wrong-audience-level
### **Severity**
medium
### **Type**
conceptual
### **Check**
Demo should match audience level
### **Indicators**
  - All executives, showing code
  - Engineers, showing only business
  - No audience research
### **Message**
Demo level may not match audience.
### **Fix Action**
Research audience, adapt content and language

## Demo Without Narrative

### **Id**
no-story
### **Severity**
medium
### **Type**
conceptual
### **Check**
Demo should tell a story
### **Indicators**
  - Just showing features
  - No setup
  - No impact
### **Message**
Demo is feature dump without narrative.
### **Fix Action**
Structure as problem → solution → impact

## Demo Running Long

### **Id**
too-long
### **Severity**
low
### **Type**
conceptual
### **Check**
Demo should be concise
### **Indicators**
  - > 10 minutes for stakeholders
  - No time budgeted
  - Showing everything
### **Message**
Demo may be too long.
### **Fix Action**
Cut to 5 minutes, pick top 3 things to show

## Good Work Not Demonstrated

### **Id**
no-visibility
### **Severity**
medium
### **Type**
conceptual
### **Check**
Work should be made visible
### **Indicators**
  - No demo for invisible work
  - Nothing to show
  - Just technical work
### **Message**
Work may not be getting visibility.
### **Fix Action**
Find proxy demos, create metrics dashboards