# Azure Terraform Patterns and Best Practices

## Resource Group Management

### Always Create Resource Group First
```hcl
# Resource group is the foundation for all Azure resources
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.location

  tags = local.common_tags
}

# All other resources reference the resource group
resource "azurerm_virtual_network" "main" {
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  # ...
}
```

### Resource Group Naming Convention
```hcl
# Pattern: {project}-{environment}-rg
# Examples:
# - myapp-dev-rg
# - myapp-staging-rg
# - myapp-prod-rg

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

locals {
  rg_name = "${var.project_name}-${var.environment}-rg"
}
```

## Networking Patterns

### Virtual Network with Multiple Subnets
```hcl
locals {
  subnets = {
    app = {
      address_prefix    = "10.0.1.0/24"
      service_endpoints = ["Microsoft.Storage", "Microsoft.KeyVault"]
    }
    data = {
      address_prefix    = "10.0.2.0/24"
      service_endpoints = ["Microsoft.Sql"]
    }
    aks = {
      address_prefix    = "10.0.3.0/24"
      service_endpoints = []
    }
  }
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.project_name}-vnet"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  address_space       = ["10.0.0.0/16"]

  tags = local.common_tags
}

resource "azurerm_subnet" "subnets" {
  for_each = local.subnets

  name                 = "${var.project_name}-${each.key}-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [each.value.address_prefix]

  service_endpoints = each.value.service_endpoints
}
```

### Network Security Groups
```hcl
resource "azurerm_network_security_group" "app" {
  name                = "${var.project_name}-app-nsg"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  tags = local.common_tags
}

# Allow HTTPS inbound
resource "azurerm_network_security_rule" "allow_https" {
  name                        = "AllowHTTPS"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.app.name
}

# Associate NSG with subnet
resource "azurerm_subnet_network_security_group_association" "app" {
  subnet_id                 = azurerm_subnet.subnets["app"].id
  network_security_group_id = azurerm_network_security_group.app.id
}
```

## Private Endpoints Pattern

### App Service with Private Endpoint
```hcl
# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${var.project_name}-asp"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "P1v3"

  tags = local.common_tags
}

# Web App
resource "azurerm_linux_web_app" "main" {
  name                = "${var.project_name}-app"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_service_plan.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    always_on = true
  }

  tags = local.common_tags
}

# Private Endpoint
resource "azurerm_private_endpoint" "app" {
  name                = "${var.project_name}-app-pe"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  subnet_id           = azurerm_subnet.subnets["app"].id

  private_service_connection {
    name                           = "${var.project_name}-app-psc"
    private_connection_resource_id = azurerm_linux_web_app.main.id
    is_manual_connection           = false
    subresource_names              = ["sites"]
  }

  tags = local.common_tags
}

# Private DNS Zone
resource "azurerm_private_dns_zone" "app" {
  name                = "privatelink.azurewebsites.net"
  resource_group_name = azurerm_resource_group.main.name

  tags = local.common_tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "app" {
  name                  = "${var.project_name}-app-dns-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.app.name
  virtual_network_id    = azurerm_virtual_network.main.id

  tags = local.common_tags
}
```

## Front Door Patterns

### Front Door with WAF Policy
```hcl
resource "azurerm_cdn_frontdoor_profile" "main" {
  name                = "${var.project_name}-fd"
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "Premium_AzureFrontDoor"

  tags = local.common_tags
}

resource "azurerm_cdn_frontdoor_endpoint" "main" {
  name                     = "${var.project_name}-endpoint"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id

  tags = local.common_tags
}

resource "azurerm_cdn_frontdoor_origin_group" "main" {
  name                     = "${var.project_name}-origin-group"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id

  load_balancing {
    sample_size                        = 4
    successful_samples_required        = 3
    additional_latency_in_milliseconds = 50
  }

  health_probe {
    interval_in_seconds = 30
    path                = "/health"
    protocol            = "Https"
    request_type        = "GET"
  }
}

resource "azurerm_cdn_frontdoor_origin" "main" {
  name                          = "${var.project_name}-origin"
  cdn_frontdoor_origin_group_id = azurerm_cdn_frontdoor_origin_group.main.id
  certificate_name_check_enabled = true

  host_name          = azurerm_linux_web_app.main.default_hostname
  http_port          = 80
  https_port         = 443
  origin_host_header = azurerm_linux_web_app.main.default_hostname
  priority           = 1
  weight             = 1000
}

resource "azurerm_cdn_frontdoor_firewall_policy" "main" {
  name                = "${var.project_name}fdwaf"
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = azurerm_cdn_frontdoor_profile.main.sku_name
  mode                = "Prevention"

  managed_rule {
    type    = "Microsoft_DefaultRuleSet"
    version = "2.1"
  }

  managed_rule {
    type    = "Microsoft_BotManagerRuleSet"
    version = "1.0"
  }

  tags = local.common_tags
}

resource "azurerm_cdn_frontdoor_security_policy" "main" {
  name                     = "${var.project_name}-security-policy"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id

  security_policies {
    firewall {
      cdn_frontdoor_firewall_policy_id = azurerm_cdn_frontdoor_firewall_policy.main.id

      association {
        domain {
          cdn_frontdoor_domain_id = azurerm_cdn_frontdoor_endpoint.main.id
        }

        patterns_to_match = ["/*"]
      }
    }
  }
}
```

