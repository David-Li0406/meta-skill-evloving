# Drift Detection Testing Guide

## Overview

Drift detection tests verify that a Terraform provider's Read operation correctly identifies when resources have been modified outside of Terraform's control. This is critical for maintaining infrastructure as code accuracy and preventing configuration drift.

## Why Drift Detection Matters

### The Problem

Resources can be modified through:
- Direct API calls
- Web console interfaces
- CLI tools
- Other automation systems
- Manual interventions

When these external changes occur, Terraform must detect them during the next `terraform plan` or `terraform refresh` to maintain state accuracy.

### The Solution

Drift detection tests simulate external modifications and verify the provider's Read operation detects the changes, allowing Terraform to restore the desired state.

## Test Structure

### Three-Step Pattern

Drift detection tests follow a three-step pattern:

1. **Create**: Establish baseline resource with known state
2. **Drift**: Modify resource externally and verify detection
3. **Restore**: Verify Terraform restores desired state

### Complete Example

```go
func TestAccExampleResource_DriftDetection(t *testing.T) {
    name := generateUniqueTestName("test-drift")

    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckExampleResourceDestroy,
        Steps: []resource.TestStep{
            // Step 1: Create resource with initial configuration
            {
                Config: testAccExampleResourceConfig(name, "initial-value"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "name", name),
                    resource.TestCheckResourceAttr("example_resource.test", "attribute", "initial-value"),
                    resource.TestCheckResourceAttrSet("example_resource.test", "id"),
                ),
            },
            // Step 2: Modify externally and verify drift detection
            {
                PreConfig: func() {
                    // External modification happens here
                    modifyResourceExternally(t, name)
                },
                Config: testAccExampleResourceConfig(name, "initial-value"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectNonEmptyPlan(), // Critical: verifies drift detected
                    },
                },
            },
            // Step 3: Verify Terraform restores desired state
            {
                Config: testAccExampleResourceConfig(name, "initial-value"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "attribute", "initial-value"),
                ),
            },
        },
    })
}
```

## Implementing External Modification

### Step-by-Step Guide

The `PreConfig` function in Step 2 performs external modification:

```go
PreConfig: func() {
    // 1. Create authenticated API client
    client := createTestClient(t)
    ctx := context.Background()

    // 2. Get resource identifier
    id := getResourceIDByName(t, "ServiceName", "getMethod", name)

    // 3. Fetch current resource state from API
    body, err := client.CallAPI(ctx, "ServiceName", "getMethod", name)
    if err != nil {
        t.Fatalf("Failed to fetch resource: %v", err)
    }

    var resourceData map[string]interface{}
    if err := json.Unmarshal(body, &resourceData); err != nil {
        t.Fatalf("Failed to parse resource: %v", err)
    }

    // 4. Modify field(s) externally
    // CRITICAL: Map snake_case (Terraform) to camelCase (API)
    resourceData["camelCaseAttribute"] = "modified-value"
    resourceData["id"] = id

    // 5. Update via API (bypass Terraform)
    _, err = client.CallAPI(ctx, "ServiceName", "updateMethod", resourceData)
    if err != nil {
        t.Fatalf("Failed to update resource: %v", err)
    }

    // 6. Wait for eventual consistency
    time.Sleep(2 * time.Second)

    // 7. Log for debugging
    t.Logf("[DEBUG] Modified attribute externally: %v", resourceData["camelCaseAttribute"])
},
```

### Common Patterns

#### Pattern 1: Simple Field Update

```go
PreConfig: func() {
    client := createTestClient(t)
    id := getResourceIDByName(t, "Service", "getResource", name)

    // Update single field
    update := map[string]interface{}{
        "id":          id,
        "description": "externally-modified",
    }

    client.CallAPI(context.Background(), "Service", "update", update)
    time.Sleep(2 * time.Second)
},
```

#### Pattern 2: Complex Entity Structure

Some APIs require full entity structure with metadata:

```go
PreConfig: func() {
    client := createTestClient(t)
    ctx := context.Background()

    // Fetch full resource
    body, _ := client.CallAPI(ctx, "Service", "getResource", name)
    var resource map[string]interface{}
    json.Unmarshal(body, &resource)

    // Wrap in API entity structure
    entity := map[string]interface{}{
        "baseType":      "ResourceType",
        "childType":     "",
        "modified":      true,
        "to_be_removed": false,
        "revision":      "",
        "uuid":          resource["uuid"],
    }

    // Copy all fields
    for k, v := range resource {
        if k != "uuid" {
            entity[k] = v
        }
    }

    // Modify target field
    entity["description"] = "externally-modified"

    // Update via API
    client.CallAPI(ctx, "Service", "update", entity, false)
    time.Sleep(2 * time.Second)
},
```

