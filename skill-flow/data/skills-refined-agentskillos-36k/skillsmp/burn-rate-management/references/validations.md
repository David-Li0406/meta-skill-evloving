# Burn Rate Management - Validations

## No Runway Calculation

### **Id**
burn-no-runway-calc
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)(burn|spending|expenses|cash)(?!.*runway|.*months?\s+left|.*\d+\s*months)
### **Message**
Burn mentioned but no runway calculation. Calculate: cash / monthly burn = months.
### **Fix Action**
Add: 'Runway: $X cash / $Y monthly burn = Z months'
### **Applies To**
  - **/*.md

## Missing Budget Breakdown

### **Id**
burn-missing-budget
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)(budget|spend|expenses)(?!.*payroll|.*infrastructure|.*marketing|.*\$\d+)
### **Message**
Budget mentioned without breakdown. Detail: payroll, infra, marketing, etc.
### **Fix Action**
Add breakdown: 'Payroll: $X, Infra: $Y, Marketing: $Z, Other: $A = $Total/mo'
### **Applies To**
  - **/*.md

## Untracked Recurring Expenses

### **Id**
burn-untracked-expenses
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(subscri|saas|tool|service)(?!.*\$/.*month|.*cost|.*expense|.*budget)
### **Message**
Service mentioned without cost tracking. Document all recurring expenses.
### **Fix Action**
Track: 'Service X: $Y/month, Service Z: $A/month' in budget sheet
### **Applies To**
  - **/*.md

## Optimistic Revenue Projections

### **Id**
burn-optimistic-projections
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(expect|project|forecast)\s+(revenue|sales)(?!.*conservative|.*worst\s+case|.*assume)
### **Message**
Revenue projection without conservative scenario. Model worst-case assumptions.
### **Fix Action**
Add: 'Best: $X, Likely: $Y, Worst: $Z - planning for Worst case'
### **Applies To**
  - **/*.md

## No Burn Rate Metrics

### **Id**
burn-no-metrics
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)burn\s+rate(?!.*\$\d+|.*per\s+month|.*monthly)
### **Message**
Burn rate mentioned without specific dollar amount per month.
### **Fix Action**
Add: 'Current burn: $X/month, Target: $Y/month by [date]'
### **Applies To**
  - **/*.md

## Cash Balance Not Tracked

### **Id**
burn-no-cash-tracking
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - (?i)(finances|money|cash)(?!.*\$\d+|.*balance|.*bank|.*current)
### **Message**
Cash mentioned but not tracked. Know your exact cash balance weekly.
### **Fix Action**
Track weekly: 'Cash balance: $X as of [date], Updated every Monday'
### **Applies To**
  - **/*.md

## Hiring Without Runway Check

### **Id**
burn-hiring-without-runway
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - (?i)(hire|hiring|new\s+role|position)(?!.*runway|.*afford|.*burn)
### **Message**
Hiring plan without runway impact analysis. Each hire costs 12-18 months comp.
### **Fix Action**
Calculate: 'New hire costs $X/year, reduces runway by Y months to Z months'
### **Applies To**
  - **/*.md

## No Cash Milestones Defined

### **Id**
burn-no-milestones
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)milestones?(?!.*revenue|.*profitability|.*reduce\s+burn|.*extend\s+runway)
### **Message**
Milestones without cash impact. Link to revenue, burn reduction, or fundraising.
### **Fix Action**
Add: 'Milestone X by [date]: Hit $Y MRR, reduces burn to $Z/month'
### **Applies To**
  - **/*.md

## No Plan B for Running Out

### **Id**
burn-no-zero-plan
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - (?i)runway(?!.*if we|.*plan\s+b|.*fallback|.*contingency)
### **Message**
No contingency plan for low runway. Define actions at 12mo, 6mo, 3mo marks.
### **Fix Action**
Add: 'If runway < 6mo: freeze hiring, cut X. If < 3mo: reduce to 2 founders'
### **Applies To**
  - **/*.md

## Tracking Vanity Not Cash Metrics

### **Id**
burn-vanity-metrics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(tracking|measuring)\s+(followers|likes|page\s+views|signups)(?!.*revenue|.*paying)
### **Message**
Tracking vanity metrics, not cash metrics. Focus on revenue, burn, runway.
### **Fix Action**
Prioritize: MRR, burn rate, runway, CAC payback, gross margin
### **Applies To**
  - **/*.md

## No Path to Profitability

### **Id**
burn-unclear-path-profitability
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)(profitable|profitability)(?!.*when|.*by\s+\d|.*at\s+\$\d|.*month)
### **Message**
Profitability mentioned without timeline or revenue target.
### **Fix Action**
Define: 'Profitable at $X MRR (covers $Y burn), achievable by [date]'
### **Applies To**
  - **/*.md

## No Regular Burn Review

### **Id**
burn-no-review-cadence
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(burn|budget|runway)(?!.*weekly|.*monthly|.*review|.*check)
### **Message**
No regular burn review cadence. Review weekly/monthly to catch increases early.
### **Fix Action**
Set: 'Monthly burn review: compare actual to budget, adjust forecast'
### **Applies To**
  - **/*.md