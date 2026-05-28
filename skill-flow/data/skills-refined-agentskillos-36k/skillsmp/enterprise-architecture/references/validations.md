# Enterprise Architecture - Validations

## Architecture Decision Without Record

### **Id**
missing-adr
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - // TODO: document architecture decision
  - # DECISION: .*(?!ADR|adr)
### **Message**
Architecture decision may not be documented in ADR.
### **Fix Action**
Create Architecture Decision Record (ADR) for significant decisions
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.py

## Cross-Context Import

### **Id**
cross-boundary-import
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - from.*domains\.[a-z]+.*import.*(?!interface|event)
  - import.*@/domains/[a-z]+/(?!shared|contracts)
### **Message**
Importing implementation details across bounded context boundaries.
### **Fix Action**
Use events or public interfaces for cross-context communication
### **Applies To**
  - **/*.ts
  - **/*.py

## Shared Database Table Access

### **Id**
shared-database-access
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - FROM\s+(users|customers|orders)\s+.*JOIN.*WHERE
### **Message**
Query may access tables owned by another context.
### **Fix Action**
Access other context data via API or events, not direct DB
### **Applies To**
  - **/*.sql
  - **/*.ts
  - **/*.py

## Hardcoded Technology Choice

### **Id**
hardcoded-technology
### **Severity**
info
### **Type**
regex
### **Pattern**
  - PostgreSQL|MySQL|MongoDB
  - Redis|Kafka|RabbitMQ
### **Message**
Technology choice may need abstraction for portability.
### **Fix Action**
Consider abstraction layer for technology-specific code
### **Applies To**
  - **/*.ts
  - **/*.js

## API Without Contract Documentation

### **Id**
undocumented-api-contract
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.get\(|app\.post\((?!.*openapi|.*swagger|.*schema)
  - router\.get\(|router\.post\((?!.*docs)
### **Message**
API endpoint may lack contract documentation.
### **Fix Action**
Document API contract with OpenAPI/Swagger specification
### **Applies To**
  - **/*.ts
  - **/*.js

## Feature Without Capability Mapping

### **Id**
missing-capability-mapping
### **Severity**
info
### **Type**
regex
### **Pattern**
  - // Feature:.*(?!Capability:|CAP-)
  - # Feature.*(?!maps to|capability)
### **Message**
Feature may not be mapped to business capability.
### **Fix Action**
Map features to business capabilities for traceability
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.md