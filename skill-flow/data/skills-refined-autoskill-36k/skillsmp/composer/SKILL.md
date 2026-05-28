---
name: composer
description: GCP Composer 2 deployment and operations with Terraform configuration. Use when creating Composer environments, configuring worker/scheduler/triggerer resources, setting up Airflow connections and variables, implementing monitoring dashboards, troubleshooting worker crashes or scheduler lag, performing version upgrades, or implementing disaster recovery.
---

# GCP Composer Deployment Skill

Configure and manage GCP Composer environments following best practices.

## Terraform Configuration

### Composer 2 Environment
```hcl
# composer.tf
resource "google_composer_environment" "recommendation_env" {
  name    = "recommendation-${var.environment}"
  region  = var.region
  project = var.project_id

  config {
    software_config {
      image_version = "composer-2.9.0-airflow-2.9.3"
      
      pypi_packages = {
        "google-cloud-bigquery"  = ">=3.0.0"
        "pandas"                 = ">=2.0.0"
        "scikit-learn"           = ">=1.3.0"
      }
      
      env_variables = {
        GCP_PROJECT      = var.project_id
        ENVIRONMENT      = var.environment
        AIRFLOW_VAR_ENV  = var.environment
      }
    }

    workloads_config {
      scheduler {
        cpu        = 2
        memory_gb  = 4
        storage_gb = 10
        count      = 2  # HA scheduler
      }
      
      web_server {
        cpu        = 2
        memory_gb  = 4
        storage_gb = 10
      }
      
      worker {
        cpu        = 4
        memory_gb  = 8
        storage_gb = 20
        min_count  = 2
        max_count  = 10  # Auto-scaling
      }
      
      triggerer {
        count     = 2
        cpu       = 1
        memory_gb = 2
      }
    }

    environment_size = "ENVIRONMENT_SIZE_MEDIUM"

    node_config {
      service_account = google_service_account.composer_sa.email
      network         = google_compute_network.main.id
      subnetwork      = google_compute_subnetwork.composer.id
    }

    private_environment_config {
      enable_private_endpoint = true
    }

    master_authorized_networks_config {
      enabled = true
      cidr_blocks {
        cidr_block   = var.allowed_cidr
        display_name = "Allowed Network"
      }
    }
  }

  labels = {
    environment = var.environment
    team        = "data-engineering"
    project     = "recommendation"
  }
}
```

### Service Account
```hcl
resource "google_service_account" "composer_sa" {
  account_id   = "composer-${var.environment}"
  display_name = "Composer Service Account"
  project      = var.project_id
}

# Required roles for Composer
resource "google_project_iam_member" "composer_roles" {
  for_each = toset([
    "roles/composer.worker",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/storage.objectViewer",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
  ])
  
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.composer_sa.email}"
}
```

## Airflow Variables Setup

```python
# scripts/setup_variables.py
from airflow.models import Variable
import json

# Environment-specific configuration
config = {
    "gcp_project": "recommendation-prod",
    "gcp_region": "asia-southeast1",
    "bq_dataset": "recommendation",
    "gcs_bucket": "recommendation-data",
    "slack_webhook": "{{ secret.slack_webhook }}",
    "email_recipients": "data-team@example.com",
}

for key, value in config.items():
    Variable.set(key, value)

# Complex configuration as JSON
ml_config = {
    "model_params": {
        "num_factors": 50,
        "learning_rate": 0.1,
        "regularization": 0.01,
    },
    "training_days": 180,
    "min_interactions": 5,
}
Variable.set("ml_config", json.dumps(ml_config))
```

## Airflow Connections

```bash
# BigQuery connection (via gcloud)
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  connections add \
  -- \
  --conn-id google_cloud_default \
  --conn-type google_cloud_platform \
  --conn-extra '{"project": "recommendation-prod", "location": "asia-southeast1"}'

# Secret Manager connection
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  connections add \
  -- \
  --conn-id google_cloud_secret_manager \
  --conn-type google_cloud_platform \
  --conn-extra '{"project": "recommendation-prod"}'
```

## Environment Configuration

