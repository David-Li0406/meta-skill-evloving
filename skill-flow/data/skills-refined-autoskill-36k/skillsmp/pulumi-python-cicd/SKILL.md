---
name: pulumi-python-cicd
description: "Expert guidance for Pulumi infrastructure-as-code with Python and CI/CD pipeline integration. Use this skill when users ask about: (1) Creating or managing Pulumi projects with Python, (2) Writing Pulumi stacks for AWS, Azure, GCP, or Kubernetes, (3) Setting up CI/CD pipelines for infrastructure deployment (GitHub Actions, GitLab CI, Azure DevOps, Jenkins), (4) Pulumi stack management, secrets, and configuration, (5) Testing infrastructure code, (6) Pulumi Automation API, (7) Infrastructure deployment patterns and best practices, (8) Multi-environment or multi-stack deployments."
---

# Pulumi Python CI/CD Expert

## Project Structure

```
my-infra/
├── Pulumi.yaml           # Project definition
├── Pulumi.dev.yaml       # Dev stack config
├── Pulumi.prod.yaml      # Prod stack config
├── __main__.py           # Entry point
├── requirements.txt      # Python dependencies
├── infrastructure/       # Modular components
│   ├── __init__.py
│   ├── networking.py
│   ├── compute.py
│   └── storage.py
└── tests/
    └── test_infra.py
```

**Pulumi.yaml:**
```yaml
name: project-name
runtime:
  name: python
  options:
    virtualenv: venv
description: Infrastructure for [project]
```

## Basic Stack Pattern

```python
import pulumi
from pulumi_aws import s3

config = pulumi.Config()
env = pulumi.get_stack()

bucket = s3.Bucket(f"{env}-data",
    tags={"Environment": env, "ManagedBy": "pulumi"})

pulumi.export("bucket_name", bucket.id)
```

## Component Resources

```python
from pulumi import ComponentResource, ResourceOptions
from pulumi_aws import ec2, lb

class WebService(ComponentResource):
    def __init__(self, name: str, args: dict, opts: ResourceOptions = None):
        super().__init__("custom:app:WebService", name, {}, opts)
        child_opts = ResourceOptions(parent=self)
        
        self.sg = ec2.SecurityGroup(f"{name}-sg",
            vpc_id=args["vpc_id"],
            ingress=[{"protocol": "tcp", "from_port": 80, "to_port": 80, 
                      "cidr_blocks": ["0.0.0.0/0"]}],
            opts=child_opts)
        
        self.alb = lb.LoadBalancer(f"{name}-alb",
            security_groups=[self.sg.id], subnets=args["subnet_ids"],
            opts=child_opts)
        
        self.register_outputs({"dns_name": self.alb.dns_name})
```

## Configuration & Secrets

```python
config = pulumi.Config()
instance_type = config.get("instanceType") or "t3.micro"  # Optional with default
db_name = config.require("dbName")                         # Required
db_password = config.require_secret("dbPassword")          # Secret (encrypted)
```

CLI: `pulumi config set --secret dbPassword "s3cr3t"`

## Stack References

```python
network_stack = pulumi.StackReference("org/network-infra/prod")
vpc_id = network_stack.get_output("vpc_id")
```

## CI/CD Patterns

### GitHub Actions

```yaml
name: Pulumi
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }

env:
  PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

jobs:
  preview:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - uses: pulumi/actions@v5
        with:
          command: preview
          stack-name: org/project/dev
          comment-on-pr: true

  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - uses: pulumi/actions@v5
        with:
          command: up
          stack-name: org/project/prod
```

### GitLab CI

```yaml
image: python:3.11
variables:
  PULUMI_ACCESS_TOKEN: $PULUMI_ACCESS_TOKEN

before_script:
  - pip install -r requirements.txt
  - curl -fsSL https://get.pulumi.com | sh
  - export PATH=$PATH:$HOME/.pulumi/bin

preview:
  script: [pulumi stack select org/project/dev, pulumi preview]
  only: [merge_requests]

deploy:
  script: [pulumi stack select org/project/prod, pulumi up --yes]
  only: [main]
  when: manual
```

### Azure DevOps

See `references/azure-devops.md` for complete pipeline template.

## Automation API

```python
from pulumi import automation as auto

def pulumi_program():
    from pulumi_aws import s3
    bucket = s3.Bucket("auto-bucket")
    pulumi.export("bucket_name", bucket.id)

stack = auto.create_or_select_stack(
    stack_name="dev", project_name="automation-project", program=pulumi_program)
stack.set_config("aws:region", auto.ConfigValue("us-west-2"))

preview = stack.preview(on_output=print)
up_result = stack.up(on_output=print)
print(f"Outputs: {up_result.outputs}")
```

## Testing

### Unit Testing

```python
import pulumi
class MockMixin:
    def call(self, args): return {}
    def new_resource(self, args): return [f"{args.name}_id", args.inputs]

pulumi.runtime.set_mocks(MockMixin())

def test_instance_has_tags():
    from infrastructure import compute
    def check(args):
        urn, props = args
        assert "Environment" in props.get("tags", {})
    return pulumi.Output.all(compute.instance.urn, compute.instance.tags).apply(check)
```

### Integration Testing

```python
from pulumi import automation as auto
import pytest

@pytest.fixture(scope="module")
def stack():
    s = auto.create_or_select_stack(stack_name="test", work_dir=".")
    s.up(on_output=print)
    yield s
    s.destroy(on_output=print)

def test_bucket_exists(stack):
    assert "bucket_name" in stack.outputs()
```

## Multi-Environment Config

```python
stack = pulumi.get_stack()
env_config = {
    "dev": {"instance_type": "t3.micro", "replicas": 1},
    "staging": {"instance_type": "t3.small", "replicas": 2},
    "prod": {"instance_type": "t3.medium", "replicas": 3},
}
settings = env_config.get(stack, env_config["dev"])
```

## Global Tagging Transform

```python
def auto_tag(args):
    if hasattr(args.props, "tags"):
        args.props["tags"] = {**(args.props.get("tags") or {}),
            "ManagedBy": "pulumi", "Stack": pulumi.get_stack()}
    return pulumi.ResourceTransformationResult(args.props, args.opts)

pulumi.runtime.register_stack_transformation(auto_tag)
```

## Multi-Provider Setup

```python
from pulumi_aws import Provider, s3

us_east = Provider("us-east", region="us-east-1")
us_west = Provider("us-west", region="us-west-2")

bucket_east = s3.Bucket("east", opts=pulumi.ResourceOptions(provider=us_east))
bucket_west = s3.Bucket("west", opts=pulumi.ResourceOptions(provider=us_west))
```

## Key CLI Commands

```bash
pulumi stack init/select org/project/env  # Stack management
pulumi preview                             # Preview changes
pulumi up [--yes]                          # Deploy
pulumi refresh                             # Sync state
pulumi stack output [key]                  # Get outputs
pulumi destroy                             # Tear down
pulumi import <type> <name> <id>           # Import existing
pulumi cancel                              # Release state lock
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| State lock conflict | `pulumi cancel` |
| Resource exists | `pulumi import` |
| Dependency cycle | Add `depends_on` to ResourceOptions |
| Auth failure | Check env vars / `pulumi config set aws:profile` |

## References

- `references/cloud-providers.md` - AWS/Azure/GCP/K8s patterns
- `references/advanced-patterns.md` - Policy as Code, ESC, OIDC
