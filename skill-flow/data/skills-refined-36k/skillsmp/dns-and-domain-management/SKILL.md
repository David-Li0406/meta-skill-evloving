---
name: DNS and Domain Management
description: This skill should be used when the user asks to "configure DNS", "set up DNS records", "manage domains", "register a domain", "transfer a domain", "set up SSL certificates", "configure CDN", "DNS troubleshooting", "DNS propagation", "DNSSEC", "domain registrar", or needs help with DNS configuration, domain management, or SSL/TLS setup.
version: 1.0.0
---

# DNS and Domain Management

Comprehensive guidance for DNS configuration, domain management, SSL/TLS certificates, and CDN setup.

## DNS Record Types

### Essential Records

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | `example.com → 93.184.216.34` |
| AAAA | IPv6 address | `example.com → 2606:2800:220:1::` |
| CNAME | Alias to another domain | `www.example.com → example.com` |
| MX | Mail server | `example.com → mail.example.com (priority 10)` |
| TXT | Text data (SPF, DKIM, verification) | `v=spf1 include:_spf.google.com ~all` |
| NS | Nameserver delegation | `example.com → ns1.provider.com` |

### Service Records

| Type | Purpose | Example |
|------|---------|---------|
| SRV | Service location | `_sip._tcp.example.com → 10 5 5060 sip.example.com` |
| CAA | Certificate authority authorization | `0 issue "letsencrypt.org"` |
| PTR | Reverse DNS lookup | `34.216.184.93.in-addr.arpa → example.com` |

## Common DNS Configurations

### Web Application

```
; Root domain
example.com.        A       93.184.216.34
example.com.        AAAA    2606:2800:220:1::

; WWW subdomain (CNAME to root)
www.example.com.    CNAME   example.com.

; API subdomain
api.example.com.    A       93.184.216.35

; CDN for static assets
cdn.example.com.    CNAME   d1234567890.cloudfront.net.
```

### Email Configuration

```
; MX records (lower priority = higher preference)
example.com.        MX      10 mail1.example.com.
example.com.        MX      20 mail2.example.com.

; SPF record
example.com.        TXT     "v=spf1 include:_spf.google.com ~all"

; DKIM record
selector._domainkey.example.com.  TXT  "v=DKIM1; k=rsa; p=MIGfMA0..."

; DMARC record
_dmarc.example.com. TXT     "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
```

### Multi-Region Setup

```
; Geographic DNS routing (provider-specific)
; US users
us.example.com.     A       192.0.2.1

; EU users
eu.example.com.     A       192.0.2.2

; Latency-based routing via cloud provider DNS
app.example.com.    ALIAS   app-lb.us-east-1.elb.amazonaws.com.
```

## DNS Management Commands

### Query DNS Records

```bash
# Basic lookup
dig example.com A
dig example.com MX
dig example.com TXT

# Specific nameserver
dig @8.8.8.8 example.com A

# Trace DNS resolution
dig +trace example.com

# Short output
dig +short example.com A

# All records
dig example.com ANY
```

### Check DNS Propagation

```bash
# Check multiple DNS servers
for ns in 8.8.8.8 1.1.1.1 9.9.9.9; do
  echo "=== $ns ==="
  dig @$ns example.com A +short
done
```

### Verify Email DNS

```bash
# Check MX records
dig example.com MX

# Verify SPF
dig example.com TXT | grep spf

# Check DKIM
dig selector._domainkey.example.com TXT

# Verify DMARC
dig _dmarc.example.com TXT
```

## SSL/TLS Certificates

### Certificate Types

| Type | Validation | Use Case |
|------|------------|----------|
| DV (Domain) | Domain ownership | Basic websites |
| OV (Organization) | + Business verification | Business websites |
| EV (Extended) | + Extensive verification | Financial, e-commerce |
| Wildcard | *.domain.com | Multiple subdomains |
| Multi-domain (SAN) | Multiple specific domains | Complex setups |

### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (standalone)
sudo certbot certonly --standalone -d example.com -d www.example.com

# Get certificate (webroot)
sudo certbot certonly --webroot -w /var/www/html -d example.com

