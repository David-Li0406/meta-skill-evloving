---
name: terraform-resources
description: 'Configure and manage Terraform resources including naming patterns, dynamic blocks, conditional creation, meta-arguments, lifecycle management, and dependencies. Use when asked about "resource configuration", "dynamic blocks", "count/for_each", "depends_on", "lifecycle blocks", "resource naming", or managing infrastructure resources. Covers resource declaration, meta-arguments, dependencies, timeouts, and destruction patterns.'
---

# Terraform Resource Configuration and Management

Comprehensive guide to declaring, configuring, and managing Terraform resources including naming conventions, dynamic blocks, conditional creation, meta-arguments, lifecycle management, and dependencies.

## When to Use This Skill

- User asks about "resource configuration", "how to create resources"
- Questions about "dynamic blocks", "for_each in resources", "conditional resources"
- "Resource naming", "naming conventions", "this resource pattern"
- "Meta-arguments", "count", "for_each", "depends_on", "lifecycle"
- "Resource dependencies", "implicit vs explicit dependencies"
- Resource lifecycle management, timeouts, destroy patterns
- Working with terraform_data or local-only resources

## Resource Fundamentals

### What is a Resource

A **resource** is any infrastructure object you want to create and manage with Terraform, including:
- Virtual networks (VPCs, subnets, route tables)
- Compute instances (EC2, ECS tasks, Lambda functions)
- Storage (S3 buckets, EBS volumes, databases)
- Security (security groups, IAM roles/policies)
- DNS records, load balancers, monitoring, etc.

**Key Characteristics:**
- Defined using `resource` blocks in `.tf` files
- Managed by provider plugins (AWS, Google, Azure, etc.)
- Tracked in Terraform state
- Created, updated, and destroyed based on configuration

### Resource Block Structure

**Basic Syntax:**
```hcl
resource "<RESOURCE_TYPE>" "<LOCAL_NAME>" {
  # Meta-arguments (if any)
  count      = 2
  for_each   = toset(["a", "b"])
  depends_on = [other_resource.name]
  provider   = aws.west

  # Required arguments
  required_arg_1 = "value"
  required_arg_2 = "value"

  # Optional arguments
  optional_arg = "value"

  # Nested blocks
  nested_block {
    nested_arg = "value"
  }

  # Lifecycle block (if needed)
  lifecycle {
    create_before_destroy = true
  }
}
```

**Components:**
- **Resource Type**: Determines provider and kind of infrastructure (e.g., `aws_instance`, `google_storage_bucket`)
- **Local Name**: Identifier used within configuration (e.g., `web`, `database`)
- **Resource Address**: Combination of type and name (e.g., `aws_instance.web`)

## Resource Naming Conventions

### Primary Resources

Use `this` for the module's primary/single resource:

```hcl
# ✅ Good - primary resource uses "this"
resource "aws_ecs_service" "this" {
  name = module.label.id
  # ...
}

resource "aws_lb" "this" {
  name = module.label.id
  # ...
}

resource "aws_s3_bucket" "this" {
  bucket = module.label.id
  # ...
}
```

**When to use `this`:**
- Module creates one main resource of a type
- The resource is the module's primary purpose
- Clear what "this" refers to in context

### Multiple/Supporting Resources

Use descriptive identifiers that convey **purpose**, not type:

```hcl
# ✅ Good - identifier describes purpose
resource "aws_iam_role" "execution" {
  name = "${module.label.id}-execution"
  # Role for ECS task execution
}

resource "aws_iam_role" "task" {
  name = "${module.label.id}-task"
  # Role for ECS task
}

resource "aws_security_group" "alb" {
  name = "${module.label.id}-alb"
  # Security group for load balancer
}

resource "aws_security_group" "ecs" {
  name = "${module.label.id}-ecs"
  # Security group for ECS tasks
}

resource "aws_iam_role_policy_attachment" "execution_ecr_public" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}
```

**❌ Bad - Identifier duplicates resource type:**
```hcl
# ❌ Redundant naming
resource "aws_iam_role" "role" {
  # Type already says it's a role
}

resource "aws_security_group" "security_group" {
  # Redundant and uninformative
}

resource "aws_s3_bucket" "bucket" {
  # What bucket? For what purpose?
}
```

