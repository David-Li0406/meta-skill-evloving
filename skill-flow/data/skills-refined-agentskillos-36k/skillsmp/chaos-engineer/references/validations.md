# Chaos Engineer - Validations

## Chaos Experiment Without Hypothesis

### **Id**
no-hypothesis
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ChaosEngine(?!.*hypothesis)
  - experiment(?!.*expect|.*hypothesis)
### **Message**
Chaos experiment without hypothesis. No learning possible.
### **Fix Action**
Define expected behavior: 'We expect system to maintain 99% availability when X fails'
### **Applies To**
  - **/chaos/**/*.yaml
  - **/litmus/**/*.yaml

## Chaos Without Abort Condition

### **Id**
no-abort-condition
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ChaosEngine(?!.*abort|.*probe)
  - experiments:(?!.*runProperties.*abort)
### **Message**
Chaos experiment without abort condition. Can't stop if things go wrong.
### **Fix Action**
Add abort probe that triggers on error rate exceeding threshold
### **Applies To**
  - **/chaos/**/*.yaml
  - **/litmus/**/*.yaml

## Chaos Without Time Limit

### **Id**
no-duration-limit
### **Severity**
error
### **Type**
regex
### **Pattern**
  - TOTAL_CHAOS_DURATION(?!.*[0-9])
  - duration:(?!.*[0-9])
### **Message**
Chaos experiment without duration limit. May run indefinitely.
### **Fix Action**
Set TOTAL_CHAOS_DURATION to a reasonable limit (e.g., 60 seconds)
### **Applies To**
  - **/chaos/**/*.yaml
  - **/litmus/**/*.yaml

## Chaos Affecting Too Many Resources

### **Id**
high-blast-radius
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - PODS_AFFECTED_PERC.*[5-9][0-9]
  - PODS_AFFECTED_PERC.*100
### **Message**
Chaos affecting high percentage of resources. Consider smaller blast radius.
### **Fix Action**
Start with 10-20% of pods affected, increase gradually
### **Applies To**
  - **/chaos/**/*.yaml
  - **/litmus/**/*.yaml

## Chaos Without Cleanup Strategy

### **Id**
no-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ChaosEngine(?!.*cleanup)
  - spec:(?!.*cleanup.*strategy)
### **Message**
Chaos experiment without cleanup strategy. May leave resources in bad state.
### **Fix Action**
Add cleanup strategy: 'always' or 'onSuccess'
### **Applies To**
  - **/chaos/**/*.yaml
  - **/litmus/**/*.yaml

## Production Chaos Without Canary Label

### **Id**
production-without-canary
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - namespace.*prod(?!.*canary)
  - environment.*production(?!.*percentage|.*subset)
### **Message**
Production chaos without canary scope. Start with subset of traffic.
### **Fix Action**
Add canary label or traffic percentage to limit blast radius
### **Applies To**
  - **/chaos/**/*.yaml

## Chaos Without Team Notification

### **Id**
no-notification
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ChaosEngine(?!.*annotation|.*notification)
  - spec:(?!.*notify|.*slack|.*pagerduty)
### **Message**
Chaos experiment without notification. Team may not know it's running.
### **Fix Action**
Add notification to Slack or PagerDuty before experiment starts
### **Applies To**
  - **/chaos/**/*.yaml

## Network Chaos Affecting All Ports

### **Id**
network-chaos-all-ports
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pod-network.*(?!.*PORT)
  - network.*chaos(?!.*port)
### **Message**
Network chaos affecting all ports. May block monitoring and control plane.
### **Fix Action**
Specify target ports to avoid affecting health checks and metrics
### **Applies To**
  - **/chaos/**/*.yaml

## No Pre-Experiment Steady State Check

### **Id**
no-steady-state-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - experiments:(?!.*steady.*state|.*baseline)
  - ChaosEngine(?!.*probe.*type.*httpProbe)
### **Message**
No steady state verification before chaos. Can't compare impact.
### **Fix Action**
Add pre-chaos probe to verify system is healthy before injection
### **Applies To**
  - **/chaos/**/*.yaml

## No Post-Chaos Recovery Check

### **Id**
no-recovery-verification
### **Severity**
info
### **Type**
regex
### **Pattern**
  - experiments:(?!.*post.*action|.*recovery)
  - ChaosEngine(?!.*post.*chaos.*check)
### **Message**
No verification that system recovered after chaos.
### **Fix Action**
Add post-chaos probe to verify system returns to steady state
### **Applies To**
  - **/chaos/**/*.yaml

## Hardcoded Pod/Service Target

### **Id**
hardcoded-target
### **Severity**
info
### **Type**
regex
### **Pattern**
  - podName:.*"[^"]+pod[^"]*"
  - serviceName:.*"[^"]+-[0-9]+"
### **Message**
Hardcoded target in chaos experiment. May break when pods change.
### **Fix Action**
Use label selectors instead of hardcoded names
### **Applies To**
  - **/chaos/**/*.yaml