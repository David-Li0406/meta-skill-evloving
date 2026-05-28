# Main resources and data sources

# Data sources should be defined before resources that reference them

data "azurerm_client_config" "current" {}

# Resource Group (always create first)
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.location

  tags = local.common_tags
}

# Example: Virtual Network
# resource "azurerm_virtual_network" "main" {
#   name                = "${local.resource_prefix}-vnet"
#   resource_group_name = azurerm_resource_group.main.name
#   location            = azurerm_resource_group.main.location
#   address_space       = var.vnet_address_space
#
#   tags = local.common_tags
# }

# Example: Subnets using for_each
# resource "azurerm_subnet" "private" {
#   for_each = local.network_config.subnets
#
#   name                 = "${local.resource_prefix}-${each.key}-subnet"
#   resource_group_name  = azurerm_resource_group.main.name
#   virtual_network_name = azurerm_virtual_network.main.name
#   address_prefixes     = [each.value.address_prefix]
#
#   service_endpoints = each.value.service_endpoints
# }

# Example: Using azapi for preview features
# resource "azapi_resource" "example" {
#   type      = "Microsoft.Example/exampleResources@2024-01-01"
#   name      = "${local.resource_prefix}-example"
#   parent_id = azurerm_resource_group.main.id
#   location  = var.location
#
#   body = jsonencode({
#     properties = {
#       exampleProperty = "value"
#     }
#   })
#
#   tags = local.common_tags
# }
