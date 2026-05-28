# Terraform Provider TDD Patterns

## TDD Philosophy for Providers

**RED-GREEN-REFACTOR in Parallel Batches**

Terraform provider development follows strict TDD cycles with parallel execution:
- 🔴 **RED**: Write failing acceptance tests first
- 🟢 **GREEN**: Write minimal CRUD code to pass tests
- 🔄 **REFACTOR**: Improve code while keeping tests green

## Testing Pyramid

```
     Acceptance Tests (Most Important)
           /        \
          /          \
         /____________\
        /   Unit Tests  \
       /__________________\
      / Integration Tests  \
     /______________________\
```

## Test-First Development Workflow

### 1. Write Test First (RED Phase)

Before writing any resource code:

1. Define what the resource should do
2. Write acceptance test that describes the behavior
3. Run test and verify it fails
4. Understand WHY it fails

### 2. Make It Pass (GREEN Phase)

Implement minimum code to pass:

1. Start with hardcoded values if needed
2. Focus solely on making test green
3. Don't optimize or add features
4. Verify test passes

### 3. Improve Code (REFACTOR Phase)

With passing tests:

1. Add real API integration
2. Improve error handling
3. Add validation
4. Optimize performance
5. Keep tests green throughout

## Acceptance Test Structure

### Required Test Steps

According to HashiCorp's official testing patterns, every resource MUST test:

1. **Basic Attribute Verification** - Verifies resource creation, state correctness, and idempotency
2. **Update/Modification Test** - Tests configuration changes (superset of basic test)
3. **ImportState Test** - Validates `terraform import` functionality
4. **Delete with CheckDestroy** - Verifies cleanup after tests complete

**HashiCorp Recommendation**: "It's common for resources to just have the update test, as it is a superset of the basic test."

### Additional Recommended Tests

5. **Drift Detection Test** - Verifies provider detects external changes
6. **Idempotency Test** - Confirms repeated applies produce no changes
7. **Error Cases** - Tests expected validation failures with `ExpectError`
8. **Regression Tests** - Documents and tests bug fixes

### Test Pattern Template

```go
func TestAccInstanceResource(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            // Create and Read testing
            {
                Config: testAccInstanceResourceConfig("test"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("bcm_instance.test", "name", "test"),
                    resource.TestCheckResourceAttrSet("bcm_instance.test", "id"),
                    resource.TestCheckResourceAttrSet("bcm_instance.test", "created_at"),
                ),
            },
            // ImportState testing
            {
                ResourceName:      "bcm_instance.test",
                ImportState:       true,
                ImportStateVerify: true,
                ImportStateVerifyIgnore: []string{"last_updated"},
            },
            // Update and Read testing
            {
                Config: testAccInstanceResourceConfig("test-updated"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("bcm_instance.test", "name", "test-updated"),
                ),
            },
        },
    })
}

func testAccInstanceResourceConfig(name string) string {
    return fmt.Sprintf(`
resource "bcm_instance" "test" {
  name = %[1]q
}
`, name)
}
```

## Minimal Implementation Pattern (GREEN Phase)

Start with hardcoded values to pass tests quickly:

```go
func (r *InstanceResource) Create(ctx context.Context, req resource.CreateRequest, resp *resource.CreateResponse) {
    var data InstanceResourceModel
    resp.Diagnostics.Append(req.Plan.Get(ctx, &data)...)
    if resp.Diagnostics.HasError() {
        return
    }

    // Minimal implementation - hardcoded ID
    data.ID = types.StringValue("instance-123")

    tflog.Trace(ctx, "created instance resource")
    resp.Diagnostics.Append(resp.State.Set(ctx, &data)...)
}
```

## Refactoring Pattern (REFACTOR Phase)

Add real API integration after tests pass:

```go
func (r *InstanceResource) Create(ctx context.Context, req resource.CreateRequest, resp *resource.CreateResponse) {
    var data InstanceResourceModel
    resp.Diagnostics.Append(req.Plan.Get(ctx, &data)...)
    if resp.Diagnostics.HasError() {
        return
    }

    // Make actual API call
    instance, err := r.client.CreateInstance(ctx, data.Name.ValueString())
    if err != nil {
        resp.Diagnostics.AddError(
            "Error Creating Instance",
            "Could not create instance, unexpected error: "+err.Error(),
        )
        return
    }

    data.ID = types.StringValue(instance.ID)
    tflog.Trace(ctx, "created instance resource")
    resp.Diagnostics.Append(resp.State.Set(ctx, &data)...)
}
```

## Test Helper Patterns

### Why Test Helpers?

