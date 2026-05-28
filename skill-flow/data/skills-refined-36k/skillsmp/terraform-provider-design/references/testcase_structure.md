# TestCase Structure for Terraform Acceptance Testing

## Overview

Acceptance tests in Terraform providers are built around `resource.TestCase`, a Go struct that defines the complete test lifecycle. Every acceptance test follows the pattern:

```go
func TestAccResourceName(t *testing.T) {
    resource.Test(t, resource.TestCase{
        // TestCase configuration
    })
}
```

**Naming Convention**: All acceptance tests MUST start with `TestAcc` prefix.

## TestCase Anatomy

### Complete Example

```go
func TestAccExampleResource(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        TerraformVersionChecks:   []tfversion.TerraformVersionCheck{
            tfversion.SkipBelow(tfversion.Version1_8_0),
        },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckExampleResourceDestroy,
        Steps: []resource.TestStep{
            // Test steps here
        },
    })
}
```

## TestCase Fields Reference

### Required Fields

#### ProtoV6ProviderFactories (Plugin Framework)

Maps provider names to their factory functions:

```go
var testAccProtoV6ProviderFactories = map[string]func() (tfprotov6.ProviderServer, error){
    "example": providerserver.NewProtocol6WithError(New("test")()),
}
```

**Usage in TestCase**:
```go
ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
```

**Key Points**:
- Required for Plugin Framework providers
- Initialize once in `provider_test.go`
- Only included providers load during tests
- Maps provider name to implementation

#### Providers (Legacy SDK)

For older SDKv2 providers:

```go
var testAccProviders = map[string]*schema.Provider{
    "example": New(),
}
```

**Note**: Use `ProtoV6ProviderFactories` for modern Plugin Framework providers.

#### Steps

Array of `TestStep` structs defining test sequence:

```go
Steps: []resource.TestStep{
    {
        Config: testAccResourceConfig("initial"),
        Check: resource.ComposeAggregateTestCheckFunc(
            resource.TestCheckResourceAttr("example_resource.test", "name", "initial"),
        ),
    },
    {
        ResourceName:      "example_resource.test",
        ImportState:       true,
        ImportStateVerify: true,
    },
    {
        Config: testAccResourceConfig("updated"),
        Check: resource.ComposeAggregateTestCheckFunc(
            resource.TestCheckResourceAttr("example_resource.test", "name", "updated"),
        ),
    },
}
```

**Test Step Types**:
1. **Config step** - Apply Terraform configuration
2. **Import step** - Test `terraform import`
3. **Refresh step** - Test state refresh
4. **Plan-only step** - Generate plan without apply

### Optional Fields

#### PreCheck

Function that validates test prerequisites before any steps execute:

```go
PreCheck: func() { testAccPreCheck(t) },
```

**Common PreCheck Implementation**:

```go
func testAccPreCheck(t *testing.T) {
    // Verify required environment variables
    if v := os.Getenv("EXAMPLE_API_KEY"); v == "" {
        t.Fatal("EXAMPLE_API_KEY must be set for acceptance tests")
    }

    if v := os.Getenv("EXAMPLE_ENDPOINT"); v == "" {
        t.Skip("EXAMPLE_ENDPOINT not set, skipping acceptance tests")
    }

    // Verify API connectivity (optional)
    client, err := NewClient(os.Getenv("EXAMPLE_ENDPOINT"), os.Getenv("EXAMPLE_API_KEY"))
    if err != nil {
        t.Fatalf("Failed to create test client: %v", err)
    }

    // Test basic API call
    if err := client.Ping(); err != nil {
        t.Fatalf("API connectivity check failed: %v", err)
    }
}
```

**Best Practices**:
- Validate ALL required environment variables
- Use `t.Fatal()` for missing required variables
- Use `t.Skip()` for optional configurations
- Keep PreCheck fast (<5 seconds)
- Test API connectivity if critical

#### TerraformVersionChecks

Array of version constraints that run after PreCheck:

```go
TerraformVersionChecks: []tfversion.TerraformVersionCheck{
    tfversion.SkipBelow(tfversion.Version1_8_0),
    tfversion.SkipAbove(tfversion.Version1_10_0),
},
```

**Available Checks**:

