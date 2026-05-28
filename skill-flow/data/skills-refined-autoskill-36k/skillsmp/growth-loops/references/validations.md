# Growth Loops - Validations

## Loop Definition Without Metrics

### **Id**
loop-without-metrics
### **Severity**
high
### **Type**
conceptual
### **Check**
Loop strategy document must define measurable metrics for each loop stage
### **Message**
Growth loop defined without clear metrics at each stage.
### **Fix Action**
Add specific, measurable KPIs for: trigger rate, action rate, conversion rate, cycle time

## Single Loop Strategy

### **Id**
single-loop-strategy
### **Severity**
medium
### **Type**
conceptual
### **Check**
Growth strategy should not depend on single acquisition loop
### **Message**
Strategy relies on single growth loop without backup.
### **Fix Action**
Add secondary loop or acknowledge risk with mitigation plan

## Vanity Metric Focus

### **Id**
vanity-metric-focus
### **Severity**
high
### **Type**
conceptual
### **Check**
Loop metrics should measure conversions, not just activities
### **Indicators**
  - "invites sent" without "invites accepted"
  - "shares" without "share conversions"
  - "referral links" without "referral signups"
### **Message**
Loop metrics focus on activity rather than conversion.
### **Fix Action**
Track end-to-end conversion, not just top-of-loop activity

## Missing Cycle Time Metric

### **Id**
missing-cycle-time
### **Severity**
medium
### **Type**
conceptual
### **Check**
Loop analysis must include cycle time measurement
### **Message**
Loop analysis missing cycle time - critical for growth projection.
### **Fix Action**
Add average cycle time measurement and optimization target

## No Loop Quality Tracking

### **Id**
no-quality-tracking
### **Severity**
medium
### **Type**
conceptual
### **Check**
Loop metrics should include quality indicators (retention, LTV)
### **Message**
Loop tracking volume without quality metrics.
### **Fix Action**
Add retention comparison: loop-acquired vs organic users

## Unrealistic K-Factor Target

### **Id**
unrealistic-k-factor
### **Severity**
low
### **Type**
conceptual
### **Check**
K-factor targets should be grounded in benchmarks
### **Message**
K-factor target may be unrealistic for product category.
### **Fix Action**
Benchmark against similar products; most sustainable K-factors are 0.3-0.8