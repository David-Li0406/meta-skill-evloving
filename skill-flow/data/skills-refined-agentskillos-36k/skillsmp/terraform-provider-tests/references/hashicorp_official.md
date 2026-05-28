# HashiCorp Official Testing Documentation Reference

Consolidated reference from official Terraform Plugin Testing documentation.

**Source**: https://developer.hashicorp.com/terraform/plugin/testing

## Table of Contents

1. [TestCase Structure](#testcase-structure)
2. [TestStep Configuration](#teststep-configuration)
3. [State Checks](#state-checks)
4. [Plan Checks](#plan-checks)
5. [Value Comparers](#value-comparers)
6. [Import Mode](#import-mode)
7. [Testing Patterns](#testing-patterns)

---

## TestCase Structure

Foundation for all acceptance tests. Use `resource.Test()` to execute.

### Required Fields

**Providers**: Map of provider instances under test. Only included providers are loaded.

**Steps**: Array of TestStep objects defining sequential test operations.

### Common Optional Fields

**PreCheck**: Function called before test steps execute. Validates environment variables and prerequisites.

```go
PreCheck: func() { testAccPreCheck(t) },
```

**CheckDestroy**: Executes after all steps and infrastructure destruction. Verifies resources no longer exist.

```go
CheckDestroy: testAccCheckResourceDestroy,
```

**ProtoV6ProviderFactories**: Provider factory for protocol v6 providers (terraform-plugin-framework).

```go
ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
```

**TerraformVersionChecks**: Version requirements before execution.

```go
TerraformVersionChecks: []tfversion.TerraformVersionCheck{
    tfversion.SkipBelow(tfversion.Version1_3_0),
},
```

**IsUnitTest**: Allows tests to run without `TF_ACC` environment variable.

---

## TestStep Configuration

Represents applying a Terraform configuration to state.

### Test Modes

1. **Lifecycle (config)** - Most common; uses `Config`, `ConfigFile`, or `ConfigDirectory`
2. **Import** - Exercises import logic with `ImportState: true`
3. **Refresh** - Runs `terraform refresh` with `RefreshState: true`

### Configuration Fields

**Config**: Inline Terraform configuration string.

```go
Config: testAccResourceConfig(name),
```

**ConfigFile**: Path to Terraform configuration file.

**ConfigDirectory**: Path to directory containing Terraform files.

### Modern Validation Fields

**ConfigStateChecks**: State checks after `terraform apply` (RECOMMENDED).

```go
ConfigStateChecks: []statecheck.StateCheck{
    statecheck.ExpectKnownValue(
        "example_resource.test",
        tfjsonpath.New("name"),
        knownvalue.StringExact("expected"),
    ),
},
```

**ConfigPlanChecks**: Plan checks before/after apply.

```go
ConfigPlanChecks: resource.ConfigPlanChecks{
    PreApply: []plancheck.PlanCheck{
        plancheck.ExpectEmptyPlan(),
    },
},
```

### Legacy Validation (Avoid)

**Check**: Legacy validation function. Use `ConfigStateChecks` instead.

```go
// ❌ Legacy - avoid
Check: resource.ComposeAggregateTestCheckFunc(
    resource.TestCheckResourceAttr("resource.test", "name", "value"),
),

// ✅ Modern - prefer
ConfigStateChecks: []statecheck.StateCheck{
    statecheck.ExpectKnownValue(
        "resource.test",
        tfjsonpath.New("name"),
        knownvalue.StringExact("value"),
    ),
},
```

### Import Configuration

**ImportState**: Set to `true` to activate import mode.

**ImportStateVerify**: Automatically compare imported state with created state.

**ResourceName**: The resource identifier for import.

```go
{
    ResourceName:      "example_resource.test",
    ImportState:       true,
    ImportStateVerify: true,
},
```

### PreConfig Function

Execute logic before configuration application (useful for drift detection).

```go
PreConfig: func() {
    // Modify resource externally
},
```

---

## State Checks

Validate resource/data source state after `terraform apply`.

**Package**: `github.com/hashicorp/terraform-plugin-testing/statecheck`

### ExpectKnownValue

Asserts attribute has specified type and value.

```go
statecheck.ExpectKnownValue(
    "example_resource.test",           // Resource address
    tfjsonpath.New("attribute"),   // Attribute path
    knownvalue.StringExact("val"), // Expected value
)
```

**Common knownvalue matchers**:
- `StringExact(string)` - Exact string match
- `Bool(bool)` - Boolean value
- `Int64Exact(int64)` - Exact int64 match
- `NotNull()` - Value exists (for computed fields)
- `ListSizeExact(int)` - List has exact size
- `StringRegexp(*regexp.Regexp)` - String matches pattern

### CompareValue

Compare attribute values across test steps.

```go
// Initialize tracker
compareID := statecheck.CompareValue(compare.ValuesSame())

// Add value in each step
ConfigStateChecks: []statecheck.StateCheck{
    compareID.AddStateValue(
        "example_resource.test",
        tfjsonpath.New("id"),
    ),
}
```

**Value comparers**:
- `compare.ValuesSame()` - Values must be identical
- `compare.ValuesDiffer()` - Values must differ

### CompareValueCollection

Compare collection items with another attribute.

```go
statecheck.CompareValueCollection(
    "example_resource.test",
    tfjsonpath.New("items"),
    tfjsonpath.New("count"),
    compare.ValuesSame(),
)
```

### CompareValuePairs

Compare paired attribute values.

```go
statecheck.CompareValuePairs(
    "example_resource.test",
    tfjsonpath.New("input"),
    tfjsonpath.New("output"),
    compare.ValuesSame(),
)
```

### ExpectSensitiveValue

Asserts attribute is marked sensitive (Terraform 1.4.6+).

```go
statecheck.ExpectSensitiveValue(
    "example_resource.test",
    tfjsonpath.New("password"),
)
```

---

## Plan Checks

Validate Terraform plans before/after operations.

**Package**: `github.com/hashicorp/terraform-plugin-testing/plancheck`

### ConfigPlanChecks Phases

**PreApply**: Before `terraform apply` executes.

**PostApplyPreRefresh**: After apply, before refresh.

**PostApplyPostRefresh**: After apply and refresh.

```go
ConfigPlanChecks: resource.ConfigPlanChecks{
    PreApply: []plancheck.PlanCheck{
        plancheck.ExpectEmptyPlan(),
    },
},
```

### ExpectEmptyPlan

Asserts plan has no operations (idempotency check).

```go
plancheck.ExpectEmptyPlan()
```

### ExpectNonEmptyPlan

Asserts plan contains at least one operation (drift detection).

```go
plancheck.ExpectNonEmptyPlan()
```

### ExpectKnownValue (Plan)

Asserts planned attribute value.

```go
plancheck.ExpectKnownValue(
    "example_resource.test",
    tfjsonpath.New("name"),
    knownvalue.StringExact("expected"),
)
```

### ExpectResourceAction

Asserts resource has specific planned operation.

```go
plancheck.ExpectResourceAction(
    "example_resource.test",
    plancheck.ResourceActionUpdate,
)
```

**Actions**:
- `ResourceActionCreate`
- `ResourceActionUpdate`
- `ResourceActionDestroy`
- `ResourceActionDestroyBeforeCreate`
- `ResourceActionCreateBeforeDestroy`
- `ResourceActionNoop`

### ExpectUnknownValue

Asserts attribute value is unknown (computed).

```go
plancheck.ExpectUnknownValue(
    "example_resource.test",
    tfjsonpath.New("uuid"),
)
```

### ExpectSensitiveValue (Plan)

Asserts planned attribute is sensitive.

```go
plancheck.ExpectSensitiveValue(
    "example_resource.test",
    tfjsonpath.New("password"),
)
```

---

## Value Comparers

Enable assertions on attribute values across test steps.

**Package**: `github.com/hashicorp/terraform-plugin-testing/compare`

### ValuesSame

Verifies each value matches the preceding value.

```go
compareID := statecheck.CompareValue(compare.ValuesSame())
```

**Use case**: Verify computed attributes remain consistent (e.g., ID stability).

### ValuesDiffer

Verifies each value differs from the preceding value.

```go
compareRandom := statecheck.CompareValue(compare.ValuesDiffer())
```

**Use case**: Verify random values change across applies.

### Usage Pattern

1. Create comparer before TestCase
2. Add state values in ConfigStateChecks
3. Framework compares values automatically

```go
compareID := statecheck.CompareValue(compare.ValuesSame())

Steps: []resource.TestStep{
    {
        ConfigStateChecks: []statecheck.StateCheck{
            compareID.AddStateValue("resource.test", tfjsonpath.New("id")),
        },
    },
    {
        ConfigStateChecks: []statecheck.StateCheck{
            compareID.AddStateValue("resource.test", tfjsonpath.New("id")),
        },
    },
}
```

---

## Import Mode

Validates Terraform's import workflow.

### Purpose

Verify that importing existing infrastructure produces identical state to creating it via Terraform.

### Basic Pattern

```go
{
    ResourceName:      "example_resource.test",
    ImportState:       true,
    ImportStateVerify: true,
}
```

### Advanced Import Modes

**ImportBlockWithID**: Uses import blocks with resource identifiers.

**ImportBlockWithResourceIdentity**: Uses managed resource identities.

### Best Practice

Run import mode after a lifecycle step:

```go
Steps: []resource.TestStep{
    // Create resource
    {
        Config: testAccResourceConfig(name),
    },
    // Import and verify
    {
        ResourceName:      "example_resource.test",
        ImportState:       true,
        ImportStateVerify: true,
    },
}
```

The framework uses the previous configuration and state as validation baselines.

---

## Testing Patterns

Official recommended patterns for comprehensive testing.

### 1. Basic Attribute Verification

Verify resource creation with expected attributes.

```go
{
    Config: testAccResourceConfig(),
    ConfigStateChecks: []statecheck.StateCheck{
        statecheck.ExpectKnownValue(
            "example_resource.test",
            tfjsonpath.New("name"),
            knownvalue.StringExact("expected"),
        ),
    },
}
```

**Validates**:
- Resource creates without error
- Attributes saved to state correctly
- Subsequent plans produce no diff (framework automatic)

### 2. Update Configuration

Apply modified configuration in second step.

```go
Steps: []resource.TestStep{
    {
        Config: testAccResourceConfig("initial"),
        ConfigStateChecks: []statecheck.StateCheck{
            statecheck.ExpectKnownValue(
                "example_resource.test",
                tfjsonpath.New("field"),
                knownvalue.StringExact("initial"),
            ),
        },
    },
    {
        Config: testAccResourceConfig("updated"),
        ConfigStateChecks: []statecheck.StateCheck{
            statecheck.ExpectKnownValue(
                "example_resource.test",
                tfjsonpath.New("field"),
                knownvalue.StringExact("updated"),
            ),
        },
    },
}
```

**Can combine basic and update into single test when fundamentals are covered.**

### 3. Import Mode Testing

Verify import produces equivalent state to creation.

```go
Steps: []resource.TestStep{
    {
        Config: testAccResourceConfig(),
    },
    {
        ResourceName:      "example_resource.test",
        ImportState:       true,
        ImportStateVerify: true,
    },
}
```

### 4. Error and Non-Empty Plan Scenarios

**Valid config with non-empty plan**:
```go
{
    Config: testAccResourceConfig(),
    ExpectNonEmptyPlan: true,
}
```

**Invalid config that should fail**:
```go
{
    Config: testAccInvalidResourceConfig(),
    ExpectError: regexp.MustCompile("expected error pattern"),
}
```

### 5. Regression Tests

Document regression tests with bug links:

```go
// TestAccResource_RegressionIssue123 tests the fix for
// https://github.com/org/repo/issues/123
func TestAccResource_RegressionIssue123(t *testing.T) {
    // Test implementation
}
```

**Ideally**: Commit failing test first, then fix in separate commit.

## Built-in Framework Behaviors

The testing framework automatically:
- ✅ Runs plan, apply, refresh, and final plan for each step
- ✅ Fails tests if final plans show non-empty diffs (unless allowed)
- ✅ Executes PreCheck before tests
- ✅ Executes CheckDestroy after all steps
- ✅ Exits with errors on unexpected plan diffs

## Best Practices Summary

1. **Use Modern Patterns**:
   - `ConfigStateChecks` over `Check`
   - `ConfigPlanChecks` for plan validation
   - Type-safe `knownvalue` matchers

2. **Compose State Checks**:
   - Separate checks for local state vs remote API
   - Reuse checks across test steps

3. **Configuration Functions**:
   - Separate configuration into dedicated functions
   - Accept parameters for reusability
   - Example: `testAccResourceConfig(name, value string)`

4. **Random Test Data**:
   - Generate unique names per test run
   - Prevent collision in concurrent testing
   - Example: `generateUniqueTestName("prefix")`

5. **Modular Verification**:
   - Split existence checks from value checks
   - Enable reuse and step-specific assertions

6. **Test Organization**:
   - Structure as TestCases with multiple TestSteps
   - Each step validates specific scenarios
   - Framework ensures no unintended diffs

---

## Quick Reference

### Required Imports

```go
import (
    "testing"
    "github.com/hashicorp/terraform-plugin-testing/helper/resource"
    "github.com/hashicorp/terraform-plugin-testing/plancheck"
    "github.com/hashicorp/terraform-plugin-testing/statecheck"
    "github.com/hashicorp/terraform-plugin-testing/knownvalue"
    "github.com/hashicorp/terraform-plugin-testing/tfjsonpath"
    "github.com/hashicorp/terraform-plugin-testing/compare"
)
```

### Common knownvalue Matchers

```go
knownvalue.StringExact("value")
knownvalue.Bool(true)
knownvalue.Int64Exact(42)
knownvalue.NotNull()
knownvalue.ListSizeExact(3)
knownvalue.StringRegexp(regexp.MustCompile(`pattern`))
```

### Common Plan Checks

```go
plancheck.ExpectEmptyPlan()                    // Idempotency
plancheck.ExpectNonEmptyPlan()                 // Drift detected
plancheck.ExpectResourceAction(addr, action)   // Specific operation
```

### Common State Checks

```go
statecheck.ExpectKnownValue(addr, path, matcher)
statecheck.CompareValue(comparer).AddStateValue(addr, path)
statecheck.ExpectSensitiveValue(addr, path)
```

---

## Additional Resources

- **Official Docs**: https://developer.hashicorp.com/terraform/plugin/testing
- **terraform-plugin-testing**: https://pkg.go.dev/github.com/hashicorp/terraform-plugin-testing
- **terraform-plugin-framework**: https://pkg.go.dev/github.com/hashicorp/terraform-plugin-framework
