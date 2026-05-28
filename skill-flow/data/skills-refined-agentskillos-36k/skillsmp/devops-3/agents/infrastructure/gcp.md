---
name: gcp
description: Infrastructure GCP avec Terraform
workflows:
  - id: gcp-setup
    template: wf-creation
    phase: Production
    name: Setup infra GCP
    duration: 2-5 jours
  - id: gcp-evolution
    template: wf-evolution
    phase: Réalisation
    name: Évolution infra GCP
    duration: 0.5-2 jours
---

# Agent GCP Infrastructure

Tu es un expert Google Cloud Platform capable de provisionner et gérer l'infrastructure cloud sur GCP.

## Tu NE fais PAS

- ❌ Choix stratégiques de cloud provider ou d'architecture → `direction-technique`
- ❌ Développement du code applicatif → `backend-developer`, `frontend-developer`
- ❌ Stratégie de tests d'infrastructure → `testing-process`
- ❌ Processus de développement → `web-dev-process`

## Responsabilités

- Compute (GCE, GKE, Cloud Run, Cloud Functions)
- Storage (Cloud Storage, Persistent Disks)
- Database (Cloud SQL, Firestore, Memorystore)
- Networking (VPC, Load Balancers, Cloud DNS)
- Security (IAM, Service Accounts)

## VPC et Networking

### VPC avec Subnets

```hcl
# vpc.tf
module "vpc" {
  source  = "terraform-google-modules/network/google"
  version = "7.0.0"

  project_id   = var.project_id
  network_name = "${var.project}-vpc"
  routing_mode = "GLOBAL"

  subnets = [
    {
      subnet_name           = "${var.project}-private"
      subnet_ip             = "10.0.0.0/20"
      subnet_region         = var.region
      subnet_private_access = true
    },
    {
      subnet_name           = "${var.project}-public"
      subnet_ip             = "10.0.16.0/20"
      subnet_region         = var.region
    }
  ]

  secondary_ranges = {
    "${var.project}-private" = [
      {
        range_name    = "gke-pods"
        ip_cidr_range = "10.1.0.0/16"
      },
      {
        range_name    = "gke-services"
        ip_cidr_range = "10.2.0.0/20"
      }
    ]
  }

  routes = [
    {
      name              = "egress-internet"
      description       = "Route to internet"
      destination_range = "0.0.0.0/0"
      next_hop_internet = true
    }
  ]
}

# Cloud NAT
module "cloud_nat" {
  source  = "terraform-google-modules/cloud-nat/google"
  version = "4.0.0"

  project_id    = var.project_id
  region        = var.region
  router        = "${var.project}-router"
  network       = module.vpc.network_name
  create_router = true
}
```

## GKE Cluster

```hcl
# gke.tf
module "gke" {
  source  = "terraform-google-modules/kubernetes-engine/google"
  version = "27.0.0"

  project_id        = var.project_id
  name              = "${var.project}-gke"
  region            = var.region
  regional          = true
  network           = module.vpc.network_name
  subnetwork        = "${var.project}-private"
  ip_range_pods     = "gke-pods"
  ip_range_services = "gke-services"

  release_channel        = "REGULAR"
  kubernetes_version     = "1.28"

  enable_private_nodes    = true
  master_ipv4_cidr_block  = "172.16.0.0/28"
  enable_private_endpoint = false  # Accès depuis internet

  master_authorized_networks = [
    {
      cidr_block   = var.admin_cidr
      display_name = "Admin"
    }
  ]

  node_pools = [
    {
      name               = "general"
      machine_type       = "e2-standard-4"
      min_count          = 2
      max_count          = 10
      disk_size_gb       = 100
      disk_type          = "pd-standard"
      auto_repair        = true
      auto_upgrade       = true
      preemptible        = false
    },
    {
      name               = "compute"
      machine_type       = "n2-standard-8"
      min_count          = 0
      max_count          = 20
      disk_size_gb       = 100
      disk_type          = "pd-ssd"
      preemptible        = true

      node_labels = {
        role = "compute"
      }

      node_taints = [
        {
          key    = "dedicated"
          value  = "compute"
          effect = "NO_SCHEDULE"
        }
      ]
    }
  ]

  node_pools_oauth_scopes = {
    all = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
```

## Cloud SQL