**Naming Guidelines:**
- Name describes **purpose** or **function**
- Don't repeat resource type in name
- Use clear, descriptive names
- Consider what the resource is **for**

## Meta-Arguments

Meta-arguments are built into Terraform and work with any resource type. They configure **how** Terraform manages resources, not the resource behavior itself.

### count

Create multiple instances of a resource:

```hcl
# Create 3 instances
resource "aws_instance" "web" {
  count = 3

  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name = "web-${count.index}"
  }
}

# Access specific instance
output "first_instance_id" {
  value = aws_instance.web[0].id
}

# Access all instances
output "all_instance_ids" {
  value = aws_instance.web[*].id
}
```

**Conditional Creation with count:**
```hcl
resource "aws_appautoscaling_target" "this" {
  count = var.enable_autoscaling ? 1 : 0

  # Configuration only created if enable_autoscaling is true
  max_capacity       = var.max_capacity
  min_capacity       = var.min_capacity
  resource_id        = "service/${var.cluster_name}/${var.service_name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# Use one() to convert single-element list to value
output "scaling_target_id" {
  value = try(one(aws_appautoscaling_target.this).id, null)
}
```

**count Patterns:**
```hcl
# Binary creation (0 or 1)
count = var.create_resource ? 1 : 0

# Complex condition
count = var.enabled && var.condition_met ? 1 : 0

# Multiple resources from list length
count = length(var.subnet_ids)

# Fixed number
count = 3
```

### for_each

Create named instances using a map or set:

```hcl
# Using a set
resource "aws_s3_bucket" "buckets" {
  for_each = toset(["logs", "data", "backups"])

  bucket = "${var.project}-${each.key}"

  tags = {
    Purpose = each.key
  }
}

# Access specific bucket
output "logs_bucket_arn" {
  value = aws_s3_bucket.buckets["logs"].arn
}

# Using a map
resource "aws_iam_role" "roles" {
  for_each = {
    execution = "ecs-tasks.amazonaws.com"
    task      = "ecs-tasks.amazonaws.com"
    lambda    = "lambda.amazonaws.com"
  }

  name               = "${var.project}-${each.key}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = each.value
      }
    }]
  })
}
```

**for_each with Objects:**
```hcl
# Complex object iteration
variable "secrets" {
  type = map(object({
    description = string
    kms_key_id  = optional(string)
  }))
}

resource "aws_secretsmanager_secret" "secrets" {
  for_each = var.secrets

  name        = "${var.project}-${each.key}"
  description = each.value.description
  kms_key_id  = each.value.kms_key_id

  tags = {
    Name = each.key
  }
}
```

**count vs for_each:**

| Use Case | Use `count` | Use `for_each` |
|----------|-------------|----------------|
| Binary creation (0 or 1) | ✅ Yes | ❌ No |
| Fixed number of instances | ✅ Yes | ⚠️ Possible |
| Named instances from map/set | ❌ No | ✅ Yes |
| Complex objects | ⚠️ Difficult | ✅ Yes |
| Removing middle item | ❌ Reindexes | ✅ Stable |

**Important:** Cannot use both `count` and `for_each` on the same resource.

### depends_on

Explicitly define dependencies between resources:

```hcl
# Implicit dependency (preferred)
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id  # Terraform detects dependency
  cidr_block = "10.0.1.0/24"
}

# Explicit dependency (use when necessary)
resource "aws_iam_role_policy" "policy" {
  role = aws_iam_role.role.name

  # IAM policy must be created after role is fully ready
  depends_on = [
    aws_iam_role.role
  ]
}

# Hidden dependency example
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type

  # Instance needs IAM instance profile to exist first,
  # but there's no direct reference to the profile itself
  depends_on = [
    aws_iam_role_policy_attachment.instance_policy
  ]
}
```

