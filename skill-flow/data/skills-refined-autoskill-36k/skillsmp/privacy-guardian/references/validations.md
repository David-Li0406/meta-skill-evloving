# Privacy Guardian - Validations

## Hardcoded Secret or API Key

### **Id**
hardcoded-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - API_KEY.*=.*["'][a-zA-Z0-9]{20,}["']
  - SECRET.*=.*["'][a-zA-Z0-9]{20,}["']
  - PASSWORD.*=.*["'][^"']+["']
  - Fernet\(b["']
  - ENCRYPTION_KEY.*=.*["']
### **Message**
Hardcoded secret detected. Use environment variables or secret manager.
### **Fix Action**
Move secret to environment variable or secret management system
### **Applies To**
  - **/*.py
  - **/*.js
  - **/*.ts

## PII Logged to Application Logs

### **Id**
pii-in-log
### **Severity**
error
### **Type**
regex
### **Pattern**
  - log.*\\(.*email
  - log.*\\(.*password
  - log.*\\(.*ssn
  - log.*\\(.*phone
  - print\\(.*user\\.name
  - logger.*content
### **Message**
Potential PII in log statement. Sanitize before logging.
### **Fix Action**
Remove PII from log or use anonymized identifiers
### **Applies To**
  - **/*.py

## Embedding Without PII Check

### **Id**
no-pii-check-before-embed
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - embed\\(.*content(?!.*sanitiz)
  - embed\\(.*text(?!.*pii|.*clean)
  - embedder.*memory\\.content
### **Message**
Embedding content without PII sanitization. PII may be reconstructable.
### **Fix Action**
Sanitize PII before embedding text
### **Applies To**
  - **/embedding/**/*.py
  - **/memory/**/*.py

## Encryption Without Key Rotation

### **Id**
encryption-no-rotation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Fernet\\(.*os\\.environ
  - AES.*key.*=.*config
  - encryption_key.*=.*settings
### **Message**
Static encryption key without rotation mechanism.
### **Fix Action**
Implement envelope encryption with key rotation
### **Applies To**
  - **/crypto/**/*.py
  - **/encryption/**/*.py

## Differential Privacy Without Budget Tracking

### **Id**
dp-no-budget-track
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - laplace.*epsilon(?!.*budget)
  - differential.*privacy(?!.*track|.*budget|.*account)
  - add.*noise.*epsilon
### **Message**
Differential privacy without budget tracking. Privacy degrades over queries.
### **Fix Action**
Track and limit privacy budget per user
### **Applies To**
  - **/privacy/**/*.py
  - **/federation/**/*.py

## Audit Log Without Immutability

### **Id**
audit-log-mutable
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - INSERT INTO audit(?!.*hash)
  - audit.*log(?!.*append|.*immutable|.*chain)
### **Message**
Audit log without hash chain or immutability guarantee.
### **Fix Action**
Implement hash chain and append-only constraints
### **Applies To**
  - **/audit/**/*.py
  - **/*audit*.py

## Data Access Without Audit Logging

### **Id**
access-no-audit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - get.*memory(?!.*audit)
  - fetch.*user.*data(?!.*log)
  - SELECT.*FROM.*memories(?!.*audit)
### **Message**
Data access without audit logging. Can't track who accessed what.
### **Fix Action**
Add audit logging for all data access
### **Applies To**
  - **/memory/**/*.py
  - **/db/**/*.py

## Data Deletion Without Verification

### **Id**
deletion-no-verify
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DELETE.*FROM(?!.*verify|.*confirm)
  - delete.*user.*data(?!.*all|.*complete)
### **Message**
Deletion without verification. Data may remain in backups/caches.
### **Fix Action**
Verify deletion across all data stores
### **Applies To**
  - **/db/**/*.py
  - **/deletion/**/*.py

## Data Storage Without Retention Policy

### **Id**
no-retention-policy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - INSERT INTO.*memories(?!.*expires|.*retention)
  - store.*memory(?!.*ttl|.*retention)
### **Message**
Data stored without retention policy. May accumulate indefinitely.
### **Fix Action**
Add retention policy with automated cleanup
### **Applies To**
  - **/memory/**/*.py
  - **/storage/**/*.py

## Federation Without Aggregation Threshold

### **Id**
federation-no-threshold
### **Severity**
error
### **Type**
regex
### **Pattern**
  - federat.*pattern(?!.*threshold|.*min.*count)
  - share.*pattern(?!.*aggregat)
### **Message**
Federating patterns without aggregation threshold. Individual users identifiable.
### **Fix Action**
Apply k-anonymity threshold before federation
### **Applies To**
  - **/federation/**/*.py

## Sensitive Field Not Encrypted

### **Id**
unencrypted-sensitive-field
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - content.*=.*memory\\.content(?!.*encrypt)
  - INSERT.*content(?!.*encrypted)
### **Message**
Sensitive content stored without encryption.
### **Fix Action**
Encrypt sensitive fields before storage
### **Applies To**
  - **/memory/**/*.py
  - **/db/**/*.py

## Session Without Expiry

### **Id**
session-no-expiry
### **Severity**
info
### **Type**
regex
### **Pattern**
  - session(?!.*expire|.*ttl|.*timeout)
  - create.*session(?!.*lifetime)
### **Message**
Session created without expiry. Stale sessions are security risk.
### **Fix Action**
Set session expiry and implement refresh logic
### **Applies To**
  - **/auth/**/*.py
  - **/session/**/*.py