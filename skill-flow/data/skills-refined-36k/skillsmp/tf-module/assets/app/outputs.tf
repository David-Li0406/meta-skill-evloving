# {{APP_NAME}} Outputs

output "tenant_id" {
  description = "Tenant ID"
  value       = local.tenant.id
}

output "namespace" {
  description = "Kubernetes namespace"
  value       = local.tenant.namespace
}

# Add additional outputs as needed
# output "hostname" {
#   description = "Application hostname"
#   value       = local.hostname
# }
