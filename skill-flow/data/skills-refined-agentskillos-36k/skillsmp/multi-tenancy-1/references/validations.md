# Multi Tenancy - Validations

## Query Without Tenant Filter

### **Id**
missing-tenant-filter
### **Severity**
error
### **Type**
regex
### **Pattern**
  - SELECT.*FROM(?!.*tenant_id)
  - UPDATE.*SET(?!.*WHERE.*tenant_id)
  - DELETE FROM(?!.*tenant_id)
### **Message**
Database query may lack tenant_id filter - potential data leakage.
### **Fix Action**
Add WHERE tenant_id = :tenant_id to all queries
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.sql

## Global Tenant Context

### **Id**
global-tenant-context
### **Severity**
error
### **Type**
regex
### **Pattern**
  - global\s+tenant
  - threading\.local\(\).*tenant
  - let\s+currentTenant\s*=
### **Message**
Global or thread-local tenant context is unsafe in async environments.
### **Fix Action**
Use contextvars (Python) or AsyncLocalStorage (Node.js)
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Hardcoded Tenant ID

### **Id**
hardcoded-tenant-id
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tenant_id\s*=\s*['"][a-z0-9-]+['"]
  - tenantId:\s*['"][a-z0-9-]+['"]
### **Message**
Hardcoded tenant ID found - should come from request context.
### **Fix Action**
Get tenant ID from authenticated request context
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Missing Rate Limiting

### **Id**
no-rate-limiting
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.route\((?!.*rate_limit)
  - @router\.(?!.*RateLimiter)
  - express\.Router\(\)(?!.*rateLimit)
### **Message**
API route may lack rate limiting - noisy neighbor risk.
### **Fix Action**
Add per-tenant rate limiting middleware
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## JOIN Without Tenant ID

### **Id**
tenant-join-missing
### **Severity**
error
### **Type**
regex
### **Pattern**
  - JOIN.*ON(?!.*tenant_id)
  - INNER JOIN.*=(?!.*tenant_id)
  - LEFT JOIN.*ON(?!.*tenant_id)
### **Message**
JOIN clause may lack tenant_id - cross-tenant data risk.
### **Fix Action**
Include tenant_id in all JOIN conditions
### **Applies To**
  - **/*.py
  - **/*.sql

## Missing Usage Metering

### **Id**
missing-metering
### **Severity**
info
### **Type**
regex
### **Pattern**
  - api_call\((?!.*meter)
  - process_request\((?!.*track_usage)
### **Message**
API operation may not be metered - billing accuracy risk.
### **Fix Action**
Add usage metering for billing-relevant operations
### **Applies To**
  - **/*.py
  - **/*.ts

## Tenant Context Not Cleared

### **Id**
tenant-context-not-cleared
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - set_tenant\((?!.*finally.*clear)
  - setTenantContext\((?!.*finally)
### **Message**
Tenant context may not be cleared after request.
### **Fix Action**
Use try/finally or middleware to ensure context cleanup
### **Applies To**
  - **/*.py
  - **/*.ts