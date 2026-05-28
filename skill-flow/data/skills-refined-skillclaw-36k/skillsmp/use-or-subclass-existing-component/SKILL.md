---
name: use-or-subclass-existing-component
description: Discover, use, or subclass existing Dagster integration components (dbt, Looker, PowerBI, Fivetran, etc.). Handles configuration-file-based components (dbt, Sling) and API-based components (Fivetran, PowerBI) appropriately. Use only when an existing Dagster component exists within Dagster's integration libraries.
license: MIT
---

# Use or Subclass Existing Dagster Component

## Overview

This skill helps you discover and work with existing Dagster integration components from the 70+ available integrations. It guides you through finding the right component, using it directly, or subclassing it to add custom functionality.

**Key distinction:** This skill differentiates between configuration-file-based components (like dbt and Sling) that read from local files, and API-based components (like Fivetran, PowerBI, Looker) that call external services. Configuration-based components should be used directly without demo_mode, while API-based components benefit from demo_mode implementation.

The documentation for subclassing components can be found here: https://docs.dagster.io/guides/build/components/creating-new-components/subclassing-components

## What This Skill Does

When invoked, this skill will:

1. ✅ Help discover available Dagster integrations using `uv run dg docs integrations --json` or browsing https://docs.dagster.io/integrations/libraries
2. ✅ Determine whether to use the component directly or create a subclass
3. ✅ If subclassing: Create a local component subclass that extends the integration component
4. ✅ Implement demo mode support by overriding the `execute()` method
5. ✅ Add custom templating scope if needed via `get_additional_scope()`
6. ✅ Create and configure component instance YAML with proper type references
7. ✅ Validate that the component loads correctly using `uv run dg check defs`
8. ✅ Verify assets are created using `uv run dg list defs`

## Prerequisites

Before running this skill, ensure:

- `uv` is installed (check with `uv --version`)
- You're in a Dagster project directory with the dg CLI available
- You know which integration you want to use (e.g., dbt, Looker, PowerBI, Fivetran)

### Important: When to Switch Skills

  If you discover the integration package exists but has NO Component class:
  - Run: `uv run python -c "import dagster_<integration>; print([x for x in dir(dagster_<integration>) if 'Component' in x])"`
  - If result is `[]`, the integration doesn't have a Component class
  - **STOP and use the `create-custom-dagster-component` skill instead**

  This skill is ONLY for integrations that have existing Component classes to subclass.

## Skill Workflow

### Step 1: Discover Available Integrations

Help the user find the right integration component:

1. **Run discovery command:**
   ```bash
   uv run dg docs integrations --json
   ```

2. **Alternative:** Browse https://docs.dagster.io/integrations/libraries for visual list

3. **Common integrations include:**
   - `dagster_dbt.DbtProjectComponent` - dbt projects
   - `dagster_fivetran.FivetranComponent` - Fivetran syncs
   - `dagster_sling.SlingReplicationCollectionComponent` - Sling replications
   - `dagster_powerbi.PowerBIWorkspaceComponent` - PowerBI workspaces
   - `dagster_looker.LookerComponent` - Looker instances
   - `dagster_airbyte.AirbyteComponent` - Airbyte connections
   - `dagster_databricks.DatabricksComponent` - Databricks workflows
   - `dagster_snowflake.SnowflakeComponent` - Snowflake resources

### Step 2: Determine Component Type and Use Case

**IMPORTANT:** First determine if this is a configuration-file-based or API-based component:

#### Configuration-File-Based Components
These components read from local configuration files and do NOT require external API credentials:
- `DbtProjectComponent` - Reads from dbt project files (`dbt_project.yml`, SQL/Python models)
- `SlingReplicationCollectionComponent` - Reads from replication YAML files
- Components that primarily process local files

**For configuration-file-based components:**
- ✅ **DO** use the component directly or subclass for custom behavior
- ❌ **DO NOT** implement demo_mode - just load the project files
- The component naturally works with local files without external dependencies

#### API-Based Components
These components call out to external services and require API credentials:
- `FivetranComponent` - Calls Fivetran API
- `PowerBIWorkspaceComponent` - Calls PowerBI API
- `LookerComponent` - Calls Looker API
- `AirbyteComponent` - Calls Airbyte API
- `CensusComponent` - Calls Census API

