resource "infoblox_cname_record" "{{name}}" {
  dns_view  = "{{view}}"
  alias     = "{{domain}}"
  canonical = "{{target}}"
  comment   = "{{comment}}"
}
