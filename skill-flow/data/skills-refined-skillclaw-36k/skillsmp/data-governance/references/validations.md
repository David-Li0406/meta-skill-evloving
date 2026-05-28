# Data Governance - Validations

## PII in Logging Statements

### **Id**
pii-in-logs
### **Severity**
error
### **Type**
regex
### **Pattern**
  - log.*email.*=
  - print.*ssn|phone|address
  - logger.*customer_name
### **Message**
Personal data may be written to logs without masking.
### **Fix Action**
Mask or remove PII before logging
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Missing Data Classification

### **Id**
no-data-classification
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CREATE TABLE(?!.*-- classification:)
  - class.*Model(?!.*classification)
### **Message**
Data model may lack classification metadata.
### **Fix Action**
Add data classification comment or attribute
### **Applies To**
  - **/*.sql
  - **/*.py

## Hardcoded PII in Query

### **Id**
hardcoded-pii-query
### **Severity**
error
### **Type**
regex
### **Pattern**
  - WHERE email = '[^']+
  - AND phone = '[0-9]+
  - customer_name = 'John
### **Message**
Hardcoded PII in query - use parameters.
### **Fix Action**
Use parameterized queries, not hardcoded PII
### **Applies To**
  - **/*.sql
  - **/*.py
  - **/*.ts

## Missing Data Quality Check

### **Id**
missing-quality-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - INSERT INTO(?!.*check|.*validate|.*assert)
  - COPY.*FROM(?!.*quality)
### **Message**
Data ingestion may lack quality validation.
### **Fix Action**
Add data quality checks before ingestion
### **Applies To**
  - **/*.sql
  - **/*.py

## Missing Retention Policy

### **Id**
no-retention-policy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - CREATE TABLE(?!.*retention|.*ttl|.*expire)
### **Message**
Table may lack retention policy definition.
### **Fix Action**
Define data retention policy for table
### **Applies To**
  - **/*.sql

## Sensitive Data in Response

### **Id**
sensitive-data-exposure
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - return.*password|secret|token
  - response.*ssn|credit_card
### **Message**
Sensitive data may be exposed in API response.
### **Fix Action**
Remove or mask sensitive fields from responses
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## ETL Without Lineage

### **Id**
missing-lineage-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - transform.*(?!lineage|track|audit)
  - pipeline.*(?!openlineage|marquez)
### **Message**
Data transformation may not track lineage.
### **Fix Action**
Integrate lineage tracking (OpenLineage/Marquez)
### **Applies To**
  - **/*.py
  - **/*.yaml