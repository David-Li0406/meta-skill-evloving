---
name: terraform-tests
description: 'Write Terraform tests using test blocks, run blocks, assertions, and provider configuration. Use when asked to "write Terraform tests", "create .tftest.hcl", "add test coverage", "validate Terraform module", or when implementing test-driven development for infrastructure code. Covers test/run/variables/provider blocks, assertions, expect_failures, and helper modules.'
---

# Terraform Tests

Write effective Terraform tests using the native testing framework introduced in Terraform 1.6+. This skill covers the syntax and structure of `.tftest.hcl` files and how different blocks work together.

## When to Use This Skill

- User asks to "write Terraform tests", "create test file", "add test coverage"
- Implementing test-driven development (TDD) for infrastructure
- Validating module behavior without affecting production
- Testing resource configurations, variable validation, outputs
- Creating integration or unit tests for Terraform modules
- Validating refactoring hasn't broken existing functionality

## Test File Basics

### File Extension

**Required:** `.tftest.hcl` or `.tftest.json`

**Location:** Root directory or `tests/` directory

**Discovery:** Terraform automatically finds all `*.tftest.hcl` files

### Minimal Test File

```hcl
run "basic_test" {
  assert {
    condition     = output.name == "expected"
    error_message = "Output name mismatch"
  }
}
```

**That's it!** A test file only needs one `run` block.

## Block Types and Their Relationships

### Block Hierarchy

```
test file (.tftest.hcl)
├── test block (optional, file-level config)
├── variables block (optional, global defaults)
├── provider blocks (optional, test-specific providers)
└── run blocks (required, one or more)
    ├── command (plan or apply)
    ├── variables block (run-specific overrides)
    ├── module block (alternate module to test)
    ├── assert blocks (validation)
    ├── expect_failures (negative testing)
    └── plan_options (advanced plan control)
```

## The `test` Block

**Purpose:** Configure test execution behavior

**Scope:** Entire test file

**Optional:** Yes (use defaults if omitted)

```hcl
test {
  parallel = true  # Run tests in parallel (default: false)
}
```

**When to use:**
- Enable parallel execution for independent tests
- Configure test-wide settings

**Example:**
```hcl
test {
  parallel = true
}

run "test_1" { }
run "test_2" { }
run "test_3" { }
# All three run simultaneously
```

## The `run` Block

**Purpose:** Define a single test case

**Scope:** One test execution (plan or apply)

**Required:** Yes (at least one per file)

### Basic Structure

```hcl
run "descriptive_test_name" {
  command = plan  # or apply (default: apply)

  variables {
    # Override module variables
  }

  assert {
    # Validate results
  }
}
```

### Command Types

**`command = plan` (Unit Tests):**
- No real infrastructure created
- Fast execution
- Tests configuration logic
- Use for validation without resource creation

```hcl
run "validate_naming_logic" {
  command = plan

  variables {
    name = "test"
  }

  assert {
    condition     = aws_s3_bucket.this.bucket == "test-bucket"
    error_message = "Naming logic incorrect"
  }
}
```

**`command = apply` (Integration Tests - Default):**
- Creates real infrastructure
- Tests actual behavior
- Automatically cleaned up
- Use for end-to-end validation

```hcl
run "create_real_bucket" {
  command = apply  # Can be omitted (default)

  assert {
    condition     = can(regex("^arn:aws:s3:::.*", aws_s3_bucket.this.arn))
    error_message = "Bucket not created"
  }
}
```

### Run Block Execution Order

**Sequential by default:**
```hcl
run "setup" {
  # Runs first
}

run "test" {
  # Runs second, can reference run.setup
}

run "validate" {
  # Runs third, can reference run.setup and run.test
}
```

**Referencing previous runs:**
```hcl
run "create_resource" {
  command = apply
}

run "validate_output" {
  variables {
    resource_id = run.create_resource.resource_id
  }

  assert {
    condition     = output.id == run.create_resource.resource_id
    error_message = "ID mismatch"
  }
}
```

### Plan Options

**Advanced control over plan execution:**

```hcl
run "advanced_test" {
  command = apply

  plan_options {
    mode    = "refresh-only"  # or "normal" (default)
    refresh = true            # Enable/disable refresh
    replace = [               # Force replacement
      aws_instance.web
    ]
    target = [                # Target specific resources
      aws_s3_bucket.bucket
    ]
  }
}
```

