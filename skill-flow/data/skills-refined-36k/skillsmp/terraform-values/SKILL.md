---
name: terraform-values
description: 'Manage Terraform values including input variables, local values, and output values. Use when asked about "variables", "locals", "outputs", "input values", "how to pass values", "variable validation", "sensitive values", or when defining module interfaces, reusing expressions, or exposing data. Covers variable types, defaults, validation, precedence, locals usage patterns, and output configuration.'
---

# Terraform Values

Comprehensive guide to managing values in Terraform modules including input variables, local values, and output values. Learn how to create flexible, composable, and reusable modules.

## When to Use This Skill

- User asks about "variables", "locals", "outputs", "input values"
- Questions about "how to pass values to modules"
- "Variable validation", "type constraints", "sensitive values"
- Defining module interfaces and boundaries
- Reusing expressions within modules
- Exposing module data to CLI, HCP Terraform, or other configurations
- Variable precedence and assignment methods

## Value Types Overview

Terraform uses three types of values to manage data flow:

| Type | Purpose | Scope | Reference |
|------|---------|-------|-----------|
| **Variables** | Module inputs | Module-specific | `var.<NAME>` |
| **Locals** | Reusable expressions | Module-scoped | `local.<NAME>` |
| **Outputs** | Module data export | Cross-module | `output.<NAME>` or `module.<NAME>.<OUTPUT>` |

**Value Flow:**
```
Variables (input) → Locals (processing) → Resources → Outputs (export)
```

## Input Variables

Variables define the input interface of your module, letting consumers customize behavior without modifying source code.

### Variable Definition

**Basic Syntax:**
```hcl
variable "name" {
  type        = type_constraint
  description = "Description of the variable"
  default     = default_value
  sensitive   = true/false
  nullable    = true/false
  validation {
    # Validation rules
  }
}
```

**Complete Example:**
```hcl
variable "instance_type" {
  type        = string
  description = "EC2 instance type for the web server"
  default     = "t2.micro"

  validation {
    condition     = can(regex("^t[23]\\.", var.instance_type))
    error_message = "Instance type must be t2 or t3 family."
  }
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID where the web server will be deployed"
  # No default - required input
}

variable "environment" {
  type        = string
  description = "Deployment environment name"
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Variable Arguments

#### type

Specifies the value type constraint:

**Simple Types:**
```hcl
variable "name" {
  type = string
}

variable "count" {
  type = number
}

variable "enabled" {
  type = bool
}
```

**Collection Types:**
```hcl
variable "tags" {
  type = map(string)
}

variable "subnet_ids" {
  type = list(string)
}

variable "ports" {
  type = set(number)
}
```

**Structural Types:**
```hcl
variable "config" {
  type = object({
    name    = string
    port    = number
    enabled = bool
  })
}

variable "instances" {
  type = list(object({
    name = string
    size = string
  }))
}

variable "settings" {
  type = map(object({
    value   = string
    enabled = bool
  }))
}
```

**Optional Attributes:**
```hcl
variable "server" {
  type = object({
    name     = string
    port     = optional(number, 80)      # Default: 80
    enabled  = optional(bool, true)       # Default: true
    tags     = optional(map(string), {})  # Default: {}
  })
}
```

**Any Type:**
```hcl
variable "custom_data" {
  type        = any
  description = "Custom data of any type"
}
```

#### description

Always provide clear descriptions:

```hcl
# ✅ Good - Specific and helpful
variable "subnet_id" {
  type        = string
  description = "Subnet ID where the web server will be deployed"
}

# ❌ Bad - Vague
variable "subnet_id" {
  type        = string
  description = "Subnet"
}
```

#### default

Makes variables optional:

```hcl
# Required variable (no default)
variable "vpc_id" {
  type        = string
  description = "VPC ID for resource deployment"
}

# Optional variable (has default)
variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t2.micro"
}

# Complex default
variable "tags" {
  type        = map(string)
  description = "Resource tags"
  default = {
    Terraform = "true"
    ManagedBy = "terraform"
  }
}
```

#### sensitive

Prevents values from appearing in CLI output:

```hcl
variable "database_password" {
  type        = string
  description = "Password for the RDS database instance"
  sensitive   = true
}
```

**Behavior:**
```bash
$ terraform plan
# Password value not shown in plan output

