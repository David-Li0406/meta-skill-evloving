# Compliance Automation - Validations

## Mutable Evidence Storage

### **Id**
mutable-evidence-storage
### **Severity**
error
### **Type**
regex
### **Pattern**
  - evidence.*bucket(?!.*object_lock)
  - store_evidence\((?!.*immutable)
  - s3.*put_object(?!.*ObjectLockMode)
### **Message**
Evidence may be stored in mutable storage - integrity risk.
### **Fix Action**
Use S3 Object Lock or immutable blob storage
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.yaml

## Missing Evidence Hash

### **Id**
no-evidence-hash
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - collect_evidence\((?!.*hash)
  - store_evidence\((?!.*sha256)
  - Evidence\((?!.*content_hash)
### **Message**
Evidence may lack integrity hash for verification.
### **Fix Action**
Add SHA-256 hash to all evidence artifacts
### **Applies To**
  - **/*.py
  - **/*.ts

## Policy Without Version Control

### **Id**
policy-no-version
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - policy.*=.*"""(?!.*version)
  - POLICY.*=(?!.*v[0-9])
### **Message**
Policy may not be version controlled.
### **Fix Action**
Store policies in version control with versioning
### **Applies To**
  - **/*.py
  - **/*.rego

## Missing Compliance Alerting

### **Id**
no-compliance-alerting
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - compliance.*check(?!.*alert)
  - control.*fail(?!.*notify)
### **Message**
Compliance failure may not trigger alerts.
### **Fix Action**
Add alerting for compliance violations
### **Applies To**
  - **/*.py
  - **/*.yaml

## Manual Evidence Collection

### **Id**
manual-evidence-collection
### **Severity**
info
### **Type**
regex
### **Pattern**
  - evidence.*manual
  - collect.*screenshot.*manually
  - export.*for.*audit
### **Message**
Evidence collection may be manual - consider automation.
### **Fix Action**
Automate evidence collection on schedule
### **Applies To**
  - **/*.py
  - **/*.md

## Missing Evidence Retention

### **Id**
no-retention-policy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - evidence(?!.*retention)
  - store_artifact(?!.*expire)
### **Message**
Evidence may lack retention policy.
### **Fix Action**
Define evidence retention (typically 7 years)
### **Applies To**
  - **/*.py
  - **/*.yaml

## Hardcoded Compliance Exception

### **Id**
hardcoded-compliance-exception
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - skip.*compliance.*=.*True
  - ignore.*control.*=.*True
  - exception.*permanent
### **Message**
Hardcoded compliance exception found.
### **Fix Action**
Use time-bound exceptions with approval workflow
### **Applies To**
  - **/*.py
  - **/*.yaml