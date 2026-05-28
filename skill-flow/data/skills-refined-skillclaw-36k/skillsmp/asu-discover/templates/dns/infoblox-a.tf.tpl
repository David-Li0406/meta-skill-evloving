resource "infoblox_a_record" "{{name}}" {
  dns_view = "{{view}}"
  fqdn     = "{{domain}}"
  ip_addr  = "{{ip}}"
  comment  = "{{comment}}"
}
