---
name: creating-kubernetes-deployments
description: Use this skill when you need to generate Kubernetes deployment manifests, services, and related configurations following best practices.
---

## Overview

This skill allows Claude to create production-ready Kubernetes deployments and services. It generates complete K8s manifests with health checks, auto-scaling, ingress, TLS, and resource management configured.

## How It Works

1. **Receiving Request**: Claude receives a request to create Kubernetes resources.
2. **Generating Manifests**: Claude generates YAML manifests for deployments, services, configmaps, secrets, ingress, and horizontal pod autoscalers based on the user's requirements.
3. **Presenting Manifests**: Claude presents the generated manifests to the user for review and deployment.

## When to Use This Skill

This skill activates when you need to:
- Create a new Kubernetes deployment.
- Define a Kubernetes service for an application.
- Generate Kubernetes manifests for any K8s resource.

## Examples

### Example 1: Deploying a Web Application

User request: "Create a Kubernetes deployment for a web application named `<app_name>` with `<replica_count>` replicas, exposing port `<port>`."

The skill will:
1. Generate a Deployment manifest for `<app_name>` with `<replica_count>` replicas.
2. Generate a Service manifest to expose port `<port>` of the deployment.

### Example 2: Setting up Ingress for a Service

User request: "Set up an Ingress resource to route traffic to the `<app_name>` service."

The skill will:
1. Generate an Ingress manifest to route external traffic to the `<app_name>` service.
2. Configure TLS termination for secure access.

## Best Practices

- **Resource Limits**: Define resource requests and limits for each container to ensure fair resource allocation.
- **Health Checks**: Configure liveness and readiness probes to enable automatic restarts and prevent traffic from being routed to unhealthy pods.
- **Namespaces**: Use namespaces to isolate different environments or applications within the cluster.

## Integration

This skill can be used with other Claude Code plugins for tasks such as deploying infrastructure-as-code (IaC) or integrating with CI/CD pipelines. It provides the Kubernetes manifests that other plugins can then deploy or manage.