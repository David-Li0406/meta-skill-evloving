# Ai Trend Alchemy - Validations

## Trend response should have context check

### **Id**
context-check-exists
### **Severity**
critical
### **Description**
Missing context causes brand crises
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
trend.*respond|join.*trending|trending.*content
  #### **Exclude**
context|check|news|sensitive
### **Message**
Trend response without context check. Add sensitivity/context verification.
### **Autofix**


## Trend participation should check cultural appropriateness

### **Id**
cultural-check-present
### **Severity**
high
### **Description**
Cultural trends need standing assessment
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
trend.*participate|join.*trend|trending.*topic
  #### **Exclude**
cultural|appropriate|standing|community
### **Message**
Trend participation without cultural check. Verify standing and appropriateness.
### **Autofix**


## Trend response should verify brand fit

### **Id**
brand-fit-verified
### **Severity**
high
### **Description**
Forced connections damage brand perception
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
trend.*content|trending.*response
  #### **Exclude**
fit|relevant|connection|natural
### **Message**
Trend response without brand fit verification. Check for natural connection.
### **Autofix**


## Trend content should assess timing window

### **Id**
timing-assessment
### **Severity**
high
### **Description**
Late trend content is worse than no content
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
trend.*publish|post.*trending
  #### **Exclude**
timing|window|peak|lifecycle
### **Message**
Trend publishing without timing assessment. Verify still relevant.
### **Autofix**


## Trend signals should be validated before action

### **Id**
signal-validation
### **Severity**
high
### **Description**
Not all spikes are real trends
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
trend.*detect|signal.*trend
  #### **Exclude**
validate|verify|confirm|multi.*source
### **Message**
Trend detection without validation. Confirm signal before acting.
### **Autofix**


## Trend content should have unique angle

### **Id**
unique-angle-defined
### **Severity**
medium
### **Description**
Derivative responses waste effort
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
trend.*content|create.*trending
  #### **Exclude**
angle|unique|perspective|differentiate
### **Message**
Trend content without unique angle. Define brand's distinctive perspective.
### **Autofix**


## Trend decisions should use framework

### **Id**
decision-framework-used
### **Severity**
medium
### **Description**
Ad-hoc decisions lead to inconsistent results
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
trend.*decision|should.*trend|trend.*go
  #### **Exclude**
framework|criteria|checklist|process
### **Message**
Trend decision without framework. Use systematic go/no-go process.
### **Autofix**


## Trend detection should connect to execution

### **Id**
execution-pipeline-exists
### **Severity**
medium
### **Description**
Prediction without execution is waste
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
trend.*predict|detect.*trend|trend.*signal
  #### **Exclude**
execute|action|generate|create
### **Message**
Trend detection without execution pipeline. Connect prediction to content creation.
### **Autofix**


## Trend detection should use multiple sources

### **Id**
multi-layer-detection
### **Severity**
medium
### **Description**
Single-source detection misses signals
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
trend.*monitor|track.*trend
  #### **Exclude**
multi|multiple|sources|layers
### **Message**
Trend monitoring may rely on single source. Use multi-layer detection.
### **Autofix**


## Trend velocity should be measured

### **Id**
velocity-tracked
### **Severity**
low
### **Description**
Velocity matters more than volume
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
trend.*data|trending.*metrics
  #### **Exclude**
velocity|acceleration|rate.*change
### **Message**
Trend analysis may miss velocity. Track acceleration, not just volume.
### **Autofix**


## Trend attempts should be documented for learning

### **Id**
learning-documented
### **Severity**
low
### **Description**
Learning from successes and failures improves future performance
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
trend.*complete|trend.*publish
  #### **Exclude**
learn|document|analyze|retrospective
### **Message**
Trend execution without learning capture. Document what worked.
### **Autofix**


## Trend pursuit should have capacity limits

### **Id**
team-not-exhausted
### **Severity**
low
### **Description**
Team burnout kills quality
### **Pattern**
  #### **File Glob**
**/*.{yaml,md}
  #### **Match**
trend.*strategy|content.*calendar
  #### **Exclude**
limit|capacity|maximum|sustainable
### **Message**
Trend strategy may lack capacity limits. Define sustainable pace.
### **Autofix**
