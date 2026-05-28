resource "cloudflare_record" "{{name}}" {
  zone_id = data.vault_generic_secret.cloudflare.data["zone_id"]
  name    = "{{subdomain}}"
  value   = "{{value}}"
  type    = "A"
  proxied = {{proxied}}
}