**For API-based components:**
- ✅ **DO** implement demo_mode to mock external API calls
- ✅ **DO** provide dummy credentials in YAML (ignored when demo_mode is true)
- This allows the component to work locally without external connections

#### Determine Your Use Case

Based on the component type, choose:

1. **Use directly (Configuration-based)** - Load the component with local configuration files
2. **Use directly (API-based)** - Use the component with real API credentials
3. **Subclass for demo mode (API-based only)** - Add demo_mode to mock external API calls
4. **Subclass for other customization** - Add other custom behavior beyond demo mode

If using directly, skip to Step 7 to create the component instance YAML.

### Step 3: Install Integration Package

Install the required Dagster integration package:

```bash
uv add dagster-<integration-name>
```

Examples:
- `uv add dagster-dbt`
- `uv add dagster-sling`
- `uv add dagster-powerbi`

### Step 4: Scaffold Component Instance

Use `dg scaffold defs` to create the component instance directory:

```bash
uv run dg scaffold defs <package>.<ComponentClass> <instance_name>
```

Example:
```bash
uv run dg scaffold defs dagster_sling.SlingReplicationCollectionComponent my_sling_sync
```

This creates a directory structure like:
```
defs/
  my_sling_sync/
    defs.yaml
    # Other config files as needed
```

### Step 5: Create Component Subclass

Create a `component.py` file in the component instance directory.

**IMPORTANT: Only add demo_mode for API-based components!**
- Configuration-file-based components (dbt, Sling) read from local files and don't need demo_mode
- API-based components (Fivetran, PowerBI, Looker) call external APIs and should use demo_mode

When extending integration components, you must understand whether they use **dataclass** or **Pydantic BaseModel** patterns, as this determines how to add custom fields like `demo_mode`.

## Identifying Component Type

First, check the parent component's implementation:

```python
# Check if it's a dataclass
uv run python -c "from <package> import <Component>; import dataclasses; print(dataclasses.is_dataclass(<Component>))"
```

Most Dagster integration components (like `SlingReplicationCollectionComponent`, `DbtProjectComponent`, `FivetranComponent`) use **dataclass** with the `Resolvable` interface.

## Pattern for Dataclass-Based Components (Recommended)

This is the most common pattern for Dagster integration components:

```python
from dataclasses import dataclass
import dagster as dg
from <integration_package> import <BaseComponentClass>

@dataclass
class Custom<ComponentName>(BaseComponentClass):
    """Customized component with demo mode support."""

    # New field - will automatically appear in YAML schema via Resolvable
    demo_mode: bool = False

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        """Build definitions, using demo mode if enabled.

        Note: The parent class fields (like API credentials) are still set from YAML,
        but when demo_mode is True, we bypass the parent's build_defs() method
        and return mocked assets instead, so those credentials are never used.
        """
        if self.demo_mode:
            # Return mock assets for demo mode - parent credentials are ignored
            return self._build_demo_defs(context)
        else:
            # Use real integration with actual credentials from parent fields
            return super().build_defs(context)

    def _build_demo_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        """Build demo mode definitions with mocked assets."""
        @dg.asset(
            key=dg.AssetKey(["mock_asset"]),
            kinds={"integration_name"},  # IMPORTANT: Add the integration kind
        )
        def mock_asset(context: dg.AssetExecutionContext):
            context.log.info("Demo mode: simulating asset execution")
            return {"status": "demo_mode"}

        return dg.Definitions(assets=[mock_asset])
```

**Key points for dataclass components:**
1. Use `@dataclass` decorator on your subclass
2. Add fields with type annotations - they automatically become YAML schema fields
3. Use `field(default_factory=...)` for mutable defaults (lists, dicts)
4. The `Resolvable` interface (inherited from parent) handles YAML schema generation
5. All fields with defaults must come after fields without defaults

**Example with multiple custom fields:**

```python
from dataclasses import dataclass, field
import dagster as dg
from dagster_sling import SlingReplicationCollectionComponent

@dataclass
class CustomSlingComponent(SlingReplicationCollectionComponent):
    """Extended Sling component with additional configuration."""

    # New fields - all will appear in YAML schema
    demo_mode: bool = False
    enable_notifications: bool = False
    notification_channel: str = "slack"
    custom_tags: list[str] = field(default_factory=list)

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        if self.demo_mode:
            return self._build_demo_defs(context)
        return super().build_defs(context)
```

