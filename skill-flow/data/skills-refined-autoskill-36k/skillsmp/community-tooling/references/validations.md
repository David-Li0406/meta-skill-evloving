# Community Tooling - Validations

## No Tool Documentation

### **Id**
no-tool-documentation
### **Severity**
medium
### **Type**
conceptual
### **Check**
Tool configuration should be documented
### **Indicators**
  - Only one person knows setup
  - No runbooks
  - Tribal knowledge
### **Message**
Tool configuration not documented.
### **Fix Action**
Document all tool configurations, bot settings, and integration details

## No Tool Backup Plan

### **Id**
no-backup-plan
### **Severity**
high
### **Type**
conceptual
### **Check**
Should have fallback if tool fails
### **Indicators**
  - No manual alternative
  - Tool is single point of failure
  - No data exports
### **Message**
No backup plan if key tool fails.
### **Fix Action**
Document manual fallback procedures and regular data exports

## Bot Tokens in Code

### **Id**
token-in-code
### **Severity**
critical
### **Type**
pattern
### **Check**
Bot tokens should never be in code
### **Pattern**
discord.*token|bot.*token|client.*secret
### **Indicators**
  - Hardcoded tokens
  - Tokens in git history
  - Shared credentials
### **Message**
Bot tokens or secrets found in code.
### **Fix Action**
Move to environment variables, rotate compromised tokens

## Too Many Bots

### **Id**
too-many-bots
### **Severity**
low
### **Type**
conceptual
### **Check**
Discord shouldn't have excessive bots
### **Indicators**
  - More than 10 bots
  - Overlapping functionality
  - Unused bots present
### **Message**
Too many bots in server.
### **Fix Action**
Audit bots, remove unused, consolidate functionality

## No Regular Tool Audit

### **Id**
no-tool-audit
### **Severity**
medium
### **Type**
conceptual
### **Check**
Tools should be reviewed periodically
### **Indicators**
  - Tools added never reviewed
  - Paying for unused features
  - No evaluation schedule
### **Message**
No regular tool audit process.
### **Fix Action**
Implement quarterly tool audit to review usage, cost, and fit