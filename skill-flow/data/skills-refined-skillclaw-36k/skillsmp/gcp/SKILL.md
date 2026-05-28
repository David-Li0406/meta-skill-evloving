---
name: gcp
description: Query Google Cloud Platform infrastructure using gcloud CLI for debugging and understanding current setup. READ-ONLY - never modify infrastructure state. Always ask user approval before any state-changing operations.
license: MIT
compatibility: opencode
---

# Google Cloud Platform CLI Skill

Query GCP infrastructure for debugging and understanding the current setup. This skill is strictly READ-ONLY.

## CRITICAL RULES

### READ-ONLY BY DEFAULT

**NEVER execute commands that modify infrastructure state without explicit user approval.**

Allowed (read-only):
- `gcloud <service> <resource> list`
- `gcloud <service> <resource> describe`
- `gcloud <service> <resource> get-iam-policy`
- `gcloud config list`
- `gsutil ls`, `gsutil stat`
- Any command with `--format` for output formatting

**FORBIDDEN (state-changing):**
- `create`, `delete`, `update`, `set`, `add`, `remove`
- `start`, `stop`, `reset`, `suspend`, `resume`
- `attach`, `detach`
- `deploy`, `apply`
- `gsutil cp`, `gsutil rm`, `gsutil mv`
- `gcloud config set` (except project switching for read access)
- Any command that modifies resources

### Approval Request Format

Before any state-changing operation (if ever needed), ask:

```
I need to run a state-changing GCP command:
  Command: gcloud compute instances stop my-instance --zone us-central1-a
  Impact: Will stop the VM instance
  
Do you approve? (yes/no)
```

### Before Any Query

1. Check current config: `gcloud config list`
2. Verify you're querying the correct project (dev/prod)
3. Use `--format json` or `--format yaml` for parseable output

## Quick Reference

### Configuration

```bash
# Show current config
gcloud config list

# List available configurations
gcloud config configurations list

# Switch configuration (safe - just changes read context)
gcloud config configurations activate <config-name>

# Get current project
gcloud config get-value project

# List accessible projects
gcloud projects list

# Get project details
gcloud projects describe <project-id>
```

### Compute Engine (VMs)

```bash
# List all VMs
gcloud compute instances list

# Get VM details
gcloud compute instances describe <instance-name> --zone <zone>

# List disks
gcloud compute disks list

# Get disk details
gcloud compute disks describe <disk-name> --zone <zone>

# List images
gcloud compute images list --project <project-id>

# List snapshots
gcloud compute snapshots list

# List instance templates
gcloud compute instance-templates list

# List instance groups
gcloud compute instance-groups list
gcloud compute instance-groups managed list

# List machine types
gcloud compute machine-types list --zones <zone>
```

### Google Kubernetes Engine (GKE)

```bash
# List clusters
gcloud container clusters list

# Get cluster details
gcloud container clusters describe <cluster-name> --zone <zone>
# or for regional clusters
gcloud container clusters describe <cluster-name> --region <region>

# List node pools
gcloud container node-pools list --cluster <cluster-name> --zone <zone>

# Get node pool details
gcloud container node-pools describe <pool-name> --cluster <cluster-name> --zone <zone>

# Get cluster credentials (for kubectl access)
gcloud container clusters get-credentials <cluster-name> --zone <zone>

# List GKE operations (useful for debugging)
gcloud container operations list
```

### Cloud SQL (Databases)

```bash
# List instances
gcloud sql instances list

# Get instance details
gcloud sql instances describe <instance-name>

# List databases in instance
gcloud sql databases list --instance <instance-name>

# List users
gcloud sql users list --instance <instance-name>

# List backups
gcloud sql backups list --instance <instance-name>

# List operations
gcloud sql operations list --instance <instance-name>
```

### Cloud Memorystore (Redis/Memcached)

```bash
# Redis instances
gcloud redis instances list --region <region>
gcloud redis instances describe <instance-name> --region <region>

# Memcached instances
gcloud memcache instances list --region <region>
gcloud memcache instances describe <instance-name> --region <region>
```

### Networking (VPC)

```bash
# List VPC networks
gcloud compute networks list

# Get network details
gcloud compute networks describe <network-name>

# List subnets
gcloud compute networks subnets list
gcloud compute networks subnets describe <subnet-name> --region <region>

# List firewall rules
gcloud compute firewall-rules list
gcloud compute firewall-rules describe <rule-name>

# List routes
gcloud compute routes list

# List external IPs
gcloud compute addresses list

# List routers (Cloud Router)
gcloud compute routers list
gcloud compute routers describe <router-name> --region <region>

# List NAT configs
gcloud compute routers nats list --router <router-name> --region <region>

# List VPN tunnels
gcloud compute vpn-tunnels list

# List interconnects
gcloud compute interconnects list
```

