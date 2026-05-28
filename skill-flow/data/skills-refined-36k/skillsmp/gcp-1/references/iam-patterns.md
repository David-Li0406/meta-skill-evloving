# GCP IAM Security Patterns

## Predefined Roles Reference

### Storage Roles (Use Instead of Primitive)

| Instead of | Use | Permissions |
|------------|-----|-------------|
| `roles/viewer` | `roles/storage.objectViewer` | Read objects only |
| `roles/editor` | `roles/storage.objectAdmin` | Full object control |
| `roles/owner` | `roles/storage.admin` | Full bucket + object control |

### Compute Roles

| Instead of | Use | Permissions |
|------------|-----|-------------|
| `roles/viewer` | `roles/compute.viewer` | Read compute resources |
| `roles/editor` | `roles/compute.instanceAdmin.v1` | Manage instances |
| `roles/owner` | `roles/compute.admin` | Full compute control |

### Cloud SQL Roles

| Role | Use Case |
|------|----------|
| `roles/cloudsql.client` | Connect to instances |
| `roles/cloudsql.viewer` | View instances |
| `roles/cloudsql.editor` | Manage instances |

### Cloud Functions Roles

| Role | Use Case |
|------|----------|
| `roles/cloudfunctions.invoker` | Invoke functions |
| `roles/cloudfunctions.viewer` | View functions |
| `roles/cloudfunctions.developer` | Deploy functions |

## Service Account Patterns

### Dedicated Service Account

```hcl
# Create dedicated SA
resource "google_service_account" "app" {
  account_id   = "my-app-sa"
  display_name = "My App Service Account"
  description  = "Service account for my-app workload"
}

# Grant specific roles
resource "google_project_iam_member" "app_storage" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.app.email}"
}

resource "google_project_iam_member" "app_sql" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.app.email}"
}
```

### Service Account Impersonation

```hcl
# Allow user to impersonate SA (instead of using SA key)
resource "google_service_account_iam_member" "impersonation" {
  service_account_id = google_service_account.app.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "user:developer@example.com"
}

# Allow SA to impersonate another SA
resource "google_service_account_iam_member" "sa_impersonation" {
  service_account_id = google_service_account.target.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${google_service_account.source.email}"
}
```

### Workload Identity (GKE)

```hcl
# GCP Service Account
resource "google_service_account" "gke_workload" {
  account_id   = "gke-workload-sa"
  display_name = "GKE Workload Service Account"
}

# Allow Kubernetes SA to use GCP SA
resource "google_service_account_iam_member" "workload_identity" {
  service_account_id = google_service_account.gke_workload.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.namespace}/${var.ksa_name}]"
}

# Kubernetes Service Account annotation
resource "kubernetes_service_account" "app" {
  metadata {
    name      = var.ksa_name
    namespace = var.namespace
    annotations = {
      "iam.gke.io/gcp-service-account" = google_service_account.gke_workload.email
    }
  }
}
```

## IAM Conditions

### Time-Based Access

```hcl
resource "google_project_iam_member" "temporary_access" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "user:contractor@example.com"

  condition {
    title       = "temporary_access"
    description = "Access expires end of month"
    expression  = "request.time < timestamp('2024-01-31T23:59:59Z')"
  }
}
```

### Resource-Based Conditions

```hcl
resource "google_project_iam_member" "bucket_specific" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.app.email}"

  condition {
    title       = "specific_bucket"
    description = "Only access specific bucket"
    expression  = "resource.name.startsWith('projects/_/buckets/my-bucket')"
  }
}
```

### Attribute-Based Access

```hcl
resource "google_project_iam_member" "tagged_resources" {
  project = var.project_id
  role    = "roles/compute.instanceAdmin.v1"
  member  = "group:developers@example.com"

  condition {
    title       = "dev_instances_only"
    description = "Only manage instances with env=dev label"
    expression  = "resource.matchTag('env', 'dev')"
  }
}
```

## Custom Roles

### Minimal Custom Role

```hcl
resource "google_project_iam_custom_role" "minimal_deployer" {
  role_id     = "minimalDeployer"
  title       = "Minimal Deployer"
  description = "Deploy Cloud Run services only"
  permissions = [
    "run.services.create",
    "run.services.update",
    "run.services.get",
    "run.services.list",
    "iam.serviceAccounts.actAs"
  ]
}
```

### Read-Only Custom Role

```hcl
resource "google_project_iam_custom_role" "security_viewer" {
  role_id     = "securityViewer"
  title       = "Security Viewer"
  description = "View security configurations without modification"
  permissions = [
    "compute.firewalls.list",
    "compute.firewalls.get",
    "iam.serviceAccounts.list",
    "iam.serviceAccounts.get",
    "storage.buckets.list",
    "storage.buckets.getIamPolicy",
    "cloudsql.instances.list"
  ]
}
```

## Organization Policies

### Restrict Public Access

```hcl
resource "google_organization_policy" "no_public_ip" {
  org_id     = var.org_id
  constraint = "compute.vmExternalIpAccess"

  list_policy {
    deny {
      all = true
    }
  }
}

resource "google_organization_policy" "uniform_bucket_access" {
  org_id     = var.org_id
  constraint = "storage.uniformBucketLevelAccess"

  boolean_policy {
    enforced = true
  }
}
```

### Restrict Service Account Key Creation

```hcl
resource "google_organization_policy" "no_sa_keys" {
  org_id     = var.org_id
  constraint = "iam.disableServiceAccountKeyCreation"

  boolean_policy {
    enforced = true
  }
}
```

### Restrict Allowed Services

```hcl
resource "google_organization_policy" "allowed_services" {
  org_id     = var.org_id
  constraint = "gcp.restrictServiceUsage"

  list_policy {
    allow {
      values = [
        "compute.googleapis.com",
        "storage.googleapis.com",
        "run.googleapis.com",
        "cloudsql.googleapis.com"
      ]
    }
  }
}
```

## Audit Queries

```bash
# Find allUsers bindings
gcloud asset search-all-iam-policies \
  --scope=projects/PROJECT_ID \
  --query="policy:allUsers"

# Find allAuthenticatedUsers bindings
gcloud asset search-all-iam-policies \
  --scope=projects/PROJECT_ID \
  --query="policy:allAuthenticatedUsers"

# Find primitive role usage
gcloud asset search-all-iam-policies \
  --scope=projects/PROJECT_ID \
  --query="policy:roles/editor OR policy:roles/owner"

# List service account keys
gcloud iam service-accounts keys list \
  --iam-account=SA_EMAIL \
  --managed-by=user

# Find unused service accounts
gcloud recommender recommendations list \
  --project=PROJECT_ID \
  --location=global \
  --recommender=google.iam.policy.Recommender
```

## IAM Recommender Integration

```bash
# Get IAM recommendations
gcloud recommender recommendations list \
  --project=PROJECT_ID \
  --location=global \
  --recommender=google.iam.policy.Recommender \
  --format="table(name,stateInfo.state,primaryImpact.category)"

# Apply recommendation
gcloud recommender recommendations mark-claimed \
  --project=PROJECT_ID \
  --location=global \
  --recommender=google.iam.policy.Recommender \
  --recommendation=RECOMMENDATION_ID
```
