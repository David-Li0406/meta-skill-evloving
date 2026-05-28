# Easter Egg Design - Validations

## Easter Egg Affects Core Experience

### **Id**
breaks-core
### **Severity**
high
### **Type**
conceptual
### **Check**
Easter eggs should not interfere with main product
### **Indicators**
  - Triggers during normal use
  - Affects critical user paths
### **Message**
Easter egg breaks core experience.
### **Fix Action**
Isolate trigger to avoid accidental activation

## Inaccessible Easter Egg

### **Id**
inaccessible
### **Severity**
high
### **Type**
conceptual
### **Check**
Easter eggs should be accessible to all users
### **Indicators**
  - Mouse-only trigger
  - Vision-only reward
### **Message**
Easter egg excludes users with disabilities.
### **Fix Action**
Add alternative triggers and accessible rewards

## Undocumented Easter Egg

### **Id**
no-documentation
### **Severity**
medium
### **Type**
conceptual
### **Check**
Easter eggs should be documented internally
### **Message**
Easter egg not documented - maintenance risk.
### **Fix Action**
Document trigger, location, and owner in codebase

## Impossible to Discover

### **Id**
over-hidden
### **Severity**
medium
### **Type**
conceptual
### **Check**
Easter eggs should be discoverable
### **Indicators**
  - Zero discoveries after launch
  - Trigger too complex
### **Message**
Easter egg too hidden to find.
### **Fix Action**
Add hints or simplify trigger

## Reference Will Age Poorly

### **Id**
dated-reference
### **Severity**
low
### **Type**
conceptual
### **Check**
References should age gracefully
### **Indicators**
  - Current meme reference
  - Trending topic dependency
### **Message**
Reference may age quickly.
### **Fix Action**
Use timeless references or plan sunset

## No Way to Exit Easter Egg

### **Id**
no-exit
### **Severity**
medium
### **Type**
conceptual
### **Check**
Users should be able to return to normal state
### **Message**
User stuck in easter egg state.
### **Fix Action**
Add clear exit mechanism