# Shared Configuration for {{WORKSPACE_NAME}}
#
# Place this file at: config/shared/{{WORKSPACE_NAME}}/shared.tfvars

portal_name = "myportal"
infra       = "nonprod01"

# Uncomment to configure RDS
# rds = {
#   engine_version = "15.4"
#   multi_az       = false
#   scaling_configuration = {
#     min_capacity = 0.5
#     max_capacity = 8
#   }
# }
