---
id: gcp-architecture
name: "GCP Architecture"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# GCP Architecture

## Overview

Google Cloud Platform (GCP) provides cloud infrastructure with strengths in data analytics, machine learning, and Kubernetes (GKE). This methodology covers GCP service selection, architectural patterns, and best practices following Google Cloud's architecture framework.

## When to Use

- Building data-intensive applications
- Deploying ML/AI workloads
- Running Kubernetes-native applications
- Multi-region global deployments
- BigQuery analytics pipelines

## Key Concepts

### GCP Architecture Framework Pillars

| Pillar | Focus Areas |
|--------|-------------|
| Operational Excellence | Monitoring, incident response, automation |
| Security | IAM, encryption, network security |
| Reliability | Availability, disaster recovery, capacity |
| Performance | Scaling, optimization, caching |
| Cost Optimization | Committed use, preemptible VMs, rightsizing |

### Core Services

| Category | Services |
|----------|----------|
| Compute | Compute Engine, GKE, Cloud Run, Cloud Functions |
| Storage | Cloud Storage, Persistent Disk, Filestore |
| Database | Cloud SQL, Cloud Spanner, Firestore, Bigtable |
| Networking | VPC, Cloud Load Balancing, Cloud CDN, Cloud Armor |
| Security | IAM, Secret Manager, Cloud KMS |
| Monitoring | Cloud Monitoring, Cloud Logging, Cloud Trace |

## Implementation

### VPC Network

```hcl
# VPC with custom subnets
resource "google_compute_network" "main" {
  name                            = "${var.project_id}-vpc"
  auto_create_subnetworks         = false
  routing_mode                    = "GLOBAL"
  delete_default_routes_on_create = true
}

# Public subnet
resource "google_compute_subnetwork" "public" {
  name          = "${var.project_id}-public"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.main.id

  # Enable private Google access
  private_ip_google_access = true

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Private subnet with secondary ranges for GKE
resource "google_compute_subnetwork" "private" {
  name          = "${var.project_id}-private"
  ip_cidr_range = "10.0.2.0/24"
  region        = var.region
  network       = google_compute_network.main.id

  private_ip_google_access = true

  # Secondary ranges for GKE pods and services
  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.2.0.0/20"
  }

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Cloud NAT for private subnet egress
resource "google_compute_router" "main" {
  name    = "${var.project_id}-router"
  region  = var.region
  network = google_compute_network.main.id
}

resource "google_compute_router_nat" "main" {
  name                               = "${var.project_id}-nat"
  router                             = google_compute_router.main.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"

  subnetwork {
    name                    = google_compute_subnetwork.private.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# Default route to internet
resource "google_compute_route" "default" {
  name             = "${var.project_id}-default-route"
  dest_range       = "0.0.0.0/0"
  network          = google_compute_network.main.name
  next_hop_gateway = "default-internet-gateway"
  priority         = 1000
}
```

### GKE Cluster

```hcl
# GKE Cluster
resource "google_container_cluster" "main" {
  name     = "${var.project_id}-gke"
  location = var.region

  # Regional cluster for high availability
  node_locations = [
    "${var.region}-a",
    "${var.region}-b",
    "${var.region}-c"
  ]

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.private.name

  # VPC-native cluster
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Private cluster
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"

    master_global_access_config {
      enabled = true
    }
  }

  # Master authorized networks
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.admin_cidr
      display_name = "Admin access"
    }
  }

  # Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Binary Authorization
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  # Release channel
  release_channel {
    channel = "REGULAR"
  }

  # Maintenance window
  maintenance_policy {
    recurring_window {
      start_time = "2024-01-01T02:00:00Z"
      end_time   = "2024-01-01T06:00:00Z"
      recurrence = "FREQ=WEEKLY;BYDAY=SU"
    }
  }

  # Cluster addons
  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
    gce_persistent_disk_csi_driver_config {
      enabled = true
    }
    gcs_fuse_csi_driver_config {
      enabled = true
    }
  }

  # Enable Dataplane V2 (eBPF)
  datapath_provider = "ADVANCED_DATAPATH"

  # Network policy
  network_policy {
    enabled  = true
    provider = "CALICO"
  }

  # Logging and monitoring
  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = true
    }
  }

  # Remove default node pool
  remove_default_node_pool = true
  initial_node_count       = 1

  # Security
  enable_shielded_nodes = true
}

# Node pool
resource "google_container_node_pool" "general" {
  name     = "general"
  location = var.region
  cluster  = google_container_cluster.main.name

  node_count = 1

  autoscaling {
    min_node_count  = 1
    max_node_count  = 10
    location_policy = "BALANCED"
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  upgrade_settings {
    strategy        = "SURGE"
    max_surge       = 1
    max_unavailable = 0
  }

  node_config {
    preemptible  = false
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-ssd"

    # Use containerd
    image_type = "COS_CONTAINERD"

    # Security
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    # Workload Identity
    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    # Service account
    service_account = google_service_account.gke_nodes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      environment = var.environment
      workload    = "general"
    }

    tags = ["gke-node", var.environment]

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}

# Spot node pool
resource "google_container_node_pool" "spot" {
  name     = "spot"
  location = var.region
  cluster  = google_container_cluster.main.name

  autoscaling {
    min_node_count  = 0
    max_node_count  = 20
    location_policy = "ANY"
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    spot         = true
    machine_type = "e2-standard-4"
    disk_size_gb = 50
    disk_type    = "pd-standard"

    image_type = "COS_CONTAINERD"

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    service_account = google_service_account.gke_nodes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      environment = var.environment
      workload    = "spot"
    }

    taint {
      key    = "spot"
      value  = "true"
      effect = "NO_SCHEDULE"
    }
  }
}
```