Test helpers eliminate code duplication across tests and provide reusable utilities for:
- Creating authenticated API clients
- Querying resources by name or ID
- Verifying resource deletion with retry logic
- Generating unique test names
- Documenting field name mappings (snake_case vs camelCase)

### Essential Test Helpers

Create `internal/provider/test_helpers.go` with these functions:

```go
package provider

import (
    "context"
    "encoding/json"
    "fmt"
    "os"
    "testing"
    "time"
)

// Field Name Mappings Documentation
//
// Document snake_case (Terraform) to camelCase (API) mappings here.
// This is critical for drift detection tests when modifying resources via API.
//
// Example Mappings:
//   Terraform Schema       API Field
//   -----------------      ---------------
//   kernel_parameters   → kernelParameters
//   enable_sol          → enableSOL
//   management_network  → managementNetwork

// createTestClient creates an authenticated API client for test use
//
// Used by:
// - Drift detection tests (PreConfig to modify resources externally)
// - CheckDestroy functions (to verify resource deletion)
// - PreCheck cleanup functions (to remove leftover test resources)
//
// Environment Variables (required):
//   API_ENDPOINT - API endpoint (e.g., https://api.example.com)
//   API_USERNAME - API username
//   API_PASSWORD - API password
func createTestClient(t *testing.T) *APIClient {
    endpoint := os.Getenv("API_ENDPOINT")
    username := os.Getenv("API_USERNAME")
    password := os.Getenv("API_PASSWORD")

    if endpoint == "" || username == "" || password == "" {
        t.Fatalf("API credentials not set (API_ENDPOINT, API_USERNAME, API_PASSWORD)")
    }

    client, err := NewAPIClient(context.Background(), endpoint, username, password, true, 30)
    if err != nil {
        t.Fatalf("Failed to create API client: %v", err)
    }

    return client
}

// getResourceIDByName queries API to get resource ID by name
//
// This is essential for drift detection tests that need to modify resources
// via the API after Terraform creates them.
//
// Parameters:
//   t - Testing context
//   service - API service name (e.g., "ResourceService")
//   method - API method name (e.g., "getResource")
//   name - Resource name to look up
//
// Returns: Resource ID (UUID or identifier string)
func getResourceIDByName(t *testing.T, service, method, name string) string {
    client := createTestClient(t)
    body, err := client.CallAPI(context.Background(), service, method, name)
    if err != nil {
        t.Fatalf("Failed to get resource %s: %v", name, err)
    }

    var resource map[string]interface{}
    if err := json.Unmarshal(body, &resource); err != nil {
        t.Fatalf("Failed to parse resource response: %v", err)
    }

    id, ok := resource["id"].(string)
    if !ok {
        t.Fatalf("Resource %s has no ID field", name)
    }

    return id
}

// verifyResourceDeleted polls API with exponential backoff to verify deletion
//
// Handles eventual consistency by retrying resource lookups with exponentially
// increasing wait times. Designed to complete within 30 seconds (PreCheck requirement).
//
// Parameters:
//   ctx - Context for API calls (can include timeout)
//   client - Authenticated API client
//   service - API service name (e.g., "ResourceService")
//   method - API method name (e.g., "getResource")
//   identifier - Resource identifier (name or UUID)
//   maxRetries - Maximum retry attempts (e.g., 4 for 15s total: 1+2+4+8)
//
// Returns:
//   deleted - true if resource not found (successfully deleted)
//   error - any error encountered during verification
func verifyResourceDeleted(ctx context.Context, client *APIClient,
    service, method, identifier string, maxRetries int) (bool, error) {

    for i := 0; i < maxRetries; i++ {
        _, err := client.CallAPI(ctx, service, method, identifier)
        if err != nil {
            // Resource not found - successfully deleted
            return true, nil
        }

        // Wait before retry (exponential backoff: 1s, 2s, 4s, 8s, ...)
        if i < maxRetries-1 {
            backoff := time.Duration(1<<uint(i)) * time.Second
            time.Sleep(backoff)
        }
    }

    return false, fmt.Errorf("resource %s still exists after %d retries", identifier, maxRetries)
}

// generateUniqueTestName creates timestamped unique test names
//
// Prevents conflicts when running tests in parallel or when leftover resources exist.
// Use "citest" or similar prefix for easy identification and cleanup.
//
// Example: generateUniqueTestName("citest-image") → "citest-image-1704912345"
func generateUniqueTestName(prefix string) string {
    return fmt.Sprintf("%s-%d", prefix, time.Now().Unix())
}
```

## CheckDestroy Pattern

### Purpose

`CheckDestroy` verifies that Terraform properly cleaned up all resources after test completion. It's called after all test steps finish.