$ terraform output database_password
database_password = <sensitive>
```

**Warning:** Sensitive values are still stored in state. Use `ephemeral` (Terraform 1.10+) to omit from state entirely.

#### nullable

Controls whether null is accepted:

```hcl
# Allows null (default behavior)
variable "optional_value" {
  type     = string
  nullable = true
  default  = null
}

# Rejects null
variable "required_value" {
  type     = string
  nullable = false
  # If no value provided, Terraform errors
}
```

#### validation

Add custom validation rules:

**Basic Validation:**
```hcl
variable "environment" {
  type        = string
  description = "Deployment environment"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

**Regex Validation:**
```hcl
variable "subnet_id" {
  type        = string
  description = "AWS subnet ID"

  validation {
    condition     = can(regex("^subnet-[a-f0-9]{8,17}$", var.subnet_id))
    error_message = "Subnet ID must be a valid AWS subnet ID format."
  }
}
```

**Numeric Range Validation:**
```hcl
variable "max_size" {
  type        = number
  description = "Maximum cluster size"

  validation {
    condition     = var.max_size >= 1 && var.max_size <= 10
    error_message = "Max size must be between 1 and 10."
  }
}
```

**Multiple Validations:**
```hcl
variable "instance_config" {
  type = object({
    type = string
    size = number
  })

  validation {
    condition     = contains(["t2.micro", "t2.small", "t2.medium"], var.instance_config.type)
    error_message = "Instance type must be t2.micro, t2.small, or t2.medium."
  }

  validation {
    condition     = var.instance_config.size >= 8 && var.instance_config.size <= 100
    error_message = "Instance size must be between 8 and 100 GB."
  }
}
```

**Cross-Field Validation:**
```hcl
variable "min_size" {
  type = number
}

variable "max_size" {
  type = number

  validation {
    condition     = var.max_size >= var.min_size
    error_message = "Max size must be greater than or equal to min size."
  }
}
```

### Referencing Variables

Use `var.<NAME>` syntax:

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id

  tags = {
    Environment = var.environment
    Name        = "${var.environment}-web-server"
  }
}
```

### Assigning Variable Values

#### Value Precedence

Terraform applies variable values in this order (highest to lowest):

1. **Command-line flags** (`-var`, `-var-file`) and HCP Terraform variables
2. **Auto-loaded files** (`*.auto.tfvars`, `*.auto.tfvars.json`) in lexical order
3. **terraform.tfvars.json**
4. **terraform.tfvars**
5. **Environment variables** (`TF_VAR_*`)
6. **Variable default** argument

**Later sources override earlier ones.**

#### Command-Line Variables

```bash
# Single variable
terraform apply -var="instance_type=t3.medium"

# Multiple variables
terraform apply \
  -var="instance_type=t3.medium" \
  -var="environment=prod"

# Complex types (use JSON)
terraform apply -var='subnet_ids=["subnet-12345","subnet-67890"]'
```

#### Variable Definition Files

**Create `.tfvars` files:**

```hcl
# production.tfvars
instance_type     = "t3.large"
environment      = "prod"
subnet_ids       = ["subnet-12345", "subnet-67890"]
enable_monitoring = true
```

**Auto-loaded files:**
- `*.auto.tfvars` (loaded automatically)
- `*.auto.tfvars.json` (loaded automatically)
- `terraform.tfvars` (loaded automatically)
- `terraform.tfvars.json` (loaded automatically)

**Manual loading:**
```bash
terraform apply -var-file="production.tfvars"
```

**JSON format:**
```json
{
  "instance_type": "t3.large",
  "environment": "prod",
  "subnet_ids": ["subnet-12345", "subnet-67890"],
  "enable_monitoring": true
}
```

#### Environment Variables

Use `TF_VAR_` prefix:

```bash
# Simple values
export TF_VAR_instance_type=t3.medium
export TF_VAR_environment=staging

# Complex values (use JSON)
export TF_VAR_subnet_ids='["subnet-12345","subnet-67890"]'
export TF_VAR_config='{"key": "value", "enabled": true}'

