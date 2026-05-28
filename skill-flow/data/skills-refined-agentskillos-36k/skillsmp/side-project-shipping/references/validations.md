# Side Project Shipping - Validations

## Scope Exceeds Side Project

### **Id**
scope-too-big
### **Severity**
high
### **Type**
conceptual
### **Check**
Side project scope should be achievable in weekends
### **Indicators**
  - This will take months
  - Need to build infrastructure first
  - Complex multi-user system
### **Message**
Scope too large for side project.
### **Fix Action**
Cut to one core feature shippable in 48 hours

## Perfectionism Blocking Ship

### **Id**
perfectionism-detected
### **Severity**
high
### **Type**
conceptual
### **Check**
Project should ship before it feels ready
### **Indicators**
  - Almost done
  - Just need to polish
  - One more feature
### **Message**
Perfectionism is blocking launch.
### **Fix Action**
Set hard deadline and ship as-is

## Technology Tourism

### **Id**
tech-over-shipping
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should use familiar tech for shipping goals
### **Indicators**
  - Learning new framework
  - Trying new language
  - Experimenting with
### **Message**
New tech is slowing shipping.
### **Fix Action**
Switch to boring tech you know well, or accept it's a learning project

## Missing Ship Date

### **Id**
no-deadline
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should have concrete launch date
### **Indicators**
  - When it's ready
  - Eventually
  - Sometime soon
### **Message**
No deadline means no shipping.
### **Fix Action**
Pick a date. Announce it publicly.

## Solo Without Accountability

### **Id**
no-accountability
### **Severity**
low
### **Type**
conceptual
### **Check**
Should have external accountability
### **Indicators**
  - Haven't told anyone
  - Working in secret
  - Will announce when done
### **Message**
No accountability increases abandonment risk.
### **Fix Action**
Tell someone. Post publicly. Create accountability.

## Feature Creep Active

### **Id**
feature-creep
### **Severity**
medium
### **Type**
conceptual
### **Check**
Features should be ruthlessly minimal
### **Indicators**
  - While I'm at it
  - Easy to add
  - Might as well
### **Message**
Feature creep detected.
### **Fix Action**
Add to V2_FEATURES.md and ship without it