# Auto-renewal
sudo certbot renew --dry-run

# Wildcard certificate (requires DNS challenge)
sudo certbot certonly --manual --preferred-challenges dns \
  -d "*.example.com" -d example.com
```

### Certificate Management

```bash
# View certificate details
openssl x509 -in cert.pem -text -noout

# Check certificate expiration
openssl x509 -in cert.pem -enddate -noout

# Verify certificate chain
openssl verify -CAfile chain.pem cert.pem

# Test SSL connection
openssl s_client -connect example.com:443 -servername example.com
```

## CDN Configuration

### CloudFront Setup

1. Create distribution
2. Configure origins (S3, ALB, custom origin)
3. Set cache behaviors
4. Configure SSL certificate
5. Create DNS alias

```bash
# AWS CLI example
aws cloudfront create-distribution \
  --distribution-config file://distribution-config.json
```

### Cloudflare Setup

1. Add site to Cloudflare
2. Update nameservers at registrar
3. Configure SSL mode (Flexible, Full, Full Strict)
4. Enable caching rules
5. Configure page rules

### Cache Control Headers

```
# Static assets (long cache)
Cache-Control: public, max-age=31536000, immutable

# Dynamic content (revalidate)
Cache-Control: no-cache, must-revalidate

# Private content (no CDN caching)
Cache-Control: private, no-store
```

## Domain Registrar Operations

### Domain Registration Checklist

- [ ] Choose registrar (Cloudflare, Namecheap, Google Domains)
- [ ] Enable WHOIS privacy
- [ ] Enable auto-renewal
- [ ] Set up registrar lock
- [ ] Configure 2FA on registrar account
- [ ] Document DNS settings before changes

### Domain Transfer Process

1. Unlock domain at current registrar
2. Get authorization/EPP code
3. Initiate transfer at new registrar
4. Confirm transfer via email
5. Wait for transfer completion (5-7 days typical)
6. Verify DNS settings after transfer

### DNSSEC Configuration

```bash
# Generate DNSSEC keys (using bind-utils)
dnssec-keygen -a ECDSAP256SHA256 -b 256 -n ZONE example.com

# Sign zone
dnssec-signzone -o example.com -k Kexample.com.+013+12345.key \
  example.com.zone Kexample.com.+013+67890.key

# Add DS record at registrar
# DS record format: keytag algorithm digest-type digest
```

## Troubleshooting

### Common DNS Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Propagation delay | Old records still showing | Wait 24-48h, lower TTL before changes |
| CNAME at apex | Cannot add CNAME for root | Use ALIAS/ANAME or A record |
| Missing www | www.site.com not working | Add CNAME or A record for www |
| Email not working | Emails bouncing | Check MX, SPF, DKIM, DMARC |
| SSL mismatch | Browser certificate warning | Ensure cert matches domain |

### Debug Commands

```bash
# Full DNS trace
dig +trace example.com

# Check all nameservers
dig example.com NS +short | while read ns; do
  echo "=== $ns ==="
  dig @$ns example.com A +short
done

# Reverse lookup
dig -x 93.184.216.34

# Check HTTPS certificate
curl -vI https://example.com 2>&1 | grep -A5 "Server certificate"
```

## Best Practices

### TTL Management

| Scenario | Recommended TTL |
|----------|-----------------|
| Stable records | 86400 (1 day) |
| Before migration | 300 (5 min) |
| During migration | 60 (1 min) |
| After migration | Gradually increase |

### Security Checklist

- [ ] Enable DNSSEC where supported
- [ ] Use CAA records to restrict CAs
- [ ] Monitor certificate transparency logs
- [ ] Enable registrar lock
- [ ] Use 2FA on registrar and DNS accounts
- [ ] Keep WHOIS contact info current
- [ ] Document all DNS changes

## Additional Resources

### Reference Files

- **`references/dns-providers.md`** - Provider-specific configurations
- **`references/email-dns.md`** - Complete email DNS setup guide

### Example Files

- **`examples/dns-migration-checklist.md`** - Migration playbook
- **`examples/cloudflare-config.json`** - Cloudflare API configuration
