# Hybrid Pattern: Infoblox CNAME -> Cloudflare CDN -> Origin
# Use this when an *.asu.edu domain needs Cloudflare CDN/WAF protection
#
# Flow: User -> {{subdomain}}.asu.edu (Infoblox) -> Cloudflare CDN -> {{origin}}

# Step 1: Infoblox CNAME records pointing to Cloudflare CDN
resource "infoblox_cname_record" "{{name}}_internal" {
  dns_view  = "default"
  alias     = "{{subdomain}}.asu.edu"
  canonical = "{{subdomain}}.asu.edu.cdn.cloudflare.net"
  comment   = "Points to Cloudflare CDN - Managed by Terraform"
}

resource "infoblox_cname_record" "{{name}}_external" {
  dns_view  = "external"
  alias     = "{{subdomain}}.asu.edu"
  canonical = "{{subdomain}}.asu.edu.cdn.cloudflare.net"
  comment   = "Points to Cloudflare CDN - Managed by Terraform"
}

# Step 2: Cloudflare proxied record pointing to actual origin
resource "cloudflare_record" "{{name}}" {
  zone_id = data.vault_generic_secret.cloudflare.data["zone_id"]
  name    = "{{subdomain}}.asu.edu"
  value   = "{{origin}}"
  type    = "CNAME"
  proxied = true
}