### Load Balancing

```bash
# List forwarding rules
gcloud compute forwarding-rules list

# List target pools
gcloud compute target-pools list

# List backend services
gcloud compute backend-services list

# Get backend service details
gcloud compute backend-services describe <service-name> --global
# or regional
gcloud compute backend-services describe <service-name> --region <region>

# List URL maps
gcloud compute url-maps list

# List target HTTP(S) proxies
gcloud compute target-http-proxies list
gcloud compute target-https-proxies list

# List health checks
gcloud compute health-checks list

# List SSL certificates
gcloud compute ssl-certificates list

# List NEGs (Network Endpoint Groups)
gcloud compute network-endpoint-groups list
```

### Container Registry / Artifact Registry

```bash
# List Artifact Registry repositories
gcloud artifacts repositories list

# List images in repository
gcloud artifacts docker images list <location>-docker.pkg.dev/<project>/<repo>

# List tags for image
gcloud artifacts docker tags list <location>-docker.pkg.dev/<project>/<repo>/<image>

# Container Registry (legacy)
gcloud container images list --repository gcr.io/<project>
gcloud container images list-tags gcr.io/<project>/<image>
```

### Cloud Run

```bash
# List services
gcloud run services list

# Get service details
gcloud run services describe <service-name> --region <region>

# List revisions
gcloud run revisions list --service <service-name> --region <region>

# List jobs
gcloud run jobs list
gcloud run jobs describe <job-name> --region <region>
```

### Cloud Functions

```bash
# List functions (Gen 1)
gcloud functions list

# Get function details
gcloud functions describe <function-name> --region <region>

# List functions (Gen 2)
gcloud functions list --gen2
```

### IAM & Service Accounts

```bash
# List service accounts
gcloud iam service-accounts list

# Get service account details
gcloud iam service-accounts describe <sa-email>

# List keys for service account
gcloud iam service-accounts keys list --iam-account <sa-email>

# Get IAM policy for project
gcloud projects get-iam-policy <project-id>

# Get IAM policy for specific resource
gcloud <service> <resource> get-iam-policy <resource-name>

# List custom roles
gcloud iam roles list --project <project-id>

# List predefined roles
gcloud iam roles list
```

### Cloud Storage (GCS)

```bash
# List buckets
gsutil ls

# List bucket contents
gsutil ls gs://<bucket-name>/
gsutil ls -l gs://<bucket-name>/  # with details

# Get bucket metadata
gsutil stat gs://<bucket-name>/

# Get object metadata
gsutil stat gs://<bucket-name>/<object-path>

# List bucket IAM
gsutil iam get gs://<bucket-name>

# Get bucket lifecycle
gsutil lifecycle get gs://<bucket-name>

# Using gcloud (alternative)
gcloud storage buckets list
gcloud storage buckets describe gs://<bucket-name>
```

### Cloud Logging

```bash
# Read logs
gcloud logging read "resource.type=gce_instance" --limit 100

# Read logs with filter
gcloud logging read "severity>=ERROR" --limit 50

# Read logs for specific resource
gcloud logging read "resource.type=k8s_container AND resource.labels.cluster_name=<cluster>" --limit 100

# List log entries for a service
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=<service>" --limit 50

# List sinks
gcloud logging sinks list

# List metrics
gcloud logging metrics list
```

### Cloud Monitoring

```bash
# List alerting policies
gcloud alpha monitoring policies list

# Describe alerting policy
gcloud alpha monitoring policies describe <policy-id>

# List notification channels
gcloud alpha monitoring channels list

# List uptime checks
gcloud alpha monitoring uptime list-configs
```

### Pub/Sub

```bash
# List topics
gcloud pubsub topics list

# Get topic details
gcloud pubsub topics describe <topic-name>

# List subscriptions
gcloud pubsub subscriptions list

# Get subscription details
gcloud pubsub subscriptions describe <subscription-name>

# List snapshots
gcloud pubsub snapshots list
```

### Cloud Scheduler

```bash
# List jobs
gcloud scheduler jobs list --location <location>

# Get job details
gcloud scheduler jobs describe <job-name> --location <location>
```

### Secret Manager

