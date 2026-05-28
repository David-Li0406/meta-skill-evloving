# Terraform MCP Tools Usage Guide

## Available MCP Tools

The Terraform MCP server provides three essential tools for working with Terraform providers:

### 1. search_providers
Search for Terraform providers in the registry.

**Usage:**
```
search_providers(query: str)
```

**When to use:**
- Finding providers for specific cloud platforms or services
- Discovering available providers before writing resources
- Exploring provider options for a requirement

**Example:**
```
search_providers("aws")
search_providers("azure networking")
search_providers("kubernetes")
```

### 2. get_provider_details
Get comprehensive details about a specific provider including available resources and data sources.

**Usage:**
```
get_provider_details(namespace: str, name: str, version: str = "latest")
```

**When to use:**
- Understanding available resources for a provider
- Checking data sources before writing queries
- Verifying resource types and capabilities
- Looking up provider configuration requirements

**Example:**
```
get_provider_details("hashicorp", "aws", "5.0.0")
get_provider_details("hashicorp", "azurerm")  # Uses latest version
```

### 3. get_latest_provider_version
Get the latest version number for a specific provider.

**Usage:**
```
get_latest_provider_version(namespace: str, name: str)
```

**When to use:**
- Determining the current stable version
- Writing version constraints in terraform.tf
- Ensuring compatibility with latest features

**Example:**
```
get_latest_provider_version("hashicorp", "aws")
get_latest_provider_version("hashicorp", "google")
```

## Terraform MCP Workflow

### Standard Implementation Pattern (Azure)

When implementing Terraform resources for Azure, follow this workflow:

1. **Search for Provider** (if provider is unknown)
   ```
   search_providers("azure")
   search_providers("azure api")
   ```

2. **Get Provider Details for azurerm**
   ```
   get_provider_details("hashicorp", "azurerm")
   ```
   This returns:
   - Available resource types (azurerm_*)
   - Available data sources (data.azurerm_*)
   - Provider configuration schema
   - Documentation links

3. **Get Provider Details for azapi** (for preview features)
   ```
   get_provider_details("azure", "azapi")
   ```

4. **Get Latest Versions** (for version constraints)
   ```
   get_latest_provider_version("hashicorp", "azurerm")
   get_latest_provider_version("azure", "azapi")
   ```

5. **Implement Resources**
   - Use resource types from provider details
   - Follow HashiCorp style conventions
   - Use azapi for preview/unsupported features
   - Reference official documentation for argument details

### Example Workflow

**User Request:** "Create an Azure VNet with subnets using Terraform"

**Step 1:** Get azurerm provider details
```
get_provider_details("hashicorp", "azurerm")
```

**Step 2:** Identify relevant resources from response:
- `azurerm_resource_group` - Resource group (always first)
- `azurerm_virtual_network` - VNet resource
- `azurerm_subnet` - Subnet resource
- Data source: `azurerm_client_config`

**Step 3:** Get latest version for terraform.tf
```
get_latest_provider_version("hashicorp", "azurerm")
```

**Step 4:** Implement following style guide conventions

## Integration with Style Guide

### Provider Block Structure

Based on MCP provider details, structure provider blocks properly:

**In providers.tf:**
```hcl
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}
```

**In terraform.tf:**
```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### Resource Implementation from MCP Data

When MCP returns resource types, implement with:
1. Proper naming (underscore-separated)
2. Required arguments first
3. Optional arguments with sensible defaults
4. Nested blocks properly indented

**Example:**
```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}
```

## Best Practices

### Always Query MCP Before Implementing
- Don't assume resource types or arguments
- Verify provider capabilities before writing code
- Check for available data sources to avoid hard-coding values

### Use Latest Versions Appropriately
- Pin to major versions: `~> 5.0` (allows 5.x updates)
- Avoid exact pins unless necessary: `= 5.0.1`
- Document version requirements in comments if constraints are strict

### Leverage Data Sources
- Use MCP to discover available data sources
- Prefer data sources over hard-coded values
- Examples: `aws_ami`, `aws_availability_zones`, `azurerm_client_config`

### Provider Documentation Links
- MCP responses include documentation URLs
- Reference official docs for complex resource configurations
- Use MCP for quick lookups, docs for detailed examples

## Azure Provider Patterns

### azurerm Provider (Primary)
```hcl
# Get provider details
get_provider_details("hashicorp", "azurerm")

# Common resources:
# - azurerm_resource_group (always create first)
# - azurerm_virtual_network, azurerm_subnet
# - azurerm_network_security_group
# - azurerm_storage_account
# - azurerm_app_service_plan, azurerm_linux_web_app
# - azurerm_cdn_frontdoor_profile, azurerm_cdn_frontdoor_firewall_policy
# - azurerm_key_vault, azurerm_key_vault_secret
# - azurerm_private_endpoint

# Common data sources:
# - azurerm_client_config (tenant, subscription, object IDs)
# - azurerm_subscription
# - azurerm_resource_group (for existing RGs)
```

### azapi Provider (Preview Features)
```hcl
# Get provider details
get_provider_details("azure", "azapi")

# Use for:
# - Preview features not yet in azurerm
# - Resources with new API versions
# - Custom Azure Resource Manager operations

# Common resources:
# - azapi_resource (generic resource creation)
# - azapi_update_resource (update existing resources)

# Common data sources:
# - azapi_resource (query existing resources)
# - azapi_resource_id (construct resource IDs)
```

### When to Use azapi vs azurerm

**Use azurerm when:**
- Resource is generally available in Azure
- Stable API version
- Full Terraform state management needed
- Standard Azure resources

**Use azapi when:**
- Feature is in preview
- Newer API version needed
- azurerm doesn't support the resource yet
- Custom ARM template logic needed

**Example Decision:**
```hcl
# Storage Account - use azurerm (stable, widely used)
resource "azurerm_storage_account" "main" {
  # ...
}

# New preview feature - use azapi
resource "azapi_resource" "preview_feature" {
  type = "Microsoft.NewService/resources@2024-01-01-preview"
  # ...
}
```

## Error Handling

### Provider Not Found
If `search_providers` returns no results:
- Try broader search terms
- Check spelling of provider name
- Verify provider exists in Terraform Registry

### Resource Type Not Available
If expected resource is missing from `get_provider_details`:
- Check provider version (may need newer version)
- Verify resource name spelling
- Consider alternative resources or data sources

### Version Compatibility
If version conflicts occur:
- Use `get_latest_provider_version` to check current version
- Review provider changelog for breaking changes
- Adjust version constraints in terraform.tf