### Implementation

```go
// testAccCheckResourceDestroy verifies resource cleanup after test completion
func testAccCheckResourceDestroy(s *terraform.State) error {
    client := createTestClient(&testing.T{})
    ctx := context.Background()

    for _, rs := range s.RootModule().Resources {
        // Only check resources of this type
        if rs.Type != "example_resource" {
            continue
        }

        // Verify resource is deleted with exponential backoff
        deleted, err := verifyResourceDeleted(ctx, client,
            "ResourceService", "getResource", rs.Primary.ID, 4)

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

### Adding to TestCase

```go
resource.Test(t, resource.TestCase{
    PreCheck:                 func() { testAccPreCheck(t) },
    ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
    CheckDestroy:             testAccCheckResourceDestroy, // Add this line
    Steps: []resource.TestStep{
        // ... test steps
    },
})
```

### CheckDestroy Best Practices

1. **Exponential Backoff**: Use `verifyResourceDeleted()` helper to handle eventual consistency
2. **Resource Type Filtering**: Only check resources managed by the provider
3. **Error Context**: Wrap errors with `%w` to preserve error chains
4. **Timeout Budget**: Target completion within 15-30 seconds (typical test cleanup time)
5. **Retry Count**: 4 retries (1s + 2s + 4s + 8s = 15s total) is usually sufficient

## Drift Detection Test Pattern

### Purpose

Drift detection tests verify that the provider's Read operation correctly detects when resources are modified outside of Terraform.

### Three-Step Test Structure

```go
func TestAccResource_Drift(t *testing.T) {
    name := generateUniqueTestName("test-drift")

    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckResourceDestroy,
        Steps: []resource.TestStep{
            // Step 1: Create resource with initial value
            {
                Config: testAccResourceConfig(name, "initial-value"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "attribute", "initial-value"),
                ),
            },
            // Step 2: Modify resource externally via API (drift)
            {
                PreConfig: func() {
                    client := createTestClient(t)
                    ctx := context.Background()

                    // Get resource ID by name
                    id := getResourceIDByName(t, "ResourceService", "getResource", name)

                    // Fetch full resource data
                    body, _ := client.CallAPI(ctx, "ResourceService", "getResource", name)
                    var resourceData map[string]interface{}
                    json.Unmarshal(body, &resourceData)

                    // Modify field externally
                    // IMPORTANT: Map snake_case → camelCase (see field mappings in test_helpers.go)
                    resourceData["camelCaseAttribute"] = "modified-value"
                    resourceData["id"] = id

                    // Update via API
                    client.CallAPI(ctx, "ResourceService", "updateResource", resourceData)

                    // Wait for eventual consistency
                    time.Sleep(2 * time.Second)

                    t.Logf("[DEBUG] Modified attribute externally to: %v", resourceData["camelCaseAttribute"])
                },
                Config: testAccResourceConfig(name, "initial-value"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectNonEmptyPlan(), // Verify drift detected
                    },
                },
            },
            // Step 3: Terraform restores desired state
            {
                Config: testAccResourceConfig(name, "initial-value"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "attribute", "initial-value"),
                ),
            },
        },
    })
}
```

### Drift Detection Best Practices

1. **Field Name Mapping**: Document snake_case ↔ camelCase mappings in `test_helpers.go`
2. **API Entity Structure**: Some APIs require full entity structure (baseType, uuid, revision, etc.)
3. **Eventual Consistency**: Add 2-second sleep after API modifications for changes to propagate
4. **UUID Lookup**: Use `getResourceIDByName()` helper for consistent resource identification
5. **Plan Checks**: Use `plancheck.ExpectNonEmptyPlan()` to verify drift was detected
6. **Restore Step**: Always add a third step to verify Terraform restores desired state
7. **Unique Names**: Use `generateUniqueTestName()` to avoid conflicts with parallel tests

## State Check Functions

### Common Check Patterns

```go
// Exact value match
resource.TestCheckResourceAttr("bcm_instance.test", "name", "expected-value")

// Attribute exists with any value
resource.TestCheckResourceAttrSet("bcm_instance.test", "id")

// Match two resources' attributes
resource.TestCheckResourceAttrPair(
    "bcm_instance.test", "vpc_id",
    "bcm_vpc.test", "id",
)

// Combine multiple checks (continue on failure)
resource.ComposeAggregateTestCheckFunc(
    resource.TestCheckResourceAttr(...),
    resource.TestCheckResourceAttrSet(...),
)
```

## Provider Test Setup

```go
// internal/provider/provider_test.go
package provider

