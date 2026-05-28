---
name: terraform-modules
description: 'Develop reusable Terraform modules including structure, composition, nested modules, and provider configuration. Use when asked about "creating modules", "module structure", "child modules", "module composition", "provider inheritance", or when building reusable infrastructure components. Covers standard module structure, nested modules, dependency inversion, provider passing, and module best practices.'
---

# Terraform Module Development

Comprehensive guide to developing reusable Terraform modules including standard structure, composition patterns, nested modules, and provider configuration.

## When to Use This Skill

- User asks about "creating modules", "module structure", "how to build modules"
- Questions about "child modules", "nested modules", "sub-modules"
- "Module composition", "dependency inversion", "module patterns"
- "Provider configuration in modules", "passing providers"
- Designing reusable infrastructure components
- Refactoring infrastructure into modules
- Module best practices and standards

## Module Fundamentals

### What is a Module

A **module** is a container for multiple resources that are used together. Modules create lightweight abstractions, letting you describe infrastructure in terms of architecture rather than physical objects.

**Every Terraform configuration has at least one module:**
- **Root Module**: The `.tf` files in your working directory
- **Child Modules**: Modules called by the root module using `module` blocks

**Key Benefits:**
- **Reusability**: Use same module across multiple projects
- **Abstraction**: Hide complexity behind simple interfaces
- **Encapsulation**: Group related resources together
- **Standardization**: Enforce organizational standards
- **Maintainability**: Update once, apply everywhere

### When to Write a Module

**Write a module when:**
- ✅ Creating a higher-level abstraction (e.g., "Consul cluster" not just "EC2 instances")
- ✅ Reusing same infrastructure pattern across multiple environments
- ✅ Standardizing infrastructure configuration
- ✅ Encapsulating complex resource relationships
- ✅ Sharing infrastructure patterns across teams

**Don't write a module when:**
- ❌ It's just a thin wrapper around a single resource type
- ❌ You can't find a name different from the main resource type
- ❌ The abstraction doesn't raise the level of complexity
- ❌ It's used only once with no reuse potential

**Example - Good Module:**
```hcl
# Module: "aws-consul-cluster"
# Abstracts: Multiple resources (instances, security groups, IAM) into "Consul cluster"
module "consul_cluster" {
  source = "./modules/aws-consul-cluster"

  cluster_size = 3
  vpc_id       = var.vpc_id
  subnet_ids   = var.subnet_ids
}
```

**Example - Unnecessary Module:**
```hcl
# ❌ Bad - just wrapping aws_instance
module "instance" {
  source = "./modules/instance"

  ami           = var.ami
  instance_type = var.instance_type
}

# ✅ Better - use resource directly
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
}
```

## Standard Module Structure

### Minimal Module

**Required Files:**
```
terraform-<PROVIDER>-<NAME>/
├── README.md           # Module documentation
├── main.tf             # Primary resources
├── variables.tf        # Input variable declarations
└── outputs.tf          # Output value declarations
```

**Purpose of Each File:**

**README.md:**
- Module description and purpose
- Usage examples (basic and advanced)
- Visual diagrams (optional)
- Requirements and prerequisites
- License information

**main.tf:**
- Primary resource definitions
- Data source declarations
- Module calls to child modules
- Main entry point for module logic

**variables.tf:**
- All input variable declarations
- Variable descriptions, types, defaults
- Validation blocks
- Alphabetical order (context variable first)

**outputs.tf:**
- All output value declarations
- Output descriptions
- Values exposed to parent modules
- Alphabetical order

### Complete Module

**Recommended Structure:**
```
terraform-<PROVIDER>-<NAME>/
├── README.md                # Module documentation
├── LICENSE                  # License file
├── main.tf                  # Primary resources and data sources
├── variables.tf             # Input variables (alphabetical)
├── outputs.tf               # Output values (alphabetical)
├── versions.tf              # Provider version constraints
├── locals.tf                # Local value definitions (optional)
├── <resource-type>.tf       # Resource-specific files (optional)
├── modules/                 # Nested modules directory
│   ├── submodule-a/
│   │   ├── README.md        # Include if externally usable
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── submodule-b/
│       ├── main.tf          # No README = internal only
│       ├── variables.tf
│       └── outputs.tf
└── examples/                # Usage examples directory
    ├── README.md
    ├── basic/
    │   ├── README.md
    │   └── main.tf
    └── complete/
        ├── README.md
        └── main.tf
```

