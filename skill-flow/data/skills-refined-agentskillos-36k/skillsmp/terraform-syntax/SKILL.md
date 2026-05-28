---
name: terraform-syntax
description: 'Master Terraform HCL syntax including blocks, arguments, expressions, operators, templates, and formatting conventions. Use when asked about "Terraform syntax", "HCL syntax", "write Terraform code", "expression syntax", "template syntax", or when writing, reviewing, or understanding Terraform configuration. Covers structural language, expression language, template language, and style guidelines.'
---

# Terraform HCL Syntax

Comprehensive guide to Terraform's HashiCorp Configuration Language (HCL) syntax, covering structural elements, expressions, templates, operators, and style conventions.

## When to Use This Skill

- User asks about "Terraform syntax", "HCL syntax", "how to write Terraform"
- Writing new Terraform configuration files
- Reviewing or understanding existing Terraform code
- Questions about expressions, operators, or templates
- Formatting and style questions
- Syntax errors or validation issues
- Learning Terraform language fundamentals

## Language Components

Terraform's configuration language consists of three integrated sub-languages:

1. **Structural Language** - Defines hierarchical configuration (bodies, blocks, attributes)
2. **Expression Language** - Specifies values (literals, operations, functions)
3. **Template Language** - Composes strings (interpolation, directives)

## Structural Language

### Configuration Files

A configuration file is a UTF-8 encoded text file whose top-level is interpreted as a Body.

**File Extensions:**
- `.tf` - Native Terraform syntax
- `.tf.json` - JSON syntax (for programmatic generation)

**Character Encoding:**
- Must be UTF-8
- Unix-style line endings (LF) preferred
- Windows-style (CRLF) accepted but may be auto-converted

### Bodies

A body is a collection of associated attributes and blocks.

```hcl
# Body contains attributes and blocks
resource "aws_instance" "example" {
  # This is a body - contains attributes and nested blocks
  ami           = "abc123"
  instance_type = "t2.micro"

  tags = {
    Name = "example"
  }
}
```

### Attributes (Arguments)

An attribute assigns a value to a name. Each distinct attribute name may be defined **no more than once** within a single body.

**Syntax:**
```hcl
Attribute = Identifier "=" Expression Newline
```

**Examples:**
```hcl
# Simple attribute
ami = "abc123"

# Attribute with expression
instance_type = var.instance_type

# Attribute with complex expression
count = var.enabled ? 1 : 0

# Object attribute
tags = {
  Name        = "example"
  Environment = var.environment
}
```

**Formatting:**
```hcl
# ✅ Good - Align equals signs
ami           = "abc123"
instance_type = "t2.micro"
subnet_id     = var.subnet_id

# ❌ Bad - Unaligned
ami = "abc123"
instance_type = "t2.micro"
subnet_id = var.subnet_id
```

### Blocks

A block creates a child body annotated with a type and optional labels.

**Syntax:**
```hcl
Block = Identifier (StringLit|Identifier)* "{" Newline Body "}" Newline
```

**Structure:**
```hcl
block_type "label1" "label2" {
  # Block body - can contain attributes and nested blocks
  argument = value

  nested_block {
    # Nested block body
  }
}
```

**Examples:**
```hcl
# Resource block (2 labels: type, name)
resource "aws_instance" "web" {
  ami = "abc123"
}

# Variable block (1 label: name)
variable "instance_count" {
  type    = number
  default = 1
}

# Nested blocks
resource "aws_instance" "web" {
  ami = "abc123"

  # Nested block
  root_block_device {
    volume_size = 20
  }

  # Another nested block
  network_interface {
    device_index = 0
  }
}
```

**One-Line Blocks:**
```hcl
# Short blocks can be on one line
lifecycle { create_before_destroy = true }
```

### Top-Level Blocks

Terraform uses a limited number of top-level block types:

```hcl
terraform {
  required_version = ">= 1.3"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami = "abc123"
}

data "aws_ami" "ubuntu" {
  most_recent = true
}

variable "region" {
  type = string
}

output "instance_id" {
  value = aws_instance.web.id
}

module "vpc" {
  source = "./modules/vpc"
}

locals {
  common_tags = {
    Project = "example"
  }
}
```

