terraform {
  required_version = ">= 1.4.4"

  backend "s3" {
    key                  = "{{APP_NAME}}"
    workspace_key_prefix = "{{APP_NAME}}"
    encrypt              = true
  }

  required_providers {
    duplocloud = {
      source  = "duplocloud/duplocloud"
      version = ">= 0.11.0"
    }
    # Uncomment providers as needed
    # aws = {
    #   source  = "hashicorp/aws"
    #   version = ">= 5.0"
    # }
    # kubernetes = {
    #   source  = "hashicorp/kubernetes"
    #   version = ">= 2.0"
    # }
    # helm = {
    #   source  = "hashicorp/helm"
    #   version = ">= 2.0"
    # }
  }
}

provider "duplocloud" {}

# Uncomment if jit.aws = true in module.ctx
# provider "aws" {
#   region     = module.ctx.region
#   access_key = module.ctx.creds.aws.access_key_id
#   secret_key = module.ctx.creds.aws.secret_access_key
#   token      = module.ctx.creds.aws.session_token
# }

# Uncomment if jit.k8s = true in module.ctx
# provider "kubernetes" {
#   host                   = module.ctx.creds.k8s.endpoint
#   cluster_ca_certificate = module.ctx.creds.k8s.ca_certificate_data
#   token                  = module.ctx.creds.k8s.token
# }
