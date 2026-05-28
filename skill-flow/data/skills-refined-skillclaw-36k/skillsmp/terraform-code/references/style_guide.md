# HashiCorp Terraform Style Guide

## Formatting Rules

### Indentation
- Use **2 spaces** for each nesting level
- Never use tabs
- Maintain consistent indentation throughout all files

### Alignment
- Align equals signs (`=`) when multiple arguments appear on consecutive lines at the same nesting level
- Example:
  ```hcl
  resource "aws_instance" "web" {
    ami           = "ami-abc123"
    instance_type = "t2.micro"

    tags = {
      Name = "web-server"
    }
  }
  ```

### Block Organization
1. Meta-arguments first (`count`, `for_each`, `provider`, `lifecycle`, `depends_on`)
2. Regular arguments
3. Nested blocks
4. Separate meta-arguments from regular arguments with one blank line
5. Separate nested blocks with blank lines

Example:
```hcl
resource "aws_instance" "example" {
  count = 3

  ami           = "ami-abc123"
  instance_type = "t2.micro"

  network_interface {
    # ...
  }

  lifecycle {
    create_before_destroy = true
  }
}
```

### Spacing
- Separate top-level blocks with one blank line
- Use blank lines to group related arguments within blocks

## Naming Conventions

### Resource Names
- Use **descriptive nouns**
- Separate words with **underscores** (snake_case)
- **Do NOT** include the resource type in the identifier
- **Do NOT** use hyphens

✅ **Correct:**
```hcl
resource "aws_instance" "web_server" { }
resource "aws_security_group" "api_access" { }
```

❌ **Incorrect:**
```hcl
resource "aws_instance" "web-server" { }          # Hyphens not allowed
resource "aws_instance" "aws_instance_web" { }   # Redundant type
resource "aws_security_group" "apiAccess" { }    # camelCase not preferred
```

### Variables and Outputs
- Follow the same underscore-separated naming pattern
- Use descriptive nouns
- Example: `vpc_id`, `database_endpoint`, `instance_count`

### Modules
- Use lowercase and hyphens for module names
- Example: `terraform-aws-vpc`, `database-cluster`

## File Organization

Organize Terraform code into these standard files:

### Core Files
- **`terraform.tf`** - Terraform and provider version constraints
- **`providers.tf`** - Provider blocks and configuration
- **`main.tf`** - Primary resources and data sources
- **`variables.tf`** - Input variable declarations (alphabetically ordered)
- **`outputs.tf`** - Output value declarations (alphabetically ordered)
- **`locals.tf`** - Local value definitions

### Optional Files
- **`backend.tf`** - Backend configuration (if using remote state)
- **`data.tf`** - Data source definitions (if many data sources)
- **`versions.tf`** - Alternative to terraform.tf for version constraints

### Logical Organization (for larger projects)
Split by functional area when appropriate:
- `network.tf` - VPC, subnets, routing
- `compute.tf` - EC2, ASG, launch templates
- `storage.tf` - S3, EBS volumes
- `database.tf` - RDS, DynamoDB
- `security.tf` - Security groups, IAM roles

## Variable and Output Best Practices

### Variables
Every variable must have:
1. **Type** - Specify the variable type
2. **Description** - Clear explanation of purpose
3. **Default** (optional) - Reasonable default value when appropriate

```hcl
variable "instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 1
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "database_password" {
  description = "Master password for database"
  type        = string
  sensitive   = true
}
```

### Outputs
Every output should have:
1. **Description** - Explain the output's purpose
2. **Sensitive flag** - Mark sensitive data appropriately

```hcl
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "database_password" {
  description = "Master password for RDS database"
  value       = aws_db_instance.main.password
  sensitive   = true
}
```

## Comments

### When to Comment
- Use comments **sparingly**
- Write code that is self-explanatory
- Add comments only when:
  - Logic is complex or non-obvious
  - Explaining business requirements or constraints
  - Clarifying meta-argument effects

### Comment Syntax
- Use `#` for single-line and multi-line comments
- Avoid `//` and `/* */` (legacy syntax)

```hcl
# This security group allows access from our office network only
resource "aws_security_group" "office_access" {
  # Port 443 required for HTTPS traffic
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
}
```

## Resource Organization

### Data Sources Before Resources
Define data sources before the resources that reference them:

```hcl
# Data sources first
data "aws_ami" "ubuntu" {
  # ...
}

# Then resources that use them
resource "aws_instance" "web" {
  ami = data.aws_ami.ubuntu.id
  # ...
}
```

### Meta-Argument Order
Maintain consistent parameter ordering within resources:
1. `count` / `for_each`
2. Regular arguments (alphabetically when possible)
3. Nested blocks
4. `lifecycle`
5. `depends_on`

## Validation and Formatting

### Before Committing
Always run these commands before committing:
```bash
terraform fmt -recursive
terraform validate
```

### Optional: Use TFLint
For additional quality checks:
```bash
tflint
```

## Common Patterns

### Use of count and for_each
- Use sparingly to avoid complexity
- Prefer `for_each` over `count` for creating multiple similar resources
- Example:

```hcl
resource "aws_instance" "server" {
  for_each = toset(["web", "api", "worker"])

  ami           = var.ami_id
  instance_type = "t2.micro"

  tags = {
    Name = "${each.key}-server"
  }
}
```

### Locals for Repeated Values
Use locals to avoid repetition:

```hcl
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_name
  }
}

resource "aws_instance" "web" {
  # ...
  tags = merge(
    local.common_tags,
    {
      Name = "web-server"
    }
  )
}
```

### Resource Dependencies
- Prefer implicit dependencies (references) over explicit `depends_on`
- Use `depends_on` only when implicit dependencies don't work

```hcl
# Implicit dependency (preferred)
resource "aws_eip" "example" {
  instance = aws_instance.web.id
}

# Explicit dependency (use when necessary)
resource "aws_instance" "web" {
  # ...

  depends_on = [aws_security_group.allow_web]
}
```