## The `variables` Block

**Purpose:** Set input variable values

**Scope:** Global (file-level) or run-specific

**Precedence:** Run-level > File-level > Auto .tfvars > CLI

### Global Variables

```hcl
# Set once, used by all run blocks
variables {
  environment = "test"
  region      = "us-east-1"
}

run "test_one" {
  # Uses global variables
}

run "test_two" {
  # Also uses global variables
}
```

### Run-Specific Variables

```hcl
variables {
  prefix = "default"  # Global default
}

run "use_default" {
  # Uses prefix = "default"
}

run "override_prefix" {
  variables {
    prefix = "custom"  # Overrides global
  }
  # Uses prefix = "custom"
}
```

### Variable Precedence (Highest to Lowest)

1. Run block `variables` block
2. File-level `variables` block
3. `*.auto.tfvars` in test directory
4. `terraform.tfvars` in test directory
5. CLI flags (`-var`, `-var-file`)
6. Environment variables (`TF_VAR_*`)

## The `provider` Block

**Purpose:** Configure test-specific providers

**Scope:** Entire test file

**Use cases:**
- Test in specific regions
- Use test credentials
- Configure multiple provider instances

### Basic Provider

```hcl
provider "aws" {
  region = "us-east-1"
}

run "test" {
  # Uses configured provider
}
```

### Multiple Providers

```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "secondary"
  region = "eu-west-1"
}

run "multi_region_test" {
  # Both providers available
}
```

### Override Provider Per Run

```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "eu"
  region = "eu-west-1"
}

run "test_eu_region" {
  providers = {
    aws = aws.eu  # Use eu provider instead
  }
}
```

### Dynamic Provider Configuration

```hcl
provider "vault" {
  # ... vault config ...
}

provider "aws" {
  # Reference output from setup run
  access_key = run.vault_setup.aws_access_key
  secret_key = run.vault_setup.aws_secret_key
}

run "vault_setup" {
  module {
    source = "./tests/setup"
  }
}

run "use_dynamic_credentials" {
  # Uses AWS provider with Vault credentials
}
```

## The `assert` Block

**Purpose:** Validate test results

**Scope:** Within a run block

**Required:** At least one per run block (usually)

### Structure

```hcl
assert {
  condition     = <boolean expression>
  error_message = "Helpful message when assertion fails"
}
```

### Assertion Types

**Resource attributes:**
```hcl
assert {
  condition     = aws_s3_bucket.bucket.bucket == "expected-name"
  error_message = "Bucket name incorrect"
}
```

**Output values:**
```hcl
assert {
  condition     = output.bucket_arn != null
  error_message = "Bucket ARN output missing"
}
```

**Previous run references:**
```hcl
assert {
  condition     = output.id == run.setup.resource_id
  error_message = "ID doesn't match setup"
}
```

**Complex conditions:**
```hcl
assert {
  condition     = length([for s in aws_subnet.private : s if s.availability_zone == "us-east-1a"]) > 0
  error_message = "No subnet in us-east-1a"
}
```

### Multiple Assertions

```hcl
run "validate_bucket" {
  assert {
    condition     = aws_s3_bucket.bucket.bucket == "test-bucket"
    error_message = "Name mismatch"
  }

  assert {
    condition     = aws_s3_bucket.bucket.versioning[0].enabled == true
    error_message = "Versioning not enabled"
  }

  assert {
    condition     = aws_s3_bucket.bucket.server_side_encryption_configuration != null
    error_message = "Encryption missing"
  }
}
```

## The `expect_failures` Block

**Purpose:** Test that validations/preconditions fail correctly

**Scope:** Within a run block

**Use for:** Negative testing (validation should fail)

### Structure

```hcl
run "test_validation_fails" {
  command = plan

  variables {
    invalid_value = "bad"
  }

  expect_failures = [
    var.input_variable,
  ]
}
```

### Testing Variable Validation

```hcl
# In module: variables.tf
variable "environment" {
  type = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod"
  }
}
```

