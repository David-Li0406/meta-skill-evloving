---
name: temporal-cloud
description: Temporal Cloud managed service documentation. Use for deploying workflows to Temporal Cloud, managing namespaces, certificates, API keys, users, billing, and using the tcld CLI.
---

# Temporal Cloud Skill

Comprehensive documentation for Temporal Cloud, the managed Temporal service. This skill covers deployment, namespace management, security configuration, API keys, and the tcld CLI.

## When to Use This Skill

This skill should be triggered when:
- Connecting applications to Temporal Cloud
- Managing Temporal Cloud namespaces
- Configuring mTLS certificates or API keys
- Using tcld CLI commands
- Setting up Terraform for Temporal Cloud
- Configuring private connectivity (AWS PrivateLink, GCP PSC)
- Managing users and billing

## Quick Reference

### Connect to Temporal Cloud (TypeScript)

```typescript
import { Connection, Client } from '@temporalio/client';

const connection = await Connection.connect({
  address: '<namespace>.<account_id>.tmprl.cloud:7233',
  tls: {
    clientCertPair: {
      crt: fs.readFileSync('/path/to/client.pem'),
      key: fs.readFileSync('/path/to/client.key'),
    },
  },
});

const client = new Client({
  connection,
  namespace: '<namespace>.<account_id>',
});
```

### Connect with API Key (TypeScript)

```typescript
const connection = await Connection.connect({
  address: '<region>.<cloud_provider>.api.temporal.io:7233',
  apiKey: process.env.TEMPORAL_API_KEY,
  tls: true,
});

const client = new Client({
  connection,
  namespace: '<namespace_id>.<account_id>',
});
```

### Connect to Temporal Cloud (Go)

```go
clientOptions := client.Options{
    HostPort:  "<namespace>.<account_id>.tmprl.cloud:7233",
    Namespace: "<namespace>.<account_id>",
    ConnectionOptions: client.ConnectionOptions{
        TLS: &tls.Config{
            Certificates: []tls.Certificate{cert},
        },
    },
}
c, err := client.Dial(clientOptions)
```

### Worker Setup (TypeScript)

```typescript
import { NativeConnection, Worker } from '@temporalio/worker';
import * as activities from './activities';

async function run() {
  const connection = await NativeConnection.connect({
    address: 'localhost:7233',
  });

  const worker = await Worker.create({
    connection,
    namespace: 'default',
    taskQueue: 'hello-world',
    workflowsPath: require.resolve('./workflows'),
    activities,
  });

  await worker.run();
}
```

### tcld CLI Commands

```bash
# Install tcld
brew install temporalio/brew/tcld

# Login to Temporal Cloud
tcld login

# Create namespace
tcld namespace create --namespace <name> --region aws-us-east-1

# Create API key
tcld apikey create --name "my-api-key" --duration 90d

# Create connectivity rule (AWS PrivateLink)
tcld connectivity-rule create \
  --connectivity-type private \
  --connection-id "vpce-abcde" \
  --region "aws-us-east-1"

# List namespaces
tcld namespace list

# Get namespace details
tcld namespace get -n "<namespace>.<account_id>"
```

### CLI Profile Configuration

```bash
# Configure local development profile
temporal config set --prop address --value "localhost:7233"
temporal config set --prop namespace --value "default"

# Configure Temporal Cloud profile with API key
temporal --profile prod config set --prop address \
  --value "<region>.<cloud_provider>.api.temporal.io:7233"
temporal --profile prod config set --prop namespace \
  --value "<namespace_id>.<account_id>"
temporal --profile prod config set --prop api_key \
  --value "<your-api-key>"
```

### Terraform Provider Setup

```hcl
terraform {
  required_providers {
    temporalcloud = {
      source = "temporalio/temporalcloud"
    }
  }
}

provider "temporalcloud" {
  # Uses TEMPORAL_CLOUD_API_KEY environment variable
}

resource "temporalcloud_namespace" "example" {
  name               = "my-namespace"
  regions            = ["aws-us-east-1"]
  accepted_client_ca = base64encode(file("ca.pem"))
  retention_days     = 14
}
```

### Private Connectivity (AWS PrivateLink)

