# Community Analytics - Validations

## No Health Metrics Defined

### **Id**
no-health-metrics
### **Severity**
high
### **Type**
conceptual
### **Check**
Should have community health metrics
### **Indicators**
  - No health dashboard
  - Only tracking growth
  - No retention tracking
### **Message**
No community health metrics defined.
### **Fix Action**
Define health score with activity, engagement, retention, sentiment

## Not Tracking Retention

### **Id**
no-retention-tracking
### **Severity**
high
### **Type**
conceptual
### **Check**
Should track retention by cohort
### **Indicators**
  - No cohort analysis
  - Don't know retention rates
  - Only track new joins
### **Message**
Retention not being tracked.
### **Fix Action**
Implement cohort retention tracking (D1, D7, D30, D90)

## Not Measuring Engagement Depth

### **Id**
no-engagement-depth
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should measure quality of engagement
### **Indicators**
  - Only counting messages
  - No thread depth analysis
  - No contribution levels
### **Message**
Engagement depth not measured.
### **Fix Action**
Track engagement levels and conversation depth

## Not Tracking Sentiment

### **Id**
no-sentiment-tracking
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should measure member sentiment
### **Indicators**
  - No NPS or satisfaction survey
  - No sentiment analysis
  - Surprised by negative feedback
### **Message**
Member sentiment not tracked.
### **Fix Action**
Implement regular sentiment measurement

## No Regular Reporting

### **Id**
no-regular-reporting
### **Severity**
low
### **Type**
conceptual
### **Check**
Should have regular analytics reports
### **Indicators**
  - Ad-hoc analysis only
  - No reporting cadence
  - Leadership uninformed
### **Message**
No regular reporting cadence.
### **Fix Action**
Establish weekly/monthly reporting rhythm