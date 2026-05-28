# Voiceover - Validations

## Voice requirements should be documented

### **Id**
voice-match-defined
### **Severity**
critical
### **Description**
Wrong voice undermines entire video
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
voiceover|voice.*talent|narrator
  #### **Exclude**
voice.*type|tone|gender|age|style|requirements
### **Message**
Voice casting may lack requirements. Document voice type, tone, and audience match.
### **Autofix**


## Script should be optimized for speaking

### **Id**
script-speakability
### **Severity**
critical
### **Description**
Written language ≠ spoken language
### **Pattern**
  #### **File Glob**
**/*.{yaml,md,txt}
  #### **Match**
script|voiceover.*text|narration
  #### **Exclude**
read.*aloud|speakable|breath|pronunciation
### **Message**
Script may not be optimized for speaking. Read aloud and adjust.
### **Autofix**


## Audio quality requirements should be specified

### **Id**
audio-specs-defined
### **Severity**
high
### **Description**
Bad audio destroys credibility
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
voiceover|recording|audio
  #### **Exclude**
wav|24-bit|48kHz|quality|spec
### **Message**
Audio requirements may not be specified. Define format and quality specs.
### **Autofix**


## Recording environment should be specified

### **Id**
recording-environment
### **Severity**
high
### **Description**
Room sound affects audio quality
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
record|voiceover|session
  #### **Exclude**
booth|studio|treated|environment|quiet
### **Message**
Recording environment may not be specified. Define quality requirements.
### **Autofix**


## AI voice output should be reviewed

### **Id**
ai-voice-review
### **Severity**
high
### **Description**
AI voices need human quality check
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
AI.*voice|eleven.*labs|text.*speech|synthetic
  #### **Exclude**
review|check|verify|approve|listen
### **Message**
AI voice usage may lack review process. Always review before publishing.
### **Autofix**


## Voice talent should receive context

### **Id**
direction-context
### **Severity**
medium
### **Description**
Context enables better performance
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
record.*session|talent|voice.*actor
  #### **Exclude**
context|brand|audience|reference|direction
### **Message**
Recording may lack proper context. Share brand, audience, and reference.
### **Autofix**


## Multiple takes should be recorded

### **Id**
multiple-takes
### **Severity**
medium
### **Description**
Options enable better editing
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
record|session|take
  #### **Exclude**
multiple.*take|3.*take|variation|option
### **Message**
Recording may not specify multiple takes. Record 3+ takes per section.
### **Autofix**


## Voiceover timing should match video

### **Id**
timing-sync
### **Severity**
medium
### **Description**
Audio-visual sync is essential
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
voiceover|narration|video
  #### **Exclude**
timing|sync|duration|match|align
### **Message**
Voiceover timing may not be verified. Check sync with video.
### **Autofix**


## Voice style should be consistent across project

### **Id**
style-consistency
### **Severity**
low
### **Description**
Consistency builds brand
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
series|campaign|multiple.*video
  #### **Exclude**
consistent|same.*voice|style.*guide|reference
### **Message**
Multi-video project may lack voice consistency plan.
### **Autofix**


## Unusual terms should have pronunciation guides

### **Id**
pronunciation-guide
### **Severity**
low
### **Description**
Mispronunciation affects credibility
### **Pattern**
  #### **File Glob**
**/*.{yaml,md,txt}
  #### **Match**
brand.*name|product.*name|technical|acronym
  #### **Exclude**
pronunciat|phonetic|say|spell
### **Message**
Script may lack pronunciation guides for unusual terms.
### **Autofix**
