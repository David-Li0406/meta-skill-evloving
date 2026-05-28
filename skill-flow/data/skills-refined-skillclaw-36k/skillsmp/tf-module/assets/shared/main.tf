# Shared Module
#
# Creates shared stateful resources (databases, caches) for an infrastructure.
# This is a tenant with enable_host_other_tenants = true.
# Workspace name = shared tenant name

locals {
  tenant_name = terraform.workspace
  portal      = module.ctx.workspaces.portal
  infra       = module.ctx.workspaces.infra
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit = {
    aws = true
  }
  workspaces = {
    portal = {
      name = var.portal_name
    }
    infra = {
      name   = var.infra
      prefix = "infra"
    }
  }
}

module "tenant" {
  source     = "duplocloud/components/duplocloud//modules/tenant"
  version    = "0.0.41"
  infra_name = var.infra

  settings = {
    enable_host_other_tenants = "true"
    delete_protection         = "true"
  }
}
