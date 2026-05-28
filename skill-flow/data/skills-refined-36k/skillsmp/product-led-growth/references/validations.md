# Product Led Growth - Validations

## Missing Activation Metric

### **Id**
no-activation-metric
### **Severity**
high
### **Type**
conceptual
### **Check**
PLG strategy must define a clear, measurable activation metric
### **Message**
PLG motion lacks defined activation metric.
### **Fix Action**
Define activation metric: specific action that correlates with retention

## Value Gate Before Signup

### **Id**
signup-before-value
### **Severity**
high
### **Type**
conceptual
### **Check**
Users should see value before being forced to sign up
### **Indicators**
  - Sign up required before any product interaction
  - Can't see product without account
### **Message**
Signup wall before any value demonstration.
### **Fix Action**
Allow product preview or free usage before requiring signup

## Unclear Free Tier Limits

### **Id**
free-tier-undefined
### **Severity**
medium
### **Type**
conceptual
### **Check**
Free tier must have clear, value-aligned limits
### **Indicators**
  - Unlimited free tier
  - Vague limits on free
### **Message**
Free tier lacks clear boundaries for upgrade triggers.
### **Fix Action**
Define specific limits that trigger upgrade when value proven

## Missing PQL Definition

### **Id**
no-pql-definition
### **Severity**
medium
### **Type**
conceptual
### **Check**
PLG with sales must define PQL criteria
### **Message**
No product-qualified lead definition for sales handoff.
### **Fix Action**
Define PQL scoring based on usage + fit + intent signals

## Vanity Funnel Metrics

### **Id**
vanity-funnel-metrics
### **Severity**
medium
### **Type**
conceptual
### **Check**
Funnel metrics should measure value delivery, not just progress
### **Indicators**
  - Measuring signups without activation
  - Tracking page views without conversions
### **Message**
PLG metrics focus on vanity (signups) over value (activation).
### **Fix Action**
Track full funnel from signup through activation to paid

## Single Conversion Path

### **Id**
single-conversion-path
### **Severity**
low
### **Type**
conceptual
### **Check**
Multiple paths to paid should exist
### **Indicators**
  - Only one way to upgrade
  - Single paywall location
### **Message**
PLG relies on single conversion trigger.
### **Fix Action**
Add multiple upgrade triggers: limits, team needs, features

## Missing Analytics Instrumentation

### **Id**
no-instrumentation-plan
### **Severity**
high
### **Type**
conceptual
### **Check**
PLG requires comprehensive event tracking
### **Message**
PLG strategy lacks analytics instrumentation plan.
### **Fix Action**
Define events to track at each funnel stage