```go
import "github.com/hashicorp/terraform-plugin-testing/tfversion"

// Skip test if Terraform version is below specified
tfversion.SkipBelow(tfversion.Version1_8_0)

// Skip test if Terraform version is above specified
tfversion.SkipAbove(tfversion.Version1_10_0)

// Skip test if Terraform version matches exactly
tfversion.SkipIf(tfversion.Version1_9_0)

// Skip test if version is between range (inclusive)
tfversion.SkipBetween(tfversion.Version1_8_0, tfversion.Version1_9_5)

// Require specific version
tfversion.RequireAbove(tfversion.Version1_8_0)
tfversion.RequireBelow(tfversion.Version1_10_0)
```

**Use Cases**:
- Feature requires specific Terraform version
- Bug exists in certain Terraform versions
- Testing version-specific behavior
- Compatibility testing across versions

**Example**:

```go
func TestAccResource_NewFeature(t *testing.T) {
    resource.Test(t, resource.TestCase{
        TerraformVersionChecks: []tfversion.TerraformVersionCheck{
            // Feature requires Terraform 1.8+
            tfversion.SkipBelow(tfversion.Version1_8_0),
        },
        // ... rest of test
    })
}
```

#### CheckDestroy

Function that verifies resource cleanup after all test steps complete:

```go
CheckDestroy: testAccCheckExampleResourceDestroy,
```

**Implementation Pattern**:

```go
func testAccCheckExampleResourceDestroy(s *terraform.State) error {
    client := createTestClient(&testing.T{})
    ctx := context.Background()

    for _, rs := range s.RootModule().Resources {
        // Only check resources of this type
        if rs.Type != "example_resource" {
            continue
        }

        // Verify resource is deleted with retry logic
        deleted, err := verifyResourceDeleted(ctx, client,
            "ServiceName", "getMethod", rs.Primary.ID, 4)

        if !deleted {
            if err != nil {
                return fmt.Errorf("error checking deletion of %s: %w", rs.Primary.ID, err)
            }
            return fmt.Errorf("resource %s still exists", rs.Primary.ID)
        }
    }

    return nil
}
```

**Best Practices**:
- Use exponential backoff for eventual consistency
- Check only resources managed by the provider
- Return descriptive errors
- Target 15-30 second completion
- Handle API errors gracefully

**When CheckDestroy Runs**:
1. All test steps complete successfully
2. Terraform destroy operation completes
3. CheckDestroy function executes
4. Test fails if CheckDestroy returns error

#### IsUnitTest

Boolean flag allowing tests to run without `TF_ACC=1`:

```go
IsUnitTest: true,
```

**⚠️ Use Cautiously**:
- Only for fast, local-only tests
- No real infrastructure created
- Typically with mocked providers
- NOT for standard acceptance tests

**Example Use Case**:

```go
func TestAccProvider_Configuration(t *testing.T) {
    resource.Test(t, resource.TestCase{
        IsUnitTest:               true,  // Test provider config only
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {
                Config: `
                    provider "example" {
                        endpoint = "https://api.example.com"
                        api_key  = "test-key"
                    }
                `,
            },
        },
    })
}
```

#### ErrorCheck

Custom function for error handling:

```go
ErrorCheck: func(err error) error {
    // Custom error handling logic
    if isExpectedError(err) {
        return nil  // Suppress expected errors
    }
    return err
},
```

**Use Cases**:
- Suppress known transient errors
- Add context to error messages
- Log errors for debugging
- Handle provider-specific error patterns

#### ProtoV5ProviderFactories

For Plugin Framework providers using Protocol version 5:

```go
ProtoV5ProviderFactories: map[string]func() (tfprotov5.ProviderServer, error){
    "example": providerserver.NewProtocol5WithError(New("test")()),
},
```

#### ExternalProviders

For testing with external providers:

```go
ExternalProviders: map[string]resource.ExternalProvider{
    "aws": {
        Source:            "hashicorp/aws",
        VersionConstraint: "~> 5.0",
    },
},
```

## TestStep Structure

Each test step represents a distinct test operation:

### Config Step (Most Common)

Apply Terraform configuration and verify results:

```go
{
    Config: testAccResourceConfig("value"),
    Check: resource.ComposeAggregateTestCheckFunc(
        resource.TestCheckResourceAttr("example_resource.test", "name", "value"),
    ),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectNonEmptyPlan(),
        },
    },
}
```

**Fields**:
- `Config` - Terraform configuration string
- `Check` - Validation function(s) for state
- `ConfigPlanChecks` - Plan assertions
- `ConfigStateChecks` - State checks (Plugin Framework)

