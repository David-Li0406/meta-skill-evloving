---
name: dns
title: DNS Configuration
description: DNS management patterns for ASU - Infoblox for *.asu.edu, Cloudflare for external
subtypes:
  - infoblox
  - cloudflare
  - hybrid
---

# DNS Configuration

DNS management patterns for ASU infrastructure using Terraform.

## Routing Rules

| Domain Pattern | Provider | Action |
|----------------|----------|--------|
| *.asu.edu | Infoblox | Create records via dnsadmin.asu.edu |
| Non-ASU domains | Cloudflare | Register domain + configure DNS |
| ASU + CDN/WAF | Hybrid | Infoblox CNAME → Cloudflare CDN → Origin |

## Infoblox

For all `*.asu.edu` domains.

### Configuration

| Setting | Value |
|---------|-------|
| Server | dnsadmin.asu.edu |
| Views | default (internal), external (public) |
| Vault Path | secret/services/dco/jenkins/dco/jenkins/prod/kerberos/principals/jenkins_app |

### Resources
- infoblox_a_record
- infoblox_cname_record

### Example

```hcl
resource "infoblox_cname_record" "myapp_internal" {
  dns_view  = "default"
  alias     = "myapp.asu.edu"
  canonical = "myapp-origin.aws.amazon.com"
  comment   = "Managed by Terraform"
}

resource "infoblox_cname_record" "myapp_external" {
  dns_view  = "external"
  alias     = "myapp.asu.edu"
  canonical = "myapp-origin.aws.amazon.com"
  comment   = "Managed by Terraform"
}
```

### Example Repos
- ASU/sso-shibboleth - Hybrid Infoblox+Cloudflare pattern
- ASU/hosting-fse - Infoblox CNAME with for_each
- ASU/ewp-www-farm-acquia - Infoblox A and CNAME records
- ASU/hosting-cronkite - infoblox-cname-record module

## Cloudflare

For non-ASU domain registration and DNS.

### Configuration

| Setting | Value |
|---------|-------|
| Vault Path | secret/services/dco/jenkins/ewp/cloudflare/prod/api/principals/asu-jenkins-devops |

### Resources
- cloudflare_record
- cloudflare_zone

### Terraform Modules
- cloudflare-tunnel
- cloudflare-tunnel-route53-dns
- cloudflare-access-app
- cloudflare-origin-ca-certificate

### Example

```hcl
resource "cloudflare_record" "myapp" {
  zone_id = data.vault_generic_secret.cloudflare.data["zone_id"]
  name    = "www"
  value   = "myapp-origin.aws.amazon.com"
  type    = "CNAME"
  proxied = true  # Enable Cloudflare CDN/WAF
}
```

## Hybrid

Use when ASU domain needs Cloudflare CDN/WAF protection.

### Flow

```
User → myapp.asu.edu (Infoblox) → Cloudflare CDN → Origin
```

### Example

```hcl
# Step 1: Infoblox CNAMEs pointing to Cloudflare CDN
resource "infoblox_cname_record" "myapp_internal" {
  dns_view  = "default"
  alias     = "myapp.asu.edu"
  canonical = "myapp.asu.edu.cdn.cloudflare.net"
  comment   = "Points to Cloudflare CDN"
}

resource "infoblox_cname_record" "myapp_external" {
  dns_view  = "external"
  alias     = "myapp.asu.edu"
  canonical = "myapp.asu.edu.cdn.cloudflare.net"
  comment   = "Points to Cloudflare CDN"
}

# Step 2: Cloudflare proxied record to origin
resource "cloudflare_record" "myapp" {
  zone_id = data.vault_generic_secret.cloudflare.data["zone_id"]
  name    = "myapp.asu.edu"
  value   = "myapp-origin.aws.amazon.com"
  type    = "CNAME"
  proxied = true
}
```

### Example Repos
- ASU/sso-shibboleth - Full hybrid pattern implementation

## Vault Secrets

```hcl
# Infoblox credentials
data "vault_generic_secret" "infoblox" {
  path = "secret/services/dco/jenkins/dco/jenkins/prod/kerberos/principals/jenkins_app"
}

# Cloudflare credentials
data "vault_generic_secret" "cloudflare" {
  path = "secret/services/dco/jenkins/ewp/cloudflare/prod/api/principals/asu-jenkins-devops"
}
```

## Best Practices

- Always create records in BOTH Infoblox views (default + external) for *.asu.edu
- Use Vault for provider credentials - never hardcode
- Enable proxied=true on Cloudflare records for CDN/WAF benefits
- Use hybrid pattern when ASU domains need Cloudflare protection
- Add meaningful comments to DNS records for auditability
- Use for_each when creating multiple similar records

## Related Commands

```bash
discover.sh dns-validate --domain myapp.asu.edu
discover.sh dns-scaffold --domain myapp.asu.edu --type cname --target cdn.example.com
discover.sh dns-scaffold --domain myapp.asu.edu --pattern hybrid --origin origin.aws.com
discover.sh dns-examples
```