```hcl
# In test
run "valid_environment" {
  command = plan
  variables {
    environment = "dev"
  }
  # Should succeed
}

run "invalid_environment" {
  command = plan
  variables {
    environment = "invalid"
  }

  expect_failures = [
    var.environment,  # Validation should fail
  ]
}
```

### Testing Preconditions

```hcl
# In module
resource "aws_instance" "web" {
  lifecycle {
    precondition {
      condition     = var.instance_type != "t1.micro"
      error_message = "t1.micro deprecated"
    }
  }
}
```

```hcl
# In test
run "deprecated_instance_type" {
  command = plan
  variables {
    instance_type = "t1.micro"
  }

  expect_failures = [
    aws_instance.web,  # Precondition should fail
  ]
}
```

### Testing Check Blocks

```hcl
# In module
check "health_check" {
  data "http" "health" {
    url = aws_lb.main.dns_name
  }

  assert {
    condition     = data.http.health.status_code == 200
    error_message = "Health check failed"
  }
}
```

```hcl
# In test
run "health_check_fails" {
  expect_failures = [
    check.health_check,
  ]
}
```

## The `module` Block

**Purpose:** Test a different module than the current directory

**Scope:** Within a run block

**Use cases:**
- Test helper/setup modules
- Test nested modules
- Validate module composition

```hcl
run "setup" {
  module {
    source = "./tests/setup"
  }
}

run "test_main_module" {
  variables {
    # Use outputs from setup
    vpc_id = run.setup.vpc_id
  }
}

run "validate" {
  module {
    source = "./tests/validation"
  }

  variables {
    endpoint = run.test_main_module.service_endpoint
  }
}
```

## State Management

### State Keys

**Purpose:** Isolate state between run blocks

**Default:** All runs share state

**Use `state_key`** for independent runs:

```hcl
run "scenario_a" {
  state_key = "scenario_a"
  # Independent state
}

run "scenario_b" {
  state_key = "scenario_b"
  # Independent state
}
```

### Parallel Execution with State

```hcl
test {
  parallel = true
}

run "parallel_1" {
  state_key = "test_1"
}

run "parallel_2" {
  state_key = "test_2"
}

run "parallel_3" {
  state_key = "test_3"
}
# All run simultaneously with isolated state
```

### Sequential Synchronization Point

```hcl
test {
  parallel = true
}

run "parallel_1" { }
run "parallel_2" { }
run "parallel_3" { }
# All three run in parallel

run "wait_for_all" {
  parallel = false  # Synchronization point
}
# This runs after all previous runs complete

run "continue_sequential" { }
```

## How Blocks Work Together

### Complete Example

```hcl
# File-level configuration
test {
  parallel = true  # Enable parallel execution
}

# Global variables
variables {
  environment = "test"
  region      = "us-east-1"
}

# Test-specific provider
provider "aws" {
  region = var.region
}

# Setup run
run "create_vpc" {
  module {
    source = "./tests/setup-vpc"
  }
}

# Main test run
run "create_service" {
  command = apply

  variables {
    vpc_id = run.create_vpc.vpc_id
    name   = "test-service"
  }

  assert {
    condition     = aws_ecs_service.this.name == "test-service"
    error_message = "Service name incorrect"
  }

  assert {
    condition     = output.service_arn != null
    error_message = "Service ARN missing"
  }
}

# Validation run
run "validate_endpoints" {
  command = plan

  module {
    source = "./tests/validate-http"
  }

  variables {
    endpoint = run.create_service.service_url
  }

  assert {
    condition     = data.http.health.status_code == 200
    error_message = "Health check failed"
  }
}

# Negative test
run "invalid_configuration" {
  command = plan

  variables {
    vpc_id = ""  # Invalid
  }

  expect_failures = [
    var.vpc_id,
  ]
}
```

## Common Patterns

### Pattern: Setup → Execute → Validate

```hcl
run "setup" {
  module {
    source = "./tests/setup"
  }
}

run "execute" {
  variables {
    dependency = run.setup.output
  }
}

run "validate" {
  module {
    source = "./tests/validate"
  }
  variables {
    target = run.execute.endpoint
  }
}
```

### Pattern: Matrix Testing

