# {{APP_NAME}} Module
#
# This module deploys {{APP_NAME}} to a tenant environment.
# Workspace name = target tenant name (e.g., dev01, stg01, prod01)

locals {
  name   = "{{APP_NAME}}"
  tenant = module.ctx.workspaces.tenant
  # Uncomment if you need shared workspace data
  # shared = module.ctx.workspaces.shared
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  # Uncomment JIT credentials as needed
  # jit = {
  #   aws = true
  #   k8s = true
  # }
  workspaces = {
    tenant = {} # Empty = terraform.workspace is the tenant name
    # Uncomment to access shared workspace
    # shared = {
    #   nameRef = {
    #     workspace = "tenant"
    #     nameKey   = "shared_name"
    #   }
    #   prefix = "infra"
    # }
  }
}