### Import Step

Test `terraform import` functionality:

```go
{
    ResourceName:            "example_resource.test",
    ImportState:             true,
    ImportStateVerify:       true,
    ImportStateVerifyIgnore: []string{"last_updated"},
}
```

**Fields**:
- `ResourceName` - Resource to import
- `ImportState` - Enable import mode
- `ImportStateVerify` - Compare imported state to config
- `ImportStateVerifyIgnore` - Skip specific attributes
- `ImportStateId` - Custom import ID (optional)

### Refresh Step

Test state refresh without changes:

```go
{
    RefreshState: true,
    Check: resource.ComposeAggregateTestCheckFunc(
        resource.TestCheckResourceAttr("example_resource.test", "name", "value"),
    ),
}
```

### Plan-Only Step

Generate plan without applying:

```go
{
    Config:       testAccResourceConfig("value"),
    PlanOnly:     true,
    ExpectNonEmptyPlan: true,
}
```

## Execution Flow

### Standard Test Lifecycle

```
1. PreCheck()                    → Validate prerequisites
2. TerraformVersionChecks        → Check Terraform version
3. For each TestStep:
   a. Generate plan              → terraform plan
   b. ConfigPlanChecks.PreApply  → Verify plan
   c. Apply plan                 → terraform apply
   d. ConfigPlanChecks.PostApply → Verify post-apply
   e. Check functions            → Validate state
   f. ConfigStateChecks          → Advanced state validation
   g. Refresh state              → terraform refresh
   h. Final plan                 → Verify no changes
4. Destroy resources             → terraform destroy
5. CheckDestroy()                → Verify cleanup
```

### Step-by-Step Example

```go
func TestAccResource_Complete(t *testing.T) {
    resource.Test(t, resource.TestCase{
        // 1. Validate prerequisites
        PreCheck: func() { testAccPreCheck(t) },

        // 2. Check Terraform version
        TerraformVersionChecks: []tfversion.TerraformVersionCheck{
            tfversion.SkipBelow(tfversion.Version1_8_0),
        },

        // Provider setup
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,

        // 5. Verify cleanup after destroy
        CheckDestroy: testAccCheckResourceDestroy,

        // 3. Test steps
        Steps: []resource.TestStep{
            // Step 1: Create resource
            {
                Config: testAccResourceConfig("initial"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "name", "initial"),
                ),
            },

            // Step 2: Test import
            {
                ResourceName:      "example_resource.test",
                ImportState:       true,
                ImportStateVerify: true,
            },

            // Step 3: Update resource
            {
                Config: testAccResourceConfig("updated"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectNonEmptyPlan(), // Verify update detected
                    },
                },
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "name", "updated"),
                ),
            },

            // Step 4: Verify idempotency
            {
                Config: testAccResourceConfig("updated"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectEmptyPlan(), // No changes expected
                    },
                },
            },
        },
    })
}

// 4. After all steps: terraform destroy automatically runs
```

## Best Practices

### 1. Test Organization

**Separate concerns**:

```
provider_test.go          → Provider setup, factories, PreCheck
resource_widget_test.go   → Widget resource tests
data_source_items_test.go → Items data source tests
test_helpers.go           → Shared test utilities
```

### 2. PreCheck Validation

✅ **Good PreCheck**:

```go
func testAccPreCheck(t *testing.T) {
    required := []string{"API_KEY", "API_ENDPOINT"}
    for _, v := range required {
        if os.Getenv(v) == "" {
            t.Fatalf("%s must be set for acceptance tests", v)
        }
    }
}
```

❌ **Bad PreCheck** (no validation):

```go
func testAccPreCheck(t *testing.T) {
    // Empty - doesn't validate anything!
}
```

### 3. CheckDestroy Implementation

✅ **Good CheckDestroy** (with retry):

```go
func testAccCheckResourceDestroy(s *terraform.State) error {
    client := createTestClient(&testing.T{})

    for _, rs := range s.RootModule().Resources {
        if rs.Type != "example_resource" {
            continue
        }

        // Use exponential backoff
        deleted, _ := verifyResourceDeleted(context.Background(), client,
            "Service", "getMethod", rs.Primary.ID, 4)

        if !deleted {
            return fmt.Errorf("resource %s still exists", rs.Primary.ID)
        }
    }
    return nil
}
```

❌ **Bad CheckDestroy** (no retry):