### File Naming Conventions

**Standard Files:**
- `main.tf` - Primary entry point
- `variables.tf` - Input variables
- `outputs.tf` - Output values
- `versions.tf` - Version constraints
- `README.md` - Documentation
- `LICENSE` - License information

**Optional Files:**
- `locals.tf` - Local value definitions
- `providers.tf` - Provider configurations (root module only)
- `backend.tf` - Backend configuration (root module only)
- `<resource-type>.tf` - Logical groupings (e.g., `network.tf`, `security.tf`)

**Naming Rules:**
- Use kebab-case for directories: `consul-cluster/`, `vpc-network/`
- Use snake_case within .tf files: `aws_instance`, `vpc_id`
- Repository names: `terraform-<PROVIDER>-<NAME>`

## Module Interface Design

### Input Variables

Variables define the module's input interface.

**Best Practices:**

```hcl
# ✅ Good variable definition
variable "cluster_size" {
  type        = number
  description = "Number of instances in the cluster"
  default     = 3

  validation {
    condition     = var.cluster_size >= 1 && var.cluster_size <= 10
    error_message = "Cluster size must be between 1 and 10."
  }
}

# ✅ Required variable (no default)
variable "vpc_id" {
  type        = string
  description = "VPC ID where resources will be created"
}

# ✅ Complex type with optional attributes
variable "network_config" {
  type = object({
    vpc_id     = string
    subnet_ids = list(string)
    enable_dns = optional(bool, true)
  })
  description = "Network configuration for the module"
}
```

**Variable Guidelines:**
- Always include `description`
- Use appropriate `type` constraints
- Provide `default` for optional variables
- Add `validation` blocks for important constraints
- Mark sensitive variables with `sensitive = true`
- Use objects for related parameters

### Output Values

Outputs expose module data to parent modules.

**Best Practices:**

```hcl
# ✅ Good output definition
output "cluster_id" {
  description = "ID of the cluster for use in other resources"
  value       = aws_ecs_cluster.main.id
}

# ✅ Output for integration
output "security_group_id" {
  description = "Security group ID for allowing traffic to cluster"
  value       = aws_security_group.cluster.id
}

# ✅ Sensitive output
output "admin_password" {
  description = "Auto-generated admin password"
  value       = random_password.admin.result
  sensitive   = true
}

# ✅ Complex output
output "endpoints" {
  description = "Map of service endpoints"
  value = {
    primary   = aws_instance.primary.private_ip
    secondary = aws_instance.secondary.private_ip
    public    = aws_lb.main.dns_name
  }
}
```

**Output Guidelines:**
- Always include `description`
- Expose values needed by parent modules
- Mark sensitive outputs appropriately
- Use descriptive names
- Consider what consumers will need for integration

### Local Values

Locals reduce repetition within a module.

**Best Practices:**

```hcl
locals {
  # Naming convention
  resource_name = "${var.project}-${var.environment}"

  # Feature flags
  create_lb     = var.load_balancer_config != null
  enable_backup = var.environment == "prod"

  # Common tags
  common_tags = merge(
    var.tags,
    {
      Module      = "consul-cluster"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  )
}
```

## Nested Modules (Sub-modules)

### When to Use Nested Modules

**Create nested modules when:**
- ✅ Splitting complex functionality into smaller, focused pieces
- ✅ Providing optional, advanced configuration paths
- ✅ Reusing common patterns within your module
- ✅ Allowing users to compose infrastructure differently

**Nested Module Types:**

**1. Public Nested Modules (with README.md):**
- Can be used independently by external users
- Have their own documentation
- Expose a public interface
- Example: `modules/cluster/`, `modules/networking/`

**2. Internal Nested Modules (no README.md):**
- Internal implementation details
- Not intended for external use
- May change without notice
- Example: `modules/internal-helper/`

### Nested Module Structure

```hcl
# Root module (main.tf)
module "network" {
  source = "./modules/network"

  vpc_cidr = var.vpc_cidr
  azs      = var.availability_zones
}

module "cluster" {
  source = "./modules/cluster"

  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.private_subnet_ids
}

# Output from nested modules
output "vpc_id" {
  description = "VPC ID from network module"
  value       = module.network.vpc_id
}
```

**Nested Module Guidelines:**
- Use relative paths: `./modules/module-name`
- Each nested module follows same structure as root module
- Nested modules should be composable, not deeply nested
- Prefer flat module hierarchy (1 level deep)

