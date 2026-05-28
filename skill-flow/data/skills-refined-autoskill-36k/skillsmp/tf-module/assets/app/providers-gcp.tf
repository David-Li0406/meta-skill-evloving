terraform {
  required_version = ">= 1.4.4"

  backend "gcs" {
    prefix = "{{APP_NAME}}"
  }

  required_providers {
    duplocloud = {
      source  = "duplocloud/duplocloud"
      version = ">= 0.11.0"
    }
    # Uncomment providers as needed
    # google = {
    #   source  = "hashicorp/google"
    #   version = ">= 6.0"
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

# provider "google" {
#   project = module.ctx.account_id
#   region  = module.ctx.region
# }

# Uncomment if jit.k8s = true in module.ctx
# provider "kubernetes" {
#   host                   = module.ctx.creds.k8s.endpoint
#   cluster_ca_certificate = module.ctx.creds.k8s.ca_certificate_data
#   token                  = module.ctx.creds.k8s.token
# }
