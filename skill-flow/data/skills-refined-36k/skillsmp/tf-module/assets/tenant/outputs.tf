# Tenant Module Outputs

output "tenant_id" {
  description = "Tenant ID"
  value       = module.tenant.id
}

output "name" {
  description = "Tenant name"
  value       = module.tenant.name
}

output "namespace" {
  description = "Kubernetes namespace"
  value       = module.tenant.namespace
}

output "infra_name" {
  description = "Infrastructure name"
  value       = local.shared.infra_name
}

output "shared_name" {
  description = "Shared workspace name"
  value       = var.shared
}

output "portal_name" {
  description = "Portal workspace name"
  value       = local.portal_name
}

# Pass through shared resources for app modules
output "rds_endpoint" {
  description = "Database endpoint from shared"
  value       = try(local.shared.rds_endpoint, null)
  sensitive   = true
}
