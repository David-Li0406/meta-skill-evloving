---
name: gcp
description: "GCP infrastructure security review process. Use when reviewing IAM policies and service accounts, auditing Cloud Storage buckets, securing Cloud Functions and Cloud Run, reviewing Terraform for GCP, or configuring VPC and firewall rules. Also use when primitive roles (owner/editor/viewer) are used, `allUsers` appears in bindings, default service accounts are used, or Cloud SQL has public IP. Essential for Workload Identity, VPC Service Controls, organization policies, and GCP security scanning."
---

# GCP Skill

## Overview

GCP's resource hierarchy provides powerful security controls, but defaults are often permissive. This skill guides systematic review of GCP infrastructure for security misconfigurations.

**Core principle:** Never use primitive roles. GCP's predefined and custom roles exist for a reason. `roles/owner`, `roles/editor`, and `roles/viewer` are almost never appropriate.

## The GCP Security Review Process

### Phase 1: Check IAM First

**IAM is the foundation. Start here:**

1. **Review Role Assignments**
   - Using predefined roles (not primitive)?
   - Scoped to specific resources (not project)?
   - Conditions applied where possible?

2. **Check Service Accounts**
   - Dedicated accounts per workload?
   - Not using default service accounts?
   - Keys managed properly (or none)?

3. **Verify No Public Access**
   - No `allUsers` bindings?
   - No `allAuthenticatedUsers` bindings?
   - Workload Identity for GKE?

### Phase 2: Check Network Boundaries

**Then verify network isolation:**

1. **Firewall Rules**
   - No 0.0.0.0/0 ingress (except load balancers)?
   - Deny rules to restrict default allow?
   - Tags used to target specific instances?

2. **VPC Design**
   - Private Google Access enabled?
   - Cloud NAT for outbound?
   - VPC Flow Logs enabled?

3. **Service Access**
   - Private Service Connect?
   - VPC Service Controls?
   - No public IPs on compute?

### Phase 3: Check Data Protection

**Finally, verify data security:**

1. **Encryption**
   - CMEK for sensitive data?
   - Data encrypted in transit?
   - Secret Manager for credentials?

2. **Storage Security**
   - Uniform bucket-level access?
   - No public buckets?
   - Versioning for critical data?

## Red Flags - STOP and Investigate

### IAM Red Flags

```hcl
# ❌ CRITICAL: Primitive role
resource "google_project_iam_member" "bad" {
  role   = "roles/editor"  # Too broad!
  member = "serviceAccount:..."
}

# ❌ CRITICAL: Public access
resource "google_storage_bucket_iam_member" "bad" {
  role   = "roles/storage.objectViewer"
  member = "allUsers"  # Anyone on internet!
}

# ❌ HIGH: All authenticated users
member = "allAuthenticatedUsers"  # Any Google account!

# ❌ HIGH: Default service account
resource "google_compute_instance" "bad" {
  service_account {
    email = "PROJECT_NUMBER-compute@developer.gserviceaccount.com"
  }
}
```

### Network Red Flags

```hcl
# ❌ CRITICAL: SSH from anywhere
resource "google_compute_firewall" "bad" {
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = ["0.0.0.0/0"]  # From anywhere!
}

# ❌ HIGH: All protocols
allow {
  protocol = "all"  # Everything open!
}

# ❌ HIGH: Cloud SQL public IP
resource "google_sql_database_instance" "bad" {
  settings {
    ip_configuration {
      ipv4_enabled = true  # Public IP!
    }
  }
}
```

### Cloud Functions Red Flags

```hcl
# ❌ HIGH: Public invocation
resource "google_cloudfunctions2_function_iam_member" "bad" {
  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"  # Anyone can invoke!
}

# ❌ HIGH: Default service account
# (Not specifying service_account_email)

# ❌ MEDIUM: No VPC connector
# (Missing vpc_connector for internal resources)
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "Editor role is easiest" | Predefined roles exist. Take 5 minutes to find the right one. |
| "allAuthenticatedUsers is secure" | It means ANY Google account. That's not secure. |
| "Default SA is fine" | Default SA has Editor. Create dedicated accounts. |
| "We need public Cloud SQL" | Use Cloud SQL Auth Proxy. Never public. |
| "0.0.0.0/0 is temporary" | Temporary becomes permanent. Use IAP from day one. |
| "Function must be public" | Use API Gateway or load balancer with auth. |

## GCP Security Checklist

Before approving GCP infrastructure:

**IAM:**
- [ ] No primitive roles (owner/editor/viewer)
- [ ] Dedicated service accounts per workload
- [ ] No `allUsers` or `allAuthenticatedUsers`
- [ ] Workload Identity for GKE
- [ ] Conditions on sensitive bindings

**Network:**
- [ ] No 0.0.0.0/0 firewall rules
- [ ] IAP for administrative access
- [ ] VPC Flow Logs enabled
- [ ] Private Google Access enabled

**Storage:**
- [ ] Uniform bucket-level access
- [ ] No public buckets
- [ ] CMEK for sensitive data
- [ ] Versioning enabled

**Compute:**
- [ ] Dedicated service accounts
- [ ] No public IPs (use Cloud NAT)
- [ ] VPC connectors for serverless

## Quick Patterns

### Secure Service Account

```hcl
resource "google_service_account" "app" {
  account_id   = "my-app-sa"
  display_name = "My App Service Account"
  description  = "Dedicated SA for my-app with minimal permissions"
}

# Specific predefined role
resource "google_project_iam_member" "app_storage" {
  project = var.project_id
  role    = "roles/storage.objectViewer"  # Predefined, minimal
  member  = "serviceAccount:${google_service_account.app.email}"

  condition {
    title       = "Only from VPC"
    description = "Restrict to internal access"
    expression  = "request.auth.access_levels.hasOnly(['accessPolicies/123/accessLevels/vpc_only'])"
  }
}
```

### Secure Cloud Storage

```hcl
resource "google_storage_bucket" "secure" {
  name     = "my-secure-bucket"
  location = "US"

  uniform_bucket_level_access = true

  encryption {
    default_kms_key_name = google_kms_crypto_key.bucket_key.id
  }

  versioning {
    enabled = true
  }

  logging {
    log_bucket = google_storage_bucket.logs.name
  }
}

# No public access - only specific SA
resource "google_storage_bucket_iam_member" "app_access" {
  bucket = google_storage_bucket.secure.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.app.email}"
}
```

### Secure Firewall

```hcl
# Allow only from IAP for SSH
resource "google_compute_firewall" "allow_iap_ssh" {
  name    = "allow-iap-ssh"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["35.235.240.0/20"]  # IAP range only
  target_tags   = ["allow-iap-ssh"]
}
```

## Quick Security Scans

```bash
# GCP native tools
gcloud asset search-all-iam-policies --query="policy:allUsers"
gcloud compute firewall-rules list --filter="sourceRanges:0.0.0.0/0"
gcloud sql instances list --filter="settings.ipConfiguration.ipv4Enabled=true"

# Third-party scanners
checkov -f main.tf              # Terraform scanning
forseti                         # GCP security scanning
gcloud scc findings list        # Security Command Center
```

## References

Detailed patterns and examples in `references/`:
- `iam-patterns.md` - Advanced IAM and Workload Identity
- `network-security.md` - VPC and firewall patterns
- `organization-policies.md` - Org-level constraints
