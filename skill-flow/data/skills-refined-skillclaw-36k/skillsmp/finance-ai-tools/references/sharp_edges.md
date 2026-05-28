# Finance - Sharp Edges

## Ai Categorization Errors

### **Id**
ai-categorization-errors
### **Summary**
AI miscategorizes transactions
### **Severity**
high
### **Tools Affected**
  - quickbooks-ai
  - xero
  - ramp
### **Situation**
AI learns from limited data
### **Why**
Financial data is nuanced, categories overlap
### **Solution**
Review AI suggestions, train with corrections, audit monthly
### **Symptoms**
  - Expenses in wrong categories
  - Tax deductions missed
  - Reports inaccurate

## Bank Feed Delays

### **Id**
bank-feed-delays
### **Summary**
Bank connections break or lag
### **Severity**
medium
### **Tools Affected**
  - all
### **Situation**
Bank APIs change, connections drop
### **Why**
Banks update security, third-party aggregators fail
### **Solution**
Monitor connections, have backup import process
### **Symptoms**
  - Missing transactions
  - Duplicate entries after reconnect
  - Reconciliation gaps

## Integration Data Sync

### **Id**
integration-data-sync
### **Summary**
Data doesn't sync between tools
### **Severity**
high
### **Tools Affected**
  - all
### **Situation**
Multi-tool finance stack
### **Why**
Different data models, timing issues
### **Solution**
Single source of truth, audit sync regularly
### **Symptoms**
  - Numbers don't match across systems
  - Duplicate data
  - Missing records

## Forecast Over Confidence

### **Id**
forecast-over-confidence
### **Summary**
AI forecasts treated as certainty
### **Severity**
critical
### **Tools Affected**
  - planful
  - anaplan
  - runway-finance
### **Situation**
AI generates confident predictions
### **Why**
Models extrapolate from limited data
### **Solution**
Always use scenarios, understand assumptions
### **Symptoms**
  - Missed runway
  - Over-hiring based on projections
  - Board confusion when actuals differ

## Tax Compliance Gaps

### **Id**
tax-compliance-gaps
### **Summary**
AI doesn't catch all tax rules
### **Severity**
critical
### **Tools Affected**
  - avalara
  - quickbooks-ai
### **Situation**
Tax laws are complex and local
### **Why**
AI can't know every jurisdiction, every exception
### **Solution**
Work with tax professional, don't rely solely on AI
### **Symptoms**
  - Nexus violations
  - Incorrect tax rates
  - Audit exposure

## Expense Policy Gaming

### **Id**
expense-policy-gaming
### **Summary**
Employees game AI expense rules
### **Severity**
medium
### **Tools Affected**
  - ramp
  - brex
  - expensify
### **Situation**
AI enforces policies automatically
### **Why**
People learn to phrase things to pass AI checks
### **Solution**
Random audits, manager reviews, clear policies
### **Symptoms**
  - Unusual spending patterns
  - Creative expense descriptions
  - Policy violations that slip through

## Receipt Ocr Errors

### **Id**
receipt-ocr-errors
### **Summary**
Receipt scanning makes mistakes
### **Severity**
medium
### **Tools Affected**
  - expensify
  - ramp
  - quickbooks-ai
### **Situation**
AI reads receipts automatically
### **Why**
Poor image quality, unusual formats
### **Solution**
Verify large expenses, spot-check regularly
### **Symptoms**
  - Wrong amounts
  - Incorrect vendors
  - Missing tax details

## Multi Currency Complexity

### **Id**
multi-currency-complexity
### **Summary**
Currency conversion causes issues
### **Severity**
high
### **Tools Affected**
  - xero
  - quickbooks-ai
  - sage-intacct
### **Situation**
International business
### **Why**
Exchange rates fluctuate, timing matters
### **Solution**
Consistent rate sources, understand gain/loss
### **Symptoms**
  - Unexpected forex gains/losses
  - Reconciliation nightmares
  - Reporting inconsistencies

## Audit Trail Gaps

### **Id**
audit-trail-gaps
### **Summary**
AI changes without documentation
### **Severity**
high
### **Tools Affected**
  - all
### **Situation**
AI auto-corrects or adjusts
### **Why**
Automation can obscure what happened
### **Solution**
Ensure full audit logs, review AI actions
### **Symptoms**
  - Can't explain changes to auditors
  - Historical data looks different
  - Compliance questions

## Startup Burn Miscalculation

### **Id**
startup-burn-miscalculation
### **Summary**
AI calculates runway wrong
### **Severity**
critical
### **Tools Affected**
  - runway-finance
  - finmark
### **Situation**
Cash runway is critical metric
### **Why**
AI may not account for timing, commitments
### **Solution**
Manual runway check, include all obligations
### **Symptoms**
  - Surprised by cash crunch
  - Missed payroll risk
  - Emergency fundraising