### Module Composition vs. Nesting

**✅ Recommended: Flat Composition**

```hcl
# Root module composes independent modules
module "network" {
  source = "./modules/network"
  # ...
}

module "database" {
  source = "./modules/database"

  vpc_id    = module.network.vpc_id
  subnet_ids = module.network.private_subnet_ids
}

module "application" {
  source = "./modules/application"

  vpc_id      = module.network.vpc_id
  subnet_ids  = module.network.private_subnet_ids
  db_endpoint = module.database.endpoint
}
```

**❌ Avoid: Deep Nesting**

```hcl
# Deep nesting makes modules hard to reuse
module "infrastructure" {
  source = "./modules/infrastructure"
  # Module internally calls network, database, application
  # Hard to use pieces independently
}
```

## Module Composition Patterns

### Dependency Inversion

Pass dependencies into modules rather than having modules create them.

**❌ Bad - Module Creates Dependencies:**
```hcl
# Module internally creates VPC
module "cluster" {
  source = "./modules/cluster"

  vpc_cidr = "10.0.0.0/16"
  # Module creates its own VPC internally
}
```

**✅ Good - Dependency Injection:**
```hcl
# Parent provides VPC to module
module "network" {
  source = "./modules/network"

  vpc_cidr = "10.0.0.0/16"
}

module "cluster" {
  source = "./modules/cluster"

  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.subnet_ids
}
```

**Benefits:**
- Modules can coexist in same network
- Easier to refactor later
- Clear dependency relationships
- Modules are more reusable

### Conditional Resource Creation

Use dependency inversion for conditional creation.

**Pattern:**
```hcl
# Variable accepts existing or new resource
variable "ami" {
  type = object({
    id           = string
    architecture = string
  })
  description = "AMI to use for instances"
}

# Caller decides whether to create or use existing
# Option 1: Create new AMI
resource "aws_ami_copy" "example" {
  name              = "local-copy"
  source_ami_id     = "ami-abc123"
  source_ami_region = "eu-west-1"
}

module "cluster" {
  source = "./modules/cluster"
  ami    = aws_ami_copy.example
}

# Option 2: Use existing AMI
data "aws_ami" "example" {
  owner = "099720109477"

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*"]
  }
}

module "cluster" {
  source = "./modules/cluster"
  ami    = data.aws_ami.example
}
```

### Data-Only Modules

Modules that retrieve existing infrastructure without creating new resources.

**Use Case:**
```hcl
# Data-only module retrieves network information
module "network" {
  source = "./modules/join-network-aws"

  environment = "production"
}

# Use retrieved information
module "application" {
  source = "./modules/application"

  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.subnet_ids
}
```

**Data Module Implementation:**
```hcl
# modules/join-network-aws/main.tf
data "aws_vpc" "main" {
  tags = {
    Environment = var.environment
  }
}

data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.main.id

  tags = {
    Tier = "private"
  }
}

output "vpc_id" {
  value = data.aws_vpc.main.id
}

output "subnet_ids" {
  value = data.aws_subnet_ids.private.ids
}
```

**Benefits:**
- Source of information can change without updating consumers
- Can swap between data and management modules easily
- Clear separation between infrastructure management boundaries

### Multi-Cloud Abstractions

Create lightweight abstractions across cloud providers.

**Example - DNS Records:**
```hcl
# Common recordset abstraction
variable "recordsets" {
  type = list(object({
    name    = string
    type    = string
    ttl     = number
    records = list(string)
  }))
}

# AWS implementation
module "dns_aws" {
  source = "./modules/route53-dns"

  zone_id    = var.route53_zone_id
  recordsets = local.recordsets
}

# Google Cloud implementation
module "dns_gcp" {
  source = "./modules/cloud-dns"

  project    = var.project_id
  zone_name  = var.dns_zone_name
  recordsets = local.recordsets
}
```

## Provider Configuration in Modules

### Provider Requirements

Every module must declare its provider requirements.

**Module versions.tf:**
```hcl
terraform {
  required_version = ">= 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.9"
    }
  }
}
```

**Guidelines:**
- Declare `required_providers` in every module
- Use `>=` for minimum version (flexibility for consumers)
- Specify the minimum version containing required features
- Don't include `provider` blocks in child modules

### Implicit Provider Inheritance

