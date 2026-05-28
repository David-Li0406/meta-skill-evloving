# OCI Patterns & Knowledge

## Table of Contents
- [Core Concepts](#core-concepts)
- [IAM & Security](#iam--security)
- [SDK Patterns](#sdk-patterns)
- [Gotchas & Debugging](#gotchas--debugging)

## Core Concepts

### Resource Model
Resources identified by **OCIDs** (Oracle Cloud Identifiers):
```
ocid1.<resource_type>.<realm>.<region>.<unique_id>
ocid1.instance.oc1.uk-london-1.abcdefgh...
```

### Compartment Hierarchy
```
Tenancy (Root Compartment)
  └── Compartment
        └── Sub-Compartment (up to 6 levels)
              └── Resource
```

**Compartments are the IAM boundary** — policies reference compartments.

### Regions
- **uk-london-1:** London
- **eu-frankfurt-1:** Frankfurt
- **Realm:** Commercial (oc1), Government, etc.

## IAM & Security

### Policy Syntax
Human-readable format:
```
Allow <subject> to <verb> <resource-type> in <location> [where <conditions>]
```

**Verbs (increasing privilege):**
- `inspect` — List only
- `read` — Inspect + get
- `use` — Read + use existing
- `manage` — Full control

**Example:**
```
Allow group ComputeAdmins to manage instance-family in compartment Production
Allow group Viewers to read all-resources in tenancy
Allow any-user to read buckets in compartment Public where request.principal.type='instance'
```

### Principal Types
| Principal | Syntax | Use Case |
|-----------|--------|----------|
| User | `user 'username'` | Human access |
| Group | `group 'groupname'` | Collection of users |
| Dynamic Group | `dynamic-group 'name'` | Auto-membership by matching rule |
| Any-user | `any-user` | All authenticated users |
| Service | `service 'servicename'` | OCI service |

### Dynamic Groups (Instance Principals)
Let compute instances call OCI APIs without credentials:
```
# Matching rule
ANY {instance.compartment.id = 'ocid1.compartment.oc1..xxx'}

# Policy
Allow dynamic-group AppInstances to read secret-family in compartment Secrets
```

## SDK Patterns

### Go SDK
```go
import (
    "github.com/oracle/oci-go-sdk/v65/common"
    "github.com/oracle/oci-go-sdk/v65/core"
)

// Config file auth (~/.oci/config)
provider := common.DefaultConfigProvider()

// Instance principal (from OCI compute)
provider, _ := auth.InstancePrincipalConfigurationProvider()

client, _ := core.NewComputeClientWithConfigurationProvider(provider)
```

### Python SDK
```python
import oci

# Config file auth
config = oci.config.from_file()
client = oci.core.ComputeClient(config)

# Instance principal
signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
client = oci.core.ComputeClient({}, signer=signer)

# Pagination
for instance in oci.pagination.list_call_get_all_results(
    client.list_instances, compartment_id
).data:
    # process instance
```

## Gotchas & Debugging

| Issue | Cause | Fix |
|-------|-------|-----|
| `NotAuthorizedOrNotFound` | Policy or compartment wrong | Check policy scope |
| Terraform can't find resource | Wrong compartment | Specify `compartment_id` |
| Policy not working | Eventual consistency | Wait 1-2 minutes |
| Can't delete compartment | Contains resources | Delete resources first |
| API key auth fails | Clock skew | Sync NTP |

### Rate Limits
- Per-tenancy limits with service-specific quotas
- Check `opc-request-id` header for debugging

### Useful CLI Commands
```bash
# Who am I?
oci iam user get --user-id $(oci iam user list --query 'data[0].id' --raw-output)

# List compartments
oci iam compartment list --compartment-id-in-subtree true

# Query resources
oci search resource structured-search --query-text "query all resources"
```
