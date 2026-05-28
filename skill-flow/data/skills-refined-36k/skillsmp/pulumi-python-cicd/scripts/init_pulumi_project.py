#!/usr/bin/env python3
"""
Initialize a new Pulumi Python project with best practices structure.
Usage: python init_pulumi_project.py <project-name> [--cloud aws|azure|gcp|k8s]
"""

import argparse
import os
import sys

PULUMI_YAML_TEMPLATE = """name: {project_name}
runtime:
  name: python
  options:
    virtualenv: venv
description: Infrastructure for {project_name}
"""

REQUIREMENTS_TEMPLATE = """pulumi>=3.0.0,<4.0.0
{provider_package}
"""

PROVIDER_PACKAGES = {
    "aws": "pulumi-aws>=6.0.0",
    "azure": "pulumi-azure-native>=2.0.0",
    "gcp": "pulumi-gcp>=7.0.0",
    "k8s": "pulumi-kubernetes>=4.0.0",
}

MAIN_TEMPLATES = {
    "aws": '''"""
{project_name} infrastructure - AWS
"""
import pulumi
from pulumi_aws import s3

# Configuration
config = pulumi.Config()
env = pulumi.get_stack()

# Example: S3 bucket
bucket = s3.Bucket(f"{{env}}-data",
    tags={{
        "Environment": env,
        "ManagedBy": "pulumi",
        "Project": "{project_name}",
    }})

# Exports
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
''',
    "azure": '''"""
{project_name} infrastructure - Azure
"""
import pulumi
from pulumi_azure_native import resources, storage

# Configuration
config = pulumi.Config()
env = pulumi.get_stack()

# Resource Group
rg = resources.ResourceGroup(f"{{env}}-rg")

# Example: Storage Account
storage_account = storage.StorageAccount(f"{{env}}sa",
    resource_group_name=rg.name,
    sku=storage.SkuArgs(name="Standard_LRS"),
    kind="StorageV2")

# Exports
pulumi.export("resource_group_name", rg.name)
pulumi.export("storage_account_name", storage_account.name)
''',
    "gcp": '''"""
{project_name} infrastructure - GCP
"""
import pulumi
from pulumi_gcp import storage

# Configuration
config = pulumi.Config()
env = pulumi.get_stack()
project = config.require("gcp:project")

# Example: GCS bucket
bucket = storage.Bucket(f"{{env}}-data",
    location="US",
    labels={{
        "environment": env,
        "managed-by": "pulumi",
    }})

# Exports
pulumi.export("bucket_name", bucket.name)
pulumi.export("bucket_url", bucket.url)
''',
    "k8s": '''"""
{project_name} infrastructure - Kubernetes
"""
import pulumi
from pulumi_kubernetes import core, apps

# Configuration
config = pulumi.Config()
env = pulumi.get_stack()

# Namespace
namespace = core.v1.Namespace(f"{{env}}-ns",
    metadata={{"name": f"{project_name}-{{env}}"}})

# Example: Deployment
deployment = apps.v1.Deployment(f"{{env}}-app",
    metadata={{"namespace": namespace.metadata.name}},
    spec={{
        "replicas": 2,
        "selector": {{"matchLabels": {{"app": "{project_name}"}}}},
        "template": {{
            "metadata": {{"labels": {{"app": "{project_name}"}}}},
            "spec": {{
                "containers": [{{
                    "name": "app",
                    "image": "nginx:latest",
                    "ports": [{{"containerPort": 80}}],
                }}]
            }}
        }}
    }})

# Exports
pulumi.export("namespace", namespace.metadata.name)
''',
}

GITHUB_ACTIONS_TEMPLATE = """name: Pulumi
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PULUMI_ACCESS_TOKEN: ${{{{ secrets.PULUMI_ACCESS_TOKEN }}}}
{cloud_env_vars}

jobs:
  preview:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - uses: pulumi/actions@v5
        with:
          command: preview
          stack-name: ${{{{ github.repository_owner }}}}/{project_name}/dev
          comment-on-pr: true
          github-token: ${{{{ secrets.GITHUB_TOKEN }}}}

  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - uses: pulumi/actions@v5
        with:
          command: up
          stack-name: ${{{{ github.repository_owner }}}}/{project_name}/prod
"""

