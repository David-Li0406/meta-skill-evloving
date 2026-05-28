# Terraform

**Category**: developer-tools/infrastructure
**Description**: Infrastructure as Code tool for building, changing, and versioning infrastructure
**Homepage**: https://www.terraform.io

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `cdktf` - CDK for Terraform
- `@cdktf/provider-aws` - AWS provider for CDKTF
- `@cdktf/provider-azurerm` - Azure provider for CDKTF
- `@cdktf/provider-google` - GCP provider for CDKTF
- `@cdktf/provider-kubernetes` - Kubernetes provider for CDKTF

#### PYPI
- `cdktf` - CDK for Terraform Python bindings
- `cdktf-cdktf-provider-aws` - AWS provider for CDKTF
- `cdktf-cdktf-provider-azurerm` - Azure provider for CDKTF
- `cdktf-cdktf-provider-google` - GCP provider for CDKTF
- `python-terraform` - Python wrapper for Terraform CLI

#### GO
- `github.com/hashicorp/terraform-exec` - Terraform execution library
- `github.com/hashicorp/terraform-plugin-sdk` - Terraform plugin SDK
- `github.com/hashicorp/terraform-plugin-framework` - Terraform plugin framework
- `github.com/hashicorp/hcl` - HCL parser

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### File Extensions
*Presence of these extensions indicates Terraform usage*

- `.tf` - Terraform configuration files
- `.tf.json` - Terraform JSON configuration
- `.tfvars` - Terraform variable files
- `.tfvars.json` - Terraform JSON variable files

### Configuration Files
*Known configuration files that indicate Terraform*

- `.terraform.lock.hcl` - Terraform dependency lock file (strong indicator of initialized project)
- `terraform.tfstate` - Terraform state file (indicates active infrastructure)
- `terraform.tfstate.backup` - Terraform state backup
- `.terraformrc` - Terraform CLI configuration
- `terraform.rc` - Terraform CLI configuration (Windows)
- `.terraform/` - Terraform working directory

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `^import\s+cdktf`
- CDKTF import
- Example: `import cdktf`

**Pattern**: `^from\s+cdktf\s+import`
- CDKTF from import
- Example: `from cdktf import App, TerraformStack`

**Pattern**: `^from\s+cdktf_cdktf_provider`
- CDKTF provider import
- Example: `from cdktf_cdktf_provider_aws import AwsProvider`

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `import\s+.*\s+from\s+['"]cdktf['"]`
- CDKTF ES6 import
- Example: `import { App, TerraformStack } from 'cdktf';`

