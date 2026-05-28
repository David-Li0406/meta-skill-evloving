terraform {
  required_version = ">= 1.4.4"

  backend "s3" {
    key                  = "shared"
    workspace_key_prefix = "infra"
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
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
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