CLOUD_ENV_VARS = {
    "aws": """  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  AWS_REGION: us-west-2""",
    "azure": """  ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
  ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
  ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}
  ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}""",
    "gcp": """  GOOGLE_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
  GOOGLE_PROJECT: ${{ secrets.GOOGLE_PROJECT }}""",
    "k8s": """  KUBECONFIG: ${{ secrets.KUBECONFIG }}""",
}

GITIGNORE_TEMPLATE = """# Pulumi
*.pyc
__pycache__/
venv/
.pulumi/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store

# Environment
.env
*.local.yaml
"""

TEST_TEMPLATE = '''"""
Unit tests for {project_name} infrastructure
"""
import pulumi

class MockMixin:
    """Mock for Pulumi resources during testing"""
    def call(self, args):
        return {{}}
    
    def new_resource(self, args):
        return [f"{{args.name}}_id", args.inputs]

# Set mocks before importing infrastructure
pulumi.runtime.set_mocks(MockMixin())

def test_resources_have_tags():
    """Verify all resources have required tags"""
    # Import after setting mocks
    # from infrastructure import main
    pass

def test_naming_convention():
    """Verify resources follow naming convention"""
    pass
'''


def create_project(project_name: str, cloud: str):
    """Create the project directory structure"""
    
    # Create directories
    dirs = [
        project_name,
        f"{project_name}/infrastructure",
        f"{project_name}/tests",
        f"{project_name}/.github/workflows",
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Create files
    files = {
        f"{project_name}/Pulumi.yaml": PULUMI_YAML_TEMPLATE.format(project_name=project_name),
        f"{project_name}/Pulumi.dev.yaml": f"config:\n  {cloud}:region: us-west-2\n",
        f"{project_name}/Pulumi.prod.yaml": f"config:\n  {cloud}:region: us-west-2\n",
        f"{project_name}/requirements.txt": REQUIREMENTS_TEMPLATE.format(
            provider_package=PROVIDER_PACKAGES[cloud]
        ),
        f"{project_name}/__main__.py": MAIN_TEMPLATES[cloud].format(project_name=project_name),
        f"{project_name}/infrastructure/__init__.py": '"""Infrastructure components"""',
        f"{project_name}/tests/__init__.py": "",
        f"{project_name}/tests/test_infra.py": TEST_TEMPLATE.format(project_name=project_name),
        f"{project_name}/.github/workflows/pulumi.yml": GITHUB_ACTIONS_TEMPLATE.format(
            project_name=project_name,
            cloud_env_vars=CLOUD_ENV_VARS[cloud]
        ),
        f"{project_name}/.gitignore": GITIGNORE_TEMPLATE,
    }
    
    for filepath, content in files.items():
        with open(filepath, "w") as f:
            f.write(content)
    
    print(f"✅ Created Pulumi Python project: {project_name}")
    print(f"   Cloud provider: {cloud}")
    print(f"\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. python -m venv venv && source venv/bin/activate")
    print(f"  3. pip install -r requirements.txt")
    print(f"  4. pulumi stack init dev")
    print(f"  5. pulumi up")


def main():
    parser = argparse.ArgumentParser(description="Initialize a Pulumi Python project")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument(
        "--cloud",
        choices=["aws", "azure", "gcp", "k8s"],
        default="aws",
        help="Cloud provider (default: aws)"
    )
    
    args = parser.parse_args()
    
    if os.path.exists(args.project_name):
        print(f"Error: Directory '{args.project_name}' already exists")
        sys.exit(1)
    
    create_project(args.project_name, args.cloud)


if __name__ == "__main__":
    main()