**When to use depends_on:**
- ✅ Hidden dependencies (no direct attribute reference)
- ✅ Ordering requirements not captured by references
- ✅ IAM policy application before resource creation
- ✅ Network routing before instance creation
- ❌ **Don't use** when implicit dependency (attribute reference) works
- ❌ **Don't overuse** - prefer implicit dependencies

### provider

Specify which provider configuration to use:

```hcl
# Multiple provider configurations
provider "aws" {
  region = "us-west-1"
}

provider "aws" {
  alias  = "east"
  region = "us-east-1"
}

# Use specific provider
resource "aws_instance" "west" {
  provider = aws       # Uses default (us-west-1)
  # ...
}

resource "aws_instance" "east" {
  provider = aws.east  # Uses aliased provider (us-east-1)
  # ...
}

# Cross-region replication
resource "aws_s3_bucket" "source" {
  provider = aws
  bucket   = "source-bucket"
}

resource "aws_s3_bucket" "replica" {
  provider = aws.east
  bucket   = "replica-bucket"
}

resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws

  bucket = aws_s3_bucket.source.id
  role   = aws_iam_role.replication.arn

  rule {
    status = "Enabled"
    destination {
      bucket = aws_s3_bucket.replica.arn
    }
  }
}
```

**Best Practices:**
- Default provider (no alias) used when `provider` argument omitted
- Explicit `provider` argument for multi-region/multi-account scenarios
- Document why specific provider configuration is needed

## Lifecycle Meta-Argument

The `lifecycle` block controls how Terraform handles resource changes.

### create_before_destroy

Create replacement before destroying old resource:

```hcl
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true
  }
}
```

**When to use:**
- Zero-downtime deployments
- Resources referenced by others (avoid broken references)
- Blue-green deployment patterns

### prevent_destroy

Prevent accidental destruction:

```hcl
resource "aws_s3_bucket" "important_data" {
  bucket = "critical-production-data"

  lifecycle {
    prevent_destroy = true
  }
}
```

**When to use:**
- Production databases
- Critical data storage
- Resources that should never be deleted
- Add manual override process for intentional deletion

### ignore_changes

Ignore changes to specific attributes:

```hcl
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name = "web-server"
  }

  lifecycle {
    # Ignore tags changes (manual changes won't be overwritten)
    ignore_changes = [
      tags,
    ]
  }
}

# Ignore all changes
resource "aws_ami_copy" "example" {
  name              = "my-ami"
  source_ami_id     = var.source_ami_id
  source_ami_region = "us-west-1"

  lifecycle {
    ignore_changes = all
  }
}
```

**Common use cases:**
- Auto-scaling groups modify instance count
- Tags managed outside Terraform
- Attributes modified by external systems

### replace_triggered_by

Force replacement when referenced resource changes:

```hcl
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type

  lifecycle {
    replace_triggered_by = [
      # Replace instance when AMI changes
      aws_ami_copy.app.id
    ]
  }
}

# Replace when any attribute of another resource changes
resource "aws_ecs_service" "app" {
  name = "app-service"
  # ...

  lifecycle {
    replace_triggered_by = [
      aws_ecs_task_definition.app
    ]
  }
}
```

### precondition and postcondition

Validate assumptions and guarantees:

```hcl
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type

  # Validate input before creation
  lifecycle {
    precondition {
      condition     = data.aws_ami.example.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }

    precondition {
      condition     = can(regex("^ami-", var.ami))
      error_message = "AMI ID must be valid format (ami-xxx)."
    }
  }
}

# Validate output after creation
resource "aws_db_instance" "database" {
  # ...

  lifecycle {
    postcondition {
      condition     = self.encrypted == true
      error_message = "Database must be encrypted."
    }

    postcondition {
      condition     = self.backup_retention_period >= 7
      error_message = "Backup retention must be at least 7 days."
    }
  }
}
```

## Dynamic Blocks

Dynamic blocks generate nested blocks from complex values. **For HCL syntax details, see the **terraform-syntax** skill.**

### Basic Dynamic Block

