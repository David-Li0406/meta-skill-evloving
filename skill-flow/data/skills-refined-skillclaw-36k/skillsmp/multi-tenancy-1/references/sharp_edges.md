# Multi Tenancy - Sharp Edges

## Missing Tenant Filter in Query

### **Id**
missing-tenant-filter
### **Severity**
critical
### **Summary**
Database query lacks tenant_id filter allowing cross-tenant data access
### **Symptoms**
  - Users see other tenants' data
  - Data counts don't match expectations
  - Security audit flags data leakage
### **Why**
  Every database query must filter by tenant_id. Without this, a query
  returns data from all tenants - a severe security vulnerability.
  One missing filter can expose all customer data.
  
### **Gotcha**
  "Why can tenant A see tenant B's orders?"
  "Let me check the query..."
  "SELECT * FROM orders WHERE status = 'pending'"
  "Where's the tenant filter?"
  "..."
  
  # Forgot to add WHERE tenant_id = :tenant_id
  
### **Solution**
  1. Use ORM middleware to auto-add tenant filter:
     - SQLAlchemy event listener
     - Django model managers
     - Prisma middleware
  
  2. PostgreSQL Row-Level Security:
     - Enable RLS on all tables
     - Create tenant isolation policy
     - Force RLS for table owner
  
  3. Code review checklist:
     - Every query has tenant_id
     - JOIN conditions include tenant_id
     - Subqueries filter by tenant
  

## Tenant Context Leaks Between Requests

### **Id**
tenant-context-leak
### **Severity**
critical
### **Summary**
Thread-local or global tenant context persists across requests
### **Symptoms**
  - Random data from wrong tenant
  - Intermittent cross-tenant issues
  - Only happens under load
### **Why**
  Using global or thread-local storage for tenant context is dangerous
  in async environments. If not properly cleared, one request's tenant
  context leaks to another request - especially in connection pools.
  
### **Gotcha**
  "Our tests pass but production shows random tenant data"
  "Only happens when traffic is high"
  "The same endpoint sometimes returns wrong data"
  
  # Async framework reused connection, tenant context wasn't cleared
  
### **Solution**
  1. Use contextvars (Python) or AsyncLocalStorage (Node):
     - Request-scoped, async-safe
     - Can't leak between requests
  
  2. Middleware must:
     - Set context at request start
     - Clear context at request end
     - Handle errors to ensure cleanup
  
  3. Never use:
     - Global variables for tenant
     - Thread-local in async code
     - Module-level state
  

## No Noisy Neighbor Protection

### **Id**
noisy-neighbor-unprotected
### **Severity**
high
### **Summary**
One tenant's heavy usage impacts all other tenants
### **Symptoms**
  - Latency spikes correlate with specific tenant activity
  - Small tenants complain about slow performance
  - Database CPU spikes from one tenant's queries
### **Why**
  In shared infrastructure, one tenant running expensive queries or
  making excessive API calls degrades performance for everyone.
  Without quotas and limits, the biggest tenant wins.
  
### **Gotcha**
  "Why is our API so slow today?"
  "Looking at metrics... one tenant made 10x their normal API calls"
  "They're running a big migration"
  "And everyone else is suffering?"
  
  # No per-tenant rate limiting or resource quotas
  
### **Solution**
  1. Per-tenant rate limiting:
     - API request limits (requests/second)
     - Burst allowance with token bucket
     - Different limits by plan tier
  
  2. Resource quotas:
     - CPU limits per tenant
     - Memory limits per tenant
     - Database connection limits
     - IOPS limits
  
  3. Fair scheduling:
     - Tenant-aware query queues
     - Priority based on plan
     - Throttle heavy users
  

## Schema Migration Hits All Tenants

### **Id**
migration-all-at-once
### **Severity**
high
### **Summary**
Applying migrations to all tenant schemas simultaneously
### **Symptoms**
  - Long downtime during migrations
  - Failed migration leaves tenants inconsistent
  - Can't rollback without affecting everyone
### **Why**
  With schema-per-tenant, you have N schemas to migrate. Running them
  all at once is slow, risky, and blocks rollout. One failure can
  leave your database in an inconsistent state across tenants.
  
### **Gotcha**
  "The migration is taking 4 hours..."
  "We have 500 tenant schemas"
  "And now schema 347 failed"
  "How do we rollback the other 346?"
  
  # Ran ALTER TABLE on all schemas in one transaction
  
### **Solution**
  1. Rolling migrations:
     - Migrate tenants in batches
     - Verify each batch before continuing
     - Pause on errors
  
  2. Online schema changes:
     - Use pt-online-schema-change
     - Or gh-ost for MySQL
     - Minimal locking
  
  3. Canary deployments:
     - Migrate 1% of tenants first
     - Verify application works
     - Then roll out to rest
  