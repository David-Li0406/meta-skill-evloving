# ==============================================================================
# Vault Secrets for DNS Provider Authentication
# ==============================================================================
# Choose the appropriate section based on your DNS provider requirements.
# These data sources retrieve credentials from HashiCorp Vault.

# ------------------------------------------------------------------------------
# infoblox
# ------------------------------------------------------------------------------
# Vault secrets for Infoblox provider authentication
# Used for *.asu.edu domains via dnsadmin.asu.edu
data "vault_generic_secret" "infoblox" {
  path = "secret/services/dco/jenkins/dco/jenkins/prod/kerberos/principals/jenkins_app"
}

# Provider configuration (add to providers.tf)
# provider "infoblox" {
#   server   = "dnsadmin.asu.edu"
#   username = data.vault_generic_secret.infoblox.data["username"]
#   password = data.vault_generic_secret.infoblox.data["password"]
# }

# ------------------------------------------------------------------------------
# cloudflare
# ------------------------------------------------------------------------------
# Vault secrets for Cloudflare provider authentication
# Used for non-ASU domains and CDN/WAF configurations
data "vault_generic_secret" "cloudflare" {
  path = "secret/services/dco/jenkins/ewp/cloudflare/prod/api/principals/asu-jenkins-devops"
}

# Provider configuration (add to providers.tf)
# provider "cloudflare" {
#   api_token = data.vault_generic_secret.cloudflare.data["api_token"]
# }
