# Azure Patterns & Knowledge

## Table of Contents
- [Core Concepts](#core-concepts)
- [Identity & RBAC](#identity--rbac)
- [SDK Patterns (Go/Python)](#sdk-patterns)
- [Management Groups & Subscriptions](#management-groups--subscriptions)
- [Common Services](#common-services)
- [Gotchas & Debugging](#gotchas--debugging)

## Core Concepts

### Resource Model
Everything is a **resource** with a **Resource ID**:
```
/subscriptions/{sub-id}/resourceGroups/{rg}/providers/{namespace}/{type}/{name}
/subscriptions/abc-123/resourceGroups/my-rg/providers/Microsoft.Compute/virtualMachines/my-vm
```

### Control Plane vs Data Plane
**The `isDataAction` field is the definitive indicator** — not naming patterns.

- **Control plane:** ARM operations (create VM, configure storage account)
- **Data plane:** Content operations (read blob, query database)

```bash
# Check if an action is data plane
az provider operation show --namespace Microsoft.Storage \
  --resource-type blobServices/containers/blobs \
  --query "[].{Name:name, IsDataAction:isDataAction}"
```

### Regions & Availability Zones
- **Region:** Geographic area (uksouth, ukwest)
- **AZ:** Isolated zone within region (zones 1, 2, 3)
- **Paired regions:** For geo-redundancy (uksouth ↔ ukwest)
- Some services are **global** (Entra ID, Azure DNS)

## Identity & RBAC

### Principal Types
| Principal | Object | Use Case |
|-----------|--------|----------|
| User | Entra ID user | Human access |
| Service Principal | App registration | Automation, apps |
| Managed Identity | System/User assigned | Azure resources calling Azure |
| Group | Entra ID group | Bulk assignment |

### RBAC Scope Hierarchy
```
Management Group
  └── Subscription
        └── Resource Group
              └── Resource
```

Assignments **inherit down**. Use `--include-inherited` when querying.

### Built-in Roles (Common)
| Role | Access Level |
|------|--------------|
| Owner | Full access + can assign roles |
| Contributor | Full access, can't assign roles |
| Reader | View only |
| User Access Administrator | Manage role assignments only |

### Custom Role Pattern
```json
{
  "Name": "Custom Scanner",
  "Description": "Minimal permissions for resource scanning",
  "Actions": ["*/read", "Microsoft.Support/*"],
  "NotActions": [],
  "DataActions": ["Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read"],
  "NotDataActions": [],
  "AssignableScopes": ["/subscriptions/{sub-id}"]
}
```

### Deny Assignments
**Can override RBAC grants**. Check when debugging unexpected denials:
```bash
az rest --method GET \
  --uri "/subscriptions/{sub}/providers/Microsoft.Authorization/denyAssignments?api-version=2022-04-01"
```

## SDK Patterns

### Go SDK (azure-sdk-for-go)

**Authentication (DefaultAzureCredential):**
```go
import (
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/compute/armcompute"
)

cred, err := azidentity.NewDefaultAzureCredential(nil)
if err != nil { return err }

client, err := armcompute.NewVirtualMachinesClient(subscriptionID, cred, nil)
```

**Client secret auth:**
```go
cred, err := azidentity.NewClientSecretCredential(tenantID, clientID, clientSecret, nil)
```

**Pagination:**
```go
pager := client.NewListAllPager(nil)
for pager.More() {
    page, err := pager.NextPage(context.TODO())
    if err != nil { return err }
    for _, vm := range page.Value {
        // process vm
    }
}
```

### Python SDK (azure-sdk-for-python)

**Authentication:**
```python
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient

# Default (tries multiple methods)
credential = DefaultAzureCredential()

# Explicit service principal
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

client = ComputeManagementClient(credential, subscription_id)
```

**Pagination:**
```python
for vm in client.virtual_machines.list_all():
    # process vm
```

**Resource Graph (efficient bulk queries):**
```python
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

client = ResourceGraphClient(credential)
query = QueryRequest(
    query="Resources | where type =~ 'Microsoft.Compute/virtualMachines'",
    subscriptions=[subscription_id]
)
result = client.resources(query)
```

## Management Groups & Subscriptions

### Hierarchy
```
Tenant Root Group
  └── Management Group
        └── Subscription
              └── Resource Group
```

### Enterprise App Pattern (Multi-Tenant)
When your platform hosts Enterprise Apps for customers:
1. Customer consents to your app in their tenant
2. You get a service principal in their tenant
3. Customer assigns roles at their Management Group root
4. Your app assumes that identity to scan their resources

**Key constraint:** Graph API limits are **global per-app**, not per-tenant.

### Resource Providers
Must be registered on subscription before using:
```bash
# Check status
az provider show -n Microsoft.Compute --query "registrationState"

# Register
az provider register -n Microsoft.Compute
```

## Common Services

### Storage Account Quirks
- **Storage account names globally unique**, 3-24 chars, lowercase/numbers only
- **Hierarchical namespace** (ADLS Gen2) changes behaviour significantly
- **Access tiers:** Hot, Cool, Archive (retrieval latency differs)
- **Shared access signatures (SAS):** Time-limited URLs, can't revoke individually

### Virtual Machine Quirks
- **Instance metadata:** `http://169.254.169.254/metadata/instance?api-version=2021-02-01` (requires `Metadata: true` header)
- **Managed identity token:** `http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/`
- **Spot VMs:** Can be evicted with 30-second notice

### Entra ID (Azure AD) Quirks
- **Application vs Service Principal:** App registration creates both; SP is the tenant-local instance
- **Delegated vs Application permissions:** Delegated = user context, Application = app's own identity
- **Consent:** Admin consent required for many permissions in enterprise tenants

## Gotchas & Debugging

| Issue | Cause | Fix |
|-------|-------|-----|
| Role assignment succeeds, no access | Propagation delay | Wait up to 10 minutes |
| `AuthorizationFailed` with correct role | Scope mismatch | Verify exact resource ID |
| Can't assign roles despite Owner | Missing write permission | Check for deny assignments |
| Custom role not visible | Wrong assignable scope | Include target scope |
| Reader can't see resources | Provider not registered | Register provider |
| Inherited role not showing | Query omitted inherited | Use `--include-inherited` |

### Rate Limits

**ARM API (per subscription):**
- Read: 12,000 requests/hour
- Write: 1,200 requests/hour

**Graph API (CRITICAL for multi-tenant):**
- **Global per-application:** ~10,000 requests/10 minutes
- Shared across ALL tenants your app accesses
- This is typically your primary bottleneck

**Throttling headers:**
```
Retry-After: 30
x-ms-ratelimit-remaining-subscription-reads: 11999
```

### Useful CLI Commands
```bash
# Who am I?
az account show
az ad signed-in-user show  # For user context

# Check role assignments
az role assignment list --assignee <principal-id> --all --include-inherited

# Resource Graph query
az graph query -q "Resources | where type =~ 'Microsoft.Compute/virtualMachines' | project name, resourceGroup"
```
