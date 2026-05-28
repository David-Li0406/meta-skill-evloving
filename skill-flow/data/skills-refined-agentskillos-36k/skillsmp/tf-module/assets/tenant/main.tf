# Tenant Module
#
# Creates application tenant environments (dev01, stg01, prod01, etc.)
# Workspace name = tenant name

locals {
  portal_name = var.portal_name
  portal      = module.ctx.workspaces.portal
  devops      = module.ctx.workspaces.devops
  shared      = module.ctx.workspaces.shared
  infra       = module.ctx.workspaces.infra
}

module "ctx" {
  source  = "duplocloud/components/duplocloud//modules/context"
  version = "0.0.41"
  admin   = true
  jit = {
    aws = true
    k8s = true
  }
  workspaces = {
    portal = {
      name = local.portal_name
    }
    devops = {
      name   = local.portal_name
      prefix = "portal"
    }
    shared = {
      name   = var.shared
      prefix = "infra"
    }
    infra = {
      nameRef = {
        workspace = "shared"
        nameKey   = "infra_name"
      }
    }
  }
}

module "tenant" {
  source     = "duplocloud/components/duplocloud//modules/tenant"
  version    = "0.0.41"
  infra_name = local.shared.infra_name

  settings = {
    delete_protection = var.environment == "prod" ? "true" : "false"
  }
}