```go
func testAccCheckResourceDestroy(s *terraform.State) error {
    client := createTestClient(&testing.T{})

    for _, rs := range s.RootModule().Resources {
        if rs.Type != "example_resource" {
            continue
        }

        // Single check - fails with eventual consistency
        _, err := client.Get(rs.Primary.ID)
        if err == nil {
            return fmt.Errorf("resource still exists")
        }
    }
    return nil
}
```

### 4. Version Constraints

Use version checks for feature-specific tests:

```go
func TestAccResource_NewFeature(t *testing.T) {
    resource.Test(t, resource.TestCase{
        TerraformVersionChecks: []tfversion.TerraformVersionCheck{
            tfversion.SkipBelow(tfversion.Version1_8_0),  // Feature requires 1.8+
        },
        // ... test for feature that requires Terraform 1.8+
    })
}
```

### 5. Multiple Test Steps

Use multiple steps to test full lifecycle:

```go
Steps: []resource.TestStep{
    // 1. Create
    {Config: config("initial"), Check: checkInitial},

    // 2. Import
    {ResourceName: "example_resource.test", ImportState: true, ImportStateVerify: true},

    // 3. Update
    {Config: config("updated"), Check: checkUpdated},

    // 4. Idempotency
    {Config: config("updated"), ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{plancheck.ExpectEmptyPlan()},
    }},
}
```

## Common Patterns

### Pattern 1: Basic CRUD Test

```go
func TestAccResource_Basic(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckResourceDestroy,
        Steps: []resource.TestStep{
            {
                Config: testAccResourceConfig("test"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "name", "test"),
                ),
            },
        },
    })
}
```

### Pattern 2: Update Test

```go
func TestAccResource_Update(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckResourceDestroy,
        Steps: []resource.TestStep{
            {Config: config("initial"), Check: checkInitial},
            {Config: config("updated"), Check: checkUpdated},
        },
    })
}
```

### Pattern 3: Import Test

```go
func TestAccResource_Import(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckResourceDestroy,
        Steps: []resource.TestStep{
            {Config: config("test"), Check: check},
            {
                ResourceName:      "example_resource.test",
                ImportState:       true,
                ImportStateVerify: true,
            },
        },
    })
}
```

### Pattern 4: Version-Specific Test

```go
func TestAccResource_NewFeature(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck: func() { testAccPreCheck(t) },
        TerraformVersionChecks: []tfversion.TerraformVersionCheck{
            tfversion.SkipBelow(tfversion.Version1_8_0),
        },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {Config: config("new-feature"), Check: check},
        },
    })
}
```

## Anti-Patterns to Avoid

❌ **Missing PreCheck**
```go
// Bad: No environment validation
PreCheck: func() {},
```

❌ **Missing CheckDestroy**
```go
// Bad: No cleanup verification
// CheckDestroy field omitted
```

❌ **Single-Step Tests**
```go
// Bad: Only tests creation, not updates or import
Steps: []resource.TestStep{
    {Config: config, Check: check},
}
```

❌ **Hardcoded Values**
```go
// Bad: Same name for all test runs
Config: `resource "example_resource" "test" { name = "test" }`,
```

✅ **Use Unique Names**
```go
name := generateUniqueTestName("test")
Config: fmt.Sprintf(`resource "example_resource" "test" { name = %q }`, name),
```

## Troubleshooting

### Common Issues

**Issue**: "Provider not found"
```
Solution: Verify ProtoV6ProviderFactories is set correctly
```

**Issue**: "TF_ACC not set"
```
Solution: Run with TF_ACC=1 or set IsUnitTest: true
```

**Issue**: "CheckDestroy failed"
```
Solution: Add exponential backoff for eventual consistency
```

**Issue**: "Import verification failed"
```
Solution: Add computed fields to ImportStateVerifyIgnore
```

## Summary

Key TestCase fields:

1. ✅ **Required**: `ProtoV6ProviderFactories`, `Steps`
2. ✅ **Recommended**: `PreCheck`, `CheckDestroy`
3. ✅ **Optional**: `TerraformVersionChecks`, `ErrorCheck`, `IsUnitTest`

Every acceptance test should:

1. Validate prerequisites in `PreCheck`
2. Test full CRUD lifecycle in `Steps`
3. Verify cleanup in `CheckDestroy`
4. Use unique resource names
5. Handle eventual consistency