**Pattern**: `require\(['"]cdktf['"]\)`
- CDKTF CommonJS require
- Example: `const { App } = require('cdktf');`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/hashicorp/terraform`
- Terraform Go package import
- Example: `import "github.com/hashicorp/terraform-exec/tfexec"`

### Code Patterns
*Terraform HCL patterns in .tf files*

**Pattern**: `^resource\s+"[^"]+"\s+"[^"]+"`
- Resource block definition
- Example: `resource "aws_instance" "example" {`

**Pattern**: `^provider\s+"[^"]+"`
- Provider block definition
- Example: `provider "aws" {`

**Pattern**: `^module\s+"[^"]+"`
- Module block definition
- Example: `module "vpc" {`

**Pattern**: `^terraform\s+\{`
- Terraform configuration block
- Example: `terraform { required_version = ">= 1.0" }`

**Pattern**: `^data\s+"[^"]+"\s+"[^"]+"`
- Data source block
- Example: `data "aws_ami" "ubuntu" {`

**Pattern**: `^variable\s+"[^"]+"`
- Variable declaration
- Example: `variable "region" {`

**Pattern**: `^output\s+"[^"]+"`
- Output declaration
- Example: `output "instance_ip" {`

---

## Environment Variables

- `TF_VAR_*` - Terraform input variables
- `TF_CLI_ARGS` - CLI arguments
- `TF_CLI_ARGS_*` - Command-specific CLI arguments
- `TF_DATA_DIR` - Location for Terraform data files
- `TF_INPUT` - Disable interactive prompts
- `TF_LOG` - Logging level
- `TF_LOG_PATH` - Log file path
- `TF_LOG_CORE` - Core logging level
- `TF_LOG_PROVIDER` - Provider logging level
- `TF_WORKSPACE` - Workspace selection
- `TERRAFORM_CLOUD_TOKEN` - Terraform Cloud authentication
- `TF_TOKEN_*` - Provider-specific tokens
- `TF_REGISTRY_CLIENT_TIMEOUT` - Registry timeout

## Detection Notes

- `.tf` files are the strongest indicator of Terraform usage
- `.terraform.lock.hcl` indicates an initialized Terraform project
- `terraform.tfstate` indicates active infrastructure management
- Provider blocks reveal which cloud platforms are being managed
- Module blocks indicate modular infrastructure patterns
- CDKTF packages indicate programmatic Terraform usage

---

## TIER 3: Configuration Extraction

These patterns extract specific infrastructure configuration from Terraform files.

### Backend Configuration Extraction

**Pattern**: `backend\s+"s3"\s*\{[^}]*bucket\s*=\s*"([^"]+)"`
- S3 backend bucket for Terraform state
- Extracts: `state_bucket`
- Example: `bucket = "my-terraform-state"`
- Multiline: true

**Pattern**: `backend\s+"s3"\s*\{[^}]*region\s*=\s*"([^"]+)"`
- S3 backend region
- Extracts: `state_region`
- Example: `region = "us-west-2"`
- Multiline: true

**Pattern**: `backend\s+"s3"\s*\{[^}]*dynamodb_table\s*=\s*"([^"]+)"`
- DynamoDB table for state locking
- Extracts: `lock_table`
- Example: `dynamodb_table = "terraform-locks"`
- Multiline: true

**Pattern**: `backend\s+"gcs"\s*\{[^}]*bucket\s*=\s*"([^"]+)"`
- GCS backend bucket
- Extracts: `state_bucket`
- Example: `bucket = "my-terraform-state"`
- Multiline: true

**Pattern**: `backend\s+"azurerm"\s*\{[^}]*storage_account_name\s*=\s*"([^"]+)"`
- Azure storage account for state
- Extracts: `storage_account`
- Example: `storage_account_name = "tfstate"`
- Multiline: true

### Provider Configuration Extraction

**Pattern**: `provider\s+"aws"\s*\{[^}]*region\s*=\s*"([^"]+)"`
- AWS provider region
- Extracts: `aws_region`
- Example: `region = "us-west-2"`
- Multiline: true

**Pattern**: `provider\s+"aws"\s*\{[^}]*profile\s*=\s*"([^"]+)"`
- AWS profile
- Extracts: `aws_profile`
- Example: `profile = "production"`
- Multiline: true

**Pattern**: `provider\s+"google"\s*\{[^}]*project\s*=\s*"([^"]+)"`
- GCP project
- Extracts: `gcp_project`
- Example: `project = "my-project-123"`
- Multiline: true

**Pattern**: `provider\s+"google"\s*\{[^}]*region\s*=\s*"([^"]+)"`
- GCP region
- Extracts: `gcp_region`
- Example: `region = "us-central1"`
- Multiline: true

**Pattern**: `provider\s+"azurerm"\s*\{[^}]*subscription_id\s*=\s*"([^"]+)"`
- Azure subscription ID
- Extracts: `azure_subscription_id`
- Example: `subscription_id = "12345678-..."`
- Multiline: true

### Resource Extraction

**Pattern**: `resource\s+"aws_s3_bucket"\s+"([^"]+)"`
- S3 bucket resource
- Extracts: `resource_name`
- Example: `resource "aws_s3_bucket" "main"`

**Pattern**: `bucket\s*=\s*"([a-z0-9][a-z0-9.-]{1,61}[a-z0-9])"`
- S3 bucket name
- Extracts: `bucket_name`
- Example: `bucket = "my-application-data"`

**Pattern**: `resource\s+"aws_db_instance"\s+"([^"]+)"`
- RDS instance resource
- Extracts: `resource_name`
- Example: `resource "aws_db_instance" "main"`

**Pattern**: `resource\s+"aws_eks_cluster"\s+"([^"]+)"`
- EKS cluster resource
- Extracts: `resource_name`
- Example: `resource "aws_eks_cluster" "main"`

**Pattern**: `cluster_name\s*=\s*"([^"]+)"`
- EKS cluster name
- Extracts: `cluster_name`
- Example: `cluster_name = "prod-cluster"`

**Pattern**: `resource\s+"aws_ecr_repository"\s+"([^"]+)"`
- ECR repository resource
- Extracts: `resource_name`
- Example: `resource "aws_ecr_repository" "app"`

**Pattern**: `name\s*=\s*"([^"]+)"`
- Generic resource name (context-dependent)
- Extracts: `name`
- Example: `name = "my-app"`

### Module Source Extraction

**Pattern**: `source\s*=\s*"([^"]+)"`
- Module source
- Extracts: `module_source`
- Example: `source = "terraform-aws-modules/vpc/aws"`

**Pattern**: `source\s*=\s*"git::([^"?]+)`
- Git module source
- Extracts: `git_repo`
- Example: `source = "git::https://github.com/org/module.git"`

**Pattern**: `source\s*=\s*"s3::([^"]+)"`
- S3 module source
- Extracts: `s3_path`
- Example: `source = "s3::https://s3.amazonaws.com/bucket/module.zip"`

### Variable Extraction

**Pattern**: `variable\s+"([^"]+)"\s*\{`
- Variable declaration
- Extracts: `variable_name`
- Example: `variable "environment" {`

**Pattern**: `default\s*=\s*"([^"]+)"`
- Variable default value
- Extracts: `default_value`
- Example: `default = "production"`

### Extraction Output Example

```json
{
  "extractions": {
    "terraform_backend": {
      "type": "s3",
      "bucket": "company-terraform-state",
      "region": "us-west-2",
      "dynamodb_table": "terraform-locks",
      "source_file": "backend.tf"
    },
    "providers": {
      "aws": {
        "regions": ["us-west-2", "us-east-1"],
        "profile": "production"
      },
      "google": {
        "project": "my-project-123",
        "region": "us-central1"
      }
    },
    "aws_resources": {
      "s3_buckets": ["app-data", "logs-bucket"],
      "eks_clusters": ["prod-cluster"],
      "ecr_repositories": ["app", "worker"],
      "rds_instances": ["main-db"]
    },
    "modules": [
      {
        "source": "terraform-aws-modules/vpc/aws",
        "version": "5.0.0"
      },
      {
        "source": "git::https://github.com/company/terraform-modules.git//networking",
        "ref": "v1.2.0"
      }
    ],
    "variables_defined": [
      "environment",
      "region",
      "cluster_name",
      "db_instance_class"
    ]
  }
}
```