terraform apply
```

#### HCP Terraform Variables

Set variables in workspace settings:

- **Terraform Variables** - Input to configuration
- **Environment Variables** - Shell environment (e.g., `AWS_ACCESS_KEY_ID`)
- **Variable Sets** - Reusable groups applied to multiple workspaces

### Variable Best Practices

**Do's:**

✅ **Always add descriptions**
```hcl
variable "instance_type" {
  type        = string
  description = "EC2 instance type for the web server"
  default     = "t2.micro"
}
```

✅ **Use type constraints**
```hcl
variable "tags" {
  type = map(string)
}
```

✅ **Add validation for important values**
```hcl
validation {
  condition     = contains(["dev", "staging", "prod"], var.environment)
  error_message = "Environment must be dev, staging, or prod."
}
```

✅ **Mark sensitive variables**
```hcl
variable "api_key" {
  type      = string
  sensitive = true
}
```

✅ **Provide sensible defaults**
```hcl
variable "enable_monitoring" {
  type    = bool
  default = true
}
```

**Don'ts:**

❌ **Don't hardcode values that should be variables**
```hcl
# Bad
resource "aws_instance" "web" {
  instance_type = "t2.micro"  # Should be var.instance_type
}
```

❌ **Don't skip descriptions**
```hcl
# Bad
variable "x" {
  type = string
}
```

❌ **Don't use `any` type unnecessarily**
```hcl
# Bad - be specific when possible
variable "config" {
  type = any
}

# Good
variable "config" {
  type = object({
    name = string
    port = number
  })
}
```

## Local Values

Locals assign names to expressions, letting you reuse complex calculations and avoid repetition.

### Local Definition

**Basic Syntax:**
```hcl
locals {
  name1 = expression1
  name2 = expression2
}
```

**Examples:**
```hcl
locals {
  # Naming convention
  resource_name = "${var.project_name}-${var.environment}"

  # Process collections
  primary_subnet = var.subnet_ids[0]
  subnet_count   = length(var.subnet_ids)

  # Conditional logic
  is_production      = var.environment == "prod"
  monitoring_enabled = var.monitoring || local.is_production

  # Complex transformations
  tags = merge(
    var.common_tags,
    {
      Name        = local.resource_name
      Environment = var.environment
    }
  )
}
```

### Referencing Locals

Use `local.<NAME>` syntax (singular `local`, not `locals`):

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = local.primary_subnet
  monitoring    = local.monitoring_enabled

  tags = local.tags
}

resource "aws_security_group" "web" {
  name = "${local.resource_name}-sg"

  tags = {
    Name = "${local.resource_name}-security-group"
  }
}
```

### Local Value Patterns

#### Conditional Locals

```hcl
locals {
  # Feature flags
  create_bucket = var.enable_storage && var.bucket_name != null
  use_kms       = var.encryption_enabled && var.kms_key_arn != null

  # Environment-specific settings
  instance_count = var.environment == "prod" ? 3 : 1
  instance_type  = var.environment == "prod" ? "t3.large" : "t2.micro"
}
```

#### Processing Collections

```hcl
locals {
  # Extract values
  subnet_ids = [for s in var.subnets : s.id]

  # Transform collections
  uppercase_tags = {
    for k, v in var.tags : upper(k) => upper(v)
  }

  # Filter collections
  private_subnets = [
    for s in var.subnets : s if s.type == "private"
  ]

  # Flatten nested lists
  all_cidrs = flatten([
    for zone in var.availability_zones : zone.cidrs
  ])
}
```

#### Resource ARN Lists

```hcl
locals {
  # Collect resource ARNs
  bucket_arns = [for b in aws_s3_bucket.buckets : b.arn]

  # Create ARN list from keys
  secret_arns = [
    for name in keys(var.secrets) :
    aws_secretsmanager_secret.secrets[name].arn
  ]

  # Combine multiple sources
  all_arns = concat(
    local.bucket_arns,
    local.secret_arns
  )
}
```

#### Merging Values

