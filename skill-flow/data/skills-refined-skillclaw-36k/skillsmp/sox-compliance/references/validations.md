# Sox Compliance - Validations

## Direct Database Mutation

### **Id**
direct-db-mutation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - db\.execute.*UPDATE
  - db\.execute.*DELETE
  - query.*UPDATE.*WHERE
  - rawQuery.*UPDATE
### **Message**
Direct database mutation bypasses audit trail.
### **Fix Action**
Use application service with audit logging
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py

## Missing Audit Log

### **Id**
missing-audit-log
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - save\(\)(?!.*auditLog|.*createAudit|.*logChange)
  - update\((?!.*audit)
### **Message**
Data modification may not be audit logged.
### **Fix Action**
Add audit log entry for all data changes
### **Applies To**
  - **/*.ts
  - **/*.js

## Hardcoded Credentials

### **Id**
hardcoded-credentials
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password\s*[:=]\s*['"][^'"]+['"]
  - apiKey\s*[:=]\s*['"][^'"]+['"]
  - secret\s*[:=]\s*['"][^'"]+['"]
### **Message**
Hardcoded credentials violate access control requirements.
### **Fix Action**
Use environment variables or secrets manager
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py

## Action Without User Context

### **Id**
no-user-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - createTransaction(?!.*userId|.*user|.*createdBy)
  - approvePayment(?!.*approverId|.*approvedBy)
### **Message**
Financial action may not track responsible user.
### **Fix Action**
Include user ID in all financial transactions
### **Applies To**
  - **/*.ts
  - **/*.js

## Same User Approve Pattern

### **Id**
same-user-approve
### **Severity**
error
### **Type**
regex
### **Pattern**
  - if.*creator.*===.*approver
  - submittedBy.*===.*approvedBy(?!.*throw|.*error)
### **Message**
Self-approval check may be missing or bypassed.
### **Fix Action**
Enforce different users for create and approve
### **Applies To**
  - **/*.ts
  - **/*.js

## Admin Bypass Logic

### **Id**
admin-bypass
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if.*isAdmin.*skip.*approval
  - admin.*bypass.*control
  - role.*===.*admin.*return true
### **Message**
Admin users may bypass controls.
### **Fix Action**
Apply controls to all users including admins
### **Applies To**
  - **/*.ts
  - **/*.js

## Missing Change Request Logging

### **Id**
no-change-logging
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - deploy(?!.*changeRequest|.*changeId|.*ticket)
  - pushToProduction(?!.*approved)
### **Message**
Deployment may not be tied to change request.
### **Fix Action**
Require change ticket for all deployments
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.sh

## No Data Retention Enforcement

### **Id**
retention-not-enforced
### **Severity**
info
### **Type**
regex
### **Pattern**
  - delete.*audit(?!.*older.*7.*year)
  - purge.*log(?!.*retention)
### **Message**
Audit data deletion may violate retention requirements.
### **Fix Action**
Enforce 7-year retention for financial audit logs
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.sql