```bash
# List secrets
gcloud secrets list

# Get secret metadata (NOT the value)
gcloud secrets describe <secret-name>

# List secret versions
gcloud secrets versions list <secret-name>

# Access secret value (use carefully, logs may capture)
gcloud secrets versions access latest --secret <secret-name>
```

### Cloud DNS

```bash
# List managed zones
gcloud dns managed-zones list

# Get zone details
gcloud dns managed-zones describe <zone-name>

# List DNS records
gcloud dns record-sets list --zone <zone-name>
```

### Certificate Manager

```bash
# List certificates
gcloud certificate-manager certificates list

# Get certificate details
gcloud certificate-manager certificates describe <cert-name>

# List certificate maps
gcloud certificate-manager maps list
```

### Cloud Armor (Security Policies)

```bash
# List security policies
gcloud compute security-policies list

# Get policy details
gcloud compute security-policies describe <policy-name>

# List rules in policy
gcloud compute security-policies rules list <policy-name>
```

## Debugging Workflows

### Check GKE Cluster Health

```bash
# 1. Get cluster info
gcloud container clusters describe <cluster-name> --zone <zone> --format json

# 2. Check node pools
gcloud container node-pools list --cluster <cluster-name> --zone <zone>

# 3. Get credentials and use kubectl
gcloud container clusters get-credentials <cluster-name> --zone <zone>
kubectl get nodes
kubectl get pods -A

# 4. Check recent operations
gcloud container operations list --filter "targetLink~<cluster-name>"
```

### Investigate Cloud SQL Issues

```bash
# 1. Check instance status
gcloud sql instances describe <instance-name> --format json

# 2. Check recent operations
gcloud sql operations list --instance <instance-name> --limit 10

# 3. Check databases
gcloud sql databases list --instance <instance-name>

# 4. Check connection settings
gcloud sql instances describe <instance-name> --format="value(connectionName)"
```

### Network Connectivity Issues

```bash
# 1. Check VPC and subnets
gcloud compute networks list
gcloud compute networks subnets list --network <network-name>

# 2. Review firewall rules
gcloud compute firewall-rules list --filter="network~<network-name>"

# 3. Check external IPs
gcloud compute addresses list

# 4. Check routes
gcloud compute routes list --filter="network~<network-name>"

# 5. Check Cloud NAT (if used)
gcloud compute routers list
gcloud compute routers nats list --router <router-name> --region <region>
```

### Check Cloud Run Service

```bash
# 1. Get service status
gcloud run services describe <service-name> --region <region> --format json

# 2. List revisions
gcloud run revisions list --service <service-name> --region <region>

# 3. Check logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=<service-name>" --limit 100
```

## Output Formatting

Always use structured output for parsing:

```bash
# JSON output (best for jq processing)
gcloud compute instances list --format json

# YAML output
gcloud compute instances list --format yaml

# Table output (human-readable)
gcloud compute instances list --format="table(name,zone,status)"

# Get specific fields
gcloud compute instances list --format="value(name,networkInterfaces[0].accessConfigs[0].natIP)"

# Custom formatting
gcloud compute instances list --format="table[box](name,zone.basename(),status,networkInterfaces[0].networkIP)"

# Filter results
gcloud compute instances list --filter="status=RUNNING"
gcloud compute instances list --filter="zone~us-central"

# Combine filter and format with jq
gcloud compute instances describe <name> --zone <zone> --format json | jq '.networkInterfaces[0].accessConfigs[0].natIP'
```

## Safety Checklist

Before running any command:

1. [ ] Is this a read-only command (list, describe, get)?
2. [ ] Am I querying the correct project (check `gcloud config list`)?
3. [ ] Does the command contain any forbidden verbs (create, delete, update, deploy, etc.)?
4. [ ] Am I using appropriate output format for the task?
5. [ ] For gsutil, am I only using `ls` and `stat` (not cp, rm, mv)?

## Troubleshooting

### "Permission denied" / "Required permission"
- Check current project: `gcloud config get-value project`
- Verify account has required read permissions: `gcloud auth list`
- Check IAM bindings: `gcloud projects get-iam-policy <project-id>`

### "Resource not found"
- Verify correct project: `gcloud config get-value project`
- Check resource exists: `gcloud <service> <resource> list`
- Verify zone/region is correct

### "Command not found"
- Ensure gcloud is installed: `gcloud version`
- Update gcloud components: `gcloud components update`

### Authentication Issues
- Check active account: `gcloud auth list`
- Re-authenticate: `gcloud auth login` (interactive)
- For service accounts: `gcloud auth activate-service-account --key-file <key.json>`
