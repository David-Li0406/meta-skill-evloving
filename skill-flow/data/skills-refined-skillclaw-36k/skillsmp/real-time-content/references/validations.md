# Real Time Content - Validations

## Real-time content must have sensitivity check

### **Id**
sensitivity-check-exists
### **Severity**
critical
### **Description**
Speed doesn't justify insensitivity
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
(real.time|rapid|trending).*publish
  #### **Exclude**
sensitivity|check|review|appropriate
### **Message**
Real-time publishing without sensitivity check. Add safety review step.
### **Autofix**


## Trend content should verify brand fit

### **Id**
brand-fit-verified
### **Severity**
high
### **Description**
Forced connections damage brand
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
trend.*content|respond.*trending
  #### **Exclude**
fit|relevant|appropriate|connection
### **Message**
Trend response without brand fit check. Verify natural connection.
### **Autofix**


## Real-time workflow should use templates

### **Id**
templates-exist
### **Severity**
high
### **Description**
Templates enable speed without chaos
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
real.time.*create|rapid.*content
  #### **Exclude**
template|pre.approved|framework
### **Message**
Real-time content without templates. Build template library.
### **Autofix**


## Verify trend is still relevant before publishing

### **Id**
timing-check
### **Severity**
high
### **Description**
Late real-time content damages brand
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
trend.*publish|post.*trending
  #### **Exclude**
timing|window|relevant|current
### **Message**
Publishing trend content without timing check. Verify still relevant.
### **Autofix**


## Real-time content needs expedited approval path

### **Id**
approval-path-defined
### **Severity**
medium
### **Description**
Standard approval kills real-time
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
real.time|rapid.*content
  #### **Exclude**
approval|tier|expedited|pre.approved
### **Message**
Real-time workflow without approval path. Define expedited process.
### **Autofix**


## Trend content should have unique angle

### **Id**
unique-angle-required
### **Severity**
medium
### **Description**
Derivative content wastes effort
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
trend.*create|respond.*trending
  #### **Exclude**
angle|unique|perspective|differentiate
### **Message**
Trend content without unique angle. Define brand's perspective.
### **Autofix**


## Real-time content should be monitored post-publish

### **Id**
monitoring-after-publish
### **Severity**
medium
### **Description**
Engagement and problems need attention
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
publish.*real.time|post.*trend
  #### **Exclude**
monitor|track|watch|engage
### **Message**
Publishing without monitoring plan. Add post-publish tracking.
### **Autofix**


## Meme usage should be verified

### **Id**
meme-verification
### **Severity**
medium
### **Description**
Meme misuse creates cringe
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
meme|trending.*format
  #### **Exclude**
verify|check|research|origin
### **Message**
Using meme without verification. Research format and usage.
### **Autofix**


## Real-time should have pre-built asset library

### **Id**
asset-library-exists
### **Severity**
low
### **Description**
Pre-built assets enable speed
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
real.time|rapid
  #### **Exclude**
asset|library|template|pre.built
### **Message**
Real-time capability without asset library. Build asset collection.
### **Autofix**


## Real-time executions should document learnings

### **Id**
learning-documented
### **Severity**
low
### **Description**
Learning improves future executions
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
real.time.*complete|trend.*done
  #### **Exclude**
learn|document|record|analyze
### **Message**
Trend execution without learning capture. Document what worked.
### **Autofix**
