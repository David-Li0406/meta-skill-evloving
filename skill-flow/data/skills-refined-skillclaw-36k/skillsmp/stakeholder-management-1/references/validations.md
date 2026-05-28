# Stakeholder Management - Validations

## Application Without Metrics Dashboard

### **Id**
no-metrics-dashboard
### **Severity**
info
### **Type**
regex
### **Pattern**
  - analytics|Analytics|dashboard|Dashboard
  - metrics|Metrics|reporting|Reporting
### **Message**
Analytics reference without exportable metrics for stakeholder reporting.
### **Fix Action**
Ensure key metrics are easily exportable for investor updates
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - export|csv|download|report

## Subscription Without MRR Tracking

### **Id**
no-mrr-calculation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - subscription|Subscription|recurring
  - stripe.*subscription|createSubscription
### **Message**
Subscription system without MRR calculation for investor reporting.
### **Fix Action**
Track and calculate MRR for stakeholder updates
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - mrr|MRR|monthlyRecurring|monthly_recurring

## Hardcoded Metrics in Reports

### **Id**
hardcoded-metrics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - revenue.*=.*\d+
  - users.*=.*\d{3,}
  - customers.*=.*\d+
### **Message**
Hardcoded metric values. Should be calculated from source data.
### **Fix Action**
Calculate metrics dynamically from database for accurate stakeholder reporting
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - mock|test|example|placeholder|default

## Data Changes Without Audit Trail

### **Id**
no-audit-trail
### **Severity**
info
### **Type**
regex
### **Pattern**
  - update.*SET|UPDATE|delete|DELETE
  - \.update\(|\.delete\(
### **Message**
Data modifications without audit trail for stakeholder accountability.
### **Fix Action**
Add audit logging for board-level data integrity requirements
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - audit|log|history|createdAt|updatedAt|deletedAt

## Customer Deletion Without Churn Tracking

### **Id**
no-churn-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - deleteCustomer|deleteUser|cancelSubscription
  - churn|Churn|cancel|Cancel
### **Message**
Customer removal without churn rate tracking.
### **Fix Action**
Track churn rate and reasons for stakeholder reporting
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - churnRate|churn.*reason|cancelReason

## Finance Dashboard Without Runway

### **Id**
no-runway-calculation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - finance|Finance|budget|Budget
  - burn|Burn|expenses|Expenses
### **Message**
Financial tracking without runway calculation.
### **Fix Action**
Add runway calculation (cash / monthly burn) for stakeholder visibility
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - runway|Runway|monthsRemaining|cashRunway

## User Tracking Without Cohort Analysis

### **Id**
no-cohort-analysis
### **Severity**
info
### **Type**
regex
### **Pattern**
  - createdAt|signupDate|registrationDate
  - newUser|createUser|signup
### **Message**
User tracking without cohort analysis capability.
### **Fix Action**
Track signup cohorts for retention analysis in stakeholder reporting
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - cohort|Cohort|vintage|retentionCohort

## Auth System Without Investor Access

### **Id**
no-investor-role
### **Severity**
info
### **Type**
regex
### **Pattern**
  - role.*admin|isAdmin|adminRole
  - permissions|authorize|checkRole
### **Message**
Role system without investor/board member access consideration.
### **Fix Action**
Consider read-only stakeholder access for transparency
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - investor|board|stakeholder|readonly|viewer

## Reporting Without Scheduled Delivery

### **Id**
no-scheduled-reports
### **Severity**
info
### **Type**
regex
### **Pattern**
  - report|Report|generateReport
  - export|Export|download|Download
### **Message**
Manual report generation without scheduled delivery.
### **Fix Action**
Add scheduled/automated report delivery for consistent stakeholder updates
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - schedule|cron|automate|recurring|weekly|monthly

## User Activity Without Retention Tracking

### **Id**
no-retention-metrics
### **Severity**
info
### **Type**
regex
### **Pattern**
  - lastActive|lastLogin|lastSeen
  - activeUser|dailyActive|monthlyActive
### **Message**
Activity tracking without retention metrics for stakeholder reporting.
### **Fix Action**
Calculate and track retention metrics (D1, D7, D30)
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - retention|d1|d7|d30|dau|mau|wau

## Data Without Growth Rate Calculation

### **Id**
no-growth-metrics
### **Severity**
info
### **Type**
regex
### **Pattern**
  - count|total|sum
  - users|customers|revenue
### **Message**
Aggregate metrics without growth rate calculation.
### **Fix Action**
Add MoM and YoY growth rate calculations for stakeholder updates
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - growth|Growth|rate|percent|yoy|mom|wow

## Multiple Metric Definitions

### **Id**
inconsistent-metric-definition
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - const.*revenue|let.*revenue|var.*revenue
  - calculateRevenue|getRevenue|computeRevenue
### **Message**
Multiple revenue/metric calculations may cause inconsistent reporting.
### **Fix Action**
Centralize metric calculations for consistent stakeholder reporting
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - MetricsService|metricsUtils|centralized

## Dashboard Without Data Export

### **Id**
no-data-export
### **Severity**
info
### **Type**
regex
### **Pattern**
  - dashboard|Dashboard|analytics|Analytics
  - chart|Chart|graph|Graph
### **Message**
Dashboard without data export for stakeholder reporting.
### **Fix Action**
Add CSV/PDF export capability for stakeholder presentations
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - export|download|csv|pdf|excel

## Metrics Without Historical Tracking

### **Id**
no-historical-data
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - current.*metric|latest.*count
  - getMetric|fetchMetric
### **Message**
Current metrics without historical tracking.
### **Fix Action**
Store historical metric snapshots for trend analysis in updates
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - history|historical|trend|snapshot|timeseries

## Integration Without Partner Attribution

### **Id**
no-partner-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - integration|Integration|partner|Partner
  - referral|affiliate|channel
### **Message**
Partner integration without attribution tracking.
### **Fix Action**
Track partner-sourced revenue and users for partnership reporting
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - partnerRevenue|partnerAttribution|channelSource