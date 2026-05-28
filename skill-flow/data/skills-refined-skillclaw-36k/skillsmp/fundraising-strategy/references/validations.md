# Fundraising Strategy - Validations

## Product Without Metrics Dashboard

### **Id**
no-metrics-dashboard
### **Severity**
info
### **Type**
regex
### **Pattern**
  - dashboard|Dashboard|analytics|Analytics
  - metrics|Metrics|reporting|Reporting
### **Message**
Dashboard/analytics reference without visible metrics implementation.
### **Fix Action**
Ensure key metrics are tracked for investor reporting
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - track|log|event|measure|count

## Payment Without Revenue Tracking

### **Id**
no-revenue-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - payment|Payment|checkout|Checkout
  - subscribe|Subscribe|purchase|Purchase
### **Message**
Payment flow without visible revenue tracking.
### **Fix Action**
Track MRR, ARR, and revenue metrics for fundraising
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - revenue|Revenue|mrr|MRR|arr|ARR|track

## User System Without Customer Tracking

### **Id**
no-customer-count
### **Severity**
info
### **Type**
regex
### **Pattern**
  - createUser|newUser|signup
  - registerUser|addUser
### **Message**
User creation without customer count tracking.
### **Fix Action**
Track customer counts and growth for investor updates
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - count|total|track|metric|analytics

## Subscription Without Churn Tracking

### **Id**
no-churn-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - cancel|Cancel|unsubscribe|Unsubscribe
  - churn|Churn|downgrade|Downgrade
### **Message**
Cancellation flow without churn rate tracking.
### **Fix Action**
Track churn rate for investor unit economics
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - churnRate|churn.*track|metric|analytics

## User Registration Without Cohort

### **Id**
no-cohort-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - signup|signUp|register|createUser
### **Message**
User creation without cohort tracking.
### **Fix Action**
Track signup cohorts for retention analysis
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - cohort|Cohort|signupDate|createdAt

## Revenue Without LTV Calculation

### **Id**
no-ltv-calculation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - revenue|Revenue|payment|Payment
  - subscription|Subscription
### **Message**
Revenue tracking without LTV calculation.
### **Fix Action**
Calculate and track LTV for unit economics
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - ltv|LTV|lifetime|lifetimeValue

## Acquisition Without CAC Tracking

### **Id**
no-cac-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - utm|referral|source|campaign
  - attribution|acquisition
### **Message**
Attribution tracking without CAC calculation.
### **Fix Action**
Calculate CAC by channel for unit economics
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - cac|CAC|cost.*acquisition|acquisitionCost

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
Activity tracking without retention metrics.
### **Fix Action**
Calculate DAU, MAU, retention for investor metrics
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - retention|dau|DAU|mau|MAU|d7|d30

## Revenue Changes Without NRR

### **Id**
no-nrr-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - upgrade|Upgrade|downgrade|Downgrade
  - expansion|Expansion|contraction
### **Message**
Revenue changes without net revenue retention tracking.
### **Fix Action**
Track NRR (expansion - churn) for SaaS metrics
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - nrr|NRR|netRevenue|revenueRetention

## Hardcoded Financial Values

### **Id**
hardcoded-financials
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - price.*=.*\d+\.\d+
  - amount.*=.*\d{3,}
### **Message**
Hardcoded financial values. Consider configuration.
### **Fix Action**
Move financial values to configuration for easy updates
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - config|Config|env|ENV|process\.env

## Financial Dashboard Without Runway

### **Id**
no-runway-calculation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - financials|Financials|dashboard|Dashboard
  - burn|Burn|expenses|Expenses
### **Message**
Financial tracking without runway calculation.
### **Fix Action**
Calculate runway (cash / monthly burn) for planning
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - runway|Runway|monthsLeft|cashRunway

## Metrics Without Growth Rate

### **Id**
no-growth-rate
### **Severity**
info
### **Type**
regex
### **Pattern**
  - revenue|Revenue|users|Users
  - customers|Customers|mrr|MRR
### **Message**
Metrics tracking without growth rate calculation.
### **Fix Action**
Calculate MoM and YoY growth rates for investor reporting
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - growth|Growth|rate|percent|yoy|mom