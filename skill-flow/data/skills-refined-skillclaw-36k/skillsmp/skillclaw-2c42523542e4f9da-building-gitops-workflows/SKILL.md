---
name: building-gitops-workflows
description: Use this skill when you need to construct GitOps workflows using ArgoCD or Flux, generating production-ready configurations and implementing best practices for Kubernetes deployments.
---

# Skill body

## Overview

This skill empowers you to create GitOps workflows, automating application deployments and infrastructure management through Git repositories. It provides production-ready configurations for both ArgoCD and Flux, ensuring best practices and a secure approach.

## When to Use This Skill

This skill activates when you need to:
- Create a new GitOps workflow using ArgoCD or Flux.
- Automate application deployments to a Kubernetes cluster using GitOps principles.
- Generate production-ready configurations for GitOps deployments.

## Instructions

1. **Select GitOps Tool**: Determine whether to use ArgoCD or Flux based on your requirements.
2. **Requirement Gathering**: Analyze your request to understand the desired GitOps setup, including the choice of tool, target Kubernetes cluster, and application requirements.
3. **Define Application Structure**: Establish the repository layout with environment separation (dev/staging/prod).
4. **Generate Manifests**: Create Application/Kustomization files pointing to Git sources.
5. **Configure Sync Policy**: Set automated or manual sync with self-heal and prune options.
6. **Implement RBAC**: Define service accounts and role bindings for the GitOps operator.
7. **Set Up Monitoring**: Configure notifications and health checks for deployments.
8. **Validate Configuration**: Test sync behavior and verify reconciliation loops.

## Examples

### Example 1: Setting up ArgoCD for a new application

User request: "Create an ArgoCD workflow to deploy a new application from a Git repository to my Kubernetes cluster."

The skill will:
1. Generate an ArgoCD Application manifest that points to the application's Git repository.
2. Provide instructions on how to deploy the ArgoCD Application to the Kubernetes cluster.

### Example 2: Configuring FluxCD for infrastructure management

User request: "Set up FluxCD to manage my Kubernetes infrastructure configurations stored in a Git repository."

The skill will:
1. Generate Flux Kustomization files that define the desired state of the Kubernetes infrastructure.
2. Provide instructions on how to install FluxCD and configure it to synchronize with the repository.