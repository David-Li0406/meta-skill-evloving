# Terraform State Management

## Remote Backends

### AWS S3

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Azure Blob

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate"
    storage_account_name = "tfstate12345"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

## Workspaces

```bash
terraform workspace list
terraform workspace new staging
terraform workspace select prod
```

```hcl
locals {
  env_config = {
    dev     = { instance_count = 1, cidr = "10.0.0.0/16" }
    staging = { instance_count = 2, cidr = "10.1.0.0/16" }
    prod    = { instance_count = 3, cidr = "10.2.0.0/16" }
  }
  config = local.env_config[terraform.workspace]
}
```

## State Operations

```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# List resources
terraform state list

# Move resource
terraform state mv aws_instance.old aws_instance.new

# Remove from state (without destroying)
terraform state rm aws_instance.orphan
```

## Security

- Enable encryption with KMS
- Block public access
- Enable versioning
- Never commit state files
- Use separate state per environment
