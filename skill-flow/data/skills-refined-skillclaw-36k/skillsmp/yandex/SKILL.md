---
name: yandex
description: >
  Query Yandex Cloud infrastructure using yc CLI for debugging and understanding
  current setup. READ-ONLY - never modify infrastructure state. Triggers: checking
  VMs, Kubernetes clusters, databases, networking, storage, serverless functions,
  or any yc CLI operations. Always ask user approval before state-changing operations.
license: MIT
compatibility: opencode
---

# Yandex Cloud CLI Skill

Query Yandex Cloud infrastructure for debugging and understanding the current setup. This skill is strictly READ-ONLY.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Checking VM (Compute) status or configuration
- Viewing Kubernetes cluster state
- Checking database (PostgreSQL, MySQL, Redis) status
- Investigating networking (VPC, subnets, security groups)
- Viewing Object Storage (S3) buckets
- Checking serverless functions or triggers
- DNS zone and record inspection
- Certificate status
- Any `yc` CLI operation

**If the user asks about Yandex Cloud resources, use this skill.**

## Critical Safety Rules

**NEVER (state-changing commands - forbidden without explicit approval):**
- `create`, `delete`, `update`, `set`, `add`, `remove`
- `start`, `stop`, `restart`
- `attach`, `detach`
- Any command that modifies resources

**ALWAYS allowed (read-only):**
- `yc <service> <resource> list`
- `yc <service> <resource> get`
- `yc config list`
- `yc config profile list`
- Any command with `--format` for output formatting

### Approval Request Format

Before any state-changing operation (if ever needed), ask:

```
I need to run a state-changing Yandex Cloud command:
  Command: yc compute instance stop my-instance
  Impact: Will stop the VM instance
  
Do you approve? (yes/no)
```

## Quick Reference

| Task | Command |
|------|---------|
| Check current config | `yc config list` |
| List profiles | `yc config profile list` |
| List VMs | `yc compute instance list` |
| List K8s clusters | `yc managed-kubernetes cluster list` |
| List PostgreSQL clusters | `yc managed-postgresql cluster list` |
| List networks | `yc vpc network list` |

## Configuration

```bash
# Show current config
yc config list

# List available profiles
yc config profile list

# Get current profile
yc config profile get

# Switch profile (safe - just changes read context)
yc config profile activate <profile-name>

# Get current folder
yc config get folder-id

# Get current cloud
yc config get cloud-id
```

## Compute (VMs)

```bash
# List all VMs
yc compute instance list

# Get VM details
yc compute instance get <instance-name>

# List disks
yc compute disk list

# Get disk details
yc compute disk get <disk-name>

# List images
yc compute image list

# List snapshots
yc compute snapshot list

# List instance groups
yc compute instance-group list

# List zones
yc compute zone list
```

## Managed Kubernetes

```bash
# List clusters
yc managed-kubernetes cluster list

# Get cluster details
yc managed-kubernetes cluster get <cluster-name>

# List node groups
yc managed-kubernetes node-group list --cluster-name <cluster-name>

# Get node group details
yc managed-kubernetes node-group get <node-group-name>

# Get cluster credentials (for kubectl access)
yc managed-kubernetes cluster get-credentials <cluster-name> --external
```

## Managed Databases

### PostgreSQL

```bash
# List clusters
yc managed-postgresql cluster list

# Get cluster details
yc managed-postgresql cluster get <cluster-name>

# List databases
yc managed-postgresql database list --cluster-name <cluster-name>

# List users
yc managed-postgresql user list --cluster-name <cluster-name>

# List hosts
yc managed-postgresql hosts list --cluster-name <cluster-name>

# List backups
yc managed-postgresql backup list --cluster-id <cluster-id>
```

### MySQL

```bash
# List clusters
yc managed-mysql cluster list

# Get cluster details
yc managed-mysql cluster get <cluster-name>

# List databases
yc managed-mysql database list --cluster-name <cluster-name>

# List users
yc managed-mysql user list --cluster-name <cluster-name>

# List hosts
yc managed-mysql hosts list --cluster-name <cluster-name>
```

### Redis

```bash
# List clusters
yc managed-redis cluster list

# Get cluster details
yc managed-redis cluster get <cluster-name>

# List hosts
yc managed-redis hosts list --cluster-name <cluster-name>
```

## VPC (Networking)

```bash
# List networks
yc vpc network list

# Get network details
yc vpc network get <network-name>

# List subnets
yc vpc subnet list

# Get subnet details
yc vpc subnet get <subnet-name>

# List security groups
yc vpc security-group list

# Get security group details
yc vpc security-group get <security-group-name>

# List addresses
yc vpc address list

# List route tables
yc vpc route-table list
```

