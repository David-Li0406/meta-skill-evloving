---
name: brev
description: Manage NVIDIA GPU instances on Brev cloud. Use for creating, starting, stopping, and managing GPU instances for the data platform.
allowed-tools: Bash(brev:*)
argument-hint: [command] [args]
---

# Brev CLI Skill

Manage GPU instances on NVIDIA Brev for the data platform deployment.

## Available Commands

### Instance Management

| Command | Description |
|---------|-------------|
| `brev create <name>` | Create a new instance |
| `brev start <name>` | Start a stopped instance |
| `brev stop <name>` | Stop a running instance |
| `brev delete <name>` | Delete an instance |
| `brev reset <name>` | Reset instance if in weird state |
| `brev status` | Show status of current instance |

### Listing & Context

| Command | Description |
|---------|-------------|
| `brev ls` | List instances in active org |
| `brev ls --all` | List all instances including teammates' |
| `brev org ls` | List available organizations |
| `brev set <org-id>` | Set active organization |

### SSH & Access

| Command | Description |
|---------|-------------|
| `brev shell <name>` | Open shell in instance |
| `brev open <name>` | Open VSCode/Cursor to instance |
| `brev port-forward <name>` | Set up port forwarding |
| `brev copy <src> <dest>` | Copy files to/from instance |

### Secrets

| Command | Description |
|---------|-------------|
| `brev secret` | Manage secrets/environment variables |

## GPU Instance Types

When creating instances with `-g/--gpu`, common options include:

| Type | GPUs | Use Case |
|------|------|----------|
| `h200-141gb.1x` | 1x H200-141GB | **REQUIRED for this platform** - fractional GPU sharing |
| `a100-80gb.1x` | 1x A100-80GB | Insufficient for concurrent GPU workloads |
| `n1-highmem-4:nvidia-tesla-t4:1` | 1x T4 | NOT SUPPORTED - too small |

**Note**: This platform requires H200 141GB for KAI Scheduler fractional GPU sharing (NIM 70GB + JupyterHub 70GB).

See https://brev.dev/docs/reference/gpu for full list.

## CPU Instance Types

When creating CPU-only instances with `-c/--cpu`:

| Type | vCPUs | Memory |
|------|-------|--------|
| `2x8` | 2 | 8GB |
| `4x16` | 4 | 16GB |
| `8x32` | 8 | 32GB |
| `16x32` | 16 | 32GB |

## Common Workflows

### Create a GPU instance for development

```bash
brev create dev-platform -g "a2-highgpu-1g:nvidia-a100-40gb:1"
```

### SSH into an instance

```bash
brev shell dev-platform
```

### Port forward to access services

```bash
# Forward ArgoCD UI (port 8080)
brev port-forward dev-platform -p 8080:8080

# Forward multiple ports
brev port-forward dev-platform -p 8080:8080 -p 9000:9000 -p 3000:3000
```

### Copy kubeconfig from instance

```bash
brev copy dev-platform:/etc/rancher/k3s/k3s.yaml ./kubeconfig.yaml
```

### Stop instance when not in use (saves cost)

```bash
brev stop dev-platform
```

### Delete instance completely

```bash
brev delete dev-platform
```

## Project-Specific Instance

For this data platform, the recommended instance name is `brev-data-platform` with GPU configuration suitable for NIM LLM inference.

### Create the data platform instance

```bash
brev create brev-data-platform -g "a2-highgpu-1g:nvidia-a100-40gb:1"
```

## Arguments

When invoked with `/brev`, pass commands directly:

- `/brev ls` - List instances
- `/brev create my-instance -g "..."` - Create instance
- `/brev shell my-instance` - SSH into instance