#### Pattern 3: Multiple Field Changes

```go
PreConfig: func() {
    client := createTestClient(t)
    body, _ := client.CallAPI(context.Background(), "Service", "get", name)
    var resource map[string]interface{}
    json.Unmarshal(body, &resource)

    // Modify multiple fields
    resource["description"] = "modified"
    resource["enabled"] = false
    resource["tags"] = []string{"external-tag"}

    client.CallAPI(context.Background(), "Service", "update", resource)
    time.Sleep(2 * time.Second)
},
```

## Field Name Mapping

### The Challenge

Terraform schemas use `snake_case` (lowercase with underscores), but many APIs use `camelCase` or other conventions. This creates a mapping challenge when modifying resources externally.

### Documentation Strategy

Document all field mappings in `test_helpers.go`:

```go
// BCM API Field Name Mappings
//
// The BCM API uses camelCase field names, while Terraform schemas use snake_case.
// This mapping is critical for drift detection tests when modifying resources via API.
//
// Resource: bcm_software_image
//   Terraform Schema         API Field
//   -----------------        ---------------
//   kernel_parameters     → kernelParameters
//   enable_sol            → enableSOL
//   sol_speed             → solSpeed
//   sol_flow_control      → solFlowControl
//   sol_port              → solPort
//   kernel_output_console → kernelOutputConsole
//   software_image_proxy  → softwareImageProxy
//   original_image        → originalImage
//   notes                 → notes (unchanged)
//
// Resource: bcm_device_category
//   Terraform Schema           API Field
//   -----------------          ---------------
//   kernel_parameters       → kernelParameters
//   install_boot_record     → installBootRecord
//   allow_networking_restart → allowNetworkingRestart
//   management_network      → managementNetwork
//   boot_loader             → bootLoader
//   software_image_proxy    → softwareImageProxy
```

### Mapping Helper Function

```go
// toAPIFieldName converts Terraform snake_case to API camelCase
func toAPIFieldName(terraformField string) string {
    // Special cases (acronyms, etc.)
    specialCases := map[string]string{
        "enable_sol":       "enableSOL",
        "sol_speed":        "solSpeed",
        "sol_flow_control": "solFlowControl",
        "sol_port":         "solPort",
    }

    if apiName, ok := specialCases[terraformField]; ok {
        return apiName
    }

    // Standard conversion: kernel_parameters → kernelParameters
    parts := strings.Split(terraformField, "_")
    for i := 1; i < len(parts); i++ {
        parts[i] = strings.Title(parts[i])
    }
    return strings.Join(parts, "")
}

// toTerraformFieldName converts API camelCase to Terraform snake_case
func toTerraformFieldName(apiField string) string {
    // Insert underscores before capitals
    var result []rune
    for i, r := range apiField {
        if i > 0 && unicode.IsUpper(r) {
            result = append(result, '_')
        }
        result = append(result, unicode.ToLower(r))
    }
    return string(result)
}
```

## Eventual Consistency Handling

### The Problem

Many APIs exhibit eventual consistency:
- Updates take time to propagate
- Reads immediately after writes may return stale data
- Distributed systems need time to synchronize

### The Solution

Add explicit wait periods after external modifications:

```go
// Update via API
client.CallAPI(ctx, "Service", "update", resourceData)

// Wait for eventual consistency (typically 2 seconds)
time.Sleep(2 * time.Second)
```

### Timing Guidelines

| Scenario | Recommended Wait | Reasoning |
|----------|------------------|-----------|
| Simple field update | 2 seconds | Typical API propagation delay |
| Complex entity update | 2-5 seconds | More fields = more propagation time |
| Multi-region update | 5-10 seconds | Cross-region replication delay |
| Background job trigger | 10-30 seconds | Async processing completion |

### Exponential Backoff Alternative

For more robust testing:

```go
func waitForFieldUpdate(ctx context.Context, client *APIClient,
    resourceName, fieldName string, expectedValue interface{}, maxRetries int) error {

    for i := 0; i < maxRetries; i++ {
        body, _ := client.CallAPI(ctx, "Service", "get", resourceName)
        var resource map[string]interface{}
        json.Unmarshal(body, &resource)

        if resource[fieldName] == expectedValue {
            return nil
        }

        // Exponential backoff
        time.Sleep(time.Duration(1<<uint(i)) * time.Second)
    }

    return fmt.Errorf("field %s did not reach expected value", fieldName)
}
```

