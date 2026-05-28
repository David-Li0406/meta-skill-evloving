---
name: building-gitops-workflows
description: Use this skill when constructing GitOps workflows with ArgoCD or Flux to automate Kubernetes deployments and generate production-ready configurations.
---

## Overview

This skill empowers the creation of GitOps workflows, automating application deployments and infrastructure management through Git repositories. It provides production-ready configurations for both ArgoCD and Flux, ensuring best practices and a security-first approach.

## How It Works

1. **Requirement Gathering**: Analyze the user's request to understand the desired GitOps setup, including the choice of ArgoCD or Flux, target Kubernetes cluster, and application requirements.
2. **Configuration Generation**: Generate the necessary configuration files, such as ArgoCD Application manifests or Flux Kustomization files, based on the gathered requirements.
3. **Code Snippet Creation**: Create code snippets for setting up the GitOps repository structure and deploying the initial configurations to the Kubernetes cluster.

## When to Use This Skill

This skill activates when you need to:
- Create a new GitOps workflow using ArgoCD or Flux.
- Automate application deployments to a Kubernetes cluster using GitOps principles.
- Generate production-ready configurations for GitOps deployments.

## Prerequisites

Before using this skill, ensure:
- Kubernetes cluster is accessible and `kubectl` is configured.
- Git repository is available for GitOps source.
- ArgoCD or Flux is installed on the cluster (or ready to install).
- Appropriate RBAC permissions for the GitOps operator.
- Network connectivity between the cluster and Git repository.

## Instructions

1. **Select GitOps Tool**: Determine whether to use ArgoCD or Flux based on requirements.
2. **Define Application Structure**: Establish repository layout with environment separation (dev/staging/prod).
3. **Generate Manifests**: Create Application/Kustomization files pointing to Git sources.
4. **Configure Sync Policy**: Set automated or manual sync with self-heal and prune options.
5. **Implement RBAC**: Define service accounts and role bindings for the GitOps operator.
6. **Set Up Monitoring**: Configure notifications and health checks for deployments.
7. **Validate Configuration**: Test sync behavior and verify reconciliation loops.

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
2. Provide instructions on how to install FluxCD and configure it to synchronize with the Git repository.

## Best Practices

- **Repository Structure**: Organize your GitOps repository with clear separation of concerns, such as environments (dev, staging, prod) and application components.
- **Declarative Configuration**: Define all application and infrastructure configurations declaratively in Git, using tools like Kustomize or Helm.
- **Automated Reconciliation**: Ensure that your GitOps tool continuously reconciles the desired state in Git with the actual state in the Kubernetes cluster.

## Error Handling

Common issues and solutions:

- **Sync Failures**: Verify Git repository URL, credentials, and target path exist.
- **RBAC Permissions**: Grant GitOps service account appropriate cluster roles.
- **Out of Sync State**: Enable automated sync or manually sync via UI/CLI.
- **Git Authentication**: Configure SSH keys or access tokens in the Git configuration.
- **Resource Conflicts**: Import existing resources or remove conflicting manual deployments.

## Integration

This skill can be used in conjunction with other skills that manage Kubernetes resources, such as creating deployments, services, and ingress controllers. It also integrates with version control systems like Git to store and manage the GitOps configurations.

## Resources

- ArgoCD documentation: [ArgoCD Docs](https://argo-cd.readthedocs.io/)
- Flux documentation: [Flux Docs](https://fluxcd.io/docs/)
- GitOps principles and patterns guide
- Kubernetes manifest best practices
- Repository structure templates in the GitOps examples.