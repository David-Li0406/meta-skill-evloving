# Ai Workflow Automation - Validations

## Workflows should have quality gates before auto-publish

### **Id**
quality-gates-exist
### **Severity**
critical
### **Description**
Automation without quality gates amplifies errors
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
auto.*publish|publish.*auto|automated.*publish
  #### **Exclude**
quality.*gate|validation|check|verify|approve
### **Message**
Workflow may auto-publish without quality gates. Add validation checks before publication.
### **Autofix**


## AI workflows should track costs per request

### **Id**
cost-tracking-implemented
### **Severity**
critical
### **Description**
Unmonitored costs can spiral out of control
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
openai|anthropic|claude|gpt-4|api.*key|ai.*generate
  #### **Exclude**
cost|token.*count|usage|budget|track|log.*cost
### **Message**
AI API usage detected without cost tracking. Implement per-request cost logging.
### **Autofix**


## Content workflows should have defined approval process

### **Id**
approval-workflow-defined
### **Severity**
high
### **Description**
Automated content needs human oversight
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
workflow|pipeline|automation
  #### **Exclude**
approval|review|human.*check|authorize
### **Message**
Workflow may lack approval process. Define who approves what and when.
### **Autofix**


## Approval workflows should have backup approvers

### **Id**
backup-approver-exists
### **Severity**
high
### **Description**
Single approver creates bottleneck
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json}
  #### **Match**
approver|reviewer
  #### **Exclude**
backup|delegate|alternate|fallback
### **Message**
Approval workflow may lack backup approver. Add delegation for when primary unavailable.
### **Autofix**


## API calls should have rate limiting

### **Id**
rate-limiting-implemented
### **Severity**
high
### **Description**
Prevents hitting API rate limits
### **Pattern**
  #### **File Glob**
**/*.{js,ts,py}
  #### **Match**
api\..*\(|fetch\(|axios\.|request\(
  #### **Exclude**
rate.*limit|throttle|queue|delay|backoff
### **Message**
API calls may lack rate limiting. Implement request throttling to prevent 429 errors.
### **Autofix**


## Generated content should check brand compliance

### **Id**
brand-compliance-check
### **Severity**
high
### **Description**
Automated content must stay on-brand
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
generate.*content|ai.*content|llm.*generate
  #### **Exclude**
brand.*check|brand.*term|voice.*check|compliance
### **Message**
Content generation may lack brand compliance checks. Add brand term validation.
### **Autofix**


## API calls should have retry logic

### **Id**
retry-logic-exists
### **Severity**
medium
### **Description**
Temporary failures should be retried
### **Pattern**
  #### **File Glob**
**/*.{js,ts,py}
  #### **Match**
api\..*\(|fetch\(|axios\.
  #### **Exclude**
retry|catch|try.*catch|error.*handler
### **Message**
API calls may lack retry logic. Add exponential backoff for transient failures.
### **Autofix**


## Workflows should log errors with context

### **Id**
error-logging-present
### **Severity**
medium
### **Description**
Errors need investigation and pattern analysis
### **Pattern**
  #### **File Glob**
**/*.{js,ts,py}
  #### **Match**
catch|error|exception
  #### **Exclude**
log|console\.error|logger|track
### **Message**
Error handling may not log errors. Add structured logging for debugging.
### **Autofix**


## Workflows should handle integration failures gracefully

### **Id**
graceful-degradation
### **Severity**
medium
### **Description**
One failure shouldn't break entire workflow
### **Pattern**
  #### **File Glob**
**/*.{js,ts,py,yaml,yml}
  #### **Match**
integration|api.*call|external.*service
  #### **Exclude**
fallback|graceful|degrade|try.*catch|optional
### **Message**
Integration may lack graceful degradation. Add fallback behavior for failures.
### **Autofix**


## API calls should have timeouts

### **Id**
timeout-configured
### **Severity**
medium
### **Description**
Prevent hanging on slow/failed requests
### **Pattern**
  #### **File Glob**
**/*.{js,ts,py}
  #### **Match**
fetch\(|axios\.|request\(
  #### **Exclude**
timeout|signal|abort
### **Message**
API call may lack timeout. Add timeout to prevent hanging requests.
### **Autofix**


## Workflows should have health monitoring

### **Id**
workflow-monitoring
### **Severity**
medium
### **Description**
Track success rate and performance
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
workflow|pipeline|automation
  #### **Exclude**
monitor|metric|track|dashboard|alert
### **Message**
Workflow may lack monitoring. Add success rate and performance tracking.
### **Autofix**


## AI workflows should have cost budget limits

### **Id**
cost-budget-limits
### **Severity**
medium
### **Description**
Prevent runaway spending
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
openai|anthropic|gpt|claude
  #### **Exclude**
budget|limit|max.*cost|threshold
### **Message**
AI usage may lack budget limits. Set daily/monthly spending caps.
### **Autofix**


## Generated content should track performance metrics

### **Id**
performance-tracking
### **Severity**
medium
### **Description**
Measure what works to improve over time
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
publish|post|send.*email|distribute
  #### **Exclude**
track|analytics|metric|measure|performance
### **Message**
Content publication may not track performance. Add analytics integration.
### **Autofix**


## Workflows should be documented

### **Id**
workflow-documentation
### **Severity**
low
### **Description**
Team needs to understand how automation works
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json}
  #### **Match**
workflow|pipeline
  #### **Exclude**
description|comment|doc|readme
### **Message**
Workflow may lack documentation. Add description of purpose and behavior.
### **Autofix**


## Automation should allow manual override

### **Id**
human-override-available
### **Severity**
low
### **Description**
Humans need ability to intervene
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
auto.*publish|automated|pipeline
  #### **Exclude**
manual|override|pause|stop|emergency
### **Message**
Automation may lack manual override. Add ability to pause or intervene.
### **Autofix**


## Multi-channel content should adapt per platform

### **Id**
channel-adaptation
### **Severity**
low
### **Description**
Same content everywhere feels spammy
### **Pattern**
  #### **File Glob**
**/*.{yaml,yml,json,js,ts,py}
  #### **Match**
publish.*to.*\[|multi.*channel|cross.*post
  #### **Exclude**
adapt|customize|format.*for|platform.*specific
### **Message**
Multi-channel publishing may not adapt content. Customize for each platform.
### **Autofix**
