---
name: adk-infra-expert
description: Use this skill when provisioning production-grade Vertex AI ADK infrastructure with Terraform, including secure networking, IAM roles, and Agent Engine runtime.
---

# Adk Infra Expert

## Overview

Provision production-grade Vertex AI ADK infrastructure with Terraform, including secure networking, least-privilege IAM, Agent Engine runtime, Code Execution sandbox defaults, and Memory Bank configuration. This skill generates and validates Terraform modules and a deployment checklist that matches enterprise security constraints, including VPC Service Controls when required.

## Prerequisites

Before using this skill, ensure:
- Google Cloud project with billing enabled
- Terraform 1.0+ installed
- gcloud CLI authenticated with appropriate permissions
- Vertex AI API enabled in the target project
- VPC Service Controls access policy created (for enterprise)
- Understanding of Agent Engine architecture and requirements

## Instructions

1. **Initialize Terraform**: Set up backend for remote state storage.
2. **Configure Variables**: Define `project_id`, `region`, and agent configuration.
3. **Provision VPC**: Create network infrastructure with Private Service Connect.
4. **Set Up IAM**: Create service accounts with least privilege roles.
5. **Deploy Agent Engine**: Configure runtime with code execution and memory bank.
6. **Enable VPC-SC**: Apply service perimeter for data exfiltration protection.
7. **Configure Monitoring**: Set up Cloud Monitoring dashboards and alerts.
8. **Validate Deployment**: Test agent endpoint and verify all components.

## Core Terraform Modules

### Agent Engine Deployment

```hcl
resource "google_vertex_ai_agent_runtime" "adk_agent" {
  project  = var.project_id
  location = var.region

  display_name = "adk-production-agent"

  agent_config {
    model         = "gemini-2.5-flash"

    code_execution {
      enabled           = true
      state_ttl_days    = 14
      sandbox_type      = "SECURE_ISOLATED"
    }

    memory_bank {
      enabled = true
    }

    tools = [
      {
        code_execution = {}
      },
      {
        memory_bank = {}
      }
    ]
  }

  vpc_config {
    vpc_network    = google_compute_network.agent_vpc.id
    private_service_connect {
      enabled = true
    }
  }
}
```

### VPC Service Controls

```hcl
resource "google_access_context_manager_service_perimeter" "adk_perimeter" {
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/servicePerimeters/adk_perimeter"
  title  = "ADK Agent Engine Perimeter"

  status {
    restricted_services = [
      "aiplatform.googleapis.com",
      "run.googleapis.com"
    ]

    vpc_accessible_services {
      enable_restriction = true
      allowed_services   = [
        "aiplatform.googleapis.com"
      ]
    }
  }
}
```

### IAM for Native Agent Identity

```hcl
resource "google_project_iam_member" "agent_identity" {
  project = var.project_id
  role    = "roles/aiplatform.agentUser"
  member  = "serviceAccount:${google_service_account.adk_agent.email}"
}

resource "google_service_account" "adk_agent" {
  account_id   = "adk-agent-sa"
  display_name = "ADK Agent Service Account"
}

# Least privilege for Code Execution
resource "google_project_iam_member" "code_exec_permissions" {
  for_each = toset([
    "roles/compute.viewer",
    "roles/container.viewer",
    "roles/run.viewer"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.adk_agent.email}"
}
```

## Tool Permissions

Read, Write, Edit, Grep, Glob, Bash - Enterprise infrastructure provisioning.

## References

- Agent Engine: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview
- VPC-SC: https://cloud.google.com/vpc-service-controls/docs
- Terraform Google Provider: https://registry.terraform.io/providers/hashicorp/google/latest