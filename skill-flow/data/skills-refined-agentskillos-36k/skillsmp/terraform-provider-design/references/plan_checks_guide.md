# Plan Checks Guide for Terraform Provider Testing

## Overview

**Plan checks** are test assertions that inspect Terraform plan files at specific phases during acceptance testing. They verify that Terraform generates expected plans before and after apply operations.

According to HashiCorp: "A plan check is a test assertion that inspects the plan file at a specific phase during the current testing mode."

## Why Plan Checks Matter

Plan checks validate:
- **Idempotency**: Resources don't change on subsequent applies
- **Change Detection**: Updates trigger appropriate plans
- **Drift Detection**: External changes are detected
- **Plan Accuracy**: Plans match expected operations

## Plan Check Types

### 1. General Plan Checks

Built-in checks from `github.com/hashicorp/terraform-plugin-testing/plancheck`:

#### ExpectEmptyPlan

**Purpose**: Verifies plan contains NO operations for apply.

**Use Cases**:
- Validating idempotency after resource creation
- Confirming no changes when configuration unchanged
- Verifying computed fields don't cause spurious diffs

**Example**:

```go
import "github.com/hashicorp/terraform-plugin-testing/plancheck"

{
    Config: testAccResourceConfig("test"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectEmptyPlan(),
        },
    },
}
```

**When It Runs**: Before apply phase in Lifecycle (config) mode.

**What It Verifies**:
- No resources will be created
- No resources will be updated
- No resources will be destroyed
- No output changes
- Plan is completely empty

#### ExpectNonEmptyPlan

**Purpose**: Confirms plan includes AT LEAST ONE operation for apply.

**Use Cases**:
- Verifying configuration changes trigger updates
- Validating drift detection
- Confirming creates/updates/destroys occur

**Example**:

```go
{
    Config: testAccResourceConfig("updated"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectNonEmptyPlan(),
        },
    },
}
```

**When It Runs**: Before apply phase in Lifecycle (config) mode.

**What It Verifies**:
- At least one resource operation exists
- Plan is not empty
- Changes will be applied

### 2. Resource Plan Checks

Checks specific to managed resources and data sources.

#### ExpectResourceAction

**Purpose**: Verifies specific action for a resource.

**Available Actions**:
- `plancheck.ResourceActionCreate`
- `plancheck.ResourceActionUpdate`
- `plancheck.ResourceActionDestroy`
- `plancheck.ResourceActionReplace`
- `plancheck.ResourceActionRead`
- `plancheck.ResourceActionNoop`

**Example**:

```go
import "github.com/hashicorp/terraform-plugin-testing/plancheck"

{
    Config: testAccResourceConfig("updated"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectResourceAction("example_resource.test",
                plancheck.ResourceActionUpdate),
        },
    },
}
```

**Use Cases**:
- Verify resource will be created
- Confirm update (not replace) on change
- Validate destroy behavior
- Check force-replacement scenarios

#### ExpectKnownValue

**Purpose**: Validates planned value for specific attribute.

**Example**:

```go
import (
    "github.com/hashicorp/terraform-plugin-testing/plancheck"
    "github.com/hashicorp/terraform-plugin-testing/tfjsonpath"
    "github.com/hashicorp/terraform-plugin-testing/knownvalue"
)

{
    Config: testAccResourceConfig("test"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectKnownValue(
                "example_resource.test",
                tfjsonpath.New("name"),
                knownvalue.StringExact("test"),
            ),
        },
    },
}
```

#### ExpectUnknownValue

**Purpose**: Verifies attribute value is unknown (computed) in plan.

**Example**:

```go
{
    Config: testAccResourceConfig("test"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectUnknownValue(
                "example_resource.test",
                tfjsonpath.New("id"),
            ),
        },
    },
}
```

**Use Cases**:
- Verify computed attributes remain unknown before apply
- Validate API-generated values aren't prematurely set
- Check dependent resource references

### 3. Output Plan Checks

Checks for Terraform outputs.

#### ExpectKnownOutputValue

**Example**:

```go
{
    Config: testAccConfig(),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectKnownOutputValue(
                "resource_id",
                knownvalue.NotNull(),
            ),
        },
    },
}
```

### 4. Custom Plan Checks

Implement custom plan check logic:

```go
type customPlanCheck struct{}

func (c customPlanCheck) CheckPlan(ctx context.Context, req plancheck.CheckPlanRequest, resp *plancheck.CheckPlanResponse) {
    // Access plan via req.Plan
    for _, rc := range req.Plan.ResourceChanges {
        if rc.Change.Actions.Create() {
            // Custom validation logic
            if rc.Type == "example_resource" {
                // Verify custom conditions
            }
        }
    }
}

// Use in test
{
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            customPlanCheck{},
        },
    },
}
```

## When Plan Checks Execute

### Execution Phases

Plan checks run at different phases:

**ConfigPlanChecks**:
- `PreApply` - Before terraform apply
- `PostApply` - After terraform apply (before refresh)

**RefreshPlanChecks**:
- `PreRefresh` - Before terraform refresh
- `PostRefresh` - After terraform refresh

### Test Mode Support

| Mode | ConfigPlanChecks | RefreshPlanChecks |
|------|------------------|-------------------|
| Lifecycle (config) | ✅ Supported | ✅ Supported |
| Refresh | ✅ Supported | ✅ Supported |
| Import | ❌ Not supported | ❌ Not supported |

## Configuration Structure

### Basic Structure

```go
{
    Config: testAccResourceConfig("test"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            // Checks run before apply
        },
        PostApply: []plancheck.PlanCheck{
            // Checks run after apply, before refresh
        },
    },
}
```

### With Refresh Checks

```go
{
    RefreshState: true,
    RefreshPlanChecks: resource.RefreshPlanChecks{
        PreRefresh: []plancheck.PlanCheck{
            // Checks run before refresh
        },
        PostRefresh: []plancheck.PlanCheck{
            // Checks run after refresh
        },
    },
}
```

## Common Testing Patterns

### Pattern 1: Idempotency Verification

Verify resource doesn't change on second apply:

```go
func TestAccResource_Idempotent(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            // Step 1: Create resource
            {
                Config: testAccResourceConfig("test"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "name", "test"),
                ),
            },
            // Step 2: Verify no changes on reapply
            {
                Config: testAccResourceConfig("test"),
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

### Pattern 2: Update Detection

Verify configuration changes trigger updates:

```go
func TestAccResource_Update(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            // Create with initial value
            {
                Config: testAccResourceConfig("initial"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "name", "initial"),
                ),
            },
            // Update and verify plan shows update
            {
                Config: testAccResourceConfig("updated"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectNonEmptyPlan(),
                        plancheck.ExpectResourceAction("example_resource.test",
                            plancheck.ResourceActionUpdate),
                    },
                },
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "name", "updated"),
                ),
            },
        },
    })
}
```

### Pattern 3: Drift Detection

Verify provider detects external changes:

```go
func TestAccResource_Drift(t *testing.T) {
    name := generateUniqueTestName("test-drift")

    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            // Create resource
            {
                Config: testAccResourceConfig(name, "initial"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "attr", "initial"),
                ),
            },
            // Modify externally and verify drift detected
            {
                PreConfig: func() {
                    // Modify resource via API
                    modifyResourceExternally(t, name)
                },
                Config: testAccResourceConfig(name, "initial"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectNonEmptyPlan(),  // Drift detected
                    },
                },
            },
            // Verify Terraform restores desired state
            {
                Config: testAccResourceConfig(name, "initial"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test", "attr", "initial"),
                ),
            },
        },
    })
}
```

### Pattern 4: Force Replacement

Verify attribute changes force replacement:

```go
func TestAccResource_ForceReplacement(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {
                Config: testAccResourceConfig("initial-immutable-value"),
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttr("example_resource.test",
                        "immutable_field", "initial-immutable-value"),
                ),
            },
            {
                Config: testAccResourceConfig("updated-immutable-value"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        plancheck.ExpectResourceAction("example_resource.test",
                            plancheck.ResourceActionReplace),
                    },
                },
            },
        },
    })
}
```

### Pattern 5: Computed Value Verification

Verify computed fields in plan:

```go
func TestAccResource_ComputedFields(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {
                Config: testAccResourceConfig("test"),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        // Verify ID is unknown before apply
                        plancheck.ExpectUnknownValue(
                            "example_resource.test",
                            tfjsonpath.New("id"),
                        ),
                        // Verify name is known in plan
                        plancheck.ExpectKnownValue(
                            "example_resource.test",
                            tfjsonpath.New("name"),
                            knownvalue.StringExact("test"),
                        ),
                    },
                },
                Check: resource.ComposeAggregateTestCheckFunc(
                    resource.TestCheckResourceAttrSet("example_resource.test", "id"),
                ),
            },
        },
    })
}
```

### Pattern 6: Multiple Resources

Check plans for multiple resources:

```go
func TestAccResource_MultiResource(t *testing.T) {
    resource.Test(t, resource.TestCase{
        PreCheck:                 func() { testAccPreCheck(t) },
        ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
        Steps: []resource.TestStep{
            {
                Config: testAccMultiResourceConfig(),
                ConfigPlanChecks: resource.ConfigPlanChecks{
                    PreApply: []plancheck.PlanCheck{
                        // Verify both resources will be created
                        plancheck.ExpectResourceAction("example_resource.one",
                            plancheck.ResourceActionCreate),
                        plancheck.ExpectResourceAction("example_resource.two",
                            plancheck.ResourceActionCreate),
                    },
                },
            },
        },
    })
}
```

## Advanced Usage

### Combining Multiple Checks

Multiple checks run with aggregated error reporting:

```go
{
    Config: testAccResourceConfig("test"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectNonEmptyPlan(),
            plancheck.ExpectResourceAction("example_resource.test",
                plancheck.ResourceActionUpdate),
            plancheck.ExpectKnownValue("example_resource.test",
                tfjsonpath.New("name"),
                knownvalue.StringExact("test")),
            plancheck.ExpectUnknownValue("example_resource.test",
                tfjsonpath.New("last_updated")),
        },
    },
}
```

### Pre and Post Apply Checks

```go
{
    Config: testAccResourceConfig("test"),
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectUnknownValue("example_resource.test",
                tfjsonpath.New("id")),
        },
        PostApply: []plancheck.PlanCheck{
            // After apply, verify no more changes needed
            plancheck.ExpectEmptyPlan(),
        },
    },
}
```

### Refresh Plan Checks

```go
{
    RefreshState: true,
    RefreshPlanChecks: resource.RefreshPlanChecks{
        PostRefresh: []plancheck.PlanCheck{
            // After refresh, no changes should be detected
            plancheck.ExpectEmptyPlan(),
        },
    },
}
```

## Best Practices

### 1. Always Test Idempotency

Every resource should verify no changes on second apply:

```go
✅ Good:
Steps: []resource.TestStep{
    {Config: config, Check: check},
    {Config: config, ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{plancheck.ExpectEmptyPlan()},
    }},
}

❌ Bad:
Steps: []resource.TestStep{
    {Config: config, Check: check},
    // Missing idempotency check
}
```

### 2. Verify Update Actions

Confirm updates don't force replacement:

```go
✅ Good:
ConfigPlanChecks: resource.ConfigPlanChecks{
    PreApply: []plancheck.PlanCheck{
        plancheck.ExpectResourceAction("example_resource.test",
            plancheck.ResourceActionUpdate),  // Verify update, not replace
    },
}
```

### 3. Test Drift Detection

Verify external changes are detected:

```go
✅ Good:
{
    PreConfig: func() { modifyExternally(t) },
    Config: originalConfig,
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectNonEmptyPlan(),  // Drift detected
        },
    },
}
```

### 4. Use Specific Checks

Prefer specific checks over general ones:

```go
✅ Good (specific):
plancheck.ExpectResourceAction("example_resource.test",
    plancheck.ResourceActionUpdate)

