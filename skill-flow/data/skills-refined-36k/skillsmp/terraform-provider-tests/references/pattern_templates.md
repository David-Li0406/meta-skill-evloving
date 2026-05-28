# Modern Testing Pattern Templates

Ready-to-use code templates for common modernization patterns.

## Table of Contents

1. [Required Imports](#required-imports)
2. [Legacy to Modern Conversion](#legacy-to-modern-conversion)
3. [Idempotency Verification](#idempotency-verification)
4. [Import Test Step](#import-test-step)
5. [Drift Detection Test](#drift-detection-test)
6. [ID Consistency Tracking](#id-consistency-tracking)
7. [knownvalue Type Matchers](#knownvalue-type-matchers)
8. [Complete Test Example](#complete-test-example)

---

## Required Imports

Add these to any file using modern patterns:

```go
import (
    "github.com/hashicorp/terraform-plugin-testing/helper/resource"
    "github.com/hashicorp/terraform-plugin-testing/plancheck"
    "github.com/hashicorp/terraform-plugin-testing/statecheck"
    "github.com/hashicorp/terraform-plugin-testing/knownvalue"
    "github.com/hashicorp/terraform-plugin-testing/tfjsonpath"
    "github.com/hashicorp/terraform-plugin-testing/compare"
)
```

For drift detection tests, also add:

```go
import (
    "context"
    "encoding/json"
    "time"
)
```

---

## Legacy to Modern Conversion

### Pattern: String Attribute

**Legacy**:
```go
Check: resource.ComposeAggregateTestCheckFunc(
    resource.TestCheckResourceAttr("example_resource.test", "name", "expected-value"),
),
```

**Modern**:
```go
ConfigStateChecks: []statecheck.StateCheck{
    statecheck.ExpectKnownValue(
        "example_resource.test",
        tfjsonpath.New("name"),
        knownvalue.StringExact("expected-value"),
    ),
},
```

### Pattern: Boolean Attribute

**Legacy**:
```go
resource.TestCheckResourceAttr("example_resource.test", "enabled", "true"),
```

**Modern**:
```go
statecheck.ExpectKnownValue(
    "example_resource.test",
    tfjsonpath.New("enabled"),
    knownvalue.Bool(true),
),
```

### Pattern: Numeric Attribute

**Legacy**:
```go
resource.TestCheckResourceAttr("example_resource.test", "port", "8080"),
```

**Modern**:
```go
statecheck.ExpectKnownValue(
    "example_resource.test",
    tfjsonpath.New("port"),
    knownvalue.Int64Exact(8080),
),
```

### Pattern: Computed Attribute (UUID, ID)

**Legacy**:
```go
resource.TestCheckResourceAttrSet("example_resource.test", "uuid"),
resource.TestCheckResourceAttrSet("example_resource.test", "id"),
```

**Modern**:
```go
statecheck.ExpectKnownValue(
    "example_resource.test",
    tfjsonpath.New("uuid"),
    knownvalue.NotNull(),
),
statecheck.ExpectKnownValue(
    "example_resource.test",
    tfjsonpath.New("id"),
    knownvalue.NotNull(),
),
```

### Pattern: List Size

**Legacy**:
```go
resource.TestCheckResourceAttr("example_resource.test", "items.#", "3"),
```

**Modern**:
```go
statecheck.ExpectKnownValue(
    "example_resource.test",
    tfjsonpath.New("items"),
    knownvalue.ListSizeExact(3),
),
```

---

## Idempotency Verification

**Purpose**: Verify that applying the same configuration twice produces no changes.

**Pattern**: Add after Create step and after each Update step.

```go
// After Create
{
    Config: testAccResourceConfig(name, "value"),
    ConfigStateChecks: []statecheck.StateCheck{
        statecheck.ExpectKnownValue(
            "example_resource.test",
            tfjsonpath.New("name"),
            knownvalue.StringExact(name),
        ),
    },
},
// Idempotency check
{
    Config: testAccResourceConfig(name, "value"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectEmptyPlan(),
        },
    },
},
```

**After Update**:
```go
// Update step
{
    Config: testAccResourceConfig(name, "updated-value"),
    ConfigStateChecks: []statecheck.StateCheck{
        statecheck.ExpectKnownValue(
            "example_resource.test",
            tfjsonpath.New("field"),
            knownvalue.StringExact("updated-value"),
        ),
    },
},
// Idempotency check after update
{
    Config: testAccResourceConfig(name, "updated-value"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectEmptyPlan(),
        },
    },
},
```

---

## Import Test Step

**Purpose**: Verify that resource import produces identical state to resource creation.

**Pattern**: Add after Create step, tracks ID consistency.

```go
// Initialize ID tracker
compareID := statecheck.CompareValue(compare.ValuesSame())

Steps: []resource.TestStep{
    // Create step
    {
        Config: testAccResourceConfig(name),
        ConfigStateChecks: []statecheck.StateCheck{
            statecheck.ExpectKnownValue(
                "example_resource.test",
                tfjsonpath.New("name"),
                knownvalue.StringExact(name),
            ),
            // Capture ID after create
            compareID.AddStateValue(
                "example_resource.test",
                tfjsonpath.New("id"),
            ),
        },
    },
    // Import step
    {
        ResourceName:      "example_resource.test",
        ImportState:       true,
        ImportStateVerify: true,
        ConfigStateChecks: []statecheck.StateCheck{
            // Verify ID unchanged after import
            compareID.AddStateValue(
                "example_resource.test",
                tfjsonpath.New("id"),
            ),
        },
    },
}
```

---

## Drift Detection Test

**Purpose**: Verify that Terraform detects external changes and can restore desired state.

**Pattern**: Three-step process: Create → Modify Externally → Verify Drift → Restore

### Full Template

```go
func TestAccResourceName_DriftDetection(t *testing.T) {
    resourceName := generateUniqueTestName("drift-test")

    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckResourceDestroy,
        Steps: []resource.TestStep{
            // Step 1: Create resource with initial value
            {
                Config: testAccResourceConfigWithField(resourceName, "initial-value"),
                ConfigStateChecks: []statecheck.StateCheck{
                    statecheck.ExpectKnownValue(
                        "example_resource.test",
                        tfjsonpath.New("field"),
                        knownvalue.StringExact("initial-value"),
                    ),
                },
            },
            // Step 2: Modify resource externally via provider API
            {
                PreConfig: func() {
                    client := createTestAPIClient(t)
                    ctx := context.Background()

                    // Get resource UUID by name
                    uuid := getResourceUUIDByName(t, "service", "getMethod", resourceName)

                    // Fetch full resource data
                    body, err := client.CallJSONRPC(ctx, "service", "getMethod", uuid)
                    if err != nil {
                        t.Fatalf("Failed to get resource: %v", err)
                    }

                    var resourceData map[string]interface{}
                    if err := json.Unmarshal(body, &resourceData); err != nil {
                        t.Fatalf("Failed to unmarshal resource data: %v", err)
                    }

                    // Modify field externally (NOTE: snake_case → camelCase!)
                    resourceData["camelCaseField"] = "modified-value"

                    // Wrap in provider API entity structure
                    entity := map[string]interface{}{
                        "baseType":      "ResourceType",
                        "childType":     "",
                        "modified":      true,
                        "to_be_removed": false,
                        "revision":      "",
                        "uuid":          uuid,
                    }

                    // Copy resource data into entity
                    for k, v := range resourceData {
                        if k != "uuid" {
                            entity[k] = v
                        }
                    }

                    // Update via provider API
                    _, err = client.CallJSONRPC(ctx, "service", "updateMethod", entity, false)
                    if err != nil {
                        t.Fatalf("Failed to update resource: %v", err)
                    }

                    // Wait for eventual consistency
                    time.Sleep(2 * time.Second)

                    t.Logf("[DEBUG] Modified field externally to: %v", entity["camelCaseField"])
                },
                Config: testAccResourceConfigWithField(resourceName, "initial-value"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectNonEmptyPlan(),
                    },
                },
            },
            // Step 3: Verify Terraform restores desired state
            {
                Config: testAccResourceConfigWithField(resourceName, "initial-value"),
                ConfigStateChecks: []statecheck.StateCheck{
                    statecheck.ExpectKnownValue(
                        "example_resource.test",
                        tfjsonpath.New("field"),
                        knownvalue.StringExact("initial-value"),
                    ),
                },
            },
        },
    })
}

// Helper function for config with field
func testAccResourceConfigWithField(name, fieldValue string) string {
    return fmt.Sprintf(`
provider "example" {
  endpoint             = %[1]q
  username             = %[2]q
  password             = %[3]q
  insecure_skip_verify = true
}

resource "example_resource" "test" {
  name  = %[4]q
  field = %[5]q
}
`,
        os.Getenv("PROVIDER_ENDPOINT"),
        os.Getenv("PROVIDER_USERNAME"),
        os.Getenv("PROVIDER_PASSWORD"),
        name,
        fieldValue,
    )
}
```

**Key Points**:
- Use `createTestAPIClient(t)` helper
- Use `getResourceUUIDByName(t, service, method, name)` helper
- Map Terraform snake_case → Provider camelCase (e.g., `kernel_parameters` → `kernelParameters`)
- Include full Provider entity structure (baseType, childType, modified, etc.)
- Wait 2 seconds after Provider update for consistency
- Verify `ExpectNonEmptyPlan()` detects drift
- Verify Terraform restores desired state

---

## ID Consistency Tracking

**Purpose**: Verify ID remains stable across Create, Import, and Update operations.

```go
func TestAccResourceName_IDConsistency(t *testing.T) {
    resourceName := generateUniqueTestName("id-test")

    // Initialize ID consistency tracker
    compareID := statecheck.CompareValue(compare.ValuesSame())

    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckResourceDestroy,
        Steps: []resource.TestStep{
            // Create
            {
                Config: testAccResourceConfig(resourceName),
                ConfigStateChecks: []statecheck.StateCheck{
                    compareID.AddStateValue(
                        "example_resource.test",
                        tfjsonpath.New("id"),
                    ),
                },
            },
            // Import
            {
                ResourceName:      "example_resource.test",
                ImportState:       true,
                ImportStateVerify: true,
                ConfigStateChecks: []statecheck.StateCheck{
                    compareID.AddStateValue(
                        "example_resource.test",
                        tfjsonpath.New("id"),
                    ),
                },
            },
            // Update
            {
                Config: testAccResourceConfigUpdated(resourceName),
                ConfigStateChecks: []statecheck.StateCheck{
                    compareID.AddStateValue(
                        "example_resource.test",
                        tfjsonpath.New("id"),
                    ),
                },
            },
        },
    })
}
```

---

## knownvalue Type Matchers

Complete reference for Provider attribute types:

| Provider Attribute | Terraform Type | knownvalue Matcher | Example |
|---------------|----------------|-------------------|---------|
| name, path, notes | String | `knownvalue.StringExact()` | `knownvalue.StringExact("test-name")` |
| enabled, dhcp_enabled | Bool | `knownvalue.Bool()` | `knownvalue.Bool(true)` |
| port, mtu, count | Int64 | `knownvalue.Int64Exact()` | `knownvalue.Int64Exact(1500)` |
| uuid, id | String (computed) | `knownvalue.NotNull()` | `knownvalue.NotNull()` |
| nodes, networks | List | `knownvalue.ListSizeExact()` | `knownvalue.ListSizeExact(3)` |

**Common Patterns**:

```go
// String
knownvalue.StringExact("expected-value")

// Boolean
knownvalue.Bool(true)
knownvalue.Bool(false)

// Integer
knownvalue.Int64Exact(8080)
knownvalue.Int64Exact(1500)

// Computed (must exist but value unknown)
knownvalue.NotNull()

// List size
knownvalue.ListSizeExact(3)
knownvalue.ListSizeExact(0)  // empty list

// String pattern match (use for dynamic values)
knownvalue.StringRegexp(regexp.MustCompile(`^test-\d+`))
```

---

## Complete Test Example

Putting it all together - a fully modernized test with all patterns:

```go
func TestAccCMResourceExample_Complete(t *testing.T) {
    resourceName := generateUniqueTestName("complete-test")

    // ID consistency tracker
    compareID := statecheck.CompareValue(compare.ValuesSame())

    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        CheckDestroy:             testAccCheckCMResourceDestroy,
        Steps: []resource.TestStep{
            // Create with state checks + ID tracking
            {
                Config: testAccCMResourceConfig(resourceName, "initial"),
                ConfigStateChecks: []statecheck.StateCheck{
                    statecheck.ExpectKnownValue(
                        "example_cmresource.test",
                        tfjsonpath.New("name"),
                        knownvalue.StringExact(resourceName),
                    ),
                    statecheck.ExpectKnownValue(
                        "example_cmresource.test",
                        tfjsonpath.New("field"),
                        knownvalue.StringExact("initial"),
                    ),
                    statecheck.ExpectKnownValue(
                        "example_cmresource.test",
                        tfjsonpath.New("enabled"),
                        knownvalue.Bool(true),
                    ),
                    statecheck.ExpectKnownValue(
                        "example_cmresource.test",
                        tfjsonpath.New("uuid"),
                        knownvalue.NotNull(),
                    ),
                    compareID.AddStateValue(
                        "example_cmresource.test",
                        tfjsonpath.New("id"),
                    ),
                },
            },
            // Idempotency after Create
            {
                Config: testAccCMResourceConfig(resourceName, "initial"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectEmptyPlan(),
                    },
                },
            },
            // Import with ID tracking
            {
                ResourceName:      "example_cmresource.test",
                ImportState:       true,
                ImportStateVerify: true,
                ConfigStateChecks: []statecheck.StateCheck{
                    compareID.AddStateValue(
                        "example_cmresource.test",
                        tfjsonpath.New("id"),
                    ),
                },
            },
            // Update with state checks + ID tracking
            {
                Config: testAccCMResourceConfig(resourceName, "updated"),
                ConfigStateChecks: []statecheck.StateCheck{
                    statecheck.ExpectKnownValue(
                        "example_cmresource.test",
                        tfjsonpath.New("field"),
                        knownvalue.StringExact("updated"),
                    ),
                    compareID.AddStateValue(
                        "example_cmresource.test",
                        tfjsonpath.New("id"),
                    ),
                },
            },
            // Idempotency after Update
            {
                Config: testAccCMResourceConfig(resourceName, "updated"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectEmptyPlan(),
                    },
                },
            },
        },
    })
}
```

This example demonstrates:
- ✅ Modern state checks with type-safe matchers
- ✅ Idempotency verification after Create and Update
- ✅ Import test with ID consistency tracking
- ✅ All computed fields validated with NotNull()
- ✅ No legacy Check blocks