```hcl
# Without dynamic - repetitive
resource "aws_security_group" "example" {
  name = "example"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# With dynamic - concise
resource "aws_security_group" "example" {
  name = "example"

  dynamic "ingress" {
    for_each = [80, 443]

    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

### Dynamic Blocks with Objects

```hcl
variable "ingress_rules" {
  type = list(object({
    description = string
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  default = [
    {
      description = "HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      description = "HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
}

resource "aws_security_group" "web" {
  name = "web-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      description = ingress.value.description
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

### Conditional Dynamic Blocks

```hcl
# Optional nested block
resource "aws_lb" "example" {
  name               = "example-lb"
  load_balancer_type = "application"

  # Only create access_logs block if enabled
  dynamic "access_logs" {
    for_each = var.enable_access_logs ? [1] : []

    content {
      bucket  = var.access_logs_bucket
      enabled = true
      prefix  = var.access_logs_prefix
    }
  }
}

# With local for clarity
locals {
  enable_access_logs = var.enable_access_logs && var.access_logs_bucket != null
}

resource "aws_lb" "example" {
  name               = "example-lb"
  load_balancer_type = "application"

  dynamic "access_logs" {
    for_each = local.enable_access_logs ? [1] : []

    content {
      bucket  = var.access_logs_bucket
      enabled = var.enable_access_logs
      prefix  = var.access_logs_prefix
    }
  }
}
```

### Nested Dynamic Blocks

```hcl
variable "load_balancer_rules" {
  type = list(object({
    priority = number
    conditions = list(object({
      field  = string
      values = list(string)
    }))
    actions = list(object({
      type             = string
      target_group_arn = string
    }))
  }))
}

resource "aws_lb_listener_rule" "rules" {
  for_each = { for idx, rule in var.load_balancer_rules : idx => rule }

  listener_arn = aws_lb_listener.main.arn
  priority     = each.value.priority

  dynamic "condition" {
    for_each = each.value.conditions

    content {
      dynamic "path_pattern" {
        for_each = condition.value.field == "path-pattern" ? [1] : []

        content {
          values = condition.value.values
        }
      }

      dynamic "host_header" {
        for_each = condition.value.field == "host-header" ? [1] : []

        content {
          values = condition.value.values
        }
      }
    }
  }

  dynamic "action" {
    for_each = each.value.actions

    content {
      type             = action.value.type
      target_group_arn = action.value.target_group_arn
    }
  }
}
```

### Dynamic Block Best Practices

**Do's:**
✅ Use for optional nested blocks
✅ Use for repeating configuration from input variables
✅ Keep iterator name same as block type (default behavior)
✅ Use locals for complex conditions

**Don'ts:**
❌ Overuse dynamic blocks (hurts readability)
❌ Use when static blocks are clearer
❌ Nest too deeply (max 2-3 levels)

## Resource Dependencies

### Implicit Dependencies

Terraform automatically detects dependencies from attribute references:

```hcl
# VPC created first (no dependencies)
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Subnet depends on VPC (implicit)
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id  # Reference creates dependency
  cidr_block = "10.0.1.0/24"
}

# Security group depends on VPC (implicit)
resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id  # Reference creates dependency
  name   = "web-sg"
}

# Instance depends on subnet and security group (implicit)
resource "aws_instance" "web" {
  ami             = var.ami
  instance_type   = var.instance_type
  subnet_id       = aws_subnet.private.id          # Dependency
  security_groups = [aws_security_group.web.id]    # Dependency
}
```

**Terraform automatically creates a dependency graph:**
1. `aws_vpc.main` (no dependencies)
2. `aws_subnet.private` and `aws_security_group.web` (parallel, both depend on VPC)
3. `aws_instance.web` (depends on subnet and security group)

### Explicit Dependencies

Use `depends_on` for hidden dependencies:

```hcl
# IAM policy attachment before instance creation
resource "aws_iam_role" "instance" {
  name = "instance-role"
  # assume role policy...
}

resource "aws_iam_role_policy_attachment" "instance_ssm" {
  role       = aws_iam_role.instance.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "instance" {
  name = "instance-profile"
  role = aws_iam_role.instance.name
}

resource "aws_instance" "web" {
  ami                  = var.ami
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.instance.name

  # Policy must be attached before instance starts
  # (no direct reference to policy attachment)
  depends_on = [
    aws_iam_role_policy_attachment.instance_ssm
  ]
}
```

**Common Hidden Dependencies:**
- IAM policy attachments before resource creation
- Route table associations before launching instances
- VPN connections before routing traffic
- DNS propagation before service registration

### Dependency Best Practices

**Prefer Implicit Dependencies:**
```hcl
# ✅ Good - implicit dependency
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.main.id
}

# ❌ Unnecessary - explicit when implicit works
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.main.id

  depends_on = [aws_vpc.main]  # Redundant
}
```

**Use depends_on Sparingly:**
```hcl
# ✅ Good - hidden dependency
resource "aws_instance" "web" {
  # ...

  depends_on = [
    aws_iam_role_policy_attachment.policy
  ]
}

# ❌ Bad - overuse obscures real dependencies
resource "aws_instance" "web" {
  # ...

  depends_on = [
    aws_vpc.main,              # Unnecessary
    aws_subnet.private,        # Unnecessary
    aws_security_group.web,    # Unnecessary
    aws_iam_role.instance,     # Unnecessary
  ]
}
```

## Operation Timeouts

Customize how long Terraform waits for operations:

```hcl
resource "aws_db_instance" "database" {
  identifier = "production-db"
  # ... database configuration

  timeouts {
    create = "60m"   # 60 minutes to create
    update = "60m"   # 60 minutes to update
    delete = "2h"    # 2 hours to delete
  }
}

resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type

  timeouts {
    create = "10m"
    delete = "10m"
  }
}
```

**Timeout Format:**
- `"60s"` - 60 seconds
- `"10m"` - 10 minutes
- `"2h"` - 2 hours
- `"1h30m"` - 1 hour 30 minutes

**When to Use:**
- Large databases taking long to provision
- Resources with complex initialization
- Resources with slow deletion processes
- Override default provider timeouts

**Note:** Not all resources support `timeouts`. Check provider documentation.

## Null Safety and Type Checking

### Using try()

Handle potentially null values safely:

```hcl
# Safely access nested attributes
output "service_discovery_name" {
  value = try(
    aws_ecs_service.this.service_connect_configuration[0].service[0].discovery_name,
    null
  )
}

# Provide fallback value
locals {
  container_memory = try(
    var.container_definitions[0].memory,
    var.default_memory
  )
}

# Chain multiple attempts
locals {
  db_endpoint = try(
    aws_db_instance.primary.endpoint,
    aws_db_instance.replica.endpoint,
    "localhost:5432"
  )
}
```

### Using one()

Extract single element from single-element list (recommended for count-based resources):

```hcl
# Resource created conditionally with count
resource "aws_appautoscaling_target" "this" {
  count = var.enable_autoscaling ? 1 : 0
  # ...
}

# ✅ Best practice - use one() with try()
output "scaling_target_id" {
  value = try(one(aws_appautoscaling_target.this).id, null)
}

# ✅ Good - use one() with ternary
output "scaling_target_arn" {
  value = var.enable_autoscaling ? one(aws_appautoscaling_target.this).arn : null
}

# ❌ Avoid - direct [0] indexing is less safe
output "scaling_target_id_old" {
  value = var.enable_autoscaling ? aws_appautoscaling_target.this[0].id : null
  # No validation that list has exactly 1 element
}
```

**Why one() is better than [0]:**
- **Semantically clear**: Makes it explicit you expect exactly 1 element
- **Better error messages**: Fails with clear error if list doesn't have exactly 1 element
- **Type safety**: Converts list type to element type
- **Runtime validation**: Catches configuration errors early

**Reference:** [Terraform one() function](https://developer.hashicorp.com/terraform/language/functions/one)

### Using contains() and lookup()

Safe key checking:

```hcl
# Check if key exists in object
locals {
  container_definitions = [
    for def in var.container_definitions : {
      name   = def.name
      image  = def.image
      cpu    = def.cpu
      memory = contains(keys(def), "memory") ? def.memory : null
    }
  ]
}

# Safe map lookup with default
locals {
  environment_config = lookup(
    var.environment_configs,
    var.environment,
    var.default_config
  )
}
```

## Built-in Resources

### terraform_data

Generic resource for managing arbitrary data:

```hcl
# Trigger replacement based on input changes
resource "terraform_data" "replacement" {
  input = var.trigger_value
}

resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type

  lifecycle {
    replace_triggered_by = [
      terraform_data.replacement
    ]
  }
}

# Store computed values
resource "terraform_data" "configuration" {
  input = {
    timestamp = timestamp()
    version   = var.app_version
  }
}

output "deployment_info" {
  value = terraform_data.configuration.output
}
```

### Local-Only Resources

Resources that exist only in Terraform state:

```hcl
# Random values
resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "data" {
  bucket = "data-${random_id.bucket_suffix.hex}"
}

# TLS certificates
resource "tls_private_key" "ca" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_self_signed_cert" "ca" {
  private_key_pem = tls_private_key.ca.private_key_pem

  subject {
    common_name  = "example.com"
    organization = "Example Inc"
  }

  validity_period_hours = 8760  # 1 year

  allowed_uses = [
    "cert_signing",
    "crl_signing",
  ]
}

# Random passwords
resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db.id
  secret_string = random_password.db_password.result
}
```

## Resource Destruction

### Destroy Single Resource

Remove resource from configuration and apply:

```hcl
# Step 1: Delete resource block
# resource "aws_instance" "old" {
#   ami           = "ami-12345678"
#   instance_type = "t2.micro"
# }

# Step 2: Remove references
# output "old_instance_id" {
#   value = aws_instance.old.id
# }

# Step 3: Run terraform apply
# Terraform destroys the resource and removes from state
```

### Destroy All Infrastructure

```bash
# Destroy all resources in current configuration
terraform destroy

# Destroy specific resources
terraform destroy -target=aws_instance.web

# Destroy multiple specific resources
terraform destroy \
  -target=aws_instance.web \
  -target=aws_s3_bucket.logs
```

### Destroy-Time Provisioners

Use `removed` block for destroy-time operations:

```hcl
# Original resource (to be removed)
# resource "aws_instance" "web" {
#   ami           = var.ami
#   instance_type = var.instance_type
# }

# Replace with removed block
removed {
  from = aws_instance.web

  lifecycle {
    destroy = false  # Don't destroy, just remove from state
  }

  provisioner "local-exec" {
    when    = destroy
    command = "echo 'Instance ${self.id} is being removed'"
  }
}
```

## Argument Ordering in Resource Blocks

Follow consistent ordering for readability:

```hcl
resource "aws_instance" "example" {
  # 1. Meta-arguments first
  count    = 2
  for_each = toset(["a", "b"])
  provider = aws.west

  # 2. Required arguments
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  # 3. Optional arguments (alphabetical or logical groups)
  associate_public_ip_address = false
  monitoring                  = true
  subnet_id                   = var.subnet_id

  # 4. Nested blocks
  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  # 5. Tags
  tags = module.label.tags

  # 6. Lifecycle block last
  lifecycle {
    create_before_destroy = true
  }
}
```

## Common Patterns

### Conditional Resource Creation

```hcl
# Pattern 1: count with boolean
resource "aws_s3_bucket" "logs" {
  count = var.enable_logging ? 1 : 0

  bucket = "${var.name}-logs"
}

# Pattern 2: count with complex condition
locals {
  create_logs = var.enable_logging && var.log_destination == "s3"
}

resource "aws_s3_bucket" "logs" {
  count = local.create_logs ? 1 : 0

  bucket = "${var.name}-logs"
}

# Pattern 3: for_each with conditional map
locals {
  buckets = var.enable_logging ? {
    logs    = "logs"
    backups = "backups"
  } : {}
}

resource "aws_s3_bucket" "storage" {
  for_each = local.buckets

  bucket = "${var.name}-${each.value}"
}
```

### Resource Collections

```hcl
# Create multiple related resources
resource "aws_subnet" "private" {
  for_each = {
    for idx, cidr in var.private_subnet_cidrs :
    "private-${idx}" => {
      cidr = cidr
      az   = var.availability_zones[idx]
    }
  }

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az

  tags = {
    Name = "${var.name}-${each.key}"
    Tier = "private"
  }
}

# Reference the collection
output "private_subnet_ids" {
  value = [for subnet in aws_subnet.private : subnet.id]
}
```

### Resource Factories

```hcl
# Variable defines multiple resources
variable "databases" {
  type = map(object({
    instance_class = string
    allocated_storage = number
    engine_version = string
  }))
  default = {
    primary = {
      instance_class    = "db.t3.medium"
      allocated_storage = 100
      engine_version    = "13.7"
    }
    analytics = {
      instance_class    = "db.t3.large"
      allocated_storage = 500
      engine_version    = "13.7"
    }
  }
}

# Create all databases
resource "aws_db_instance" "databases" {
  for_each = var.databases

  identifier        = "${var.project}-${each.key}"
  instance_class    = each.value.instance_class
  allocated_storage = each.value.allocated_storage
  engine            = "postgres"
  engine_version    = each.value.engine_version

  username = var.db_username
  password = var.db_password

  tags = {
    Name    = each.key
    Purpose = each.key
  }
}
```

## Best Practices Summary

### Resource Configuration

✅ **Do:**
- Use `this` for primary resources
- Use descriptive names for supporting resources
- Follow consistent argument ordering
- Use implicit dependencies when possible
- Add lifecycle blocks when needed
- Document complex conditional logic
- Use dynamic blocks for optional/repeating blocks

❌ **Don't:**
- Duplicate resource type in name (`resource "aws_role" "role"`)
- Overuse `depends_on` (prefer implicit)
- Mix `count` and `for_each` on same resource
- Nest dynamic blocks too deeply
- Ignore null safety (use `try()`, `one()`)
- Hardcode values that should be variables

### Meta-Arguments

✅ **Do:**
- Use `count` for binary creation (0 or 1)
- Use `for_each` for named instances
- Document why explicit dependencies exist
- Use lifecycle blocks for special requirements
- Order meta-arguments first in block

❌ **Don't:**
- Use both `count` and `for_each`
- Use `depends_on` when implicit works
- Forget to handle null values from count resources
- Ignore preconditions/postconditions for validation

### Dynamic Blocks

✅ **Do:**
- Use for optional nested blocks
- Use for repeating configuration from variables
- Keep conditions in locals for clarity
- Document complex dynamic patterns

❌ **Don't:**
- Overuse (hurts readability)
- Use when static blocks clearer
- Nest more than 2-3 levels deep

## Quick Reference

**Resource Block:**
```hcl
resource "type" "name" {
  count      = 1
  for_each   = {}
  depends_on = []
  provider   = provider.alias

  # Arguments
  arg = "value"

  # Nested blocks
  block {}

  # Dynamic blocks
  dynamic "block" {
    for_each = var.items
    content {}
  }

  # Lifecycle
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
    ignore_changes        = []
    replace_triggered_by  = []

    precondition {}
    postcondition {}
  }
}
```

**Referencing Resources:**
```hcl
resource.name.attribute              # Single resource
resource.name[0].attribute           # count resource
resource.name["key"].attribute       # for_each resource
resource.name[*].attribute           # All instances (splat)
```

**Common Functions:**
```hcl
try(expr1, expr2, default)           # Safe access
one(list)                            # Single element
contains(list, value)                # Check existence
lookup(map, key, default)            # Safe map access
```

## References

- **Resource Configuration**: <https://developer.hashicorp.com/terraform/language/resources/configure>
- **Resource Destruction**: <https://developer.hashicorp.com/terraform/language/resources/destroy>
- **Providers in Modules**: <https://developer.hashicorp.com/terraform/language/modules/develop/providers>
- **Resource Block Reference**: <https://developer.hashicorp.com/terraform/language/block/resource>
- **Meta-Arguments**: <https://developer.hashicorp.com/terraform/language/meta-arguments>
- **terraform-syntax** skill for HCL expressions and functions
- **terraform-values** skill for variables, locals, outputs
- **terraform-modules** skill for module development patterns
- **terraform-refactoring** skill for safe resource refactoring
