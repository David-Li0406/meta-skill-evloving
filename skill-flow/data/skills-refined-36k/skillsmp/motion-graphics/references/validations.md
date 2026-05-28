# Motion Graphics - Validations

## Animation should use proper easing curves

### **Id**
easing-applied
### **Severity**
critical
### **Description**
Linear motion looks robotic and unprofessional
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animate|animation|motion
  #### **Exclude**
easing|ease.*in|ease.*out|bezier|curve
### **Message**
Animation may use linear easing. Always apply ease-in/ease-out curves.
### **Autofix**


## Style frames should be approved before animation

### **Id**
style-frames-approved
### **Severity**
critical
### **Description**
Animation without style approval risks expensive rework
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animation|motion.*graphic|animate
  #### **Exclude**
style.*frame|visual.*approved|design.*locked
### **Message**
Style frames may not be approved. Get visual design sign-off before animating.
### **Autofix**


## Animation purpose should be clear

### **Id**
animation-purpose-defined
### **Severity**
high
### **Description**
Every animation should have a communication purpose
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animate|animation|motion.*graphic
  #### **Exclude**
purpose|goal|communicate|guide|clarify
### **Message**
Animation purpose may not be defined. Document what each animation communicates.
### **Autofix**


## Animation timing should create hierarchy

### **Id**
timing-hierarchy
### **Severity**
high
### **Description**
Uniform timing feels mechanical; variation creates focus
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animation|animate|timeline
  #### **Exclude**
timing|duration|stagger|sequence
### **Message**
Animation timing may be uniform. Vary duration to create visual hierarchy.
### **Autofix**


## Animation should plan for audio synchronization

### **Id**
audio-sync-planned
### **Severity**
high
### **Description**
Motion and audio must work together
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animation|motion.*graphic|kinetic
  #### **Exclude**
audio|sync|music|beat|sound
### **Message**
Audio sync may not be planned. Design animation to work with audio track.
### **Autofix**


## Export specifications should be defined

### **Id**
export-specs-defined
### **Severity**
medium
### **Description**
Wrong format wastes time and causes issues
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animation|motion|export|deliver
  #### **Exclude**
format|codec|lottie|resolution|specs
### **Message**
Export specs may not be defined. Know delivery format before starting.
### **Autofix**


## File size optimization should be considered

### **Id**
file-size-considered
### **Severity**
medium
### **Description**
Large files cause performance issues
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
lottie|web.*animation|animation|json
  #### **Exclude**
optimize|size|performance|compress
### **Message**
File size may not be optimized. Plan for performance requirements.
### **Autofix**


## Composition should work at key frames

### **Id**
composition-checked
### **Severity**
medium
### **Description**
Each frame should work as a still image
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animation|motion|design
  #### **Exclude**
composition|frame|balance|hierarchy
### **Message**
Composition may not be verified. Check that key frames work as stills.
### **Autofix**


## Motion style should be documented

### **Id**
motion-style-guide
### **Severity**
low
### **Description**
Consistency requires documented guidelines
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animation|motion|brand
  #### **Exclude**
style.*guide|motion.*principle|guideline
### **Message**
Motion style may not be documented. Create guidelines for consistency.
### **Autofix**


## Motion accessibility should be considered

### **Id**
accessibility-considered
### **Severity**
low
### **Description**
Some users are sensitive to motion
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animation|motion|web
  #### **Exclude**
accessible|prefers.*reduced|motion.*sensitivity
### **Message**
Accessibility may not be considered. Respect prefers-reduced-motion.
### **Autofix**