### airflow.cfg overrides
```python
# Composer environment variables for Airflow config
env_variables = {
    # Core
    "AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION": "True",
    "AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG": "3",
    "AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG": "16",
    "AIRFLOW__CORE__PARALLELISM": "32",
    
    # Scheduler
    "AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL": "60",
    "AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL": "120",
    
    # Email
    "AIRFLOW__EMAIL__EMAIL_BACKEND": "airflow.providers.sendgrid.utils.emailer.send_email",
    
    # Secrets
    "AIRFLOW__SECRETS__BACKEND": "airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend",
    "AIRFLOW__SECRETS__BACKEND_KWARGS": '{"project_id": "recommendation-prod", "prefix": "airflow-"}',
}
```

## Monitoring & Alerting

### Cloud Monitoring Dashboard
```yaml
# monitoring/composer_dashboard.yaml
displayName: Composer Recommendation Pipeline
gridLayout:
  widgets:
    - title: DAG Run Success Rate
      xyChart:
        dataSets:
          - timeSeriesQuery:
              timeSeriesFilter:
                filter: metric.type="composer.googleapis.com/workflow/run_count"
                aggregation:
                  perSeriesAligner: ALIGN_RATE
                  groupByFields: ["metric.label.status"]
                  
    - title: Task Duration
      xyChart:
        dataSets:
          - timeSeriesQuery:
              timeSeriesFilter:
                filter: metric.type="composer.googleapis.com/workflow/task/duration"
                
    - title: Worker CPU Utilization
      xyChart:
        dataSets:
          - timeSeriesQuery:
              timeSeriesFilter:
                filter: metric.type="composer.googleapis.com/environment/worker/cpu_utilization"
```

## Operational Troubleshooting

### Common Issues and Solutions

#### Worker Pod Crashes
```bash
# Check worker pod status
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  kubectl -- get pods -n composer-user-workloads

# View logs for crashed pods
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  kubectl -- logs -l component=worker -n composer-user-workloads --tail=100

# Describe pod for detailed error information
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  kubectl -- describe pod <pod-name> -n composer-user-workloads
```

#### Scheduler Lag Diagnosis
```python
# scripts/check_scheduler_health.py
from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def check_scheduler_health(project_id: str, environment_name: str):
    """Check scheduler heartbeat and performance."""

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Check scheduler heartbeat
    heartbeat_filter = f'''
    metric.type="composer.googleapis.com/environment/scheduler/heartbeat"
    AND resource.labels.environment_name="{environment_name}"
    '''

    interval = monitoring_v3.TimeInterval({
        "end_time": {"seconds": int(datetime.now().timestamp())},
        "start_time": {"seconds": int((datetime.now() - timedelta(minutes=5)).timestamp())},
    })

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": heartbeat_filter,
            "interval": interval,
        }
    )

    heartbeats = list(results)
    if not heartbeats:
        print("WARNING: No scheduler heartbeats detected!")
        return False

    print(f"Scheduler healthy - {len(heartbeats)} heartbeats in last 5 minutes")
    return True
```

#### Clear Stuck Tasks
```bash
# Clear tasks in specific state
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  tasks clear \
  -- recommendation_train_daily \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --only-failed \
  --yes

# Force mark task as success (use with caution)
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  tasks state \
  -- recommendation_train_daily extract_features 2024-01-15 \
  --state success
```

### Database Deadlock Resolution
```bash
# Check database connections
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  db check

# Reset database if corrupted
gcloud composer environments run recommendation-prod \
  --location asia-southeast1 \
  db reset \
  --yes
```

## Upgrade & Migration Strategies

### Airflow Version Upgrade Process
```bash
# 1. Check current version
gcloud composer environments describe recommendation-prod \
  --location asia-southeast1 \
  --format="value(config.softwareConfig.imageVersion)"

# 2. List available versions
gcloud composer environments list-upgrades recommendation-prod \
  --location asia-southeast1

# 3. Create staging environment with new version
gcloud composer environments create recommendation-staging \
  --location asia-southeast1 \
  --image-version composer-2.10.0-airflow-2.10.0 \
  --environment-size small

# 4. Test DAGs in staging
# Deploy DAGs to staging and run validation

# 5. Upgrade production
gcloud composer environments update recommendation-prod \
  --location asia-southeast1 \
  --update-image-version composer-2.10.0-airflow-2.10.0
```