```hcl
locals {
  # Merge tags
  common_tags = merge(
    var.default_tags,
    var.additional_tags,
    {
      ManagedBy = "terraform"
      Module    = "web-server"
    }
  )

  # Merge configurations
  full_config = merge(
    var.base_config,
    var.environment_config,
    {
      timestamp = timestamp()
    }
  )
}
```

#### Multiple Locals Blocks

Organize related locals:

```hcl
# Feature flags
locals {
  scaling_enabled     = var.autoscaling != null
  monitoring_enabled  = var.enable_monitoring || local.is_production
  backup_enabled      = var.environment == "prod"
}

# Naming and tagging
locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Complex transformations
locals {
  container_definitions = [
    for container in var.containers : merge(
      container,
      {
        environment = concat(
          container.environment,
          local.default_environment_vars
        )
      }
    )
  ]
}
```

### When to Use Locals

**Use locals when:**
- ✅ Reusing the same expression multiple times
- ✅ Naming a complex expression for clarity
- ✅ Calculating intermediate values
- ✅ Conditional logic based on input variables
- ✅ Processing collections (map, filter, transform)

**Don't use locals when:**
- ❌ Value is used only once (inline instead)
- ❌ Simple variable reference (use var directly)
- ❌ Value should be configurable by users (use variable instead)

**Example - Good Use:**
```hcl
# ✅ Good - reused multiple times
locals {
  common_name = "${var.project}-${var.environment}-${var.region}"
}

resource "aws_instance" "web" {
  tags = { Name = local.common_name }
}

resource "aws_security_group" "web" {
  name = "${local.common_name}-sg"
}
```

**Example - Unnecessary:**
```hcl
# ❌ Bad - used only once, simple value
locals {
  instance_type = var.instance_type
}

resource "aws_instance" "web" {
  instance_type = local.instance_type  # Just use var.instance_type
}
```

### Local Values Best Practices

**Do's:**

✅ **Use descriptive names**
```hcl
locals {
  primary_subnet_id = var.subnet_ids[0]  # Clear purpose
}
```

✅ **Group related locals**
```hcl
# Naming
locals {
  name_prefix = "${var.project}-${var.environment}"
}

# Feature flags
locals {
  create_backup = var.environment == "prod"
}
```

✅ **Document complex logic**
```hcl
locals {
  # Calculate instance count based on environment
  # Production: 3 instances minimum
  # Staging: 2 instances
  # Development: 1 instance
  instance_count = (
    var.environment == "prod" ? max(3, var.instance_count) :
    var.environment == "staging" ? 2 :
    1
  )
}
```

**Don'ts:**

❌ **Don't overuse locals**
```hcl
# Bad - unnecessary local
locals {
  ami = var.ami
}
```

❌ **Don't create circular dependencies**
```hcl
# Error - circular reference
locals {
  a = local.b + 1
  b = local.a + 1
}
```

## Output Values

Outputs expose data from your module for use in CLI, HCP Terraform, parent modules, and remote state.

### Output Definition

**Basic Syntax:**
```hcl
output "name" {
  description = "Description of output"
  value       = expression
  sensitive   = true/false
}
```

**Examples:**
```hcl
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "instance_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.web.private_ip
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}
```

### Output Arguments

#### description

Always include helpful descriptions:

```hcl
# ✅ Good - specific and helpful
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

# ❌ Bad - vague
output "id" {
  description = "ID"
  value       = aws_instance.web.id
}
```

#### value

Can be any valid expression:

```hcl
# Resource attribute
output "instance_arn" {
  description = "ARN of the instance"
  value       = aws_instance.web.arn
}

# Local value
output "resource_name" {
  description = "Computed resource name"
  value       = local.resource_name
}

# Complex expression
output "instance_url" {
  description = "HTTP URL for the instance"
  value       = "http://${aws_instance.web.public_ip}:80"
}

# Map output
output "instance_tags" {
  description = "Tags applied to the instance"
  value       = aws_instance.web.tags
}

# List output
output "subnet_ids" {
  description = "List of subnet IDs"
  value       = aws_subnet.private[*].id
}

# Object output
output "instance_details" {
  description = "Instance configuration details"
  value = {
    id         = aws_instance.web.id
    type       = aws_instance.web.instance_type
    private_ip = aws_instance.web.private_ip
    public_ip  = aws_instance.web.public_ip
  }
}
```