Child modules automatically inherit default provider configurations.

**Root Module:**
```hcl
provider "aws" {
  region = "us-west-1"
}

module "cluster" {
  source = "./modules/cluster"
  # Automatically uses parent's AWS provider
}
```

**Child Module:**
```hcl
# No provider block needed - inherited from parent
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
}
```

**When to Use:**
- Single provider configuration is sufficient
- Simple, straightforward module usage
- No special provider requirements

### Passing Providers Explicitly

Pass different provider configurations to child modules.

**Scenario: Multi-Region Deployment**

```hcl
# Root module
provider "aws" {
  alias  = "usw1"
  region = "us-west-1"
}

provider "aws" {
  alias  = "usw2"
  region = "us-west-2"
}

module "cluster_west1" {
  source = "./modules/cluster"

  providers = {
    aws = aws.usw1
  }
}

module "cluster_west2" {
  source = "./modules/cluster"

  providers = {
    aws = aws.usw2
  }
}
```

**Child Module with Configuration Aliases:**
```hcl
# modules/cluster/versions.tf
terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 4.9"
      configuration_aliases = [aws.src, aws.dst]
    }
  }
}

# modules/cluster/main.tf
resource "aws_instance" "src" {
  provider = aws.src
  # ...
}

resource "aws_instance" "dst" {
  provider = aws.dst
  # ...
}
```

**Root Module Calling:**
```hcl
module "cross_region" {
  source = "./modules/cluster"

  providers = {
    aws.src = aws.usw1
    aws.dst = aws.usw2
  }
}
```

### Provider Best Practices

**Do's:**

✅ **Declare provider requirements in every module**
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.9"
    }
  }
}
```

✅ **Use configuration_aliases for multi-provider modules**
```hcl
configuration_aliases = [aws.primary, aws.secondary]
```

✅ **Pass providers explicitly when needed**
```hcl
module "example" {
  source = "./modules/example"

  providers = {
    aws = aws.west
  }
}
```

**Don'ts:**

❌ **Don't include provider blocks in child modules**
```hcl
# ❌ Bad - no provider blocks in child modules
provider "aws" {
  region = "us-west-1"
}
```

❌ **Don't use modules with provider blocks with count/for_each**
```hcl
# Error: Module with provider blocks can't use count
module "example" {
  count  = 3
  source = "./module-with-provider"  # Has provider block inside
}
```

## Module Meta-Arguments

Modules support special meta-arguments.

### count

Create multiple instances of a module:

```hcl
module "instances" {
  count  = 3
  source = "./modules/instance"

  name = "instance-${count.index}"
}

# Access specific instance
output "first_instance_id" {
  value = module.instances[0].instance_id
}
```

### for_each

Create named instances of a module:

```hcl
module "buckets" {
  for_each = toset(["logs", "data", "backups"])
  source   = "./modules/s3-bucket"

  bucket_name = "${var.project}-${each.key}"
}

# Access specific bucket
output "logs_bucket_arn" {
  value = module.buckets["logs"].bucket_arn
}
```

### depends_on

Explicit module dependencies:

```hcl
module "network" {
  source = "./modules/network"
}

module "database" {
  source = "./modules/database"

  # Ensure network is created first
  depends_on = [module.network]
}
```

### providers

Pass provider configurations:

```hcl
module "west_coast" {
  source = "./modules/infrastructure"

  providers = {
    aws = aws.west
  }
}
```

## Assumptions and Guarantees

Document what your module assumes and guarantees.

### Assumptions

Conditions that must be true for the module to work:

```hcl
variable "ami_id" {
  type        = string
  description = "AMI ID for EC2 instances (must be x86_64 architecture)"

  # Document assumption with validation
  validation {
    condition     = can(regex("^ami-[a-f0-9]{8,17}$", var.ami_id))
    error_message = "AMI ID must be valid format."
  }
}
```

### Guarantees

Characteristics consumers can rely on:

```hcl
output "instance_private_dns" {
  description = "Private DNS name - guaranteed to be set in VPC with DNS enabled"
  value       = aws_instance.web.private_dns

  # Validate guarantee with precondition
  precondition {
    condition     = aws_instance.web.private_dns != ""
    error_message = "Instance must have private DNS name."
  }
}
```

## Module Versioning

### Version Constraints

**When consuming modules:**
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"  # Allow patch and minor updates

  # Configuration
}
```