⚠️ Less specific:
plancheck.ExpectNonEmptyPlan()  // Could be any resource
```

### 5. Combine with State Checks

Plan checks verify plans, state checks verify results:

```go
{
    Config: config,
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectUnknownValue("example_resource.test",
                tfjsonpath.New("id")),
        },
    },
    ConfigStateChecks: []statecheck.StateCheck{
        statecheck.ExpectKnownValue("example_resource.test",
            tfjsonpath.New("id"),
            knownvalue.NotNull()),
    },
}
```

## Common Pitfalls

### ❌ Pitfall 1: Missing Idempotency Tests

```go
// Bad: Only tests creation
Steps: []resource.TestStep{
    {Config: config, Check: check},
}

// Good: Tests creation and idempotency
Steps: []resource.TestStep{
    {Config: config, Check: check},
    {Config: config, ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{plancheck.ExpectEmptyPlan()},
    }},
}
```

### ❌ Pitfall 2: Wrong Phase

```go
// Bad: PostApply expects empty plan (refresh might show changes)
ConfigPlanChecks: resource.ConfigPlanChecks{
    PostApply: []plancheck.PlanCheck{
        plancheck.ExpectEmptyPlan(),  // May fail after refresh
    },
}

// Good: PreApply for idempotency
ConfigPlanChecks: resource.ConfigPlanChecks{
    PreApply: []plancheck.PlanCheck{
        plancheck.ExpectEmptyPlan(),
    },
}
```

### ❌ Pitfall 3: Not Testing Updates

```go
// Bad: Creates but never updates
Steps: []resource.TestStep{
    {Config: config("initial"), Check: check},
}

// Good: Tests both create and update
Steps: []resource.TestStep{
    {Config: config("initial"), Check: check},
    {
        Config: config("updated"),
        ConfigPlanChecks: resource.ConfigPlanChecks{
            PreApply: []plancheck.PlanCheck{
                plancheck.ExpectNonEmptyPlan(),
            },
        },
        Check: check,
    },
}
```

### ❌ Pitfall 4: Not Verifying Drift

```go
// Bad: No drift detection test
// Resources might not detect external changes

// Good: Test drift detection
{
    PreConfig: func() { modifyExternally(t) },
    Config: config,
    ConfigPlanChecks: resource.ConfigPlanChecks{
        PreApply: []plancheck.PlanCheck{
            plancheck.ExpectNonEmptyPlan(),
        },
    },
}
```

## Error Messages

Plan check failures provide clear error messages:

```
Error: plan check failed: expected non-empty plan, but got empty plan

Error: plan check failed: expected resource action "update" for "example_resource.test", but got "replace"

Error: plan check failed: expected known value at path "name", but value was unknown
```

## Summary

### Essential Plan Checks

1. ✅ **ExpectEmptyPlan** - Verify idempotency
2. ✅ **ExpectNonEmptyPlan** - Verify changes detected
3. ✅ **ExpectResourceAction** - Verify specific actions
4. ✅ **ExpectKnownValue** - Verify planned values
5. ✅ **ExpectUnknownValue** - Verify computed values

### When to Use Each Check

| Check | Use When |
|-------|----------|
| ExpectEmptyPlan | Testing idempotency, no changes expected |
| ExpectNonEmptyPlan | Verifying updates, drift detection |
| ExpectResourceAction | Confirming specific create/update/replace/destroy |
| ExpectKnownValue | Validating planned attribute values |
| ExpectUnknownValue | Verifying computed attributes |

### Every Test Should Include

1. ✅ Idempotency check with `ExpectEmptyPlan`
2. ✅ Update verification with `ExpectNonEmptyPlan`
3. ✅ Drift detection with external modification
4. ✅ Specific action verification with `ExpectResourceAction`

### Key Takeaways

- Plan checks validate Terraform plans, not state
- Use `PreApply` for most checks
- Combine multiple checks for comprehensive validation
- Always test idempotency
- Verify drift detection
- Check both create and update operations
