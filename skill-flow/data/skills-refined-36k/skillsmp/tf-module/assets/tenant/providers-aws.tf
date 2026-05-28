terraform {
  required_version = ">= 1.4.4"

  backend "s3" {
    key                  = "tenant"
    workspace_key_prefix = "tenant"
    encrypt              = true
  }

  required_providers {
    duplocloud = {
      source  = "duplocloud/duplocloud"
      version = ">= 0.11.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0"
    }
    github = {
      source  = "integrations/github"
      version = ">= 6.0"
    }
  }
}

provider "duplocloud" {}

provider "aws" {
  region     = local.infra.region
  access_key = module.ctx.creds.aws.access_key_id
  secret_key = module.ctx.creds.aws.secret_access_key
  token      = module.ctx.creds.aws.session_token
}

provider "kubernetes" {
  host                   = module.ctx.creds.k8s.endpoint
  cluster_ca_certificate = module.ctx.creds.k8s.ca_certificate_data
  token                  = module.ctx.creds.k8s.token
}

# Uncomment for GitHub integration
# data "aws_ssm_parameter" "github_app_id" {
#   name = "/github/app_id"
# }
#
# data "aws_ssm_parameter" "github_private_key" {
#   name            = "/github/private_key"
#   with_decryption = true
# }
#
# provider "github" {
#   owner = var.github_org
#   app_auth {
#     id              = data.aws_ssm_parameter.github_app_id.value
#     installation_id = var.github_installation_id
#     pem_file        = data.aws_ssm_parameter.github_private_key.value
#   }
# }