## Pattern for Pydantic BaseModel Components (Rare)

Some components may use Pydantic BaseModel. In these cases, inherit from both the parent component and `dg.Model`:

```python
import dagster as dg
from <integration_package> import <BaseComponentClass>

class Custom<ComponentName>(BaseComponentClass, dg.Model):
    """Customized component with demo mode support."""

    # New field - will appear in YAML schema
    demo_mode: bool = False

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        if self.demo_mode:
            return self._build_demo_defs(context)
        return super().build_defs(context)
```

## Pattern for Legacy execute()-based Components

For older components that override `execute()` instead of `build_defs()`:

```python
from dataclasses import dataclass
from dagster import AssetExecutionContext
from <integration_package> import <BaseComponentClass>
from collections.abc import Iterator
from typing import Any

@dataclass
class Custom<ComponentName>(BaseComponentClass):
    """Customized component with demo mode support."""

    demo_mode: bool = False

    def execute(
        self,
        context: AssetExecutionContext,
        **kwargs: Any,
    ) -> Iterator:
        """Custom execution logic with demo mode support."""
        if self.demo_mode:
            context.log.info("Running in demo mode with mocked data")
            yield from self._execute_demo_mode(context, **kwargs)
        else:
            context.log.info("Running with real integration")
            yield from super().execute(context, **kwargs)

    def _execute_demo_mode(
        self,
        context: AssetExecutionContext,
        **kwargs: Any,
    ) -> Iterator:
        """Demo mode implementation."""
        from dagster import Output
        context.log.info("Simulating integration execution locally")
        yield Output(value=None, output_name="result")
```

**Key customization points:**

1. **Override `build_defs()` or `execute()`** - Check demo_mode and return mock data
2. **Use dataclass fields** - They automatically become YAML schema fields via Resolvable
3. **Provide default values** - All custom fields should have defaults
4. **Add custom templating** - Override `get_additional_scope()` for YAML templating

**Example with custom templating:**

```python
from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any
import dagster as dg
from <integration_package> import <BaseComponentClass>

@dataclass
class Custom<ComponentName>(BaseComponentClass):
    demo_mode: bool = False

    @classmethod
    def get_additional_scope(cls) -> Mapping[str, Any]:
        """Add custom YAML templating functions."""
        def _custom_cron(cron_schedule: str) -> dg.AutomationCondition:
            return (
                dg.AutomationCondition.on_cron(cron_schedule)
                & ~dg.AutomationCondition.in_progress()
            )
        return {"custom_cron": _custom_cron}
```

### Step 5.5: Align Asset Keys for Downstream Components (CRITICAL for Multi-Component Pipelines)

**When to do this:** If other Dagster components in your pipeline will depend on assets from this component, override `get_asset_spec()` to generate asset keys that match downstream expectations.

**This applies when:**
- dbt models will consume these assets
- Custom Dagster assets will reference these assets in their `deps`
- Another integration component (Hightouch, Census, BI tools) expects specific asset key patterns
- You want to simplify multi-level nested keys for easier downstream consumption

#### Why This Matters

By default, integration components generate asset keys in their own structure. For example:
- Fivetran: `["fivetran", "raw", "customers"]`
- Sling: `["sling", "replications", "sync_name", "table"]`
- dbt: `["analytics", "marts", "customer_360"]`

**The problem:** Downstream components may expect different key structures, leading to broken dependencies or requiring per-asset configuration with `meta.dagster.asset_key`.

**The solution:** Override `get_asset_spec()` in the upstream component to generate keys that downstream components naturally reference.

#### Pattern: Override get_asset_spec()

```python
def get_asset_spec(self, props) -> dg.AssetSpec:
    """Override to generate asset keys matching downstream component expectations.

    This eliminates the need for meta.dagster.asset_key configuration in downstream
    components by aligning keys at the source.
    """
    base_spec = super().get_asset_spec(props)
    original_key = base_spec.key.path

    # Customize key structure for your pipeline
    # Example: Flatten nested keys for easier consumption
    custom_key = dg.AssetKey([...])  # Your key transformation logic

    return base_spec.replace_attributes(key=custom_key)
```