### Cloud SQL

```hcl
resource "google_sql_database_instance" "main" {
  name             = "${var.project_id}-postgres"
  database_version = "POSTGRES_15"
  region           = var.region

  deletion_protection = var.environment == "prod"

  settings {
    tier              = var.environment == "prod" ? "db-custom-4-16384" : "db-f1-micro"
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100
    disk_autoresize   = true

    # Backup
    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      point_in_time_recovery_enabled = var.environment == "prod"
      backup_retention_settings {
        retained_backups = var.environment == "prod" ? 30 : 7
      }
    }

    # Maintenance
    maintenance_window {
      day          = 7  # Sunday
      hour         = 4
      update_track = "stable"
    }

    # Network
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }

    # Insights
    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = true
      record_client_address   = true
    }

    # Flags
    database_flags {
      name  = "log_checkpoints"
      value = "on"
    }
    database_flags {
      name  = "log_connections"
      value = "on"
    }
    database_flags {
      name  = "log_disconnections"
      value = "on"
    }
    database_flags {
      name  = "log_lock_waits"
      value = "on"
    }
  }

  depends_on = [google_service_networking_connection.private_vpc_connection]
}

# Read replica for production
resource "google_sql_database_instance" "replica" {
  count = var.environment == "prod" ? 1 : 0

  name                 = "${var.project_id}-postgres-replica"
  master_instance_name = google_sql_database_instance.main.name
  region               = var.region
  database_version     = "POSTGRES_15"

  replica_configuration {
    failover_target = true
  }

  settings {
    tier              = "db-custom-4-16384"
    availability_type = "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
      require_ssl     = true
    }
  }
}

# Database
resource "google_sql_database" "main" {
  name     = var.database_name
  instance = google_sql_database_instance.main.name
}

# User
resource "google_sql_user" "main" {
  name     = var.database_user
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}
```

### Cloud Storage and CDN

```hcl
# Storage bucket
resource "google_storage_bucket" "static" {
  name     = "${var.project_id}-static"
  location = var.region

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  lifecycle_rule {
    condition {
      num_newer_versions = 3
    }
    action {
      type = "Delete"
    }
  }

  cors {
    origin          = ["https://${var.domain}"]
    method          = ["GET", "HEAD"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }
}

# CDN Backend bucket
resource "google_compute_backend_bucket" "static" {
  name        = "${var.project_id}-static-backend"
  bucket_name = google_storage_bucket.static.name
  enable_cdn  = true

  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    default_ttl       = 3600
    max_ttl           = 86400
    client_ttl        = 3600
    negative_caching  = true
    serve_while_stale = 86400

    cache_key_policy {
      include_host         = true
      include_protocol     = true
      include_query_string = false
    }
  }
}

# URL map
resource "google_compute_url_map" "main" {
  name            = "${var.project_id}-url-map"
  default_service = google_compute_backend_bucket.static.id

  host_rule {
    hosts        = ["static.${var.domain}"]
    path_matcher = "static"
  }

  path_matcher {
    name            = "static"
    default_service = google_compute_backend_bucket.static.id
  }
}

# HTTPS proxy
resource "google_compute_target_https_proxy" "main" {
  name             = "${var.project_id}-https-proxy"
  url_map          = google_compute_url_map.main.id
  ssl_certificates = [google_compute_managed_ssl_certificate.main.id]
}

# SSL certificate
resource "google_compute_managed_ssl_certificate" "main" {
  name = "${var.project_id}-cert"

  managed {
    domains = ["static.${var.domain}"]
  }
}

# Global forwarding rule
resource "google_compute_global_forwarding_rule" "https" {
  name                  = "${var.project_id}-https-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "443"
  target                = google_compute_target_https_proxy.main.id
  ip_address            = google_compute_global_address.main.id
}
```

