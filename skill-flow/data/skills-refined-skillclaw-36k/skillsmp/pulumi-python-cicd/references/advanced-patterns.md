# Advanced Patterns

## Policy as Code (CrossGuard)

### Basic Policy Pack

```python
# policy/__main__.py
from pulumi_policy import (
    EnforcementLevel,
    PolicyPack,
    ResourceValidationArgs,
    ResourceValidationPolicy,
)

def s3_no_public_read(args: ResourceValidationArgs, report_violation):
    if args.resource_type == "aws:s3/bucket:Bucket":
        acl = args.props.get("acl")
        if acl == "public-read" or acl == "public-read-write":
            report_violation("S3 buckets must not have public read access")

PolicyPack(
    name="aws-security",
    enforcement_level=EnforcementLevel.MANDATORY,
    policies=[
        ResourceValidationPolicy(
            name="s3-no-public-read",
            description="Prohibits public read access on S3 buckets",
            validate=s3_no_public_read,
        ),
    ],
)
```

### Cost Control Policy

```python
def limit_instance_size(args: ResourceValidationArgs, report_violation):
    if args.resource_type == "aws:ec2/instance:Instance":
        allowed = ["t3.micro", "t3.small", "t3.medium"]
        instance_type = args.props.get("instanceType")
        if instance_type not in allowed:
            report_violation(f"Instance type {instance_type} not allowed. Use: {allowed}")
```

### Run Policies

```bash
pulumi preview --policy-pack ./policy
pulumi up --policy-pack ./policy
```

## Pulumi ESC (Environments, Secrets, Configuration)

### ESC Environment File

```yaml
# environments/aws-dev.yaml
values:
  aws:
    region: us-west-2
    accountId: "123456789012"
  app:
    environment: development
    logLevel: debug
  pulumiConfig:
    aws:region: ${aws.region}
    instanceType: t3.micro

  environmentVariables:
    AWS_REGION: ${aws.region}
    APP_ENV: ${app.environment}
```

### Using ESC in Pulumi.yaml

```yaml
name: my-project
runtime: python
environment:
  - aws-dev  # Reference ESC environment
```

### ESC with OIDC (GitHub Actions)

```yaml
# environments/aws-prod.yaml
values:
  aws:
    login:
      fn::open::aws-login:
        oidc:
          roleArn: arn:aws:iam::123456789012:role/pulumi-deploy
          sessionName: pulumi-github-actions
          duration: 1h
  
  environmentVariables:
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
```

## OIDC Integration

### GitHub Actions with AWS OIDC

```yaml
# .github/workflows/pulumi.yml
name: Pulumi Deploy
on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-role
          aws-region: us-west-2
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - run: pip install -r requirements.txt
      
      - uses: pulumi/actions@v5
        with:
          command: up
          stack-name: org/project/prod
        env:
          PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
```

### AWS OIDC Provider Setup (Pulumi)

```python
from pulumi_aws import iam
import json

github_oidc = iam.OpenIdConnectProvider("github-oidc",
    url="https://token.actions.githubusercontent.com",
    client_id_lists=["sts.amazonaws.com"],
    thumbprint_lists=["6938fd4d98bab03faadb97b34396831e3780aea1"])

deploy_role = iam.Role("github-deploy-role",
    assume_role_policy=pulumi.Output.all(github_oidc.arn).apply(lambda args: json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Federated": args[0]},
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:*"
                }
            }
        }]
    })))

iam.RolePolicyAttachment("deploy-policy",
    role=deploy_role.name,
    policy_arn="arn:aws:iam::aws:policy/AdministratorAccess")
```

## Dynamic Providers

### External API Integration

```python
from pulumi.dynamic import Resource, ResourceProvider, CreateResult, UpdateResult
import requests

class GitHubRepoProvider(ResourceProvider):
    def create(self, props):
        resp = requests.post(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {props['token']}"},
            json={"name": props["name"], "private": props.get("private", True)}
        )
        repo = resp.json()
        return CreateResult(id_=str(repo["id"]), outs={
            "name": repo["name"],
            "url": repo["html_url"],
            "clone_url": repo["clone_url"],
        })
    
    def delete(self, id, props):
        requests.delete(
            f"https://api.github.com/repos/{props['owner']}/{props['name']}",
            headers={"Authorization": f"token {props['token']}"}
        )

class GitHubRepo(Resource):
    name: pulumi.Output[str]
    url: pulumi.Output[str]
    
    def __init__(self, name, token, private=True, opts=None):
        super().__init__(
            GitHubRepoProvider(),
            name,
            {"token": token, "name": name, "private": private, "url": None},
            opts
        )
```

