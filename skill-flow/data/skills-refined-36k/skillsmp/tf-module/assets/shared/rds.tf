# Shared RDS Instance
#
# Uncomment to create a shared database

# resource "random_password" "db" {
#   length  = 24
#   special = false
# }

# resource "duplocloud_rds_instance" "main" {
#   tenant_id       = module.tenant.id
#   name            = "main"
#   engine          = 1 # PostgreSQL
#   engine_version  = var.rds.engine_version
#   size            = var.rds.instance_class
#   encrypt_storage = true
#   multi_az        = var.rds.multi_az
#   master_username = "postgres"
#   master_password = random_password.db.result
#
#   dynamic "v2_scaling_configuration" {
#     for_each = var.rds.scaling_configuration != null ? [1] : []
#     content {
#       min_capacity = var.rds.scaling_configuration.min_capacity
#       max_capacity = var.rds.scaling_configuration.max_capacity
#     }
#   }
# }