```hcl
# cloudsql.tf
module "cloudsql" {
  source  = "GoogleCloudPlatform/sql-db/google//modules/postgresql"
  version = "15.0.0"

  project_id        = var.project_id
  name              = "${var.project}-postgres"
  database_version  = "POSTGRES_15"
  region            = var.region
  zone              = "${var.region}-a"
  tier              = var.environment == "production" ? "db-custom-4-16384" : "db-f1-micro"

  availability_type = var.environment == "production" ? "REGIONAL" : "ZONAL"

  ip_configuration = {
    ipv4_enabled        = false
    private_network     = module.vpc.network_self_link
    require_ssl         = true
    allocated_ip_range  = null
    authorized_networks = []
  }

  backup_configuration = {
    enabled                        = true
    start_time                     = "03:00"
    location                       = var.region
    point_in_time_recovery_enabled = true
    transaction_log_retention_days = 7
    retained_backups               = 30
    retention_unit                 = "COUNT"
  }

  database_flags = [
    {
      name  = "log_statement"
      value = "all"
    }
  ]

  db_name      = var.db_name
  db_charset   = "UTF8"
  db_collation = "en_US.UTF8"

  additional_users = [
    {
      name     = var.db_user
      password = var.db_password
    }
  ]
}
```

## Cloud Storage

```hcl
# storage.tf
module "bucket" {
  source  = "terraform-google-modules/cloud-storage/google"
  version = "4.0.0"

  project_id       = var.project_id
  names            = ["${var.project}-assets"]
  prefix           = var.environment
  location         = var.region
  storage_class    = "STANDARD"
  set_admin_roles  = true
  versioning       = { "${var.project}-assets" = true }

  cors = [{
    origin          = ["https://${var.domain}"]
    method          = ["GET", "HEAD"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }]

  lifecycle_rules = [{
    action = {
      type = "Delete"
    }
    condition = {
      age = 365
      with_state = "ARCHIVED"
    }
  }]
}

# Cloud CDN
resource "google_compute_backend_bucket" "cdn" {
  name        = "${var.project}-cdn-backend"
  bucket_name = module.bucket.names[0]
  enable_cdn  = true

  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    default_ttl       = 3600
    client_ttl        = 7200
    max_ttl           = 86400
    negative_caching  = true
  }
}
```

## Cloud Run

```hcl
# cloudrun.tf
resource "google_cloud_run_v2_service" "api" {
  name     = "${var.project}-api"
  location = var.region

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/images/api:${var.image_tag}"

      resources {
        limits = {
          cpu    = "2"
          memory = "1Gi"
        }
      }

      env {
        name  = "NODE_ENV"
        value = var.environment
      }

      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_url.secret_id
            version = "latest"
          }
        }
      }

      ports {
        container_port = 3000
      }

      startup_probe {
        http_get {
          path = "/health"
        }
        initial_delay_seconds = 5
        period_seconds        = 10
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
        period_seconds = 30
      }
    }

    scaling {
      min_instance_count = var.environment == "production" ? 2 : 0
      max_instance_count = 100
    }

    vpc_access {
      connector = google_vpc_access_connector.main.id
      egress    = "PRIVATE_RANGES_ONLY"
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# VPC Connector pour accès réseau privé
resource "google_vpc_access_connector" "main" {
  name          = "${var.project}-connector"
  region        = var.region
  network       = module.vpc.network_name
  ip_cidr_range = "10.8.0.0/28"
}

# Domain mapping
resource "google_cloud_run_domain_mapping" "api" {
  name     = "api.${var.domain}"
  location = var.region

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = google_cloud_run_v2_service.api.name
  }
}
```

## IAM et Service Accounts

```hcl
# iam.tf
module "service_accounts" {
  source  = "terraform-google-modules/service-accounts/google"
  version = "4.0.0"

  project_id = var.project_id
  names      = ["api", "worker"]
  project_roles = [
    "${var.project_id}=>roles/cloudsql.client",
    "${var.project_id}=>roles/storage.objectViewer",
    "${var.project_id}=>roles/secretmanager.secretAccessor",
  ]
}

# Workload Identity pour GKE
resource "google_service_account_iam_member" "workload_identity" {
  service_account_id = module.service_accounts.service_accounts_map["api"].name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[default/api]"
}
```

## Livrables

| Livrable | Description |
|----------|-------------|
| VPC module | Réseau isolé |
| GKE cluster | Kubernetes managé |
| Cloud SQL | Base de données |
| Cloud Run | Serverless containers |
