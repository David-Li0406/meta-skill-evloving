# GCP Patterns & Knowledge

## Table of Contents
- [Core Concepts](#core-concepts)
- [IAM & Security](#iam--security)
- [SDK Patterns (Go/Python)](#sdk-patterns)
- [Organisation Structure](#organisation-structure)
- [Common Services](#common-services)
- [Gotchas & Debugging](#gotchas--debugging)

## Core Concepts

### Resource Model
Hierarchical model with **fully-qualified resource names**:
```
//compute.googleapis.com/projects/my-project/zones/europe-west2-a/instances/my-vm
//storage.googleapis.com/projects/_/buckets/my-bucket
```

### Resource Hierarchy
```
Organisation
  └── Folder
        └── Project
              └── Resource
```

**Projects are the billing and API boundary** — most resources live in a project.

### Control Plane vs Data Plane
- **Control plane:** Resource management (create VM, configure bucket)
- **Data plane:** Content operations (read objects, query BigQuery)

Unlike Azure, no explicit "isDataAction" — you need to know based on the API.

### Regions & Zones
- **Region:** Geographic area (europe-west2 = London)
- **Zone:** Isolated location within region (europe-west2-a, -b, -c)
- **Multi-region:** For geo-redundant storage (eu, us, asia)
- Some services are **global** (Cloud DNS, IAM)

## IAM & Security

### Principal Types
| Principal | Format | Use Case |
|-----------|--------|----------|
| User | `user:email@example.com` | Human access |
| Service Account | `serviceAccount:sa@project.iam.gserviceaccount.com` | Apps, automation |
| Group | `group:group@example.com` | Bulk assignment |
| Domain | `domain:example.com` | All users in domain |
| allUsers | `allUsers` | Anonymous (public) |
| allAuthenticatedUsers | `allAuthenticatedUsers` | Any Google account |

### IAM Policy Model
**Additive only** — GCP IAM has no explicit deny (use Organisation Policies for restrictions).

```json
{
  "bindings": [{
    "role": "roles/viewer",
    "members": ["user:alice@example.com", "serviceAccount:sa@project.iam.gserviceaccount.com"]
  }]
}
```

### Common Roles
| Role | Access Level |
|------|--------------|
| roles/owner | Full access + IAM management |
| roles/editor | Full access, no IAM |
| roles/viewer | Read-only |
| roles/browser | List projects/folders only |

### Service Accounts
**Two types:**
- **User-managed:** You create and control
- **Service agents:** Auto-created by GCP services (format: `service-PROJECT_NUMBER@*.iam.gserviceaccount.com`)

**Key management:**
- Prefer **Workload Identity Federation** over keys
- Keys don't expire — easy to leak
- Use **short-lived tokens** when possible

### Workload Identity Federation
Federate external identities (AWS, Azure, OIDC) without GCP keys:
```bash
gcloud iam workload-identity-pools create "external-pool" \
  --location="global" \
  --display-name="External Identity Pool"
```

## SDK Patterns

### Go SDK (google-cloud-go)

**Authentication:**
```go
import (
    "context"
    compute "cloud.google.com/go/compute/apiv1"
    "google.golang.org/api/option"
)

// Default credentials (ADC)
client, err := compute.NewInstancesRESTClient(context.Background())

// Explicit credentials file
client, err := compute.NewInstancesRESTClient(context.Background(),
    option.WithCredentialsFile("/path/to/key.json"),
)

// Impersonation
client, err := compute.NewInstancesRESTClient(context.Background(),
    option.ImpersonateCredentials("target-sa@project.iam.gserviceaccount.com"),
)
```

**Pagination:**
```go
import computepb "cloud.google.com/go/compute/apiv1/computepb"

req := &computepb.AggregatedListInstancesRequest{Project: projectID}
it := client.AggregatedList(context.Background(), req)
for {
    pair, err := it.Next()
    if err == iterator.Done { break }
    if err != nil { return err }
    for _, instance := range pair.Value.Instances {
        // process instance
    }
}
```

### Python SDK (google-cloud-python)

**Authentication:**
```python
from google.cloud import compute_v1
from google.oauth2 import service_account

# Default credentials
client = compute_v1.InstancesClient()

# Explicit credentials
credentials = service_account.Credentials.from_service_account_file('/path/to/key.json')
client = compute_v1.InstancesClient(credentials=credentials)

# Impersonation
from google.auth import impersonated_credentials
target_credentials = impersonated_credentials.Credentials(
    source_credentials=credentials,
    target_principal='target-sa@project.iam.gserviceaccount.com',
    target_scopes=['https://www.googleapis.com/auth/cloud-platform']
)
```

**Pagination:**
```python
from google.cloud import compute_v1

client = compute_v1.InstancesClient()
for zone, response in client.aggregated_list(project=project_id):
    if response.instances:
        for instance in response.instances:
            # process instance
```

**Cloud Asset Inventory (bulk queries):**
```python
from google.cloud import asset_v1

client = asset_v1.AssetServiceClient()
response = client.search_all_resources(
    scope=f"organizations/{org_id}",
    asset_types=["compute.googleapis.com/Instance"],
)
for resource in response:
    # process resource
```

## Organisation Structure

### Organisation Policies (Not IAM)
Use for restrictions — since IAM has no deny:
```bash
gcloud resource-manager org-policies set-policy policy.yaml --organization=ORG_ID
```

Common constraints:
- `gcp.resourceLocations` — Restrict regions
- `iam.allowedPolicyMemberDomains` — Restrict sharing
- `compute.vmExternalIpAccess` — Deny external IPs

### Folder-Level IAM
```bash
gcloud resource-manager folders add-iam-policy-binding FOLDER_ID \
  --member="group:viewers@example.com" \
  --role="roles/viewer"
```

## Common Services

### Cloud Storage Quirks
- **Bucket names globally unique** (like S3)
- **Strong consistency** since 2021 (unlike S3's historical eventual consistency)
- **Uniform vs Fine-grained ACLs:** Uniform recommended (bucket-level only)
- **Object versioning:** Optional, not on by default
- **Lifecycle rules:** Delete old versions, transition storage class

### Compute Engine Quirks
- **Metadata server:** `http://metadata.google.internal/computeMetadata/v1/`
  - Requires header: `Metadata-Flavor: Google`
- **Instance identity token:** `/instance/service-accounts/default/identity?audience=AUDIENCE`
- **Preemptible/Spot VMs:** Cheaper, max 24h lifetime, can be terminated

### BigQuery Quirks
- **Serverless** — no infrastructure to manage
- **Slots:** Query processing capacity (on-demand vs reserved)
- **Streaming inserts:** Near real-time, but costs more than batch loads
- **Partitioning & clustering:** Critical for cost/performance

## Gotchas & Debugging

| Issue | Cause | Fix |
|-------|-------|-----|
| `PERMISSION_DENIED` with correct role | API not enabled | Enable API on project |
| IAM changes delayed | Eventual consistency | Wait 60+ seconds |
| Can't create resources | Billing not linked | Link billing account |
| Terraform destroy fails | Lien on project | Remove lien first |
| SA key auth fails | Key deleted/rotated | Regenerate or use WIF |
| Cross-project denied | Missing service agent role | Grant explicitly |

### Rate Limits (CRITICAL)

**Service-account-scoped limits:**
Unlike AWS (per-account) or Azure (per-subscription for ARM), GCP limits follow the **caller**.

| API | Limit | Scope |
|-----|-------|-------|
| Compute Engine | 20 req/sec | Per service account |
| Cloud Storage | 1 req/sec (list) | Per service account |
| Resource Manager | 5 req/sec | Per service account |
| Cloud Asset API | 100 req/100 sec | Per organisation |

**Mitigation:**
1. Use **Cloud Asset Inventory** for bulk discovery
2. Use **multiple service accounts** to parallelise
3. Cache aggressively

### Useful CLI Commands
```bash
# Who am I?
gcloud auth list
gcloud config get-value account

# Check IAM policy
gcloud projects get-iam-policy PROJECT_ID

# Test permissions
gcloud asset analyze-iam-policy \
  --organization=ORG_ID \
  --identity="serviceAccount:sa@project.iam.gserviceaccount.com" \
  --full-resource-name="//compute.googleapis.com/projects/PROJECT/zones/ZONE/instances/INSTANCE"

# Cloud Asset search
gcloud asset search-all-resources --scope=organizations/ORG_ID \
  --asset-types="compute.googleapis.com/Instance"
```
