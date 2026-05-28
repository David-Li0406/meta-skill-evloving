---
name: vertex-ai-infrastructure-provisioning
description: Use this skill when provisioning Vertex AI infrastructure with Terraform, including endpoints, models, and vector search indices.
---

# Vertex AI Infrastructure Provisioning

## Overview

This skill enables the provisioning of Vertex AI infrastructure using Terraform, covering components such as endpoints, deployed models, vector search indices, and ML pipelines. It incorporates production guardrails like encryption, autoscaling, IAM least privilege, and operational validation steps.

## When This Skill Activates

Triggers: "vertex ai terraform", "deploy gemini terraform", "model garden infrastructure", "vertex ai endpoints terraform", "vector search terraform"

## Prerequisites

Before using this skill, ensure:
- Google Cloud project with Vertex AI API enabled
- Terraform 1.0+ installed
- gcloud CLI authenticated with appropriate permissions
- Understanding of Vertex AI services and ML models
- KMS keys created for encryption (if required)
- GCS buckets for model artifacts and embeddings

## Instructions

1. **Define AI Services**: Identify required Vertex AI components (endpoints, vector search, pipelines).
2. **Configure Terraform**: Set up backend and define project variables.
3. **Provision Endpoints**: Deploy Gemini or custom model endpoints with auto-scaling.
4. **Set Up Vector Search**: Create indices for embeddings with appropriate dimensions.
5. **Configure Encryption**: Apply KMS encryption to endpoints and data.
6. **Implement Monitoring**: Set up Cloud Monitoring for model performance.
7. **Apply IAM Policies**: Grant least privilege access to AI services.
8. **Validate Deployment**: Test endpoints and verify model availability.

## Core Terraform Modules

### Gemini Model Endpoint

```hcl
resource "google_vertex_ai_endpoint" "gemini_endpoint" {
  name         = "<endpoint_name>"
  display_name = "<display_name>"
  location     = var.region

  encryption_spec {
    kms_key_name = google_kms_crypto_key.vertex_key.id
  }
}

resource "google_vertex_ai_deployed_model" "gemini_deployment" {
  endpoint = google_vertex_ai_endpoint.gemini_endpoint.id
  model    = "<model_path>"

  dedicated_resources {
    min_replica_count      = 1
    max_replica_count      = 10
    machine_spec {
      machine_type = "<machine_type>"
    }
  }

  automatic_resources {
    min_replica_count = 1
    max_replica_count = 5
  }
}
```

### Vector Search Index

```hcl
resource "google_vertex_ai_index" "embeddings_index" {
  display_name = "<index_display_name>"
  location     = var.region

  metadata {
    contents_delta_uri = "gs://${google_storage_bucket.embeddings.name}/index"
    config {
      dimensions                  = <dimensions>
      approximate_neighbors_count = <neighbors_count>
      distance_measure_type       = "<distance_measure>"

      algorithm_config {
        tree_ah_config {
          leaf_node_embedding_count    = <leaf_node_count>
          leaf_nodes_to_search_percent = <search_percent>
        }
      }
    }
  }
}
```

## Tool Permissions

Read, Write, Edit, Grep, Glob, Bash - AI infrastructure provisioning

## Resources

- Vertex AI Terraform: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/vertex_ai_endpoint
- Vertex AI documentation: https://cloud.google.com/vertex-ai/docs
- Model Garden: https://cloud.google.com/model-garden
- Vector Search guide: https://cloud.google.com/vertex-ai/docs/vector-search