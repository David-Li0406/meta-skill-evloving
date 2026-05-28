---
name: asu-discover
description: "Smart discovery across ASU GitHub repositories. ONLY use when active repo is in ASU org (github.com/ASU). Use for finding ASU repos, code patterns, integrations, and SDKs. Domains: PeopleSoft, EDNA, DPL, Terraform, Salesforce, Auth, CI/CD. Use BEFORE starting ASU integration tasks."
allowed-tools: Bash(gh:*) Bash(./scripts/*) Read Glob Grep
context: fork
---

# ASU Domain Discovery Skill

Intelligent search and discovery across Arizona State University's GitHub organization. This skill provides domain-aware search with local caching to work within GitHub's rate limits.

**Prerequisite:** The active repository must be in the [ASU GitHub organization](https://github.com/ASU). ASU org repos integrate with ASU infrastructure (EDNA, DPL, PeopleSoft, Vault, etc.).

**Requirements:**
- `gh` CLI authenticated with access to ASU org (`gh auth login`)
- `yq` for YAML parsing (`brew install yq`)

**Note:** Run `./scripts/discover.sh index stats` to see current repository counts.

## Architecture

```
┌─────────────────────────────────────────┐
│          User Query                     │
│   "How do I integrate with EDNA?"       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│     Domain Detection & Expansion        │
│  Detected: edna                         │
│  Expanded: checkAccess, hasPermission   │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌───────────────┐      ┌───────────────────┐
│   Tier 1      │      │     Tier 2        │
│ Local SQLite  │      │  GitHub API       │
│ (instant)     │      │  (rate limited)   │
│               │      │                   │
│ FTS5 search   │      │ gh search code    │
│ All ASU repos │      │ 10 req/min        │
│ No rate limit │      │ 24h cache         │
└───────────────┘      └───────────────────┘
        │                       │
        └───────────┬───────────┘
                    ▼
           Merged Results
```

## Quick Reference

| Action | Description | Rate Limited |
|--------|-------------|--------------|
| `search` | Two-tier search (local + API) | API tier only |
| `repos` | Find repos by domain/prefix | No |
| `code` | Search code with caching | Yes (10/min) |
| `context` | Build integration context | Partial |
| `patterns` | Find integration patterns between systems | Yes |
| `pattern` | Show design pattern details (e.g., EEL) | No |
| `index` | Manage local index | No |

## How to Use

### Basic Discovery

```bash
cd {base_directory}

# Search with automatic domain detection
./scripts/discover.sh search --query "PeopleSoft integration"

# Search within a specific domain  
./scripts/discover.sh search --query "check access" --domain edna

# Find repos by team prefix
./scripts/discover.sh repos --prefix crm --limit 20

# Find repos by domain
./scripts/discover.sh repos --domain dpl
```

### Code Search (Rate Limited)

```bash
# Search code (checks cache first, rate limited)
./scripts/discover.sh code --query "checkAccess" --language typescript

# Use only cached results (no API calls)
./scripts/discover.sh code --query "DplClient" --cached-only

# Local-only search (no API at all)
./scripts/discover.sh search --query "terraform module" --local-only
```

### Building Integration Context

```bash
# Get full context for an integration task
./scripts/discover.sh context --query "sync employee data from PeopleSoft to DPL"

# Find patterns between two systems
./scripts/discover.sh patterns --source peoplesoft --target dpl
```

### Managing the Index

```bash
# Build full index (first time, ~30 seconds)
./scripts/discover.sh index build

# Refresh with recent changes
./scripts/discover.sh index refresh

# View statistics
./scripts/discover.sh index stats

# Re-classify domains
./scripts/discover.sh index classify
```

### Using Design Patterns

Design patterns are architectural templates with implementation guidance. They go beyond simple domain search by providing boilerplate code, best practices, and real-world examples.

```bash
# List available design patterns
./scripts/discover.sh pattern --list

# Show full pattern overview
./scripts/discover.sh pattern --name eel
./scripts/discover.sh pattern --name cicd
./scripts/discover.sh pattern --name terraform-modules
./scripts/discover.sh pattern --name vault
./scripts/discover.sh pattern --name observability

# Get specific pattern types
./scripts/discover.sh pattern --name eel --type publisher
./scripts/discover.sh pattern --name cicd --type jenkins
./scripts/discover.sh pattern --name terraform-modules --type database
./scripts/discover.sh pattern --name vault --type typescript
./scripts/discover.sh pattern --name observability --type datadog
./scripts/discover.sh pattern --name observability --type logging-lake
```

The `context` action auto-suggests relevant patterns when your query matches pattern triggers.

## Design Patterns

### EEL (Enterprise Event Lake)

ASU's real-time, Kafka-based event-driven architecture backbone. Use for decoupled, asynchronous communication between services.

| Aspect | Details |
|--------|---------|
| Platform | Confluent Cloud (Managed Apache Kafka) |
| Schema Format | Apache Avro |
| Delivery | At-least-once |
| Infrastructure | `ASU/evbr-enterprise-event-lake` |

**When to use:**
- Real-time data sync across systems
- Loose coupling (publishers don't know subscribers)
- Event-driven workflows and notifications
- Fan-out scenarios (one event, many consumers)

**Key Repositories:**

| Type | Repository | Description |
|------|------------|-------------|
| Boilerplate | `evbr-enterprise-event-lake-event-handler-boilerplate` | Start here for new handlers |
| Java Publisher | `edna` → `EELClient.java` | Identity/entitlement events |
| Python Publisher | `iden-identity-resolution-service-api` → `eel_client.py` | Lambda-based publishing |
| Python Subscriber | `sisfa-peoplesoft-financial-aid-module-event-listeners` | Financial Aid events |

**Pattern triggers:** `event-driven`, `real-time`, `publish`, `subscribe`, `kafka`, `confluent`, `avro`, `async`, `decoupled`, `fanout`

---

### CI/CD Pipelines

Centralized CI/CD patterns for Jenkins and GitHub Actions. The primary asset is the Jenkins Shared Library with 75+ reusable Groovy functions.

| Aspect | Details |
|--------|---------|
| Jenkins Library | `ASU/devops-jenkins-pipeline-library` (75+ functions) |
| GitHub Actions | `ASU/caas-image-library` (reusable workflows) |
| Pipeline Templates | `ASU/caas-pipeline-templates`, `ASU/ddt-mulesoft-base-application-template` |

**IMPORTANT:** MuleSoft is DEPRECATED. New integrations should use AWS tooling (API Gateway, Lambda, Step Functions, etc.).

**When to use:**
- Setting up Jenkins pipelines for new projects
- Integrating Vault secrets into CI/CD
- Adding security scanning (Bridgecrew, Docker image scanning)
- Terraform automation in pipelines
- ServiceNow change management integration

**Jenkins Shared Library Functions:**

| Category | Functions |
|----------|-----------|
| Terraform | `terraformInit`, `terraformPlan`, `terraformApply`, `pipelineTerraformSingleEnvironment` |
| Vault | `vaultLogin`, `getVaultSecret`, `getVaultToken`, `getVaultAppRoleToken` |
| Credentials | `setupMavenCredentials`, `setupNpmCredentials`, `setupPipCredentials` |
| Security | `bridgecrewScan`, `scanDockerImage`, `scanDockerImageWithInspector` |
| Notifications | `slackNotification`, `datadogDeployment` |
| ServiceNow | `servicenow_change`, `changeFreezeCheck` |

**Pattern triggers:** `jenkins`, `pipeline`, `shared-library`, `github actions`, `workflow_call`, `terraformApply`, `getVaultSecret`

---

### ASU Terraform Modules

Custom Terraform modules from `dco-terraform` hosted on JFrog Artifactory.

| Aspect | Details |
|--------|---------|
| Registry | `jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform` |
| Main Repo | `ASU/dco-terraform` |
| Examples | `ASU/dco-examples` |
| Requirements | Terraform >= 1.5.6, AWS Provider >= 5.82.0 |

**Module Source Pattern:**
```hcl
module "example" {
  source  = "jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform/<module>/aws"
  version = ">= 1.0"
}
```

**Module Categories:**

| Category | Key Modules |
|----------|-------------|
| Compute | `ec2-instance`, `ec2-windows`, `nutanix-vm` |
| Database | `aurora`, `aurora-mysql`, `aurora-postgres`, `rds-mssql`, `rds-oracle` |
| Networking | `vpc-core-v5`, `security-group`, `route53-host` |
| Kubernetes | `eks-oidc-provider`, `eks-pod-identity-role`, `eks-service-account-role` |
| Cloudflare | `cloudflare-tunnel`, `cloudflare-access-app`, `cloudflare-access-edna-group` |
| IAM | `iam-role-github-actions`, `iam-role-vault`, `github-oidc-provider` |
| Observability | `cloudwatch-logs-to-datadog`, `datadog-lambda-forwarder` |
| Standards | `product-tags` **(MANDATORY)** |

**Custom Providers:**
- `terraform-provider-edna` - EDNA resource management
- `terraform-provider-mandiantasm` - Security scanning

**Pattern triggers:** `terraform module`, `dco-terraform`, `product-tags`, `aurora`, `vpc-core`, `eks-oidc`

---

### HashiCorp Vault Secrets

Patterns for accessing secrets from Vault and syncing to AWS.

| Aspect | Details |
|--------|---------|
| CaaS Vault | `vault.caas-{env}.asu.edu` |
| Ops Vault | `ops-vault-prod.opsprod.asu.edu` |
| Infrastructure | `ASU/caas-caas-vault`, `ASU/authn-ops-vault` |

**When to use:**
- Reading secrets in TypeScript/Python/Java applications
- Syncing Vault secrets to AWS Secrets Manager
- Syncing Vault secrets to SSM Parameter Store
- Setting up Jenkins CI/CD with Vault integration
- Configuring AWS Lambda/EC2 to authenticate with Vault

**TypeScript/Node.js Pattern (AWS SDK - RECOMMENDED):**
```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-west-2' });
const secret = await client.send(
  new GetSecretValueCommand({ SecretId: 'my-secret' })
);
const data = JSON.parse(secret.SecretString!);
```

**Python Pattern (hvac):**
```python
import hvac
with open('/var/run/vault-token') as token:
    client = hvac.Client(url='https://ops-vault-prod.opsprod.asu.edu', token=token.read())
secret = client.secrets.kv.v1.read_secret(path='services/...')['data']
client.logout()
```

**Terraform Pattern (Vault → Secrets Manager):**
```hcl
data "vault_generic_secret" "api_key" {
  path = "secret/services/dco/jenkins/..."
}
resource "aws_secretsmanager_secret_version" "api_key" {
  secret_id     = aws_secretsmanager_secret.api_key.id
  secret_string = data.vault_generic_secret.api_key.data["api_key"]
}
```

**Authentication Methods:**
- AppRole - Jenkins CI/CD (30 min TTL)
- AWS IAM - EC2/Lambda workloads
- Kubernetes - EKS pods
- OIDC - Human users (via Cognito)

**Secret Path Convention:**
```
secret/services/{org}/{team}/{app}/{environment}/{component}
```

**Pattern triggers:** `vault`, `hvac`, `secret`, `getVaultSecret`, `secretsmanager`, `approle`

---

### Observability Stack

ASU's observability stack for monitoring, logging, and tracing. Primary tools: Datadog (APM/RUM), Cribl/Logging Lake (logs), CloudWatch (AWS metrics), OpenTelemetry (K8s).

| Aspect | Details |
|--------|---------|
| APM | Datadog (dd-trace, ddtrace, dd-java-agent) |
| RUM | Datadog Browser RUM (@datadog/browser-rum) |
| Logs | Cribl Stream → S3 → OpenSearch (Logging Lake) |
| Metrics | CloudWatch, Datadog |
| Tracing | Datadog APM, OpenTelemetry |

**IMPORTANT:** Splunk is DEPRECATED. All new implementations MUST use Logging Lake.

**When to use:**
- Setting up APM for TypeScript/Python/Java services
- Adding Real User Monitoring (RUM) to React apps
- Configuring log pipelines and aggregation
- Setting up CloudWatch alarms and routing
- Migrating from Splunk to Logging Lake

**Datadog APM (TypeScript):**
```typescript
import tracer from 'dd-trace';
tracer.init({ service: 'my-service' });
```

**Datadog RUM (React):**
```typescript
import { datadogRum } from '@datadog/browser-rum';
datadogRum.init({
  applicationId: 'xxx',
  clientToken: 'xxx',
  site: 'datadoghq.com',
  service: 'my-app',
  env: process.env.NODE_ENV
});
```

**Key Repositories:**

| Type | Repository | Description |
|------|------------|-------------|
| Logging Platform | `eli5-observability-pipeline-platform` | Cribl Stream on EKS |
| Kafka Bridge | `eli5-kafkabahn` | Kafka to logging pipeline |
| OSIS Pipelines | `eli5-osis-pipelines` | OpenSearch Ingestion Service |

**Terraform Modules:**
- `cloudwatch-logs-to-datadog` - CloudWatch to Datadog
- `cloudwatch-logs-to-log-lake` - CloudWatch to S3 data lake
- `datadog-lambda-forwarder` - Datadog Lambda forwarder
- `datadog-logs-firehose-forwarder` - Datadog Kinesis Firehose

**Splunk Migration Path:**
1. Identify current Splunk sources
2. Configure Cribl Stream inputs
3. Update Terraform to use cloudwatch-logs-to-log-lake
4. Migrate dashboards to OpenSearch
5. Decommission Splunk forwarders

**Pattern triggers:** `datadog`, `logging`, `cribl`, `cloudwatch`, `otel`, `opentelemetry`, `metrics`, `monitoring`, `apm`, `rum`, `tracing`, `observability`, `splunk`

## Domains

| Domain | Triggers | Team Prefixes | Key Repos |
|--------|----------|---------------|-----------|
| `peoplesoft` | ps, psft, integration broker, ib | ps, aiml | aiml-peoplesoft-ib |
| `edna` | edna, entitlement, checkAccess, authz | edna, eadv | edna-sdk, edna-*-client |
| `dpl` | dpl, data potluck, principal, emplid | dpl | dpl-python-sdk |
| `serviceauth` | serviceauth, jwt, token | authn | serviceauth-client |
| `auth` | authn, sso, saml, oidc | authn, auth | auth-service |
| `identity` | identity, unity, unityid | iden, unity | unity-identity |
| `salesforce` | salesforce, crm, sfdc, apex | crm, sf | salesforce-integrations |
| `terraform` | terraform, tf, iac, hcl | tf, infra, dco, ceng | dco-terraform, dco-examples |
| `cicd` | cicd, pipeline, workflow, actions, jenkins | cicd, devops, dco, caas, dot | devops-jenkins-pipeline-library |
| `cloudflare` | cloudflare, cf, worker | cf, ewp | cloudflare-workers |
| `ml` | ml, ai, machine learning, model | aiml | ml-models |
| `eel` | eel, event lake, kafka, confluent, avro | evbr | evbr-enterprise-event-lake |
| `logging` | logging, observability, cribl, kafkabahn | eli5 | eli5-kafkabahn, eli5-observability-pipeline-platform |
| `vault` | vault, hvac, secret, hashicorp | authn, caas | caas-caas-vault |
| `devops` | devops, jenkins, pipeline, shared library | devops, dco | devops-jenkins-pipeline-library |
| `mulesoft` | mulesoft, mule, anypoint, esb | ddt | ddt-mulesoft-base-application-template | **DEPRECATED** - Use AWS tooling |
| `feature-flags` | feature flag, toggle | appss | appss-enterprise-feature-flags |

## Team Prefixes

Based on ASU org analysis:

| Prefix | Count | Domain |
|--------|-------|--------|
| crm | 66 | salesforce |
| eadv | 38 | edna |
| authn | 15 | auth |
| aiml | 12 | ml |
| edna | 11 | edna |
| iden | 10 | identity |
| eli5 | 9 | logging |
| evbr | 2 | eel |
| tf | - | terraform |
| infra | - | infrastructure |

## Rate Limiting

GitHub code search is limited to **10 requests per minute**. This skill handles rate limits by:

1. **Local Index First** - Searches SQLite FTS5 index (instant, no limit)
2. **24h Caching** - Caches code search results for 24 hours
3. **Rate Tracking** - Waits 6 seconds between API calls
4. **`--cached-only`** - Option to skip API entirely
5. **`--local-only`** - Search only local index

## Common Options

| Option | Description |
|--------|-------------|
| `--query QUERY` | Search query (natural language or keywords) |
| `--domain DOMAIN` | Filter to specific domain |
| `--prefix PREFIX` | Filter by team prefix |
| `--language LANG` | Filter by programming language |
| `--limit N` | Maximum results (default: 30) |
| `--no-expand` | Disable keyword expansion |
| `--local-only` | Only search local index |
| `--cached-only` | Only use cached API results |
| `--json` | JSON output format |
| `--verbose` | Show debug information |

## Examples

### Finding EDNA Integration Patterns

```bash
# Step 1: Find relevant repos
./scripts/discover.sh repos --domain edna

# Step 2: Search for checkAccess usage
./scripts/discover.sh code --query "checkAccess" --language typescript

# Step 3: Get full context
./scripts/discover.sh context --query "implement EDNA authorization in Node.js API"
```

### Discovering PeopleSoft Integrations

```bash
# Find all PS-related repos
./scripts/discover.sh repos --prefix ps

# Search for Integration Broker code
./scripts/discover.sh search --query "ServiceOperation IBRequest"

# Find PS-to-DPL integration patterns
./scripts/discover.sh patterns --source peoplesoft --target dpl
```

### Working with Terraform Modules

```bash
# Find terraform repos
./scripts/discover.sh repos --prefix tf
./scripts/discover.sh repos --domain terraform

# Search for specific module patterns
./scripts/discover.sh code --query "aws_lambda_function" --language HCL
```

## Files

```
skills/asu-discover/
├── SKILL.md                 # This file
├── config/
│   └── domains.yaml         # Domain taxonomy and synonyms
├── data/
│   ├── .gitignore           # Ignore generated files
│   └── asu-repos.db         # SQLite index (generated)
└── scripts/
    ├── lib/
    │   └── db.sh            # SQLite helper functions
    └── discover.sh          # Main script
```

## Troubleshooting

### "Index not found" 
The index will auto-build on first use. To manually build:
```bash
./scripts/discover.sh index build
```

### Rate limit errors
Use `--cached-only` or `--local-only` to avoid API calls:
```bash
./scripts/discover.sh search --query "..." --local-only
```

### No results
Try broader terms or check domain spelling:
```bash
./scripts/discover.sh expand --query "your query"  # Debug expansion
```

---

**Note:** This skill is ONLY useful when working in a repository within the [ASU GitHub organization](https://github.com/ASU). ASU org repos integrate with ASU infrastructure. For general GitHub operations, use the `github-ops` skill instead.