```hcl
run "test_small_instance" {
  variables {
    instance_type = "t2.small"
  }
}

run "test_medium_instance" {
  variables {
    instance_type = "t2.medium"
  }
}

run "test_large_instance" {
  variables {
    instance_type = "t2.large"
  }
}
```

### Pattern: Progressive Validation

```hcl
run "plan_validation" {
  command = plan
  # Fast: no resources created
}

run "apply_validation" {
  command = apply
  # Slower: creates resources
}

run "runtime_validation" {
  command = plan
  module {
    source = "./tests/validate"
  }
  # Validates live resources
}
```

## Best Practices

### Run Block Naming

```hcl
# ✅ Good - descriptive names
run "validate_bucket_encryption" { }
run "test_autoscaling_cpu_trigger" { }
run "verify_iam_permissions" { }

# ❌ Bad - vague names
run "test1" { }
run "check" { }
run "validate" { }
```

### One Test = One Concern

```hcl
# ✅ Good - focused tests
run "validate_bucket_name" {
  assert {
    condition = aws_s3_bucket.bucket.bucket == "expected"
  }
}

run "validate_bucket_encryption" {
  assert {
    condition = aws_s3_bucket.bucket.encryption != null
  }
}

# ❌ Bad - too many concerns
run "validate_everything" {
  assert { condition = aws_s3_bucket.bucket.bucket == "expected" }
  assert { condition = aws_s3_bucket.bucket.encryption != null }
  assert { condition = aws_s3_bucket.bucket.versioning.enabled }
  assert { condition = aws_iam_role.role.name == "expected" }
  assert { condition = output.url != null }
}
```

### Use `command = plan` When Possible

```hcl
# ✅ Good - fast unit test
run "validate_naming_logic" {
  command = plan
  # No resources created
}

# ⚠️ Only use apply when necessary
run "test_actual_deployment" {
  command = apply
  # Creates real resources (slower, costs money)
}
```

### Clear Error Messages

```hcl
# ✅ Good - includes actual value
assert {
  condition     = output.count == 3
  error_message = "Expected 3 instances, got ${output.count}"
}

# ❌ Bad - no context
assert {
  condition     = output.count == 3
  error_message = "Wrong count"
}
```

## Execution Flow

### Test File Execution Order

1. **Load test file** - Parse all blocks
2. **Process `test` block** - Apply file-level config
3. **Initialize variables** - File-level `variables` block
4. **Initialize providers** - `provider` blocks
5. **Execute `run` blocks** - Sequential or parallel
6. **Cleanup** - Destroy all created resources

### Run Block Execution Order

1. **Process variables** - Merge file-level + run-level
2. **Load module** - Main module or alternate via `module` block
3. **Execute command** - `plan` or `apply`
4. **Evaluate assertions** - All `assert` blocks
5. **Check failures** - Validate `expect_failures`
6. **Store outputs** - Available to later runs via `run.<name>.<output>`

## Helper Modules

Helper modules create test-specific resources outside your main configuration.

### When to Use Helper Modules

**Use Cases:**
1. **Setup** - Create dependencies (VPC, networks, databases)
2. **Validation** - Validate outputs (HTTP checks, data sources)
3. **Cleanup** - Ensure proper resource deletion order
4. **Data Generation** - Generate test data (random names, passwords)

### Helper Module Structure

**Setup Module Example:**

```
tests/
└── setup/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

```hcl
# tests/setup/main.tf
terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.5.1"
    }
  }
}

resource "random_pet" "bucket_prefix" {
  length = 4
}

output "bucket_prefix" {
  value = random_pet.bucket_prefix.id
}
```

**Using Helper Module:**

```hcl
# tests/integration.tftest.hcl

run "setup" {
  module {
    source = "./tests/setup"
  }
}

run "create_bucket" {
  variables {
    # Use output from setup module
    bucket_name = "${run.setup.bucket_prefix}-test"
  }

  assert {
    condition     = aws_s3_bucket.bucket.bucket == "${run.setup.bucket_prefix}-test"
    error_message = "Bucket name mismatch"
  }
}
```

**Validation Module Example:**

```hcl
# tests/final/main.tf
terraform {
  required_providers {
    http = {
      source  = "hashicorp/http"
      version = "3.4.0"
    }
  }
}

variable "endpoint" {
  type = string
}