## Plan Checks for Drift Verification

### ExpectNonEmptyPlan

The critical assertion for drift detection:

```go
ConfigPlanChecks: resource.ConfigPlanChecks{
    PreApply: []plancheck.PlanCheck{
        plancheck.ExpectNonEmptyPlan(),
    },
},
```

**What it verifies:**
- Terraform detected the external change
- A plan was generated with updates
- The Read operation correctly identified drift

**When it fails:**
- Read operation didn't detect the change
- Provider incorrectly considers resources in sync
- Field mapping issues (wrong API field modified)

### ExpectResourceAction

For more specific drift validation:

```go
ConfigPlanChecks: resource.ConfigPlanChecks{
    PreApply: []plancheck.PlanCheck{
        plancheck.ExpectResourceAction("example_resource.test", plancheck.ResourceActionUpdate),
    },
},
```

## Common Pitfalls

### ❌ Pitfall 1: Incorrect Field Mapping

```go
// Wrong: Using Terraform field name in API call
resourceData["kernel_parameters"] = "modified"  // API won't recognize this

// Correct: Using API field name
resourceData["kernelParameters"] = "modified"
```

### ❌ Pitfall 2: Missing Eventual Consistency Wait

```go
// Wrong: No wait after update
client.CallAPI(ctx, "Service", "update", resourceData)
// Terraform refresh happens immediately - may see stale data

// Correct: Wait for propagation
client.CallAPI(ctx, "Service", "update", resourceData)
time.Sleep(2 * time.Second)
```

### ❌ Pitfall 3: Incomplete API Entity

```go
// Wrong: Partial entity (missing required metadata)
update := map[string]interface{}{
    "id":          id,
    "description": "modified",
}

// Correct: Full entity with metadata
entity := map[string]interface{}{
    "baseType":      "ResourceType",
    "modified":      true,
    "uuid":          id,
    "description":   "modified",
    // ... all other fields
}
```

### ❌ Pitfall 4: Not Verifying Restore

```go
// Wrong: Only two steps (create + drift)
Steps: []resource.TestStep{
    {Config: config("initial"), Check: ...},
    {PreConfig: drift, Config: config("initial"), ConfigPlanChecks: ...},
    // Missing: verification that Terraform restored state
}

// Correct: Three steps including restore verification
Steps: []resource.TestStep{
    {Config: config("initial"), Check: ...},
    {PreConfig: drift, Config: config("initial"), ConfigPlanChecks: ...},
    {Config: config("initial"), Check: ...}, // Verifies restore
}
```

### ❌ Pitfall 5: Hardcoded Resource Names

```go
// Wrong: Hardcoded name (conflicts in parallel tests)
func TestAccResource_Drift(t *testing.T) {
    name := "test-resource"  // Always the same

// Correct: Unique timestamped names
func TestAccResource_Drift(t *testing.T) {
    name := generateUniqueTestName("test-drift")
```

## Testing Multiple Fields

### Pattern: Sequential Field Tests

Test each field individually for clarity:

```go
func TestAccResource_DriftKernelParameters(t *testing.T) {
    name := generateUniqueTestName("test-drift-kernel")
    // ... test kernel_parameters drift
}

func TestAccResource_DriftDescription(t *testing.T) {
    name := generateUniqueTestName("test-drift-desc")
    // ... test description drift
}
```

### Pattern: Combined Field Test

Test multiple fields together for efficiency:

```go
func TestAccResource_DriftMultipleFields(t *testing.T) {
    name := generateUniqueTestName("test-drift-multi")

    resource.Test(t, resource.TestCase{
        // ... standard setup
        Steps: []resource.TestStep{
            {Config: testAccConfig(name, "val1", "val2"), Check: ...},
            {
                PreConfig: func() {
                    client := createTestClient(t)
                    resource := fetchResource(client, name)

                    // Modify multiple fields
                    resource["field1"] = "modified1"
                    resource["field2"] = "modified2"

                    updateResource(client, resource)
                    time.Sleep(2 * time.Second)
                },
                Config: testAccConfig(name, "val1", "val2"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectNonEmptyPlan(),
                    },
                },
            },
            {Config: testAccConfig(name, "val1", "val2"), Check: ...},
        },
    })
}
```

## Debugging Drift Detection

### Enable Detailed Logging

```bash
TF_LOG=TRACE TF_ACC=1 go test -v -run TestAccResource_Drift ./internal/provider/
```

### Add Debug Statements