## Storage Account Patterns

### Secure Storage Account
```hcl
resource "azurerm_storage_account" "main" {
  name                     = "${var.project_name}${var.environment}st"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # Security settings
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  enable_https_traffic_only       = true

  # Network rules
  network_rules {
    default_action             = "Deny"
    bypass                     = ["AzureServices"]
    virtual_network_subnet_ids = [azurerm_subnet.subnets["app"].id]
  }

  tags = local.common_tags
}

resource "azurerm_storage_container" "data" {
  name                  = "data"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}
```

## Key Vault Patterns

### Key Vault with Access Policies
```hcl
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                = "${var.project_name}-${var.environment}-kv"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  # Security settings
  purge_protection_enabled   = true
  soft_delete_retention_days = 90

  # Network ACLs
  network_acls {
    default_action             = "Deny"
    bypass                     = "AzureServices"
    virtual_network_subnet_ids = [azurerm_subnet.subnets["app"].id]
  }

  tags = local.common_tags
}

# Access policy for current user/service principal
resource "azurerm_key_vault_access_policy" "admin" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  secret_permissions = [
    "Get",
    "List",
    "Set",
    "Delete",
    "Purge",
    "Recover"
  ]

  key_permissions = [
    "Get",
    "List",
    "Create",
    "Delete",
    "Purge",
    "Recover"
  ]
}

# Store secrets
resource "azurerm_key_vault_secret" "app_secret" {
  name         = "app-secret"
  value        = var.app_secret
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [azurerm_key_vault_access_policy.admin]

  tags = local.common_tags
}
```

## azapi Provider Usage

### Using azapi for Preview Features
```hcl
# Use azapi when resource is not yet available in azurerm
resource "azapi_resource" "example" {
  type      = "Microsoft.Example/exampleResources@2024-01-01-preview"
  name      = "${var.project_name}-example"
  parent_id = azurerm_resource_group.main.id
  location  = var.location

  body = jsonencode({
    properties = {
      setting1 = "value1"
      setting2 = {
        nestedSetting = "value2"
      }
    }
  })

  tags = local.common_tags
}

# Query existing resource with azapi
data "azapi_resource" "existing" {
  type      = "Microsoft.Example/exampleResources@2024-01-01-preview"
  name      = "existing-resource"
  parent_id = azurerm_resource_group.main.id

  response_export_values = ["properties.endpoint"]
}

# Use exported values
output "endpoint" {
  value = jsondecode(data.azapi_resource.existing.output).properties.endpoint
}
```

### Update Existing Resources with azapi
```hcl
# Update specific properties on existing resources
resource "azapi_update_resource" "example" {
  type        = "Microsoft.Example/exampleResources@2024-01-01"
  resource_id = azurerm_example_resource.main.id

  body = jsonencode({
    properties = {
      newFeature = true
    }
  })
}
```

## Common Locals Pattern

### Standard Locals Configuration
```hcl
locals {
  # Common tags for all resources
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_name
    CostCenter  = var.cost_center
  }

  # Resource naming prefix
  resource_prefix = "${var.project_name}-${var.environment}"

  # Location abbreviations
  location_abbr = {
    japaneast      = "jpe"
    japanwest      = "jpw"
    eastus         = "eus"
    westus         = "wus"
    westeurope     = "weu"
    northeurope    = "neu"
  }

  # Environment-specific settings
  sku_map = {
    dev     = "B1"
    staging = "S1"
    prod    = "P1v3"
  }
}
```

## Data Sources Pattern

### Common Data Sources
```hcl
# Get current Azure client configuration
data "azurerm_client_config" "current" {}

# Get subscription details
data "azurerm_subscription" "current" {}

# Get existing resource group
data "azurerm_resource_group" "existing" {
  name = var.existing_rg_name
}

# Get existing virtual network
data "azurerm_virtual_network" "existing" {
  name                = var.existing_vnet_name
  resource_group_name = data.azurerm_resource_group.existing.name
}
```