## State Management

### Backend Configuration

```bash
# Pulumi Cloud (default)
pulumi login

# Self-managed S3
pulumi login s3://my-state-bucket

# Self-managed Azure Blob
pulumi login azblob://my-container

# Self-managed GCS
pulumi login gs://my-bucket

# Local filesystem
pulumi login --local
```

### S3 Backend with Encryption

```bash
export PULUMI_BACKEND_URL="s3://my-state-bucket?region=us-west-2&awssdk=v2"
export PULUMI_CONFIG_PASSPHRASE="your-encryption-passphrase"
```

### State Import/Export

```bash
# Export state
pulumi stack export --file state.json

# Import state
pulumi stack import --file state.json

# Import existing resource
pulumi import aws:s3/bucket:Bucket my-bucket my-existing-bucket-name
```

## Secrets Management

### Secret Providers

```yaml
# Pulumi.yaml - Use AWS KMS
encryptionsalt: v1:abc123:...
secretsprovider: awskms://alias/pulumi-secrets?region=us-west-2

# Use Azure Key Vault
secretsprovider: azurekeyvault://my-vault.vault.azure.net/keys/pulumi-key

# Use GCP KMS
secretsprovider: gcpkms://projects/my-project/locations/us/keyRings/pulumi/cryptoKeys/key

# Use HashiCorp Vault
secretsprovider: hashivault://transit/keys/pulumi
```

### Programmatic Secret Handling

```python
# Create secret output
db_password = pulumi.Output.secret("sensitive-value")

# Convert existing output to secret
bucket_name_secret = bucket.name.apply(lambda n: pulumi.Output.secret(n))

# Access secret in apply (use carefully)
db_password.apply(lambda p: print(f"Password length: {len(p)}"))
```

## Resource Options

### Advanced Dependency Control

```python
from pulumi import ResourceOptions

# Explicit dependencies
bucket = s3.Bucket("data")
lambda_fn = lambda_.Function("processor",
    opts=ResourceOptions(depends_on=[bucket]))

# Protect from deletion
database = rds.Instance("prod-db",
    opts=ResourceOptions(protect=True))

# Ignore changes to specific properties
asg = autoscaling.Group("asg",
    desired_capacity=3,
    opts=ResourceOptions(ignore_changes=["desired_capacity"]))

# Replace before delete
instance = ec2.Instance("web",
    opts=ResourceOptions(delete_before_replace=True))

# Custom timeouts
cluster = ecs.Cluster("main",
    opts=ResourceOptions(custom_timeouts=CustomTimeouts(
        create="30m", update="30m", delete="30m")))

# Aliases for resource renaming
bucket = s3.Bucket("new-name",
    opts=ResourceOptions(aliases=[Alias(name="old-name")]))
```

## Drift Detection

```bash
# Detect drift
pulumi refresh --preview-only

# Fix drift (update state to match cloud)
pulumi refresh

# Fix drift (update cloud to match state)
pulumi up
```

## CI/CD Best Practices

### Branch Strategy

```
main       → production stack (auto-deploy)
staging    → staging stack (auto-deploy)
feature/*  → preview only on PR
```

### Preview on PR Template

```yaml
# GitHub Actions
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: pulumi/actions@v5
        with:
          command: preview
          stack-name: org/project/dev
          comment-on-pr: true
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Deployment Approval

```yaml
# GitHub Actions with environment protection
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - uses: pulumi/actions@v5
        with:
          command: up
          stack-name: org/project/prod
```

## Monorepo Structure

```
infrastructure/
├── shared/                    # Shared components
│   ├── __init__.py
│   └── networking.py
├── services/
│   ├── api/
│   │   ├── Pulumi.yaml
│   │   └── __main__.py
│   └── worker/
│       ├── Pulumi.yaml
│       └── __main__.py
├── platform/
│   ├── kubernetes/
│   │   ├── Pulumi.yaml
│   │   └── __main__.py
│   └── databases/
│       ├── Pulumi.yaml
│       └── __main__.py
└── requirements.txt
```

### Shared Component Usage

```python
# services/api/__main__.py
import sys
sys.path.insert(0, "../..")

from shared.networking import create_vpc

vpc = create_vpc("api-vpc", cidr="10.0.0.0/16")
```