#### sensitive

Prevent values from appearing in CLI output:

```hcl
output "database_password" {
  description = "Auto-generated password for the RDS database"
  value       = aws_db_instance.main.password
  sensitive   = true
}
```

**CLI Behavior:**
```bash
$ terraform output
instance_id       = "i-1234567890abcdef0"
database_password = <sensitive>

# Access with -json or -raw (shows actual value)
$ terraform output -json database_password
"supersecret123"
```

**Warning:** Sensitive outputs are stored in state. Use `-json` or `-raw` flags cautiously.

### Accessing Output Values

#### Root Module Outputs

**CLI Access:**
```bash
# List all outputs
terraform output

# Get specific output
terraform output instance_id

# Get as JSON
terraform output -json

# Get raw value (no quotes)
terraform output -raw instance_ip
```

**HCP Terraform:**
- View outputs on workspace overview page
- Access via API
- Use in run triggers

#### Child Module Outputs

Parent modules access child outputs with `module.<NAME>.<OUTPUT>`:

```hcl
# Child module
module "web_server" {
  source = "./modules/web_server"
  # ...
}

# Access child module outputs
resource "aws_route53_record" "web" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "web.example.com"
  type    = "A"
  records = [module.web_server.instance_ip]
}

resource "aws_cloudwatch_alarm" "web_health" {
  alarm_name = "web-server-health"

  dimensions = {
    InstanceId = module.web_server.instance_id
  }
}

# Use outputs in other module calls
module "monitoring" {
  source = "./modules/monitoring"

  instance_id = module.web_server.instance_id
  instance_ip = module.web_server.instance_ip
}
```

#### Remote State

Access outputs from other Terraform configurations:

```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "web" {
  subnet_id = data.terraform_remote_state.vpc.outputs.private_subnet_id
  vpc_security_group_ids = [
    data.terraform_remote_state.vpc.outputs.web_security_group_id
  ]
}
```

### Output Patterns

#### Exposing Resource IDs

```hcl
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.web.id
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}
```

#### Exposing Collections

```hcl
output "subnet_ids" {
  description = "List of subnet IDs"
  value       = aws_subnet.private[*].id
}

output "instance_arns" {
  description = "Map of instance names to ARNs"
  value = {
    for name, instance in aws_instance.servers :
    name => instance.arn
  }
}
```

#### Exposing Connection Information

```hcl
output "endpoint" {
  description = "Connection endpoint for the database"
  value       = aws_db_instance.main.endpoint
}

output "connection_string" {
  description = "Database connection string"
  value       = "postgresql://${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}"
  sensitive   = true
}
```

#### Exposing for IAM Policies

```hcl
output "bucket_arns" {
  description = "List of S3 bucket ARNs for IAM policy attachment"
  value       = [for b in aws_s3_bucket.buckets : b.arn]
}

output "secret_arns" {
  description = "List of secret ARNs for task execution role"
  value       = [for s in aws_secretsmanager_secret.secrets : s.arn]
}
```

#### Conditional Outputs

```hcl
output "load_balancer_dns" {
  description = "DNS name of the load balancer (if created)"
  value       = var.create_lb ? aws_lb.main[0].dns_name : null
}

output "monitoring_dashboard" {
  description = "CloudWatch dashboard URL (if monitoring enabled)"
  value = var.enable_monitoring ? (
    "https://console.aws.amazon.com/cloudwatch/home?region=${var.region}#dashboards:name=${aws_cloudwatch_dashboard.main[0].dashboard_name}"
  ) : null
}
```

### Output Best Practices

**Do's:**

✅ **Always add descriptions**
```hcl
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}
```

✅ **Mark sensitive outputs**
```hcl
output "api_key" {
  description = "API key for service authentication"
  value       = random_password.api_key.result
  sensitive   = true
}
```

✅ **Expose useful values for integration**
```hcl
output "instance_id" {
  description = "Instance ID for CloudWatch alarms"
  value       = aws_instance.web.id
}
```

✅ **Use descriptive output names**
```hcl
# Good
output "web_server_public_ip" {}

# Bad
output "ip" {}
```

