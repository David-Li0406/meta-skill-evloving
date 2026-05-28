# Video Production - Validations

## Video script should be approved before production

### **Id**
script-approved
### **Severity**
critical
### **Description**
Shooting without approved script causes expensive problems
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
video|shoot|production|filming
  #### **Exclude**
script|approved|signed.off|locked
### **Message**
Video production may lack approved script. Script must be locked before shooting.
### **Autofix**


## Shot list should be documented before production

### **Id**
shot-list-exists
### **Severity**
critical
### **Description**
No shot list means forgotten shots and wasted time
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
shoot|filming|production.*day
  #### **Exclude**
shot.*list|shots.*needed|shooting.*schedule
### **Message**
Production may lack shot list. Document every shot needed before the shoot.
### **Autofix**


## Audio capture plan should be defined

### **Id**
audio-plan-defined
### **Severity**
high
### **Description**
Bad audio destroys video regardless of visual quality
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
video|shoot|interview|talking.*head
  #### **Exclude**
audio|lavalier|microphone|sound
### **Message**
Audio plan may not be defined. Plan microphone setup before shooting.
### **Autofix**


## Backup recording should be planned

### **Id**
backup-recording
### **Severity**
high
### **Description**
Equipment fails; backups are insurance
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
record|shoot|production
  #### **Exclude**
backup|redundant|secondary|safety
### **Message**
Backup recording may not be planned. Always have secondary audio/video capture.
### **Autofix**


## Multiple takes should be planned

### **Id**
multi-take-planned
### **Severity**
high
### **Description**
Best performances come from options
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
record|shoot|talent|interview
  #### **Exclude**
take|multiple|variation|option
### **Message**
Multiple takes may not be planned. Record 3-5 takes minimum per setup.
### **Autofix**


## Release forms should be collected

### **Id**
release-forms-required
### **Severity**
medium
### **Description**
No release means footage can't be used
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
talent|interview|on.*camera|person
  #### **Exclude**
release|consent|permission|waiver
### **Message**
Release forms may not be addressed. Collect signed releases before filming.
### **Autofix**


## Delivery formats should be defined before production

### **Id**
platform-formats-defined
### **Severity**
medium
### **Description**
Different platforms need different formats
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
video|social|youtube|instagram|tiktok
  #### **Exclude**
format|aspect.*ratio|16:9|9:16|1:1
### **Message**
Delivery formats may not be defined. Plan for all platform formats upfront.
### **Autofix**


## Post-production workflow should be defined

### **Id**
post-workflow-defined
### **Severity**
medium
### **Description**
Clear workflow prevents bottlenecks
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
edit|post.*production|video.*project
  #### **Exclude**
workflow|process|rough.*cut|approval
### **Message**
Post-production workflow may not be defined. Establish edit → review → revise cycle.
### **Autofix**


## Storage and backup should be planned

### **Id**
storage-planned
### **Severity**
low
### **Description**
Running out of storage stops production
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
shoot|production|filming
  #### **Exclude**
storage|cards|backup|capacity
### **Message**
Storage capacity may not be planned. Calculate and prepare sufficient storage.
### **Autofix**


## Quality review checkpoints should be defined

### **Id**
quality-checkpoints
### **Severity**
low
### **Description**
Catching issues early is cheaper than late
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
video|production|project
  #### **Exclude**
review|checkpoint|approval|QC
### **Message**
Quality checkpoints may not be defined. Establish rough cut and fine cut reviews.
### **Autofix**