### Blue-Green Deployment Strategy
```hcl
# terraform/environments.tf
# Maintain two identical environments for zero-downtime upgrades

resource "google_composer_environment" "blue" {
  name = "recommendation-blue"
  # ... configuration
}

resource "google_composer_environment" "green" {
  name = "recommendation-green"
  # ... same configuration
}

# Switch traffic using Cloud Load Balancer or DNS
resource "google_dns_record_set" "airflow" {
  name = "airflow.example.com."
  type = "A"
  ttl  = 300

  managed_zone = google_dns_managed_zone.main.name

  # Point to active environment
  rrdatas = [var.active_environment == "blue" ?
    google_composer_environment.blue.config.0.airflow_uri :
    google_composer_environment.green.config.0.airflow_uri
  ]
}
```

## Cost Optimization

### Right-Sizing Workloads
```hcl
# Cost-optimized configuration
resource "google_composer_environment" "cost_optimized" {
  config {
    workloads_config {
      scheduler {
        cpu        = 1       # Reduced from 2
        memory_gb  = 2       # Reduced from 4
        storage_gb = 5       # Reduced from 10
        count      = 1       # Single scheduler for non-critical
      }

      worker {
        cpu        = 2       # Reduced from 4
        memory_gb  = 4       # Reduced from 8
        storage_gb = 10      # Reduced from 20
        min_count  = 1       # Scale to zero when idle
        max_count  = 5       # Lower max for cost control
      }
    }

    # Use preemptible nodes (60-90% cost savings)
    node_config {
      machine_type = "n1-standard-2"
      preemptible  = true

      # Reduce disk size
      disk_size_gb = 30
    }
  }
}
```

### Auto-Scaling Tuning
```python
# Airflow configuration for efficient auto-scaling
env_variables = {
    # Worker auto-scaling
    "AIRFLOW__CELERY__WORKER_AUTOSCALE": "16,4",  # max,min tasks per worker

    # Reduce worker heartbeat for faster scale-down
    "AIRFLOW__CELERY_BROKER_TRANSPORT_OPTIONS__VISIBILITY_TIMEOUT": "3600",

    # Task queue optimization
    "AIRFLOW__CELERY__WORKER_PREFETCH_MULTIPLIER": "1",  # One task at a time
}
```

### Cost Tracking per DAG
```python
# scripts/track_composer_costs.py
from google.cloud import billing_v1
from datetime import datetime, timedelta

def get_composer_costs(project_id: str, environment_name: str, days: int = 30):
    """Track Composer environment costs."""

    client = billing_v1.CloudBillingClient()

    # Query Cloud Billing Export
    query = f"""
    SELECT
      service.description as service,
      sku.description as sku,
      SUM(cost) as total_cost,
      currency
    FROM `{project_id}.billing_export.gcp_billing_export_v1`
    WHERE DATE(_PARTITIONTIME) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
      AND labels.value = "{environment_name}"
      AND service.description = "Cloud Composer"
    GROUP BY service, sku, currency
    ORDER BY total_cost DESC
    """

    # Execute query and return results
    # Implementation depends on your billing export setup
    pass
```

## Security Hardening

### Private IP Configuration
```hcl
resource "google_composer_environment" "secure" {
  config {
    private_environment_config {
      # Enable private IP
      enable_private_endpoint = true
      enable_privately_used_public_ips = false

      # Define IP ranges
      cloud_sql_ipv4_cidr_block = "10.20.0.0/16"
      web_server_ipv4_cidr_block = "10.30.0.0/28"
      cloud_composer_network_ipv4_cidr_block = "10.40.0.0/16"
    }

    # Master authorized networks
    master_authorized_networks_config {
      enabled = true
      cidr_blocks {
        display_name = "Corporate VPN"
        cidr_block   = "10.0.0.0/16"
      }
    }
  }
}
```

### Workload Identity Federation
```hcl
# Use Workload Identity instead of service account keys
resource "google_service_account" "composer_wi" {
  account_id   = "composer-workload-identity"
  display_name = "Composer Workload Identity"
}

resource "google_service_account_iam_binding" "workload_identity" {
  service_account_id = google_service_account.composer_wi.name
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[composer-user-workloads/airflow-worker]"
  ]
}
```