```bash
# Create private connectivity rule
tcld connectivity-rule create \
  --connectivity-type private \
  --connection-id "vpce-0123456789abcdef" \
  --region "aws-us-east-1"

# Assign to namespace
tcld namespace set-connectivity-rules \
  --namespace "my-namespace.abc123" \
  --connectivity-rule-ids "rule-id-1"

# Environment variables for private endpoint
export TEMPORAL_ADDRESS=vpce-0123456789abcdef-abc.us-east-1.vpce.amazonaws.com:7233
export TEMPORAL_NAMESPACE=my-namespace.my-account
export TEMPORAL_TLS_CERT=path/to/cert.pem
export TEMPORAL_TLS_KEY=path/to/cert.key
export TEMPORAL_TLS_SERVER_NAME=my-namespace.my-account.tmprl.cloud
```

### Certificate Configuration (TOML)

```toml
# ~/.config/temporalio/temporal.toml

[profile.default]
address = "localhost:7233"
namespace = "default"

[profile.prod]
address = "<namespace>.<account_id>.tmprl.cloud:7233"
namespace = "<namespace>.<account_id>"

[profile.prod.tls]
client_cert_path = "/path/to/client.pem"
client_key_path = "/path/to/client.key"
```

## Key Concepts

### Namespaces
- Isolated unit of work in Temporal Cloud
- Each has its own Workflow history, visibility, and security settings
- Default retention: 14 days (configurable)

### Authentication Methods
1. **mTLS Certificates** - Client certificates for secure connections
2. **API Keys** - Simpler alternative for authentication
3. **Both** - Can be used together

### Regions
Temporal Cloud is available in multiple AWS and GCP regions. Choose based on latency requirements and data residency.

### Private Connectivity
- **AWS PrivateLink** - Private connection via VPC endpoints
- **GCP Private Service Connect** - Private connection for GCP workloads

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **getting_started.md** - Setup and hello world tutorial
- **namespaces.md** - Namespace configuration and management
- **certificates.md** - TLS/mTLS certificate setup
- **api_keys.md** - API key management and Terraform
- **users.md** - User and account management
- **tcld_cli.md** - CLI reference and connectivity rules
- **other.md** - Additional documentation topics

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
1. Start with `getting_started.md` for initial setup
2. Install Temporal CLI: `brew install temporal`
3. Start local dev server: `temporal server start-dev`
4. Create your first Workflow and Activity

### For Temporal Cloud Setup
1. Create account at cloud.temporal.io
2. Create namespace via tcld or UI
3. Generate certificates or API keys
4. Configure your application connection
5. Deploy your Worker

### For Production
1. Use mTLS or API keys for authentication
2. Configure monitoring with Prometheus metrics
3. Set up private connectivity if needed
4. Use Terraform for infrastructure as code

## Common Patterns

### Activity with Timeout

```typescript
const { greet } = proxyActivities<typeof activities>({
  startToCloseTimeout: '1 minute',
  retry: {
    maximumAttempts: 3,
  },
});

export async function myWorkflow(name: string): Promise<string> {
  return await greet(name);
}
```

### Signal Handling

```typescript
import { defineSignal, setHandler } from '@temporalio/workflow';

const mySignal = defineSignal<[string]>('mySignal');

export async function myWorkflow(): Promise<void> {
  let value = '';
  setHandler(mySignal, (newValue) => {
    value = newValue;
  });
  // workflow logic
}
```

## Resources

### references/
Organized documentation extracted from official Temporal Cloud docs. Contains:
- Detailed configuration examples
- Code samples in multiple languages
- CLI command references
- Best practices

### External Resources
- [Temporal Cloud Console](https://cloud.temporal.io)
- [Temporal Documentation](https://docs.temporal.io)
- [Temporal TypeScript SDK](https://typescript.temporal.io)
- [Terraform Provider](https://registry.terraform.io/providers/temporalio/temporalcloud)

## Notes

- This skill was generated from official Temporal Cloud documentation
- Reference files preserve structure and examples from source docs
- Code examples include TypeScript, Go, Java, and Python
- Quick reference patterns extracted from common usage examples

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper: `skill-seekers scrape --config configs/temporal-cloud.json`
2. The skill will be rebuilt with the latest information