```go
PreConfig: func() {
    client := createTestClient(t)
    body, _ := client.CallAPI(ctx, "Service", "get", name)
    var before map[string]interface{}
    json.Unmarshal(body, &before)
    t.Logf("[DEBUG] Before modification: %+v", before)

    // Modify
    before["field"] = "modified"
    client.CallAPI(ctx, "Service", "update", before)
    time.Sleep(2 * time.Second)

    body, _ = client.CallAPI(ctx, "Service", "get", name)
    var after map[string]interface{}
    json.Unmarshal(body, &after)
    t.Logf("[DEBUG] After modification: %+v", after)
},
```

### Verify API Response

Check that external modification actually succeeded:

```go
PreConfig: func() {
    client := createTestClient(t)
    // ... modify resource

    // Verify modification took effect
    body, _ := client.CallAPI(ctx, "Service", "get", name)
    var resource map[string]interface{}
    json.Unmarshal(body, &resource)

    if resource["field"] != "modified-value" {
        t.Fatalf("External modification failed: got %v, want 'modified-value'",
            resource["field"])
    }
},
```

## Best Practices Summary

1. ✅ **Document Field Mappings**: Maintain mapping table in `test_helpers.go`
2. ✅ **Use Test Helpers**: Centralize client creation, resource lookup, and verification
3. ✅ **Wait for Consistency**: Add 2-second sleep after external modifications
4. ✅ **Unique Names**: Use `generateUniqueTestName()` for parallel test safety
5. ✅ **Three-Step Pattern**: Create → Drift → Restore
6. ✅ **Plan Checks**: Use `ExpectNonEmptyPlan()` to verify drift detection
7. ✅ **Verify Restore**: Always add third step confirming Terraform fixed drift
8. ✅ **Debug Logging**: Add `t.Logf()` statements for troubleshooting
9. ✅ **Test Each Field**: Create separate drift tests for important fields
10. ✅ **Handle API Structure**: Include all required metadata in update calls

## Real-World Example

Here's a complete drift detection test from a production provider:

```go
func TestAccCMPartSoftwareImage_DriftKernelParameters(t *testing.T) {
    imageName := generateUniqueTestName("citest-drift-kernel")

    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckCMPartSoftwareImageDestroy,
        Steps: []resource.TestStep{
            // Create with initial kernel parameters
            {
                Config: testAccCMPartSoftwareImageConfig_basic(imageName, "quiet console=tty0"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("bcm_cmpart_softwareimage.test",
                        "name", imageName),
                    resource.TestCheckResourceAttr("bcm_cmpart_softwareimage.test",
                        "kernel_parameters", "quiet console=tty0"),
                ),
            },
            // Modify kernel_parameters externally
            {
                PreConfig: func() {
                    client := createTestBCMClient(t)
                    ctx := context.Background()

                    // Get image UUID
                    uuid := getResourceUUIDByName(t, "CMPart", "getSoftwareImage", imageName)

                    // Fetch full image data
                    body, _ := client.CallJSONRPC(ctx, "CMPart", "getSoftwareImage", imageName)
                    var imageData map[string]interface{}
                    json.Unmarshal(body, &imageData)

                    // Build BCM entity structure
                    entity := map[string]interface{}{
                        "baseType":      "SoftwareImage",
                        "childType":     "",
                        "modified":      true,
                        "to_be_removed": false,
                        "revision":      "",
                        "uuid":          uuid,
                    }

                    for k, v := range imageData {
                        if k != "uuid" {
                            entity[k] = v
                        }
                    }

                    // Modify kernelParameters (snake_case → camelCase!)
                    entity["kernelParameters"] = "verbose console=ttyS0"

                    // Update via BCM API
                    client.CallJSONRPC(ctx, "CMPart", "updateSoftwareImage", entity, false)

                    // Wait for consistency
                    time.Sleep(2 * time.Second)

                    t.Logf("[DEBUG] Modified kernel_parameters to: %v",
                        entity["kernelParameters"])
                },
                Config: testAccCMPartSoftwareImageConfig_basic(imageName, "quiet console=tty0"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectNonEmptyPlan(),
                    },
                },
            },
            // Verify Terraform restores desired state
            {
                Config: testAccCMPartSoftwareImageConfig_basic(imageName, "quiet console=tty0"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("bcm_cmpart_softwareimage.test",
                        "kernel_parameters", "quiet console=tty0"),
                ),
            },
        },
    })
}
```

This example demonstrates all best practices:
- Unique timestamped name
- CheckDestroy implementation
- Three-step pattern
- Complete API entity structure
- Field name mapping (kernel_parameters → kernelParameters)
- Eventual consistency wait
- Debug logging
- Plan check for drift verification
- Restore verification