#### Example 1: Fivetran → dbt Pipeline

**Problem:** Fivetran creates `["fivetran", "raw", "customers"]`, but dbt expects `["fivetran_raw", "customers"]`

**Solution:**
```python
from dagster_fivetran import FivetranAccountComponent
from dagster_fivetran.translator import FivetranConnectorTableProps
import dagster as dg

class CustomFivetranComponent(FivetranAccountComponent):
    def get_asset_spec(self, props: FivetranConnectorTableProps) -> dg.AssetSpec:
        """Flatten asset keys for dbt compatibility."""
        base_spec = super().get_asset_spec(props)
        original_key = base_spec.key.path

        # Flatten: ["fivetran", "raw", "table"] -> ["fivetran_raw", "table"]
        if len(original_key) >= 2:
            flattened_key = dg.AssetKey(["fivetran_raw", "_".join(original_key[1:])])
        else:
            flattened_key = dg.AssetKey(["fivetran_raw", original_key[-1]])

        return base_spec.replace_attributes(key=flattened_key)
```

**Result:** dbt sources work automatically without meta.dagster configuration:
```yaml
# sources.yml - references work naturally now
sources:
  - name: fivetran_raw
    tables:
      - name: customers  # Matches ["fivetran_raw", "customers"]
```

#### Example 2: Sling → Custom Processing

**Problem:** Sling creates `["sling", "replications", "sync_name", "table"]`, but custom processors expect `["raw", "table"]`

**Solution:**
```python
from dagster_sling import SlingReplicationCollectionComponent
import dagster as dg

class CustomSlingComponent(SlingReplicationCollectionComponent):
    def get_asset_spec(self, props) -> dg.AssetSpec:
        """Simplify keys for downstream consumption."""
        base_spec = super().get_asset_spec(props)
        original_key = base_spec.key.path

        # Simplify: [..., "table"] -> ["raw", "table"]
        simplified_key = dg.AssetKey(["raw", original_key[-1]])

        return base_spec.replace_attributes(key=simplified_key)
```

**Result:** Custom assets reference naturally:
```python
@dg.asset(deps=[dg.AssetKey(["raw", "customers"])])
def process_customers(context): ...
```

#### Verify Asset Key Alignment

After implementing `get_asset_spec()`, verify dependencies are correct:

```bash
# Check asset keys and dependencies
uv run dg list defs --json | uv run python -c "
import sys, json
assets = json.load(sys.stdin)['assets']
print('\\n'.join([f\"{a['key']}: deps={a.get('deps', [])}\" for a in assets]))
"
```

**What to look for:**
- Downstream assets should list upstream assets in their `deps` array
- No duplicate asset keys (e.g., both `["fivetran", "raw", "table"]` and `["fivetran_raw", "table"]`)
- Asset keys match what downstream components expect

#### Key Principles

1. **Upstream defines, downstream consumes**: The upstream component should generate keys that downstream expects
2. **Configure once, apply to all**: One `get_asset_spec()` override applies to all assets the component creates
3. **Minimize downstream configuration**: Eliminate the need for `meta.dagster.asset_key` in every downstream reference
4. **Document your key structure**: Make it clear what asset key pattern your component produces

### Step 6: Update Component YAML

Update `defs.yaml` to reference your custom subclass. Your new fields (like `demo_mode`) will be available in the YAML schema.

```yaml
type: <project_name>.defs.<instance_name>.component.Custom<ComponentName>

attributes:
  # Your custom fields
  demo_mode: true
  # Parent class required fields
  <parent_field>: <value>
```

**Example for Sling (Configuration-based - NO demo_mode):**

Sling reads from local replication YAML files, so no demo_mode is needed:

```yaml
type: dagster_sling.SlingReplicationCollectionComponent

attributes:
  replications:
    - path: replication.yaml
```

**Example for dbt (Configuration-based - NO demo_mode):**

dbt reads from local project files, so no demo_mode is needed:

```yaml
type: dagster_dbt.DbtProjectComponent

attributes:
  project:
    project_dir: analytics_dbt
```

**Example with dummy credentials for demo mode (API-based components only):**