## Identifiers

Identifiers name entities (blocks, attributes, variables).

**Rules:**
- Can contain: letters, digits, underscores (`_`), hyphens (`-`)
- Must start with: letter or underscore (not a digit)
- Follows Unicode identifier syntax (UAX #31)
- Dash `-` is allowed (Terraform extension)

**Examples:**
```hcl
# ✅ Valid identifiers
my_variable
aws_instance
web-server
resource_1
_private

# ❌ Invalid identifiers
1st_resource  # Starts with digit
my variable   # Contains space
my@resource   # Contains @
```

**Conventions:**
```hcl
# Use snake_case for multi-word identifiers
instance_type
security_group
vpc_cidr_block

# Use snake_case for labels (when appropriate)
resource "aws_instance" "web_server" {
  # ...
}
```

## Comments

Three comment syntaxes:

```hcl
# Single-line comment (preferred)

// Single-line comment (alternative)

/*
  Multi-line comment
  spans multiple lines
*/
```

**Best Practice:**
```hcl
# ✅ Preferred - Use # for single and multi-line comments
# This is a comment
# explaining the resource

# ❌ Avoid - // style
// This comment style is less idiomatic
```

## Expression Language

Expressions specify values for attributes.

### Literal Values

**Numbers:**
```hcl
42          # Integer
3.14159     # Decimal
1.5e10      # Exponent notation
```

**Booleans:**
```hcl
true
false
```

**Null:**
```hcl
null
```

**Strings:**
```hcl
# Strings use template syntax
"hello"
"hello ${var.name}"

# Heredoc strings
<<EOT
Multi-line
string content
EOT

# Indented heredoc (strips leading whitespace)
<<-EOT
  Indented content
  will have leading spaces stripped
  EOT
```

### Collection Values

**Tuples (ordered lists):**
```hcl
["a", "b", "c"]

[
  "item1",
  "item2",
  "item3",
]

# Trailing comma allowed
[1, 2, 3,]
```

**Objects (maps with named attributes):**
```hcl
{
  name = "example"
  age  = 42
}

# Keys can be expressions (use parentheses)
{
  (var.key_name) = "value"
}

# Colon syntax also allowed
{
  name: "example",
  age:  42
}

# Mixed newlines and commas
{
  name = "example",
  age  = 42
  city = "Boston"
}
```

**Ambiguity Resolution:**
```hcl
# ❌ Syntax error - for expression vs collection
[for, foo, baz]

# ✅ Use parentheses
[(for), foo, baz]

# ❌ Syntax error - for as key
{for = 1, baz = 2}

# ✅ Quote the key
{"for" = 1, baz = 2}

# ✅ Or reorder
{baz = 2, for = 1}

# ✅ Or use parentheses
{(for) = 1, baz = 2}
```

### Variables

Access variables using identifiers:

```hcl
var.instance_type
var.region
local.common_tags
```

### Functions

Call functions with parentheses:

```hcl
# Basic function call
length(var.list)

# Multiple arguments
merge(local.tags, var.additional_tags)

# Nested function calls
upper(substr(var.name, 0, 3))

# Spread operator (...)
concat(var.list1, var.list2...)
```

### Operators

**Arithmetic:**
```hcl
a + b   # Addition
a - b   # Subtraction
a * b   # Multiplication
a / b   # Division
a % b   # Modulo
-a      # Negation
```

**Comparison:**
```hcl
a == b  # Equal
a != b  # Not equal
a < b   # Less than
a <= b  # Less than or equal
a > b   # Greater than
a >= b  # Greater than or equal
```

**Logical:**
```hcl
a && b  # AND
a || b  # OR
!a      # NOT
```

**Operator Precedence (highest to lowest):**
```
1. -, ! (unary)
2. *, /, %
3. +, -
4. >, >=, <, <=
5. ==, !=
6. &&
7. ||
```

**Examples:**
```hcl
# Arithmetic
var.count * 2
(var.price * var.quantity) + var.tax

# Comparisons
var.age >= 18
var.status == "active"

# Logical
var.enabled && var.count > 0
var.env == "prod" || var.env == "staging"

# Combined
(var.count > 0) && (var.enabled || var.force)
```

### Conditional Expressions

Ternary operator:

```hcl
condition ? true_val : false_val
```

**Examples:**
```hcl
# Simple conditional
var.enabled ? 1 : 0

# With complex expressions
var.env == "prod" ? "m5.large" : "t2.micro"

# Nested conditionals
var.env == "prod" ? "m5.large" : var.env == "staging" ? "t3.medium" : "t2.micro"

# Safe indexing
length(var.list) > 0 ? var.list[0] : "default"
```

### For Expressions

Transform collections:

**Tuple For:**
```hcl
# Basic syntax
[for item in collection : transform_expression]

# With index
[for i, v in collection : expression]

# With condition
[for v in collection : v if condition]

# Examples
[for s in var.list : upper(s)]
[for i, v in var.list : "${i}: ${v}"]
[for s in var.list : s if length(s) > 3]
```

**Object For:**
```hcl
# Basic syntax
{for item in collection : key_expr => value_expr}

# With grouping (...)
{for item in collection : key_expr => value_expr...}

# Examples
{for k, v in var.map : k => upper(v)}
{for s in var.list : s => length(s)}

# Grouping mode
{for i, v in ["a", "a", "b"] : v => i...}
# Result: {a = [0, 1], b = [2]}
```

### Splat Expressions

Convenient attribute/element access:

**Attribute-Only Splat:**
```hcl
# Syntax
collection.*.attribute

# Example
var.instances.*.id
# Equivalent to: [for i in var.instances : i.id]

# Chained attributes
var.instances.*.tags.*.Name
```

**Full Splat:**
```hcl
# Syntax
collection[*].attribute_or_index

# Examples
var.instances[*].id
var.instances[*].tags["Name"]
var.instances[*].network_interfaces[0]
```

**Auto-Wrapping:**
```hcl
# If value is not a list, it's wrapped
single_object.*.id
# Equivalent to: [single_object.id]

# Null becomes empty list
null_value.*.id
# Result: []
```

### Index Operator

Access collection elements:

```hcl
# Tuple/list indexing (zero-based)
var.list[0]
var.list[var.index]

# Object/map indexing (by key)
var.map["key"]
var.map[var.dynamic_key]

# Legacy syntax (compatibility only)
var.list.0  # Don't use in new code
```

### Attribute Access

Access object attributes:

```hcl
# Syntax
object.attribute

# Examples
var.config.name
aws_instance.web.public_ip
module.vpc.vpc_id
data.aws_ami.ubuntu.id

# Chained access
var.config.network.vpc.id
```

## Template Language

Templates compose values into strings.

### Template Expressions

**Quoted Template:**
```hcl
"Hello, ${var.name}!"
"The result is ${var.a + var.b}"
```

**Heredoc Template:**
```hcl
<<EOT
Hello, ${var.name}!
Your instance is ${aws_instance.web.id}
EOT

# Indented heredoc (strips leading spaces)
<<-EOT
  Line 1
  Line 2
  EOT
```

### Escape Sequences

In quoted templates:

```hcl
"Line 1\nLine 2"         # Newline
"Column 1\tColumn 2"     # Tab
"She said \"Hello\""     # Quote
"Path: C:\\Users\\name"  # Backslash
"Unicode: \u0041"        # Unicode (A)
"Emoji: \U0001F600"      # Unicode emoji
```

**Escaping Template Sequences:**
```hcl
# Escape interpolation
"Dollar sign: $${var.name}"    # Outputs: Dollar sign: ${var.name}

# Escape directive
"Percent: %%{if true}text%{endif}"  # Outputs: Percent: %{if true}text%{endif}
```

### Interpolation

Embed expressions in strings:

```hcl
# Basic interpolation
"Hello, ${var.name}!"

# Expression interpolation
"Total: ${var.price * var.quantity}"

# Function calls
"Uppercase: ${upper(var.name)}"

# Conditional
"Status: ${var.enabled ? "active" : "inactive"}"
```

### Strip Markers

Remove whitespace with `~`:

```hcl
# Strip after opening
"hello ${~ "world" }"
# Result: "helloworld"

# Strip before closing
"hello${ "world" ~} test"
# Result: "hellotest"

# Strip both
"%{ if true ~}   hello   %{~ endif }"
# Result: "hello"
```

### Template Directives

**If Directive:**
```hcl
%{ if condition }
  true_content
%{ else }
  false_content
%{ endif }

# Example
<<EOT
%{ if var.enabled }
Service is enabled
%{ else }
Service is disabled
%{ endif }
EOT
```

**For Directive:**
```hcl
%{ for item in collection }
  ${item}
%{ endfor }

# Example with index
<<EOT
%{ for i, name in var.names }
${i + 1}. ${name}
%{ endfor }
EOT

# Result:
# 1. Alice
# 2. Bob
# 3. Carol
```

### Template Unwrapping

A template with only a single interpolation is "unwrapped":

```hcl
# Unwrapped - returns boolean
"${true}"
# Result: true (boolean, not string)

# Not unwrapped - returns string
"hello ${true}"
# Result: "hello true"

# Double unwrapping
"${"${true}"}"
# Result: true (boolean)
```

## Common Patterns

### Meta-Arguments

Meta-arguments modify resource behavior:

```hcl
resource "aws_instance" "web" {
  # Meta-arguments first
  count      = var.instance_count
  for_each   = toset(var.availability_zones)
  depends_on = [aws_security_group.web]
  provider   = aws.west

  # Regular arguments
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  # Lifecycle block last
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
  }
}
```

### Dynamic Blocks

Generate nested blocks:

```hcl
resource "aws_security_group" "example" {
  name = "example"

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

**For comprehensive examples and best practices, see the **terraform-resources** skill.**

### Type Constraints

Specify variable types:

```hcl
variable "instance_type" {
  type = string
}

variable "instance_count" {
  type = number
}

variable "enabled" {
  type = bool
}

variable "tags" {
  type = map(string)
}

variable "subnets" {
  type = list(string)
}

variable "config" {
  type = object({
    name    = string
    size    = number
    enabled = bool
  })
}

variable "instances" {
  type = list(object({
    name = string
    type = string
  }))
}

# Optional attributes
variable "server" {
  type = object({
    name     = string
    port     = optional(number, 80)
    enabled  = optional(bool, true)
  })
}
```

## Style Guidelines

### Formatting

**Indentation:**
```hcl
# ✅ Use 2 spaces per nesting level
resource "aws_instance" "web" {
  ami = "abc123"

  network_interface {
    device_index = 0
  }
}
```

**Alignment:**
```hcl
# ✅ Align equals signs
ami           = "abc123"
instance_type = "t2.micro"
subnet_id     = var.subnet_id
```

**Blank Lines:**
```hcl
# ✅ Separate top-level blocks with blank line
resource "aws_instance" "web" {
  ami = "abc123"
}

resource "aws_security_group" "web" {
  name = "web"
}
```

**Block Ordering:**
```hcl
resource "aws_instance" "example" {
  # 1. Meta-arguments first
  count = 2

  # 2. Required arguments
  ami           = "abc123"
  instance_type = "t2.micro"

  # 3. Optional arguments
  monitoring = true

  # 4. Nested blocks
  root_block_device {
    volume_size = 20
  }

  # 5. Lifecycle block last
  lifecycle {
    create_before_destroy = true
  }
}
```

### Naming Conventions

**Resources:**
```hcl
# ✅ Use descriptive nouns, snake_case
resource "aws_instance" "web_server" {}
resource "aws_security_group" "database" {}

# ❌ Avoid redundant naming
resource "aws_instance" "aws_instance_web" {}
```

**Variables and Outputs:**
```hcl
# ✅ Descriptive, snake_case
variable "instance_count" {}
output "vpc_id" {}

# Order: type, description, default, sensitive, validation
variable "db_password" {
  type        = string
  description = "Database password"
  sensitive   = true

  validation {
    condition     = length(var.db_password) >= 8
    error_message = "Password must be at least 8 characters"
  }
}
```

### File Organization

**Standard Files:**
```
main.tf       # Primary resources
variables.tf  # Input variables (alphabetical)
outputs.tf    # Output values (alphabetical)
versions.tf   # Version constraints
providers.tf  # Provider configurations
locals.tf     # Local values
backend.tf    # Backend configuration
```

**Resource-Specific Files:**
```
network.tf    # Networking resources
security.tf   # Security groups, NACLs
iam.tf        # IAM roles and policies
compute.tf    # Compute resources
```

## Validation and Formatting

### terraform fmt

Format code to standard style:

```bash
# Format current directory
terraform fmt

# Format recursively
terraform fmt -recursive

# Check formatting without changes
terraform fmt -check
```

### terraform validate

Validate syntax and internal consistency:

```bash
terraform validate
```

**What it checks:**
- Syntax correctness
- Type consistency
- Argument requirements
- Variable references
- **Does NOT check:** Provider-specific validation

## Common Syntax Errors

### Missing Equals Sign

```hcl
# ❌ Error
ami "abc123"

# ✅ Correct
ami = "abc123"
```

### Unclosed Blocks

```hcl
# ❌ Error - missing closing brace
resource "aws_instance" "web" {
  ami = "abc123"

# ✅ Correct
resource "aws_instance" "web" {
  ami = "abc123"
}
```

### Invalid Identifiers

```hcl
# ❌ Error - starts with digit
variable "1st_instance" {}

# ✅ Correct
variable "first_instance" {}
```

### Type Mismatches

```hcl
# ❌ Error - string where number expected
variable "count" {
  type    = number
  default = "five"
}

# ✅ Correct
variable "count" {
  type    = number
  default = 5
}
```

### Duplicate Attributes

```hcl
# ❌ Error - duplicate attribute
resource "aws_instance" "web" {
  ami = "abc123"
  ami = "def456"
}

# ✅ Correct - use one value
resource "aws_instance" "web" {
  ami = "abc123"
}
```

## Best Practices Summary

### Do's

✅ **Use terraform fmt before committing**
✅ **Use 2-space indentation**
✅ **Align equals signs for readability**
✅ **Use # for comments (not //)**
✅ **Use snake_case for identifiers**
✅ **Separate top-level blocks with blank lines**
✅ **Put meta-arguments first**
✅ **Put lifecycle blocks last**
✅ **Use descriptive, clear names**
✅ **Add descriptions to variables and outputs**
✅ **Use type constraints on variables**

### Don'ts

❌ **Don't use // for comments**
❌ **Don't start identifiers with digits**
❌ **Don't duplicate attribute names**
❌ **Don't use CRLF line endings**
❌ **Don't include resource type in resource name**
❌ **Don't skip terraform fmt**
❌ **Don't use legacy syntax (.0 indexing)**
❌ **Don't hardcode values that should be variables**

## Quick Reference

**Attribute:**
```hcl
name = value
```

**Block:**
```hcl
type "label" {
  attribute = value
}
```

**Expression:**
```hcl
value
var.name
function(arg)
condition ? true_val : false_val
[for x in list : transform]
{for k, v in map : k => v}
```

**Template:**
```hcl
"String with ${interpolation}"
<<EOT
Heredoc with ${interpolation}
EOT
```

**Operators:**
```hcl
+  -  *  /  %     # Arithmetic
== != < > <= >=   # Comparison
&& || !           # Logical
```

**Comments:**
```hcl
# Preferred style
// Alternative
/* Multi-line */
```

## References

- **HCL Spec**: <https://github.com/hashicorp/hcl/blob/main/hclsyntax/spec.md>
- **Terraform Configuration**: <https://developer.hashicorp.com/terraform/language/syntax/configuration>
- **Terraform Style Guide**: <https://developer.hashicorp.com/terraform/language/style>
- **Expressions**: <https://developer.hashicorp.com/terraform/language/expressions>
- **Functions**: <https://developer.hashicorp.com/terraform/language/functions>
- **terraform-refactoring** skill for safe code restructuring
- **terraform.instructions.md** for complete coding guidelines
