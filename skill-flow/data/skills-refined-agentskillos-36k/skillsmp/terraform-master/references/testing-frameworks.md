# Testing Frameworks Reference

## Native Testing (Terraform 1.6+)

### File Structure

```
module/
├── main.tf
├── variables.tf
├── outputs.tf
└── tests/
    ├── unit/
    │   ├── variables.tftest.hcl    # Variable validation
    │   └── outputs.tftest.hcl      # Output format tests
    ├── integration/
    │   ├── basic.tftest.hcl        # Minimal config
    │   └── complete.tftest.hcl     # All features enabled
    └── mocks/
        ├── aws.tfmock.hcl
        └── data.tfmock.hcl
```

### Test File Anatomy

```hcl
# tests/unit/vpc.tftest.hcl

# Global variables for all runs
variables {
  environment = "test"
  project     = "unittest"
}

# Provider configuration for tests
provider "aws" {
  region = "us-east-1"
}

# Test run with plan-only (fast, no resources created)
run "vpc_cidr_validation" {
  command = plan

  variables {
    vpc_cidr = "10.0.0.0/16"
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR does not match input"
  }
}

# Test run with apply (creates real resources)
run "vpc_creates_successfully" {
  command = apply

  variables {
    vpc_cidr    = "10.0.0.0/16"
    environment = "test"
  }

  assert {
    condition     = aws_vpc.main.id != ""
    error_message = "VPC was not created"
  }

  assert {
    condition     = length(aws_subnet.private) == 3
    error_message = "Expected 3 private subnets"
  }
}

# Test that uses output from previous run
run "vpc_outputs_are_valid" {
  command = plan

  # Reference previous run's state
  assert {
    condition     = output.vpc_id != ""
    error_message = "VPC ID output is empty"
  }

  assert {
    condition     = length(output.private_subnet_ids) > 0
    error_message = "No private subnet IDs in output"
  }
}
```

### Testing Variable Validation

```hcl
# tests/unit/variable_validation.tftest.hcl

run "rejects_invalid_environment" {
  command = plan

  variables {
    environment = "invalid"
    vpc_cidr    = "10.0.0.0/16"
  }

  # Expect this to fail validation
  expect_failures = [
    var.environment
  ]
}

run "accepts_valid_environment" {
  command = plan

  variables {
    environment = "prod"
    vpc_cidr    = "10.0.0.0/16"
  }

  # No expect_failures = success expected
}

run "rejects_invalid_cidr" {
  command = plan

  variables {
    environment = "dev"
    vpc_cidr    = "invalid-cidr"
  }

  expect_failures = [
    var.vpc_cidr
  ]
}
```

---

## Mock Providers (Terraform 1.7+)

### Basic Mock

```hcl
# tests/mocks/aws.tfmock.hcl

mock_provider "aws" {
  # Default values for all aws_vpc resources
  mock_resource "aws_vpc" {
    defaults = {
      id                       = "vpc-mock12345"
      arn                      = "arn:aws:ec2:us-east-1:123456789:vpc/vpc-mock12345"
      default_network_acl_id   = "acl-mock12345"
      default_route_table_id   = "rtb-mock12345"
      default_security_group_id = "sg-mock12345"
      enable_dns_hostnames     = true
      enable_dns_support       = true
      main_route_table_id      = "rtb-mock12345"
      owner_id                 = "123456789012"
    }
  }

  mock_resource "aws_subnet" {
    defaults = {
      id                = "subnet-mock${mock.index}"
      arn               = "arn:aws:ec2:us-east-1:123456789:subnet/subnet-mock${mock.index}"
      availability_zone = "us-east-1a"
      owner_id          = "123456789012"
    }
  }

  mock_resource "aws_security_group" {
    defaults = {
      id       = "sg-mock12345"
      arn      = "arn:aws:ec2:us-east-1:123456789:security-group/sg-mock12345"
      owner_id = "123456789012"
      vpc_id   = "vpc-mock12345"
    }
  }
}
```

### Mock Data Sources

```hcl
# tests/mocks/data.tfmock.hcl

mock_provider "aws" {
  mock_data "aws_availability_zones" {
    defaults = {
      names = ["us-east-1a", "us-east-1b", "us-east-1c"]
      zone_ids = ["use1-az1", "use1-az2", "use1-az3"]
    }
  }

  mock_data "aws_caller_identity" {
    defaults = {
      account_id = "123456789012"
      arn        = "arn:aws:iam::123456789012:user/test"
      user_id    = "AIDAMOCKUSERID"
    }
  }

  mock_data "aws_region" {
    defaults = {
      name        = "us-east-1"
      description = "US East (N. Virginia)"
    }
  }

  mock_data "aws_ami" {
    defaults = {
      id           = "ami-mock12345"
      architecture = "x86_64"
      name         = "mock-ami"
      owner_id     = "123456789012"
    }
  }
}
```