**Version Constraint Operators:**
```hcl
version = "1.2.3"      # Exact version
version = ">= 1.2.0"   # Minimum version
version = "~> 1.2.0"   # Pessimistic: >= 1.2.0, < 1.3.0
version = ">= 1.2.0, < 2.0.0"  # Range
```

**Best Practices:**
- Pin major version to avoid breaking changes
- Allow minor and patch updates for bug fixes
- Test updates before applying to production
- Document version compatibility in README

## Module Examples

### Example Structure

Every module should include working examples:

```
examples/
├── README.md           # Overview of examples
├── basic/              # Minimal example
│   ├── README.md
│   └── main.tf
├── complete/           # Full-featured example
│   ├── README.md
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── scenario/           # Specific use case
    ├── README.md
    └── main.tf
```

**Example main.tf:**
```hcl
# examples/basic/main.tf
module "example" {
  source = "../../"  # Reference root module

  # Minimal required configuration
  vpc_id     = "vpc-12345678"
  subnet_ids = ["subnet-12345678"]

  cluster_size = 3
}
```

**Important:**
- Use external source path, not relative: `source = "../../"`
- Examples should be independently runnable
- Include README with purpose and prerequisites
- Show realistic usage patterns

## Module Best Practices Summary

### Module Design

✅ **Do:**
- Raise the level of abstraction
- Use descriptive module names
- Follow standard module structure
- Document inputs, outputs, and assumptions
- Provide working examples
- Include README with usage instructions
- Version your modules
- Use semantic versioning

❌ **Don't:**
- Create thin wrappers around single resources
- Include provider blocks in child modules
- Nest modules deeply (prefer flat composition)
- Skip variable descriptions
- Hardcode values that should be configurable
- Mix multiple unrelated concerns in one module

### Module Structure

✅ **Do:**
- Follow standard file naming (`main.tf`, `variables.tf`, `outputs.tf`)
- Use kebab-case for directories
- Organize large modules into resource-specific files
- Keep nested modules in `modules/` directory
- Put examples in `examples/` directory
- Include README.md for public nested modules

❌ **Don't:**
- Mix naming conventions
- Create unnecessary files
- Skip documentation
- Use cryptic file names

### Provider Configuration

✅ **Do:**
- Declare `required_providers` in every module
- Use `>=` for minimum version constraints
- Pass providers explicitly when needed
- Document provider requirements

❌ **Don't:**
- Include `provider` blocks in child modules
- Use modules with provider blocks with `count`/`for_each`
- Forget to declare provider requirements

### Module Interface

✅ **Do:**
- Use dependency inversion (accept dependencies as inputs)
- Provide sensible defaults
- Add validation to important variables
- Mark sensitive variables and outputs
- Document all variables and outputs
- Expose useful values as outputs

❌ **Don't:**
- Create dependencies internally when they could be injected
- Skip variable validation
- Expose internal implementation details unnecessarily
- Use `any` type unless absolutely necessary

## Quick Reference

**Module Block:**
```hcl
module "name" {
  source  = "./modules/module-name"
  version = "~> 1.0"  # For registry modules

  # Input variables
  variable1 = value1
  variable2 = value2

  # Meta-arguments
  count      = 3
  for_each   = toset(["a", "b"])
  depends_on = [module.other]
  providers  = { aws = aws.west }
}
```

**Standard Module Structure:**
```
terraform-<PROVIDER>-<NAME>/
├── README.md
├── LICENSE
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── modules/
└── examples/
```

**Provider Requirements:**
```hcl
terraform {
  required_version = ">= 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.9"
    }
  }
}
```

**Accessing Child Module Outputs:**
```hcl
module.module_name.output_name
module.module_name[0].output_name  # With count
module.module_name["key"].output_name  # With for_each
```

## References

- **Modules Overview**: <https://developer.hashicorp.com/terraform/language/modules>
- **Module Development**: <https://developer.hashicorp.com/terraform/language/modules/develop>
- **Standard Structure**: <https://developer.hashicorp.com/terraform/language/modules/develop/structure>
- **Module Composition**: <https://developer.hashicorp.com/terraform/language/modules/develop/composition>
- **Providers in Modules**: <https://developer.hashicorp.com/terraform/language/modules/develop/providers>
- **terraform-refactoring** skill for refactoring modules safely
- **terraform-values** skill for variable, local, and output best practices
- **file-structure.instructions.md** for detailed file organization