### IAM and Workload Identity

```hcl
# Service account for GKE nodes
resource "google_service_account" "gke_nodes" {
  account_id   = "${var.project_id}-gke-nodes"
  display_name = "GKE Node Service Account"
}

resource "google_project_iam_member" "gke_nodes" {
  for_each = toset([
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/stackdriver.resourceMetadata.writer",
    "roles/artifactregistry.reader",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.gke_nodes.email}"
}

# Workload Identity for application
resource "google_service_account" "app" {
  account_id   = "${var.project_id}-app"
  display_name = "Application Service Account"
}

resource "google_service_account_iam_member" "app_workload_identity" {
  service_account_id = google_service_account.app.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.namespace}/app]"
}

# App permissions
resource "google_project_iam_member" "app_storage" {
  project = var.project_id
  role    = "roles/storage.objectUser"
  member  = "serviceAccount:${google_service_account.app.email}"

  condition {
    title       = "limit_to_app_bucket"
    description = "Limit access to app bucket"
    expression  = "resource.name.startsWith(\"projects/_/buckets/${google_storage_bucket.static.name}\")"
  }
}

resource "google_secret_manager_secret_iam_member" "app" {
  for_each = toset([
    google_secret_manager_secret.db_password.id,
    google_secret_manager_secret.api_key.id,
  ])

  secret_id = each.value
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}
```

### Monitoring

```hcl
# Notification channel
resource "google_monitoring_notification_channel" "email" {
  display_name = "DevOps Email"
  type         = "email"

  labels = {
    email_address = var.alert_email
  }
}

# Uptime check
resource "google_monitoring_uptime_check_config" "app" {
  display_name = "${var.project_id} Health Check"
  timeout      = "10s"
  period       = "60s"

  http_check {
    path         = "/health"
    port         = "443"
    use_ssl      = true
    validate_ssl = true
  }

  monitored_resource {
    type = "uptime_url"
    labels = {
      project_id = var.project_id
      host       = var.domain
    }
  }
}

# Alert policy
resource "google_monitoring_alert_policy" "uptime" {
  display_name = "${var.project_id} Uptime Alert"
  combiner     = "OR"

  conditions {
    display_name = "Uptime Health Check"

    condition_threshold {
      filter          = "metric.type=\"monitoring.googleapis.com/uptime_check/check_passed\" AND resource.type=\"uptime_url\" AND metric.labels.check_id=\"${google_monitoring_uptime_check_config.app.uptime_check_id}\""
      duration        = "300s"
      comparison      = "COMPARISON_LT"
      threshold_value = 1

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_NEXT_OLDER"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.id]

  alert_strategy {
    auto_close = "1800s"
  }
}

# Dashboard
resource "google_monitoring_dashboard" "main" {
  dashboard_json = jsonencode({
    displayName = "${var.project_id} Dashboard"
    gridLayout = {
      columns = 2
      widgets = [
        {
          title = "GKE CPU Utilization"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"kubernetes.io/container/cpu/core_usage_time\" resource.type=\"k8s_container\""
                }
              }
            }]
          }
        },
        {
          title = "Cloud SQL Connections"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"cloudsql.googleapis.com/database/postgresql/num_backends\" resource.type=\"cloudsql_database\""
                }
              }
            }]
          }
        }
      ]
    }
  })
}
```

## Best Practices

1. **Use VPC Service Controls** - Protect sensitive data with service perimeters
2. **Enable Workload Identity** - Use GKE Workload Identity instead of service account keys
3. **Use private GKE clusters** - Enable private nodes and authorized networks
4. **Implement Cloud Armor** - Protect applications with WAF rules
5. **Use regional resources** - Deploy across zones for high availability
6. **Enable audit logging** - Cloud Audit Logs for all admin activities
7. **Use managed services** - Cloud SQL, Memorystore, GKE over self-managed
8. **Implement IAM conditions** - Fine-grained access control
9. **Use Secret Manager** - Never hardcode secrets
10. **Enable org policies** - Enforce security constraints at organization level

## Common Pitfalls

1. **Service account key files** - Use Workload Identity or attached service accounts instead of JSON keys.

2. **Default VPC** - Always create custom VPCs with proper subnet sizing and firewall rules.

3. **Public GKE clusters** - Use private clusters with authorized networks for production.

4. **Missing resource labels** - Labels enable cost tracking and resource organization.

5. **Overly permissive IAM** - Use predefined roles and IAM conditions instead of primitive roles.

6. **No VPC flow logs** - Enable flow logs for network debugging and security analysis.

## References

- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [Cloud SQL Best Practices](https://cloud.google.com/sql/docs/postgres/best-practices)
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