## Object Storage (S3)

```bash
# List buckets (using AWS CLI with Yandex endpoint)
aws --endpoint-url=https://storage.yandexcloud.net s3 ls

# List bucket contents
aws --endpoint-url=https://storage.yandexcloud.net s3 ls s3://<bucket-name>/

# Get object metadata
aws --endpoint-url=https://storage.yandexcloud.net s3api head-object --bucket <bucket> --key <key>
```

## Serverless Functions

```bash
# List functions
yc serverless function list

# Get function details
yc serverless function get <function-name>

# List function versions
yc serverless function version list --function-name <function-name>

# List triggers
yc serverless trigger list
```

## Other Services

### Container Registry

```bash
# List registries
yc container registry list

# Get registry details
yc container registry get <registry-id>

# List images in registry
yc container image list --registry-id <registry-id>
```

### DNS

```bash
# List DNS zones
yc dns zone list

# Get zone details
yc dns zone get <zone-name>

# List DNS records
yc dns zone list-records <zone-name>
```

### Certificate Manager

```bash
# List certificates
yc certificate-manager certificate list

# Get certificate details
yc certificate-manager certificate get <certificate-id>
```

### Logging

```bash
# List log groups
yc logging group list

# Read logs
yc logging read --group-name <group-name> --limit 100

# Read logs with filter
yc logging read --group-name <group-name> --filter 'level=ERROR'
```

### IAM & Resource Manager

```bash
# List clouds
yc resource-manager cloud list

# List folders
yc resource-manager folder list

# Get folder details
yc resource-manager folder get <folder-id>

# List service accounts
yc iam service-account list

# Get service account details
yc iam service-account get <service-account-id>

# List access bindings
yc resource-manager folder list-access-bindings <folder-id>
```

## Output Formatting

```bash
# JSON output (best for jq processing)
yc compute instance list --format json

# YAML output
yc compute instance list --format yaml

# Table output (human-readable)
yc compute instance list --format table

# Get specific fields with jq
yc compute instance get <name> --format json | jq '.network_interfaces[0].primary_v4_address.one_to_one_nat.address'
```

## Debugging Workflows

### Check Kubernetes Cluster Health

```bash
# 1. Get cluster info
yc managed-kubernetes cluster get <cluster-name> --format json

# 2. Check node groups
yc managed-kubernetes node-group list --cluster-name <cluster-name>

# 3. Get credentials and use kubectl
yc managed-kubernetes cluster get-credentials <cluster-name> --external
kubectl get nodes
kubectl get pods -A
```

### Investigate Database Issues

```bash
# 1. Check cluster status
yc managed-postgresql cluster get <cluster-name> --format json

# 2. Check hosts status
yc managed-postgresql hosts list --cluster-name <cluster-name>

# 3. Check connection settings
yc managed-postgresql cluster get <cluster-name> --format json | jq '.config.postgresql_config'
```

### Network Connectivity Issues

```bash
# 1. Check VPC and subnets
yc vpc network list
yc vpc subnet list

# 2. Review security groups
yc vpc security-group list

# 3. Check addresses
yc vpc address list
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "Permission denied" | Wrong profile or folder | Check `yc config list`, verify folder-id |
| "Resource not found" | Wrong folder context | `yc config get folder-id`, switch if needed |
| "Command not found" | yc not installed | Install yc CLI, check PATH |
| Authentication issues | Token expired | `yc init` to re-authenticate |
| "Required permission" | Missing IAM role | Check `yc resource-manager folder list-access-bindings` |
| Wrong cloud/folder | Profile misconfigured | `yc config profile activate <correct-profile>` |

## Example Requests

| User Request | Action |
|--------------|--------|
| "Check VM status" | `yc compute instance list` or `yc compute instance get <name>` |
| "Is the K8s cluster healthy?" | `yc managed-kubernetes cluster get <name>`, then `kubectl get nodes` |
| "List all databases" | `yc managed-postgresql cluster list` (and mysql/redis) |
| "Check network config" | `yc vpc network list`, `yc vpc subnet list`, `yc vpc security-group list` |
| "Why can't I connect to DB?" | Check cluster status, hosts, security groups |
| "What's running in this folder?" | `yc compute instance list`, `yc managed-kubernetes cluster list`, etc. |

## Safety Checklist

Before running any command:

1. [ ] Is this a read-only command (list, get)?
2. [ ] Am I querying the correct folder (check `yc config list`)?
3. [ ] Does the command contain any forbidden verbs (create, delete, update, etc.)?
4. [ ] Am I using appropriate output format for the task?