data "http" "index" {
  url    = var.endpoint
  method = "GET"
}

output "status_code" {
  value = data.http.index.status_code
}
```

```hcl
# tests/integration.tftest.hcl

run "create_website" {
  command = apply
}

run "validate_website" {
  command = plan

  module {
    source = "./tests/final"
  }

  variables {
    endpoint = run.create_website.website_endpoint
  }

  assert {
    condition     = data.http.index.status_code == 200
    error_message = "Website not responding with 200 OK"
  }
}
```

### Helper Module Best Practices

1. **Keep Helper Modules Simple:**
   - Single, focused purpose
   - Minimal dependencies
   - Clear outputs

2. **Document Helper Modules:**
   - Add brief comment explaining purpose
   - Document required variables
   - Document outputs

3. **Reuse Helper Modules:**
   - Create shared helper modules for common patterns
   - Place in `tests/shared/` directory
   - Version helper modules if used across multiple modules

## Practical Lessons Learned

This section contains practical learnings from writing real-world Terraform tests.

### Common Pitfalls and Solutions

#### 1. Terraform Version Compatibility

**Problem:** Some test syntax features are only available in newer Terraform versions.

```hcl
# ❌ Not supported in Terraform < 1.7
test {
  parallel = true
}

# ❌ Not supported in some versions
mock_provider "aws" {
  override_during = plan  # This parameter may not exist
}
```

**Solution:** Check Terraform version and use supported syntax only.

```hcl
# ✅ Works in all versions with test support
variables {
  environment = "test"
}

mock_provider "aws" {}  # No override_during parameter
```

**Best Practice:** Run `terraform test --help` to check supported features for your version.

#### 2. Locals in Run Blocks

**Problem:** `locals {}` blocks cannot be used inside `run` blocks.

```hcl
# ❌ Error: Unsupported block type
run "validate_filters" {
  command = plan

  locals {
    grep_filters = [for f in local.filters : f if f.name == "grep"]
  }

  assert {
    condition     = length(local.grep_filters) == 4
    error_message = "Expected 4 grep filters"
  }
}
```

**Solution:** Use inline expressions instead of locals.

```hcl
# ✅ Use inline for loops
run "validate_filters" {
  command = plan

  assert {
    condition     = length([for f in local.filters : f if f.name == "grep"]) == 4
    error_message = "Expected 4 grep filters"
  }
}
```

**Best Practice:** Keep assertions simple with inline expressions, or split into multiple focused run blocks.

#### 3. Regex Escaping Complexity

**Problem:** Regex escaping in Terraform can be confusing, especially when testing strings that contain backslashes.

```hcl
# ❌ Complex regex escaping
run "validate_regex_pattern" {
  command = plan

  assert {
    condition     = can(regex("^\\^\\[", local.parser.regex))
    error_message = "Regex should start with ^\\["
  }
}
```

**Solution:** Use simpler string functions when possible.

```hcl
# ✅ Use startswith() for simple prefix checks
run "validate_regex_pattern" {
  command = plan

  assert {
    condition     = startswith(local.parser.regex, "^\\[")
    error_message = "Regex should start with ^\\["
  }
}

# ✅ Use contains() for substring checks
run "validate_pattern_content" {
  command = plan

  assert {
    condition     = strcontains(local.filter.exclude, "index.php")
    error_message = "Filter should exclude index.php"
  }
}
```

**Alternative:** Use `can(regex(...))` to check if a pattern matches without worrying about exact escaping.

```hcl
# ✅ Check if pattern exists anywhere in string
run "validate_pattern_exists" {
  command = plan

  assert {
    condition     = length([for f in local.filters : f if can(regex("index\\\\.php", f.exclude))]) > 0
    error_message = "Should have filter excluding index.php"
  }
}
```

#### 4. Provider Initialization

**Problem:** Tests fail with "Missing required provider" even with `mock_provider`.

```bash
$ terraform test tests/config.tftest.hcl
Error: Missing required provider

This configuration requires provider registry.terraform.io/hashicorp/aws,
but that provider isn't available. You may be able to install it automatically
by running:
  terraform init
```

**Solution:** Always run `terraform init` in the module root directory before running tests.

```bash
# ✅ Initialize first
terraform init
terraform test tests/config.tftest.hcl

