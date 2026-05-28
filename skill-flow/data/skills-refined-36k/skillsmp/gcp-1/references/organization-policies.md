# GCP Organization Policies

Enforce security guardrails at the organization level.

## Essential Organization Policies

### Prevent Public Access

```hcl
# Block public Cloud Storage
resource "google_organization_policy" "storage_public_access" {
  org_id     = var.org_id
  constraint = "constraints/storage.publicAccessPrevention"

  boolean_policy {
    enforced = true
  }
}

# Block public Cloud Functions
resource "google_organization_policy" "cloudfunctions_allowed_ingress" {
  org_id     = var.org_id
  constraint = "constraints/cloudfunctions.allowedIngressSettings"

  list_policy {
    allow {
      values = ["ALLOW_INTERNAL_ONLY", "ALLOW_INTERNAL_AND_GCLB"]
    }
  }
}
```

### Restrict Resource Locations

```hcl
# Limit regions (data residency)
resource "google_organization_policy" "resource_locations" {
  org_id     = var.org_id
  constraint = "constraints/gcp.resourceLocations"

  list_policy {
    allow {
      values = ["in:us-locations", "in:eu-locations"]
    }
  }
}
```

### Enforce Service Account Controls

```hcl
# Disable service account key creation
resource "google_organization_policy" "disable_sa_key_creation" {
  org_id     = var.org_id
  constraint = "constraints/iam.disableServiceAccountKeyCreation"

  boolean_policy {
    enforced = true
  }
}

# Disable service account key upload
resource "google_organization_policy" "disable_sa_key_upload" {
  org_id     = var.org_id
  constraint = "constraints/iam.disableServiceAccountKeyUpload"

  boolean_policy {
    enforced = true
  }
}
```

### Network Security

```hcl
# Restrict VPC peering
resource "google_organization_policy" "restrict_vpc_peering" {
  org_id     = var.org_id
  constraint = "constraints/compute.restrictVpcPeering"

  list_policy {
    allow {
      values = ["under:organizations/${var.org_id}"]
    }
  }
}

# Require OS Login
resource "google_organization_policy" "require_os_login" {
  org_id     = var.org_id
  constraint = "constraints/compute.requireOsLogin"

  boolean_policy {
    enforced = true
  }
}
```

## Folder-Level Overrides

```hcl
# Allow public access in specific folder (e.g., marketing)
resource "google_folder_organization_policy" "allow_public_marketing" {
  folder     = "folders/${var.marketing_folder_id}"
  constraint = "constraints/storage.publicAccessPrevention"

  boolean_policy {
    enforced = false  # Override org policy
  }
}
```

## Common Constraints

| Constraint | Purpose |
|------------|---------|
| `storage.publicAccessPrevention` | Block public buckets |
| `cloudfunctions.allowedIngressSettings` | Restrict function access |
| `sql.restrictPublicIp` | Block public Cloud SQL |
| `compute.requireOsLogin` | Require OS Login for SSH |
| `iam.disableServiceAccountKeyCreation` | Block SA keys |
| `gcp.resourceLocations` | Data residency |
| `compute.restrictVpcPeering` | Limit VPC peering |
| `compute.vmExternalIpAccess` | Control external IPs |

## Checking Policy Compliance

```bash
# List effective policies
gcloud resource-manager org-policies list \
  --organization=ORG_ID

# Get specific policy
gcloud resource-manager org-policies describe \
  constraints/storage.publicAccessPrevention \
  --organization=ORG_ID

# Test policy evaluation
gcloud asset analyze-org-policy-governed-resources \
  --constraint=constraints/storage.publicAccessPrevention \
  --scope=organizations/ORG_ID
```

## Best Practices

1. **Start restrictive** - Enable all security constraints at org level
2. **Use folders** - Group projects by trust level, override where needed
3. **Audit regularly** - Check for policy drift
4. **Document exceptions** - Explain why overrides exist
5. **Test changes** - Apply to test folder first
