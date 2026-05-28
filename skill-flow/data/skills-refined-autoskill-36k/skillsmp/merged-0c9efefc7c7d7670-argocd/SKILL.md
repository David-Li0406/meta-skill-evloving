---
name: argocd
description: Use this skill for GitOps continuous delivery with Argo CD for Kubernetes deployments, including managing applications, ApplicationSets, sync configurations, RBAC, notifications, and health checks.
---

# Argo CD GitOps Continuous Delivery

## Overview

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes that automates application deployment and lifecycle management. It continuously monitors Git repositories and automatically syncs application state to match the desired configuration.

## Core Concepts

- **Application**: A Kubernetes resource tracking a Git repo path to a cluster/namespace.
- **AppProject**: A logical grouping with source/destination restrictions and RBAC policies.
- **ApplicationSet**: A template for generating multiple Applications from generators.
- **Sync**: The process of applying Git manifests to the cluster.
- **Health**: Status assessment of deployed resources.

## Installation and Setup

### Install Argo CD in Kubernetes

```bash
# Create namespace
kubectl create namespace argocd

# Install Argo CD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access the UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# CLI Login
argocd login localhost:8080 --insecure
```

## Application Management

### Minimal Application Example

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD
    path: manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### ApplicationSets

ApplicationSets automate the creation and management of multiple Argo CD applications using generators. Use when:

- Deploying to multiple clusters with the same configuration.
- Managing multiple tenants or teams.
- Discovering applications from Git repository structure.
- Implementing environment promotion strategies.

### Sync Configuration

- **Sync Waves**: Order resource creation with sync waves and hooks.
- **Sync Options**: Configure options like pruning, replacing, and server-side apply.

## RBAC and Projects

### RBAC Configuration

Define roles and permissions for applications and projects to enforce security and access control.

### AppProject Example

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-a
  namespace: argocd
spec:
  description: Team A project
  sourceRepos:
    - "https://github.com/team-a/*"
  destinations:
    - namespace: "team-a-*"
      server: https://kubernetes.default.svc
```

## Notifications and Health Checks

Configure notifications for application events and define health checks to monitor the status of deployed resources.

## CLI Operations

### Common CLI Commands

```bash
# Application management
argocd app create <name> --repo <url> --path <path> --dest-server https://kubernetes.default.svc --dest-namespace <ns>
argocd app sync <name>
argocd app get <name>
argocd app delete <name>
argocd app list

# Cluster management
argocd cluster add <context-name>
argocd cluster list

# Repository management
argocd repo add <url> [--ssh-private-key-path | --username/--password]
argocd repo list

# Project management
argocd proj create <name> -d <server>,<namespace> -s <repo-url>
argocd proj list
```

## References

- [Argo CD Documentation](https://argo-cd.readthedocs.io/en/stable/)
- [Application Spec](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/)
- [CLI Reference](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd/)