# ✅ Or combine in one command
terraform init && terraform test
```

**Best Practice:** Add terraform init to CI/CD pipelines before test execution.

#### 5. Testing Complex Filters with For Loops

**Problem:** Testing elements in lists requires careful indexing.

```hcl
# ❌ Error if no matching elements found
run "validate_specific_filter" {
  command = plan

  assert {
    condition     = [for f in local.filters : f if f.name == "grep"][0].exclude == "pattern"
    error_message = "Grep filter not configured correctly"
  }
}
```

**Solution:** Use `length()` check first, then access elements safely.

```hcl
# ✅ Check existence first
run "validate_specific_filter" {
  command = plan

  assert {
    condition     = length([for f in local.filters : f if f.name == "grep"]) > 0
    error_message = "Should have grep filter"
  }

  assert {
    condition     = length([for f in local.filters : f if f.name == "grep" && can(regex("pattern", f.exclude))]) > 0
    error_message = "Grep filter should exclude pattern"
  }
}
```

**Best Practice:** Separate existence checks from content validation.

#### 6. Testing Multiple Variants

**Problem:** Need to test that configuration handles multiple format variations.

```hcl
# Testing multiple datetime format parsers
run "validate_all_datetime_formats" {
  command = plan

  assert {
    condition = (
      local.parsers[0].time_format == "%Y-%m-%dT%H:%M:%S%:z" &&
      local.parsers[1].time_format == "%Y-%m-%dT%H:%M:%S%z" &&
      local.parsers[2].time_format == "%Y-%m-%dT%H:%M:%SZ" &&
      local.parsers[3].time_format == "%Y-%m-%dT%H:%M:%S.%L%:z"
    )
    error_message = "Parsers should cover all ISO 8601 datetime format variants"
  }
}
```

**Best Practice:** Create separate run blocks for each variant to get more specific error messages.

```hcl
# ✅ Better: Separate tests for each variant
run "validate_datetime_tz_colon" {
  command = plan

  assert {
    condition     = local.parsers[0].time_format == "%Y-%m-%dT%H:%M:%S%:z"
    error_message = "Parser 0 should handle timezone with colon format"
  }
}

run "validate_datetime_tz_no_colon" {
  command = plan

  assert {
    condition     = local.parsers[1].time_format == "%Y-%m-%dT%H:%M:%S%z"
    error_message = "Parser 1 should handle timezone without colon format"
  }
}
```

#### 7. Validating Uniqueness

**Problem:** Need to ensure all items in a list are unique.

```hcl
# ✅ Convert to set and compare lengths
run "validate_parser_names_unique" {
  command = plan

  assert {
    condition     = length([for p in local.parsers : p.name]) == length(toset([for p in local.parsers : p.name]))
    error_message = "All parser names should be unique"
  }
}
```

**Best Practice:** Use `toset()` to remove duplicates and compare with original list length.

#### 8. Testing Conditional Logic

**Problem:** Validating that filters apply to correct items.

```hcl
# ✅ Use alltrue() for all-items validation
run "validate_all_json_parsers_have_filters" {
  command = plan

  assert {
    condition     = alltrue([for i in range(4) : contains(keys(local.parsers[i]), "filter")])
    error_message = "All JSON parsers should have filter configuration"
  }

  assert {
    condition     = alltrue([for i in range(4) : local.parsers[i].filter.reserve_data == true])
    error_message = "All JSON parser filters should reserve data"
  }
}
```

**Alternative:** Use conditional filtering in for loops.

```hcl
# ✅ Filter first, then validate
run "validate_grep_filters_all_have_exclude" {
  command = plan

  assert {
    condition     = alltrue([for f in local.filters : contains(keys(f), "exclude") if f.name == "grep"])
    error_message = "All grep filters should have exclude pattern"
  }
}
```

### Test Organization Learnings

#### Group Related Assertions

**Good:** Group related validations in the same run block.

```hcl
run "validate_monolog_parser_complete_config" {
  command = plan

  assert {
    condition     = local.parsers[0].name == "php_monolog_json_tz_colon"
    error_message = "Parser name mismatch"
  }

  assert {
    condition     = local.parsers[0].format == "json"
    error_message = "Parser should use json format"
  }

  assert {
    condition     = local.parsers[0].time_format == "%Y-%m-%dT%H:%M:%S%:z"
    error_message = "Parser should use ISO 8601 format with timezone colon"
  }

  assert {
    condition     = local.parsers[0].time_keep == false
    error_message = "Parser should not keep original time field"
  }
}
```

#### Separate Concerns

**Bad:** Testing unrelated things together makes debugging harder.

```hcl
# ❌ Too many unrelated checks
run "validate_everything" {
  command = plan

  assert {
    condition = length(local.parsers) == 5
    error_message = "Wrong parser count"
  }

  assert {
    condition = length(local.filters) == 5
    error_message = "Wrong filter count"
  }

  assert {
    condition = local.parsers[0].name == "php_monolog_json_tz_colon"
    error_message = "Wrong parser name"
  }
}
```

**Good:** Separate into focused tests.

```hcl
# ✅ Focused tests
run "validate_parser_count" {
  command = plan

  assert {
    condition     = length(local.parsers) == 5
    error_message = "Expected 5 parsers, got ${length(local.parsers)}"
  }
}

