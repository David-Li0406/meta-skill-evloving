# Export Control - Validations

## Export Without Country Check

### **Id**
no-country-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - export(?!.*country|.*destination|.*embargo)
  - shipTo(?!.*validateCountry|.*checkEmbargo)
### **Message**
Export may not validate destination country restrictions.
### **Fix Action**
Check country against embargo and license requirements
### **Applies To**
  - **/*.ts
  - **/*.js

## Missing Party Screening

### **Id**
no-party-screening
### **Severity**
error
### **Type**
regex
### **Pattern**
  - createOrder(?!.*screenParty|.*dplCheck|.*sdnCheck)
  - processExport(?!.*denied.*list)
### **Message**
Transaction may not screen against denied party lists.
### **Fix Action**
Screen all parties against DPL, Entity List, SDN
### **Applies To**
  - **/*.ts
  - **/*.js

## Hardcoded Embargo List

### **Id**
hardcoded-country-list
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - embargoedCountries\s*=\s*\[
  - restrictedCountries.*\[.*'CU'.*'IR'
### **Message**
Hardcoded embargo list may become outdated.
### **Fix Action**
Use external source for embargo list with regular updates
### **Applies To**
  - **/*.ts
  - **/*.js

## Encryption Without Classification

### **Id**
encryption-no-classification
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - AES|RSA|crypto(?!.*eccn|.*classification|.*ear)
### **Message**
Encryption functionality may require export classification.
### **Fix Action**
Classify encryption items under EAR Category 5
### **Applies To**
  - **/*.ts
  - **/*.js

## Foreign National Access Unchecked

### **Id**
foreign-access-unchecked
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - grantAccess(?!.*citizenship|.*usPersonCheck)
  - addTeamMember(?!.*nationality)
### **Message**
Access granted without checking foreign national status.
### **Fix Action**
Verify US person status before controlled data access
### **Applies To**
  - **/*.ts
  - **/*.js

## Missing End Use Verification

### **Id**
no-end-use-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - export(?!.*endUse|.*prohibited.*use)
  - shipment(?!.*intended.*use)
### **Message**
Export may not verify end use restrictions.
### **Fix Action**
Document and verify intended end use
### **Applies To**
  - **/*.ts
  - **/*.js

## Party Screening Not Logged

### **Id**
screening-not-logged
### **Severity**
info
### **Type**
regex
### **Pattern**
  - screenParty(?!.*log|.*audit|.*record)
  - dplCheck(?!.*document)
### **Message**
Party screening results may not be logged for audit.
### **Fix Action**
Log all screening results with timestamp
### **Applies To**
  - **/*.ts
  - **/*.js

## Cloud Region Not Restricted

### **Id**
cloud-region-uncontrolled
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - s3.*Bucket(?!.*region.*us-)
  - createStorage(?!.*location.*domestic)
### **Message**
Cloud storage may allow foreign region replication.
### **Fix Action**
Restrict to US regions for controlled data
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.yaml