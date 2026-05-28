# Output values
# Outputs should be alphabetically ordered

output "location" {
  description = "Azure region where resources are deployed"
  value       = var.location
}

output "resource_group_id" {
  description = "ID of the resource group"
  value       = azurerm_resource_group.main.id
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

# Example: Sensitive output
# output "storage_account_primary_key" {
#   description = "Primary access key for storage account"
#   value       = azurerm_storage_account.main.primary_access_key
#   sensitive   = true
# }

# Example: Complex output
# output "subnet_ids" {
#   description = "Map of subnet names to IDs"
#   value = {
#     for k, v in azurerm_subnet.private : k => v.id
#   }
# }
