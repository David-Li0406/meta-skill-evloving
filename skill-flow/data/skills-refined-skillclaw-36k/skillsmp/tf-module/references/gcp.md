# GCP-Specific Patterns

**When to use this reference:** When creating modules for GCP-based Duplocloud infrastructure.

## Backend Configuration

GCP uses GCS (Google Cloud Storage) backend:

```hcl
terraform {
  backend "gcs" {
    prefix = "mymodule"  # State prefix in bucket
    # bucket configured via tf init
  }
}
```

### State File Organization

The GCS state path follows this pattern:
```
gs://duplo-tfstate-<project-id>/
├── portal/<portal-name>/default.tfstate
├── infrastructure/<infra-name>/default.tfstate
├── shared/<shared-name>/default.tfstate
├── tenant/<tenant-name>/default.tfstate
└── <app>/<tenant-name>/default.tfstate
```

### Prefix Convention

| Module Type | prefix |
|-------------|--------|
| portal | `portal` |
| infrastructure | `infrastructure` |
| shared | `shared` |
| tenant | `tenant` |
| app | `<app-name>` |

## GCP Provider Configuration

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  workspaces = {
    tenant = {}
  }
}

provider "google" {
  project = module.ctx.account_id  # GCP project ID
  region  = module.ctx.region
}
```

### With Explicit Credentials

For local development or specific service accounts:

```hcl
provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_file)
}
```

## Common GCP Resources

### Cloud SQL (PostgreSQL)

```hcl
resource "duplocloud_gcp_sql_database_instance" "main" {
  tenant_id        = local.tenant.id
  name             = "main"
  database_version = "POSTGRES_15"
  tier             = "db-f1-micro"
  
  settings {
    disk_autoresize = true
    disk_size       = 20
    disk_type       = "PD_SSD"
    
    backup_configuration {
      enabled            = true
      start_time         = "03:00"
      point_in_time_recovery_enabled = true
    }
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = local.infra.vpc_id
    }
  }
}
```

### Cloud Memorystore (Redis)

```hcl
resource "duplocloud_gcp_redis_instance" "cache" {
  tenant_id      = local.tenant.id
  name           = "cache"
  display_name   = "Application Cache"
  tier           = "BASIC"
  memory_size_gb = 1
  redis_version  = "REDIS_7_0"
}
```

### GKE Configuration

GKE clusters are managed at the infrastructure level:

```hcl
resource "duplocloud_infrastructure" "this" {
  infra_name        = terraform.workspace
  cloud             = 2  # GCP
  region            = var.region
  enable_k8_cluster = true
  
  # GKE-specific settings
  gke_cluster {
    autopilot            = false
    enable_node_autoip   = true
    release_channel      = "REGULAR"
  }
}
```

### Secret Manager

```hcl
data "google_secret_manager_secret_version" "db_password" {
  secret  = "projects/${module.ctx.account_id}/secrets/db-password"
  version = "latest"
}

# Or create secrets
resource "google_secret_manager_secret" "app_secret" {
  project   = module.ctx.account_id
  secret_id = "app-secret"
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "app_secret_v1" {
  secret      = google_secret_manager_secret.app_secret.id
  secret_data = random_password.app.result
}
```

### Cloud Storage Bucket

```hcl
resource "google_storage_bucket" "assets" {
  project  = module.ctx.account_id
  name     = "${local.tenant.name}-assets"
  location = module.ctx.region
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }
}
```

## GCS Backend Auto-Configuration

The `tf init` wrapper auto-configures:

```bash
# Discovers from gcloud config:
DUPLO_ACCOUNT_ID="my-project-id"

# Constructs:
terraform init \
  -backend-config="bucket=duplo-tfstate-my-project-id"
```

## Service Accounts and IAM

GCP uses service accounts for workload identity:

```hcl
# Get tenant service account
data "duplocloud_tenant" "this" {
  name = local.tenant.name
}

locals {
  service_account = data.duplocloud_tenant.this.gcp_service_account
}

# Grant permissions
resource "google_project_iam_member" "storage_admin" {
  project = module.ctx.account_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${local.service_account}"
}
```

### Workload Identity for Kubernetes

```hcl
resource "google_service_account_iam_binding" "workload_identity" {
  service_account_id = google_service_account.app.name
  role               = "roles/iam.workloadIdentityUser"
  
  members = [
    "serviceAccount:${module.ctx.account_id}.svc.id.goog[${local.tenant.namespace}/${local.app_name}]"
  ]
}
```

## Kubernetes Provider for GKE

```hcl
module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit = {
    k8s = true
  }
  workspaces = {
    tenant = {}
  }
}

provider "kubernetes" {
  host                   = module.ctx.creds.k8s.endpoint
  cluster_ca_certificate = module.ctx.creds.k8s.ca_certificate_data
  token                  = module.ctx.creds.k8s.token
}

provider "helm" {
  kubernetes {
    host                   = module.ctx.creds.k8s.endpoint
    cluster_ca_certificate = module.ctx.creds.k8s.ca_certificate_data
    token                  = module.ctx.creds.k8s.token
  }
}
```
