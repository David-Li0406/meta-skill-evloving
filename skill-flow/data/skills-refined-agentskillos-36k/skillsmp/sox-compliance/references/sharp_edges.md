# Sox Compliance - Sharp Edges

## Shared Service Account Credentials

### **Id**
shared-service-accounts
### **Severity**
critical
### **Summary**
Multiple users sharing the same service account breaks accountability
### **Symptoms**
  - Application uses single service account for all access
  - Multiple people know the password
  - Cannot trace actions to individuals
### **Why**
  SOX requires individual accountability for actions affecting financial
  data. When multiple people share credentials, you cannot determine
  who performed a specific action. This is a common material weakness.
  
### **Gotcha**
  "The finance team all uses the 'financeapp' service account to
   access the ERP system. It's easier to manage one account."
  
  # Who made that journal entry adjustment? No one knows!
  
### **Solution**
  1. Individual user accounts for all access:
     - Each user has unique credentials
     - Tie actions to individuals in audit logs
  
  2. Service accounts for automation only:
     - Not shared with humans
     - Rotate credentials regularly
     - Monitor usage for anomalies
  
  3. Privileged Access Management:
     - Check out credentials when needed
     - Full session recording
     - Automatic rotation after use
  

## Developers Have Production Database Access

### **Id**
developer-prod-access
### **Severity**
critical
### **Summary**
Segregation of duties failure - same person can write and deploy code
### **Symptoms**
  - Developers can access production directly
  - Same person develops and deploys
  - No change approval process
### **Why**
  SOX requires segregation of duties to prevent fraud. If developers
  can both write code and push to production, they could manipulate
  financial calculations without detection. This is a common ITGC
  material weakness.
  
### **Gotcha**
  "Our senior developer handles deployments because he knows the
   system best. He just SSHs in and pushes the changes."
  
  # He could modify the revenue calculation and no one would know!
  
### **Solution**
  1. Separate environments with different access:
     - Dev: Developers have access
     - Test: QA has access
     - Prod: Operations only (not developers)
  
  2. Automated deployment pipelines:
     - Code flows through pipeline
     - Approvals required at each stage
     - Developers cannot push directly
  
  3. Emergency change procedures:
     - Documented exception process
     - Post-change review required
     - Temporary access with monitoring
  

## Financial Data Changes Without Audit Trail

### **Id**
missing-audit-trail
### **Severity**
high
### **Summary**
No log of who changed what, when, and why
### **Symptoms**
  - Direct database updates allowed
  - No change logging
  - Cannot reconstruct history
### **Why**
  SOX Section 802 requires record retention. Auditors need to trace
  any financial data back to its source. Without audit trails, you
  cannot prove controls operated effectively.
  
### **Gotcha**
  UPDATE accounts SET balance = 1000000 WHERE account_id = 12345;
  
  # Who ran this? When? Why? No one knows!
  
### **Solution**
  1. Application-level audit logging:
     - Log all data changes (CREATE, UPDATE, DELETE)
     - Include: user, timestamp, old value, new value
     - Store in immutable audit table
  
  2. Database-level protection:
     - Revoke direct UPDATE/DELETE from users
     - All changes through application with logging
     - Trigger-based audit trail as backup
  
  3. Log integrity:
     - Write-once audit logs (immutable)
     - Separate log storage from app database
     - Regular log verification
  

## No Periodic Access Reviews

### **Id**
no-access-reviews
### **Severity**
high
### **Summary**
Stale access accumulates as people change roles
### **Symptoms**
  - Former employees still have access
  - Role changes don't trigger access review
  - No documentation of access decisions
### **Why**
  Access rights accumulate over time. Without regular reviews,
  people retain access they no longer need. This creates fraud
  risk and segregation of duties failures.
  
### **Gotcha**
  "John moved from Accounts Payable to Sales 6 months ago, but
   he still has AP approval access because no one removed it."
  
  # John could approve his own invoices from his old role!
  
### **Solution**
  1. Quarterly access reviews:
     - Manager certifies each user's access
     - Compare current access to job requirements
     - Remove stale access
  
  2. Role-based access with lifecycle:
     - Access tied to job role
     - Role change triggers access review
     - Termination removes all access immediately
  
  3. Privileged access review:
     - Monthly review of admin access
     - Justify each privileged account
     - Time-limited elevated access
  