**Don'ts:**

❌ **Don't expose internal implementation details unnecessarily**
```hcl
# Bad - internal detail
output "lambda_execution_role_id" {
  value = aws_iam_role.internal_lambda.id
}
```

❌ **Don't skip descriptions**
```hcl
# Bad
output "id" {
  value = aws_instance.web.id
}
```

❌ **Don't expose secrets without marking sensitive**
```hcl
# Bad - password visible in output
output "db_password" {
  value = aws_db_instance.main.password
}

# Good
output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```

## Value Flow Example

Complete example showing variables → locals → outputs:

```hcl
# ===== Variables (Input) =====
variable "project_name" {
  type        = string
  description = "Name of the project"
}

variable "environment" {
  type        = string
  description = "Deployment environment"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "subnet_ids" {
  type        = list(string)
  description = "List of subnet IDs"
}

variable "enable_monitoring" {
  type        = bool
  description = "Enable CloudWatch monitoring"
  default     = false
}

# ===== Locals (Processing) =====
locals {
  # Naming
  resource_name = "${var.project_name}-${var.environment}"

  # Subnet selection
  primary_subnet = var.subnet_ids[0]

  # Feature flags
  is_production      = var.environment == "prod"
  monitoring_enabled = var.enable_monitoring || local.is_production

  # Tags
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# ===== Resources =====
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = local.primary_subnet
  monitoring    = local.monitoring_enabled

  tags = merge(
    local.common_tags,
    {
      Name = local.resource_name
      Role = "web-server"
    }
  )
}

# ===== Outputs (Export) =====
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "instance_private_ip" {
  description = "Private IP address of the instance"
  value       = aws_instance.web.private_ip
}

output "resource_name" {
  description = "Computed resource name"
  value       = local.resource_name
}

output "tags" {
  description = "Common tags applied to resources"
  value       = local.common_tags
}
```

## Best Practices Summary

### Variables

✅ **Do:**
- Add descriptions to all variables
- Use type constraints
- Provide sensible defaults
- Add validation for important values
- Mark sensitive variables
- Document expected formats in descriptions

❌ **Don't:**
- Hardcode values that should be variables
- Skip descriptions
- Use `any` type unnecessarily
- Forget validation for enums

### Locals

✅ **Do:**
- Use for reused expressions
- Name complex calculations clearly
- Group related locals
- Document complex logic
- Use for intermediate calculations

❌ **Don't:**
- Overuse for simple values
- Create circular dependencies
- Use when a variable is more appropriate
- Use for values needed only once

### Outputs

✅ **Do:**
- Add descriptions to all outputs
- Mark sensitive outputs
- Expose values useful for integration
- Use descriptive names
- Group related outputs

❌ **Don't:**
- Expose unnecessary internal details
- Skip descriptions
- Expose secrets without `sensitive = true`
- Use cryptic output names

## Quick Reference

**Variable Definition:**
```hcl
variable "name" {
  type        = string
  description = "..."
  default     = "value"
  sensitive   = false
  validation {
    condition     = ...
    error_message = "..."
  }
}
```

**Variable Reference:**
```hcl
var.name
```

**Local Definition:**
```hcl
locals {
  name = expression
}
```

**Local Reference:**
```hcl
local.name
```

**Output Definition:**
```hcl
output "name" {
  description = "..."
  value       = expression
  sensitive   = false
}
```

**Output Access:**
```hcl
# CLI
terraform output name

# Child module
module.module_name.output_name

# Remote state
data.terraform_remote_state.name.outputs.output_name
```

## References

- **Values Overview**: <https://developer.hashicorp.com/terraform/language/values>
- **Variables**: <https://developer.hashicorp.com/terraform/language/values/variables>
- **Locals**: <https://developer.hashicorp.com/terraform/language/values/locals>
- **Outputs**: <https://developer.hashicorp.com/terraform/language/values/outputs>
- **Type Constraints**: <https://developer.hashicorp.com/terraform/language/expressions/type-constraints>
- **terraform-syntax** skill for HCL expression syntax
- **terraform.instructions.md** for module development guidelines
- **documentation.instructions.md** for variable/output documentation standards
