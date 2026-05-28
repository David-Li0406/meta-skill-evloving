# Shared Module Outputs

output "tenant_id" {
  description = "Shared tenant ID"
  value       = module.tenant.id
}

output "infra_name" {
  description = "Infrastructure name"
  value       = var.infra
}

output "namespace" {
  description = "Kubernetes namespace"
  value       = module.tenant.namespace
}

# Database outputs - uncomment when RDS is configured
# output "rds_endpoint" {
#   description = "RDS endpoint"
#   value       = duplocloud_rds_instance.main.endpoint
#   sensitive   = true
# }

# output "rds_credentials" {
#   description = "RDS credentials"
#   value = {
#     host     = duplocloud_rds_instance.main.host
#     port     = 5432
#     username = duplocloud_rds_instance.main.master_username
#     password = random_password.db.result
#     database = "postgres"
#   }
#   sensitive = true
# }