For API-based components, you MUST provide dummy values to satisfy parent class schema validation. These values remain in the YAML but are ignored when demo_mode is true:

**Example for Looker:**

```yaml
type: my_project.defs.looker_dashboards.component.CustomLookerComponent

attributes:
  demo_mode: true
  # Dummy Looker credentials - required for schema validation but ignored in demo mode
  looker_resource:
    base_url: "https://demo.looker.com"
    client_id: "demo_client_id"
    client_secret: "demo_client_secret"
```

**Example for PowerBI:**

```yaml
type: my_project.defs.powerbi_workspace.component.CustomPowerBIComponent

attributes:
  demo_mode: true
  # Dummy PowerBI credentials - required for schema validation but ignored in demo mode
  powerbi_resource:
    client_id: "demo_client_id"
    client_secret: "demo_client_secret"
    tenant_id: "demo_tenant_id"
  workspace_id: "demo_workspace_id"
```

**Example for Fivetran:**

```yaml
type: my_project.defs.fivetran_sync.component.CustomFivetranComponent

attributes:
  demo_mode: true
  # Dummy Fivetran credentials - required for schema validation but ignored in demo mode
  fivetran_resource:
    api_key: "demo_api_key"
    api_secret: "demo_api_secret"
  connector_id: "demo_connector_id"
```

**Important Notes:**
- The type must be the fully qualified Python path to your custom component class
- **ALWAYS provide dummy values** for required parent fields - they MUST be present in the YAML for schema validation
- **Keep dummy values UNCOMMENTED** - they're required for the YAML to load properly
- Use realistic dummy values (URLs, IDs, etc.) that look like real credentials but aren't
- Your demo_mode implementation will ignore these values and use mocked data instead

**To switch to real mode:**
1. Set `demo_mode: false`
2. Replace dummy values in YAML with real credentials
3. Redeploy

### Step 7: Configure Component Attributes

Fill in the required attributes for the integration component. Consult the component's documentation:

- For dbt: https://docs.dagster.io/integrations/dbt
- For Fivetran: https://docs.dagster.io/integrations/fivetran
- For PowerBI: https://docs.dagster.io/integrations/powerbi
- For Sling: https://docs.dagster.io/integrations/sling
- For Looker: https://docs.dagster.io/integrations/looker

Common attributes include:
- Configuration file paths
- Resource credentials
- Asset specifications
- Scheduling/automation conditions

### Step 8: Validate Setup and Asset Key Alignment

Run validation commands to ensure everything works:

```bash
# Check that definitions load without errors
uv run dg check defs

# List all assets to verify they were created
uv run dg list defs
```

Verify that:
- ✅ All expected assets from the integration are listed
- ✅ The component instance is properly configured
- ✅ No errors or warnings are shown
- ✅ If using demo mode, verify it can run without external connections

**CRITICAL: Verify Asset Key Alignment**

Check that asset dependencies are correct by running:

```bash
uv run dg list defs --json | uv run python -c "
import sys, json
data = json.load(sys.stdin)
assets = data.get('assets', [])
print('Asset Dependencies:\n')
for asset in assets:
    key = asset.get('key', 'unknown')
    deps = asset.get('deps', [])
    if deps:
        print(f'{key}')
        for dep in deps:
            print(f'  ← {dep}')
    else:
        print(f'{key} (no dependencies)')
    print()
"
```

**What to verify:**
- ✅ Downstream assets list upstream assets in their `deps` array
- ✅ No missing dependencies (especially critical for dbt models that should depend on source tables)
- ✅ Asset keys are simple and descriptive (typically 2 levels: `["category", "name"]`)
- ✅ Asset keys match what downstream consumers expect

**Common Issues and Fixes:**

