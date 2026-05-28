# Community Tooling - Sharp Edges

## Tool Vendor Lock

### **Id**
tool-vendor-lock
### **Summary**
Locked into tool that no longer fits
### **Severity**
medium
### **Situation**
Can't switch tools because data is trapped
### **Why**
  No export capability.
  Workflows built around tool.
  Team too invested to switch.
  Historical data would be lost.
  
### **Solution**
  ## Avoiding Vendor Lock-in
  
  ### Prevention
  - Evaluate export capabilities before adopting
  - Keep data in portable formats
  - Document workflows independently
  - Regular export backups
  - Negotiate data portability in contracts
  
  ### Mitigation
  | Scenario | Approach |
  |----------|----------|
  | API available | Build export scripts |
  | Limited export | Manual documentation |
  | No export | Screenshot/record key data |
  
  ### Switching Checklist
  - [ ] Export all member data
  - [ ] Document current workflows
  - [ ] Parallel run period
  - [ ] Communicate to community
  - [ ] Archive old platform access
  
### **Symptoms**
  - We can't leave because...
  - Tool pricing increases
  - Features removed
  - Better options available but stuck
### **Detection Pattern**
can't switch|locked in|no export|stuck with

## Bot Compromise

### **Id**
bot-compromise
### **Summary**
Discord bot token compromised
### **Severity**
critical
### **Situation**
Malicious actor gains control of bot
### **Why**
  Token exposed in code.
  Shared with wrong person.
  Compromised team member.
  
### **Solution**
  ## Bot Security
  
  ### Prevention
  - Never commit tokens to git
  - Use environment variables
  - Rotate tokens regularly
  - Limit who has access
  - Minimum required permissions
  
  ### If Compromised
  1. Immediately regenerate token in Discord
  2. Kick bot from server temporarily
  3. Audit what happened
  4. Check for damage
  5. Re-add with new token
  6. Inform community if needed
  
  ### Token Security Checklist
  - [ ] Token in env vars, not code
  - [ ] .gitignore includes .env
  - [ ] Limited team access
  - [ ] Rotation schedule
  - [ ] Audit log monitoring
  
### **Symptoms**
  - Bot sending strange messages
  - Bot mass-DMing members
  - Bot deleting channels
  - Unknown bot actions
### **Detection Pattern**
bot hacked|compromised|strange messages|bot went crazy

## Analytics Paralysis

### **Id**
analytics-paralysis
### **Summary**
Too much data, no actionable insights
### **Severity**
medium
### **Situation**
Dashboard overload, no clear actions
### **Why**
  Tracking everything possible.
  No focus on what matters.
  Data without context.
  
### **Solution**
  ## Analytics Focus
  
  ### Hierarchy of Metrics
  | Level | Focus | Action Frequency |
  |-------|-------|------------------|
  | North Star | 1 metric | Quarterly review |
  | Primary | 3-5 metrics | Monthly review |
  | Secondary | 5-10 metrics | Weekly review |
  | Diagnostic | As needed | When investigating |
  
  ### From Data to Action
  1. Define the question first
  2. Find relevant metric
  3. Set baseline
  4. Monitor change
  5. Correlate with actions
  
  ### Dashboard Design
  - One-page summary
  - Clear trends (not just numbers)
  - Compared to goals
  - Actionable insights highlighted
  - Easy drill-down
  
### **Symptoms**
  - Multiple dashboards
  - We track everything
  - No one looks at dashboards
  - Can't answer basic questions
### **Detection Pattern**
too much data|analysis paralysis|don't know what to look at

## Automation Brittleness

### **Id**
automation-brittleness
### **Summary**
Automated workflows break silently
### **Severity**
medium
### **Situation**
Automation stops working, no one notices
### **Why**
  No monitoring.
  Platform changes break integration.
  API changes.
  Token expiration.
  
### **Solution**
  ## Robust Automation
  
  ### Monitoring
  - Error notifications
  - Regular test runs
  - Success logging
  - Human-in-loop for critical flows
  
  ### Design Principles
  - Fail loudly, not silently
  - Idempotent where possible
  - Retry with backoff
  - Fallback procedures
  - Document manual alternative
  
  ### Maintenance Schedule
  | Frequency | Check |
  |-----------|-------|
  | Daily | Critical flows running |
  | Weekly | Review error logs |
  | Monthly | Test all automations |
  | Quarterly | Full audit |
  
### **Symptoms**
  - That automation hasn't run in weeks
  - Members not getting onboarded
  - Notifications not sending
  - Data not syncing
### **Detection Pattern**
broken|stopped working|not running|haven't received