import (
    "testing"
    "github.com/hashicorp/terraform-plugin-framework/providerserver"
    "github.com/hashicorp/terraform-plugin-go/tfprotov6"
)

var testAccProtoV6ProviderFactories = map[string]func() (tfprotov6.ProviderServer, error){
    "bcm": providerserver.NewProtocol6WithError(New("test")()),
}

func testAccPreCheck(t *testing.T) {
    // Check for required environment variables
    // if v := os.Getenv("BCM_API_KEY"); v == "" {
    //     t.Fatal("BCM_API_KEY must be set for acceptance tests")
    // }
}
```

## Running Tests

### Unit Tests
```bash
go test -v ./...
go test -race ./...
```

### Acceptance Tests
```bash
TF_ACC=1 go test -v -timeout 120m ./internal/provider/
TF_ACC=1 go test -v -parallel=4 -timeout 120m ./...
```

### With Logging
```bash
TF_LOG=TRACE TF_ACC=1 go test -v ./internal/provider/
```

## Test Quality Standards

- **Coverage**: All CRUD operations tested
- **Import**: All resources must be importable
- **Edge Cases**: Error handling validated
- **Pass Rate**: 100% required
- **Execution Time**: <120m for full acceptance suite
- **Parallel Execution**: 4-8 parallel tests recommended

## Security Testing

Mark sensitive attributes appropriately:

```go
func (r *APIKeyResource) Schema(ctx context.Context, req resource.SchemaRequest, resp *resource.SchemaResponse) {
    resp.Schema = schema.Schema{
        Attributes: map[string]schema.Attribute{
            "key_value": schema.StringAttribute{
                Computed:  true,
                Sensitive: true, // Prevents display in output
            },
        },
    }
}
```

## Data Source Testing

```go
func TestAccUserDataSource(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {
                Config: testAccUserDataSourceConfig,
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("data.bcm_user.test", "username", "admin"),
                    resource.TestCheckResourceAttrSet("data.bcm_user.test", "id"),
                ),
            },
        },
    })
}

const testAccUserDataSourceConfig = `
data "bcm_user" "test" {
  username = "admin"
}
`
```

## Test Verification Best Practices

### What to Verify in Tests

**Basic Resource Test Should:**
1. Plan and apply configuration without error
2. Verify expected attributes saved to state
3. Verify values match remote API/service
4. Verify subsequent plan produces no diff

**Update Test Should:**
1. Apply initial configuration
2. Apply modified configuration
3. Verify updates reflected in state
4. Verify updates reflected in remote API

### CheckDestroy Function

Always implement CheckDestroy to verify cleanup:

```go
func testAccCheckExampleResourceDestroy(s *terraform.State) error {
    // Retrieve API client from provider
    // client := testAccProvider.Meta().(*APIClient)

    for _, rs := range s.RootModule().Resources {
        if rs.Type != "example_resource" {
            continue
        }

        // Try to find the resource
        _, err := client.GetResource(rs.Primary.ID)
        if err == nil {
            return fmt.Errorf("Resource %s still exists", rs.Primary.ID)
        }

        // Verify it's a "not found" error
        if !isNotFoundError(err) {
            return err
        }
    }

    return nil
}
```

### Testing Edge Cases

```go
// Test error handling
func TestAccExampleResource_InvalidConfig(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {
                Config:      testAccExampleResourceConfig_Invalid(),
                ExpectError: regexp.MustCompile("invalid configuration"),
            },
        },
    })
}

// Test disappears (external deletion)
func TestAccExampleResource_Disappears(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {
                Config: testAccExampleResourceConfig("test"),
                Check: resource.ComposeTestCheckFunc(
                    testAccCheckExampleResourceExists("example_resource.test"),
                    testAccCheckExampleResourceDisappears("example_resource.test"),
                ),
                ExpectNonEmptyPlan: true,
            },
        },
    })
}
```

## Common Anti-Patterns to Avoid

❌ **Skipping ImportState Tests** - Always test import functionality
❌ **Hardcoded Test Values** - Use unique resource names per test run
❌ **Incomplete CRUD** - Test all Create, Read, Update, Delete operations
❌ **Ignoring Error Cases** - Test API failures and invalid inputs
❌ **Missing Documentation** - Keep examples/ and docs/ in sync with code
❌ **Not Testing State Drift** - Verify Read correctly detects external changes
❌ **Brittle Tests** - Don't depend on external state or ordering
❌ **No CheckDestroy** - Always verify resources are destroyed
❌ **Skipping Edge Cases** - Test disappears, conflicts, invalid configs
❌ **Poor Test Isolation** - Each test should be fully independent
