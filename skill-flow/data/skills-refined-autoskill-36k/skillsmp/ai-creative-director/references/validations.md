# Ai Creative Director - Validations

## Brief document exists before AI generation starts

### **Id**
brief-exists-before-generation
### **Severity**
critical
### **Description**
AI generation without brief leads to rework and misalignment
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml,md}
  #### **Match**
(generate|create).*(image|video|audio|avatar)
  #### **Exclude**
brief|requirements|spec|direction
### **Message**
AI generation code without brief reference. Ensure brief approval process exists.
### **Autofix**


## Hero asset approval before batch generation

### **Id**
hero-before-batch
### **Severity**
critical
### **Description**
Batch generation without approved hero amplifies mistakes
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(Promise\.all|batch|forEach|map).*generate
  #### **Exclude**
hero|approved|template|single.*first
### **Message**
Batch generation without hero-first workflow. Add hero approval checkpoint.
### **Autofix**


## QA checkpoints defined in workflow

### **Id**
qa-checkpoints-exist
### **Severity**
high
### **Description**
Production without QA checkpoints catches problems too late
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
workflow|pipeline|process
  #### **Exclude**
QA|quality|review|approval|checkpoint
### **Message**
Workflow definition without QA checkpoints. Add review gates.
### **Autofix**


## Brand style lock exists for multi-asset production

### **Id**
style-lock-defined
### **Severity**
high
### **Description**
Multi-asset production needs consistent style enforcement
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
batch|multiple|campaign|variation
  #### **Exclude**
style|brand|prefix|template|consistent
### **Message**
Multi-asset workflow without style lock. Define brand consistency rules.
### **Autofix**


## Generated assets should be compared to reference

### **Id**
reference-comparison
### **Severity**
medium
### **Description**
Without reference comparison, drift goes unnoticed
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
generate.*save|export.*generated
  #### **Exclude**
compare|reference|hero|approved|check
### **Message**
Saving generated assets without reference comparison. Add consistency check.
### **Autofix**


## AI generation costs are tracked

### **Id**
cost-tracking-exists
### **Severity**
medium
### **Description**
Untracked costs lead to budget surprises
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(generate|create).*(image|video|audio)
  #### **Exclude**
cost|budget|track|log.*price|estimate
### **Message**
AI generation without cost tracking. Add budget monitoring.
### **Autofix**


## Assets should have version tracking

### **Id**
asset-versioning
### **Severity**
medium
### **Description**
Without versioning, you lose history and use wrong assets
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
save.*asset|export.*final
  #### **Exclude**
version|v\d|timestamp|increment
### **Message**
Saving assets without versioning. Add version tracking.
### **Autofix**


## Successful workflows should be documented

### **Id**
workflow-documentation
### **Severity**
low
### **Description**
Undocumented workflows can't be replicated
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
workflow|pipeline|production
  #### **Exclude**
document|log|record|save.*workflow
### **Message**
Workflow without documentation step. Add workflow recording.
### **Autofix**


## Assets should follow naming convention

### **Id**
asset-naming-convention
### **Severity**
medium
### **Description**
Inconsistent naming makes assets hard to find
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
filename.*=|name.*asset
  #### **Exclude**
convention|format|project.*type|template
### **Message**
Asset naming without convention. Implement standard naming.
### **Autofix**


## Production should use organized folder structure

### **Id**
folder-structure-exists
### **Severity**
low
### **Description**
Scattered assets cause confusion and wasted time
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
output.*path|save.*dir
  #### **Exclude**
structure|organize|folder|brief|working|approved|final
### **Message**
File output without folder structure. Organize by project phase.
### **Autofix**


## Asset quality preserved in tool handoffs

### **Id**
handoff-format-preserved
### **Severity**
medium
### **Description**
Quality loss during handoffs degrades final output
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
export|output.*format
  #### **Exclude**
PNG|TIFF|lossless|maximum.*quality|high.*quality
### **Message**
Asset export may lose quality. Use lossless formats for handoffs.
### **Autofix**


## Context should transfer between pipeline stages

### **Id**
context-transfer
### **Severity**
low
### **Description**
Without context, downstream tools don't understand intent
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
handoff|transfer|next.*stage|downstream
  #### **Exclude**
context|brief|requirements|metadata
### **Message**
Pipeline handoff without context transfer. Pass requirements downstream.
### **Autofix**
