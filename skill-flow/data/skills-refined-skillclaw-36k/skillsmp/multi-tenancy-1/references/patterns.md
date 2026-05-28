# Multi-Tenancy

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Tenant ID everywhere
    ##### **Reason**
Must be in every query, log, metric
  
---
    ##### **Rule**
Never trust tenant context
    ##### **Reason**
Validate at every layer
  
---
    ##### **Rule**
Design for noisy neighbor
    ##### **Reason**
One tenant shouldn't affect others
  
---
    ##### **Rule**
Metering from day one
    ##### **Reason**
Can't bill without usage data
  
---
    ##### **Rule**
Plan for tenant lifecycle
    ##### **Reason**
Onboarding, offboarding, data export
### **Isolation Models**
  #### **Pooled**
    ##### **Description**
Shared database with row-level security
    ##### **Cost**
Lowest
    ##### **Isolation**
Shared risk, complex RLS
    ##### **Use When**
Cost-sensitive, many small tenants
  #### **Schema Per Tenant**
    ##### **Description**
Separate schema per tenant
    ##### **Cost**
Moderate
    ##### **Isolation**
Good isolation, migration complexity
    ##### **Use When**
Moderate compliance needs
  #### **Database Per Tenant**
    ##### **Description**
Dedicated database per tenant
    ##### **Cost**
Higher
    ##### **Isolation**
Strong isolation, compliance friendly
    ##### **Use When**
Enterprise customers, strict compliance
  #### **Instance Per Tenant**
    ##### **Description**
Dedicated infrastructure per tenant
    ##### **Cost**
Highest
    ##### **Isolation**
Full isolation, simple model
    ##### **Use When**
Largest enterprise, regulated industries
### **Tenant Context Sources**
  
---
    ##### **Source**
Subdomain
    ##### **Example**
tenant.app.com
    ##### **Priority**

  
---
    ##### **Source**
Header
    ##### **Example**
X-Tenant-ID
    ##### **Priority**

  
---
    ##### **Source**
JWT claim
    ##### **Example**
token.tenant_id
    ##### **Priority**

  
---
    ##### **Source**
Path parameter
    ##### **Example**
/tenants/{id}/...
    ##### **Priority**

### **Metering Types**
  #### **Count**
Number of items (API requests)
  #### **Gauge**
Current value (storage used)
  #### **Sum**
Total accumulated (compute hours)
### **Lifecycle States**
  - provisioning
  - active
  - suspended
  - pending_deletion
  - deleted

## Anti-Patterns


---
  #### **Pattern**
Missing tenant_id
  #### **Problem**
Data leakage between tenants
  #### **Solution**
Enforce tenant_id on all queries

---
  #### **Pattern**
Trust client tenant
  #### **Problem**
Security vulnerability
  #### **Solution**
Validate tenant server-side

---
  #### **Pattern**
No rate limiting
  #### **Problem**
Noisy neighbor issues
  #### **Solution**
Implement per-tenant limits

---
  #### **Pattern**
Hardcoded isolation
  #### **Problem**
Can't upgrade tenants
  #### **Solution**
Design for flexible isolation

---
  #### **Pattern**
No metering
  #### **Problem**
Can't bill accurately
  #### **Solution**
Meter from day one

---
  #### **Pattern**
Manual provisioning
  #### **Problem**
Slow onboarding
  #### **Solution**
Automate tenant setup