1. **dbt models not depending on upstream sources:**
   - Problem: dbt staging models show no dependencies
   - Cause: SQL doesn't use `{{ source('source_name', 'table') }}`
   - Fix: Add `select * from {{ source('source_name', 'table') }}` references in SQL (even if just in a CTE that's not used for demo mode)

2. **Asset keys don't match downstream expectations:**
   - Problem: Fivetran creates `["fivetran", "connector", "schema", "table"]` but dbt expects `["fivetran_raw", "table"]`
   - Cause: Default component key structure is too nested
   - Fix: Override `get_asset_spec()` to flatten keys (see Step 5.5 for details)

3. **Reverse ETL components can't find dbt models:**
   - Problem: Hightouch/Census assets show missing dependencies
   - Cause: dbt model names don't match expected asset keys
   - Fix: Use simple dbt model names that match expected keys, or configure `deps=[AssetKey(["model_name"])]` explicitly

### Step 9: Test Demo Mode (If Applicable)

If you implemented demo mode:

1. Set `demo_mode: true` in the component YAML
2. Run `uv run dg check defs` to verify it works locally
3. Try materializing an asset to test the demo mode execution
4. Document how to switch between demo and real modes

**Testing commands:**

```bash
# Check definitions load
uv run dg check defs

# List available assets
uv run dg list defs

# Materialize a specific asset in demo mode
uv run dg materialize <asset_key>
```

## Important: Always Add Kinds to Demo Assets

When creating demo mode assets, **ALWAYS add the `kinds` parameter** to properly categorize the asset by its integration type. This helps with:
- Filtering assets in the Dagster UI
- Understanding the technology stack at a glance
- Organizing assets by integration

**Example with kinds:**
```python
@dg.asset(
    key=dg.AssetKey(["fivetran", "salesforce_sync"]),
    description="Demo Fivetran sync of Salesforce data",
    kinds={"fivetran"},  # ← REQUIRED: Add the integration kind
)
def fivetran_salesforce_sync(context: dg.AssetExecutionContext):
    context.log.info("Demo mode: Simulating Fivetran sync")
    return {"status": "success", "mode": "demo"}
```

**Common integration kinds:**
- `kinds={"fivetran"}` for Fivetran assets
- `kinds={"dbt"}` for dbt assets
- `kinds={"census"}` for Census assets
- `kinds={"sling"}` for Sling assets
- `kinds={"powerbi"}` for PowerBI assets
- `kinds={"looker"}` for Looker assets
- `kinds={"airbyte"}` for Airbyte assets

You can verify kinds are showing correctly by running:
```bash
uv run dg list defs
```
The "Kinds" column should show the integration type for each asset.

## Integration-Specific Guidance

### dbt Components (Configuration-File-Based)

**IMPORTANT:** `DbtProjectComponent` is configuration-file-based and reads from local dbt project files. **DO NOT implement demo_mode** - instead, just load the dbt project directly.

**Use the component directly:**

```yaml
# defs.yaml for dbt component
type: dagster_dbt.DbtProjectComponent

attributes:
  project:
    project_dir: my_dbt_project  # Path to local dbt project
```

**Only subclass if you need custom behavior** (NOT for demo mode):

```python
from dataclasses import dataclass
from dagster_dbt import DbtProjectComponent
import dagster as dg

@dataclass
class CustomDbtComponent(DbtProjectComponent):
    """Custom dbt component with additional features."""

    # Add custom fields if needed (NOT demo_mode)
    enable_custom_logging: bool = False

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        # Add custom behavior here
        defs = super().build_defs(context)

        if self.enable_custom_logging:
            # Custom logging logic
            pass

        return defs
```

The dbt component naturally works with local project files without requiring external API calls.

### Sling Components (Configuration-File-Based)

**IMPORTANT:** `SlingReplicationCollectionComponent` is configuration-file-based and reads from local replication YAML files. **DO NOT implement demo_mode** - instead, just load the replication configuration.

**Use the component directly:**

```yaml
# defs.yaml for Sling component
type: dagster_sling.SlingReplicationCollectionComponent

attributes:
  replications:
    - path: replication.yaml  # Path to local replication config
```

**Only subclass if you need custom behavior** (NOT for demo mode):

```python
from dataclasses import dataclass
from dagster_sling import SlingReplicationCollectionComponent
import dagster as dg

@dataclass
class CustomSlingComponent(SlingReplicationCollectionComponent):
    """Custom Sling component with additional features."""

    # Add custom fields if needed (NOT demo_mode)
    enable_custom_validation: bool = False

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        # Add custom behavior here
        defs = super().build_defs(context)

        if self.enable_custom_validation:
            # Custom validation logic
            pass

        return defs
```

The Sling component naturally works with local replication files without requiring external API calls.

### Fivetran Components (API-Based)

**Fivetran is API-based and requires credentials.** Implement demo_mode to mock API calls:

```python
from dataclasses import dataclass
from dagster_fivetran import FivetranComponent
import dagster as dg

@dataclass
class CustomFivetranComponent(FivetranComponent):
    """Fivetran component with demo mode support."""

    demo_mode: bool = False

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        if self.demo_mode:
            return self._build_demo_defs(context)
        return super().build_defs(context)

    def _build_demo_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        @dg.asset(
            key=dg.AssetKey(["fivetran", "demo_sync"]),
            kinds={"fivetran"},
        )
        def fivetran_demo_sync(context: dg.AssetExecutionContext):
            context.log.info("Demo mode: Simulating Fivetran sync")
            return {"status": "demo_success", "records_synced": 1000}

        return dg.Definitions(assets=[fivetran_demo_sync])
```

### PowerBI Components (API-Based)

**PowerBI is API-based and requires credentials.** Implement demo_mode to mock API calls:

```python
from dataclasses import dataclass
from dagster_powerbi import PowerBIWorkspaceComponent
import dagster as dg

@dataclass
class CustomPowerBIComponent(PowerBIWorkspaceComponent):
    """PowerBI component with demo mode support."""

    demo_mode: bool = False

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        if self.demo_mode:
            return self._build_demo_defs(context)
        return super().build_defs(context)

    def _build_demo_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        @dg.asset(
            key=dg.AssetKey(["powerbi", "demo_dashboard"]),
            kinds={"powerbi"},
        )
        def powerbi_demo_dashboard(context: dg.AssetExecutionContext):
            context.log.info("Demo mode: Using cached PowerBI metadata")
            return {"dashboards": ["Sales Dashboard", "Marketing Dashboard"]}

        return dg.Definitions(assets=[powerbi_demo_dashboard])
```

## Success Criteria

The component is complete when:

- ✅ Integration component is discovered and selected
- ✅ Component subclass is created (if needed) with proper inheritance
- ✅ Demo mode is implemented in `execute()` method (if applicable)
- ✅ Component YAML is properly configured with fully qualified type
- ✅ All required attributes are specified
- ✅ `uv run dg check defs` passes without errors
- ✅ `uv run dg list defs` shows all expected assets from the integration
- ✅ Demo mode works without external dependencies (if implemented)

### Troubleshooting

**Problem: Schema validation errors for missing required fields**

**Cause:** The parent component requires certain fields, but you didn't provide them in YAML.

**Solution:** Provide **dummy values** for required fields. Keep them UNCOMMENTED - they're needed for schema validation but will be ignored in demo mode:

```yaml
attributes:
  demo_mode: true
  # Dummy credentials - MUST be present and uncommented for schema validation
  looker_resource:
    base_url: "https://demo.looker.com"
    client_id: "demo_client_id"
    client_secret: "demo_client_secret"
```

### Import Errors

If you see import errors, ensure:
- The integration package is installed: `uv add dagster-<integration>`
- The package name matches the import: `from dagster_<name> import ...`

### Type Reference Errors

If the component can't be found:
- Verify the fully qualified type in `defs.yaml` matches your Python path
- Check that `component.py` is in the correct directory
- Ensure the class name matches exactly

### Validation Failures

If `dg check defs` fails:
- Check that all required attributes are provided in YAML (use dummy values if needed)
- Verify resource configurations are valid
- Ensure demo mode doesn't require external connections
- Verify `model_config = ConfigDict(extra="allow")` is set in your Python class

## Next Steps

After completion, inform the user:

1. ✅ The component has been created and validated
2. 📁 Location of the component files
3. 🔄 How to toggle demo mode (if applicable)
4. 📚 Links to integration-specific documentation
5. 🚀 How to customize further by overriding additional methods
6. 💡 How to add more component instances using the same pattern

## Additional Resources

- Subclassing Components Guide: https://docs.dagster.io/guides/build/components/creating-new-components/subclassing-components
- Integration Libraries: https://docs.dagster.io/integrations/libraries
- Component API Reference: https://docs.dagster.io/llms-full.txt
- Discovery command: `uv run dg docs integrations --json`