### Secret Manager Integration
```python
# Airflow configuration for Secret Manager backend
env_variables = {
    "AIRFLOW__SECRETS__BACKEND": "airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend",
    "AIRFLOW__SECRETS__BACKEND_KWARGS": json.dumps({
        "project_id": "recommendation-prod",
        "connections_prefix": "airflow-connections",
        "variables_prefix": "airflow-variables",
        "sep": "-",
    }),
}

# Store secrets in Secret Manager
# gcloud secrets create airflow-variables-database-password --data-file=-
```

## Disaster Recovery

### Backup Procedures
```bash
#!/bin/bash
# scripts/backup_composer.sh

PROJECT_ID="recommendation-prod"
LOCATION="asia-southeast1"
ENV_NAME="recommendation-prod"
BACKUP_BUCKET="composer-backups-${PROJECT_ID}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# 1. Backup Airflow Variables
gcloud composer environments storage data export ${ENV_NAME} \
  --location ${LOCATION} \
  --source variables \
  --destination gs://${BACKUP_BUCKET}/${TIMESTAMP}/variables/

# 2. Backup Connections
gcloud composer environments storage data export ${ENV_NAME} \
  --location ${LOCATION} \
  --source connections \
  --destination gs://${BACKUP_BUCKET}/${TIMESTAMP}/connections/

# 3. Backup DAGs
DAGS_BUCKET=$(gcloud composer environments describe ${ENV_NAME} \
  --location ${LOCATION} \
  --format='value(config.dagGcsPrefix)')

gsutil -m rsync -r ${DAGS_BUCKET}/ \
  gs://${BACKUP_BUCKET}/${TIMESTAMP}/dags/

# 4. Export environment configuration
gcloud composer environments describe ${ENV_NAME} \
  --location ${LOCATION} \
  --format yaml > /tmp/composer-config-${TIMESTAMP}.yaml

gsutil cp /tmp/composer-config-${TIMESTAMP}.yaml \
  gs://${BACKUP_BUCKET}/${TIMESTAMP}/config.yaml

echo "Backup completed: gs://${BACKUP_BUCKET}/${TIMESTAMP}/"
```

### Restore Procedures
```bash
#!/bin/bash
# scripts/restore_composer.sh

BACKUP_PATH="gs://composer-backups-project/20240115-120000"

# 1. Restore Variables
gcloud composer environments storage data import ${ENV_NAME} \
  --location ${LOCATION} \
  --source ${BACKUP_PATH}/variables/ \
  --destination variables

# 2. Restore Connections
gcloud composer environments storage data import ${ENV_NAME} \
  --location ${LOCATION} \
  --source ${BACKUP_PATH}/connections/ \
  --destination connections

# 3. Restore DAGs
DAGS_BUCKET=$(gcloud composer environments describe ${ENV_NAME} \
  --location ${LOCATION} \
  --format='value(config.dagGcsPrefix)')

gsutil -m rsync -r ${BACKUP_PATH}/dags/ ${DAGS_BUCKET}/

echo "Restore completed from ${BACKUP_PATH}"
```

### Cross-Region Failover
```hcl
# Maintain standby environment in different region
resource "google_composer_environment" "primary" {
  name   = "recommendation-prod"
  region = "asia-southeast1"
  # ... configuration
}

resource "google_composer_environment" "standby" {
  name   = "recommendation-prod-standby"
  region = "asia-northeast1"
  # ... same configuration
}

# Automated replication of DAGs via Cloud Build trigger
resource "google_cloudbuild_trigger" "dag_replication" {
  name = "replicate-dags-to-standby"

  github {
    owner = "your-org"
    name  = "airflow-dags"
    push {
      branch = "^main$"
    }
  }

  build {
    step {
      name = "gcr.io/cloud-builders/gsutil"
      args = [
        "rsync", "-r", "-d",
        "gs://primary-dags-bucket/dags/",
        "gs://standby-dags-bucket/dags/"
      ]
    }
  }
}
```

## Best Practices

- Use Composer 2 for better autoscaling and resource management
- Enable private IP for security
- Use triggerer for deferrable operators
- Store secrets in Secret Manager, not Airflow Variables
- Set up proper IAM roles with least privilege
- Monitor environment health with Cloud Monitoring
- Implement automated backups of DAGs, variables, and connections
- Use Workload Identity instead of service account keys
- Test upgrades in staging before production
- Maintain disaster recovery plan with cross-region standby
