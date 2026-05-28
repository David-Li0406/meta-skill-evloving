---
name: genkit-infra-expert
description: Use this skill when deploying Genkit applications to production with Terraform, including Firebase Functions, Cloud Run, and GKE, while ensuring secure secrets handling and observability.
---

# Genkit Infra Expert

## Overview

Deploy Genkit applications to production with Terraform, provisioning Firebase Functions, Cloud Run services, and GKE clusters. This skill also includes setting up monitoring dashboards and CI/CD for AI workflows.

## Prerequisites

Before using this skill, ensure:
- Google Cloud project with Firebase enabled
- Terraform 1.0+ installed
- gcloud and firebase CLI authenticated
- Genkit application built and containerized
- API keys for Gemini or other AI models
- Understanding of Genkit flows and deployment options

## Instructions

1. **Choose Deployment Target**: Select from Firebase Functions, Cloud Run, or GKE.
2. **Configure Terraform Backend**: Set up remote state in Google Cloud Storage (GCS).
3. **Define Variables**: Specify Project ID, region, and Genkit app configuration.
4. **Provision Compute**: Deploy functions or containers as needed.
5. **Configure Secrets**: Store API keys in Google Secret Manager.
6. **Set Up Monitoring**: Create dashboards for monitoring token usage and latency.
7. **Enable Auto-scaling**: Configure minimum and maximum instances for your services.
8. **Validate Deployment**: Test Genkit flows via HTTP endpoints.

## Core Terraform Modules

### Firebase Functions Deployment

```hcl
resource "google_cloudfunctions2_function" "genkit_function" {
  name     = "genkit-ai-flow"
  location = var.region

  build_config {
    runtime     = "nodejs20"
    entry_point = "genkitFlow"
    source {
      storage_source {
        bucket = google_storage_bucket.genkit_source.name
        object = google_storage_bucket_object.genkit_code.name
      }
    }
  }

  service_config {
    max_instance_count = 100
    available_memory   = "512Mi"
    timeout_seconds    = 300
    environment_variables = {
      GOOGLE_API_KEY      = var.gemini_api_key
      ENABLE_AI_MONITORING = "true"
    }
  }
}
```

### Cloud Run for Genkit

```hcl
resource "google_cloud_run_v2_service" "genkit_service" {
  name     = "genkit-api"
  location = var.region

  template {
    scaling {
      min_instance_count = 1
      max_instance_count = 10
    }

    containers {
      image = "gcr.io/${var.project_id}/genkit-app:latest"

      resources {
        limits = {
          cpu    = "2"
          memory = "1Gi"
        }
      }

      env {
        name  = "GOOGLE_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.gemini_key.id
            version = "latest"
          }
        }
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}
```

### AI Monitoring Integration

```hcl
resource "google_monitoring_dashboard" "genkit_dashboard" {
  dashboard_json = jsonencode({
    displayName = "Genkit AI Monitoring"
    mosaicLayout = {
      columns = 2
    }
    widgets = [
      {
        scorecard = {
          title = "API Latency"
          metrics = [
            {
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"serviceruntime.googleapis.com/api/request_count\""
                  aggregations = [
                    {
                      alignmentPeriod = "60s"
                      perSeriesAligner = "ALIGN_RATE"
                    }
                  ]
                }
              }
            }
          ]
        }
      }
    ]
  })
}
```

## Output

## Error Handling

Refer to the error handling documentation for comprehensive guidance.

## Resources

- [Genkit Deployment Documentation](https://genkit.dev/docs/deployment)
- [Firebase Terraform Provider](https://registry.terraform.io/providers/hashicorp/google/latest)
- [Genkit Examples](https://genkit.dev/examples)