---
name: bicep-generation
description: Generate Azure Bicep infrastructure files using the Bicep Generator MCP tools. Use when creating Azure infrastructure as code, designing cloud architecture, or generating Bicep templates.
---

# Bicep Infrastructure Generation

Generate Azure Bicep infrastructure files by first planning the architecture, then generating resource configurations, and finally creating complete Bicep templates.

## Workflow

### 1. Plan the Architecture

Always start by gathering comprehensive requirements using `mcp_bicepgenerato_generate_infrastructure_plan`:

```
mcp_bicepgenerato_generate_infrastructure_plan
  requirements: "Create a web application with Azure App Service, Key Vault for secrets, and Application Insights for monitoring"
```

This returns:
- Overview of the infrastructure design
- Complete list of required resources with types and API versions
- Resource relationships and dependencies
- Security and configuration requirements

### 2. Generate Resource Configurations

For each resource in the plan, use `mcp_bicepgenerato_generate_resource_body` to get properly configured resource definitions:

```
mcp_bicepgenerato_generate_resource_body
  resourceType: "Microsoft.KeyVault/vaults"
  apiVersion: "2023-07-01"
  promptDescription: "Key Vault with soft delete, purge protection, and network restrictions following security best practices"
```

Returns complete resource body JSON with security best practices applied.

### 3. Create the Bicep File

Generate complete `.bicep` and `.bicepparam` files including:
- Parameters with @description annotations for configurable values
- Variables for computed values
- Resources converted from JSON to Bicep syntax
- Proper resource dependencies using Bicep references
- Outputs for important resource properties (IDs, endpoints, URLs)
- Comments documenting configuration decisions

## Example

When asked to create infrastructure:

1. Generate plan to understand full requirements
2. Explain the proposed architecture to the user
3. Generate resource bodies for each component
4. Create main.bicep with all resources properly configured
5. Validate all planned resources are included

## Best Practices

- Always use the infrastructure plan first - never skip to resource generation
- Apply the security best practices included in generated resource bodies
- Extract environment-specific values as parameters
- Use current API versions from the plan
- Document key configuration choices with comments
- Ensure proper resource dependencies using Bicep syntax
