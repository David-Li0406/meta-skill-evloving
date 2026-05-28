# Cliffhanger Craft - Validations

## Cliffhanger Without Resolution

### **Id**
no-resolution-planned
### **Severity**
high
### **Type**
conceptual
### **Check**
Cliffhangers should have planned resolutions
### **Message**
Creating tension without knowing the payoff.
### **Fix Action**
Plan resolution before publishing cliffhanger

## Cut Point Not Strategic

### **Id**
arbitrary-cut
### **Severity**
medium
### **Type**
conceptual
### **Check**
Cut should be at tension peak
### **Indicators**
  - Random ending
  - No clear tension
### **Message**
Cut point doesn't maximize anticipation.
### **Fix Action**
End at moment of maximum investment

## Cliffhanger Overuse

### **Id**
overuse
### **Severity**
medium
### **Type**
conceptual
### **Check**
Cliffhangers should be used strategically
### **Indicators**
  - Every piece ends with cliff
  - Audience fatigue signals
### **Message**
Too many cliffhangers causing fatigue.
### **Fix Action**
Vary ending types, use cliffs sparingly

## Resolution Gap Too Long

### **Id**
gap-too-long
### **Severity**
medium
### **Type**
conceptual
### **Check**
Resolution should come within reasonable time
### **Indicators**
  - More than 2 weeks gap
  - No reminder system
### **Message**
Audience may forget before resolution.
### **Fix Action**
Shorten gap or add reminder system

## Platform Truncation Risk

### **Id**
truncation-risk
### **Severity**
low
### **Type**
conceptual
### **Check**
Cliffhanger visible in platform preview
### **Message**
Cliffhanger may be cut off on some platforms.
### **Fix Action**
Test on mobile and check platform limits

## No Return Mechanism

### **Id**
weak-return-hook
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should capture intent to return
### **Message**
No way to ensure audience returns.
### **Fix Action**
Add subscribe CTA or notification option