### Using Mocks in Tests

```hcl
# tests/unit/with_mocks.tftest.hcl

# Reference mock provider file
mock_provider "aws" {
  source = "./mocks/aws.tfmock.hcl"
}

run "test_with_mocked_provider" {
  command = plan

  variables {
    vpc_cidr    = "10.0.0.0/16"
    environment = "test"
  }

  # Assertions use mocked values
  assert {
    condition     = aws_vpc.main.id == "vpc-mock12345"
    error_message = "Expected mocked VPC ID"
  }
}
```

---

## Terratest (Go-based)

### When to Use Terratest

- Real infrastructure validation
- Cross-module integration tests
- Complex assertion logic
- Custom test fixtures
- Parallel test execution with cleanup

### Basic Terratest Example

```go
// test/vpc_test.go
package test

import (
    "testing"

    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVpcCreation(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../examples/basic",
        Vars: map[string]interface{}{
            "environment": "test",
            "vpc_cidr":    "10.0.0.0/16",
        },
    })

    // Clean up resources after test
    defer terraform.Destroy(t, terraformOptions)

    // Deploy infrastructure
    terraform.InitAndApply(t, terraformOptions)

    // Validate outputs
    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)

    privateSubnetIds := terraform.OutputList(t, terraformOptions, "private_subnet_ids")
    assert.Len(t, privateSubnetIds, 3)
}
```

### Terratest with AWS SDK Validation

```go
func TestVpcConfiguration(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../examples/complete",
        Vars: map[string]interface{}{
            "environment":      "test",
            "vpc_cidr":         "10.0.0.0/16",
            "enable_flow_logs": true,
        },
    })

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcId := terraform.Output(t, terraformOptions, "vpc_id")

    // Validate using AWS SDK
    awsRegion := "us-east-1"
    vpc := aws.GetVpcById(t, vpcId, awsRegion)
    
    assert.Equal(t, "10.0.0.0/16", aws.GetCidrBlockForVpc(t, vpc, awsRegion))
    assert.True(t, aws.IsVpcDnsEnabled(t, vpc, awsRegion))
}
```

### Test Fixtures

```go
// test/fixtures/basic/main.tf
module "vpc" {
  source = "../../../"

  environment = var.environment
  vpc_cidr    = var.vpc_cidr
  
  tags = {
    Test = "true"
  }
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
```

---

## Test Command Reference

```bash
# Run all tests
terraform test

# Run specific test file
terraform test -filter=tests/unit/basic.tftest.hcl

# Run tests with verbose output
terraform test -verbose

# Run tests in specific directory
terraform test -test-directory=tests/

# Run tests with variable overrides
terraform test -var="environment=staging"

# Run tests with variable file
terraform test -var-file="testing.tfvars"

# JSON output for CI
terraform test -json
```

---

## Test Organization Patterns

### Pattern 1: Test by Feature

```
tests/
├── encryption.tftest.hcl      # All encryption-related tests
├── networking.tftest.hcl      # All networking tests
├── monitoring.tftest.hcl      # All monitoring tests
└── mocks/
```

### Pattern 2: Test by Scenario

```
tests/
├── minimal.tftest.hcl         # Bare minimum config
├── standard.tftest.hcl        # Common production config
├── complete.tftest.hcl        # All features enabled
├── edge_cases.tftest.hcl      # Boundary conditions
└── mocks/
```

### Pattern 3: Test by Layer

```
tests/
├── unit/                      # Variable validation, output format
│   ├── variables.tftest.hcl
│   └── outputs.tftest.hcl
├── integration/               # Cross-resource dependencies
│   └── full_stack.tftest.hcl
└── mocks/
```

---

## CI Integration

### GitHub Actions

```yaml
- name: Run Terraform Tests
  run: |
    terraform init
    terraform test -json | tee test-results.json
    
- name: Upload Test Results
  uses: actions/upload-artifact@v4
  with:
    name: terraform-test-results
    path: test-results.json
```

### Test Filtering in CI

```yaml
# Run fast tests on PR
- name: Unit Tests
  if: github.event_name == 'pull_request'
  run: terraform test -filter=tests/unit/

# Run all tests on merge
- name: Full Tests
  if: github.ref == 'refs/heads/main'
  run: terraform test
```
