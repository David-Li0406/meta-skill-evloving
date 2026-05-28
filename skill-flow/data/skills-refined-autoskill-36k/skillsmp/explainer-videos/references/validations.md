# Explainer Videos - Validations

## Problem should be established before solution

### **Id**
problem-before-solution
### **Severity**
critical
### **Description**
Viewers don't care about solutions until they feel the problem
### **Pattern**
  #### **File Glob**
**/*.{yaml,md,txt}
  #### **Match**
explainer|script|video
  #### **Exclude**
problem|pain.*point|challenge|frustrat
### **Message**
Explainer may lack problem setup. Establish the problem before introducing solution.
### **Autofix**


## Script should be free of unexplained jargon

### **Id**
jargon-free
### **Severity**
critical
### **Description**
Jargon excludes viewers who need the explainer most
### **Pattern**
  #### **File Glob**
**/*.{yaml,md,txt}
  #### **Match**
script|explainer|voiceover
  #### **Exclude**
simple|plain.*language|non.*technical
### **Message**
Script may contain jargon. Test with non-expert reviewer.
### **Autofix**


## Explainer should focus on one core message

### **Id**
single-message
### **Severity**
critical
### **Description**
Multiple messages dilute impact and confuse viewers
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
explainer|video|message
  #### **Exclude**
one.*message|single.*focus|core.*point
### **Message**
Explainer may have multiple messages. Focus on one thing done well.
### **Autofix**


## Video length should match context

### **Id**
length-appropriate
### **Severity**
high
### **Description**
Attention drops significantly after 90 seconds for landing pages
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
explainer|landing.*page|video
  #### **Exclude**
duration|length|seconds|90|60
### **Message**
Video length may not be specified. Target 60-90 seconds for landing pages.
### **Autofix**


## Explainer should end with clear call-to-action

### **Id**
clear-cta
### **Severity**
high
### **Description**
Without clear CTA, viewers don't know what to do next
### **Pattern**
  #### **File Glob**
**/*.{yaml,md,txt}
  #### **Match**
explainer|video|script
  #### **Exclude**
call.*action|CTA|next.*step|sign.*up|start
### **Message**
Explainer may lack clear CTA. Tell viewers exactly what to do next.
### **Autofix**


## Script should be reviewed by non-expert

### **Id**
non-expert-review
### **Severity**
high
### **Description**
Curse of knowledge blinds experts to confusion points
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
explainer|script|review
  #### **Exclude**
non.*expert|outsider|test|feedback
### **Message**
Non-expert review may not be planned. Test comprehension with outsiders.
### **Autofix**


## Metaphors should be simpler than concepts

### **Id**
visual-metaphor-check
### **Severity**
medium
### **Description**
Bad metaphors add confusion instead of clarity
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
metaphor|analogy|like.*a
  #### **Exclude**
simple|familiar|test|understand
### **Message**
Metaphors may need verification. Test that they clarify, not complicate.
### **Autofix**


## Animation should support the message

### **Id**
animation-serves-message
### **Severity**
medium
### **Description**
Animation should clarify, not decorate
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
animation|animate|visual
  #### **Exclude**
purpose|support|clarify|serve
### **Message**
Animation purpose may not be defined. Every motion should aid understanding.
### **Autofix**


## Complex processes should be simplified to three steps

### **Id**
three-step-framework
### **Severity**
medium
### **Description**
Cognitive load research shows 3 is the magic number
### **Pattern**
  #### **File Glob**
**/*.{yaml,md,txt}
  #### **Match**
how.*works|process|step
  #### **Exclude**
three|3.*step|simple
### **Message**
Process may have too many steps. Collapse complexity into 3 memorable steps.
### **Autofix**


## Script word count should match target duration

### **Id**
word-count-check
### **Severity**
low
### **Description**
150 words ≈ 60 seconds at conversational pace
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
script|explainer|voiceover
  #### **Exclude**
word.*count|timing|duration|150
### **Message**
Word count may not be verified. Count words to estimate duration.
### **Autofix**


## Script should be tested for speakability

### **Id**
speakability-tested
### **Severity**
low
### **Description**
Written language differs from spoken language
### **Pattern**
  #### **File Glob**
**/*.{yaml,md,txt}
  #### **Match**
script|voiceover|narration
  #### **Exclude**
read.*aloud|speakable|spoken
### **Message**
Script speakability may not be tested. Read aloud before recording.
### **Autofix**
