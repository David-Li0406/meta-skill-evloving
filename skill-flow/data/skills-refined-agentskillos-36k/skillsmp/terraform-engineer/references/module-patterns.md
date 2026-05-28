# Terraform Module Patterns

## Standard Layout

```
module/
├── main.tf        # Resource definitions
├── variables.tf   # Input variables
├── outputs.tf     # Return values
├── versions.tf    # Provider constraints
└── examples/      # Usage examples
```

## Input Validation

```hcl
variable "name" {
  type        = string
  description = "Resource name (1-32 chars)"
  validation {
    condition     = length(var.name) >= 1 && length(var.name) <= 32
    error_message = "Name must be 1-32 characters."
  }
}

variable "cidr_block" {
  type        = string
  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be valid CIDR notation."
  }
}
```

## Dynamic Blocks

```hcl
resource "aws_security_group" "this" {
  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

## Conditional Creation

```hcl
resource "aws_nat_gateway" "this" {
  count = var.enable_nat_gateway ? 1 : 0
  # ...
}
```

## Module Composition

```hcl
module "network" {
  source = "./modules/networking"
}

module "security" {
  source = "./modules/security"
  vpc_id = module.network.vpc_id
}
```