run "validate_filter_count" {
  command = plan

  assert {
    condition     = length(local.filters) == 5
    error_message = "Expected 5 filters, got ${length(local.filters)}"
  }
}

run "validate_primary_parser_name" {
  command = plan

  assert {
    condition     = local.parsers[0].name == "php_monolog_json_tz_colon"
    error_message = "First parser should be php_monolog_json_tz_colon"
  }
}
```

### Error Message Best Practices

#### Include Actual Values

**Good:** Error messages that show what went wrong.

```hcl
# ✅ Helpful error with actual value
assert {
  condition     = length(local.parsers) == 5
  error_message = "Expected 5 PHP parsers (4 JSON variants + 1 error parser), got ${length(local.parsers)}"
}
```

**Bad:** Vague error messages.

```hcl
# ❌ Not helpful
assert {
  condition     = length(local.parsers) == 5
  error_message = "Wrong number of parsers"
}
```

#### Be Specific About Expected Behavior

```hcl
# ✅ Explains what should happen
assert {
  condition     = alltrue([for f in local.filters : f.match == "*" if f.name == "grep"])
  error_message = "All grep filters should match '*' (to be overridden by container pattern)"
}
```

### Quick Troubleshooting Guide

| Error | Cause | Solution |
|-------|-------|----------|
| "Unsupported block type: test" | Terraform version too old or syntax not supported | Remove `test {}` block, use only `run` blocks |
| "Unsupported argument: override_during" | Parameter not available in your Terraform version | Remove the parameter from `mock_provider` |
| "Unsupported block type: locals" | Locals cannot be in run blocks | Use inline expressions instead |
| "Missing required provider" | Provider not initialized | Run `terraform init` before `terraform test` |
| "Test assertion failed" with cryptic message | Error message doesn't include actual values | Add `${variable}` to show actual value in error |
| Index out of range | For loop filter returns empty list | Add `length()` check before accessing `[0]` |
| Regex doesn't match | Escaping issues | Use `startswith()`, `contains()`, or `strcontains()` instead |

## References

- **Terraform Testing**: <https://developer.hashicorp.com/terraform/language/tests>
- **Test Mocking**: <https://developer.hashicorp.com/terraform/language/tests/mocking>
- **Custom Conditions**: <https://developer.hashicorp.com/terraform/language/expressions/custom-conditions>
- **Test Assertions**: Use the **test-assertions** skill for universal assertion patterns
- **Test Mocking**: Use the **test-mocking** skill for mocking strategies
- **Test Organization**: Use the **test-organization-patterns** skill for file structure

## Quick Decision Tree

**What do I need?**

- **Test configuration logic only** → `command = plan`
- **Test actual infrastructure** → `command = apply` (or omit)
- **Share setup across tests** → File-level `variables` block
- **Override per test** → Run-level `variables` block
- **Test in specific region** → `provider` block
- **Test different module** → `module` block in run
- **Test validation fails** → `expect_failures`
- **Reference previous test** → `run.<name>.<output>`
- **Run tests in parallel** → `test { parallel = true }` + `state_key`
- **Validate multiple things** → Multiple `assert` blocks in one run
